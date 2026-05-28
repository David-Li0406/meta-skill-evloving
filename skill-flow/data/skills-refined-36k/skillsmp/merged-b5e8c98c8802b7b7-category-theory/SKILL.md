---
name: category-theory
description: Use this skill when working on problems related to limits, colimits, functors, and natural transformations in category theory.
---

# Category Theory

## When to Use

Use this skill when working on problems in category theory, including limits, colimits, functors, and natural transformations.

## Decision Trees

### Limits and Colimits

1. **Identify Limit Type**
   - Product: limit of discrete diagram
   - Equalizer: limit of parallel pair f, g: A -> B
   - Pullback: limit of A -> C <- B
   - Terminal object: limit of empty diagram

2. **Verify Universal Property**
   - Cone from L with projections pi_i: L -> D_i
   - For any cone from X, unique morphism u: X -> L
   - Triangles commute: pi_i . u = cone_i

3. **Colimit (Dual)**
   - Coproduct: colimit of discrete diagram
   - Coequalizer: colimit of parallel pair
   - Pushout: colimit of A <- C -> B
   - Initial object: colimit of empty diagram

4. **Compute Limits Concretely**
   - In Set: product = Cartesian product
   - Equalizer = {x | f(x) = g(x)}
   - Pullback = {(a,b) | f(a) = g(b)}

5. **Preservation**
   - Right adjoint preserves limits
   - Left adjoint preserves colimits
   - Representable functors preserve limits

### Categories and Functors

1. **Verify Category Axioms**
   - Objects and morphisms (arrows) defined?
   - Identity morphism for each object: id_A: A -> A
   - Composition associative: (f . g) . h = f . (g . h)

2. **Check Functor Properties**
   - F: C -> D maps objects to objects, arrows to arrows
   - Preserves identity: F(id_A) = id_{F(A)}
   - Preserves composition: F(g . f) = F(g) . F(f)

3. **Functor Types**
   - Covariant: preserves arrow direction
   - Contravariant: reverses arrow direction
   - Faithful/Full: injective/surjective on Hom-sets
   - Equivalence: full, faithful, essentially surjective

4. **Common Functors**
   - Forgetful functor: forgets structure (e.g., Grp -> Set)
   - Free functor: left adjoint to forgetful
   - Hom functor: Hom(A, -) or Hom(-, B)

### Natural Transformations

1. **Verify Naturality**
   - eta: F => G is natural transformation between functors F, G: C -> D
   - For each f: A -> B in C, diagram commutes: G(f) . eta_A = eta_B . F(f)

2. **Component Analysis**
   - eta_A: F(A) -> G(A) for each object A
   - Each component is morphism in target category D

3. **Natural Isomorphism**
   - Each component eta_A is isomorphism
   - Functors F and G are naturally isomorphic

4. **Functor Category**
   - [C, D] has functors as objects
   - Natural transformations as morphisms

5. **Yoneda Lemma Application**
   - Nat(Hom(A, -), F) ~ F(A) naturally in A

## Tool Commands

### Lean4 Commands
```bash
# Lean 4: import CategoryTheory.Limits.Shapes.Products
# Lean 4: IsLimit.lift cone -- unique morphism from universal property
# Lean 4: theorem assoc : (f ≫ g) ≫ h = f ≫ (g ≫ h) := Category.assoc
# Lean 4: theorem map_comp (F : C ⥤ D) : F.map (g ≫ f) = F.map g ≫ F.map f := F.map_comp
# Lean 4: theorem nat : η.app B ≫ G.map f = F.map f ≫ η.app A := η.naturality
# Lean 4: CategoryTheory.yonedaEquiv -- Yoneda lemma
# Lean 4: lake build  # Compiler-in-the-loop verification
```

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.