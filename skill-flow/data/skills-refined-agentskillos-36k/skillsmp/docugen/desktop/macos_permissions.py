"""macOS accessibility permission checking and handling."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Cache permission status per application to avoid repeated checks
_permission_cache: dict[str, bool] = {}


def check_accessibility_permission() -> bool:
    """Query current accessibility permission status without triggering dialog.

    Returns:
        True if accessibility permission is granted, False otherwise.
    """
    try:
        # Try importing atomacos to check if it's available
        import atomacos

        # Attempt a simple operation that requires permission
        # If this fails with PermissionError, we know permission is denied
        try:
            # This is a lightweight check that won't trigger a dialog
            atomacos.NativeUIElement.systemwide()
            return True
        except PermissionError:
            return False
        except Exception as e:
            # Other exceptions mean we have permission but something else failed
            logger.debug("Permission check error (not permission-related): %s", e)
            return True

    except ImportError:
        logger.warning("atomacos not installed, cannot check accessibility permission")
        return False


def get_permission_instructions() -> str:
    """Return formatted message for user to grant accessibility permission.

    Returns:
        Instructions for granting permission in System Preferences.
    """
    return (
        "Accessibility permission is required but not granted.\n"
        "To grant permission:\n"
        "1. Open System Preferences\n"
        "2. Go to Security & Privacy\n"
        "3. Click the Privacy tab\n"
        "4. Select Accessibility from the left sidebar\n"
        "5. Click the lock icon and authenticate\n"
        "6. Add this application to the list or check its box\n"
        "7. Restart the application"
    )


def check_app_permission(app_name: str) -> bool:
    """Check if accessibility permission is granted for a specific application.

    Uses a cache to avoid repeated checks for the same application.

    Args:
        app_name: Name of the application to check.

    Returns:
        True if permission is granted or cached as granted.
    """
    if app_name in _permission_cache:
        return _permission_cache[app_name]

    has_permission = check_accessibility_permission()
    _permission_cache[app_name] = has_permission
    return has_permission


def clear_permission_cache(app_name: Optional[str] = None):
    """Clear the permission cache for a specific app or all apps.

    Args:
        app_name: Specific app to clear, or None to clear all.
    """
    if app_name:
        _permission_cache.pop(app_name, None)
        logger.debug("Cleared permission cache for %s", app_name)
    else:
        _permission_cache.clear()
        logger.debug("Cleared all permission cache")
