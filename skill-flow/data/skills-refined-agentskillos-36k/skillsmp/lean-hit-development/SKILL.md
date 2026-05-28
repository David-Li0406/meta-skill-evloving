---
name: lean-hit-development
description: Guides adding new Higher Inductive Types to the ComputationalPaths library. Use when creating new HITs, defining fundamental group (pi1) calculations, implementing encode-decode proofs, or adding new topological spaces.
---

# Higher Inductive Type Development

Add new HITs to the ComputationalPaths library.

## File Location

`ComputationalPaths/Path/HIT/YourHIT.lean`

## Required Structure

```lean
import ComputationalPaths.Path.Homotopy.FundamentalGroup

namespace ComputationalPaths.Path.HIT

/-! ## Type and Constructor Axioms -/

axiom YourHIT : Type u
axiom yourHITBase : YourHIT
axiom yourHITLoop : Path yourHITBase yourHITBase

/-! ## Recursion Principle -/

axiom YourHIT.rec {β : Type v} (base : β) (loop : Path base base) : YourHIT → β

/-! ## Encode-Decode for π₁ -/

noncomputable def decode : Presentation → π₁(YourHIT, yourHITBase) := ...
noncomputable def encode : π₁(YourHIT, yourHITBase) → Presentation := ...

noncomputable def piOneEquiv : SimpleEquiv (π₁(YourHIT, base)) Presentation where
  toFun := encode
  invFun := decode
  left_inv := decode_encode
  right_inv := encode_decode

end ComputationalPaths.Path.HIT
```

## Checklist

1. Define axioms for type and constructors
2. Define recursion principle
3. Create group presentation type
4. Implement encode/decode
5. Prove round-trip properties
6. Add to imports in `ComputationalPaths/Path.lean`
7. Update README

## Common HITs

| HIT | π₁ |
|-----|-----|
| Circle (S¹) | ℤ |
| Torus (T²) | ℤ × ℤ |
| Sphere (S²) | 1 (trivial) |
| Wedge (A ∨ B) | π₁(A) * π₁(B) |
