---
name: abstract-algebra
description: Use this skill when working on problems in abstract algebra, including fields, groups, and rings.
---

# Abstract Algebra

## When to Use

Use this skill when working on problems related to fields, groups, and rings in abstract algebra.

## Decision Trees

### Fields

1. **Is F a field?**
   - (F, +) is an abelian group with identity 0
   - (F \ {0}, *) is an abelian group with identity 1
   - Distributive law holds
   - `z3_solve.py prove "field_axioms"`

2. **Field Extensions**
   - E is an extension of F if F is a subfield of E
   - Degree [E:F] = dimension of E as F-vector space
   - `sympy_compute.py minpoly "alpha" --var x` for minimal polynomial

3. **Characteristic**
   - char(F) = smallest n > 0 where n*1 = 0, or 0 if none exists
   - char(F) is 0 or prime
   - For finite field: |F| = p^n where p = char(F)

4. **Algebraic Elements**
   - alpha is algebraic over F if it satisfies a polynomial with coefficients in F
   - `sympy_compute.py solve "p(alpha) = 0"` for algebraic relations

### Groups

1. **Is G a group under operation *?**
   - Check closure: a,b in G implies a*b in G?
   - Check associativity: (a*b)*c = a*(b*c)?
   - Check identity: exists e such that e*a = a*e = a?
   - Check inverses: for all a exists a^(-1) such that a*a^(-1) = e?
   - Verify with `z3_solve.py prove "group_axioms"`

2. **Subgroup Test**
   - Show H is non-empty (usually by showing e in H)
   - Show that for all a, b in H: ab^(-1) in H
   - `z3_solve.py prove "subgroup_criterion"`

3. **Homomorphism Proof**
   - Verify phi(ab) = phi(a)phi(b) for all a, b in G1
   - Note: phi(e1) = e2 and phi(a^(-1)) = phi(a)^(-1) follow automatically
   - `sympy_compute.py simplify "phi(a*b) - phi(a)*phi(b)"`

4. **Order and Structure**
   - Element order: smallest n where a^n = e
   - Group order: |G| = number of elements
   - Lagrange: |H| divides |G| for subgroup H

### Rings

1. **Is R a ring?**
   - (R, +) is an abelian group
   - Multiplication is associative
   - Distributive laws: a(b+c) = ab + ac and (a+b)c = ac + bc
   - `z3_solve.py prove "ring_axioms"`

2. **Ring Properties**
   - Commutative ring: ab = ba for all a, b?
   - Ring with unity: exists 1 such that 1*a = a*1 = a?
   - Integral domain: ab = 0 implies a = 0 or b = 0?
   - `z3_solve.py prove "integral_domain"`

3. **Ideals**
   - I is ideal if: I is an additive subgroup AND for all r in R, a in I: ra in I, ar in I
   - Principal ideal: (a) = {ra : r in R}
   - `sympy_compute.py simplify "r*a"` for ideal multiplication

4. **Ring Homomorphisms**
   - phi(a + b) = phi(a) + phi(b)
   - phi(ab) = phi(a)phi(b)
   - phi(1) = 1 (for rings with unity)

## Tool Commands

### Z3_Field_Axioms
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "field_axioms"
```

### Z3_Group_Axioms
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "ForAll([a,b,c], op(op(a,b),c) == op(a,op(b,c)))"
```

### Z3_Ring_Axioms
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "ForAll([a,b,c], a*(b+c) == a*b + a*c)"
```

### Sympy_Minpoly
```bash
uv run python -m runtime.harness scripts/sympy_compute.py minpoly "sqrt(2)" --var x
```

### Sympy_Simplify
```bash
uv run python -m runtime.harness scripts/sympy_compute.py simplify "phi(a*b) - phi(a)*phi(b)"
```

### Sympy_Ideal
```bash
uv run python -m runtime.harness scripts/sympy_compute.py simplify "r*a"
```

## Key Techniques

*From indexed textbooks:*

- [Abstract Algebra] Write a computer program to add and multiply mod n, for any n given as input. The output of these operations should be the least residues of the sums and products of two integers.
- [Abstract Algebra] Techniques for producing normal subgroups in groups of a given order.
- [Abstract Algebra] Important ways of constructing larger rings from a given ring.

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.