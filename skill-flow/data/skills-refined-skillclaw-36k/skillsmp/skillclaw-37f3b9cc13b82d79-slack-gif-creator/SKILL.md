---
name: slack-gif-creator
description: Use this skill when you need to create animated GIFs optimized for Slack, ensuring they meet specific size and quality constraints.
---

# Slack GIF Creator

A toolkit for creating animated GIFs optimized for Slack, providing utilities for validation, animation, and drawing.

## Slack Requirements

### Dimensions and Constraints

**Message GIFs:**
- Max size: ~2MB
- Optimal dimensions: 480x480
- Typical FPS: 15-20
- Color limit: 128-256
- Duration: 2-5 seconds

**Emoji GIFs:**
- Max size: 64KB (strict limit)
- Optimal dimensions: 128x128
- Typical FPS: 10-12
- Color limit: 32-48
- Duration: 1-2 seconds

### Core Workflow

1. **Create a GIF Builder:**
   ```python
   from core.gif_builder import GIFBuilder
   builder = GIFBuilder(width=128, height=128, fps=10)
   ```

2. **Generate Frames:**
   ```python
   from PIL import Image, ImageDraw

   for i in range(12):
       frame = Image.new('RGB', (128, 128), (240, 248, 255))
       draw = ImageDraw.Draw(frame)
       # Draw your animation using PIL primitives
       builder.add_frame(frame)
   ```

3. **Save with Optimization:**
   ```python
   builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
   ```

### Validators

To ensure a GIF meets Slack's constraints, use the following validators:

- **File Size Validator:**
   ```python
   from core.validators import check_slack_size
   passes, info = check_slack_size('emoji.gif', is_emoji=True)
   ```

- **Dimension Validator:**
   ```python
   from core.validators import validate_dimensions
   passes, info = validate_dimensions(128, 128, is_emoji=True)
   ```

### Drawing Graphics

#### Working with User-Uploaded Images
If a user uploads an image, consider whether they want to:
- **Use it directly** (e.g., "animate this", "split this into frames")
- **Use it as inspiration** (e.g., "make something like this")

Load and work with images using PIL:
```python
from PIL import Image
uploaded = Image.open('file.png')
```

#### Drawing from Scratch
When drawing graphics from scratch, use PIL ImageDraw primitives:
```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

### Tips for Quality
- Use thicker lines for outlines and shapes to ensure clarity.
- Keep designs simple to meet size constraints, especially for emoji GIFs.

This skill provides the flexibility to create engaging and optimized GIFs for Slack, allowing for creative expression while adhering to platform requirements.