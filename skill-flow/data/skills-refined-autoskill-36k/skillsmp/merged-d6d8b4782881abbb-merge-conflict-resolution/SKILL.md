---
name: merge-conflict-resolution
description: Use this skill when git merge or rebase fails with conflicts, and you need to resolve conflicted files while preserving the intents of both branches.
---

# Merge Conflict Resolution

<ROLE>
Git Archaeology Expert + Code Synthesis Specialist. Reputation depends on preserving both branches' intents while creating clean, unified code.
</ROLE>

## Invariant Principles

1. **Synthesis over selection** - Create a third option combining both intents instead of picking sides.
2. **Intent preservation** - Understand the reasons behind changes in both branches before modifying code.
3. **Surgical precision** - Make line-by-line edits; avoid wholesale replacements without explicit approval.
4. **Evidence-based decisions** - Verify tests before deleting any code to avoid breaking expected behavior.
5. **Consent before loss** - Obtain user approval for any code removal after explaining tradeoffs.

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
| Mechanical | Lock files, changelogs, test fixtures | Auto: regenerate locks, chronological changelog merge |
| Binary | Images, compiled assets | Ask user to choose (synthesis impossible) |
| Complex | Source, configs, docs | 3-way analysis + synthesis required |

## Resolution Workflow

1. **Detect**: List conflicted files, classify mechanical/complex.
2. **Analyze**: Perform a 3-way diff (base vs ours vs theirs) per file.
3. **Auto-resolve**: Resolve mechanical files automatically.
4. **Plan**: Develop a synthesis strategy for complex files and present it for approval.
5. **Execute**: Make surgical edits after obtaining explicit approval.
6. **Verify**: Ensure tests pass, lint is clean, and behavior is preserved.

## Common Patterns

| Pattern | Resolution |
|---------|------------|
| Both modified same function | Merge both changes (e.g., logging AND error handling) |
| Delete vs modify | Apply modification to a new location |
| Same name, different purpose | Rename to distinguish |
| Same name, same purpose | True merge into unified implementation |

## Anti-Patterns

<FORBIDDEN>
- Using `--ours` or `--theirs` on complex files.
- Wholesale replacement (>20 lines) without explicit approval.
- Interpreting partial answers as approval for all changes.
- Deleting tested code without understanding test purpose.
- Binary questions ("ours or theirs?") on complex conflicts.
- Extrapolating approval from ONE aspect to EVERYTHING.
</FORBIDDEN>

## Red Flags (STOP immediately)

| Thought | Reality |
|---------|---------|
| "User said simplify, so use theirs" | Simplify = new third option simpler than EITHER. |
| "Basically the same" | Conflict exists because they differ. |
| "I'll adopt their approach" | `--theirs` with extra steps. |
| "Tests need updating anyway" | Understand test purpose first. |
| "This is cleaner" | Cleaner is not the goal. Preserving both intents is. |

## Question Format

| Bad (binary, over-interpreted) | Good (surgical, specific) |
|--------------------------------|---------------------------|
| "Ours or theirs?" | "What specifically needs to change?" |
| "Is master's better?" | "What from master should we adopt?" |
| "Should I simplify?" | "Which specific lines are unnecessary?" |

Binary questions lead to binary answers, which can result in unapproved wholesale changes.

## Stealth Amputation Trap

Accidental `--theirs` without command:
1. Ask a binary question about complex code.
2. Get a partial answer about ONE aspect.
3. Interpret as approval for EVERYTHING.

Prevention: Approval for ONE aspect is NOT approval for all. Each deletion requires separate verification.

## Acceptable Amputation Cases

Only with explicit user consent after tradeoff explanation:
- Binary files (no synthesis possible).
- Generated files (will regenerate).
- User explicitly requests after understanding loss.

## Plan Template

```
## Resolution: [filename]
**Base:** [original state]
**Ours:** [change + intent]
**Theirs:** [change + intent]
**Synthesis:** [how combining both]
**Risk:** [edge cases, concerns]
```

## Self-Check

Before completing resolution:
- [ ] All conflicts resolved (no `<<<<<<<` markers remain).
- [ ] Tests pass (both ours and theirs functionality).
- [ ] Lint/build clean.
- [ ] No tested code deleted without test updates.
- [ ] Behavior from both branches present.
- [ ] User approved specific changes (not extrapolated).
- [ ] Synthesis achieved, not selection.

If ANY unchecked: STOP and fix.