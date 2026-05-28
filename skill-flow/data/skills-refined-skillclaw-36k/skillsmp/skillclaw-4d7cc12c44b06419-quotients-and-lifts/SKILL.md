---
name: quotients-and-lifts
description: Use this skill when you need to work effectively with Lean 4 quotients in ComputationalPaths, including defining functions, proving equality, and handling nested lifts.
---

# Skill body

## Core Operations

### 1) Defining a function out of a quotient: `Quot.lift`

To define a map `Quot r → B`, provide:
- a function on representatives `f : A → B`
- a proof it respects the relation `hf : ∀ a b, r a b → f a = f b`

```lean
def myFun : Quot r → B :=
  Quot.lift
    (fun x => f x)  -- function on representatives
    (fun a b h => ...) -- proof: r a b → f a = f b
```

### 2) Proving something for all quotient elements: `Quot.ind`

Use quotient induction to reduce to representatives:

```lean
theorem myThm (q : Quot r) : P q := by
  induction q using Quot.ind with
  | _ x => ...  -- prove for representative
```

### 3) Proving equality in a quotient: `Quot.sound`

When the goal is an equality of quotient terms, typically:

```lean
-- goal: Quot.mk r a = Quot.mk r b
exact Quot.sound hab
```

`hab` must have the quotient’s underlying relation type.

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

- Lean 4 does not provide `Quot.liftOn₂` - prefer nested `Quot.lift`.
- Proof obligations for nested lifts often require `funext` and `Quot.ind`.

## Practical checklist for “respects relation” proofs

When `Quot.lift` fails due to the second argument:
1. Identify the quotient relation `r`.
2. Prove a lemma of the shape `r a b → f a = f b`.
3. If the lemma produces the reverse direction, wrap with symmetry.
4. Use `simp` lemmas for simplification.