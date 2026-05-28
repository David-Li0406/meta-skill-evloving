---
name: research-figure
description: Create or revise publication-ready research figures for AI or ML papers using Matplotlib, Seaborn, or Plotly. Use when asked to draw plots from a requirements doc, simulate realistic experimental data, or improve aesthetics and readability (bar charts, line trends, ablation studies, comparisons).
---

# Research Figure

## Overview
Create clear, publication-grade figures that match a written claim and look like real experimental results.

## Workflow
1. Read the requirements and locate any cited files or target output paths.
2. Choose the plotting stack (default to Matplotlib; use Seaborn for statistical framing; use Plotly for interactive output).
3. Design data values to support the stated claim while staying realistic.
4. Apply paper-quality styling and layout.
5. Generate outputs in both PNG and PDF when possible.
6. Verify against the quality checklist and iterate on feedback.

## Data Design
- Preserve the narrative: encode the intended conclusion in the relative ordering and trend shapes.
- Add realistic variation: use mild non-linearities, local fluctuations, and small noise so curves are not identical.
- Keep bounds plausible: avoid hard 0/1 extremes unless explicitly expected.
- Keep method separation plausible: avoid perfectly parallel curves or constant gaps.

Use `references/realism-patterns.md` for concrete patterns and snippets.

## Visual Style
- Use paper-friendly typography and color palettes.
- Emphasize the method of interest with stronger contrast, but keep others legible.
- Keep grids light and unobtrusive.
- Avoid cluttered legends; place them outside or in empty corners.

Use `references/style-guidelines.md` for palettes, fonts, and layout defaults.

## Output
- Save `png` (dpi=300) and `pdf` (vector) unless the user requests otherwise.
- Use `bbox_inches="tight"` and `tight_layout()` to avoid cropped labels.
- Place files at the user-specified output location.

## Iteration
- When asked to "optimize" or "fix" a figure, identify whether the issue is data realism, visual style, or narrative clarity.
- Adjust data first if the trend is not convincing; adjust style if the chart is hard to read.
- Re-run and re-export after each change.

Use `references/qa-checklist.md` before final delivery.
