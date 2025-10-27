#!/usr/bin/env python3
"""
Comprehensive taxonomy standardization mapping for dashboard consistency
"""

def get_taxonomy_standardization_mapping():
    """
    Returns comprehensive mapping for standardizing taxonomy values
    """
    
    # Foundation Type - Reduce from 37 to ~8 standard categories
    foundation_type_mapping = {
        # Corporate variations → Corporate
        'Corporate': 'Corporate',
        'Corporate (Walmart Inc. foundation)': 'Corporate',
        'Corporate (Workday Inc. foundation)': 'Corporate', 
        'Corporate (advised fund)': 'Corporate',
        'Corporate (company foundation)': 'Corporate',
        'Corporate (donor-advised fund)': 'Corporate',
        'Corporate (multiple affiliated foundations)': 'Corporate',
        'Corporate (no dedicated foundation)': 'Corporate',
        'Corporate (professional services firm foundation)': 'Corporate',
        'Collaborative (corporate coalition)': 'Corporate',
        
        # Private variations → Private  
        'Private': 'Private',
        'Private (board-funded operating model)': 'Private',
        'Private (corporate foundation)': 'Corporate',  # This is actually corporate
        'Private (dual foundation structure)': 'Private',
        'Private (endowed public charity)': 'Private',
        'Private (established by individual donor)': 'Private',
        'Private (family foundation)': 'Family',  # Move to family
        'Private (founded by hedge fund manager)': 'Private',
        'Private (independent nonprofit private foundation)': 'Private',
        'Private (independent private foundation)': 'Private',
        'Private (venture capital fund)': 'Venture Capital',
        
        # Operating variations → Operating
        'Operating': 'Operating',
        'Operating (501c3 nonprofit)': 'Operating',
        'Operating (B Corp hybrid model)': 'Operating',
        'Operating (LLC structure)': 'Operating',
        'Operating (LLC structure with foundation component)': 'Operating',
        'Operating (collaborative pooled fund)': 'Operating',
        'Operating (community foundation)': 'Operating',
        'Operating (community foundation model)': 'Operating',
        'Operating (union charitable arm)': 'Operating',
        'Operating (volunteer-based model)': 'Operating',
        
        # Family variations → Family
        'Family': 'Family',
        
        # Academic variations → Academic
        'Academic (university research center)': 'Academic',
        
        # Collaborative variations → Collaborative
        'Collaborative (pooled funding mechanism)': 'Collaborative',
        
        # Venture Capital variations → Venture Capital
        'Venture Capital (not a foundation)': 'Venture Capital',
        
        # Consulting variations → Consulting
        'Consulting (sole proprietorship)': 'Consulting',
        
        # Unknown/Not Found → Unknown
        'Unknown': 'Unknown',
        'N/A - Foundation not found': 'Unknown'
    }
    
    # Foundation Age - Reduce from 62 to 4 standard categories
    foundation_age_mapping = {}
    foundation_age_standard = {
        'Legacy': 'Legacy (pre-1970)',
        'Established': 'Established (1970-2010)', 
        'Recent': 'Recent (2010+)',
        'Unknown': 'Unknown'
    }
    
    # Auto-generate mapping based on patterns
    legacy_keywords = ['Legacy', '1936', '1937', '1940', '1942', '1944', '1948', '1950', '1954', '1959', '1960', '1964', '1966', '1969']
    established_keywords = ['1976', '1981', '1988', '1989', '1993', '1996', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2007']
    recent_keywords = ['Recent', '2013', '2015', '2018', '2019', '2020', '2021', '2023']
    
    # Decision Making Structure - Reduce to 5 categories
    decision_making_mapping = {
        # Founder-controlled variations
        'Founder-controlled': 'Founder-controlled',
        'Founder-controlled (Daniel Lurie leadership)': 'Founder-controlled',
        'Founder-controlled (Julian H. Robertson Jr.)': 'Founder-controlled', 
        'Founder-controlled (Scott Cook and Signe Ostby)': 'Founder-controlled',
        'Founder-led': 'Founder-controlled',
        'Single-founder controlled (Melinda French Gates)': 'Founder-controlled',
        'Individual-controlled (Nisha Patel)': 'Founder-controlled',
        
        # Family-controlled variations
        'Family-controlled': 'Family-controlled',
        'Family-controlled (Bennett & Meg Goodman with children)': 'Family-controlled',
        'Family-controlled (John and Tashia Morgridge)': 'Family-controlled',
        'Family-controlled (Pritzker-Traubert)': 'Family-controlled',
        'Family-controlled (currently led by David Tepper\'s daughter Randi)': 'Family-controlled',
        'Family-controlled (majority Hilton descendants)': 'Family-controlled',
        
        # Board-controlled variations
        'Board-controlled (board of trustees)': 'Board-controlled',
        'Board-controlled (community foundation governance)': 'Board-controlled',
        'Board-controlled (hedge fund leaders)': 'Board-controlled',
        'Board-controlled (independent foundation governance)': 'Board-controlled',
        'Board-governed': 'Board-controlled',
        'Board-governed (Latino philanthropist network)': 'Board-controlled',
        'Board-governed (co-chaired by Ford Foundation and Schmidt Futures)': 'Board-controlled',
        'Board-governed (shared leadership)': 'Board-controlled',
        'Board-governed (volunteer-led circles)': 'Board-controlled',
        'Committee-governed (12 contributing foundations)': 'Board-controlled',
        
        # Corporate-controlled variations  
        'Corporate-controlled': 'Corporate-controlled',
        'Corporate-controlled (Bechtel family)': 'Corporate-controlled',
        'Corporate-controlled (CEO and VP Social Impact oversight)': 'Corporate-controlled',
        'Corporate-controlled (Microsoft executive leadership)': 'Corporate-controlled',
        'Corporate-controlled (Schultz family)': 'Corporate-controlled',
        'Corporate-controlled (VC partnership)': 'Corporate-controlled',
        'Corporate-controlled (Walmart leadership)': 'Corporate-controlled',
        'Corporate-controlled (Workday leadership)': 'Corporate-controlled',
        
        # Partnership/Coalition-controlled variations
        'Coalition-controlled (17 member companies)': 'Partnership-controlled',
        'Partnership-controlled (6 team members including 3 Partners)': 'Partnership-controlled',
        
        # Unknown
        'Unknown': 'Unknown',
        'N/A - Foundation not found': 'Unknown'
    }
    
    # Grant Sourcing Strategy - Reduce to 6 categories
    grant_sourcing_mapping = {
        # Application-based variations
        'Application-based (community needs assessment)': 'Application-based',
        'Application-based (competitive fellowship program)': 'Application-based',
        'Application-based (grant seekers information available)': 'Application-based',
        'Application-based (standard foundation process)': 'Application-based',
        'Application-based (website application process)': 'Application-based',
        
        # Open application variations
        'Open application': 'Application-based',
        'Open application (Grand Challenges)': 'Application-based',
        'Open application (NEA members only)': 'Application-based',
        'Open application (RFP process)': 'Application-based',
        'Open application (geographic division)': 'Application-based',
        'Open application (plus foundation-initiated)': 'Application-based',
        'Open application (rolling basis)': 'Application-based',
        'Open application (with partnerships)': 'Application-based',
        'Open application (year-round)': 'Application-based',
        
        # Invitation only variations
        'Invitation only (email inquiry process)': 'Invitation only',
        'Invitation only (no unsolicited proposals)': 'Invitation only',
        'Invitation only (no unsolicited proposals, <1% from unsolicited)': 'Invitation only',
        
        # Program-officer initiated variations → Invitation only
        'Program-officer initiated': 'Invitation only',
        'Program-officer initiated (Chicago-focused strategic initiatives)': 'Invitation only',
        'Program-officer initiated (VC investment process)': 'Invitation only',
        'Program-officer initiated (collaborative decision-making)': 'Invitation only',
        'Program-officer initiated (currently redesigning strategy)': 'Invitation only',
        'Program-officer initiated (evidence-based approach)': 'Invitation only',
        'Program-officer initiated (invitation basis)': 'Invitation only',
        'Program-officer initiated (invitation-only approach)': 'Invitation only',
        'Program-officer initiated (invitation-only for research awards)': 'Invitation only',
        'Program-officer initiated (invitation-only)': 'Invitation only',
        'Program-officer initiated (no unsolicited proposals)': 'Invitation only',
        'Program-officer initiated (proactive identification)': 'Invitation only',
        'Program-officer initiated (strategic grants and challenges)': 'Invitation only',
        'Program-officer initiated (strategic investment approach)': 'Invitation only',
        'Program-officer initiated (strategic nonprofit partnerships)': 'Invitation only',
        'Program-officer initiated (strategic partnerships and applications)': 'Invitation only',
        'Program-officer initiated (trained volunteers)': 'Invitation only',
        
        # Mixed approach
        'Mixed (invitation only for major grants, open applications for local grants)': 'Mixed',
        'Collaborative/partnership-based': 'Mixed',
        
        # Investment-based
        'Investment-based (equity investments, not grants)': 'Investment-based',
        
        # Not applicable
        'Not applicable (consulting practice)': 'Not applicable',
        'N/A - Foundation not found': 'Unknown',
        'Unknown': 'Unknown'
    }
    
    # Endowment Size - Reduce to 6 categories
    endowment_size_mapping = {
        # Mega ($1B+)
        'Mega ($1B+ based on parent company assets)': 'Mega ($1B+)',
        'Mega ($1B+ through Mozilla Corporation)': 'Mega ($1B+)',
        'Mega ($1B+)': 'Mega ($1B+)',
        'Mega ($8+ billion)': 'Mega ($1B+)',
        'Very Large ($3.1-3.3B assets)': 'Mega ($1B+)',
        
        # Large ($100M-$1B)
        'Large ($100M+)': 'Large ($100M-$1B)',
        'Large ($351M+ assets, no traditional endowment)': 'Large ($100M-$1B)',
        'Large ($378+ million)': 'Large ($100M-$1B)',
        'Large ($381.7M assets)': 'Large ($100M-$1B)',
        'Large ($500M-$1B)': 'Large ($100M-$1B)',
        'Large ($50M five-year commitment)': 'Large ($100M-$1B)',  # Might be medium
        'Large (based on $100M Quality Jobs Fund and sustained giving)': 'Large ($100M-$1B)',
        'Large (based on $1B+ commitment history)': 'Large ($100M-$1B)',
        'Large (based on $31M annual giving and high-profile donors)': 'Large ($100M-$1B)',
        'Large (substantial based on major grant programs)': 'Large ($100M-$1B)',
        'Exceptional ($1.9B assets under management)': 'Mega ($1B+)',
        
        # Medium ($10M-$100M)
        'Medium ($100M-$500M)': 'Large ($100M-$1B)',  # Actually large
        'Medium ($10M three-year commitment)': 'Medium ($10M-$100M)',
        'Medium ($20M+ total since 2001, ongoing pooled contributions)': 'Medium ($10M-$100M)',
        'Medium ($27M+ pooled commitments)': 'Medium ($10M-$100M)',
        'Medium ($38.2M assets)': 'Medium ($10M-$100M)',
        'Medium ($39M assets)': 'Medium ($10M-$100M)',
        'Medium (based on $21.1M assets but $1.7B annual giving suggests corporate funding)': 'Corporate-backed',
        
        # Small (Under $10M)
        'Small (under $100M)': 'Small (<$10M)',  # Broad category
        'Small-Medium (estimated from $8M+ annual giving)': 'Medium ($10M-$100M)',
        'Small-Medium (member/sponsor funded)': 'Medium ($10M-$100M)',
        
        # Corporate-backed
        'Corporate assets (not applicable as foundation)': 'Corporate-backed',
        'Corporate assets (not applicable)': 'Corporate-backed',
        'Corporate backed ($80B+ Microsoft AI investment)': 'Corporate-backed',
        'Corporate giving (backed by $4T assets)': 'Corporate-backed',
        
        # Unknown
        'Unknown (100% impact committed)': 'Unknown',
        'Unknown (VC fund structure)': 'Unknown',
        'Unknown (corporate-backed)': 'Corporate-backed',
        'Unknown (family foundation of GSO Capital Partners co-founder)': 'Unknown',
        'Unknown (private family foundation)': 'Unknown',
        'Unknown (substantial based on $100K+ individual scholar support)': 'Unknown',
        'Unknown (substantial based on $1B+ total giving)': 'Unknown',
        'Unknown (substantial based on annual giving capacity)': 'Unknown',
        'Unknown (substantial based on giving capacity)': 'Unknown',
        'Unknown (substantial based on giving history)': 'Unknown',
        'Unknown (substantial based on grant activity)': 'Unknown',
        'Unknown (substantial based on major investment activities)': 'Unknown',
        'Unknown': 'Unknown',
        
        # Not applicable
        'Not applicable (consulting practice)': 'Not applicable',
        'N/A - Foundation not found': 'Unknown'
    }
    
    # Geographic Focus - Reduce to 5 categories
    geographic_focus_mapping = {
        # Global
        'International': 'Global',
        'International (40 nonprofits across 16 countries)': 'Global',
        'International (40+ countries)': 'Global',
        'International (46 countries, six continents)': 'Global',
        'International (50%+ international projects)': 'Global',
        'International (Africa-focused)': 'Global',
        'International (Japan, USA, Singapore, other regions)': 'Global',
        'International (LMIC emphasis)': 'Global',
        'International (US, Asia, Latin America, Europe, Middle East)': 'Global',
        'International (US, China, Israel, other locations)': 'Global',
        'International (emphasis on Washington state)': 'Global',
        'International (global nonprofit focus)': 'Global',
        'International (global operations, special focus on Washington state)': 'Global',
        'International (multiple locations)': 'Global',
        'International (with Bay Area emphasis)': 'Global',
        'Global (operates in 13 countries)': 'Global',
        'Global (workforce development globally)': 'Global',
        
        # National
        'National': 'National',
        'National (26 priority communities)': 'National',
        'National (NJ roots with nationwide reach)': 'National',
        'National (US education-to-employment focus)': 'National',
        'National (US focus with global collaborative elements)': 'National',
        'National (US graduate schools)': 'National',
        'National (US-based nonprofits, global impact)': 'National',
        'National (US-based)': 'National',
        'National (US-focused with global partnership elements)': 'National',
        'National (US-focused with international PwC Foundation entities)': 'National',
        'National (US-focused with some international elements)': 'National',
        'National (US-focused with some international labor connections)': 'National',
        'National (US-focused)': 'National',
        'National (United States focus)': 'National',
        'National (Washington DC-based)': 'National',
        'National (bicoastal offices)': 'National',
        'National (public education)': 'National',
        'National (with local CA focus)': 'National',
        
        # Regional
        'Regional (Baltimore, Hawaii, Israel, NYC, NE Pennsylvania, San Francisco)': 'Regional',
        'Regional (Bay Area focus)': 'Regional',
        'Regional (California statewide)': 'Regional',
        'Regional (California)': 'Regional',
        'Regional (Colorado focus)': 'Regional',
        'Regional (Great Lakes states)': 'Regional',
        'Regional (Kansas City primary, national secondary)': 'Regional',
        'Regional (San Francisco Bay Area + national)': 'Regional',
        'Regional (San Francisco Bay Area only)': 'Regional',
        'Regional (Texas only)': 'Regional',
        'Regional (US, Latin America, Canada)': 'Regional',
        
        # Local
        'Local (5 Bay Area counties)': 'Local',
        'Local (Bay Area focus)': 'Local',
        'Local (Chicago concentrated)': 'Local',
        'Local (NYC concentrated with national AI challenge)': 'Local',
        'Local (NYC five boroughs)': 'Local',
        'Local (New York City focused)': 'Local',
        
        # Unknown
        'Unknown': 'Unknown',
        'N/A - Foundation not found': 'Unknown'
    }
    
    # AI Funding Integration - Reduce to 4 categories  
    ai_funding_integration_mapping = {
        # Its own vertical
        'Its own vertical': 'Its own vertical',
        'Its own vertical (AI as core platform focus)': 'Its own vertical',
        'Its own vertical (AI as dedicated focus area)': 'Its own vertical', 
        'Its own vertical (AI as key focus area)': 'Its own vertical',
        'Its own vertical (AI for Good as dedicated program)': 'Its own vertical',
        'Its own vertical (trustworthy AI as main focus)': 'Its own vertical',
        
        # Integrated into verticals
        'Integrated across multiple verticals': 'Integrated into verticals',
        'Integrated across problem areas': 'Integrated into verticals',
        'Integrated across program areas': 'Integrated into verticals',
        'Integrated into STEM education vertical': 'Integrated into verticals',
        'Integrated into community development vertical': 'Integrated into verticals',
        'Integrated into digital equity vertical': 'Integrated into verticals',
        'Integrated into economic opportunity vertical': 'Integrated into verticals',
        'Integrated into education and entrepreneurship verticals': 'Integrated into verticals',
        'Integrated into education and medical research verticals': 'Integrated into verticals',
        'Integrated into education and technology verticals': 'Integrated into verticals',
        'Integrated into education and workforce verticals': 'Integrated into verticals',
        'Integrated into education vertical': 'Integrated into verticals',
        'Integrated into emerging tech vertical': 'Integrated into verticals',
        'Integrated into entrepreneurship vertical': 'Integrated into verticals',
        'Integrated into equity and community development verticals': 'Integrated into verticals',
        'Integrated into government innovation vertical': 'Integrated into verticals',
        'Integrated into healthcare applications': 'Integrated into verticals',
        'Integrated into journalism vertical': 'Integrated into verticals',
        'Integrated into multiple verticals': 'Integrated into verticals',
        'Integrated into technology and society vertical': 'Integrated into verticals',
        'Integrated into technology training vertical': 'Integrated into verticals',
        'Integrated into technology vertical': 'Integrated into verticals',
        'Integrated into workforce development vertical': 'Integrated into verticals',
        'Integrated into workforce vertical': 'Integrated into verticals',
        
        # Not integrated
        'Not integrated': 'Not integrated',
        'Not integrated (general technology focus)': 'Not integrated',
        'Not integrated (minimal AI focus in foundation activities)': 'Not integrated',
        'Not integrated (minimal AI focus)': 'Not integrated',
        'Not integrated (no AI focus found)': 'Not integrated',
        'Not integrated (no AI focus)': 'Not integrated',
        'Not integrated (workforce development focus without specific AI programming)': 'Not integrated',
        'Corporate separate from foundation': 'Not integrated',
        
        # Policy/Research focus
        'Policy research focus': 'Policy/Research focus',
        
        # Not applicable/Unknown
        'Not applicable (investment firm, not grant-maker)': 'Not applicable',
        'Not applicable (no AI focus)': 'Not integrated',
        'Unknown': 'Unknown',
        'N/A - Foundation not found': 'Unknown'
    }
    
    return {
        'foundation_type': foundation_type_mapping,
        'foundation_age': foundation_age_mapping,
        'decision_making_structure': decision_making_mapping,
        'grant_sourcing_strategy': grant_sourcing_mapping,
        'endowment_size': endowment_size_mapping,
        'geographic_focus': geographic_focus_mapping,
        'ai_funding_integration': ai_funding_integration_mapping
    }

if __name__ == "__main__":
    mapping = get_taxonomy_standardization_mapping()
    
    print("TAXONOMY STANDARDIZATION MAPPING")
    print("="*60)
    
    for dimension, dimension_mapping in mapping.items():
        print(f"\n{dimension.upper()}:")
        print("-" * len(dimension))
        
        # Group by standardized value
        standardized_groups = {}
        for original, standardized in dimension_mapping.items():
            if standardized not in standardized_groups:
                standardized_groups[standardized] = []
            standardized_groups[standardized].append(original)
        
        for standardized, originals in sorted(standardized_groups.items()):
            print(f"  {standardized}: {len(originals)} variations")
            if len(originals) > 3:  # Only show details for dimensions with many variations
                for original in sorted(originals)[:3]:
                    print(f"    • {original}")
                if len(originals) > 3:
                    print(f"    • ... and {len(originals)-3} more")
            else:
                for original in sorted(originals):
                    if original != standardized:
                        print(f"    • {original}")
        
        print(f"  TOTAL: {len(set(dimension_mapping.values()))} standardized categories")