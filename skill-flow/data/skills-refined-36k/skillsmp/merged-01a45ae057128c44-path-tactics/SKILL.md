---
name: path-tactics
description: Use ComputationalPaths path tactics to automate common RwEq goals and structure calc-based proofs cleanly.
---

# Path Tactics

Automated tactics for RwEq proofs that reduce boilerplate and enhance readability.

## Import

```lean
import ComputationalPaths.Path.Rewrite.PathTactic
```

## Primary Tactics

| Tactic | Use Case |
|--------|----------|
| `path_auto` | Use for standalone goals involving groupoid laws, cancellation, and associativity. |
| `path_simp` | Use for cleanup steps in longer proofs (unit laws, trivial cancellations). |
| `path_normalize` | Use when the goal is blocked by different parenthesizations. |
| `path_rfl` | Close reflexive goals `p ≈ p`. |

## Structural Tactics

| Tactic | Description |
|--------|-------------|
| `path_symm` | Apply symmetry to the goal. |
| `path_congr_left h` | Derive `RwEq (trans p q₁) (trans p q₂)` from `h : RwEq q₁ q₂`. |
| `path_congr_right h` | Derive `RwEq (trans p₁ q) (trans p₂ q)` from `h : RwEq p₁ p₂`. |
| `path_cancel_left` | Close `RwEq (trans (symm p) p) refl`. |
| `path_cancel_right` | Close `RwEq (trans p (symm p)) refl`. |

## Quick Reference

| Goal | Tactic |
|------|--------|
| `RwEq (trans refl p) p` | `path_simp` |
| `RwEq (trans p refl) p` | `path_simp` |
| `RwEq (trans (symm p) p) refl` | `path_cancel_left` |
| `RwEq (symm (symm p)) p` | `path_simp` |

## Preferred Style

Use `calc` chains for readability with `≈` notation:

```lean
calc p
  _ ≈ p' := rweq_cmpA_refl_left
  _ ≈ q := rweq_symm rweq_tt
```

## Proof Structuring Patterns

1. **Combine Tactics**: Apply key lemmas with `apply` or `exact`, then finish with `path_simp` or `path_auto`.
2. **Troubleshooting**:
   - If `path_auto` fails, normalize both sides with `path_normalize` and retry.
   - If the goal is nearly solved but has extra `trans refl _` or `trans _ refl`, use `path_simp`.
   - For congruence-heavy goals, apply project lemmas (e.g., `rweq_trans_congr_left/right`) to simplify the goal, then finish with tactics.