---
name: rweq-proof-construction
description: Use this skill when constructing RwEq (rewrite equivalence) proofs in the ComputationalPaths library, utilizing transitivity, congruence, and canonical lemmas.
---

# RwEq Proof Construction

This skill assists with constructing proofs of rewrite equivalence (`RwEq`). RwEq is the symmetric-transitive closure of the multi-step rewrite relation (`Rw`), which itself is the reflexive-transitive closure of single-step rewrites (`Step`).

## The Rewrite Hierarchy

```
Step p q    -- Single rewrite step (one rule application)
    ↓
Rw p q      -- Multi-step rewrite (reflexive-transitive closure)
    ↓
RwEq p q    -- Rewrite equivalence (symmetric-transitive closure)
```

## Core RwEq Lemmas

### Equivalence Properties

```lean
rweq_refl : RwEq p p
rweq_symm : RwEq p q → RwEq q p
rweq_trans : RwEq p q → RwEq q r → RwEq p r
```

### Unit Laws (Composition with refl)

```lean
rweq_cmpA_refl_left : RwEq (trans refl p) p
rweq_cmpA_refl_right : RwEq (trans p refl) p
```

### Inverse Laws

```lean
rweq_cmpA_inv_left : RwEq (trans (symm p) p) refl
rweq_cmpA_inv_right : RwEq (trans p (symm p)) refl
```

### Associativity

```lean
rweq_tt : RwEq (trans (trans p q) r) (trans p (trans q r))
```

### Congruence (Composition)

```lean
rweq_trans_congr_left : RwEq q₁ q₂ → RwEq (trans p q₁) (trans p q₂)
rweq_trans_congr_right : RwEq p₁ p₂ → RwEq (trans p₁ q) (trans p₂ q)
rweq_symm_congr : RwEq p q → RwEq (symm p) (symm q)
```

## Proof Strategies

### Strategy 1: Calc Block (Preferred for Clarity)

Use `calc` with the `≈` notation for RwEq:

```lean
theorem my_proof : RwEq p q := by
  calc p
    _ ≈ p' := rweq_cmpA_refl_left
    _ ≈ q := rweq_symm rweq_tt
```

### Strategy 2: Direct Transitivity Chain

For simple proofs, chain lemmas with `rweq_trans`:

```lean
theorem my_proof : RwEq p q := by
  apply rweq_trans h₁
  exact h₂
```

### Strategy 3: Congruence for Subterms

When paths differ only in subterms:

```lean
-- Goal: RwEq (trans p₁ q) (trans p₂ q)
exact rweq_trans_congr_right h  -- where h : RwEq p₁ p₂
```

## Common Proof Patterns

### Proving decode_respects_rel

When proving that decode respects a group relation:

```lean
theorem decode_respects_rel : Rel w₁ w₂ → RwEq (wordToLoop w₁) (wordToLoop w₂) := by
  intro h
  induction h with
  | inv_left => exact rweq_cmpA_inv_left
  | inv_right => exact rweq_cmpA_inv_right
  | mul_assoc => exact rweq_tt
  | mul_id_left => exact rweq_cmpA_refl_left
  | mul_id_right => exact rweq_cmpA_refl_right
  -- etc.
```

### Normalizing Complex Paths

To simplify `trans (trans (trans refl p) refl) refl`:

```lean
theorem normalize : RwEq (trans (trans (trans refl p) refl) refl) p := by
  calc trans (trans (trans refl p) refl) refl
    _ ≈ trans (trans p refl) refl := rweq_trans_congr_right (rweq_trans_congr_right rweq_cmpA_refl_left)
    _ ≈ trans p refl := rweq_trans_congr_right rweq_cmpA_refl_right
    _ ≈ p := rweq_cmpA_refl_right
```

## Quick Reference

| Goal Shape | Tactic / Lemma |
|------------|----------------|
| `RwEq (trans refl p) p` | `rweq_cmpA_refl_left` or `path_simp` |
| `RwEq (trans p refl) p` | `rweq_cmpA_refl_right` or `path_simp` |
| `RwEq (trans (symm p) p) refl` | `rweq_cmpA_inv_left` |
| `RwEq (symm (symm p)) p` | `rweq_symm_symm` or `path_simp` |
| `RwEq p p` | `rweq_refl` or `path_rfl` |
| `RwEq (trans p q) (trans p q)` | `rweq_trans_congr_left` or `path_congr_left` |
| `RwEq (trans p (symm p)) refl` | `rweq_cmpA_inv_right` |

## Debugging RwEq Proofs

1. **Check term structure**: Use `#check` to see the actual path structure.
2. **Unfold definitions**: Ensure wordToLoop and similar are unfolded.
3. **Try both directions**: If `rweq_tt` doesn't work, try `rweq_symm rweq_tt`.
4. **Break into smaller steps**: Use intermediate `have` statements.

```lean
theorem debug_proof : RwEq p q := by
  have h1 : RwEq p p' := sorry
  have h2 : RwEq p' q := sorry
  exact rweq_trans h1 h2
```

## Path Tactics (RECOMMENDED)

**Import**: `import ComputationalPaths.Path.Rewrite.PathTactic`

The PathTactic module provides automated tactics that simplify RwEq proofs significantly.

### Primary Tactics

| Tactic | Description | Use Case |
|--------|-------------|----------|
| `path_simp` | Simplify using ~25 groupoid laws | Base cases, unit/inverse elimination |
| `path_auto` | Full automation combining simp lemmas | Most common RwEq goals |
| `path_rfl` | Close reflexive goals `p ≈ p` | Trivial equality |

### Structural Tactics

| Tactic | Description |
|--------|-------------|
| `path_symm` | Apply symmetry to goal |
| `path_normalize` | Rewrite to canonical (right-assoc) form |
| `path_beta` | Apply beta reductions for products/sigmas |
| `path_eta` | Apply eta expansion/contraction |
| `path_congr_left h` | Apply `RwEq (trans p q₁) (trans p q₂)` from `h : RwEq q₁ q₂` |
| `path_congr_right h` | Apply `RwEq (trans p₁ q) (trans p₂ q)` from `h : RwEq p₁ p₂` |
| `path_cancel_left` | Close `RwEq (trans (symm p) p) refl` |
| `path_cancel_right` | Close `RwEq (trans p (symm p)) refl` |