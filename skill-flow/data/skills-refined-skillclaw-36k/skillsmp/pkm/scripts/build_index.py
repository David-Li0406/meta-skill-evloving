#!/usr/bin/env python3
"""
PKM Index Builder
Scans /github/*.md files and generates a searchable index.
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    frontmatter = {}
    body = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_content = parts[1].strip()
            body = parts[2].strip()

            current_key = None
            current_list = []

            for line in fm_content.split('\n'):
                line = line.rstrip()
                if not line:
                    continue

                # Check for list item
                if line.startswith(' - ') or line.startswith('  - '):
                    item = line.strip().lstrip('- ').strip()
                    current_list.append(item)
                elif ':' in line:
                    # Save previous list if exists
                    if current_key and current_list:
                        frontmatter[current_key] = current_list
                        current_list = []

                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    current_key = key

                    if value:
                        frontmatter[key] = value

            # Save final list
            if current_key and current_list:
                frontmatter[current_key] = current_list

    return frontmatter, body


def extract_summary(body: str) -> str:
    """Extract summary from markdown body (first paragraph before code blocks)."""
    # Remove code blocks
    body = re.sub(r'```[\s\S]*?```', '', body)

    # Get first meaningful paragraph
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]

    if paragraphs:
        # Clean up the first paragraph
        summary = paragraphs[0]
        # Remove markdown links but keep text
        summary = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', summary)
        # Remove other markdown formatting
        summary = re.sub(r'[*_`]', '', summary)
        return summary.strip()

    return ""


def load_term_mappings(base_path: Path) -> dict:
    """Load Korean/English term mappings from markdown file."""
    mappings = {}
    reverse_mappings = {}

    mapping_file = base_path / 'references' / 'term_mappings.md'

    if mapping_file.exists():
        content = mapping_file.read_text(encoding='utf-8')

        # Parse table rows
        for line in content.split('\n'):
            if '|' in line and not line.strip().startswith('|--'):
                parts = [p.strip() for p in line.split('|')]
                parts = [p for p in parts if p]

                if len(parts) >= 2:
                    english = parts[0].lower()
                    korean = parts[1]

                    if english and korean and english not in ['english', '영어']:
                        mappings[english] = korean
                        reverse_mappings[korean.lower()] = english

    return {'en_to_ko': mappings, 'ko_to_en': reverse_mappings}


def normalize_tags(tags: list, term_mappings: dict) -> list:
    """Normalize tags with Korean/English translations."""
    normalized = set()

    for tag in tags:
        normalized.add(tag)
        tag_lower = tag.lower()

        # Add English translation if Korean
        if tag_lower in term_mappings.get('ko_to_en', {}):
            normalized.add(term_mappings['ko_to_en'][tag_lower])

        # Add Korean translation if English
        if tag_lower in term_mappings.get('en_to_ko', {}):
            normalized.add(term_mappings['en_to_ko'][tag_lower])

    return list(normalized)


def build_searchable_text(entry: dict) -> str:
    """Build combined searchable text from all fields."""
    parts = []

    # Add filename (owner/repo)
    parts.append(entry.get('id', '').replace('__', ' '))

    # Add aliases
    if entry.get('aliases'):
        parts.extend(entry['aliases'])

    # Add tags (both original and normalized)
    if entry.get('tags'):
        parts.extend(entry['tags'])
    if entry.get('tags_normalized'):
        parts.extend(entry['tags_normalized'])

    # Add language
    if entry.get('language'):
        parts.append(entry['language'])

    # Add summary
    if entry.get('summary'):
        parts.append(entry['summary'])

    return ' '.join(parts).lower()


def should_rebuild_index(github_path: Path, index_path: Path) -> bool:
    """Check if index needs to be rebuilt."""
    if not index_path.exists():
        return True

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)

        # Check file count
        md_files = list(github_path.glob('*.md'))
        if len(md_files) != index.get('file_count', 0):
            print(f"File count changed: {index.get('file_count', 0)} -> {len(md_files)}")
            return True

        # Check latest modification time
        index_mtime = index_path.stat().st_mtime
        for md_file in md_files:
            if md_file.stat().st_mtime > index_mtime:
                print(f"File modified: {md_file.name}")
                return True

        return False

    except (json.JSONDecodeError, KeyError):
        return True


def build_index(base_path: Path = None, force: bool = False) -> dict:
    """Build the search index from markdown files."""
    if base_path is None:
        base_path = Path(__file__).parent.parent

    project_root = base_path.parent.parent.parent
    github_path = project_root / 'github'
    index_path = base_path / 'data' / 'index.json'

    # Check if rebuild is needed
    if not force and not should_rebuild_index(github_path, index_path):
        print("Index is up to date.")
        with open(index_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    print(f"Building index from {github_path}...")

    # Load term mappings
    term_mappings = load_term_mappings(base_path)

    entries = []
    md_files = sorted(github_path.glob('*.md'))

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            frontmatter, body = parse_frontmatter(content)

            # Create entry ID from filename
            entry_id = md_file.stem

            # Get tags and normalize
            tags = frontmatter.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]
            tags_normalized = normalize_tags(tags, term_mappings)

            # Get aliases
            aliases = frontmatter.get('aliases', [])
            if isinstance(aliases, str):
                aliases = [aliases]

            entry = {
                'id': entry_id,
                'filename': md_file.name,
                'url': frontmatter.get('url', ''),
                'language': frontmatter.get('Language', ''),
                'tags': tags,
                'tags_normalized': tags_normalized,
                'aliases': aliases,
                'summary': extract_summary(body)
            }

            # Build searchable text
            entry['searchable_text'] = build_searchable_text(entry)

            entries.append(entry)

        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    # Build the index
    index = {
        'version': '1.0',
        'generated_at': datetime.now().isoformat(),
        'file_count': len(entries),
        'entries': entries,
        'term_index': term_mappings.get('en_to_ko', {})
    }

    # Save index
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Index built successfully: {len(entries)} entries")
    return index


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Build PKM search index')
    parser.add_argument('--force', '-f', action='store_true', help='Force rebuild index')
    args = parser.parse_args()

    build_index(force=args.force)
