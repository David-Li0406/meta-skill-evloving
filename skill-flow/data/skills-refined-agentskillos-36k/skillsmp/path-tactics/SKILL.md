---
name: path-tactics
description: Use ComputationalPaths path tactics to automate common RwEq goals (path_simp/path_auto/path_normalize), and structure calc-based proofs cleanly.
---

# Path Tactics

Automated tactics for RwEq proofs.

## Import

```lean
import ComputationalPaths.Path.Rewrite.PathTactic
```

## Primary Tactics

| Tactic | Use Case |
|--------|----------|
| `path_auto` | Try first for any RwEq goal |
| `path_simp` | Unit elimination, inverse cancellation |
| `path_normalize` | Convert to right-associative form |
| `path_rfl` | Close reflexive goals `p ≈ p` |

## Structural Tactics

| Tactic | Description |
|--------|-------------|
| `path_symm` | Apply symmetry to goal |
| `path_congr_left h` | `RwEq (trans p q₁) (trans p q₂)` from `h : RwEq q₁ q₂` |
| `path_congr_right h` | `RwEq (trans p₁ q) (trans p₂ q)` from `h : RwEq p₁ p₂` |
| `path_cancel_left` | Close `RwEq (trans (symm p) p) refl` |
| `path_cancel_right` | Close `RwEq (trans p (symm p)) refl` |

## Quick Reference

| Goal | Tactic |
|------|--------|
| `RwEq (trans refl p) p` | `path_simp` |
| `RwEq (trans p refl) p` | `path_simp` |
| `RwEq (trans (symm p) p) refl` | `path_cancel_left` |
| `RwEq (symm (symm p)) p` | `path_simp` |

## Preferred Style

Use `calc` with `≈` notation:

```lean
calc p
  _ ≈ p' := rweq_cmpA_refl_left
  _ ≈ q := rweq_symm rweq_tt
```
