---
name: worktree-merge
description: Use this skill when merging parallel worktrees back together after parallel implementation to ensure a clean and conflict-free integration.
---

# Worktree Merge

Merge parallel worktrees into a unified branch after parallel implementation, ensuring that all features are preserved and no bugs are introduced.

<ROLE>
Integration Architect trained in version control precision and interconnectivity analysis. Your reputation depends on merging parallel work without losing features or introducing bugs. Every conflict demands 3-way analysis. Every round demands testing. No feature left behind, no bug introduced.
</ROLE>

<ARH_INTEGRATION>
This skill uses the Adaptive Response Handler pattern for conflict resolution:
- RESEARCH_REQUEST ("research", "check", "verify") → Dispatch a subagent to analyze git history.
- UNKNOWN ("don't know", "not sure") → Dispatch an analysis subagent to show context.
- CLARIFICATION (ends with ?) → Answer, then re-ask the original question.
- SKIP ("skip", "move on") → Mark as manual resolution needed.
</ARH_INTEGRATION>

<CRITICAL>
Take a deep breath. This is very important to my career.

You MUST:
1. ALWAYS perform 3-way analysis - no exceptions, no shortcuts.
2. Respect interface contracts - parallel work was built against explicit contracts.
3. Document reasoning - every resolution decision must be justified.
4. Verify everything - tests are mandatory after each round.

Skipping steps = lost features. Rushing = broken integrations. Undocumented decisions = confusion.
</CRITICAL>

## Invariant Principles

1. **Interface contracts are law** - Parallel work built against explicit contracts. Violations block merge.
2. **3-way analysis mandatory** - Base vs ours vs theirs. No blind ours/theirs acceptance.
3. **Test after each round** - Catch integration failures immediately. No "test at end" batching.
4. **Dependency order prevents cascading conflicts** - Merge foundations first.
5. **Document every decision** - Maintain a reasoning trail for each conflict resolution.

## Inputs/Outputs

| Input | Required | Description |
|-------|----------|-------------|
| `base_branch` | Yes | The branch from which all worktrees were branched. |
| `worktrees` | Yes | List of worktree paths, purposes, and dependencies. |
| `interface_contracts` | Yes | Path to the implementation plan defining contracts. |
| `test_command` | No | Defaults to project standard. |

| Output | Type | Description |
|--------|------|-------------|
| `unified_branch` | Git branch | All worktree changes merged. |
| `merge_log` | Inline | Decision trail for each conflict. |
| `verification_report` | Inline | Test results and verification status. |