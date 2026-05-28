---
name: abstract-algebra
description: Use this skill when working on problems in abstract algebra, including fields, groups, and rings.
---

# Abstract Algebra

## When to Use

Use this skill when working on problems related to fields, groups, and rings in abstract algebra.

## Decision Tree

1. **Is F a field?**
   - (F, +) is an abelian group with identity 0.
   - (F \ {0}, *) is an abelian group with identity 1.
   - Distributive law holds.
   - Verify with `z3_solve.py prove "field_axioms"`.

2. **Is G a group under operation *?**
   - Check closure: a,b in G implies a*b in G?
   - Check associativity: (a*b)*c = a*(b*c)?
   - Check identity: exists e such that e*a = a*e = a?
   - Check inverses: for all a exists a^(-1) such that a*a^(-1) = e?
   - Verify with `z3_solve.py prove "group_axioms"`.

3. **Is R a ring?**
   - (R, +) is an abelian group.
   - Multiplication is associative.
   - Distributive laws: a(b+c) = ab + ac and (a+b)c = ac + bc.
   - Verify with `z3_solve.py prove "ring_axioms"`.

## Tool Commands

### Z3_Field_Axioms
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "field_axioms"
```

### Z3_Group_Axioms
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "group_axioms"
```

### Z3_Ring_Axioms
```bash
uv run python -m runtime.harness scripts/z3_solve.py prove "ring_axioms"
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

- **Field Extensions**: E is an extension of F if F is a subfield of E. Degree [E:F] = dimension of E as F-vector space.
- **Subgroup Test**: Show H is non-empty and that for all a, b in H: ab^(-1) in H.
- **Ring Properties**: Check if the ring is commutative, has unity, or is an integral domain.
- **Homomorphism Proof**: Verify properties for homomorphisms in groups and rings.

This skill consolidates the essential problem-solving strategies for fields, groups, and rings in abstract algebra, providing a comprehensive approach to tackling related problems.