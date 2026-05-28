"""
Template for creating a new domain entity.

Replace:
- EntityName: Your entity name (e.g., Politician, Speaker)
- field_name: Your field names
- FieldType: Your field types
"""

from datetime import datetime

from src.domain.entities.base import BaseEntity


class EntityName(BaseEntity):
    """
    Domain entity representing [description].

    Business Rules:
    - [List key business rules here]
    - [e.g., name cannot be empty]
    - [e.g., email must be unique]
    """

    def __init__(
        self,
        name: str,
        # Add your required fields here
        description: str | None = None,
        # Add your optional fields here
        id: int | None = None,
    ) -> None:
        """
        Initialize entity.

        Args:
            name: Entity name (required)
            description: Optional description
            id: Entity ID (None for new entities, set by database)
        """
        super().__init__(id)  # Initialize BaseEntity with id
        self.name = name
        self.description = description
        # Add your other fields here

        # Note: created_at and updated_at are managed by BaseEntity
        # and set by the repository layer, not here

    def validate(self) -> None:
        """
        Validate business rules.

        Note: This method can be called explicitly when needed.
        It is NOT called automatically in __init__.

        Raises:
            ValueError: If validation fails
        """
        if not self.name or not self.name.strip():
            raise ValueError("Name is required")

        # Add your validation rules here
        # Example:
        # if len(self.name) > 100:
        #     raise ValueError("Name too long (max 100 characters)")

    def update_name(self, new_name: str) -> None:
        """
        Update entity name with business rule validation.

        Args:
            new_name: New name value

        Raises:
            ValueError: If new name is invalid
        """
        if not new_name or not new_name.strip():
            raise ValueError("Name cannot be empty")

        self.name = new_name
        # Note: updated_at timestamp is managed by repository layer

    # Add other business methods here
    # Keep them focused on this entity's state and rules
    # Avoid complex logic that involves multiple entities
    # (that belongs in domain services)
