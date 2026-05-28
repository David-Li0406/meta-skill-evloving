# PM Domain Skill

Project Manager domain skill providing professional project management methodologies for solopreneurs and teams.

## Overview

- **Name:** faion-project-manager
- **Type:** Domain Skill (orchestrator)
- **Agent:** faion-pm-agent
- **Methodologies:** 46
- **SKILL.md:** 342 lines (optimized)

## Quick Navigation

| Need | Go To |
|------|-------|
| Find the right methodology | SKILL.md > Decision Tree |
| PMBoK 7 overview | SKILL.md > PMBoK 7 Overview |
| PMBoK 8 updates | SKILL.md > PMBoK 8 Updates |
| Quick reference tables | SKILL.md > Quick Reference Tables |
| Detailed methodology | {methodology}.md |

## Core Framework

### Performance Domains (8)

| Domain | Focus |
|--------|-------|
| Stakeholder | Engaging stakeholders effectively |
| Team | Building high-performing teams |
| Development Approach | Selecting predictive/agile/hybrid |
| Planning | Scope, schedule, cost, resources |
| Project Work | Executing and monitoring activities |
| Delivery | Delivering value and outcomes |
| Measurement | Tracking with EVM, metrics, dashboards |
| Uncertainty | Managing risks and complexity |

### Core Principles (12)

Stewardship, Team, Stakeholders, Value, Systems Thinking, Leadership, Tailoring, Quality, Complexity, Risk, Adaptability, Change.

## Directory Structure

```
faion-project-manager/
├── CLAUDE.md              # This file (navigation)
├── SKILL.md               # Decision tree, PMBoK overview, quick reference
├── ref-CLAUDE.md          # References overview (renamed from references/CLAUDE.md)
├── stakeholder-*.md       # Stakeholder domain
├── raci-matrix.md         # Team domain
├── wbs-creation.md        # Planning domain
├── risk-*.md              # Uncertainty domain
├── earned-value-*.md      # Measurement domain
├── jira-*.md              # PM tools
├── linear-*.md
└── ... (46 methodology files total)
```

## Key Methodologies by Domain

| Domain | Methodologies |
|--------|---------------|
| Stakeholder | stakeholder-register, stakeholder-engagement |
| Team | raci-matrix, team-development |
| Planning | wbs-creation, schedule-development, cost-estimation |
| Work | project-integration, communications-management, change-control |
| Delivery | quality-management, benefits-realization |
| Measurement | earned-value-management, performance-domains-overview |
| Uncertainty | risk-register, risk-management |
| Closure | lessons-learned, project-closure |

## PM Tools

| File | Tool | Best For |
|------|------|----------|
| jira-workflow-management.md | Jira | Enterprise, scaled agile |
| clickup-setup.md | ClickUp | All-in-one workspace |
| linear-issue-tracking.md | Linear | Engineering teams |
| github-projects.md | GitHub Projects | Developers |
| azure-devops-boards.md | Azure DevOps | Microsoft ecosystem |
| notion-pm.md | Notion | Knowledge + PM |
| trello-kanban.md | Trello | Simple kanban |

## Integration

| Domain Skill | Integration Point |
|--------------|-------------------|
| faion-sdd | Task planning uses PMBoK scheduling |
| faion-business-analyst | Requirements feed into PM scope |
| faion-product-manager | Product roadmap aligns with project schedule |
| faion-marketing-manager | Campaign planning uses PM methods |

## Usage

Execute methodologies via faion-pm-agent:

```
# Called from faion-net or faion-sdd orchestrators
```

---

*PM Domain Skill v3.0 - 2026-01-21*
