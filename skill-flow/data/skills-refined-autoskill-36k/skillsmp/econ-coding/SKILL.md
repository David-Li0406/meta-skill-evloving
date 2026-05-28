---
name: econ-coding
description: Scientific Python coding for economic research. Use when writing computational economics code, numerical methods, solvers, simulations, or research scripts.
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
---

# Scientific Computing for Economics

## Python Stack

### Core Libraries
```python
import numpy as np              # Arrays, linear algebra
import scipy.optimize as opt    # Solvers, optimization
import scipy.stats as stats     # Distributions, tests
import pandas as pd             # Data manipulation
import matplotlib.pyplot as plt # Plotting
```

### Specialized Libraries
```python
import statsmodels.api as sm    # Econometrics
import linearmodels as lm       # Panel data, IV
import numba                    # JIT compilation
from scipy.interpolate import interp1d  # Interpolation
```

## Code Organization Pattern

```
project/
├── model.py          # Model definition, equations
├── calibration.py    # Parameter calibration
├── solver.py         # Numerical solution methods
├── simulation.py     # Monte Carlo, counterfactuals
├── analysis.py       # Results processing
├── plots.py          # Visualization
├── utils.py          # Helper functions
└── main.py           # Entry point, runs everything
```

## Numerical Methods Recipes

### Root Finding (Equilibrium)
```python
from scipy.optimize import brentq, fsolve

# Single equation (bracketed)
x_star = brentq(f, a, b)

# System of equations
x_star = fsolve(F, x0)
```

### Optimization
```python
from scipy.optimize import minimize, minimize_scalar

# Unconstrained
result = minimize(f, x0, method='BFGS')

# Constrained
result = minimize(f, x0, method='SLSQP',
                  constraints={'type': 'eq', 'fun': g})

# Bounded scalar
result = minimize_scalar(f, bounds=(a, b), method='bounded')
```

### Fixed Point Iteration
```python
def fixed_point(T, x0, tol=1e-8, maxiter=1000):
    """Solve x = T(x) by iteration."""
    x = x0
    for i in range(maxiter):
        x_new = T(x)
        if np.max(np.abs(x_new - x)) < tol:
            return x_new
        x = x_new
    raise ValueError("Did not converge")
```

### Value Function Iteration
```python
def vfi(V0, beta, u, transition, tol=1e-6):
    """Standard VFI for discrete state space."""
    V = V0.copy()
    while True:
        V_new = u + beta * transition @ V
        if np.max(np.abs(V_new - V)) < tol:
            return V_new
        V = V_new
```

## Performance Tips

### Vectorization
```python
# Bad: loop over elements
result = np.zeros(n)
for i in range(n):
    result[i] = f(x[i])

# Good: vectorized operation
result = f(x)  # if f is numpy-compatible
# or
result = np.vectorize(f)(x)  # fallback
```

### Numba JIT
```python
from numba import jit

@jit(nopython=True)
def fast_loop(x, y):
    n = len(x)
    result = 0.0
    for i in range(n):
        result += x[i] * y[i]
    return result
```

## Output Formatting

### LaTeX Tables
```python
def to_latex_table(df, caption, label):
    """Convert DataFrame to LaTeX table."""
    latex = df.to_latex(
        float_format="%.3f",
        caption=caption,
        label=label,
        escape=False
    )
    return latex
```

### Publication Figures
```python
def setup_plot():
    """Standard plot settings."""
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 12,
        'legend.fontsize': 10,
        'figure.figsize': (8, 5),
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight'
    })
```

## Reproducibility Checklist

1. **Random seeds**: Set `np.random.seed(42)` at start
2. **Version pinning**: Use `requirements.txt` with versions
3. **Parameter files**: Store calibration in JSON/YAML
4. **Output logging**: Save all results with timestamps
5. **Git commits**: Tag releases, meaningful commit messages

### Parameter File Example
```python
import json

# Save parameters
params = {'beta': 0.96, 'sigma': 2.0, 'alpha': 0.33}
with open('params.json', 'w') as f:
    json.dump(params, f, indent=2)

# Load parameters
with open('params.json', 'r') as f:
    params = json.load(f)
```

## Common Pitfalls

1. **Float comparison**: Use `np.isclose()`, not `==`
2. **Mutable defaults**: Don't use `def f(x=[]):`
3. **Copy vs view**: Use `.copy()` when modifying arrays
4. **Integer division**: Python 3 uses `/` for float division
5. **Overflow**: Check for large exponentials, use `np.log` domain
