"""
Template for creating a repository interface in the Domain layer.

Replace:
- EntityName: Your entity name
- IEntityNameRepository: Your repository interface name
"""

from typing import Any, Protocol

from src.domain.entities.entity_name import EntityName  # Replace with your entity
from src.domain.repositories.base import BaseRepository


class IEntityNameRepository(BaseRepository[EntityName], Protocol):
    """
    Repository interface for EntityName operations.

    This interface defines the contract for data access operations.
    Implementation details are in the Infrastructure layer.
    """

    # Common CRUD operations inherited from BaseRepository:
    # - async def get_by_id(self, entity_id: int) -> EntityName | None
    # - async def get_all(
    #       self, limit: int | None = None, offset: int | None = None
    #   ) -> list[EntityName]
    # - async def create(self, entity: EntityName) -> EntityName
    # - async def update(self, entity: EntityName) -> EntityName
    # - async def delete(self, entity_id: int) -> bool

    # Add custom query methods here
    async def get_by_name(self, name: str) -> list[EntityName]:
        """
        Find entities by name.

        Args:
            name: Entity name to search for

        Returns:
            List of entities matching the name
        """
        ...

    async def get_by_criteria(self, criteria: dict[str, Any]) -> list[EntityName]:
        """
        Find entities matching specific criteria.

        Args:
            criteria: Dictionary of field names and values

        Returns:
            List of matching entities
        """
        ...

    async def exists_by_name(self, name: str) -> bool:
        """
        Check if entity with given name exists.

        Args:
            name: Entity name to check

        Returns:
            True if exists, False otherwise
        """
        ...

    # Add more custom methods as needed
    # Keep them focused on data access, not business logic
