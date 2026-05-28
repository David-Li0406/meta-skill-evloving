---
name: math-help
description: Use this skill when you need guidance on which mathematical tools to use for various tasks and computations.
---

# Math Cognitive Stack Guide

Cognitive prosthetics for exact mathematical computation. This guide helps you choose the right tool for your math task.

## Quick Reference

| I want to... | Use this | Example |
|--------------|----------|---------|
| Solve equations | sympy_compute.py solve | `solve "x**2 - 4 = 0" --var x` |
| Integrate/differentiate | sympy_compute.py | `integrate "sin(x)" --var x` |
| Compute limits | sympy_compute.py limit | `limit "sin(x)/x" --var x --to 0` |
| Matrix operations | sympy_compute.py / numpy_compute.py | `det "[[1,2],[3,4]]"` |
| Verify a reasoning step | math_scratchpad.py verify | `verify "x = 2 implies x^2 = 4"` |
| Check a proof chain | math_scratchpad.py chain | `chain --steps '[...]'` |
| Get progressive hints | math_tutor.py hint | `hint "Solve x^2 - 4 = 0" --level 2` |
| Generate practice problems | math_tutor.py generate | `generate --topic algebra --difficulty 2` |
| Prove a theorem (constraints) | z3_solve.py prove | `prove "x + y == y + x" --vars x y` |
| Check satisfiability | z3_solve.py sat | `sat "x > 0, x < 10, x*x == 49"` |
| Optimize with constraints | z3_solve.py optimize | `optimize "x + y" --constraints "..."` |
| Plot 2D/3D functions | math_plot.py | `plot2d "sin(x)" --range -10 10` |
| Arbitrary precision | mpmath_compute.py | `pi --dps 100` |
| Numerical optimization | scipy_compute.py | `minimize "x**2 + 2*x" "5"` |
| Formal machine proof | Lean 4 (lean4 skill) | `/lean4` |

## The Five Layers

### Layer 1: SymPy (Symbolic Algebra)

**When:** Exact algebraic computation - solving, calculus, simplification, matrix algebra.

**Key Commands:**
```bash
# Solve equation
uv run python -m runtime.harness scripts/sympy_compute.py \
    solve "x**2 - 5*x + 6 = 0" --var x --domain real

# Integrate
uv run python -m runtime.harness scripts/sympy_compute.py \
    integrate "sin(x)" --var x

# Definite integral
uv run python -m runtime.harness scripts/sympy_compute.py \
    integrate "x**2" --var x --bounds 0 1

# Differentiate (2nd order)
uv run python -m runtime.harness scripts/sympy_compute.py \
    diff "x**3" --var x --order 2

# Simplify (trig strategy)
uv run python -m runtime.harness scripts/sympy_compute.py \
    simplify "sin(x)**2 + cos(x)**2" --strategy trig
```