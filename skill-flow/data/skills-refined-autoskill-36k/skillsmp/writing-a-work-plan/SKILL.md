---
name: writing-a-work-plan
description: Use when converting design documents and milestones into granular implementation tasks. Covers scope validation, codebase verification, task decomposition by type (infrastructure, functionality, integration), and TDD-aligned workflows.
---

# Writing Work Plans

## Overview

Work plans bridge design intent and implementation. A design document describes *what* to build and *why*; a work plan tells implementers (human engineers or LLM agents) exactly *how* — which files to create, what code to write, what tests to run, and how to verify correctness. This skill guides the conversion of milestone-level acceptance criteria into bite-sized, TDD-aligned tasks.

## Required Sub-Skills

Always load these when writing work plans:

| Skill | Purpose |
|-------|---------|
| [writing-code](../writing-code/SKILL.md) | Engineering principles, sub-skill loading |
| [writing-useful-tests](../writing-useful-tests/SKILL.md) | TDD workflow, Arrange/Act/Assert, single-assertion tests |
| [writing-effective-acceptance-criteria](../writing-effective-acceptance-criteria/SKILL.md) | AC testability and grain checks |

## When to Use

- After design review and milestone approval
- When milestones have job stories, descriptions, AC, and demos defined
- When C4 diagrams exist (at least container level, preferably component level)
- When you need to hand off implementation to another engineer or agent

## When NOT to Use

- During design exploration (use design skills first)
- When milestones are vague or lack AC (use `performing-milestone-reviews` first)
- For single-file fixes that don't need planning

## Entry Point

When the user invokes this skill or requests a work plan:

**FIRST, before any other action**, determine review mode:

1. **Choose review mode** (MANDATORY FIRST STEP):

   **STOP. You MUST use AskUserQuestion here before proceeding.**

   Use `AskUserQuestion` with these options:
   - **Interactive** (Recommended): Plan one milestone, get approval, proceed. Catches errors early.
   - **Batch**: Plan all milestones, then review all. Faster but riskier.

   Do not assume a default. Do not proceed until the user responds.

2. **Locate the design document.** Ask for the path if not provided.
3. **Validate scope.** Check milestone count (see Phase 1).
4. **Process milestones.** Follow the Core Pattern below.

## Core Pattern

### Phase 1: Validate Scope

Count milestones in the design document.

| Count | Action |
|-------|--------|
| ≤8 | Proceed |
| >8 | Stop. Ask user to split the design doc or justify why this scope is necessary. |

The 8-milestone limit is a smell detector. Larger scope often indicates the design covers multiple features that should be planned separately.

### Phase 2: Codebase Verification (Pre-Planning)

Before writing any tasks, verify the codebase matches design assumptions.

**Step 1**: Dispatch `codebase-investigator` agent to investigate **testing patterns**:
- How are tests structured in this codebase?
- What mocking patterns exist?
- What fixtures are available?
- Where do tests live (`tests/`, `test/`, colocated)?

**Step 2** (Sequential, after Step 1): Dispatch `codebase-investigator` agent to verify **design assumptions**:
- Do files exist where the design expects them?
- Do expected features/dependencies exist?
- Is there drift between design doc and current code?
- Are there naming conventions to follow?

Document findings in the milestone plan header.

### Phase 3: Write Milestone Plan (Interactive)

Process milestones one at a time. For each milestone:

#### 3A: Read the Milestone

Extract from design doc:
- Job story
- Description
- Acceptance criteria (list)
- Demo
- Components covered

#### 3B: Classify Each AC

| Type | Characteristics | Verification |
|------|-----------------|--------------|
| **Infrastructure** | Creates files, config, scaffolding | Operational (builds, runs, imports) |
| **Functionality** | Implements behavior, core logic | Unit tests (TDD) |
| **Integration** | Wires components together | Integration tests (TDD) |

#### 3C: Create Scaffold Task (if applicable)

For functionality or integration milestones, create a scaffold task first:

```markdown
**Task N.1: Scaffold [Component] with test stubs**

| Field | Value |
|-------|-------|
| **Job Story** | When I start implementing [Component], I want the module structure in place. |
| **Description** | Create module file with class skeleton and test file with test stubs. |
| **AC** | Module and test files exist; pytest runs without errors |
| **Type** | Infrastructure |

**Implementation Steps**:
1. Create `src/[path]/[module].py` with class skeleton
2. Create `tests/[path]/test_[module].py` with test stubs:
   - `test_[ac_1_behavior]`
   - `test_[ac_2_behavior]`
   - ...
3. Verify: `pytest tests/[path]/test_[module].py` runs
4. Commit: "feat(mN): scaffold [Component] with test stubs"
```

#### 3D: Create One Task Per AC

**Before writing any task**, understand the relationship between parent AC and task AC:

- **Parent AC**: The milestone-level acceptance criterion this task contributes to
- **Task AC**: This task's specific, testable criterion — more granular than the parent

**Task AC must meet the same rigor as milestone AC** (per `writing-effective-acceptance-criteria`):
- Testable — clear pass/fail
- Observable — behavior or output, not internal state
- Atomic — one condition, no "and"
- More specific than the parent AC

**Example**:
- Parent AC: "User can preview Trackman data as a formatted table"
- Task AC: "TrackmanParser.parse() returns ParseResult with session_date and shots list"

The task AC is a building block toward the parent AC, not a copy of it.

**For Infrastructure AC**:

```markdown
**Task N.X: [Description]**

| Field | Value |
|-------|-------|
| **Job Story** | When [situation], I want [motivation], so [outcome]. |
| **Description** | [What this task creates/configures] |
| **Parent AC** | [Which milestone AC this task contributes to] |
| **Task AC** | [This task's specific, testable acceptance criterion] |
| **Type** | Infrastructure |

**Implementation Steps**:
1. Create/modify [file]
2. [Additional steps...]
3. Verify: [Operational check — command runs, builds succeed, import works]
4. Commit: "[type](mN): [description]"
```

**For Functionality AC** (TDD):

```markdown
**Task N.X: [Description] (TDD)**

| Field | Value |
|-------|-------|
| **Job Story** | When [situation], I want [motivation], so [outcome]. |
| **Description** | TDD implementation of [behavior]. |
| **Parent AC** | [Which milestone AC this task contributes to] |
| **Task AC** | [This task's specific, testable acceptance criterion] |
| **Type** | Functionality |

**Implementation Steps**:
1. **Red**: Write failing test:
   ```python
   def test_[behavior](fixtures...):
       # Arrange
       [setup code]

       # Act
       result = [call under test]

       # Assert
       assert [single assertion]
   ```
2. Verify: Test **fails**
3. **Green**: Implement minimal code to pass the test
4. Verify: Test **passes**
5. Commit: "feat(mN): [description]"
```

**For Integration AC** (TDD):

```markdown
**Task N.X: Wire and test [command/flow]**

| Field | Value |
|-------|-------|
| **Job Story** | When [user action], I want [end-to-end behavior]. |
| **Description** | Wire [components] together; test full flow. |
| **Parent AC** | [Which milestone AC this task contributes to] |
| **Task AC** | [This task's specific, testable acceptance criterion] |
| **Type** | Integration |

**Implementation Steps**:
1. **Red**: Write integration test:
   ```python
   def test_[flow](cli_runner, fixtures...):
       # Arrange
       [mock setup]

       # Act
       result = cli_runner.invoke(app, ["command", "args"])

       # Assert
       assert result.exit_code == 0
       assert [expected output]
   ```
2. Verify: Test **fails**
3. **Green**: Wire components in command handler
4. Verify: Test **passes**
5. Commit: "feat(mN): wire [command]"
```

#### 3E: Check for Compound AC

If an AC implies multiple assertions or behaviors, split into multiple tasks. Each test should have a **single assertion** following Arrange/Act/Assert.

#### 3E-1: Validate Job Stories and Task AC

**Before presenting tasks to user**, validate each task against these checklists:

**Job Story Checklist**:
- [ ] Has all three parts: When [situation], I want [motivation], so [outcome]
- [ ] Situation describes a real context (not generic "I am working on this task")
- [ ] Motivation describes what the actor wants to accomplish
- [ ] Outcome describes the benefit or value delivered
- [ ] Written from the implementer's or user's perspective (not "the system")

**Bad**: "When implementing this feature, I want to write code, so it works."
**Good**: "When I parse a Trackman JSON file, I want to extract shot data into a structured format, so I can transform and store it consistently."

**Task AC Checklist** (same rigor as milestone AC):
- [ ] Testable — clear pass/fail determination
- [ ] Observable — behavior or output, not internal state
- [ ] Atomic — one condition, no compound "and"
- [ ] More granular than parent AC — a building block, not a copy
- [ ] Independent — can verify without knowing other task internals

**Bad**: "Parser works correctly" (vague, not testable)
**Bad**: "User can preview Trackman data" (copied from parent AC)
**Good**: "TrackmanParser.parse() returns ParseResult with non-empty shots list when given valid JSON"

**If validation fails**: Rewrite the job story or task AC before proceeding. Do not present tasks with placeholder or copied content.

#### 3F: Review with User

Present the task breakdown for approval:
- List all tasks with types
- Highlight any assumptions made
- Note any issues or open questions

**Use `AskUserQuestion` to get explicit approval**:
- **Approve**: Milestone plan looks good, proceed to next milestone
- **Revise**: I have feedback on specific tasks (user provides details via "Other")

Do not proceed to the next milestone until user approves or revisions are complete.

**Immediately after approval, write this milestone to disk** (see Phase 6 for directory structure). This enables:
- Session recovery if context is cleared
- Incremental progress tracking
- Resumption from last completed milestone

### Phase 4: Codebase Verification (Post-Planning)

After writing tasks for a milestone:

1. Dispatch `codebase-investigator` to verify **tasks are implementable**:
   - Do target files/directories exist?
   - Are import paths valid?
   - Any conflicts with existing code?

2. If issues found:
   - Update tasks to match reality
   - Or flag for user decision

### Phase 5: Code Review

**This phase is MANDATORY. Do not present a plan to the user without running code review.**

Run `code-reviewer` agent over the milestone plan.

**Review mode** (determined at session start — see Entry Point step 1):
- **Interactive mode**: Present issues to user; let user decide what to fix
- **Batch mode**: Automatically fix issues; user sees clean plan

**Code review checks**:
- All AC have corresponding tasks
- Tasks include concrete test code where applicable
- Verification steps are explicit (not "verify it works")
- Commit messages follow conventions
- Dependencies are noted (Blocks/Blocked By)
- No ambiguous or vague steps

**Verification**: Before proceeding to Phase 6, confirm:
- [ ] Code reviewer agent was dispatched
- [ ] All issues were addressed

### Phase 6: Write to Disk

**Write each milestone immediately after user approval** (in Phase 3F), not at the end.

This enables session recovery — if context is cleared mid-planning, you can resume from the last written milestone.

Directory structure:
```
docs/work-plans/YYYY-MM-DD-<plan-name>/
├── milestone_01.md  ← written after M1 approval
├── milestone_02.md  ← written after M2 approval
├── ...
└── milestone_NN.md
```

**On resumption**: Check which milestone files exist, read the last one to understand context, and continue from the next milestone.

## Document Format

### Milestone Plan Header

**All fields in this header are REQUIRED. Do not write a milestone plan without completing every field.**

Missing header fields cause implementation failures:
- Missing **Goal**: Implementer doesn't know what "done" looks like
- Missing **Architecture**: Implementer makes wrong structural decisions
- Missing **Codebase Verification**: Tasks may reference nonexistent files

```markdown
# Milestone N: [Title]

## Context

**Goal**: [One sentence describing what this milestone achieves]

**Architecture**: [Which C4 container/component this covers; relevant design decisions]

**Tech Stack**: [Technologies used in this milestone]

**Scope**: [Design doc phase this covers; reference to design doc]

**Codebase Verification**:
- Last verified: [timestamp]
- Testing patterns: [summary of findings]
- Design assumptions: [confirmed/issues found]

**References**:
- Design doc: [path]
- C4 diagrams: [path]
- Related code: [paths]

---

## Tasks

[Tasks follow here]
```

**Verification before proceeding to tasks**:
- [ ] Goal is a single sentence describing the outcome
- [ ] Architecture references specific C4 container/component
- [ ] Tech Stack lists technologies (not "TBD")
- [ ] Scope references specific design doc section
- [ ] Codebase Verification has timestamp and findings (from codebase-investigator)
- [ ] References include absolute paths

### Task Template

```markdown
### Task N.X: [Title]

| Field | Value |
|-------|-------|
| **Job Story** | When [situation], I want [motivation], so [outcome]. |
| **Description** | [What this task does] |
| **Parent AC** | [Which milestone AC this task contributes to] |
| **Task AC** | [This task's specific, testable acceptance criterion] |
| **Type** | Infrastructure / Functionality / Integration |
| **Blocks** | [Tasks that cannot start until this completes] |
| **Blocked By** | [Tasks that must complete before this can start] |

**Implementation Steps**:
1. [Step 1]
2. [Step 2]
3. Verify: [How to verify this task is complete]
4. Commit: "[type](mN): [message]"
```

## Validation Checklist

Before finalizing each milestone plan:

- [ ] All AC have corresponding tasks
- [ ] No compound AC (each task tests one behavior)
- [ ] Scaffold task exists for functionality/integration milestones
- [ ] Each functionality/integration task includes test code
- [ ] Verification steps are explicit (not assumed)
- [ ] Commit messages follow conventions
- [ ] Task dependencies noted (blocks/blocked by)
- [ ] Codebase verification completed (pre and post)

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Skipping review mode choice | User loses control; default behavior may not match needs | AskUserQuestion FIRST before any other action |
| Skipping scaffold task | Tests have nowhere to live | Always scaffold first |
| Multiple assertions per test | Unclear which behavior failed | One assertion per test |
| Assuming verification | Implementers skip verification | Explicit verify steps |
| Copying code from design doc | Design docs get stale | Generate fresh code based on codebase investigation |
| Batch planning without review | Early mistakes compound | Interactive milestone-by-milestone |
| Skipping codebase verification | Tasks may not be implementable | Verify before AND after planning |
| Incomplete milestone header | Implementer lacks context; wrong assumptions | All header fields are REQUIRED |
| Skipping code review | Plan quality issues become implementation bugs | Code review is MANDATORY |
| Copying parent AC to task AC | Task AC should be more granular | Write task-specific AC that builds toward parent |
| Lazy job stories ("When working on X") | No real context; doesn't guide implementation | Include real situation, motivation, outcome |

## Anti-Rationalizations

- "This milestone is simple, skip scaffolding" — Simple milestones still benefit from structure. Scaffold anyway.
- "The design doc has the code" — Design docs are directional. Generate fresh code based on current codebase.
- "I'll combine these tasks to save time" — Granular tasks provide clearer progress signals. Keep them separate.
- "Codebase verification is overhead" — Verification prevents planning tasks for files that don't exist. Do it.
- "The implementer will figure out verification" — They won't, or they'll do it inconsistently. Be explicit.
- "I'll ask about review mode later" — No. Review mode affects everything. Ask FIRST before any other action.
- "The header fields are obvious" — Missing context causes wrong assumptions. Fill in every field.
- "Code review is overkill for this plan" — Even simple plans benefit from a second pass. Review is MANDATORY.
- "Batch mode is fine for this" — User didn't choose that. Ask explicitly. Never assume.
- "The task AC is the same as the parent AC" — No. Task AC must be more granular. If they're identical, you haven't decomposed the work.
- "The job story format is tedious" — The format forces clarity. A vague job story produces vague implementation. Write all three parts.
- "This task is obvious, I'll simplify the AC" — Obvious to you isn't obvious to the implementer. Be explicit.

## Task Tracking

When working through this skill, create tasks for your own progress:

```
Phase NA: Read milestone N from design doc
Phase NB: Investigate codebase (testing patterns)
Phase NC: Investigate codebase (design assumptions)
Phase ND: Write milestone N tasks
Phase NE: Post-planning verification
Phase NF: Code review
Phase NG: User approval
```

Use `TaskCreate` and `TaskUpdate` to track progress. Note blocking dependencies.

## Summary

1. **Verify codebase before planning.** Design docs drift; ground your plan in reality.
2. **One AC = one task.** Granular tasks provide clear completion signals.
3. **Three task types.** Infrastructure (operational), Functionality (unit TDD), Integration (integration TDD).
4. **Always scaffold first.** Test files and module skeletons before TDD cycles.
5. **Include test code.** Concrete examples guide implementers.
6. **Explicit verification.** Never assume implementers will verify or commit.
7. **Interactive review.** Approve each milestone before proceeding to the next.
