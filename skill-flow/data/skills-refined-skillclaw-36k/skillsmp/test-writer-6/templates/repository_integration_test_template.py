"""
Template for integration testing repositories with real database.

Replace:
- RepositoryName: Your repository name (e.g., PoliticianRepository)
- EntityName: Your entity name (e.g., Politician)
- EntityNameModel: Your SQLAlchemy model name (e.g., PoliticianModel)

IMPORTANT: Always write tests FIRST (TDD), then implement!
"""

from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.entity_name import EntityName
from src.domain.repositories.base import ISessionAdapter
from src.domain.repositories.unit_of_work import IUnitOfWork
from src.infrastructure.persistence.entity_name_repository import (
    EntityNameRepositoryImpl,
)
from src.infrastructure.persistence.session_adapter import AsyncSessionAdapter
from src.infrastructure.persistence.unit_of_work import UnitOfWorkImpl


@pytest.mark.integration
class TestEntityNameRepositoryIntegration:
    """
    Integration tests for EntityNameRepository.

    These tests use a real test database and are slower than unit tests.
    Mark with @pytest.mark.integration to run separately.
    """

    @pytest.fixture
    async def db_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Create test database session.

        This fixture should be defined in conftest.py.
        Example implementation:
        ```python
        @pytest.fixture
        async def db_session():
            async with async_session_maker() as session:
                yield session
                await session.rollback()
        ```
        """
        # This is a placeholder - actual implementation should be in conftest.py
        raise NotImplementedError("Define db_session fixture in conftest.py")

    @pytest.fixture
    def session_adapter(self, db_session: AsyncSession) -> ISessionAdapter:
        """
        Create ISessionAdapter from database session.

        Polibase pattern: Always use ISessionAdapter, not raw AsyncSession!
        """
        return AsyncSessionAdapter(db_session)

    @pytest.fixture
    def repository(
        self, session_adapter: ISessionAdapter
    ) -> EntityNameRepositoryImpl:
        """
        Create repository with ISessionAdapter.

        IMPORTANT: Repository constructor takes ISessionAdapter, not AsyncSession!
        """
        return EntityNameRepositoryImpl(session=session_adapter)

    @pytest.fixture
    def unit_of_work(self, db_session: AsyncSession) -> IUnitOfWork:
        """
        Create UnitOfWork for transaction tests.

        UnitOfWork manages transactions across multiple repositories.
        """
        return UnitOfWorkImpl(db_session)

    @pytest.fixture
    def sample_entity(self) -> EntityName:
        """
        Create sample entity for tests.

        Use realistic Japanese names for Polibase tests.
        """
        return EntityName(
            id=None,  # Will be assigned by database
            name="山田太郎",  # Use realistic Japanese names
            # Add other fields
        )

    # Basic CRUD tests

    @pytest.mark.asyncio
    async def test_create_persists_entity(
        self, repository: EntityNameRepositoryImpl, sample_entity: EntityName
    ) -> None:
        """Test that create persists entity to database."""
        # Act
        saved = await repository.create(sample_entity)

        # Assert
        assert saved.id is not None
        assert saved.name == "山田太郎"

    @pytest.mark.asyncio
    async def test_get_by_id_returns_entity(
        self, repository: EntityNameRepositoryImpl, sample_entity: EntityName
    ) -> None:
        """Test get_by_id returns saved entity."""
        # Arrange
        saved = await repository.create(sample_entity)

        # Act
        found = await repository.get_by_id(saved.id)

        # Assert
        assert found is not None
        assert found.id == saved.id
        assert found.name == saved.name

    @pytest.mark.asyncio
    async def test_get_by_id_returns_none_when_not_found(
        self, repository: EntityNameRepositoryImpl
    ) -> None:
        """Test get_by_id returns None for non-existent ID."""
        # Act
        found = await repository.get_by_id(999999)

        # Assert
        assert found is None

    @pytest.mark.asyncio
    async def test_get_all_returns_all_entities(
        self, repository: EntityNameRepositoryImpl
    ) -> None:
        """Test get_all returns all persisted entities."""
        # Arrange
        entity1 = EntityName(id=None, name="鈴木一郎")
        entity2 = EntityName(id=None, name="佐藤花子")
        await repository.create(entity1)
        await repository.create(entity2)

        # Act
        all_entities = await repository.get_all()

        # Assert
        assert len(all_entities) >= 2
        names = [e.name for e in all_entities]
        assert "鈴木一郎" in names
        assert "佐藤花子" in names

    @pytest.mark.asyncio
    async def test_update_modifies_entity(
        self, repository: EntityNameRepositoryImpl, sample_entity: EntityName
    ) -> None:
        """Test updating entity persists changes."""
        # Arrange
        saved = await repository.create(sample_entity)
        saved.name = "山田次郎"

        # Act
        updated = await repository.update(saved)
        found = await repository.get_by_id(updated.id)

        # Assert
        assert found is not None
        assert found.name == "山田次郎"

    @pytest.mark.asyncio
    async def test_delete_removes_entity(
        self, repository: EntityNameRepositoryImpl, sample_entity: EntityName
    ) -> None:
        """Test delete removes entity from database."""
        # Arrange
        saved = await repository.create(sample_entity)
        entity_id = saved.id

        # Act
        deleted = await repository.delete(entity_id)
        found = await repository.get_by_id(entity_id)

        # Assert
        assert deleted is True
        assert found is None

    # Custom query tests

    @pytest.mark.asyncio
    async def test_get_by_name_returns_matching_entities(
        self, repository: EntityNameRepositoryImpl
    ) -> None:
        """Test custom query get_by_name returns correct results."""
        # Arrange
        entity1 = EntityName(id=None, name="田中健太")
        entity2 = EntityName(id=None, name="田中健太")
        entity3 = EntityName(id=None, name="高橋美咲")
        await repository.create(entity1)
        await repository.create(entity2)
        await repository.create(entity3)

        # Act
        found = await repository.get_by_name("田中健太")

        # Assert
        assert len(found) >= 2
        assert all(e.name == "田中健太" for e in found)

    @pytest.mark.asyncio
    async def test_get_by_name_returns_empty_list_when_not_found(
        self, repository: EntityNameRepositoryImpl
    ) -> None:
        """Test get_by_name returns empty list for no matches."""
        # Act
        found = await repository.get_by_name("存在しない名前")

        # Assert
        assert found == []

    # Complex query tests

    @pytest.mark.asyncio
    async def test_get_by_criteria_with_multiple_filters(
        self, repository: EntityNameRepositoryImpl
    ) -> None:
        """Test complex query with multiple filter criteria."""
        # Arrange
        entity1 = EntityName(id=None, name="渡辺太郎", status="active")
        entity2 = EntityName(id=None, name="渡辺太郎", status="inactive")
        await repository.create(entity1)
        await repository.create(entity2)

        # Act
        criteria = {"name": "渡辺太郎", "status": "active"}
        found = await repository.get_by_criteria(criteria)

        # Assert
        assert len(found) >= 1
        assert all(e.name == "渡辺太郎" and e.status == "active" for e in found)

    # Foreign key tests

    @pytest.mark.asyncio
    async def test_create_with_foreign_key_creates_relationship(
        self,
        repository: EntityNameRepositoryImpl,
        parent_repository: ParentRepositoryImpl,
    ) -> None:
        """Test saving entity with foreign key creates relationship."""
        # Arrange
        parent = ParentEntity(id=None, name="親エンティティ")
        saved_parent = await parent_repository.create(parent)

        entity = EntityName(id=None, name="子エンティティ", parent_id=saved_parent.id)

        # Act
        saved_entity = await repository.create(entity)
        found = await repository.get_by_id(saved_entity.id)

        # Assert
        assert found is not None
        assert found.parent_id == saved_parent.id

    # Transaction tests with UnitOfWork pattern

    @pytest.mark.asyncio
    async def test_transaction_commits_on_success(
        self, unit_of_work: IUnitOfWork
    ) -> None:
        """
        Test UnitOfWork commits transaction on success.

        Polibase pattern: Use UnitOfWork for multi-repository transactions!
        """
        # Arrange
        entity1 = EntityName(id=None, name="トランザクション1")
        entity2 = EntityName(id=None, name="トランザクション2")

        # Act
        async with unit_of_work:
            repo = unit_of_work.entity_name_repository
            await repo.create(entity1)
            await repo.create(entity2)
            await unit_of_work.commit()

        # Assert - both entities should be persisted
        async with unit_of_work:
            repo = unit_of_work.entity_name_repository
            all_entities = await repo.get_all()
            names = [e.name for e in all_entities]
            assert "トランザクション1" in names
            assert "トランザクション2" in names

    @pytest.mark.asyncio
    async def test_transaction_rollback_on_error(
        self, unit_of_work: IUnitOfWork
    ) -> None:
        """
        Test UnitOfWork rolls back transaction on error.

        Polibase pattern: Exceptions cause rollback automatically!
        """
        # Arrange
        entity = EntityName(id=None, name="ロールバックテスト")

        # Act & Assert
        with pytest.raises(Exception, match="Simulated error"):
            async with unit_of_work:
                repo = unit_of_work.entity_name_repository
                await repo.create(entity)
                # Simulate error before commit
                raise Exception("Simulated error")

        # Assert - entity should NOT be in database
        async with unit_of_work:
            repo = unit_of_work.entity_name_repository
            all_entities = await repo.get_all()
            names = [e.name for e in all_entities]
            assert "ロールバックテスト" not in names

    @pytest.mark.asyncio
    async def test_transaction_with_multiple_repositories(
        self, unit_of_work: IUnitOfWork
    ) -> None:
        """
        Test UnitOfWork coordinates multiple repositories.

        Example: Creating related entities across different repositories.
        """
        # Arrange
        parent = ParentEntity(id=None, name="親エンティティ")
        child = EntityName(id=None, name="子エンティティ")

        # Act
        async with unit_of_work:
            parent_repo = unit_of_work.parent_repository
            entity_repo = unit_of_work.entity_name_repository

            saved_parent = await parent_repo.create(parent)
            child.parent_id = saved_parent.id
            saved_child = await entity_repo.create(child)

            await unit_of_work.commit()

        # Assert - both entities persisted with relationship
        async with unit_of_work:
            entity_repo = unit_of_work.entity_name_repository
            found_child = await entity_repo.get_by_id(saved_child.id)
            assert found_child is not None
            assert found_child.parent_id == saved_parent.id

    # Performance tests (optional)

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_bulk_insert_performance(
        self, repository: EntityNameRepositoryImpl
    ) -> None:
        """
        Test bulk insert of many entities (marked as slow).

        Note: For large datasets, consider using bulk insert methods.
        """
        # Arrange
        entities = [EntityName(id=None, name=f"エンティティ{i}") for i in range(1000)]

        # Act
        for entity in entities:
            await repository.create(entity)

        # Assert
        all_entities = await repository.get_all()
        assert len(all_entities) >= 1000
