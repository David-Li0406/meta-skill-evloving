"""
Utility functions for Obsidian frontmatter operations.
Handles YAML parsing, file operations, and property type validation.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


def find_markdown_files(vault_path: str) -> List[str]:
    """
    Recursively find all markdown files in the vault.
    
    Args:
        vault_path: Path to Obsidian vault
        
    Returns:
        List of absolute paths to .md files
    """
    vault = Path(vault_path)
    if not vault.exists():
        raise ValueError(f"Vault path does not exist: {vault_path}")
    
    md_files = []
    for md_file in vault.rglob("*.md"):
        md_files.append(str(md_file.absolute()))
    
    return md_files


def parse_frontmatter(file_path: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Parse YAML frontmatter from a markdown file.
    
    Args:
        file_path: Path to markdown file
        
    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
        Returns (None, full_content) if no frontmatter found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {e}")
    
    # Check for frontmatter (must start with ---)
    if not content.startswith('---'):
        return None, content
    
    # Find the closing ---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return None, content
    
    yaml_content = match.group(1)
    body_content = match.group(2)
    
    try:
        frontmatter = yaml.safe_load(yaml_content)
        if frontmatter is None:
            frontmatter = {}
        return frontmatter, body_content
    except yaml.YAMLError as e:
        # Malformed YAML
        raise ValueError(f"Invalid YAML in {file_path}: {e}")


def write_frontmatter(file_path: str, frontmatter: Dict[str, Any], content: str) -> None:
    """
    Write frontmatter and content back to a markdown file.
    
    Args:
        file_path: Path to markdown file
        frontmatter: Dictionary of frontmatter properties
        content: Body content (without frontmatter)
    """
    # Convert frontmatter to YAML
    yaml_str = yaml.dump(frontmatter, 
                         default_flow_style=False, 
                         allow_unicode=True,
                         sort_keys=False)
    
    # Construct full content
    full_content = f"---\n{yaml_str}---\n{content}"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
    except Exception as e:
        raise IOError(f"Error writing file {file_path}: {e}")


def get_property_value(frontmatter: Optional[Dict[str, Any]], property_name: str) -> Any:
    """
    Get a property value from frontmatter, handling nested properties.
    
    Args:
        frontmatter: Frontmatter dictionary
        property_name: Property name (supports dot notation for nested)
        
    Returns:
        Property value or None if not found
    """
    if frontmatter is None:
        return None
    
    # Handle nested properties (e.g., "metadata.author")
    parts = property_name.split('.')
    value = frontmatter
    
    for part in parts:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None
    
    return value


def set_property_value(frontmatter: Dict[str, Any], property_name: str, value: Any) -> Dict[str, Any]:
    """
    Set a property value in frontmatter, handling nested properties.
    
    Args:
        frontmatter: Frontmatter dictionary
        property_name: Property name (supports dot notation for nested)
        value: Value to set
        
    Returns:
        Updated frontmatter dictionary
    """
    parts = property_name.split('.')
    
    if len(parts) == 1:
        frontmatter[property_name] = value
    else:
        # Handle nested properties
        current = frontmatter
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    
    return frontmatter


def delete_property(frontmatter: Dict[str, Any], property_name: str) -> Dict[str, Any]:
    """
    Delete a property from frontmatter.
    
    Args:
        frontmatter: Frontmatter dictionary
        property_name: Property name to delete
        
    Returns:
        Updated frontmatter dictionary
    """
    parts = property_name.split('.')
    
    if len(parts) == 1:
        if property_name in frontmatter:
            del frontmatter[property_name]
    else:
        # Handle nested properties
        current = frontmatter
        for part in parts[:-1]:
            if part not in current:
                return frontmatter
            current = current[part]
        if parts[-1] in current:
            del current[parts[-1]]
    
    return frontmatter


def infer_property_type(value_str: str) -> Any:
    """
    Infer the type of a property value from a string.
    
    Args:
        value_str: String representation of value
        
    Returns:
        Typed value (bool, int, float, datetime, list, or str)
    """
    # Boolean
    if value_str.lower() in ('true', 'yes', 'on'):
        return True
    if value_str.lower() in ('false', 'no', 'off'):
        return False
    
    # Number
    try:
        if '.' in value_str:
            return float(value_str)
        else:
            return int(value_str)
    except ValueError:
        pass
    
    # Date/DateTime
    try:
        # Try ISO datetime
        return datetime.fromisoformat(value_str)
    except ValueError:
        pass
    
    # List (comma-separated or JSON array)
    if value_str.startswith('[') and value_str.endswith(']'):
        try:
            import json
            return json.loads(value_str)
        except:
            pass
    
    if ',' in value_str:
        return [item.strip() for item in value_str.split(',')]
    
    # Default to string
    return value_str


def property_matches(value: Any, operator: str, target: Any) -> bool:
    """
    Check if a property value matches a condition.
    
    Args:
        value: Property value to check
        operator: Comparison operator (exists, not-exists, equals, contains, gt, lt)
        target: Target value to compare against
        
    Returns:
        True if condition matches
    """
    if operator == 'exists':
        return value is not None
    
    if operator == 'not-exists':
        return value is None
    
    if value is None:
        return False
    
    if operator == 'equals':
        return value == target
    
    if operator == 'contains':
        if isinstance(value, list):
            return target in value
        if isinstance(value, str):
            return target in value
        return False
    
    if operator == 'gt':
        try:
            return value > target
        except TypeError:
            return False
    
    if operator == 'lt':
        try:
            return value < target
        except TypeError:
            return False
    
    return False


def format_value(value: Any) -> str:
    """
    Format a property value for display.
    
    Args:
        value: Property value
        
    Returns:
        Formatted string representation
    """
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return str(value)
