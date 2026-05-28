---
name: market-research-reports
description: "Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Features professional LaTeX formatting, extensive visual generation with project-diagrams and generate-image, deep integration with research-lookup for data gathering, and multi-framework strategic analysis including Porter's Five Forces, PESTLE, SWOT, TAM/SAM/SOM, and BCG Matrix."
---

# Market Research Reports

## Overview

Market research reports are comprehensive strategic documents that analyze industries, markets, and competitive landscapes to inform business decisions, investment strategies, and strategic planning. This skill generates **professional-grade reports of 50+ pages** with extensive visual content, modeled after deliverables from top consulting firms like McKinsey, BCG, Bain, Gartner, and Forrester.

**Key Features:**
- **Comprehensive length**: Reports are designed to be 50+ pages with no token constraints.
- **Visual-rich content**: 5-6 key diagrams generated at start (more added as needed during writing).
- **Data-driven analysis**: Deep integration with research-lookup for market data.
- **Multi-framework approach**: Porter's Five Forces, PESTLE, SWOT, BCG Matrix, TAM/SAM/SOM.
- **Professional formatting**: Consulting-firm quality typography, colors, and layout.
- **Actionable recommendations**: Strategic focus with implementation roadmaps.

**Output Format:** LaTeX with professional styling, compiled to PDF. Uses the `market_research.sty` style package for consistent, professional formatting.

## When to Use This Skill

This skill should be used when:
- Creating comprehensive market analysis for investment decisions.
- Developing industry reports for strategic planning.
- Analyzing competitive landscapes and market dynamics.
- Conducting market sizing exercises (TAM/SAM/SOM).
- Evaluating market entry opportunities.
- Preparing due diligence materials for M&A activities.
- Creating thought leadership content for industry positioning.
- Developing go-to-market strategy documentation.
- Analyzing regulatory and policy impacts on markets.
- Building business cases for new product launches.

## Visual Enhancement Requirements

**CRITICAL: Market research reports should include key visual content.**

Every report should generate **6 essential visuals** at the start, with additional visuals added as needed during writing. Start with the most critical visualizations to establish the report framework.

### Visual Generation Tools

**Use `project-diagrams` for:**
- Market growth trajectory charts.
- TAM/SAM/SOM breakdown diagrams (concentric circles).
- Porter's Five Forces diagrams.
- Competitive positioning matrices.
- Market segmentation charts.
- Value chain diagrams.
- Technology roadmaps.
- Risk heatmaps.
- Strategic prioritization matrices.
- Implementation timelines/Gantt charts.
- SWOT analysis diagrams.
- BCG Growth-Share matrices.

```bash
# Example: Generate a TAM/SAM/SOM diagram
python .claude/skills/project-diagrams/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circle diagram showing Total Addressable Market $50B outer circle, Serviceable Addressable Market $15B middle circle, Serviceable Obtainable Market $3B inner circle, with labels and arrows pointing to each segment" \
  -o figures/tam_sam_som.png --doc-type report

# Example: Generate Porter's Five Forces
python .claude/skills/project-diagrams/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: 'Threat of New Entrants' (top), 'Bargaining Power of Suppliers' (left), 'Bargaining Power of Buyers' (right), 'Threat of Substitutes' (bottom). Each box should show High/Medium/Low rating" \
  -o figures/porters_five_forces.png --doc-type report
```

**Use `generate-image` for:**
- Executive summary hero infographics.
- Industry/sector conceptual illustrations.
- Abstract technology visualizations.
- Cover page imagery.

```bash
# Example: Generate executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, showing key metrics in modern data visualization style, blue and green color scheme, clean minimalist design with icons representing market size, growth rate, and competitive landscape" \
  --output figures/executive_summary.png
```

### Recommended Visuals by Section (Generate as Needed)

| Section                   | Priority Visuals                                         | Optional Visuals                     |
|---------------------------|---------------------------------------------------------|--------------------------------------|
| Executive Summary         | Executive infographic (START)                           | -                                    |
| Market Size & Growth      | Growth trajectory (START), TAM/SAM/SOM (START)         | Regional breakdown, segment growth   |
| Competitive Landscape      | Porter's Five Forces (START), Positioning matrix (START)| Market share chart, strategic groups  |
| Risk Analysis             | Risk heatmap (START)                                   | Mitigation matrix                    |
| Strategic Recommendations  | Opportunity matrix                                      | Priority framework                   |
| Implementation Roadmap    | Timeline/Gantt                                          | Milestone tracker                    |
| Investment Thesis         | Financial projections                                   | Scenario analysis                    |

**Start with 6 priority visuals** (marked as START above), then generate additional visuals as specific sections are written and require visual support.

---

## Report Structure (50+ Pages)

### Front Matter (~5 pages)

#### Cover Page (1 page)
- Report title and subtitle.
- Hero visualization (generated).
- Date and classification.
- Prepared for / Prepared by.

#### Table of Contents (1-2 pages)
- Automated from LaTeX.
- List of Figures.
- List of Tables.

#### Executive Summary (2-3 pages)
- **Market Snapshot Box**: Key metrics at a glance.
- **Investment Thesis**: 3-5 bullet point summary.
- **Key Findings**: Major discoveries and insights.
- **Strategic Recommendations**: Top 3-5 actionable recommendations.
- **Executive Summary Infographic**: Visual synthesis of report highlights.

---

### Core Analysis (~35 pages)

#### Chapter 1: Market Overview & Definition (4-5 pages)

**Content Requirements:**
- Market definition and scope.
- Industry ecosystem mapping.
- Key stakeholders and their roles.
- Market boundaries and adjacencies.
- Historical context and evolution.

**Required Visuals (2):**
1. Market ecosystem/value chain diagram.
2. Industry structure diagram.

**Key Data Points:**
- Market definition criteria.
- Included/excluded segments.
- Geographic scope.
- Time horizon for analysis.

---

#### Chapter 2: Market Size & Growth Analysis (6-8 pages)

**Content Requirements:**
- Total Addressable Market (TAM) calculation.
- Serviceable Addressable Market (SAM) definition.
- Serviceable Obtainable Market (SOM) estimation.
- Historical growth analysis (5-10 years).
- Growth projections (5-10 years forward).
- Growth drivers and inhibitors.
- Regional market breakdown.
- Segment-level analysis.

**Required Visuals (4):**
1. Market growth trajectory chart (historical + projected).
2. TAM/SAM/SOM concentric circles diagram.
3. Regional market breakdown (pie chart or treemap).
4. Segment growth comparison (bar chart).

**Key Data Points:**
- Current market size (with source).
- CAGR (historical and projected).
- Market size by region.
- Market size by segment.
- Key assumptions for projections.

**Data Sources:**
Use `research-lookup` to find:
- Market research reports (Gartner, Forrester, IDC, etc.).
- Industry association data.
- Government statistics.
- Company financial reports.
- Academic studies.

---

#### Chapter 3: Industry Drivers & Trends (5-6 pages)

**Content Requirements:**
- Macroeconomic factors.
- Technology trends.
- Regulatory drivers.
- Social and demographic shifts.
- Environmental factors.
- Industry-specific trends.

**Analysis Frameworks:**
- **PESTLE Analysis**: Political, Economic, Social, Technological, Legal, Environmental.
- **Trend Impact Assessment**: Likelihood vs Impact matrix.

**Required Visuals (3):**
1. Industry trends timeline or radar chart.
2. Driver impact matrix.
3. PESTLE analysis diagram.

**Key Data Points:**
- Top 5-10 growth drivers with quantified impact.
- Emerging trends with timeline.
- Disruption factors.

---

#### Chapter 4: Competitive Landscape (6-8 pages)

**Content Requirements:**
- Market structure analysis.
- Major player profiles.
- Market share analysis.
- Competitive positioning.
- Barriers to entry.
- Competitive dynamics.

**Analysis Frameworks:**
- **Porter's Five Forces**: Comprehensive industry analysis.
- **Competitive Positioning Matrix**: 2x2 matrix on key dimensions.
- **Strategic Group Mapping**: Cluster competitors by strategy.

**Required Visuals (4):**
1. Porter's Five Forces diagram.
2. Market share pie chart or bar chart.
3. Competitive positioning matrix (2x2).
4. Strategic group map.

**Key Data Points:**
- Market share by company (top 10).
- Competitive intensity rating.
- Entry barriers assessment.
- Supplier/buyer power assessment.

---

#### Chapter 5: Customer Analysis & Segmentation (4-5 pages)

**Content Requirements:**
- Customer segment definitions.
- Segment size and growth.
- Buying behavior analysis.
- Customer needs and pain points.
- Decision-making process.
- Value drivers by segment.

**Analysis Frameworks:**
- **Customer Segmentation Matrix**: Size vs Growth.
- **Value Proposition Canvas**: Jobs, Pains, Gains.
- **Customer Journey Mapping**: Awareness to Advocacy.

**Required Visuals (3):**
1. Customer segmentation breakdown (pie/treemap).
2. Segment attractiveness matrix.
3. Customer journey or value proposition diagram.

**Key Data Points:**
- Segment sizes and percentages.
- Growth rates by segment.
- Average deal size / revenue per customer.
- Customer acquisition cost by segment.

---

#### Chapter 6: Technology & Innovation Landscape (4-5 pages)

**Content Requirements:**
- Current technology stack.
- Emerging technologies.
- Innovation trends.
- Technology adoption curves.
- R&D investment analysis.
- Patent landscape.

**Analysis Frameworks:**
- **Technology Readiness Assessment**: TRL levels.
- **Hype Cycle Positioning**: Where technologies sit.
- **Technology Roadmap**: Evolution over time.

**Required Visuals (2):**
1. Technology roadmap diagram.
2. Innovation/adoption curve or hype cycle.

**Key Data Points:**
- R&D spending in the industry.
- Key technology milestones.
- Patent filing trends.
- Technology adoption rates.

---

#### Chapter 7: Regulatory & Policy Environment (3-4 pages)

**Content Requirements:**
- Current regulatory framework.
- Key regulatory bodies.
- Compliance requirements.
- Upcoming regulatory changes.
- Policy trends.
- Impact assessment.

**Required Visuals (1):**
1. Regulatory timeline or framework diagram.

**Key Data Points:**
- Key regulations and effective dates.
- Compliance costs.
- Regulatory risks.
- Policy change probability.

---

#### Chapter 8: Risk Analysis (3-4 pages)

**Content Requirements:**
- Market risks.
- Competitive risks.
- Regulatory risks.
- Technology risks.
- Operational risks.
- Financial risks.
- Risk mitigation strategies.

**Analysis Frameworks:**
- **Risk Heatmap**: Probability vs Impact.
- **Risk Register**: Comprehensive risk inventory.
- **Mitigation Matrix**: Risk vs Mitigation strategy.

**Required Visuals (2):**
1. Risk heatmap (probability vs impact).
2. Risk mitigation matrix.

**Key Data Points:**
- Top 10 risks with ratings.
- Risk probability scores.
- Impact severity scores.
- Mitigation cost estimates.

---

### Strategic Recommendations (~10 pages)

#### Chapter 9: Strategic Opportunities & Recommendations (4-5 pages)

**Content Requirements:**
- Opportunity identification.
- Opportunity sizing.
- Strategic options analysis.
- Prioritization framework.
- Detailed recommendations.
- Success factors.

**Analysis Frameworks:**
- **Opportunity Attractiveness Matrix**: Attractiveness vs Ability to Win.
- **Strategic Options Framework**: Build, Buy, Partner, Ignore.
- **Priority Matrix**: Impact vs Effort.

**Required Visuals (3):**
1. Opportunity matrix.
2. Strategic options framework.
3. Priority/recommendation matrix.

**Key Data Points:**
- Opportunity sizes.
- Investment requirements.
- Expected returns.
- Timeline to value.

---

#### Chapter 10: Implementation Roadmap (3-4 pages)

**Content Requirements:**
- Phased implementation plan.
- Key milestones and deliverables.
- Resource requirements.
- Timeline and sequencing.
- Dependencies and critical path.
- Governance structure.

**Required Visuals (2):**
1. Implementation timeline/Gantt chart.
2. Milestone tracker or phase diagram.

**Key Data Points:**
- Phase durations.
- Resource requirements.
- Key milestones with dates.
- Budget allocation by phase.

---

#### Chapter 11: Investment Thesis & Financial Projections (3-4 pages)

**Content Requirements:**
- Investment summary.
- Financial projections.
- Scenario analysis.
- Return expectations.
- Key assumptions.
- Sensitivity analysis.

**Required Visuals (2):**
1. Financial projection chart (revenue, growth).
2. Scenario analysis comparison.

**Key Data Points:**
- Revenue projections (3-5 years).
- CAGR projections.
- ROI/IRR expectations.
- Key financial assumptions.

---

### Back Matter (~5 pages)

#### Appendix A: Methodology & Data Sources (1-2 pages)
- Research methodology.
- Data collection approach.
- Data sources and citations.
- Limitations and assumptions.

#### Appendix B: Detailed Market Data Tables (2-3 pages)
- Comprehensive market data tables.
- Regional breakdowns.
- Segment details.
- Historical data series.

#### Appendix C: Company Profiles (1-2 pages)
- Brief profiles of key competitors.
- Financial highlights.
- Strategic focus areas.

#### References/Bibliography
- All sources cited.
- BibTeX format for LaTeX.

---

## Workflow

### Phase 1: Research & Data Gathering

**Step 1: Define Scope**
- Clarify market definition.
- Set geographic boundaries.
- Determine time horizon.
- Identify key questions to answer.

**Step 2: Conduct Deep Research**

Use `research-lookup` extensively to gather market data:

```bash
# Market size and growth data
python skills/research-lookup/scripts/research_lookup.py \
  "What is the current market size and projected growth rate for [MARKET] industry? Include TAM, SAM, SOM estimates and CAGR projections"

# Competitive landscape
python skills/research-lookup/scripts/research_lookup.py \
  "Who are the top 10 competitors in the [MARKET] market? What is their market share and competitive positioning?"

# Industry trends
python skills/research-lookup/scripts/research_lookup.py \
  "What are the major trends and growth drivers in the [MARKET] industry for 2024-2030?"

# Regulatory environment
python skills/research-lookup/scripts/research_lookup.py \
  "What are the key regulations and policy changes affecting the [MARKET] industry?"
```

**Step 3: Data Organization**
- Create `sources/` folder with research notes.
- Organize data by section.
- Identify data gaps.
- Conduct follow-up research as needed.

### Phase 2: Analysis & Framework Application

**Step 4: Apply Analysis Frameworks**

For each framework, conduct structured analysis:

- **Market Sizing**: TAM → SAM → SOM with clear assumptions.
- **Porter's Five Forces**: Rate each force High/Medium/Low with rationale.
- **PESTLE**: Analyze each dimension with trends and impacts.
- **SWOT**: Internal strengths/weaknesses, external opportunities/threats.
- **Competitive Positioning**: Define axes, plot competitors.

**Step 5: Develop Insights**
- Synthesize findings into key insights.
- Identify strategic implications.
- Develop recommendations.
- Prioritize opportunities.

### Phase 3: Visual Generation

**Step 6: Generate All Visuals**

Generate visuals BEFORE writing the report. Use the batch generation script:

```bash
# Generate all standard market report visuals
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "[MARKET NAME]" \
  --output-dir figures/
```

Or generate individually:

```bash
# 1. Market growth trajectory
python .claude/skills/project-diagrams/scripts/generate_schematic.py \
  "Bar chart showing market growth from 2020 to 2034, with historical