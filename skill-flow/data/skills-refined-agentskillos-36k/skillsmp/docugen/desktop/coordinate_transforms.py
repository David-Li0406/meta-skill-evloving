"""Coordinate transformation utilities for DPI scaling and multi-monitor support.

This module provides functions to transform coordinates between screen space,
DPI-scaled space, and image space. It handles:
- DPI scaling (standard 96/72 DPI and high-DPI displays at 125%, 150%, 200%)
- Multi-monitor setups with negative coordinates on secondary monitors
- Bounds clipping to ensure annotations stay within image dimensions

DPI Scale Values:
- 1.0: Standard DPI (96 DPI on Windows, 72 DPI on macOS)
- 1.25: 120 DPI (125% scaling)
- 1.5: 144 DPI (150% scaling)
- 2.0: 192 DPI / Retina (200% scaling)

Examples:
    Scale bounds for high-DPI display:
        >>> bounds = Rect(100, 200, 150, 50)
        >>> scaled = scale_bounds(bounds, dpi_scale=2.0)
        >>> print(scaled)
        Rect(x=200, y=400, width=300, height=100)

    Clip bounds to image dimensions:
        >>> bounds = Rect(1800, 900, 300, 200)  # Partially off-screen
        >>> clipped = clip_bounds_to_image(bounds, image_width=1920, image_height=1080)
        >>> print(clipped)
        Rect(x=1800, y=900, width=120, height=180)

    Transform screen coordinates to image coordinates:
        >>> image_x, image_y = transform_to_image_coordinates(
        ...     screen_x=1920, screen_y=100,
        ...     dpi_scale=1.5,
        ...     image_width=1920, image_height=1080,
        ...     screen_offset_x=1920, screen_offset_y=0
        ... )
        >>> print(image_x, image_y)
        0 150

    Validate multi-monitor coordinates:
        >>> validate_screen_coordinates(-1920, 100, 1920, 1080)  # Secondary monitor
        True
        >>> validate_screen_coordinates(50000, 100, 1920, 1080)  # Far outside
        False
"""

from __future__ import annotations

import platform
import sys
from typing import Tuple

from .element_metadata import Rect


def get_dpi_scale_factor() -> float:
    """Get current display DPI scale factor.

    Returns platform-specific DPI scaling:
    - Windows: GetDpiForSystem() / 96.0
    - macOS: NSScreen.backingScaleFactor
    - Other: 1.0 (fallback)

    Returns:
        DPI scale factor (1.0 for standard DPI, 1.25/1.5/2.0 for high-DPI)
    """
    system = platform.system()

    if system == "Windows":
        try:
            import ctypes

            # GetDpiForSystem() returns system DPI (96, 120, 144, 192, etc.)
            gdi32 = ctypes.windll.gdi32
            dpi = gdi32.GetDpiForSystem()
            return dpi / 96.0
        except Exception:
            return 1.0

    elif system == "Darwin":  # macOS
        try:
            # Use NSScreen backingScaleFactor (1.0 for standard, 2.0 for Retina)
            from Cocoa import NSScreen  # type: ignore

            main_screen = NSScreen.mainScreen()
            if main_screen:
                return main_screen.backingScaleFactor()
            return 1.0
        except Exception:
            return 1.0

    else:
        # Fallback for Linux or unknown platforms
        return 1.0


def scale_bounds(bounds: Rect, dpi_scale: float) -> Rect:
    """Scale rectangular bounds by DPI scale factor.

    Multiplies x, y, width, height by dpi_scale. Rounds to int to handle
    fractional pixels.

    Args:
        bounds: Original bounds
        dpi_scale: DPI scale factor (1.0, 1.25, 1.5, 2.0, etc.)

    Returns:
        New Rect with scaled coordinates

    Examples:
        >>> bounds = Rect(100, 200, 150, 50)
        >>> scale_bounds(bounds, 1.5)
        Rect(x=150, y=300, width=225, height=75)
        >>> scale_bounds(bounds, 2.0)
        Rect(x=200, y=400, width=300, height=100)
    """
    return Rect(
        x=round(bounds.x * dpi_scale),
        y=round(bounds.y * dpi_scale),
        width=round(bounds.width * dpi_scale),
        height=round(bounds.height * dpi_scale),
    )


def clip_bounds_to_image(
    bounds: Rect, image_width: int, image_height: int
) -> Rect:
    """Clip bounds to image dimensions to prevent annotations outside image.

    Handles:
    - Bounds extending past right/bottom edges (reduces width/height)
    - Negative x/y coordinates from off-screen elements (clamps to 0)
    - Bounds completely off-screen (returns minimal valid Rect)

    Args:
        bounds: Original bounds (may extend outside image)
        image_width: Image width in pixels
        image_height: Image height in pixels

    Returns:
        New Rect with coordinates clamped to [0, image_width] x [0, image_height]

    Examples:
        >>> bounds = Rect(1800, 900, 300, 200)
        >>> clip_bounds_to_image(bounds, 1920, 1080)
        Rect(x=1800, y=900, width=120, height=180)

        >>> bounds = Rect(-50, -100, 200, 150)  # Off-screen top-left
        >>> clip_bounds_to_image(bounds, 1920, 1080)
        Rect(x=0, y=0, width=150, height=50)
    """
    # Clamp x, y to [0, image dimensions]
    new_x = max(0, min(bounds.x, image_width))
    new_y = max(0, min(bounds.y, image_height))

    # Calculate how much was clipped from left/top
    x_clip = new_x - bounds.x
    y_clip = new_y - bounds.y

    # Adjust width/height to account for clipping and right/bottom edges
    new_width = max(1, min(bounds.width - x_clip, image_width - new_x))
    new_height = max(1, min(bounds.height - y_clip, image_height - new_y))

    return Rect(x=new_x, y=new_y, width=new_width, height=new_height)


def validate_screen_coordinates(
    x: int, y: int, screen_width: int, screen_height: int
) -> bool:
    """Validate screen coordinates with multi-monitor support.

    Returns True if coordinates are within reasonable screen bounds.
    Accepts negative coordinates for secondary monitors positioned left/above
    the primary monitor.

    Reasonable bounds: -10000 to +10000 pixels (covers typical multi-monitor setups)

    Args:
        x: Screen X coordinate
        y: Screen Y coordinate
        screen_width: Primary screen width (reference)
        screen_height: Primary screen height (reference)

    Returns:
        True if coordinates are within reasonable screen space

    Examples:
        >>> validate_screen_coordinates(100, 200, 1920, 1080)  # Primary monitor
        True
        >>> validate_screen_coordinates(-1920, 100, 1920, 1080)  # Secondary left
        True
        >>> validate_screen_coordinates(-50000, 100, 1920, 1080)  # Far outside
        False
    """
    # Allow coordinates in reasonable multi-monitor range
    # Typical setups: 4K primary (3840x2160) + 2 secondary = ~11520 width max
    MAX_REASONABLE = 10000
    MIN_REASONABLE = -10000

    if not (MIN_REASONABLE <= x <= MAX_REASONABLE):
        return False
    if not (MIN_REASONABLE <= y <= MAX_REASONABLE):
        return False

    return True


def transform_to_image_coordinates(
    screen_x: int,
    screen_y: int,
    dpi_scale: float,
    image_width: int,
    image_height: int,
    screen_offset_x: int = 0,
    screen_offset_y: int = 0,
) -> Tuple[int, int]:
    """Transform screen coordinates to image coordinates.

    Workflow:
    1. Subtract screen_offset (for region captures, not full screen)
    2. Apply DPI scaling
    3. Clamp to image dimensions [0, image_width] x [0, image_height]

    Args:
        screen_x: Screen X coordinate
        screen_y: Screen Y coordinate
        dpi_scale: DPI scale factor (1.0, 1.25, 1.5, 2.0, etc.)
        image_width: Image width in pixels
        image_height: Image height in pixels
        screen_offset_x: Offset for region captures (default 0)
        screen_offset_y: Offset for region captures (default 0)

    Returns:
        Tuple of (image_x, image_y) clamped to image dimensions

    Examples:
        >>> transform_to_image_coordinates(
        ...     screen_x=1920, screen_y=100, dpi_scale=1.0,
        ...     image_width=1920, image_height=1080,
        ...     screen_offset_x=0, screen_offset_y=0
        ... )
        (1920, 100)

        >>> transform_to_image_coordinates(
        ...     screen_x=1920, screen_y=100, dpi_scale=1.5,
        ...     image_width=1920, image_height=1080,
        ...     screen_offset_x=1920, screen_offset_y=0
        ... )
        (0, 150)
    """
    # Subtract screen offset (for region captures)
    x_relative = screen_x - screen_offset_x
    y_relative = screen_y - screen_offset_y

    # Apply DPI scaling
    x_scaled = round(x_relative * dpi_scale)
    y_scaled = round(y_relative * dpi_scale)

    # Clamp to image dimensions
    image_x = max(0, min(x_scaled, image_width))
    image_y = max(0, min(y_scaled, image_height))

    return (image_x, image_y)
