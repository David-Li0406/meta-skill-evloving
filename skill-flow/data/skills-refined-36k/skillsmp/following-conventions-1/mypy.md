# Mypy Configuration

Standard Mypy configuration for Tenzir Python projects.

```toml
[tool.mypy]
files = ["src"]
plugins = ["pydantic.mypy"]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

## Key Points

- **Scope**: Only checks `src/`, not tests
- **Strict mode**: All `disallow_*` and `warn_*` flags enabled
- **No implicit optional**: `None` must be explicit in type hints
- **No untyped definitions**: All functions must have type annotations
