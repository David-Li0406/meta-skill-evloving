"""
List all unique values for a frontmatter property across the vault.

Usage:
    python frontmatter_list.py <vault_path> --property <name> [options]

Examples:
    # List all tag values
    python frontmatter_list.py "d:\vault" --property tags
    
    # List status values used at least 5 times
    python frontmatter_list.py "d:\vault" --property status --min-count 5
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    find_markdown_files,
    parse_frontmatter,
    get_property_value,
    format_value
)


def list_property_values(vault_path: str, property_name: str, min_count: int = 1) -> Dict[Any, int]:
    """
    List all unique values for a property with usage counts.
    
    Args:
        vault_path: Path to Obsidian vault
        property_name: Property name to list
        min_count: Minimum usage count to include
        
    Returns:
        Dictionary mapping values to counts
    """
    value_counts = defaultdict(int)
    md_files = find_markdown_files(vault_path)
    
    for file_path in md_files:
        try:
            frontmatter, _ = parse_frontmatter(file_path)
            prop_value = get_property_value(frontmatter, property_name)
            
            if prop_value is not None:
                # Handle list properties (count each item separately)
                if isinstance(prop_value, list):
                    for item in prop_value:
                        value_counts[format_value(item)] += 1
                else:
                    value_counts[format_value(prop_value)] += 1
        
        except Exception as e:
            # Skip files with errors
            print(f"Warning: Skipping {file_path}: {e}", file=sys.stderr)
            continue
    
    # Filter by min_count
    filtered = {k: v for k, v in value_counts.items() if v >= min_count}
    
    return filtered


def format_results_table(property_name: str, value_counts: Dict[Any, int]) -> str:
    """Format results as a table."""
    if not value_counts:
        return f"No values found for property '{property_name}'."
    
    output = []
    output.append(f"\nProperty: {property_name}")
    output.append(f"Total unique values: {len(value_counts)}")
    output.append(f"Total usage count: {sum(value_counts.values())}\n")
    output.append("=" * 80)
    output.append(f"{'Value':<50} {'Count':>10}")
    output.append("=" * 80)
    
    # Sort by count (descending)
    sorted_items = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
    
    for value, count in sorted_items:
        value_str = str(value)[:50]  # Truncate long values
        output.append(f"{value_str:<50} {count:>10}")
    
    output.append("=" * 80)
    
    return "\n".join(output)


def format_results_json(property_name: str, value_counts: Dict[Any, int]) -> str:
    """Format results as JSON."""
    result = {
        'property': property_name,
        'total_unique_values': len(value_counts),
        'total_usage_count': sum(value_counts.values()),
        'values': [
            {'value': str(k), 'count': v}
            for k, v in sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
        ]
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='List unique values for a frontmatter property',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    parser.add_argument('--property', required=True,
                        help='Property name to list')
    parser.add_argument('--min-count', type=int, default=1,
                        help='Minimum usage count (default: 1)')
    parser.add_argument('--format', choices=['json', 'table'], default='table',
                        help='Output format (default: table)')
    parser.add_argument('--output', metavar='FILE',
                        help='Save output to file instead of printing to console')
    
    args = parser.parse_args()
    
    try:
        value_counts = list_property_values(args.vault_path, args.property, args.min_count)
        
        # Format output
        if args.format == 'json':
            output = format_results_json(args.property, value_counts)
        else:
            output = format_results_table(args.property, value_counts)
        
        # Write to file or print
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Results saved to: {args.output}")
        else:
            print(output)
        
        sys.exit(0)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
