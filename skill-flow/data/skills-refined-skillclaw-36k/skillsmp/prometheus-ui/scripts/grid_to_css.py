#!/usr/bin/env python3
"""
Prometheus Grid to CSS Converter

Converts Grid Unit coordinates to CSS viewport units (vw/vh) 
based on the Prometheus Implementation Viewport Baseline (1890×940).

Usage:
    python grid_to_css.py <x> <y>
    python grid_to_css.py <x> <y> --width <w> --height <h>
    python grid_to_css.py --batch <file.csv>

Examples:
    python grid_to_css.py -875 -375
    python grid_to_css.py 0 -400 --width 908 --height 76
"""

import argparse
import sys
import csv

# Implementation Viewport Baseline
VIEWPORT_WIDTH = 1890
VIEWPORT_HEIGHT = 940
ORIGIN_X = 945  # Centre X in pixels
ORIGIN_Y = 470  # Centre Y in pixels


def grid_x_to_vw(x: float) -> float:
    """Convert Grid X coordinate to CSS left (vw)"""
    return ((ORIGIN_X + x) / VIEWPORT_WIDTH) * 100


def grid_y_to_vh(y: float) -> float:
    """Convert Grid Y coordinate to CSS bottom (vh)"""
    return ((ORIGIN_Y + y) / VIEWPORT_HEIGHT) * 100


def px_to_vw(px: float) -> float:
    """Convert pixel width to viewport width units (vw)"""
    return (px / VIEWPORT_WIDTH) * 100


def px_to_vh(px: float) -> float:
    """Convert pixel height to viewport height units (vh)"""
    return (px / VIEWPORT_HEIGHT) * 100


def vw_to_px(vw: float) -> float:
    """Convert viewport width units to pixels"""
    return (vw / 100) * VIEWPORT_WIDTH


def vh_to_px(vh: float) -> float:
    """Convert viewport height units to pixels"""
    return (vh / 100) * VIEWPORT_HEIGHT


def format_conversion(x: float, y: float, width: float = None, height: float = None) -> str:
    """Format a complete CSS conversion result"""
    left_vw = grid_x_to_vw(x)
    bottom_vh = grid_y_to_vh(y)
    
    result = []
    result.append("=" * 60)
    result.append("PROMETHEUS GRID CONVERSION")
    result.append("=" * 60)
    result.append(f"Input Grid Position: X: {x:+.0f}, Y: {y:+.0f}")
    result.append("")
    result.append("CSS OUTPUT:")
    result.append(f"  left:   {left_vw:.2f}vw")
    result.append(f"  bottom: {bottom_vh:.2f}vh")
    
    if width is not None and height is not None:
        width_vw = px_to_vw(width)
        height_vh = px_to_vh(height)
        result.append("")
        result.append(f"Input Dimensions: {width:.0f}px × {height:.0f}px")
        result.append("SIZE OUTPUT:")
        result.append(f"  width:  {width_vw:.2f}vw")
        result.append(f"  height: {height_vh:.2f}vh")
    
    result.append("")
    result.append("AFFIRMATION PROTOCOL:")
    result.append(f"Grid conversion applied: X:{x:+.0f} → {left_vw:.2f}vw, Y:{y:+.0f} → {bottom_vh:.2f}vh")
    result.append("Implementation baseline: 1890×940")
    result.append("=" * 60)
    
    return "\n".join(result)


def format_css_rule(x: float, y: float, width: float = None, height: float = None) -> str:
    """Output just the CSS properties"""
    lines = []
    lines.append(f"left: {grid_x_to_vw(x):.2f}vw;")
    lines.append(f"bottom: {grid_y_to_vh(y):.2f}vh;")
    
    if width is not None:
        lines.append(f"width: {px_to_vw(width):.2f}vw;")
    if height is not None:
        lines.append(f"height: {px_to_vh(height):.2f}vh;")
    
    return "\n".join(lines)


def process_batch_file(filepath: str) -> str:
    """Process a CSV file of conversions
    
    CSV format: name,x,y[,width,height]
    """
    results = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # Skip header if present
        
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            
            name = row[0] if len(row) > 0 else "unnamed"
            x = float(row[1]) if len(row) > 1 else 0
            y = float(row[2]) if len(row) > 2 else 0
            width = float(row[3]) if len(row) > 3 and row[3] else None
            height = float(row[4]) if len(row) > 4 and row[4] else None
            
            css = format_css_rule(x, y, width, height)
            results.append(f"/* {name} - Grid: X:{x:+.0f}, Y:{y:+.0f} */")
            results.append(css)
            results.append("")
    
    return "\n".join(results)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Prometheus Grid Units to CSS viewport units",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -875 -375              Position only
  %(prog)s 0 -400 -w 908 -H 76    Position with dimensions
  %(prog)s --batch elements.csv   Process multiple elements

Coordinate System:
  Origin (0,0) at viewport centre
  X: -945 to +945 (negative left, positive right)
  Y: -470 to +470 (positive up, negative down)
  
Implementation Baseline: 1890×940 pixels
        """
    )
    
    parser.add_argument('x', type=float, nargs='?', help='Grid X coordinate')
    parser.add_argument('y', type=float, nargs='?', help='Grid Y coordinate')
    parser.add_argument('-w', '--width', type=float, help='Width in pixels')
    parser.add_argument('-H', '--height', type=float, help='Height in pixels')
    parser.add_argument('--batch', type=str, help='CSV file for batch processing')
    parser.add_argument('--css-only', action='store_true', help='Output only CSS properties')
    
    args = parser.parse_args()
    
    if args.batch:
        print(process_batch_file(args.batch))
    elif args.x is not None and args.y is not None:
        if args.css_only:
            print(format_css_rule(args.x, args.y, args.width, args.height))
        else:
            print(format_conversion(args.x, args.y, args.width, args.height))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
