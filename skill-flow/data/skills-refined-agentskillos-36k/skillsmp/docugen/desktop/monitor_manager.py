"""Monitor detection and management for multi-display setups."""

from dataclasses import dataclass

from .platform_utils import get_dpi_scale


@dataclass
class MonitorInfo:
    """Information about a single display monitor."""

    index: int  # 1-based monitor number
    left: int
    top: int
    width: int
    height: int
    is_primary: bool = False
    dpi_scale: float = 1.0

    @property
    def logical_width(self) -> int:
        """Width in logical (UI) pixels."""
        return int(self.width / self.dpi_scale)

    @property
    def logical_height(self) -> int:
        """Height in logical (UI) pixels."""
        return int(self.height / self.dpi_scale)

    def to_mss_region(self) -> dict:
        """Convert to mss-compatible region dict."""
        return {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
        }


class MonitorManager:
    """Lazily detects and manages display monitors."""

    def __init__(self):
        self._monitors: list[MonitorInfo] | None = None
        self._dpi_scale = get_dpi_scale()

    def _load_monitors(self) -> list[MonitorInfo]:
        """Load monitor info from mss (called lazily on first access)."""
        import mss

        monitors = []
        with mss.mss() as sct:
            # sct.monitors[0] is the combined virtual screen
            # sct.monitors[1:] are individual monitors
            for i, mon in enumerate(sct.monitors[1:], start=1):
                monitors.append(
                    MonitorInfo(
                        index=i,
                        left=mon["left"],
                        top=mon["top"],
                        width=mon["width"],
                        height=mon["height"],
                        is_primary=(i == 1),
                        dpi_scale=self._dpi_scale,
                    )
                )
        return monitors

    @property
    def monitors(self) -> list[MonitorInfo]:
        """All detected monitors (lazy-loaded)."""
        if self._monitors is None:
            self._monitors = self._load_monitors()
        return self._monitors

    @property
    def primary(self) -> MonitorInfo | None:
        """The primary monitor, or None if no monitors detected."""
        for mon in self.monitors:
            if mon.is_primary:
                return mon
        return self.monitors[0] if self.monitors else None

    def get_by_index(self, index: int) -> MonitorInfo | None:
        """Get monitor by 1-based index.

        Args:
            index: 1-based monitor number.

        Returns:
            MonitorInfo or None if index is out of range.
        """
        for mon in self.monitors:
            if mon.index == index:
                return mon
        return None

    def get_virtual_screen(self) -> dict:
        """Get the combined virtual screen region (all monitors).

        Returns:
            mss-compatible region dict spanning all monitors.
        """
        import mss

        with mss.mss() as sct:
            return dict(sct.monitors[0])

    @property
    def count(self) -> int:
        """Number of monitors detected."""
        return len(self.monitors)

    def refresh(self) -> None:
        """Force re-detection of monitors (e.g., after display change)."""
        self._monitors = None
