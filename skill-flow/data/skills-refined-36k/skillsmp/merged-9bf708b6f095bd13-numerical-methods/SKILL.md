---
name: numerical-methods
description: Use this skill when working on problems involving interpolation and numerical integration in numerical methods.
---

# Numerical Methods

## When to Use

Use this skill when working on interpolation and numerical integration problems in numerical methods.

## Interpolation

### Decision Tree

1. **Assess Data Characteristics**
   - How many data points? Spacing uniform or non-uniform?
   - Is data smooth or noisy?
   - Need derivatives at endpoints?

2. **Select Interpolation Method**
   - Few points (<10): Polynomial (Lagrange, Newton)
   - Many points, smooth data: Cubic splines
   - Noisy data: Smoothing splines or least squares
   - High dimensions: Use simplex-based (n+1 neighbors vs 2^n)

3. **Implement with SciPy**
   - `scipy.interpolate.CubicSpline(x, y)` - natural cubic spline
   - `scipy.interpolate.make_interp_spline(x, y, k=3)` - B-spline
   - `scipy.interpolate.interp1d(x, y, kind='cubic')` - 1D interpolation

4. **Validate Results**
   - Check for Runge's phenomenon at boundaries (high-degree polynomials)
   - Cross-validate: leave-one-out error estimation
   - Visual inspection of interpolated curve

### Tool Commands

#### Scipy_Cubic_Spline
```bash
uv run python -c "from scipy.interpolate import CubicSpline; import numpy as np; x = np.array([0,1,2,3]); y = np.array([0,1,4,9]); cs = CubicSpline(x, y); print(cs(1.5))"
```

#### Scipy_Bspline
```bash
uv run python -c "from scipy.interpolate import make_interp_spline; import numpy as np; x = np.array([0,1,2,3]); y = np.array([0,1,4,9]); bspl = make_interp_spline(x, y, k=3); print(bspl(1.5))"
```

#### Sympy_Lagrange
```bash
uv run python -m runtime.harness scripts/sympy_compute.py interpolate "[(0,0),(1,1),(2,4)]" --var x
```

## Numerical Integration

### Decision Tree

1. **Identify Integral Type**
   - Definite integral over finite interval?
   - Improper integral (infinite bounds or singularities)?
   - Multiple dimensions?

2. **Select Quadrature Method**
   - Smooth function, finite interval: Gaussian quadrature
   - Oscillatory integrand: specialized methods (Filon, Levin)
   - Singularity at endpoint: adaptive methods
   - `scipy.integrate.quad(f, a, b)` for general 1D

3. **Adaptive Integration**
   - Let algorithm subdivide where needed
   - Specify error tolerances (rtol, atol)

4. **Multiple Dimensions**
   - `scipy.integrate.dblquad` for 2D
   - `scipy.integrate.tplquad` for 3D
   - Monte Carlo for higher dimensions

5. **Verify Accuracy**
   - Compare with known analytic solutions
   - Check convergence by refining tolerance

### Tool Commands

#### Scipy_Quad
```bash
uv run python -c "from scipy.integrate import quad; import numpy as np; result, err = quad(lambda x: np.sin(x), 0, np.pi); print('Integral:', result, 'Error:', err)"
```

#### Scipy_Dblquad
```bash
uv run python -c "from scipy.integrate import dblquad; result, err = dblquad(lambda y, x: x*y, 0, 1, 0, 1); print('Integral:', result)"
```

#### Sympy_Integrate
```bash
uv run python -m runtime.harness scripts/sympy_compute.py integrate "sin(x)" --var x --from 0 --to "pi"
```

## Key Techniques

*From indexed textbooks:*

- Interpolation theory is foundational for numerical integration and differentiation.
- Piecewise-polynomial interpolation is commonly used for smooth functions.
- Numerical integration methods continue to evolve, addressing special classes of problems.

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.