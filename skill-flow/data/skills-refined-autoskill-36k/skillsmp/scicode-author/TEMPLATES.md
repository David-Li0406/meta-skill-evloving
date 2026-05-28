# SciCode Templates

Complete templates for all task files.

## problem.yaml Template

```yaml
# =============================================================================
# Task Definition
# =============================================================================

# TASK IDENTIFIER - unique snake_case name
problem_id: "your_task_name"

# DISPLAY NAME - human-readable title
problem_name: "Your Task Title"

# DOMAIN - one of: physics, chemistry, biology, mathematics, materials
domain: "mathematics"

# SUBDOMAIN - specific area
# Mathematics: Numerical Linear Algebra, Computational Mechanics
# Physics: Optics, Quantum Information, Statistical Mechanics, Particle Physics
# Chemistry: Computational Chemistry, DFT, Molecular Dynamics
# Biology: Biochemistry, Population Dynamics
# Materials: Semiconductor Materials
subdomain: "numerical linear algebra"

# =============================================================================
# Problem Description (shown to LLM)
# =============================================================================

description: |
  2-4 sentences describing the problem goal.

  What algorithm are you implementing?
  What does a complete solution accomplish?
  Include important domain context.

# =============================================================================
# I/O Specification (shown to LLM)
# =============================================================================

io_spec: |
  """
  Task Title

  Parameters
  ----------
  matrix : np.ndarray, shape (n, n)
      Input matrix description
  tolerance : float
      Convergence tolerance (e.g., 1e-10)
  max_iter : int, optional
      Maximum iterations (default: 1000)

  Returns
  -------
  result : np.ndarray, shape (n, n)
      Description of output
  iterations : int
      Number of iterations performed

  Notes
  -----
  - For iterative solvers: specify convergence metric
  - Specify what to return if not converged
  """

# =============================================================================
# Dependencies
# =============================================================================

dependencies:
  - import numpy as np
  - from scipy import linalg
  - from typing import Tuple, List
  # Add only what's needed

# =============================================================================
# Steps (in execution order, without .py extension)
# =============================================================================

steps:
  - 01_first_step
  - 02_second_step
  - 03_third_step
  - 04_fourth_step
  - 05_fifth_step
  - 06_sixth_step
  - 07_seventh_step
  - 08_final_step
  # Minimum 8 steps, aim for 8-10

# =============================================================================
# Background (optional)
# =============================================================================

background_main: |
  Optional: General background for the entire problem.
  Include key concepts that apply to all steps.
  Delete if not needed.
```

---

## Step File Template (steps/01_step_name.py)

```python
"""
STEP DESCRIPTION (this entire docstring is shown to the LLM)

Explain what this step implements. Include:
- Clear description of the function's purpose
- Mathematical formulas (use LaTeX notation if helpful)
- Edge cases to handle
- Constraints (e.g., "matrix must be positive definite")

Example:
    "Implement a function to compute the LU decomposition of a square matrix
    using partial pivoting. The function should return separate L and U
    matrices along with the permutation vector."
"""

import numpy as np
from typing import Tuple


# =============================================================================
# FUNCTION SIGNATURE (shown to the LLM)
# =============================================================================

def step_function(matrix: np.ndarray, tolerance: float = 1e-10) -> Tuple[np.ndarray, np.ndarray]:
    """Compute decomposition factors for the input matrix.

    Parameters
    ----------
    matrix : np.ndarray, shape (n, n)
        Input square matrix (must be non-singular)
    tolerance : float, optional
        Tolerance for detecting singular values (default: 1e-10)

    Returns
    -------
    L : np.ndarray, shape (n, n)
        Lower triangular factor
    U : np.ndarray, shape (n, n)
        Upper triangular factor

    Examples
    --------
    >>> A = np.array([[4, 1], [1, 3]], dtype=float)
    >>> L, U = step_function(A)
    >>> np.allclose(L @ U, A)
    True
    """
    return L, U  # <- This becomes the "return hint" shown to model


# =============================================================================
# GOLD SOLUTION (NOT shown to LLM)
# =============================================================================

def _gold_step_function(matrix: np.ndarray, tolerance: float = 1e-10) -> Tuple[np.ndarray, np.ndarray]:
    """Reference implementation - generates expected test outputs."""
    n = matrix.shape[0]
    L = np.eye(n)
    U = matrix.copy().astype(float)

    for k in range(n - 1):
        if abs(U[k, k]) < tolerance:
            raise ValueError(f"Zero pivot at position {k}")
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]

    return L, U


# =============================================================================
# TEST CASES
# =============================================================================

def test_cases():
    """Test case specifications.

    Each test case has:
    - setup: Code to create test variables
    - call: How to call the function being tested
    - gold_call: How to call the gold solution

    Include 2-3 test cases covering:
    - Normal/typical inputs
    - Edge cases (small matrices, special structures)
    - Boundary conditions
    """
    return [
        {
            # Test case 1: Simple 3x3 matrix
            "setup": """
n = 3
A = np.array([[4, 1, 0],
              [1, 4, 1],
              [0, 1, 4]], dtype=float)
tol = 1e-10
""",
            "call": "step_function(A, tol)",
            "gold_call": "_gold_step_function(A, tol)",
        },
        {
            # Test case 2: Random positive definite matrix
            "setup": """
np.random.seed(42)
n = 5
A = np.random.randn(n, n)
A = A @ A.T + n * np.eye(n)  # Make positive definite
tol = 1e-8
""",
            "call": "step_function(A, tol)",
            "gold_call": "_gold_step_function(A, tol)",
        },
        {
            # Test case 3: Edge case - 2x2 matrix
            "setup": """
A = np.array([[2, 1],
              [1, 2]], dtype=float)
tol = 1e-12
""",
            "call": "step_function(A, tol)",
            "gold_call": "_gold_step_function(A, tol)",
        },
    ]
```

---

## Background File Template (background/01_concept.md)

```markdown
# Background: [Concept Name]

## Overview

Brief conceptual explanation of the topic. What is it? Why is it important?

## Mathematical Formulation

Key formulas using LaTeX:

$$A = LU$$

where:
- $L$ is lower triangular with unit diagonal
- $U$ is upper triangular

## Algorithm Description

1. Initialize L as identity, U as copy of A
2. For each column k:
   - Compute multipliers: $l_{ik} = u_{ik} / u_{kk}$
   - Update rows: $u_{ij} = u_{ij} - l_{ik} u_{kj}$

## Implementation Notes

- **Numerical stability**: Use pivoting for small diagonal elements
- **Complexity**: O(n^3) operations
- **Memory**: Can be done in-place

## Common Pitfalls

1. Forgetting to handle zero pivots
2. Integer overflow with large matrices
3. Accumulation of rounding errors

## References

- [Paper author], "[Paper title]", arXiv:XXXX.XXXXX (2025)
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Task ID | `snake_case` | `hankel_low_rank` |
| Step files | `##_descriptive_name.py` | `01_construct_matrix.py` |
| Main function | `descriptive_name` | `construct_matrix` |
| Gold solution | `_gold_descriptive_name` | `_gold_construct_matrix` |
| Background | `##_concept.md` | `01_matrix_theory.md` |

---

## Test Case Design Tips

### Cover Multiple Scenarios

```python
def test_cases():
    return [
        # 1. Simple/small case (easy to verify manually)
        {"setup": "A = np.eye(3)", ...},

        # 2. Typical random case
        {"setup": "np.random.seed(42); A = np.random.randn(10,10)", ...},

        # 3. Edge case (boundary condition)
        {"setup": "A = np.array([[1.0]])", ...},
    ]
```

### Use Appropriate Tolerances

```python
# For floating-point comparisons
import numpy.testing as npt
npt.assert_allclose(actual, expected, rtol=1e-5, atol=1e-8)
```

### Set Random Seeds

```python
"setup": """
np.random.seed(42)  # Reproducible randomness
A = np.random.randn(5, 5)
"""
```
