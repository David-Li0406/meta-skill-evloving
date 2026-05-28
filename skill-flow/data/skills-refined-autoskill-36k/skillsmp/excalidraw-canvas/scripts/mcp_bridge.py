import json
import subprocess
import os
import sys
import uuid

# --- GLOBAL STYLES ---
STYLES = {
    "node_agent": {"backgroundColor": "#1d3557", "strokeColor": "#f1faee", "strokeWidth": 2},
    "node_tool": {"backgroundColor": "#457b9d", "strokeColor": "#f1faee", "strokeWidth": 1},
    "node_data": {"backgroundColor": "#a8dadc", "strokeColor": "#1d3557", "strokeWidth": 1},
    "node_audit": {"backgroundColor": "#e63946", "strokeColor": "#f1faee", "strokeWidth": 1, "strokeStyle": "dashed"},
}

def execute_mcp_command(tool_name, arguments):
    """
    Bridge script to call the external mcp_excalidraw server.
    
    Environment Variables:
        EXCALIDRAW_MCP_PATH: Path to mcp_excalidraw/dist/index.js
                             Default: ~/mcp_excalidraw/dist/index.js
        EXPRESS_SERVER_URL:  Canvas server URL (default: http://localhost:3000)
    """
    # Configuration - Portable via environment variable
    mcp_path = os.environ.get(
        "EXCALIDRAW_MCP_PATH",
        os.path.expanduser("~/mcp_excalidraw/dist/index.js")
    )
    express_url = os.environ.get("EXPRESS_SERVER_URL", "http://localhost:3000")
    
    if not os.path.exists(mcp_path):
        return {"isError": True, "error": f"MCP Server not found at {mcp_path}."}

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    
    # Calculate LOG_FILE_PATH relative to this script's directory
    # This ensures the log is stored in .agent/skills/excalidraw_canvas/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(os.path.dirname(script_dir), "excalidraw.log")
    
    try:
        process = subprocess.Popen(
            ["node", mcp_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={
                **os.environ,
                "EXPRESS_SERVER_URL": express_url,
                "ENABLE_CANVAS_SYNC": "true",
                "LOG_FILE_PATH": log_file_path  # Dynamic log path
            }
        )
        stdout, stderr = process.communicate(input=json.dumps(request) + "\n", timeout=20)
        if process.returncode != 0:
            return {"isError": True, "error": stderr}
        return json.loads(stdout)
    except Exception as e:
        return {"isError": True, "error": str(e)}

def get_scene_elements():
    """Fetches all elements current on the canvas."""
    res = execute_mcp_command("get_resource", {"resource": "elements"})
    if "result" in res:
        try:
            data = json.loads(res["result"]["content"][0]["text"])
            return data.get("elements", [])
        except:
            return []
    return []

def clear_canvas():
    """Atomic wipe of the entire scene using the new backend tool."""
    print("🧹 Clearing scene (Atomic Wipe)...")
    res = execute_mcp_command("clear_scene", {})
    if "isError" in res:
        print(f"⚠️  clear_scene tool failed: {res.get('error')}")
    return res

# --- ZENITH V5 HELPERS (SMART LAYOUT & DYNAMICS) ---

# Vivid Palette for Arrows (Empirically Validated)
CONTRAST_PALETTE = {
    "node_agent": "#f77f00", # Vivid Orange (TESTED: VISIBLE)
    "node_tool": "#118ab2",  # Ocean Blue
    "node_data": "#06d6a0",  # Aqua Green
    "node_audit": "#e63946", # Vivid Red
}

def auto_size_box(text, padding=40):
    """Calculates approximate width based on text length."""
    return max(180, len(text) * 10 + padding)

def create_box(x, y, text, type="node_tool", group_id=None):
    """Zenith standard box with auto-sizing and grouping."""
    style = STYLES.get(type, STYLES["node_tool"])
    width = auto_size_box(text)
    el = {
        "type": "rectangle",
        "x": x,
        "y": y,
        "width": width,
        "height": 60,
        "text": text,
        **style
    }
    if group_id: el["groupIds"] = [group_id]
    return el

def create_arrow_abs(x1, y1, x2, y2, group_id=None, **kwargs):
    """
    Zenith Arrow Engine - Empirically Calibrated.
    strokeWidth=2 confirmed VISIBLE in Excalidraw.
    """
    el = {
        "type": "arrow",
        "x": x1,
        "y": y1,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "endArrowhead": "arrow",
        "strokeWidth": 2,  # EMPIRICAL: Width=2 is VISIBLE
        "strokeColor": "#000000",
        "opacity": 100,
        "roughness": 0,
        **kwargs
    }
    if group_id: el["groupIds"] = [group_id]
    return el

def create_legend(x, y, categories):
    """
    Automatically renders a styled legend box.
    Categories: list of ("Name", "node_type")
    """
    elements = []
    legend_group = str(uuid.uuid4())
    
    # Legend Container (No internal text to avoid centering issues)
    elements.append({
        "type": "rectangle",
        "x": x,
        "y": y,
        "width": 250,
        "height": 60 + (len(categories) * 40),
        "backgroundColor": "#f8f9fa",
        "strokeColor": "#adb5bd",
        "strokeWidth": 1,
        "groupIds": [legend_group]
    })
    
    # Header Text (Centered and Readable)
    elements.append({
        "type": "text",
        "x": x + 80,
        "y": y + 15,
        "text": "LEGEND",
        "fontSize": 18,
        "groupIds": [legend_group],
        "strokeColor": "#000000"
    })
    
    for i, (name, type) in enumerate(categories):
        style = STYLES.get(type, STYLES["node_tool"])
        # Use the Contrast palette for the rect representation in legend if needed
        # but here we use the original styles to match the diagram nodes
        elements.append({
            "type": "rectangle",
            "x": x + 20,
            "y": y + 55 + (i * 35),
            "width": 30,
            "height": 20,
            "groupIds": [legend_group],
            **style
        })
        elements.append({
            "type": "text",
            "x": x + 65,
            "y": y + 55 + (i * 35),
            "text": name,
            "fontSize": 14,
            "groupIds": [legend_group]
        })
        
    return elements

def create_arrow(start_x, start_y, end_x, end_y, **kwargs):
    """Backward compatibility wrapper."""
    return create_arrow_abs(start_x, start_y, end_x, end_y, **kwargs)

def batch_create_with_layout(elements, start_y=100, spacing=80):
    """
    Creates elements with automatic vertical layout to avoid overlap.
    """
    current_y = start_y
    adjusted_elements = []
    
    for el in elements:
        # Simple vertical stack if no Y is provided or if we want to enforce layout
        el["y"] = current_y
        adjusted_elements.append(el)
        # Increment Y based on height or default spacing
        height = el.get("height", 60)
        current_y += height + spacing
        
    return execute_mcp_command("batch_create_elements", {"elements": adjusted_elements})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mcp_bridge.py <command> [args_json]")
        print("Special commands: clear_canvas, get_elements")
        sys.exit(1)
        
    cmd = sys.argv[1]
    
    if cmd == "clear_canvas":
        print(json.dumps(clear_canvas(), indent=2))
    elif cmd == "get_elements":
        print(json.dumps(get_scene_elements(), indent=2))
    elif cmd == "draw_infrastructure":
        # Draw the Zenith structure
        clear_canvas()
        
        main_group = str(uuid.uuid4())
        # Root .agent
        root = create_box(400, 50, ".agent (Telemetry & Rules Hub)", type="node_agent", group_id=main_group)
        
        folders = [
            ("project", 100, 200, "node_data"),
            ("rules", 300, 200, "node_data"),
            ("skills", 500, 200, "node_data"),
            ("workflows", 700, 200, "node_data"),
            
            ("tools", 100, 350, "node_tool"),
            ("evals", 300, 350, "node_tool"),
            ("memory", 500, 350, "node_tool"),
            ("docs", 700, 350, "node_tool"),
            
            ("fix_logs", 200, 500, "node_audit"),
            ("audit", 400, 500, "node_audit"),
            ("research_summaries", 600, 500, "node_audit"),
        ]
        
        elements = [root]
        for name, x, y, style_name in folders:
            # Box
            box = create_box(x, y, name, type=style_name, group_id=main_group)
            elements.append(box)
            
            # Arrow from root: Bottom Center -> Top Center
            # Use CONTRAST_PALETTE for extreme visibility on white background
            arrow_color = CONTRAST_PALETTE.get(style_name, "#000000")
            
            elements.append(create_arrow_abs(
                root["x"] + root["width"]/2, root["y"] + root["height"], 
                box["x"] + box["width"]/2, box["y"], 
                strokeColor=arrow_color,
                group_id=main_group
            ))
            
        # Add Legend to the SIDE (x=950 instead of 50)
        elements.extend(create_legend(950, 50, [
            ("Identity/Root", "node_agent"),
            ("Function/Tool", "node_tool"),
            ("Knowledge/Data", "node_data"),
            ("Tracking/Audit", "node_audit")
        ]))
        
        print(json.dumps(execute_mcp_command("batch_create_elements", {"elements": elements}), indent=2))
    elif cmd == "test_perfect":
        # Pixel-perfect architecture test
        clear_canvas()
        
        # Nodes
        nodes = [
            {"id": "a", "type": "rectangle", "x": 100, "y": 200, "width": 200, "height": 60, "text": "Antigravity Agent", "backgroundColor": "#1d3557", "strokeColor": "#f1faee"},
            {"id": "b", "type": "rectangle", "x": 500, "y": 200, "width": 200, "height": 60, "text": "MCP Server", "backgroundColor": "#457b9d", "strokeColor": "#f1faee"}
        ]
        
        # Arrow: Correct relative logic
        arrow = create_arrow(
            start_x=300, start_y=230, # x1+w1, y1+h/2
            end_x=500, end_y=230,   # x2, y2+h/2
            strokeColor="#e63946",
            strokeWidth=2
        )
        
        print(json.dumps(execute_mcp_command("batch_create_elements", {"elements": nodes + [arrow]}), indent=2))
    else:
        args = json.loads(sys.argv[2])
        result = execute_mcp_command(cmd, args)
        print(json.dumps(result, indent=2))
