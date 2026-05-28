#!/usr/bin/env python3
"""
Tests for _github.py shared utilities.

Run with: pytest tests/test_github.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from _github import (
    parse_github_url,
    pick_key_files,
    score_entrypoint_path,
    score_entrypoint_content,
    extract_ci_commands,
    slugify_path,
    RepoRef,
)


class TestParseGitHubUrl:
    """Tests for parse_github_url function."""

    def test_https_url(self):
        ref = parse_github_url("https://github.com/owner/repo")
        assert ref.owner == "owner"
        assert ref.repo == "repo"

    def test_https_url_with_trailing_slash(self):
        ref = parse_github_url("https://github.com/owner/repo/")
        assert ref.owner == "owner"
        assert ref.repo == "repo"

    def test_https_url_with_git_suffix(self):
        ref = parse_github_url("https://github.com/owner/repo.git")
        assert ref.owner == "owner"
        assert ref.repo == "repo"

    def test_ssh_url(self):
        ref = parse_github_url("git@github.com:owner/repo.git")
        assert ref.owner == "owner"
        assert ref.repo == "repo"

    def test_ssh_url_without_git_suffix(self):
        ref = parse_github_url("git@github.com:owner/repo")
        assert ref.owner == "owner"
        assert ref.repo == "repo"

    def test_invalid_url_raises(self):
        try:
            parse_github_url("https://gitlab.com/owner/repo")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestPickKeyFiles:
    """Tests for pick_key_files function."""

    def test_finds_readme(self):
        paths = ["README.md", "src/main.py", "tests/test_main.py"]
        result = pick_key_files(paths)
        assert "README.md" in result["docs"]

    def test_finds_python_manifest(self):
        paths = ["README.md", "pyproject.toml", "src/main.py"]
        result = pick_key_files(paths)
        assert "pyproject.toml" in result["manifests"]

    def test_finds_package_json(self):
        paths = ["package.json", "src/index.ts", "tsconfig.json"]
        result = pick_key_files(paths)
        assert "package.json" in result["manifests"]

    def test_finds_cargo_toml(self):
        paths = ["Cargo.toml", "src/main.rs", "src/lib.rs"]
        result = pick_key_files(paths)
        assert "Cargo.toml" in result["manifests"]

    def test_finds_github_actions(self):
        paths = [".github/workflows/ci.yml", "src/main.py"]
        result = pick_key_files(paths)
        assert ".github/workflows/ci.yml" in result["ci"]

    def test_finds_gitlab_ci(self):
        paths = [".gitlab-ci.yml", "src/main.py"]
        result = pick_key_files(paths)
        assert ".gitlab-ci.yml" in result["ci"]

    def test_finds_entrypoints_python(self):
        paths = ["main.py", "src/utils.py", "tests/test_main.py"]
        result = pick_key_files(paths)
        assert "main.py" in result["entrypoints"]

    def test_finds_entrypoints_rust(self):
        paths = ["src/main.rs", "src/lib.rs", "src/utils.rs"]
        result = pick_key_files(paths)
        assert "src/main.rs" in result["entrypoints"]
        assert "src/lib.rs" in result["entrypoints"]

    def test_finds_entrypoints_go(self):
        paths = ["main.go", "pkg/utils.go"]
        result = pick_key_files(paths)
        assert "main.go" in result["entrypoints"]

    def test_finds_tests(self):
        paths = ["src/utils.py", "tests/test_main.py", "tests/test_utils.py"]
        result = pick_key_files(paths)
        assert len(result["tests_sample"]) >= 2

    def test_finds_nested_entrypoints(self):
        paths = ["home-mixer/main.rs", "thunder/main.rs"]
        result = pick_key_files(paths)
        assert "home-mixer/main.rs" in result["entrypoints"]
        assert "thunder/main.rs" in result["entrypoints"]


class TestScoreEntrypointPath:
    """Tests for entrypoint path scoring."""

    def test_python_main(self):
        assert score_entrypoint_path("main.py") > 0.8

    def test_python_src_main(self):
        assert score_entrypoint_path("src/main.py") > 0.8

    def test_rust_main(self):
        assert score_entrypoint_path("src/main.rs") > 0.9

    def test_go_main(self):
        assert score_entrypoint_path("main.go") > 0.8

    def test_java_main(self):
        assert score_entrypoint_path("src/Main.java") > 0.8

    def test_csharp_program(self):
        assert score_entrypoint_path("Program.cs") > 0.8

    def test_non_entrypoint(self):
        assert score_entrypoint_path("utils.py") == 0.0

    def test_nested_main(self):
        assert score_entrypoint_path("home-mixer/main.rs") > 0.8


class TestScoreEntrypointContent:
    """Tests for entrypoint content scoring."""

    def test_python_main_guard(self):
        content = """
if __name__ == "__main__":
    main()
"""
        assert score_entrypoint_content(content) > 0.1

    def test_fastapi(self):
        content = "app = FastAPI()"
        assert score_entrypoint_content(content) > 0.1

    def test_rust_main(self):
        content = "fn main() {"
        assert score_entrypoint_content(content) > 0.15

    def test_go_main(self):
        content = "func main() {"
        assert score_entrypoint_content(content) > 0.15

    def test_java_main(self):
        content = "public static void main(String[] args) {"
        assert score_entrypoint_content(content) > 0.15

    def test_spring_boot(self):
        content = "@SpringBootApplication"
        assert score_entrypoint_content(content) > 0.1


class TestExtractCICommands:
    """Tests for CI command extraction."""

    def test_github_actions(self):
        yaml = """
name: CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm install
      - run: npm test
"""
        run_cmds, test_cmds = extract_ci_commands(yaml, ".github/workflows/ci.yml")
        assert "npm test" in test_cmds

    def test_gitlab_ci(self):
        yaml = """
test:
  script:
    - npm install
    - npm test
"""
        run_cmds, test_cmds = extract_ci_commands(yaml, ".gitlab-ci.yml")
        assert "npm test" in test_cmds

    def test_cargo_test(self):
        yaml = """
name: CI
jobs:
  test:
    steps:
      - run: cargo test
"""
        run_cmds, test_cmds = extract_ci_commands(yaml, ".github/workflows/ci.yml")
        assert "cargo test" in test_cmds


class TestSlugifyPath:
    """Tests for slugify_path function."""

    def test_simple_path(self):
        assert slugify_path("src/main.py") == "src__main.py"

    def test_deep_path(self):
        assert slugify_path("a/b/c/d.py") == "a__b__c__d.py"

    def test_no_slashes(self):
        assert slugify_path("main.py") == "main.py"


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
