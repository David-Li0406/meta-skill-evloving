"""
Template for testing domain services.

Replace:
- ServiceName: Your service name (e.g., SpeakerDomainService)
- EntityName: Your entity name (e.g., Speaker)

IMPORTANT: Always write tests FIRST (TDD), then implement!
"""

import pytest

from src.domain.entities.entity_name import EntityName
from src.domain.services.service_name import ServiceName


class TestServiceName:
    """Test suite for ServiceName domain service."""

    @pytest.fixture
    def service(self) -> ServiceName:
        """Create service instance for tests."""
        return ServiceName()

    @pytest.fixture
    def sample_entity(self) -> EntityName:
        """Create sample entity for tests."""
        return EntityName(
            id=1,
            name="山田太郎",  # Use realistic Japanese names
            # Add other fields
        )

    # Test basic functionality
    def test_method_name_returns_expected_result(self, service: ServiceName) -> None:
        """Test that method returns expected result for valid input."""
        # Arrange
        input_value = "test input"

        # Act
        result = service.method_name(input_value)

        # Assert
        assert result == "expected output"

    # Test edge cases
    def test_method_name_handles_empty_string(self, service: ServiceName) -> None:
        """Test that method handles empty string gracefully."""
        # Arrange
        input_value = ""

        # Act
        result = service.method_name(input_value)

        # Assert
        assert result == ""

    def test_method_name_raises_error_for_none(self, service: ServiceName) -> None:
        """Test that method raises error for None input."""
        # Arrange
        input_value = None

        # Act & Assert - Polibase pattern: raise exceptions!
        with pytest.raises(ValueError, match="Input cannot be None"):
            service.method_name(input_value)

    # Test with entity
    def test_validate_entity_succeeds_for_valid(
        self, service: ServiceName, sample_entity: EntityName
    ) -> None:
        """Test validation succeeds for valid entity."""
        # Act & Assert
        # Polibase pattern: raise exception if invalid, return nothing if valid
        service.validate(sample_entity)  # Should not raise

    def test_validate_entity_raises_error_for_invalid(
        self, service: ServiceName
    ) -> None:
        """Test validation raises error for invalid entity."""
        # Arrange
        invalid_entity = EntityName(id=None, name="")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            service.validate(invalid_entity)

        # Can also check specific error message
        assert "Name is required" in str(exc_info.value)

    # Parametrized tests for multiple inputs
    @pytest.mark.parametrize(
        "input_value,expected",
        [
            ("input1", "output1"),
            ("input2", "output2"),
            ("input3", "output3"),
        ],
    )
    def test_method_name_with_various_inputs(
        self, service: ServiceName, input_value: str, expected: str
    ) -> None:
        """Test method with various input/output combinations."""
        result = service.method_name(input_value)
        assert result == expected

    # Test business rules
    def test_is_duplicate_returns_true_for_same_name(
        self, service: ServiceName
    ) -> None:
        """Test duplicate detection returns True for matching entities."""
        # Arrange
        entity1 = EntityName(id=1, name="山田太郎")
        entity2 = EntityName(id=2, name="山田太郎")

        # Act
        is_duplicate = service.is_duplicate(entity1, [entity2])

        # Assert
        assert is_duplicate is True

    def test_is_duplicate_returns_false_for_different_name(
        self, service: ServiceName
    ) -> None:
        """Test duplicate detection returns False for different entities."""
        # Arrange
        entity1 = EntityName(id=1, name="山田太郎")
        entity2 = EntityName(id=2, name="鈴木一郎")

        # Act
        is_duplicate = service.is_duplicate(entity1, [entity2])

        # Assert
        assert is_duplicate is False
