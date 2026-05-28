---
name: python-development-guidelines
description: Use this skill when you need universal guidelines and best practices for Python development across various projects.
---

# Python Development Guidelines

## Overview

This skill provides universal guidelines and best practices for Python development, covering coding standards, project structure, CLI development, and more.

## Code Quality Principles

### 1. Readability First
- Code is read more than written.
- Use clear variable and function names.
- Prefer self-documenting code over comments.
- Maintain consistent formatting.

### 2. KISS (Keep It Simple, Stupid)
- Implement the simplest solution that works.
- Avoid over-engineering and premature optimization.
- Favor easy-to-understand code over clever code.

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions.
- Create reusable components and share utilities across modules.
- Avoid copy-paste programming.

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed.
- Avoid speculative generality and add complexity only when required.

### 5. SOLID Principles
- Follow five design guidelines for maintainable, scalable, and testable code.
- Encourage separation of responsibilities and clear abstractions.

## Project Structure

```text
# Universal Python project structure
project/
├── src/                  # Main source code
│   └── package/          # Importable package
├── tests/                # Test suite
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── pyproject.toml        # Project configuration
├── README.md             # Project overview
└── .gitignore            # Version control ignore
```

## Dependency Management

```bash
# Universal Python dependency management
# Use uv for all package operations
uv add package-name          # Add production dependency
uv add package-name --dev    # Add development dependency
uv remove package-name       # Remove dependency
uv sync --all-extras -U     # Update all dependencies
```

## Type Hints and Annotations

```python
# Universal type hint patterns
from typing import List, Dict, Optional, Union

def process_data(
    input_data: List[Dict[str, Union[int, str]]],
    config: Optional[Dict[str, str]] = None
) -> Dict[str, List[float]]:
    """Process data with type-safe operations"""
    # Implementation with type-checked operations
    return processed_results
```

## Python CLI Development

### Recommended Frameworks
- **Typer**: For simple, type-annotated CLIs.
- **Click**: For more complex CLI applications.
- **Argparse**: For standard library compatibility.

### Universal CLI Example

```python
import typer
from typing import Optional

def main(
    input_file: str = typer.Argument(..., help="Input file path"),
    output_file: Optional[str] = typer.Option(None, "-o", "--output", help="Output file path"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output")
):
    """Universal CLI entry point"""
    # CLI logic here
    typer.echo(f"Processing {input_file}")

if __name__ == "__main__":
    typer.run(main)
```

## Error Handling Patterns

```python
# Universal Python error handling
class DataValidationError(Exception):
    """Custom exception for data validation issues"""
    pass

def validate_input(data: dict) -> None:
    """Validate input data with specific error handling"""
    if not isinstance(data, dict):
        raise DataValidationError("Input must be a dictionary.")
```