# Business Analyst Skill

## Overview

BA Domain Skill for professional business analysis. Orchestrates business analysis activities across 6 Knowledge Areas with 24 methodologies.

**Agent:** `faion-ba-agent`

## Quick Decision: What BA Task?

| If you need to... | Use Knowledge Area | Key Methodology |
|-------------------|-------------------|-----------------|
| Plan BA approach, stakeholders | KA-1 Planning | ba-planning, stakeholder-analysis |
| Gather requirements | KA-2 Elicitation | elicitation-techniques |
| Track/prioritize requirements | KA-3 Lifecycle | requirements-traceability, requirements-prioritization |
| Analyze current/future state | KA-4 Strategy | strategy-analysis |
| Model/document requirements | KA-5 Analysis | use-case-modeling, user-story-mapping |
| Evaluate solution | KA-6 Evaluation | solution-assessment |

**Full decision trees:** See [SKILL.md](SKILL.md#decision-trees)

## Directory Structure

```
faion-business-analyst/
├── SKILL.md                          # Main skill
├── CLAUDE.md                         # Navigation (this file)
├── ref-CLAUDE.md                     # References overview
├── ba-planning.md
├── stakeholder-analysis.md
├── elicitation-techniques.md
├── requirements-documentation.md
├── requirements-traceability.md
├── strategy-analysis.md
├── requirements-lifecycle.md
├── solution-assessment.md
├── business-process-analysis.md
├── data-analysis.md
├── decision-analysis.md
├── use-case-modeling.md
├── user-story-mapping.md
├── acceptance-criteria.md
├── requirements-validation.md
├── requirements-prioritization.md
├── interface-analysis.md
├── knowledge-areas-overview.md
├── methodologies-detail.md           # Governance, risk, change templates
├── ai-enabled-business-analysis.md
├── agile-ba-frameworks.md
├── process-mining-automation.md
├── data-driven-requirements.md
├── modern-ba-framework.md
├── ba-strategic-partnership.md
└── ba-trends-summary.md
```

## Key Files

| File | Description | Lines |
|------|-------------|-------|
| SKILL.md | Main skill: decision trees, 6 KAs, methodology table | ~370 |
| methodologies-detail.md | Detailed templates: governance, risk, change | ~450 |
| *.md (26 files) | Individual methodology files | ~250 each |

## 6 Knowledge Areas Summary

| # | Knowledge Area | Focus | Key Outputs |
|---|----------------|-------|-------------|
| 1 | BA Planning & Monitoring | Approach, stakeholders, governance | BA approach, stakeholder map |
| 2 | Elicitation & Collaboration | Gather and confirm information | Elicitation results |
| 3 | Requirements Lifecycle | Trace, maintain, prioritize, approve | Traced/approved requirements |
| 4 | Strategy Analysis | Current/future state, risks, change | Change strategy |
| 5 | Requirements Analysis & Design | Model, verify, validate, recommend | Solution recommendation |
| 6 | Solution Evaluation | Measure, assess, improve | Value improvement recommendations |

## Methodology Quick Reference

### Core (KA-1 to KA-3)

| Methodology | When to Use |
|-------------|-------------|
| ba-planning | Define BA approach |
| stakeholder-analysis | Map stakeholders |
| elicitation-techniques | Gather requirements |
| requirements-traceability | Track relationships |
| requirements-prioritization | Rank requirements |
| requirements-lifecycle | Manage over time |

### Analysis (KA-4 to KA-5)

| Methodology | When to Use |
|-------------|-------------|
| strategy-analysis | Current/future state |
| use-case-modeling | User-system interactions |
| user-story-mapping | Agile requirements |
| business-process-analysis | Process flows (BPMN) |
| data-analysis | Data requirements |
| decision-analysis | Business rules |
| interface-analysis | System interfaces |
| acceptance-criteria | Done criteria (BDD) |
| requirements-validation | Validate vs goals |
| requirements-documentation | Formal documentation |

### Evaluation (KA-6)

| Methodology | When to Use |
|-------------|-------------|
| solution-assessment | Evaluate performance |

## Modern BA (2025-2026)

| Topic | File |
|-------|------|
| AI-Enabled BA | ai-enabled-business-analysis.md |
| Agile BA | agile-ba-frameworks.md |
| Process Mining | process-mining-automation.md |
| Data-Driven Requirements | data-driven-requirements.md |
| Modern BA Framework | modern-ba-framework.md |

## Usage

```
# Via faion-ba-agent for methodology execution
# Called from faion-net or faion-sdd orchestrators
```

## References

- Business Analysis Framework Guide (BABOK)
- BA industry standards
- Certifications: ECBA, CCBA, CBAP, AAC
