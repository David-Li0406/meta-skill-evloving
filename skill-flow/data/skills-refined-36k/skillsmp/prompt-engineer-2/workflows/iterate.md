# Iterate Workflow

## Purpose

Refine prompts based on validation feedback using self-refine pattern.

---

## Iteration Triggers

| Validation Result | Action |
|-------------------|--------|
| ≥80% pass | Production ready, skip iteration |
| 60-79% pass | 1 iteration recommended |
| 40-59% pass | 2 iterations required |
| <40% pass | Major redesign needed |

**Maximum iterations**: 3 (then flag for human review)

---

## Self-Refine Loop

```
Current Prompt → Critique → Improvements → Refined Prompt → Validate → [Repeat if needed]
```

---

## Step 1: Critique Generation

```markdown
## Prompt Critique

### Failed Tests Summary
| Test | Result | Root Cause |
|------|--------|------------|
| $TEST_1 | FAIL | $CAUSE_1 |
| $TEST_2 | FAIL | $CAUSE_2 |

### Issue Analysis

**Issue 1: $ISSUE_NAME**
- What happened: $DESCRIPTION
- Why it happened: $ROOT_CAUSE
- Fix strategy: $FIX

**Issue 2: $ISSUE_NAME**
- What happened: $DESCRIPTION
- Why it happened: $ROOT_CAUSE
- Fix strategy: $FIX

### What to Preserve
- $WORKING_ELEMENT_1
- $WORKING_ELEMENT_2

### What to Change
1. $CHANGE_1
2. $CHANGE_2

### What to Add
1. $ADDITION_1
2. $ADDITION_2
```

---

## Step 2: Apply Improvements

### Common Fixes

| Issue | Fix |
|-------|-----|
| Wrong format | Add explicit format section with example |
| Ignores instructions | Move critical instructions to top |
| Inconsistent | Add more diverse examples |
| Edge case failure | Add explicit edge case handling |
| Too verbose | Add length constraints |
| Hallucination | Add context section |

### Refinement Template

```xml
<original_prompt>
$CURRENT_PROMPT
</original_prompt>

<critique>
$CRITIQUE_FROM_STEP_1
</critique>

<improvements_to_apply>
1. $IMPROVEMENT_1
2. $IMPROVEMENT_2
</improvements_to_apply>

<refined_prompt>
Apply improvements while preserving working elements:

[Generate refined version here]
</refined_prompt>
```

---

## Step 3: Re-Validate

**Run same tests on refined prompt:**

```python
# Re-run failed tests first
Task(
    subagent_type="prompt-validator",
    description="Re-test failed: $TEST_NAME",
    prompt="""
    Test refined prompt:

    <prompt>$REFINED_PROMPT</prompt>
    <test_input>$ORIGINAL_FAILING_INPUT</test_input>

    Previous issue: $ISSUE_DESCRIPTION
    Expected fix: $FIX_APPLIED

    Evaluate: Is issue resolved?
    """
)

# Then run passing tests to check for regressions
Task(
    subagent_type="prompt-validator",
    description="Regression test: $TEST_NAME",
    prompt="""
    Verify no regression:

    <prompt>$REFINED_PROMPT</prompt>
    <test_input>$PREVIOUSLY_PASSING_INPUT</test_input>

    Evaluate: Still works correctly?
    """
)
```

---

## Iteration Tracking

```markdown
## Iteration History

### Iteration 1
**Date**: $TIMESTAMP
**Pass Rate Before**: 60%
**Changes Made**:
1. Added edge case handling
2. Improved format section
**Pass Rate After**: 80%
**Status**: ✅ Complete

### Iteration 2 (if needed)
**Date**: $TIMESTAMP
**Pass Rate Before**: 70%
**Changes Made**:
1. Added more examples
**Pass Rate After**: 90%
**Status**: ✅ Complete
```

---

## Exit Conditions

### Success Exit (≥80% pass)

```markdown
## Iteration Complete

**Final Pass Rate**: X%
**Iterations Required**: Y
**Status**: Production Ready

### Version History
| Version | Pass Rate | Key Changes |
|---------|-----------|-------------|
| 1.0 | 60% | Initial |
| 1.1 | 80% | Edge case fix |
| 1.2 | 90% | Format improvement |
```

### Maximum Iterations Reached

```markdown
## Iteration Limit Reached

**Pass Rate**: X% (below 80%)
**Iterations**: 3 (maximum)
**Status**: Needs Human Review

### Unresolved Issues
1. $ISSUE_1 - attempted fix: $FIX
2. $ISSUE_2 - attempted fix: $FIX

### Recommendation
[What to try next or fundamental redesign needed]
```

---

## Anti-Patterns

| Anti-Pattern | Issue | Prevention |
|--------------|-------|------------|
| Over-iteration | Diminishing returns | Cap at 3 iterations |
| Breaking fixes | New bugs from fixes | Run regression tests |
| Scope creep | Adding unrelated features | Focus only on failed tests |
| Ignoring root cause | Treating symptoms | Always analyze why |

---

## Version

**Version**: 1.0.0
