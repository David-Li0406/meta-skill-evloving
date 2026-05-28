#!/usr/bin/env python3
import csv
import json
import sys
import argparse
from pathlib import Path

# Path configuration relative to script
BASE_DIR = Path(__file__).parent.parent
# Downloaded structure is .agent/skills/ui_ux_designer/resources/data/*.csv
RESOURCE_DIR = BASE_DIR / "resources" / "data"

def load_db(filename):
    """Load a CSV file from the resources database and transform it into a list of dicts."""
    path = RESOURCE_DIR / filename
    if not path.exists():
        return []
    
    results = []
    try:
        with open(path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
    except Exception as e:
        print(f"Error loading {filename}: {e}", file=sys.stderr)
    
    return results

def search(query, db_name="colors.csv"):
    data = load_db(db_name)
    results = []
    query = query.lower()
    
    for item in data:
        # Search in all dictionary values (CSV row)
        content = " ".join([str(v).lower() for v in item.values() if v])
        if query in content:
            results.append(item)
    
    return results[:3]  # Limit to 3 results to avoid context overflow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="What you're looking for (e.g., 'dark mode', 'corporate')")
    parser.add_argument("--type", default="colors", 
                        choices=["colors", "typography", "styles", "products", "ux", "landing", "charts"])
    args = parser.parse_args()

    # Mapping of actual CSV files found in the repo
    db_map = {
        "colors": "colors.csv",
        "typography": "typography.csv",
        "styles": "styles.csv",
        "products": "products.csv",
        "ux": "ux-guidelines.csv",
        "landing": "landing.csv",
        "charts": "charts.csv"
    }

    target_file = db_map.get(args.type, "colors.csv")
    results = search(args.query, target_file)
    
    if results:
        print(json.dumps(results, indent=2))
    else:
        print(f"No results found for '{args.query}' in {target_file}.")

if __name__ == "__main__":
    main()
