# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
Core book initialization logic.

Creates config.yaml and calls type-specific init scripts.

Can be used as:
1. Module: from init_book import init_project
2. Standalone: uv run init_book.py <type>

Examples:
    uv run init_book.py latex
    uv run init_book.py markdown
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # Will fail gracefully if run without yaml


SUPPORTED_TYPES = ["latex", "markdown", "html"]


def create_config(project_root: Path, book_type: str, echo=print) -> None:
    """Create or update config.yaml with the book type."""
    config_path = project_root / "config.yaml"

    if config_path.exists():
        # Load existing config
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        # Add type to list if not already present
        if "types" not in config:
            config["types"] = []
        if book_type not in config["types"]:
            config["types"].append(book_type)
            echo(f"Added '{book_type}' to existing config.yaml")
        else:
            echo(f"Type '{book_type}' already in config.yaml")
    else:
        # Create new config
        config = {
            "types": [book_type]
        }
        echo(f"Created config.yaml with type '{book_type}'")

    # Write config
    with open(config_path, "w", encoding="utf-8") as f:
        f.write("# Book project configuration\n")
        yaml.dump(config, f, default_flow_style=False)


def init_project(project_root: Path, book_type: str, echo=print, success_style=None, error_style=None) -> int:
    """
    Initialize a book project.

    Args:
        project_root: Path to the project root
        book_type: Type of book (latex, markdown, html)
        echo: Function for normal output
        success_style: Function for success messages
        error_style: Function for error messages

    Returns:
        0 on success, 1 on error
    """
    if success_style is None:
        success_style = echo
    if error_style is None:
        error_style = echo

    # Validate type
    if book_type not in SUPPORTED_TYPES:
        error_style(f"Error: Unsupported type '{book_type}'. Supported: {', '.join(SUPPORTED_TYPES)}")
        return 1

    echo(f"Initializing {book_type} book project in {project_root}")
    echo("-" * 50)

    # Create config.yaml
    if yaml is None:
        error_style("Error: PyYAML not installed. Run: pip install pyyaml")
        return 1

    create_config(project_root, book_type, echo)

    # Call type-specific init
    if book_type == "latex":
        from init_latex import scaffold_latex
        scaffold_latex(project_root, echo)
    elif book_type == "markdown":
        error_style("Error: Markdown support not yet implemented")
        return 1
    elif book_type == "html":
        error_style("Error: HTML support not yet implemented")
        return 1

    echo("-" * 50)
    success_style(f"Book project initialized successfully!")
    return 0


def main():
    """Standalone entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run init_book.py <type>")
        print(f"Types: {', '.join(SUPPORTED_TYPES)}")
        sys.exit(1)

    book_type = sys.argv[1].lower()
    project_root = Path.cwd()

    return_code = init_project(project_root, book_type)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
