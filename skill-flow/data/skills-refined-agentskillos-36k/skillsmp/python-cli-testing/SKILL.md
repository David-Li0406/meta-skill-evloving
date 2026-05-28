---
name: python-cli-testing
description: Write tests for Typer/Click-based Python CLIs using CliRunner. Covers conftest.py fixtures, exit code testing, stdout/stderr capture, isolated filesystem, and interactive prompts. Use when adding tests to Typer CLI projects.
---

# Python CLI Testing Guide

Write tests for Typer/Click-based Python CLIs using the built-in CliRunner.

## Testing Terminology

| Type | What it tests | How to run | Skill |
|------|---------------|------------|-------|
| **Unit test** | Individual functions/classes in isolation | `pytest` | `python-unit-testing` |
| **CLI test** | Command-line interface via CliRunner | `pytest` | This skill |
| **Smoketest** | Full system with real services (AKA e2e, integration) | `RUN_INTEGRATION_TESTS=true pytest` | `smoketest-writing` |

## Core Principles

1. **CliRunner for isolation** - Captures stdout/stderr, tests exit codes, no subprocess needed
2. **No production code changes** - Tests invoke CLI as-is
3. **Fast** - CliRunner tests are unit-test speed

## Directory Structure

```
project/
├── myapp/
│   └── cli.py              # Typer CLI
└── tests/
    ├── conftest.py         # CLI fixtures
    └── test_cli.py         # CLI tests
```

## conftest.py

```python
# tests/conftest.py

import pytest
from pathlib import Path
from typer.testing import CliRunner

from myapp.cli import app


@pytest.fixture
def runner():
    """Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def cli(runner):
    """Convenience fixture that returns invoke function."""
    def invoke(*args):
        return runner.invoke(app, list(args))
    return invoke


@pytest.fixture
def sample_fasta(tmp_path):
    """Create a sample FASTA file."""
    fasta = tmp_path / "sample.fa"
    fasta.write_text(">chr1\nACGTACGT\n>chr2\nGGCCGGCC\n")
    return fasta
```

## Writing CLI Tests

### Basic Structure

```python
# tests/test_cli.py

class TestFastaDigest:
    """Tests for: myapp fasta digest <file>"""

    def test_digest_success(self, cli, sample_fasta):
        """Compute digest of valid FASTA."""
        result = cli("fasta", "digest", str(sample_fasta))

        assert result.exit_code == 0
        assert "digest" in result.stdout

    def test_digest_file_not_found(self, cli):
        """Error on missing file."""
        result = cli("fasta", "digest", "/nonexistent.fa")

        assert result.exit_code != 0

    def test_digest_missing_argument(self, cli):
        """Error when file argument missing."""
        result = cli("fasta", "digest")

        assert result.exit_code != 0
        assert "Missing argument" in result.stdout
```

### CliRunner Result Object

```python
result = runner.invoke(app, ["command", "arg", "--option", "value"])

result.exit_code      # Integer exit code
result.stdout         # Captured standard output
result.stderr         # Captured stderr (if mix_stderr=False)
result.output         # Combined stdout (default)
result.exception      # Any unhandled exception
```

### Separate stdout and stderr

```python
def test_output_streams(runner, sample_fasta):
    # Default: stderr mixed into stdout
    result = runner.invoke(app, ["fasta", "digest", str(sample_fasta)])
    assert "digest" in result.output

    # Separate them:
    result = runner.invoke(
        app,
        ["fasta", "digest", str(sample_fasta)],
        mix_stderr=False
    )
    assert "digest" in result.stdout
    assert result.stderr == ""
```

## Testing Exit Codes

```python
def test_exit_codes(cli):
    # Success
    result = cli("fasta", "digest", "valid.fa")
    assert result.exit_code == 0

    # File not found (exit code 2)
    result = cli("fasta", "digest", "/missing.fa")
    assert result.exit_code == 2
```

In CLI implementation, use `raise typer.Exit(code)`:

```python
@app.command()
def digest(file: Path):
    if not file.exists():
        typer.echo(f"Error: File not found: {file}", err=True)
        raise typer.Exit(2)
```

## Testing with Environment Variables

```python
def test_with_env_var(runner, monkeypatch):
    """Test CLI respects environment variables."""
    monkeypatch.setenv("MYAPP_STORE_PATH", "/custom/store")

    result = runner.invoke(app, ["config", "show"])

    assert result.exit_code == 0
    assert "/custom/store" in result.stdout
```

## Testing with Isolated Filesystem

```python
def test_file_creation(runner):
    """Test command that creates files."""
    with runner.isolated_filesystem():
        Path("input.fa").write_text(">chr1\nACGT\n")

        result = runner.invoke(app, ["fasta", "index", "input.fa"])

        assert result.exit_code == 0
        assert Path("input.fa.fai").exists()
```

Or use fixture approach:

```python
@pytest.fixture
def isolated_fs(monkeypatch, tmp_path):
    """Isolate test in temporary directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_relative_paths(cli, isolated_fs):
    (isolated_fs / "genome.fa").write_text(">chr1\nACGT\n")

    result = cli("fasta", "digest", "genome.fa")
    assert result.exit_code == 0
```

## Testing Interactive Prompts

```python
def test_interactive_config(runner):
    """Test interactive configuration wizard."""
    result = runner.invoke(
        app,
        ["config", "init"],
        input="~/.myapp/store\nhttps://api.example.com\n"
    )

    assert result.exit_code == 0
    assert "Configuration saved" in result.stdout


def test_confirm_delete(runner):
    # User confirms
    result = runner.invoke(app, ["store", "delete"], input="y\n")
    assert result.exit_code == 0

    # User declines
    result = runner.invoke(app, ["store", "delete"], input="n\n")
    assert result.exit_code == 1
    assert "Aborted" in result.stdout
```

## Testing Help Output

```python
class TestHelpOutput:
    """Verify help text is correct."""

    def test_main_help(self, cli):
        result = cli("--help")

        assert result.exit_code == 0
        assert "Usage:" in result.stdout

    def test_subcommand_help(self, cli):
        result = cli("fasta", "--help")

        assert result.exit_code == 0
        assert "digest" in result.stdout

    def test_command_help(self, cli):
        result = cli("fasta", "digest", "--help")

        assert result.exit_code == 0
        assert "FILE" in result.stdout


def test_version(cli):
    result = cli("--version")

    assert result.exit_code == 0
    # Use regex or partial match for version
```

## Checklist

- [ ] `conftest.py` with `runner` and `cli` fixtures
- [ ] Test data fixtures for sample files
- [ ] Tests grouped by command in classes
- [ ] Exit codes tested for success and error cases
- [ ] Help output verified
- [ ] Version command tested
- [ ] Interactive prompts tested with `input=` parameter

## References

- [Typer Testing Documentation](https://typer.tiangolo.com/tutorial/testing/)
- [Click Testing Documentation](https://click.palletsprojects.com/en/stable/testing/)
