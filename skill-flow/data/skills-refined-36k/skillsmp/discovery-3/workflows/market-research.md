# Market Research Workflow

Conduct comprehensive market research including competitive analysis, market sizing, and opportunity assessment.

## When to Use

- After vision statement is defined (D01-vision-statement.md exists)
- Before solution ideation begins
- During PDLC workflow at Market_And_Feasibility_Research node
- When product positioning needs validation

## Prerequisites

**Required artifacts**:
- D01-vision-statement.md - Product vision and scope
- D02-success-criteria.md - Success metrics and goals

**Optional context**:
- D03-solution-candidates.md - If solution ideas already exist
- D04-prioritized-ideas.md - If priorities are set

## Workflow Steps

### 1. Review Vision and Scope

Read the vision statement to understand:
- Target market and customer segments
- Problem being solved
- Key differentiators
- Success criteria

### 2. Identify Competitors

Use WebSearch to find:
- Direct competitors (same problem, same solution approach)
- Indirect competitors (same problem, different approach)
- Adjacent solutions (related problem space)

For each competitor, document:
- Product name and website
- Key features and capabilities
- Pricing model
- Target audience
- Strengths and weaknesses

### 3. Analyze Market Size

Research and estimate:
- Total Addressable Market (TAM)
- Serviceable Available Market (SAM)
- Serviceable Obtainable Market (SOM)

Include:
- Market sizing methodology and sources
- Growth trends and projections
- Market segmentation

### 4. Assess Market Trends

Identify relevant trends:
- Technology trends affecting the space
- Regulatory or compliance changes
- User behavior shifts
- Industry consolidation or disruption

### 5. Evaluate Positioning Opportunity

Analyze:
- White space opportunities (unmet needs)
- Differentiation potential
- Market entry barriers
- Go-to-market considerations

### 6. Document Findings

Create D02-market-research.md with structure:

```markdown
# Market Research Report

## Executive Summary
[Key findings in 3-5 bullet points]

## Market Overview
### Market Size
- TAM: [value and source]
- SAM: [value and source]
- SOM: [estimated share]

### Market Trends
[Key trends affecting this space]

## Competitive Landscape

### Direct Competitors
[For each major competitor]
- **[Competitor Name]** ([website])
  - Features: [key capabilities]
  - Pricing: [model and tiers]
  - Strengths: [what they do well]
  - Weaknesses: [gaps and limitations]

### Indirect Competitors
[Similar format for adjacent solutions]

### Competitive Matrix
| Feature | Our Vision | Competitor A | Competitor B | Competitor C |
|---------|-----------|-------------|-------------|-------------|
| [Key feature 1] | [our approach] | [their approach] | ... | ... |

## Positioning Opportunity

### White Space Analysis
[Unmet needs in the market]

### Differentiation Strategy
[How we differentiate from competitors]

### Market Entry Considerations
[Barriers, challenges, opportunities]

## Recommendations

1. [Actionable recommendation based on findings]
2. [Another recommendation]
3. [...]

## Sources
- [List all sources with URLs]
```

### 7. Store Artifact

Save the completed research report:
```bash
/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/D02-market-research.md
```

## Success Criteria

Research is complete when:
- At least 3-5 competitors are analyzed in depth
- Market sizing includes methodology and sources
- Competitive matrix compares key dimensions
- Positioning opportunities are clearly identified
- Recommendations are specific and actionable
- All claims are supported by cited sources

## Next Steps

After market research:
- Workflow advances to Stakeholder_Alignment or Ideation_Brainstorming
- Findings inform solution ideation and feature prioritization
- Competitive insights shape product differentiation
- Market data validates business case

## Related Workflows

- `feasibility-analysis.md` - Technical viability assessment
- `stakeholder-research.md` - User and stakeholder insights
- `brainstorming/workflows/*` - Solution ideation using market insights
