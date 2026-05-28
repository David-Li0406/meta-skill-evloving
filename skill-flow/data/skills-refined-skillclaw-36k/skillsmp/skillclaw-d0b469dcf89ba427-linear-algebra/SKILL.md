---
name: linear-algebra
description: Use this skill when solving problems related to linear algebra, including matrices, eigenvalues, and vector spaces.
---

# Skill body

## When to Use

Use this skill when working on problems in linear algebra, including eigenvalues, matrices, and vector spaces.

## Decision Tree

1. **Eigenvalues and Eigenvectors**
   - Compute the characteristic polynomial: `det(A - lambda*I) = 0`
     ```bash
     uv run python -m runtime.harness scripts/sympy_compute.py charpoly "[[a,b],[c,d]]" --var lam
     ```
   - Find eigenvalues by solving the characteristic polynomial:
     ```bash
     uv run python -m runtime.harness scripts/sympy_compute.py eigenvalues "[[1,2],[3,4]]"
     ```
   - For each eigenvalue, find eigenvectors by solving \((A - \lambda I)v = 0\):
     ```bash
     uv run python -m runtime.harness scripts/sympy_compute.py eigenvectors "[[1,2],[3,4]]"
     ```
   - Verify the result: Check \(Av = \lambda v\) with:
     ```bash
     uv run python -m runtime.harness scripts/z3_solve.py prove
     ```

2. **Matrix Operations**
   - Identify matrix type (square, symmetric, etc.):
     ```bash
     uv run python -m runtime.harness scripts/sympy_compute.py matrix_type "[[a,b],[c,d]]"
     ```
   - Perform basic operations:
     - Multiplication:
       ```bash
       uv run python -m runtime.harness scripts/sympy_compute.py matmul "A" "B"
       ```
     - Inverse:
       ```bash
       uv run python -m runtime.harness scripts/sympy_compute.py inverse "A"
       ```
     - Transpose:
       ```bash
       uv run python -m runtime.harness scripts/sympy_compute.py transpose "A"
       ```
   - Solve linear systems \(Ax = b\):
     ```bash
     uv run python -m runtime.harness scripts/sympy_compute.py linsolve "A" "b"
     ```

3. **Vector Spaces**
   - Check if a set is a subspace:
     - Contains zero vector?
     - Closed under addition?
     - Closed under scalar multiplication?
     - Verify with:
       ```bash
       uv run python -m runtime.harness scripts/z3_solve.py prove "subspace_closed"
       ```
   - Determine linear independence:
     - Set up \(Ax = 0\) where columns are vectors:
       ```bash
       uv run python -m runtime.harness scripts/sympy_compute.py nullspace "A"
       ```
   - Find basis and dimension:
     - Use reduced row echelon form:
       ```bash
       uv run python -m runtime.harness scripts/sympy_compute.py rref "A"
       ```

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.