---
name: foundry-research
description: AI-powered research skill with five workflows - chat (single-model conversation), consensus (multi-model synthesis), thinkdeep (systematic investigation), ideate (creative brainstorming), and deep (multi-phase web research). Supports persistent threads and research sessions.
---

# Research Skill

## Overview

- **Purpose:** AI-powered research with multiple reasoning strategies
- **Scope:** Five workflows, persistent thread and session management
- **Entry:** `Skill(foundry:foundry-research)` or user invocation

### Flow

> `[x?]`=decision `(GATE)`=user approval `→`=sequence

```
- **Entry** → [route?]
  - [explicit?] → Dispatch → Execute → Persist thread → Response + thread_id
  - [thread-id?] → Resume → Dispatch → Execute → Persist thread → Response + thread_id
  - [research-id?] → SessionMgmt
  - [sessions?] → ListSessions
  - [no args?] → (GATE: choose workflow) → AutoRoute → Dispatch → Execute → Persist thread → Response + thread_id
  - [deep?] → Start → Poll → Report (background execution)
```

**CRITICAL for `deep` workflow:** Read [references/deep-research-workflow.md](./references/deep-research-workflow.md) before execution. Contains required polling strategy and MCP parameters.

### Deep Research Polling Protocol (MANDATORY)

**BEFORE EVERY status check, you MUST:**
1. Generate user-facing text about current progress
2. Do NOT call deep-research-status immediately after another MCP tool
3. Track your check count (max 5)

| Check # | What to Say |
|---------|-------------|
| 1 | "Research underway. Currently in {phase} phase..." |
| 2-3 | "Progress: {queries_completed}/{total} queries done..." |
| 4 | "Still working ({elapsed} minutes)..." |
| 5 | Stop polling, use AskUserQuestion with options |

**Stall Detection**: Only after `elapsed_ms > 300000` AND no progress change.

**NO INDEPENDENT RESEARCH**: While deep research is running, do NOT use WebSearch, WebFetch, or other research tools. The deep research workflow handles all web gathering - doing your own searches is redundant and wastes resources.

## MCP Tooling

| Router | Actions |
|--------|---------|
| `research` | `chat`, `consensus`, `thinkdeep`, `ideate`, `deep-research`, `deep-research-status`, `deep-research-report`, `deep-research-list`, `deep-research-delete`, `thread-list`, `thread-get`, `thread-delete`, `node-execute`, `node-record`, `node-status`, `node-findings` |

## MCP Contract

| Action | Required | Optional | Errors |
|--------|----------|----------|--------|
| `chat` | `prompt` | `thread_id`, `provider_id` | `THREAD_NOT_FOUND` |
| `consensus` | `prompt` | `providers`, `strategy` | `NO_MODELS_AVAILABLE` |
| `thinkdeep` | `prompt` | `thread_id`, `depth` | `MAX_DEPTH_EXCEEDED` |
| `ideate` | `prompt` | `thread_id`, `phase` | `INVALID_PHASE` |
| `deep-research` | `query` | `max_iterations`, `max_sub_queries`, `follow_links` | `RESEARCH_TIMEOUT` |
| `deep-research-status` | `research_id` | - | `RESEARCH_NOT_FOUND` |
| `deep-research-report` | `research_id` | - | `RESEARCH_NOT_FOUND` |
| `deep-research-list` | - | `limit`, `completed_only` | - |
| `deep-research-delete` | `research_id` | - | `RESEARCH_NOT_FOUND` |
| `thread-*` | `thread_id` | `limit` | `THREAD_NOT_FOUND` |
| `node-status` | `spec_id`, `research_node_id` | - | `NODE_NOT_FOUND` |
| `node-execute` | `spec_id`, `research_node_id` | `prompt` | `NODE_NOT_FOUND`, `INVALID_TYPE` |
| `node-record` | `spec_id`, `research_node_id`, `result` | `summary`, `key_insights`, `recommendations`, `confidence` | `NODE_NOT_FOUND` |
| `node-findings` | `spec_id`, `research_node_id` | - | `NODE_NOT_FOUND`, `NO_FINDINGS` |

## Workflow Selection

| Signal | Workflow |
|--------|----------|
| Follow-up, iteration | `chat` |
| Multiple perspectives | `consensus` |
| Complex problem | `thinkdeep` |
| Brainstorming | `ideate` |
| Comprehensive research, multiple sources | `deep` |

## User Gates

- No args: workflow selection
- Ambiguous: clarify before auto-route
- Consensus: strategy selection
- Ideate: phase transition
- Deep: progress updates during background execution

## Output Formats

| Workflow | Response |
|----------|----------|
| `chat` | `{response, thread_id, model}` |
| `consensus` | `{responses[], synthesis, strategy}` |
| `thinkdeep` | `{findings[], confidence, thread_id}` |
| `ideate` | `{ideas[], phase, selected[]}` |
| `deep` | `{research_id, status, report{summary, findings[], sources[]}}` |

## References

- [Chat](./references/chat-workflow.md) | [Consensus](./references/consensus-workflow.md) | [Deep](./references/deep-research-workflow.md)
- [ThinkDeep](./references/thinkdeep-workflow.md) | [Ideate](./references/ideate-workflow.md)
- [Sessions](./references/session-management.md) | [Auto-Route](./references/auto-routing.md)
