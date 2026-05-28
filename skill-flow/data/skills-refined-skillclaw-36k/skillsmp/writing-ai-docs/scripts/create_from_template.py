#!/usr/bin/env python3
"""
Create a new documentation file from a template.

This script copies a template, updates dates to current date,
and saves to the specified location.
"""

import sys
import re
from pathlib import Path
from datetime import date


def update_dates_in_content(content: str) -> str:
    """Update YYYY-MM-DD placeholders to current date."""
    today = date.today().isoformat()

    # Replace YYYY-MM-DD with current date
    content = content.replace('YYYY-MM-DD', today)

    return content


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: create_from_template.py <template-name> <output-path>")
        print()
        print("Examples:")
        print("  python scripts/create_from_template.py api-endpoint docs/api/get-users.md")
        print("  python scripts/create_from_template.py how-to-guide docs/guides/deploy.md")
        print("  python scripts/create_from_template.py tutorial docs/tutorials/first-app.md")
        print()
        print("Available templates:")
        print("  Run: python scripts/list_templates.py")
        sys.exit(1)

    template_name = sys.argv[1]
    output_path = Path(sys.argv[2])

    # Get templates directory
    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent / 'templates'

    if not templates_dir.exists():
        print("❌ Error: Templates directory not found")
        sys.exit(1)

    # Find template file
    # Support with or without .md extension
    if not template_name.endswith('.md'):
        template_name += '.md'

    template_file = templates_dir / template_name

    if not template_file.exists():
        print(f"❌ Error: Template '{template_name}' not found")
        print()
        print("Available templates:")
        print("  Run: python scripts/list_templates.py")
        sys.exit(1)

    # Check if output file already exists
    if output_path.exists():
        print(f"❌ Error: Output file already exists: {output_path}")
        print()
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            sys.exit(0)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read template
    try:
        content = template_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading template: {e}")
        sys.exit(1)

    # Update dates
    content = update_dates_in_content(content)

    # Write output
    try:
        output_path.write_text(content, encoding='utf-8')
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        sys.exit(1)

    print(f"✅ Created: {output_path}")
    print()
    print("📝 Next steps:")
    print(f"   1. Edit {output_path}")
    print("   2. Replace all [placeholders] with actual content")
    print("   3. Update frontmatter fields")
    print("   4. Validate:")
    print(f"      $ python scripts/check_doc_quality.py {output_path}")
    print(f"      $ bash scripts/lint_markdown.sh {output_path}")
    print()
    print("💡 For full documentation structure validation, use maintaining-docs skill")
    print()


if __name__ == "__main__":
    main()
