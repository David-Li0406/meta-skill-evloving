---
name: quotients-and-lifts
description: Work effectively with Lean 4 quotients in ComputationalPaths, including defining functions, proving equality, and using nested lifts.
---

# Quotients & Lifts (Lean 4)

This skill provides a practical guide to working with `Quot`-based quotients in the ComputationalPaths codebase, including defining functions, proving properties, and handling nested lifts.

## Core Operations

### 1) Define a function out of a quotient: `Quot.lift`

To define a map `Quot r → B`, provide:
- A function on representatives `f : A → B`
- A proof that it respects the relation `hf : ∀ a b, r a b → f a = f b`

```lean
def myFun : Quot r → B :=
  Quot.lift
    (fun x => f x)  -- function on representatives
    (fun a b h => ...) -- proof: r a b → f a = f b
```

### 2) Prove equality in a quotient: `Quot.sound`

When the goal is an equality of quotient terms, use:

```lean
-- goal: Quot.mk r a = Quot.mk r b
exact Quot.sound hab
```

`hab` must have the quotient’s underlying relation type.

### 3) Induction on quotient: `Quot.ind`

Use quotient induction to reduce to representatives:

```lean
theorem my_thm (q : Quot r) : P q := by
  induction q using Quot.ind with
  | _ x => ...  -- prove for representative
```

## Nested Quotients

For `Quot r → Quot s → C`, prefer nested `Quot.lift`:

```lean
def myFun₂ : Quot r → Quot s → C :=
  Quot.lift
    (fun a => Quot.lift
      (fun b => f a b)
      (fun b₁ b₂ h => ...))
    (fun a₁ a₂ h => funext (Quot.ind (fun b => ...)))
```

## Practical Checklist for “Respects Relation” Proofs

When `Quot.lift` fails due to the second argument:
1. Identify the quotient relation `r`.
2. Prove a lemma of the shape `r a b → f a = f b`.
3. If the lemma produces the reverse direction, wrap with symmetry.
4. Use `simp` lemmas for quotient constructors when applicable.

## Common Pitfalls (and Fixes)

- **Wrong obligation shape**: Ensure `Quot.lift` is used correctly for equality in the codomain.
- **Direction mismatch**: Use symmetry of the relation when necessary.
- **Getting stuck on function equality**: Use `funext` + `Quot.ind` on remaining quotient arguments.

## Example

```lean
noncomputable def encode : π₁(Circle, circleBase) → Int :=
  Quot.lift
    encodePath
    (fun _ _ h => encodePath_respects_rweq h)
```