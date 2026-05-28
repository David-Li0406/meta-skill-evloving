#!/usr/bin/env python3
"""
Integration tests for the RepoGPS orchestrator (repogps.py).

These tests mock the GitHub API to test the full analysis flow.

Run with: pytest tests/test_orchestrator.py -v
"""

import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from repogps import (
    run_analysis,
    scan_repo,
    find_entrypoints,
    extract_runbook,
    generate_summary,
    detect_repo_type,
    AnalysisResult,
)
from _github import RepoRef


class MockResponse:
    """Mock HTTP response for testing."""

    def __init__(self, json_data=None, text_data="", status_code=200):
        self._json = json_data
        self.text = text_data
        self.status_code = status_code
        self.headers = {"X-RateLimit-Remaining": "100"}

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


def create_mock_repo_tree():
    """Create a mock repo tree for a Python project."""
    return {
        "tree": [
            {"path": "README.md", "type": "blob"},
            {"path": "pyproject.toml", "type": "blob"},
            {"path": "src/main.py", "type": "blob"},
            {"path": "src/__init__.py", "type": "blob"},
            {"path": "tests/test_main.py", "type": "blob"},
            {"path": ".github/workflows/ci.yml", "type": "blob"},
        ],
        "truncated": False,
    }


def create_mock_file_contents():
    """Create mock file contents for testing."""
    return {
        "README.md": """# Test Project

A simple test project.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python -m src.main
```

## Testing

```bash
pytest tests/
```
""",
        "pyproject.toml": """
[project]
name = "test-project"
version = "0.1.0"

[project.scripts]
myapp = "src.main:main"
""",
        "src/main.py": '''
"""Main entry point."""

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
''',
        "src/__init__.py": "",
        "tests/test_main.py": """
import pytest
from src.main import main

def test_main():
    main()
""",
        ".github/workflows/ci.yml": """
name: CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -e .
      - run: pytest tests/
""",
    }


class TestGenerateSummary:
    """Tests for summary generation."""

    def test_generates_summary_from_cache(self):
        """Test that summary is generated correctly from cache files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)

            # Create mock cache files
            repo_tree = {
                "repo_url": "https://github.com/test/repo",
                "branch": "main",
                "paths": ["README.md", "main.py"],
                "total_files": 2,
                "truncated": False,
            }
            (cache_dir / "repo_tree.json").write_text(json.dumps(repo_tree))

            key_files = {
                "docs": ["README.md"],
                "entrypoints": ["main.py"],
            }
            (cache_dir / "key_files.json").write_text(json.dumps(key_files))

            entrypoints = {
                "top_entrypoints": [
                    {"path": "main.py", "confidence": 0.9, "evidence": ["path_match"]}
                ]
            }
            (cache_dir / "entrypoints.json").write_text(json.dumps(entrypoints))

            runbook = {
                "run": {"confirmed": ["python main.py"], "inferred": []},
                "test": {"confirmed": ["pytest"], "inferred": []},
                "languages_detected": ["python"],
            }
            (cache_dir / "runbook.json").write_text(json.dumps(runbook))

            # Generate summary
            summary = generate_summary(cache_dir)

            assert summary["repo_info"]["url"] == "https://github.com/test/repo"
            assert summary["repo_info"]["branch"] == "main"
            assert summary["repo_info"]["total_files"] == 2
            assert "python" in summary["languages"]
            assert len(summary["entrypoints"]) == 1
            assert summary["entrypoints"][0]["path"] == "main.py"

    def test_handles_missing_files(self):
        """Test that summary handles missing cache files gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)

            # Generate summary with empty cache
            summary = generate_summary(cache_dir)

            assert summary["repo_info"] == {}
            assert summary["key_files"] == {}
            assert summary["entrypoints"] == []
            assert summary["runbook"] == {}
            assert summary["languages"] == []


class TestFindEntrypoints:
    """Tests for entrypoint detection stage."""

    def test_finds_entrypoints_in_cache(self):
        """Test that entrypoints are detected from cached files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)
            dl_dir = cache_dir / "downloaded"
            dl_dir.mkdir(parents=True)

            # Create repo tree
            repo_tree = {
                "paths": ["src/main.py", "src/utils.py", "main.rs"],
            }
            (cache_dir / "repo_tree.json").write_text(json.dumps(repo_tree))

            # Create downloaded files with content hints
            (dl_dir / "src__main.py.txt").write_text(
                """
if __name__ == "__main__":
    main()
"""
            )
            (dl_dir / "main.rs.txt").write_text("fn main() { }")

            # Run entrypoint detection
            find_entrypoints(cache_dir)

            # Check output
            result = json.loads((cache_dir / "entrypoints.json").read_text())
            assert "top_entrypoints" in result
            assert len(result["top_entrypoints"]) > 0

            # Should find main.py and main.rs as top entrypoints
            paths = [e["path"] for e in result["top_entrypoints"]]
            assert "src/main.py" in paths or "main.rs" in paths


class TestExtractRunbook:
    """Tests for runbook extraction stage."""

    def test_extracts_commands_from_readme(self):
        """Test that commands are extracted from README."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)
            dl_dir = cache_dir / "downloaded"
            dl_dir.mkdir(parents=True)

            # Create key_files.json
            key_files = {
                "docs": ["README.md"],
                "manifests": ["pyproject.toml"],
                "ci": [],
                "entrypoints": ["main.py"],
            }
            (cache_dir / "key_files.json").write_text(json.dumps(key_files))

            # Create README with commands
            (dl_dir / "README.md.txt").write_text(
                """
# Project

```bash
python main.py
pytest tests/
```
"""
            )
            (dl_dir / "pyproject.toml.txt").write_text("[project]\nname = 'test'")

            # Run extraction
            extract_runbook(cache_dir)

            # Check output
            result = json.loads((cache_dir / "runbook.json").read_text())
            assert "python main.py" in result["run"]["confirmed"]
            assert "pytest tests/" in result["test"]["confirmed"]

    def test_extracts_from_package_json(self):
        """Test that npm scripts are extracted from package.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)
            dl_dir = cache_dir / "downloaded"
            dl_dir.mkdir(parents=True)

            # Create key_files.json
            key_files = {
                "docs": [],
                "manifests": ["package.json"],
                "ci": [],
                "entrypoints": [],
            }
            (cache_dir / "key_files.json").write_text(json.dumps(key_files))

            # Create package.json
            package_json = {
                "scripts": {
                    "dev": "node server.js",
                    "test": "jest",
                    "build": "tsc",
                }
            }
            (dl_dir / "package.json.txt").write_text(json.dumps(package_json))

            # Run extraction
            extract_runbook(cache_dir)

            # Check output
            result = json.loads((cache_dir / "runbook.json").read_text())
            assert "npm run dev" in result["run"]["confirmed"]
            assert "npm run test" in result["test"]["confirmed"]
            assert "npm run build" in result["run"]["confirmed"]

    def test_infers_commands_when_missing(self):
        """Test that commands are inferred when not found in docs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)
            dl_dir = cache_dir / "downloaded"
            dl_dir.mkdir(parents=True)

            # Create key_files.json with Python manifest but no README
            key_files = {
                "docs": [],
                "manifests": ["pyproject.toml"],
                "ci": [],
                "entrypoints": ["main.py"],
            }
            (cache_dir / "key_files.json").write_text(json.dumps(key_files))

            # Create pyproject.toml
            (dl_dir / "pyproject.toml.txt").write_text("[project]\nname = 'test'")

            # Run extraction
            extract_runbook(cache_dir)

            # Check output - should have inferred commands
            result = json.loads((cache_dir / "runbook.json").read_text())
            assert "python" in result["languages_detected"]
            assert (
                len(result["test"]["inferred"]) > 0
                or len(result["test"]["confirmed"]) > 0
            )


class TestAnalysisResult:
    """Tests for AnalysisResult dataclass."""

    def test_default_values(self):
        result = AnalysisResult(success=True)
        assert result.success is True
        assert result.cache_dir is None
        assert result.error is None
        assert result.stages_completed == []

    def test_stages_tracking(self):
        result = AnalysisResult(success=False)
        result.stages_completed.append("scan")
        result.stages_completed.append("entrypoints")
        assert len(result.stages_completed) == 2
        assert "scan" in result.stages_completed


class TestGracefulDegradation:
    """Tests for error handling and graceful degradation."""

    def test_handles_empty_cache(self):
        """Test that stages handle empty cache gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)

            # Create minimal cache structure
            (cache_dir / "repo_tree.json").write_text('{"paths": []}')
            (cache_dir / "key_files.json").write_text("{}")

            # Should not raise
            find_entrypoints(cache_dir)
            extract_runbook(cache_dir)

            # Verify outputs exist
            assert (cache_dir / "entrypoints.json").exists()
            assert (cache_dir / "runbook.json").exists()

    def test_handles_malformed_json(self):
        """Test that stages handle malformed JSON gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)
            dl_dir = cache_dir / "downloaded"
            dl_dir.mkdir(parents=True)

            # Create valid key_files.json
            (cache_dir / "key_files.json").write_text('{"manifests": ["package.json"]}')

            # Create malformed package.json
            (dl_dir / "package.json.txt").write_text("not valid json {{{")

            # Should not raise
            extract_runbook(cache_dir)

            # Should still produce output
            assert (cache_dir / "runbook.json").exists()


class TestDetectRepoType:
    """Tests for repository type detection."""

    def test_detects_monorepo(self):
        """Test monorepo detection with multiple manifest directories."""
        key_files = {
            "manifests": [
                "frontend/package.json",
                "backend/pyproject.toml",
                "shared/package.json",
            ],
            "tests_sample": ["tests/test_main.py"],
            "ci": [".github/workflows/ci.yml"],
            "docs": ["README.md"],
        }
        result = detect_repo_type(key_files, ["python", "javascript"])

        assert result["is_monorepo"] is True
        assert "frontend" in result["sub_projects"]
        assert "backend" in result["sub_projects"]

    def test_detects_single_project(self):
        """Test that single project repos are not marked as monorepos."""
        key_files = {
            "manifests": ["pyproject.toml", "requirements.txt"],
            "tests_sample": ["tests/test_main.py"],
            "ci": [".github/workflows/ci.yml"],
            "docs": ["README.md"],
        }
        result = detect_repo_type(key_files, ["python"])

        assert result["is_monorepo"] is False

    def test_detects_missing_tests(self):
        """Test warning for missing tests."""
        key_files = {
            "manifests": ["package.json"],
            "tests_sample": [],
            "ci": [".github/workflows/ci.yml"],
            "docs": ["README.md"],
        }
        result = detect_repo_type(key_files, ["javascript"])

        assert result["has_tests"] is False
        assert "No tests detected" in result["warnings"]

    def test_detects_missing_ci(self):
        """Test warning for missing CI."""
        key_files = {
            "manifests": ["package.json"],
            "tests_sample": ["tests/test.js"],
            "ci": [],
            "docs": ["README.md"],
        }
        result = detect_repo_type(key_files, ["javascript"])

        assert result["has_ci"] is False
        assert "No CI configuration found" in result["warnings"]

    def test_detects_missing_docs(self):
        """Test warning for missing documentation."""
        key_files = {
            "manifests": ["package.json"],
            "tests_sample": ["tests/test.js"],
            "ci": [".github/workflows/ci.yml"],
            "docs": [],
        }
        result = detect_repo_type(key_files, ["javascript"])

        assert result["has_docs"] is False
        assert "No README or documentation found" in result["warnings"]

    def test_detects_frameworks(self):
        """Test framework detection from manifests."""
        key_files = {
            "manifests": ["package.json", "Cargo.toml"],
            "tests_sample": [],
            "ci": [],
            "docs": [],
        }
        result = detect_repo_type(key_files, ["javascript", "rust"])

        assert "node" in result["frameworks"]
        assert "rust" in result["frameworks"]

    def test_healthy_repo_no_warnings(self):
        """Test that healthy repos have no warnings except missing tests if applicable."""
        key_files = {
            "manifests": ["pyproject.toml"],
            "tests_sample": ["tests/test_main.py"],
            "ci": [".github/workflows/ci.yml"],
            "docs": ["README.md"],
        }
        result = detect_repo_type(key_files, ["python"])

        assert result["has_tests"] is True
        assert result["has_ci"] is True
        assert result["has_docs"] is True
        assert len(result["warnings"]) == 0


class TestIntegrationWithMockedAPI:
    """Integration tests with mocked GitHub API."""

    @patch("_github.requests.get")
    def test_full_analysis_flow(self, mock_get):
        """Test the complete analysis flow with mocked API."""
        mock_contents = create_mock_file_contents()
        mock_tree = create_mock_repo_tree()

        def mock_request(url, *args, **kwargs):
            if "branches" in url:
                return MockResponse(json_data={"commit": {"sha": "abc123"}})
            elif "trees" in url:
                return MockResponse(json_data=mock_tree)
            elif "raw.githubusercontent.com" in url:
                # Extract filename from URL
                for filename, content in mock_contents.items():
                    if filename in url:
                        return MockResponse(text_data=content)
                return MockResponse(text_data="", status_code=404)
            elif "repos/" in url and "trees" not in url and "branches" not in url:
                return MockResponse(json_data={"default_branch": "main"})
            return MockResponse(json_data={})

        mock_get.side_effect = mock_request

        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_analysis(
                repo_url="https://github.com/test/repo",
                branch="main",
                out_base=Path(tmpdir),
            )

            assert result.success is True
            assert result.cache_dir is not None
            assert "scan" in result.stages_completed
            assert "entrypoints" in result.stages_completed
            assert "runbook" in result.stages_completed

            # Verify summary was generated
            summary_path = result.cache_dir / "summary.json"
            assert summary_path.exists()

            summary = json.loads(summary_path.read_text())
            assert summary["repo_info"]["url"] == "https://github.com/test/repo"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
