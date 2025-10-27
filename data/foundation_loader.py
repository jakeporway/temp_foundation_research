#!/usr/bin/env python3
"""
Foundation Data Loader
Loads and processes foundation data from existing YAML files and foundation_cards.js
"""

import json
import yaml
import re
import os
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

class FoundationDataLoader:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.results_dir = self.base_dir / "results"
        self.foundations = []
        self.foundation_cards = []
        self.taxonomy_options = {}
        self._load_data()
    
    def _load_data(self):
        """Load all foundation data from existing files"""
        self._load_foundation_cards()
        self._load_yaml_data()
        self._build_taxonomy_options()
    
    def _load_foundation_cards(self):
        """Load foundation data from foundation_cards.js"""
        cards_file = self.base_dir / "foundation_cards.js"
        if not cards_file.exists():
            print(f"Warning: {cards_file} not found")
            return
        
        try:
            with open(cards_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract the JavaScript array
                match = re.search(r'const foundationCards = (\[.*?\]);', content, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    self.foundation_cards = json.loads(json_str)
                    print(f"Loaded {len(self.foundation_cards)} foundation cards")
        except Exception as e:
            print(f"Error loading foundation_cards.js: {e}")
    
    def _load_yaml_data(self):
        """Load complete YAML data for detailed views"""
        yaml_files = list(self.results_dir.glob("*_real_analysis.yaml"))
        self.yaml_data = {}
        successful_loads = 0
        failed_loads = 0
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'foundation_name' in data:
                        # Normalize foundation name for lookup
                        name_key = self._normalize_name(data['foundation_name'])
                        data['filename'] = yaml_file.name
                        self.yaml_data[name_key] = data
                        successful_loads += 1
                    else:
                        failed_loads += 1
                        print(f"Warning: {yaml_file.name} missing foundation_name or empty")
            except Exception as e:
                failed_loads += 1
                print(f"Warning: Could not parse {yaml_file.name} - {str(e)[:100]}...")
        
        print(f"Successfully loaded {successful_loads} YAML files ({failed_loads} failed due to parsing issues)")
    
    def _normalize_name(self, name: str) -> str:
        """Normalize foundation names for consistent lookup"""
        if not name:
            return ""
        # Convert to lowercase, remove special chars, replace spaces with underscores
        normalized = re.sub(r'[^\w\s]', '', name.lower())
        normalized = re.sub(r'\s+', '_', normalized.strip())
        return normalized
    
    def _build_taxonomy_options(self):
        """Build options for each taxonomy dimension from foundation cards"""
        if not self.foundation_cards:
            return
        
        # Define taxonomy fields with their display names - only include fields that exist in foundation cards
        taxonomy_fields = {
            # Foundation Identity
            'foundation_type': 'Foundation Type',
            
            # AI Strategy
            'ai_funding_integration': 'AI Funding Integration'
        }
        
        self.taxonomy_options = {}
        
        for field, display_name in taxonomy_fields.items():
            values = []
            for card in self.foundation_cards:
                value = card.get(field)
                if value and value not in ['Unknown', 'Not applicable', '']:
                    values.append(value)
            
            # Count occurrences and sort by frequency
            value_counts = Counter(values)
            sorted_values = sorted(value_counts.keys())
            
            self.taxonomy_options[field] = {
                'display_name': display_name,
                'options': sorted_values,
                'counts': dict(value_counts)
            }
        
        # Special handling for AI readiness score ranges
        readiness_scores = [card.get('ai_readiness_score', 0) for card in self.foundation_cards]
        readiness_ranges = {
            'High (8-10)': len([s for s in readiness_scores if s >= 8]),
            'Medium-High (6-7)': len([s for s in readiness_scores if 6 <= s < 8]),
            'Medium (4-5)': len([s for s in readiness_scores if 4 <= s < 6]),
            'Low (0-3)': len([s for s in readiness_scores if s < 4])
        }
        
        self.taxonomy_options['ai_readiness_range'] = {
            'display_name': 'AI Readiness Score',
            'options': list(readiness_ranges.keys()),
            'counts': readiness_ranges
        }
    
    def get_foundation_count(self) -> int:
        """Get total number of foundations"""
        return len(self.foundation_cards)
    
    def get_taxonomy_options(self) -> Dict:
        """Get all taxonomy options for building filters"""
        return self.taxonomy_options
    
    def get_foundation_by_name(self, name: str) -> Optional[Dict]:
        """Get detailed foundation data by name"""
        normalized_name = self._normalize_name(name)
        
        # Try to find in YAML data first (most complete)
        if normalized_name in self.yaml_data:
            yaml_data = self.yaml_data[normalized_name]
            # Enhance with card data
            card_data = self._find_card_by_name(name)
            if card_data:
                # Merge card and YAML data
                return {**card_data, **yaml_data, 'has_yaml': True}
            return {**yaml_data, 'has_yaml': True}
        
        # Fallback to card data only
        card_data = self._find_card_by_name(name)
        if card_data:
            return {**card_data, 'has_yaml': False}
        
        return None
    
    def _find_card_by_name(self, name: str) -> Optional[Dict]:
        """Find foundation card by name (flexible matching)"""
        normalized_search = self._normalize_name(name)
        
        for card in self.foundation_cards:
            card_name = card.get('name', '')
            if self._normalize_name(card_name) == normalized_search:
                return card
        
        return None
    
    def get_filtered_foundations(self, filters: Dict) -> List[Dict]:
        """Get foundations matching the provided filters"""
        results = self.foundation_cards.copy()
        
        # Apply search filter
        if 'search' in filters and filters['search']:
            search_term = filters['search'].lower()
            results = [f for f in results if self._matches_search(f, search_term)]
        
        # Apply AI readiness score range filter
        if 'ai_readiness_min' in filters or 'ai_readiness_max' in filters:
            min_score = filters.get('ai_readiness_min', 0)
            max_score = filters.get('ai_readiness_max', 10)
            results = [f for f in results if min_score <= f.get('ai_readiness_score', 0) <= max_score]
        
        # Apply AI readiness range filter
        if 'ai_readiness_range' in filters:
            range_values = filters['ai_readiness_range']
            if range_values:
                filtered_results = []
                for f in results:
                    score = f.get('ai_readiness_score', 0)
                    for range_val in range_values:
                        if self._score_in_range(score, range_val):
                            filtered_results.append(f)
                            break
                results = filtered_results
        
        # Apply taxonomy filters
        taxonomy_fields = [
            'foundation_type', 'geographic_focus', 'decision_making_structure',
            'grant_sourcing_strategy', 'endowment_size', 'funding_approach',
            'ai_funding_integration', 'ai_outcome', 'ai_related_output',
            'ai_product_lifecycle_stage', 'internal_ai_investment', 
            'innovation_focus', 'eo_focus_area'
        ]
        
        for field in taxonomy_fields:
            if field in filters and filters[field]:
                allowed_values = filters[field]
                results = [f for f in results if f.get(field) in allowed_values]
        
        return results
    
    def _matches_search(self, foundation: Dict, search_term: str) -> bool:
        """Check if foundation matches search term"""
        searchable_fields = [
            'name', 'location', 'readiness_level',
            'foundation_type', 'ai_funding_integration',
            'focus_areas'
        ]
        
        for field in searchable_fields:
            value = foundation.get(field, '')
            if isinstance(value, list):
                value = ' '.join(str(v) for v in value)
            if search_term in str(value).lower():
                return True
        
        return False
    
    def _score_in_range(self, score: int, range_name: str) -> bool:
        """Check if score falls within the named range"""
        if 'High (8-10)' in range_name:
            return score >= 8
        elif 'Medium-High (6-7)' in range_name:
            return 6 <= score < 8
        elif 'Medium (4-5)' in range_name:
            return 4 <= score < 6
        elif 'Low (0-3)' in range_name:
            return score < 4
        return False
    
    def get_filtered_statistics(self, foundations: List[Dict]) -> Dict:
        """Calculate statistics for filtered foundations"""
        if not foundations:
            return {}
        
        stats = {}
        
        # AI Readiness distribution
        readiness_scores = [f.get('ai_readiness_score', 0) for f in foundations]
        stats['ai_readiness'] = {
            'average': round(sum(readiness_scores) / len(readiness_scores), 1),
            'high_count': len([s for s in readiness_scores if s >= 8]),
            'medium_count': len([s for s in readiness_scores if 4 <= s < 8]),
            'low_count': len([s for s in readiness_scores if s < 4])
        }
        
        # Foundation type distribution
        foundation_types = [f.get('foundation_type', 'Unknown') for f in foundations]
        stats['foundation_types'] = dict(Counter(foundation_types))
        
        # AI integration distribution
        ai_integration = [f.get('ai_funding_integration', 'Unknown') for f in foundations]
        stats['ai_integration'] = dict(Counter(ai_integration))
        
        # Geographic distribution
        geographic_focus = [f.get('geographic_focus', 'Unknown') for f in foundations]
        stats['geographic'] = dict(Counter(geographic_focus))
        
        return stats
    
    def get_overall_statistics(self) -> Dict:
        """Get overall statistics for all foundations"""
        return self.get_filtered_statistics(self.foundation_cards)