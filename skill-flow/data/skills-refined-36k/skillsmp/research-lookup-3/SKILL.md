---
name: research-lookup
description: "Multi-provider research lookup supporting Gemini Deep Research (60-min comprehensive analysis) and Perplexity Sonar (fast web-grounded research). Intelligently routes between providers based on research mode and query complexity. Supports balanced mode for optimal quality/time tradeoff."
allowed-tools: [Read, Write, Edit, Bash]
---

# Research Information Lookup

## Overview

This skill provides **multi-provider research lookup** with intelligent routing between:

- **Gemini Deep Research**: 60-minute comprehensive research with extensive citations (requires GEMINI_API_KEY + Google AI Pro subscription)
- **Perplexity Sonar**: Fast web-grounded research in 30 seconds (requires OPENROUTER_API_KEY)

The skill automatically selects the best provider and model based on:
- **Research mode** configuration (balanced, perplexity, deep_research, auto)
- **Query complexity** (keywords, length, structure)
- **Context** (planning phase, task type)

## Research Modes

### Balanced (Recommended)
- Use Deep Research for Phase 1 market analysis and competitive landscape
- Use Perplexity for quick fact lookups and technology verification
- **Best quality/time tradeoff**: Comprehensive where it matters, fast elsewhere
- **Total plan time**: ~90 minutes

### Quick (Perplexity Only)
- Fast 30-second lookups for all research queries
- **Total plan time**: ~30 minutes
- Good for well-known tech stacks and familiar domains

### Comprehensive (Deep Research for All)
- 60-minute deep research for every major decision
- **Total plan time**: ~4 hours
- Best for novel technologies, uncertain markets, or high-stakes projects

### Auto (Context-Aware)
- Automatically selects based on query keywords and planning phase
- Uses Deep Research for: competitive analysis, market landscape, architecture decisions
- Uses Perplexity for: quick facts, pricing, version numbers, simple comparisons

## ⚠️ Deep Research Budget Constraints

**CRITICAL: You have a strict budget of 2 Deep Research queries per `/full-plan` session.**

### Budget Allocation Strategy

**Deep Research is expensive (30-60 min per query, high API cost). Use it ONLY for:**

1. **Phase 1: Competitive Landscape/Analysis** (Highest Priority)
   - Comprehensive market analysis with multiple competitors
   - Industry trends and adoption patterns
   - Regulatory landscape with complex timelines

2. **Phase 2: Novel Architecture Decisions** (Use Sparingly)
   - ONLY if technology stack is highly uncertain or cutting-edge
   - ONLY if multiple architectural approaches need deep comparison
   - DEFAULT to Gemini Pro or Perplexity for standard tech stack research

### DO NOT Use Deep Research For:

❌ Version checks or feature comparisons (use Perplexity)
❌ Pricing lookups or cost estimates (use Perplexity)
❌ Quick technical documentation (use Perplexity)
❌ Simple "what is X" queries (use Gemini Flash/Perplexity)
❌ Phases 3-6 research (use Perplexity - better temporal accuracy)

### Recommended Budget Allocation

**Conservative (Recommended):**
- 1 Deep Research: Phase 1 competitive landscape
- 1 Deep Research: Phase 1 regulatory timeline OR Phase 2 architecture (if novel)
- All others: Perplexity or Gemini Pro

**Aggressive (High-Stakes Projects):**
- 2 Deep Research: Phase 1 market analysis queries
- All others: Perplexity or Gemini Pro

### Budget Tracking

The system automatically tracks your Deep Research usage:
- `planning_outputs/<project>/DEEP_RESEARCH_BUDGET.json` contains the budget state
- Progress warnings appear when approaching limit: `⚠️ 1/2 Deep Research queries used`
- System falls back to Gemini Pro if budget exhausted

**Before using Deep Research, ask yourself:**
1. Is this query critical to project viability/direction?
2. Does it require 30-60 min comprehensive multi-source analysis?
3. Can Perplexity or Gemini Pro provide sufficient depth?

**Remember: Perplexity has better temporal accuracy for 2026 data, so prefer it for time-sensitive queries even in Phase 1.**

## When to Use This Skill

Use this skill when you need:

- **Current Research Information**: Latest studies, papers, and findings in a specific field
- **Literature Verification**: Check facts, statistics, or claims against current research
- **Background Research**: Gather context and supporting evidence for project planning
- **Citation Sources**: Find relevant papers and studies to cite in manuscripts
- **Technical Documentation**: Look up specifications, protocols, or methodologies
- **Recent Developments**: Stay current with emerging trends and breakthroughs
- **Statistical Data**: Find recent statistics, survey results, or research findings
- **Expert Opinions**: Access insights from recent interviews, reviews, or commentary

## Visual Enhancement with Project Diagrams

**When creating documents with this skill, always consider adding diagrams to enhance visual communication.**

If your document does not already contain diagrams:
- Use the **project-diagrams** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language
- Nano Banana Pro will automatically generate, review, and refine the diagram

**For project planning documents:** Diagrams should be generated by default to visually represent system architectures, workflows, data flows, or relationships described in the text.

**How to generate schematics:**
```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When to add diagrams:**
- System architecture diagrams
- Data flow illustrations
- Integration workflow diagrams
- Process pipeline visualizations
- Component relationship frameworks
- Any complex concept that benefits from visualization

For detailed guidance on creating diagrams, refer to the project-diagrams skill documentation.

---

## Usage

### Command-Line Interface

```bash
# Basic usage with auto mode (context-aware selection)
python research_lookup.py "Your research query here"

# Specify research mode explicitly
python research_lookup.py "Competitive landscape for SaaS market" \
  --research-mode deep_research

# Provide context for smart routing
python research_lookup.py "Latest PostgreSQL features" \
  --research-mode balanced \
  --phase 2 \
  --task-type architecture-research

# Force specific Perplexity model
python research_lookup.py "Quick fact check" \
  --research-mode perplexity \
  --force-model pro
```

### Research Mode Options

| Mode | Provider Selection | Best For |
|------|-------------------|----------|
| `balanced` | Deep Research for Phase 1 analysis, Perplexity for others | Most projects (recommended) |
| `perplexity` | Always use Perplexity | Quick planning, well-known tech |
| `deep_research` | Always use Gemini Deep Research | Novel domains, high-stakes |
| `auto` | Automatic based on keywords/context | Let the system decide |

### Context Parameters

**Phase-based routing:**
- `--phase 1` with `--task-type competitive-analysis` → triggers Deep Research in balanced/auto modes
- `--phase 2` with keywords like "architecture decision" → may trigger Deep Research
- Other phases → generally use Perplexity unless query is complex

**Example in planning workflow:**

```bash
# Phase 1: Competitive analysis (use Deep Research)
python research_lookup.py "Comprehensive competitive analysis for task management SaaS" \
  --research-mode balanced \
  --phase 1 \
  --task-type competitive-analysis

# Phase 2: Quick tech lookup (use Perplexity)
python research_lookup.py "Latest React best practices 2026" \
  --research-mode balanced \
  --phase 2 \
  --task-type research-lookup
```

### API Requirements

**For Perplexity (required for perplexity and balanced modes):**
```bash
export OPENROUTER_API_KEY='your_openrouter_key'
```

**For Gemini Deep Research (required for deep_research and balanced modes):**
```bash
export GEMINI_API_KEY='your_gemini_key'
# Requires Google AI Pro subscription ($19.99/month)
```

---

## Progress Tracking & Monitoring (v1.4.0+)

**For long-running Deep Research operations (60+ minutes)**, the plugin provides comprehensive progress tracking and checkpoint capabilities.

### Real-Time Progress Monitoring

When research operations take longer than 30 seconds, progress tracking is automatically enabled:

**Tier 1: Streaming Progress (Perplexity ~30s)**
- Real-time event callbacks for instant feedback
- No external monitoring needed

**Tier 2: Progress Files (Deep Research ~60 min)**
- JSON progress tracking with checkpoint history
- External monitoring from separate terminal
- Resume capability if interrupted

### Monitor Active Research

Monitor long-running research from a separate terminal:

```bash
# List all active research operations
python scripts/monitor-research-progress.py <project_folder> --list

# Monitor specific operation with live updates
python scripts/monitor-research-progress.py <project_folder> <task_id> --follow

# Example output:
# [14:23:45] 🔄 [████████████░░░░░] 30% | analyzing: Cross-referencing...
# [14:38:12] 🔄 [████████████████░░] 50% | synthesizing: Results...
# [14:52:30] ✅ [████████████████████] 100% | Complete!
```

### Resume Interrupted Research

If Deep Research is interrupted (network issues, timeout), resume from checkpoints:

```bash
# List resumable tasks with time estimates
python scripts/resume-research.py <project_folder> 1 --list

# Resume from checkpoint (saves up to 50 minutes)
python scripts/resume-research.py <project_folder> 1 --task <task_name>
```

**Checkpoint Strategy:**
- 15% checkpoint: ~9 minutes saved if interrupted
- 30% checkpoint: ~18 minutes saved if interrupted
- 50% checkpoint: ~30 minutes saved if interrupted

### Enhanced Research Integration

For Python API usage with full progress tracking:

```python
import asyncio
from pathlib import Path
from enhanced_research_integration import EnhancedResearchLookup

async def main():
    # Initialize with progress tracking
    research = EnhancedResearchLookup(
        project_folder=Path("planning_outputs/20260115_my-project"),
        phase_num=1,
        research_mode="balanced"  # or "quick", "deep_research", "auto"
    )

    # Execute with automatic progress tracking and checkpoints
    result = await research.research_with_progress(
        task_name="competitive-analysis",
        query="Comprehensive competitive landscape analysis",
        estimated_duration_sec=3600  # Auto-detected if not provided
    )

    # Access results and statistics
    print(f"Success: {result['success']}")
    print(f"Provider: {result['provider']}")
    print(f"Sources: {len(result.get('sources', []))}")

    # View execution statistics
    stats = research.get_stats()
    print(f"Tasks completed: {stats['tasks_completed']}")
    print(f"Time saved: {stats['total_time_saved_min']} minutes")

asyncio.run(main())
```

**Key Features:**
- Automatic checkpoint creation at 15%, 30%, 50% milestones
- Graceful degradation (Deep Research → Perplexity fallback)
- Error recovery with exponential backoff
- External monitoring support via progress files
- Statistics tracking across all research operations

**See Also:**
- `docs/WORKFLOWS.md` - Complete workflow examples with dual-terminal monitoring
- `scripts/enhanced_research_integration.py` - Integration layer implementation
- `scripts/resumable_research.py` - Core resumable research executor

---

## Core Capabilities

### 1. Academic Research Queries

**Search Academic Literature**: Query for recent papers, studies, and reviews in specific domains:

```
Query Examples:
- "Recent advances in CRISPR gene editing 2024"
- "Latest clinical trials for Alzheimer's disease treatment"
- "Machine learning applications in drug discovery systematic review"
- "Climate change impacts on biodiversity meta-analysis"
```

**Expected Response Format**:
- Summary of key findings from recent literature
- Citation of 3-5 most relevant papers with authors, titles, journals, and years
- Key statistics or findings highlighted
- Identification of research gaps or controversies
- Links to full papers when available

### 2. Technical and Methodological Information

**Protocol and Method Lookups**: Find detailed procedures, specifications, and methodologies:

```
Query Examples:
- "Western blot protocol for protein detection"
- "RNA sequencing library preparation methods"
- "Statistical power analysis for clinical trials"
- "Machine learning model evaluation metrics"
```

**Expected Response Format**:
- Step-by-step procedures or protocols
- Required materials and equipment
- Critical parameters and considerations
- Troubleshooting common issues
- References to standard protocols or seminal papers

### 3. Statistical and Data Information

**Research Statistics**: Look up current statistics, survey results, and research data:

```
Query Examples:
- "Prevalence of diabetes in US population 2024"
- "Global renewable energy adoption statistics"
- "COVID-19 vaccination rates by country"
- "AI adoption in healthcare industry survey"
```

**Expected Response Format**:
- Current statistics with dates and sources
- Methodology of data collection
- Confidence intervals or margins of error when available
- Comparison with previous years or benchmarks
- Citations to original surveys or studies

### 4. Citation and Reference Assistance

**Citation Finding**: Locate the most influential, highly-cited papers from reputable authors and prestigious venues:

```
Query Examples:
- "Foundational papers on transformer architecture" (expect: Vaswani et al. 2017 in NeurIPS, 90,000+ citations)
- "Seminal works in quantum computing" (expect: papers from Nature, Science by leading researchers)
- "Key studies on climate change mitigation" (expect: IPCC-cited papers, Nature Climate Change)
- "Landmark trials in cancer immunotherapy" (expect: NEJM, Lancet trials with 1000+ citations)
```

**Expected Response Format**:
- 5-10 most influential papers, **ranked by impact and relevance**
- Complete citation information (authors, title, journal, year, DOI)
- **Citation count** for each paper (approximate if exact unavailable)
- **Venue tier** indication (Nature, Science, Cell = Tier 1, etc.)
- Brief description of each paper's contribution
- **Author credentials** when notable (e.g., "from the Hinton lab", "Nobel laureate")
- Journal impact factors when relevant

**Quality Criteria for Citation Selection**:
- Prefer papers with **100+ citations** (for papers 3+ years old)
- Prioritize **Tier-1 journals** (Nature, Science, Cell, NEJM, Lancet)
- Include work from **recognized leaders** in the field
- Balance **foundational papers** (high citations, older) with **recent advances** (emerging, high-impact venues)

## Automatic Model Selection

This skill features **intelligent model selection** based on query complexity:

### Model Types

**1. Sonar Pro** (`perplexity/sonar-pro`)
- **Use Case**: Straightforward information lookup
- **Context**: 200K tokens
- **Pricing**: $3/1M prompt + $15/1M completion + $5/1K searches
- **Best For**:
  - Simple fact-finding queries
  - Recent publication searches
  - Basic protocol lookups
  - Statistical data retrieval
- **Speed**: Fast responses

**2. Sonar Reasoning Pro** (`perplexity/sonar-reasoning-pro`)
- **Use Case**: Complex analytical queries requiring deep reasoning
- **Model**: Powered by DeepSeek R1 with Chain of Thought
- **Context**: 128K tokens
- **Pricing**: $2/1M prompt + $8/1M completion + $5/1K searches
- **Best For**:
  - Comparative analysis ("compare X vs Y")
  - Synthesis of multiple studies
  - Evaluating trade-offs or controversies
  - Explaining mechanisms or relationships
  - Critical analysis and interpretation
- **Speed**: Slower but more thorough

### Complexity Assessment

The skill automatically detects query complexity using these indicators:

**Reasoning Keywords** (triggers Sonar Reasoning Pro):
- Analytical: `compare`, `contrast`, `analyze`, `analysis`, `evaluate`, `critique`
- Comparative: `versus`, `vs`, `vs.`, `compared to`, `differences between`, `similarities`
- Synthesis: `meta-analysis`, `systematic review`, `synthesis`, `integrate`
- Causal: `mechanism`, `why`, `how does`, `how do`, `explain`, `relationship`, `causal relationship`, `underlying mechanism`
- Theoretical: `theoretical framework`, `implications`, `interpret`, `reasoning`
- Debate: `controversy`, `conflicting`, `paradox`, `debate`, `reconcile`
- Trade-offs: `pros and cons`, `advantages and disadvantages`, `trade-off`, `tradeoff`, `trade offs`
- Complexity: `multifaceted`, `complex interaction`, `critical analysis`

**Complexity Scoring**:
- Reasoning keywords: 3 points each (heavily weighted)
- Multiple questions: 2 points per question mark
- Complex sentence structures: 1.5 points per clause indicator (and, or, but, however, whereas, although)
- Very long queries: 1 point if >150 characters
- **Threshold**: Queries scoring ≥3 points trigger Sonar Reasoning Pro

**Practical Result**: Even a single strong reasoning keyword (compare, explain, analyze, etc.) will trigger the more powerful Sonar Reasoning Pro model, ensuring you get deep analysis when needed.

**Example Query Classification**:

✅ **Sonar Pro Search** (straightforward lookup):
- "Recent advances in CRISPR gene editing 2024"
- "Prevalence of diabetes in US population"
- "Western blot protocol for protein detection"

✅ **Sonar Reasoning Pro** (complex analysis):
- "Compare and contrast mRNA vaccines vs traditional vaccines for cancer treatment"
- "Explain the mechanism underlying the relationship between gut microbiome and depression"
- "Analyze the controversy surrounding AI in medical diagnosis and evaluate trade-offs"

### Manual Override

You can force a specific model using the `force_model` parameter:

```python
# Force Sonar Pro Search for fast lookup
research = ResearchLookup(force_model='pro')

# Force Sonar Reasoning Pro for deep analysis
research = ResearchLookup(force_model='reasoning')

# Automatic selection (default)
research = ResearchLookup()
```

Command-line usage:
```bash
# Force Sonar Pro Search
python research_lookup.py "your query" --force-model pro

# Force Sonar Reasoning Pro
python research_lookup.py "your query" --force-model reasoning

# Automatic (no flag)
python research_lookup.py "your query"

# Save output to a file
python research_lookup.py "your query" -o results.txt

# Output as JSON (useful for programmatic access)
python research_lookup.py "your query" --json

# Combine: JSON output saved to file
python research_lookup.py "your query" --json -o results.json
```

## Technical Integration

### OpenRouter API Configuration

This skill integrates with OpenRouter (openrouter.ai) to access Perplexity's Sonar models:

**Model Specifications**:
- **Models**:
  - `perplexity/sonar-pro` (fast lookup, 200K context)
  - `perplexity/sonar-reasoning-pro` (deep analysis with DeepSeek R1, 128K context)
- **Search Mode**: Academic/scholarly mode (prioritizes peer-reviewed sources)
- **Search Context**: Always uses `high` search context for deeper, more comprehensive research results
- **Context Window**: 128-200K tokens depending on model
- **Capabilities**: Academic paper search, citation generation, scholarly analysis
- **Output**: Rich responses with citations and source links from academic databases
- **Pricing**: $2-3/1M input + $8-15/1M output + $5/1K searches

**API Requirements**:
- OpenRouter API key (set as `OPENROUTER_API_KEY` environment variable)
- Account with sufficient credits for research queries
- Proper attribution and citation of sources

**Python Dependencies** (for CLI usage):
If using the `research_lookup.py` script directly, install dependencies:
```bash
pip install requests
# Or install all plugin dependencies:
pip install -r requirements.txt
```

**Academic Mode Configuration**:
- System message configured to prioritize scholarly sources
- Search focused on peer-reviewed journals and academic publications
- Enhanced citation extraction for academic references
- Preference for recent academic literature (2020-2024)
- Direct access to academic databases and repositories

### Response Quality and Reliability

**Source Verification**: The skill prioritizes:
- Peer-reviewed academic papers and journals
- Reputable institutional sources (universities, government agencies, NGOs)
- Recent publications (within last 2-3 years preferred)
- High-impact journals and conferences
- Primary research over secondary sources

**Citation Standards**: All responses include:
- Complete bibliographic information
- DOI or stable URLs when available
- Access dates for web sources
- Clear attribution of direct quotes or data

## Paper Quality and Popularity Prioritization

**CRITICAL**: When searching for papers, ALWAYS prioritize high-quality, influential papers over obscure or low-impact publications. Quality matters more than quantity.

### Citation-Based Ranking

Prioritize papers based on citation count relative to their age:

| Paper Age | Citation Threshold | Classification |
|-----------|-------------------|----------------|
| 0-3 years | 20+ citations | Noteworthy |
| 0-3 years | 100+ citations | Highly Influential |
| 3-7 years | 100+ citations | Significant |
| 3-7 years | 500+ citations | Landmark Paper |
| 7+ years | 500+ citations | Seminal Work |
| 7+ years | 1000+ citations | Foundational |

**When reporting citations**: Always indicate approximate citation count when known (e.g., "cited 500+ times" or "highly cited").

### Venue Quality Tiers

Prioritize papers from higher-tier venues:

**Tier 1 - Premier Venues** (Always prefer):
- **General Science**: Nature, Science, Cell, PNAS
- **Medicine**: NEJM, Lancet, JAMA, BMJ
- **Field-Specific Flagships**: Nature Medicine, Nature Biotechnology, Nature Methods, Nature Genetics, Cell Stem Cell, Immunity
- **Top CS/AI**: NeurIPS, ICML, ICLR, ACL, CVPR (for ML/AI topics)

**Tier 2 - High-Impact Specialized** (Strong preference):
- Journals with Impact Factor > 10
- Top conferences in subfields (e.g., EMNLP, NAACL, ECCV, MICCAI)
- Society flagship journals (e.g., Blood, Circulation, Gastroenterology)

**Tier 3 - Respected Specialized** (Include when relevant):
- Journals with Impact Factor 5-10
- Established conferences in the field
- Well-indexed specialized journals

**Tier 4 - Other Peer-Reviewed** (Use sparingly):
- Lower-impact journals, only if directly relevant and no better source exists

### Author Reputation Indicators

Prefer papers from established, reputable researchers:

- **Senior authors with high h-index** (>40 in established fields)
- **Multiple publications in Tier-1 venues**
- **Leadership positions** at recognized research institutions
- **Recognized expertise**: Awards, editorial positions, society fellows
- **First/last author on landmark papers** in the field

### Direct Relevance Scoring

Always prioritize papers that directly address the research question:

1. **Primary Priority**: Papers directly addressing the exact research question
2. **Secondary Priority**: Papers with applicable methods, data, or conceptual frameworks
3. **Tertiary Priority**: Tangentially related papers (include ONLY if from Tier-1 venues or highly cited)

### Practical Application

When conducting research lookups:

1. **Start with the most influential papers** - Look for highly-cited, foundational work first
2. **Prioritize Tier-1 venues** - Nature, Science, Cell family journals, NEJM, Lancet for medical topics
3. **Check author credentials** - Prefer work from established research groups
4. **Balance recency with impact** - Recent highly-cited papers > older obscure papers > recent uncited papers
5. **Report quality indicators** - Include citation counts, journal names, and author affiliations in responses

**Example Quality-Focused Query Response**:
```
Key findings from high-impact literature:

1. Smith et al. (2023), Nature Medicine (IF: 82.9, cited 450+ times)
   - Senior author: Prof. John Smith, Harvard Medical School
   - Key finding: [finding]

2. Johnson & Lee (2024), Cell (IF: 64.5, cited 120+ times)
   - From the renowned Lee Lab at Stanford
   - Key finding: [finding]

3. Chen et al. (2022), NEJM (IF: 158.5, cited 890+ times)
   - Landmark clinical trial (N=5,000)
   - Key finding: [finding]
```

## Query Best Practices

### 1. Model Selection Strategy

**For Simple Lookups (Sonar Pro Search)**:
- Recent papers on a specific topic
- Statistical data or prevalence rates
- Standard protocols or methodologies
- Citation finding for specific papers
- Factual information retrieval

**For Complex Analysis (Sonar Reasoning Pro)**:
- Comparative studies and synthesis
- Mechanism explanations
- Controversy evaluation
- Trade-off analysis
- Theoretical frameworks
- Multi-faceted relationships

**Pro Tip**: The automatic selection is optimized for most use cases. Only use `force_model` if you have specific requirements or know the query needs deeper reasoning than detected.

### 2. Specific and Focused Queries

**Good Queries** (will trigger appropriate model):
- "Randomized controlled trials of mRNA vaccines for cancer treatment 2023-2024" → Sonar Pro Search
- "Compare the efficacy and safety of mRNA vaccines vs traditional vaccines for cancer treatment" → Sonar Reasoning Pro
- "Explain the mechanism by which CRISPR off-target effects occur and strategies to minimize them" → Sonar Reasoning Pro

**Poor Queries**:
- "Tell me about AI" (too broad)
- "Cancer research" (lacks specificity)
- "Latest news" (too vague)

### 3. Structured Query Format

**Recommended Structure**:
```
[Topic] + [Specific Aspect] + [Time Frame] + [Type of Information]
```

**Examples**:
- "CRISPR gene editing + off-target effects + 2024 + clinical trials"
- "Quantum computing + error correction + recent advances + review papers"
- "Renewable energy + solar efficiency + 2023-2024 + statistical data"

### 4. Follow-up Queries

**Effective Follow-ups**:
- "Show me the full citation for the Smith et al. 2024 paper"
- "What are the limitations of this methodology?"
- "Find similar studies using different approaches"
- "What controversies exist in this research area?"

## Integration with Project Planning

This skill enhances project planning by providing:

1. **Technology Research**: Gather current information on frameworks, tools, and best practices
2. **Architecture Validation**: Verify patterns and approaches against current standards
3. **Competitive Analysis**: Compare solutions with recent similar projects
4. **Decision Support**: Inform architectural decisions with latest evidence
5. **Cost Research**: Research pricing and service comparisons

## Error Handling and Limitations

**Known Limitations**:
- Information cutoff: Responses limited to training data (typically 2023-2024)
- Paywall content: May not access full text behind paywalls
- Emerging research: May miss very recent papers not yet indexed
- Specialized databases: Cannot access proprietary or restricted databases

**Error Conditions**:
- API rate limits or quota exceeded
- Network connectivity issues
- Malformed or ambiguous queries
- Model unavailability or maintenance

**Fallback Strategies**:
- Rephrase queries for better clarity
- Break complex queries into simpler components
- Use broader time frames if recent data unavailable
- Cross-reference with multiple query variations

## Usage Examples

### Example 1: Simple Literature Search (Sonar Pro Search)

**Query**: "Recent advances in transformer attention mechanisms 2024"

**Model Selected**: Sonar Pro Search (straightforward lookup)

**Response Includes**:
- Summary of 5 key papers from 2024
- Complete citations with DOIs
- Key innovations and improvements
- Performance benchmarks
- Future research directions

### Example 2: Comparative Analysis (Sonar Reasoning Pro)

**Query**: "Compare and contrast the advantages and limitations of transformer-based models versus traditional RNNs for sequence modeling"

**Model Selected**: Sonar Reasoning Pro (complex analysis required)

**Response Includes**:
- Detailed comparison across multiple dimensions
- Analysis of architectural differences
- Trade-offs in computational efficiency vs performance
- Use case recommendations
- Synthesis of evidence from multiple studies
- Discussion of ongoing debates in the field

### Example 3: Method Verification (Sonar Pro Search)

**Query**: "Standard protocols for flow cytometry analysis"

**Model Selected**: Sonar Pro Search (protocol lookup)

**Response Includes**:
- Step-by-step protocol from recent review
- Required controls and calibrations
- Common pitfalls and troubleshooting
- Reference to definitive methodology paper
- Alternative approaches with pros/cons

### Example 4: Mechanism Explanation (Sonar Reasoning Pro)

**Query**: "Explain the underlying mechanism of how mRNA vaccines trigger immune responses and why they differ from traditional vaccines"

**Model Selected**: Sonar Reasoning Pro (requires causal reasoning)

**Response Includes**:
- Detailed mechanistic explanation
- Step-by-step biological processes
- Comparative analysis with traditional vaccines
- Molecular-level interactions
- Integration of immunology and pharmacology concepts
- Evidence from recent research

### Example 5: Statistical Data (Sonar Pro Search)

**Query**: "Global AI adoption in healthcare statistics 2024"

**Model Selected**: Sonar Pro Search (data lookup)

**Response Includes**:
- Current adoption rates by region
- Market size and growth projections
- Survey methodology and sample size
- Comparison with previous years
- Citations to market research reports

## Performance and Cost Considerations

### Response Times

**Sonar Pro Search**:
- Typical response time: 5-15 seconds
- Best for rapid information gathering
- Suitable for batch queries

**Sonar Reasoning Pro**:
- Typical response time: 15-45 seconds
- Worth the wait for complex analytical queries
- Provides more thorough reasoning and synthesis

### Cost Optimization

**Automatic Selection Benefits**:
- Saves costs by using Sonar Pro Search for straightforward queries
- Reserves Sonar Reasoning Pro for queries that truly benefit from deeper analysis
- Optimizes the balance between cost and quality

**Manual Override Use Cases**:
- Force Sonar Pro Search when budget is constrained and speed is priority
- Force Sonar Reasoning Pro when working on critical research requiring maximum depth
- Use for specific sections of papers (e.g., Pro Search for methods, Reasoning for discussion)

**Best Practices**:
1. Trust the automatic selection for most use cases
2. Review query results - if Sonar Pro Search doesn't provide sufficient depth, rephrase with reasoning keywords
3. Use batch queries strategically - combine simple lookups to minimize total query count
4. For literature reviews, start with Sonar Pro Search for breadth, then use Sonar Reasoning Pro for synthesis

## Security and Ethical Considerations

**Responsible Use**:
- Verify all information against primary sources when possible
- Clearly attribute all data and quotes to original sources
- Avoid presenting AI-generated summaries as original research
- Respect copyright and licensing restrictions
- Use for research assistance, not to bypass paywalls or subscriptions

**Academic Integrity**:
- Always cite original sources, not the AI tool
- Use as a starting point for literature searches
- Follow institutional guidelines for AI tool usage
- Maintain transparency about research methods

## Complementary Tools

In addition to research-lookup, the project planner has access to **WebSearch** for:

- **Quick metadata verification**: Look up DOIs, publication years, journal names, volume/page numbers
- **Non-academic sources**: News, blogs, technical documentation, current events
- **General information**: Company info, product details, current statistics
- **Cross-referencing**: Verify citation details found through research-lookup

**When to use which tool:**
| Task | Tool |
|------|------|
| Find academic papers | research-lookup |
| Literature search | research-lookup |
| Deep analysis/comparison | research-lookup (Sonar Reasoning Pro) |
| Look up DOI/metadata | WebSearch |
| Verify publication year | WebSearch |
| Find journal volume/pages | WebSearch |
| Current events/news | WebSearch |
| Non-scholarly sources | WebSearch |

## Summary

This skill serves as a powerful research assistant with intelligent dual-model selection:

- **Automatic Intelligence**: Analyzes query complexity and selects the optimal model (Sonar Pro Search or Sonar Reasoning Pro)
- **Cost-Effective**: Uses faster, cheaper Sonar Pro Search for straightforward lookups
- **Deep Analysis**: Automatically engages Sonar Reasoning Pro for complex comparative, analytical, and theoretical queries
- **Flexible Control**: Manual override available when you know exactly what level of analysis you need
- **Academic Focus**: Both models configured to prioritize peer-reviewed sources and scholarly literature
- **Complementary WebSearch**: Use alongside WebSearch for metadata verification and non-academic sources

Whether you need quick fact-finding or deep analytical synthesis, this skill automatically adapts to deliver the right level of research support for your project planning needs.
