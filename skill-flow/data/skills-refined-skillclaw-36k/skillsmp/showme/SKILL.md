# ShowMe - Visual Mockup & Annotation Tool for Gemini CLI

ShowMe lets you create visual mockups with coordinate-tracked annotations across multiple pages. Draw, annotate, and provide component-specific feedback that Gemini CLI can see and act on.

## Instructions for Gemini CLI

When the user invokes `/showme`, execute this command and wait for the result:

```bash
bun run ../ai.apps/ShowMe/server/index.ts
```

Run the command through the `powershell` tool (typically `mode:"sync"` with a generous `initial_wait`) so that stdout, stderr, and the resulting JSON are captured in the transcript.

The command will:

1. Open a browser with a multi-page drawing canvas
2. Let the user create pages (blank or from images), draw, and add annotations
3. Output JSON with structured page and annotation data
4. **Images are saved to temp files** (paths provided in `imagePath` field)

---

## Processing the Output

The hook output contains structured JSON with:

```json
{
  "hookSpecificOutput": {
    "decision": { "behavior": "allow" },
    "showme": {
      "pages": [
        {
          "id": "...",
          "name": "Page 1",
          "imagePath": "/tmp/showme-images/page-id.png",
          "width": 1200,
          "height": 800,
          "annotations": [...]
        }
      ],
      "globalNotes": "..."
    }
  }
}
```

### Steps to Process:

1. **Parse the JSON output** - Extract the `showme` object
2. **Read each page image** - Use the `imagePath` field to read the PNG file
3. **Review annotations** - Each has coordinates and user feedback
4. **Address globalNotes** - Overall context or questions from the user
5. **Acknowledge each annotation** - Let the user know you saw their specific feedback

---

## Understanding Annotations

Annotations are coordinate-tracked markers. Each has:

- `number` - Display order (1, 2, 3...) - unique across ALL pages
- `type` - The kind of marker (see below)
- `bounds` - Location on canvas: `{x, y, width, height}`
- `feedback` - User's specific feedback for that component

| Type        | What It Means                  | Bounds Usage                    |
| ----------- | ------------------------------ | ------------------------------- |
| `pin`       | Point marker (numbered circle) | x, y = center point             |
| `area`      | Rectangle selection            | x, y, width, height = full rect |
| `arrow`     | Directional pointer            | bounds covers start-to-end      |
| `highlight` | Freehand highlight stroke      | bounds covers the stroke area   |

**Coordinate System:** (0, 0) is top-left corner. X increases rightward, Y increases downward.

---

## Example Output Processing

Given this output:

```json
{
  "hookSpecificOutput": {
    "decision": { "behavior": "allow" },
    "showme": {
      "pages": [
        {
          "id": "abc123",
          "name": "Login Screen",
          "imagePath": "/tmp/showme-images/abc123.png",
          "width": 800,
          "height": 600,
          "annotations": [
            {
              "id": "ann1",
              "type": "pin",
              "number": 1,
              "bounds": { "x": 452, "y": 128, "width": 28, "height": 28 },
              "feedback": "This button should be blue, not gray"
            }
          ]
        }
      ],
      "globalNotes": "Please fix the login button styling"
    }
  }
}
```

You should:

1. Read the image at `/tmp/showme-images/abc123.png`
2. Note that annotation #1 at (452, 128) says "This button should be blue, not gray"
3. Address the global notes about button styling

---

## User Instructions

### Tools (use toolbar buttons)

**Drawing:** Pen, Rectangle, Circle, Arrow, Text, Eraser

**Annotations:** Pin, Area, Arrow, Highlight

### Page Management

- Click **+** to add blank page or import image
- Click page thumbnail to switch pages
- Each page has its own annotations and undo history

### Zoom & Pan

- **Ctrl + Wheel** - Zoom with mouse wheel
- **Space + Drag** - Pan canvas
- Toolbar buttons: Zoom in, Zoom out, Fit, Reset

### Keyboard Shortcuts

- **Ctrl+V** - Paste screenshot
- **Ctrl+Z** - Undo
- **Ctrl+Y** - Redo
- **Delete** - Remove selected annotation
- **Escape** - Deselect / close popover

### Workflow

1. Create pages (blank or from imported images/screenshots)
2. Draw your mockup using drawing tools
3. Switch to annotation mode and add markers
4. Click annotations to add component-specific feedback
5. Add global notes at the bottom for overall context
6. Click "Send to Gemini" when done

---

Built with love by **Yaron - No Fluff** | [YouTube](https://www.youtube.com/channel/UCuCwMz8aMJBFfhDnYicfdjg/)