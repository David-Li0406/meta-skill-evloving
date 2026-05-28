#!/usr/bin/env python3
"""
Integration tests for local directory scanning.

Run with: pytest tests/test_local_integration.py -v
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from _github import (
    is_local_path,
    parse_local_path,
    get_local_tree,
    read_local_file,
    copy_local_files,
    LocalRef,
)


class TestIsLocalPath:
    """Tests for local path detection."""

    def test_detects_current_directory(self):
        assert is_local_path(".")

    def test_detects_parent_directory(self):
        assert is_local_path("..")

    def test_detects_absolute_path(self, tmp_path):
        assert is_local_path(str(tmp_path))

    def test_detects_relative_path(self):
        # Create a temp dir in current directory
        test_dir = Path("./test_temp_dir")
        test_dir.mkdir(exist_ok=True)
        try:
            assert is_local_path("./test_temp_dir")
        finally:
            test_dir.rmdir()

    def test_rejects_github_https_url(self):
        assert not is_local_path("https://github.com/owner/repo")

    def test_rejects_github_http_url(self):
        assert not is_local_path("http://github.com/owner/repo")

    def test_rejects_github_ssh_url(self):
        assert not is_local_path("git@github.com:owner/repo.git")

    def test_rejects_nonexistent_path(self):
        assert not is_local_path("/this/path/does/not/exist/hopefully")


class TestParseLocalPath:
    """Tests for local path parsing."""

    def test_parses_absolute_path(self, tmp_path):
        ref = parse_local_path(str(tmp_path))
        assert isinstance(ref, LocalRef)
        assert ref.path == tmp_path
        assert ref.name == tmp_path.name

    def test_parses_relative_path(self):
        ref = parse_local_path(".")
        assert isinstance(ref, LocalRef)
        assert ref.path.is_absolute()

    def test_expands_tilde(self):
        ref = parse_local_path("~")
        assert isinstance(ref, LocalRef)
        assert ref.path.is_absolute()
        assert not str(ref.path).startswith("~")

    def test_raises_on_nonexistent_path(self):
        try:
            parse_local_path("/this/does/not/exist")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "does not exist" in str(e)

    def test_raises_on_file_not_directory(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        try:
            parse_local_path(str(test_file))
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not a directory" in str(e)


class TestGetLocalTree:
    """Tests for local directory tree scanning."""

    def test_scans_simple_directory(self, tmp_path):
        # Create test structure
        (tmp_path / "file1.py").write_text("print('hello')")
        (tmp_path / "file2.js").write_text("console.log('hello')")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file3.txt").write_text("hello")

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        paths, truncated = get_local_tree(ref)

        assert not truncated
        assert "file1.py" in paths
        assert "file2.js" in paths
        assert "subdir/file3.txt" in paths

    def test_skips_hidden_files(self, tmp_path):
        (tmp_path / ".hidden").write_text("secret")
        (tmp_path / "visible.py").write_text("print('hello')")

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        paths, truncated = get_local_tree(ref)

        assert "visible.py" in paths
        assert ".hidden" not in paths

    def test_includes_special_dotfiles(self, tmp_path):
        (tmp_path / ".gitignore").write_text("*.pyc")
        (tmp_path / ".env.example").write_text("KEY=value")

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        paths, truncated = get_local_tree(ref)

        assert ".gitignore" in paths
        assert ".env.example" in paths

    def test_skips_node_modules(self, tmp_path):
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "package.json").write_text("{}")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "index.js").write_text("console.log('hello')")

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        paths, truncated = get_local_tree(ref)

        assert "src/index.js" in paths
        assert not any("node_modules" in p for p in paths)

    def test_skips_git_directory(self, tmp_path):
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").write_text("[core]")
        (tmp_path / "README.md").write_text("# Test")

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        paths, truncated = get_local_tree(ref)

        assert "README.md" in paths
        assert not any(".git" in p for p in paths)


class TestReadLocalFile:
    """Tests for reading local files."""

    def test_reads_text_file(self, tmp_path):
        test_file = tmp_path / "test.py"
        content = "print('hello world')"
        test_file.write_text(content)

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        result = read_local_file(ref, "test.py")

        assert result == content

    def test_truncates_large_file(self, tmp_path):
        test_file = tmp_path / "large.txt"
        content = "x" * 200_000
        test_file.write_text(content)

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        result = read_local_file(ref, "large.txt", max_chars=1000)

        assert len(result) < 200_000
        assert "TRUNCATED" in result

    def test_raises_on_nonexistent_file(self, tmp_path):
        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        try:
            read_local_file(ref, "nonexistent.txt")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_handles_utf8_content(self, tmp_path):
        test_file = tmp_path / "unicode.txt"
        content = "Hello 世界 🌍"
        test_file.write_text(content, encoding="utf-8")

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        result = read_local_file(ref, "unicode.txt")

        assert result == content


class TestCopyLocalFiles:
    """Tests for copying local files to cache."""

    def test_copies_files_successfully(self, tmp_path):
        # Create source files
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "file1.py").write_text("print('1')")
        (tmp_path / "src" / "file2.py").write_text("print('2')")

        # Create output directory
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        ref = LocalRef(path=tmp_path / "src", name="src")
        results = copy_local_files(
            ref,
            ["file1.py", "file2.py"],
            output_dir,
            show_progress=False,
        )

        assert len(results) == 2
        assert all(r.success for r in results)
        assert (output_dir / "file1.py.txt").exists()
        assert (output_dir / "file2.py.txt").exists()

    def test_handles_missing_files_gracefully(self, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        ref = LocalRef(path=tmp_path, name=tmp_path.name)
        results = copy_local_files(
            ref,
            ["nonexistent.py"],
            output_dir,
            show_progress=False,
        )

        assert len(results) == 1
        assert not results[0].success
        assert results[0].error is not None


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
