---
name: research-executor
description: Execute complete 7-phase deep research workflow by delegating to the research-orchestrator-agent. Thin wrapper skill that ensures proper agent invocation with structured research prompts.
---

# Research Executor

## Overview

The Research Executor is a **thin wrapper skill** that delegates research execution to the `research-orchestrator-agent`. It validates inputs, prepares the execution context, and invokes the autonomous orchestrator agent to handle the complete 7-phase deep research workflow.

## When to Use

- User provides a structured research prompt (from question-refiner)
- Need to execute systematic research with multiple agents
- Require comprehensive report with verified citations
- Research involves 3+ subtopics requiring parallel investigation

## Core Responsibilities

1. **Input Validation**: Verify structured prompt completeness
2. **Agent Invocation**: Deploy research-orchestrator-agent with proper context
3. **Progress Monitoring**: Track agent execution and report status
4. **Result Delivery**: Return final research package to user

## Architecture (Post-Refactoring)

```
User Request
     ↓
research-executor skill (this skill - thin wrapper)
     ↓
research-orchestrator-agent (autonomous agent)
     ↓
├── Phase 1: Question Refinement
├── Phase 2: Research Planning
├── Phase 3: Multi-Agent Deployment
├── Phase 4: Source Triangulation
├── Phase 5: Knowledge Synthesis
├── Phase 6: Quality Assurance
└── Phase 7: Output Generation
```

**Key Change**: All orchestration logic has been moved to `research-orchestrator-agent`. This skill only handles:
- Input validation
- Agent deployment
- Error handling at skill level

## Quick Start

```markdown
Execute research using structured prompt:
[STRUCTURED_PROMPT]

The executor will:
1. Validate prompt structure
2. Invoke research-orchestrator-agent
3. Monitor progress
4. Return results from RESEARCH/[topic]/
```

## Input Requirements

**Required**: Structured research prompt with:
- **TASK**: Clear research objective
- **CONTEXT**: Background and significance
- **SPECIFIC_QUESTIONS**: 3-7 concrete sub-questions
- **KEYWORDS**: Search terms
- **CONSTRAINTS**: Timeframe, geography, sources
- **OUTPUT_FORMAT**: Deliverable specifications

**Optional**:
- Research type (deep/quick/custom)
- Quality threshold (default: 8.0)
- Max agents (default: 8)
- Token budget per agent (default: 15k)

## Output Structure

```
RESEARCH/[topic]/
├── README.md
├── executive_summary.md
├── full_report.md
├── data/
│   ├── statistics.md
│   └── ontology/
├── sources/
│   ├── bibliography.md
│   └── source_quality_table.md
├── research_notes/
│   └── agent_findings_summary.md
└── appendices/
    ├── methodology.md
    └── limitations.md
```

## Error Handling

| Error Code | Description | Action |
|------------|-------------|--------|
| **E001** | Incomplete structured prompt | Request missing fields |
| **E002** | Agent deployment failed | Retry with fallback config |
| **E003** | Agent execution timeout | Report partial results |
| **E004** | Quality threshold not met | Trigger refinement (max 2 attempts) |

## Safety Limits

| Limit | Value | Enforced By |
|-------|-------|-------------|
| Max parallel agents | 8 | research-orchestrator-agent |
| Max research time | 90 minutes | research-orchestrator-agent |
| Min quality score | 8.0 | research-orchestrator-agent |
| Max token per agent | 15,000 | research-orchestrator-agent |

## Integration with Agents

**Primary Agent**: `research-orchestrator-agent`
- Handles all 7 phases
- Manages agent deployment
- Enforces quality gates
- Coordinates synthesis and validation

**Supporting Agents** (invoked by orchestrator):
- `got-agent`: For complex research optimization
- `synthesizer-agent`: For findings aggregation
- `red-team-agent`: For quality validation
- `ontology-scout-agent`: For domain reconnaissance
- Multiple research agents (web, academic, verification)

## Key Features

- **Simplified Design**: ~95% of logic moved to orchestrator agent
- **Backwards Compatible**: Same interface for users
- **Better Error Recovery**: Agent-level autonomy improves resilience
- **Clearer Separation**: Skill = invocation, Agent = execution

## Examples

See [examples.md](./examples.md) for usage scenarios.

## Detailed Instructions

See [instructions.md](./instructions.md) for implementation guide.
