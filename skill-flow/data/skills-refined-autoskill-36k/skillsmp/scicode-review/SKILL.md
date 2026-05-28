---
name: scicode-review
description: Review and validate SciCode benchmark problems for quality and correctness. Use when checking problem quality, verifying test cases, reviewing decomposition, or preparing tasks for submission. Triggers on "review task", "validate problem", "check benchmark".
---

# SciCode Task Review

Review and validate SciCode benchmark tasks for quality, correctness, and benchmark suitability.

## Review Process

```
+---------------------------------------------------------------+
| REVIEW STAGES                                                  |
+---------------------------------------------------------------+
| 1. STEM Review     -> Scientific accuracy, decomposition       |
| 2. Python Review   -> Code quality, test coverage              |
| 3. Automated       -> Structure validation, test execution     |
+---------------------------------------------------------------+
```

## Quick Validation

```bash
# Check structure and required fields
task validate tasks/<task_name>/

# Run gold solution tests (must be 100%)
task test tasks/<task_name>/
```

## Stage 1: STEM Review

Validate scientific content and algorithm decomposition.

### Questions to Answer

1. **Paper Validity**
   - Is the paper published after February 2025?
   - Does it propose a novel computational algorithm?
   - Is the algorithm clearly described with formulas?

2. **Decomposition Quality**
   - Does the decomposition capture the novel algorithm from the paper?
   - Are there 8-10 independently testable subproblems?
   - Does each step have clear scientific meaning?
   - Is the logical progression correct?

3. **Scientific Accuracy**
   - Are mathematical formulas correctly translated to code?
   - Do the gold solutions match the paper's algorithm?
   - Are domain-specific assumptions handled correctly?

4. **Background Context**
   - Is there sufficient context for domain experts?
   - Are key equations documented?
   - Are implementation notes helpful?

## Stage 2: Python Review

Assess code quality, testing, and implementation.

### Code Quality Checklist

- [ ] Function signatures have type hints
- [ ] Docstrings explain Parameters and Returns
- [ ] No magic numbers (constants explained)
- [ ] No debug prints or commented-out code
- [ ] Appropriate error handling

### Test Coverage Checklist

- [ ] 2-3 test cases per step
- [ ] Tests cover normal inputs
- [ ] Tests cover edge cases (empty, zero, boundary)
- [ ] Random seeds for reproducibility
- [ ] Appropriate tolerances for floats

### Numerical Stability

- [ ] Zero/near-zero divisors handled
- [ ] Overflow conditions considered
- [ ] Tolerances documented

## Stage 3: Automated Checks

Run validation commands and verify results.

```bash
# Structure validation
task validate tasks/<task_name>/
# Expected: No errors

# Compile and test
task test tasks/<task_name>/
# Expected: 100% pass rate
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Missing main function | Add non-underscore function to step file |
| Missing gold solution | Add `_gold_functionname()` function |
| Test case failure | Fix gold solution or test setup code |
| Invalid domain | Use: physics, chemistry, biology, mathematics, materials |
| Invalid YAML | Check indentation, quotes, colons |
| Import error | Add missing import to dependencies list |
| Zero pivot error | Add tolerance check or pivoting |

## Red Flags

Stop review and request fixes if you see:

- Paper published before February 2025
- Fewer than 8 subproblems
- String outputs instead of numerical values
- Magic numbers without explanation
- Missing test cases
- Gold solution doesn't match paper algorithm
- Cross-dependencies between steps (except outputs)

## Review Feedback Template

When providing review feedback:

```markdown
## STEM Review

### Paper & Decomposition
- [ ] Paper is post-Feb 2025
- [ ] Novel algorithm captured
- [ ] 8+ subproblems
- [ ] Logical progression

### Issues Found
1. [Issue description]
   - Location: `steps/03_*.py`
   - Suggestion: [how to fix]

## Python Review

### Code Quality
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Tests adequate

### Issues Found
1. [Issue description]
   - Location: `steps/05_*.py:42`
   - Suggestion: [how to fix]

## Automated Checks

- [ ] `task validate` passes
- [ ] `task test` 100% pass rate

## Verdict

[ ] Approved
[ ] Needs revision (see issues above)
```

## Detailed Criteria

See [CRITERIA.md](CRITERIA.md) for comprehensive review criteria.

## After Review

### If Approved
- Task ready for merge into benchmark
- Author notified of approval

### If Needs Revision
1. Create issues in review feedback
2. Author addresses issues
3. Re-review after fixes
4. Repeat until approved
