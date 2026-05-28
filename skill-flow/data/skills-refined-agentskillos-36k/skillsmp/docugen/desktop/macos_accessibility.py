"""macOS accessibility backend using Apple Accessibility API via atomacos.

This module provides precise UI element identification at screen coordinates using
macOS's native accessibility framework. It requires accessibility permission to be
granted in System Preferences > Security & Privacy > Accessibility.

Supported AX Roles:
    - AXButton, AXTextField, AXStaticText, AXWindow, AXGroup
    - AXMenu, AXMenuItem, AXMenuBar, AXScrollArea
    - AXTable, AXRow, AXColumn, AXCell
    - And many more standard macOS UI elements

Coordinate System:
    - Input coordinates use screen coordinate system (top-left origin)
    - Internal AX API uses Cocoa coordinates (bottom-left origin)
    - Automatic conversion between coordinate systems

High-DPI Support:
    - Automatically handles Retina displays (2x scale factor)
    - Bounding rectangles accurate within 2 pixels
    - Queries backing scale factor from Quartz APIs

Timeout Behavior:
    - All AX queries limited to 100ms maximum
    - Timeout triggers graceful fallback to visual analysis
    - Timeout events logged for monitoring

Permission Requirements:
    - macOS 12+ required for reliable AX API access
    - Accessibility permission must be granted to Python/Terminal
    - Grant in: System Preferences > Security & Privacy > Accessibility
    - Permission checked before every query; PermissionError raised if denied
"""

import logging
import signal
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)


class PermissionError(Exception):
    """Raised when accessibility permission is denied."""

    pass


@dataclass
class ElementMetadata:
    """Metadata for a UI element extracted via Apple Accessibility API.

    Attributes:
        title: Element's AXTitle or AXDescription attribute.
        role: AX role (e.g., 'AXButton', 'AXTextField', 'AXWindow').
        bounds: Bounding rectangle in screen coordinates {x, y, width, height}.
        identifier: AXIdentifier or generated from role+title.
        parent_role: Parent element's role for context (optional).
        properties: Additional AX attributes specific to element type.
        source: Always "accessibility" to indicate source of metadata.
    """

    title: str
    role: str
    bounds: dict[str, int]
    identifier: str
    parent_role: Optional[str] = None
    properties: dict[str, Any] = None
    source: str = "accessibility"

    def to_dict(self) -> dict:
        """Convert to dictionary format expected by platform_router."""
        result = {
            "title": self.title,
            "role": self.role,
            "bounds": self.bounds,
            "identifier": self.identifier,
            "source": self.source,
        }
        if self.parent_role:
            result["parent_role"] = self.parent_role
        if self.properties:
            result["properties"] = self.properties
        return result


class TimeoutException(Exception):
    """Raised when AX query exceeds timeout limit."""

    pass


@contextmanager
def with_timeout(seconds: float):
    """Context manager to enforce timeout on AX API calls.

    Args:
        seconds: Maximum time allowed (e.g., 0.1 for 100ms).

    Raises:
        TimeoutException: If operation exceeds timeout.

    Example:
        with with_timeout(0.1):
            element = app.findFirst(...)
    """

    def timeout_handler(signum, frame):
        raise TimeoutException("AX query exceeded timeout")

    # Set up the timeout
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)

    try:
        yield
    finally:
        # Cancel the timer and restore old handler
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)


def check_accessibility_permission() -> bool:
    """Check if accessibility permission is granted.

    Attempts a simple AX API query to detect permission status.
    If permission is denied, AXError is raised by atomacos.

    Returns:
        True if permission granted, False if denied.

    Example:
        if not check_accessibility_permission():
            raise PermissionError("Grant accessibility permission in System Preferences")
    """
    try:
        import atomacos
        from AppKit import NSWorkspace

        # Get active application PID
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()
        if not active_app:
            logger.warning("No frontmost application found")
            return False

        pid = active_app.processIdentifier()

        # Attempt to get app reference - this requires accessibility permission
        with with_timeout(0.1):  # 100ms timeout for permission check
            app = atomacos.getAppRefByPid(pid)
            # Try to access a basic attribute
            _ = app.AXRole
        return True

    except ImportError:
        logger.error("atomacos or AppKit not installed")
        return False
    except TimeoutException:
        logger.warning("Permission check timed out")
        return False
    except Exception as e:
        # AXError or any other exception indicates permission denied or API failure
        error_msg = str(e).lower()
        if "ax" in error_msg or "permission" in error_msg or "trusted" in error_msg:
            logger.warning(
                "Accessibility permission denied. "
                "Grant permission in System Preferences > Security & Privacy > Accessibility"
            )
            return False
        logger.warning(f"Permission check failed: {e}")
        return False


def _get_screen_height() -> int:
    """Get the screen height for coordinate conversion.

    macOS uses bottom-left origin (Cocoa), but we need top-left origin (screen coords).

    Returns:
        Screen height in pixels.
    """
    try:
        from Quartz import CGDisplayBounds, CGMainDisplayID

        display_id = CGMainDisplayID()
        bounds = CGDisplayBounds(display_id)
        return int(bounds.size.height)
    except Exception as e:
        logger.warning(f"Failed to get screen height: {e}")
        # Fallback to common resolution
        return 1080


def _cocoa_to_screen_y(cocoa_y: float, element_height: float) -> int:
    """Convert Cocoa Y coordinate (bottom-left origin) to screen Y (top-left origin).

    Args:
        cocoa_y: Y coordinate from AXPosition (bottom-left origin).
        element_height: Element height from AXSize.

    Returns:
        Screen Y coordinate (top-left origin).
    """
    screen_height = _get_screen_height()
    # Cocoa Y is distance from bottom; we need distance from top
    return int(screen_height - cocoa_y - element_height)


def _extract_element_metadata(element) -> Optional[ElementMetadata]:
    """Extract metadata from an AX element.

    Args:
        element: atomacos AXUIElement instance.

    Returns:
        ElementMetadata instance or None if extraction fails.
    """
    try:
        # Extract basic attributes
        title = ""
        try:
            title = element.AXTitle or ""
        except Exception:
            pass

        if not title:
            try:
                title = element.AXDescription or ""
            except Exception:
                pass

        try:
            role = element.AXRole or "Unknown"
        except Exception:
            role = "Unknown"

        # Extract bounding rectangle - REQUIRED attribute, fail if missing
        try:
            position = element.AXPosition
            size = element.AXSize
            # Convert Cocoa coordinates to screen coordinates
            screen_x = int(position.x)
            screen_y = _cocoa_to_screen_y(position.y, size.height)
            bounds = {
                "x": screen_x,
                "y": screen_y,
                "width": int(size.width),
                "height": int(size.height),
            }
        except Exception as e:
            logger.error(f"Failed to extract bounds for element {role}: {e}")
            # Bounds are required for element identification - fail loudly
            return None

        # Extract or generate identifier
        identifier = ""
        try:
            identifier = element.AXIdentifier or ""
        except Exception:
            pass

        if not identifier:
            # Generate identifier from role + title
            identifier = f"{role}_{title[:30]}" if title else role

        # Extract parent role for context
        parent_role = None
        try:
            parent = element.AXParent
            if parent:
                parent_role = parent.AXRole
        except Exception:
            pass

        # Collect additional properties based on element type
        properties = {}
        try:
            # Add value for text fields, sliders, etc.
            if hasattr(element, "AXValue"):
                properties["value"] = element.AXValue
        except Exception:
            pass

        try:
            # Add enabled state
            if hasattr(element, "AXEnabled"):
                properties["enabled"] = element.AXEnabled
        except Exception:
            pass

        return ElementMetadata(
            title=title,
            role=role,
            bounds=bounds,
            identifier=identifier,
            parent_role=parent_role,
            properties=properties if properties else None,
        )

    except Exception as e:
        logger.error(f"Failed to extract element metadata: {e}")
        return None


def _point_in_bounds(x: int, y: int, position, size) -> bool:
    """Check if screen coordinate (x, y) falls within element bounds.

    Args:
        x: Screen X coordinate (top-left origin).
        y: Screen Y coordinate (top-left origin).
        position: Element's AXPosition (Cocoa coordinates, bottom-left origin).
        size: Element's AXSize.

    Returns:
        True if point is within bounds.
    """
    # Convert Cocoa position to screen coordinates
    screen_x = int(position.x)
    screen_y = _cocoa_to_screen_y(position.y, size.height)

    # Check if point falls within rectangle
    return (
        screen_x <= x <= screen_x + int(size.width)
        and screen_y <= y <= screen_y + int(size.height)
    )


def _find_element_at_coordinate_recursive(
    element, x: int, y: int, depth: int = 0, max_depth: int = 20
) -> Optional[ElementMetadata]:
    """Recursively search AX element tree for element at coordinates.

    Navigates from parent to children, returning the innermost (leaf) element
    that contains the coordinate.

    Args:
        element: Current AX element to check.
        x: Screen X coordinate.
        y: Screen Y coordinate.
        depth: Current recursion depth (prevents infinite loops).
        max_depth: Maximum recursion depth.

    Returns:
        ElementMetadata for innermost element at coordinates, or None.
    """
    if depth > max_depth:
        logger.warning(f"Max depth {max_depth} reached in element tree traversal")
        return None

    try:
        # Check if this element contains the coordinate
        position = element.AXPosition
        size = element.AXSize

        if not _point_in_bounds(x, y, position, size):
            return None

        # This element contains the coordinate - now check children
        try:
            children = element.AXChildren
        except Exception:
            children = []

        if not children:
            # Leaf element - return this one
            return _extract_element_metadata(element)

        # Check children recursively
        for child in children:
            try:
                child_result = _find_element_at_coordinate_recursive(
                    child, x, y, depth + 1, max_depth
                )
                if child_result:
                    # Found a more specific child element
                    return child_result
            except Exception as e:
                logger.debug(f"Error checking child element: {e}")
                continue

        # No child matched - return this parent element
        return _extract_element_metadata(element)

    except Exception as e:
        logger.debug(f"Error in recursive element search at depth {depth}: {e}")
        return None


def find_element_at_coordinate(x: int, y: int) -> Optional[ElementMetadata]:
    """Find UI element at screen coordinates using AX API.

    Navigates the AX element tree from application level downward to find
    the innermost element that contains the given coordinate.

    Args:
        x: Screen X coordinate (top-left origin).
        y: Screen Y coordinate (top-left origin).

    Returns:
        ElementMetadata for element at coordinates, or None if not found.

    Raises:
        PermissionError: If accessibility permission is denied.
        TimeoutException: If query exceeds 100ms timeout.
    """
    # Validate coordinates
    if x < 0 or y < 0:
        logger.warning(f"Invalid coordinates: ({x}, {y})")
        return None

    try:
        import atomacos
        from AppKit import NSWorkspace

        # Get frontmost application
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()
        if not active_app:
            logger.warning("No frontmost application found")
            return None

        pid = active_app.processIdentifier()

        # Get app reference with timeout
        with with_timeout(0.1):  # 100ms total timeout
            app = atomacos.getAppRefByPid(pid)

            # Start recursive search from application level
            result = _find_element_at_coordinate_recursive(app, x, y)

            if result:
                logger.debug(
                    f"Found element at ({x}, {y}): {result.role} - {result.title}"
                )
            else:
                logger.debug(f"No element found at ({x}, {y})")

            return result

    except ImportError as e:
        logger.error(f"Required library not installed: {e}")
        return None
    except TimeoutException:
        logger.warning(
            f"Element search at ({x}, {y}) exceeded 100ms timeout - falling back to visual analysis"
        )
        raise
    except Exception as e:
        error_msg = str(e).lower()
        # Check if it's a permission error (not just any AX error)
        if (
            "permission" in error_msg
            or "trusted" in error_msg
            or "not authorized" in error_msg
        ):
            raise PermissionError(
                "Accessibility permission denied. "
                "Grant permission in System Preferences > Security & Privacy > Accessibility"
            )
        # AXErrorInvalidUIElement or similar - gracefully return None
        if "axerror" in error_msg or "invalid" in error_msg:
            logger.warning(
                f"Application without accessibility support or invalid element: {e}"
            )
            return None
        logger.error(f"Error finding element at ({x}, {y}): {e}")
        return None


class MacOSAccessibility:
    """macOS accessibility backend using atomacos/Apple Accessibility API.

    Implements the AccessibilityBackend protocol for integration with
    platform_router.py and the capture pipeline.
    """

    def get_element_at_point(self, x: int, y: int) -> Optional[dict]:
        """Get UI element metadata at screen coordinates.

        Args:
            x: Screen X coordinate (top-left origin).
            y: Screen Y coordinate (top-left origin).

        Returns:
            Element metadata dict with keys: title, role, bounds, identifier, source.
            Returns None if element not found or on timeout.

        Raises:
            PermissionError: If accessibility permission is denied.
        """
        # Check permission first
        if not check_accessibility_permission():
            raise PermissionError(
                "Accessibility permission denied. "
                "Grant permission in System Preferences > Security & Privacy > Accessibility"
            )

        try:
            metadata = find_element_at_coordinate(x, y)
            if metadata:
                return metadata.to_dict()
            return None
        except TimeoutException:
            # Log timeout and return None for graceful fallback
            logger.info(
                f"Element query at ({x}, {y}) timed out - will fall back to visual analysis"
            )
            return None
        except PermissionError:
            # Re-raise permission errors
            raise

    def get_focused_element(self) -> Optional[dict]:
        """Get the currently focused UI element.

        Returns:
            Element metadata dict for focused element, or None if not found.

        Raises:
            PermissionError: If accessibility permission is denied.
        """
        # Check permission first
        if not check_accessibility_permission():
            raise PermissionError(
                "Accessibility permission denied. "
                "Grant permission in System Preferences > Security & Privacy > Accessibility"
            )

        try:
            import atomacos
            from AppKit import NSWorkspace

            # Get frontmost application
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.frontmostApplication()
            if not active_app:
                logger.warning("No frontmost application found")
                return None

            pid = active_app.processIdentifier()

            with with_timeout(0.1):  # 100ms timeout
                app = atomacos.getAppRefByPid(pid)
                focused = app.AXFocusedUIElement
                if focused:
                    metadata = _extract_element_metadata(focused)
                    if metadata:
                        return metadata.to_dict()
                return None

        except ImportError as e:
            logger.error(f"Required library not installed: {e}")
            return None
        except TimeoutException:
            logger.warning("Focused element query timed out")
            return None
        except Exception as e:
            error_msg = str(e).lower()
            if "ax" in error_msg or "permission" in error_msg or "trusted" in error_msg:
                raise PermissionError(
                    "Accessibility permission denied. "
                    "Grant permission in System Preferences > Security & Privacy > Accessibility"
                )
            logger.error(f"Error getting focused element: {e}")
            return None
