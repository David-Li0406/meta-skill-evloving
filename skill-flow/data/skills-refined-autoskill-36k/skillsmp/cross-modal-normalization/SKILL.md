---
name: cross-modal-normalization
description: "Scale alignment for RNA-protein cross-modal integration - BOTH modalities must be z-scored"
author: Claude Code
date: 2025-01-20
---

# Cross-Modal Normalization - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-20 |
| **Goal** | Fix matching quality issues caused by scale mismatch between RNA and protein |
| **Environment** | Python 3.10, scanpy 1.9+, sklearn |
| **Status** | Success |

## Context

MaxFuse matching quality was poor with cells matching across clusters and "B-cell outliers" that weren't actually B cells. Investigation revealed a **16x variance mismatch** between modalities:

- **RNA**: normalize_total → log1p → z-score → mean≈0, std≈0.8, range [-1.5, 5]
- **Protein**: Used as-is ("pre-scaled") → mean≈0.4, std≈0.08, range [0, 1]

The matching algorithm over-weighted RNA features because they had 16x higher variance.

## The Problem: Scale Mismatch

```
RNA variance:     ~0.64 (std² = 0.8²)
Protein variance: ~0.006 (std² = 0.08²)
Ratio:           ~100x (RNA dominates matching)
```

When computing distances for matching, features with higher variance dominate. If RNA has 100x the variance of protein, the matching effectively ignores protein information.

## Verified Workflow

### Correct Normalization (BOTH z-scored)

```python
from sklearn.preprocessing import StandardScaler
from scipy import sparse

# ============================================================
# RNA NORMALIZATION (standard pipeline)
# ============================================================
sc.pp.normalize_total(rna_shared_adata, target_sum=1e4)
sc.pp.log1p(rna_shared_adata)
sc.pp.scale(rna_shared_adata, zero_center=True, max_value=5)
rna_shared_normalized = rna_shared_adata.X.copy()
if sparse.issparse(rna_shared_normalized):
    rna_shared_normalized = rna_shared_normalized.toarray()

# ============================================================
# PROTEIN NORMALIZATION - MUST Z-SCORE TO MATCH RNA
# ============================================================
protein_shared_raw = protein_shared_adata.X.copy()
if sparse.issparse(protein_shared_raw):
    protein_shared_raw = protein_shared_raw.toarray()

# Z-score protein to match RNA scale
scaler = StandardScaler()
protein_shared_normalized = scaler.fit_transform(protein_shared_raw)
protein_shared_normalized = np.clip(protein_shared_normalized, -5, 5)

# ============================================================
# VERIFICATION - CRITICAL
# ============================================================
print("RNA:")
print(f"  Mean: {rna_shared_normalized.mean():.4f}")
print(f"  Std:  {rna_shared_normalized.std():.4f}")
print(f"  Range: [{rna_shared_normalized.min():.2f}, {rna_shared_normalized.max():.2f}]")

print("Protein:")
print(f"  Mean: {protein_shared_normalized.mean():.4f}")
print(f"  Std:  {protein_shared_normalized.std():.4f}")
print(f"  Range: [{protein_shared_normalized.min():.2f}, {protein_shared_normalized.max():.2f}]")

# EXPECTED OUTPUT:
# RNA:     Mean: ~0, Std: ~0.8-1.0, Range: [-1.5, 5.0]
# Protein: Mean: ~0, Std: ~0.8-1.0, Range: [-5.0, 5.0]
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Protein "pre-scaled" used as-is | 16x variance mismatch → RNA dominated matching | ALWAYS z-score both modalities |
| Assuming gated data is normalized | Gating ≠ normalization, still needs z-score | Check actual statistics, don't assume |
| Only checking mean (not std) | Mean≈0 but std was 0.08 vs 0.8 | Always check BOTH mean AND std |

## Key Insights

1. **Both modalities MUST have similar scales**: mean≈0, std≈1, range ~[-5, 5]

2. **"Pre-scaled" or "normalized" doesn't mean z-scored**: Always verify with actual statistics

3. **Check the VERIFICATION output**: The normalization cell should print statistics for both modalities. If they don't match, the integration will fail.

4. **Symptoms of scale mismatch**:
   - Cells matching across different UMAP clusters
   - "Outliers" that don't match expected cell types
   - Very high canonical correlations (overfitting to dominant modality)
   - Poor downstream validation metrics

5. **Clip both to same range**: Using `np.clip(..., -5, 5)` ensures neither modality has extreme outliers that dominate matching.

## Diagnostic Checks

### Before Integration
```python
# Both should be similar
for name, data in [("RNA", rna_shared), ("Protein", protein_shared)]:
    print(f"{name}: mean={data.mean():.3f}, std={data.std():.3f}")

# WARNING signs:
# - std differs by >2x between modalities
# - mean is far from 0 for either modality
# - range is very different (e.g., [0,1] vs [-5,5])
```

### After Integration
```python
# Check if matched pairs make biological sense
# - Same cell type markers should be correlated
# - Cells should match within clusters, not across
# - Permutation test should show significance (p < 0.01)
```

## References

- Integration notebook: `notebooks/2_integration.ipynb`, cell starting with "# Normalize shared features"
- MaxFuse matching uses correlation distance, which is scale-sensitive
- sklearn StandardScaler: per-feature z-scoring
