---
name: optimization-techniques
description: Use this skill when working on various optimization problems, including convex, constrained, and gradient-based methods.
---

# Optimization Techniques

## When to Use

Use this skill when tackling optimization problems that may involve convexity, constraints, or gradient methods.

## Decision Tree

1. **Verify Convexity (for Convex Problems)**
   - Objective function: Is the Hessian positive semidefinite?
   - Constraint set: Is it the intersection of convex sets?
   - Use `z3_solve.py prove "hessian_psd"` to verify.

2. **Problem Classification**
   | Type | Solver |
   |------|--------|
   | Linear Programming | `scipy.optimize.linprog` |
   | Quadratic Programming | `scipy.optimize.minimize(method='SLSQP')` |
   | General Convex | Interior point methods |
   | Semidefinite | CVXPY with SDP solver |

3. **Constraint Classification (for Constrained Problems)**
   - Equality: h(x) = 0
   - Inequality: g(x) <= 0
   - Bounds: l <= x <= u

4. **Lagrangian Method (for Equality Constraints)**
   - L(x, lambda) = f(x) + sum lambda_j * h_j(x)
   - Solve: grad_x L = 0 and h(x) = 0
   - Use `sympy_compute.py solve "grad_L_system"`.

5. **KKT Conditions (for Inequality Constraints)**
   - Extend Lagrangian with mu_i for g_i(x) <= 0.
   - Complementary slackness: mu_i * g_i(x) = 0.
   - Use `z3_solve.py prove "kkt_satisfied"`.

6. **Basic Gradient Descent (for Gradient Methods)**
   - Update: x_{k+1} = x_k - alpha * grad f(x_k).
   - Step size alpha: fixed, diminishing, or line search.
   - Convergence: O(1/k) for convex, linear for strongly convex.

7. **Step Size Selection**
   | Method | Approach |
   |--------|----------|
   | Fixed | alpha constant (requires tuning) |
   | Backtracking | Armijo condition: f(x - alpha*grad) <= f(x) - c*alpha*||grad||^2 |
   | Exact line search | Minimize f(x - alpha*grad) over alpha |
   | Adaptive | Adam, RMSprop (ML applications) |

8. **Accelerated Methods**
   - Momentum: add velocity term.
   - Nesterov: look-ahead gradient.
   - Conjugate gradient: for quadratic functions.
   - Use `scipy.optimize.minimize(f, x0, method='CG')`.

9. **Newton's Method**
   - Update: x_{k+1} = x_k - H^{-1} * grad f.
   - Requires Hessian (expensive but quadratic convergence).
   - Quasi-Newton (BFGS): approximate Hessian.
   - Use `scipy.optimize.minimize(f, x0, method='BFGS')`.

10. **Convergence Diagnostics**
    - Monitor ||grad f|| < tolerance.
    - Check function value decrease.
    - Watch for oscillation (step size too large).
    - Use `sympy_compute.py diff "f" --var x` for gradient.

## Tool Commands

### Scipy_Linprog
```bash
uv run python -c "from scipy.optimize import linprog; res = linprog([-1, -2], A_ub=[[1, 1], [2, 1]], b_ub=[4, 5]); print('Optimal:', -res.fun, 'at x=', res.x)"
```

### Scipy_Minimize
```bash
uv run python -c "from scipy.optimize import minimize; res = minimize(lambda x: (x[0]-1)**2 + (x[1]-2)**2, [0, 0]); print('Minimum at', res.x)"
```

### Scipy_Slsqp
```bash
uv run python -c "from scipy.optimize import minimize; cons = dict(type='eq', fun=lambda x: x[0] + x[1] - 1); res = minimize(lambda x: x[0]**2 + x[1]**2, [1, 1], method='SLSQP', constraints=cons); print('Min at', res.x)"
```

### Scipy_Bfgs
```bash
uv run python -c "from scipy.optimize import minimize; res = minimize(lambda x: (x[0]-1)**2 + 100*(x[1]-x[0]**2)**2, [0, 0], method='BFGS'); print('Rosenbrock min at', res.x)"
```

### Z3_Kkt
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "kkt_conditions"
```

### Sympy_Lagrangian
```bash
uv run python -m runtime.harness scripts/sympy_compute.py solve "[2*x - lam, 2*y - lam, x + y - 1]" --vars "[x, y, lam]"
```

### Sympy_Gradient
```bash
uv run python -m runtime.harness scripts/sympy_compute.py diff "x**2 + y**2" --var "[x, y]"
```