---
name: jules-pr-manager
description: Use this skill to manage the lifecycle of PRs created by Google's Jules agent, including batch investigation, reverse-order processing, and tiered decision presentation.
---

# Skill body

## Overview

This skill orchestrates a **Batch-Analyze-Present-Execute** loop for managing PRs. It prioritizes finishing work (merging) before starting new work (vetting).

⚠️ **MANDATORY**: Use the bash scripts in `.gemini/skills/jules-pr-manager/` for ALL interactions. Do not assemble `gh` commands manually.

## Workflow

### Step 1: Gather Data

Run `./summary.sh` to get an overview of all open PRs and categorize them:

| Condition | Category |
|:----------|:---------|
| No labels | Unvetted (needs review) |
| `jules:copilot-review` + Copilot APPROVED + CI SUCCESS | Merge candidate |
| `jules:copilot-review` + Copilot commented | Needs feedback relay |
| `jules:copilot-review` + CI FAILURE | Needs CI fix |
| `jules:changes-requested` | Waiting on Jules |
| `mergeable: CONFLICTING` | Has conflicts |

**Duplicate Detection**: Use `./diff.sh <id1> [id2]` to compare PRs for duplicates.

### Step 2: Present Findings to User

Summarize your findings:
- Total number of PRs and how many are Jules PRs
- List of merge candidates
- Clusters of potential duplicates
- PRs needing attention (CI failures, stalled, conflicts)

### Step 3: Process One Decision at a Time

For each PR requiring action, present:

1. **The PR**: Number, title, what it does
2. **Your Analysis**: Is it a duplicate? Worth merging? Any concerns?
3. **Your Recommendation**: What you suggest and why
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

### Step 4: Execute Actions

Process PRs in this order (closest to completion first):

1. **Merge Candidates**:
   - **Definition**: PRs vetted, Copilot Approved, CI Passed, No Conflicts.
   - **MANDATORY**: Present a detailed summary of the PR to the User and wait for explicit confirmation.
   - **Action**: Run `./merge.sh <ID> ["message"]`.

2. **Copilot Review**:
   - If Copilot left comments, run `./request-changes.sh <ID> "Refined Copilot comments..."` and update labels accordingly.
   - If CI Failed, run `./request-changes.sh <ID> "Fix CI failures: <details>"`.

3. **Transition to Copilot Review**:
   - If `jules:vetted` AND CI Passed AND NOT `jules:copilot-review`, run `./mark-ready.sh <ID>` and label the PR for Copilot review.

4. **Changes Requested**:
   - If Jules responded with new commits/comments, evaluate and either move to Copilot Review or request further changes.

5. **New PRs**:
   - For unvetted PRs, run `./diff.sh <ID1> <ID2>` to compare and determine the best implementation.

### Important Notes

- Always ensure user approval is obtained before merging or closing PRs.
- Maintain clear communication with the user throughout the process to facilitate informed decision-making.