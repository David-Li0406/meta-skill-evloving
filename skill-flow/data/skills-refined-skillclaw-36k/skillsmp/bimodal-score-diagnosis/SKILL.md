---
name: bimodal-score-diagnosis
description: "Diagnosing and fixing bimodal matching score distributions in MaxFuse"
author: Claude Code
date: 2026-01-23
---

# Bimodal Matching Score Diagnosis

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-23 |
| **Goal** | Understand why MaxFuse matching scores show bimodal distribution (peaks at 0.2 and 0.8) |
| **Environment** | Python 3.10, MaxFuse, 10k RNA cells, 500k protein cells |
| **Status** | Diagnosed and fixed |

## Symptom

After CCA refinement, matching scores show two distinct modes:
- **Good mode**: mean ≈ 0.2-0.3 (45% of matches)
- **Bad mode**: mean ≈ 0.8 (55% of matches)

GMM analysis confirms bimodality with clear separation at threshold ≈ 0.5.

## Diagnostic Process

### Step 1: Check Tissue Cross-Tabulation

```python
# Get tissue labels for matched cells
rna_tissues = rna_adata.obs['Tissue'].values[rna_indices[ref_rows]]
prot_tissues = protein_adata.obs['Tissue'].values[prot_indices[ref_cols]]

print(pd.crosstab(rna_tissues, prot_tissues, margins=True))
```

**Finding**: pLN RNA cells (10k) forced to match Pancreas protein (476k) due to imbalance.

### Step 2: Check Expression Levels by Mode

```python
low_mode = ref_scores < 0.5
high_mode = ref_scores >= 0.5

print(f"Low mode: mean protein expr = {prot_total_expr[low_mode].mean():.2f}")
print(f"High mode: mean protein expr = {prot_total_expr[high_mode].mean():.2f}")
```

**Finding**: Bad mode has near-zero or negative mean expression → non-immune cells.

### Step 3: Check if CCA Creates Bimodality

```python
from scipy.stats import kurtosis

init_kurtosis = kurtosis(init_scores)   # Before CCA
ref_kurtosis = kurtosis(ref_scores)     # After CCA

# Negative kurtosis = bimodal
# If ref_kurtosis << init_kurtosis, CCA increased bimodality
```

**Finding**: CCA refinement INCREASED bimodality (kurtosis went from 0.87 to -1.78).

## Root Causes Identified

| Cause | Evidence | Solution |
|-------|----------|----------|
| **Tissue imbalance** | 58% of pLN RNA matched to Pancreas protein | Increase region prior weight |
| **Non-immune cells** | Bad mode has negative protein expression | Pre-filter by immune score |
| **Marker detection issues** | MPO has spike at z=-3.0 | Filter by marker z-score threshold |

## Solutions Implemented

### 1. Increase Region Prior Weight

```python
fusor.set_region_priors(
    rna_labels=rna_tissue,
    spatial_regions=protein_tissue,
    celltype_to_region_weights=tissue_weights,
    wt_on_prior=0.7,  # Increased from 0.3
    verbose=True
)
```

### 2. Pre-filter Non-Immune Cells

```python
# Calculate immune score
immune_markers = ['CD3E', 'MS4A1', 'CD68', 'PTPRC']
marker_idx = [marker_names.index(m) for m in immune_markers]
immune_score = protein_shared[:, marker_idx].sum(axis=1)

# Use pLN 25th percentile as threshold
threshold = np.percentile(immune_score[is_pln], 25)
keep_mask = (is_pln) | (immune_score > threshold)

protein_shared = protein_shared[keep_mask]
protein_active = protein_active[keep_mask]
protein_adata = protein_adata[keep_mask].copy()
```

### 3. Marker-Specific Z-Score Filtering

```python
# Filter cells where specific markers have extreme values
MARKER_ZSCORE_THRESHOLDS = {
    'MPO': -2.5,  # Remove cells where MPO z-score < -2.5
}

for marker, threshold in MARKER_ZSCORE_THRESHOLDS.items():
    marker_idx = marker_names.index(marker)
    keep_mask &= protein_shared[:, marker_idx] >= threshold
```

## Critical: Cell Execution Order

After pre-filtering, **ALL subsequent cells must be re-run**:
1. Fusor creation
2. Batching parameters
3. Tissue priors
4. Graph construction
5. Initial pivots, refinement, etc.

Add verification to Fusor creation:
```python
if protein_shared.shape[0] > 400000:
    print("WARNING: Filter may not have run!")
```

## Failed Attempts

| Attempt | Why it Failed | Lesson |
|---------|---------------|--------|
| Only increasing region prior weight | Still had non-immune cells creating bad matches | Pre-filtering is essential |
| Excluding MPO marker entirely | Lost biological information | Use marker-specific z-score filter instead |
| Running only the filter cell | Fusor still used old unfiltered data | Must re-run all cells after filter |

## Key Insights

1. **Bimodality is diagnostic**: Two score modes usually indicate systematic data issues, not random noise.

2. **CCA amplifies, doesn't create**: If initial scores are unimodal but refined are bimodal, CCA is correctly separating matchable from unmatchable pairs.

3. **Filter BEFORE Fusor**: Pre-filtering must happen before Fusor creation. Arrays must be reduced in size.

4. **GMM threshold is useful**: The threshold between GMM modes (≈0.5) is a good cutoff for filtering bad matches if pre-filtering isn't sufficient.

5. **Check tissue cross-tabulation first**: This is the fastest diagnostic - often reveals the root cause immediately.

## References

- Integration notebook: `notebooks/2_integration.ipynb`
- Pre-filter cell: `# PRE-FILTER: Remove non-immune Pancreas protein cells`
- Diagnostic cells: After GMM analysis cell
