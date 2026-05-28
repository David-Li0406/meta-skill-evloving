---
name: path-tactics
description: Use this skill to automate common RwEq goals and structure calc-based proofs cleanly with ComputationalPaths path tactics.
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
| `path_auto` | Use for standalone goals involving groupoid laws, cancellation, and associativity. |
| `path_simp` | Use as a cleanup step in longer proofs to close trivial cancellations. |
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

## Proof Structuring Patterns

### Prefer `calc` Chains for Readability

This project commonly uses a `calc` chain with the `≈` notation for RwEq:

```lean
theorem my_rweq : RwEq p q := by
  calc p
    _ ≈ p' := h1
    _ ≈ p'' := h2
    _ ≈ q := by
      path_simp
```

### Combining Tactics with Targeted Lemmas

1. Apply key lemma(s) with `apply` / `exact`.
2. Finish with `path_simp` or `path_auto`.

## Troubleshooting

- If `path_auto` fails, normalize both sides with `path_normalize` and retry.
- If the goal is almost solved but has extra `trans refl _` or `trans _ refl`, use `path_simp`.
- For congruence-heavy goals, apply project lemmas (e.g., `rweq_trans_congr_left/right`) to reduce the goal, then finish with tactics.