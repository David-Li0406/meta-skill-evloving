---
name: jules-pr-manager
description: Manage the lifecycle of Google Jules PRs through batch investigation, decision presentation, and execution of actions based on user input.
---

# Jules PR Manager

## Overview

This skill orchestrates a **Batch-Analyze-Present-Execute** loop for managing PRs created by Google's Jules agent (Gemini 2.5 Pro). It prioritizes finishing work (merging) before starting new tasks (vetting).

⚠️ **MANDATORY**: Use the bash scripts in `.gemini/skills/jules-pr-manager/` for all interactions. Do not assemble `gh` commands manually.

## Workflow

### Step 1: Gather Data

Run `./summary.sh` to categorize PRs:

| Condition | Category |
|:----------|:---------|
| No labels | Unvetted (needs review) |
| `jules:copilot-review` + Copilot APPROVED + CI SUCCESS | Merge candidate |
| `jules:copilot-review` + Copilot commented | Needs feedback relay |
| `jules:copilot-review` + CI FAILURE | Needs CI fix |
| `jules:changes-requested` | Waiting on Jules |
| `mergeable: CONFLICTING` | Has conflicts |

**Duplicate Detection**: PRs with overlapping `files` arrays are likely duplicates. Use `./diff.sh <id1> [id2]` to confirm.

### Step 2: Present Findings to User

Summarize findings:
- Total PRs and how many are Jules PRs
- Merge candidates
- Duplicate clusters
- PRs needing attention (CI failures, stalled, conflicts)

### Step 3: Process Decisions

For each PR requiring action, present:

1. **The PR**: Number, title, what it does
2. **Your Analysis**: Is it a duplicate? Worth merging? Any concerns?
3. **Your Recommendation**: Suggested action and rationale
4. **Options**: Clear choices for the user

Example presentation:
```
**#796: Add indexes for issue severity and priority**

Analysis: This adds DB indexes for faster filtering. Appears to be
a duplicate of #794 (same files modified). #796 is newer.

Recommendation: Close #794 as duplicate, keep #796.

Options:
A) Close #794, keep #796 (recommended)
B) Close #796, keep #794
C) Keep both (explain why)
D) Close both
E) Need more info (I'll run detail.sh)
```

### Step 4: Execute Approved Actions

Only after user approval:
- Run the appropriate script(s)
- Report the result
- Move to the next decision

## Execution Model

### Batch Investigation

Run `./investigate.sh` to get a consolidated JSON of all Jules PRs and their activity timelines. Log the status and plan for every PR before presenting.

### Decision Collection

Group actions into: **Merge Decisions**, **Vetting Decisions**, and **Trivial Batch** (label changes, automated request-changes).

### Tiered Presentation

Present decisions in this order:
1. **Merge Decisions**: Provide a detailed summary and request explicit confirmation before merging.
2. **Vetting Requests**: Include deep opinion on rationale/impact.
3. **Trivial Batch**: As a numbered list for bulk approval.

### Batch Execution

Execute all approved actions in one turn. Use `&` to run script calls in the background where appropriate to improve performance.

## Automation Scripts Reference

| Script                                  | Purpose                                |
| :-------------------------------------- | :------------------------------------- |
| `./summary.sh`                          | Overview of ALL open PRs (run first) |
| `./detail.sh <id>`                     | Deep dive on single PR                |
| `./diff.sh <id1> [id2]`                | Compare PRs for duplicates            |
| `./request-changes.sh <id> <msg>`      | Request fixes from Jules              |
| `./merge.sh <id> [msg]`                | Merge (USER APPROVAL REQUIRED)        |
| `./close.sh <id> [msg]`                | Close PR (USER APPROVAL REQUIRED)     |
| `./mark-ready.sh <id>`                 | Convert Draft → PR                    |
| `./label.sh <id> <add\|remove> <label>`| Manage labels                         |

## GitHub Labels Reference

| Label | Meaning |
|:------|:--------|
| `jules:vetted` | Approved for processing |
| `jules:copilot-review` | Waiting for Copilot |
| `jules:changes-requested` | Waiting for Jules fixes |
| `jules:agent-stalled` | >30m silence from Jules |
| `jules:merge-conflicts` | Has git conflicts |

## Agent Search Optimization (ASO)

**Keywords**: jules, pr manager, scripts, automation, batch, merge, vetting, duplicates, tiered presentation