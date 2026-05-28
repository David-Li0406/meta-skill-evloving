#!/usr/bin/env python
"""
md2xmind: Convert Markdown tree structure to XMind (.xmind) files.

Creates XMind files from markdown bullet lists, preserving the hierarchical 
structure as topics and subtopics in a mind map format.

Examples:
  md2xmind file.md output.xmind
  md2xmind --title "My Mind Map" input.md output.xmind
"""

from __future__ import annotations
import argparse
import json
import re
import sys
import zipfile
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def generate_id() -> str:
    """Generate a unique ID for XMind topics."""
    return str(uuid4())


def parse_markdown_line(line: str) -> Tuple[int, str]:
    """Parse a markdown line to extract depth and content.
    
    Returns (depth, content) where depth is 0-based.
    Supports both spaces (2 per level) and tabs for indentation.
    """
    # Remove leading spaces/tabs and count indentation
    stripped = line.lstrip()
    if not stripped.startswith('-'):
        return -1, ""  # Not a bullet point
    
    # Count indentation level
    indent_chars = len(line) - len(stripped)
    # Assume 2 spaces per level, but also handle tabs
    if '\t' in line[:indent_chars]:
        depth = line[:indent_chars].count('\t')
    else:
        depth = indent_chars // 2
    
    # Extract content after the dash and any numbering
    content = stripped[1:].strip()
    
    # Remove hierarchical numbering if present (e.g., "1.2.3 Title" -> "Title")
    content = re.sub(r'^\d+(\.\d+)*\s+', '', content)
    
    return depth, content


def parse_markdown_to_tree(content: str) -> List[Dict[str, Any]]:
    """Parse markdown content into a tree structure suitable for XMind."""
    lines = content.strip().split('\n')
    
    # Stack to keep track of parents at each level
    stack: List[Dict[str, Any]] = []
    roots: List[Dict[str, Any]] = []
    
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
            
        depth, text = parse_markdown_line(line)
        if depth == -1 or not text:
            continue
            
        # Create new topic
        topic = {
            "id": generate_id(),
            "title": text,
            "children": {"attached": []}
        }
        
        if depth == 0:
            # Root level topic
            roots.append(topic)
            stack = [topic]
        else:
            # Adjust stack to current depth
            while len(stack) > depth:
                stack.pop()
            
            # Ensure we have a parent at depth-1
            if len(stack) == depth and stack:
                parent = stack[-1]
                parent["children"]["attached"].append(topic)
                stack.append(topic)
            elif len(stack) < depth:
                # Handle case where indentation jumps levels
                # Add to the deepest available parent
                if stack:
                    parent = stack[-1]
                    parent["children"]["attached"].append(topic)
                    # Fill the stack to match current depth
                    while len(stack) < depth + 1:
                        stack.append(topic)
                else:
                    # No parent available, treat as root
                    roots.append(topic)
                    stack = [topic]
            else:
                # len(stack) == depth + 1, normal case
                parent = stack[depth - 1]
                parent["children"]["attached"].append(topic)
                stack = stack[:depth + 1]
                stack[depth] = topic
    
    return roots


def create_xmind_content(topics: List[Dict[str, Any]], title: str = "Mind Map") -> Dict[str, Any]:
    """Create the JSON content structure for XMind file."""
    if not topics:
        # Create a default empty topic if no content
        topics = [{
            "id": generate_id(),
            "title": "Main Topic",
            "children": {"attached": []}
        }]
    
    # If multiple root topics, create a wrapper root
    if len(topics) > 1:
        wrapper_root = {
            "id": generate_id(),
            "title": title,
            "children": {"attached": topics}
        }
        root_topic = wrapper_root
    else:
        root_topic = topics[0]
        # Update the title of single root if provided
        if title != "Mind Map":
            root_topic["title"] = title
    
    # XMind content structure
    content = {
        "id": generate_id(),
        "title": title,
        "rootTopic": root_topic,
        "theme": "robust"
    }
    
    return [content]  # XMind expects an array of sheets


def create_xmind_file(content: List[Dict[str, Any]], output_path: str) -> None:
    """Create an XMind file with the given content."""
    
    # Create the content.json
    content_json = json.dumps(content, indent=2, ensure_ascii=False)
    
    # Create manifest.json
    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {}
        }
    }
    manifest_json = json.dumps(manifest, indent=2)
    
    # Create metadata.json
    metadata = {
        "creator": {
            "name": "md2xmind",
            "version": "1.0.0"
        },
        "created-time": "2025-01-10T00:00:00Z",
        "last-modified-time": "2025-01-10T00:00:00Z"
    }
    metadata_json = json.dumps(metadata, indent=2)
    
    # Create the XMind file (ZIP archive)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('content.json', content_json)
        zf.writestr('manifest.json', manifest_json)
        zf.writestr('metadata.json', metadata_json)


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Markdown tree to XMind (.xmind) file.")
    ap.add_argument("input", help="Path to input Markdown file")
    ap.add_argument("output", help="Path to output XMind file")
    ap.add_argument("--title", default="Mind Map", help="Title for the mind map (default: Mind Map)")
    args = ap.parse_args()
    
    try:
        # Read input markdown file
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except Exception as ex:
        eprint(f"Error reading input file: {ex}")
        return 1
    
    try:
        # Parse markdown to tree structure
        topics = parse_markdown_to_tree(markdown_content)
        
        if not topics:
            eprint("Warning: No valid markdown bullet points found in input file.")
            eprint("Expected format:")
            eprint("- Root topic")
            eprint("  - Child topic")
            eprint("    - Grandchild topic")
        
        # Create XMind content structure
        xmind_content = create_xmind_content(topics, args.title)
        
        # Create XMind file
        create_xmind_file(xmind_content, args.output)
        
        print(f"Successfully created XMind file: {args.output}")
        return 0
        
    except Exception as ex:
        eprint(f"Error creating XMind file: {ex}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())