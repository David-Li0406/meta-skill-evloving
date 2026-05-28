---
name: bug-coordinator
description: Orchestrates the complete bug-fixing workflow from Jira ticket to implementation. Use when starting to fix a bug, managing the bug-fixing pipeline, or checking workflow progress.
license: MIT
compatibility: Requires VS Code Insiders with GitHub Copilot and Atlassian MCP
metadata:
  author: accruent
  version: "1.0"
---

# Bug Coordinator

This skill provides workflow orchestration for the multi-agent bug-fixing pipeline.

## When to Use

- User wants to start fixing a bug
- User provides a Jira ticket key
- User asks about bug-fixing workflow progress
- User wants to resume an in-progress bug fix

## Workflow Overview

```
┌──────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐   ┌──────────────────┐
│  FETCH   │ → │ RESEARCH │ → │ VERIFY  │ → │   RCA   │ → │ PLAN & IMPLEMENT │
│ (Jira)   │   │(Codebase)│   │(Research)│  │(Analysis)│  │   (Fix Bug)      │
└──────────┘   └──────────┘   └─────────┘   └─────────┘   └──────────────────┘
     │              │              │              │               │
     ▼              ▼              ▼              ▼               ▼
bug-context.md  research/    verified-      rca-report.md   impl-plan.md
                *.md         research.md                    + code changes
```

## Specialized Agents

The coordinator delegates to these specialized agents:

| Agent | Phase | Purpose |
|-------|-------|---------|
| Bug Researcher | 2 | Research codebase context |
| Research Verifier | 3 | Verify research accuracy |
| RCA Analyst | 4 | Root cause analysis |
| RCA Verifier | 5 | Verify RCA accuracy |
| Bug Planner | 6 | Create implementation plan |
| Bug Implementer | 7 | Execute the fix |

## Artifact Directory Structure

```
context/bugs/{TICKET-ID}/
├── bug-context.md
├── research/
│   ├── hypothesis.md
│   ├── codebase-research.md
│   └── verified-research.md
├── rca-report.md
├── verified-rca.md
├── implementation-plan.md
└── fix-summary.md
```

## Entry Points

### Start New Bug Fix
```
@Bug Coordinator EMS-1234
```

### Resume Existing Workflow
```
@Bug Coordinator context/bugs/EMS-1234/bug-context.md
```

### Using Prompt Shortcut
```
/start-bug-workflow EMS-1234
```

## Prerequisites

1. **VS Code Setting Enabled:**
   ```json
   "chat.customAgentInSubagent.enabled": true
   ```

2. **Atlassian MCP Connected** (for Jira integration)

3. **All Bug-Fixing Agents Installed:**
   - Bug Researcher
   - Research Verifier
   - RCA Analyst
   - RCA Verifier
   - Bug Planner
   - Bug Implementer

## Human Checkpoints

The workflow requires human approval at critical phases:

1. **Before Planning (Phase 6)**: User reviews verified RCA
2. **Before Implementation (Phase 7)**: User approves implementation plan

These checkpoints ensure the analysis is correct before investing in fix development.

## Error Handling

See the Bug Coordinator agent for detailed error handling patterns for:
- Jira ticket not found
- Missing prerequisite artifacts
- Agent handoff failures
