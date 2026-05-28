---
name: geometry-microsim
description: Refactoring patterns and best practices for creating maintainable geometry MicroSims using p5.js. Provides guidelines for local coordinate systems, push/pop/translate/scale patterns, mathematical accuracy, and clean code structure.
---

# Geometry MicroSim Refactoring Patterns

## Overview

This skill provides best practices for creating and refactoring geometry MicroSims in p5.js. These patterns make code more maintainable, mathematically accurate, and easier to debug.

## When to Use This Skill

Use this skill when:
- Creating new geometry MicroSims with multiple shapes or drawing regions
- Refactoring existing geometry code that has complex manual positioning
- Debugging geometry visualizations with incorrect labels or positioning
- Building MicroSims with shapes that need to be scaled, rotated, or transformed

## File Naming Convention

**ALWAYS use `main.html` as the HTML filename for all MicroSims.** This ensures consistent iframe embedding across the project.

### Standard Directory Structure

Each MicroSim should have this structure:

```
docs/sims/[sim-name]/
├── main.html           # REQUIRED: The HTML file (always named main.html)
├── [sim-name].js       # JavaScript file with p5.js code
├── index.md            # Documentation page
├── [sim-name].png      # Screenshot/preview image
└── metadata.json       # Optional: MicroSim metadata
```

### Live Server Preview URL

After creating or modifying a MicroSim, use this URL pattern for Live Server preview:

```
http://127.0.0.1:5500/docs/sims/[sim-name]/main.html
```

### Iframe Embedding

Always use `main.html` in iframe references:

```html
<iframe src="main.html" width="100%" height="450px" scrolling="no"></iframe>
```

For external embedding:

```html
<iframe src="https://dmccreary.github.io/geometry-course/sims/[sim-name]/main.html" width="100%" height="450px" scrolling="no"></iframe>
```

## Core Principle: Local Coordinate Systems

**Always draw geometric shapes in local coordinates centered at the origin, then use transformations to position them.**

### The Push/Pop/Translate/Scale Pattern

Instead of calculating global positions for every vertex, use this pattern:

```javascript
function drawShape(centerX, centerY, scaleFactor) {
  push();
  translate(centerX, centerY);
  scale(scaleFactor);

  // Draw shape at origin in local coordinates
  // All coordinates are relative to (0, 0)
  triangle(verts.A.x, verts.A.y, verts.B.x, verts.B.y, verts.C.x, verts.C.y);

  // Draw labels, angle arcs, etc. in same local system
  drawAngleLabels(verts);
  drawVertexLabels(verts);

  pop();
}
```

### Benefits of This Approach

1. **Separation of concerns**: Geometry calculation is separate from positioning
2. **Easier debugging**: Shapes work correctly at origin before positioning
3. **Reusability**: Same shape function works at any position/scale
4. **Cleaner code**: No scattered offset calculations throughout code
5. **Accurate labels**: Labels stay associated with correct vertices through transforms

## Scale Factor Compensation

When scaling, compensate for stroke weights and text sizes:

```javascript
push();
translate(centerX, centerY);
scale(scaleFactor);

// Compensate stroke weight so it appears consistent
strokeWeight(2 / scaleFactor);

// Compensate text size
textSize(12 / scaleFactor);

// Draw geometry...
pop();
```

## Geometry Calculation Best Practices

### Separate Vertex Calculation from Rendering

Create a function that calculates vertices in normalized coordinates:

```javascript
// Calculate triangle vertices from angles using law of sines
// Returns vertices in local coordinates centered at origin
function calculateTriangleVertices(angles, baseLength) {
  let angleA = radians(angles[0]);
  let angleB = radians(angles[1]);
  let angleC = radians(angles[2]);

  // Using law of sines: a/sin(A) = b/sin(B) = c/sin(C)
  let sideC = baseLength;
  let k = sideC / sin(angleC);
  let sideA = k * sin(angleA);
  let sideB = k * sin(angleB);

  // Place vertices, then center at origin
  let Cx = 0, Cy = 0;
  let Bx = sideA, By = 0;
  let Ax = sideB * cos(angleC);
  let Ay = -sideB * sin(angleC);

  // Center the triangle at origin
  let centX = (Ax + Bx + Cx) / 3;
  let centY = (Ay + By + Cy) / 3;

  return {
    A: { x: Ax - centX, y: Ay - centY },
    B: { x: Bx - centX, y: By - centY },
    C: { x: Cx - centX, y: Cy - centY }
  };
}
```

### Calculate Bounding Box for Auto-Scaling

```javascript
function drawShapePanel(centerX, centerY, panelWidth, panelHeight) {
  let verts = calculateVertices();

  // Calculate bounding box
  let minX = min(verts.A.x, verts.B.x, verts.C.x);
  let maxX = max(verts.A.x, verts.B.x, verts.C.x);
  let minY = min(verts.A.y, verts.B.y, verts.C.y);
  let maxY = max(verts.A.y, verts.B.y, verts.C.y);
  let shapeWidth = maxX - minX;
  let shapeHeight = maxY - minY;

  // Scale to fit panel with padding
  let scaleX = (panelWidth - 40) / shapeWidth;
  let scaleY = (panelHeight - 40) / shapeHeight;
  let scaleFactor = min(scaleX, scaleY) * 0.85;

  push();
  translate(centerX, centerY);
  scale(scaleFactor);
  // Draw...
  pop();
}
```

## Label Positioning

### Vertex Labels

Position labels radially outward from centroid:

```javascript
function drawVertexLabels(verts, scaleFactor) {
  let centX = (verts.A.x + verts.B.x + verts.C.x) / 3;
  let centY = (verts.A.y + verts.B.y + verts.C.y) / 3;

  let labelDist = 16 / scaleFactor;

  // For each vertex, push label away from centroid
  let dirX = verts.A.x - centX;
  let dirY = verts.A.y - centY;
  let len = sqrt(dirX * dirX + dirY * dirY);

  text('A', verts.A.x + labelDist * dirX / len,
           verts.A.y + labelDist * dirY / len);
}
```

### Angle Labels

Position angle measurements along the angle bisector:

```javascript
function drawAngleLabel(vertex, adj1, adj2, angleDeg, scaleFactor) {
  let a1 = atan2(adj1.y - vertex.y, adj1.x - vertex.x);
  let a2 = atan2(adj2.y - vertex.y, adj2.x - vertex.x);

  // Normalize and find midpoint angle
  // ... angle normalization code ...

  let midAngle = (a1 + a2) / 2;
  let labelDist = 35 / scaleFactor;

  let labelX = vertex.x + labelDist * cos(midAngle);
  let labelY = vertex.y + labelDist * sin(midAngle);
  text(angleDeg + "°", labelX, labelY);
}
```

## Common Patterns

### Multiple Panels with Shapes

When displaying multiple shapes in panels (like triangle classifications):

```javascript
function drawPanels() {
  let panelWidth = (canvasWidth - 80) / 3;
  let startX = 30;

  for (let i = 0; i < 3; i++) {
    let x = startX + i * (panelWidth + 10);
    let centerX = x + panelWidth / 2;
    let centerY = panelY + 130;

    // Each shape draws in its own coordinate system
    drawShapePanel(centerX, centerY, shapes[i], panelWidth);
  }
}
```

### Right Angle Indicators

```javascript
function drawRightAngle(vertex, adj1, adj2, scaleFactor) {
  let size = 12 / scaleFactor;
  let dir1 = atan2(adj1.y - vertex.y, adj1.x - vertex.x);
  let dir2 = atan2(adj2.y - vertex.y, adj2.x - vertex.x);

  let p1 = { x: vertex.x + size * cos(dir1), y: vertex.y + size * sin(dir1) };
  let p2 = { x: vertex.x + size * cos(dir2), y: vertex.y + size * sin(dir2) };
  let corner = {
    x: vertex.x + size * cos(dir1) + size * cos(dir2),
    y: vertex.y + size * sin(dir1) + size * sin(dir2)
  };

  line(p1.x, p1.y, corner.x, corner.y);
  line(p2.x, p2.y, corner.x, corner.y);
}
```

## Checklist for Geometry MicroSims

Before finalizing a geometry MicroSim, verify:

### File Structure
- [ ] HTML file is named `main.html`
- [ ] Directory follows `docs/sims/[sim-name]/` pattern
- [ ] index.md uses `main.html` in iframe src
- [ ] Screenshot image exists for preview

### Geometry Code Quality
- [ ] Shapes draw in local coordinates (centered at origin)
- [ ] Push/pop/translate/scale used for positioning
- [ ] Stroke weights compensated for scale factor
- [ ] Text sizes compensated for scale factor
- [ ] Vertex labels positioned radially from centroid
- [ ] Angle measurements match the actual drawn angles
- [ ] Geometry calculations use mathematically correct formulas
- [ ] Labels stay associated with correct elements through transforms
- [ ] Bounding box calculated for auto-fit scaling

## Anti-Patterns to Avoid

### Manual Offset Calculations

**Bad:**
```javascript
// Scattered offsets throughout code
let ax = cx - baseLen / 2 + offsetX + panelX;
let ay = cy + verticalOffset + panelY - 10;
```

**Good:**
```javascript
// Clean local coordinates with transform
push();
translate(panelCenterX, panelCenterY);
let ax = -baseLen / 2;
let ay = 0;
// ...
pop();
```

### Rotation Breaking Label Associations

**Bad:**
```javascript
// Rotate vertices but keep same angle labels
rotateVertices();
drawAngle(verts.A, angleA);  // angleA no longer at vertex A!
```

**Good:**
```javascript
// Calculate vertices directly from angles
let verts = calculateFromAngles(angles);
// verts.A always has angles[0]
```

## Mathematical Accuracy

For geometry education, mathematical accuracy is critical:

1. **Use law of sines/cosines** for triangle calculations
2. **Verify angle sums** (triangle: 180°, quadrilateral: 360°)
3. **Test with known values** (30-60-90, 45-45-90 triangles)
4. **Display angles that match** the actual geometric shape

## Related Skills

- `microsim-generator/references/p5-guide.md` - General p5.js MicroSim patterns
- `microsim-utils` - Quality validation and standardization

## Examples

See these MicroSims for implementation examples:
- `docs/sims/triangle-classification-angles/` - Triangle types by angles
- `docs/sims/triangle-classification-sides/` - Triangle types by sides (if exists)
- Other geometry sims in `docs/sims/`
