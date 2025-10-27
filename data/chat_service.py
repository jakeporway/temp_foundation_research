#!/usr/bin/env python3
"""
Foundation Chat Service
Implements map-reduce pattern for semantic queries against foundation YAML database
"""

import os
import json
import yaml
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import anthropic

@dataclass
class BatchResult:
    batch_id: int
    query: str
    relevant_foundations: List[Dict[str, Any]]
    reasoning: str

class FoundationChatService:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # Load environment variables from .env file
        load_dotenv()
        
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Please add it to your .env file")
        
        # Set model (with fallback to default)
        self.model = model or os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.base_dir = Path(__file__).parent.parent
        self.results_dir = self.base_dir / "results"
        self.batch_size = 20  # Larger batches = fewer API calls = faster processing
        
        # Load successful YAML files
        self.yaml_files = self._load_yaml_files()
        print(f"Loaded {len(self.yaml_files)} YAML files for chat analysis")
        print(f"Using Anthropic model: {self.model}")
    
    def _load_yaml_files(self) -> List[Dict[str, Any]]:
        """Load all successfully parsing YAML files"""
        yaml_files = list(self.results_dir.glob("*_real_analysis.yaml"))
        loaded_files = []
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'foundation_name' in data:
                        data['filename'] = yaml_file.name
                        loaded_files.append(data)
            except Exception as e:
                continue  # Skip files that can't be parsed
        
        return loaded_files
    
    def _create_batches(self) -> List[List[Dict[str, Any]]]:
        """Split YAML files into batches for processing"""
        batches = []
        for i in range(0, len(self.yaml_files), self.batch_size):
            batch = self.yaml_files[i:i + self.batch_size]
            batches.append(batch)
        return batches
    
    def _create_map_prompt(self, query: str, batch: List[Dict[str, Any]]) -> str:
        """Create prompt for map phase - analyze batch for relevant foundations"""
        foundation_summaries = []
        
        for foundation in batch:
            # Create concise summary of each foundation for the prompt
            summary = {
                'name': foundation.get('foundation_name', 'Unknown'),
                'type': foundation.get('basic_info', {}).get('foundation_type', 'Unknown'),
                'focus_areas': foundation.get('basic_info', {}).get('focus_areas', []),
                'assets': foundation.get('basic_info', {}).get('assets', 'Unknown'),
                'ai_grants': len(foundation.get('ai_research_findings', {}).get('ai_grants_discovered', [])),
                'ai_strategy': foundation.get('ai_research_findings', {}).get('ai_strategy_evidence', []),
                'location': foundation.get('basic_info', {}).get('location', 'Unknown'),
                'annual_giving': foundation.get('basic_info', {}).get('annual_giving', 'Unknown'),
            }
            foundation_summaries.append(summary)
        
        prompt = f"""You are analyzing a batch of foundations to find matches for this user query: "{query}"

Here are {len(foundation_summaries)} foundations in this batch:

{json.dumps(foundation_summaries, indent=2)}

Please analyze each foundation and identify which ones are most relevant to the user's query. Consider:
- Their focus areas and mission alignment
- Their AI grant activities and strategy evidence
- Their foundation type, size, and capacity
- Geographic considerations if relevant
- Any specific programs or initiatives mentioned

Return your response as a JSON object with this structure:
{{
    "relevant_foundations": [
        {{
            "name": "Foundation Name",
            "relevance_score": 0.9,
            "reasoning": "Specific reason why this foundation matches the query"
        }}
    ],
    "batch_summary": "Brief summary of findings from this batch"
}}

Only include foundations with relevance_score >= 0.6. Be selective - it's better to miss some matches than include false positives."""

        return prompt
    
    def _create_reduce_prompt(self, query: str, batch_results: List[BatchResult]) -> str:
        """Create prompt for reduce phase - consolidate and rank results"""
        all_results = []
        for result in batch_results:
            all_results.extend(result.relevant_foundations)
        
        prompt = f"""You are consolidating results from multiple batches of foundation analysis for this user query: "{query}"

Here are all the relevant foundations found across {len(batch_results)} batches:

{json.dumps(all_results, indent=2)}

Please:
1. Remove any duplicates
2. Rank the foundations by overall relevance to the query
3. Provide a clear, natural language response that directly answers the user's question
4. Include specific details about why these foundations match
5. Limit to the top 8-10 most relevant foundations

Format your response as:
{{
    "answer": "Natural language response directly answering the user's question",
    "top_foundations": [
        {{
            "name": "Foundation Name",
            "final_score": 0.95,
            "key_reasons": ["reason 1", "reason 2", "reason 3"],
            "specific_programs": ["program 1", "program 2"]
        }}
    ],
    "query_insights": "Additional insights about the landscape for this type of query"
}}"""

        return prompt
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a natural language query using map-reduce approach"""
        try:
            # Create batches
            batches = self._create_batches()
            print(f"Processing query across {len(batches)} batches...")
            
            # Map phase - process each batch
            batch_results = []
            for i, batch in enumerate(batches):
                print(f"Processing batch {i+1}/{len(batches)}...")
                
                map_prompt = self._create_map_prompt(query, batch)
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    messages=[{
                        "role": "user",
                        "content": map_prompt
                    }]
                )
                
                try:
                    # Parse Claude's JSON response
                    result_json = json.loads(response.content[0].text)
                    batch_result = BatchResult(
                        batch_id=i,
                        query=query,
                        relevant_foundations=result_json.get('relevant_foundations', []),
                        reasoning=result_json.get('batch_summary', '')
                    )
                    batch_results.append(batch_result)
                    
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse JSON from batch {i+1}")
                    continue
            
            # Reduce phase - consolidate results
            print("Consolidating results...")
            reduce_prompt = self._create_reduce_prompt(query, batch_results)
            
            final_response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{
                    "role": "user", 
                    "content": reduce_prompt
                }]
            )
            
            try:
                final_result = json.loads(final_response.content[0].text)
                final_result['processing_stats'] = {
                    'total_foundations_analyzed': len(self.yaml_files),
                    'batches_processed': len(batch_results),
                    'batch_size': self.batch_size
                }
                return final_result
                
            except json.JSONDecodeError:
                return {
                    "error": "Could not parse final response",
                    "raw_response": final_response.content[0].text
                }
                
        except Exception as e:
            return {
                "error": f"Error processing query: {str(e)}"
            }
    
    def get_available_foundations(self) -> List[str]:
        """Get list of available foundation names for reference"""
        return [f.get('foundation_name', 'Unknown') for f in self.yaml_files]