#!/usr/bin/env python3
"""
md-to-pptx: Convert Markdown to PowerPoint

Main entry point for the md-to-pptx skill.
Supports both MD file conversion and direct content generation.

Usage:
    python md_to_pptx.py input.md -o output.pptx
    python md_to_pptx.py input.md --theme tech_dark
    python md_to_pptx.py input.md --template custom.pptx
"""

import argparse
import os
import sys
from typing import Optional, List, Tuple

# Add script directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
skill_dir = os.path.dirname(script_dir)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from md_parser import parse_markdown, SlideData
from pptx_generator import generate_pptx, THEMES

# Built-in template paths
BUILTIN_TEMPLATES = {
    "business": os.path.join(skill_dir, "assets", "templates", "business_template.pptx"),
    "tech_dark": os.path.join(skill_dir, "assets", "templates", "tech_dark_template.pptx"),
    "education": os.path.join(skill_dir, "assets", "templates", "education_template.pptx"),
    "neumorphism": os.path.join(skill_dir, "assets", "templates", "蓝黄色新拟态行业调研报告PPT模板.pptx"),
}


def print_progress(current: int, total: int, message: str):
    """Print progress to console."""
    bar_width = 30
    filled = int(bar_width * current / total)
    bar = '█' * filled + '░' * (bar_width - filled)
    print(f"\r[{bar}] {current}/{total} - {message}", end='', flush=True)
    if current == total:
        print()  # New line at completion


def get_builtin_template(theme: str) -> Optional[str]:
    """Get path to built-in template for a theme."""
    template_path = BUILTIN_TEMPLATES.get(theme)
    if template_path and os.path.exists(template_path):
        return template_path
    return None


def convert_md_to_pptx(
    input_path: str,
    output_path: Optional[str] = None,
    theme: str = "business",
    template_path: Optional[str] = None,
    use_builtin_template: bool = True,
    verbose: bool = True
) -> Tuple[bool, str, List[str]]:
    """
    Convert Markdown file to PowerPoint presentation.

    Args:
        input_path: Path to input Markdown file
        output_path: Path for output PPTX (default: same name as input)
        theme: Theme name (business, tech_dark, education)
        template_path: Optional path to custom PPTX template
        use_builtin_template: Whether to use built-in template for theme
        verbose: Print progress messages

    Returns:
        Tuple of (success, output_path, warnings)
    """
    warnings = []

    # Validate input
    if not os.path.exists(input_path):
        return False, "", [f"Input file not found: {input_path}"]

    # Determine output path
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{base_name}.pptx"

    # Read Markdown content
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        return False, "", [f"Failed to read input file: {str(e)}"]

    if verbose:
        print(f"📄 Reading: {input_path}")

    # Parse Markdown
    slides, parse_warnings = parse_markdown(md_content)
    warnings.extend(parse_warnings)

    if not slides:
        return False, "", ["No slides generated from Markdown content"]

    if verbose:
        print(f"📊 Parsed {len(slides)} slides")

    # Determine template to use
    actual_template = template_path
    if template_path:
        if not os.path.exists(template_path):
            warnings.append(f"Custom template not found: {template_path}")
            actual_template = None
    elif use_builtin_template:
        actual_template = get_builtin_template(theme)
        if actual_template and verbose:
            print(f"📋 Using built-in template: {os.path.basename(actual_template)}")

    # Generate PPTX
    progress_cb = print_progress if verbose else None
    success, gen_warnings = generate_pptx(
        slides,
        output_path,
        theme=theme,
        template_path=actual_template,
        progress_callback=progress_cb
    )
    warnings.extend(gen_warnings)

    if success and verbose:
        print(f"✅ Created: {os.path.abspath(output_path)}")

    return success, output_path, warnings


def generate_from_content(
    content: str,
    output_path: str,
    theme: str = "business",
    template_path: Optional[str] = None,
    use_builtin_template: bool = True,
    verbose: bool = True
) -> Tuple[bool, List[str]]:
    """
    Generate PPTX from Markdown content string.

    Args:
        content: Markdown content string
        output_path: Path for output PPTX
        theme: Theme name
        template_path: Optional custom template path
        use_builtin_template: Whether to use built-in template
        verbose: Print progress messages

    Returns:
        Tuple of (success, warnings)
    """
    warnings = []

    # Parse content
    slides, parse_warnings = parse_markdown(content)
    warnings.extend(parse_warnings)

    if not slides:
        return False, ["No slides generated from content"]

    if verbose:
        print(f"📊 Generated {len(slides)} slides from content")

    # Determine template
    actual_template = template_path
    if not template_path and use_builtin_template:
        actual_template = get_builtin_template(theme)

    # Generate PPTX
    progress_cb = print_progress if verbose else None
    success, gen_warnings = generate_pptx(
        slides,
        output_path,
        theme=theme,
        template_path=actual_template,
        progress_callback=progress_cb
    )
    warnings.extend(gen_warnings)

    return success, warnings


def list_themes():
    """Print available themes and their templates."""
    print("\n📎 Available themes:")
    print("-" * 50)
    for name, config in THEMES.items():
        template_path = BUILTIN_TEMPLATES.get(name)
        has_template = template_path and os.path.exists(template_path)
        template_status = "✅ Template available" if has_template else "⚠️  No template"

        print(f"  {name:12} - {config.name}")
        print(f"               {template_status}")
        print()


def list_templates():
    """Print available built-in templates."""
    print("\n📋 Built-in templates:")
    print("-" * 50)
    for name, path in BUILTIN_TEMPLATES.items():
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"  {status} {name:12} -> {path}")

    print("\n📁 Custom template location:")
    print(f"   Place your .pptx templates in: {os.path.join(skill_dir, 'assets', 'templates')}")
    print("   Or specify path with --template option")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown to PowerPoint presentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s presentation.md                    # Save to current directory
  %(prog)s presentation.md -o slides.pptx     # Specify output filename
  %(prog)s presentation.md -d ~/Desktop       # Save to Desktop
  %(prog)s presentation.md --theme tech_dark  # Use tech dark theme
  %(prog)s presentation.md --template my.pptx # Use custom template
  %(prog)s --list-themes                      # Show available themes
  %(prog)s --list-templates                   # Show template locations
        """
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="Input Markdown file path"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output PPTX filename (default: input name with .pptx)"
    )
    parser.add_argument(
        "-d", "--directory",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "-t", "--theme",
        default="business",
        choices=list(THEMES.keys()),
        help="Theme style (default: business)"
    )
    parser.add_argument(
        "--template",
        help="Path to custom PPTX template file"
    )
    parser.add_argument(
        "--no-template",
        action="store_true",
        help="Don't use built-in template, generate from scratch"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List available themes and exit"
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List template locations and exit"
    )

    args = parser.parse_args()

    # Handle list commands
    if args.list_themes:
        list_themes()
        return 0

    if args.list_templates:
        list_templates()
        return 0

    # Require input file
    if not args.input:
        parser.print_help()
        return 1

    # Get the original working directory (where user invoked the command)
    # This ensures output goes to user's directory, not skill's directory
    original_cwd = os.getcwd()

    # Determine output path
    output_path = args.output
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_path = f"{base_name}.pptx"

    # Apply directory - default to original working directory
    if args.directory and args.directory != ".":
        # User specified a directory
        output_dir = os.path.expanduser(args.directory)
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(original_cwd, output_dir)
    else:
        # Default: use original working directory (user's current directory)
        output_dir = original_cwd

    # Create directory if needed
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"❌ Cannot create directory: {output_dir}")
            return 1

    # Make output path absolute
    if not os.path.isabs(output_path):
        output_path = os.path.join(output_dir, os.path.basename(output_path))

    # Make input path absolute relative to original cwd
    input_path = args.input
    if not os.path.isabs(input_path):
        input_path = os.path.join(original_cwd, input_path)

    # Convert
    success, final_path, warnings = convert_md_to_pptx(
        input_path,
        output_path,
        theme=args.theme,
        template_path=args.template,
        use_builtin_template=not args.no_template,
        verbose=not args.quiet
    )

    # Print warnings
    if warnings and not args.quiet:
        print("\n⚠️  Warnings:")
        for w in warnings:
            print(f"   - {w}")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
