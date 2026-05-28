---
name: rweq-proofs
description: Helps construct RwEq (rewrite equivalence) proofs using transitivity, congruence, and canonical lemmas from the LND_EQ-TRS system. Use when proving path equalities, working with quotients, or establishing rewrite equivalences in the ComputationalPaths library.
---

# RwEq Proof Construction

Construct proofs of rewrite equivalence (`RwEq`).

## Rewrite Hierarchy

```
Step p q  -- single rewrite step
    ↓
Rw p q    -- multi-step (reflexive-transitive)
    ↓
RwEq p q  -- equivalence (symmetric-transitive)
```

## Core Lemmas

### Equivalence

```lean
rweq_refl : RwEq p p
rweq_symm : RwEq p q → RwEq q p
rweq_trans : RwEq p q → RwEq q r → RwEq p r
```

### Unit Laws

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

### Congruence

```lean
rweq_trans_congr_left : RwEq q₁ q₂ → RwEq (trans p q₁) (trans p q₂)
rweq_trans_congr_right : RwEq p₁ p₂ → RwEq (trans p₁ q) (trans p₂ q)
rweq_symm_congr : RwEq p q → RwEq (symm p) (symm q)
```

## Proof Strategies

### Calc Block (Preferred)

```lean
theorem my_proof : RwEq p q := by
  calc p
    _ ≈ p' := rweq_cmpA_refl_left
    _ ≈ q := rweq_symm rweq_tt
```

### Transitivity Chain

```lean
theorem my_proof : RwEq p q := by
  apply rweq_trans h₁
  exact h₂
```

### Congruence for Subterms

```lean
-- Goal: RwEq (trans p₁ q) (trans p₂ q)
exact rweq_trans_congr_right h  -- where h : RwEq p₁ p₂
```

## Quick Reference

| Goal | Lemma / Tactic |
|------|----------------|
| `RwEq (trans refl p) p` | `rweq_cmpA_refl_left` or `path_simp` |
| `RwEq (trans p refl) p` | `rweq_cmpA_refl_right` or `path_simp` |
| `RwEq (trans (symm p) p) refl` | `rweq_cmpA_inv_left` |
| `RwEq (symm (symm p)) p` | `rweq_ss` or `path_simp` |
| `RwEq p p` | `rweq_refl` or `path_rfl` |
