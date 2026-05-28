# faion-researcher Skill

## Overview

Research domain skill for product/startup development. Orchestrates idea discovery, market research, competitor analysis, persona building, pricing research, problem validation, niche evaluation, project naming, and trend analysis.

**Invocation:** `/faion-researcher`

**Agents:** 2
- `faion-research-agent` (opus) - Research orchestrator with 9 modes
- `faion-domain-checker-agent` (sonnet) - Domain availability verification

**Methodologies:** 32 (semantic naming)

**Tools:** Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite

---

## Research Modes

| Mode | Output | Description |
|------|--------|-------------|
| ideas | 15-20 candidates | Idea generation using 7 Ps, Paul Graham questions |
| market | market-research.md | TAM/SAM/SOM analysis, market trends |
| competitors | competitive-analysis.md | Competitor mapping, feature gaps |
| pains | pain-points.md | Reddit, forums, reviews mining |
| personas | user-personas.md | Demographics, JTBD, behaviors |
| validate | problem-validation.md | Evidence gathering for problem existence |
| niche | niche-evaluation.md | Market size, competition, barriers |
| pricing | pricing-research.md | Pricing models, benchmarking |
| names | name-candidates.md | Project naming with domain check |

---

## Directory Structure

```
faion-researcher/
├── SKILL.md                    # Full skill specification
├── CLAUDE.md                   # This file
├── methodologies-detail.md     # Full methodology templates (~1500 lines)
├── *.md                        # 32 methodologies (semantic naming)
└── ref-*.md                    # Reference materials (AI tools, best practices)
```

---

## Key Workflows

### Idea Discovery
```
Gather Context → Generate Ideas → User Selection → Pain Research → Niche Evaluation → Present Results
```

### Product Research
```
Parse project → Read constitution.md → Select modules → Run agents sequentially → Write summary
```

### Project Naming
```
Gather Concept → Generate 15-20 Names → User Selection → Check Domains → Present Results → Update constitution
```

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File |
|--------|-------------|
| Idea Discovery | idea-validation.md |
| Market Research | market-research.md |
| Competitors | competitive-analysis.md |
| Personas | user-personas.md |
| Validation | problem-validation.md |
| Pricing | pricing-research.md |
| Summary | executive-summary.md |
| Naming | Updates constitution.md |

---

## Quick Reference

### Invoke Idea Generation
```python
Task(
    subagent_type="faion-research-agent (mode: ideas)",
    prompt="Generate ideas using 7 Ps framework"
)
```

### Invoke Market Research
```python
Task(
    subagent_type="faion-research-agent (mode: market)",
    prompt="Research TAM/SAM/SOM for {product}"
)
```

### Invoke Competitor Analysis
```python
Task(
    subagent_type="faion-research-agent (mode: competitors)",
    prompt="Analyze competitors for {product}"
)
```

---

## Related Skills

- `faion-sdd` - SDD workflow orchestrator
- `faion-product-manager` - Product planning, roadmaps
- `faion-marketing-manager` - GTM strategy, landing pages
- `faion-ux-ui-designer` - User research, journey mapping

---

*faion-researcher v1.1*
