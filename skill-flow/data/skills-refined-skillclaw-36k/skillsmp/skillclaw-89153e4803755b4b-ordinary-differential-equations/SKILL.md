---
name: ordinary-differential-equations
description: Use this skill when solving ordinary differential equations (ODEs) of various orders, including first, second, and boundary value problems.
---

# Ordinary Differential Equations

## When to Use

Use this skill when working on ordinary differential equations (ODEs) problems, including first-order, second-order, and boundary value problems.

## Decision Tree

1. **Classify the ODE**
   - **First Order:**
     - Linear: \( y' + P(x)y = Q(x) \)?
     - Separable: \( y' = f(x)g(y) \)?
     - Exact: \( M(x,y)dx + N(x,y)dy = 0 \) with \( \frac{dM}{dy} = \frac{dN}{dx} \)?
     - Bernoulli: \( y' + P(x)y = Q(x)y^n \)?
   - **Second Order:**
     - Constant coefficients: \( ay'' + by' + cy = f(x) \)?
     - Variable coefficients: \( y'' + P(x)y' + Q(x)y = R(x) \)?
     - Cauchy-Euler: \( x^2 y'' + bxy' + cy = 0 \)?
   - **Boundary Value Problems:**
     - Two-point BVP: conditions at \( x=a \) and \( x=b \)?
     - Sturm-Liouville: eigenvalue problem?

2. **Select Solution Method**
   - **First Order:**
     - Separable: Separate and integrate.
     - Linear: Use integrating factor \( e^{\int P \, dx} \).
     - Exact: Find potential function.
     - Bernoulli: Substitute \( v = y^{1-n} \).
   - **Second Order:**
     - Homogeneous with constant coefficients: Solve characteristic equation.
     - Particular solution (non-homogeneous): Use undetermined coefficients or variation of parameters.
     - Numerical solution: Convert to first-order system and use `scipy.integrate.solve_ivp`.
   - **Boundary Value Problems:**
     - Shooting method: Convert BVP to IVP and iterate to satisfy boundary conditions.
     - Finite difference method: Discretize domain and solve the resulting linear system.

3. **Numerical Solution (IVP)**
   - Use `scipy.integrate.solve_ivp(f, [t0, tf], y0, method='RK45')` for general cases.
   - For stiff systems, use `method='Radau'` or `method='BDF'`.

4. **Verify Solution**
   - Substitute back into the ODE.
   - Check initial/boundary conditions.

5. **Phase Portrait (Autonomous)**
   - Find equilibria: \( f(y^*) = 0 \).
   - Analyze stability: sign of \( f'(y^*) \).

## Tool Commands

### Scipy_Solve_Ivp
```bash
uv run python -c "from scipy.integrate import solve_ivp; sol = solve_ivp(lambda t, y: -y, [0, 5], [1]); print('y(5) =', sol.y[0][-1])"
```

### Sympy_Dsolve
```bash
uv run python -m runtime.harness scripts/sympy_compute.py dsolve "Derivative(y,x) + y" --ics "{y(0): 1}"
```

### Scipy_Solve_Bvp
```bash
uv run python -c "from scipy.integrate import solve_bvp; import numpy as np; ode = lambda x, y: [y[1], -y[0]]; bc = lambda ya, yb: [ya[0], yb[0]-1]; x = np.linspace(0, np.pi, 10); y = np.zeros((2, 10)); sol = solve_bvp(ode, bc, x, y); print('Solution at pi/2:', sol.sol(np.pi/2)[0])"
```

### Sympy_Linsolve
```bash
uv run python -m runtime.harness scripts/sympy_compute.py linsolve "tridiagonal_matrix" "boundary_vector"
```

## Key Techniques

*From indexed textbooks:*

- [Elementary Differential Equations and... (Z-Library)] Solving ODEs with MATLAB (New York: Cambridge).
- [An Introduction to Numerical Analysis... (Z-Library)] Modern Numerical Methods for Ordinary Differential Equations.