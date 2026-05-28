# Project Structure

Standard layout for Tenzir Python projects.

```
project/
├── src/tenzir_<name>/   # Main package code
│   ├── __init__.py
│   ├── py.typed         # PEP 561 marker for type hints
│   ├── cli.py           # CLI entrypoint (Click)
│   ├── config.py        # Configuration helpers
│   └── ...
├── tests/               # Test suite
│   ├── conftest.py      # Shared fixtures
│   └── test_*.py        # Test modules (mirror src structure)
├── pyproject.toml       # Project metadata
├── uv.lock              # Locked dependencies
├── README.md            # User onboarding
└── DEVELOPMENT.md       # Contributor workflows (optional)
```

## Key Points

- **src layout**: Package lives in `src/tenzir_<name>/`
- **Naming**: Use `tenzir_` prefix for package directories
- **Tests**: Mirror module names (e.g., `cli.py` → `test_cli.py`)
- **Typed package**: Include `py.typed` marker for type hint exports

## Testing Conventions

- Place tests in `tests/` following the `test_*.py` pattern
