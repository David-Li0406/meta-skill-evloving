# Superpowers - Agent Development Skills

**Version 1.0.0**  
Jesse's Agent Skills Collection  
January 2026

> **Note:**  
> This document is for AI agents and LLMs to follow when developing,  
> maintaining, or debugging codebases. It provides structured workflows  
> optimized for AI-assisted coding with discipline and verification.

---

## Abstract

Comprehensive agent development skill collection for AI-assisted coding workflows. Contains 14 skills across 6 categories, from ideation through completion. Each skill includes detailed processes, red flags, common mistakes, and integration points with other skills. Designed to enforce discipline, quality, and systematic approaches to software development.

---

## Table of Contents

1. [Ideation & Planning](#1-ideation--planning) — **CRITICAL**
   - 1.1 [Brainstorming](#11-brainstorming)
   - 1.2 [Writing Plans](#12-writing-plans)
2. [Implementation](#2-implementation) — **CRITICAL**
   - 2.1 [Test-Driven Development](#21-test-driven-development)
   - 2.2 [Subagent-Driven Development](#22-subagent-driven-development)
   - 2.3 [Executing Plans](#23-executing-plans)
3. [Debugging](#3-debugging) — **HIGH**
   - 3.1 [Systematic Debugging](#31-systematic-debugging)
4. [Code Review](#4-code-review) — **HIGH**
   - 4.1 [Requesting Code Review](#41-requesting-code-review)
   - 4.2 [Receiving Code Review](#42-receiving-code-review)
5. [Completion](#5-completion) — **HIGH**
   - 5.1 [Verification Before Completion](#51-verification-before-completion)
   - 5.2 [Finishing a Development Branch](#52-finishing-a-development-branch)
6. [Utilities](#6-utilities) — **MEDIUM**
   - 6.1 [Using Git Worktrees](#61-using-git-worktrees)
   - 6.2 [Dispatching Parallel Agents](#62-dispatching-parallel-agents)
   - 6.3 [Using Superpowers](#63-using-superpowers)
   - 6.4 [Writing Skills](#64-writing-skills)

---

## 1. Ideation & Planning

**Impact: CRITICAL**

No code without design. These skills ensure you understand what you're building before touching code.

### 1.1 Brainstorming

**Impact: HIGH (prevents building wrong thing)**

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

**Core Principle:** Understand what you're building before building it.

**The Process:**

1. **Understanding the idea:**
   - Check out the current project state first (files, docs, recent commits)
   - Ask questions one at a time to refine the idea
   - Prefer multiple choice questions when possible
   - Only one question per message
   - Focus on understanding: purpose, constraints, success criteria

2. **Exploring approaches:**
   - Propose 2-3 different approaches with trade-offs
   - Present options conversationally with your recommendation and reasoning
   - Lead with your recommended option and explain why

3. **Presenting the design:**
   - Once you believe you understand what you're building, present the design
   - Break it into sections of 200-300 words
   - Ask after each section whether it looks right so far
   - Cover: architecture, components, data flow, error handling, testing
   - Be ready to go back and clarify if something doesn't make sense

**After the Design:**

- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Commit the design document to git
- Ask: "Ready to set up for implementation?"
- Use `using-git-worktrees` to create isolated workspace
- Use `writing-plans` to create detailed implementation plan

**Key Principles:**
- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense

---

### 1.2 Writing Plans

**Impact: CRITICAL (prevents building with unclear requirements)**

Write comprehensive implementation plans assuming the engineer has zero context for the codebase.

**Core Principle:** Document everything they need to know: which files to touch, code, testing, how to test.

**Bite-Sized Task Granularity:**

Each step is one action (2-5 minutes):
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

**Plan Document Header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

**Task Structure:**

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**
[Code block]

**Step 2: Run test to verify it fails**
Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**
[Code block]

**Step 4: Run test to verify it passes**
Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**
```

**Remember:**
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

---

## 2. Implementation

**Impact: CRITICAL**

Code quality starts here. These skills ensure you write tested, reviewable code.

### 2.1 Test-Driven Development

**Impact: CRITICAL (prevents untested code)**

Write the test first. Watch it fail. Write minimal code to pass.

**Core Principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**The Iron Law:**

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

**Red-Green-Refactor Cycle:**

```
RED → Write failing test
↓
Verify fails correctly
↓
GREEN → Minimal code to pass
↓
Verify passes (all green)
↓
REFACTOR → Clean up
↓
Next test → RED
```

**RED - Write Failing Test:**

Write one minimal test showing what should happen.

**Good test:**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

Requirements:
- One behavior
- Clear name
- Real code (no mocks unless unavoidable)

**Verify RED - Watch It Fail:**

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**GREEN - Minimal Code:**

Write simplest code to pass the test.

Don't add features, refactor other code, or "improve" beyond the test.

**Common Rationalizations:**

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |

**Red Flags - STOP and Start Over:**

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Rationalizing "just this once"
- "I already manually tested it"

**All of these mean: Delete code. Start over with TDD.**

---

### 2.2 Subagent-Driven Development

**Impact: HIGH (quality gates on every task)**

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core Principle:** Fresh subagent per task + two-stage review = high quality, fast iteration

**When to Use:**

- Have implementation plan? YES
- Tasks mostly independent? YES
- Stay in this session? YES → subagent-driven-development
- Stay in this session? NO → executing-plans

**The Process:**

1. Read plan, extract all tasks with full text, note context, create TodoWrite
2. For each task:
   - Dispatch implementer subagent with full task text + context
   - Answer any questions from subagent
   - Subagent implements, tests, commits, self-reviews
   - Dispatch spec reviewer subagent
   - If issues: implementer fixes, spec reviewer re-reviews
   - Dispatch code quality reviewer subagent
   - If issues: implementer fixes, code quality reviewer re-reviews
   - Mark task complete
3. After all tasks: dispatch final code reviewer for entire implementation
4. Use `finishing-a-development-branch`

**Prompt Templates:**

- `./implementer-prompt.md` - Dispatch implementer subagent
- `./spec-reviewer-prompt.md` - Dispatch spec compliance reviewer
- `./code-quality-reviewer-prompt.md` - Dispatch code quality reviewer

**Red Flags:**

**Never:**
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context
- Accept "close enough" on spec compliance
- **Start code quality review before spec compliance is ✅**

---

### 2.3 Executing Plans

**Impact: HIGH (quality checkpoints)**

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core Principle:** Batch execution with checkpoints for architect review.

**The Process:**

1. **Load and Review Plan:**
   - Read plan file
   - Review critically - identify any questions or concerns
   - If concerns: Raise them before starting
   - If no concerns: Create TodoWrite and proceed

2. **Execute Batch (Default: First 3 tasks):**
   - For each task: Mark as in_progress → Follow steps exactly → Run verifications → Mark as completed

3. **Report:**
   - Show what was implemented
   - Show verification output
   - Say: "Ready for feedback."

4. **Continue:**
   - Apply feedback changes if needed
   - Execute next batch
   - Repeat until complete

5. **Complete Development:**
   - Use `finishing-a-development-branch` skill

**When to Stop and Ask for Help:**

- Hit a blocker mid-batch
- Plan has critical gaps
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

---

## 3. Debugging

**Impact: HIGH**

Systematic debugging prevents wasted time and new bugs from random fixes.

### 3.1 Systematic Debugging

**Impact: CRITICAL (prevents thrashing)**

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core Principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**The Iron Law:**

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

**When to Use:**

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work

**The Four Phases:**

**Phase 1: Root Cause Investigation**

BEFORE attempting ANY fix:

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes

4. **Gather Evidence in Multi-Component Systems**
   - Log what data enters/exits each component
   - Verify environment/config propagation
   - Check state at each layer

5. **Trace Data Flow**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

**Phase 2: Pattern Analysis**

1. Find working examples - what works that's similar?
2. Compare against references - read completely
3. Identify differences - list every difference, however small
4. Understand dependencies - what other components needed?

**Phase 3: Hypothesis and Testing**

1. Form single hypothesis: "I think X is the root cause because Y"
2. Test minimally - smallest possible change
3. Verify before continuing - didn't work? Form NEW hypothesis

**Phase 4: Implementation**

1. Create failing test case
2. Implement single fix
3. Verify fix
4. If 3+ fixes failed: Question architecture

**Red Flags - STOP and Follow Process:**

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- "One more fix attempt" (when already tried 2+)

**If 3+ fixes failed:** Question the architecture

---

## 4. Code Review

**Impact: HIGH**

Code review catches issues early and maintains standards.

### 4.1 Requesting Code Review

**Impact: MEDIUM (catches issues early)**

Dispatch superpowers:code-reviewer subagent to catch issues before they cascade.

**Core Principle:** Review early, review often.

**When to Request Review:**

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

**How to Request:**

1. Get git SHAs:
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

2. Dispatch code-reviewer subagent with template

3. Act on feedback:
   - Fix Critical issues immediately
   - Fix Important issues before proceeding
   - Note Minor issues for later
   - Push back if reviewer is wrong (with reasoning)

---

### 4.2 Receiving Code Review

**Impact: HIGH (prevents blind implementation)**

Code review requires technical evaluation, not emotional performance.

**Core Principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

**The Response Pattern:**

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

**Forbidden Responses:**

**NEVER:**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

**Handling Unclear Feedback:**

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items
```

**When To Push Back:**

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Conflicts with architect's decisions

**Acknowledging Correct Feedback:**

```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ ANY gratitude expression
```

---

## 5. Completion

**Impact: HIGH**

Proper completion ensures work is verified and integrated correctly.

### 5.1 Verification Before Completion

**Impact: CRITICAL (prevents false claims)**

Claiming work is complete without verification is dishonesty, not efficiency.

**Core Principle:** Evidence before claims, always.

**The Iron Law:**

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

**The Gate Function:**

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

**Common Failures:**

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Requirements met | Line-by-line checklist | Tests passing |

**Red Flags - STOP:**

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- **ANY wording implying success without having run verification**

**Rationalization Prevention:**

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |

---

### 5.2 Finishing a Development Branch

**Impact: HIGH (proper integration)**

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core Principle:** Verify tests → Present options → Execute choice → Clean up.

**The Process:**

**Step 1: Verify Tests**

Before presenting options, verify tests pass:

```bash
npm test / cargo test / pytest / go test ./...
```

If tests fail: Stop. Don't proceed to Step 2.

**Step 2: Determine Base Branch**

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

**Step 3: Present Options**

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Step 4: Execute Choice**

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

**Step 5: Cleanup Worktree**

For Options 1, 2, 4: `git worktree remove <worktree-path>`
For Option 3: Keep worktree

**Red Flags:**

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

---

## 6. Utilities

**Impact: MEDIUM**

Supporting skills that enhance the development workflow.

### 6.1 Using Git Worktrees

**Impact: MEDIUM (enables parallel work)**

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously.

**Core Principle:** Systematic directory selection + safety verification = reliable isolation.

**Directory Selection Process:**

1. Check existing directories (`.worktrees` or `worktrees`)
2. Check CLAUDE.md for preference
3. Ask user

**Safety Verification:**

For project-local directories, MUST verify directory is ignored:

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If NOT ignored: Add to .gitignore + commit

**Creation Steps:**

1. Detect project name
2. Create worktree: `git worktree add "$path" -b "$BRANCH_NAME"`
3. Run project setup (npm install, cargo build, etc.)
4. Verify clean baseline (run tests)
5. Report location

**Quick Reference:**

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |

---

### 6.2 Dispatching Parallel Agents

**Impact: HIGH (parallelization)**

When you have multiple unrelated failures, investigating them sequentially wastes time.

**Core Principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

**When to Use:**

- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't Use When:**

- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other

**The Pattern:**

1. **Identify Independent Domains** - Group failures by what's broken
2. **Create Focused Agent Tasks** - Specific scope, clear goal, constraints
3. **Dispatch in Parallel**
4. **Review and Integrate** - Verify fixes don't conflict, run full test suite

**Agent Prompt Structure:**

Good prompts are:
- **Focused** - One clear problem domain
- **Self-contained** - All context needed
- **Specific about output** - What should the agent return?

**Common Mistakes:**

| ❌ Too broad | ✅ Specific |
|--------------|-------------|
| "Fix all the tests" | "Fix agent-tool-abort.test.ts" |
| "Fix the race condition" | Paste error messages and test names |
| No constraints | "Do NOT change production code" |
| "Fix it" | "Return summary of root cause and changes" |

---

### 6.3 Using Superpowers

**Impact: HIGH (proper skill usage)**

Establishes how to find and use skills, requiring Skill invocation before ANY response.

**The Rule:**

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means you should invoke the skill to check.

**Flow:**

1. User message received
2. Might any skill apply? (even 1%)
3. If YES: Invoke Skill tool
4. Announce: "Using [skill] to [purpose]"
5. Has checklist? Create TodoWrite per item
6. Follow skill exactly
7. Respond

**Red Flags (Rationalizations):**

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |

**Skill Priority:**

1. **Process skills first** (brainstorming, debugging) - determine HOW to approach
2. **Implementation skills second** (frontend-design, mcp-builder) - guide execution

**Skill Types:**

- **Rigid** (TDD, debugging): Follow exactly. Don't adapt away discipline.
- **Flexible** (patterns): Adapt principles to context.

---

### 6.4 Writing Skills

**Impact: HIGH (quality documentation)**

Writing skills IS Test-Driven Development applied to process documentation.

**Core Principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**TDD Mapping for Skills:**

| TDD Concept | Skill Creation |
|-------------|----------------|
| Test case | Pressure scenario with subagent |
| Production code | Skill document (SKILL.md) |
| Test fails (RED) | Agent violates rule without skill |
| Test passes (GREEN) | Agent complies with skill present |
| Refactor | Close loopholes while maintaining compliance |

**When to Create a Skill:**

- Technique wasn't intuitively obvious
- You'd reference this again across projects
- Pattern applies broadly
- Others would benefit

**Don't Create For:**

- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)

**SKILL.md Structure:**

```markdown
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
Bullet list with SYMPTOMS and use cases

## Core Pattern
Before/after code comparison

## Quick Reference
Table or bullets for scanning

## Common Mistakes
What goes wrong + fixes
```

**The Iron Law:**

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

**RED-GREEN-REFACTOR for Skills:**

1. **RED:** Run pressure scenario WITHOUT skill - document baseline behavior
2. **GREEN:** Write skill addressing those specific violations - verify agents now comply
3. **REFACTOR:** Add explicit counters for new rationalizations - re-test until bulletproof

---

## Integration Map

Skills work together in workflows:

```
brainstorming
    ↓
writing-plans + using-git-worktrees
    ↓
subagent-driven-development OR executing-plans
    ↓ (using test-driven-development throughout)
    ↓ (using systematic-debugging when issues arise)
    ↓ (using requesting-code-review after tasks)
    ↓ (using receiving-code-review for feedback)
    ↓
verification-before-completion
    ↓
finishing-a-development-branch
```

**Key Dependencies:**

| Skill | Calls | Called By |
|-------|-------|-----------|
| `brainstorming` | `using-git-worktrees`, `writing-plans` | - |
| `writing-plans` | `executing-plans`, `subagent-driven-development` | `brainstorming` |
| `subagent-driven-development` | `test-driven-development`, `finishing-a-development-branch` | `writing-plans` |
| `executing-plans` | `finishing-a-development-branch` | `writing-plans` |
| `finishing-a-development-branch` | - | `subagent-driven-development`, `executing-plans` |
| `using-git-worktrees` | - | `brainstorming` |
| `test-driven-development` | - | All implementation skills |
| `systematic-debugging` | `test-driven-development` | Any debugging scenario |

---

## The Bottom Lines

**Core Iron Laws:**

| Skill | Iron Law |
|-------|----------|
| `test-driven-development` | No production code without failing test first |
| `systematic-debugging` | No fixes without root cause investigation first |
| `verification-before-completion` | No completion claims without fresh verification evidence |
| `writing-skills` | No skill without failing test first |

**Real-World Impact:**

From development sessions:
- TDD: First-time fix rate 95% vs 40%
- Systematic debugging: 15-30 minutes vs 2-3 hours thrashing
- Verification: Zero false completion claims
- Parallel agents: 3 problems solved in time of 1
