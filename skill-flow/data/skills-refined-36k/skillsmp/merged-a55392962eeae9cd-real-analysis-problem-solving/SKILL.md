---
name: real-analysis-problem-solving
description: Use this skill when working on limits, convergence, or continuity problems in real analysis.
---

# Real Analysis Problem Solving

## When to Use

This skill is applicable for solving problems related to limits, convergence, and continuity in real analysis.

## Decision Tree

### Limits

1. **Direct Substitution**
   - Plug in the value directly; if determinate, that's the answer.

2. **Indeterminate Form? (0/0, inf/inf)**
   - Use algebraic manipulation or L'Hopital's rule.

3. **Squeeze Theorem**
   - Find functions g(x) and h(x) such that g(x) ≤ f(x) ≤ h(x) and verify limits.

4. **Epsilon-Delta Proof**
   - Set up |f(x) - L| < epsilon and find delta in terms of epsilon.

### Convergence

1. **Identify Sequence/Series Type**
   - Determine if it's geometric, p-series, or alternating.

2. **Apply Convergence Tests**
   - Use ratio test, root test, or comparison test.

3. **Verify Bounds**
   - Use Z3 to prove inequalities and check monotonicity.

4. **Compute Sum (if convergent)**
   - Calculate the sum of the series.

### Continuity

1. **Check Definition**
   - Ensure f(a) exists, lim_{x->a} f(x) exists, and lim_{x->a} f(x) = f(a).

2. **Use SymPy for Limit Check**
   - Compare limit with f(a).

3. **Piecewise Functions**
   - Check left and right limits separately.

4. **Verify with Z3**
   - Prove continuity at a point.

## Tool Commands

### Sympy_Limit
```bash
uv run python -m runtime.harness scripts/sympy_compute.py limit "<function>" --var <variable> --at <point>
```

### Sympy_Diff
```bash
uv run python -m runtime.harness scripts/sympy_compute.py diff "<function>" --var <variable>
```

### Sympy_Sum
```bash
uv run python -m runtime.harness scripts/sympy_compute.py sum "<series>" --var <variable> --from <start> --to <end>
```

### Z3_Prove
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "<condition>" --vars <variables>
```

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.