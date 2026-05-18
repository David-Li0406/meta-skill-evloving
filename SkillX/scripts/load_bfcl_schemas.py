"""Load and convert BFCL tool schemas from JSONL files.

BFCL schemas use a slightly different format:
- "type": "dict" instead of "type": "object"
- Has "response" field for return type

This script converts them to OpenAPI function calling format.
"""

import os
import json
from typing import Dict, List, Any


BFCL_SOURCE_DIR = "/ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc"
OUTPUT_DIR = "/ossfs/workspace/AutoSkills/SkillX/config/schemas/bfcl"


def convert_bfcl_schema(raw_schema: Dict[str, Any]) -> Dict[str, Any]:
    """Convert BFCL schema format to OpenAPI function calling format."""
    name = raw_schema["name"]
    description = raw_schema.get("description", "")
    parameters = raw_schema.get("parameters", {})

    # Convert "dict" type to "object"
    def convert_type(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "dict":
                obj["type"] = "object"
            for key, value in obj.items():
                convert_type(value)
        elif isinstance(obj, list):
            for item in obj:
                convert_type(item)
        return obj

    parameters = convert_type(parameters)

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters
        }
    }


def load_bfcl_schemas_from_file(filepath: str) -> List[Dict[str, Any]]:
    """Load schemas from a BFCL JSONL file."""
    schemas = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                raw = json.loads(line)
                schema = convert_bfcl_schema(raw)
                schemas.append(schema)
    return schemas


def load_all_bfcl_schemas() -> Dict[str, List[Dict[str, Any]]]:
    """Load all BFCL schemas from source directory."""
    all_schemas = {}

    for filename in os.listdir(BFCL_SOURCE_DIR):
        if filename.endswith(".json"):
            domain = filename.replace(".json", "")
            filepath = os.path.join(BFCL_SOURCE_DIR, filename)
            schemas = load_bfcl_schemas_from_file(filepath)
            all_schemas[domain] = schemas
            print(f"Loaded {len(schemas)} schemas from {domain}")

    return all_schemas


def to_python_literal(obj, indent=0):
    """Convert object to Python literal string (True/False/None instead of true/false/null)."""
    spaces = "    " * indent
    if obj is None:
        return "None"
    elif isinstance(obj, bool):
        return "True" if obj else "False"
    elif isinstance(obj, str):
        # Use repr for proper string escaping
        return repr(obj)
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, list):
        if not obj:
            return "[]"
        items = [to_python_literal(item, indent + 1) for item in obj]
        inner_spaces = "    " * (indent + 1)
        return "[\n" + ",\n".join(f"{inner_spaces}{item}" for item in items) + f"\n{spaces}]"
    elif isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            key_str = repr(k)
            val_str = to_python_literal(v, indent + 1)
            items.append(f"{key_str}: {val_str}")
        inner_spaces = "    " * (indent + 1)
        return "{\n" + ",\n".join(f"{inner_spaces}{item}" for item in items) + f"\n{spaces}}}"
    else:
        return repr(obj)


def save_schemas_to_python(schemas: Dict[str, List[Dict[str, Any]]], output_dir: str):
    """Save schemas to Python files."""
    os.makedirs(output_dir, exist_ok=True)

    all_domains = []

    for domain, schema_list in schemas.items():
        # Convert domain name to Python variable name
        var_name = domain.upper().replace("-", "_") + "_TOOL_SCHEMAS"
        all_domains.append((domain, var_name))

        # Convert to Python literal (True/False/None instead of true/false/null)
        schema_str = to_python_literal(schema_list)

        # Write Python file
        py_content = f'''"""BFCL {domain} tool schemas.

Auto-generated from {BFCL_SOURCE_DIR}/{domain}.json
"""

from typing import List, Dict, Any

{var_name}: List[Dict[str, Any]] = {schema_str}
'''

        filepath = os.path.join(output_dir, f"{domain.replace('-', '_')}.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(py_content)
        print(f"Saved {domain} to {filepath}")

    # Write __init__.py
    imports = "\n".join([f"from .{d.replace('-', '_')} import {v}" for d, v in all_domains])
    all_exports = ", ".join([f'"{v}"' for _, v in all_domains])

    init_content = f'''"""BFCL tool schemas.

Auto-generated from {BFCL_SOURCE_DIR}
"""

{imports}

__all__ = [{all_exports}]

# Combined schemas for easy access
BFCL_ALL_SCHEMAS = {{
{chr(10).join([f'    "{d}": {v},' for d, v in all_domains])}
}}
'''

    init_path = os.path.join(output_dir, "__init__.py")
    with open(init_path, "w", encoding="utf-8") as f:
        f.write(init_content)
    print(f"Saved __init__.py to {init_path}")


def save_schemas_to_json(schemas: Dict[str, List[Dict[str, Any]]], output_dir: str):
    """Save all schemas to a combined JSON file."""
    # Save combined
    combined = {}
    for domain, schema_list in schemas.items():
        for schema in schema_list:
            name = schema["function"]["name"]
            combined[name] = schema

    combined_path = os.path.join(output_dir, "bfcl_all_schemas.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Saved combined schemas to {combined_path}")

    return combined


if __name__ == "__main__":
    print("Loading BFCL schemas...")
    schemas = load_all_bfcl_schemas()

    print(f"\nTotal domains: {len(schemas)}")
    total_tools = sum(len(s) for s in schemas.values())
    print(f"Total tools: {total_tools}")

    print("\nSaving to Python files...")
    save_schemas_to_python(schemas, OUTPUT_DIR)

    print("\nSaving to JSON...")
    combined = save_schemas_to_json(schemas, OUTPUT_DIR)

    print(f"\nDone! {len(combined)} unique tools saved.")
