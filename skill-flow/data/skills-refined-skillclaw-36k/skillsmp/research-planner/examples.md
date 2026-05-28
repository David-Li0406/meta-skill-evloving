# Research Planner - Usage Examples

## Example 1: Simple Exploratory Research

**Input (from question-refiner)**:
```markdown
TASK: Provide a brief overview of quantum computing
CONTEXT: Need basic understanding for a blog post
SPECIFIC_QUESTIONS:
1. What is quantum computing?
2. How does it work?
3. What are practical applications?
KEYWORDS: quantum computing, qubits, quantum mechanics, superposition
CONSTRAINTS:
- Timeframe: Current
- Geography: Global
- Sources: General web + Wikipedia
- Max length: 2000 words
OUTPUT_FORMAT:
- Type: executive_summary
- Citation style: inline-with-url
```

**Output (Research Plan)**:
```markdown
# Research Plan: Quantum Computing Overview

## Executive Summary
- **Topic**: Quantum Computing Basics
- **Research Type**: Exploratory (Simple)
- **Complexity**: Simple
- **Estimated Duration**: 20-25 minutes
- **Estimated Cost**: ~$0.20

## Subtopic Decomposition

1. **Fundamentals of Quantum Computing**
   - Focus: Core concepts, qubits, superposition
   - Priority: High

2. **How Quantum Computers Work**
   - Focus: Architecture, gates, algorithms
   - Priority: High

3. **Practical Applications**
   - Focus: Current use cases, industries
   - Priority: Medium

## Search Strategies

### Subtopic 1: Fundamentals
- "quantum computing basics introduction"
- "what are qubits superposition entanglement"
- "quantum computing vs classical computing"

### Subtopic 2: How It Works
- "quantum computer architecture explained"
- "quantum gates algorithms simple"
- "how quantum computers process information"

### Subtopic 3: Applications
- "quantum computing applications use cases"
- "quantum computing practical examples 2024"
- "industries using quantum computing"

## Agent Deployment
- **Total Agents**: 3 (all haiku)
- **Agent 1**: Subtopic 1 - Fundamentals
- **Agent 2**: Subtopic 2 - How It Works
- **Agent 3**: Subtopic 3 - Applications

## Resource Estimation
- Time: 20-25 minutes
- Tokens: 55,000
- Cost: ~$0.20

Approval? ✅
```

---

## Example 2: Standard Comparative Research

**Input**:
```markdown
TASK: Compare React vs Vue for building enterprise web applications
CONTEXT: Tech lead needs to decide between frameworks for new project
SPECIFIC_QUESTIONS:
1. What are the key features of React and Vue?
2. How do they compare in performance?
3. Which has better enterprise ecosystem?
4. What are the learning curves?
5. Which is better for our use case?
KEYWORDS: React, Vue, JavaScript frameworks, enterprise apps, performance, ecosystem
CONSTRAINTS:
- Timeframe: 2022-present
- Geography: Global
- Sources: Technical blogs, documentation, benchmarks
- Max length: 8000 words
OUTPUT_FORMAT:
- Type: comparison_table + comprehensive_report
- Citation style: inline-with-url
```

**Output**:
```markdown
# Research Plan: React vs Vue Comparison

## Executive Summary
- **Research Type**: Comparative (Standard)
- **Complexity**: Standard
- **Estimated Duration**: 45-50 minutes
- **Estimated Cost**: ~$0.60

## Subtopic Decomposition

1. **React: Features & Capabilities**
2. **Vue: Features & Capabilities**
3. **Performance Benchmarking**
4. **Enterprise Ecosystem Comparison**
5. **Learning Curve & Developer Experience**

## Agent Deployment
- **Total Agents**: 5
- **Agent 1** (haiku): React features
- **Agent 2** (haiku): Vue features
- **Agent 3** (sonnet): Performance analysis (technical depth)
- **Agent 4** (sonnet): Enterprise ecosystem (comprehensive)
- **Agent 5** (haiku): Developer experience

## Resource Estimation
- Time: 45-50 minutes
- Tokens: 85,000
- Cost: ~$0.60

Modify options:
- "Make cheaper": Use all haiku ($0.35, 40 min)
- "More depth": Add academic agent ($0.90, 60 min)

Approval? ✅
```

---

## Example 3: Complex Market Analysis

**Input**:
```markdown
TASK: Comprehensive analysis of the AI chip market
CONTEXT: Investment firm evaluating AI chip sector for fund allocation
SPECIFIC_QUESTIONS:
1. What is the market size and growth trajectory?
2. Who are the major players and their market shares?
3. What are the key technologies and differentiation?
4. What are the competitive dynamics?
5. What are the growth drivers and trends?
6. What are the risks and challenges?
7. What is the future outlook?
KEYWORDS: AI chips, GPUs, TPUs, neural processors, NVIDIA, AMD, Intel, market analysis
CONSTRAINTS:
- Timeframe: 2020-present
- Geography: Global with regional breakdown
- Sources: Industry reports (Gartner, IDC), financial data, technical specs
- Max length: 20,000 words
OUTPUT_FORMAT:
- Type: comprehensive_report with executive summary
- Citation style: academic (for investor presentation)
```

**Output**:
```markdown
# Research Plan: AI Chip Market Analysis

## Executive Summary
- **Research Type**: Market Analysis (Complex)
- **Complexity**: Complex
- **Estimated Duration**: 75-90 minutes
- **Estimated Cost**: ~$1.80

## Subtopic Decomposition

1. **Market Size, Growth & Forecasts**
2. **Competitive Landscape & Market Shares**
3. **Technology Analysis & Differentiation**
4. **Application Segments & Use Cases**
5. **Trends & Growth Drivers**
6. **Risks, Challenges & Barriers**
7. **Future Outlook & Opportunities**

## Search Strategies
(3-5 queries per subtopic)

### Subtopic 1: Market Size
- "AI chip market size 2024 forecast Gartner IDC"
- "GPU market revenue growth statistics"
- "neural processor market analysis report"
- "AI accelerator shipments data"
- "semiconductor AI market trends"

[Similar detailed queries for other subtopics...]

## Data Sources

| Source Type | Examples | Priority | Rationale |
|-------------|----------|----------|-----------|
| Industry Reports | Gartner, IDC, Forrester | High | Market sizing data |
| Financial Data | Company reports, SEC filings | High | Revenue, market share |
| Technical | ArXiv, IEEE, vendor specs | Medium | Technology analysis |
| News | Bloomberg, Reuters | Medium | Recent developments |

## Agent Deployment
- **Total Agents**: 8 (4 sonnet, 4 haiku)
- **Agent 1** (sonnet): Market sizing (requires analysis)
- **Agent 2** (sonnet): Competitive analysis (complex)
- **Agent 3** (sonnet): Technology deep dive (technical)
- **Agent 4** (haiku): Applications & use cases
- **Agent 5** (haiku): Trends & drivers
- **Agent 6** (haiku): Risks & challenges
- **Agent 7** (sonnet): Future outlook (strategic)
- **Agent 8** (haiku): Cross-reference verification

## Resource Estimation
- Time: 75-90 minutes
- Tokens: 130,000
- Cost: ~$1.80

## Quality Gates
- Minimum 50 citations required
- At least 10 industry report sources (Gartner/IDC)
- Numeric data cross-verified from 3+ sources
- Overall quality score ≥ 8.5

## Contingency Plans
- If premium reports unavailable: Use vendor data + analyst summaries
- If data conflicts: Present range + explain variance
- If agent fails: Redeploy with alternative query set

Modify options:
- "Reduce cost": Use 6 agents (3 sonnet, 3 haiku) → $1.20, 60 min
- "Faster": Focus on top 5 subtopics only → $1.00, 50 min
- "More comprehensive": Add 2 more agents for regional analysis → $2.40, 100 min

Approval? ✅
```

---

## Example 4: Plan Modification Flow

**User**: "Make the AI chip plan faster and cheaper"

**Modified Plan**:
```markdown
# Research Plan: AI Chip Market Analysis (Fast & Economical)

## Modifications Applied
- ❌ Removed: "Application Segments" subtopic (lower priority)
- ❌ Removed: "Future Outlook" subtopic (can infer from trends)
- 🔄 Changed: All sonnet agents → haiku (except 1 for market sizing)
- 🔽 Reduced: From 8 agents to 5 agents

## New Configuration

### Subtopics (Reduced to 5)
1. Market Size & Growth
2. Competitive Landscape
3. Technology Overview (simplified)
4. Trends & Drivers
5. Cross-Reference Verification

### Agent Deployment
- **Agent 1** (sonnet): Market sizing (critical accuracy)
- **Agent 2-4** (haiku): Other subtopics
- **Agent 5** (haiku): Verification

### New Resource Estimation
- Time: **40-50 minutes** (was 75-90)
- Tokens: **75,000** (was 130,000)
- Cost: **~$0.50** (was $1.80)

### Trade-offs
- ✅ 70% cost reduction
- ✅ 45% time reduction
- ⚠️ Less technical depth (haiku vs sonnet)
- ⚠️ Fewer subtopics (5 vs 7)
- ⚠️ May need follow-up for application analysis

Accept modified plan? ✅
```

---

## Example 5: User Requests Alternative Plan

**User**: "Generate an alternative plan focused only on NVIDIA vs AMD"

**Alternative Plan**:
```markdown
# Alternative Research Plan: NVIDIA vs AMD Focused

## Reframed Approach
Instead of full market analysis, focus on two-player comparison:

### Subtopics (4)
1. NVIDIA: Products, Technology, Market Position
2. AMD: Products, Technology, Market Position
3. Head-to-Head Comparison (Performance, Pricing, Ecosystem)
4. Strategic Outlook: Competitive Dynamics

### Agent Deployment
- **Total Agents**: 4 (2 sonnet, 2 haiku)
- **Agent 1** (sonnet): NVIDIA deep dive
- **Agent 2** (sonnet): AMD deep dive
- **Agent 3** (haiku): Direct comparison
- **Agent 4** (haiku): Strategic outlook

### Resource Estimation
- Time: **35-40 minutes**
- Cost: **~$0.70**
- Output: **6,000-8,000 words**

This focused approach provides deeper competitive analysis but less market context.

Prefer this plan or the modified broader plan?
```

---

## Key Takeaways

1. **Plans adapt to complexity**: Simple queries get simple plans
2. **Resource estimates are transparent**: Users know cost/time upfront
3. **Modification is supported**: Plans can be adjusted based on constraints
4. **Quality gates are explicit**: Clear success criteria defined
5. **Alternative plans possible**: Different strategic approaches offered

These examples demonstrate how the research-planner skill creates actionable, resource-efficient plans tailored to user needs.
