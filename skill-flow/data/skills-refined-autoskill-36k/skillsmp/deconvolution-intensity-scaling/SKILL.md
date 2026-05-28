---
name: deconvolution-intensity-scaling
description: "KINTSUGI deconvolution: Output scaling must preserve original intensity relationships for quantitative analysis. Trigger: deconvolution saturates at 65535, channel intensity ratios inverted, hist_clip scaling issues."
author: KINTSUGI Team
date: 2026-01-15
---

# Deconvolution Intensity Scaling - Preserving Quantitative Relationships

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-15 |
| **Goal** | Fix pixel range scaling errors that break quantitative marker analysis |
| **Environment** | KINTSUGI KDecon module, HiPerGator, CuPy GPU |
| **Status** | RESOLVED |

## Context

After deconvolution, all channels were saturating at 65535 (max uint16) regardless of their original intensity ranges. This caused:
- Artificial clipping of bright regions
- Inverted relative intensity relationships between channels
- Broken quantitative marker expression analysis

## Root Cause

The histogram clipping and rescaling logic in `notebooks/Kdecon/main.py` (lines 265-289) always stretched output to full 16-bit range:

```python
# BROKEN CODE (before fix)
if raw_max <= 65535:
    scale = 65535  # <-- Always stretched to full range!
else:
    scale = raw_max
result = result * scale
```

### Impact Analysis

| Channel | Stage | Mean | Max | Problem |
|---------|-------|------|-----|---------|
| CH2 (weak) | Stitched | 280 | 41,620 | - |
| CH2 (weak) | Deconvolved | 11,109 | 65,535 | **39.7x mean inflation!** |
| CH1 (DAPI) | Stitched | 3,998 | 58,214 | - |
| CH1 (DAPI) | Deconvolved | 7,927 | 65,535 | 1.98x mean inflation |

**Critical:** The CH1/CH2 intensity ratio was **inverted** from 14.28 to 0.71.

## Solution

Change the scaling to preserve original intensity relationships:

```python
# FIXED CODE
# Scale to output range - preserve original intensity scale
# Using raw_max maintains relative intensity relationships between channels,
# which is critical for quantitative analysis of marker expression
scale = raw_max

result = result * scale
```

### Fixed Results

| Metric | Broken | Fixed |
|--------|--------|-------|
| CH2 max | 65,535 (saturated) | 41,620 (preserved) |
| CH1 max | 65,535 (saturated) | 58,214 (preserved) |
| CH1/CH2 ratio | 0.71 (inverted!) | 1.00 (consistent) |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Assuming 65535 scaling was intentional | Destroyed quantitative relationships | Always check if scaling preserves relative intensities |
| Only checking max values | Missed the mean inflation and ratio inversion | Check both absolute AND relative intensity metrics |
| Ignoring hist_clip parameter | It normalizes to 0-1 then rescales | Understand the full pipeline before diagnosing |
| Looking only at single channel | Issue only visible when comparing channels | Multi-channel analysis reveals scaling bugs |

## Diagnostic Checklist

When deconvolved images show intensity issues:

1. **Check for saturation**: `np.sum(img >= 65535)` should be near zero
2. **Compare channel ratios**: Before/after deconvolution should be similar
3. **Check mean inflation**: Deconvolved mean shouldn't be dramatically higher than input
4. **Trace the scaling pipeline**: Input → deconv → clip → normalize → scale → output

## Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `hist_clip` | 0.01 | Histogram clipping percentage (clips 0.01% at each end) |
| `raw_max` | varies | Maximum value from input image (used for output scaling) |

## Key Insights

- **Histogram clipping normalizes to 0-1**: The `hist_clip` parameter clips percentiles, then normalizes the result to 0-1 range. The final scaling determines the output range.
- **Weak channels are most affected**: Channels with low mean intensity show the largest inflation when stretched to full range.
- **Relative relationships matter for quantitative analysis**: Marker expression comparisons require consistent scaling across channels.
- **Test with multiple channels**: Single-channel testing won't reveal ratio inversion bugs.

## Files Modified

- `notebooks/Kdecon/main.py`: Lines 283-288 (scaling logic)
- `CLAUDE.md`: Added documentation in Recent Enhancements section

## References

- `notebooks/Kdecon/main.py`: KDecon class and `decon()` function
- `notebooks/2_Cycle_Processing.ipynb`: Deconvolution workflow
- Related skill: `lightsheet-psf-deconvolution` (PSF-related deconvolution issues)
