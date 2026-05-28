---
name: lean-hit-development
description: Use this skill when adding new Higher Inductive Types (HITs) to the ComputationalPaths library, defining fundamental group calculations, or implementing encode-decode proofs.
---

# Higher Inductive Type Development

This skill guides the implementation of new Higher Inductive Types (HITs) in the ComputationalPaths Lean 4 library, following established patterns for axiom declarations, recursion principles, and fundamental group calculations.

## File Location

New HITs go in `ComputationalPaths/Path/HIT/YourHIT.lean`

## Required Structure

```lean
import ComputationalPaths.Path.Homotopy.FundamentalGroup
import ComputationalPaths.Path.Rewrite.SimpleEquiv
-- other imports as needed

namespace ComputationalPaths.Path.HIT

/-! ## Type and Constructor Axioms -/

axiom YourHIT : Type u
axiom yourHITBase : YourHIT
axiom yourHITLoop : Path yourHITBase yourHITBase

/-! ## Recursion Principle -/

axiom YourHIT.rec {β : Type v} (base : β) (loop : Path base base) : YourHIT → β
axiom YourHIT.rec_base : YourHIT.rec base yourHITLoop yourHITBase = base

/-! ## Path Recursion (for encode) -/

axiom YourHIT.recPath {a : YourHIT} (P : YourHIT → Type)
  (pbase : P yourHITBase)
  (ploop : Path (transport P yourHITLoop pbase) pbase)
  : (x : YourHIT) → P x

/-! ## Presentation Type -/

-- Define the group presentation
inductive YourGroupWord
  | e : YourGroupWord           -- identity
  | gen : YourGroupWord         -- generator(s)
  | inv : YourGroupWord → YourGroupWord
  | mul : YourGroupWord → YourGroupWord → YourGroupWord

inductive YourGroupRel : YourGroupWord → YourGroupWord → Prop
  | inv_left : YourGroupRel (mul (inv w) w) e
  | inv_right : YourGroupRel (mul w (inv w)) e
  -- group-specific relations

def YourGroupPresentation := Quot YourGroupRel

/-! ## Encode-Decode -/

-- Decode: presentation → π₁
noncomputable def decode : YourGroupPresentation → π₁(YourHIT, yourHITBase) :=
  Quot.lift
    (fun w => wordToLoop w)
    (fun _ _ h => Quot.sound (decode_respects_rel h))

-- Encode: π₁ → presentation
noncomputable def encode : π₁(YourHIT, yourHITBase) → YourGroupPresentation := ...

noncomputable def piOneEquiv : SimpleEquiv (π₁(YourHIT, yourHITBase)) YourGroupPresentation where
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