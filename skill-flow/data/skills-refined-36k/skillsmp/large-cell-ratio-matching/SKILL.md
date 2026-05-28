---
name: large-cell-ratio-matching
description: "MaxFuse parameter tuning for datasets with large protein:RNA cell ratios (>100:1)"
author: smith6jt
date: 2025-01-21
---

# Large Cell Ratio Matching - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-21 |
| **Goal** | Fix MaxFuse integration losing ~23% of RNA cells due to excessive filtering in pancreas/lymph node dataset |
| **Environment** | Python 3.10, MaxFuse local package, 1,284 RNA cells, 1.74M protein cells (59 markers) |
| **Status** | Success |

## Context

When integrating datasets with very large protein:RNA cell ratios (>1000:1), the default MaxFuse batching formula causes problems:

- **Dataset**: Pancreas + lymph node, 59-marker PhenoCycler
- **RNA cells**: 1,284
- **Protein cells**: 1,740,774
- **Ratio**: 1,355:1

The original `matching_ratio` formula (`max(10, int(ratio) + 5)`) yielded 1,360, causing:
1. Over-sampling of protein cells in batches
2. Excessive pivot filtering (fixed 20%) removing good matches
3. Additional propagation filtering (10%) compounding losses
4. Final RNA coverage: only 77.3% (291 cells unmatched)

## The Problem: Cascading Filter Losses

```
Initial pivots: N matches
  ↓ pivot_filter_prop=0.2 → 80% remain
  ↓ propagate_filter_prop=0.1 → 72% remain
  ↓ score_threshold=0.0 → ~70% remain
Final: ~77% RNA coverage
```

With `matching_ratio=1360`, the algorithm over-samples protein cells, creating noisy matches that then get filtered away—taking good matches with them.

## Verified Workflow

### Fix 1: Sqrt-Scaled Matching Ratio

```python
# OLD (problematic for large ratios)
matching_ratio = max(10, int(ratio) + 5)  # = 1360 for ratio=1355

# NEW (sqrt scaling with cap)
matching_ratio = min(100, max(10, int(np.sqrt(ratio)) + 5))
# For ratio=1355: min(100, sqrt(1355)+5) ≈ 42
```

**Why sqrt scaling?** MaxFuse uses pivot propagation—it doesn't need every protein cell in the initial batch. The pivots establish correspondences that propagate to the full dataset. Sqrt scaling provides sufficient coverage without over-sampling.

### Fix 2: GMM-Guided Pivot Filtering

```python
# OLD (fixed proportion)
pivot_filter_prop = 0.2  # Always remove 20%

# NEW (adaptive to score distribution)
# Requires GMM analysis cell to run first, which computes bad_mode_fraction
pivot_filter_prop = min(0.2, bad_mode_fraction + 0.02)
```

The GMM analysis fits a 2-component Gaussian mixture to pivot scores, identifying:
- **Good mode**: High-quality matches (lower scores for distance-based)
- **Bad mode**: Poor matches

Filter proportion adapts to actual data instead of assuming 20% are bad.

### Fix 3: Conservative Propagation Filtering

```python
# OLD
propagate_filter_prop = 0.1  # Remove bottom 10%

# NEW
propagate_filter_prop = 0.05  # Remove bottom 5%
```

Since pivot filtering already removed poor seeds, propagation filtering can be gentler.

## Parameter Summary

| Parameter | Before | After | Scaling Rule |
|-----------|--------|-------|--------------|
| `matching_ratio` | 1360 | 42 | `min(100, sqrt(ratio) + 5)` |
| `pivot_filter_prop` | 0.20 | GMM-guided | `min(0.2, bad_mode_fraction + 0.02)` |
| `propagate_filter_prop` | 0.10 | 0.05 | Fixed reduction |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| `matching_ratio = ratio + 5` | Created 1360x over-sampling, noisy matches filtered away | Use sqrt scaling for ratios >100 |
| Fixed 20% pivot filter | Removed good matches when bad mode was <20% | Use GMM to detect actual bad match fraction |
| 10% propagation filter after 20% pivot filter | Cumulative 28% loss too aggressive | Reduce propagation filter when pivots already filtered |
| Linear ratio scaling | Doesn't account for pivot propagation mechanism | Algorithm propagates from pivots; doesn't need all cells in batch |

## Key Insights

1. **Sqrt scaling for large ratios**: When protein:RNA ratio exceeds ~100:1, use `sqrt(ratio)` not `ratio` for `matching_ratio`. The propagation mechanism means initial batches don't need comprehensive protein coverage.

2. **GMM-guided filtering is superior**: The score distribution is often bimodal. Let the data tell you what fraction is "bad" instead of assuming 20%.

3. **Filter proportions compound**: 20% pivot + 10% propagate + score threshold ≈ 30% loss. Plan cumulative filtering budget.

4. **Cap matching_ratio at 100**: Even with sqrt scaling, cap at 100 to prevent memory issues and ensure representative sampling.

5. **Check coverage early**: If RNA coverage drops below 90% after integration, suspect over-filtering from inflated matching_ratio.

## Diagnostic Checks

```python
# Before integration: Check if ratio needs sqrt scaling
ratio = n_prot / n_rna
if ratio > 100:
    print(f"WARNING: Large ratio ({ratio:.0f}:1) - use sqrt scaling!")
    matching_ratio = min(100, int(np.sqrt(ratio)) + 5)
else:
    matching_ratio = max(10, int(ratio) + 5)

# After GMM analysis: Verify bad mode fraction
print(f"Bad mode fraction: {bad_mode_fraction:.2%}")
if bad_mode_fraction < 0.15:
    print("Consider pivot_filter_prop < 0.2")

# After integration: Check coverage
rna_coverage = len(np.unique(full_matching[0])) / n_rna * 100
if rna_coverage < 90:
    print(f"WARNING: Low RNA coverage ({rna_coverage:.1f}%)")
    print("Consider reducing filter proportions or matching_ratio")
```

## Applicability

This skill applies when:
- Protein:RNA cell ratio > 100:1
- Using MaxFuse for cross-modal integration
- Observing >10% RNA cell loss after integration
- GMM analysis shows bad mode fraction < 20%

Datasets tested:
- Pancreas + lymph node (1.7M protein, 1.3k RNA, 59 markers)
- Expected to apply to any PhenoCycler/CODEX with large FOV

## References

- MaxFuse paper: Cross-modal matching with pivot propagation
- Integration notebook: `notebooks/2_integration.ipynb`
- Related skills: `parameter-scaling`, `cross-modal-normalization`
