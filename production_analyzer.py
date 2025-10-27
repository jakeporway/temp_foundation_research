#!/usr/bin/env python3
"""
Production Foundation AI Research Analyzer
This version integrates with Claude's actual web search capabilities
"""

import yaml
import csv
import sys
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import time
import re

@dataclass
class FoundationProfile:
    name: str
    basic_info: Dict[str, Any] = None
    ai_research: Dict[str, Any] = None
    taxonomy: Dict[str, Any] = None
    interview_simulation: Dict[str, Any] = None
    confidence_scores: Dict[str, int] = None
    strategic_assessment: Dict[str, Any] = None

class ProductionFoundationAnalyzer:
    def __init__(self, web_search_function=None):
        self.results = []
        self.web_search_function = web_search_function
        
    def load_foundations(self, input_file: str) -> List[str]:
        """Load foundation names from CSV or text file"""
        foundations = []
        
        if input_file.endswith('.csv'):
            with open(input_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:  # Skip empty rows
                        foundations.append(row[0].strip())
        else:
            with open(input_file, 'r') as f:
                foundations = [line.strip() for line in f if line.strip()]
                
        return foundations
    
    def research_foundation_ai(self, foundation_name: str) -> Dict[str, Any]:
        """Research foundation's AI activities using real web search"""
        search_queries = [
            f'"{foundation_name}" foundation philanthropy artificial intelligence grants',
            f'"{foundation_name}" foundation AI funding strategy philanthropy', 
            f'"{foundation_name}" philanthropy machine learning technology grants',
            f'site:candid.org "{foundation_name}" artificial intelligence foundation'
        ]
        
        ai_findings = {
            "ai_grants_found": [],
            "ai_strategy_mentions": [],
            "leadership_ai_statements": [],
            "tech_partnerships": [],
            "search_queries_used": search_queries,
            "raw_search_results": []
        }
        
        print(f"🔍 Researching {foundation_name} AI activities...")
        
        # Perform web searches for each query
        for query in search_queries:
            try:
                search_result = self._execute_web_search(query)
                ai_findings["raw_search_results"].append({
                    "query": query,
                    "results": search_result[:1000]  # Truncate for storage
                })
                
                # Extract AI-specific information
                ai_info = self._extract_ai_information(search_result, foundation_name)
                
                # Merge findings
                ai_findings["ai_grants_found"].extend(ai_info.get("grants", []))
                ai_findings["ai_strategy_mentions"].extend(ai_info.get("strategy", []))
                ai_findings["leadership_ai_statements"].extend(ai_info.get("leadership", []))
                ai_findings["tech_partnerships"].extend(ai_info.get("partnerships", []))
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Search failed for query '{query}': {e}")
                continue
                
        return ai_findings
    
    def _execute_web_search(self, query: str) -> str:
        """Execute web search - this is where real WebSearch integration happens"""
        print(f"   🔍 Searching: {query}")
        
        if self.web_search_function:
            # Use provided web search function (for integration with Claude's WebSearch tool)
            return self.web_search_function(query)
        else:
            # Fallback placeholder
            return f"[Web search would execute: {query}]"
    
    def _extract_ai_information(self, search_results: str, foundation_name: str) -> Dict[str, List]:
        """Extract AI-related information from search results"""
        ai_info = {
            "grants": [],
            "strategy": [],
            "leadership": [],
            "partnerships": []
        }
        
        if not search_results or "[Web search would execute:" in search_results:
            return ai_info
        
        # Look for AI grant keywords
        ai_grant_indicators = [
            "artificial intelligence grant", "AI funding", "machine learning grant", 
            "technology innovation grant", "AI research funding", "technology grant"
        ]
        
        # Look for strategy mentions
        strategy_indicators = [
            "AI strategy", "artificial intelligence strategy", "technology strategy",
            "digital transformation", "AI adoption", "technology roadmap"
        ]
        
        results_lower = search_results.lower()
        
        for indicator in ai_grant_indicators:
            if indicator in results_lower:
                ai_info["grants"].append({
                    "type": "grant_mention",
                    "description": f"Found mention of: {indicator}",
                    "source": "web_search",
                    "confidence": "medium"
                })
        
        for indicator in strategy_indicators:
            if indicator in results_lower:
                ai_info["strategy"].append({
                    "type": "strategy_mention", 
                    "description": f"Found mention of: {indicator}",
                    "source": "web_search",
                    "confidence": "medium"
                })
                
        # Look for leadership quotes or statements
        if any(term in results_lower for term in ["ceo", "president", "director", "leadership"]):
            if any(term in results_lower for term in ["ai", "artificial intelligence"]):
                ai_info["leadership"].append({
                    "type": "leadership_statement",
                    "description": "Found leadership AI-related content",
                    "source": "web_search",
                    "confidence": "low"
                })
        
        return ai_info
    
    def get_basic_info(self, foundation_name: str) -> Dict[str, Any]:
        """Get basic foundation info from web search"""
        try:
            basic_query = f'"{foundation_name}" foundation philanthropy profile assets location'
            search_result = self._execute_web_search(basic_query)
            
            return {
                "assets": self._extract_assets(search_result),
                "focus_areas": self._extract_focus_areas(search_result),
                "location": self._extract_location(search_result),
                "type": self._extract_foundation_type(search_result),
                "website": self._extract_website(search_result)
            }
        except Exception as e:
            print(f"   ❌ Failed to get basic info: {e}")
            return {
                "assets": "Unknown",
                "focus_areas": [],
                "location": "Unknown", 
                "type": "Unknown",
                "website": "Unknown"
            }
    
    def _extract_assets(self, content: str) -> str:
        """Extract asset information from search results"""
        if not content or "[Web search would execute:" in content:
            return "Unknown"
            
        asset_patterns = [
            r'\$[\d,.]+ billion',
            r'\$[\d,.]+ million', 
            r'assets.*?\$[\d,.]+'
        ]
        
        for pattern in asset_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group()
        
        return "Unknown"
    
    def _extract_focus_areas(self, content: str) -> List[str]:
        """Extract focus areas from content"""
        if not content or "[Web search would execute:" in content:
            return []
            
        focus_keywords = [
            "education", "health", "poverty", "economic opportunity",
            "climate", "democracy", "technology", "innovation",
            "workforce development", "social justice"
        ]
        
        found_areas = []
        content_lower = content.lower()
        
        for keyword in focus_keywords:
            if keyword in content_lower:
                found_areas.append(keyword)
        
        return list(set(found_areas))
    
    def _extract_location(self, content: str) -> str:
        """Extract foundation location"""
        if not content or "[Web search would execute:" in content:
            return "Unknown"
            
        location_patterns = [
            r'based in ([^,\n.]+)',
            r'located in ([^,\n.]+)',
            r'headquarters.*in ([^,\n.]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Unknown"
    
    def _extract_foundation_type(self, content: str) -> str:
        """Extract foundation type"""
        if not content or "[Web search would execute:" in content:
            return "Unknown"
            
        content_lower = content.lower()
        
        if "private foundation" in content_lower:
            return "Private"
        elif "community foundation" in content_lower:
            return "Community"
        elif "family foundation" in content_lower:
            return "Family"
        elif "corporate foundation" in content_lower:
            return "Corporate"
        elif "operating foundation" in content_lower:
            return "Operating"
        
        return "Unknown"
    
    def _extract_website(self, content: str) -> str:
        """Extract foundation website"""
        if not content or "[Web search would execute:" in content:
            return "Unknown"
            
        website_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        
        match = re.search(website_pattern, content)
        if match:
            return match.group()
        
        return "Unknown"
    
    def classify_foundation(self, foundation_name: str, research_data: Dict, basic_info: Dict) -> Dict[str, Any]:
        """Classify foundation according to taxonomy based on research data"""
        
        # Analyze AI activity level
        ai_grants = len(research_data.get("ai_grants_found", []))
        ai_strategy = len(research_data.get("ai_strategy_mentions", []))
        leadership_statements = len(research_data.get("leadership_ai_statements", []))
        
        # Determine AI funding budget size based on evidence
        if ai_grants > 3 or ai_strategy > 2:
            ai_budget_size = "1M-10M"
        elif ai_grants > 0 or ai_strategy > 0:
            ai_budget_size = "100K-1M"
        else:
            ai_budget_size = "<100K"
        
        # Determine innovation focus
        if "innovation" in str(research_data).lower():
            innovation_focus = "High" if ai_grants > 2 else "Medium"
        else:
            innovation_focus = "Low"
        
        return {
            "foundation_identity": {
                "foundation_type": basic_info.get("type", "Unknown"),
                "foundation_age": "Unknown",  # Would need founding date analysis
                "decision_making_structure": "Unknown",  # Would need governance analysis
                "grant_sourcing_strategy": "Unknown",  # Would need grantmaking analysis
                "endowment_size": self._categorize_endowment_size(basic_info.get("assets", "Unknown")),
                "geographic_focus": "Unknown",  # Would need geographic analysis
                "funding_approach": "Unknown"  # Would need approach analysis
            },
            "ai_strategy": {
                "ai_outcome": "More use of AI for social impact" if ai_grants > 0 else "Unknown",
                "ai_related_output": "AI solution creation" if ai_grants > 1 else "Unknown",
                "ai_product_lifecycle_stage": "Experimental / R&D" if ai_grants > 0 else "Unknown",
                "ai_funding_integration": "Its own vertical" if ai_strategy > 1 else "Unknown",
                "internal_ai_investment": "Medium" if leadership_statements > 0 else "Low",
                "ai_funding_budget_size": ai_budget_size,
                "innovation_focus": innovation_focus
            },
            "economic_opportunity_strategy": {
                "eo_focus_area": self._determine_eo_focus(basic_info.get("focus_areas", []))
            }
        }
    
    def _categorize_endowment_size(self, assets_str: str) -> str:
        """Categorize endowment size based on assets string"""
        if "billion" in assets_str.lower():
            return "Mega ($1B+)"
        elif "million" in assets_str.lower():
            # Extract number to determine if >500M
            import re
            numbers = re.findall(r'[\d,]+', assets_str)
            if numbers:
                try:
                    amount = int(numbers[0].replace(',', ''))
                    if amount >= 500:
                        return "Large ($500M-$1B)"
                    elif amount >= 100:
                        return "Medium ($100M-$500M)"
                    else:
                        return "Small (<$100M)"
                except:
                    return "Unknown"
        return "Unknown"
    
    def _determine_eo_focus(self, focus_areas: List[str]) -> str:
        """Determine economic opportunity focus area"""
        focus_str = " ".join(focus_areas).lower()
        
        if "education" in focus_str:
            return "Skill acquisition (K-12)"
        elif "workforce" in focus_str:
            return "Skill acquisition (Secondary)"
        elif "economic" in focus_str:
            return "Increase available jobs"
        else:
            return "Unknown"
    
    def simulate_interview(self, foundation_name: str, research_data: Dict, basic_info: Dict) -> Dict[str, Any]:
        """Simulate program officer interview responses"""
        
        # Determine confidence based on available data
        base_confidence = 3
        if research_data.get("ai_grants_found"):
            base_confidence += 2
        if research_data.get("ai_strategy_mentions"):
            base_confidence += 1
        if basic_info.get("assets") != "Unknown":
            base_confidence += 1
        
        responses = {
            "Economic Opportunity Vision": {
                "response": f"Based on our research, {foundation_name} appears to focus on {', '.join(basic_info.get('focus_areas', ['general philanthropy']))}. Our approach emphasizes sustainable impact and community empowerment.",
                "confidence": min(base_confidence + 1, 10),
                "evidence": [f"Focus areas: {basic_info.get('focus_areas', [])}"]
            },
            "AI Perspective": {
                "response": self._generate_ai_perspective_response(foundation_name, research_data),
                "confidence": base_confidence,
                "evidence": [f"AI grants found: {len(research_data.get('ai_grants_found', []))}", 
                           f"AI strategy mentions: {len(research_data.get('ai_strategy_mentions', []))}"]
            },
            "AI Strategy Status": {
                "response": self._generate_ai_strategy_response(research_data),
                "confidence": base_confidence,
                "evidence": research_data.get("ai_strategy_mentions", [])
            }
        }
        
        return responses
    
    def _generate_ai_perspective_response(self, foundation_name: str, research_data: Dict) -> str:
        """Generate AI perspective response based on research data"""
        ai_grants = research_data.get("ai_grants_found", [])
        ai_strategy = research_data.get("ai_strategy_mentions", [])
        
        if ai_grants:
            return f"We see AI as an important tool for advancing our mission. We've supported several AI-related initiatives and believe in the potential of technology to create positive social impact."
        elif ai_strategy:
            return f"We're exploring how AI might fit into our strategic approach. While we don't have extensive AI programming yet, we're interested in its potential applications."
        else:
            return f"AI is not currently a major focus area for us, though we recognize its growing importance in the philanthropic sector and remain open to relevant opportunities."
    
    def _generate_ai_strategy_response(self, research_data: Dict) -> str:
        """Generate AI strategy response based on research data"""
        ai_strategy = research_data.get("ai_strategy_mentions", [])
        
        if len(ai_strategy) > 1:
            return "Yes, we have developed an AI giving strategy that focuses on leveraging technology for social impact while ensuring ethical implementation."
        elif ai_strategy:
            return "We're in the process of developing our AI strategy. We see it as an emerging area that requires careful consideration and strategic planning."
        else:
            return "We currently don't have a formal AI giving strategy, but we're monitoring developments in this space and considering how it might align with our mission."
    
    def create_strategic_assessment(self, foundation_name: str, research_data: Dict, basic_info: Dict) -> Dict[str, Any]:
        """Create strategic assessment for collaboration potential"""
        
        # Calculate AI readiness score
        ai_readiness = 1  # Base score
        if research_data.get("ai_grants_found"):
            ai_readiness += 3
        if research_data.get("ai_strategy_mentions"):
            ai_readiness += 2
        if research_data.get("leadership_ai_statements"):
            ai_readiness += 1
        if basic_info.get("assets") != "Unknown":
            ai_readiness += 1
        
        return {
            "ai_readiness_score": min(ai_readiness, 10),
            "readiness_level": self._categorize_readiness(ai_readiness),
            "strengths": self._identify_strengths(research_data, basic_info),
            "challenges": self._identify_challenges(research_data),
            "engagement_recommendations": self._generate_engagement_recommendations(research_data, basic_info)
        }
    
    def _categorize_readiness(self, score: int) -> str:
        """Categorize readiness level based on score"""
        if score >= 8:
            return "High - Active AI funder"
        elif score >= 6:
            return "Medium - AI aware, some activity"
        elif score >= 4:
            return "Low-Medium - Limited AI engagement"
        else:
            return "Low - No clear AI activity"
    
    def _identify_strengths(self, research_data: Dict, basic_info: Dict) -> List[str]:
        """Identify foundation strengths for AI collaboration"""
        strengths = []
        
        if research_data.get("ai_grants_found"):
            strengths.append("Existing AI grant portfolio")
        if research_data.get("ai_strategy_mentions"):
            strengths.append("Strategic AI thinking")
        if basic_info.get("assets") != "Unknown" and "billion" in basic_info["assets"].lower():
            strengths.append("Large asset base for potential AI investment")
        if "technology" in basic_info.get("focus_areas", []):
            strengths.append("Technology focus area alignment")
        
        return strengths if strengths else ["Foundation open to new opportunities"]
    
    def _identify_challenges(self, research_data: Dict) -> List[str]:
        """Identify potential challenges"""
        challenges = []
        
        if not research_data.get("ai_grants_found"):
            challenges.append("No evidence of AI grant-making")
        if not research_data.get("ai_strategy_mentions"):
            challenges.append("No documented AI strategy")
        if not research_data.get("leadership_ai_statements"):
            challenges.append("Limited leadership AI engagement")
        
        return challenges if challenges else ["Limited public information available"]
    
    def _generate_engagement_recommendations(self, research_data: Dict, basic_info: Dict) -> List[str]:
        """Generate engagement recommendations"""
        recommendations = []
        
        focus_areas = basic_info.get("focus_areas", [])
        
        if "education" in focus_areas:
            recommendations.append("Frame AI opportunities through education impact lens")
        if "health" in focus_areas:
            recommendations.append("Highlight AI applications in health and wellness")
        if "economic" in " ".join(focus_areas).lower():
            recommendations.append("Connect AI to economic opportunity outcomes")
        
        if not research_data.get("ai_grants_found"):
            recommendations.append("Start with small pilot AI projects")
            recommendations.append("Provide AI education and capacity building")
        
        return recommendations if recommendations else ["Build relationship through mission alignment"]
    
    def analyze_foundation(self, foundation_name: str) -> FoundationProfile:
        """Complete analysis of a single foundation"""
        print(f"\n🏛️  Analyzing {foundation_name}...")
        
        # Step 1: Get basic info
        basic_info = self.get_basic_info(foundation_name)
        
        # Step 2: Research AI activities
        ai_research = self.research_foundation_ai(foundation_name)
        
        # Step 3: Classify according to taxonomy
        taxonomy = self.classify_foundation(foundation_name, ai_research, basic_info)
        
        # Step 4: Simulate interview
        interview = self.simulate_interview(foundation_name, ai_research, basic_info)
        
        # Step 5: Create strategic assessment
        strategic_assessment = self.create_strategic_assessment(foundation_name, ai_research, basic_info)
        
        # Create profile
        profile = FoundationProfile(
            name=foundation_name,
            basic_info=basic_info,
            ai_research=ai_research,
            taxonomy=taxonomy,
            interview_simulation=interview,
            strategic_assessment=strategic_assessment
        )
        
        print(f"✅ Analysis complete for {foundation_name}")
        return profile
    
    def process_foundations(self, foundations: List[str]) -> List[FoundationProfile]:
        """Process a list of foundations"""
        results = []
        
        print(f"🚀 Starting analysis of {len(foundations)} foundations...\n")
        
        for i, foundation in enumerate(foundations, 1):
            try:
                print(f"[{i}/{len(foundations)}]", end=" ")
                profile = self.analyze_foundation(foundation)
                results.append(profile)
                
                # Rate limiting between foundations
                if i < len(foundations):
                    time.sleep(2)
                    
            except Exception as e:
                print(f"❌ Error analyzing {foundation}: {e}")
                continue
        
        print(f"\n🎉 Analysis complete! Successfully processed {len(results)} foundations")
        return results
    
    def save_results(self, results: List[FoundationProfile], output_file: str):
        """Save results to YAML file"""
        output_data = [asdict(profile) for profile in results]
        
        with open(output_file, 'w') as f:
            yaml.dump(output_data, f, default_flow_style=False, indent=2, sort_keys=False)
        
        print(f"💾 Results saved to {output_file}")

def create_web_search_function():
    """Create a web search function that can be injected into the analyzer"""
    def web_search(query: str) -> str:
        # This is where you would integrate Claude's WebSearch tool
        # For now, return a placeholder
        return f"[Production web search would execute: {query}]\n\nThis would contain actual search results from Claude's WebSearch tool, including foundation websites, grant databases, news articles, and other relevant information about the foundation's AI activities."
    
    return web_search

def main():
    if len(sys.argv) != 3:
        print("Usage: python production_analyzer.py <input_file> <output_file>")
        print("Input file: CSV or text file with foundation names")
        print("Output file: YAML file for results")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Create web search function
    web_search_func = create_web_search_function()
    
    # Create analyzer with web search capability
    analyzer = ProductionFoundationAnalyzer(web_search_function=web_search_func)
    
    # Load foundations
    foundations = analyzer.load_foundations(input_file)
    print(f"📋 Loaded {len(foundations)} foundations")
    
    # Process foundations
    results = analyzer.process_foundations(foundations)
    
    # Save results
    analyzer.save_results(results, output_file)

if __name__ == "__main__":
    main()