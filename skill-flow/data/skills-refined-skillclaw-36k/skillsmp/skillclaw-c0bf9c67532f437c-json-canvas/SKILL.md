---
name: json-canvas
description: Use this skill when creating and editing JSON Canvas files (.canvas) for visual canvases, mind maps, or flowcharts in Obsidian and other applications.
---

# JSON Canvas Skill

This skill enables agents to create and edit valid JSON Canvas files (`.canvas`) used in Obsidian and other applications.

## Overview

JSON Canvas is an open file format for infinite canvas data. Canvas files use the `.canvas` extension and contain valid JSON following the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/).

## File Structure

A canvas file contains two top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (optional): Array of node objects.
- `edges` (optional): Array of edge objects connecting nodes.

## Nodes

Nodes are objects placed on the canvas. There are four node types:
- `text`: Text content with Markdown.
- `file`: Reference to files/attachments.
- `link`: External URL.
- `group`: Visual container for other nodes.

### Z-Index Ordering

Nodes are ordered by z-index in the array:
- First node = bottom layer (displayed below others).
- Last node = top layer (displayed above others).

### Generic Node Attributes

All nodes share these attributes:

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `id` | Yes | string | Unique identifier for the node. |
| `type` | Yes | string | Node type: `text`, `file`, `link`, or `group`. |
| `x` | Yes | integer | X position in pixels. |
| `y` | Yes | integer | Y position in pixels. |
| `width` | Yes | integer | Width in pixels. |
| `height` | Yes | integer | Height in pixels. |
| `color` | No | canvasColor | Node color (see Color section). |

### Text Nodes

Text nodes contain Markdown content.

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `text` | Yes | string | Plain text with Markdown syntax. |

### File Nodes

File nodes reference files or attachments (images, videos, PDFs, notes, etc.).

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Attachments/diagram.png"
}
```