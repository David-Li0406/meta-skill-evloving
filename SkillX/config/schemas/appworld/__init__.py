"""AppWorld tool schemas.

457 APIs extracted from AppWorld environment covering 11 apps:
- api_docs, supervisor, amazon, phone, file_system
- spotify, venmo, gmail, splitwise, simple_note, todoist
"""

import os
import json
from typing import List, Dict, Any

_SCHEMA_DIR = os.path.dirname(os.path.abspath(__file__))
_SCHEMAS_LOADED = False
_SCHEMAS_CACHE: Dict[str, Dict[str, Any]] = {}

APPWORLD_TOOL_SCHEMAS: List[Dict[str, Any]] = []


def _load_schemas():
    """Load schemas from JSON file."""
    global _SCHEMAS_LOADED, _SCHEMAS_CACHE, APPWORLD_TOOL_SCHEMAS

    if _SCHEMAS_LOADED:
        return

    schemas_path = os.path.join(_SCHEMA_DIR, "appworld_schemas.json")
    if os.path.exists(schemas_path):
        with open(schemas_path, "r", encoding="utf-8") as f:
            APPWORLD_TOOL_SCHEMAS.clear()
            APPWORLD_TOOL_SCHEMAS.extend(json.load(f))
            for schema in APPWORLD_TOOL_SCHEMAS:
                name = schema.get("function", {}).get("name", "")
                if name:
                    _SCHEMAS_CACHE[name] = schema

    _SCHEMAS_LOADED = True


def get_schema(tool_name: str) -> Dict[str, Any]:
    """Get schema for a specific tool."""
    _load_schemas()
    return _SCHEMAS_CACHE.get(tool_name, {})


def get_all_schemas() -> List[Dict[str, Any]]:
    """Get all AppWorld schemas."""
    _load_schemas()
    return APPWORLD_TOOL_SCHEMAS


def list_tool_names() -> List[str]:
    """List all tool names."""
    _load_schemas()
    return list(_SCHEMAS_CACHE.keys())


# Auto-load on import
_load_schemas()
