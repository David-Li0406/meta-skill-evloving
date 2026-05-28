---
name: qc-plot-pdf-export
description: "KINTSUGI quantification plots: Always save QC heatmaps and profiles as PDF"
author: Claude Code
date: 2026-01-15
triggers:
  - quantification
  - QC plots
  - heatmaps
  - summary plots
  - PDF export
  - plot_summary_heatmaps
  - plot_zplane_profiles
---

# QC Plot PDF Export Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-15 |
| **Goal** | Ensure all quantification plots are saved as PDFs for documentation |
| **Environment** | KINTSUGI notebooks/2_Cycle_Processing.ipynb |
| **Status** | Implemented |

## Context
Quantification cells in the cycle processing notebook generate heatmaps and profile plots showing:
- SNR (Signal-to-Noise Ratio) by cycle/channel
- CV (Coefficient of Variation) for uniformity assessment
- Mean intensity distributions
- Z-plane profiles

These plots should be saved as PDFs to `PROJECT_DIR/qc_plots/` for archival and reporting.

## Implementation Pattern

### QC Output Directory Setup
```python
# QC output directory for PDF plots
QC_OUTPUT_DIR = PROJECT_DIR / 'qc_plots'
QC_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

### Summary Heatmap Function
```python
def plot_summary_heatmaps(stats_df, stage_name="raw", save_pdf=True):
    """Create summary heatmaps: SNR and CV by cycle/channel.

    Args:
        stats_df: DataFrame with statistics
        stage_name: Name for the processing stage (used in PDF filename)
        save_pdf: Whether to save the plot as PDF (default: True)
    """
    # ... create figure with 3 subplots ...

    plt.suptitle(f'{stage_name.upper()} Summary Heatmaps', y=1.02, fontsize=14)
    plt.tight_layout()

    if save_pdf:
        pdf_path = QC_OUTPUT_DIR / f'{stage_name}_summary_heatmaps.pdf'
        fig.savefig(pdf_path, format='pdf', bbox_inches='tight', dpi=150)
        print(f"  Saved: {pdf_path}")

    plt.show()
    return fig
```

### Z-Plane Profile Function
```python
def plot_zplane_profiles(stats_df, cycle, channel, stage_name="raw", save_pdf=True):
    """Plot statistics across all z-planes for one cycle/channel.

    Args:
        stats_df: DataFrame with statistics
        cycle: Cycle number
        channel: Channel number
        stage_name: Name for the processing stage (used in PDF filename)
        save_pdf: Whether to save the plot as PDF (default: True)
    """
    # ... create figure with 4 subplots ...

    plt.tight_layout()

    if save_pdf:
        pdf_path = QC_OUTPUT_DIR / f'{stage_name}_zprofile_cyc{cycle:02d}_ch{channel}.pdf'
        fig.savefig(pdf_path, format='pdf', bbox_inches='tight', dpi=150)

    plt.show()
    return fig
```

### Usage in Quantification Cells
```python
# Summary heatmaps (always save)
plot_summary_heatmaps(raw_stats_df, stage_name="raw")
plot_summary_heatmaps(stitched_stats_df, stage_name="stitched")
plot_summary_heatmaps(decon_stats_df, stage_name="deconvolved")

# Z-plane profiles (save first cycle only to avoid too many files)
for cycle in range(start_cycle, end_cycle + 1):
    for channel in range(start_channel, end_channel + 1):
        save_pdf = (cycle == start_cycle)  # Only first cycle
        plot_zplane_profiles(stats_df, cycle, channel, stage_name="raw", save_pdf=save_pdf)
```

## Output Files

| File Pattern | Description |
|--------------|-------------|
| `{stage}_summary_heatmaps.pdf` | 3-panel heatmap (SNR, CV, Intensity) |
| `{stage}_zprofile_cyc{NN}_ch{N}.pdf` | 4-panel z-profile (Intensity, SNR, CV, StdDev) |

Where `{stage}` is one of: `raw`, `stitched`, `deconvolved`, `edf`

## Key Insights
- Always include `stage_name` parameter to differentiate processing stages
- Use `bbox_inches='tight'` to prevent label clipping
- DPI of 150 provides good balance of quality and file size
- Return the figure object for programmatic use if needed
- Limit z-profile PDFs to first cycle to avoid excessive file count

## Related Skills
- `gpu-parallel-scheduling` - Statistics collection uses GPU parallelism
- `notebook-module-refactoring` - Function extraction pattern
- `repo-project-sync-workflow` - Edit main repo first

## References
- KINTSUGI `notebooks/2_Cycle_Processing.ipynb` - Quantification cells
- KINTSUGI `docs/workflows.md` - Workflow 2 documentation
