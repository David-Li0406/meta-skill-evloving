---
name: researching-external-sources
description: Use when researching documentation, papers, or articles for insights. Triggers on "research external", "find sources", "literature review", "what do the docs say".
---

# Researching External Sources

Guide for comprehensive multi-source research that synthesizes findings from documentation, academic papers, and practitioner articles into actionable recommendations.

## Instructions

### Step 1: Parse Research Parameters

Extract from the request:
- **Topic**: Main subject to investigate
- **Date Range** (optional): Prioritize recent sources if specified
- **Source Preferences**: Any specific sources to focus on

### Step 2: Research in Parallel (Conceptually)

Investigate three source categories:

**Documentation Sources**
- Official SDK docs (Claude Code, Google ADK, OpenAI)
- API references and guides
- Extract: Key concepts, APIs, patterns, best practices
- Format findings with source URLs

**Academic Papers**
- arxiv.org, Google Scholar, ACL Anthology
- Prioritize last 12 months unless specified
- Extract: Methodologies, findings, evaluation metrics
- Include paper URLs and publication dates

**Practitioner Articles**
- Engineering blogs, known practitioners
- Simon Willison, Eugene Yan, vendor blogs
- Extract: Production experiences, lessons learned
- Include article URLs and dates

### Step 3: Synthesize Cross-Source Findings

**Consensus Patterns** (High Confidence)
- Insights appearing across multiple source types
- Universal best practices
- Evidence from docs + papers + practice

**Unique Insights** (Source-Specific Value)
- Documentation: Technical details, API specs
- Academic: Novel methodologies, rigorous evaluations
- Practitioner: Production war stories, real-world constraints

**Contradictions & Trade-offs**
- Where sources disagree (note context differences)
- Evolution of thinking over time
- Theory vs practice gaps

### Step 4: Perform Gap Analysis

Map findings against existing book content:

1. **Find related content**
   ```
   Glob: chapters/**/*.md
   Grep: {topic keywords}
   ```

2. **Assess current coverage**
   - Read identified files
   - Check frontmatter status
   - Note partial vs complete coverage

3. **Identify gaps**
   - Topics missing from book
   - Entries needing updates
   - Areas where research provides deeper insights
   - Contradictions to existing content (needs correction)

### Step 5: Generate Recommendations

**Priority 1: Critical Updates**
- Contradicts existing content
- Fills major foundational gap
- Supported by all source types
- High impact

**Priority 2: Valuable Additions**
- Extends existing content
- Supported by 2+ source types
- Medium-high impact

**Priority 3: Nice to Have**
- Interesting but not essential
- Single-source insights
- Could seed new questions

**For each recommendation:**
- File: Absolute path to target
- Action: extend | new section | new entry | create questions
- Insight: Phrased in book voice
- Sources: Citation numbers
- Reasoning: Why this priority

### Step 6: Save Research Report

Save to: `.claude/.cache/research/external/{topic-slug}-{YYYY-MM-DD}.md`

Include:
- Research summary (2-3 sentences)
- Findings by source type
- Cross-source synthesis
- Gap analysis table
- Priority-ranked recommendations
- All citations with URLs

### Step 7: Report Results

```markdown
## Research Complete

**Topic:** {topic}
**Date:** {YYYY-MM-DD}

### Sources Researched

| Type | Status | Findings |
|------|--------|----------|
| Documentation | Complete | {count} |
| Academic Papers | Complete | {count} |
| Practitioner Articles | Complete | {count} |

### Cross-Source Synthesis

- **Consensus Patterns:** {count}
- **Unique Insights:** {count}
- **Contradictions:** {count}

### Gap Analysis

- **Existing Coverage:** {count} sections
- **Gaps Found:** {count}

### Top Recommendations

**Priority 1:**
1. `{path}` - {action}: "{insight}"

**Priority 2:**
1. `{path}` - {action}: "{insight}"

### Full Report

Saved to: {report_path}
```

## Key Principles

**Cross-Source Validation**
- Consensus across multiple sources = high confidence
- Single source = interesting but needs validation
- Documentation + papers + practice = strongest signal

**Priority Assignment Logic**
- Contradicts book = always Priority 1 (accuracy matters)
- Fills foundational gap + multi-source = Priority 1
- Extends existing + multi-source = Priority 2
- Single source + novel = Priority 3

**Book Voice Integration**
- Phrase insights as learnings, not facts
- Include production context when available
- Match existing chapter tone

**Citation Management**
- Number all citations sequentially
- Include full URLs (stable, not temporary)
- Note source type and publication date
- Enable verification and deep dives

## Examples

### Example 1: Research prompt caching
```
Topic: "prompt caching strategies"

Documentation: Anthropic docs on prompt caching API
Papers: Recent arxiv on KV cache optimization
Articles: Simon Willison on practical caching

Synthesis:
- Consensus: Caching prefix significantly reduces latency
- Unique: Papers show 40% cost reduction metrics
- Trade-off: Memory vs compute at different scales

Gap Analysis:
- chapters/4-context/ mentions caching briefly
- No detailed implementation guidance

Priority 1: Extend 4-context/2-context-strategies.md with caching patterns
```

### Example 2: Research agent orchestration
```
Topic: "multi-agent coordination patterns"

Sources found across all three types
Strong consensus on supervisor patterns
Contradictions on when to use hierarchical vs flat

Gap Analysis:
- chapters/6-patterns/ has orchestrator chapter
- Missing: comparison of coordination approaches

Priority 1: Add coordination comparison to 6-patterns/3-orchestrator-pattern.md
Priority 2: New section on failure handling
```

### Example 3: No contradictions found
```
Topic: "tool use best practices"

All sources align on core principles
Practitioner articles add production nuances

Gap Analysis:
- chapters/5-tool-use/ covers basics well
- Could deepen with production examples

Priority 2: Extend with practitioner war stories
Priority 3: Add edge case handling section
```

### Example 4: Partial source failure
```
Topic: "emerging evaluation methods"

Documentation: Complete
Papers: Complete
Articles: Failed (connection issue)

Report continues with available sources
Note limitation in findings
Suggest manual article search for completeness
```
