"""Cross-platform screenshot capture using mss.

Supports fullscreen, specific monitor, window, and region capture modes
with DPI awareness and graceful error handling.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .monitor_manager import MonitorManager, MonitorInfo
from .platform_utils import get_dpi_scale


@dataclass
class CaptureResult:
    """Result of a screenshot capture operation."""

    image_bytes: bytes  # Raw PNG bytes
    width: int  # Physical pixel width
    height: int  # Physical pixel height
    dpi_scale: float = 1.0
    monitor_index: Optional[int] = None
    window_title: Optional[str] = None
    region: Optional[dict] = None
    metadata: dict = field(default_factory=dict)

    @property
    def logical_width(self) -> int:
        return int(self.width / self.dpi_scale)

    @property
    def logical_height(self) -> int:
        return int(self.height / self.dpi_scale)

    def save(self, path: str | Path) -> Path:
        """Save the captured image to a file.

        Args:
            path: Destination file path.

        Returns:
            The resolved Path where the file was saved.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.image_bytes)
        return path


class ScreenCapture:
    """Cross-platform screen capture with DPI awareness.

    Usage:
        capture = ScreenCapture()
        result = capture.fullscreen()
        result.save("screenshot.png")

        # Specific monitor
        result = capture.monitor(2)

        # Region
        result = capture.region(left=100, top=100, width=800, height=600)

        # Window (requires window_enumerator)
        result = capture.window(window_id=12345)
    """

    def __init__(self):
        self._monitor_manager = MonitorManager()
        self._dpi_scale = get_dpi_scale()

    @property
    def monitors(self) -> MonitorManager:
        """Access the monitor manager."""
        return self._monitor_manager

    def fullscreen(self, monitor_index: Optional[int] = None) -> CaptureResult:
        """Capture the full screen or a specific monitor.

        Args:
            monitor_index: 1-based monitor number. None captures primary monitor.

        Returns:
            CaptureResult with PNG image bytes and metadata.

        Raises:
            ValueError: If the specified monitor index doesn't exist.
            RuntimeError: If screenshot capture fails.
        """
        if monitor_index is not None:
            monitor = self._monitor_manager.get_by_index(monitor_index)
            if monitor is None:
                available = self._monitor_manager.count
                raise ValueError(
                    f"Monitor {monitor_index} not found. "
                    f"Available monitors: 1-{available}"
                )
            region = monitor.to_mss_region()
        else:
            # Primary monitor
            monitor = self._monitor_manager.primary
            if monitor is None:
                raise RuntimeError("No monitors detected.")
            region = monitor.to_mss_region()

        return self._grab(
            region,
            monitor_index=monitor.index if monitor else None,
        )

    def all_monitors(self) -> CaptureResult:
        """Capture the combined virtual screen (all monitors).

        Returns:
            CaptureResult spanning all connected displays.
        """
        region = self._monitor_manager.get_virtual_screen()
        return self._grab(region, metadata={"mode": "all_monitors"})

    def monitor(self, index: int) -> CaptureResult:
        """Capture a specific monitor by index.

        Args:
            index: 1-based monitor number.

        Returns:
            CaptureResult for the specified monitor.
        """
        return self.fullscreen(monitor_index=index)

    def region(self, left: int, top: int, width: int, height: int) -> CaptureResult:
        """Capture a specific rectangular region of the screen.

        Args:
            left: X coordinate of the top-left corner.
            top: Y coordinate of the top-left corner.
            width: Width in pixels.
            height: Height in pixels.

        Returns:
            CaptureResult for the specified region.

        Raises:
            ValueError: If width or height is <= 0.
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid region size: {width}x{height}")

        capture_region = {
            "left": left,
            "top": top,
            "width": width,
            "height": height,
        }
        return self._grab(capture_region, region_info=capture_region)

    def window(self, window_id: int) -> CaptureResult:
        """Capture a specific window by its platform ID.

        Uses the window enumerator to find the window's bounding box,
        then captures that region.

        Args:
            window_id: Platform-specific window identifier.

        Returns:
            CaptureResult for the window's bounding box.

        Raises:
            ValueError: If the window is not found.
        """
        from .window_enumerator import WindowEnumerator

        enumerator = WindowEnumerator()
        windows = enumerator.list_windows()
        target = next((w for w in windows if w["id"] == window_id), None)

        if target is None:
            raise ValueError(
                f"Window with ID {window_id} not found or is not visible."
            )

        bbox = target["bbox"]
        capture_region = {
            "left": bbox["left"],
            "top": bbox["top"],
            "width": bbox["width"],
            "height": bbox["height"],
        }

        return self._grab(
            capture_region,
            window_title=target.get("title"),
            region=capture_region,
        )

    def window_by_title(self, title: str, exact: bool = False) -> CaptureResult:
        """Capture a window matching the given title.

        Args:
            title: Window title to search for.
            exact: If True, requires exact match. Otherwise uses substring match.

        Returns:
            CaptureResult for the first matching window.

        Raises:
            ValueError: If no matching window is found.
        """
        from .window_enumerator import WindowEnumerator

        enumerator = WindowEnumerator()
        windows = enumerator.list_windows()

        if exact:
            target = next((w for w in windows if w["title"] == title), None)
        else:
            title_lower = title.lower()
            target = next(
                (w for w in windows if title_lower in w["title"].lower()), None
            )

        if target is None:
            available = [w["title"] for w in windows[:10]]
            raise ValueError(
                f"No window matching '{title}'. "
                f"Available windows: {available}"
            )

        return self.window(target["id"])

    def _grab(
        self,
        region: dict,
        monitor_index: Optional[int] = None,
        window_title: Optional[str] = None,
        region_info: Optional[dict] = None,
        metadata: Optional[dict] = None,
        **kwargs,
    ) -> CaptureResult:
        """Internal: perform the actual mss grab and return CaptureResult."""
        import mss
        import mss.tools

        try:
            with mss.mss() as sct:
                sct_img = sct.grab(region)
                png_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)

                return CaptureResult(
                    image_bytes=png_bytes,
                    width=sct_img.size.width,
                    height=sct_img.size.height,
                    dpi_scale=self._dpi_scale,
                    monitor_index=monitor_index,
                    window_title=window_title,
                    region=kwargs.get("region") or region_info,
                    metadata=metadata or {},
                )
        except Exception as e:
            raise RuntimeError(f"Screenshot capture failed: {e}") from e
