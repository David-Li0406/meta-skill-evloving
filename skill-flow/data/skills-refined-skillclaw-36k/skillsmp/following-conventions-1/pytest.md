# Pytest Configuration

Standard Pytest configuration for Tenzir Python projects.

```toml
[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra --strict-markers"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
pythonpath = ["src"]
```

## Key Points

- **Strict markers**: Unknown markers cause errors (no typos)
- **Test discovery**: `test_*.py` and `*_test.py` patterns
- **Python path**: `src/` added so imports work without installation
- **Output**: `-ra` shows summary of all non-passing tests
