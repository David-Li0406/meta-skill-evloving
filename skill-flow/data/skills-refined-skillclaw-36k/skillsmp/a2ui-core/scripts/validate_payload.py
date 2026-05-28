#!/usr/bin/env python3
"""
A2UI Payload Validator

Validates that A2UI payloads follow the flat Adjacency List model.
Checks for:
- Valid JSON structure
- Required fields (surfaceUpdate, components, id)
- Unique component IDs
- Flat structure (no nested components in children)

Usage:
    python3 validate_payload.py '<json_string>'
    python3 validate_payload.py payload.json
"""

import json
import sys
from typing import Tuple, List, Any


def validate_component(comp: dict, seen_ids: set) -> Tuple[bool, str]:
    """
    Validate a single component definition.
    
    Args:
        comp: The component object
        seen_ids: Set of already-seen component IDs
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for required ID
    if "id" not in comp:
        return False, "Component missing 'id' field"
    
    comp_id = comp["id"]
    
    # Check for unique IDs
    if comp_id in seen_ids:
        return False, f"Duplicate component ID: '{comp_id}'"
    
    seen_ids.add(comp_id)
    
    # Check for nested structures (the anti-pattern)
    component_def = comp.get("component", {})
    if not isinstance(component_def, dict):
        return False, f"Component '{comp_id}' has invalid 'component' field"
    
    for comp_type, comp_props in component_def.items():
        if not isinstance(comp_props, dict):
            continue
            
        children = comp_props.get("children", {})
        if isinstance(children, dict):
            explicit_list = children.get("explicitList", [])
            if explicit_list and isinstance(explicit_list[0], dict):
                return False, (
                    f"NESTING DETECTED in component '{comp_id}': "
                    f"'children' should contain ID strings, not nested objects. "
                    f"A2UI requires a flat adjacency list."
                )
    
    return True, ""


def validate_a2ui_payload(json_data: str) -> Tuple[bool, str, List[str]]:
    """
    Validate an A2UI payload for protocol compliance.
    
    Args:
        json_data: JSON string to validate
        
    Returns:
        Tuple of (is_valid, message, component_ids)
    """
    # Parse JSON
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}", []
    
    # Check for surfaceUpdate
    if "surfaceUpdate" not in data:
        # Check for other valid message types
        valid_types = ["dataModelUpdate", "beginRendering", "deleteSurface", "userAction"]
        for msg_type in valid_types:
            if msg_type in data:
                return True, f"Valid {msg_type} message", []
        return False, "Missing required message type (surfaceUpdate, dataModelUpdate, etc.)", []
    
    update = data["surfaceUpdate"]
    
    # Check for surfaceId
    if "surfaceId" not in update:
        return False, "surfaceUpdate missing 'surfaceId'", []
    
    # Check for components
    if "components" not in update:
        return False, "surfaceUpdate missing 'components' list", []
    
    components = update["components"]
    if not isinstance(components, list):
        return False, "'components' must be an array", []
    
    # Validate each component
    seen_ids: set = set()
    for comp in components:
        is_valid, error = validate_component(comp, seen_ids)
        if not is_valid:
            return False, error, list(seen_ids)
    
    return True, f"Valid A2UI payload with {len(seen_ids)} component(s)", list(seen_ids)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 validate_payload.py <json_file_or_string>")
        print("\nExamples:")
        print('  python3 validate_payload.py \'{"surfaceUpdate":{"surfaceId":"test","components":[{"id":"a"}]}}\'')
        print("  python3 validate_payload.py ./payload.json")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    # Check if argument looks like JSON (starts with '{' or '[')
    # If so, treat as JSON string directly; otherwise try as file path
    arg_stripped = arg.strip()
    if arg_stripped.startswith('{') or arg_stripped.startswith('['):
        content = arg
    else:
        try:
            with open(arg, 'r') as f:
                content = f.read()
        except (FileNotFoundError, IsADirectoryError, OSError):
            content = arg
    
    # Validate
    is_valid, message, component_ids = validate_a2ui_payload(content)
    
    # Output
    icon = "✅" if is_valid else "❌"
    print(f"{icon} {message}")
    
    if component_ids:
        print(f"   Components: {', '.join(component_ids)}")
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
