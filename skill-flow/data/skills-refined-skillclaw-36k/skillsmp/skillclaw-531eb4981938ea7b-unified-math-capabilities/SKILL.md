---
name: unified-math-capabilities
description: Use this skill when you need to perform mathematical computations, solve equations, or seek explanations in mathematics.
---

# Skill body

## Overview
**One entry point for all computation and explanation.** I route to the right tool based on your request.

For formal proofs, use `/prove` instead.

## Quick Examples

| You Say | I Use |
|---------|-------|
| "Solve x² - 4 = 0" | SymPy solve |
| "Integrate sin(x) from 0 to π" | SymPy integrate |
| "Eigenvalues of [[1,2],[3,4]]" | SymPy eigenvalues |
| "Is x² + 1 > 0 for all x?" | Z3 prove |
| "Convert 5 miles to km" | Pint |
| "Explain what a functor is" | Category theory skill |

## Computation Scripts

### SymPy (Symbolic Math)
```bash
uv run python "$CLAUDE_PROJECT_DIR/.claude/scripts/math/sympy_compute.py" <command> <args>
```

| Command | Description | Example |
|---------|-------------|---------|
| `solve` | Solve equations | `solve "x**2 - 4" --var x` |
| `integrate` | Definite/indefinite integral | `integrate "sin(x)" --var x --lower 0 --upper pi` |
| `diff` | Derivative | `diff "x**3" --var x` |
| `simplify` | Simplify expression | `simplify "sin(x)**2 + cos(x)**2"` |
| `limit` | Compute limit | `limit "sin(x)/x" --var x --point 0` |
| `series` | Taylor expansion | `series "exp(x)" --var x --point 0 --n 5` |
| `dsolve` | Solve ODE | `dsolve "f''(x) + f(x)" --func f --var x` |
| `laplace` | Laplace transform | `laplace "sin(t)" --var t` |

### Matrix Operations
| Command | Description |
|---------|-------------|
| `det` | Determinant |
| `eigenvalues` | Eigenvalues |
| `eigenvectors` | Eigenvectors with multiplicities |
| `inverse` | Matrix inverse |
| `transpose` | Transpose |
| `rref` | Row echelon form |
| `rank` | Matrix rank |
| `nullspace` | Null space basis |
| `linsolve` | Linear system Ax=b |
| `charpoly` | Characteristic polynomial |

### Number Theory
| Command | Description |
|---------|-------------|
| `factor` | Factor polynomial |
| `factorint` | Prime factorization |
| `isprime` | Primality test |
| `gcd` | Greatest common divisor |
| `lcm` | Least common multiple |
| `modinverse` | Modular inverse |

### Combinatorics
| Command | Description |
|---------|-------------|
| `binomial` | C(n,k) |
| `factorial` | n! |
| `permutations` | Number of permutations |
| `combinations` | Number of combinations |