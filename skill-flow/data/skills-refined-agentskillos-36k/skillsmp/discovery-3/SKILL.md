---
name: discovery
description: Market research, feasibility analysis, and context gathering workflows for product discovery phase. Use when conducting market research, competitive analysis, stakeholder interviews, technical feasibility assessment, or gathering discovery-phase context before ideation and design. Used in PDLC workflow for Market_And_Feasibility_Research and Stakeholder_Alignment nodes.
---

# Discovery Skill

You are conducting discovery research to gather market, stakeholder, and technical context before product design. This skill provides systematic approaches to market research, feasibility analysis, and stakeholder engagement.

## Available Workflows

### 1. Market Research (`workflows/market-research.md`)
Conduct competitive analysis, market sizing, and opportunity assessment.
- **Use for**: Understanding market landscape, competitors, positioning
- **Output**: D02-market-research.md artifact
- **Agent**: Researcher

### 2. Feasibility Analysis (`workflows/feasibility-analysis.md`)
Assess technical, operational, and business feasibility of proposed solutions.
- **Use for**: Risk assessment, constraint analysis, viability evaluation
- **Output**: D05-feasibility-report.md artifact
- **Agent**: Architect (technical), BusinessAnalyst (business)

### 3. Stakeholder Research (`workflows/stakeholder-research.md`)
Gather stakeholder insights, interview users, document requirements.
- **Use for**: User research, stakeholder alignment, requirements gathering
- **Output**: D06-stakeholder-insights.md artifact
- **Agent**: BusinessAnalyst

## Workflow Selection

**Early PDLC Phase (after vision, before ideation)**:
1. Start with `market-research` to understand landscape
2. Use `stakeholder-research` to gather user/stakeholder needs
3. Complete with `feasibility-analysis` to assess viability

**Feature Refinement Phase**:
1. Use `stakeholder-research` for feature-specific feedback
2. Use `feasibility-analysis` for technical risk assessment

## Context Resources

- **research-techniques.md** - Interview templates, survey design, competitive analysis frameworks
- **feasibility-frameworks.md** - Technical feasibility checklists, risk assessment matrices

## Tools Required

- **WebSearch** - Market research, competitor analysis, technology research
- **Read** - Review existing documentation and context
- **Write** - Create discovery artifacts
- **Grep/Glob** - Search existing codebase for technical feasibility

## Integration Points

**Feeds into**:
- `brainstorming` - Market insights inform solution ideation
- `specification-writing` - Research findings shape PRD content
- `architecture` - Feasibility reports guide architecture decisions

**Used by agents**:
- Researcher (market research, competitive analysis)
- BusinessAnalyst (stakeholder research, requirements)
- Architect (technical feasibility assessment)

## Output Standards

All discovery artifacts must:
1. Be evidence-based with sources cited
2. Include concrete findings, not speculation
3. Provide actionable insights and recommendations
4. Document assumptions and limitations
5. Be stored in `/docs/workflow/artifacts/`
