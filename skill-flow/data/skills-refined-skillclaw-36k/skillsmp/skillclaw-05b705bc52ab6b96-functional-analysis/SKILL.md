---
name: functional-analysis
description: Use this skill when working on problems in functional analysis, including Banach spaces, operator theory, and Hilbert spaces.
---

# Functional Analysis

## When to Use

Use this skill when addressing problems in functional analysis, which encompasses Banach spaces, operator theory, and Hilbert spaces.

## Decision Tree

1. **Verify Space Properties**
   - For Banach spaces: Check completeness of normed vector space.
   - For Hilbert spaces: Verify orthogonal decomposition and projection properties.

2. **Banach Space Techniques**
   - **Hahn-Banach Theorem**: Extend bounded linear functionals.
   - **Open Mapping Theorem**: Surjective bounded operator is open.
   - **Closed Graph Theorem**: Closed graph implies bounded operator.
   - **Uniform Boundedness Principle**: Pointwise bounded family of operators is uniformly bounded.

3. **Operator Theory Techniques**
   - **Bounded Operator Verification**: Check if ||Tx|| <= M||x|| for some M.
   - **Adjoint Operator**: Define T* using inner products.
   - **Spectral Theory**: Analyze spectrum and self-adjoint properties.
   - **Compact Operators**: Verify compactness through closure properties.

4. **Hilbert Space Techniques**
   - **Orthogonal Decomposition**: Express elements as sums of projections.
   - **Projection Theorem**: Establish existence and uniqueness of nearest points.
   - **Riesz Representation**: Relate functionals to inner products.
   - **Parseval's Identity**: Relate norms to sums of inner products.
   - **Bessel's Inequality**: Establish bounds for orthonormal sets.

## Tool Commands

### Banach Space Tools
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "completeness"
uv run python -m runtime.harness scripts/z3_solve.py prove "extension_exists"
uv run python -m runtime.harness scripts/z3_solve.py prove "open_mapping"
uv run python -m runtime.harness scripts/z3_solve.py prove "closed_graph_implies_bounded"
```

### Operator Theory Tools
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "operator_bounded"
uv run python -m runtime.harness scripts/sympy_compute.py simplify "<Tx, y> - <x, T_star_y>"
uv run python -m runtime.harness scripts/z3_solve.py prove "self_adjoint implies real_spectrum"
uv run python -m runtime.harness scripts/sympy_compute.py limit "norm(T - T_n)" --var n --at oo
```

### Hilbert Space Tools
```bash
uv run python -m runtime.harness scripts/sympy_compute.py simplify "x - projection"
uv run python -m runtime.harness scripts/z3_solve.py prove "projection_exists_unique"
uv run python -m runtime.harness scripts/z3_solve.py prove "bounded_linear_functional iff inner_product_form"
uv run python -m runtime.harness scripts/sympy_compute.py sum "abs(<x, e_n>)**2" --var n --from 1 --to oo
```

## Key Techniques

*From indexed textbooks:*

- [Introductory Functional Analysis with Applications] This resource covers essential properties and theorems relevant to functional analysis, including the behavior of operators and the structure of various spaces.