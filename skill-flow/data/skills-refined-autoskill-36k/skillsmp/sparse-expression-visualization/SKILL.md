---
name: sparse-expression-visualization
description: "Visualization patterns for sparse single-cell gene expression data. Trigger: boxplots flat at zero, single-cell expression plots, sparse data visualization"
author: Claude Code
date: 2026-01-14
---

# Sparse Expression Data Visualization

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-14 |
| **Goal** | Visualize gene expression by cell type when data is sparse (many zeros) |
| **Environment** | Python, matplotlib, scRNA-seq log-normalized data |
| **Status** | Success |

## Context
Single-cell RNA-seq data is inherently sparse - most genes are not expressed in most cells. For a typical gene:
- 75%+ of cells have expression = 0
- Q1 = 0, Median = 0, Q3 = 0 (for sparse genes)
- Mean is pulled up by a few expressing cells
- Distribution is highly skewed

This causes problems with standard visualization approaches.

## The Problem: Boxplots Fail for Sparse Data

When Q1, Q3, and median are all 0:
- Box collapses to a line at y=0
- Whiskers are 0 (IQR = 0, so whisker limit = 0)
- Only outliers show variation, but hiding them leaves nothing

**Example - JAK2 expression:**
```
Cell Type      Q1    Q3    IQR   Whisker  Max
T cell         0     0     0     0        2.13
B cell         0     0     0     0        1.52
Monocyte       0     0     0     0        1.80
```

Boxplot shows 5 flat lines at y=0 with empty space above.

## Verified Solution: Bar Plots with Mean ± SEM

For sparse expression data, use bar plots showing mean ± standard error:

```python
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

cell_types_ordered = ['T cell', 'B cell', 'Monocyte/Macrophage', 'Endothelial', 'Other']
cell_type_colors = {
    'T cell': '#E41A1C', 'B cell': '#377EB8',
    'Monocyte/Macrophage': '#4DAF4A', 'Endothelial': '#984EA3', 'Other': '#999999'
}

fig, ax = plt.subplots(figsize=(8, 6))

means = []
sems = []
colors = []

for ct in cell_types_ordered:
    data = df[df['cell_type'] == ct][gene].values
    means.append(np.mean(data))
    sems.append(stats.sem(data))
    colors.append(cell_type_colors[ct])

x = np.arange(len(cell_types_ordered))
bars = ax.bar(x, means, yerr=sems, capsize=4, color=colors, alpha=0.7, edgecolor='black')

ax.set_xticks(x)
ax.set_xticklabels(cell_types_ordered, rotation=45, ha='right')
ax.set_ylabel('Mean Expression')
ax.set_ylim(bottom=0)

# Add value labels
for i, (m, s) in enumerate(zip(means, sems)):
    ax.text(i, m + s + 0.02, f'{m:.2f}', ha='center', va='bottom', fontsize=9)
```

## Alternative: Boxplots with Whisker-Based Y-Axis

If you must use boxplots, calculate y-axis based on whisker extent, not data max:

```python
# WRONG - y-axis extends to outliers (even when hidden)
ymax = np.max(all_data) * 1.1

# CORRECT - y-axis based on whisker position
whisker_tops = []
for d in box_data:
    if len(d) > 0:
        q1, q3 = np.percentile(d, [25, 75])
        iqr = q3 - q1
        whisker_top = q3 + 1.5 * iqr
        whisker_tops.append(min(whisker_top, np.max(d)))

ymax = max(whisker_tops) * 1.1 if whisker_tops and max(whisker_tops) > 0 else 1
ax.set_ylim(bottom=0, top=ymax)
```

**Warning**: For sparse data where all groups have IQR=0, this still results in flat lines. Use bar plots instead.

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Standard boxplots | Q1=Q3=median=0 for sparse genes, boxes collapse to lines | Boxplots require IQR > 0 to be meaningful |
| `showfliers=False` with `ymax=max(data)` | Y-axis extends to hidden outliers, boxes still compressed | Must calculate ymax from whisker position, not data max |
| Log-scale y-axis | Can't log(0), adds complexity | Doesn't solve the fundamental IQR=0 problem |
| Violin plots | Also collapse when most values are 0 | Same underlying problem as boxplots |
| Filtering to expressing cells only | Changes interpretation (now showing "expression given expressing") | Use for supplementary analysis, not main figure |

## When to Use Each Approach

| Data Characteristic | Recommended Visualization |
|--------------------|---------------------------|
| >50% zeros | Bar plot (mean ± SEM) |
| <25% zeros | Boxplot or violin |
| Comparing expression levels | Bar plot with error bars |
| Showing distribution shape | Violin (if <25% zeros) or histogram |
| Highlighting variability | Boxplot (if IQR > 0) |

## Additional Tips

### Color Maps for Spatial Expression
- **Bad**: `'Reds'` - low values are white/light gray, invisible on white background
- **Good**: `'YlOrRd'` (Yellow-Orange-Red) - low values are visible yellow
- For non-expressing cells: use light blue (`#a6cee3`) instead of gray

### Colorbar Range
- Set `vmin=0` for expression data (negative values are meaningless)
- Set `vmax` to 95th percentile of expressing cells to avoid outlier compression

```python
vmax = np.percentile(expr_vals[expr_vals > 0], 95) if (expr_vals > 0).any() else 1
scatter = ax.scatter(x, y, c=expr_vals, cmap='YlOrRd', vmin=0, vmax=vmax)
```

## Key Insights

1. **Mean is always informative** - even when median/IQR are 0
2. **SEM shows precision** - accounts for sample size differences between groups
3. **Bar plots are honest** - they show exactly what they claim (mean with uncertainty)
4. **Boxplots can mislead** - compressed boxes at zero suggest "no expression" when mean might be meaningful
5. **Test your visualization** - always check output before presenting

## References
- Single-cell RNA-seq data characteristics: https://www.nature.com/articles/s41576-019-0093-7
- Matplotlib boxplot documentation: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html
