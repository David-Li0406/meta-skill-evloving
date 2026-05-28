---
name: rweq-proofs
description: Use this skill when constructing RwEq (rewrite equivalence) proofs in the ComputationalPaths library, particularly for proving path equalities and establishing rewrite equivalences.
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

### Preferred: Calc Block

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
| `RwEq (symm (symm p)) p` | `rweq_symm_symm` or `path_simp` |
| `RwEq p p` | `rweq_refl` or `path_rfl` |