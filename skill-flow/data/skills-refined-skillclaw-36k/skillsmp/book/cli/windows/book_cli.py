"""
Book CLI - Command line tool for managing LaTeX book projects.

Usage:
    book init <type>        # Initialize a new book project
    book compile [FILENAME] # Compile a LaTeX file
    book image new          # Generate a new image
    book image edit         # Edit an existing image

Examples:
    book init latex        # Create a new LaTeX book project
    book compile           # Compiles main.tex
    book compile ch01      # Compiles ch01-*.tex (prefix match)
    book image new --path "figures/diagram.png" "A flowchart..."
    book image edit --path "figures/chart.png" "Add a legend"
"""

import sys
from functools import partial
from pathlib import Path

import click

from compile_latex import find_tex_file, run_compile
from init_book import init_project, SUPPORTED_TYPES
from image_gen import generate_image, edit_image


@click.group()
def cli():
    """Book CLI - Tools for managing LaTeX book projects."""
    pass


@cli.command()
@click.argument("filename", default="main")
def compile(filename: str):
    """Compile a LaTeX file from the book.

    FILENAME is the name of the .tex file without extension (default: main).

    Supports prefix matching: 'ch01' will find 'ch01-ettersporselprognoser.tex'

    Examples:

        book compile              # Compiles main.tex

        book compile ch01         # Compiles ch01-*.tex

        book compile chii         # Compiles chii-*.tex
    """
    # Find latex directory relative to current working directory
    cwd = Path.cwd()
    latex_dir = cwd / "latex"

    if not latex_dir.exists():
        click.secho(f"Error: latex directory not found at {latex_dir}", fg="red")
        click.echo("Make sure you run this command from the project root.")
        sys.exit(1)

    # Check for excluded file
    if filename == "localsettings":
        click.secho("Error: localsettings.tex is not a standalone file and cannot be compiled.", fg="red")
        sys.exit(1)

    # Find the tex file
    tex_file = find_tex_file(latex_dir, filename)

    if tex_file is None:
        click.secho(f"Error: Could not find {filename}.tex in {latex_dir}", fg="red")
        sys.exit(1)

    # Compile with click-styled output
    return_code = run_compile(
        tex_file,
        latex_dir,
        echo=click.echo,
        success_style=partial(click.secho, fg="green"),
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


@cli.command()
@click.argument("book_type", type=click.Choice(SUPPORTED_TYPES, case_sensitive=False))
def init(book_type: str):
    """Initialize a new book project.

    BOOK_TYPE is the format: latex, markdown, or html

    Creates:
      - config.yaml with project settings
      - Type-specific folder structure (e.g., latex/)

    Examples:

        book init latex        # Create LaTeX book project

        book init markdown     # Create Markdown book project (not yet supported)
    """
    cwd = Path.cwd()

    return_code = init_project(
        cwd,
        book_type.lower(),
        echo=click.echo,
        success_style=partial(click.secho, fg="green"),
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


@cli.group()
def image():
    """Image generation and editing commands.

    Generate new images or edit existing ones using AI (Gemini API).
    Requires GEMINI_API_KEY in .env file.
    """
    pass


@image.command()
@click.option("--path", "-p", required=True, help="Output path for the image (e.g., figures/flowchart.png)")
@click.option("--resolution", "-r", type=click.Choice(["1K", "2K", "4K"]), default="1K", help="Image resolution")
@click.argument("prompt")
def new(path: str, resolution: str, prompt: str):
    """Generate a new image from a text prompt.

    PROMPT is the text description of the image to generate.

    Examples:

        book image new --path "figures/flowchart.png" "A process flowchart"

        book image new -p "diagrams/network.png" -r 4K "Network topology diagram"
    """
    return_code = generate_image(
        prompt=prompt,
        output_path=Path(path),
        resolution=resolution,
        echo=click.echo,
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


@image.command()
@click.option("--path", "-p", required=True, help="Path to image to edit (will be overwritten)")
@click.option("--resolution", "-r", type=click.Choice(["1K", "2K", "4K"]), default=None, help="Output resolution (auto-detected if not specified)")
@click.argument("prompt")
def edit(path: str, resolution: str | None, prompt: str):
    """Edit an existing image with a text prompt.

    PROMPT is the text instructions for editing the image.
    The edited image overwrites the original file.

    Examples:

        book image edit --path "figures/chart.png" "Add a legend in the corner"

        book image edit -p "logo.png" -r 2K "Change the color scheme to blue"
    """
    return_code = edit_image(
        prompt=prompt,
        image_path=Path(path),
        resolution=resolution,
        echo=click.echo,
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


if __name__ == "__main__":
    cli()
