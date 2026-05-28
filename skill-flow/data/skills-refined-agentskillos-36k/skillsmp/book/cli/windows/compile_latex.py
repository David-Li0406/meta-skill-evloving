# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Core compilation logic for LaTeX books.

Can be used as:
1. Module: from compile_latex import find_tex_file, run_compile
2. Standalone: uv run compile_latex.py [filename]

Examples:
    uv run compile_latex.py              # Compiles main.tex
    uv run compile_latex.py ch01         # Compiles ch01-*.tex (prefix match)
    uv run compile_latex.py ch01-name    # Compiles specific chapter
"""

import subprocess
import sys
from pathlib import Path


def find_tex_file(latex_dir: Path, name: str) -> Path | None:
    """Find a .tex file by name or prefix in the latex directory."""
    # Exclude localsettings.tex as it's not a standalone file
    if name == "localsettings":
        return None

    # Try exact match first
    for tex_file in latex_dir.rglob(f"{name}.tex"):
        return tex_file

    # Try prefix match (e.g., "chii" matches "chii-arbeidsflyt-og-ki.tex")
    for tex_file in latex_dir.rglob(f"{name}-*.tex"):
        return tex_file

    return None


def run_compile(tex_file: Path, latex_dir: Path, echo=print, success_style=None, error_style=None) -> int:
    """
    Compile a LaTeX file using pdflatex.

    Args:
        tex_file: Path to the .tex file
        latex_dir: Path to the latex directory
        echo: Function for normal output (print or click.echo)
        success_style: Function for success messages (optional, e.g., click.secho with fg="green")
        error_style: Function for error messages (optional, e.g., click.secho with fg="red")
    """
    # Default styled output to regular echo if not provided
    if success_style is None:
        success_style = echo
    if error_style is None:
        error_style = echo

    build_dir = latex_dir / "build"
    build_dir.mkdir(exist_ok=True)

    # Calculate relative path from latex_dir to tex_file (for display)
    rel_path = tex_file.relative_to(latex_dir)

    # For subfiles to work, we must compile from the file's directory
    # so that relative paths like ../../../main.tex resolve correctly
    file_dir = tex_file.parent
    file_name = tex_file.name

    echo(f"Compiling: {rel_path}")
    echo(f"Working directory: {file_dir.relative_to(latex_dir) if file_dir != latex_dir else '.'}")
    echo(f"Output directory: {build_dir}")
    echo("-" * 50)

    # Run pdflatex from the file's directory with absolute output path
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        file_name
    ]

    result = subprocess.run(
        cmd,
        cwd=file_dir,
        capture_output=False
    )

    if result.returncode == 0:
        pdf_name = tex_file.stem + ".pdf"
        echo("-" * 50)
        success_style(f"Success! Output: {build_dir / pdf_name}")
    else:
        echo("-" * 50)
        error_style(f"Compilation failed with return code {result.returncode}")

    return result.returncode


def main():
    """Standalone entry point."""
    cwd = Path.cwd()
    latex_dir = cwd / "latex"

    if not latex_dir.exists():
        print(f"Error: latex directory not found at {latex_dir}")
        print("Make sure you run this command from the project root.")
        sys.exit(1)

    # Get filename from arguments (default: main)
    name = sys.argv[1] if len(sys.argv) > 1 else "main"

    # Check for excluded file
    if name == "localsettings":
        print("Error: localsettings.tex is not a standalone file and cannot be compiled.")
        sys.exit(1)

    # Find the tex file
    tex_file = find_tex_file(latex_dir, name)

    if tex_file is None:
        print(f"Error: Could not find {name}.tex in {latex_dir}")
        sys.exit(1)

    # Compile
    return_code = run_compile(tex_file, latex_dir)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
