# Graph Planning (Required for Coordinate Planes)

**When to read this file:** You identified "SVG graphs" or "coordinate planes" as your visual type in Step 1.3e.

**Purpose:** Complete semantic planning for your graph BEFORE any pixel-level implementation.

---

## MANDATORY: Complete All Steps Below

If you skip this planning, your graph will have incorrect scales or misplaced annotations.

---

## Step 1: List Your Equations/Data

Write out every line or data series that will appear on the graph:

```
Line 1: [equation, e.g., y = 3x]
Line 2: [equation, e.g., y = 3x + 50]
Line 3: [if applicable]
```

---

## Step 2: Calculate Data Ranges

### Find X_MAX
Choose the rightmost x-value you need to show. Common values: 4, 5, 6, 8, 10

```
X_MAX = [your value]
```

### Find Y_MAX
For EACH line, calculate Y at x=0 and x=X_MAX:

```
Line 1: y = [equation]
  - At x=0: y = [calculate]
  - At x=X_MAX: y = [calculate]

Line 2: y = [equation]
  - At x=0: y = [calculate]
  - At x=X_MAX: y = [calculate]

Largest Y value across all lines: [value]
```

### Round Y_MAX Up

**Choose the smallest Y_MAX that fits your data AND keeps ticks ≤10.**

| If largest Y is... | Use Y_MAX | Increment | Ticks |
|-------------------|-----------|-----------|-------|
| ≤ 6 | 6 | 1 | 7 |
| 7-8 | 8 | 1 | 9 |
| 9 | 9 | 1 | 10 |
| 10-16 | 16 | 2 | 9 |
| 17-18 | 18 | 2 | 10 |
| 19-36 | 36 | 4 | 10 |
| 37-45 | 45 | 5 | 10 |
| 46-72 | 72 | 8 | 10 |
| 73-90 | 90 | 10 | 10 |
| 91-180 | 180 | 20 | 10 |

**Note:** These Y_MAX values are chosen to give exactly 9-10 ticks with clean increments.

```
Y_MAX = [your rounded value]
```

---

## Step 3: Determine Axis Labels and Scales

### X-Axis Labels

Based on your X_MAX, use these labels:

| X_MAX | X-axis labels | X scale (increment) |
|-------|---------------|---------------------|
| 4 | 0, 1, 2, 3, 4 | 1 |
| 5 | 0, 1, 2, 3, 4, 5 | 1 |
| 6 | 0, 1, 2, 3, 4, 5, 6 | 1 |
| 8 | 0, 2, 4, 6, 8 | 2 |
| 10 | 0, 2, 4, 6, 8, 10 | 2 |
| 12 | 0, 3, 6, 9, 12 | 3 |
| 20 | 0, 5, 10, 15, 20 | 5 |

```
X-axis labels: [your labels]
X scale: [increment between labels]
```

### Y-Axis Labels

**⚠️ Y-axis labels MUST start at 0.** Don't start at the first increment (e.g., `10, 20, 30...` is WRONG; `0, 10, 20, 30...` is CORRECT).

Based on your Y_MAX, use these labels. **Target: ≤10 ticks** (never exceed 10).

**Priority:** Use smallest whole-number increment possible. Count by 1s or 2s when Y_MAX allows.

**If you need more than 10 ticks, reduce Y_MAX slightly** to hit exactly 9-10 ticks.

| Y_MAX | Y-axis labels (bottom to top) | Y scale (increment) | Ticks |
|-------|------------------------------|---------------------|-------|
| 6 | 0, 1, 2, 3, 4, 5, 6 | 1 | 7 |
| 8 | 0, 1, 2, 3, 4, 5, 6, 7, 8 | 1 | 9 |
| 9 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 | 1 | 10 |
| 16 | 0, 2, 4, 6, 8, 10, 12, 14, 16 | 2 | 9 |
| 18 | 0, 2, 4, 6, 8, 10, 12, 14, 16, 18 | 2 | 10 |
| 36 | 0, 4, 8, 12, 16, 20, 24, 28, 32, 36 | 4 | 10 |
| 45 | 0, 5, 10, 15, 20, 25, 30, 35, 40, 45 | 5 | 10 |
| 72 | 0, 8, 16, 24, 32, 40, 48, 56, 64, 72 | 8 | 10 |
| 90 | 0, 10, 20, 30, 40, 50, 60, 70, 80, 90 | 10 | 10 |
| 180 | 0, 20, 40, 60, 80, 100, 120, 140, 160, 180 | 20 | 10 |

**Formula:** For increment I, max Y_MAX = I × 9 (to get 10 ticks including 0)

| Increment | Max Y_MAX for 10 ticks |
|-----------|------------------------|
| 1 | 9 |
| 2 | 18 |
| 4 | 36 |
| 5 | 45 |
| 8 | 72 |
| 10 | 90 |
| 20 | 180 |

```
Y-axis labels: [your labels]
Y scale: [increment between labels]
```

---

## Step 4: Calculate Line Endpoints (CRITICAL)

**This step ensures mathematically accurate line drawing.**

For each line equation y = mx + b, calculate:
- **Start point**: Where the line enters the plot (usually at x=0, the y-intercept)
- **End point**: Where the line exits the plot (usually at x=X_MAX)

### Formula

```
Start Point: (x=0, y=b)              -- where b is the y-intercept
End Point:   (x=X_MAX, y=m*X_MAX+b)  -- plug X_MAX into the equation
```

### Example Calculations

**Given:** Line 1: y = 5x, Line 2: y = 5x + 20, X_MAX = 8

```
Line 1: y = 5x (slope=5, y-intercept=0)
  - Start point: (0, 0)
  - End point: (8, 5*8 + 0) = (8, 40)

Line 2: y = 5x + 20 (slope=5, y-intercept=20)
  - Start point: (0, 20)
  - End point: (8, 5*8 + 20) = (8, 60)
```

### Edge Cases

If a line exits through the TOP of the plot before reaching X_MAX:
- Calculate where y = Y_MAX: x = (Y_MAX - b) / m
- Use that x value as the end point's x coordinate

```
Example: y = 20x with X_MAX=8, Y_MAX=80
  - At x=8: y = 160 (exceeds Y_MAX=80!)
  - Line exits at top: x = (80 - 0) / 20 = 4
  - End point: (4, 80) instead of (8, 160)
```

### Record Your Line Endpoints

```
Line 1: y = [equation]
  - Start point: ([x], [y])
  - End point: ([x], [y])

Line 2: y = [equation]
  - Start point: ([x], [y])
  - End point: ([x], [y])
```

**⚠️ These values will be used DIRECTLY in the SVG line element as x1, y1, x2, y2 coordinates (after pixel conversion).**

---

## Step 5: Identify the Mathematical Relationship to Annotate

What is the KEY mathematical concept this graph should emphasize?

| If the problem involves... | Annotation type | What to show |
|---------------------------|-----------------|--------------|
| Two parallel lines (same slope, different y-intercepts) | Y-intercept shift | Vertical double-arrow between y-intercepts |
| Two parallel lines | Parallel indicator | "PARALLEL" label or "Same slope = m" |
| Two lines with different slopes | Slope comparison | Slope labels next to each line |
| Lines that intersect | Intersection point | Highlighted point with coordinates |
| Single line with slope focus | Slope triangle | Rise/run annotation |
| Single line with intercept focus | Y-intercept point | Highlighted point at (0, b) |

```
Key relationship: [what to emphasize]
Annotation type: [from table above]
```

---

## Step 5: Plan Annotation Position

### For Y-Intercept Shift (Parallel Lines)

The vertical arrow showing the shift goes **LEFT of the y-axis**:

```
Arrow X position: ORIGIN_X - 15 pixels (left of axis)
Arrow starts at: pixelY of first y-intercept
Arrow ends at: pixelY of second y-intercept
Label: the numerical difference (e.g., "50 units")
```

### For Parallel/Slope Labels

Place in **open space** away from:
- The lines themselves
- Axis labels
- Other annotations

Typical positions:
- Upper right quadrant for legend
- Near the lines but offset by 10-15px

### For Intersection Points

Highlight the intersection with:
- A larger circle (r=6 or r=8)
- Coordinate label offset by 10px

---

## Step 6: Write Your Complete Graph Plan

**Copy this template and fill it in:**

```
GRAPH PLAN
==========
Equations:
- Line 1: [equation] ([color])
- Line 2: [equation] ([color])

Scale:
- X range: 0 to [X_MAX]
- X-axis labels: [list]
- X scale: [increment between labels]
- Y range: 0 to [Y_MAX]
- Y-axis labels: [list]
- Y scale: [increment between labels]

Annotation:
- Relationship to show: [what mathematical concept]
- Annotation type: [from Step 4 table]
- Position: [from Step 5]

Visual notes:
- [any other visual elements needed]
```

---

## Example: Comparing y = 3x and y = 3x + 15

```
GRAPH PLAN
==========
Equations:
- Line 1: y = 3x (blue)
- Line 2: y = 3x + 15 (green)

Scale:
- X range: 0 to 6
- X-axis labels: 0, 1, 2, 3, 4, 5, 6
- X scale: 1
- Calculations:
  - Line 1 at x=6: y = 18
  - Line 2 at x=6: y = 33
  - Largest Y = 33 → use Y_MAX = 36 (from table: 19-36 → 36)
- Y range: 0 to 36
- Y-axis labels: 0, 4, 8, 12, 16, 20, 24, 28, 32, 36
- Y scale: 4 (gives exactly 10 ticks)

Annotation:
- Relationship to show: Y-intercept shift (parallel lines)
- Annotation type: Vertical double-arrow between y-intercepts
- Position: Left of y-axis (x = ORIGIN_X - 15)
- Arrow from: y=0 to y=15
- Label: "+15"

Visual notes:
- Both lines should be clearly visible
- 10 ticks on Y-axis for clear reading
- "PARALLEL" label near the lines
```

---

## Add Graph Plan to Your PROBLEM ANALYSIS

After completing this planning, add the GRAPH PLAN section to your PROBLEM ANALYSIS output in Phase 1.

This plan will be referenced in Phase 3 when you implement the SVG.

---

## Pixel Implementation

When you reach Phase 3 and need to convert your graph plan to actual SVG pixels, reference:

```
Read: .claude/skills/create-worked-example-sg/reference/svg-pixel-tables.md
```

That file contains the pixel lookup tables for converting your planned scale to actual SVG coordinates.
