---
name: topology-problem-solving
description: Use this skill when working on problems related to connectedness and compactness in topology.
---

# Skill body

## When to Use

Use this skill when addressing problems in topology, specifically those involving connectedness and compactness.

## Decision Tree

### Connectedness

1. **Is X connected?**
   - **Strategy 1 - Contradiction:**
     * Assume X = U union V where U, V are disjoint, non-empty, and open.
     * Derive a contradiction.
   - **Strategy 2 - Path connectedness:**
     * Show for all x,y in X, there exists a continuous path f: [0,1] -> X with f(0)=x, f(1)=y.
   - **Strategy 3 - Fan lemma:**
     * If {A_i} are connected sharing a common point, then union A_i is connected.

2. **Connectedness Proofs**
   - Show no separation exists.
   - Use `z3_solve.py prove "no_separation"`.

3. **Path Connectedness**
   - Construct explicit path: f(t) = (1-t)x + ty for convex sets.
   - Use `sympy_compute.py simplify "(1-t)*x + t*y"` to verify path.

4. **Components**
   - Connected component: maximal connected subset containing x.
   - Path component: maximal path-connected subset containing x.

### Compactness

1. **Is X compact?**
   - If X subset R^n: Is X closed AND bounded? (Heine-Borel).
   - If X is metric: Does every sequence have a convergent subsequence?
   - General: Does every open cover have a finite subcover?
   - Use `z3_solve.py prove "bounded_and_closed"`.

2. **Compactness Tests**
   - Heine-Borel (R^n): closed + bounded = compact.
   - Sequential: every sequence has a convergent subsequence.
   - Use `sympy_compute.py limit "a_n" --var n` to check convergence.

3. **Product Spaces**
   - Tychonoff: product of compact spaces is compact.
   - Finite products preserve compactness directly.

4. **Consequences of Compactness**
   - Continuous image of compact is compact.
   - Continuous real function on compact attains max/min.
   - Use `sympy_compute.py maximum "f(x)" --var x --domain "[a,b]"`.

## Tool Commands

### Z3_No_Separation
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "no_separation"
```

### Z3_Bounded_Closed
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "bounded_and_closed"
```

### Sympy_Path
```bash
uv run python -m runtime.harness scripts/sympy_compute.py simplify "(1-t)*x + t*y"
```

### Sympy_Limit
```bash
uv run python -m runtime.harness scripts/sympy_compute.py limit "a_n" --var n --at oo
```

### Sympy_Maximum
```bash
uv run python -m runtime.harness scripts/sympy_compute.py maximum "f(x)" --var x --domain "[a,b]"
```