---
name: pymoo
description: Use this skill when you need to solve single or multi-objective optimization problems using advanced evolutionary algorithms and analyze trade-offs between competing objectives.
---

# Pymoo - Multi-Objective Optimization in Python

## Overview

Pymoo is a comprehensive Python framework for optimization with an emphasis on multi-objective problems. It allows you to solve both single and multi-objective optimization tasks using state-of-the-art algorithms (NSGA-II, NSGA-III, MOEA/D), benchmark problems (ZDT, DTLZ), and customizable genetic operators. Pymoo excels at finding trade-off solutions (Pareto fronts) for problems with conflicting objectives.

## When to Use This Skill

This skill should be used when:
- Solving optimization problems with one or multiple objectives.
- Finding Pareto-optimal solutions and analyzing trade-offs.
- Implementing evolutionary algorithms (GA, DE, PSO, NSGA-II/III).
- Working with constrained optimization problems.
- Benchmarking algorithms on standard test problems (ZDT, DTLZ, WFG).
- Customizing genetic operators (crossover, mutation, selection).
- Visualizing high-dimensional optimization results.
- Making decisions from multiple competing solutions.
- Handling binary, discrete, continuous, or mixed-variable problems.

## Core Concepts

### The Unified Interface

Pymoo uses a consistent `minimize()` function for all optimization tasks:

```python
from pymoo.optimize import minimize

result = minimize(
    problem,        # What to optimize
    algorithm,      # How to optimize
    termination,    # When to stop
    seed=1,
    verbose=True
)
```

**Result object contains:**
- `result.X`: Decision variables of optimal solution(s).
- `result.F`: Objective values of optimal solution(s).
- `result.G`: Constraint violations (if constrained).
- `result.algorithm`: Algorithm object with history.

### Problem Types

- **Single-objective:** One objective to minimize/maximize.
- **Multi-objective:** 2-3 conflicting objectives → Pareto front.
- **Many-objective:** 4+ objectives → High-dimensional Pareto front.
- **Constrained:** Objectives + inequality/equality constraints.
- **Dynamic:** Time-varying objectives or constraints.

## Quick Start Workflows

### Workflow 1: Single-Objective Optimization

**When:** Optimizing one objective function.

**Steps:**
1. Define or select the problem.
2. Choose a single-objective algorithm (GA, DE, PSO, CMA-ES).
3. Configure termination criteria.
4. Run optimization.
5. Extract the best solution.