---
name: writing-implementation-plans
description: Use this skill when the design is complete and you need detailed implementation tasks for engineers with zero codebase context, creating comprehensive plans with exact file paths, complete code examples, and verification steps.
---

# Writing Implementation Plans

## Overview

Create comprehensive implementation plans assuming the engineer has zero context for our codebase. Document everything they need to know: which files to touch for each task, code, testing, and documentation they might need to check. Provide the whole plan as bite-sized tasks. Follow principles like DRY, YAGNI, and TDD.

**Announce at start:** "I'm using the writing-implementation-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

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
git commit -m "feat: add functionality"
```
```

## Testing Plan

Every plan MUST include a testing section that outlines how you plan to test the behavior. For example:

```markdown
**Testing Plan**

I will add an integration test that ensures foo behaves like blah. The integration test will mock A/B/C. The test will then call function/cli/etc.

I will add a unit test that ensures baz behaves like qux...
```

## Remember

- Use exact file paths.
- Include complete code in the plan.
- Provide exact commands and verification steps with expected output.
- Reference relevant skills with @ syntax.
- Emphasize how you will test your plan.
- Present the plan to the user.