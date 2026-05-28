# Development Dependencies

Standard dev dependencies for Tenzir Python projects.

> **Note**: The versions below are examples. Always use the latest available
> versions from PyPI rather than copying these verbatim.

```toml
[dependency-groups]
dev = [
  "pytest>=9.0",
  "pytest-cov>=7.0",
  "mypy>=1.19",
  "ruff>=0.14",
  "coverage[toml]>=7.12",
]
```

## Key Points

- **Ruff**: Linting and formatting
- **Mypy**: Static type checking
- **Pytest + pytest-cov**: Testing with coverage
- **Coverage**: Coverage reporting with TOML config support

Add type stubs as needed (e.g., `types-pyyaml` for PyYAML).
