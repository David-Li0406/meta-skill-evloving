#!/usr/bin/env python3
"""
Unit tests for cartographer4all codebase scanner
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the scanner module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
try:
    from scan_codebase import (
        parse_gitignore, matches_pattern, should_ignore, count_tokens,
        is_text_file, scan_directory, format_tree, DEFAULT_IGNORE
    )
except ImportError:
    # For testing, create a minimal version of the module
    import argparse
    import json
    from pathlib import Path
    
    DEFAULT_IGNORE = {
        ".git", ".svn", ".hg", "node_modules", "__pycache__", ".pytest_cache",
        ".mypy_cache", ".ruff_cache", "venv", ".venv", "env", ".env", "dist",
        "build", ".next", ".nuxt", ".output", "coverage", ".coverage", ".nyc_output",
        "target", "vendor", ".bundle", ".cargo", ".DS_Store", "Thumbs.db",
        "*.pyc", "*.pyo", "*.so", "*.dylib", "*.dll", "*.exe", "*.o", "*.a",
        "*.lib", "*.class", "*.jar", "*.war", "*.egg", "*.whl", "*.lock",
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
        "Cargo.lock", "poetry.lock", "Gemfile.lock", "composer.lock",
        "*.png", "*.jpg", "*.jpeg", "*.gif", "*.ico", "*.svg", "*.webp",
        "*.mp3", "*.mp4", "*.wav", "*.avi", "*.mov", "*.pdf", "*.zip",
        "*.tar", "*.gz", "*.rar", "*.7z", "*.woff", "*.woff2", "*.ttf",
        "*.eot", "*.otf", "*.min.js", "*.min.css", "*.map", "*.chunk.js", "*.bundle.js",
    }
    
    # Mock implementations for testing
    def parse_gitignore(root): return []
    def matches_pattern(path, pattern, root): return False
    def should_ignore(path, root, gitignore_patterns): return False
    def count_tokens(text, encoding=None): return len(text) // 4
    def is_text_file(path): return path.suffix in ['.py', '.js', '.ts', '.md', '.txt']
    def scan_directory(root, encoding=None, max_file_tokens=50000): return {"files": [], "directories": [], "total_tokens": 0, "total_files": 0, "skipped": []}
    def format_tree(scan_result, show_tokens=True): return "tree output"


class TestGitIgnoreParsing(unittest.TestCase):
    """Test gitignore parsing functionality"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_parse_empty_gitignore(self):
        """Test parsing empty gitignore"""
        result = parse_gitignore(self.temp_dir)
        self.assertEqual(result, [])
    
    def test_parse_basic_gitignore(self):
        """Test parsing basic gitignore patterns"""
        gitignore_path = self.temp_dir / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write("node_modules\n*.pyc\n.env\n# comment\n\n")
        
        result = parse_gitignore(self.temp_dir)
        expected = ["node_modules", "*.pyc", ".env"]
        self.assertEqual(result, expected)
    
    def test_parse_nonexistent_gitignore(self):
        """Test parsing when .gitignore doesn't exist"""
        result = parse_gitignore(self.temp_dir)
        self.assertEqual(result, [])


class TestPatternMatching(unittest.TestCase):
    """Test pattern matching functionality"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_match_exact_file(self):
        """Test exact file matching"""
        path = self.temp_dir / "node_modules"
        pattern = "node_modules"
        self.assertTrue(matches_pattern(path, pattern, self.temp_dir))
    
    def test_match_wildcard(self):
        """Test wildcard pattern matching"""
        path = self.temp_dir / "test.pyc"
        pattern = "*.pyc"
        self.assertTrue(matches_pattern(path, pattern, self.temp_dir))
    
    def test_match_directory_pattern(self):
        """Test directory pattern matching"""
        dir_path = self.temp_dir / "build"
        dir_path.mkdir()
        pattern = "build/"
        self.assertTrue(matches_pattern(dir_path, pattern, self.temp_dir))
    
    def test_negation_pattern(self):
        """Test negation pattern (!pattern)"""
        path = self.temp_dir / "important.txt"
        pattern = "!important.txt"
        self.assertFalse(matches_pattern(path, pattern, self.temp_dir))


class TestIgnoreLogic(unittest.TestCase):
    """Test ignore logic"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_ignore_default_patterns(self):
        """Test that default patterns are ignored"""
        test_paths = [
            self.temp_dir / "node_modules",
            self.temp_dir / ".git",
            self.temp_dir / "test.pyc",
            self.temp_dir / "dist",
            self.temp_dir / "build"
        ]
        
        for path in test_paths:
            if path.suffix:
                path.touch()
            else:
                path.mkdir()
            
            self.assertTrue(should_ignore(path, self.temp_dir, []))
    
    def test_custom_gitignore_patterns(self):
        """Test custom gitignore patterns"""
        gitignore_path = self.temp_dir / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write("custom_dir\n*.custom\n")
        
        # Create test files/dirs
        (self.temp_dir / "custom_dir").mkdir()
        (self.temp_dir / "test.custom").touch()
        (self.temp_dir / "normal.txt").touch()
        
        custom_patterns = parse_gitignore(self.temp_dir)
        
        self.assertTrue(should_ignore(self.temp_dir / "custom_dir", self.temp_dir, custom_patterns))
        self.assertTrue(should_ignore(self.temp_dir / "test.custom", self.temp_dir, custom_patterns))
        self.assertFalse(should_ignore(self.temp_dir / "normal.txt", self.temp_dir, custom_patterns))


class TestTokenCounting(unittest.TestCase):
    """Test token counting functionality"""
    
    def test_count_tokens_without_encoding(self):
        """Test token counting without encoding (char-based)"""
        text = "Hello, world!"
        result = count_tokens(text)
        self.assertEqual(result, len(text) // 4)  # Should be character count divided by 4
    
    def test_count_tokens_with_encoding(self):
        """Test token counting with encoding"""
        text = "Hello, world!"
        mock_encoding = MagicMock()
        mock_encoding.encode.return_value = [1, 2, 3, 4, 5]  # 5 tokens
        
        result = count_tokens(text, mock_encoding)
        self.assertEqual(result, 5)
    
    def test_count_tokens_encoding_fallback(self):
        """Test fallback when encoding fails"""
        text = "Hello, world!"
        mock_encoding = MagicMock()
        mock_encoding.encode.side_effect = Exception("Encoding failed")
        
        result = count_tokens(text, mock_encoding)
        self.assertEqual(result, len(text) // 4)


class TestTextFileDetection(unittest.TestCase):
    """Test text file detection"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_text_file_by_extension(self):
        """Test text file detection by extension"""
        text_files = [
            "test.py", "test.js", "test.ts", "test.md", "test.txt",
            "test.json", "test.yaml", "test.css", "test.html"
        ]
        
        for filename in text_files:
            path = self.temp_dir / filename
            path.touch()
            self.assertTrue(is_text_file(path), f"Failed for {filename}")
    
    def test_text_file_by_name(self):
        """Test text file detection by name"""
        text_files = [
            "README", "LICENSE", "Dockerfile", "Makefile",
            "readme", "license", "dockerfile"
        ]
        
        for filename in text_files:
            path = self.temp_dir / filename
            path.touch()
            self.assertTrue(is_text_file(path), f"Failed for {filename}")
    
    def test_binary_file_detection(self):
        """Test binary file detection"""
        # Create a binary file with null bytes
        binary_path = self.temp_dir / "binary.exe"
        with open(binary_path, 'wb') as f:
            f.write(b"Binary file \x00 with null bytes")
        
        self.assertFalse(is_text_file(binary_path))
    
    def test_empty_file_detection(self):
        """Test empty file detection"""
        empty_path = self.temp_dir / "empty.txt"
        empty_path.touch()
        self.assertTrue(is_text_file(empty_path))


class TestDirectoryScanning(unittest.TestCase):
    """Test directory scanning functionality"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_scan_empty_directory(self):
        """Test scanning empty directory"""
        result = scan_directory(self.temp_dir)
        
        self.assertEqual(result["files"], [])
        self.assertEqual(result["directories"], [])
        self.assertEqual(result["total_tokens"], 0)
        self.assertEqual(result["total_files"], 0)
    
    def test_scan_simple_directory(self):
        """Test scanning directory with files"""
        # Create test files
        (self.temp_dir / "test.py").write_text("print('hello')")
        (self.temp_dir / "test.js").write_text("console.log('hello')")
        subdir = self.temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "test.md").write_text("# Test")
        
        result = scan_directory(self.temp_dir)
        
        self.assertEqual(result["total_files"], 3)
        self.assertEqual(len(result["files"]), 3)
        self.assertIn("subdir", result["directories"])
        self.assertGreater(result["total_tokens"], 0)
    
    def test_scan_ignores_gitignore(self):
        """Test that scanning respects .gitignore"""
        gitignore_path = self.temp_dir / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write("ignored/\n*.ignored\n")
        
        # Create files
        (self.temp_dir / "included.txt").write_text("included")
        (self.temp_dir / "test.ignored").write_text("ignored")
        ignored_dir = self.temp_dir / "ignored"
        ignored_dir.mkdir()
        (ignored_dir / "file.txt").write_text("ignored")
        
        result = scan_directory(self.temp_dir)
        
        # Should only include the non-ignored file
        file_paths = [f["path"] for f in result["files"]]
        self.assertIn("included.txt", file_paths)
        self.assertNotIn("test.ignored", file_paths)
        self.assertNotIn("ignored/file.txt", file_paths)
    
    def test_scan_handles_large_files(self):
        """Test handling of large files"""
        # Create a large file (over 1MB)
        large_path = self.temp_dir / "large.txt"
        with open(large_path, 'w') as f:
            f.write("x" * 2_000_000)  # 2MB
        
        result = scan_directory(self.temp_dir)
        
        # Large file should be in skipped
        skipped_reasons = [s["reason"] for s in result["skipped"]]
        self.assertIn("too_large", skipped_reasons)
    
    def test_scan_handles_high_token_files(self):
        """Test handling of files with too many tokens"""
        # Create a file with many tokens
        high_token_path = self.temp_dir / "high_tokens.txt"
        with open(high_token_path, 'w') as f:
            f.write("word " * 100_000)  # Lots of tokens
        
        # Use low token limit for testing
        result = scan_directory(self.temp_dir, max_file_tokens=1000)
        
        # Should be skipped for too many tokens
        skipped_reasons = [s["reason"] for s in result["skipped"]]
        self.assertIn("too_many_tokens", skipped_reasons)


class TestTreeFormatting(unittest.TestCase):
    """Test tree formatting functionality"""
    
    def test_format_tree_basic(self):
        """Test basic tree formatting"""
        scan_result = {
            "root": "/test",
            "files": [
                {"path": "file1.py", "tokens": 100},
                {"path": "dir/file2.js", "tokens": 200},
                {"path": "dir/subdir/file3.md", "tokens": 50}
            ],
            "directories": ["dir", "dir/subdir"],
            "total_tokens": 350,
            "total_files": 3,
            "skipped": []
        }
        
        formatted = format_tree(scan_result)
        
        self.assertIn("test/", formatted)
        self.assertIn("3 files", formatted)
        self.assertIn("350 tokens", formatted)
        self.assertIn("file1.py", formatted)
        self.assertIn("dir/", formatted)
    
    def test_format_tree_no_tokens(self):
        """Test tree formatting without token counts"""
        scan_result = {
            "root": "/test",
            "files": [
                {"path": "file1.py", "tokens": 100}
            ],
            "directories": [],
            "total_tokens": 100,
            "total_files": 1,
            "skipped": []
        }
        
        # Mock the formatting to test show_tokens=False
        with patch('scan_codebase.format_tree') as mock_format:
            mock_format.return_value = "formatted_output"
            result = format_tree(scan_result, show_tokens=False)
            mock_format.assert_called_with(scan_result, show_tokens=False)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_scan_workflow(self):
        """Test complete scanning workflow"""
        # Create a realistic project structure
        gitignore_path = self.temp_dir / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write("node_modules\n*.pyc\n.env\n")
        
        # Create directories and files
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "src" / "main.py").write_text("print('hello')")
        (self.temp_dir / "src" / "utils.py").write_text("def helper(): pass")
        (self.temp_dir / "tests").mkdir()
        (self.temp_dir / "tests" / "test_main.py").write_text("def test(): pass")
        (self.temp_dir / "README.md").write_text("# Test Project")
        (self.temp_dir / "requirements.txt").write_text("pytest==7.0.0")
        
        # Create ignored items
        (self.temp_dir / "node_modules").mkdir()
        (self.temp_dir / "node_modules" / "package.json").write_text("{}")
        (self.temp_dir / ".env").write_text("SECRET=123")
        (self.temp_dir / "test.pyc").write_bytes(b"compiled")
        
        result = scan_directory(self.temp_dir)
        
        # Verify results
        self.assertEqual(result["total_files"], 5)  # Should ignore node_modules, .env, .pyc
        file_paths = [f["path"] for f in result["files"]]
        
        expected_files = [
            "README.md", "requirements.txt",
            "src/main.py", "src/utils.py", "tests/test_main.py"
        ]
        
        for expected in expected_files:
            self.assertIn(expected, file_paths)
        
        # Should include directories
        self.assertIn("src", result["directories"])
        self.assertIn("tests", result["directories"])
        
        # Should have skipped items
        self.assertGreater(len(result["skipped"]), 0)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestGitIgnoreParsing,
        TestPatternMatching,
        TestIgnoreLogic,
        TestTokenCounting,
        TestTextFileDetection,
        TestDirectoryScanning,
        TestTreeFormatting,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)