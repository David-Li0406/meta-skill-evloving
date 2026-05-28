# Python Best Practices
- Follow PEP 8 naming and formatting; prefer snake_case for functions/vars, PascalCase for classes.
- Use pyproject.toml with black + isort + ruff; keep settings aligned (line length, quote style).
- Type hints: enable mypy or pyright; annotate public functions and dataclasses.
- Virtualenv management: prefer uv/venv; pin dependencies in requirements.txt or poetry.lock.
- Logging: use logging module; avoid bare prints in libraries.
- Error handling: raise typed exceptions; avoid broad except; add context messages.
- Testing: use pytest; place tests in tests/ with test_*.py naming; use fixtures for setup.
