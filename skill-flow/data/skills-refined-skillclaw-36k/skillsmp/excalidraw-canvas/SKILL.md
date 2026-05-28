---
name: excalidraw_canvas
description: Advanced Visual Drawing Skill for Antigravity Agents.
version: 1.0.0
author: Antigravity
---

# Operational Instructions: Excalidraw Canvas 🎨

## Overview
This skill allows the agent to create and manipulate visual diagrams on the Excalidraw canvas (Port 3000). It acts as a visual reasoning tool for architecture, flows, and planning.

## Triggers
- When the user asks to "Draw", "Visualize", or "Diagram" a concept.
- When explaining complex architectural changes (Architecture Gate).
- When converting Mermaid documentation to a high-fidelity visual format.

## ⚠️ Prerequisites (External Dependency)

> [!IMPORTANT]
> This skill requires the **mcp_excalidraw** server, which is NOT bundled with Antigravity.
> You must install it separately before using this skill.

### Option A: Local Installation
```bash
# Clone the MCP server
git clone https://github.com/yctimlin/mcp_excalidraw ~/mcp_excalidraw
cd ~/mcp_excalidraw && npm install && npm run build

# Set environment variable (add to ~/.bashrc or ~/.zshrc)
export EXCALIDRAW_MCP_PATH="$HOME/mcp_excalidraw/dist/index.js"

# Start Canvas Server (keep running in separate terminal)
npm run canvas  # Opens http://localhost:3000
```

### Option B: Docker Installation (Recommended for Production)
```bash
# Pull and run Canvas Server
docker pull ghcr.io/yctimlin/mcp_excalidraw-canvas:latest
docker run -d -p 3000:3000 --name mcp-canvas ghcr.io/yctimlin/mcp_excalidraw-canvas:latest

# For MCP server in Docker, add to your IDE's MCP config:
# { "command": "docker", "args": ["run", "-i", "--rm", "--network", "host", 
#   "-e", "EXPRESS_SERVER_URL=http://localhost:3000", "ghcr.io/yctimlin/mcp_excalidraw:latest"] }
```

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `EXCALIDRAW_MCP_PATH` | `~/mcp_excalidraw/dist/index.js` | Path to MCP server entry point |
| `EXPRESS_SERVER_URL` | `http://localhost:3000` | Canvas server URL |


## Zenith V5 Upgrade (Empirically Validated) 💎🔬
This skill has been battle-tested with empirical validation to ensure maximum visual impact.

### Critical Visual Parameters (TESTED)
**Arrow Rendering:**
- ✅ **strokeWidth: 2** (Confirmed visible in Excalidraw UI)
- ✅ **Vivid Palette** (High saturation colors for white backgrounds):
  - `node_agent`: #f77f00 (Vivid Orange)
  - `node_tool`: #118ab2 (Ocean Blue)
  - `node_data`: #06d6a0 (Aqua Green)
  - `node_audit`: #e63946 (Vivid Red)
- ✅ **opacity: 100** (Not 1.0 - Excalidraw uses 0-100 scale)
- ✅ **roughness: 0** (Sharp, professional lines)

**Legend & Text:**
- ✅ **fontSize: 18** for headers (readable)
- ✅ **Simplified Text**: Use "LEGEND" not long descriptive strings
- ✅ **No fontFamily Override**: Let Excalidraw use defaults to avoid validation errors

### Empirical Testing Methodology
When uncertain about visual parameters, create a test script:
1. Generate 5+ variants of the element with different parameters
2. Use vivid, contrasting colors (#e63946, #f77f00, #fcbf49, #06d6a0, #118ab2)
3. Label each variant clearly
4. Ask user for visual confirmation of which is visible
5. Apply confirmed parameters to production code

**Example Test** (see `verifiche_test/test_arrow_rendering.py`):
```python
widths = [1, 2, 4, 8, 16]
colors = ["#e63946", "#f77f00", "#fcbf49", "#06d6a0", "#118ab2"]
# Render all, user confirms which is visible
```

### Advanced Features

## Steps
1. **Analyze Demand**: Understand the diagram type (Flowchart, ERD, System Arch).
2. **Define Elements**: Create a list of elements (rectangles, text, arrows).
3. **Invoke Bridge**: Use the `mcp_bridge.py` script to call `create_element` or `batch_create_elements`.
4. **Iterative Refinement**: If the user provides feedback, use `update_element` or `delete_element`.

## Tool Usage (via Bridge)
```python
# Create a Rectangle
python3 .agent/skills/excalidraw_canvas/scripts/mcp_bridge.py create_element '{
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 150,
    "height": 100,
    "backgroundColor": "#f1faee",
    "strokeColor": "#e63946"
}'

# Create a Text element
python3 .agent/skills/excalidraw_canvas/scripts/mcp_bridge.py create_element '{
    "type": "text",
    "x": 110,
    "y": 140,
    "text": "Antigravity Node",
    "fontSize": 20
}'

# Create an Arrow
python3 .agent/skills/excalidraw_canvas/scripts/mcp_bridge.py create_element '{
    "type": "arrow",
    "x": 100,
    "y": 100,
    "points": [[0, 0], [100, 50]],
    "strokeColor": "#e63946",
    "endArrowhead": "arrow"
}'

### Geometric Rules for Arrows
- **Base Coordinate (x, y)**: The starting point of the arrow.
- **Points Array**: An array of relative offsets from (x, y). 
- **Format**: MUST be an array of tuples `[[0,0], [dx, dy]]`.
- **Logic**: Target coordinate = `(x + dx, y + dy)`.
- **Horizontal**: `[[0,0], [dx, 0]]`
- **Vertical**: `[[0,0], [0, dy]]`

## Advanced: Mermaid Conversion
To convert a Mermaid snippet:
```bash
python3 .agent/skills/excalidraw_canvas/scripts/mcp_bridge.py create_from_mermaid '{"mermaid": "graph TD; A-->B"}'
```

## Special Bridge Commands
The Python bridge includes helper functions for scene management:
- **Clear Canvas**: `python3 .agent/skills/excalidraw_canvas/scripts/mcp_bridge.py clear_canvas`
- **Get Elements**: `python3 .agent/skills/excalidraw_canvas/scripts/mcp_bridge.py get_elements`

## Operational Workflow (V3)
1. **Always Clear**: Before starting a major new architecture diagram, run `clear_canvas`. This is now atomic.
2. **Geometric Arrows**: Always use the `create_arrow` helper or follow the relative offset formula: `Points[1] = (TargetX - StartX, TargetY - StartY)`.
3. **Build First**: If the UI returns 404, run `npm run build` in `~/mcp_excalidraw`.
4. **Z-Order**: Place background grouping rectangles first, then components, then labels.

## Examples & Templates
Pre-configured JSON payloads are available in the `examples/` directory for common architectural patterns:
- `examples/connected_components.json`: Simple node-link structure.
- `examples/insight_labeling.json`: Labeling and pointing to existing elements.
- `examples/vivid_infrastructure.json`: High-contrast vivid palette demo.
