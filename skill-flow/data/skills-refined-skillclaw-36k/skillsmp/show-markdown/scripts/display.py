#!/usr/bin/env python3
"""
Display markdown content in a browser using marked.js via CDN.

Usage:
    python display.py <file.md>
    python display.py --content "# Title\\n\\nContent"
"""

import argparse
import html
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def get_script_dir() -> Path:
    """Get the directory where this script is located."""
    return Path(__file__).parent


def read_template() -> str:
    """Read the HTML template file."""
    template_path = get_script_dir() / "template.html"

    if not template_path.exists():
        print(f"Error: Template file not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    return template_path.read_text(encoding="utf-8")


def read_markdown_file(file_path: str) -> str:
    """Read markdown content from a file."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    return path.read_text(encoding="utf-8")


def escape_for_js(markdown: str) -> str:
    """Escape markdown content for safe embedding in JavaScript."""
    # First, escape </script> tags to prevent premature script tag closure
    # This must be done BEFORE JSON escaping because we're modifying the content
    escaped = markdown.replace("</script>", "<\\/script>")

    # Return as a JSON string for proper escaping (quotes, newlines, etc.)
    return json.dumps(escaped, ensure_ascii=False)


def extract_title_from_markdown(markdown: str) -> str | None:
    """Extract the first heading from markdown content."""
    for line in markdown.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line.startswith('## ') or line.startswith('### '):
            return line.split(' ', 1)[1].strip()
    return None


def get_title(markdown: str, file_path: str | None, explicit_title: str | None) -> str:
    """Get title with fallback chain: explicit > heading > filename > default."""
    if explicit_title:
        return explicit_title

    # Try to extract from markdown content
    extracted = extract_title_from_markdown(markdown)
    if extracted:
        return extracted

    # Fall back to filename (without extension)
    if file_path:
        return Path(file_path).stem

    return "Markdown Preview"


def generate_html(markdown: str, title: str) -> str:
    """Generate HTML from markdown content using the template."""
    template = read_template()
    escaped_markdown = escape_for_js(markdown)
    escaped_title = html.escape(title)
    return template.replace("{{MARKDOWN_CONTENT}}", escaped_markdown)\
                   .replace("{{TITLE}}", escaped_title)


def open_in_browser(html_path: Path) -> None:
    """Open HTML file in the default browser using xdg-open."""
    try:
        subprocess.run(["xdg-open", str(html_path)], check=True)
    except FileNotFoundError:
        print("Error: xdg-open not found. Please install it to open files in browser.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to open browser: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display markdown content in a browser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md
  %(prog)s --content "# Title\\n\\nContent"
  %(prog)s README.md --title "My Custom Title"
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="Path to markdown file")
    group.add_argument("--content", "-c", help="Raw markdown content")

    parser.add_argument("--title", "-t", help="Custom title for the page", default=None)

    args = parser.parse_args()

    # Get markdown content
    if args.file:
        markdown = read_markdown_file(args.file)
        source_desc = f"file: {args.file}"
    else:
        markdown = args.content
        source_desc = "inline content"

    # Get title with fallback chain
    title = get_title(markdown, args.file, args.title)

    # Generate HTML
    html = generate_html(markdown, title)

    # Write to temp file
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        prefix="markdown-preview-",
        encoding="utf-8",
        delete=False,
    ) as f:
        f.write(html)
        temp_path = Path(f.name)

    # Open in browser
    print(f"Opening {source_desc} in browser...")
    print(f"Temp file: {temp_path}")
    open_in_browser(temp_path)


if __name__ == "__main__":
    main()
