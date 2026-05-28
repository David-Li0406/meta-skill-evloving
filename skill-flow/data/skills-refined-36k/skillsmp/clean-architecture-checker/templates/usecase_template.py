"""
Template for creating a use case in the Application layer.

Replace:
- OperationName: Your operation name (e.g., CreatePolitician, MatchSpeakers)
- EntityName: Your entity name
"""

from src.application.dtos.operation_name_dto import (
    OperationNameInputDTO,
    OperationNameOutputDTO,
)
from src.domain.entities.entity_name import EntityName
from src.domain.repositories.entity_name_repository import IEntityNameRepository
from src.domain.services.entity_name_domain_service import EntityNameDomainService


class OperationNameUseCase:
    """
    Use case for [operation description].

    Responsibilities:
    - Validate input via DTO
    - Orchestrate workflow between repositories and services
    - Handle transactions
    - Convert entities to output DTOs
    - Handle errors appropriately

    Does NOT contain business logic - delegates to domain services.
    """

    def __init__(
        self,
        entity_repository: IEntityNameRepository,
        # Add other repository dependencies
        entity_service: EntityNameDomainService,
        # Add other service dependencies
    ):
        """
        Initialize use case with dependencies.

        Args:
            entity_repository: Repository for entity data access
            entity_service: Domain service for business logic
        """
        self.entity_repository = entity_repository
        self.entity_service = entity_service

    async def execute(self, input_dto: OperationNameInputDTO) -> OperationNameOutputDTO:
        """
        Execute the use case.

        Args:
            input_dto: Input data transfer object

        Returns:
            Output data transfer object with result

        Raises:
            ValueError: If validation fails or business rule violated
        """
        try:
            # Step 1: Validate input
            input_dto.validate()

            # Step 2: Fetch required data from repositories
            # Example: existing_entity = await self.entity_repository.find_by_id(...)

            # Step 3: Delegate business logic to domain services
            # Example: result = self.entity_service.process(...)

            # Step 4: Create or update entities
            entity = EntityName(
                id=None,  # New entity
                name=input_dto.name,
                # Map other fields from DTO
            )

            # Step 5: Save via repository
            saved_entity = await self.entity_repository.save(entity)

            # Step 6: Return success output DTO
            return OperationNameOutputDTO(
                success=True,
                entity_id=saved_entity.id,
                message="Operation completed successfully",
            )

        except ValueError as e:
            # Business rule violation or validation error
            return OperationNameOutputDTO(
                success=False, message=str(e), errors=[str(e)]
            )
        except Exception as e:
            # Unexpected error
            return OperationNameOutputDTO(
                success=False,
                message="An unexpected error occurred",
                errors=[str(e)],
            )


class ListOperationNameUseCase:
    """
    Use case for listing entities with filters and pagination.
    """

    def __init__(
        self,
        entity_repository: IEntityNameRepository,
    ):
        self.entity_repository = entity_repository

    async def execute(
        self, input_dto: ListOperationNameInputDTO
    ) -> ListOperationNameOutputDTO:
        """
        Execute listing with pagination.

        Args:
            input_dto: Input with filters and pagination params

        Returns:
            Output with list of entities and pagination info
        """
        try:
            input_dto.validate()

            # Build criteria from filters
            criteria = {}
            if input_dto.name_filter:
                criteria["name"] = input_dto.name_filter

            # Fetch from repository
            entities = await self.entity_repository.find_by_criteria(criteria)

            # Apply pagination (simplified - real implementation might be in repo)
            start = (input_dto.page - 1) * input_dto.page_size
            end = start + input_dto.page_size
            paginated = entities[start:end]

            # Convert entities to dict/DTO
            items = [
                {
                    "id": e.id,
                    "name": e.name,
                    # Add other fields
                }
                for e in paginated
            ]

            return ListOperationNameOutputDTO(
                success=True,
                items=items,
                total_count=len(entities),
                page=input_dto.page,
                page_size=input_dto.page_size,
            )

        except ValueError as e:
            return ListOperationNameOutputDTO(success=False, message=str(e))


class UpdateOperationNameUseCase:
    """
    Use case for updating an entity.
    """

    def __init__(
        self,
        entity_repository: IEntityNameRepository,
        entity_service: EntityNameDomainService,
    ):
        self.entity_repository = entity_repository
        self.entity_service = entity_service

    async def execute(
        self, input_dto: UpdateOperationNameInputDTO
    ) -> UpdateOperationNameOutputDTO:
        """Execute update operation."""
        try:
            input_dto.validate()

            # Find existing entity
            entity = await self.entity_repository.find_by_id(input_dto.id)
            if entity is None:
                return UpdateOperationNameOutputDTO(
                    success=False, message=f"Entity {input_dto.id} not found"
                )

            # Update fields (use entity methods for business rules)
            if input_dto.new_name:
                entity.update_name(input_dto.new_name)

            # Save updated entity
            updated = await self.entity_repository.save(entity)

            return UpdateOperationNameOutputDTO(
                success=True,
                entity_id=updated.id,
                message="Entity updated successfully",
            )

        except ValueError as e:
            return UpdateOperationNameOutputDTO(success=False, message=str(e))


class DeleteOperationNameUseCase:
    """
    Use case for deleting an entity.
    """

    def __init__(self, entity_repository: IEntityNameRepository):
        self.entity_repository = entity_repository

    async def execute(
        self, input_dto: DeleteOperationNameInputDTO
    ) -> DeleteOperationNameOutputDTO:
        """Execute delete operation."""
        try:
            # Check if entity exists
            entity = await self.entity_repository.find_by_id(input_dto.id)
            if entity is None:
                return DeleteOperationNameOutputDTO(
                    success=False, message=f"Entity {input_dto.id} not found"
                )

            # Delete
            deleted = await self.entity_repository.delete(input_dto.id)

            if deleted:
                return DeleteOperationNameOutputDTO(
                    success=True, message="Entity deleted successfully"
                )
            else:
                return DeleteOperationNameOutputDTO(
                    success=False, message="Failed to delete entity"
                )

        except Exception as e:
            return DeleteOperationNameOutputDTO(success=False, message=str(e))
