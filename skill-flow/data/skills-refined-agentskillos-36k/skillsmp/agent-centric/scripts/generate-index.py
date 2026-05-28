#!/usr/bin/env python3
"""
Generate index files for the Agent Centric framework.

Managed by: agent-centric skill (auto-updated, do not edit manually)
To disable auto-update, add this filename to disableAutoUpdateScripts in config.json.

Usage:
    generate-index.py                    # Auto-detect from CLAUDE_PROJECT_DIR
    generate-index.py <project_dir>      # Manual override

Generates:
    - INDEX-TAGS.md: Files with their tags
    - INDEX-AGD-RELATIONS.md: AGD obsoletes/updates relationships
"""

import sys
from pathlib import Path

from utils import (
    AGD_PATTERN,
    DECISIONS_DIR,
    RELATION_FIELDS,
    find_agd_file,
    get_agd_sort_key,
    get_agents_dir,
    get_decisions_dir,
    get_project_dir,
    parse_frontmatter,
)


def collect_agd_data(decisions_dir: Path) -> tuple[list, list]:
    """Collect tags and relations data from all AGD files."""
    tags_data = []       # [(relative_path, [tags])]
    relations_data = []  # [(source_path, target_path, relation_type)]

    for agd_file in sorted(decisions_dir.glob(AGD_PATTERN), key=lambda f: get_agd_sort_key(f.name)):
        try:
            content = agd_file.read_text()
        except IOError:
            continue

        frontmatter = parse_frontmatter(content)
        relative_path = f"{DECISIONS_DIR}/{agd_file.name}"

        # Collect tags
        if 'tags' in frontmatter and frontmatter['tags']:
            tags = [f"#{t.strip()}" for t in frontmatter['tags'].split(',') if t.strip()]
            if tags:
                tags_data.append((relative_path, tags))

        # Collect relationships
        for field, rel_type in RELATION_FIELDS:
            if field in frontmatter and frontmatter[field]:
                refs = [r.strip() for r in frontmatter[field].split(',') if r.strip()]
                for ref in refs:
                    target_file = find_agd_file(decisions_dir, ref)
                    if target_file:
                        target_path = f"{DECISIONS_DIR}/{target_file.name}"
                        relations_data.append((relative_path, target_path, rel_type))

    return tags_data, relations_data


def write_tags_index(agents_dir: Path, tags_data: list) -> None:
    """Write INDEX-TAGS.md file."""
    content = "# Tags Index\n\n"
    content += "<!-- AUTO-GENERATED - DO NOT EDIT -->\n"
    content += "<!-- Search with: grep \"#tagname\" INDEX-TAGS.md -->\n\n"

    for path, tags in sorted(tags_data, key=lambda x: get_agd_sort_key(x[0])):
        content += f"{path}: {', '.join(tags)}\n"

    (agents_dir / 'INDEX-TAGS.md').write_text(content)


def write_relations_index(agents_dir: Path, relations_data: list) -> None:
    """Write INDEX-AGD-RELATIONS.md file."""
    content = "# AGD Relations Index\n\n"
    content += "<!-- AUTO-GENERATED - DO NOT EDIT -->\n"
    content += "<!-- -(o)-> : obsoletes, -(u)-> : updates -->\n"
    content += "<!-- Search with: grep \"AGD-001\" INDEX-AGD-RELATIONS.md -->\n\n"

    for source, target, rel_type in sorted(relations_data, key=lambda x: get_agd_sort_key(x[0])):
        content += f"{source} -({rel_type})-> {target}\n"

    (agents_dir / 'INDEX-AGD-RELATIONS.md').write_text(content)


def generate_indexes(project_dir: Path) -> tuple[int, int]:
    """Generate all index files. Returns (tags_count, relations_count)."""
    agents_dir = get_agents_dir(project_dir)
    decisions_dir = get_decisions_dir(project_dir)

    if not decisions_dir.exists():
        return 0, 0

    tags_data, relations_data = collect_agd_data(decisions_dir)
    write_tags_index(agents_dir, tags_data)
    write_relations_index(agents_dir, relations_data)

    return len(tags_data), len(relations_data)


def main():
    project_dir = get_project_dir()
    tags_count, relations_count = generate_indexes(project_dir)
    print(f"✓ Index updated: {tags_count} files tagged, {relations_count} relations")
    sys.exit(0)


if __name__ == '__main__':
    main()
