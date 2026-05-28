---
name: python-cli-click
description: |
  Patterns for building Click CLI applications with Rich output formatting, shell completion,
  and interactive pickers. Use when creating new CLI commands, adding shell completion,
  implementing interactive selection, or testing CLI functionality. Covers command groups,
  formatters, exit codes, and CliRunner testing.
version: 1.0.0
tags:
  - python
  - cli
  - click
  - rich
  - testing
---

# Python Click CLI Patterns

## Overview

This skill documents the CLI patterns used in the context-harness project. The CLI is built with Click for command parsing, Rich for beautiful terminal output, and Questionary for interactive selection.

The architecture follows a clean separation:
- **main.py**: Root command group and entry point
- **{feature}_cmd.py**: Feature-specific command groups
- **formatters.py**: Centralized Rich output functions
- **completion.py**: Shell completion and interactive pickers

## When to Use This Skill

Activate this skill when:
- Creating a new CLI command or subcommand
- Working with files in `src/context_harness/interfaces/cli/`
- Adding shell completion to a Click argument
- Implementing interactive pickers with Questionary
- Integrating Rich output formatting
- Writing tests for CLI commands with CliRunner

---

## Command Group Organization

### Root CLI Entry Point

The main CLI is defined in `main.py` with version option and subcommand registration:

```python
# src/context_harness/interfaces/cli/main.py
from __future__ import annotations

import click

from context_harness import __version__
from context_harness.interfaces.cli.init_cmd import init_command
from context_harness.interfaces.cli.mcp_cmd import mcp_group
from context_harness.interfaces.cli.skill_cmd import skill_group


@click.group()
@click.version_option(version=__version__, prog_name="context-harness")
def main() -> None:
    """ContextHarness CLI - Initialize agent frameworks in your project.

    A context-aware agent framework for OpenCode.ai that maintains session
    continuity through user-driven compaction cycles.
    """
    pass


# Register command groups
main.add_command(init_command, name="init")
main.add_command(mcp_group, name="mcp")
main.add_command(skill_group, name="skill")


def cli_main() -> None:
    """Entry point for the CLI."""
    main()


if __name__ == "__main__":
    cli_main()
```

### Feature Command Group

Each feature gets its own command group in a separate file:

```python
# src/context_harness/interfaces/cli/{feature}_cmd.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

import click

from context_harness.interfaces.cli.formatters import (
    console,
    print_header,
    print_success,
    print_warning,
    print_error,
    print_info,
    print_bold,
)


@click.group("feature")
def feature_group() -> None:
    """Manage feature X.

    Detailed description of what this command group does.
    """
    pass


@feature_group.command("action")
@click.option(
    "--target",
    "-t",
    default=".",
    type=click.Path(),
    help="Target directory (default: current directory).",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Overwrite existing files without prompting.",
)
def feature_action(target: str, force: bool) -> None:
    """Do something with the feature.

    Examples:

        context-harness feature action

        context-harness feature action --target ./my-project

        context-harness feature action --force
    """
    print_header("Feature Action")
    
    # Implementation...
    result = do_something(target, force=force)
    
    if result == Result.SUCCESS:
        print_success("Action completed successfully!")
    elif result == Result.ALREADY_EXISTS:
        print_warning("Already exists.")
        raise SystemExit(0)  # Not an error
    elif result == Result.ERROR:
        print_error("Action failed.")
        raise SystemExit(1)
```

---

## Rich Console Integration

### Centralized Formatters

All Rich formatting is centralized in `formatters.py`:

```python
# src/context_harness/interfaces/cli/formatters.py
from __future__ import annotations

from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from context_harness import __version__

# Shared console instance - import this in command modules
console = Console()


def print_header(title: str, subtitle: Optional[str] = None) -> None:
    """Print a styled header panel."""
    console.print()
    console.print(
        Panel.fit(
            f"[bold blue]ContextHarness[/bold blue] {title}",
            subtitle=subtitle or f"v{__version__}",
        )
    )
    console.print()


def print_success(message: str) -> None:
    """Print a success message with checkmark."""
    console.print(f"[green]✅ {message}[/green]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def print_error(message: str) -> None:
    """Print an error message with X."""
    console.print(f"[red]❌ {message}[/red]")


def print_info(message: str) -> None:
    """Print an informational message (dimmed)."""
    console.print(f"[dim]{message}[/dim]")


def print_bold(message: str) -> None:
    """Print bold text."""
    console.print(f"[bold]{message}[/bold]")


def print_next_steps(steps: List[str]) -> None:
    """Print a list of next steps."""
    console.print()
    console.print("[bold]Next steps:[/bold]")
    for i, step in enumerate(steps, 1):
        console.print(f"  {i}. {step}")
    console.print()
```

---

## Error Handling Patterns

### Exit Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 0 | Success | Operation completed successfully |
| 0 | User cancelled | User cancelled interactive picker |
| 0 | Already exists | Item already exists (informational) |
| 1 | Error | Operation failed |
| 1 | Not found | Requested resource not found |
| 1 | Auth error | Authentication failed |

### Handling Results in CLI

```python
result = perform_action(name, target=target)

if result == FeatureResult.SUCCESS:
    console.print()
    print_bold("Action completed!")
    console.print()
    print_info("Additional context here.")
elif result == FeatureResult.ALREADY_EXISTS:
    raise SystemExit(0)  # Not an error, just informational
elif result == FeatureResult.NOT_FOUND:
    console.print()
    print_error(f"'{name}' not found.")
    print_info("Use 'context-harness feature list' to see available options.")
    raise SystemExit(1)
elif result in (FeatureResult.AUTH_ERROR, FeatureResult.ERROR):
    console.print()
    print_error("Action failed.")
    raise SystemExit(1)
```

---

## Testing CLI Commands

### Test Setup

```python
# tests/test_cli.py
import pytest
from click.testing import CliRunner
from context_harness.cli import main


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


class TestFeatureCommand:
    """Tests for the feature command group."""

    def test_feature_help(self, runner):
        """Test that feature --help works."""
        result = runner.invoke(main, ["feature", "--help"])
        assert result.exit_code == 0
        assert "Manage feature" in result.output

    def test_feature_action_help(self, runner):
        """Test that feature action --help works."""
        result = runner.invoke(main, ["feature", "action", "--help"])
        assert result.exit_code == 0
        assert "--target" in result.output
        assert "--force" in result.output
```

### Testing with Temporary Directories

```python
def test_action_creates_files(self, runner, tmp_path):
    """Test that action creates the expected files."""
    result = runner.invoke(main, ["feature", "action", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / "expected_file.txt").is_file()
```

### Testing Error Cases

```python
def test_action_fails_if_exists(self, runner, tmp_path):
    """Test that action fails if target already exists."""
    (tmp_path / "expected_file.txt").touch()

    result = runner.invoke(main, ["feature", "action", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "already exist" in result.output

def test_action_force_overwrites(self, runner, tmp_path):
    """Test that action --force overwrites existing files."""
    (tmp_path / "expected_file.txt").write_text("old content")

    result = runner.invoke(main, ["feature", "action", "--force", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "successfully" in result.output
```

---

## Entry Point Configuration

### pyproject.toml

```toml
[project.scripts]
context-harness = "context_harness.cli:main"

[project.dependencies]
click = ">=8.0"
rich = ">=13.0"
questionary = ">=2.1.1"
```

---

## Templates

### New Command File Template

```python
"""[Feature] commands for ContextHarness CLI.

Handles the `context-harness [feature]` command group.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click

from context_harness.interfaces.cli.formatters import (
    console,
    print_header,
    print_success,
    print_warning,
    print_error,
    print_info,
    print_bold,
)


@click.group("[feature]")
def [feature]_group() -> None:
    """Manage [feature].

    Description of what this command group does.
    """
    pass


@[feature]_group.command("[action]")
@click.argument("name", required=False, default=None)
@click.option(
    "--target",
    "-t",
    default=".",
    type=click.Path(),
    help="Target directory (default: current directory).",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force operation.",
)
def [feature]_[action](name: Optional[str], target: str, force: bool) -> None:
    """[Action description].

    Examples:

        context-harness [feature] [action]

        context-harness [feature] [action] my-name

        context-harness [feature] [action] --force
    """
    print_header("[Feature] [Action]")
    # Implementation...
```

---

## References

- [Click Documentation](https://click.palletsprojects.com/)
- [Click Testing](https://click.palletsprojects.com/en/8.1.x/testing/)
- [Click Shell Completion](https://click.palletsprojects.com/en/8.1.x/shell-completion/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Questionary](https://questionary.readthedocs.io/)

---

_Skill: python-cli-click v1.0.0 | Last updated: 2025-12-30_
