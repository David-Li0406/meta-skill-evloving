# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0.0", "notion-client>=2.6.0"]
# ///
"""Integration tests for Notion API operations.

These tests make REAL API calls to Notion.
Requires NOTION_TOKEN environment variable.

Test Database: Books & Audiobooks (8eacdd87-6c53-431a-9dec-55932ac571b5)
Properties: Name (title), Author (rich_text), Format (select), Tags (multi_select),
            Status (select), Date Read (date), Rating (number), Audio Page (url)

Test Principles:
- Integration tests verify end-to-end API behavior
- Created resources are cleaned up after tests
- Tests are idempotent and can run repeatedly
"""

import os
import sys
import time
import pytest
from pathlib import Path

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from notion_wrapper import get_client, validate_token, api_call_with_retry
from create_page import (
    create_database_page,
    title_property,
    rich_text_property,
    number_property,
    select_property,
)
from add_blocks import paragraph, heading, bullet, divider, append_blocks
from query_database import number_greater_than_filter


# =============================================================================
# FIXTURES
# =============================================================================

# Test database ID (Books & Audiobooks)
TEST_DATABASE_ID = "8eacdd87-6c53-431a-9dec-55932ac571b5"


@pytest.fixture(scope="module")
def notion_token():
    """Get Notion token from environment."""
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        pytest.skip("NOTION_TOKEN not set - skipping integration tests")
    return token


@pytest.fixture(scope="module")
def client(notion_token):
    """Create authenticated Notion client."""
    return get_client(notion_token)


@pytest.fixture
def cleanup_pages(client):
    """Fixture to track and cleanup created pages."""
    created_page_ids = []

    yield created_page_ids

    # Cleanup: Archive all created pages
    for page_id in created_page_ids:
        try:
            client.pages.update(page_id, archived=True)
        except Exception:
            pass  # Best effort cleanup


# =============================================================================
# TOKEN VALIDATION TESTS
# =============================================================================

class TestTokenValidation:
    """Integration tests for token validation."""

    def test_valid_token_authenticates(self, notion_token):
        """Valid token successfully authenticates."""
        success, message = validate_token(notion_token)
        assert success is True
        assert "Authenticated as" in message

    def test_invalid_token_fails(self):
        """Invalid token (valid format) fails authentication."""
        success, message = validate_token("ntn_invalid_token_12345")
        assert success is False
        # Should fail with API error, not format error
        assert "ntn_" not in message or "secret_" not in message


# =============================================================================
# DATABASE QUERY TESTS (Read-only, safe to run repeatedly)
# =============================================================================

class TestDatabaseQuery:
    """Integration tests for database queries."""

    def test_query_database_returns_results(self, client):
        """Query returns results from the database."""
        results = api_call_with_retry(
            client.data_sources.query,
            TEST_DATABASE_ID,
            page_size=5
        )

        assert "results" in results
        assert isinstance(results["results"], list)
        # Database has content
        assert len(results["results"]) > 0

    def test_query_database_with_filter(self, client):
        """Query with filter returns filtered results."""
        # Query for books with rating > 0 (should reduce result count)
        results = api_call_with_retry(
            client.data_sources.query,
            TEST_DATABASE_ID,
            filter=number_greater_than_filter("Rating", 0),
            page_size=10
        )

        assert "results" in results
        # All results should have rating > 0
        for row in results["results"]:
            rating = row["properties"]["Rating"]["number"]
            if rating is not None:
                assert rating > 0

    def test_query_database_with_pagination(self, client):
        """Query respects page_size limit."""
        results = api_call_with_retry(
            client.data_sources.query,
            TEST_DATABASE_ID,
            page_size=2
        )

        # Should return at most 2 results
        assert len(results["results"]) <= 2

        # If more results exist, should have next_cursor
        if results.get("has_more"):
            assert results.get("next_cursor") is not None

    def test_query_returns_expected_properties(self, client):
        """Query results contain expected property types."""
        results = api_call_with_retry(
            client.data_sources.query,
            TEST_DATABASE_ID,
            page_size=1
        )

        if results["results"]:
            row = results["results"][0]
            props = row["properties"]

            # Verify expected properties exist
            assert "Name" in props
            assert props["Name"]["type"] == "title"

            assert "Rating" in props
            assert props["Rating"]["type"] == "number"

            assert "Author" in props
            assert props["Author"]["type"] == "rich_text"


# =============================================================================
# PAGE CREATION TESTS (Creates and cleans up pages)
# =============================================================================

class TestPageCreation:
    """Integration tests for page creation."""

    def test_create_page_in_database(self, client, cleanup_pages):
        """Create a page in the database with properties."""
        # Create test page
        properties = {
            "Name": title_property("[TEST] Integration Test Book"),
            "Author": rich_text_property("Test Author"),
            "Rating": number_property(5),
        }

        page = api_call_with_retry(
            create_database_page,
            client,
            TEST_DATABASE_ID,
            properties
        )

        # Track for cleanup
        cleanup_pages.append(page["id"])

        # Verify page was created
        assert "id" in page
        assert page["object"] == "page"

        # Verify properties were set
        assert page["properties"]["Name"]["title"][0]["plain_text"] == "[TEST] Integration Test Book"
        assert page["properties"]["Rating"]["number"] == 5

    def test_create_page_with_select_property(self, client, cleanup_pages):
        """Create a page with select property."""
        properties = {
            "Name": title_property("[TEST] Book with Format"),
            "Format": select_property("Physical"),
        }

        page = api_call_with_retry(
            create_database_page,
            client,
            TEST_DATABASE_ID,
            properties
        )

        cleanup_pages.append(page["id"])

        # Verify select was set
        format_prop = page["properties"]["Format"]["select"]
        assert format_prop is not None
        assert format_prop["name"] == "Physical"


# =============================================================================
# BLOCK APPEND TESTS (Creates page, adds blocks, cleans up)
# =============================================================================

class TestBlockAppend:
    """Integration tests for block operations."""

    def test_append_blocks_to_page(self, client, cleanup_pages):
        """Append blocks to a newly created page."""
        # Create a test page first
        properties = {
            "Name": title_property("[TEST] Page with Blocks"),
        }

        page = api_call_with_retry(
            create_database_page,
            client,
            TEST_DATABASE_ID,
            properties
        )
        cleanup_pages.append(page["id"])

        # Append blocks
        blocks = [
            heading("Test Heading", 1),
            paragraph("This is a test paragraph."),
            bullet("First bullet point"),
            bullet("Second bullet point"),
            divider(),
            paragraph("Content after divider."),
        ]

        result = api_call_with_retry(
            append_blocks,
            client,
            page["id"],
            blocks
        )

        # Verify blocks were added
        assert "results" in result
        assert len(result["results"]) == 6

        # Verify block types
        assert result["results"][0]["type"] == "heading_1"
        assert result["results"][1]["type"] == "paragraph"
        assert result["results"][2]["type"] == "bulleted_list_item"
        assert result["results"][4]["type"] == "divider"

    def test_retrieve_appended_blocks(self, client, cleanup_pages):
        """Retrieve blocks after appending to verify persistence."""
        # Create page with blocks
        properties = {"Name": title_property("[TEST] Page for Block Retrieval")}

        page = api_call_with_retry(
            create_database_page,
            client,
            TEST_DATABASE_ID,
            properties
        )
        cleanup_pages.append(page["id"])

        # Append a paragraph
        blocks = [paragraph("Persistent paragraph content")]
        api_call_with_retry(append_blocks, client, page["id"], blocks)

        # Small delay for API consistency
        time.sleep(0.5)

        # Retrieve blocks
        children = api_call_with_retry(
            client.blocks.children.list,
            page["id"]
        )

        assert len(children["results"]) >= 1
        block = children["results"][0]
        assert block["type"] == "paragraph"
        assert block["paragraph"]["rich_text"][0]["plain_text"] == "Persistent paragraph content"


# =============================================================================
# RATE LIMIT TESTS (Verify retry logic works)
# =============================================================================

class TestRateLimitHandling:
    """Tests for rate limit handling (implicit in rapid operations)."""

    def test_rapid_queries_succeed(self, client):
        """Multiple rapid queries succeed with retry logic."""
        # Make several queries rapidly - retry logic should handle any rate limits
        for i in range(5):
            results = api_call_with_retry(
                client.data_sources.query,
                TEST_DATABASE_ID,
                page_size=1
            )
            assert "results" in results

        # If we get here, rate limit handling worked


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
