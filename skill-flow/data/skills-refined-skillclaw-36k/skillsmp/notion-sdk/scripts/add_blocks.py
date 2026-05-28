# /// script
# requires-python = ">=3.11"
# dependencies = ["notion-client>=2.6.0"]
# ///
"""Append and manipulate blocks in Notion pages.

Supports:
- Appending blocks to pages
- Block builder helpers for common types
- Nested block structures (toggles, callouts)

Note: Max 1000 blocks per request. Chunk larger payloads.
"""

from notion_client import Client


def append_blocks(
    client: Client,
    page_id: str,
    blocks: list[dict],
) -> dict:
    """Append blocks to an existing page.

    Args:
        client: Authenticated Notion client
        page_id: Page or block ID to append to
        blocks: List of block objects

    Returns:
        Response with created block objects

    Raises:
        ValueError: If blocks exceeds 1000 limit
    """
    if len(blocks) > 1000:
        raise ValueError("Max 1000 blocks per request. Chunk your payload.")
    return client.blocks.children.append(block_id=page_id, children=blocks)


def get_block_children(
    client: Client,
    block_id: str,
) -> list[dict]:
    """Get all children of a block (with pagination).

    Args:
        client: Authenticated Notion client
        block_id: Block or page ID

    Returns:
        List of child block objects
    """
    from notion_client.helpers import collect_paginated_api

    return collect_paginated_api(client.blocks.children.list, block_id=block_id)


def delete_block(client: Client, block_id: str) -> dict:
    """Delete a block (moves to trash).

    Args:
        client: Authenticated Notion client
        block_id: Block ID to delete

    Returns:
        Deleted block object
    """
    return client.blocks.delete(block_id=block_id)


# ============================================================================
# Block Builder Helpers
# ============================================================================


def _rich_text(text: str, bold: bool = False, italic: bool = False, code: bool = False) -> list:
    """Create rich_text array with optional formatting."""
    return [
        {
            "type": "text",
            "text": {"content": text},
            "annotations": {
                "bold": bold,
                "italic": italic,
                "code": code,
                "strikethrough": False,
                "underline": False,
                "color": "default",
            },
        }
    ]


def paragraph(text: str, bold: bool = False) -> dict:
    """Create paragraph block."""
    return {
        "type": "paragraph",
        "paragraph": {"rich_text": _rich_text(text, bold=bold)},
    }


def heading(text: str, level: int = 2) -> dict:
    """Create heading block (level 1-3).

    Args:
        text: Heading text
        level: Heading level (1, 2, or 3)

    Returns:
        Heading block object
    """
    if level not in (1, 2, 3):
        raise ValueError("Heading level must be 1, 2, or 3")
    key = f"heading_{level}"
    return {"type": key, key: {"rich_text": _rich_text(text)}}


def bullet(text: str) -> dict:
    """Create bulleted list item."""
    return {
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": _rich_text(text)},
    }


def numbered(text: str) -> dict:
    """Create numbered list item."""
    return {
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": _rich_text(text)},
    }


def todo(text: str, checked: bool = False) -> dict:
    """Create to-do checkbox item."""
    return {
        "type": "to_do",
        "to_do": {
            "rich_text": _rich_text(text),
            "checked": checked,
        },
    }


def code_block(code: str, language: str = "python") -> dict:
    """Create code block.

    Args:
        code: Code content
        language: Programming language (python, javascript, typescript, etc.)
    """
    return {
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": code}}],
            "language": language,
        },
    }


def divider() -> dict:
    """Create horizontal divider."""
    return {"type": "divider", "divider": {}}


def callout(text: str, emoji: str = "💡") -> dict:
    """Create callout block with emoji icon.

    Args:
        text: Callout content
        emoji: Emoji for icon (default: lightbulb)
    """
    return {
        "type": "callout",
        "callout": {
            "rich_text": _rich_text(text),
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


def quote(text: str) -> dict:
    """Create quote block."""
    return {
        "type": "quote",
        "quote": {"rich_text": _rich_text(text)},
    }


def toggle(text: str, children: list[dict] | None = None) -> dict:
    """Create toggle block with optional nested content.

    Args:
        text: Toggle header text
        children: Nested blocks inside toggle
    """
    block = {
        "type": "toggle",
        "toggle": {"rich_text": _rich_text(text)},
    }
    if children:
        block["toggle"]["children"] = children
    return block


def table_of_contents() -> dict:
    """Create table of contents block."""
    return {"type": "table_of_contents", "table_of_contents": {}}


def bookmark(url: str) -> dict:
    """Create bookmark block for a URL."""
    return {"type": "bookmark", "bookmark": {"url": url}}
