---
name: seaborn
description: Use this skill for creating publication-quality statistical graphics with minimal code, ideal for exploring distributions, relationships, and categorical comparisons.
---

# Seaborn Statistical Visualization

## Overview

Seaborn is a Python visualization library built on top of Matplotlib, designed for creating attractive and informative statistical graphics. It is particularly useful for dataset-oriented plotting, multivariate analysis, automatic statistical estimation, and complex multi-panel figures.

## Design Philosophy

Seaborn follows these core principles:

1. **Dataset-oriented**: Work directly with DataFrames and named variables rather than abstract coordinates.
2. **Semantic mapping**: Automatically translate data values into visual properties (colors, sizes, styles).
3. **Statistical awareness**: Built-in aggregation, error estimation, and confidence intervals.
4. **Aesthetic defaults**: Publication-ready themes and color palettes out of the box.
5. **Matplotlib integration**: Full compatibility with Matplotlib customization when needed.

## Quick Start

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load example dataset
df = sns.load_dataset('tips')

# Create a simple visualization
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()
```

## Core Plotting Interfaces

### Function Interface (Traditional)

The function interface provides specialized plotting functions organized by visualization type. Each category has **axes-level** functions (plot to single axes) and **figure-level** functions (manage entire figure with faceting).

**When to use:**
- Quick exploratory analysis
- Single-purpose visualizations
- When you need a specific plot type

### Objects Interface (Modern)

The `seaborn.objects` interface provides a declarative, composable API similar to ggplot2. Build visualizations by chaining methods to specify data mappings, marks, transformations, and scales.

**When to use:**
- Complex layered visualizations
- When you need fine-grained control over transformations
- Building custom plot types
- Programmatic plot generation

```python
from seaborn import objects as so

# Declarative syntax
(
    so.Plot(data=df, x='total_bill', y='tip')
    .add(so.Dot(), color='blue')
)
```