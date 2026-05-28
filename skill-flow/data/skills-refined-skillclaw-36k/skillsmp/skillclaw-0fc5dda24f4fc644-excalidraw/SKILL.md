---
name: excalidraw
description: Use this skill when you want to generate hand-drawn style diagrams (architecture, flowcharts, system design) in Excalidraw JSON format.
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

6. **Container binding (MUST follow)**: When connecting to grouped/nested structures, arrows must bind to the outer container (background region), NOT to internal elements:
   - If a phase/subgraph contains multiple internal steps, arrows from outside should connect to the container box.
   - Internal element connections stay internal; external connections go to the container.

7. **Sibling layout (MUST follow)**: Elements at the same hierarchy level must be placed horizontally (same row), NOT vertically:
   - Siblings represent parallel/alternative paths (e.g., TCP and HTTP handlers).
   - Vertical stacking implies sequential execution, which is semantically wrong for siblings.

8. **Nested structure clarity (MUST follow)**: When a container has internal elements, ensure clear hierarchy and no overlaps.