#!/usr/bin/env python3
"""
List all available documentation templates with descriptions.

This script scans the templates directory and displays available templates
organized by category with their descriptions.
"""

import sys
from pathlib import Path
import yaml
import re


def extract_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)

        if match:
            frontmatter_text = match.group(1)
            return yaml.safe_load(frontmatter_text) or {}
    except Exception as e:
        print(f"Warning: Could not read {file_path.name}: {e}", file=sys.stderr)

    return {}


def categorize_template(filename: str, frontmatter: dict) -> str:
    """Determine template category."""
    # High-frequency templates
    high_freq = ['api-endpoint', 'how-to-guide', 'troubleshooting-entry',
                 'cli-command', 'config-option']

    # Medium-frequency templates
    medium_freq = ['tutorial', 'concept-explanation', 'error-reference']

    # One-time templates
    one_time = ['getting-started', 'installation-guide']

    # Special documentation
    special = ['CHANGELOG', 'README', 'adr-template', 'personas', 'faq', 'glossary']

    base_name = filename.replace('.md', '')

    if base_name in high_freq:
        return 'high-frequency'
    elif base_name in medium_freq:
        return 'medium-frequency'
    elif base_name in one_time:
        return 'one-time'
    elif base_name in special:
        return 'special'
    else:
        return 'other'


def main():
    """Main entry point."""
    # Get templates directory
    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent / 'templates'

    if not templates_dir.exists():
        print("❌ Error: Templates directory not found")
        sys.exit(1)

    # Scan templates
    templates = {}
    for template_file in sorted(templates_dir.glob('*.md')):
        frontmatter = extract_frontmatter(template_file)
        category = categorize_template(template_file.name, frontmatter)

        if category not in templates:
            templates[category] = []

        templates[category].append({
            'filename': template_file.name,
            'title': frontmatter.get('title', 'N/A'),
            'description': frontmatter.get('description', 'No description available'),
            'type': frontmatter.get('type', 'N/A')
        })

    # Display templates
    print("📋 Available Documentation Templates")
    print("=" * 70)
    print()

    # Category display order and titles
    categories = [
        ('high-frequency', '🔥 High-Frequency Templates',
         'Use multiple times per project'),
        ('medium-frequency', '📦 Medium-Frequency Templates',
         'Use several times per project'),
        ('one-time', '⭐ One-Time Essential Templates',
         'Project setup documentation'),
        ('special', '📚 Special Documentation Templates',
         'Specific documentation types'),
        ('other', '🔧 Other Templates',
         'General purpose templates')
    ]

    for category_key, category_title, category_desc in categories:
        if category_key not in templates:
            continue

        print(f"{category_title}")
        print(f"   {category_desc}")
        print()

        for template in templates[category_key]:
            filename = template['filename']
            description = template['description']

            # Clean up description for display
            if description.startswith('[') and description.endswith(']'):
                description = "Template for specific content (see file)"

            # Truncate long descriptions
            if len(description) > 80:
                description = description[:77] + "..."

            print(f"   • {filename:<30} {description}")

        print()

    # Usage instructions
    print("=" * 70)
    print()
    print("📖 Usage:")
    print()
    print("   Create from template:")
    print("   $ python scripts/create_from_template.py <template-name> <output-path>")
    print()
    print("   Example:")
    print("   $ python scripts/create_from_template.py api-endpoint docs/api/get-users.md")
    print()
    print("   Validate document:")
    print("   $ python scripts/check_doc_quality.py docs/api/get-users.md")
    print("   $ bash scripts/lint_markdown.sh docs/api/get-users.md")
    print()
    print("💡 For full documentation structure validation, use maintaining-docs skill")
    print()


if __name__ == "__main__":
    main()
