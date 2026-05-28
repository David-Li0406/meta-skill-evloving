#!/usr/bin/env python3
"""
Parse Android UI XML dump and extract interactive elements with coordinates.

This script is designed for TEXT-BASED Android automation - it extracts
structured UI elements from the Android Accessibility Tree, avoiding the
need for expensive screenshot/vision processing.

Based on android-action-kernel approach:
- Text UI dump: ~$0.01/action, <1s, 99%+ accuracy
- Screenshot + Vision: ~$0.15/action, 3-5s, 70-80% accuracy

Usage:
    python parse_ui.py <xml_file>
    python parse_ui.py <xml_file> --json
    python parse_ui.py <xml_file> --compact
    python parse_ui.py <xml_file> --verbose

Examples:
    python parse_ui.py window_dump.xml
    python parse_ui.py /tmp/screen.xml --json
    python parse_ui.py /tmp/screen.xml --compact
"""

import xml.etree.ElementTree as ET
import json
import sys
import argparse
from typing import List, Dict


def get_interactive_elements(xml_content: str, verbose: bool = False) -> List[Dict]:
    """
    Parses Android Accessibility XML and returns a list of interactive elements.
    Calculates center coordinates (x, y) for every element.

    Args:
        xml_content: Raw XML string from uiautomator dump
        verbose: If True, include all elements; if False, only interactive ones

    Returns:
        List of element dictionaries with id, text, type, bounds, center, clickable, action
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        return []

    elements = []

    for node in root.iter():
        is_clickable = node.attrib.get("clickable") == "true"
        is_focusable = node.attrib.get("focusable") == "true"
        is_editable = node.attrib.get("class", "").endswith("EditText")
        is_scrollable = node.attrib.get("scrollable") == "true"
        text = node.attrib.get("text", "")
        desc = node.attrib.get("content-desc", "")
        resource_id = node.attrib.get("resource-id", "")

        # Skip empty containers unless verbose mode
        if not verbose:
            if not is_clickable and not is_focusable and not is_editable and not text and not desc:
                continue

        bounds = node.attrib.get("bounds")
        if bounds:
            try:
                # Parse bounds: "[x1,y1][x2,y2]" -> coordinates
                coords = bounds.replace("][", ",").replace("[", "").replace("]", "").split(",")
                x1, y1, x2, y2 = map(int, coords)

                # Skip elements with zero area or off-screen
                if x2 <= x1 or y2 <= y1:
                    continue
                if x1 < 0 and x2 < 0:
                    continue

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Determine element type
                class_name = node.attrib.get("class", "")
                element_type = class_name.split(".")[-1] if class_name else "Unknown"

                # Determine suggested action
                if is_editable:
                    action = "type"
                elif is_clickable:
                    action = "tap"
                elif is_scrollable:
                    action = "scroll"
                else:
                    action = "read"

                element = {
                    "id": resource_id,
                    "text": text or desc,
                    "type": element_type,
                    "bounds": bounds,
                    "center": [center_x, center_y],
                    "clickable": is_clickable,
                    "focusable": is_focusable,
                    "editable": is_editable,
                    "action": action
                }
                elements.append(element)
            except (ValueError, IndexError):
                continue

    return elements


def format_element(elem: Dict, compact: bool = False) -> str:
    """Format a single element for human-readable output."""
    text = elem['text']
    if len(text) > 50:
        text = text[:47] + "..."

    action_icon = {"tap": "👆", "type": "⌨️", "scroll": "📜", "read": "👁️"}.get(elem['action'], "")

    parts = []
    if text:
        parts.append(f'"{text}"')
    if elem['id']:
        short_id = elem['id'].split("/")[-1] if "/" in elem['id'] else elem['id']
        parts.append(f"[{short_id}]")

    label = " ".join(parts) if parts else elem['type']

    if compact:
        return f"{action_icon} {label} @ ({elem['center'][0]}, {elem['center'][1]})"
    else:
        return f"  {action_icon} {label} @ ({elem['center'][0]}, {elem['center'][1]})"


def format_compact(elements: List[Dict]) -> str:
    """
    Format elements in a very compact way optimised for LLM consumption.
    Groups by action type with minimal formatting.
    """
    lines = []

    tappable = [e for e in elements if e['action'] == 'tap']
    typeable = [e for e in elements if e['action'] == 'type']
    scrollable = [e for e in elements if e['action'] == 'scroll']

    if tappable:
        lines.append("TAP:")
        for elem in tappable:
            text = elem['text'][:40] if elem['text'] else elem['id'].split("/")[-1] if elem['id'] else elem['type']
            lines.append(f"  [{elem['center'][0]},{elem['center'][1]}] {text}")

    if typeable:
        lines.append("TYPE:")
        for elem in typeable:
            text = elem['text'][:40] if elem['text'] else elem['id'].split("/")[-1] if elem['id'] else "input"
            lines.append(f"  [{elem['center'][0]},{elem['center'][1]}] {text}")

    if scrollable:
        lines.append("SCROLL:")
        for elem in scrollable:
            lines.append(f"  [{elem['center'][0]},{elem['center'][1]}] {elem['type']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Parse Android UI XML dump - TEXT-BASED automation (no screenshots needed)"
    )
    parser.add_argument("xml_file", help="Path to XML file from uiautomator dump")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--compact", "-c", action="store_true", help="Compact output for LLM consumption")
    parser.add_argument("--verbose", "-v", action="store_true", help="Include all elements")
    args = parser.parse_args()

    try:
        with open(args.xml_file, "r", encoding="utf-8") as f:
            xml_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.xml_file}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    elements = get_interactive_elements(xml_content, verbose=args.verbose)

    if not elements:
        print("No interactive elements found. Screen may be loading or empty.", file=sys.stderr)
        sys.exit(0)

    if args.json:
        print(json.dumps(elements, indent=2))
    elif args.compact:
        print(format_compact(elements))
    else:
        # Human-readable format grouped by action
        print(f"\n📱 Found {len(elements)} interactive elements:\n")

        # Group by action type
        tappable = [e for e in elements if e['action'] == 'tap']
        typeable = [e for e in elements if e['action'] == 'type']
        scrollable = [e for e in elements if e['action'] == 'scroll']
        readable = [e for e in elements if e['action'] == 'read']

        if tappable:
            print("TAPPABLE:")
            for elem in tappable:
                print(format_element(elem))
            print()

        if typeable:
            print("INPUT FIELDS:")
            for elem in typeable:
                print(format_element(elem))
            print()

        if scrollable:
            print("SCROLLABLE:")
            for elem in scrollable:
                print(format_element(elem))
            print()

        if readable:
            print("TEXT/INFO:")
            for elem in readable[:10]:  # Limit readable to 10
                print(format_element(elem))
            if len(readable) > 10:
                print(f"  ... and {len(readable) - 10} more")
            print()


if __name__ == "__main__":
    main()
