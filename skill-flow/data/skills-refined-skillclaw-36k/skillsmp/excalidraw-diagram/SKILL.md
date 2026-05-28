---
name: excalidraw-diagram
description: Create an Excalidraw diagram from a text description. Use when the user wants to create a diagram, flowchart, architecture diagram, or visual explanation for their blog post.
---

# Create Excalidraw Diagram

Generate an Excalidraw diagram from a text description that the user can import into Excalidraw.

## Instructions

1. **Understand what the user wants to visualize**:
   - Ask clarifying questions if needed
   - Identify the type of diagram (flowchart, architecture, comparison, timeline, etc.)
   - Note key elements, relationships, and groupings

2. **Generate Excalidraw JSON**:
   - Create valid Excalidraw JSON format
   - Use appropriate shapes (rectangles, arrows, text, etc.)
   - Apply sensible positioning and sizing
   - Use colors that work well together

3. **Provide the output**:
   - Save the JSON to a `.excalidraw` file in a sensible location
   - Give instructions on how to use it

## Excalidraw JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "rectangle",
      "id": "unique-id",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 60,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roundness": { "type": 3 },
      "seed": 12345
    },
    {
      "type": "text",
      "id": "unique-id-2",
      "x": 120,
      "y": 120,
      "text": "Label",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center"
    },
    {
      "type": "arrow",
      "id": "unique-id-3",
      "x": 300,
      "y": 130,
      "width": 100,
      "height": 0,
      "points": [[0, 0], [100, 0]]
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

## Color Palette (Hand-drawn friendly)

Use these Excalidraw default colors:

| Purpose | Color Code | Name |
|---------|------------|------|
| Safe/Good | `#b2f2bb` | Light green |
| Warning/Caution | `#ffec99` | Light yellow |
| Danger/Avoid | `#ffc9c9` | Light red |
| Info/Neutral | `#a5d8ff` | Light blue |
| Highlight | `#d0bfff` | Light purple |
| Stroke | `#1e1e1e` | Dark gray |

## Common Element Types

- `rectangle` - Boxes, containers
- `ellipse` - Circles, ovals
- `diamond` - Decision points
- `arrow` - Connections, flow
- `line` - Simple connections
- `text` - Labels, descriptions
- `freedraw` - Hand-drawn elements

## Output

1. **Save the file** to `assets/excalidraw/[descriptive-name].excalidraw`

2. **Tell the user** how to open and export:
```
To use this diagram:
1. Go to https://excalidraw.com
2. Click the menu (hamburger icon) → Open
3. Select the .excalidraw file
4. Edit as needed, then export as PNG/SVG to assets/images/
```

## Example

User: "Create a diagram showing the three port ranges"

Output: An Excalidraw file with:
- Three colored rectangles (green for safe range, yellow for system, red for ephemeral)
- Labels for each range (0-1023, 1024-49151, 49152-65535)
- Text descriptions below each
- Arrow pointing to the recommended range
