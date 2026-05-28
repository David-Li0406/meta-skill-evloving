# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0.0", "notion-client>=2.6.0"]
# ///
"""Tests for filter builder functions.

Oracle Source: Notion API Reference - Database Query Filter
https://developers.notion.com/reference/post-database-query-filter

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

from query_database import (
    checkbox_filter,
    select_filter,
    status_filter,
    text_contains_filter,
    date_after_filter,
    date_before_filter,
    number_greater_than_filter,
    number_less_than_filter,
    and_filter,
    or_filter,
    sort_by_property,
    sort_by_created_time,
    sort_by_last_edited_time,
)


# =============================================================================
# ORACLES: Structures defined by Notion API documentation (independent source)
# =============================================================================

class NotionFilterOracle:
    """Oracle structures from Notion API Reference.

    Source: https://developers.notion.com/reference/post-database-query-filter
    Retrieved: 2025-12-23
    """

    @staticmethod
    def checkbox(property_name: str, equals: bool) -> dict:
        """Oracle: Checkbox filter structure per API docs."""
        return {
            "property": property_name,
            "checkbox": {"equals": equals}
        }

    @staticmethod
    def select(property_name: str, equals: str) -> dict:
        """Oracle: Select filter structure per API docs."""
        return {
            "property": property_name,
            "select": {"equals": equals}
        }

    @staticmethod
    def status(property_name: str, equals: str) -> dict:
        """Oracle: Status filter structure per API docs."""
        return {
            "property": property_name,
            "status": {"equals": equals}
        }

    @staticmethod
    def rich_text_contains(property_name: str, contains: str) -> dict:
        """Oracle: Rich text contains filter structure per API docs."""
        return {
            "property": property_name,
            "rich_text": {"contains": contains}
        }

    @staticmethod
    def date_after(property_name: str, after: str) -> dict:
        """Oracle: Date after filter structure per API docs."""
        return {
            "property": property_name,
            "date": {"after": after}
        }

    @staticmethod
    def date_before(property_name: str, before: str) -> dict:
        """Oracle: Date before filter structure per API docs."""
        return {
            "property": property_name,
            "date": {"before": before}
        }

    @staticmethod
    def number_gt(property_name: str, value: int | float) -> dict:
        """Oracle: Number greater than filter structure per API docs."""
        return {
            "property": property_name,
            "number": {"greater_than": value}
        }

    @staticmethod
    def number_lt(property_name: str, value: int | float) -> dict:
        """Oracle: Number less than filter structure per API docs."""
        return {
            "property": property_name,
            "number": {"less_than": value}
        }

    @staticmethod
    def compound_and(*filters: dict) -> dict:
        """Oracle: AND compound filter structure per API docs."""
        return {"and": list(filters)}

    @staticmethod
    def compound_or(*filters: dict) -> dict:
        """Oracle: OR compound filter structure per API docs."""
        return {"or": list(filters)}


# =============================================================================
# INTEGRITY TESTS: First principles validation
# =============================================================================

class TestFilterBuilderIntegrity:
    """Integrity tests validating first principles."""

    def test_all_simple_filters_have_property_field(self):
        """First principle: Simple filters must have 'property' field."""
        filters = [
            checkbox_filter("Done", True),
            select_filter("Status", "Active"),
            status_filter("Status", "Done"),
            text_contains_filter("Title", "test"),
            date_after_filter("Date", "2025-01-01"),
            date_before_filter("Date", "2025-12-31"),
            number_greater_than_filter("Count", 10),
            number_less_than_filter("Count", 100),
        ]
        for f in filters:
            assert "property" in f, f"Filter missing 'property' field: {f}"

    def test_compound_filters_have_correct_key(self):
        """First principle: Compound filters use 'and'/'or' key."""
        f1 = checkbox_filter("A", True)
        f2 = checkbox_filter("B", False)

        and_result = and_filter(f1, f2)
        or_result = or_filter(f1, f2)

        assert "and" in and_result
        assert "or" in or_result

    def test_compound_filters_contain_arrays(self):
        """First principle: Compound filter values are arrays."""
        f1 = checkbox_filter("A", True)
        f2 = checkbox_filter("B", False)

        and_result = and_filter(f1, f2)
        or_result = or_filter(f1, f2)

        assert isinstance(and_result["and"], list)
        assert isinstance(or_result["or"], list)


# =============================================================================
# BLACK-BOX TESTS: Public interface against oracle
# =============================================================================

class TestFilterBuildersBlackBox:
    """Black-box tests: Verify output matches Notion API oracle."""

    def test_checkbox_filter_true_matches_oracle(self):
        """Checkbox filter (true) matches Notion API specification."""
        result = checkbox_filter("Done", True)
        oracle = NotionFilterOracle.checkbox("Done", True)
        assert result == oracle

    def test_checkbox_filter_false_matches_oracle(self):
        """Checkbox filter (false) matches Notion API specification."""
        result = checkbox_filter("Archived", False)
        oracle = NotionFilterOracle.checkbox("Archived", False)
        assert result == oracle

    def test_select_filter_matches_oracle(self):
        """Select filter matches Notion API specification."""
        result = select_filter("Priority", "High")
        oracle = NotionFilterOracle.select("Priority", "High")
        assert result == oracle

    def test_status_filter_matches_oracle(self):
        """Status filter matches Notion API specification."""
        result = status_filter("Status", "In Progress")
        oracle = NotionFilterOracle.status("Status", "In Progress")
        assert result == oracle

    def test_text_contains_filter_matches_oracle(self):
        """Text contains filter matches Notion API specification."""
        result = text_contains_filter("Name", "API")
        oracle = NotionFilterOracle.rich_text_contains("Name", "API")
        assert result == oracle

    def test_date_after_filter_matches_oracle(self):
        """Date after filter matches Notion API specification."""
        result = date_after_filter("Due Date", "2025-01-01")
        oracle = NotionFilterOracle.date_after("Due Date", "2025-01-01")
        assert result == oracle

    def test_date_before_filter_matches_oracle(self):
        """Date before filter matches Notion API specification."""
        result = date_before_filter("Created", "2025-12-31")
        oracle = NotionFilterOracle.date_before("Created", "2025-12-31")
        assert result == oracle

    def test_number_greater_than_filter_matches_oracle(self):
        """Number greater than filter matches Notion API specification."""
        result = number_greater_than_filter("Score", 90)
        oracle = NotionFilterOracle.number_gt("Score", 90)
        assert result == oracle

    def test_number_less_than_filter_matches_oracle(self):
        """Number less than filter matches Notion API specification."""
        result = number_less_than_filter("Age", 30)
        oracle = NotionFilterOracle.number_lt("Age", 30)
        assert result == oracle

    def test_and_filter_matches_oracle(self):
        """AND compound filter matches Notion API specification."""
        f1 = checkbox_filter("Done", True)
        f2 = number_greater_than_filter("Days", 10)

        result = and_filter(f1, f2)
        oracle = NotionFilterOracle.compound_and(f1, f2)
        assert result == oracle

    def test_or_filter_matches_oracle(self):
        """OR compound filter matches Notion API specification."""
        f1 = text_contains_filter("Tag", "A")
        f2 = text_contains_filter("Tag", "B")

        result = or_filter(f1, f2)
        oracle = NotionFilterOracle.compound_or(f1, f2)
        assert result == oracle


# =============================================================================
# WHITE-BOX TESTS: Internal structure validation
# =============================================================================

class TestFilterBuildersWhiteBox:
    """White-box tests: Verify internal structure details."""

    def test_nested_compound_filter(self):
        """Nested compound filters maintain correct structure."""
        # Build: (A AND B) OR C
        a = checkbox_filter("A", True)
        b = select_filter("B", "opt")
        c = status_filter("C", "Done")

        inner = and_filter(a, b)
        outer = or_filter(inner, c)

        assert "or" in outer
        assert len(outer["or"]) == 2
        assert "and" in outer["or"][0]

    def test_filter_preserves_property_name_exactly(self):
        """Filter preserves property name with exact casing/spacing."""
        result = select_filter("My Custom Property", "Value")
        assert result["property"] == "My Custom Property"

    def test_number_filter_preserves_float(self):
        """Number filter preserves float precision."""
        result = number_greater_than_filter("Score", 3.14159)
        assert result["number"]["greater_than"] == 3.14159


# =============================================================================
# SORT BUILDER TESTS
# =============================================================================

class TestSortBuilders:
    """Tests for sort builder functions."""

    def test_sort_by_property_ascending(self):
        """Sort by property (ascending) creates correct structure."""
        result = sort_by_property("Name", "ascending")
        assert result == {"property": "Name", "direction": "ascending"}

    def test_sort_by_property_descending(self):
        """Sort by property (descending) creates correct structure."""
        result = sort_by_property("Date", "descending")
        assert result == {"property": "Date", "direction": "descending"}

    def test_sort_by_created_time(self):
        """Sort by created_time creates correct structure."""
        result = sort_by_created_time("descending")
        assert result == {"timestamp": "created_time", "direction": "descending"}

    def test_sort_by_last_edited_time(self):
        """Sort by last_edited_time creates correct structure."""
        result = sort_by_last_edited_time("ascending")
        assert result == {"timestamp": "last_edited_time", "direction": "ascending"}

    def test_sort_default_direction(self):
        """Sort functions have sensible defaults."""
        # created_time defaults to descending (most recent first)
        result = sort_by_created_time()
        assert result["direction"] == "descending"


# =============================================================================
# EDGE CASES AND COMPOUND FILTER TESTS
# =============================================================================

class TestFilterEdgeCases:
    """Edge case and complex filter tests."""

    def test_empty_and_filter(self):
        """AND filter with no arguments creates empty array."""
        result = and_filter()
        assert result == {"and": []}

    def test_single_item_compound(self):
        """Compound filter with single item is valid."""
        f = checkbox_filter("Done", True)
        result = and_filter(f)
        assert result == {"and": [f]}

    def test_many_items_in_compound(self):
        """Compound filter supports many items."""
        filters = [checkbox_filter(f"Prop{i}", True) for i in range(10)]
        result = and_filter(*filters)
        assert len(result["and"]) == 10

    def test_deeply_nested_compounds(self):
        """Deeply nested compound filters work correctly."""
        # ((A AND B) OR (C AND D)) AND E
        a = checkbox_filter("A", True)
        b = checkbox_filter("B", True)
        c = checkbox_filter("C", True)
        d = checkbox_filter("D", True)
        e = checkbox_filter("E", True)

        ab = and_filter(a, b)
        cd = and_filter(c, d)
        ab_or_cd = or_filter(ab, cd)
        final = and_filter(ab_or_cd, e)

        assert "and" in final
        assert len(final["and"]) == 2
        assert "or" in final["and"][0]

    def test_unicode_in_property_names(self):
        """Unicode characters in property names are preserved."""
        result = select_filter("状態", "完了")  # Japanese: Status, Done
        assert result["property"] == "状態"
        assert result["select"]["equals"] == "完了"

    def test_special_characters_in_text_filter(self):
        """Special characters in text filter are preserved."""
        result = text_contains_filter("Title", "Hello! @#$%^&*()")
        assert result["rich_text"]["contains"] == "Hello! @#$%^&*()"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
