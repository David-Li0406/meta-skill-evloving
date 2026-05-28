"""Platform-agnostic element metadata schema for desktop accessibility.

This module provides unified dataclasses for representing UI element metadata
from Windows UI Automation and macOS Accessibility API in a consistent format.

Examples:
    Creating a Rect:
        >>> bounds = Rect(x=100, y=200, width=150, height=50)
        >>> print(bounds)
        Rect(x=100, y=200, width=150, height=50)

    Creating ElementMetadata for Windows button:
        >>> metadata = ElementMetadata(
        ...     element_id="button_1",
        ...     name="Submit",
        ...     role="button",
        ...     bounds=Rect(100, 200, 150, 50),
        ...     confidence_score=1.0,
        ...     platform="windows",
        ...     windows_automation_id="submitBtn",
        ...     windows_class_name="Button",
        ...     properties={},
        ...     query_latency_ms=45.2,
        ...     permission_status=None,
        ...     fallback_used=False
        ... )

    Creating ElementMetadata for macOS text field:
        >>> metadata = ElementMetadata(
        ...     element_id="textfield_1",
        ...     name="Username",
        ...     role="text_field",
        ...     bounds=Rect(50, 100, 200, 30),
        ...     confidence_score=0.9,
        ...     platform="macos",
        ...     macos_ax_identifier="usernameField",
        ...     macos_ax_role="AXTextField",
        ...     properties={"AXFocused": True},
        ...     query_latency_ms=120.5,
        ...     permission_status="granted",
        ...     fallback_used=False
        ... )

    Serialization:
        >>> data = metadata.to_dict()
        >>> reconstructed = ElementMetadata.from_dict(data)
        >>> assert metadata == reconstructed
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal, Optional, Any


@dataclass
class Rect:
    """Rectangular bounds with validation.

    Attributes:
        x: X-coordinate of top-left corner (screen or image coordinates)
        y: Y-coordinate of top-left corner (screen or image coordinates)
        width: Width in pixels (must be > 0)
        height: Height in pixels (must be > 0)
    """

    x: int | float
    y: int | float
    width: int | float
    height: int | float

    def validate(self) -> None:
        """Validate that width and height are positive.

        Raises:
            ValueError: If width or height is <= 0
        """
        if self.width <= 0:
            raise ValueError(f"Rect width must be > 0, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"Rect height must be > 0, got {self.height}")

    def to_dict(self) -> dict[str, int | float]:
        """Convert to JSON-serializable dict."""
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Rect:
        """Reconstruct Rect from dict.

        Args:
            data: Dict with keys: x, y, width, height

        Returns:
            Rect instance

        Raises:
            KeyError: If required keys are missing
        """
        return cls(
            x=data["x"], y=data["y"], width=data["width"], height=data["height"]
        )


@dataclass
class ElementMetadata:
    """Unified metadata for UI elements from Windows or macOS accessibility APIs.

    This dataclass normalizes outputs from Windows UI Automation and macOS
    Accessibility API into a consistent schema for annotation placement.

    Attributes:
        element_id: Unique identifier for this element
        name: Display text or accessible name
        role: Normalized role (e.g., "button", "text_field", "window")
        bounds: Rectangular bounds (screen or image coordinates)
        confidence_score: Accuracy metric (0.0 to 1.0)
        platform: Source platform ("windows" or "macos")
        windows_automation_id: Windows UI Automation ID (Windows only)
        windows_class_name: Windows class name (Windows only)
        macos_ax_identifier: macOS AXIdentifier (macOS only)
        macos_ax_role: macOS AXRole string (macOS only)
        properties: Additional platform-specific attributes
        query_latency_ms: Time taken to query element (milliseconds)
        permission_status: macOS accessibility permission status
        fallback_used: Whether visual analysis fallback was used
    """

    element_id: str
    name: str
    role: str
    bounds: Rect
    confidence_score: float
    platform: Literal["windows", "macos"]
    windows_automation_id: Optional[str] = None
    windows_class_name: Optional[str] = None
    macos_ax_identifier: Optional[str] = None
    macos_ax_role: Optional[str] = None
    properties: dict[str, Any] = field(default_factory=dict)
    query_latency_ms: float = 0.0
    permission_status: Optional[str] = None
    fallback_used: bool = False

    def validate(self) -> None:
        """Validate element metadata fields.

        Raises:
            ValueError: If platform, confidence_score, or bounds are invalid
            TypeError: If bounds is not a Rect instance
        """
        if self.platform not in ("windows", "macos"):
            raise ValueError(
                f"Platform must be 'windows' or 'macos', got '{self.platform}'"
            )

        if not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError(
                f"Confidence score must be in [0.0, 1.0], got {self.confidence_score}"
            )

        if not isinstance(self.bounds, Rect):
            raise TypeError(
                f"Bounds must be a Rect instance, got {type(self.bounds).__name__}"
            )

        # Validate bounds (will raise ValueError if width/height <= 0)
        self.bounds.validate()

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        Returns:
            Dict with all ElementMetadata fields, Rect serialized to nested dict
        """
        data = asdict(self)
        # Ensure bounds is serialized as dict (not dataclass)
        data["bounds"] = self.bounds.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ElementMetadata:
        """Reconstruct ElementMetadata from dict.

        Args:
            data: Dict with ElementMetadata fields (bounds as nested dict)

        Returns:
            ElementMetadata instance

        Raises:
            KeyError: If required fields are missing
            ValueError: If field values are invalid
        """
        # Reconstruct Rect from nested dict
        bounds_data = data["bounds"]
        if isinstance(bounds_data, dict):
            bounds = Rect.from_dict(bounds_data)
        elif isinstance(bounds_data, Rect):
            bounds = bounds_data
        else:
            raise TypeError(f"bounds must be dict or Rect, got {type(bounds_data)}")

        return cls(
            element_id=data["element_id"],
            name=data["name"],
            role=data["role"],
            bounds=bounds,
            confidence_score=data["confidence_score"],
            platform=data["platform"],
            windows_automation_id=data.get("windows_automation_id"),
            windows_class_name=data.get("windows_class_name"),
            macos_ax_identifier=data.get("macos_ax_identifier"),
            macos_ax_role=data.get("macos_ax_role"),
            properties=data.get("properties", {}),
            query_latency_ms=data.get("query_latency_ms", 0.0),
            permission_status=data.get("permission_status"),
            fallback_used=data.get("fallback_used", False),
        )
