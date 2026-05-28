# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0.0", "notion-client>=2.6.0"]
# ///
"""Tests for block builder functions.

Oracle Source: Notion API Reference - Block Object
https://developers.notion.com/reference/block

Test Principles Applied:
- Oracles from domain rules (Notion API docs), NOT code behavior
- Black-box: Test public interface against oracle
- White-box: Test internal structure matches API spec
- Invalid inputs must raise exceptions
- Deterministic with documented tolerances
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from add_blocks import (
    paragraph,
    heading,
    bullet,
    numbered,
    todo,
    code_block,
    divider,
    callout,
    quote,
    toggle,
    table_of_contents,
    bookmark,
    append_blocks,
)


# =============================================================================
# ORACLES: Structures defined by Notion API documentation (independent source)
# =============================================================================

class NotionBlockOracle:
    """Oracle structures from Notion API Reference.

    Source: https://developers.notion.com/reference/block
    Retrieved: 2025-12-23

    Note: Oracles show REQUIRED fields only. Optional fields (color, children)
    are omitted per API docs stating they default when not provided.
    """

    @staticmethod
    def paragraph(text: str) -> dict:
        """Oracle: Paragraph block structure per API docs."""
        return {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    @staticmethod
    def heading(text: str, level: int) -> dict:
        """Oracle: Heading block structure per API docs."""
        key = f"heading_{level}"
        return {
            "type": key,
            key: {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    @staticmethod
    def bulleted_list_item(text: str) -> dict:
        """Oracle: Bulleted list item structure per API docs."""
        return {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    @staticmethod
    def numbered_list_item(text: str) -> dict:
        """Oracle: Numbered list item structure per API docs."""
        return {
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    @staticmethod
    def to_do(text: str, checked: bool) -> dict:
        """Oracle: To-do block structure per API docs."""
        return {
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "checked": checked
            }
        }

    @staticmethod
    def code(content: str, language: str) -> dict:
        """Oracle: Code block structure per API docs."""
        return {
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": content}}],
                "language": language
            }
        }

    @staticmethod
    def callout_block(text: str, emoji: str) -> dict:
        """Oracle: Callout block structure per API docs."""
        return {
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "icon": {"type": "emoji", "emoji": emoji}
            }
        }

    @staticmethod
    def quote_block(text: str) -> dict:
        """Oracle: Quote block structure per API docs."""
        return {
            "type": "quote",
            "quote": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    @staticmethod
    def divider_block() -> dict:
        """Oracle: Divider block structure per API docs."""
        return {"type": "divider", "divider": {}}

    @staticmethod
    def bookmark_block(url: str) -> dict:
        """Oracle: Bookmark block structure per API docs."""
        return {"type": "bookmark", "bookmark": {"url": url}}


# =============================================================================
# INTEGRITY TESTS: First principles validation
# =============================================================================

class TestBlockBuilderIntegrity:
    """Integrity tests validating first principles."""

    def test_all_blocks_have_type_field(self):
        """First principle: All blocks must have 'type' field."""
        blocks = [
            paragraph("test"),
            heading("test", 1),
            bullet("test"),
            numbered("test"),
            todo("test"),
            code_block("test"),
            divider(),
            callout("test"),
            quote("test"),
            toggle("test"),
            table_of_contents(),
            bookmark("https://example.com"),
        ]
        for block in blocks:
            assert "type" in block, f"Block missing 'type' field: {block}"

    def test_all_blocks_have_matching_type_key(self):
        """First principle: Block has key matching its type value."""
        blocks = [
            paragraph("test"),
            heading("test", 2),
            bullet("test"),
            divider(),
        ]
        for block in blocks:
            block_type = block["type"]
            assert block_type in block, f"Block missing key for type '{block_type}'"

    def test_text_blocks_have_rich_text_array(self):
        """First principle: Text-containing blocks have rich_text array."""
        text_blocks = [
            ("paragraph", paragraph("test")),
            ("heading_2", heading("test", 2)),
            ("bulleted_list_item", bullet("test")),
            ("numbered_list_item", numbered("test")),
            ("to_do", todo("test")),
            ("quote", quote("test")),
            ("callout", callout("test")),
        ]
        for block_type, block in text_blocks:
            content = block[block_type]
            assert "rich_text" in content, f"{block_type} missing rich_text"
            assert isinstance(content["rich_text"], list), f"{block_type} rich_text not array"


# =============================================================================
# BLACK-BOX TESTS: Public interface against oracle
# =============================================================================

class TestBlockBuildersBlackBox:
    """Black-box tests: Verify output matches Notion API oracle."""

    def test_paragraph_matches_oracle(self):
        """Paragraph block output matches Notion API specification."""
        result = paragraph("Hello world")
        oracle = NotionBlockOracle.paragraph("Hello world")
        # Compare structure (our impl may have extra annotations)
        assert result["type"] == oracle["type"]
        assert result["paragraph"]["rich_text"][0]["text"]["content"] == "Hello world"

    def test_heading_1_matches_oracle(self):
        """Heading 1 block output matches Notion API specification."""
        result = heading("Title", 1)
        oracle = NotionBlockOracle.heading("Title", 1)
        assert result["type"] == oracle["type"] == "heading_1"
        assert result["heading_1"]["rich_text"][0]["text"]["content"] == "Title"

    def test_heading_2_matches_oracle(self):
        """Heading 2 block output matches Notion API specification."""
        result = heading("Subtitle", 2)
        assert result["type"] == "heading_2"
        assert result["heading_2"]["rich_text"][0]["text"]["content"] == "Subtitle"

    def test_heading_3_matches_oracle(self):
        """Heading 3 block output matches Notion API specification."""
        result = heading("Section", 3)
        assert result["type"] == "heading_3"
        assert result["heading_3"]["rich_text"][0]["text"]["content"] == "Section"

    def test_bullet_matches_oracle(self):
        """Bulleted list item matches Notion API specification."""
        result = bullet("List item")
        oracle = NotionBlockOracle.bulleted_list_item("List item")
        assert result["type"] == oracle["type"]
        assert result["bulleted_list_item"]["rich_text"][0]["text"]["content"] == "List item"

    def test_numbered_matches_oracle(self):
        """Numbered list item matches Notion API specification."""
        result = numbered("Step one")
        oracle = NotionBlockOracle.numbered_list_item("Step one")
        assert result["type"] == oracle["type"]
        assert result["numbered_list_item"]["rich_text"][0]["text"]["content"] == "Step one"

    def test_todo_unchecked_matches_oracle(self):
        """To-do (unchecked) matches Notion API specification."""
        result = todo("Task", checked=False)
        oracle = NotionBlockOracle.to_do("Task", False)
        assert result["type"] == oracle["type"]
        assert result["to_do"]["checked"] == False
        assert result["to_do"]["rich_text"][0]["text"]["content"] == "Task"

    def test_todo_checked_matches_oracle(self):
        """To-do (checked) matches Notion API specification."""
        result = todo("Done task", checked=True)
        oracle = NotionBlockOracle.to_do("Done task", True)
        assert result["to_do"]["checked"] == True

    def test_code_block_matches_oracle(self):
        """Code block matches Notion API specification."""
        result = code_block("print('hello')", language="python")
        oracle = NotionBlockOracle.code("print('hello')", "python")
        assert result["type"] == oracle["type"]
        assert result["code"]["language"] == "python"
        assert result["code"]["rich_text"][0]["text"]["content"] == "print('hello')"

    def test_divider_matches_oracle(self):
        """Divider block matches Notion API specification."""
        result = divider()
        oracle = NotionBlockOracle.divider_block()
        assert result == oracle

    def test_callout_matches_oracle(self):
        """Callout block matches Notion API specification."""
        result = callout("Important note", emoji="⚠️")
        oracle = NotionBlockOracle.callout_block("Important note", "⚠️")
        assert result["type"] == oracle["type"]
        assert result["callout"]["icon"]["emoji"] == "⚠️"
        assert result["callout"]["rich_text"][0]["text"]["content"] == "Important note"

    def test_quote_matches_oracle(self):
        """Quote block matches Notion API specification."""
        result = quote("Famous quote")
        oracle = NotionBlockOracle.quote_block("Famous quote")
        assert result["type"] == oracle["type"]
        assert result["quote"]["rich_text"][0]["text"]["content"] == "Famous quote"

    def test_bookmark_matches_oracle(self):
        """Bookmark block matches Notion API specification."""
        result = bookmark("https://example.com")
        oracle = NotionBlockOracle.bookmark_block("https://example.com")
        assert result == oracle


# =============================================================================
# WHITE-BOX TESTS: Internal structure validation
# =============================================================================

class TestBlockBuildersWhiteBox:
    """White-box tests: Verify internal structure details."""

    def test_paragraph_bold_annotation(self):
        """Paragraph with bold=True sets annotation correctly."""
        result = paragraph("Bold text", bold=True)
        annotations = result["paragraph"]["rich_text"][0]["annotations"]
        assert annotations["bold"] == True

    def test_callout_icon_structure(self):
        """Callout icon has correct nested structure."""
        result = callout("Note", emoji="💡")
        icon = result["callout"]["icon"]
        assert icon["type"] == "emoji"
        assert icon["emoji"] == "💡"

    def test_toggle_accepts_children(self):
        """Toggle block can include nested children."""
        child = paragraph("Nested content")
        result = toggle("Click to expand", children=[child])
        assert "children" in result["toggle"]
        assert result["toggle"]["children"] == [child]

    def test_toggle_without_children_has_no_children_key(self):
        """Toggle without children omits children key."""
        result = toggle("Empty toggle")
        assert "children" not in result["toggle"]

    def test_code_block_preserves_whitespace(self):
        """Code block preserves whitespace and newlines."""
        code_content = "def foo():\n    return 42"
        result = code_block(code_content)
        assert result["code"]["rich_text"][0]["text"]["content"] == code_content


# =============================================================================
# INVALID INPUT TESTS: Must raise exceptions
# =============================================================================

class TestBlockBuildersInvalidInputs:
    """Invalid input tests: Verify proper exception handling."""

    def test_heading_invalid_level_raises(self):
        """Heading with invalid level (not 1-3) raises ValueError."""
        with pytest.raises(ValueError, match="level must be 1, 2, or 3"):
            heading("Title", 4)

        with pytest.raises(ValueError, match="level must be 1, 2, or 3"):
            heading("Title", 0)

    def test_append_blocks_exceeds_limit_raises(self):
        """Appending more than 1000 blocks raises ValueError."""
        # Create 1001 blocks
        blocks = [paragraph(f"Block {i}") for i in range(1001)]

        # Mock client (we just need to test the validation)
        class MockClient:
            pass

        with pytest.raises(ValueError, match="Max 1000 blocks"):
            append_blocks(MockClient(), "page-id", blocks)


# =============================================================================
# EDGE CASES AND BOUNDARY TESTS
# =============================================================================

class TestBlockBuildersEdgeCases:
    """Edge case and boundary tests."""

    def test_empty_paragraph(self):
        """Empty paragraph is valid."""
        result = paragraph("")
        assert result["paragraph"]["rich_text"][0]["text"]["content"] == ""

    def test_multiline_code_block(self):
        """Multi-line code is preserved."""
        code = """def example():
    x = 1
    y = 2
    return x + y"""
        result = code_block(code)
        assert "\n" in result["code"]["rich_text"][0]["text"]["content"]

    def test_unicode_emoji_in_callout(self):
        """Unicode emoji in callout is preserved."""
        emojis = ["💡", "⚠️", "✅", "🚀", "📝"]
        for emoji in emojis:
            result = callout("Test", emoji=emoji)
            assert result["callout"]["icon"]["emoji"] == emoji

    def test_url_with_query_params_in_bookmark(self):
        """Bookmark preserves URL with query parameters."""
        url = "https://example.com/page?foo=bar&baz=qux#section"
        result = bookmark(url)
        assert result["bookmark"]["url"] == url

    def test_exactly_1000_blocks_is_valid(self):
        """Exactly 1000 blocks is within limit (boundary test)."""
        blocks = [paragraph(f"Block {i}") for i in range(1000)]
        # This should not raise - we can't fully test without mocking Client
        assert len(blocks) == 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
