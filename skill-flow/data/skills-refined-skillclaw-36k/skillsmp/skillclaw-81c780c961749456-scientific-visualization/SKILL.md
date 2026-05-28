---
name: scientific-visualization
description: Use this skill when creating publication-ready figures for scientific manuscripts, ensuring compliance with journal formatting and accessibility standards.
---

# Scientific Visualization

## Overview

Scientific visualization transforms data into clear, accurate figures for publication. Create journal-ready plots with multi-panel layouts, error bars, significance markers, and colorblind-safe palettes. Export as PDF/EPS/TIFF using matplotlib, seaborn, and plotly for manuscripts.

## When to Use This Skill

This skill should be used when:
- Creating plots or visualizations for scientific manuscripts
- Preparing figures for journal submission (Nature, Science, Cell, PLOS, etc.)
- Ensuring figures are colorblind-friendly and accessible
- Making multi-panel figures with consistent styling
- Exporting figures at correct resolution and format
- Following specific publication guidelines
- Improving existing figures to meet publication standards
- Creating figures that need to work in both color and grayscale

## Quick Start Guide

### Basic Publication-Quality Figure

```python
import matplotlib.pyplot as plt
import numpy as np

# Apply publication style
from style_presets import apply_publication_style
apply_publication_style('default')

# Create figure with appropriate size (single column = 3.5 inches)
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Plot data
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Proper labeling with units
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude (mV)')
ax.legend(frameon=False)

# Remove unnecessary spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save in publication formats
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

### Using Pre-configured Styles

Apply journal-specific styles using the matplotlib style files:

```python
import matplotlib.pyplot as plt

# Option 1: Use style file directly
plt.style.use('assets/nature.mplstyle')

# Option 2: Use style_presets.py for custom styles
```