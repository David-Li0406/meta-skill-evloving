"""
Modify frontmatter properties in Obsidian notes.
Supports create, update, and delete operations with preview mode.

Usage:
    python frontmatter_modify.py <file_or_pattern> [operation] [options]

Examples:
    # Preview adding a property (shows diff)
    python frontmatter_modify.py "note.md" --create "reviewed:true"
    
    # Apply the change
    python frontmatter_modify.py "note.md" --create "reviewed:true" --apply
    
    # Update existing property
    python frontmatter_modify.py "note.md" --update "status:done" --apply
    
    # Delete a property
    python frontmatter_modify.py "note.md" --delete "draft" --apply
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import difflib

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    parse_frontmatter,
    write_frontmatter,
    set_property_value,
    delete_property,
    infer_property_type
)


def parse_key_value(kv_string: str) -> Tuple[str, Any]:
    """
    Parse a key:value string into property name and typed value.
    
    Args:
        kv_string: String in format "key:value"
        
    Returns:
        Tuple of (property_name, typed_value)
    """
    if ':' not in kv_string:
        raise ValueError(f"Invalid key:value format: {kv_string}")
    
    key, value_str = kv_string.split(':', 1)
    key = key.strip()
    value_str = value_str.strip()
    
    # Infer type
    value = infer_property_type(value_str)
    
    return key, value


def modify_file(file_path: str, operation: str, key: str, value: Any = None) -> Tuple[str, str, bool]:
    """
    Modify frontmatter in a file.
    
    Args:
        file_path: Path to markdown file
        operation: 'create', 'update', or 'delete'
        key: Property name
        value: Property value (for create/update)
        
    Returns:
        Tuple of (original_content, modified_content, changed)
    """
    # Read original file
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Parse frontmatter
    frontmatter, body = parse_frontmatter(file_path)
    
    # Initialize frontmatter if it doesn't exist
    if frontmatter is None:
        frontmatter = {}
    
    # Make a copy for modification
    modified_frontmatter = frontmatter.copy()
    changed = False
    
    # Apply operation
    if operation == 'create' or operation == 'update':
        # Check if property exists for 'create'
        if operation == 'create' and key in modified_frontmatter:
            # Skip if already exists
            return original_content, original_content, False
        
        modified_frontmatter = set_property_value(modified_frontmatter, key, value)
        changed = True
    
    elif operation == 'delete':
        if key in modified_frontmatter:
            modified_frontmatter = delete_property(modified_frontmatter, key)
            changed = True
        else:
            # Property doesn't exist, no change
            return original_content, original_content, False
    
    if not changed:
        return original_content, original_content, False
    
    # Generate modified content
    import yaml
    yaml_str = yaml.dump(modified_frontmatter, 
                         default_flow_style=False, 
                         allow_unicode=True,
                         sort_keys=False)
    modified_content = f"---\n{yaml_str}---\n{body}"
    
    return original_content, modified_content, True


def show_diff(file_path: str, original: str, modified: str) -> str:
    """
    Generate a diff between original and modified content.
    
    Args:
        file_path: Path to file
        original: Original content
        modified: Modified content
        
    Returns:
        Diff string
    """
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"a/{Path(file_path).name}",
        tofile=f"b/{Path(file_path).name}",
        lineterm=''
    )
    
    return ''.join(diff)


def main():
    parser = argparse.ArgumentParser(
        description='Modify frontmatter properties in Obsidian notes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('file', nargs='?', help='Path to markdown file')
    parser.add_argument('--files', nargs='+', help='Multiple file paths')
    
    # Operations
    parser.add_argument('--create', metavar='KEY:VALUE',
                        help='Create new property (format: key:value)')
    parser.add_argument('--update', metavar='KEY:VALUE',
                        help='Update existing property (format: key:value)')
    parser.add_argument('--delete', metavar='KEY',
                        help='Delete property')
    
    # Execution mode
    parser.add_argument('--apply', action='store_true',
                        help='Actually apply changes (default: preview only)')
    parser.add_argument('--force', action='store_true',
                        help='Skip confirmation (use with caution!)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.file and not args.files:
        parser.error("Must specify either file or --files")
    
    # Determine operation
    operations = []
    if args.create:
        operations.append(('create', args.create))
    if args.update:
        operations.append(('update', args.update))
    if args.delete:
        operations.append(('delete', args.delete))
    
    if len(operations) == 0:
        parser.error("Must specify at least one operation: --create, --update, or --delete")
    if len(operations) > 1:
        parser.error("Can only specify one operation at a time")
    
    operation_type, operation_value = operations[0]
    
    # Parse key and value
    if operation_type in ('create', 'update'):
        key, value = parse_key_value(operation_value)
    else:  # delete
        key = operation_value
        value = None
    
    # Get file list
    files = []
    if args.file:
        files.append(args.file)
    if args.files:
        files.extend(args.files)
    
    # Process files
    total_files = len(files)
    changed_files = 0
    
    print(f"\n{'='*80}")
    print(f"Operation: {operation_type.upper()}")
    print(f"Property: {key}")
    if value is not None:
        print(f"Value: {value}")
    print(f"Files to process: {total_files}")
    print(f"Mode: {'APPLY' if args.apply else 'PREVIEW'}")
    print(f"{'='*80}\n")
    
    for file_path in files:
        try:
            original, modified, changed = modify_file(file_path, operation_type, key, value)
            
            if not changed:
                print(f"⊘ {file_path}: No changes needed")
                continue
            
            changed_files += 1
            
            # Show diff
            print(f"\n{'─'*80}")
            print(f"File: {file_path}")
            print(f"{'─'*80}")
            diff = show_diff(file_path, original, modified)
            print(diff)
            
            # Apply changes if requested
            if args.apply:
                if not args.force:
                    # Ask for confirmation
                    response = input(f"\nApply changes to {Path(file_path).name}? [y/N]: ")
                    if response.lower() != 'y':
                        print("  Skipped")
                        continue
                
                # Write changes
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified)
                print(f"✓ Applied changes to {file_path}")
        
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}", file=sys.stderr)
            continue
    
    # Summary
    print(f"\n{'='*80}")
    print(f"Summary:")
    print(f"  Total files: {total_files}")
    print(f"  Changed files: {changed_files}")
    print(f"  Mode: {'APPLIED' if args.apply else 'PREVIEW ONLY'}")
    print(f"{'='*80}\n")
    
    if not args.apply and changed_files > 0:
        print("⚠ Changes were NOT applied. Add --apply flag to apply changes.")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
