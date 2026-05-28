# UXR Analysis Template

This template provides the structure for all UXR report analyses. Follow this format exactly to ensure consistency across the research catalog.

---

## HTML Comment Summary (Lines 1-9)

```markdown
<!-- SUMMARY
Title: [Report Title]
Type: [Research Type - e.g., Qualitative UXR Study, Market Analysis, JTBD Framework, Quantitative Survey]
Key Themes: [3-5 core themes, comma-separated]
Core Insights: [2-3 sentences capturing the most critical findings and their implications]
Relevance: [How this connects to strategic objectives - reference SO1-SO5, Data Hub strategy, etc.]
Quality: [High/Medium/Low - Brief justification based on methodology rigor, sample size, actionability]
Last Reviewed: [YYYY-MM-DD]
-->
```

---

## Main Document Structure

### Title
```markdown
# [Report Name] Analysis
```

---

### Metadata Section
```markdown
## Metadata
- **Study Name**: [Official name of the study]
- **Created By**: [Researchers, team, or organization]
- **Study URL**: [URL provided by user, or "URL not available"]
```

Optional metadata fields (include if available in report):
- **Date**: [When research was conducted]
- **Research Scope**: [Sample size, participant details]
- **Type**: [Qualitative, Quantitative, Mixed Methods]

---

### The Big Picture
```markdown
## The Big Picture

[2-3 paragraphs that answer:]

**Paragraph 1**: What did this research explore, and what are the headline findings?
- Summarize the research question and approach
- State the most important discovery or insight

**Paragraph 2**: How do these findings connect to HubSpot's Overall Data Strategy?
- Reference specific strategic objectives (SO1-SO5) if relevant
- Explain alignment or tension with current strategy
- Note any paradigm shifts or foundational insights

**Paragraph 3**: What are the strategic implications?
- How should this influence product decisions?
- What gaps or opportunities does it reveal?
- What changes in execution does it suggest?
```

**Writing Guidelines for This Section**:
- Be specific, not abstract
- Use clear frameworks and analogies
- Make strategic connections explicit
- Avoid jargon; explain simply and powerfully

---

### Key Findings
```markdown
## Key Findings

### 1. [Finding Theme 1]
- [Specific insight or data point]
- [Supporting detail or context]
- [Implication or consequence]

### 2. [Finding Theme 2]
- [Specific insight or data point]
- [Supporting detail or context]
- [Implication or consequence]

[Continue for all major findings - typically 3-7 themed findings]
```

**Guidelines**:
- Use descriptive headers that capture the essence
- Each finding should be actionable or insight-generating
- Include specific details: numbers, quotes, examples
- Group related insights under single themes
- Prioritize findings by strategic importance

---

### Interesting Metrics (Optional)
```markdown
## Interesting Metrics

- [X%] of [population] [behavior/characteristic] (Source: [page/section])
- [Metric] shows [correlation/trend] with [outcome]
- [Specific number] [units] for [measurement]
- [Comparative statistic]: [Group A] vs [Group B]
```

**Include this section ONLY if**:
- Research contains highly significant quantitative data
- Numbers are surprising or counter-intuitive
- Metrics have direct strategic implications
- Data points will be referenced in strategic documents

**Omit this section if**:
- Research is purely qualitative
- No standout metrics emerge
- Numbers are already well-covered in Key Findings

---

### Recommendations
```markdown
## Recommendations

### Strategic Initiatives
1. **[Strategic Recommendation 1]**
   - [What to do]
   - [Why it matters]
   - [Expected outcome]

2. **[Strategic Recommendation 2]**
   - [What to do]
   - [Why it matters]
   - [Expected outcome]

[Continue for 2-4 strategic initiatives]

### Tactical Actions
1. **[Tactical Recommendation 1]**
   - [Specific action to take]
   - [How it addresses findings]
   - [Success criteria]

2. **[Tactical Recommendation 2]**
   - [Specific action to take]
   - [How it addresses findings]
   - [Success criteria]

[Continue for 3-5 tactical actions]
```

**Strategic vs Tactical**:
- **Strategic**: Requires cross-functional alignment, long-term investment, fundamental changes
- **Tactical**: Can be executed by single team, near-term, incremental improvements

**Guidelines**:
- Connect each recommendation directly to findings
- Be specific and actionable
- Include success criteria when possible
- Prioritize by impact and feasibility

---

### Connected Research
```markdown
## Connected Research

### 1. "[Related Research Title 1]"
[2-3 sentences explaining how this research connects to the current analysis. What themes overlap? What insights reinforce each other? How do they build on one another?]

### 2. "[Related Research Title 2]"
[2-3 sentences explaining the connection. Be specific about which findings align or complement each other.]

[Continue for 3-5 related research items]
```

**How to Identify Connected Research**:
1. Review the UXR catalog: `/Users/jvincent/Projects/writing/resources/UXR Reports/Analysis/claude.md`
2. Look for research that:
   - Explores similar themes or user segments
   - Provides complementary data (qualitative ↔ quantitative)
   - Shows longitudinal progression (earlier/later studies)
   - Addresses related pain points or opportunities
3. Reference actual research from the catalog
4. Explain the connection explicitly; don't assume it's obvious

---

### Disconnected Research (Optional)
```markdown
## Disconnected Research

### 1. "[Contradictory Research Title 1]"
**The Contradiction**: [Explain what this research found that contradicts or challenges the current analysis]

**Why It Matters**: [Explain the implications of this disconnect - does it suggest segment differences, methodology issues, or evolving customer needs?]

### 2. "[Contradictory Research Title 2]"
**The Contradiction**: [Explain the conflict]

**Why It Matters**: [Explain implications]
```

**Include this section ONLY if**:
- Genuine contradictions exist with other research
- Findings challenge previous assumptions
- Different segments show opposite patterns
- Methodology differences lead to different conclusions

**Omit this section if**:
- No meaningful contradictions exist
- Differences are due to different scopes (not contradictions)

---

### Slide/Section Index
```markdown
## Slide/Section Index

For searchability and quick reference:

- **Slide 1-5**: [Key concept or section theme]
- **Slide 6-12**: [Key concept or section theme]
- **Slide 13-20**: [Key concept or section theme]
- **Slide 21-28**: [Key concept or section theme]

[Or for text-based reports:]

- **Executive Summary**: [Key points covered]
- **Methodology**: [Research approach]
- **Section 1 - [Title]**: [Key concept]
- **Section 2 - [Title]**: [Key concept]
- **Appendix**: [What's included]
```

**Guidelines**:
- Group slides/sections by theme rather than listing every single slide
- Focus on major sections and transitions
- Include page/slide numbers for reference
- Make it useful for future searches

---

## Quality Standards Checklist

When creating an analysis, ensure:

- [ ] **Specificity**: Exact numbers, percentages, quotes included
- [ ] **Strategic Connection**: Every insight tied to business implications
- [ ] **Honesty**: Research limitations acknowledged
- [ ] **Connected**: References to other research; builds knowledge graph
- [ ] **Clarity**: No unnecessary jargon; frameworks explained simply
- [ ] **Customer Voice**: Direct quotes used to add authenticity
- [ ] **Actionability**: Recommendations are specific and implementable
- [ ] **Context**: HubSpot strategy referenced explicitly

---

## Formatting Guidelines

- Use `##` for main sections, `###` for subsections
- Use `**bold**` for emphasis on key terms and headers
- Use `- bullets` for lists
- Use `> blockquotes` for customer quotes
- Use `code blocks` for specific UI elements or technical terms
- Keep paragraphs short (3-5 sentences max)
- Use clear, active voice

---

## Common Pitfalls to Avoid

1. **Generic Summaries**: Don't just restate what the report says; analyze what it means
2. **Missing Numbers**: Always include specific metrics and data points
3. **Disconnected Recommendations**: Every recommendation must trace to a finding
4. **Ignoring Contradictions**: Address conflicts with other research honestly
5. **Abstract Language**: Use concrete examples and specific scenarios
6. **Isolated Analysis**: Always connect to broader strategic context
7. **Missing Strategic Connection**: Every analysis must tie to HubSpot's Overall Data Strategy

---

## Example Section: The Big Picture

```markdown
## The Big Picture

This research explores how upmarket companies (200+ employees) approach the setup process for HubSpot's CRM and reveals that it's a complex, long-term endeavor fraught with challenges. The findings align with HubSpot's broader data strategy of creating a unified customer platform, but highlight significant gaps in the current implementation process. While HubSpot aims to make sophisticated operations "easy, fast, and unified," the reality for admins is quite different - they face steep learning curves, time pressures, and limited guidance during a process that typically spans 4-6 months to 2-3 years.

The research demonstrates that poor initial setup decisions can lead to months of rework and diminished data quality, directly impacting HubSpot's value proposition as a unified data platform. This connects to the company's strategic transformation toward becoming a complete data platform ("Data Hub") that enables effective data management and activation, but shows that significant improvements are needed in guiding users through the complex initial setup phase.

These findings are critical for SO5 (Win Upmarket) and validate the need for guided setup experiences in the Data Hub strategy. They also challenge the assumption that fast time-to-value applies equally to all segments - upmarket customers require sustained support through extended implementation timelines.
```

---

## Reference

This template should be used for all UXR report analyses to ensure:
- Consistency across the research catalog
- Easy cross-referencing between studies
- Clear strategic connections
- Actionable insights for product and business decisions
- Comprehensive knowledge base for strategic planning
