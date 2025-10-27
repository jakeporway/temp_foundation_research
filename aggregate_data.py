#!/usr/bin/env python3
"""
Foundation Data Aggregation Script
Parses all YAML files and generates aggregate statistics for dashboard
"""

import os
import yaml
import json
from collections import defaultdict, Counter
from pathlib import Path
from datetime import date, datetime
from taxonomy_standardization import get_taxonomy_standardization_mapping

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

class FoundationDataAggregator:
    def __init__(self, results_dir="results"):
        self.results_dir = Path(results_dir)
        self.foundations = []
        self.stats = {}
        self.standardization_mapping = get_taxonomy_standardization_mapping()
        
    def load_all_foundations(self):
        """Load all YAML files from results directory"""
        yaml_files = list(self.results_dir.glob("*_real_analysis.yaml"))
        print(f"Found {len(yaml_files)} YAML files")
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        # Add filename for reference
                        data['filename'] = yaml_file.name
                        self.foundations.append(data)
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
                continue
        
        print(f"Successfully loaded {len(self.foundations)} foundations")
        return self.foundations
    
    def safe_get(self, data, path, default="Unknown"):
        """Safely get nested dictionary value"""
        try:
            keys = path.split('.')
            for key in keys:
                data = data[key]
            return data if data is not None else default
        except (KeyError, TypeError):
            return default
    
    def standardize_value(self, dimension, value):
        """Apply standardization mapping to taxonomy values"""
        if dimension in self.standardization_mapping:
            return self.standardization_mapping[dimension].get(value, value)
        return value
    
    def categorize_ai_readiness(self, score):
        """Categorize AI readiness score into ranges"""
        if score == "N/A" or score is None:
            return "N/A"
        try:
            score_num = float(score)
            if score_num <= 2:
                return "Low (0-2)"
            elif score_num <= 4:
                return "Medium-Low (3-4)"
            elif score_num <= 6:
                return "Medium (5-6)"
            elif score_num <= 8:
                return "Medium-High (7-8)"
            else:
                return "High (9-10)"
        except (ValueError, TypeError):
            return "Unknown"
    
    def categorize_assets(self, assets_text):
        """Categorize asset information into ranges"""
        if not assets_text or assets_text.lower() in ["unknown", "n/a"]:
            return "Unknown"
        
        assets_lower = str(assets_text).lower()
        
        # Look for billion indicators
        if "billion" in assets_lower or "$" in assets_lower and "b" in assets_lower:
            try:
                # Extract number
                import re
                numbers = re.findall(r'[\d.]+', assets_lower)
                if numbers and float(numbers[0]) >= 1:
                    return "Very Large ($1B+)"
            except:
                pass
            return "Very Large ($1B+)"
        
        # Look for million indicators
        if "million" in assets_lower or "$" in assets_lower and "m" in assets_lower:
            try:
                import re
                numbers = re.findall(r'[\d.]+', assets_lower)
                if numbers:
                    amount = float(numbers[0])
                    if amount >= 500:
                        return "Large ($500M+)"
                    elif amount >= 100:
                        return "Medium ($100-500M)"
                    else:
                        return "Small (<$100M)"
            except:
                pass
            return "Medium ($100-500M)"
        
        return "Unknown"
    
    def categorize_annual_giving(self, giving_text):
        """Categorize annual giving into ranges"""
        if not giving_text or str(giving_text).lower() in ["unknown", "n/a"]:
            return "Unknown"
        
        giving_lower = str(giving_text).lower()
        
        if "billion" in giving_lower:
            return "Very Large ($1B+)"
        elif "million" in giving_lower:
            try:
                import re
                numbers = re.findall(r'[\d.]+', giving_lower)
                if numbers:
                    amount = float(numbers[0])
                    if amount >= 100:
                        return "Large ($100M+)"
                    elif amount >= 25:
                        return "Medium ($25-100M)"
                    else:
                        return "Small (<$25M)"
            except:
                pass
            return "Medium ($25-100M)"
        
        return "Unknown"
    
    def aggregate_statistics(self):
        """Generate aggregate statistics for all taxonomy dimensions"""
        stats = {}
        
        # Foundation Identity dimensions
        foundation_identity_stats = {}
        
        # Foundation Type
        foundation_types = [self.standardize_value('foundation_type', self.safe_get(f, 'taxonomy_classification.foundation_identity.foundation_type')) for f in self.foundations]
        foundation_identity_stats['foundation_type'] = dict(Counter(foundation_types))
        
        # Foundation Age
        foundation_ages = [self.safe_get(f, 'taxonomy_classification.foundation_identity.foundation_age') for f in self.foundations]
        foundation_identity_stats['foundation_age'] = dict(Counter(foundation_ages))
        
        # Decision Making Structure
        decision_structures = [self.standardize_value('decision_making_structure', self.safe_get(f, 'taxonomy_classification.foundation_identity.decision_making_structure')) for f in self.foundations]
        foundation_identity_stats['decision_making_structure'] = dict(Counter(decision_structures))
        
        # Grant Sourcing Strategy
        grant_strategies = [self.standardize_value('grant_sourcing_strategy', self.safe_get(f, 'taxonomy_classification.foundation_identity.grant_sourcing_strategy')) for f in self.foundations]
        foundation_identity_stats['grant_sourcing_strategy'] = dict(Counter(grant_strategies))
        
        # Endowment Size
        endowment_sizes = [self.standardize_value('endowment_size', self.safe_get(f, 'taxonomy_classification.foundation_identity.endowment_size')) for f in self.foundations]
        foundation_identity_stats['endowment_size'] = dict(Counter(endowment_sizes))
        
        # Geographic Focus
        geographic_focuses = [self.standardize_value('geographic_focus', self.safe_get(f, 'taxonomy_classification.foundation_identity.geographic_focus')) for f in self.foundations]
        foundation_identity_stats['geographic_focus'] = dict(Counter(geographic_focuses))
        
        # Funding Approach
        funding_approaches = [self.safe_get(f, 'taxonomy_classification.foundation_identity.funding_approach') for f in self.foundations]
        foundation_identity_stats['funding_approach'] = dict(Counter(funding_approaches))
        
        stats['foundation_identity'] = foundation_identity_stats
        
        # AI Strategy dimensions
        ai_strategy_stats = {}
        
        # AI Funding Integration
        ai_integrations = [self.standardize_value('ai_funding_integration', self.safe_get(f, 'taxonomy_classification.ai_strategy.ai_funding_integration')) for f in self.foundations]
        ai_strategy_stats['ai_funding_integration'] = dict(Counter(ai_integrations))
        
        # AI Readiness Score (categorized)
        ai_readiness_scores = [self.categorize_ai_readiness(self.safe_get(f, 'strategic_assessment.ai_readiness_score')) for f in self.foundations]
        ai_strategy_stats['ai_readiness_score'] = dict(Counter(ai_readiness_scores))
        
        # Internal AI Investment
        ai_investments = [self.safe_get(f, 'taxonomy_classification.ai_strategy.internal_ai_investment') for f in self.foundations]
        ai_strategy_stats['internal_ai_investment'] = dict(Counter(ai_investments))
        
        # Innovation Focus
        innovation_focuses = [self.safe_get(f, 'taxonomy_classification.ai_strategy.innovation_focus') for f in self.foundations]
        ai_strategy_stats['innovation_focus'] = dict(Counter(innovation_focuses))
        
        # AI Budget Size
        ai_budgets = [self.safe_get(f, 'taxonomy_classification.ai_strategy.ai_funding_budget_size') for f in self.foundations]
        ai_strategy_stats['ai_funding_budget_size'] = dict(Counter(ai_budgets))
        
        stats['ai_strategy'] = ai_strategy_stats
        
        # Economic Opportunity Strategy
        eo_strategy_stats = {}
        eo_focuses = [self.safe_get(f, 'taxonomy_classification.economic_opportunity_strategy.eo_focus_area') for f in self.foundations]
        eo_strategy_stats['eo_focus_area'] = dict(Counter(eo_focuses))
        
        stats['economic_opportunity_strategy'] = eo_strategy_stats
        
        # Additional useful breakdowns
        additional_stats = {}
        
        # Assets categorized
        assets_categories = [self.categorize_assets(self.safe_get(f, 'basic_info.assets')) for f in self.foundations]
        additional_stats['assets_category'] = dict(Counter(assets_categories))
        
        # Annual giving categorized
        giving_categories = [self.categorize_annual_giving(self.safe_get(f, 'basic_info.annual_giving')) for f in self.foundations]
        additional_stats['annual_giving_category'] = dict(Counter(giving_categories))
        
        # Location by state/country
        locations = [self.safe_get(f, 'basic_info.location') for f in self.foundations]
        # Extract state/country from location strings
        location_summary = {}
        for loc in locations:
            if loc and loc != "Unknown":
                # Simple extraction - look for state patterns
                if ", " in loc:
                    parts = loc.split(", ")
                    if len(parts) >= 2:
                        state_country = parts[-1].strip()
                        location_summary[state_country] = location_summary.get(state_country, 0) + 1
                else:
                    location_summary[loc] = location_summary.get(loc, 0) + 1
        
        additional_stats['location_breakdown'] = location_summary
        
        stats['additional'] = additional_stats
        
        self.stats = stats
        return stats
    
    def calculate_percentages(self, stats_dict, total_foundations):
        """Add percentage calculations to statistics"""
        result = {}
        for category, counts in stats_dict.items():
            result[category] = {}
            for value, count in counts.items():
                result[category][value] = {
                    'count': count,
                    'percentage': round((count / total_foundations) * 100, 1)
                }
        return result
    
    def create_foundation_lookup(self):
        """Create lookup for filtering foundations by taxonomy values"""
        lookup = defaultdict(lambda: defaultdict(list))
        
        for foundation in self.foundations:
            # Foundation identity lookups  
            foundation_type = self.standardize_value('foundation_type', self.safe_get(foundation, 'taxonomy_classification.foundation_identity.foundation_type'))
            lookup['foundation_type'][foundation_type].append(foundation)
            
            foundation_age = self.safe_get(foundation, 'taxonomy_classification.foundation_identity.foundation_age')
            lookup['foundation_age'][foundation_age].append(foundation)
            
            decision_structure = self.standardize_value('decision_making_structure', self.safe_get(foundation, 'taxonomy_classification.foundation_identity.decision_making_structure'))
            lookup['decision_making_structure'][decision_structure].append(foundation)
            
            grant_strategy = self.standardize_value('grant_sourcing_strategy', self.safe_get(foundation, 'taxonomy_classification.foundation_identity.grant_sourcing_strategy'))
            lookup['grant_sourcing_strategy'][grant_strategy].append(foundation)
            
            endowment_size = self.standardize_value('endowment_size', self.safe_get(foundation, 'taxonomy_classification.foundation_identity.endowment_size'))
            lookup['endowment_size'][endowment_size].append(foundation)
            
            geographic_focus = self.standardize_value('geographic_focus', self.safe_get(foundation, 'taxonomy_classification.foundation_identity.geographic_focus'))
            lookup['geographic_focus'][geographic_focus].append(foundation)
            
            funding_approach = self.safe_get(foundation, 'taxonomy_classification.foundation_identity.funding_approach')
            lookup['funding_approach'][funding_approach].append(foundation)
            
            # AI strategy lookups
            ai_integration = self.standardize_value('ai_funding_integration', self.safe_get(foundation, 'taxonomy_classification.ai_strategy.ai_funding_integration'))
            lookup['ai_funding_integration'][ai_integration].append(foundation)
            
            ai_readiness = self.categorize_ai_readiness(self.safe_get(foundation, 'strategic_assessment.ai_readiness_score'))
            lookup['ai_readiness_score'][ai_readiness].append(foundation)
            
            ai_investment = self.safe_get(foundation, 'taxonomy_classification.ai_strategy.internal_ai_investment')
            lookup['internal_ai_investment'][ai_investment].append(foundation)
            
            innovation_focus = self.safe_get(foundation, 'taxonomy_classification.ai_strategy.innovation_focus')
            lookup['innovation_focus'][innovation_focus].append(foundation)
            
            ai_budget = self.safe_get(foundation, 'taxonomy_classification.ai_strategy.ai_funding_budget_size')
            lookup['ai_funding_budget_size'][ai_budget].append(foundation)
            
            # Economic opportunity lookup
            eo_focus = self.safe_get(foundation, 'taxonomy_classification.economic_opportunity_strategy.eo_focus_area')
            lookup['eo_focus_area'][eo_focus].append(foundation)
            
            # Additional lookups
            assets_category = self.categorize_assets(self.safe_get(foundation, 'basic_info.assets'))
            lookup['assets_category'][assets_category].append(foundation)
            
            giving_category = self.categorize_annual_giving(self.safe_get(foundation, 'basic_info.annual_giving'))
            lookup['annual_giving_category'][giving_category].append(foundation)
        
        return dict(lookup)
    
    def generate_dashboard_data(self):
        """Generate complete dashboard data structure"""
        print("Loading foundations...")
        self.load_all_foundations()
        
        print("Calculating statistics...")
        raw_stats = self.aggregate_statistics()
        
        print("Adding percentages...")
        total_foundations = len(self.foundations)
        stats_with_percentages = {}
        
        for section, section_stats in raw_stats.items():
            stats_with_percentages[section] = self.calculate_percentages(section_stats, total_foundations)
        
        print("Creating foundation lookup...")
        foundation_lookup = self.create_foundation_lookup()
        
        # Create simplified foundation data for cards
        foundation_cards = []
        for f in self.foundations:
            card = {
                'name': f.get('foundation_name', 'Unknown'),
                'filename': f.get('filename', ''),
                'ai_readiness_score': f.get('strategic_assessment', {}).get('ai_readiness_score', 'N/A'),
                'readiness_level': f.get('strategic_assessment', {}).get('readiness_level', 'Unknown'),
                'foundation_type': self.standardize_value('foundation_type', self.safe_get(f, 'taxonomy_classification.foundation_identity.foundation_type')),
                'foundation_type_raw': self.safe_get(f, 'taxonomy_classification.foundation_identity.foundation_type'),
                'assets': f.get('basic_info', {}).get('assets', 'Unknown'),
                'annual_giving': f.get('basic_info', {}).get('annual_giving', 'Unknown'),
                'location': f.get('basic_info', {}).get('location', 'Unknown'),
                'website': f.get('basic_info', {}).get('website', ''),
                'focus_areas': f.get('basic_info', {}).get('focus_areas', []),
                'ai_grants_count': len(f.get('ai_research_findings', {}).get('ai_grants_discovered', [])),
                'ai_grant_urls': f.get('ai_research_findings', {}).get('ai_grant_urls', []),
                'ai_funding_integration': self.standardize_value('ai_funding_integration', self.safe_get(f, 'taxonomy_classification.ai_strategy.ai_funding_integration')),
                'ai_funding_integration_raw': self.safe_get(f, 'taxonomy_classification.ai_strategy.ai_funding_integration')
            }
            foundation_cards.append(card)
        
        dashboard_data = {
            'metadata': {
                'total_foundations': total_foundations,
                'generated_at': "2025-01-28",
                'source': 'Foundation Research Analysis'
            },
            'statistics': stats_with_percentages,
            'foundation_lookup': dict(foundation_lookup),
            'foundation_cards': foundation_cards
        }
        
        return dashboard_data
    
    def save_dashboard_data(self, output_file="dashboard_data.json"):
        """Save dashboard data to JSON file"""
        dashboard_data = self.generate_dashboard_data()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
        
        print(f"Dashboard data saved to {output_file}")
        print(f"Total foundations: {dashboard_data['metadata']['total_foundations']}")
        
        # Print some sample statistics
        print("\nSample Statistics:")
        if 'foundation_identity' in dashboard_data['statistics']:
            foundation_types = dashboard_data['statistics']['foundation_identity']['foundation_type']
            print("Foundation Types:")
            for ftype, data in foundation_types.items():
                print(f"  {ftype}: {data['count']} ({data['percentage']}%)")
        
        if 'ai_strategy' in dashboard_data['statistics']:
            ai_readiness = dashboard_data['statistics']['ai_strategy']['ai_readiness_score']
            print("\nAI Readiness Distribution:")
            for score_range, data in ai_readiness.items():
                print(f"  {score_range}: {data['count']} ({data['percentage']}%)")
        
        return dashboard_data

if __name__ == "__main__":
    aggregator = FoundationDataAggregator()
    aggregator.save_dashboard_data()