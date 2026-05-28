#!/usr/bin/env python3
"""
Generate specs/README.md index from spec frontmatter.

Usage: python index.py [specs_dir]
       specs_dir defaults to ./specs
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            frontmatter[key.strip()] = value.strip().strip('"\'')
    return frontmatter


def find_specs(specs_dir: Path) -> list[dict]:
    """Find all specs and extract their metadata."""
    specs = []

    for item in specs_dir.iterdir():
        # Skip hidden files, templates, and the README itself
        if item.name.startswith(('_', '.')) or item.name == 'README.md':
            continue

        spec_path = None
        if item.is_file() and item.suffix == '.md':
            spec_path = item
        elif item.is_dir() and (item / 'README.md').exists():
            spec_path = item / 'README.md'

        if spec_path:
            content = spec_path.read_text()
            frontmatter = parse_frontmatter(content)

            # Extract title from frontmatter or first heading
            title = frontmatter.get('title', '')
            if not title:
                heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = heading_match.group(1) if heading_match else item.stem.replace('-', ' ').title()

            specs.append({
                'name': item.name,
                'path': item.name if item.is_dir() else item.name,
                'link': f"{item.name}/README.md" if item.is_dir() else item.name,
                'title': title,
                'status': frontmatter.get('status', 'planned').lower(),
                'date': frontmatter.get('date', ''),
                'priority': int(frontmatter.get('priority', 999)),
            })

    return specs


def generate_readme(specs: list[dict]) -> str:
    """Generate the README.md content."""
    # Group by status
    in_progress = [s for s in specs if s['status'] == 'in-progress']
    planned = [s for s in specs if s['status'] == 'planned']
    completed = [s for s in specs if s['status'] == 'completed']
    archived = [s for s in specs if s['status'] == 'archived']

    # Sort each group by priority, then by name
    for group in [in_progress, planned, completed, archived]:
        group.sort(key=lambda s: (s['priority'], s['name']))

    lines = [
        "# Specifications",
        "",
        f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
    ]

    if in_progress:
        lines.extend(["## In Progress", ""])
        for spec in in_progress:
            lines.append(f"- [{spec['title']}]({spec['link']})")
        lines.append("")

    if planned:
        lines.extend(["## Planned", ""])
        for spec in planned:
            lines.append(f"- [{spec['title']}]({spec['link']})")
        lines.append("")

    if completed:
        lines.extend(["## Completed", ""])
        for spec in completed:
            lines.append(f"- [{spec['title']}]({spec['link']})")
        lines.append("")

    if archived:
        lines.extend(["## Archived", ""])
        for spec in archived:
            lines.append(f"- [{spec['title']}]({spec['link']})")
        lines.append("")

    if not specs:
        lines.extend([
            "*No specifications found.*",
            "",
            "Create a new spec with `/specs init <feature-name>`",
            "",
        ])

    return '\n'.join(lines)


def main():
    specs_dir = Path(sys.argv[1] if len(sys.argv) > 1 else './specs')

    if not specs_dir.exists():
        print(f"Error: {specs_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    specs = find_specs(specs_dir)
    readme_content = generate_readme(specs)

    readme_path = specs_dir / 'README.md'
    readme_path.write_text(readme_content)
    print(f"Generated {readme_path} with {len(specs)} spec(s)")


if __name__ == '__main__':
    main()
