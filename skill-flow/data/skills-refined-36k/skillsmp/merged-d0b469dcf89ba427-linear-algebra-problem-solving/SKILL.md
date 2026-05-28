---
name: linear-algebra-problem-solving
description: Use this skill when working on various problems in linear algebra, including eigenvalues, matrices, and vector spaces.
---

# Linear Algebra Problem Solving

## When to Use

Use this skill when addressing problems related to eigenvalues, matrices, and vector spaces in linear algebra.

## Decision Tree

### Eigenvalues

1. **Compute Characteristic Polynomial**
   - det(A - lambda*I) = 0
   - `sympy_compute.py charpoly "<matrix>" --var lam`

2. **Find Eigenvalues**
   - Solve characteristic polynomial
   - `sympy_compute.py eigenvalues "<matrix>"`

3. **Find Eigenvectors**
   - For each eigenvalue lambda: solve (A - lambda*I)v = 0
   - `sympy_compute.py eigenvectors "<matrix>"`

4. **Verify**
   - Check Av = lambda*v with `z3_solve.py prove`
   - Verify algebraic/geometric multiplicity

### Matrices

1. **Identify Matrix Type**
   - Square, symmetric, orthogonal, diagonal?
   - Check properties with `sympy_compute.py matrix_type "<matrix>"`

2. **Basic Operations**
   - Multiplication: `sympy_compute.py matmul "<matrix_A>" "<matrix_B>"`
   - Inverse: `sympy_compute.py inverse "<matrix>"`
   - Transpose: `sympy_compute.py transpose "<matrix>"`

3. **Solve Linear Systems**
   - Ax = b: `sympy_compute.py linsolve "<matrix_A>" "<vector_b>"`
   - Check consistency with `z3_solve.py sat`

4. **Decompositions**
   - LU: `sympy_compute.py lu "<matrix>"`
   - QR: `sympy_compute.py qr "<matrix>"`
   - SVD: `sympy_compute.py svd "<matrix>"`

### Vector Spaces

1. **Check Subspace**
   - Contains zero vector?
   - Closed under addition?
   - Closed under scalar multiplication?
   - Verify with `z3_solve.py prove`

2. **Linear Independence**
   - Set up Ax = 0 where columns are vectors
   - `sympy_compute.py nullspace "<matrix>"`

3. **Basis and Dimension**
   - Find spanning set, remove dependent vectors
   - `sympy_compute.py rref "<matrix>"` to find pivot columns
   - Dimension = number of pivots

4. **Change of Basis**
   - Find transition matrix P
   - New coords = P^(-1) * old coords
   - `sympy_compute.py inverse "<matrix_P>"`

## Tool Commands

### Eigenvalues
```bash
uv run python -m runtime.harness scripts/sympy_compute.py eigenvalues "<matrix>"
```

### Characteristic Polynomial
```bash
uv run python -m runtime.harness scripts/sympy_compute.py charpoly "<matrix>" --var lam
```

### Matrix Inverse
```bash
uv run python -m runtime.harness scripts/sympy_compute.py inverse "<matrix>"
```

### Linear System Solver
```bash
uv run python -m runtime.harness scripts/sympy_compute.py linsolve "<matrix_A>" "<vector_b>"
```

### Nullspace
```bash
uv run python -m runtime.harness scripts/sympy_compute.py nullspace "<matrix>"
```

### RREF
```bash
uv run python -m runtime.harness scripts/sympy_compute.py rref "<matrix>"
```

### Z3 Verification
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "<condition>"
```

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.