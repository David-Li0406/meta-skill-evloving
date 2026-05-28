#!/usr/bin/env python3
"""
YAML Frontmatter Parser Utility

A reusable function to parse YAML frontmatter from markdown files.
"""

import sys
import re
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_frontmatter(file_path: str) -> dict:
    """
    Parse YAML frontmatter from a markdown file.

    Args:
        file_path: Path to markdown file

    Returns:
        dict: Parsed frontmatter as dictionary, or empty dict if parsing fails
    """
    try:
        content = Path(file_path).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return {}
    except PermissionError:
        print(f"Error: Permission denied reading file: {file_path}", file=sys.stderr)
        return {}
    except UnicodeDecodeError as e:
        print(f"Error: Failed to decode file {file_path}: {e}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error reading file {file_path}: {type(e).__name__}: {e}", file=sys.stderr)
        return {}

    # Find YAML frontmatter between first two --- markers
    parts = content.split('---')
    if len(parts) < 3:
        return {}

    frontmatter_text = parts[1].strip()
    if not frontmatter_text:
        return {}

    # Parse YAML if available, otherwise use regex for basic key-value pairs
    if HAS_YAML:
        import yaml as yaml_module
        try:
            parsed = yaml_module.safe_load(frontmatter_text)
            return parsed if isinstance(parsed, dict) else {}
        except yaml_module.YAMLError as e:
            print(f"Warning: Failed to parse YAML frontmatter in {file_path}: {e}", file=sys.stderr)
            return {}
        except Exception as e:
            print(f"Unexpected error parsing YAML in {file_path}: {type(e).__name__}: {e}", file=sys.stderr)
            return {}
    else:
        # Fallback: basic regex parsing for key: value pairs
        metadata = {}
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        return metadata


if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) > 1:
        result = parse_frontmatter(sys.argv[1])
        print(result)
    else:
        print("Usage: python frontmatter_parser.py <file_path>")
