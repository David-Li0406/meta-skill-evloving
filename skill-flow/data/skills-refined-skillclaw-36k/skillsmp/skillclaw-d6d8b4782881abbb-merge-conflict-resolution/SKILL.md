---
name: merge-conflict-resolution
description: Use this skill when git merge or rebase fails with conflicts, you see 'unmerged paths' or conflict markers (<<<<<<< =======), or need help resolving conflicted files.
---

# Merge Conflict Resolution

<ROLE>
Git Archaeology Expert + Code Synthesis Specialist. Reputation depends on preserving both branches' intents while creating clean, unified code.
</ROLE>

## Invariant Principles

1. **Synthesis over selection** - Never pick sides. Create a third option combining both intents. `--ours`/`--theirs` = amputation.
2. **Intent preservation** - Both branches represent valuable parallel work. Understand WHY each changed before touching code.
3. **Surgical precision** - Line-by-line edits, never wholesale replacement. More than 20 line changes require explicit approval.
4. **Evidence-based decisions** - Tests exist for reasons. Deleting tested code = breaking expected behavior. Check first.
5. **Consent before loss** - User must explicitly approve any code removal after understanding tradeoffs.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `conflict_files` | Yes | List of files with merge conflicts (from `git status`) |
| `merge_base` | Yes | Common ancestor commit (from `git merge-base`) |
| `ours_branch` | Yes | Current branch name |
| `theirs_branch` | Yes | Branch being merged |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `resolution_plan` | Inline | Per-file synthesis strategy with base/ours/theirs analysis |
| `resolved_files` | Files | Conflict-free source files with synthesized changes |
| `verification_report` | Inline | Test results, lint status, behavior confirmation |

## Reasoning Schema

<analysis>
Before resolving each conflict:
- Merge base state: [original before divergence]
- Ours changed: [what + why]
- Theirs changed: [what + why]
- Tests covering this code: [yes/no, which ones]
- Both intents preservable: [yes/how or no/why]
</analysis>

<reflection>
After resolution:
- Am I synthesizing or selecting? [must be synthesizing]
- Surgical or wholesale? [must be surgical]
- User approved THIS specific change? [not extrapolated from other approval]
- If removing code, what breaks? [tests, features, behaviors]
IF NO to ANY: STOP. Revise synthesis strategy.
</reflection>

Proceed only when synthesis strategy is clear and surgical.

## Conflict Classification

| Type | Files | Resolution |
|------|-------|------------|
| Mechanical | Lock |