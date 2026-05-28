---
name: quotients-and-lifts
description: Work effectively with Lean 4 quotients in ComputationalPaths (Quot.lift/Quot.ind/Quot.sound), including nested lifts and common proof obligations.
---

# Quotients & Lifts

Work with Lean 4 quotients in ComputationalPaths.

## Core Operations

### Define function out of quotient

```lean
def myFun : Quot r → B :=
  Quot.lift
    (fun x => f x)  -- function on representatives
    (fun a b h => ...) -- proof: r a b → f a = f b
```

### Prove equality in quotient

```lean
Quot.sound : r a b → Quot.mk r a = Quot.mk r b
```

### Induction on quotient

```lean
theorem my_thm (q : Quot r) : P q := by
  induction q using Quot.ind with
  | _ x => ...  -- prove for representative
```

## Nested Quotients

For `Quot r → Quot s → C`, use nested lifts:

```lean
def myFun₂ : Quot r → Quot s → C :=
  Quot.lift
    (fun a => Quot.lift
      (fun b => f a b)
      (fun b₁ b₂ h => ...))
    (fun a₁ a₂ h => funext (Quot.ind (fun b => ...)))
```

## Important Notes

- **No `Quot.liftOn₂`** in Lean 4 - use nested `Quot.lift`
- Proof obligation for nested lifts often needs `funext` + `Quot.ind`

## Example (from Circle.lean)

```lean
noncomputable def encode : π₁(Circle, circleBase) → Int :=
  Quot.lift
    encodePath
    (fun _ _ h => encodePath_respects_rweq h)
```
