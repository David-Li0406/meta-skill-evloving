#!/usr/bin/env python3
"""
Unit tests for update_claude_md.py

Tests the CLAUDE.md update functionality including:
- Template loading and population
- Marker detection
- Insertion point detection
- Content generation
- Safe update operations

Usage:
    python test_update_claude_md.py
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Import the module to test
import update_claude_md


class TestTemplateFunctions(unittest.TestCase):
    """Test template loading and population functions."""

    def test_populate_template_basic(self):
        """Test basic template placeholder replacement."""
        template = "Project: {{PROJECT_NAME}}\nDir: {{SYMBOLS_DIR}}"

        # Mock config
        config = MagicMock()
        config.project_name = "TestProject"
        config._raw_config = {"symbolsDir": "symbols"}
        config.get_enabled_domains.return_value = []
        config.get_enabled_api_layers.return_value = []
        config.domains = {}
        config.api_layers = {}

        result = update_claude_md.populate_template(template, config, {})

        self.assertIn("TestProject", result)
        self.assertIn("symbols", result)
        self.assertNotIn("{{PROJECT_NAME}}", result)
        self.assertNotIn("{{SYMBOLS_DIR}}", result)

    def test_generate_symbol_files_section(self):
        """Test symbol files section generation."""
        # Mock config with domains
        config = MagicMock()
        config._raw_config = {"symbolsDir": "ai"}
        config.get_enabled_domains.return_value = ["ui", "api"]
        config.get_enabled_api_layers.return_value = []

        # Mock domain configs
        ui_config = MagicMock()
        ui_config.file = "symbols-ui.json"
        ui_config.description = "UI components"
        ui_config.test_file = None

        api_config = MagicMock()
        api_config.file = "symbols-api.json"
        api_config.description = "API backend"
        api_config.test_file = "symbols-api-tests.json"

        config.domains = {"ui": ui_config, "api": api_config}
        config.api_layers = {}

        stats = {"ui": 100, "api": 200, "api-tests": 50}

        result = update_claude_md.generate_symbol_files_section(config, stats)

        self.assertIn("symbols-ui.json", result)
        self.assertIn("symbols-api.json", result)
        self.assertIn("100 symbols", result)
        self.assertIn("200 symbols", result)
        self.assertIn("UI components", result)
        self.assertIn("API backend", result)


class TestMarkerDetection(unittest.TestCase):
    """Test marker and section detection functions."""

    def test_find_symbols_section_with_markers(self):
        """Test finding symbols section with markers."""
        content = """# Header

<!-- BEGIN SYMBOLS SECTION -->
Some content here
<!-- END SYMBOLS SECTION -->

More content
"""
        result = update_claude_md.find_symbols_section(content)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)  # start and end indices
        self.assertTrue(result[0] < result[1])

    def test_find_symbols_section_without_markers(self):
        """Test finding symbols section without markers."""
        content = "# Header\n\nSome content without markers\n"
        result = update_claude_md.find_symbols_section(content)

        self.assertIsNone(result)

    def test_detect_existing_symbols_content(self):
        """Test detection of symbols content without markers."""
        # Content with symbols indicators
        content_with = "This uses codebase-explorer and symbols system"
        self.assertTrue(update_claude_md.detect_existing_symbols_content(content_with))

        content_with_2 = "See symbols-ui.json for details"
        self.assertTrue(update_claude_md.detect_existing_symbols_content(content_with_2))

        # Content without symbols indicators
        content_without = "Just some regular documentation here"
        self.assertFalse(update_claude_md.detect_existing_symbols_content(content_without))


class TestInsertionPoint(unittest.TestCase):
    """Test insertion point detection."""

    def test_find_insertion_after_prime_directives(self):
        """Test finding insertion point after Prime directives."""
        content = """# CLAUDE.md

## Prime directives

- First directive
- Second directive

## Next Section

More content
"""
        result = update_claude_md.find_insertion_point(content)

        self.assertIsNotNone(result)
        # Should insert before "## Next Section"
        self.assertGreater(result, content.find("Prime directives"))
        self.assertLessEqual(result, content.find("## Next Section"))

    def test_find_insertion_after_key_guidance(self):
        """Test finding insertion point after Key Guidance."""
        content = """# CLAUDE.md

## Key Guidance

- Important point
- Another point

## Features

More content
"""
        result = update_claude_md.find_insertion_point(content)

        self.assertIsNotNone(result)
        # Should insert before "## Features"
        self.assertGreater(result, content.find("Key Guidance"))
        self.assertLessEqual(result, content.find("## Features"))

    def test_find_insertion_no_suitable_location(self):
        """Test finding insertion point when no suitable location exists."""
        content = "Just some content without proper headers"
        result = update_claude_md.find_insertion_point(content)

        # Should still return None or handle gracefully
        # (depending on implementation strategy)
        # For now, expect None
        self.assertIsNone(result)


class TestUpdateLogic(unittest.TestCase):
    """Test core update logic."""

    def test_update_with_markers_replaces_content(self):
        """Test that update replaces content between markers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            claude_md = tmpdir_path / "CLAUDE.md"

            # Create initial file with markers
            original_content = """# CLAUDE.md

## Prime directives

<!-- BEGIN SYMBOLS SECTION -->
Old symbols content here
<!-- END SYMBOLS SECTION -->

## Other Section
"""
            claude_md.write_text(original_content)

            new_template = "New symbols content"

            result = update_claude_md.update_claude_md(
                tmpdir_path,
                new_template,
                dry_run=True,
                no_backup=True
            )

            self.assertEqual(result["action"], "updated (dry-run)")
            self.assertGreater(result["lines_modified"], 0)
            self.assertEqual(len(result["errors"]), 0)

    def test_update_without_markers_inserts_content(self):
        """Test that update inserts content when no markers exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            claude_md = tmpdir_path / "CLAUDE.md"

            # Create file without markers
            original_content = """# CLAUDE.md

## Prime directives

Some content

## Next Section

More content
"""
            claude_md.write_text(original_content)

            new_template = "New symbols content"

            result = update_claude_md.update_claude_md(
                tmpdir_path,
                new_template,
                force=True,  # Force insertion
                dry_run=True,
                no_backup=True
            )

            # Should insert new content
            self.assertIn("inserted", result["action"])
            self.assertGreater(result["lines_added"], 0)
            self.assertEqual(len(result["errors"]), 0)

    def test_update_file_not_found(self):
        """Test handling of missing CLAUDE.md file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            # Don't create CLAUDE.md

            result = update_claude_md.update_claude_md(
                tmpdir_path,
                "content",
                dry_run=True,
                no_backup=True
            )

            self.assertFalse(result["exists"])
            self.assertGreater(len(result["errors"]), 0)
            self.assertIn("not found", result["errors"][0].lower())


class TestColorPrinting(unittest.TestCase):
    """Test color printing functions."""

    def test_print_color_with_color(self):
        """Test print_color when colorama is available."""
        # Just ensure it doesn't crash
        update_claude_md.print_color("Test message", "RED", "BRIGHT")

    def test_print_color_without_color(self):
        """Test print_color when colorama is not available."""
        # Save original HAS_COLOR
        original_has_color = update_claude_md.HAS_COLOR

        try:
            # Temporarily disable color
            update_claude_md.HAS_COLOR = False
            update_claude_md.print_color("Test message", "RED", "BRIGHT")
        finally:
            # Restore original
            update_claude_md.HAS_COLOR = original_has_color


class TestProjectRootDetection(unittest.TestCase):
    """Test project root detection."""

    def test_find_project_root_with_git(self):
        """Test finding project root with .git marker."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            git_dir = tmpdir_path / ".git"
            git_dir.mkdir()

            # Change to subdirectory
            sub_dir = tmpdir_path / "subdir"
            sub_dir.mkdir()

            # Temporarily change directory
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(sub_dir)
                result = update_claude_md.find_project_root()
                # Should find parent directory with .git
                self.assertEqual(result.resolve(), tmpdir_path.resolve())
            finally:
                os.chdir(original_cwd)


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTemplateFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestMarkerDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestInsertionPoint))
    suite.addTests(loader.loadTestsFromTestCase(TestUpdateLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestColorPrinting))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectRootDetection))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit(run_tests())
