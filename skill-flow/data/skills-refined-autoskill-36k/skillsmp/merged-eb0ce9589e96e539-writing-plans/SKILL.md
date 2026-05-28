---
name: writing-plans
description: Use this skill when you have a spec or requirements for a multi-step task, before touching code.
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, and how to test it. Give them the whole plan as bite-sized tasks. Follow principles of DRY, YAGNI, TDD, and frequent commits.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Invariant Principles

1. **Zero-Context Assumption** - Engineer reading plan knows nothing about codebase, toolset, or domain.
2. **Atomic Tasks** - Each step is one action (2-5 min): write test, run test, implement, verify, commit.
3. **Complete Specification** - Full code, exact paths, expected outputs; never vague instructions or placeholders.
4. **TDD Flow** - RED (failing test) -> GREEN (minimal pass) -> commit; repeat.
5. **Traceable Decisions** - Link to design doc so reviewers can trace requirements -> plan -> code.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Design document OR requirements | Yes | Spec defining what to build. |
| Codebase access | Yes | Ability to inspect existing patterns. |
| Target feature name | Yes | Short identifier for plan filename. |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Implementation plan | File | `docs/plans/YYYY-MM-DD-<feature>.md` |
| Execution guidance | Inline | Choice of subagent-driven vs parallel session. |

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Source Design Doc:** [path or "None - requirements provided directly"]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Remember
- Exact file paths always.
- Complete code in plan (not "add validation").
- Exact commands with expected output.
- Reference relevant skills with @ syntax.
- DRY, YAGNI, TDD, frequent commits.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration.
2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints.

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development.
- Stay in this session.
- Fresh subagent per task + code review.

**If Parallel Session chosen:**
- Guide them to open new session in worktree.
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans.

## Design Alignment Verification

**Every task MUST be traceable to the design:**
- Reference the specific section of the design doc that this task implements.
- If design artifacts exist, reference them appropriately.
- Verification steps must check against design, not just "does code work".

## Self-Check

Before completing plan:
- [ ] Every task has exact file paths (no "somewhere in src/").
- [ ] Every code block is complete (no placeholders or TODOs).
- [ ] Every test command includes expected output.
- [ ] Each step is a single atomic action (2-5 min max).
- [ ] Design doc path recorded in header.
- [ ] Plan saved to correct location (`docs/plans/...`).

If ANY unchecked: STOP and fix before proceeding.