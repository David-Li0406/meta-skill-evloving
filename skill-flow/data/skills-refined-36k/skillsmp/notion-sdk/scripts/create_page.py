# /// script
# requires-python = ">=3.11"
# dependencies = ["notion-client>=2.6.0"]
# ///
"""Create pages in Notion databases with properties and content blocks.

Supports:
- Creating pages in databases (with full property support)
- Creating sub-pages under existing pages
- Adding initial content blocks during creation

Note: Uses data_source_id per Notion API v2.6.0+ multi-source model.
For legacy databases, data_source_id == database_id.
"""

from notion_client import Client


def create_database_page(
    client: Client,
    data_source_id: str,
    properties: dict,
    children: list | None = None,
) -> dict:
    """Create a new page in a database.

    Args:
        client: Authenticated Notion client
        data_source_id: Database/data source ID (32-char UUID without dashes works too)
        properties: Property values matching database schema
        children: Optional list of block objects for initial content

    Returns:
        Created page object with id, url, properties, etc.

    Example properties:
        {
            "Name": {"title": [{"text": {"content": "Page Title"}}]},
            "Status": {"status": {"name": "In Progress"}},
            "Tags": {"multi_select": [{"name": "api"}, {"name": "python"}]},
            "Due Date": {"date": {"start": "2025-12-31"}}
        }
    """
    return client.pages.create(
        parent={"type": "data_source_id", "data_source_id": data_source_id},
        properties=properties,
        children=children or [],
    )


def create_child_page(
    client: Client,
    parent_page_id: str,
    title: str,
    children: list | None = None,
) -> dict:
    """Create a sub-page under an existing page.

    Note: Pages under pages can only have a title property.
    For full property support, use create_database_page().

    Args:
        client: Authenticated Notion client
        parent_page_id: Parent page ID
        title: Page title text
        children: Optional list of block objects for content

    Returns:
        Created page object
    """
    return client.pages.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        properties={"title": [{"text": {"content": title}}]},
        children=children or [],
    )


def update_page_properties(
    client: Client,
    page_id: str,
    properties: dict,
) -> dict:
    """Update properties of an existing page.

    Args:
        client: Authenticated Notion client
        page_id: Page ID to update
        properties: Properties to update (only include changed ones)

    Returns:
        Updated page object
    """
    return client.pages.update(page_id=page_id, properties=properties)


def archive_page(client: Client, page_id: str) -> dict:
    """Move a page to trash (archive).

    Args:
        client: Authenticated Notion client
        page_id: Page ID to archive

    Returns:
        Updated page object with archived=True
    """
    return client.pages.update(page_id=page_id, archived=True)


# Property builder helpers for common types
def title_property(text: str) -> dict:
    """Build title property value."""
    return {"title": [{"text": {"content": text}}]}


def rich_text_property(text: str) -> dict:
    """Build rich_text property value."""
    return {"rich_text": [{"text": {"content": text}}]}


def select_property(option_name: str) -> dict:
    """Build select property value."""
    return {"select": {"name": option_name}}


def multi_select_property(option_names: list[str]) -> dict:
    """Build multi_select property value."""
    return {"multi_select": [{"name": name} for name in option_names]}


def date_property(start: str, end: str | None = None) -> dict:
    """Build date property value (ISO 8601 format)."""
    date_obj = {"start": start}
    if end:
        date_obj["end"] = end
    return {"date": date_obj}


def checkbox_property(checked: bool) -> dict:
    """Build checkbox property value."""
    return {"checkbox": checked}


def number_property(value: int | float) -> dict:
    """Build number property value."""
    return {"number": value}


def url_property(url: str) -> dict:
    """Build URL property value."""
    return {"url": url}


def status_property(status_name: str) -> dict:
    """Build status property value."""
    return {"status": {"name": status_name}}


def relation_property(page_ids: list[str]) -> dict:
    """Build relation property value."""
    return {"relation": [{"id": pid} for pid in page_ids]}
