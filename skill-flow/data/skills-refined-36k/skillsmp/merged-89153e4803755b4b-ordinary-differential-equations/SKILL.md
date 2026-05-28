---
name: ordinary-differential-equations
description: Use this skill when solving ordinary differential equations (ODEs) of various orders and types.
---

# Ordinary Differential Equations

## When to Use

Use this skill when working on ordinary differential equations (ODEs) problems, including first-order, second-order, and boundary value problems.

## Decision Tree

### First Order ODEs
1. **Classify the ODE**
   - Linear: \( y' + P(x)y = Q(x) \)?
   - Separable: \( y' = f(x)g(y) \)?
   - Exact: \( M(x,y)dx + N(x,y)dy = 0 \) with \( \frac{dM}{dy} = \frac{dN}{dx} \)?
   - Bernoulli: \( y' + P(x)y = Q(x)y^n \)?

2. **Select Solution Method**
   | Type | Method |
   |------|--------|
   | Separable | Separate and integrate |
   | Linear | Integrating factor \( e^{\int P \, dx} \) |
   | Exact | Find potential function |
   | Bernoulli | Substitute \( v = y^{1-n} \) |

3. **Numerical Solution (IVP)**
   - Use `scipy.integrate.solve_ivp(f, [t0, tf], y0, method='RK45')` for non-stiff systems.
   - For stiff systems, use `method='Radau'` or `method='BDF'`.

4. **Verify Solution**
   - Substitute back into ODE and check initial/boundary conditions.

5. **Phase Portrait (Autonomous)**
   - Find equilibria: \( f(y^*) = 0 \).
   - Analyze stability: sign of \( f'(y^*) \).

### Second Order ODEs
1. **Classify the ODE**
   - Constant coefficients: \( ay'' + by' + cy = f(x) \)?
   - Variable coefficients: \( y'' + P(x)y' + Q(x)y = R(x) \)?
   - Cauchy-Euler: \( x^2 y'' + bxy' + cy = 0 \)?

2. **Homogeneous with Constant Coefficients**
   - Characteristic equation: \( ar^2 + br + c = 0 \).
   - Distinct real roots: \( y = c_1 e^{r_1 x} + c_2 e^{r_2 x} \).
   - Repeated root: \( y = (c_1 + c_2 x)e^{r x} \).
   - Complex roots: \( y = e^{ax}(c_1 \cos(bx) + c_2 \sin(bx)) \).

3. **Particular Solution (Non-homogeneous)**
   - Use undetermined coefficients or variation of parameters.

4. **Numerical Solution**
   - Convert to first-order system and use `solve_ivp`.

5. **Boundary Value Problems**
   - Use shooting method or `scipy.integrate.solve_bvp(ode, bc, x, y_init)`.

### Boundary Value Problems
1. **Problem Classification**
   - Two-point BVP: conditions at \( x=a \) and \( x=b \)?
   - Sturm-Liouville: eigenvalue problem?
   - Mixed conditions: Dirichlet, Neumann, Robin?

2. **Shooting Method**
   - Convert BVP to IVP and iterate to satisfy boundary conditions.

3. **Finite Difference Method**
   - Discretize domain and replace derivatives with differences.

4. **Collocation/BVP Solver**
   - Use `scipy.integrate.solve_bvp(ode, bc, x, y_init)`.

5. **Eigenvalue Problems**
   - Sturm-Liouville form: \( -(p(x)y')' + q(x)y = \lambda w(x)y \).

## Tool Commands

### First Order ODEs
```bash
uv run python -c "from scipy.integrate import solve_ivp; sol = solve_ivp(lambda t, y: -y, [0, 5], [1]); print('y(5) =', sol.y[0][-1])"
```

### Second Order ODEs
```bash
uv run python -m runtime.harness scripts/sympy_compute.py dsolve "Derivative(y,x,2) + y"
```

### Boundary Value Problems
```bash
uv run python -c "from scipy.integrate import solve_bvp; import numpy as np; ode = lambda x, y: [y[1], -y[0]]; bc = lambda ya, yb: [ya[0], yb[0]-1]; x = np.linspace(0, np.pi, 10); y = np.zeros((2, 10)); sol = solve_bvp(ode, bc, x, y); print('Solution at pi/2:', sol.sol(np.pi/2)[0])"
```

## Key Techniques

*From indexed textbooks:*

- [Elementary Differential Equations and... (Z-Library)] Various methods and applications for solving ODEs.
- [An Introduction to Numerical Analysis... (Z-Library)] Modern numerical methods for ODEs.

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.