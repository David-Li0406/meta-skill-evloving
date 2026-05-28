# Coverage Configuration

Standard coverage configuration for Tenzir Python projects.

```toml
[tool.coverage.run]
source = ["src/<package_name>"]
branch = true
omit = ["*/tests/*", "*/__main__.py"]

[tool.coverage.report]
fail_under = 80
show_missing = true
skip_covered = true
```

## Key Points

- **Threshold**: 80% minimum coverage required
- **Branch coverage**: Enabled for conditional logic
- **Omissions**: Tests and `__main__.py` excluded from metrics
- **Reporting**: Shows missing lines, hides fully covered files
