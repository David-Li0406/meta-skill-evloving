# StackSketch JSON Schema

This document defines the JSON structure used by StackSketch diagrams. Use it to author or edit diagrams that can be rendered by the viewer.

## Root Object

Required fields:
- `version`: string (example: "0.1")
- `name`: string (diagram title)
- `diagram`: object with `type`
- `canvas`: object
- `nodes`: array
- `edges`: array

Optional fields:
- `groups`: array
- `legend`: array
- `data`: object for extra metadata

Example:
```json
{
  "version": "0.1",
  "name": "Quiz Navigation Flow",
  "diagram": { "type": "flow" },
  "canvas": { "width": 1200, "height": 800, "grid": 16, "background": "dots" },
  "nodes": [],
  "edges": [],
  "groups": []
}
```

## Diagram Types

- `flow`: navigation, logic, state machines
- `infra`: infrastructure maps, data flows
- `ui`: device mockups and component layouts

## Node Object

Required fields:
- `id`: string
- `type`: string (shape)
- `position`: `{ "x": number, "y": number }`
- `size`: `{ "width": number, "height": number }`

Common optional fields:
- `label`: string
- `kind`: string (semantic role, especially for infra)
- `icon`: `{ "name": string, "size": number, "color": string }`
- `style`: `{ "fill": string, "stroke": string, "textColor": string, "cornerRadius": number, "lineWidth": number, "fontSize": number, "fontFamily": string, "shadow": string }`
- `data`: object (extra metadata)
- `parentId`: string (nest within another node or group)
- `link`: `{ "type": "diagram" | "url", "target": string }`

Supported `type` values:
- `rect`, `circle`, `diamond`, `pill`
- `device` (UI mockups)
- `component` (UI elements)

Suggested `kind` values for infra:
- `frontend`, `backend`, `database`, `cache`, `queue`, `worker`, `cdn`, `external`, `auth`

### UI Component Payload

When `type` is `component`, include a `component` object:
```json
{
  "component": {
    "type": "button",
    "variant": "primary",
    "state": "default",
    "text": "Start Quiz",
    "action": "StartQuiz"
  }
}
```

Suggested `component.type` values:
- `button`, `card`, `input`, `text`, `progress`, `badge`, `list`, `image`, `navbar`, `statusbar`

### Device Frames

When `type` is `device`, include a `device` object:
```json
{
  "device": {
    "platform": "ios",
    "model": "iphone-14",
    "safeArea": { "top": 47, "bottom": 34, "left": 0, "right": 0 },
    "screen": { "width": 390, "height": 844 }
  }
}
```

## Edge Object

Required fields:
- `id`: string
- `from`: string (node id)
- `to`: string (node id)
- `type`: string

Optional fields:
- `label`: string
- `style`: `{ "stroke": string, "lineWidth": number, "dashed": boolean }`
- `data`: object
- `path`: `{ "type": "straight" | "orthogonal" | "curved" }`

Supported `type` values:
- `arrow`, `line`, `dashed`, `orthogonal`, `curved`

Suggested `data.kind` values for infra edges:
- `http`, `grpc`, `db`, `queue`, `cache`, `auth`, `event`, `storage`

## Group Object

Groups define swimlanes or zones.

Required fields:
- `id`: string
- `label`: string
- `bounds`: `{ "x": number, "y": number, "width": number, "height": number }`

Optional fields:
- `style`: `{ "fill": string, "stroke": string, "cornerRadius": number, "labelColor": string }`
- `data`: object

## Style Defaults

Use these defaults when no explicit style is provided:
- `fill`: "#ffffff"
- `stroke`: "#2b2b2b"
- `textColor`: "#1c1c1c"
- `lineWidth`: 2
- `cornerRadius`: 10
- `fontSize`: 12
- `fontFamily`: "SF Pro Text"

## Formatting Rules

- Use 2-space indentation.
- Keep object keys in a stable order: `id`, `type`, `label`, `position`, `size`, `kind`, `icon`, `style`, `component`, `device`, `data`.
- Preserve unknown fields when editing.
