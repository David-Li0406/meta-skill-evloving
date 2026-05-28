---
name: slack-gif-creator
description: Use this skill to create animated GIFs optimized for Slack, incorporating validators for size constraints and composable animation primitives.
---

# Slack GIF Creator

A comprehensive toolkit for creating animated GIFs optimized for Slack. This skill provides utilities for validating GIFs against Slack's requirements, composable animation primitives, and optional helper utilities. Apply these tools creatively to achieve your desired animations.

## Slack Requirements

Slack has specific requirements for GIFs based on their use:

**Message GIFs:**
- Max size: ~2MB
- Optimal dimensions: 480x480
- Typical FPS: 15-20
- Color limit: 128-256
- Duration: 2-5s

**Emoji GIFs:**
- Max size: 64KB (strict limit)
- Optimal dimensions: 128x128
- Typical FPS: 10-12
- Color limit: 32-48
- Duration: 1-2s

**Strategies for Emoji GIFs:**
- Limit to 10-15 frames total
- Use 32-48 colors maximum
- Keep designs simple
- Avoid gradients
- Validate file size frequently

## Core Workflow

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. Create builder
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. Generate frames
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # Draw your animation using PIL primitives
    # (circles, polygons, lines, etc.)

    builder.add_frame(frame)

# 3. Save with optimization
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## Drawing Graphics

### Working with User-Uploaded Images
If a user uploads an image, consider whether they want to:
- **Use it directly** (e.g., "animate this", "split this into frames")
- **Use it as inspiration** (e.g., "make something like this")

Load and work with images using PIL:
```python
from PIL import Image

uploaded = Image.open('file.png')
# Use directly, or just as reference for colors/style
```

### Drawing from Scratch
When drawing graphics from scratch, use PIL ImageDraw primitives:

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# Circles/ovals
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# Stars, triangles, any polygon
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# Lines
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# Rectangles
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

### Making Graphics Look Good
Graphics should look polished and creative, not basic. Here are some tips:
- Use thicker lines (width=2 or higher).
- Add visual depth with gradients and layered shapes.
- Use vibrant, complementary colors and ensure good contrast.
- For complex shapes, combine polygons and ellipses, and add details.

## Available Utilities

### GIFBuilder (`core.gif_builder`)
Assembles frames and optimizes for Slack:
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # Add PIL Image
builder.add_frames(frames)  # Add list of frames
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### Validators (`core.validators`)
Check if GIF meets Slack requirements:
```python
from core.validators import validate_gif, is_slack_ready

# Detailed validation
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# Quick check
if is_slack_ready('my.gif'):
    print("Ready!")
```

### Easing Functions (`core.easing`)
Smooth motion instead of linear:
```python
from core.easing import interpolate

# Progress from 0.0 to 1.0
t = i / (num_frames - 1)

# Apply easing
y = interpolate(start=0, end=400, t=t, easing='ease_out')
```

### Animation Primitives
These are composable building blocks for motion. Apply these to any object in any combination:
- **Shake**
- **Bounce**
- **Spin / Rotate**
- **Pulse / Heartbeat**
- **Fade**
- **Zoom**
- **Explode / Shatter**
- **Wiggle / Jiggle**
- **Slide**
- **Flip**
- **Morph / Transform**
- **Move Effect**
- **Kaleidoscope Effect**

## Optimization Strategies
When your GIF is too large:
1. Reduce frames (lower FPS or shorter duration).
2. Reduce colors (128 → 64 colors).
3. Reduce dimensions (480x480 → 320x320).
4. Enable duplicate frame removal.
5. For Emoji GIFs, limit to 10-12 frames and use 32-40 colors maximum.

## Example Composition Patterns
### Simple Reaction (Pulsing)
```python
builder = GIFBuilder(128, 128, 10)

for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    scale = 1.0 + math.sin(i * 0.5) * 0.15
    size = int(60 * scale)
    draw_emoji(frame, '😱', position=(64-size//2, 64-size//2), size=size)
    builder.add_frame(frame)

builder.save('reaction.gif', num_colors=40, optimize_for_emoji=True)
```

### Action with Impact (Bounce + Flash)
```python
builder = GIFBuilder(480, 480, 20)

# Phase 1: Object falls
for i in range(15):
    frame = create_gradient_background(480, 480, (240, 248, 255), (200, 230, 255))
    t = i / 14
    y = interpolate(0, 350, t, 'ease_in')
    draw_emoji(frame, '⚽', position=(220, int(y)), size=80)
    builder.add_frame(frame)

# Phase 2: Impact + flash
for i in range(8):
    frame = create_gradient_background(480, 480, (240, 248, 255), (200, 230, 255))
    if i < 3:
        frame = create_impact_flash(frame, (240, 350), radius=120, intensity=0.6)
    draw_emoji(frame, '⚽', position=(220, 350), size=80)
    builder.add_frame(frame)

builder.save('goal.gif', num_colors=128)
```

## Dependencies
To use this toolkit, install these dependencies:
```bash
pip install pillow imageio numpy
```