---
name: logical-proof-strategies
description: Use this skill when working on problems in mathematical logic, including proof theory, propositional logic, and predicate logic.
---

# Logical Proof Strategies

## When to Use

Use this skill when addressing problems in mathematical logic, encompassing proof theory, propositional logic, and predicate logic.

## Decision Tree

1. **Proof Strategy Selection**
   - Direct proof: assume premises, derive conclusion
   - Proof by contradiction: assume negation, derive false
   - Proof by cases: split on disjunction
   - Induction: base case + inductive step

2. **Structural Induction**
   - Define well-founded ordering on structures
   - Base: prove for minimal elements
   - Step: assume for smaller, prove for current

3. **Cut Elimination**
   - Gentzen's Hauptsatz: cuts can be eliminated
   - Useful for proof normalization

4. **Completeness/Soundness Check**
   - Soundness: if provable then valid
   - Completeness: if valid then provable

5. **Quantifier Analysis (Predicate Logic)**
   - Identify: ForAll (universal), Exists (existential)
   - Scope of quantifiers and free/bound variables

6. **Prenex Normal Form (Predicate Logic)**
   - Move all quantifiers to front
   - Standardize variables to avoid capture

7. **Truth Table Method (Propositional Logic)**
   - For small formulas (<=4 variables): enumerate all valuations
   - Tautology = all T, Contradiction = all F

8. **Natural Deduction (Propositional Logic)**
   - Apply inference rules: Modus Ponens, Modus Tollens
   - Conditional proof: assume antecedent, derive consequent

9. **Semantic Tableaux (Propositional Logic)**
   - Build tree by decomposing formula
   - Closed branches = contradictions

10. **Resolution Proof (Predicate Logic)**
    - Convert to CNF, negate conclusion
    - Apply resolution rule until empty clause or saturation

11. **Model Theory (Predicate Logic)**
    - Construct countermodel to refute invalid argument
    - Finite model for finite domain

## Tool Commands

### Z3 Induction Base
```bash
uv run python -m runtime.harness scripts/cc_math/z3_solve.py prove "P(0)"
```

### Z3 Induction Step
```bash
uv run python -m runtime.harness scripts/cc_math/z3_solve.py prove "ForAll([n], Implies(P(n), P(n+1)))"
```

### Z3 Soundness
```bash
uv run python -m runtime.harness scripts/cc_math/z3_solve.py prove "Implies(derivable(phi), valid(phi))"
```

### Z3 Sat
```bash
uv run python -m runtime.harness scripts/z3_solve.py sat "And(p, Implies(p, q), Not(q))"
```

### Sympy Truth Table
```bash
uv run python -m runtime.harness scripts/sympy_compute.py truthtable "p & (p >> q) >> q"
```

### Z3 ForAll
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "ForAll([x], Implies(P(x), Q(x)))"
```

### Z3 Model
```bash
uv run python -m runtime.harness scripts/z3_solve.py model "Exists([x], P(x))"
```

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.