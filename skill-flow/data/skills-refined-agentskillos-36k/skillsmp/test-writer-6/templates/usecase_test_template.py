"""
Template for testing use cases with mocks.

Replace:
- UseCaseName: Your use case name
- OperationName: Your operation (e.g., CreatePolitician)
- EntityName: Your entity name (e.g., Politician, Speaker)

IMPORTANT: Always write tests FIRST (TDD), then implement!
"""

from unittest.mock import AsyncMock

import pytest

from src.application.dtos.operation_dto import OperationNameInputDTO
from src.application.usecases.usecase_name import UseCaseName
from src.domain.entities.entity_name import EntityName
from src.domain.repositories.entity_name_repository import IEntityNameRepository
from src.domain.services.entity_name_domain_service import EntityNameDomainService


class TestUseCaseName:
    """Test suite for UseCaseName use case."""

    @pytest.fixture
    def mock_entity_repo(self) -> AsyncMock:
        """
        Mock entity repository.

        ALWAYS use AsyncMock with spec= for async repositories!
        """
        mock = AsyncMock(spec=IEntityNameRepository)
        return mock

    @pytest.fixture
    def mock_service(self) -> EntityNameDomainService:
        """
        Mock domain service.

        Domain services are typically sync (not async), so use regular mock.
        If your service IS async, use AsyncMock with spec=!
        """
        # For sync services, you can use actual instance or Mock
        # For this template, showing actual instance pattern
        return EntityNameDomainService()

    @pytest.fixture
    def usecase(
        self, mock_entity_repo: AsyncMock, mock_service: EntityNameDomainService
    ) -> UseCaseName:
        """Create use case with mocked dependencies."""
        return UseCaseName(
            entity_repository=mock_entity_repo,
            entity_service=mock_service,
        )

    # Happy path test
    @pytest.mark.asyncio
    async def test_execute_succeeds_with_valid_input(
        self,
        usecase: UseCaseName,
        mock_entity_repo: AsyncMock,
        mock_service: EntityNameDomainService,
    ) -> None:
        """Test use case succeeds with valid input."""
        # Arrange
        input_dto = OperationNameInputDTO(
            name="山田太郎",  # Use realistic Japanese names
            # Add other input fields
        )
        mock_entity_repo.create.return_value = EntityName(
            id=1,
            name="山田太郎",
        )

        # Act
        result = await usecase.execute(input_dto)

        # Assert
        assert result.entity_id == 1
        # For async mocks, use assert_awaited_once() not assert_called_once()
        mock_entity_repo.create.assert_awaited_once()

    # Validation error test - Polibase pattern: raise exceptions!
    @pytest.mark.asyncio
    async def test_execute_raises_error_with_invalid_input(
        self, usecase: UseCaseName
    ) -> None:
        """Test use case raises ValueError for invalid input."""
        # Arrange
        input_dto = OperationNameInputDTO(
            name="",  # Invalid: empty name
        )

        # Act & Assert - Polibase raises exceptions, not returning success=False
        with pytest.raises(ValueError, match="Name.*required"):
            await usecase.execute(input_dto)

    # Business rule violation test
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_entity_already_exists(
        self, usecase: UseCaseName, mock_entity_repo: AsyncMock
    ) -> None:
        """Test use case raises error when entity already exists."""
        # Arrange
        input_dto = OperationNameInputDTO(name="既存エンティティ")
        mock_entity_repo.get_by_name.return_value = [
            EntityName(id=1, name="既存エンティティ")
        ]

        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            await usecase.execute(input_dto)

        # Verify we checked for existence
        mock_entity_repo.get_by_name.assert_awaited_once_with("既存エンティティ")

    # Dependency not found test
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_dependency_not_found(
        self, usecase: UseCaseName, mock_entity_repo: AsyncMock
    ) -> None:
        """Test use case raises error when required dependency not found."""
        # Arrange
        input_dto = OperationNameInputDTO(
            name="Test",
            parent_id=999,  # Non-existent parent
        )
        mock_entity_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            await usecase.execute(input_dto)

    # Domain service interaction test
    @pytest.mark.asyncio
    async def test_execute_calls_domain_service(
        self,
        usecase: UseCaseName,
        mock_service: EntityNameDomainService,
        mock_entity_repo: AsyncMock,
    ) -> None:
        """Test use case delegates to domain service."""
        # Arrange
        input_dto = OperationNameInputDTO(name="Test")
        mock_entity_repo.create.return_value = EntityName(id=1, name="Test")

        # Act
        await usecase.execute(input_dto)

        # Assert
        # If service is mocked and async:
        # mock_service.process.assert_awaited_once()
        # If service is real or sync:
        # Just verify the result is correct

    # Error handling test
    @pytest.mark.asyncio
    async def test_execute_propagates_repository_error(
        self, usecase: UseCaseName, mock_entity_repo: AsyncMock
    ) -> None:
        """Test use case propagates repository errors."""
        # Arrange
        input_dto = OperationNameInputDTO(name="Test")
        mock_entity_repo.create.side_effect = Exception("Database error")

        # Act & Assert
        # In Polibase, exceptions typically propagate
        with pytest.raises(Exception, match="Database error"):
            await usecase.execute(input_dto)

    # Multiple entities test
    @pytest.mark.asyncio
    async def test_execute_processes_multiple_entities(
        self, usecase: UseCaseName, mock_entity_repo: AsyncMock
    ) -> None:
        """Test use case can process multiple entities."""
        # Arrange
        input_dto = OperationNameInputDTO(entity_ids=[1, 2, 3])
        mock_entity_repo.get_by_id.side_effect = [
            EntityName(id=1, name="Entity1"),
            EntityName(id=2, name="Entity2"),
            EntityName(id=3, name="Entity3"),
        ]

        # Act
        result = await usecase.execute(input_dto)

        # Assert
        assert result.processed_count == 3
        assert mock_entity_repo.get_by_id.await_count == 3
