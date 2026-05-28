---
name: Jules PR Manager
description: Manage Google Jules PR lifecycle - batch investigation, reverse-order processing, and tiered decision presentation.
version: 2.7.0
---

# Jules PR Manager

## Overview

**Manage the lifecycle of PRs created by Google's Jules agent (Gemini 2.5 Pro).**

This skill orchestrates a **Batch-Analyze-Present-Execute** loop. It strictly prioritizes **finishing work** (merging) before **starting work** (vetting).

⚠️ **MANDATORY**: You MUST use the bash scripts in `.gemini/skills/jules-pr-manager/` for ALL interactions. Do not assemble `gh` commands manually.

## State Machine (The Workflow)

Process PRs in this order (closest to completion first):

### 1. Merge Candidates (The Exit)

- **Definition**: PRs vetted, Copilot Approved, CI Passed, No Conflicts.
- **MANDATORY**: Before running merge, you MUST present a detailed summary of the PR to the User and wait for explicit confirmation.
- **Action**: Run `./merge.sh <ID> ["message"]`.

### 2. Copilot Review (`jules:copilot-review`)

- **Condition: Copilot left comments**:
  - Run `./request-changes.sh <ID> "Refined Copilot comments..."`.
  - Run `./label.sh <ID> remove jules:copilot-review`.
  - Run `./label.sh <ID> add jules:changes-requested`.
- **Condition: CI Failed**:
  - Run `./request-changes.sh <ID> "Fix CI failures: <details>"`.
  - Run `./label.sh <ID> remove jules:copilot-review`.
  - Run `./label.sh <ID> add jules:changes-requested`.
- **Condition: Approved**: Move to Merge Candidate.

### 3. Transition to Copilot Review (CRITICAL STEP)

- **Condition**: `jules:vetted` AND CI Passed AND NOT `jules:copilot-review`.
- **MANDATORY ACTION**:
  1. Run `./mark-ready.sh <ID>`. **(This converts Draft to PR; Copilot will ignore Drafts.)**
  2. Run `./label.sh <ID> add jules:copilot-review`.
- **Why**: This is the primary trigger for the automated audit pipeline. If you skip `mark-ready.sh`, the PR will stall indefinitely in the Copilot queue.

### 4. Changes Requested (`jules:changes-requested`)

- **Condition: Jules Responded (New commits/comments)**:
  - If fixes are good -> Move to "Transition to Copilot Review".
  - If fixes are bad -> Run `./request-changes.sh <ID> "Still needs work: <details>"`.
- **Condition: Stalled (>30m silence)**:
  - Run `./request-changes.sh <ID> "Ping @jules - status update?"`.

### 5. New PRs (Unvetted)

- **Action 1: Duplicate Detection**:
  - Run `./diff.sh <ID1> <ID2>` to compare.
  - Pick the best implementation (the "Keeper").
  - Run `./request-changes.sh <Keeper_ID> "Incorporate good parts from #<Loser_ID>..."`.
  - Run `./close.sh <Loser_ID> "Duplicate of #<Keeper_ID>"`.
- **Action 2: Vetting**:
  - Review code. If worth doing:
    - Run `./label.sh <ID> add jules:vetted`.
    - If CI is already passing, move to "Transition to Copilot Review".
  - If NOT worth doing:
    - Run `./close.sh <ID> "Rationale for rejection"`.

---

## Execution Model

### 1. Batch Investigation

- Run `./investigate.sh` to get a consolidated JSON (check `lastInstructionAcknowledged` field to confirm Jules has read feedback). of all Jules PRs and their filtered activity timelines.
- Log the status and plan for every PR before presenting.

### 2. Decision Collection

- Group actions into: **Merge Decisions**, **Vetting Decisions**, and **Trivial Batch** (label changes, automated request-changes).

### 3. Tiered Presentation

Present decisions to the User in this EXACT order:

1. **Merge Decisions**: One by one. You MUST provide a detailed summary of each PR (logic changes, impact, vetting results) and request explicit confirmation before merging.
2. **Vetting Requests**: One by one (include deep opinion on rationale/impact).
3. **Trivial Batch**: As a numbered list for bulk approval.

### 4. Batch Execution

- Execute all approved actions in one turn. Use `&` to run script calls in the background where appropriate to improve performance.

---

## Automation Scripts Reference

| Script                                  | Purpose                                | Review Type       | Tags @jules |
| :-------------------------------------- | :------------------------------------- | :---------------- | :---------- |
| `./investigate.sh`                      | One-shot fetch of all PRs + timelines. | N/A               | No          |
| `./view-pr.sh <id>`                     | Full unfiltered JSON for one PR.       | N/A               | No          |
| `./diff.sh <id1> [id2]`                 | View diff or compare two PRs.          | N/A               | No          |
| `./request-changes.sh <id> <msg>`       | Demand work/fixes or nudge.            | `REQUEST_CHANGES` | **Yes**     |
| `./merge.sh <id> [msg]`                 | Finalize and merge.                    | `APPROVE`         | **Yes**     |
| `./close.sh <id> [msg]`                 | Close the PR.                          | N/A               | No          |
| `./mark-ready.sh <id>`                  | Trigger Copilot (gh pr ready).         | N/A               | No          |
| `./label.sh <id> <add\|remove> <label>` | Manage state labels.                   | N/A               | No          |

---

## GitHub Labels Reference

- `jules:vetted`: Approved for processing.
- `jules:copilot-review`: Waiting for Copilot.
- `jules:changes-requested`: Waiting for Jules (Fixes/Comments).
- `jules:agent-stalled`: >30m silence.
- `jules:merge-conflicts`: Git conflict.

## Agent Search Optimization (ASO)

**Keywords**: jules, pr manager, scripts, automation, batch, merge, vetting, duplicates, tiered presentation
