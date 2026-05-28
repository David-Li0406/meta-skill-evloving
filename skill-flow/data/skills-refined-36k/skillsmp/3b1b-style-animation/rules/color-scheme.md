---
name: color-scheme
description: 3Blue1Brown color palette and styling guidelines
metadata:
  tags: manim, colors, style, 3b1b
---

# 3Blue1Brown Color Scheme

## Official 3b1b Color Palette

```python
from manim import *

# Background
BACKGROUND_COLOR = "#1c1c1c"  # Dark gray (almost black)

# Primary colors (3b1b signature)
BLUE_3B1B = "#3b82f6"      # Primary blue
YELLOW_3B1B = "#fbbf24"    # Accent yellow
TEAL_3B1B = "#14b8a6"      # Teal for highlights

# Neural network specific
NEURON_COLOR = "#4a9eff"    # Neuron fill
POSITIVE_WEIGHT = "#22c55e" # Green for positive weights
NEGATIVE_WEIGHT = "#ef4444" # Red for negative weights
NEUTRAL_COLOR = "#9ca3af"   # Gray for inactive

# Gradient colors
GRADIENT_START = "#60a5fa"  # Light blue
GRADIENT_END = "#7c3aed"    # Purple

# Text colors
TEXT_COLOR = WHITE
LABEL_COLOR = "#e5e5e5"     # Slightly dimmed white
MATH_COLOR = "#fde047"      # Yellow for math equations
```

## Color Usage Guidelines

### Neural Networks

```python
class NeuronColors:
    # Activation levels (use interpolation)
    @staticmethod
    def activation_color(value):
        """Map activation value [-1, 1] to color"""
        if value >= 0:
            return interpolate_color(NEUTRAL_COLOR, POSITIVE_WEIGHT, value)
        else:
            return interpolate_color(NEUTRAL_COLOR, NEGATIVE_WEIGHT, -value)

    # Weight visualization
    @staticmethod
    def weight_color(weight):
        """Map weight to color intensity"""
        intensity = min(abs(weight), 1)
        if weight >= 0:
            return interpolate_color(WHITE, POSITIVE_WEIGHT, intensity)
        else:
            return interpolate_color(WHITE, NEGATIVE_WEIGHT, intensity)
```

### Layer Distinction

```python
# Use different colors for different layer types
LAYER_COLORS = {
    "input": "#60a5fa",      # Blue
    "hidden": "#a78bfa",     # Purple
    "output": "#34d399",     # Green
    "conv": "#f97316",       # Orange
    "attention": "#ec4899",  # Pink
}
```

### Gradient Flow Visualization

```python
def gradient_magnitude_color(grad_value):
    """Visualize gradient magnitude"""
    normalized = min(abs(grad_value) / max_grad, 1)
    return interpolate_color("#1e3a5f", "#ff6b6b", normalized)
```

## Styling Objects

### Neurons

```python
neuron = Circle(
    radius=0.3,
    fill_color=NEURON_COLOR,
    fill_opacity=0.8,
    stroke_color=WHITE,
    stroke_width=2
)
```

### Connections/Weights

```python
connection = Line(
    start_point, end_point,
    stroke_color=weight_color(weight_value),
    stroke_width=1 + abs(weight_value) * 2,  # Thicker for stronger weights
    stroke_opacity=0.6 + abs(weight_value) * 0.4
)
```

### Text and Labels

```python
# Title text
title = Text("Neural Network", font_size=48, color=TEXT_COLOR)

# Math equations (always yellow/gold)
equation = MathTex(r"\sigma(x) = \frac{1}{1 + e^{-x}}", color=MATH_COLOR)

# Labels
label = Text("Layer 1", font_size=24, color=LABEL_COLOR)
```

## Forbidden

- Do NOT use pure black (#000000) as background - use #1c1c1c
- Do NOT use saturated primary colors (pure red/green/blue)
- Do NOT use more than 4-5 colors in one scene
- Do NOT use low contrast text colors
- Do NOT forget stroke on important shapes (neurons need visible boundaries)
