# Ruff Configuration

Standard Ruff configuration for Tenzir Python projects.

```toml
[tool.ruff]
target-version = "py312"
line-length = 88
src = ["src"]

[tool.ruff.lint]
select = ["E", "F"]
ignore = ["E501"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"
```

## Key Points

- **Line length**: 88 characters (Ruff/Black default)
- **Lint rules**: Only `E` (pycodestyle) and `F` (pyflakes)
- **E501 ignored**: Let the formatter handle line wrapping
- **F401 in `__init__.py`**: Allow unused imports for re-exports
- **Formatting**: Double quotes, spaces (not tabs), LF line endings
