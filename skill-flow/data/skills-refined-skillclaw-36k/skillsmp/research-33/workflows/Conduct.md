---
description: Comprehensive multi-source research - Kai orchestrates CLI research tools
globs: ""
alwaysApply: false
---

# COMPREHENSIVE RESEARCH WORKFLOW FOR KAI

**YOU (Kai) are reading this because a research request was detected by the load-context hook.**

This workflow instructs you to orchestrate parallel multi-source research using the `research` CLI tool.

## THE RESEARCH CLI

Location: `~/.claude/bin/research`

```bash
# Single source queries
research --perplexity "your query here"
research --claude "your query here"
research --gemini "your query here"

# All sources in parallel (recommended)
research --all "your query here"

# Output is JSON to stdout - pipe-friendly
research --all "query" | jq '.[] | .content'
```

**Output format (JSON):**
```json
{
  "source": "perplexity|claude|gemini",
  "query": "the query",
  "timestamp": "ISO timestamp",
  "success": true,
  "content": "research findings...",
  "citations": ["url1", "url2"],
  "duration_ms": 1234
}
```

## RESEARCH MODES

### Quick Research (Single --all query)
- **Activation:** User says "quick research" or simple queries
- **Method:** Single `research --all "query"` call
- **Time:** ~15-30 seconds

### Standard Research (3 parallel queries)
- **Activation:** Default for most research requests
- **Method:** 3 parallel Bash calls with different query angles
- **Time:** ~30-45 seconds

### Extensive Research (8+ parallel queries)
- **Activation:** User says "extensive research"
- **Method:** 8 parallel Bash calls covering diverse angles
- **Time:** ~45-90 seconds

## WORKFLOW: STANDARD RESEARCH

### Step 1: Decompose the Question

Break the user's question into 3 focused sub-questions covering different angles:
- Core facts and recent developments
- Context, implications, and analysis
- Contrarian views, controversies, or edge cases

### Step 2: Launch Parallel Research (ONE MESSAGE)

**CRITICAL: Use a SINGLE message with multiple Bash tool calls for parallel execution**

```bash
# Launch all 3 in parallel (single message with 3 Bash calls)
research --all "sub-question 1 focusing on core facts"
research --all "sub-question 2 focusing on implications"
research --all "sub-question 3 focusing on controversies"
```

Each call returns JSON array with results from all 3 sources (perplexity, claude, gemini).

### Step 3: Collect and Parse Results

Each Bash call returns JSON. Parse the results:
- Extract `content` field from each source
- Note `citations` for attribution
- Check `success` field for any failures
- Note `duration_ms` for performance metrics

### Step 4: Synthesize Findings

Create a comprehensive report:

**A. Identify Confidence Levels:**
- **HIGH CONFIDENCE**: Corroborated by 2+ sources
- **MEDIUM CONFIDENCE**: Found by one source, seems reliable
- **LOW CONFIDENCE**: Single source, needs verification

**B. Structure Information:**
```markdown
## Key Findings

### [Topic Area 1]
**High Confidence:**
- Finding X (Sources: perplexity, claude)
- Finding Y (Sources: perplexity, gemini)

**Medium Confidence:**
- Finding Z (Source: gemini only)

### [Topic Area 2]
...

## Source Attribution
- **Perplexity**: [unique contributions - web/current events]
- **Claude**: [unique contributions - detailed analysis]
- **Gemini**: [unique contributions - multi-perspective synthesis]

## Conflicting Information
- [Note any disagreements between sources]
```

**C. Calculate Research Metrics:**
- **Total Queries**: Count of research CLI calls
- **Sources Used**: 3 (Perplexity, Claude, Gemini)
- **Total Results**: Number of successful responses
- **Confidence Level**: Overall confidence percentage

### Step 5: Return Results Using MANDATORY Format

📅 [current date]
**📋 SUMMARY:** Research coordination and key findings overview
**🔍 ANALYSIS:** Synthesis of multi-source research results
**⚡ ACTIONS:** Research queries executed, sources consulted
**✅ RESULTS:** Complete synthesized findings with source attribution
**📊 STATUS:** Research coverage, confidence levels, data quality
**➡️ NEXT:** Recommended follow-up research or verification needed
**🎯 COMPLETED:** Completed multi-source [topic] research
**🗣️ CUSTOM COMPLETED:** [Voice-optimized under 8 words]

**📈 RESEARCH METRICS:**
- **Total Queries:** [X] (--all queries × 3 sources each)
- **Sources Used:** 3 (Perplexity, Claude, Gemini)
- **Total Output:** [~X words]
- **Confidence Level:** [High/Medium/Low] ([percentage]%)
- **Result:** [Brief summary answer]

## WORKFLOW: QUICK RESEARCH

### Step 1: Single Query

For simple queries, use a single `--all` call:

```bash
research --all "the user's question"
```

### Step 2: Quick Synthesis

Parse the JSON results and provide a concise answer with source attribution.

**Time:** ~15-30 seconds

## WORKFLOW: EXTENSIVE RESEARCH

### Step 1: Generate Diverse Angles (8+)

Think deeply about the topic. Generate 8 unique research angles:
- Core facts and current state
- Historical context and evolution
- Technical/detailed deep-dive
- Practical implications and applications
- Contrarian views and criticisms
- Future predictions and trends
- Cross-domain connections
- Edge cases and unusual perspectives

### Step 2: Launch 8 Parallel Queries

**CRITICAL: Use a SINGLE message with 8 Bash tool calls**

```bash
# All 8 in parallel (single message)
research --all "angle 1: core facts about [topic]"
research --all "angle 2: historical context of [topic]"
research --all "angle 3: technical deep-dive on [topic]"
research --all "angle 4: practical implications of [topic]"
research --all "angle 5: criticisms and controversies around [topic]"
research --all "angle 6: future predictions for [topic]"
research --all "angle 7: cross-domain connections to [topic]"
research --all "angle 8: edge cases and unusual aspects of [topic]"
```

### Step 3: Enhanced Synthesis

Comprehensive cross-validation and domain mapping:

```markdown
## Executive Summary
[1-2 paragraph overview]

## Key Findings by Domain
### [Domain 1]
**High Confidence (multiple sources):**
- Finding with extensive corroboration

**Medium Confidence:**
- Finding with moderate corroboration

### [Domain 2]
...

## Unique Insights by Source
**Perplexity (Web/Current):**
- Novel findings from broad web search

**Claude (Analytical):**
- Deep analytical insights

**Gemini (Multi-Perspective):**
- Cross-domain connections

## Coverage Map
- Aspects covered: [list]
- Perspectives explored: [list]
- Time periods analyzed: [list]

## Conflicting Information & Uncertainties
[Note disagreements or gaps]

## Research Metrics
- Total Queries: [8 angles × 3 sources = 24 source queries]
- Sources: Perplexity, Claude, Gemini
- Confidence Level: [High/Medium] ([%])
```

## CRITICAL RULES

### Parallel Execution
- ✅ Launch ALL research queries in ONE message (parallel Bash calls)
- ✅ Each query covers a different angle
- ❌ DON'T launch sequentially (kills speed benefit)
- ❌ DON'T wait between queries

### Timeout Handling
- **Quick:** 30 second expectation
- **Standard:** 45 second expectation
- **Extensive:** 90 second expectation
- If a source fails, proceed with successful results
- Note failures in the final report

### JSON Parsing
- Results are JSON - parse `content`, `citations`, `success`
- Handle `--all` returning an array of 3 results
- Check `success: false` for errors

## EXAMPLE EXECUTION

**User asks:** "Research quantum computing developments"

**Your workflow:**

1. ✅ Decompose into 3 angles:
   - Recent breakthroughs and news
   - Practical applications and timeline
   - Challenges and limitations

2. ✅ Launch in parallel (ONE message with 3 Bash calls):
   ```bash
   research --all "quantum computing recent breakthroughs 2026"
   research --all "quantum computing practical applications timeline"
   research --all "quantum computing challenges limitations current state"
   ```

3. ✅ Parse JSON results from each call

4. ✅ Synthesize:
   - Cross-reference findings
   - Identify high-confidence facts
   - Note unique insights per source

5. ✅ Return with mandatory format and metrics

**Result:** Comprehensive quantum computing research from 9 source queries (3 angles × 3 sources) in ~30-45 seconds.

## API KEY REQUIREMENTS

The research CLI loads API keys from:
- `~/.claude/.env`
- `~/.config/pai/.env`
- `~/.env`

Required keys:
- `PERPLEXITY_API_KEY` - For Perplexity searches
- `GOOGLE_API_KEY` - For Gemini searches
- Claude uses WebSearch (no key needed)

## BENEFITS

**Why CLI-based research is superior:**
1. ✅ **Miessler-style composable** - Unix philosophy, pipe-friendly
2. ✅ **Minimal tokens** - No agent overhead, just results
3. ✅ **True parallelism** - Multiple Bash calls execute simultaneously
4. ✅ **JSON output** - Easy to parse and process
5. ✅ **API-direct** - Perplexity and Gemini called directly, no subprocess overhead
6. ✅ **Extensible** - Easy to add new sources

**This is the correct architecture. Use it for FAST research.**
