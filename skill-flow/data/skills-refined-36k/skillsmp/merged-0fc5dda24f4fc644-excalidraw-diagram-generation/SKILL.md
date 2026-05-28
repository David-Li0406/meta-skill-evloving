---
name: excalidraw-diagram-generation
description: Use this skill to generate hand-drawn style diagrams (architecture, flowcharts, system design) in Excalidraw JSON format when the user requests diagrams or mentions Excalidraw.
---

# Excalidraw Diagram Generation

Generate professional hand-drawn style diagrams in Excalidraw JSON format.

## Critical Rules

1. **Arrow Binding (MUST follow)**: Arrows must bind to components bidirectionally:
   - Arrow needs `startBinding` and `endBinding` pointing to component IDs.
   - Rectangle needs `boundElements` array listing bound arrow IDs.
   - Without both, arrows won't snap to components.

2. **Text requires width/height**: Text elements must have `width` and `height` fields; otherwise, they won't render.

3. **Arrow labels**: Place below arrow (y + 30) or above (y - 30), never overlapping components.

4. **Background region sizing (MUST follow)**: Background regions (subgraphs/phases) must fully cover all contained elements:
   - Calculate bounding box: find min/max x/y of ALL elements in the region.
   - Add padding: 40px on all sides.
   - Formula: `width = (maxX + maxWidth) - minX + 80`, `height = (maxY + maxHeight) - minY + 80`.
   - Verify: every child element's bottom-right corner must be inside the region.

5. **No overlaps (MUST follow)**: Arrows must not cross unrelated components; labels must not overlap components.

6. **Container binding (MUST follow)**: When connecting to grouped/nested structures, arrows must bind to the outer container (background region), NOT to internal elements.

7. **Sibling layout (MUST follow)**: Elements at the same hierarchy level must be placed horizontally (same row), NOT vertically.

8. **Nested structure clarity (MUST follow)**: When a container has internal elements, ensure clear hierarchy and no overlaps.

9. **Arrow path space reservation (MUST follow)**: When arrows connect nested containers, ensure sufficient space for arrow routing.

## Mandatory Workflow (MUST follow before writing JSON)

**Step 1: Arrow Path Analysis**
Before placing any component, list ALL arrows and their source→target pairs:
```
Arrow 1: A → B (horizontal)
Arrow 2: B → C (horizontal)
Arrow 3: C → A (return arrow - DANGER: will cross B if horizontal layout)
```

**Step 2: Identify Crossing Risks**
For each arrow, check: "Does a straight line from source to target pass through any other component?"
- If YES → mark as "needs layout adjustment" or "needs bypass path".

**Step 3: Choose Layout Strategy**
Based on crossing risks, select appropriate layout:
- **No crossings**: Use simple horizontal/vertical layout.
- **1-2 crossings**: Use bypass paths (multi-point arrows).
- **3+ crossings or complex flows**: Restructure to 2D layout (grid, triangle, diamond).

**Step 4: Verify Before Finalizing**
After generating JSON, mentally trace each arrow path and confirm:
- [ ] No arrow passes through any component it doesn't connect to.
- [ ] No label overlaps any component.
- [ ] All background regions fully contain their elements.

## Core Elements

### Base Template
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

### Element Templates

**Rectangle (Component Box)**
```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 140, "height": 60,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "roundness": { "type": 3 },
  "boundElements": [{"id": "arrow-id", "type": "arrow"}]
}
```

**Text** (width/height required, fontFamily: 4 required)
```json
{
  "id": "unique-id",
  "type": "text",
  "x": 120, "y": 120,
  "width": 80, "height": 24,
  "text": "Label",
  "fontSize": 16,
  "fontFamily": 4,
  "textAlign": "center"
}
```

**Arrow**
```json
{
  "id": "unique-id",
  "type": "arrow",
  "x": 240, "y": 130,
  "points": [[0, 0], [100, 0]],
  "startBinding": { "elementId": "source-id", "focus": 0, "gap": 5 },
  "endBinding": { "elementId": "target-id", "focus": 0, "gap": 5 },
  "endArrowhead": "arrow"
}
```

### Default Values (can be omitted)
```json
"fillStyle": "solid", "strokeWidth": 2, "roughness": 1,
"opacity": 100, "angle": 0, "seed": 1, "version": 1
```

## Color System

| Purpose | Background | Stroke |
|---------|------------|--------|
| Primary / Phase 1 | `#a5d8ff` | `#1971c2` |
| Secondary / Phase 2 | `#b2f2bb` | `#2f9e44` |
| Accent / Shared | `#fff3bf` | `#e67700` |
| Storage / State | `#d0bfff` | `#7048e8` |

## Layout Rules

- Align coordinates to multiples of 20.
- Component spacing: 100-150px.
- Standard component size: `140×60`.
- Background regions: `opacity: 30`.
- Render order: earlier elements in array appear behind.

## Common Diagram Patterns

### Sequence Diagram Layout
For sequence diagrams (multiple participants with message flows):
- Place participants horizontally at top (y = 100).
- Each phase/stage gets its own vertical section below.
- Use background regions to separate phases.

## Complete Example

**Flow with Return Arrow (using bypass path)**
A → B → C, then C → A (return arrow routes above to avoid crossing B).

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {"id": "a", "type": "rectangle", "x": 100, "y": 150, "width": 140, "height": 60, "backgroundColor": "#a5d8ff", "strokeColor": "#1971c2", "roundness": {"type": 3}},
    {"id": "b", "type": "rectangle", "x": 340, "y": 150, "width": 140, "height": 60, "backgroundColor": "#b2f2bb", "strokeColor": "#2f9e44", "roundness": {"type": 3}},
    {"id": "c", "type": "rectangle", "x": 580, "y": 150, "width": 140, "height": 60, "backgroundColor": "#d0bfff", "strokeColor": "#7048e8", "roundness": {"type": 3}},
    {"id": "arr1", "type": "arrow", "x": 245, "y": 180, "points": [[0, 0], [90, 0]], "endArrowhead": "arrow"},
    {"id": "arr2", "type": "arrow", "x": 485, "y": 180, "points": [[0, 0], [90, 0]], "endArrowhead": "arrow"},
    {"id": "arr3", "type": "arrow", "x": 650, "y": 145, "points": [[0, 0], [0, -60], [-480, -60], [-480, 0]], "endArrowhead": "arrow"}
  ],
  "appState": {"viewBackgroundColor": "#ffffff"},
  "files": {}
}
```

## Output

- Filename: `{descriptive-name}.excalidraw.json`
- Location: project root or `docs/` folder.
- Tell user: drag into https://excalidraw.com or open with VS Code Excalidraw extension.

## Notes

- IDs must be unique across the file.
- `fontFamily`: 1=Virgil, 2=Helvetica, 3=Cascadia, 4=Comic Shanns (MUST use for hand-drawn style).
- `strokeWidth` usage in software diagrams:
  - `1` (thin): background regions, container borders, secondary connections.
  - `2` (normal/default): primary components, main flow arrows.
  - `4` (bold): emphasis, critical paths, highlighted elements.
- Dashed arrows: add `"strokeStyle": "dashed"`.