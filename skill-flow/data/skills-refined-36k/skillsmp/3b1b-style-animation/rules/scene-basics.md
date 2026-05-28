---
name: scene-basics
description: Scene creation and animation timing fundamentals
metadata:
  tags: manim, scene, animation, timing
---

# Scene Basics and Animation Timing

## Scene Structure

Every scene MUST follow this pattern:

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # 1. Create objects
        # 2. Add to scene
        # 3. Animate
        # 4. Wait for viewer comprehension
        pass
```

## Animation Timing Guidelines

### Standard Durations (3b1b style)

```python
# Object appearance
self.play(Create(obj), run_time=1)      # Drawing objects
self.play(FadeIn(obj), run_time=0.5)    # Quick appearance
self.play(Write(text), run_time=1.5)    # Text/equations

# Transformations
self.play(Transform(a, b), run_time=1)  # Shape morphing
self.play(MoveToTarget(obj), run_time=0.8)  # Movement

# Emphasis
self.play(Indicate(obj), run_time=0.5)  # Highlight
self.play(Flash(point), run_time=0.3)   # Quick flash

# Waiting
self.wait(0.5)  # Brief pause
self.wait(1)    # Standard pause
self.wait(2)    # Extended pause for complex concepts
```

## Grouping Animations

### Sequential (one after another)

```python
self.play(Create(circle))
self.play(Create(square))
```

### Simultaneous (at the same time)

```python
self.play(
    Create(circle),
    FadeIn(label),
    run_time=1
)
```

### Staggered with AnimationGroup

```python
neurons = VGroup(*[Circle() for _ in range(5)])
self.play(
    AnimationGroup(
        *[Create(n) for n in neurons],
        lag_ratio=0.2  # 0.2 second delay between each
    )
)
```

## Scene Sections

Use wait() to create natural breaks:

```python
def construct(self):
    # Section 1: Introduction
    title = Text("Neural Networks")
    self.play(Write(title))
    self.wait(1)

    # Section 2: Main content
    self.play(FadeOut(title))
    # ... main content ...

    # Section 3: Conclusion
    self.wait(2)
```

## Forbidden

- Do NOT use `run_time=0` - always provide visible animation time
- Do NOT skip `self.wait()` between concept transitions
- Do NOT animate more than 3-4 elements simultaneously without lag_ratio
- Do NOT use abrupt cuts - use FadeOut/FadeIn for transitions
