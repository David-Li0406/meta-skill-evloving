#!/usr/bin/env python3
"""
Script to generate index.md for Diátaxis-organized documentation.

Scans the specified docs root (default .docs) for subfolders: tutorials, how-to, reference, explanation.
Extracts titles from .md files and generates an index.md file with links organized by category.
"""

import os
import sys

def get_title(filepath):
    """Extract the title from the first line of a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('# '):
                return first_line[2:].strip()
            else:
                # Fallback: use filename as title
                return os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()

def main(docs_root='.docs'):
    """Generate the index.md file."""
    categories = {
        'tutorials': 'Tutorials',
        'how-to': 'How-to Guides',
        'reference': 'Reference',
        'explanation': 'Explanation'
    }

    index_content = """# Copilot Workspace Documentation Index

This index links Diátaxis-organized documentation for the `copilot-fc.json` manifest.

"""

    for folder, section in categories.items():
        path = os.path.join(docs_root, folder)
        if os.path.exists(path) and os.path.isdir(path):
            files = [f for f in os.listdir(path) if f.endswith('.md')]
            if files:
                index_content += f"## {section}\n\n"
                for file in sorted(files):
                    filepath = os.path.join(path, file)
                    title = get_title(filepath)
                    link = f"{folder}/{file}"
                    index_content += f"- [{title}]({link})\n"
                index_content += "\n"

    index_path = os.path.join(docs_root, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"Generated {index_path}")

if __name__ == '__main__':
    docs_root = sys.argv[1] if len(sys.argv) > 1 else '.docs'
    main(docs_root)