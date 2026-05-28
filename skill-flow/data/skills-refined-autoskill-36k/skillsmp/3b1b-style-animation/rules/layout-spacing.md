---
name: layout-spacing
description: Visual layout, spacing, margins, and overlap prevention
metadata:
  tags: layout, spacing, margins, composition, visual-hierarchy
priority: high
---

# Layout and Spacing Guidelines

Proper spacing is as important as the content itself. Crowded visuals confuse; clean layouts clarify.

## The Golden Rules

1. **Nothing should touch** - Always maintain buffer space between elements
2. **Consistent margins** - Use the same spacing throughout a scene
3. **Visual breathing room** - Important elements need space around them
4. **Hierarchy through space** - More important = more space around it

## Standard Spacing Constants

```python
# Use these constants throughout your animations
class Spacing:
    # Edge margins (from screen edge)
    EDGE_SMALL = 0.3
    EDGE_MEDIUM = 0.5
    EDGE_LARGE = 1.0

    # Element spacing
    TIGHT = 0.2       # Related items (label next to object)
    NORMAL = 0.5      # Default spacing
    COMFORTABLE = 0.8 # Distinct groups
    LOOSE = 1.2       # Major sections

    # Text spacing
    LINE_SPACING = 0.3
    PARAGRAPH_SPACING = 0.6

    # Node/graph spacing
    NODE_RADIUS = 0.4
    NODE_GAP = 1.5    # Center to center
    EDGE_LABEL_OFFSET = 0.25
```

## Screen Layout Zones

```
┌─────────────────────────────────────────────┐
│  TITLE ZONE (UP, buff=0.5)                  │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │                                     │    │
│  │         MAIN CONTENT ZONE           │    │
│  │         (CENTER area)               │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  INFO ZONE (DOWN, buff=0.8)                 │
├─────────────────────────────────────────────┤
│  LEFT      │    CENTER    │     RIGHT       │
│  SIDEBAR   │    STAGE     │     SIDEBAR     │
│  (buff=1)  │              │     (buff=1)    │
└─────────────────────────────────────────────┘
```

### Zone Usage

```python
# Title/header area
title.to_edge(UP, buff=0.5)

# Main content - keep centered, don't go to edges
content.move_to(ORIGIN)

# Info/footer area
formula.to_edge(DOWN, buff=0.8)

# Sidebars for auxiliary info
legend.to_edge(LEFT, buff=1.0)
stats.to_edge(RIGHT, buff=1.0)

# Corner placements
label.to_corner(UR, buff=0.5)
```

## Preventing Overlaps

### Check Before Placing

```python
def safe_place(mobject, target_pos, existing_mobjects, min_distance=0.5):
    """Place mobject, adjusting if it would overlap."""
    mobject.move_to(target_pos)

    for existing in existing_mobjects:
        if mobject.get_center()[1] == existing.get_center()[1]:  # Same height
            distance = abs(mobject.get_center()[0] - existing.get_center()[0])
            if distance < min_distance + mobject.width/2 + existing.width/2:
                # Shift to avoid overlap
                mobject.next_to(existing, RIGHT, buff=min_distance)

    return mobject
```

### Label Placement

```python
# ❌ BAD: Label overlaps with object
label.move_to(circle.get_center())

# ✅ GOOD: Label with proper offset
label.next_to(circle, UP, buff=0.2)

# ✅ BETTER: Check for collisions with other labels
def place_label(obj, label, direction=UP, buff=0.2, avoid=[]):
    """Place label avoiding collisions."""
    label.next_to(obj, direction, buff=buff)

    # Check for overlaps with items to avoid
    for other in avoid:
        if has_overlap(label, other):
            # Try different direction
            for alt_dir in [DOWN, LEFT, RIGHT, UR, UL, DR, DL]:
                label.next_to(obj, alt_dir, buff=buff)
                if not any(has_overlap(label, o) for o in avoid):
                    break

    return label

def has_overlap(mob1, mob2, threshold=0.1):
    """Check if two mobjects overlap."""
    # Bounding box check
    b1 = mob1.get_critical_point(ORIGIN)
    b2 = mob2.get_critical_point(ORIGIN)
    dist = np.linalg.norm(b1 - b2)
    min_dist = (mob1.width + mob2.width) / 2 + threshold
    return dist < min_dist
```

### Edge Labels in Graphs

```python
def place_edge_label(start_pos, end_pos, label, offset=0.25):
    """Place edge label perpendicular to edge, avoiding overlap."""
    mid = (start_pos + end_pos) / 2
    direction = end_pos - start_pos
    direction = direction / np.linalg.norm(direction)

    # Perpendicular direction
    perp = np.array([-direction[1], direction[0], 0])

    # Place label offset from edge
    label.move_to(mid + perp * offset)

    return label
```

## Layout Patterns

### Side-by-Side Comparison

```python
def create_comparison(left_content, right_content, labels=None):
    """Create side-by-side comparison with proper spacing."""

    left_group = VGroup(left_content)
    right_group = VGroup(right_content)

    # Position with gap in middle
    left_group.move_to(LEFT * 3)
    right_group.move_to(RIGHT * 3)

    # Add labels if provided
    if labels:
        left_label = Text(labels[0], font_size=24)
        right_label = Text(labels[1], font_size=24)
        left_label.next_to(left_group, UP, buff=0.3)
        right_label.next_to(right_group, UP, buff=0.3)

    # VS indicator in middle
    vs = Text("vs", font_size=20, color=GRAY)
    vs.move_to(ORIGIN)

    return VGroup(left_group, right_group, vs)
```

### Grid Layout

```python
def create_grid(items, rows, cols, cell_size=1.5, buff=0.3):
    """Arrange items in a grid with consistent spacing."""

    grid = VGroup()
    for i, item in enumerate(items):
        row = i // cols
        col = i % cols

        x = (col - (cols - 1) / 2) * (cell_size + buff)
        y = ((rows - 1) / 2 - row) * (cell_size + buff)

        item.move_to([x, y, 0])
        grid.add(item)

    return grid
```

### Vertical Stack

```python
def create_stack(items, spacing=0.5, alignment=LEFT):
    """Stack items vertically with consistent spacing."""

    group = VGroup(*items)
    group.arrange(DOWN, buff=spacing, aligned_edge=alignment)

    return group
```

## Text Layout

### Multi-line Text

```python
# ❌ BAD: Long single line that runs off screen
text = Text("This is a very long explanation that will definitely run off the edge of the screen")

# ✅ GOOD: Use line breaks or Paragraph
text = Text("This is a very long explanation\\nthat wraps to multiple lines", font_size=24)

# ✅ BETTER: Control width explicitly
from manim import Paragraph
text = Paragraph(
    "This is a very long explanation",
    "that wraps to multiple lines",
    "with controlled width",
    font_size=24,
    line_spacing=0.3
)
```

### Equation with Context

```python
# Give equations breathing room
equation = MathTex(r"E = mc^2")
context = Text("Einstein's famous equation", font_size=20, color=GRAY)

equation.move_to(ORIGIN)
context.next_to(equation, DOWN, buff=0.5)  # Not too close!

# Add visual emphasis with space
box = SurroundingRectangle(equation, buff=0.3, color=YELLOW)
```

## Dynamic Layout Adjustments

### Responsive to Content Size

```python
def fit_to_screen(mobject, margin=0.5):
    """Scale mobject to fit within screen bounds."""
    max_width = config.frame_width - 2 * margin
    max_height = config.frame_height - 2 * margin

    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)

    if mobject.height > max_height:
        mobject.scale(max_height / mobject.height)

    return mobject
```

### Auto-arrange on Add

```python
class AutoLayoutScene(Scene):
    """Scene that automatically manages layout."""

    def __init__(self):
        super().__init__()
        self.content_items = []

    def add_content(self, item, zone="center"):
        """Add content with automatic positioning."""
        self.content_items.append(item)

        if zone == "center":
            # Reflow all center items
            self.reflow_center()
        elif zone == "sidebar":
            item.to_edge(RIGHT, buff=1)

    def reflow_center(self):
        """Rearrange center content to avoid overlaps."""
        center_items = [i for i in self.content_items if not i.is_sidebar]
        group = VGroup(*center_items)
        group.arrange(DOWN, buff=0.5)
        group.move_to(ORIGIN)
```

## Common Mistakes

### ❌ DON'T

```python
# Too close to edge
title.to_edge(UP, buff=0.1)  # Will feel cramped

# Overlapping elements
label.move_to(circle)  # Label inside circle!

# Inconsistent spacing
item1.next_to(title, DOWN, buff=0.3)
item2.next_to(item1, DOWN, buff=0.8)  # Why different?

# Text running off screen
long_text = Text("Very long text that goes off screen...")
long_text.to_edge(LEFT)
```

### ✅ DO

```python
# Comfortable margin
title.to_edge(UP, buff=0.5)

# Clear separation
label.next_to(circle, UP, buff=0.2)

# Consistent spacing throughout
ITEM_SPACING = 0.5
item1.next_to(title, DOWN, buff=ITEM_SPACING)
item2.next_to(item1, DOWN, buff=ITEM_SPACING)

# Check and scale if needed
long_text = Text("Very long text...")
if long_text.width > config.frame_width - 1:
    long_text.scale_to_fit_width(config.frame_width - 1)
```

## Pre-render Checklist

Before rendering, verify:

- [ ] No elements touch screen edges (min 0.3 buffer)
- [ ] No overlapping text/labels
- [ ] Consistent spacing between similar elements
- [ ] Important elements have visual breathing room
- [ ] Text is readable (not too small, not too crowded)
- [ ] Graph nodes have enough separation
- [ ] Edge labels don't overlap edges or nodes
