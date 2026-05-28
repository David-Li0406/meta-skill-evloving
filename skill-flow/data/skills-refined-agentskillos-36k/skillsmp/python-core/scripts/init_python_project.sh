#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:-}"
PROJECT_TYPE="${2:-package}"  # package or fastapi

if [[ -z "$PROJECT_NAME" ]]; then
    echo "Usage: $0 <project-name> [package|fastapi]"
    exit 1
fi

echo "Creating Python project: $PROJECT_NAME (type: $PROJECT_TYPE)"

if [[ "$PROJECT_TYPE" == "fastapi" ]]; then
    mkdir -p "$PROJECT_NAME/app"
    cd "$PROJECT_NAME"
    
    # Create FastAPI structure
    cat > app/main.py << 'PY'
from fastapi import FastAPI

app = FastAPI(title="My API")

@app.get("/")
async def root():
    return {"message": "Hello World"}
PY
    
    cat > app/__init__.py << 'PY'
PY

else
    mkdir -p "$PROJECT_NAME/src/$PROJECT_NAME"
    mkdir -p "$PROJECT_NAME/tests"
    cd "$PROJECT_NAME"
    
    cat > "src/$PROJECT_NAME/__init__.py" << 'PY'
"""$PROJECT_NAME package."""
__version__ = "0.1.0"
PY

    cat > "src/$PROJECT_NAME/main.py" << 'PY'
def main() -> None:
    """Main function."""
    print("Hello from $PROJECT_NAME!")

if __name__ == "__main__":
    main()
PY
fi

# Create pyproject.toml
cat > pyproject.toml << 'TOML'
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = ""
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
TOML

# Create .gitignore
cat > .gitignore << 'IGNORE'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.env
.venv
*.egg-info/
dist/
build/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
IGNORE

echo "✅ Project created: $PROJECT_NAME"
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  python -m venv venv"
echo "  source venv/bin/activate"
echo "  pip install -e '.[dev]'"
