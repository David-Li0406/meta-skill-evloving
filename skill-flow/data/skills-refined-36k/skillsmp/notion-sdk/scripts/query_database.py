# /// script
# requires-python = ">=3.11"
# dependencies = ["notion-client>=2.6.0"]
# ///
"""Query Notion databases with filters and sorting.

Supports:
- Database queries with filters and sorts
- Workspace-wide search
- Pagination via helper functions

Note: Uses data_sources.query per Notion API v2.6.0+ multi-source model.
For legacy databases, data_source_id == database_id.
"""

from notion_client import Client
from notion_client.helpers import collect_paginated_api


def query_data_source(
    client: Client,
    data_source_id: str,
    filter_obj: dict | None = None,
    sorts: list | None = None,
) -> list[dict]:
    """Query database with optional filters and sorting.

    Args:
        client: Authenticated Notion client
        data_source_id: Database/data source ID
        filter_obj: Filter object (see filter builders below)
        sorts: List of sort objects

    Returns:
        List of page objects matching query

    Example:
        results = query_data_source(
            client,
            "abc123...",
            filter_obj=checkbox_filter("Done", False),
            sorts=[{"property": "Created", "direction": "descending"}]
        )
    """
    kwargs = {"data_source_id": data_source_id}
    if filter_obj:
        kwargs["filter"] = filter_obj
    if sorts:
        kwargs["sorts"] = sorts

    return collect_paginated_api(client.data_sources.query, **kwargs)


def search_workspace(
    client: Client,
    query: str,
    filter_type: str | None = None,
) -> list[dict]:
    """Search across workspace by title.

    Args:
        client: Authenticated Notion client
        query: Search query string
        filter_type: "page" or "database" to filter results

    Returns:
        List of matching pages and/or databases
    """
    params: dict = {"query": query}
    if filter_type:
        params["filter"] = {"value": filter_type, "property": "object"}
    return collect_paginated_api(client.search, **params)


def get_page(client: Client, page_id: str) -> dict:
    """Retrieve a single page by ID.

    Args:
        client: Authenticated Notion client
        page_id: Page ID

    Returns:
        Page object with properties
    """
    return client.pages.retrieve(page_id=page_id)


def get_database(client: Client, database_id: str) -> dict:
    """Retrieve database schema (properties, title).

    Args:
        client: Authenticated Notion client
        database_id: Database ID

    Returns:
        Database object with properties schema
    """
    return client.databases.retrieve(database_id=database_id)


# ============================================================================
# Filter Builders
# ============================================================================


def checkbox_filter(property_name: str, equals: bool) -> dict:
    """Filter by checkbox property.

    Example: checkbox_filter("Done", True) -> only checked items
    """
    return {"property": property_name, "checkbox": {"equals": equals}}


def select_filter(property_name: str, equals: str) -> dict:
    """Filter by select property value.

    Example: select_filter("Priority", "High")
    """
    return {"property": property_name, "select": {"equals": equals}}


def status_filter(property_name: str, equals: str) -> dict:
    """Filter by status property value.

    Example: status_filter("Status", "In Progress")
    """
    return {"property": property_name, "status": {"equals": equals}}


def text_contains_filter(property_name: str, contains: str) -> dict:
    """Filter rich_text or title containing substring.

    Example: text_contains_filter("Name", "API")
    """
    return {"property": property_name, "rich_text": {"contains": contains}}


def date_after_filter(property_name: str, after: str) -> dict:
    """Filter date property after given date (ISO 8601).

    Example: date_after_filter("Due Date", "2025-01-01")
    """
    return {"property": property_name, "date": {"after": after}}


def date_before_filter(property_name: str, before: str) -> dict:
    """Filter date property before given date (ISO 8601)."""
    return {"property": property_name, "date": {"before": before}}


def number_greater_than_filter(property_name: str, value: int | float) -> dict:
    """Filter number property greater than value."""
    return {"property": property_name, "number": {"greater_than": value}}


def number_less_than_filter(property_name: str, value: int | float) -> dict:
    """Filter number property less than value."""
    return {"property": property_name, "number": {"less_than": value}}


def and_filter(*filters: dict) -> dict:
    """Combine multiple filters with AND logic.

    Example: and_filter(
        checkbox_filter("Done", False),
        status_filter("Status", "In Progress")
    )
    """
    return {"and": list(filters)}


def or_filter(*filters: dict) -> dict:
    """Combine multiple filters with OR logic."""
    return {"or": list(filters)}


# ============================================================================
# Sort Builders
# ============================================================================


def sort_by_property(property_name: str, direction: str = "ascending") -> dict:
    """Create sort object for a property.

    Args:
        property_name: Property to sort by
        direction: "ascending" or "descending"
    """
    return {"property": property_name, "direction": direction}


def sort_by_created_time(direction: str = "descending") -> dict:
    """Sort by creation timestamp."""
    return {"timestamp": "created_time", "direction": direction}


def sort_by_last_edited_time(direction: str = "descending") -> dict:
    """Sort by last edit timestamp."""
    return {"timestamp": "last_edited_time", "direction": direction}
