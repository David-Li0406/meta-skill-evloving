---
name: visual-quality
description: Strict visual quality requirements - NO overlapping, proper hierarchy, clean layouts
metadata:
  tags: quality, overlap, visual, hierarchy, validation
priority: highest
---

# Visual Quality Standards

**These rules are NON-NEGOTIABLE. Every animation must pass these checks.**

## The Three Absolute Rules

```
1. NOTHING OVERLAPS - Text, graphics, labels must NEVER overlap
2. EVERYTHING READABLE - All text must be clearly visible and readable
3. CLEAR HIERARCHY - Visual importance must be obvious
```

---

## Rule 1: No Overlapping Elements

### What Counts as Overlap

```
❌ Text on top of text
❌ Text on top of graphics
❌ Labels overlapping edges
❌ Nodes too close together
❌ Elements touching screen edges
```

### Validation Code

```python
def validate_no_overlaps(scene):
    """Check all mobjects for overlaps. Run before render."""

    all_mobs = scene.mobjects
    issues = []

    for i, mob1 in enumerate(all_mobs):
        for mob2 in all_mobs[i+1:]:
            if check_overlap(mob1, mob2):
                issues.append(f"OVERLAP: {mob1} and {mob2}")

    if issues:
        print("⚠️ VISUAL QUALITY ISSUES:")
        for issue in issues:
            print(f"  - {issue}")
        raise ValueError("Fix overlaps before rendering!")

    return True


def check_overlap(mob1, mob2, buffer=0.1):
    """Check if two mobjects overlap."""
    # Get bounding boxes
    b1_min = mob1.get_corner(DL)
    b1_max = mob1.get_corner(UR)
    b2_min = mob2.get_corner(DL)
    b2_max = mob2.get_corner(UR)

    # Add buffer
    b1_min -= buffer
    b1_max += buffer

    # Check intersection
    x_overlap = (b1_min[0] < b2_max[0]) and (b1_max[0] > b2_min[0])
    y_overlap = (b1_min[1] < b2_max[1]) and (b1_max[1] > b2_min[1])

    return x_overlap and y_overlap
```

### Safe Placement Patterns

```python
class SafeLayout:
    """Utility class for safe element placement."""

    def __init__(self, scene):
        self.scene = scene
        self.placed_items = []

    def place(self, mobject, position, avoid_overlap=True):
        """Place mobject, adjusting if necessary to avoid overlaps."""
        mobject.move_to(position)

        if avoid_overlap:
            self._resolve_overlaps(mobject)

        self.placed_items.append(mobject)
        return mobject

    def place_label(self, label, target, direction=UP, buff=0.3):
        """Place label near target, trying multiple directions if needed."""
        directions = [direction, DOWN, LEFT, RIGHT, UR, UL, DR, DL]

        for d in directions:
            label.next_to(target, d, buff=buff)
            if not self._has_any_overlap(label):
                self.placed_items.append(label)
                return label

        # If all directions fail, scale down and try again
        label.scale(0.8)
        return self.place_label(label, target, direction, buff)

    def _has_any_overlap(self, mobject):
        """Check if mobject overlaps with any placed item."""
        for item in self.placed_items:
            if check_overlap(mobject, item):
                return True
        return False

    def _resolve_overlaps(self, mobject):
        """Shift mobject to resolve overlaps."""
        max_attempts = 10
        shift_amount = 0.2

        for _ in range(max_attempts):
            overlap_found = False
            for item in self.placed_items:
                if check_overlap(mobject, item):
                    overlap_found = True
                    # Shift away from overlapping item
                    direction = mobject.get_center() - item.get_center()
                    if np.linalg.norm(direction) > 0:
                        direction = direction / np.linalg.norm(direction)
                    else:
                        direction = RIGHT
                    mobject.shift(direction * shift_amount)

            if not overlap_found:
                break
```

---

## Rule 2: Everything Readable

### Minimum Sizes

```python
class TextSizes:
    TITLE = 48          # Main titles
    HEADING = 36        # Section headings
    BODY = 28           # Main content
    LABEL = 22          # Labels on graphics
    CAPTION = 18        # Small captions
    ANNOTATION = 16     # Tiny annotations (use sparingly)

    # NEVER go below 14 for any text
    MINIMUM = 14
```

### Contrast Requirements

```python
class Contrast:
    """Ensure text is readable against background."""

    DARK_BG = "#1c1c1c"  # Standard 3b1b background

    # Good text colors on dark background
    GOOD_COLORS = [
        "#ffffff",  # White - best
        "#e5e5e5",  # Light gray - good
        "#fbbf24",  # Yellow - accent
        "#3b82f6",  # Blue - accent
        "#22c55e",  # Green - accent
    ]

    # NEVER use these on dark background
    BAD_COLORS = [
        "#333333",  # Too dark
        "#666666",  # Too dark
        "#1c1c1c",  # Same as background!
    ]
```

### Text Spacing

```python
# ❌ BAD: Text too close together
line1.next_to(line2, UP, buff=0.1)  # Cramped!

# ✅ GOOD: Readable spacing
line1.next_to(line2, UP, buff=0.4)  # Clear separation
```

---

## Rule 3: Clear Visual Hierarchy

### Hierarchy Principles

```
1. MOST IMPORTANT = Largest + Most contrast + Center
2. SUPPORTING = Medium size + Less contrast + Around edges
3. AUXILIARY = Smallest + Subtle color + Corners/edges
```

### Implementation

```python
class VisualHierarchy:
    """Create proper visual hierarchy."""

    # Size hierarchy
    SIZES = {
        "primary": 1.0,
        "secondary": 0.8,
        "tertiary": 0.6,
    }

    # Color hierarchy (on dark background)
    COLORS = {
        "primary": "#ffffff",     # Pure white - main focus
        "secondary": "#e5e5e5",   # Light gray - supporting
        "tertiary": "#9ca3af",    # Medium gray - auxiliary
        "accent": "#fbbf24",      # Yellow - highlights
    }

    # Position hierarchy
    POSITIONS = {
        "primary": ORIGIN,        # Center = most important
        "secondary": UP * 2,      # Top = titles/headers
        "tertiary": DOWN * 2.5,   # Bottom = info/captions
    }
```

---

## Screen Zones (Strict)

```
┌──────────────────────────────────────────────────────────────┐
│                     TITLE ZONE (y > 2.5)                     │
│                     - Titles, headers only                   │
│──────────────────────────────────────────────────────────────│
│                                                              │
│   LEFT         │     MAIN CONTENT ZONE      │      RIGHT     │
│   MARGIN       │     (-2.5 < y < 2.5)       │      MARGIN    │
│   (x < -5)     │     - Core visuals here    │      (x > 5)   │
│   - Legends    │     - Keep centered        │      - Stats   │
│                │                            │                │
│──────────────────────────────────────────────────────────────│
│                     INFO ZONE (y < -2.5)                     │
│                     - Formulas, captions                     │
└──────────────────────────────────────────────────────────────┘
```

### Zone Validation

```python
def validate_zones(mobject, expected_zone):
    """Validate mobject is in correct zone."""
    center = mobject.get_center()
    x, y = center[0], center[1]

    zones = {
        "title": y > 2.5,
        "main": -2.5 <= y <= 2.5 and -5 <= x <= 5,
        "info": y < -2.5,
        "left_margin": x < -5,
        "right_margin": x > 5,
    }

    if not zones.get(expected_zone, False):
        print(f"⚠️ {mobject} is not in {expected_zone} zone!")
        return False
    return True
```

---

## Graph-Specific Rules

### Node Placement

```python
class GraphLayout:
    NODE_RADIUS = 0.4
    MIN_NODE_DISTANCE = 2.0  # Center to center (must be > 2 * radius + buffer)
    LABEL_OFFSET = 0.3
    EDGE_LABEL_OFFSET = 0.35

    @staticmethod
    def validate_graph(nodes, edges, labels):
        """Validate graph layout."""
        issues = []

        # Check node distances
        positions = list(nodes.values())
        for i, pos1 in enumerate(positions):
            for pos2 in positions[i+1:]:
                dist = np.linalg.norm(pos1 - pos2)
                if dist < GraphLayout.MIN_NODE_DISTANCE:
                    issues.append(f"Nodes too close: {dist:.1f} < {GraphLayout.MIN_NODE_DISTANCE}")

        # Check labels don't overlap nodes
        for label in labels:
            for node_pos in positions:
                dist = np.linalg.norm(label.get_center() - node_pos)
                if dist < GraphLayout.NODE_RADIUS + 0.2:
                    issues.append(f"Label overlaps node")

        if issues:
            for issue in issues:
                print(f"⚠️ {issue}")
            return False
        return True
```

### Edge Labels

```python
def place_edge_label(start, end, label, offset=0.35):
    """Place edge label safely - perpendicular to edge."""
    mid = (start + end) / 2
    direction = end - start
    direction = direction / np.linalg.norm(direction)

    # Perpendicular direction
    perp = np.array([-direction[1], direction[0], 0])

    # Always place on consistent side (e.g., "above" the edge)
    if perp[1] < 0:
        perp = -perp

    label.move_to(mid + perp * offset)
    return label
```

---

## Pre-Render Quality Check

**Run this before EVERY render:**

```python
def quality_check(scene):
    """Complete quality validation."""

    print("🔍 Running quality check...")
    passed = True

    # 1. Check for overlaps
    print("  Checking overlaps...")
    if not validate_no_overlaps(scene):
        passed = False

    # 2. Check text sizes
    print("  Checking text sizes...")
    for mob in scene.mobjects:
        if hasattr(mob, 'font_size'):
            if mob.font_size < 14:
                print(f"    ⚠️ Text too small: {mob.font_size}")
                passed = False

    # 3. Check screen bounds
    print("  Checking screen bounds...")
    for mob in scene.mobjects:
        if mob.get_right()[0] > 7 or mob.get_left()[0] < -7:
            print(f"    ⚠️ Element exceeds horizontal bounds")
            passed = False
        if mob.get_top()[1] > 4 or mob.get_bottom()[1] < -4:
            print(f"    ⚠️ Element exceeds vertical bounds")
            passed = False

    if passed:
        print("✅ Quality check passed!")
    else:
        print("❌ Quality check FAILED - fix issues before rendering")

    return passed
```

---

## Quick Reference

| Check | Requirement |
|-------|-------------|
| Text overlap | NEVER |
| Graphics overlap | NEVER |
| Min text size | 14pt |
| Min node distance | 2.0 units |
| Screen margin | 0.5 units minimum |
| Label buffer | 0.3 units minimum |
| Edge label offset | 0.35 units |
