# SVG Graph Workflow

**What this file covers:** Complete workflow for creating SVG coordinate graphs, pixel formulas, pre-calculated tables, and validation rules.

**Only read this file if Visual Type = "SVG visual" (coordinate graphs).**

For non-graph diagrams (tape diagrams, hangers, etc.), see `../../reference/diagram-patterns.md`.

---

## Workflow Overview

**SVG graphs are the ONLY component that requires the clone-and-modify workflow.** All other card-patterns use simple placeholder replacement.

```
Step 1: READ graph-snippet.html       ← Copy the complete SVG structure
Step 2: READ this file                ← Get formulas and tables
Step 3: CALCULATE pixel positions     ← For your specific scale
Step 4: MODIFY the copied SVG         ← Replace values
Step 5: READ annotation-snippet.html  ← Add labels and annotations
Step 6: VERIFY grid alignment         ← Run the checklist
```

**DO NOT create graphs from scratch.** Always copy and modify from graph-snippet.html.

---

## Required Reading (HTML Files)

**Before using the formulas below, READ these HTML files:**

```
READ: card-patterns/complex-patterns/graph-snippet.html      ← SOURCE OF TRUTH for SVG structure
READ: card-patterns/complex-patterns/annotation-snippet.html ← SOURCE OF TRUTH for annotation patterns
```

This markdown file contains only formulas and tables. The HTML patterns you copy and modify are in the files above.

---

## SVG Graph Checklist (VERIFY BEFORE WRITING SLIDE)

**Structure:**
- [ ] Started from graph-snippet.html (NOT from scratch)
- [ ] SVG wrapped in container with `data-pptx-region="svg-container"`
- [ ] Container has position attributes: `data-pptx-x`, `data-pptx-y`, `data-pptx-w`, `data-pptx-h`

**Coordinate System:**
- [ ] X_MAX and Y_MAX set correctly for your data
- [ ] Grid lines align with axis labels (same pixel values)
- [ ] Single "0" at origin (not two separate zeros)
- [ ] Scale labels go to last tick before arrow

**Axes & Lines:**
- [ ] Axes have arrowheads (marker-end)
- [ ] Data lines extend to plot edges with arrows
- [ ] All lines use correct colors from styling.md

**Annotations:**
- [ ] All `<text>` elements have `font-family="Arial"`
- [ ] Annotations use `font-weight="normal"` (NOT bold)
- [ ] Annotation positions calculated using pixel formula

**PPTX Export:**
- [ ] Each line in its own `data-pptx-layer` group
- [ ] Each annotation in its own `data-pptx-layer` group
- [ ] Layer names follow convention: `line-1`, `label-b0`, `arrow-shift`, etc.

---

## Grid Alignment Rules (CRITICAL)

**The #1 problem with SVG graphs is misaligned grids.**

### Rule 1: Use Consistent Spacing Formula

All coordinate calculations MUST use the same linear interpolation formula:

```
pixelX = ORIGIN_X + (dataX / X_MAX) * PLOT_WIDTH
pixelY = ORIGIN_Y - (dataY / Y_MAX) * PLOT_HEIGHT
```

Where:
- `ORIGIN_X`, `ORIGIN_Y` = pixel coordinates of the origin (0,0) point
- `PLOT_WIDTH` = width of the plot area in pixels
- `PLOT_HEIGHT` = height of the plot area in pixels
- `X_MAX`, `Y_MAX` = maximum data values on each axis

### Rule 2: Grid Lines Must Match Labels

If you place a label at x=40 for value "0", x=150 for value "5", and x=260 for value "10":
- Grid lines MUST be at x=40, 150, 260 (NOT different values)
- The spacing is (260-40)/(10-0) = 22 pixels per unit

### Rule 3: Define Constants First

Before writing any SVG, define these values:

```
ORIGIN_X = 40      // Left edge of plot (after Y-axis labels)
ORIGIN_Y = 170     // Bottom edge of plot (above X-axis labels)
PLOT_WIDTH = 220   // Width from origin to right edge
PLOT_HEIGHT = 150  // Height from origin to top edge
X_MAX = 10         // Maximum X value
Y_MAX = 100        // Maximum Y value
```

---

## Axis Requirements

**Every coordinate plane MUST have all 5 elements:**

### 1. Tick Marks at Each Label Position

```html
<!-- X-axis ticks (5px below axis, from y=170 to y=175) -->
<g stroke="#1e293b" stroke-width="1.5">
    <line x1="40" y1="170" x2="40" y2="175"/>
    <line x1="95" y1="170" x2="95" y2="175"/>
    <line x1="150" y1="170" x2="150" y2="175"/>
    <!-- ... one tick per label position -->
</g>

<!-- Y-axis ticks (5px left of axis, from x=35 to x=40) -->
<g stroke="#1e293b" stroke-width="1.5">
    <line x1="35" y1="170" x2="40" y2="170"/>
    <line x1="35" y1="132.5" x2="40" y2="132.5"/>
    <!-- ... one tick per label position -->
</g>
```

### 2. Arrowheads on Both Axes

```html
<defs>
  <marker id="axis-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#1e293b"/>
  </marker>
</defs>

<!-- X-axis with arrow (extends 10px past last label) -->
<line x1="40" y1="170" x2="275" y2="170" stroke="#1e293b" stroke-width="2" marker-end="url(#axis-arrow)"/>

<!-- Y-axis with arrow (extends 10px past last label) -->
<line x1="40" y1="180" x2="40" y2="5" stroke="#1e293b" stroke-width="2" marker-end="url(#axis-arrow)"/>
```

### 3. Single "0" at Origin (NOT two separate zeros)

```html
<!-- ONE zero label at origin, positioned to serve both axes -->
<text x="33" y="182" fill="#64748b" font-family="Arial" font-size="11" text-anchor="end">0</text>
```

**WRONG:**
```html
<!-- DON'T do this - two separate zeros -->
<text x="40" y="185">0</text>  <!-- X-axis zero -->
<text x="35" y="174">0</text>  <!-- Y-axis zero - WRONG! -->
```

### 4. Complete Scale Labels (to the arrows)

Labels must go all the way to the last tick mark before the arrow:
- X-axis: 0, 10, 20, 30, 40, 50 (if X_MAX=50)
- Y-axis: 0, 10, 20, 30, 40, 50 (if Y_MAX=50)

**Scale must be consistent** - use increments of 5, 10, 20, 25, 50, or 100.

### 5. Axis Labels (Optional)

If including axis labels like "x" and "y":
```html
<text x="280" y="175" fill="#64748b" font-family="Arial" font-size="12" font-style="italic">x</text>
<text x="45" y="8" fill="#64748b" font-family="Arial" font-size="12" font-style="italic">y</text>
```

---

## Line Extension Rules

**Lines must extend to the edges of the plot area** with arrows showing they continue beyond.

### How to Calculate Line Endpoints

For a line y = mx + b within plot area (0, 0) to (X_MAX, Y_MAX):

**Step 1: Calculate where line intersects plot boundaries**
```
Left edge (x=0):      y = b
Right edge (x=X_MAX): y = m * X_MAX + b
Top edge (y=Y_MAX):   x = (Y_MAX - b) / m
Bottom edge (y=0):    x = -b / m
```

**Step 2: Determine entry point (where line enters plot area)**
- If 0 <= b <= Y_MAX: entry is **(0, b)** on left edge
- If b < 0: entry is **(-b/m, 0)** on bottom edge
- If b > Y_MAX: entry is **((Y_MAX-b)/m, Y_MAX)** on top edge

**Step 3: Determine exit point (where line exits plot area)**
- Calculate y at x=X_MAX: `y_exit = m * X_MAX + b`
- If 0 <= y_exit <= Y_MAX: exit is **(X_MAX, y_exit)** on right edge
- If y_exit > Y_MAX: exit is **((Y_MAX-b)/m, Y_MAX)** on top edge
- If y_exit < 0: exit is **(-b/m, 0)** on bottom edge

**Step 4: Draw line with arrow at exit point**
- Use `marker-end="url(#line-arrow)"` to show line continues

### Line Arrow Marker (separate from axis arrows)

```html
<defs>
    <marker id="line-arrow" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
        <polygon points="0 0, 6 2, 0 4" fill="currentColor"/>
    </marker>
</defs>
```

### Examples

**Example 1: y = 10x (steep, hits top before right edge)**
- X_MAX=8, Y_MAX=80
- Entry: (0, 0) - starts at origin
- At x=8: y=80 - exactly at corner
- Exit: (8, 80) - right-top corner
- Draw: `<line x1="40" y1="170" x2="260" y2="20" ... marker-end="url(#line-arrow)"/>`

**Example 2: y = 5x + 20 (moderate slope, y-intercept at 20)**
- X_MAX=8, Y_MAX=80
- Entry: (0, 20) - left edge at y=20
- At x=8: y=60 - still within Y_MAX
- Exit: (8, 60) - right edge at y=60
- Draw: from (0,20) to (8,60) with arrow

**Example 3: y = 20x (very steep, exits through top)**
- X_MAX=8, Y_MAX=80
- Entry: (0, 0) - origin
- At x=4: y=80 - hits top
- Exit: (4, 80) - top edge at x=4
- Draw: from (0,0) to (4,80) with arrow pointing up-right

### Pixel Conversion for Line Endpoints

After calculating data coordinates, convert to pixels:
```
pixelX = 40 + (dataX / X_MAX) * 220
pixelY = 170 - (dataY / Y_MAX) * 150
```

---

## Quick Reference: Pixel Calculations

### Standard Plot Area (viewBox 280x200)

| Constant | Value | Purpose |
|----------|-------|---------|
| ORIGIN_X | 40 | X pixel of origin |
| ORIGIN_Y | 170 | Y pixel of origin |
| PLOT_WIDTH | 220 | Pixels from x=0 to x=max |
| PLOT_HEIGHT | 150 | Pixels from y=0 to y=max |
| LABEL_Y_OFFSET | 185 | Y pixel for X-axis labels |
| LABEL_X_OFFSET | 35 | X pixel for Y-axis labels |

### Conversion Formulas

```javascript
// Data to Pixel
function dataToPixelX(dataX, xMax) {
    return 40 + (dataX / xMax) * 220;
}

function dataToPixelY(dataY, yMax) {
    return 170 - (dataY / yMax) * 150;
}

// Example: Point (6, 45) with X_MAX=10, Y_MAX=100
// pixelX = 40 + (6/10)*220 = 40 + 132 = 172
// pixelY = 170 - (45/100)*150 = 170 - 67.5 = 102.5
```

---

## Common X-Axis Scales

Use these pre-calculated values for common scales (ORIGIN_X=40, PLOT_WIDTH=220):

### X: 0 to 4 (spacing = 55px per unit)
| Data | Pixel |
|------|-------|
| 0 | 40 |
| 1 | 95 |
| 2 | 150 |
| 3 | 205 |
| 4 | 260 |

### X: 0 to 5 (spacing = 44px per unit)
| Data | Pixel |
|------|-------|
| 0 | 40 |
| 1 | 84 |
| 2 | 128 |
| 3 | 172 |
| 4 | 216 |
| 5 | 260 |

### X: 0 to 8 (spacing = 27.5px per unit)
| Data | Pixel |
|------|-------|
| 0 | 40 |
| 2 | 95 |
| 4 | 150 |
| 6 | 205 |
| 8 | 260 |

### X: 0 to 10 (spacing = 22px per unit)
| Data | Pixel |
|------|-------|
| 0 | 40 |
| 2 | 84 |
| 4 | 128 |
| 5 | 150 |
| 6 | 172 |
| 8 | 216 |
| 10 | 260 |

### X: 0 to 12 (spacing = 18.33px per unit)
| Data | Pixel |
|------|-------|
| 0 | 40 |
| 3 | 95 |
| 6 | 150 |
| 9 | 205 |
| 12 | 260 |

### X: 0 to 20 (spacing = 11px per unit)
| Data | Pixel |
|------|-------|
| 0 | 40 |
| 5 | 95 |
| 10 | 150 |
| 15 | 205 |
| 20 | 260 |

---

## Common Y-Axis Scales

Use these pre-calculated values (ORIGIN_Y=170, PLOT_HEIGHT=150):

### Y: 0 to 100 (spacing = 1.5px per unit)
| Data | Pixel |
|------|-------|
| 0 | 170 |
| 25 | 132.5 |
| 50 | 95 |
| 75 | 57.5 |
| 100 | 20 |

### Y: 0 to 80 (spacing = 1.875px per unit)
| Data | Pixel |
|------|-------|
| 0 | 170 |
| 20 | 132.5 |
| 40 | 95 |
| 60 | 57.5 |
| 80 | 20 |

### Y: 0 to 200 (spacing = 0.75px per unit)
| Data | Pixel |
|------|-------|
| 0 | 170 |
| 50 | 132.5 |
| 100 | 95 |
| 150 | 57.5 |
| 200 | 20 |

### Y: 0 to 400 (spacing = 0.375px per unit)
| Data | Pixel |
|------|-------|
| 0 | 170 |
| 100 | 132.5 |
| 200 | 95 |
| 300 | 57.5 |
| 400 | 20 |

---

## Scale Selection Reference

**Target: 10 or fewer ticks per axis**

**X-AXIS (ORIGIN_X=40, PLOT_WIDTH=220):**
| X_MAX | Increment | Ticks | Pixel positions |
|-------|-----------|-------|-----------------|
| 4     | 1         | 5     | 0->40, 1->95, 2->150, 3->205, 4->260 |
| 5     | 1         | 6     | 0->40, 1->84, 2->128, 3->172, 4->216, 5->260 |
| 6     | 1         | 7     | 0->40, 1->77, 2->113, 3->150, 4->187, 5->223, 6->260 |
| 8     | 2         | 5     | 0->40, 2->95, 4->150, 6->205, 8->260 |
| 10    | 2         | 6     | 0->40, 2->84, 4->128, 6->172, 8->216, 10->260 |

**Y-AXIS (ORIGIN_Y=170, PLOT_HEIGHT=150):**
| Y_MAX | Increment | Ticks | Notes |
|-------|-----------|-------|-------|
| 9     | 1         | 10    | Max for counting by 1s |
| 18    | 2         | 10    | Max for counting by 2s |
| 36    | 4         | 10    | Count by 4s |
| 45    | 5         | 10    | Count by 5s |
| 72    | 8         | 10    | Count by 8s |
| 90    | 10        | 10    | Count by 10s |

**RULE: Grid lines at EVERY tick position. Never skip values!**

---

## Preventing Element Overlap (CRITICAL)

**The #2 problem with SVG graphs is overlapping elements.**

### Recommended Element Sizes

| Element | Recommended Size | Max Size |
|---------|-----------------|----------|
| Data point circles | r="4" to r="5" | r="6" |
| Point labels | font-size="9" to "10" | font-size="11" |
| Arrow stroke width | stroke-width="2" | stroke-width="3" |
| Arrow markers | markerWidth="6" markerHeight="4" | markerWidth="8" markerHeight="5" |
| Annotation text | font-size="9" | font-size="11" |

### Label Positioning Strategy

**Point labels** - Position AWAY from other elements:
- If point is in upper area: place label ABOVE (y - 10px)
- If point is in lower area: place label BELOW (y + 15px)
- If two points are close horizontally: stagger labels (one above, one below)
- Never place labels directly on the axes

**Annotation labels** (rise/run, change in y/x):
- Position to the LEFT of vertical arrows (x - 25px)
- Position BELOW horizontal arrows (y + 15px)
- Use smaller font-size="9" for annotations

### Minimum Spacing Guidelines

| Between | Minimum Distance |
|---------|-----------------|
| Point label and point center | 10px |
| Point label and axis | 15px |
| Two point labels | 20px |
| Arrow end and target point | 5px gap |
| Annotation text and arrow line | 3px |

### Overlap Scenarios to Check

Before finalizing, verify NO overlaps between:
- [ ] Point labels and data points
- [ ] Point labels and axis labels
- [ ] Point labels and grid lines (especially at intersections)
- [ ] Arrow markers and data points
- [ ] Arrow markers and axes
- [ ] Annotation text and arrows
- [ ] Two point labels (when points are close together)

---

## Common Mistakes to Avoid

### WRONG: Hardcoded unrelated grid positions
```html
<!-- BAD: Grid lines don't match labels -->
<line x1="100" y1="20" x2="100" y2="170"/>  <!-- Grid at x=100 -->
<text x="95" y="185">2</text>                 <!-- Label at x=95 - MISMATCH! -->
```

### CORRECT: Grid and labels use same positions
```html
<!-- GOOD: Grid lines match labels -->
<line x1="95" y1="20" x2="95" y2="170"/>   <!-- Grid at x=95 -->
<text x="95" y="185">2</text>               <!-- Label at x=95 - ALIGNED! -->
```

### WRONG: Inconsistent spacing
```html
<!-- BAD: Spacing not uniform -->
<text x="40">0</text>   <!-- 0 at 40 -->
<text x="100">2</text>  <!-- 2 at 100 (60px from 0) -->
<text x="150">4</text>  <!-- 4 at 150 (50px from 2) - WRONG! -->
```

### CORRECT: Uniform spacing
```html
<!-- GOOD: Each tick is 55px apart -->
<text x="40">0</text>   <!-- 0 at 40 -->
<text x="95">2</text>   <!-- 2 at 95 (55px from 0) -->
<text x="150">4</text>  <!-- 4 at 150 (55px from 2) -->
```

---

## PPTX Layer System

Each SVG element that should be independently selectable needs `data-pptx-layer`:

| Prefix | Use For | Example |
|--------|---------|---------|
| `line-N` | Data lines and their points | `line-1`, `line-2` |
| `label-X` | Text annotations | `label-b0`, `label-shift20` |
| `arrow-X` | Arrow annotations | `arrow-shift`, `arrow-highlight` |
| `eq-N` | Equation labels | `eq-line-1`, `eq-line-2` |

See `card-patterns/complex-patterns/graph-snippet.html` for the complete layer structure implementation.

---

## Printable Worksheet SVG

For printable slides, use smaller dimensions and monochrome colors. See `card-patterns/complex-patterns/printable-slide-snippet.html` for complete example.

**Key differences from projection SVG:**
- Smaller viewBox (200x150 vs 280x200)
- Black on white colors only
- No arrows/animation

---

## Colors Reference

| Use | Color | Hex |
|-----|-------|-----|
| Line 1 | Blue | #60a5fa |
| Line 2 | Green | #22c55e |
| Line 3 | Red | #ef4444 |
| Axis/Grid | Slate | #1e293b |
| Labels | Gray | #64748b |
| Light grid | Slate | #e2e8f0 |
