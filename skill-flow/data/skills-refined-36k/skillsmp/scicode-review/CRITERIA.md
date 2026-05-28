# SciCode Review Criteria

Comprehensive criteria for reviewing SciCode benchmark tasks.

---

## Paper Selection Criteria

### Must Meet ALL Requirements

| Criterion | Requirement | How to Verify |
|-----------|-------------|---------------|
| Publication Date | After February 2025 | Check arXiv/journal date |
| Content Type | Novel computational algorithm | Not just analysis/theory |
| Implementation | numpy/scipy compatible | No specialized libraries |
| Decomposition | 8-10 subproblems | Count step files |
| Output Type | Numerical values | Check return types |

### Automatic Rejection

Reject immediately if:
- Paper before February 2025 (in model training data)
- Survey paper without novel contribution
- Method requires specialized software/datasets
- Ambiguous problem with multiple valid solutions
- Outputs are strings instead of numbers

---

## Decomposition Quality

### Good Decomposition

Each step should:

1. **Have Scientific Meaning**
   - Represents a meaningful computation
   - Can be understood independently
   - Has clear input/output semantics

2. **Be Independently Testable**
   - Function can be tested in isolation
   - Output can be numerically compared
   - Doesn't require running other steps

3. **Follow Logical Progression**
   - Each step builds on previous outputs
   - No circular dependencies
   - Final step is most general/complex

4. **Match Paper Algorithm**
   - Captures the novel process from paper
   - Follows paper's mathematical formulation
   - Doesn't skip important steps

### Poor Decomposition (Red Flags)

- Steps that just call other steps
- Steps with no meaningful output
- Steps that duplicate functionality
- Missing key algorithmic components
- Order doesn't match paper's flow

---

## Code Quality Criteria

### Function Signatures

```python
# GOOD: Type hints, clear names
def compute_leverage_scores(matrix: np.ndarray, rank: int) -> np.ndarray:

# BAD: No types, unclear names
def func(x, r):
```

### Docstrings

```python
# GOOD: Complete documentation
def compute_leverage_scores(matrix: np.ndarray, rank: int) -> np.ndarray:
    """Compute statistical leverage scores for matrix rows.

    Parameters
    ----------
    matrix : np.ndarray, shape (m, n)
        Input matrix with m rows and n columns
    rank : int
        Target rank for approximation

    Returns
    -------
    scores : np.ndarray, shape (m,)
        Leverage score for each row

    Notes
    -----
    Uses ridge regression with regularization lambda = 0.1
    """

# BAD: Missing or incomplete
def compute_leverage_scores(matrix, rank):
    """Compute scores."""
```

### Numerical Stability

```python
# GOOD: Handles edge cases
def safe_divide(a, b, tolerance=1e-10):
    if abs(b) < tolerance:
        raise ValueError(f"Division by near-zero value: {b}")
    return a / b

# BAD: No protection
def divide(a, b):
    return a / b  # Will fail on b=0
```

---

## Test Case Criteria

### Minimum Requirements

- [ ] 2-3 test cases per step
- [ ] Tests use reproducible inputs (random seeds)
- [ ] Tests cover normal/typical case
- [ ] Tests cover at least one edge case

### Good Test Design

```python
def test_cases():
    return [
        # Test 1: Simple, manually verifiable
        {
            "setup": """
A = np.array([[1, 0], [0, 1]], dtype=float)
rank = 1
""",
            "call": "compute_leverage_scores(A, rank)",
            "gold_call": "_gold_compute_leverage_scores(A, rank)",
        },
        # Test 2: Typical random case
        {
            "setup": """
np.random.seed(42)
A = np.random.randn(10, 5)
rank = 3
""",
            "call": "compute_leverage_scores(A, rank)",
            "gold_call": "_gold_compute_leverage_scores(A, rank)",
        },
        # Test 3: Edge case
        {
            "setup": """
A = np.array([[1.0]])  # 1x1 matrix
rank = 1
""",
            "call": "compute_leverage_scores(A, rank)",
            "gold_call": "_gold_compute_leverage_scores(A, rank)",
        },
    ]
```

### Bad Test Design (Red Flags)

- Only one test case
- No random seed (non-reproducible)
- No edge cases tested
- Tests that always pass
- Overly complex setup code

---

## Gold Solution Criteria

### Requirements

1. **Correctness**: Matches paper's algorithm exactly
2. **Completeness**: Handles all specified inputs
3. **Stability**: Numerically robust
4. **Clarity**: Readable and maintainable

### Verification Steps

1. Read the corresponding paper section
2. Compare gold solution to paper's algorithm
3. Check formula implementation
4. Verify edge case handling
5. Run tests and confirm 100% pass

---

## problem.yaml Criteria

### Required Fields

| Field | Requirement |
|-------|-------------|
| `problem_id` | Unique snake_case, matches directory |
| `problem_name` | Human-readable title |
| `domain` | One of: physics, chemistry, biology, mathematics, materials |
| `subdomain` | Specific area |
| `description` | 2-4 clear sentences |
| `io_spec` | Complete I/O documentation |
| `dependencies` | All imports listed |
| `steps` | All step files in order |

### I/O Spec Quality

Should include:
- Parameter names and types
- Array shapes with variables (n, m)
- Return value types and shapes
- Units if applicable
- Convergence criteria for iterative methods

---

## Background File Criteria

### When Required

- Complex mathematical concepts
- Domain-specific knowledge
- Non-obvious algorithms
- Stability considerations

### Content Requirements

- [ ] Overview section
- [ ] Mathematical formulation with LaTeX
- [ ] Algorithm description
- [ ] Implementation notes
- [ ] No excessive length

---

## Difficulty Assessment

### Target Difficulty

- SOTA models should solve < 10% of tasks
- Novel algorithms not in training data
- Complex multi-step reasoning required

### Signs of Appropriate Difficulty

- 8-10 subproblems with dependencies
- Requires understanding paper's contribution
- Numerical precision matters
- Multiple concepts to integrate

### Signs of Insufficient Difficulty

- Fewer than 8 subproblems
- Standard algorithms (already in training data)
- Simple formula translation
- No integration of concepts

---

## Review Scoring Rubric

### Scoring Scale (1-5)

| Score | Meaning |
|-------|---------|
| 5 | Excellent - Ready to merge |
| 4 | Good - Minor issues |
| 3 | Acceptable - Some issues to fix |
| 2 | Poor - Major issues |
| 1 | Unacceptable - Needs complete rework |

### Scoring Categories

1. **Paper Selection** (1-5)
   - Date, novelty, decomposability

2. **Decomposition Quality** (1-5)
   - Scientific meaning, independence, progression

3. **Code Quality** (1-5)
   - Types, docs, stability

4. **Test Coverage** (1-5)
   - Quantity, variety, edge cases

5. **Documentation** (1-5)
   - YAML, docstrings, background

### Approval Threshold

- All categories >= 3
- Average >= 4
- No blocking issues
