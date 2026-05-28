#!/usr/bin/env python3
"""Validate Pandoc markdown file with YAML frontmatter"""

import yaml
import sys
import os
import re
from pathlib import Path


def validate_file(filepath):
    """Validate markdown file with YAML frontmatter

    Returns:
        tuple: (is_valid, errors, warnings)
    """
    issues = []
    warnings = []

    # Check file exists
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"], []

    # Read file content
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Failed to read file: {e}"], []

    # Check for YAML frontmatter
    if not content.startswith('---'):
        issues.append("No YAML frontmatter found (should start with '---')")
        return False, issues, warnings

    # Find end of YAML block
    try:
        yaml_end = content.index('---', 3)
        yaml_content = content[3:yaml_end]
    except ValueError:
        issues.append("YAML frontmatter not properly closed (missing second '---')")
        return False, issues, warnings

    # Check for tabs in YAML
    if '\t' in yaml_content:
        issues.append("YAML contains tabs - use spaces for indentation")

    # Parse YAML
    try:
        metadata = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        issues.append(f"YAML syntax error: {e}")
        return False, issues, warnings

    if metadata is None:
        metadata = {}

    # Get file directory for relative path resolution
    file_dir = os.path.dirname(os.path.abspath(filepath))

    # Validate bibliography file
    if 'bibliography' in metadata:
        bib_path = metadata['bibliography']
        # Handle relative paths
        if not os.path.isabs(bib_path):
            bib_path = os.path.join(file_dir, bib_path)

        if not os.path.exists(bib_path):
            issues.append(f"Bibliography file not found: {metadata['bibliography']}")

    # Validate CSL file
    if 'csl' in metadata:
        csl_path = metadata['csl']
        # Handle relative paths
        if not os.path.isabs(csl_path):
            csl_path = os.path.join(file_dir, csl_path)

        if not os.path.exists(csl_path):
            issues.append(f"CSL file not found: {metadata['csl']}")

    # Check for images in markdown content
    markdown_content = content[yaml_end + 3:]
    image_pattern = r'!\[.*?\]\((.*?)\)'
    images = re.findall(image_pattern, markdown_content)

    missing_images = []
    for img_path in images:
        # Skip URLs
        if img_path.startswith(('http://', 'https://')):
            continue

        # Handle relative paths
        if not os.path.isabs(img_path):
            img_path = os.path.join(file_dir, img_path)

        if not os.path.exists(img_path):
            missing_images.append(img_path)

    if missing_images:
        issues.append(f"Missing images: {', '.join(missing_images)}")

    # Check recommended fields
    recommended_fields = ['title', 'author']
    for field in recommended_fields:
        if field not in metadata or not metadata[field]:
            warnings.append(f"Missing recommended field: {field}")

    # Check date format
    if 'date' in metadata:
        date_val = str(metadata['date'])
        # Warn if date looks like it needs formatting
        if date_val.lower() in ['date', 'todo', 'tbd']:
            warnings.append(f"Date field needs to be filled in: '{date_val}'")

    # Check for common mistakes
    if 'documentclass' in metadata:
        valid_classes = ['article', 'report', 'book', 'beamer']
        if metadata['documentclass'] not in valid_classes:
            warnings.append(f"Unusual documentclass: '{metadata['documentclass']}' (common: {', '.join(valid_classes)})")

    # Bibliography + CSL warning
    if 'bibliography' in metadata and 'csl' not in metadata:
        warnings.append("Bibliography specified but no CSL file (will use default citation style)")

    return len(issues) == 0, issues, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: validate.py <file>")
        sys.exit(1)

    filepath = sys.argv[1]
    is_valid, errors, warnings = validate_file(filepath)

    print("Pandoc Markdown Validation")
    print("=" * 40)
    print(f"File: {filepath}")
    print()

    # Print errors
    if errors:
        print("❌ Errors:")
        for error in errors:
            print(f"  • {error}")
        print()

    # Print warnings
    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"  • {warning}")
        print()

    # Print result
    if is_valid:
        if warnings:
            print(f"✅ Validation passed with {len(warnings)} warning(s)")
        else:
            print("✅ Validation passed - ready to convert!")
        sys.exit(0)
    else:
        print(f"❌ Validation failed with {len(errors)} error(s)")
        sys.exit(1)


if __name__ == '__main__':
    main()
