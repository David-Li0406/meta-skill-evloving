#!/usr/bin/env python3
"""
Save content to Notion database via official API with Markdown support.
Requires: pip install requests
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)

# Configuration
DEFAULT_DATABASE_ID = "2decc7dd-3404-8002-a7e7-d64733a75885"
NOTION_API_VERSION = "2022-06-28"
NOTION_API_BASE = "https://api.notion.com/v1"
MAX_TEXT_LENGTH = 1900  # Notion limit is 2000, leave buffer

API_KEY_OVERRIDE = None


def get_api_key():
    """Get Notion API key from environment or override."""
    if API_KEY_OVERRIDE:
        return API_KEY_OVERRIDE
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        print("Error: NOTION_API_KEY environment variable not set")
        sys.exit(1)
    return key


def parse_inline_formatting(text: str) -> list:
    """Parse inline markdown formatting (bold, italic, code, links)."""
    rich_text = []

    # Pattern for **bold**, *italic*, `code`, [link](url)
    pattern = r'(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|\[(.+?)\]\((.+?)\))'

    last_end = 0
    for match in re.finditer(pattern, text):
        # Add plain text before this match
        if match.start() > last_end:
            plain_text = text[last_end:match.start()]
            if plain_text:
                rich_text.append({
                    "type": "text",
                    "text": {"content": plain_text}
                })

        full_match = match.group(0)

        if full_match.startswith('**'):
            # Bold
            content = match.group(2)
            rich_text.append({
                "type": "text",
                "text": {"content": content},
                "annotations": {"bold": True}
            })
        elif full_match.startswith('*') and not full_match.startswith('**'):
            # Italic
            content = match.group(3)
            rich_text.append({
                "type": "text",
                "text": {"content": content},
                "annotations": {"italic": True}
            })
        elif full_match.startswith('`'):
            # Code
            content = match.group(4)
            rich_text.append({
                "type": "text",
                "text": {"content": content},
                "annotations": {"code": True}
            })
        elif full_match.startswith('['):
            # Link
            link_text = match.group(5)
            link_url = match.group(6)
            rich_text.append({
                "type": "text",
                "text": {"content": link_text, "link": {"url": link_url}}
            })

        last_end = match.end()

    # Add remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            rich_text.append({
                "type": "text",
                "text": {"content": remaining}
            })

    # If no formatting found, return plain text
    if not rich_text:
        rich_text.append({
            "type": "text",
            "text": {"content": text}
        })

    return rich_text


def parse_table(lines: list) -> dict:
    """Parse markdown table into Notion table block."""
    if len(lines) < 2:
        return None

    # Parse header
    header_line = lines[0].strip()
    if not header_line.startswith('|'):
        return None

    headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
    if not headers:
        return None

    # Skip separator line (line with ---)
    data_start = 1
    if len(lines) > 1 and '---' in lines[1]:
        data_start = 2

    # Parse data rows
    rows = []
    for line in lines[data_start:]:
        line = line.strip()
        if line.startswith('|'):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            rows.append(cells)

    # Build Notion table
    table_width = len(headers)
    table_rows = []

    # Header row
    header_cells = []
    for h in headers:
        header_cells.append({
            "type": "table_cell",
            "table_cell": {
                "rich_text": parse_inline_formatting(h)
            }
        })
    table_rows.append({
        "type": "table_row",
        "table_row": {"cells": [[{"type": "text", "text": {"content": h}}] for h in headers]}
    })

    # Data rows
    for row in rows:
        # Pad row if needed
        while len(row) < table_width:
            row.append("")
        table_rows.append({
            "type": "table_row",
            "table_row": {"cells": [[{"type": "text", "text": {"content": cell}}] for cell in row[:table_width]]}
        })

    return {
        "type": "table",
        "table": {
            "table_width": table_width,
            "has_column_header": True,
            "has_row_header": False,
            "children": table_rows
        }
    }


def markdown_to_notion_blocks(content: str) -> list:
    """Convert markdown content to Notion blocks."""
    blocks = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty line - skip
        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped in ['---', '***', '___']:
            blocks.append({"type": "divider", "divider": {}})
            i += 1
            continue

        # Headings
        if stripped.startswith('# '):
            text = stripped[2:]
            if len(text) > MAX_TEXT_LENGTH:
                text = text[:MAX_TEXT_LENGTH]
            blocks.append({
                "type": "heading_1",
                "heading_1": {"rich_text": parse_inline_formatting(text)}
            })
            i += 1
            continue

        if stripped.startswith('## '):
            text = stripped[3:]
            if len(text) > MAX_TEXT_LENGTH:
                text = text[:MAX_TEXT_LENGTH]
            blocks.append({
                "type": "heading_2",
                "heading_2": {"rich_text": parse_inline_formatting(text)}
            })
            i += 1
            continue

        if stripped.startswith('### '):
            text = stripped[4:]
            if len(text) > MAX_TEXT_LENGTH:
                text = text[:MAX_TEXT_LENGTH]
            blocks.append({
                "type": "heading_3",
                "heading_3": {"rich_text": parse_inline_formatting(text)}
            })
            i += 1
            continue

        # Code block
        if stripped.startswith('```'):
            language = stripped[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_content = '\n'.join(code_lines)
            if len(code_content) > MAX_TEXT_LENGTH:
                code_content = code_content[:MAX_TEXT_LENGTH]
            blocks.append({
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": code_content}}],
                    "language": language
                }
            })
            i += 1  # Skip closing ```
            continue

        # Table detection
        if stripped.startswith('|'):
            table_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('|'):
                table_lines.append(lines[j])
                j += 1

            if len(table_lines) >= 2:
                table_block = parse_table(table_lines)
                if table_block:
                    blocks.append(table_block)
                    i = j
                    continue

        # Bulleted list
        if stripped.startswith('- ') or stripped.startswith('* '):
            text = stripped[2:]
            if len(text) > MAX_TEXT_LENGTH:
                text = text[:MAX_TEXT_LENGTH]
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": parse_inline_formatting(text)}
            })
            i += 1
            continue

        # Numbered list
        numbered_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if numbered_match:
            text = numbered_match.group(2)
            if len(text) > MAX_TEXT_LENGTH:
                text = text[:MAX_TEXT_LENGTH]
            blocks.append({
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": parse_inline_formatting(text)}
            })
            i += 1
            continue

        # Blockquote
        if stripped.startswith('> '):
            text = stripped[2:]
            if len(text) > MAX_TEXT_LENGTH:
                text = text[:MAX_TEXT_LENGTH]
            blocks.append({
                "type": "quote",
                "quote": {"rich_text": parse_inline_formatting(text)}
            })
            i += 1
            continue

        # Regular paragraph
        # Collect consecutive non-special lines
        para_lines = [stripped]
        j = i + 1
        while j < len(lines):
            next_line = lines[j].strip()
            if not next_line or next_line.startswith('#') or next_line.startswith('-') or \
               next_line.startswith('*') or next_line.startswith('|') or next_line.startswith('>') or \
               next_line.startswith('```') or next_line in ['---', '***', '___'] or \
               re.match(r'^\d+\.', next_line):
                break
            para_lines.append(next_line)
            j += 1

        para_text = ' '.join(para_lines)

        # Split long paragraphs
        while para_text:
            chunk = para_text[:MAX_TEXT_LENGTH]
            para_text = para_text[MAX_TEXT_LENGTH:]
            blocks.append({
                "type": "paragraph",
                "paragraph": {"rich_text": parse_inline_formatting(chunk)}
            })

        i = j

    return blocks


def create_page_with_markdown(database_id: str, title: str, content: str = None):
    """Create a new page with markdown content."""
    api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_API_VERSION
    }

    page_properties = {
        "Name": {
            "title": [{"text": {"content": title}}]
        }
    }

    body = {
        "parent": {"database_id": database_id},
        "properties": page_properties
    }

    # Parse markdown to blocks
    if content:
        all_blocks = markdown_to_notion_blocks(content)
    else:
        all_blocks = []

    # Create page with first 100 blocks (Notion limit)
    if all_blocks:
        body["children"] = all_blocks[:100]

    response = requests.post(
        f"{NOTION_API_BASE}/pages",
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        print(f"[ERROR] Error creating page: {response.status_code}")
        print(f"   Response: {response.text}")
        sys.exit(1)

    result = response.json()
    page_id = result['id']
    url = result.get('url', 'N/A')

    print(f"[OK] Created page: {title}")
    print(f"     URL: {url}")

    # Append remaining blocks if any
    if len(all_blocks) > 100:
        remaining = all_blocks[100:]
        for i in range(0, len(remaining), 100):
            batch = remaining[i:i+100]
            append_response = requests.patch(
                f"{NOTION_API_BASE}/blocks/{page_id}/children",
                headers=headers,
                json={"children": batch}
            )
            if append_response.status_code == 200:
                print(f"     Appended {len(batch)} more blocks")
            else:
                print(f"[WARN] Failed to append blocks: {append_response.status_code}")

    print(f"     Total blocks: {len(all_blocks)}")
    return result


def query_database(database_id: str, limit: int = 10):
    """Query pages in a database."""
    api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_API_VERSION
    }

    body = {
        "page_size": limit,
        "sorts": [{"timestamp": "created_time", "direction": "descending"}]
    }

    response = requests.post(
        f"{NOTION_API_BASE}/databases/{database_id}/query",
        headers=headers,
        json=body
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"[ERROR] Error querying database: {response.status_code}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Save markdown content to Notion database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Save with inline content
  %(prog)s --title "My Note" --content "# Hello\\n- Item 1\\n- Item 2"

  # Save from file (recommended for long content)
  %(prog)s --title "Research Report" --file report.md

  # List recent pages
  %(prog)s --list
        """
    )

    parser.add_argument("--database-id", "-d", default=DEFAULT_DATABASE_ID)
    parser.add_argument("--title", "-t", help="Page title")
    parser.add_argument("--content", "-c", help="Markdown content (inline)")
    parser.add_argument("--file", "-f", help="Read content from markdown file")
    parser.add_argument("--list", "-l", action="store_true", help="List recent pages")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--api-key", "-k", help="Notion API key")

    args = parser.parse_args()

    global API_KEY_OVERRIDE
    if args.api_key:
        API_KEY_OVERRIDE = args.api_key

    database_id = args.database_id.replace("-", "")

    if args.list:
        result = query_database(database_id)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("Recent pages:\n")
                for page in result.get("results", []):
                    title_prop = page.get("properties", {}).get("Name", {})
                    title_arr = title_prop.get("title", [])
                    title = title_arr[0].get("text", {}).get("content", "Untitled") if title_arr else "Untitled"
                    created = page.get("created_time", "")[:10]
                    url = page.get("url", "")
                    print(f"  - {title} ({created})")
                    print(f"    {url}")
    elif args.title:
        content = None
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"[INFO] Read {len(content)} chars from {args.file}")
        elif args.content:
            content = args.content

        result = create_page_with_markdown(database_id, args.title, content)
        if args.json:
            print(json.dumps(result, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
