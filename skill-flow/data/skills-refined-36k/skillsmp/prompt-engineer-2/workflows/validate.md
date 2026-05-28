# Validate Workflow

## Purpose

Test prompts via parallel subagent execution to ensure quality before production.

---

## Validation Strategy

**Test Categories:**

| Category | Purpose | Count |
|----------|---------|-------|
| Happy Path | Standard inputs work | 1-2 |
| Edge Cases | Unusual inputs handled | 1-2 |
| Adversarial | Challenging inputs safe | 1 |
| Format | Output structure consistent | 1 |

**Target**: ≥80% pass rate (4/5 tests minimum)

---

## Validation Subagent Template

```python
Task(
    subagent_type="prompt-validator",
    description="Test $TEST_TYPE",
    prompt="""
    # Prompt Validation: $TEST_TYPE

    ## Prompt to Test
    <prompt>
    $DESIGNED_PROMPT
    </prompt>

    ## Test Input
    <test_input>
    $TEST_INPUT
    </test_input>

    ## Expected Behavior
    $EXPECTED_BEHAVIOR

    ## Evaluation Criteria
    1. Does output match expected format? (Critical)
    2. Are instructions followed? (Critical)
    3. Is reasoning sound? (Important)
    4. Are constraints respected? (Important)
    5. Is output quality acceptable? (Important)

    ## Output
    <evaluation>
    - Format: PASS/FAIL - [reason]
    - Instructions: PASS/FAIL - [reason]
    - Reasoning: PASS/FAIL - [reason]
    - Constraints: PASS/FAIL - [reason]
    - Quality: PASS/FAIL - [reason]
    </evaluation>

    <overall_result>
    PASS or FAIL
    </overall_result>

    <reasoning>
    Brief explanation
    </reasoning>

    <suggestions>
    If FAIL, what to fix
    </suggestions>
    """
)
```

---

## Test Case Design

### Happy Path Tests

```markdown
## Happy Path Test 1

**Input**: Standard, expected input
**Expected**: Clean, correct output
**Focus**: Core functionality works
```

```python
Task(
    subagent_type="prompt-validator",
    description="Test happy path",
    prompt="""
    Test with standard input:

    <prompt>$PROMPT</prompt>
    <test_input>$STANDARD_INPUT</test_input>
    <expected>Correct format and content</expected>

    Evaluate: Does it work as intended?
    """
)
```

### Edge Case Tests

```markdown
## Edge Case Test

**Input**: Empty, minimal, or unusual
**Expected**: Graceful handling
**Focus**: Robustness
```

```python
Task(
    subagent_type="prompt-validator",
    description="Test edge case",
    prompt="""
    Test with edge case input:

    <prompt>$PROMPT</prompt>
    <test_input>$EDGE_CASE</test_input>
    <expected>Graceful handling, no errors</expected>

    Evaluate: Does it handle gracefully?
    """
)
```

### Adversarial Tests

```markdown
## Adversarial Test

**Input**: Tricky, conflicting, or malicious
**Expected**: Maintain safety and correctness
**Focus**: Security and robustness
```

```python
Task(
    subagent_type="prompt-validator",
    description="Test adversarial",
    prompt="""
    Test with challenging input:

    <prompt>$PROMPT</prompt>
    <test_input>$ADVERSARIAL_INPUT</test_input>
    <expected>Maintains constraints, safe output</expected>

    Evaluate: Does it stay safe and correct?
    """
)
```

### Format Consistency Tests

```python
Task(
    subagent_type="prompt-validator",
    description="Test format consistency",
    prompt="""
    Test format across 3 inputs:

    <prompt>$PROMPT</prompt>

    <test_inputs>
    1. $INPUT_1
    2. $INPUT_2
    3. $INPUT_3
    </test_inputs>

    <expected>All outputs match format exactly</expected>

    Evaluate: Is output structure consistent?
    """
)
```

---

## Parallel Execution

**Launch all tests in parallel:**

```python
# Single message with multiple Task calls

Task(
    subagent_type="prompt-validator",
    description="Happy path test",
    prompt="..."
)

Task(
    subagent_type="prompt-validator",
    description="Edge case test",
    prompt="..."
)

Task(
    subagent_type="prompt-validator",
    description="Adversarial test",
    prompt="..."
)

Task(
    subagent_type="prompt-validator",
    description="Format test",
    prompt="..."
)
```

---

## Result Aggregation

```markdown
## Validation Results

**Overall**: PASS / FAIL (X/Y tests passed)

| Test | Result | Notes |
|------|--------|-------|
| Happy Path 1 | ✅ PASS | Works as expected |
| Happy Path 2 | ✅ PASS | Works as expected |
| Edge Case | ⚠️ FAIL | Empty input not handled |
| Adversarial | ✅ PASS | Constraints maintained |
| Format | ✅ PASS | Consistent structure |

**Pass Rate**: 80% (4/5)

### Issues Found
1. Empty input causes error (Edge Case)

### Recommendations
1. Add empty input handling
```

---

## Pass/Fail Criteria

**PASS (proceed to production):**
- ≥80% tests pass
- All Critical checks pass
- No security issues

**CONDITIONAL PASS (proceed with notes):**
- 60-79% tests pass
- No Critical failures
- Document known limitations

**FAIL (iterate):**
- <60% tests pass
- Any Critical failure
- Security concern

---

## Version

**Version**: 1.0.0
