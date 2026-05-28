---
name: matplotlib
description: Use this skill when you need to create and customize a wide variety of static, animated, or interactive plots in Python, ensuring high-quality visualizations for scientific and statistical data.
---

# Skill body

## Overview

Matplotlib is Python's foundational visualization library for creating static, animated, and interactive plots. This skill provides guidance on using Matplotlib effectively, covering both the pyplot interface (MATLAB-style) and the object-oriented API (Figure/Axes), along with best practices for creating publication-quality visualizations.

## When to Use This Skill

This skill should be used when:
- Creating any type of plot or chart (line, scatter, bar, histogram, heatmap, contour, etc.)
- Generating scientific or statistical visualizations
- Customizing plot appearance (colors, styles, labels, legends)
- Creating multi-panel figures with subplots
- Exporting visualizations to various formats (PNG, PDF, SVG, etc.)
- Building interactive plots or animations
- Working with 3D visualizations
- Integrating plots into Jupyter notebooks or GUI applications

## Core Concepts

### The Matplotlib Hierarchy

Matplotlib uses a hierarchical structure of objects:

1. **Figure** - The top-level container for all plot elements
2. **Axes** - The actual plotting area where data is displayed (one Figure can contain multiple Axes)
3. **Artist** - Everything visible on the figure (lines, text, ticks, etc.)
4. **Axis** - The number line objects (x-axis, y-axis) that handle ticks and labels

### Two Interfaces

**1. Pyplot Interface (Implicit, MATLAB-style)**
```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
```
- Convenient for quick, simple plots
- Maintains state automatically
- Good for interactive work and simple scripts

**2. Object-Oriented Interface (Explicit)**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4])
ax.set_ylabel('some numbers')
plt.show()
```
- Recommended for most use cases
- More explicit control over figure and axes
- Better for complex figures with multiple subplots
- Easier to maintain and modify