"""Cross-platform window enumeration for targeting specific application windows."""

import logging
from typing import Optional

from .platform_utils import get_os

logger = logging.getLogger(__name__)


class WindowEnumerator:
    """Lists visible windows with their IDs, titles, and bounding boxes.

    Delegates to platform-specific implementations. Falls back gracefully
    when platform libraries are unavailable.
    """

    def __init__(self):
        self._os = get_os()

    def list_windows(self) -> list[dict]:
        """List all visible, non-minimized windows.

        Returns:
            List of dicts with keys: 'id', 'title', 'bbox'.
            bbox contains: 'left', 'top', 'width', 'height'.
            Returns empty list if enumeration is unavailable.
        """
        try:
            if self._os == "windows":
                return _list_windows_win32()
            elif self._os == "macos":
                return _list_windows_macos()
            elif self._os == "linux":
                return _list_windows_linux()
        except ImportError as e:
            logger.warning("Window enumeration unavailable: %s", e)
        except Exception as e:
            logger.error("Window enumeration failed: %s", e)
        return []

    def find_by_title(
        self, title: str, exact: bool = False
    ) -> Optional[dict]:
        """Find first window matching the given title.

        Args:
            title: Title to search for.
            exact: If True, requires exact match. Otherwise substring match.

        Returns:
            Window dict or None.
        """
        windows = self.list_windows()
        if exact:
            return next((w for w in windows if w["title"] == title), None)
        title_lower = title.lower()
        return next(
            (w for w in windows if title_lower in w["title"].lower()), None
        )

    def find_by_pid(self, pid: int) -> list[dict]:
        """Find windows belonging to a specific process ID.

        Args:
            pid: Process ID.

        Returns:
            List of window dicts for that process (may be empty).
        """
        windows = self.list_windows()
        return [w for w in windows if w.get("pid") == pid]


def _list_windows_win32() -> list[dict]:
    """Enumerate windows on Windows using win32gui."""
    import win32gui
    import win32process

    windows = []

    def enum_callback(hwnd, _results):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return

        # Check if minimized
        style = win32gui.GetWindowLong(hwnd, -16)  # GWL_STYLE
        if style & 0x20000000:  # WS_MINIMIZE
            return

        rect = win32gui.GetWindowRect(hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]

        if width <= 0 or height <= 0:
            return

        # Get process ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        windows.append({
            "id": hwnd,
            "title": title,
            "pid": pid,
            "bbox": {
                "left": rect[0],
                "top": rect[1],
                "width": width,
                "height": height,
            },
        })

    win32gui.EnumWindows(enum_callback, None)
    return windows


def _list_windows_macos() -> list[dict]:
    """Enumerate windows on macOS using Quartz."""
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )

    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly, kCGNullWindowID
    )

    windows = []
    for window in window_list:
        title = window.get("kCGWindowName")
        if not title:
            continue

        bounds = window.get("kCGWindowBounds")
        if not bounds:
            continue

        width = int(bounds.get("Width", 0))
        height = int(bounds.get("Height", 0))
        if width <= 0 or height <= 0:
            continue

        windows.append({
            "id": window.get("kCGWindowNumber"),
            "title": title,
            "pid": window.get("kCGWindowOwnerPID"),
            "bbox": {
                "left": int(bounds["X"]),
                "top": int(bounds["Y"]),
                "width": width,
                "height": height,
            },
        })

    return windows


def _list_windows_linux() -> list[dict]:
    """Enumerate windows on Linux using Xlib (X11 only)."""
    from Xlib import display, X
    from Xlib.error import XError

    d = display.Display()
    root = d.screen().root
    windows = []

    try:
        client_list_atom = d.intern_atom("_NET_CLIENT_LIST")
        prop = root.get_full_property(client_list_atom, X.AnyPropertyType)
        if prop is None:
            return windows

        net_wm_name_atom = d.intern_atom("_NET_WM_NAME")
        utf8_atom = d.intern_atom("UTF8_STRING")
        net_wm_pid_atom = d.intern_atom("_NET_WM_PID")

        for window_id in prop.value:
            try:
                window = d.create_resource_object("window", window_id)
                attrs = window.get_attributes()

                if attrs.map_state != X.IsViewable:
                    continue

                # Get window title
                name_prop = window.get_full_property(net_wm_name_atom, utf8_atom)
                if name_prop:
                    title = name_prop.value.decode("utf-8", "ignore")
                else:
                    title = window.get_wm_name()

                if not title:
                    continue

                # Get geometry
                geom = window.get_geometry()
                if geom.width <= 0 or geom.height <= 0:
                    continue

                # Translate coordinates to root window space
                translated = root.translate_coords(window, 0, 0)
                x, y = translated.x, translated.y

                # Get PID if available
                pid = None
                pid_prop = window.get_full_property(
                    net_wm_pid_atom, X.AnyPropertyType
                )
                if pid_prop:
                    pid = int(pid_prop.value[0])

                windows.append({
                    "id": window_id,
                    "title": title,
                    "pid": pid,
                    "bbox": {
                        "left": x,
                        "top": y,
                        "width": geom.width,
                        "height": geom.height,
                    },
                })

            except XError:
                continue
    except XError:
        pass
    finally:
        d.close()

    return windows
