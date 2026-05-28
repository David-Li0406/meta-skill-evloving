#!/usr/bin/env python3
"""
WoD Toolkit Data Lookup

Query the consolidated data.json reference file.

Usage:
    python lookup.py <category> [object] [key] [--search term]
    
Examples:
    python lookup.py                           # List all categories
    python lookup.py v20.disciplines           # List objects in category
    python lookup.py v20.disciplines disciplines # Get full object
    python lookup.py v20.disciplines disciplines Dominate  # Get specific key
    python lookup.py --search Brujah           # Search all data for term
    python lookup.py v20.rules --search generation  # Search within category
"""

import json
import sys
from pathlib import Path

# Find data.json relative to this script
SCRIPT_DIR = Path(__file__).parent.parent
DATA_FILE = SCRIPT_DIR / "references" / "data.json"

def load_data():
    """Load the consolidated data file."""
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found")
        sys.exit(1)
    with open(DATA_FILE) as f:
        return json.load(f)

def list_categories(data):
    """List all available categories."""
    print("Available categories:")
    for cat in sorted(data.keys()):
        print(f"  {cat} ({len(data[cat])} objects)")

def list_objects(data, category):
    """List objects within a category."""
    if category not in data:
        print(f"Error: Category '{category}' not found")
        print(f"Available: {', '.join(sorted(data.keys()))}")
        return
    print(f"Objects in {category}:")
    for obj in sorted(data[category].keys()):
        print(f"  {obj}")

def get_object(data, category, obj_name):
    """Get a full object from a category."""
    if category not in data:
        print(f"Error: Category '{category}' not found")
        return
    if obj_name not in data[category]:
        print(f"Error: Object '{obj_name}' not found in {category}")
        print(f"Available: {', '.join(sorted(data[category].keys()))}")
        return
    print(json.dumps(data[category][obj_name], indent=2))

def get_key(data, category, obj_name, key):
    """Get a specific key from an object."""
    if category not in data:
        print(f"Error: Category '{category}' not found")
        return
    if obj_name not in data[category]:
        print(f"Error: Object '{obj_name}' not found in {category}")
        return
    obj = data[category][obj_name]

    # Handle nested key access with dot notation
    keys = key.split('.')
    current = obj
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        elif isinstance(current, list):
            try:
                current = current[int(k)]
            except (ValueError, IndexError):
                print(f"Error: Key '{key}' not found")
                return
        else:
            print(f"Error: Key '{key}' not found")
            return

    if isinstance(current, (dict, list)):
        print(json.dumps(current, indent=2))
    else:
        print(current)

def search_data(data, term, category=None):
    """Search for a term in the data."""
    term_lower = term.lower()
    results = []

    categories = [category] if category else data.keys()

    for cat in categories:
        if cat not in data:
            continue
        for obj_name, obj_data in data[cat].items():
            matches = search_in_value(obj_data, term_lower, f"{cat}.{obj_name}")
            results.extend(matches)

    if results:
        print(f"Found {len(results)} matches for '{term}':")
        for path, snippet in results[:20]:  # Limit to 20 results
            print(f"  {path}")
            print(f"    {snippet[:100]}..." if len(snippet) > 100 else f"    {snippet}")
        if len(results) > 20:
            print(f"  ... and {len(results) - 20} more")
    else:
        print(f"No matches found for '{term}'")

def search_in_value(value, term, path):
    """Recursively search for term in a value."""
    results = []

    if isinstance(value, str):
        if term in value.lower():
            results.append((path, value))
    elif isinstance(value, dict):
        for k, v in value.items():
            if term in k.lower():
                results.append((f"{path}.{k}", str(v)[:200]))
            results.extend(search_in_value(v, term, f"{path}.{k}"))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            results.extend(search_in_value(v, term, f"{path}[{i}]"))

    return results

def main():
    args = sys.argv[1:]

    # Handle --search flag
    search_term = None
    search_category = None
    if '--search' in args:
        idx = args.index('--search')
        if idx + 1 < len(args):
            search_term = args[idx + 1]
            args = args[:idx]  # Remove search args
            if args:
                search_category = args[0]

    data = load_data()

    if search_term:
        search_data(data, search_term, search_category)
    elif len(args) == 0:
        list_categories(data)
    elif len(args) == 1:
        list_objects(data, args[0])
    elif len(args) == 2:
        get_object(data, args[0], args[1])
    else:
        get_key(data, args[0], args[1], args[2])

if __name__ == "__main__":
    main()
