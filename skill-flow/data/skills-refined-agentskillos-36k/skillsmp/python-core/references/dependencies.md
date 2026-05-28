# Python Dependency Management

## Modern Tools

### uv (Recommended)
```bash
uv pip install fastapi
uv pip install -r requirements.txt
uv venv  # Create virtual environment
```

### Poetry
```bash
poetry add fastapi
poetry install
poetry run python main.py
```

### pip
```bash
pip install fastapi
pip install -r requirements.txt
pip freeze > requirements.txt
```

## pyproject.toml

```toml
[project]
name = "myproject"
version = "0.1.0"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]

[tool.mypy]
python_version = "3.11"
strict = true
```

## Best Practices

1. Pin major versions: `fastapi>=0.104.0,<1.0.0`
2. Use lock files (poetry.lock, uv.lock)
3. Separate dev dependencies
4. Regular security audits: `pip-audit`
5. Use virtual environments
