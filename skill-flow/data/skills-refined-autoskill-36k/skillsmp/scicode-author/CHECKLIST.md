# SciCode Pre-Submission Checklist

Complete this checklist before submitting your task for review.

---

## Paper & Scope

- [ ] **Publication Date**: Paper published after February 2025
- [ ] **Novel Method**: Proposes a new computational algorithm (not just analysis)
- [ ] **Decomposable**: Can be broken into 8-10 independent subproblems
- [ ] **Implementable**: Uses only numpy/scipy (no obscure dependencies)
- [ ] **Testable**: Outputs numerical values that can be automatically verified

---

## Directory Structure

- [ ] Task directory exists: `tasks/<your_task_name>/`
- [ ] Paper PDF included: `tasks/<your_task_name>/<paper>.pdf`
- [ ] problem.yaml present: `tasks/<your_task_name>/problem.yaml`
- [ ] Steps directory: `tasks/<your_task_name>/steps/`
- [ ] 8-10 step files: `steps/01_*.py` through `steps/08_*.py` (minimum)

---

## problem.yaml

- [ ] `problem_id`: Unique snake_case identifier
- [ ] `problem_name`: Human-readable title
- [ ] `domain`: One of: physics, chemistry, biology, mathematics, materials
- [ ] `subdomain`: Specific area within domain
- [ ] `description`: 2-4 sentences explaining the problem goal
- [ ] `io_spec`: Complete input/output specification with types and shapes
- [ ] `dependencies`: All required imports listed
- [ ] `steps`: All step files listed in order (without .py)

---

## Step Files

For EACH step file (`steps/##_name.py`):

- [ ] **Module docstring**: Clear description shown to LLM
- [ ] **Main function**: Non-underscore function with type hints
- [ ] **Docstring**: Parameters and Returns sections
- [ ] **Return statement**: Clear return hint for model
- [ ] **Gold solution**: `_gold_<function_name>()` implemented
- [ ] **Test cases**: `test_cases()` function with 2-3 tests

### Test Case Requirements

- [ ] Each test has: `setup`, `call`, `gold_call`
- [ ] Tests cover: normal inputs, edge cases, boundary conditions
- [ ] Random seeds set for reproducibility
- [ ] Appropriate tolerances for floating-point comparison

---

## Background Files (if applicable)

- [ ] Named with step prefix: `background/##_concept.md`
- [ ] Contains: Overview, Math Formulation, Algorithm, Implementation Notes
- [ ] Formulas in LaTeX notation
- [ ] No excessive length (keep focused)

---

## Validation & Testing

Run these commands and verify output:

```bash
# 1. Validate structure (should pass with no errors)
task validate tasks/<your_task_name>/

# 2. Compile to evaluation format
task compile tasks/<your_task_name>/

# 3. Run gold tests (must show 100% pass rate)
task test tasks/<your_task_name>/
```

- [ ] `task validate` passes with no errors
- [ ] `task compile` generates problems.jsonl and test_data.h5
- [ ] `task test` shows 100% pass rate

---

## Code Quality

- [ ] **No magic numbers**: All constants explained or parameterized
- [ ] **Type hints**: Function signatures have type annotations
- [ ] **Docstrings**: All functions documented
- [ ] **Numerical stability**: Handled edge cases (zero divisors, overflow)
- [ ] **Clean code**: No debug prints, commented-out code, or TODOs

---

## Final Checks

- [ ] Gold solutions match paper's algorithm description
- [ ] Steps follow logical progression
- [ ] Each step's output can be independently verified
- [ ] No cross-dependencies between steps (except defined outputs)
- [ ] Difficulty appropriate for benchmark (SOTA models < 10% accuracy)

---

## Ready to Submit?

Once all boxes are checked:

1. Create a branch for your task
2. Commit all files
3. Open PR with title: `[Task] <problem_name>`
4. Request STEM + Python review

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `task validate` fails | Check file names, YAML syntax, required fields |
| `task compile` fails | Fix gold solution bugs, import errors |
| `task test` fails | Debug gold solution, check test setup code |
| Low pass rate | Verify gold solution matches paper exactly |
