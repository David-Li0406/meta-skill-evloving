"""
Search Obsidian notes by frontmatter properties.

Usage:
    python frontmatter_search.py <vault_path> --property <name> [options]

Examples:
    # Find notes with 'status' property
    python frontmatter_search.py "d:\vault" --property status --exists
    
    # Find notes tagged with specific tag
    python frontmatter_search.py "d:\vault" --property tags --contains "project"
    
    # Find notes with status equals "done"
    python frontmatter_search.py "d:\vault" --property status --equals "done"
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    find_markdown_files,
    parse_frontmatter,
    get_property_value,
    property_matches,
    format_value,
    infer_property_type
)


def search_notes(vault_path: str, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Search notes by frontmatter properties.
    
    Args:
        vault_path: Path to Obsidian vault
        filters: List of filter dictionaries with 'property', 'operator', 'value'
        
    Returns:
        List of matching notes with file path and matching properties
    """
    results = []
    md_files = find_markdown_files(vault_path)
    
    for file_path in md_files:
        try:
            frontmatter, _ = parse_frontmatter(file_path)
            
            # Check if all filters match (AND logic)
            all_match = True
            matched_properties = {}
            
            for filter_spec in filters:
                prop_name = filter_spec['property']
                operator = filter_spec['operator']
                target = filter_spec.get('value')
                
                prop_value = get_property_value(frontmatter, prop_name)
                
                if not property_matches(prop_value, operator, target):
                    all_match = False
                    break
                
                matched_properties[prop_name] = prop_value
            
            if all_match and matched_properties:
                results.append({
                    'file': file_path,
                    'properties': matched_properties
                })
        
        except Exception as e:
            # Skip files with errors (malformed YAML, etc.)
            print(f"Warning: Skipping {file_path}: {e}", file=sys.stderr)
            continue
    
    return results


def format_results_table(results: List[Dict[str, Any]]) -> str:
    """Format search results as a table."""
    if not results:
        return "No matching notes found."
    
    output = []
    output.append(f"\nFound {len(results)} matching note(s):\n")
    output.append("=" * 80)
    
    for result in results:
        file_path = result['file']
        properties = result['properties']
        
        # Show relative path if possible
        output.append(f"\nFile: {Path(file_path).name}")
        output.append(f"Path: {file_path}")
        output.append("Properties:")
        
        for key, value in properties.items():
            formatted_value = format_value(value)
            output.append(f"  {key}: {formatted_value}")
        
        output.append("-" * 80)
    
    return "\n".join(output)


def format_results_json(results: List[Dict[str, Any]]) -> str:
    """Format search results as JSON."""
    # Convert datetime objects to strings for JSON serialization
    serializable_results = []
    for result in results:
        serializable_result = {
            'file': result['file'],
            'properties': {}
        }
        for key, value in result['properties'].items():
            serializable_result['properties'][key] = format_value(value)
        serializable_results.append(serializable_result)
    
    return json.dumps(serializable_results, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Search Obsidian notes by frontmatter properties',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    parser.add_argument('--property', action='append', dest='properties',
                        help='Property name to search (can specify multiple times)')
    parser.add_argument('--exists', action='store_true',
                        help='Check if property exists')
    parser.add_argument('--not-exists', action='store_true', dest='not_exists',
                        help='Check if property does not exist')
    parser.add_argument('--equals', metavar='VALUE',
                        help='Check if property equals value')
    parser.add_argument('--contains', metavar='VALUE',
                        help='Check if property contains value (for lists/text)')
    parser.add_argument('--gt', metavar='VALUE',
                        help='Check if property is greater than value')
    parser.add_argument('--lt', metavar='VALUE',
                        help='Check if property is less than value')
    parser.add_argument('--format', choices=['json', 'table'], default='table',
                        help='Output format (default: table)')
    parser.add_argument('--output', metavar='FILE',
                        help='Save output to file instead of printing to console')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.properties:
        parser.error("At least one --property must be specified")
    
    # Determine operator
    operators = []
    if args.exists:
        operators.append('exists')
    if args.not_exists:
        operators.append('not-exists')
    if args.equals:
        operators.append('equals')
    if args.contains:
        operators.append('contains')
    if args.gt:
        operators.append('gt')
    if args.lt:
        operators.append('lt')
    
    if len(operators) == 0:
        parser.error("Must specify at least one operator: --exists, --not-exists, --equals, --contains, --gt, or --lt")
    if len(operators) > 1:
        parser.error("Can only specify one operator per search")
    
    operator = operators[0]
    
    # Get target value
    target = None
    if operator == 'equals':
        target = infer_property_type(args.equals)
    elif operator == 'contains':
        target = args.contains
    elif operator == 'gt':
        target = infer_property_type(args.gt)
    elif operator == 'lt':
        target = infer_property_type(args.lt)
    
    # Build filters (one filter per property)
    filters = []
    for prop_name in args.properties:
        filters.append({
            'property': prop_name,
            'operator': operator,
            'value': target
        })
    
    # Execute search
    try:
        results = search_notes(args.vault_path, filters)
        
        # Format output
        if args.format == 'json':
            output = format_results_json(results)
        else:
            output = format_results_table(results)
        
        # Write to file or print
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Results saved to: {args.output}")
        else:
            print(output)
        
        # Exit code: 0 if found, 1 if not found
        sys.exit(0 if results else 1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
