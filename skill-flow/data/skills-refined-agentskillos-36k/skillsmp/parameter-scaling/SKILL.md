---
name: parameter-scaling
description: "MaxFuse parameter tuning when protein panel size changes (26 → 59+ markers)"
author: Claude Code
date: 2025-01-20
---

# MaxFuse Parameter Scaling - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-20 |
| **Goal** | Adapt MaxFuse parameters for 59-marker PhenoCycler dataset (originally tuned for 26-marker CODEX) |
| **Environment** | Python 3.10, MaxFuse local package, scanpy 1.9+ |
| **Status** | Success |

## Context

MaxFuse was originally configured for a 26-marker CODEX dataset with ~1,284 RNA cells and ~1.7M protein cells. When migrating to a 59-marker PhenoCycler dataset, the default parameters caused CCA overfitting because:

1. **More protein features** (59 vs 26) means more dimensions for CCA to fit
2. **Same number of RNA cells** (~1,284) means higher risk of fitting noise
3. **CCA with too many components** finds trivially perfect correlations by fitting noise

## Critical Issue: CCA Overfitting

The most dangerous parameter is `cca_components`. With 25 CCA components and 59 protein features, CCA can find nearly perfect correlations that don't reflect real biological signal.

**Rule of thumb**: `cca_components = min(n_shared - 1, sqrt(n_prot_active) + 1, hard_cap)`

For 59 markers with 26 shared features:
- `n_prot_active = 59 - 26 = 33`
- `sqrt(33) + 1 ≈ 7`
- Use **7 CCA components**, not 25

## Verified Parameters

### Parameter Scaling Table

| Parameter | 26 Markers | 59 Markers | 19 Markers | Scaling Rule |
|-----------|-----------|-----------|------------|--------------|
| CCA Components | 25 | 7 | **10** | `min(n_shared - 1, 10)` for small panels |
| SVD for CCA (RNA) | 40 | 50 | 50 | RNA has many features |
| SVD for CCA (Protein) | None | 35 | **15** | `min(15, n_prot - 1)` |
| SVD for Graphs (Protein) | 15 | 30 | **15** | `min(15, n_prot - 1)` |
| SVD for Initial Pivots | 25/20 | 20/18 | **15/15** | `min(15, n_shared - 1)` |
| Metacell Size | 2 | 2 | **1** | Disable for <25 features |

**Critical rule**: All SVD components MUST be < n_features - 1.

### Small Panel (<25 markers) Considerations

When protein_active == protein_shared (all markers are shared):
- The sqrt rule for CCA components breaks (`n_prot_active = 0`)
- Use simpler rule: `cca_components = min(n_shared - 1, 10)`
- Metacell size of 2 provides minimal benefit - use `metacell_size=1` (disabled)

### Implementation Code

```python
# In notebook 2_integration.ipynb

# 1. Graph construction SVD
svd_comp1_graph = min(50, n_rna_features - 1)   # RNA: increased from 40
svd_comp2_graph = min(30, n_prot_features - 1)  # Protein: increased from 15

# 2. Initial pivots (shared features only - be conservative)
svd_shared1 = min(20, n_shared - 1)  # Reduced from 25
svd_shared2 = min(18, n_shared - 1)  # Reduced from 20

# 3. CCA components - CRITICAL
n_prot_active = n_prot_features - n_shared
cca_components = min(
    n_shared - 1,                     # Can't exceed shared features
    int(np.sqrt(n_prot_active)) + 1,  # sqrt rule for overfitting prevention
    12                                # Hard cap
)
cca_components = max(5, cca_components)  # At least 5

# 4. SVD before CCA
svd_cca_rna = min(50, n_rna_features - 1)
svd_cca_prot = min(35, n_prot_features - 1)  # NEW: was None (keep all)

# 5. Propagate - match CCA settings
fusor.propagate(
    svd_components1=min(50, n_rna_features - 1),
    svd_components2=min(35, n_prot_features - 1),
    wt1=0.7, wt2=0.7
)
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using 25 CCA components with 59 markers | CCA found perfect correlations by fitting noise | Always use sqrt rule for CCA components |
| Keeping SVD=None for protein before CCA | Too many dimensions caused unstable CCA | Limit protein SVD to ~60% of features |
| Same initial pivot SVD (25/20) | Overfitting on shared features in weak linkage | Reduce SVD for initial matching |

## Key Insights

1. **CCA components scale with sqrt, not linearly**: Doubling protein features does NOT mean doubling CCA components. Use `sqrt(n_active) + 1`.

2. **Protein SVD limits are essential**: With more protein features, you MUST limit SVD before CCA to prevent overfitting. ~60% of features is a good target.

3. **Graph SVD can be more generous**: Graph construction is robust to dimensionality. Scale roughly with feature count.

4. **Initial pivots need conservatism**: The first matching uses only shared features (~26). Use fewer SVD components to avoid fitting noise.

5. **Check canonical correlations**: If the first few canonical correlations are all >0.95, you're overfitting. Reduce CCA components until you see meaningful decay.

## Diagnostic Checks

After running with new parameters:

```python
# Check 1: Canonical correlations should decay smoothly
# Good: [0.92, 0.85, 0.78, 0.65, 0.52, ...]
# Bad:  [0.99, 0.98, 0.97, 0.96, ...] (overfitting)

# Check 2: Distribution alignment
print(f"RNA: mean={rna.mean():.3f}, std={rna.std():.3f}")
print(f"Prot: mean={prot.mean():.3f}, std={prot.std():.3f}")
# Both should have similar scales (mean≈0, std≈1)

# Check 3: Matching quality
# Score distribution should be centered, not all near 1.0
```

## References

- MaxFuse paper: Cross-modal data integration methods
- CCA overfitting: Rule of thumb is n_components < sqrt(min(n1, n2))
- Integration notebook: `notebooks/2_integration.ipynb`
