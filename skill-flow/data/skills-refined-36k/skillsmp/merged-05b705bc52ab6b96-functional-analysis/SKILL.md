---
name: functional-analysis
description: Use this skill when working on problems in functional analysis, including Banach spaces, operator theory, and Hilbert spaces.
---

# Functional Analysis

## When to Use

Use this skill when addressing problems in functional analysis, covering Banach spaces, operator theory, and Hilbert spaces.

## Decision Tree

### Banach Spaces
1. **Verify Banach space**
   - Complete normed vector space
   - Check: every Cauchy sequence converges
   - `z3_solve.py prove "completeness"`

2. **Hahn-Banach Theorem**
   - Extend bounded linear functionals
   - Separate convex sets
   - `z3_solve.py prove "extension_exists"`

3. **Open Mapping Theorem**
   - Surjective bounded operator between Banach spaces is open
   - Consequence: bounded inverse exists
   - `z3_solve.py prove "open_mapping"`

4. **Closed Graph Theorem**
   - T: X -> Y has closed graph implies T bounded
   - Strategy: verify graph closure, conclude boundedness
   - `z3_solve.py prove "closed_graph_implies_bounded"`

5. **Uniform Boundedness Principle**
   - Pointwise bounded family of operators is uniformly bounded

### Operator Theory
1. **Bounded operator verification**
   - ||Tx|| <= M||x|| for some M
   - Operator norm: ||T|| = sup{||Tx|| : ||x|| = 1}
   - `z3_solve.py prove "operator_bounded"`

2. **Adjoint operator**
   - <Tx, y> = <x, T*y> defines T*
   - For matrices: T* = conjugate transpose
   - `sympy_compute.py simplify "<Tx, y> - <x, T*y>"`

3. **Spectral Theory**
   - Spectrum: sigma(T) = {lambda : T - lambda*I not invertible}
   - Self-adjoint: spectrum is real
   - `z3_solve.py prove "self_adjoint_real_spectrum"`

4. **Compact operators**
   - T compact if T(bounded set) has compact closure
   - Approximable by finite-rank operators
   - `sympy_compute.py limit "||T - T_n||" --var n`

5. **Spectral Theorem**
   - Self-adjoint compact: T = sum(lambda_n * P_n)
   - eigenvalues -> 0, eigenvectors form orthonormal basis

### Hilbert Spaces
1. **Orthogonal decomposition**
   - For closed subspace M: H = M + M^perp (direct sum)
   - Every x = P_M(x) + P_{M^perp}(x)
   - `sympy_compute.py simplify "x - projection"`

2. **Projection Theorem**
   - For closed convex C, unique nearest point exists
   - P_C is nonexpansive: ||P_C(x) - P_C(y)|| <= ||x - y||
   - `z3_solve.py prove "projection_exists_unique"`

3. **Riesz Representation**
   - Every f in H* has form f(x) = <x, y_f> for unique y_f
   - ||f|| = ||y_f||
   - `z3_solve.py prove "riesz_representation"`

4. **Parseval's Identity**
   - For orthonormal basis {e_n}: ||x||^2 = sum|<x, e_n>|^2
   - `sympy_compute.py sum "abs(<x, e_n>)**2"`

5. **Bessel's Inequality**
   - sum|<x, e_n>|^2 <= ||x||^2 for any orthonormal set

## Tool Commands

### Z3 Completeness
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "cauchy_sequence implies convergent"
```

### Z3 Bounded Operator
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "norm(Tx) <= M*norm(x)"
```

### Z3 Projection
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "x - P_M(x) in M_perp"
```

### Sympy Norm
```bash
uv run python -m runtime.harness scripts/sympy_compute.py simplify "norm(alpha*x + beta*y)"
```

### Sympy Inner Product
```bash
uv run python -m runtime.harness scripts/sympy_compute.py simplify "<x + y, z> == <x,z> + <y,z>"
```

### Sympy Parseval
```bash
uv run python -m runtime.harness scripts/sympy_compute.py sum "abs(<x, e_n>)**2" --var n --from 1 --to oo
```

## Key Techniques

*From indexed textbooks:*

- [Introductory Functional Analysis with Applications] Discusses the properties and applications of Banach and Hilbert spaces, including completeness, orthogonality, and bounded linear operators.
- [Measure, Integration Real Analysis] Covers foundational concepts in functional analysis relevant to operator theory and Hilbert spaces.
- [Real Analysis] Explores the implications of the Hahn-Banach theorem and spectral theory in functional analysis.

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.