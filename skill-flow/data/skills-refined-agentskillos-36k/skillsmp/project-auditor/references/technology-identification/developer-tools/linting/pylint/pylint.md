# Pylint

**Category**: developer-tools/linting
**Description**: Pylint - Python static code analyzer for errors, coding standards, and code smells
**Homepage**: https://pylint.pycqa.org

## Package Detection

### PYPI
- `pylint`
- `pylint-django`
- `pylint-flask`
- `pylint-celery`

## Configuration Files

- `.pylintrc`
- `pylintrc`
- `pyproject.toml` (with [tool.pylint])
- `setup.cfg` (with [pylint])

## Detection Notes

- Look for .pylintrc in repository root
- Check for pylint in requirements
- May be configured in pyproject.toml
- Often used alongside black, mypy, flake8

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
