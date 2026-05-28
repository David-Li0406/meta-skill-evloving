#!/usr/bin/env python3
"""
API Endpoint Scanner for Frappe Apps

Scans Python files for @frappe.whitelist decorators and extracts API endpoint information.
Creates/updates a YAML file with all discovered endpoints for security review.

Usage:
    python scan_api_endpoints.py [--path <app-path>] [--output <yaml-file>]

Examples:
    python scan_api_endpoints.py --path tweaks
    python scan_api_endpoints.py --path /path/to/app --output ../../../docs/api-review.yaml
"""

import argparse
import ast
import os
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml


class APIEndpointVisitor(ast.NodeVisitor):
    """AST visitor to find functions decorated with @frappe.whitelist"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.endpoints = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definitions to check for whitelist decorator"""
        has_whitelist = False

        for decorator in node.decorator_list:
            # Check for @frappe.whitelist() or @frappe.whitelist
            if isinstance(decorator, ast.Call):
                if self._is_frappe_whitelist(decorator.func):
                    has_whitelist = True
                    break
            elif self._is_frappe_whitelist(decorator):
                has_whitelist = True
                break

        if has_whitelist:
            endpoint_info = self._extract_endpoint_info(node)
            self.endpoints.append(endpoint_info)

        self.generic_visit(node)

    def _is_frappe_whitelist(self, node) -> bool:
        """Check if node represents frappe.whitelist"""
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                return node.value.id == "frappe" and node.attr == "whitelist"
        elif isinstance(node, ast.Name):
            # Could be imported as `from frappe import whitelist`
            return node.id == "whitelist"
        return False

    def _extract_endpoint_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Extract endpoint information from function node"""
        # Get function arguments
        args = []
        for arg in node.args.args:
            if arg.arg != "self":
                args.append(arg.arg)

        # Get docstring
        docstring = ast.get_docstring(node) or ""

        # Extract security checks from function body
        security_checks = self._extract_security_checks(node)

        # Calculate relative path for the endpoint
        relative_path = self.filepath

        return {
            "function": node.name,
            "file": relative_path,
            "line": node.lineno,
            "arguments": args,
            "docstring": docstring.strip() if docstring else None,
            "security_checks": security_checks,
            "reviewed": False,
            "notes": None,
        }

    def _extract_security_checks(self, node: ast.FunctionDef) -> Dict[str, bool]:
        """Detect security patterns in function body"""
        checks = {
            "has_frappe_only_for": False,
            "has_frappe_get_list": False,
            "has_frappe_has_permission": False,
            "has_permission_check": False,
        }

        # Convert function body to string for simple pattern matching
        func_source = ast.unparse(node)

        # Check for security patterns
        if "frappe.only_for" in func_source:
            checks["has_frappe_only_for"] = True
        if "frappe.get_list" in func_source:
            checks["has_frappe_get_list"] = True
        if "frappe.has_permission" in func_source:
            checks["has_frappe_has_permission"] = True
        if any(
            pattern in func_source
            for pattern in ["has_permission", "check_permission", "validate_permission"]
        ):
            checks["has_permission_check"] = True

        return checks


def scan_directory(directory: Path, base_path: Path = None) -> List[Dict[str, Any]]:
    """Recursively scan directory for Python files with API endpoints"""
    if base_path is None:
        base_path = directory

    all_endpoints = []

    for item in directory.rglob("*.py"):
        if item.is_file() and not item.name.startswith("__"):
            try:
                with open(item, "r", encoding="utf-8") as f:
                    content = f.read()

                # Quick check if file contains @frappe.whitelist before parsing
                if "@frappe.whitelist" not in content:
                    continue

                tree = ast.parse(content, filename=str(item))
                relative_path = str(item.relative_to(base_path))
                visitor = APIEndpointVisitor(relative_path)
                visitor.visit(tree)
                all_endpoints.extend(visitor.endpoints)

            except Exception as e:
                print(f"Error processing {item}: {e}")

    return all_endpoints


def load_existing_endpoints(yaml_file: Path) -> Dict[str, Any]:
    """Load existing endpoint data from YAML file"""
    if yaml_file.exists():
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f) or {}
            return data
    return {}


def merge_endpoints(
    existing_data: Dict[str, Any], new_endpoints: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Merge new endpoints with existing data, preserving review notes"""
    # Create a map of existing endpoints by file+function
    existing_map = {}
    for endpoint in existing_data.get("endpoints", []):
        key = f"{endpoint['file']}::{endpoint['function']}"
        existing_map[key] = endpoint

    # Merge new endpoints
    merged_endpoints = []
    for new_endpoint in new_endpoints:
        key = f"{new_endpoint['file']}::{new_endpoint['function']}"
        if key in existing_map:
            # Preserve review status and notes from existing
            existing = existing_map[key]
            new_endpoint["reviewed"] = existing.get("reviewed", False)
            new_endpoint["notes"] = existing.get("notes")
            # Update other fields with new data
            new_endpoint["line"] = new_endpoint["line"]
            new_endpoint["security_checks"] = new_endpoint["security_checks"]
        merged_endpoints.append(new_endpoint)

    return {
        "scan_info": {
            "total_endpoints": len(merged_endpoints),
            "reviewed": sum(1 for e in merged_endpoints if e.get("reviewed")),
            "unreviewed": sum(1 for e in merged_endpoints if not e.get("reviewed")),
        },
        "endpoints": sorted(merged_endpoints, key=lambda x: (x["file"], x["function"])),
    }


def save_endpoints(endpoints_data: Dict[str, Any], yaml_file: Path):
    """Save endpoints to YAML file"""
    yaml_file.parent.mkdir(parents=True, exist_ok=True)

    with open(yaml_file, "w") as f:
        yaml.dump(
            endpoints_data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def main():
    parser = argparse.ArgumentParser(
        description="Scan Frappe app for API endpoints with @frappe.whitelist decorator"
    )
    parser.add_argument(
        "--path",
        default="tweaks",
        help="Path to the Frappe app directory to scan (default: tweaks)",
    )
    parser.add_argument(
        "--output",
        default="../../../docs/api-review.yaml",
        help="Output YAML file path (default: ../../../docs/api-review.yaml)",
    )

    args = parser.parse_args()

    # Resolve paths
    script_dir = Path(__file__).parent
    app_path = Path(args.path).resolve()
    output_path = (script_dir / args.output).resolve()

    if not app_path.exists():
        print(f"Error: Path {app_path} does not exist")
        return 1

    print(f"Scanning for API endpoints in: {app_path}")
    print(f"Output file: {output_path}")

    # Scan for endpoints
    endpoints = scan_directory(app_path, app_path)
    print(f"Found {len(endpoints)} API endpoints")

    # Load existing data
    existing_data = load_existing_endpoints(output_path)

    # Merge with existing
    merged_data = merge_endpoints(existing_data, endpoints)

    # Save to YAML
    save_endpoints(merged_data, output_path)
    print(f"Saved endpoint data to: {output_path}")
    print(
        f"Summary: {merged_data['scan_info']['total_endpoints']} total, "
        f"{merged_data['scan_info']['reviewed']} reviewed, "
        f"{merged_data['scan_info']['unreviewed']} unreviewed"
    )

    return 0


if __name__ == "__main__":
    exit(main())
