#!/usr/bin/env python3
"""
Transform workflow designer export format to generator-compatible format.

Designer Export Format:
{
  "metadata": { "title": "My Workflow" },
  "nodes": [{ "id", "type", "label", "config", "position" }],
  "edges": [...]
}

Generator Expected Format:
{
  "name": "my-workflow",
  "nodes": [{ "id", "type", "position", "data": { "label", "config" } }],
  "edges": [...]
}

Usage:
  python transform-spec.py <input.json> [output.json]

  If output.json is not provided, prints to stdout.
"""

import json
import sys
import re


def to_kebab_case(s: str) -> str:
    """Convert string to kebab-case."""
    # Replace spaces and underscores with hyphens
    s = re.sub(r'[\s_]+', '-', s)
    # Insert hyphen before uppercase letters and lowercase them
    s = re.sub(r'([a-z])([A-Z])', r'\1-\2', s)
    # Remove non-alphanumeric (except hyphens)
    s = re.sub(r'[^a-zA-Z0-9-]', '', s)
    # Collapse multiple hyphens
    s = re.sub(r'-+', '-', s)
    return s.lower().strip('-')


# Map designer node types to generator node types
NODE_TYPE_MAP = {
    "loop-container": "loop",
    # Add other mappings as needed
}


def transform_node(node: dict) -> dict:
    """Transform a designer node to generator format."""
    node_type = node.get("type", "")
    config = node.get("config", {})

    # Map node type if needed
    mapped_type = NODE_TYPE_MAP.get(node_type, node_type)

    # Special case: data-validate with expression (not schema) -> data-transform
    # Designer uses data-validate for filtering, generator expects JSON Schema
    if node_type == "data-validate" and "expression" in config and "schema" not in config:
        mapped_type = "data-transform"
        # Restructure config for data-transform
        config = {
            "expression": config.get("expression", ""),
            "inputPath": config.get("inputPath", "$"),
        }

    return {
        "id": node.get("id"),
        "type": mapped_type,
        "position": node.get("position", {"x": 0, "y": 0}),
        "data": {
            "label": node.get("label", ""),
            "description": node.get("description", ""),
            "config": config
        }
    }


def transform_spec(spec: dict) -> dict:
    """Transform designer export to generator format."""
    # Extract name from metadata.title or use default
    metadata = spec.get("metadata", {})
    title = metadata.get("title", "untitled-workflow")
    name = to_kebab_case(title)

    # Transform nodes
    nodes = [transform_node(n) for n in spec.get("nodes", [])]

    # Edges stay the same format
    edges = spec.get("edges", [])

    # Build output spec
    output = {
        "name": name,
        "description": metadata.get("description", ""),
        "nodes": nodes,
        "edges": edges,
    }

    # Preserve any other metadata
    if "version" in metadata:
        output.setdefault("metadata", {})["version"] = metadata["version"]
    if "author" in metadata:
        output.setdefault("metadata", {})["author"] = metadata["author"]

    return output


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Read input
    with open(input_file, 'r') as f:
        spec = json.load(f)

    # Transform
    transformed = transform_spec(spec)

    # Output
    output_json = json.dumps(transformed, indent=2)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output_json)
        print(f"Transformed spec written to: {output_file}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
