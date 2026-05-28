---
name: category-theory
description: Use this skill when working on problems in category theory, including limits, functors, and natural transformations.
---

# Category Theory Skill

## When to Use

Use this skill when working on various problems in category theory, including limits, functors, and natural transformations.

## Decision Tree

1. **Limits and Colimits**
   - **Identify Limit Type**
     - Product: limit of discrete diagram
     - Equalizer: limit of parallel pair f, g: A -> B
     - Pullback: limit of A -> C <- B
     - Terminal object: limit of empty diagram
   - **Verify Universal Property**
     - Cone from L with projections pi_i: L -> D_i
     - For any cone from X, unique morphism u: X -> L
     - Triangles commute: pi_i . u = cone_i
   - **Colimit (Dual)**
     - Coproduct: colimit of discrete diagram
     - Coequalizer: colimit of parallel pair
     - Pushout: colimit of A <- C -> B
   - **Compute Limits Concretely**
     - In Set: product = Cartesian product, Equalizer = {x | f(x) = g(x)}, Pullback = {(a,b) | f(a) = g(b)}

2. **Categories and Functors**
   - **Verify Category Axioms**
     - Objects and morphisms defined?
     - Identity morphism for each object: id_A: A -> A
     - Composition associative: (f . g) . h = f . (g . h)
   - **Check Functor Properties**
     - F: C -> D maps objects to objects, arrows to arrows
     - Preserves identity: F(id_A) = id_{F(A)}
     - Preserves composition: F(g . f) = F(g) . F(f)
   - **Common Functors**
     - Forgetful functor: forgets structure (e.g., Grp -> Set)
     - Free functor: left adjoint to forgetful
     - Hom functor: Hom(A, -) or Hom(-, B)

3. **Natural Transformations**
   - **Verify Naturality**
     - eta: F => G is natural transformation between functors F, G: C -> D
     - For each f: A -> B in C, diagram commutes: G(f) . eta_A = eta_B . F(f)
   - **Component Analysis**
     - eta_A: F(A) -> G(A) for each object A
   - **Natural Isomorphism**
     - Each component eta_A is isomorphism
   - **Functor Category**
     - [C, D] has functors as objects, natural transformations as morphisms

## Tool Commands

### Lean4_Limit
```bash
# Lean 4: import CategoryTheory.Limits.Shapes.Products
```

### Lean4_Category
```bash
# Lean 4 with Mathlib: import CategoryTheory.Category.Basic
```

### Lean4_Naturality
```bash
# Lean 4: theorem nat : η.app B ≫ G.map f = F.map f ≫ η.app A := η.naturality
```

### Lean4_Build
```bash
lake build  # Compiler-in-the-loop verification
```

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.