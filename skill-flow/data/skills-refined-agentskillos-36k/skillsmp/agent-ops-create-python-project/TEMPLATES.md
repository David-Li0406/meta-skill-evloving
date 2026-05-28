# Python Project Templates

Reference templates for `agent-ops-create-python-project` skill.

---

## Project Structure

```
project-name/
├── pyproject.toml          # All config, dependencies, tool settings
├── README.md               # Overview, install, usage, dev setup
├── AGENTS.md               # AI agent guidelines
├── .gitignore              # Standard Python ignores
├── scripts/
│   └── build.py            # Build pipeline (lint, type-check, test)
├── src/
│   └── <package>/
│       ├── __init__.py
│       ├── cli.py          # Thin CLI layer (typer)
│       ├── config.py       # Configuration management
│       └── <modules>.py    # Core logic modules
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```

---

## pyproject.toml

```toml
[project]
name = "<package-name>"
version = "0.1.0"
description = "<extracted from discussion>"
readme = "README.md"
requires-python = ">=3.11"
authors = [{ name = "Author", email = "author@example.com" }]
dependencies = [
  "typer>=0.12.3",
  "rich>=13.9.0",
  "pyyaml>=6.0.0",
  "python-dotenv>=1.0.1",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0.0",
  "pytest-cov>=4.1.0",
  "pytest-mock>=3.12.0",
  "pytest-timeout>=2.4.0",
  "ruff>=0.6.0",
  "mypy>=1.11.0",
  "types-PyYAML>=6.0.0",
]

[project.scripts]
<cli-name> = "<package>.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/<package>"]

[tool.hatch.build.targets.sdist]
include = ["src/<package>"]

[tool.uv]
package = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
timeout = 30
addopts = ["-v", "--tb=short", "--strict-markers"]
markers = [
  "slow: marks tests as slow (deselect with '-m \"not slow\"')",
  "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src/<package>"]
branch = true
omit = ["*/tests/*", "*/__pycache__/*", "src/<package>/cli.py"]

[tool.coverage.report]
fail_under = 75
show_missing = true
exclude_lines = [
  "pragma: no cover",
  "def __repr__",
  "raise NotImplementedError",
  "if __name__ == .__main__.:",
  "if TYPE_CHECKING:",
]

[tool.coverage.html]
directory = "htmlcov"

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "C4", "UP", "PT"]
ignore = ["E501", "B008", "B904"]

[tool.mypy]
python_version = "3.11"
warn_unused_ignores = true
warn_redundant_casts = true
exclude = ["tests/"]
```

---

## scripts/build.py

Replace `<PROJECT_NAME>` and `<package>` with actual values.

```python
#!/usr/bin/env python3
"""Build script for <PROJECT_NAME>."""

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path


class BuildRunner:
    """Handles the build process for the project."""

    def __init__(self, verbose: bool = False, fix: bool = False, run_integration: bool = False):
        self.verbose = verbose
        self.fix = fix
        self.run_integration = run_integration
        self.project_root = Path(__file__).parent.parent
        self.src_path = self.project_root / "src" / "<package>"
        self.tests_path = self.project_root / "tests"
        self.failed_steps: list[str] = []

    def run_command(
        self, cmd: list[str], description: str, check: bool = True, capture_output: bool = True
    ) -> tuple[bool, str, str]:
        if self.verbose:
            print(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd, capture_output=capture_output, text=True, cwd=self.project_root,
                check=check, encoding="utf-8", errors="replace"
            )
            return True, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout or "", e.stderr or ""
        except FileNotFoundError:
            return False, "", f"Command not found: {cmd[0]}"

    def print_step(self, step: str) -> None:
        print(f"\n{'=' * 60}\n[TOOL] {step}\n{'=' * 60}")

    def print_result(self, success: bool, step: str, output: str = "", error: str = "") -> None:
        if success:
            print(f"[OK] {step} - PASSED")
        else:
            print(f"[FAIL] {step} - FAILED")
            self.failed_steps.append(step)
            if error: print(f"Error: {error}")
            if output: print(f"Output: {output}")

    def check_dependencies(self) -> bool:
        self.print_step("Checking Dependencies")
        tools = [
            ("uv", ["uv", "--version"]),
            ("ruff", ["uv", "run", "ruff", "--version"]),
            ("mypy", ["uv", "run", "mypy", "--version"]),
            ("pytest", ["uv", "run", "pytest", "--version"]),
        ]
        all_available = True
        for tool_name, cmd in tools:
            success, output, _ = self.run_command(cmd, f"Check {tool_name}")
            if success:
                print(f"[OK] {tool_name}: {output.strip().split()[0] if output else 'unknown'}")
            else:
                print(f"[FAIL] {tool_name}: Not available")
                all_available = False
        return all_available

    def sync_dependencies(self) -> bool:
        self.print_step("Syncing Dependencies")
        success, output, error = self.run_command(["uv", "sync", "--all-extras"], "Sync")
        self.print_result(success, "Dependency Sync", output, error)
        return success

    def format_code(self) -> bool:
        self.print_step("Code Formatting")
        if not self.src_path.exists():
            print(f"[WARN] Source not found: {self.src_path}")
            return False
        cmd = ["uv", "run", "ruff", "format"]
        cmd.extend([str(self.src_path)] if self.fix else ["--check", str(self.src_path)])
        success, output, error = self.run_command(cmd, "ruff format")
        self.print_result(success, "ruff format", output, error)
        return success

    def lint_code(self) -> bool:
        self.print_step("Code Linting")
        if not self.src_path.exists():
            return False
        cmd = ["uv", "run", "ruff", "check"]
        if self.fix: cmd.append("--fix")
        cmd.append(str(self.src_path))
        success, output, error = self.run_command(cmd, "ruff check")
        self.print_result(success, "ruff check", output, error)
        return success

    def type_check(self) -> bool:
        self.print_step("Type Checking")
        if not self.src_path.exists():
            return False
        success, output, error = self.run_command(
            ["uv", "run", "mypy", str(self.src_path)], "mypy"
        )
        self.print_result(success, "mypy", output, error)
        return success

    def run_unit_tests(self) -> bool:
        self.print_step("Unit Tests")
        for f in [".coverage", "htmlcov", "coverage.xml"]:
            p = self.project_root / f
            if p.exists():
                shutil.rmtree(p) if p.is_dir() else p.unlink()
        if not self.tests_path.exists() or not self.src_path.exists():
            return False
        cmd = [
            "uv", "run", "pytest", str(self.tests_path),
            f"--cov={self.src_path}", "--cov-report=term-missing",
            "--cov-report=html", "--cov-report=xml", "--cov-fail-under=75",
            "--durations=20", "-vv" if self.verbose else "-v"
        ]
        if not self.run_integration:
            cmd.extend(["-m", "not integration"])
        success, _, _ = self.run_command(cmd, "pytest", capture_output=False)
        self.print_result(success, "Unit Tests", "", "")
        return success

    def step_security(self) -> bool:
        self.print_step("Security Checks")
        if not self.src_path.exists():
            return False
        success, output, error = self.run_command(
            ["uv", "run", "ruff", "check", str(self.src_path), "--select", "S"], "security"
        )
        self.print_result(success, "Security Check", output, error)
        return success

    def run_full_build(self) -> bool:
        print(f"<PROJECT_NAME> - Build Pipeline\n{'=' * 60}")
        start = time.time()
        steps = [
            ("Check Dependencies", self.check_dependencies),
            ("Sync Dependencies", self.sync_dependencies),
            ("Format Code", self.format_code),
            ("Lint Code", self.lint_code),
            ("Type Check", self.type_check),
            ("Security Check", self.step_security),
            ("Unit Tests", self.run_unit_tests),
        ]
        ok = sum(1 for _, fn in steps if fn())
        print(f"\n{'=' * 60}\n[STAT] {ok}/{len(steps)} passed in {time.time()-start:.1f}s")
        if self.failed_steps:
            print(f"[FAIL] {', '.join(self.failed_steps)}")
        return ok == len(steps)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--integration", choices=["all", "none"], default="none")
    args = parser.parse_args()
    return 0 if BuildRunner(args.verbose, args.fix, args.integration == "all").run_full_build() else 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## README.md

```markdown
# <PROJECT_NAME>

<Short description>

## ⚠️ Important: Always Use `uv run`

**All Python commands MUST be run using `uv run`.**

```bash
# ✅ CORRECT
uv run python scripts/build.py
uv run pytest

# ❌ WRONG
python scripts/build.py
```

## Installation

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone <repo-url>
cd <project>
uv sync
```

## Development

```bash
uv run python scripts/build.py        # Full build
uv run python scripts/build.py --fix  # Auto-fix
uv run pytest tests/unit -v           # Unit tests
```
```

---

## AGENTS.md

```markdown
# AI Agent Guidelines for <PROJECT_NAME>

## 🔒 Quality Gates

1. Run: `uv run python scripts/build.py`
2. All checks must pass
3. Coverage ≥75%

## ⚠️ MANDATORY: Use `uv run`

```bash
# ✅ CORRECT
uv run python scripts/build.py
uv run pytest

# ❌ WRONG
python scripts/build.py
```

## 📏 Code Standards

- Type annotations on ALL functions
- Google-style docstrings on public APIs
- Use `pathlib.Path` for file operations
- Use `@dataclass` for data structures
- Max 15 lines per function
- Max 3 levels of nesting

## Forbidden

- `from src.<package> import X` — use `from <package> import X`
- Business logic in `cli.py`
- Bare `except:` blocks
- `print()` for logging
```

---

## .gitignore

```gitignore
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.coverage
coverage.xml
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
.env
.env.local
.DS_Store
```

---

## Code Quality Standards

### Design Principles
- **SRP**: One responsibility per module/function
- **DRY**: No duplicated logic
- **Dependency Injection**: Accept dependencies as parameters
- **Separation of Concerns**: Logic ≠ I/O ≠ UI

### Pythonic Patterns
- `pathlib.Path` for file operations
- `@dataclass` for structured data
- `typing` annotations on all functions
- Context managers for resources
- `logging` module, not `print()`

### Architecture
- **Thin CLI**: Parse/format only, delegate to core
- **No src imports**: `from <package>` not `from src.<package>`
- **Config via environment**: `.env` + `python-dotenv`
