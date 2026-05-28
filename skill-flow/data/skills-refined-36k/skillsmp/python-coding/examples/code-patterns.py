"""
Python Code Patterns Examples

This module demonstrates common Python patterns and best practices
for writing clean, maintainable, and well-documented code.
"""

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Generator, Optional


# =============================================================================
# Class Definition with Type Hints
# =============================================================================


@dataclass
class User:
    """
    Represents a user in the system.

    Attributes:
        user_id: Unique identifier for the user.
        username: Display name for the user.
        email: User's email address.
        is_active: Whether the user account is active.
        metadata: Optional additional user metadata.
    """

    user_id: int
    username: str
    email: str
    is_active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def update_email(self, new_email: str) -> None:
        """
        Update the user's email address.

        Args:
            new_email: The new email address to set.

        Raises:
            ValueError: If the email format is invalid.
        """
        if "@" not in new_email:
            raise ValueError(f"Invalid email format: {new_email}")
        self.email = new_email


# =============================================================================
# Function with Comprehensive Docstring
# =============================================================================


def process_user_data(
    users: list[User],
    filter_active: bool = True,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """
    Process a list of users and return formatted data.

    This function filters and transforms user objects into dictionaries
    suitable for API responses or serialization.

    Args:
        users: List of User objects to process.
        filter_active: If True, only include active users (default: True).
        limit: Maximum number of users to return. None means no limit.

    Returns:
        List of dictionaries containing user data with keys:
        - 'id': User ID
        - 'name': Username
        - 'email': Email address

    Example:
        >>> users = [User(1, "alice", "alice@example.com")]
        >>> process_user_data(users)
        [{'id': 1, 'name': 'alice', 'email': 'alice@example.com'}]
    """
    result: list[dict[str, Any]] = []

    for user in users:
        if filter_active and not user.is_active:
            continue

        result.append({
            "id": user.user_id,
            "name": user.username,
            "email": user.email,
        })

        if limit is not None and len(result) >= limit:
            break

    return result


# =============================================================================
# Context Manager Pattern
# =============================================================================


@contextmanager
def managed_resource(resource_name: str) -> Generator[dict[str, Any], None, None]:
    """
    Context manager for handling resources with automatic cleanup.

    Args:
        resource_name: Name of the resource to manage.

    Yields:
        A dictionary representing the managed resource.

    Example:
        >>> with managed_resource("database") as resource:
        ...     resource["data"] = "some value"
        ...     # Resource is automatically cleaned up after the block
    """
    resource: dict[str, Any] = {"name": resource_name, "active": True}
    print(f"Acquiring resource: {resource_name}")

    try:
        yield resource
    finally:
        resource["active"] = False
        print(f"Releasing resource: {resource_name}")


# =============================================================================
# Error Handling Patterns
# =============================================================================


class DataProcessingError(Exception):
    """Base exception for data processing errors."""

    def __init__(self, message: str, source: Optional[str] = None) -> None:
        self.source = source
        super().__init__(message)


class ValidationError(DataProcessingError):
    """Raised when data validation fails."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"Validation failed for '{field}': {message}")


def validate_and_process(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate input data and process it.

    Args:
        data: Dictionary containing data to validate and process.

    Returns:
        Processed data dictionary.

    Raises:
        ValidationError: If required fields are missing or invalid.
        DataProcessingError: If processing fails for other reasons.
    """
    required_fields = ["name", "value"]

    for field_name in required_fields:
        if field_name not in data:
            raise ValidationError(field_name, "Field is required")

    if not isinstance(data["value"], (int, float)):
        raise ValidationError("value", "Must be a number")

    try:
        return {
            "name": data["name"].upper(),
            "value": data["value"] * 2,
            "processed": True,
        }
    except Exception as e:
        raise DataProcessingError(f"Processing failed: {e}") from e

