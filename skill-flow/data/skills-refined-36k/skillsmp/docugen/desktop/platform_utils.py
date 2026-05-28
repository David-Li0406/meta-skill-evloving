"""Platform detection and capability reporting for desktop capture."""

import platform
from dataclasses import dataclass, field


@dataclass
class PlatformInfo:
    """Describes the current platform and its capture capabilities."""

    os: str  # 'windows', 'macos', 'linux'
    version: str
    dpi_scale: float = 1.0
    has_accessibility: bool = False
    has_window_enumeration: bool = False
    notes: list[str] = field(default_factory=list)


def get_platform() -> PlatformInfo:
    """Detect the current platform and its capabilities.

    Returns:
        PlatformInfo with os name, version, DPI scale, and capability flags.
    """
    system = platform.system().lower()

    if system == "windows":
        return _detect_windows()
    elif system == "darwin":
        return _detect_macos()
    elif system == "linux":
        return _detect_linux()
    else:
        return PlatformInfo(
            os="unknown",
            version=platform.version(),
            notes=[f"Unsupported platform: {system}. Capture may not work."],
        )


def get_os() -> str:
    """Simple OS name detection. Returns 'windows', 'macos', or 'linux'.

    Raises:
        NotImplementedError: If the OS is not supported.
    """
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")


def get_dpi_scale() -> float:
    """Get the display DPI scale factor for the primary display.

    Returns:
        Scale factor (1.0 = standard, 2.0 = Retina/HiDPI).
    """
    system = platform.system().lower()

    if system == "darwin":
        return _get_macos_dpi_scale()
    elif system == "windows":
        return _get_windows_dpi_scale()
    else:
        return 1.0


def _detect_windows() -> PlatformInfo:
    info = PlatformInfo(os="windows", version=platform.version())
    info.has_window_enumeration = True
    info.dpi_scale = _get_windows_dpi_scale()

    try:
        import win32gui  # noqa: F401

        info.has_accessibility = True
    except ImportError:
        info.notes.append("pywin32 not installed; window enumeration unavailable")
        info.has_window_enumeration = False

    return info


def _detect_macos() -> PlatformInfo:
    info = PlatformInfo(
        os="macos", version=platform.mac_ver()[0] or platform.version()
    )
    info.dpi_scale = _get_macos_dpi_scale()
    info.has_window_enumeration = True

    try:
        from Quartz import CGWindowListCopyWindowInfo  # noqa: F401

        info.has_accessibility = True
    except ImportError:
        info.notes.append(
            "pyobjc-framework-Quartz not installed; window enumeration limited"
        )
        info.has_window_enumeration = False

    return info


def _detect_linux() -> PlatformInfo:
    info = PlatformInfo(os="linux", version=platform.version())

    try:
        from Xlib import display  # noqa: F401

        info.has_window_enumeration = True
    except ImportError:
        info.notes.append("python-xlib not installed; window enumeration unavailable")

    return info


def _get_macos_dpi_scale() -> float:
    """Detect Retina scale factor on macOS."""
    try:
        from Quartz import CGDisplayScreenSize, CGMainDisplayID, CGDisplayPixelsWide

        display_id = CGMainDisplayID()
        pixel_width = CGDisplayPixelsWide(display_id)
        physical_size_mm = CGDisplayScreenSize(display_id)
        if physical_size_mm.width > 0:
            # Standard is ~110 PPI; Retina is ~220 PPI
            ppi = pixel_width / (physical_size_mm.width / 25.4)
            if ppi > 150:
                return 2.0
    except Exception:
        pass
    return 1.0  # Fallback: assume non-Retina


def _get_windows_dpi_scale() -> float:
    """Detect DPI scale on Windows."""
    try:
        import ctypes

        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        dpi = user32.GetDpiForSystem()
        return dpi / 96.0
    except Exception:
        pass
    return 1.0
