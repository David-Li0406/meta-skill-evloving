---
name: topology-problem-solving
description: Use this skill when working on connectedness and compactness problems in topology.
---

# Topology Problem Solving

## When to Use

Use this skill when addressing problems related to connectedness and compactness in topology.

## Decision Tree

### Connectedness

1. **Is X connected?**
   - Strategy 1 - Contradiction:
     * Assume X = U union V where U, V are disjoint, non-empty, and open
     * Derive a contradiction
   - Strategy 2 - Path connectedness:
     * Show for all x,y in X, exists continuous path f: [0,1] -> X with f(0)=x, f(1)=y
   - Strategy 3 - Fan lemma:
     * If {A_i} are connected sharing a common point, then union A_i is connected

2. **Connectedness Proofs**
   - Show no separation exists
   - Use intermediate value theorem for R subsets

3. **Path Connectedness**
   - Construct explicit path: f(t) = (1-t)x + ty for convex sets

4. **Components**
   - Connected component: maximal connected subset containing x
   - Path component: maximal path-connected subset containing x

### Compactness

1. **Is X compact?**
   - If X subset R^n: Is X closed AND bounded? (Heine-Borel)
   - If X is metric: Does every sequence have convergent subsequence?
   - General: Does every open cover have finite subcover?

2. **Compactness Tests**
   - Heine-Borel (R^n): closed + bounded = compact
   - Sequential: every sequence has convergent subsequence

3. **Product Spaces**
   - Tychonoff: product of compact spaces is compact
   - Finite products preserve compactness directly

4. **Consequences of Compactness**
   - Continuous image of compact is compact
   - Continuous real function on compact attains max/min

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

## Key Techniques

*From indexed textbooks:*

- Connectedness and compactness are fundamental concepts in topology, with various proofs and theorems supporting their properties.
- The Heine-Borel theorem states that a subset of R^n is compact if and only if it is closed and bounded.
- The Tychonoff theorem states that the product of compact spaces is compact.

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.