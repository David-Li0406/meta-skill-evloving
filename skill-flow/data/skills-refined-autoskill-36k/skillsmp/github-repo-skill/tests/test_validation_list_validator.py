"""Tests for validation base classes - ListValidator."""

from cmm_ai_automation.validation.base import ListValidator, ValidationIssue


class ConcreteListValidator(ListValidator):
    """Concrete implementation of ListValidator for testing."""

    @property
    def name(self) -> str:
        return "test_list"

    def validate_item(
        self,
        item: str,
        _context: dict,
        sheet: str,
        row: int,
        field: str,
    ) -> list[ValidationIssue]:
        """Simple validation: reject items starting with 'BAD'."""
        if item.startswith("BAD"):
            from cmm_ai_automation.validation.base import IssueType, Severity

            return [
                ValidationIssue(
                    sheet=sheet,
                    row=row,
                    field=field,
                    issue_type=IssueType.INVALID_ID,
                    severity=Severity.ERROR,
                    message=f"Bad item: {item}",
                )
            ]
        return []


class TestListValidator:
    """Tests for ListValidator class."""

    def test_parse_list_semicolon_default(self) -> None:
        """Test parsing semicolon-separated list."""
        validator = ConcreteListValidator()
        result = validator.parse_list("item1;item2;item3")

        assert result == ["item1", "item2", "item3"]

    def test_parse_list_with_spaces(self) -> None:
        """Test that spaces around items are stripped."""
        validator = ConcreteListValidator()
        result = validator.parse_list("item1 ; item2 ; item3")

        assert result == ["item1", "item2", "item3"]

    def test_parse_list_custom_separator(self) -> None:
        """Test parsing with custom separator."""
        validator = ConcreteListValidator(separator=",")
        result = validator.parse_list("item1,item2,item3")

        assert result == ["item1", "item2", "item3"]

    def test_parse_list_empty_string(self) -> None:
        """Test that empty string returns empty list."""
        validator = ConcreteListValidator()
        result = validator.parse_list("")

        assert result == []

    def test_parse_list_single_item(self) -> None:
        """Test parsing single item (no separator)."""
        validator = ConcreteListValidator()
        result = validator.parse_list("single_item")

        assert result == ["single_item"]

    def test_parse_list_trailing_separator(self) -> None:
        """Test handling trailing separator."""
        validator = ConcreteListValidator()
        result = validator.parse_list("item1;item2;")

        assert result == ["item1", "item2"]

    def test_parse_list_multiple_separators(self) -> None:
        """Test handling multiple consecutive separators."""
        validator = ConcreteListValidator()
        result = validator.parse_list("item1;;item2")

        # Empty items should be filtered out
        assert result == ["item1", "item2"]

    def test_parse_list_whitespace_only_items(self) -> None:
        """Test that whitespace-only items are filtered."""
        validator = ConcreteListValidator()
        result = validator.parse_list("item1;  ;item2")

        assert result == ["item1", "item2"]

    def test_validate_all_valid_items(self) -> None:
        """Test validation when all items are valid."""
        validator = ConcreteListValidator()
        issues = validator.validate(
            value="good1;good2;good3",
            context={},
            sheet="test.tsv",
            row=1,
            field="test_field",
        )

        assert len(issues) == 0

    def test_validate_some_invalid_items(self) -> None:
        """Test validation when some items are invalid."""
        validator = ConcreteListValidator()
        issues = validator.validate(
            value="good1;BAD2;good3",
            context={},
            sheet="test.tsv",
            row=1,
            field="test_field",
        )

        assert len(issues) == 1
        assert "BAD2" in issues[0].message

    def test_validate_all_invalid_items(self) -> None:
        """Test validation when all items are invalid."""
        validator = ConcreteListValidator()
        issues = validator.validate(
            value="BAD1;BAD2;BAD3",
            context={},
            sheet="test.tsv",
            row=1,
            field="test_field",
        )

        assert len(issues) == 3
        assert all("BAD" in issue.message for issue in issues)

    def test_validate_empty_value(self) -> None:
        """Test validation with empty value."""
        validator = ConcreteListValidator()
        issues = validator.validate(
            value="",
            context={},
            sheet="test.tsv",
            row=1,
            field="test_field",
        )

        assert len(issues) == 0

    def test_validate_single_item(self) -> None:
        """Test validation with single item."""
        validator = ConcreteListValidator()
        issues = validator.validate(
            value="good_item",
            context={},
            sheet="test.tsv",
            row=1,
            field="test_field",
        )

        assert len(issues) == 0

    def test_validate_single_bad_item(self) -> None:
        """Test validation with single bad item."""
        validator = ConcreteListValidator()
        issues = validator.validate(
            value="BAD_item",
            context={},
            sheet="test.tsv",
            row=1,
            field="test_field",
        )

        assert len(issues) == 1

    def test_custom_separator_in_validation(self) -> None:
        """Test validation uses custom separator."""
        validator = ConcreteListValidator(separator="|")
        issues = validator.validate(
            value="good1|BAD2|good3",
            context={},
            sheet="test.tsv",
            row=1,
            field="test_field",
        )

        assert len(issues) == 1
        assert "BAD2" in issues[0].message

    def test_validator_name_property(self) -> None:
        """Test that concrete validator has name property."""
        validator = ConcreteListValidator()
        assert validator.name == "test_list"

    def test_parse_list_with_complex_items(self) -> None:
        """Test parsing list with complex item strings."""
        validator = ConcreteListValidator()
        result = validator.parse_list("CHEBI:12345;NCBITaxon:9606;GO:0008150")

        assert len(result) == 3
        assert "CHEBI:12345" in result
        assert "NCBITaxon:9606" in result
        assert "GO:0008150" in result

    def test_parse_list_preserves_item_content(self) -> None:
        """Test that item content is preserved (only surrounding whitespace stripped)."""
        validator = ConcreteListValidator()
        result = validator.parse_list("item with spaces;another item;third")

        assert "item with spaces" in result
        assert "another item" in result
