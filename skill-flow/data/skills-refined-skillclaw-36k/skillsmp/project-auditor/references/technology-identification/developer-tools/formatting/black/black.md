# Black

**Category**: developer-tools/formatting
**Description**: Black - the uncompromising Python code formatter
**Homepage**: https://black.readthedocs.io

## Package Detection

### PyPI
- `black`
- `black[jupyter]`

## Configuration Files

- `pyproject.toml`
- `.black`
- `black.toml`

## Import Detection

### Python
- **Pattern**: `^import black`
- **Pattern**: `^from black import`

## Environment Variables

- `BLACK_CACHE_DIR`

## Detection Notes

- Python code formatter
- Configuration typically in pyproject.toml under [tool.black]
- Often used with pre-commit hooks
- Look for black in dev dependencies

## Detection Confidence

- **Configuration File Detection**: 85% (HIGH)
- **Package Detection**: 95% (HIGH)
