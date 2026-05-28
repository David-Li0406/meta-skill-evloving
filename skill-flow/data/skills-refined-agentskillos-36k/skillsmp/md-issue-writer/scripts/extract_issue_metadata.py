#!/usr/bin/env python3
"""
Extract MD Issue Metadata and Generate Report Table

This script extracts metadata from issue documents in .docs/issues or _docs/issues,
generates summary statistics, and creates an index.md with a table of all issues.
"""

import os
import re
from pathlib import Path
from datetime import datetime
import yaml

def get_issues_folder():
    """Determine the issues folder: check _docs first, then .docs"""
    if Path("_docs/issues").exists():
        return Path("_docs/issues")
    else:
        return Path(".docs/issues")

def parse_yaml_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    metadata = {
        'date': '',
        'type': '',
        'severity': '',
        'status': ''
    }

    # Check if content starts with YAML frontmatter
    yaml_match = re.match(r'^\s*---\s*\n(.*?)\n---', content, re.DOTALL)
    if yaml_match:
        yaml_block = yaml_match.group(1)
        try:
            parsed = yaml.safe_load(yaml_block)
            if isinstance(parsed, dict):
                metadata.update({
                    'date': parsed.get('date', ''),
                    'type': parsed.get('type', ''),
                    'severity': parsed.get('severity', ''),
                    'status': parsed.get('status', '')
                })
        except yaml.YAMLError:
            pass  # If YAML parsing fails, treat as legacy

    return metadata if metadata['date'] or metadata['type'] or metadata['status'] else None

def parse_legacy_metadata(content):
    """Parse legacy metadata format from markdown content."""
    metadata = {
        'date': '',
        'type': '',
        'severity': '',
        'status': ''
    }

    # Extract the header part before first heading or ---
    header = re.split(r'---', content)[0]

    # Extract metadata using regex
    date_match = re.search(r'\*\*Date:\*\*\s*([^\r\n]+)', header)
    if date_match:
        metadata['date'] = date_match.group(1).strip()

    type_match = re.search(r'\*\*(?:Issue\s+)?Type:\*\*\s*([^\r\n]+)', header)
    if type_match:
        metadata['type'] = type_match.group(1).strip()

    severity_match = re.search(r'\*\*Severity:\*\*\s*([^\r\n]+)', header)
    if severity_match:
        metadata['severity'] = severity_match.group(1).strip()

    status_match = re.search(r'\*\*Status:\*\*\s*([^\r\n]+)', header)
    if status_match:
        metadata['status'] = status_match.group(1).strip()

    return metadata

def main():
    issues_path = get_issues_folder()

    # Get all .md files except index.md
    files = [f for f in issues_path.glob("*.md") if f.name != "index.md"]

    report = []

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[ERROR] Could not read {file_path.name}: {e}")
            continue

        # Try parsing YAML frontmatter first
        metadata = parse_yaml_frontmatter(content)

        # Fallback to legacy format if no YAML found
        if metadata is None:
            metadata = parse_legacy_metadata(content)
            format_type = "Legacy"
        else:
            format_type = "YAML"

        # Warn if required fields are missing
        warnings = []
        if not metadata['date']:
            warnings.append("Missing Date")
        if not metadata['type']:
            warnings.append("Missing Type")
        if not metadata['status']:
            warnings.append("Missing Status")

        if warnings:
            print(f"[WARN] {file_path.name}: {', '.join(warnings)}")

        # Add to report
        report.append({
            'file': file_path.name,
            'date': metadata['date'],
            'type': metadata['type'],
            'severity': metadata['severity'],
            'status': metadata['status'],
            'format': format_type
        })

    # Generate summary statistics
    total_files = len(report)
    yaml_count = sum(1 for item in report if item['format'] == "YAML")
    legacy_count = sum(1 for item in report if item['format'] == "Legacy")
    missing_date = sum(1 for item in report if not item['date'])
    missing_type = sum(1 for item in report if not item['type'])
    missing_status = sum(1 for item in report if not item['status'])

    print("\n===================================")
    print("Issue Metadata Extraction Summary")
    print("===================================")
    print(f"Total files: {total_files}")
    print(f"YAML frontmatter: {yaml_count}")
    print(f"Legacy format: {legacy_count}")
    print("\nMissing required fields:")
    print(f"  Date: {missing_date}")
    print(f"  Type: {missing_type}")
    print(f"  Status: {missing_status}")

    # Generate Markdown table
    output_lines = []
    output_lines.append("# Issue Metadata Index")
    output_lines.append("")
    output_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append("")
    output_lines.append("**Statistics:**")
    output_lines.append(f"- Total Issues: {total_files}")
    output_lines.append(f"- YAML Format: {yaml_count}")
    output_lines.append(f"- Legacy Format: {legacy_count}")
    output_lines.append("")
    output_lines.append("| File | Date | Type | Status | Severity | Format |")
    output_lines.append("|------|------|------|--------|----------|--------|")

    # Sort by date descending
    def sort_key(item):
        date_str = item['date']
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return datetime.min

    for item in sorted(report, key=sort_key, reverse=True):
        output_lines.append(f"| {item['file']} | {item['date']} | {item['type']} | {item['status']} | {item['severity']} | {item['format']} |")

    # Output to index.md
    output_path = issues_path / "index.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"\nReport generated at {output_path}")

if __name__ == "__main__":
    main()