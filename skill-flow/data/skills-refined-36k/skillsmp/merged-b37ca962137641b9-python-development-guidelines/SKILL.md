---
name: python-development-guidelines
description: Use this skill when you need universal guidelines and best practices for Python development, including coding standards, CLI patterns, and project organization.
---

# Python Development Guidelines

## Overview

This document provides universal guidelines and best practices for Python development, applicable across various projects and domains. It covers coding standards, command-line interface (CLI) patterns, project structure, and more.

## Coding Standards & Best Practices

### Code Quality Principles

1. **Readability First**
   - Code is read more than written.
   - Use clear variable and function names.
   - Prefer self-documenting code over comments.
   - Maintain consistent formatting.

2. **KISS (Keep It Simple, Stupid)**
   - Opt for the simplest solution that works.
   - Avoid over-engineering and premature optimization.

3. **DRY (Don't Repeat Yourself)**
   - Extract common logic into functions and create reusable components.

4. **YAGNI (You Aren't Gonna Need It)**
   - Avoid building features before they are needed.

5. **SOLID Principles**
   - Follow design guidelines for maintainable, scalable, and testable code.

### Python Standards

#### Variable Naming

```python
# ✅ GOOD: Descriptive names (snake_case)
market_search_query = 'election'
is_user_authenticated = True
```

#### Function Naming

```python
# ✅ GOOD: Verb-noun pattern (snake_case)
async def fetch_market_data(market_id: str) -> dict:
    pass
```

#### Error Handling

```python
# ✅ GOOD: Comprehensive error handling
async def fetch_data(url: str) -> dict:
    try:
        # Implementation
    except Exception as e:
        # Handle error
```

### Project Structure

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

### Dependency Management

```bash
# Use uv for all package operations
uv add package-name          # Add production dependency
uv add package-name --dev    # Add development dependency
uv remove package-name       # Remove dependency
uv sync --all-extras -U     # Update all dependencies
```

### Type Hints and Annotations

```python
from typing import List, Dict, Optional, Union

def process_data(
    input_data: List[Dict[str, Union[int, str]]],
    config: Optional[Dict[str, str]] = None
) -> Dict[str, List[float]]:
    """Process data with type-safe operations"""
    # Implementation
```

## Python CLI Development Patterns

### Framework Selection

**Recommended Frameworks:**
- **Typer**: For simple, type-annotated CLIs.
- **Click**: For more complex CLI applications.
- **Argparse**: For standard library compatibility.

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

if __name__ == "__main__":
    typer.run(main)
```

### Error Handling and User Feedback

```python
def handle_cli_error(error, context="CLI"):
    """Handle errors with user-friendly messages"""
    if isinstance(error, FileNotFoundError):
        print(f"File not found: {error.filename}")
    else:
        print(f"{context} error: {str(error)}")
```

## Best Practices

1. **Consistency**: Apply the same patterns across all Python projects.
2. **Type Safety**: Use complete type annotations.
3. **Testing**: Implement comprehensive test coverage.
4. **Documentation**: Use Google-style docstrings and provide clear help text.

## Compatibility

Works with:
- Python 3.8+ projects.
- Any Python application type.
- Cross-project standardization.
- Organizational Python guidelines.

**Remember**: Clear, maintainable code enables rapid development and confident refactoring.