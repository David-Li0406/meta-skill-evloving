#!/usr/bin/env python3
"""
Reads project MDX files from src/content/projects/ and outputs a compact summary.
Usage: python3 read_projects.py [command]
  command: list (default), json, detail <slug>
"""

import json
import re
import sys
from pathlib import Path

PROJECTS_DIR = Path(__file__).parent.parent.parent.parent.parent / "src" / "content" / "projects"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from MDX content."""
    match = re.match(r'^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)', content)
    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    body = match.group(2)

    # Simple YAML parsing for our schema
    frontmatter = {}
    current_key = None
    current_list = None

    for line in frontmatter_str.split('\n'):
        # Skip empty lines
        if not line.strip():
            continue

        # Check for list item
        if line.startswith('  - '):
            if current_list is not None:
                current_list.append(line.strip()[2:])
            continue

        # Check for key: value
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()

            if value:
                # Convert types
                if value.lower() == 'true':
                    frontmatter[key] = True
                elif value.lower() == 'false':
                    frontmatter[key] = False
                else:
                    frontmatter[key] = value
                current_list = None
            else:
                # Start of a list
                frontmatter[key] = []
                current_list = frontmatter[key]

            current_key = key

    return frontmatter, body


def get_projects() -> list[dict]:
    """Get all projects with their frontmatter."""
    projects = []

    if not PROJECTS_DIR.exists():
        return projects

    for mdx_file in sorted(PROJECTS_DIR.glob("*.mdx")):
        content = mdx_file.read_text()
        frontmatter, body = parse_frontmatter(content)

        # Count headings for TOC info
        h2_count = len(re.findall(r'^## ', body, re.MULTILINE))
        h3_count = len(re.findall(r'^### ', body, re.MULTILINE))
        word_count = len(body.split())

        projects.append({
            "slug": mdx_file.stem,
            "file": str(mdx_file.relative_to(PROJECTS_DIR.parent.parent.parent)),
            **frontmatter,
            "_h2_count": h2_count,
            "_h3_count": h3_count,
            "_word_count": word_count,
        })

    # Sort by publishedAt (newest first)
    projects.sort(key=lambda p: p.get("publishedAt", ""), reverse=True)

    return projects


def format_list(projects: list[dict]) -> str:
    """Format projects as a compact list."""
    if not projects:
        return "No projects found in src/content/projects/"

    lines = [f"PROJECTS ({len(projects)} total)", ""]

    for i, p in enumerate(projects, 1):
        tags = p.get("tags", [])
        tags_str = f"[{', '.join(tags)}]" if tags else ""
        featured = " *FEATURED*" if p.get("featured") else ""

        lines.append(f"{i}. {p.get('title', 'Untitled')} ({p['slug']}){featured}")
        lines.append(f"   Published: {p.get('publishedAt', 'N/A')} | {p['_word_count']} words | {p['_h2_count']} sections")
        lines.append(f"   Tags: {tags_str}")
        lines.append(f"   {p.get('description', 'No description')[:80]}...")
        lines.append("")

    return '\n'.join(lines)


def format_detail(projects: list[dict], slug: str) -> str:
    """Format detailed info for a single project."""
    project = next((p for p in projects if p["slug"] == slug), None)

    if not project:
        return f"Project not found: {slug}"

    lines = [
        f"PROJECT: {project.get('title', 'Untitled')}",
        f"Slug: {project['slug']}",
        f"File: {project['file']}",
        "",
        "FRONTMATTER:",
        f"  title: {project.get('title', 'N/A')}",
        f"  description: {project.get('description', 'N/A')}",
        f"  publishedAt: {project.get('publishedAt', 'N/A')}",
        f"  updatedAt: {project.get('updatedAt', 'N/A')}",
        f"  tags: {project.get('tags', [])}",
        f"  featured: {project.get('featured', False)}",
        f"  image: {project.get('image', 'N/A')}",
        "",
        "CONTENT STATS:",
        f"  Word count: {project['_word_count']}",
        f"  H2 sections: {project['_h2_count']}",
        f"  H3 subsections: {project['_h3_count']}",
    ]

    return '\n'.join(lines)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "list"
    projects = get_projects()

    if command == "list":
        print(format_list(projects))
    elif command == "json":
        # Remove internal fields for clean JSON output
        clean_projects = [
            {k: v for k, v in p.items() if not k.startswith('_')}
            for p in projects
        ]
        print(json.dumps(clean_projects, indent=2))
    elif command == "detail":
        if len(sys.argv) < 3:
            print("Usage: python3 read_projects.py detail <slug>")
            sys.exit(1)
        slug = sys.argv[2]
        print(format_detail(projects, slug))
    elif command == "slugs":
        # Just output slugs, one per line
        for p in projects:
            print(p["slug"])
    else:
        print(f"Unknown command: {command}")
        print("Usage: python3 read_projects.py [list|json|detail <slug>|slugs]")
        sys.exit(1)


if __name__ == "__main__":
    main()
