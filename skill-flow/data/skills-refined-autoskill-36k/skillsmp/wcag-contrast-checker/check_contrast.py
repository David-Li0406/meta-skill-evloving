#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "colour>=0.1.5",
# ]
# ///
"""
WCAG Color Contrast Ratio Checker

This script calculates the contrast ratio between two colors according to
WCAG 2.0 guidelines and reports compliance levels.
"""

import argparse
import sys
from colour import Color


def calculate_relative_luminance(color: Color) -> float:
    """
    Calculate the relative luminance of a color according to WCAG.
    
    Formula: L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    where R, G, B are the linearized RGB values.
    """
    def linearize(channel: float) -> float:
        """Convert sRGB channel value to linear RGB."""
        if channel <= 0.03928:
            return channel / 12.92
        else:
            return ((channel + 0.055) / 1.055) ** 2.4
    
    r, g, b = color.red, color.green, color.blue
    
    r_linear = linearize(r)
    g_linear = linearize(g)
    b_linear = linearize(b)
    
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear


def calculate_contrast_ratio(color1: Color, color2: Color) -> float:
    """
    Calculate the contrast ratio between two colors according to WCAG.
    
    Formula: (L1 + 0.05) / (L2 + 0.05)
    where L1 is the relative luminance of the lighter color
    and L2 is the relative luminance of the darker color.
    """
    l1 = calculate_relative_luminance(color1)
    l2 = calculate_relative_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def check_wcag_compliance(ratio: float) -> dict:
    """
    Check WCAG compliance levels for a given contrast ratio.
    
    Returns a dictionary with compliance information for AA and AAA levels.
    """
    return {
        'AA_normal': ratio >= 4.5,      # Normal text (< 18pt or < 14pt bold)
        'AA_large': ratio >= 3.0,       # Large text (>= 18pt or >= 14pt bold)
        'AAA_normal': ratio >= 7.0,     # Normal text (< 18pt or < 14pt bold)
        'AAA_large': ratio >= 4.5,      # Large text (>= 18pt or >= 14pt bold)
    }


def parse_color(color_string: str) -> Color:
    """
    Parse a CSS color string into a Color object.
    
    Supports: hex (#fff, #ffffff), rgb/rgba, hsl/hsla, and named colors.
    """
    import re
    
    # Strip whitespace
    color_string = color_string.strip()
    
    # Handle rgb/rgba format
    rgb_match = re.match(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*[\d.]+)?\s*\)', color_string, re.IGNORECASE)
    if rgb_match:
        r, g, b = rgb_match.groups()
        # Convert to hex format that colour library understands
        hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
        try:
            return Color(hex_color)
        except (ValueError, AttributeError) as e:
            print(f"Error: Could not parse RGB color '{color_string}'", file=sys.stderr)
            sys.exit(1)
    
    # Handle hsl/hsla format
    hsl_match = re.match(r'hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%(?:\s*,\s*[\d.]+)?\s*\)', color_string, re.IGNORECASE)
    if hsl_match:
        h, s, l = hsl_match.groups()
        try:
            # colour library can handle hsl format
            return Color(hsl=(float(h)/360, float(s)/100, float(l)/100))
        except (ValueError, AttributeError) as e:
            print(f"Error: Could not parse HSL color '{color_string}'", file=sys.stderr)
            sys.exit(1)
    
    # Try parsing as-is (hex or named color)
    try:
        return Color(color_string)
    except (ValueError, AttributeError) as e:
        print(f"Error: Could not parse color '{color_string}'", file=sys.stderr)
        print(f"Please provide a valid CSS color (e.g., '#fff', 'rgb(255,255,255)', 'white')", file=sys.stderr)
        sys.exit(1)


def format_color_display(color: Color) -> str:
    """Format a color for display with multiple representations."""
    hex_val = color.hex_l
    rgb = f"rgb({int(color.red * 255)}, {int(color.green * 255)}, {int(color.blue * 255)})"
    return f"{hex_val} ({rgb})"


def main():
    parser = argparse.ArgumentParser(
        description="Check WCAG color contrast ratios between two colors.",
        epilog="Example: %(prog)s --foreground '#333' --background '#fff'"
    )
    parser.add_argument(
        "--foreground",
        required=True,
        help="Foreground color (supports hex, rgb, rgba, hsl, hsla, and named colors)"
    )
    parser.add_argument(
        "--background",
        required=True,
        help="Background color (supports hex, rgb, rgba, hsl, hsla, and named colors)"
    )

    args = parser.parse_args()

    # Parse colors
    foreground = parse_color(args.foreground)
    background = parse_color(args.background)
    
    # Calculate contrast ratio
    ratio = calculate_contrast_ratio(foreground, background)
    
    # Check WCAG compliance
    compliance = check_wcag_compliance(ratio)
    
    # Display results
    print("=" * 60)
    print("WCAG Color Contrast Analysis")
    print("=" * 60)
    print()
    print(f"Foreground: {format_color_display(foreground)}")
    print(f"Background: {format_color_display(background)}")
    print()
    print(f"Contrast Ratio: {ratio:.2f}:1")
    print()
    print("WCAG Compliance:")
    print("-" * 60)
    
    # AA Level
    print("Level AA:")
    print(f"  • Normal text (< 18pt):     {'✓ PASS' if compliance['AA_normal'] else '✗ FAIL'} (requires 4.5:1)")
    print(f"  • Large text (≥ 18pt):      {'✓ PASS' if compliance['AA_large'] else '✗ FAIL'} (requires 3.0:1)")
    print()
    
    # AAA Level
    print("Level AAA:")
    print(f"  • Normal text (< 18pt):     {'✓ PASS' if compliance['AAA_normal'] else '✗ FAIL'} (requires 7.0:1)")
    print(f"  • Large text (≥ 18pt):      {'✓ PASS' if compliance['AAA_large'] else '✗ FAIL'} (requires 4.5:1)")
    print()
    
    # Summary
    if compliance['AAA_normal']:
        level = "AAA (excellent)"
    elif compliance['AA_normal']:
        level = "AA (good)"
    elif compliance['AA_large']:
        level = "AA for large text only (limited)"
    else:
        level = "FAIL (insufficient contrast)"
    
    print("=" * 60)
    print(f"Overall: {level}")
    print("=" * 60)


if __name__ == "__main__":
    main()
