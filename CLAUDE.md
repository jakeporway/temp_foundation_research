# Foundation AI Research Analysis Project

This project contains a comprehensive analysis of 104 foundations and their AI grant activities, with an interactive dashboard for exploring the results.

## Project Overview

This research project systematically analyzed foundations to assess their AI readiness and grant activities. Using Claude's WebSearch capabilities, we created detailed profiles for 82 foundations (out of 104 attempted) and built an interactive dashboard for data exploration.

## Key Files

### Core Analysis Files
- **`foundation_list.txt`** - Original list of 104 foundations to analyze
- **`results/`** - Directory containing 111 YAML analysis files (some foundations had multiple iterations)
- **`dashboard_data.json`** - Aggregated statistics from all analyzed foundations

### Dashboard System
- **`dashboard_standalone.html`** - Main interactive dashboard with embedded data (recommended)
- **`foundation_detail.html`** - Individual foundation profile template (uses Valhalla Foundation as example)
- **`foundation_cards.js`** - Complete dataset of all 82 foundations in JavaScript format

### Supporting Scripts
- **`aggregate_data.py`** - Parses YAML files and generates dashboard statistics
- **`taxonomy_standardization.py`** - Maps foundation taxonomy values to standardized categories
- **`analyze_taxonomy_values.py`** - Analysis tool for identifying unique taxonomy values

## Analysis Methodology

### Data Collection Process
1. **Systematic Web Search**: 4 targeted searches per foundation using Claude WebSearch:
   - AI grants and artificial intelligence initiatives
   - Philanthropy profile, assets, and location
   - AI funding strategy and technology approach
   - Machine learning grants and research funding

2. **Structured Analysis**: Each foundation received comprehensive evaluation across:
   - **Foundation Identity** (7 dimensions): Type, age, decision-making, sourcing, endowment, geography, approach
   - **AI Strategy** (7 dimensions): Integration, readiness score, outcome, output, lifecycle, investment, innovation
   - **Economic Opportunity Strategy** (1 dimension): Skills vs. jobs focus

3. **AI Readiness Scoring**: 0-10 scale assessment based on:
   - Existing AI grant activities
   - Strategic AI integration
   - Innovation focus and capacity
   - Technology sector expertise
   - Available resources and assets

### Taxonomy Standardization
Original analysis produced 37+ different foundation type values. These were standardized to 8 clean categories:
- **Corporate** (30.5% - 25 foundations)
- **Private** (30.5% - 25 foundations) 
- **Operating** (17.1% - 14 foundations)
- **Family** (12.2% - 10 foundations)
- **Unknown** (4.9% - 4 foundations)
- **Venture Capital** (2.4% - 2 foundations)
- **Collaborative** (1.2% - 1 foundation)
- **Consulting** (1.2% - 1 foundation)

## Key Findings

### AI Readiness Distribution
- **High AI Readiness (9-10)**: 21 foundations (25.6%)
- **Medium-High (7-8)**: 17 foundations (20.7%)
- **Medium-Low (3-4)**: 17 foundations (20.7%)
- **Low (0-2)**: 15 foundations (18.3%)
- **Medium (5-6)**: 12 foundations (14.6%)

### AI Strategy Patterns
- **61%** of foundations aim to increase AI use for social impact
- **52.4%** focus on AI solution creation
- **50%** have high innovation focus
- **37.8%** integrate AI into existing program verticals
- **25.6%** treat AI as its own dedicated vertical

### Foundation Characteristics
- **68.3%** use invitation-only grant sourcing
- **79.3%** employ multi-year, high engagement funding approaches
- **30.5%** have mega-endowments ($1B+)
- **37.8%** have national geographic focus, 35.4% global focus

## Interactive Dashboard Features

### Complete Taxonomy Visualization
The dashboard shows percentage breakdowns for all 15 taxonomy dimensions:

**Foundation Identity (6 dimensions):**
- Foundation Type, Geographic Focus, Decision Making Structure
- Grant Sourcing Strategy, Endowment Size, Funding Approach

**AI Strategy (6 dimensions):**  
- AI Funding Integration, AI Readiness Score, AI Outcome
- AI Related Output, Internal AI Investment, Innovation Focus

**Economic Opportunity Strategy (1 dimension):**
- EO Focus Area (Skills vs. Jobs vs. Both)

### Interactive Features
- **🔍 Search**: Search foundations by name, type, location, focus areas
- **📊 Click-to-Filter**: Click any taxonomy bar to filter results
- **🏷️ Active Filters**: View and manage applied filters
- **📋 Foundation Cards**: Browse all 82 foundations with key metrics
- **🔗 Clickable Cards**: Preview foundation details (with placeholder for full profiles)

## Notable High-Readiness Foundations

### Score 10 (Exceptional)
- **Microsoft Philanthropies** - Leading AI for Good initiatives
- **OpenAI Startup Fund** - Direct AI sector investment
- **Google.org** - Comprehensive AI.org programs

### Score 9 (Very High)
- **Valhalla Foundation** - $1B NextLadder Ventures collaboration
- **Mozilla Foundation** - Trustworthy AI advocacy
- **Meta** - AI research and responsible AI development

### Score 8 (High)
- **Chan Zuckerberg Initiative** - AI applications in science/education
- **Simons Foundation** - ML research in computational science
- **Knight Foundation** - Journalism AI and misinformation

## Usage Instructions

### Running the Web Application
1. **Setup Environment**: Copy `.env.example` to `.env` and add your Anthropic API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

2. **Start the Server**: 
   ```bash
   python app.py
   ```

3. **Access the Dashboard**: Navigate to `http://127.0.0.1:6001`
   - **📊 Dashboard**: Interactive filtering and foundation exploration
   - **💬 Chat**: Natural language queries against foundation database

### Chat Interface Features
- **Semantic Queries**: Ask questions like "foundations most likely to fund capacity building for small nonprofits"
- **Map-Reduce Processing**: Efficiently processes 82 foundations across 7 batches using Claude API
- **Configurable Model**: Set `ANTHROPIC_MODEL` in .env (defaults to claude-3-5-sonnet-20241022)
- **Detailed Results**: Foundation recommendations with match scores and reasoning
- **Processing Transparency**: Shows analysis statistics and batch processing details

### Legacy Standalone Dashboard
1. Open `dashboard_standalone.html` in any web browser
2. No server required - all data is embedded for offline use
3. Works on desktop and mobile devices

### Exploring Foundation Profiles
1. Click any foundation card to see a detail preview
2. Use `foundation_detail.html` as a template for full profiles
3. Individual YAML files in `results/` contain complete analysis data

### Filtering and Analysis
1. Click taxonomy bars to filter by specific categories
2. Use search box to find foundations by keywords
3. Apply multiple filters to narrow down results
4. View real-time counts and percentages

## Technical Implementation

### Data Processing Pipeline
1. **Web Research** → YAML analysis files (111 files created)
2. **Taxonomy Standardization** → Consistent category mapping
3. **Data Aggregation** → JSON statistics and foundation cards
4. **Dashboard Integration** → Embedded JavaScript for standalone operation

### Key Technical Solutions
- **CORS Avoidance**: Embedded data eliminates external file loading issues
- **Responsive Design**: Works across desktop/mobile devices
- **Real-time Filtering**: Client-side filtering for instant results
- **Standardized Taxonomy**: Consistent categories for meaningful comparisons

## Research Limitations

- Analysis based on publicly available web information only
- AI activities may exist but not be publicly documented  
- Foundation strategies may have evolved since analysis date (2025-01-28)
- Invitation-only foundations have limited transparency into full AI pipelines
- Some foundations (22 out of 104) could not be successfully analyzed due to insufficient public information

## Future Enhancements

### Potential Additions
- **Full Foundation Detail Pages**: Complete profiles for all 82 foundations
- **Interview Simulation Integration**: Interactive Q&A based on foundation analysis
- **Advanced Analytics**: Trend analysis, correlation studies, geographic mapping
- **Export Functionality**: CSV/PDF export of filtered results
- **Update Mechanism**: Refresh foundation data periodically

### Data Expansion
- **Grant Database Integration**: Link to actual grant records where available
- **Leadership Analysis**: Foundation board and staff AI expertise
- **Portfolio Analysis**: Detailed review of AI-related grantee organizations
- **Outcome Tracking**: Measure actual impact of AI initiatives

## Contact & Usage

This analysis was conducted using Claude Code's web search and analysis capabilities. The methodology can be replicated for other foundation research projects or updated with new foundation lists.

For technical questions about the dashboard or data processing scripts, refer to the embedded code comments and structured data formats in the JSON and YAML files.

---

**Generated**: January 28, 2025  
**Analysis Method**: Claude WebSearch systematic foundation research  
**Dataset**: 82 foundations successfully analyzed from 104 attempted  
**Dashboard**: Interactive standalone HTML with embedded data