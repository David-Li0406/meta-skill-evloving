# Python Style Guide

## Project Structure

### Package Layout
```
project/
├── pyproject.toml
├── project_name/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   └── utils.py
│   ├── scripts/
│   │   └── cli.py
│   └── tests/
│       ├── conftest.py
│       ├── unit/
│       │   └── test_core.py
│       ├── integration/
│       │   └── test_workflow.py
│       └── e2e/
│           └── test_full.py
└── .pre-commit-config.yaml
```

---

## pyproject.toml Configuration

### Poetry Setup
```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = "Project description"
authors = ["Your Name <email@example.com>"]
packages = [{include = "project_name", from = "project_name/src"}]

[tool.poetry.dependencies]
python = ">=3.11,<3.15"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^4.0"
ruff = "^0.8"
pyright = "^1.1"
pre-commit = "^3.0"
```

### Ruff Configuration
```toml
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = [
    "E", "W",      # pycodestyle
    "F",           # pyflakes
    "I",           # isort
    "UP",          # pyupgrade
    "B",           # flake8-bugbear
    "C4",          # flake8-comprehensions
    "SIM",         # flake8-simplify
    "ARG",         # flake8-unused-arguments
    "PLR", "PLW",  # pylint
]
ignore = [
    "E501",        # line too long (handled by formatter)
    "PLR0913",     # too many arguments
    "PLR2004",     # magic value comparison
]

[tool.ruff.lint.isort]
known-first-party = ["project_name"]
```

### Pyright Configuration
```toml
[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
reportMissingImports = true
reportUnusedImport = true
reportUnusedClass = true
reportUnusedFunction = true
reportUnusedVariable = true
```

### Pytest Configuration
```toml
[tool.pytest.ini_options]
testpaths = ["project_name/tests"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=project_name",
    "--cov-report=html",
    "--cov-fail-under=80",
]
markers = [
    "unit: unit tests",
    "integration: integration tests",
    "e2e: end-to-end tests",
    "slow: slow running tests",
]

[tool.coverage.run]
branch = true
source = ["project_name"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `video_processor.py` |
| Classes | PascalCase | `VideoProcessor` |
| Functions | snake_case | `process_frame()` |
| Constants | SCREAMING_SNAKE | `MAX_FRAME_SIZE` |
| Private | _prefix | `_internal_state` |
| Type aliases | PascalCase | `FrameData = dict[str, Any]` |

---

## Type Hints

### Use Modern Union Syntax
```python
# Good: Python 3.10+ union syntax
def process(data: str | None = None) -> dict[str, Any] | None:
    pass

# Bad: Old Optional syntax
from typing import Optional, Dict, Any
def process(data: Optional[str] = None) -> Optional[Dict[str, Any]]:
    pass
```

### Common Type Patterns
```python
from typing import Any, TypeVar, Protocol, Self
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path

T = TypeVar("T")

# Use Path for file paths
def load_file(path: Path) -> bytes:
    return path.read_bytes()

# Use Callable for function parameters
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

# Use Protocol for duck typing
class Readable(Protocol):
    def read(self, n: int = -1) -> bytes: ...

def process_stream(stream: Readable) -> None:
    data = stream.read()
```

### Type Aliases
```python
# Define at module level
type JsonDict = dict[str, Any]
type FrameCallback = Callable[[np.ndarray], None]
type Result[T] = T | None
```

---

## Error Handling

### Return None for Recoverable Errors
```python
def parse_config(path: str) -> Config | None:
    """Parse config file, returns None if invalid."""
    try:
        with open(path) as f:
            data = json.load(f)
        return Config(**data)
    except (OSError, json.JSONDecodeError, TypeError):
        return None
```

### Raise for Unrecoverable Errors
```python
def require_config(path: str) -> Config:
    """Load config, raises if missing or invalid."""
    config = parse_config(path)
    if config is None:
        raise ValueError(f"Invalid or missing config: {path}")
    return config
```

### Custom Exception Classes
```python
class ProjectError(Exception):
    """Base exception for this project."""
    pass

class ParseError(ProjectError):
    """Raised when parsing fails."""
    def __init__(self, message: str, position: int | None = None):
        self.position = position
        super().__init__(f"{message} at position {position}" if position else message)

class ValidationError(ProjectError):
    """Raised when validation fails."""
    pass
```

---

## Documentation

### Google-Style Docstrings
```python
def process_video(
    input_path: str,
    output_path: str | None = None,
    frame_rate: int = 30,
) -> ProcessResult:
    """Process a video file and extract frames.

    Args:
        input_path: Path to the input video file.
        output_path: Path for output. If None, uses input directory.
        frame_rate: Target frame rate for extraction.

    Returns:
        ProcessResult containing extracted frame data and metadata.

    Raises:
        FileNotFoundError: If input_path does not exist.
        ValueError: If frame_rate is not positive.

    Example:
        >>> result = process_video("input.mp4", frame_rate=60)
        >>> print(result.frame_count)
        1800
    """
    pass
```

### Module Docstrings
```python
"""Video processing utilities.

This module provides functions for extracting and processing
video frames using FFmpeg.

Example:
    >>> from project_name import process_video
    >>> result = process_video("input.mp4")
"""
```

### Class Docstrings
```python
class VideoProcessor:
    """Processes video files for frame extraction.

    Attributes:
        frame_rate: Target frame rate for extraction.
        output_dir: Directory for output files.
    """

    def __init__(self, frame_rate: int = 30) -> None:
        """Initialize the processor.

        Args:
            frame_rate: Target frame rate. Defaults to 30.
        """
        self.frame_rate = frame_rate
```

---

## Testing

### Test Organization
```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_video(tmp_path: Path) -> Path:
    """Create a sample video file for testing."""
    video_path = tmp_path / "sample.mp4"
    # Create minimal valid video
    create_test_video(video_path)
    return video_path

@pytest.fixture
def processor() -> VideoProcessor:
    """Create a VideoProcessor instance."""
    return VideoProcessor(frame_rate=30)
```

### Unit Tests
```python
# tests/unit/test_processor.py
import pytest
from project_name import VideoProcessor

class TestVideoProcessor:
    """Tests for VideoProcessor class."""

    def test_init_default_frame_rate(self):
        """Default frame rate should be 30."""
        processor = VideoProcessor()
        assert processor.frame_rate == 30

    def test_init_custom_frame_rate(self):
        """Custom frame rate should be set."""
        processor = VideoProcessor(frame_rate=60)
        assert processor.frame_rate == 60

    @pytest.mark.parametrize("frame_rate", [0, -1, -100])
    def test_init_invalid_frame_rate(self, frame_rate: int):
        """Negative frame rates should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            VideoProcessor(frame_rate=frame_rate)
```

### Integration Tests
```python
# tests/integration/test_processing.py
import pytest
from pathlib import Path

@pytest.mark.integration
def test_process_real_video(sample_video: Path, tmp_path: Path):
    """Test processing a real video file."""
    result = process_video(
        str(sample_video),
        output_path=str(tmp_path / "output"),
    )
    assert result.success
    assert result.frame_count > 0
```

### Test Markers
```python
# Run specific test types
# pytest -m unit
# pytest -m integration
# pytest -m "not slow"

@pytest.mark.slow
def test_large_video_processing():
    """Process a large video file."""
    pass

@pytest.mark.e2e
def test_full_workflow():
    """Test complete processing workflow."""
    pass
```

---

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.390
    hooks:
      - id: pyright

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v4.0.0
    hooks:
      - id: commitizen
```

---

## Logging

### Setup Pattern
```python
import logging

def setup_logging(
    level: str = "INFO",
    log_file: str | None = None,
) -> logging.Logger:
    """Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        log_file: Optional file path for log output.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("project_name")
    logger.setLevel(getattr(logging, level.upper()))

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
```

### Usage
```python
logger = logging.getLogger("project_name")

def process_file(path: str) -> None:
    logger.info("Processing file: %s", path)
    try:
        # Process
        logger.debug("File size: %d bytes", os.path.getsize(path))
    except Exception:
        logger.exception("Failed to process file")
        raise
```

---

## Common Dependencies

| Purpose | Package |
|---------|---------|
| CLI | `click`, `typer` |
| Testing | `pytest`, `pytest-cov` |
| Linting | `ruff` |
| Type checking | `pyright`, `mypy` |
| Data validation | `pydantic` |
| HTTP | `httpx`, `requests` |
| Async | `asyncio`, `aiofiles` |
| Data science | `numpy`, `pandas`, `torch` |
| Image/Video | `opencv-python`, `pillow` |
