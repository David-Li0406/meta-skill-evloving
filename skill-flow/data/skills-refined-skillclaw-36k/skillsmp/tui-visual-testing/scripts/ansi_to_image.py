#!/usr/bin/env python3
"""
Convert ANSI terminal output to a PNG image.

This script renders terminal output with ANSI escape codes to an image,
preserving colors and formatting for visual comparison.

Usage:
    python ansi_to_image.py <input-file> [options]

Options:
    --output FILE          Output PNG file (default: input.png)
    --font-size SIZE       Font size in pixels (default: 14)
    --theme THEME          Color theme: dark, light (default: dark)
    --font FONT            Font family (default: monospace)

Requirements:
    pip install Pillow

Example:
    python ansi_to_image.py /tmp/tui_output.txt --output /tmp/screenshot.png
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


# ANSI color codes to RGB
DARK_THEME = {
    'background': (30, 30, 30),
    'foreground': (204, 204, 204),
    'colors': {
        '30': (0, 0, 0),        # Black
        '31': (204, 0, 0),      # Red
        '32': (0, 204, 0),      # Green
        '33': (204, 204, 0),    # Yellow
        '34': (0, 0, 204),      # Blue
        '35': (204, 0, 204),    # Magenta
        '36': (0, 204, 204),    # Cyan
        '37': (204, 204, 204),  # White
        '90': (128, 128, 128),  # Bright Black
        '91': (255, 0, 0),      # Bright Red
        '92': (0, 255, 0),      # Bright Green
        '93': (255, 255, 0),    # Bright Yellow
        '94': (0, 0, 255),      # Bright Blue
        '95': (255, 0, 255),    # Bright Magenta
        '96': (0, 255, 255),    # Bright Cyan
        '97': (255, 255, 255),  # Bright White
    },
    'bg_colors': {
        '40': (0, 0, 0),
        '41': (204, 0, 0),
        '42': (0, 204, 0),
        '43': (204, 204, 0),
        '44': (0, 0, 204),
        '45': (204, 0, 204),
        '46': (0, 204, 204),
        '47': (204, 204, 204),
        '100': (128, 128, 128),
        '101': (255, 0, 0),
        '102': (0, 255, 0),
        '103': (255, 255, 0),
        '104': (0, 0, 255),
        '105': (255, 0, 255),
        '106': (0, 255, 255),
        '107': (255, 255, 255),
    }
}

LIGHT_THEME = {
    'background': (255, 255, 255),
    'foreground': (0, 0, 0),
    'colors': {
        '30': (0, 0, 0),
        '31': (194, 54, 33),
        '32': (37, 188, 36),
        '33': (173, 173, 39),
        '34': (73, 46, 225),
        '35': (211, 56, 211),
        '36': (51, 187, 200),
        '37': (203, 204, 205),
        '90': (129, 131, 131),
        '91': (252, 57, 31),
        '92': (49, 231, 34),
        '93': (234, 236, 35),
        '94': (88, 51, 255),
        '95': (249, 53, 248),
        '96': (20, 240, 240),
        '97': (233, 235, 235),
    },
    'bg_colors': {
        '40': (0, 0, 0),
        '41': (194, 54, 33),
        '42': (37, 188, 36),
        '43': (173, 173, 39),
        '44': (73, 46, 225),
        '45': (211, 56, 211),
        '46': (51, 187, 200),
        '47': (203, 204, 205),
        '100': (129, 131, 131),
        '101': (252, 57, 31),
        '102': (49, 231, 34),
        '103': (234, 236, 35),
        '104': (88, 51, 255),
        '105': (249, 53, 248),
        '106': (20, 240, 240),
        '107': (233, 235, 235),
    }
}


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_256_color(code: int) -> tuple:
    """Parse 256-color code to RGB."""
    if code < 16:
        # Standard colors
        standard = [
            (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
            (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
            (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
            (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)
        ]
        return standard[code]
    elif code < 232:
        # 216 colors (6x6x6 cube)
        code -= 16
        r = (code // 36) * 51
        g = ((code // 6) % 6) * 51
        b = (code % 6) * 51
        return (r, g, b)
    else:
        # Grayscale
        gray = (code - 232) * 10 + 8
        return (gray, gray, gray)


def parse_ansi(text: str, theme: dict) -> list:
    """Parse ANSI text into a list of (char, fg_color, bg_color, bold) tuples."""
    # Remove cursor control sequences
    text = re.sub(r'\x1b\[\?[0-9;]*[a-zA-Z]', '', text)
    text = re.sub(r'\x1b\[[0-9;]*[HJKfsu]', '', text)

    result = []
    fg_color = theme['foreground']
    bg_color = theme['background']
    bold = False
    underline = False

    i = 0
    while i < len(text):
        if text[i] == '\x1b' and i + 1 < len(text) and text[i + 1] == '[':
            # Parse ANSI escape sequence
            end = i + 2
            while end < len(text) and text[end] not in 'mABCDEFGHJKSTfnsu':
                end += 1
            if end < len(text) and text[end] == 'm':
                codes = text[i+2:end].split(';')
                j = 0
                while j < len(codes):
                    try:
                        code = int(codes[j]) if codes[j] else 0
                    except ValueError:
                        j += 1
                        continue

                    if code == 0:
                        fg_color = theme['foreground']
                        bg_color = theme['background']
                        bold = False
                        underline = False
                    elif code == 1:
                        bold = True
                    elif code == 4:
                        underline = True
                    elif code == 22:
                        bold = False
                    elif code == 24:
                        underline = False
                    elif code == 38:
                        # Extended foreground color
                        if j + 1 < len(codes):
                            try:
                                if int(codes[j + 1]) == 5 and j + 2 < len(codes):
                                    fg_color = parse_256_color(int(codes[j + 2]))
                                    j += 2
                                elif int(codes[j + 1]) == 2 and j + 4 < len(codes):
                                    fg_color = (int(codes[j + 2]), int(codes[j + 3]), int(codes[j + 4]))
                                    j += 4
                            except (ValueError, IndexError):
                                pass
                    elif code == 48:
                        # Extended background color
                        if j + 1 < len(codes):
                            try:
                                if int(codes[j + 1]) == 5 and j + 2 < len(codes):
                                    bg_color = parse_256_color(int(codes[j + 2]))
                                    j += 2
                                elif int(codes[j + 1]) == 2 and j + 4 < len(codes):
                                    bg_color = (int(codes[j + 2]), int(codes[j + 3]), int(codes[j + 4]))
                                    j += 4
                            except (ValueError, IndexError):
                                pass
                    elif str(code) in theme['colors']:
                        fg_color = theme['colors'][str(code)]
                    elif str(code) in theme['bg_colors']:
                        bg_color = theme['bg_colors'][str(code)]
                    elif code == 39:
                        fg_color = theme['foreground']
                    elif code == 49:
                        bg_color = theme['background']
                    j += 1
                i = end + 1
            else:
                i = end + 1
        elif text[i] == '\n':
            result.append(('\n', fg_color, bg_color, bold))
            i += 1
        elif text[i] == '\r':
            i += 1
        else:
            result.append((text[i], fg_color, bg_color, bold))
            i += 1

    return result


def render_to_image(
    parsed: list,
    font_size: int = 14,
    theme: dict = None,
    font_path: str = None
) -> Image:
    """Render parsed ANSI content to an image."""
    if theme is None:
        theme = DARK_THEME

    # Try to load a monospace font
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            # Try common monospace fonts
            font_names = [
                '/System/Library/Fonts/Monaco.ttf',
                '/System/Library/Fonts/Menlo.ttc',
                '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
            ]
            font = None
            for fn in font_names:
                try:
                    font = ImageFont.truetype(fn, font_size)
                    break
                except OSError:
                    continue
            if font is None:
                font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Calculate character dimensions
    bbox = font.getbbox('M')
    char_width = bbox[2] - bbox[0]
    char_height = int(font_size * 1.2)

    # Calculate image dimensions
    lines = []
    current_line = []
    for item in parsed:
        if item[0] == '\n':
            lines.append(current_line)
            current_line = []
        else:
            current_line.append(item)
    if current_line:
        lines.append(current_line)

    max_width = max(len(line) for line in lines) if lines else 80
    height = len(lines) if lines else 24

    # Add padding
    padding = 10
    img_width = max_width * char_width + padding * 2
    img_height = height * char_height + padding * 2

    # Create image
    img = Image.new('RGB', (img_width, img_height), theme['background'])
    draw = ImageDraw.Draw(img)

    # Render text
    y = padding
    for line in lines:
        x = padding
        for char, fg, bg, bold in line:
            # Draw background
            if bg != theme['background']:
                draw.rectangle(
                    [x, y, x + char_width, y + char_height],
                    fill=bg
                )
            # Draw character
            draw.text((x, y), char, font=font, fill=fg)
            x += char_width
        y += char_height

    return img


def main():
    parser = argparse.ArgumentParser(
        description='Convert ANSI terminal output to a PNG image'
    )
    parser.add_argument('input', help='Input file with ANSI content')
    parser.add_argument('--output', help='Output PNG file')
    parser.add_argument('--font-size', type=int, default=14, help='Font size')
    parser.add_argument('--theme', choices=['dark', 'light'], default='dark', help='Color theme')
    parser.add_argument('--font', help='Path to font file')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or str(input_path.with_suffix('.png'))

    theme = DARK_THEME if args.theme == 'dark' else LIGHT_THEME

    # Read input
    with open(input_path, 'r') as f:
        content = f.read()

    # Parse ANSI
    parsed = parse_ansi(content, theme)

    # Render to image
    img = render_to_image(parsed, args.font_size, theme, args.font)

    # Save
    img.save(output_path)
    print(f"Image saved to {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
