---
name: real-analysis-problem-solving
description: Use this skill when tackling problems related to limits, continuity, and convergence in real analysis.
---

# Skill body

## When to Use

Use this skill when working on limits, continuity, or convergence problems in real analysis.

## Decision Tree

1. **Limits**
   - **Direct Substitution**: Try plugging in the value directly. If you get a determinate form, that's the answer.
   - **Indeterminate Form? (0/0, inf/inf)**: 
     - Try algebraic manipulation (factor, rationalize).
     - Use L'Hopital's rule: `sympy_compute.py diff` on numerator/denominator.
   - **Squeeze Theorem**: If bounded, find \( g(x) \leq f(x) \leq h(x) \) where \( \lim g = \lim h \). Verify bounds with `z3_solve.py prove`.
   - **Epsilon-Delta Proof**: For rigorous proof, set up \( |f(x) - L| < \epsilon \). Find delta in terms of epsilon and verify with `math_scratchpad.py verify`.

2. **Continuity**
   - **Check Definition**: Ensure \( f(a) \) exists, \( \lim_{x \to a} f(x) \) exists, and \( \lim_{x \to a} f(x) = f(a) \).
   - **Use SymPy for Limit Check**: `sympy_compute.py limit "f(x)" --var x --at a` and compare with \( f(a) \).
   - **Piecewise Functions**: Check left and right limits separately using `sympy_compute.py limit "f(x)" --var x --at a --dir left`.
   - **Verify with Z3**: `z3_solve.py prove "limit_exists implies continuous"`.

3. **Convergence**
   - **Identify Sequence/Series Type**: 
     - Geometric series: \( |r| < 1 \) converges.
     - p-series: \( p > 1 \) converges.
     - Alternating series: check decreasing and limit 0.
   - **Apply Convergence Tests**: 
     - Ratio test: `sympy_compute.py limit "a_{n+1}/a_n"`.
     - Root test: `sympy_compute.py limit "a_n^{(1/n)}"`.
     - Comparison test: find bounding series.
   - **Verify Bounds**: Use `z3_solve.py prove` for inequality bounds and check monotonicity with derivatives.
   - **Compute Sum (if convergent)**: `sympy_compute.py sum "a_n" --var n --from 0 --to oo`.

## Tool Commands

### Sympy_Limit
```bash
uv run python -m runtime.harness scripts/sympy_compute.py limit "sin(x)/x" --var x --at 0
```

### Sympy_Diff
```bash
uv run python -m runtime.harness scripts/sympy_compute.py diff "x**2" --var x
```

### Z3_Prove
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "limit_bound" --vars x
```

### Sympy_Sum
```bash
uv run python -m runtime.harness scripts/sympy_compute.py sum "1/n**2" --var n --from 1 --to oo
```