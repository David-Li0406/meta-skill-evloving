#!/usr/bin/env python3
"""
Tests for command extraction logic (shared utilities in _github.py).

Run with: pytest tests/test_runbook.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from _github import (
    extract_commands_from_readme,
    extract_from_package_json,
    extract_from_makefile,
    detect_languages,
    dedupe,
)


class TestExtractCommandsFromReadme:
    """Tests for README command extraction."""

    def test_extracts_bash_fenced_code_blocks(self):
        readme = """
# My Project

## Installation

```bash
npm install
```

## Running

```bash
npm run dev
```

## Testing

```bash
npm test
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert "npm run dev" in run_cmds
        assert "npm test" in test_cmds

    def test_extracts_shell_fenced_code_blocks(self):
        readme = """
```shell
python main.py
pytest tests/
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert "python main.py" in run_cmds
        assert "pytest tests/" in test_cmds

    def test_strips_dollar_sign_prefix(self):
        readme = """
```bash
$ npm install
$ npm run dev
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        # Dollar sign should be stripped - "$ npm install" becomes "npm install"
        assert "npm install" in run_cmds  # "npm " matches
        assert "npm run dev" in run_cmds

    def test_ignores_comment_lines(self):
        readme = """
```bash
# This is a comment
npm run dev
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert len([c for c in run_cmds if "comment" in c.lower()]) == 0
        assert "npm run dev" in run_cmds

    def test_extracts_pytest(self):
        readme = """
```bash
pytest -v tests/
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert "pytest -v tests/" in test_cmds

    def test_extracts_cargo_commands(self):
        readme = """
```bash
cargo run
cargo test
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert "cargo run" in run_cmds
        assert "cargo test" in test_cmds

    def test_extracts_go_commands(self):
        readme = """
```bash
go run .
go test ./...
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert "go run ." in run_cmds
        assert "go test ./..." in test_cmds

    def test_extracts_uvicorn(self):
        readme = """
```bash
uvicorn app:main --reload
```
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert "uvicorn app:main --reload" in run_cmds

    def test_handles_empty_readme(self):
        run_cmds, test_cmds = extract_commands_from_readme("")
        assert run_cmds == []
        assert test_cmds == []

    def test_handles_readme_without_code_blocks(self):
        readme = """
# My Project

This is a simple README without any code blocks.
"""
        run_cmds, test_cmds = extract_commands_from_readme(readme)
        assert run_cmds == []
        assert test_cmds == []


class TestExtractFromPackageJson:
    """Tests for package.json script extraction."""

    def test_extracts_npm_test(self):
        package_json = """
{
    "name": "my-app",
    "scripts": {
        "test": "jest"
    }
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert "npm run test" in test_cmds

    def test_extracts_multiple_test_scripts(self):
        package_json = """
{
    "scripts": {
        "test": "jest",
        "test:unit": "jest --testPathPattern=unit",
        "test:e2e": "jest --testPathPattern=e2e"
    }
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert "npm run test" in test_cmds
        assert "npm run test:unit" in test_cmds
        assert "npm run test:e2e" in test_cmds

    def test_extracts_run_scripts(self):
        package_json = """
{
    "scripts": {
        "start": "node server.js",
        "dev": "nodemon server.js",
        "build": "tsc"
    }
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert "npm run start" in run_cmds
        assert "npm run dev" in run_cmds
        assert "npm run build" in run_cmds

    def test_detects_jest_in_script_value(self):
        package_json = """
{
    "scripts": {
        "check": "jest --coverage"
    }
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert "npm run check" in test_cmds

    def test_detects_vitest_in_script_value(self):
        package_json = """
{
    "scripts": {
        "verify": "vitest run"
    }
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert "npm run verify" in test_cmds

    def test_detects_node_in_script_value(self):
        package_json = """
{
    "scripts": {
        "custom": "node build.js"
    }
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert "npm run custom" in run_cmds

    def test_handles_invalid_json(self):
        run_cmds, test_cmds = extract_from_package_json("not valid json")
        assert run_cmds == []
        assert test_cmds == []

    def test_handles_missing_scripts(self):
        package_json = """
{
    "name": "my-app",
    "version": "1.0.0"
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert run_cmds == []
        assert test_cmds == []

    def test_handles_empty_scripts(self):
        package_json = """
{
    "scripts": {}
}
"""
        run_cmds, test_cmds = extract_from_package_json(package_json)
        assert run_cmds == []
        assert test_cmds == []


class TestExtractFromMakefile:
    """Tests for Makefile target extraction."""

    def test_extracts_run_target(self):
        makefile = """
.PHONY: run test

run:
\tpython main.py

test:
\tpytest tests/
"""
        run_cmds, test_cmds = extract_from_makefile(makefile)
        assert "make run" in run_cmds
        assert "make test" in test_cmds

    def test_extracts_multiple_run_targets(self):
        makefile = """
start:
\tnode server.js

dev:
\tnode --watch server.js

build:
\ttsc
"""
        run_cmds, test_cmds = extract_from_makefile(makefile)
        assert "make start" in run_cmds
        assert "make dev" in run_cmds
        assert "make build" in run_cmds

    def test_extracts_check_and_lint_targets(self):
        makefile = """
check:
\tcargo check

lint:
\tcargo clippy

verify:
\tcargo test
"""
        run_cmds, test_cmds = extract_from_makefile(makefile)
        assert "make check" in test_cmds
        assert "make lint" in test_cmds
        assert "make verify" in test_cmds

    def test_extracts_ci_target(self):
        makefile = """
ci:
\tpytest && mypy && flake8
"""
        run_cmds, test_cmds = extract_from_makefile(makefile)
        assert "make ci" in test_cmds

    def test_extracts_all_and_default_targets(self):
        makefile = """
all: build test

default: run
"""
        run_cmds, test_cmds = extract_from_makefile(makefile)
        assert "make all" in run_cmds
        assert "make default" in run_cmds

    def test_handles_targets_with_dependencies(self):
        makefile = """
test: deps
\tpytest

deps:
\tpip install -r requirements.txt
"""
        run_cmds, test_cmds = extract_from_makefile(makefile)
        assert "make test" in test_cmds

    def test_handles_empty_makefile(self):
        run_cmds, test_cmds = extract_from_makefile("")
        assert run_cmds == []
        assert test_cmds == []


class TestDetectLanguages:
    """Tests for language detection."""

    def test_detects_python_from_manifest(self):
        manifests = {"pyproject.toml"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "python" in langs

    def test_detects_python_from_requirements(self):
        manifests = {"requirements.txt"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "python" in langs

    def test_detects_javascript_from_package_json(self):
        manifests = {"package.json"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "javascript" in langs

    def test_detects_typescript_from_tsconfig(self):
        manifests = {"tsconfig.json"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "typescript" in langs

    def test_detects_rust_from_cargo(self):
        manifests = {"Cargo.toml"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "rust" in langs

    def test_detects_go_from_go_mod(self):
        manifests = {"go.mod"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "go" in langs

    def test_detects_java_from_pom(self):
        manifests = {"pom.xml"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "java" in langs

    def test_detects_java_from_gradle(self):
        manifests = {"build.gradle"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "java" in langs

    def test_detects_language_from_entrypoint_extension(self):
        manifests = set()
        entrypoints = {"main.py"}
        langs = detect_languages(manifests, entrypoints)
        assert "python" in langs

    def test_detects_multiple_languages(self):
        manifests = {"package.json", "pyproject.toml"}
        entrypoints = {"main.py", "src/index.ts"}
        langs = detect_languages(manifests, entrypoints)
        assert "python" in langs
        assert "javascript" in langs
        assert "typescript" in langs

    def test_handles_nested_manifest_paths(self):
        manifests = {"backend/pyproject.toml", "frontend/package.json"}
        entrypoints = set()
        langs = detect_languages(manifests, entrypoints)
        assert "python" in langs
        assert "javascript" in langs

    def test_handles_empty_inputs(self):
        langs = detect_languages(set(), set())
        assert len(langs) == 0


class TestDedupe:
    """Tests for deduplication utility."""

    def test_removes_duplicates(self):
        items = ["npm test", "npm run dev", "npm test"]
        result = dedupe(items)
        assert result == ["npm test", "npm run dev"]

    def test_preserves_order(self):
        items = ["c", "a", "b", "a"]
        result = dedupe(items)
        assert result == ["c", "a", "b"]

    def test_strips_whitespace(self):
        items = ["  npm test  ", "npm test"]
        result = dedupe(items)
        assert result == ["npm test"]

    def test_removes_empty_strings(self):
        items = ["npm test", "", "  ", "npm run dev"]
        result = dedupe(items)
        assert result == ["npm test", "npm run dev"]

    def test_handles_empty_list(self):
        result = dedupe([])
        assert result == []


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
