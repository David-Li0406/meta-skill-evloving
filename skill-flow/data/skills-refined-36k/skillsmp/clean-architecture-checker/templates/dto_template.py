"""
Template for creating DTOs (Data Transfer Objects) in the Application layer.

Replace:
- OperationName: Your operation name (e.g., CreatePolitician, UpdateSpeaker)
"""

from dataclasses import dataclass


@dataclass
class OperationNameInputDTO:
    """
    Input DTO for [operation description].

    This DTO carries data from the interface layer to the use case.
    It should contain only data needed for the operation.
    """

    # Required fields
    name: str
    # Add your required fields

    # Optional fields
    description: str | None = None
    # Add your optional fields

    # Note: DTOs in Polibase typically don't have validate() methods
    # Validation can be done in the use case if needed
    # Keep DTOs simple - they are just data carriers


@dataclass
class OperationNameOutputDTO:
    """
    Output DTO for [operation description].

    This DTO carries the result back to the interface layer.
    """

    # Success indicator
    success: bool

    # Result data
    entity_id: int | None = None

    # User-friendly message
    message: str = ""

    # Error details (if any)
    errors: list[str] | None = None


@dataclass
class GetOperationNameInputDTO:
    """
    Input DTO for retrieving a single entity.
    """

    entity_id: int


@dataclass
class GetOperationNameOutputDTO:
    """
    Output DTO for retrieving a single entity.
    """

    success: bool
    entity_id: int | None = None
    name: str | None = None
    # Add your entity fields here
    message: str = ""


@dataclass
class ListOperationNameInputDTO:
    """
    Input DTO for listing entities with filters and pagination.
    """

    # Pagination
    page: int = 1
    page_size: int = 20

    # Sorting
    sort_by: str = "created_at"
    sort_order: str = "desc"  # "asc" or "desc"

    # Filters (optional)
    name_filter: str | None = None
    # Add your filter fields


@dataclass
class ListOperationNameOutputDTO:
    """
    Output DTO for listing entities.
    """

    success: bool
    items: list[dict] = None  # Or use specific item DTO
    total_count: int = 0
    page: int = 1
    page_size: int = 20
    message: str = ""

    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.items is None:
            self.items = []


@dataclass
class UpdateOperationNameInputDTO:
    """
    Input DTO for updating an entity.
    """

    entity_id: int
    name: str | None = None
    # Add fields that can be updated
    # Use None to indicate "no change"


@dataclass
class UpdateOperationNameOutputDTO:
    """
    Output DTO for update operation.
    """

    success: bool
    entity_id: int | None = None
    message: str = ""


@dataclass
class DeleteOperationNameInputDTO:
    """
    Input DTO for deleting an entity.
    """

    entity_id: int


@dataclass
class DeleteOperationNameOutputDTO:
    """
    Output DTO for delete operation.
    """

    success: bool
    message: str = ""
