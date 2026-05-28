# Python CLI Checklist

Complete validation checklist for Python CLI tools.

---

## Project Structure

- [ ] `pyproject.toml` with modern build system (hatchling/setuptools)
- [ ] `src/<package>/` directory layout
- [ ] `src/<package>/__init__.py` with public API exports
- [ ] `src/<package>/__main__.py` for `python -m` support
- [ ] `src/<package>/cli.py` for argument parsing
- [ ] `tests/` directory with `conftest.py`
- [ ] `README.md` with installation and usage
- [ ] `CLAUDE.md` with architecture and patterns
- [ ] `.gitignore` excluding `__pycache__`, `dist/`, `*.egg-info`

## The Triad

### Health (Doctor)
- [ ] `<tool> doctor` or `<tool>-doctor` command exists
- [ ] Checks external binaries with version validation
- [ ] Checks required environment variables
- [ ] Checks file/directory permissions
- [ ] Error messages include: what's missing + how to fix
- [ ] First run prompts for setup if not configured

### Safety (Safety Net)
- [ ] `--dry-run` flag for destructive operations
- [ ] Batch operations (>10 items) require `--dry-run` or `--yes`
- [ ] Deletions use soft delete (trash) first
- [ ] Undo log persists to disk (`~/.config/<tool>/undo.json`)
- [ ] `<tool> undo` command to reverse last operation

### Resilience (Statekeeper)
- [ ] Long operations checkpoint after each item
- [ ] State file uses atomic writes (temp + rename)
- [ ] Resume prompt on restart if incomplete state exists
- [ ] API calls retry with exponential backoff
- [ ] Ctrl+C saves state before exit (signal handler)

## Data Models

- [ ] `@dataclass` for all configuration objects
- [ ] `@dataclass` for all domain models
- [ ] Type hints on all function signatures
- [ ] No `dict` or `Any` in public function signatures
- [ ] `Enum` for fixed sets of values
- [ ] `to_dict()` / `from_dict()` for serialization
- [ ] Pydantic or validation for external input

## Code Organization

- [ ] `cli.py` only parses arguments (no business logic)
- [ ] `models.py` contains data structures only
- [ ] One module = one responsibility
- [ ] No circular imports
- [ ] Files under ~300 lines
- [ ] `utils.py` contains pure functions only

## Error Handling

- [ ] Custom exception hierarchy (base `ToolError`)
- [ ] Error messages include: what, why, fix
- [ ] Transient errors retry with backoff
- [ ] Non-retryable errors fail fast
- [ ] Graceful degradation returns partial results when possible

## Testing

- [ ] `pytest` configured in `pyproject.toml`
- [ ] `tests/conftest.py` with shared fixtures
- [ ] External APIs mocked (no real network calls)
- [ ] Core business logic has >80% coverage
- [ ] `@pytest.mark.slow` for integration tests
- [ ] Tests run in <10 seconds (unit tests)

## Build & Deploy

- [ ] `pyproject.toml` with `[project.scripts]` entry points
- [ ] Version in single location (`pyproject.toml`)
- [ ] `ruff` configured for linting
- [ ] `mypy` configured for type checking
- [ ] GitHub Actions for CI (test on PR)
- [ ] GitHub Actions for publish (on release)
- [ ] Makefile with: `install`, `dev`, `test`, `lint`, `format`

## CLI UX

- [ ] `--help` shows usage, options, examples
- [ ] `--version` shows version number
- [ ] `--json` outputs machine-readable JSON
- [ ] `--quiet` suppresses non-essential output
- [ ] `--verbose` shows detailed progress
- [ ] Progress bars for long operations (`rich` or `tqdm`)
- [ ] Colored output (with `--no-color` option)
- [ ] Interactive setup wizard for first run

## Documentation

- [ ] README has: installation, quick start, all commands
- [ ] CLAUDE.md has: architecture, key files, patterns
- [ ] All public functions have docstrings
- [ ] Examples in docstrings
- [ ] Troubleshooting section in README

## State Persistence

- [ ] Config in `~/.config/<tool>/config.json`
- [ ] State in `~/.config/<tool>/state.json`
- [ ] All writes are atomic
- [ ] Graceful handling of corrupt/missing files
- [ ] Schema version for future migrations

---

## Quick Validation

```bash
# Check project structure
ls pyproject.toml src/ tests/

# Check Triad patterns
grep -rE "(doctor|check|verify)" src/    # Health
grep -rE "(undo|restore|dry-run)" src/   # Safety
grep -rE "(checkpoint|resume|state)" src/ # Resilience

# Check type safety
grep -rE "@dataclass" src/
grep -rE "def.*\(.*: dict\)" src/  # Should be minimal

# Check tests
pytest --collect-only | head -20

# Run lint
ruff check src tests
mypy src
```
