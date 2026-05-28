"""Windows accessibility backend using pywinauto UI Automation.

Provides precise UI element identification at screen coordinates using
Windows UI Automation framework via pywinauto (backend='uia').

Supported Control Types:
    - Button, Edit, ComboBox, CheckBox, RadioButton
    - Menu, MenuItem, MenuBar, ToolBar
    - Window, Pane, Group, Tab, TabItem
    - List, ListItem, Tree, TreeItem, DataGrid
    - And all standard Windows UIA control types

Coordinate System:
    - Uses screen coordinates (top-left origin)
    - Windows UI Automation provides screen coordinates directly
    - DPI-aware: uses logical coordinates matching mss capture

Timeout Behavior:
    - All UIA queries limited to 100ms maximum
    - Timeout triggers graceful fallback to visual analysis
    - Timeout events logged for monitoring

Requirements:
    - pip install pywinauto>=0.6.8 comtypes
    - Windows 7+ with UI Automation support
    - No additional permissions required
"""

import logging
import threading
from typing import Optional

logger = logging.getLogger(__name__)


def _query_with_timeout(func, timeout_sec: float = 0.1):
    """Execute a function with a timeout using threading.

    Args:
        func: Callable to execute.
        timeout_sec: Maximum time allowed (default 100ms).

    Returns:
        Function result or None if timed out.
    """
    result = [None]
    exception = [None]

    def wrapper():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    thread.join(timeout=timeout_sec)

    if thread.is_alive():
        logger.warning("UIA query exceeded %dms timeout", int(timeout_sec * 1000))
        return None

    if exception[0]:
        raise exception[0]

    return result[0]


def _extract_element_dict(element) -> Optional[dict]:
    """Extract metadata from a pywinauto UIA element wrapper.

    Args:
        element: pywinauto element wrapper.

    Returns:
        Dict with title, role, bounds, identifier, source keys,
        or None if extraction fails.
    """
    try:
        info = element.element_info

        # Title: window_text or name
        title = ""
        try:
            title = element.window_text() or ""
        except Exception:
            try:
                title = info.name or ""
            except Exception:
                pass

        # Control type as role
        try:
            role = info.control_type or "Unknown"
        except Exception:
            role = "Unknown"

        # Bounding rectangle (screen coordinates)
        try:
            rect = info.rectangle
            bounds = {
                "x": rect.left,
                "y": rect.top,
                "width": rect.right - rect.left,
                "height": rect.bottom - rect.top,
            }
        except Exception as e:
            logger.debug("Failed to get bounds: %s", e)
            return None

        # Automation ID as identifier
        identifier = ""
        try:
            identifier = info.automation_id or ""
        except Exception:
            pass

        if not identifier:
            identifier = f"{role}_{title[:30]}" if title else role

        # Additional properties
        properties = {}
        try:
            properties["enabled"] = info.enabled
        except Exception:
            pass
        try:
            properties["visible"] = info.visible
        except Exception:
            pass

        return {
            "title": title,
            "role": role,
            "bounds": bounds,
            "identifier": identifier,
            "source": "accessibility",
            "properties": properties if properties else None,
        }

    except Exception as e:
        logger.debug("Failed to extract element metadata: %s", e)
        return None


class WindowsAccessibility:
    """Windows accessibility backend using pywinauto UI Automation.

    Implements the AccessibilityBackend protocol for integration with
    platform_router.py and the capture pipeline.
    """

    def __init__(self):
        """Initialize the Windows UIA Desktop instance."""
        from pywinauto import Desktop

        self._desktop = Desktop(backend="uia")

    def get_element_at_point(self, x: int, y: int) -> Optional[dict]:
        """Get UI element metadata at screen coordinates.

        Uses pywinauto's from_point() to locate the UIA element at the
        given screen position.

        Args:
            x: Screen X coordinate.
            y: Screen Y coordinate.

        Returns:
            Element metadata dict with keys: title, role, bounds,
            identifier, source. Returns None if not found or on timeout.
        """
        if x < 0 or y < 0:
            logger.warning("Invalid coordinates: (%d, %d)", x, y)
            return None

        def _query():
            element = self._desktop.from_point(x, y)
            return _extract_element_dict(element)

        try:
            result = _query_with_timeout(_query, timeout_sec=0.1)
            if result:
                logger.debug(
                    "Found element at (%d, %d): %s - %s",
                    x, y, result["role"], result["title"],
                )
            return result
        except ImportError as e:
            logger.error("Required library not installed: %s", e)
            return None
        except Exception as e:
            logger.warning("UIA query failed at (%d, %d): %s", x, y, e)
            return None

    def get_focused_element(self) -> Optional[dict]:
        """Get the currently focused UI element.

        Returns:
            Element metadata dict for focused element, or None if not found.
        """

        def _query():
            try:
                window = self._desktop.top_window()
                focused = window.get_focus()
                if focused:
                    return _extract_element_dict(focused)
            except Exception:
                pass
            return None

        try:
            return _query_with_timeout(_query, timeout_sec=0.1)
        except Exception as e:
            logger.warning("Failed to get focused element: %s", e)
            return None
