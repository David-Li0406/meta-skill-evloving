---
name: animation-patterns
description: Advanced animation patterns from 3Blue1Brown style
metadata:
  tags: animation, patterns, lagged, cascading, state
priority: critical
---

# Advanced Animation Patterns

Patterns observed from 3Blue1Brown's video code.

## Core Requirements

**MUST** use LaggedStartMap for sequential element animations.

**MUST** use save_state/Restore for reversible transformations.

**MUST** build complexity progressively (layers, not all at once).

**MUST NOT** animate elements one-by-one with separate play() calls when they can be grouped.

**MUST NOT** use hard transitions without rate functions.

---

## 1. Element Grouping with Dictionaries

Map strings to visual objects for coordinated manipulation.

```python
class MyScene(Scene):
    def construct(self):
        # Group related elements
        self.node_to_circle = {}
        self.node_to_label = {}

        for name in ['A', 'B', 'C', 'D']:
            circle = Circle(radius=0.3, color=BLUE)
            label = Text(name, font_size=24)
            self.node_to_circle[name] = circle
            self.node_to_label[name] = label

        # Coordinate animations by group
        self.play(*[
            FadeIn(self.node_to_circle[n])
            for n in ['A', 'B', 'C']
        ])
```

## 2. LaggedStartMap for Cascading Effects

Sequential animations with controlled timing.

```python
# Cascade through elements with delay
boxes = [Square() for _ in range(5)]
self.play(
    LaggedStartMap(FadeIn, boxes, lag_ratio=0.2),
    run_time=2
)

# Cascade with custom animation
self.play(
    LaggedStartMap(
        lambda m: m.animate.set_fill(GREEN, opacity=0.5),
        boxes,
        lag_ratio=0.15
    ),
    run_time=1.5
)
```

## 3. State Save/Restore

Reversible transformations for clean animations.

```python
# Save initial state
element.save_state()

# Transform
self.play(element.animate.scale(2).set_color(RED))
self.wait()

# Restore to original
self.play(Restore(element))
```

## 4. Progressive Complexity

Build understanding layer by layer.

```python
def construct(self):
    # Layer 1: Basic structure
    nodes = self._create_nodes()
    self.play(FadeIn(nodes))

    # Layer 2: Add connections
    edges = self._create_edges()
    self.play(LaggedStartMap(Create, edges, lag_ratio=0.1))

    # Layer 3: Add labels
    labels = self._create_labels()
    self.play(LaggedStartMap(Write, labels, lag_ratio=0.1))

    # Layer 4: Highlight pattern
    self._highlight_path(['A', 'C', 'E'])
```

## 5. Coordinated Multi-Object Animations

Animate related objects together.

```python
# Instead of sequential:
self.play(FadeIn(text))
self.play(Create(arrow))
self.play(GrowFromCenter(circle))

# Do coordinated:
self.play(
    FadeIn(text),
    Create(arrow),
    GrowFromCenter(circle),
    run_time=1
)
```

## 6. Visual Layering

Foreground/background separation for clarity.

```python
# Background layer (dimmed)
background = VGroup(*inactive_elements)
background.set_opacity(0.3)

# Foreground layer (highlighted)
foreground = VGroup(*active_elements)

# Animate only foreground, background stays dim
self.play(
    Indicate(foreground[0]),
    run_time=0.5
)
```

## 7. Temporal Sequencing with Rate Functions

Control animation timing curves.

```python
# Smooth start and end
self.play(
    element.animate.shift(RIGHT * 3),
    rate_func=smooth,
    run_time=1
)

# Quick start, slow finish
self.play(
    element.animate.shift(UP * 2),
    rate_func=rush_into,
    run_time=0.8
)

# Bounce effect
self.play(
    element.animate.scale(1.2),
    rate_func=there_and_back,
    run_time=0.5
)
```

## 8. Animation Composition

Chain animations smoothly.

```python
# AnimationGroup for simultaneous
self.play(AnimationGroup(
    FadeIn(text1),
    FadeIn(text2),
    FadeIn(text3),
    lag_ratio=0.3
))

# Succession for sequential
self.play(Succession(
    FadeIn(step1),
    Wait(0.5),
    FadeIn(step2),
    Wait(0.5),
    FadeIn(step3),
))
```

## 9. Transform Chains

Smooth morphing between states.

```python
# Transform text through states
title = Text("Step 1")
self.play(Write(title))

for i in range(2, 5):
    new_title = Text(f"Step {i}")
    new_title.move_to(title)
    self.play(Transform(title, new_title), run_time=0.5)
```

## 10. Highlight Techniques

Draw attention without jarring transitions.

```python
# Subtle pulse
self.play(
    element.animate.scale(1.1),
    rate_func=there_and_back,
    run_time=0.4
)

# Color flash
self.play(
    Flash(element, color=YELLOW, line_length=0.3),
    run_time=0.3
)

# Circumscribe
self.play(
    Circumscribe(element, color=YELLOW),
    run_time=0.8
)

# Indicate (wiggle + color)
self.play(Indicate(element, color=YELLOW), run_time=0.5)
```

## Summary Checklist

For smooth, professional animations:

```
□ Group related elements with dictionaries
□ Use LaggedStartMap for cascading effects
□ Save/restore state for reversible transforms
□ Build complexity progressively (layers)
□ Coordinate related animations together
□ Separate visual layers (foreground/background)
□ Use appropriate rate functions
□ Chain transforms smoothly
□ Highlight subtly, not abruptly
```
