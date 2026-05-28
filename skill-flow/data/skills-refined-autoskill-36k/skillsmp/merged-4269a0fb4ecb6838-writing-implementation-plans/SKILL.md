---
name: writing-implementation-plans
description: Use this skill when the design is complete and you need detailed implementation tasks for engineers with zero codebase context, creating comprehensive plans with exact file paths, complete code examples, and verification steps.
---

# Writing Implementation Plans

## Overview

Create comprehensive implementation plans assuming the engineer has zero context for our codebase. Document everything they need to know: which files to touch for each task, code, testing, and documentation they might need to check. Provide the whole plan as bite-sized tasks. Follow principles of DRY, YAGNI, and TDD. Assume they are skilled developers but know almost nothing about our toolset or problem domain.

**Announce at start:** "I'm using the writing-implementation-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree.

**Save plans to:** `docs/implementation-plans/YYYY-MM-DD-<feature-name>/phase_##.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

- "Write the failing test for `behavior`" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

```markdown
### Task N: [Component/Feature Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts:123-145`
- Test: `tests/exact/path/to/test.ts`

**Step 1: Write the failing test**

```typescript
// Example test code
```

**Step 2: Run test to verify it fails**

Run: `command to run test`
Expected: FAIL with "error message"

**Step 3: Write minimal implementation**

```typescript
// Example implementation code
```

**Step 4: Run test to verify it passes**

Run: `command to run test`
Expected: PASS

**Step 5: Commit**

```bash
git add path/to/modified/files
git commit -m "feat: add specific feature"
```
```

## Testing Plan

Every plan MUST have a testing section. This should document how you plan to test the behavior.

```markdown
**Testing Plan**

I will add an integration test that ensures foo behaves like blah. The integration test will mock A/B/C. The test will then call function/cli/etc.

I will add a unit test that ensures baz behaves like qux...

NOTE: I will write *all* tests before I add any implementation behavior.
```

## Remember

- Exact file paths always.
- Complete code in plan (not "add validation").
- Exact commands with expected output.
- Reference relevant skills with @ syntax.
- DRY, YAGNI, TDD, frequent commits.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/implementation-plans/<filename>.md`. Ready for execution:**

Ask user if they want to execute the plan now or later. If they want to execute it now, use the executing-plans skill to execute the plan. If they want to execute it later, ask them to execute it later.

---
**Testing Details** [Brief description of what tests are being added and how they specifically test BEHAVIOR and NOT just implementation]

**Implementation Details** [maximum 10 bullets about key details]

**Question** [any questions or concerns that may be relevant that need answers]

---