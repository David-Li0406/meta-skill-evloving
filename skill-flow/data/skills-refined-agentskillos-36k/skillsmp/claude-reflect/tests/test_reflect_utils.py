#!/usr/bin/env python3
"""Tests for reflect_utils module."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.reflect_utils import (
    get_queue_path,
    get_backup_dir,
    get_claude_dir,
    load_queue,
    save_queue,
    append_to_queue,
    iso_timestamp,
    backup_timestamp,
    detect_patterns,
    create_queue_item,
    extract_user_messages,
    extract_tool_rejections,
    find_claude_files,
    suggest_claude_file,
    EXCLUDED_DIRS,
)


class TestPathUtilities(unittest.TestCase):
    """Tests for path utility functions."""

    def test_get_queue_path(self):
        """Test queue path returns correct location."""
        path = get_queue_path()
        self.assertIsInstance(path, Path)
        self.assertEqual(path.name, "learnings-queue.json")
        self.assertEqual(path.parent.name, ".claude")

    def test_get_backup_dir(self):
        """Test backup dir returns correct location."""
        path = get_backup_dir()
        self.assertIsInstance(path, Path)
        self.assertEqual(path.name, "learnings-backups")
        self.assertEqual(path.parent.name, ".claude")

    def test_get_claude_dir(self):
        """Test claude dir returns correct location."""
        path = get_claude_dir()
        self.assertIsInstance(path, Path)
        self.assertEqual(path.name, ".claude")


class TestQueueOperations(unittest.TestCase):
    """Tests for queue operations."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_queue_path = Path(self.temp_dir) / "learnings-queue.json"

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("lib.reflect_utils.get_queue_path")
    def test_load_queue_empty_file(self, mock_path):
        """Test loading empty queue."""
        mock_path.return_value = self.test_queue_path
        result = load_queue()
        self.assertEqual(result, [])

    @patch("lib.reflect_utils.get_queue_path")
    def test_load_queue_with_items(self, mock_path):
        """Test loading queue with items."""
        mock_path.return_value = self.test_queue_path
        test_items = [{"type": "auto", "message": "test"}]
        self.test_queue_path.write_text(json.dumps(test_items))

        result = load_queue()
        self.assertEqual(result, test_items)

    @patch("lib.reflect_utils.get_queue_path")
    def test_save_queue(self, mock_path):
        """Test saving queue."""
        mock_path.return_value = self.test_queue_path
        test_items = [{"type": "auto", "message": "test"}]

        save_queue(test_items)

        saved_data = json.loads(self.test_queue_path.read_text())
        self.assertEqual(saved_data, test_items)

    @patch("lib.reflect_utils.get_queue_path")
    def test_append_to_queue(self, mock_path):
        """Test appending to queue."""
        mock_path.return_value = self.test_queue_path
        self.test_queue_path.write_text("[]")

        item = {"type": "auto", "message": "new item"}
        append_to_queue(item)

        saved_data = json.loads(self.test_queue_path.read_text())
        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0]["message"], "new item")


class TestTimestampUtilities(unittest.TestCase):
    """Tests for timestamp functions."""

    def test_iso_timestamp_format(self):
        """Test ISO timestamp has correct format."""
        ts = iso_timestamp()
        # Should match YYYY-MM-DDTHH:MM:SSZ format
        self.assertRegex(ts, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_backup_timestamp_format(self):
        """Test backup timestamp has correct format."""
        ts = backup_timestamp()
        # Should match YYYYMMDD-HHMMSS format
        self.assertRegex(ts, r"^\d{8}-\d{6}$")


class TestPatternDetection(unittest.TestCase):
    """Tests for pattern detection."""

    def test_explicit_remember_pattern(self):
        """Test detection of explicit remember: marker."""
        result = detect_patterns("remember: always use gpt-5.1")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "explicit")
        self.assertIn("remember:", patterns)
        self.assertEqual(confidence, 0.90)
        self.assertEqual(decay, 120)

    def test_positive_pattern_perfect(self):
        """Test detection of positive feedback."""
        result = detect_patterns("perfect! that's exactly what I wanted")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "positive")
        self.assertEqual(sentiment, "positive")
        self.assertGreaterEqual(confidence, 0.70)

    def test_correction_no_use(self):
        """Test detection of 'no, use' correction."""
        result = detect_patterns("no, use Python instead")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertIn("no,", patterns)
        self.assertEqual(sentiment, "correction")

    def test_correction_dont_use(self):
        """Test detection of 'don't use' correction."""
        result = detect_patterns("don't use that library")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertIn("don't", patterns)

    def test_correction_stop_using(self):
        """Test detection of 'stop using' correction."""
        result = detect_patterns("stop using that approach")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertIn("stop/never", patterns)

    def test_correction_never_use(self):
        """Test detection of 'never use' correction."""
        result = detect_patterns("never use global variables")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertIn("stop/never", patterns)

    def test_correction_thats_wrong(self):
        """Test detection of 'that's wrong' correction."""
        result = detect_patterns("that's wrong, the API returns JSON")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertIn("that's-wrong", patterns)

    def test_correction_i_told_you_high_confidence(self):
        """Test that 'I told you' gets high confidence."""
        result = detect_patterns("I told you to use async")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertIn("I-told-you", patterns)
        # Base 0.85 + 0.10 short message boost = 0.90 (capped)
        self.assertGreaterEqual(confidence, 0.85)
        self.assertEqual(decay, 120)

    def test_multiple_patterns_high_confidence(self):
        """Test multiple patterns increase confidence."""
        result = detect_patterns("no, don't use that, you should use Python")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertGreaterEqual(confidence, 0.75)

    def test_guardrail_dont_add_unless(self):
        """Test detection of 'don't add X unless' guardrail pattern."""
        result = detect_patterns("don't add docstrings unless I explicitly ask")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "guardrail")
        self.assertIn("dont-unless-asked", patterns)
        self.assertGreaterEqual(confidence, 0.90)
        self.assertEqual(decay, 120)

    def test_guardrail_only_change_what_asked(self):
        """Test detection of 'only change what I asked' guardrail pattern."""
        result = detect_patterns("only change what I asked you to change")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "guardrail")
        self.assertIn("only-what-asked", patterns)
        self.assertGreaterEqual(confidence, 0.90)

    def test_guardrail_stop_refactoring(self):
        """Test detection of 'stop refactoring unrelated' guardrail pattern."""
        result = detect_patterns("stop refactoring unrelated code")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "guardrail")
        self.assertIn("stop-unrelated", patterns)

    def test_guardrail_dont_over_engineer(self):
        """Test detection of 'don't over-engineer' guardrail pattern."""
        result = detect_patterns("don't over-engineer this solution")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "guardrail")
        self.assertIn("dont-over-engineer", patterns)

    def test_guardrail_leave_alone(self):
        """Test detection of 'leave X alone' guardrail pattern."""
        result = detect_patterns("leave the existing code alone")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "guardrail")
        self.assertIn("leave-alone", patterns)

    def test_guardrail_minimal_changes(self):
        """Test detection of 'minimal changes' guardrail pattern."""
        result = detect_patterns("only make minimal changes please")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "guardrail")
        self.assertIn("minimal-changes", patterns)

    def test_no_pattern_match(self):
        """Test text without patterns returns None type."""
        result = detect_patterns("Hello, how are you?")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertIsNone(item_type)
        self.assertEqual(patterns, "")

    def test_false_positive_question_rejected(self):
        """Test that questions (ending with ?) are rejected."""
        result = detect_patterns("can you figure out how to make this fit?")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertIsNone(item_type)

    def test_false_positive_task_request_rejected(self):
        """Test that task requests are rejected."""
        result = detect_patterns("please help me fix this issue")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertIsNone(item_type)

    def test_false_positive_error_description_rejected(self):
        """Test that error descriptions are rejected."""
        result = detect_patterns("the error is: could not connect to database")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertIsNone(item_type)

    def test_false_positive_bug_report_rejected(self):
        """Test that bug reports are rejected."""
        result = detect_patterns("it just opens and closes, is not working")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertIsNone(item_type)

    def test_short_message_confidence_boost(self):
        """Test that short messages get a confidence boost."""
        result = detect_patterns("no, use gpt-5.1")
        item_type, patterns, confidence, sentiment, decay = result

        self.assertEqual(item_type, "auto")
        self.assertGreaterEqual(confidence, 0.75)  # Boosted for short message

    def test_long_message_confidence_reduced(self):
        """Test that long messages get reduced confidence."""
        long_msg = "no, " + "this is a very long explanation " * 15
        result = detect_patterns(long_msg)
        item_type, patterns, confidence, sentiment, decay = result

        # Should still match but with lower confidence
        if item_type == "auto":
            self.assertLessEqual(confidence, 0.65)


class TestQueueItemCreation(unittest.TestCase):
    """Tests for queue item creation."""

    def test_create_queue_item_all_fields(self):
        """Test queue item has all required fields."""
        item = create_queue_item(
            message="test message",
            item_type="auto",
            patterns="no,use",
            confidence=0.75,
            sentiment="correction",
            decay_days=90,
            project="/test/project",
        )

        self.assertEqual(item["message"], "test message")
        self.assertEqual(item["type"], "auto")
        self.assertEqual(item["patterns"], "no,use")
        self.assertEqual(item["confidence"], 0.75)
        self.assertEqual(item["sentiment"], "correction")
        self.assertEqual(item["decay_days"], 90)
        self.assertEqual(item["project"], "/test/project")
        self.assertIn("timestamp", item)


class TestSessionExtraction(unittest.TestCase):
    """Tests for session file extraction."""

    def setUp(self):
        """Create temporary session file."""
        self.temp_dir = tempfile.mkdtemp()
        self.session_file = Path(self.temp_dir) / "test-session.jsonl"

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_user_messages_basic(self):
        """Test extracting basic user messages."""
        session_data = [
            {
                "type": "user",
                "message": {
                    "content": [{"type": "text", "text": "Hello world"}]
                }
            },
            {
                "type": "assistant",
                "message": {"content": "Response"}
            },
            {
                "type": "user",
                "message": {
                    "content": [{"type": "text", "text": "no, use Python instead"}]
                }
            },
        ]

        with open(self.session_file, "w") as f:
            for entry in session_data:
                f.write(json.dumps(entry) + "\n")

        messages = extract_user_messages(self.session_file)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], "Hello world")
        self.assertEqual(messages[1], "no, use Python instead")

    def test_extract_user_messages_string_content(self):
        """Test extracting user messages when content is a string (not list)."""
        session_data = [
            {
                "type": "user",
                "message": {
                    "content": "This is a string content message"
                }
            },
            {
                "type": "user",
                "message": {
                    "content": "no, use this approach instead"
                }
            },
        ]

        with open(self.session_file, "w") as f:
            for entry in session_data:
                f.write(json.dumps(entry) + "\n")

        messages = extract_user_messages(self.session_file)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], "This is a string content message")
        self.assertEqual(messages[1], "no, use this approach instead")

    def test_extract_user_messages_skip_meta(self):
        """Test that isMeta messages are skipped."""
        session_data = [
            {
                "type": "user",
                "isMeta": True,
                "message": {
                    "content": [{"type": "text", "text": "Meta message"}]
                }
            },
            {
                "type": "user",
                "message": {
                    "content": [{"type": "text", "text": "Regular message"}]
                }
            },
        ]

        with open(self.session_file, "w") as f:
            for entry in session_data:
                f.write(json.dumps(entry) + "\n")

        messages = extract_user_messages(self.session_file)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], "Regular message")

    def test_extract_corrections_only(self):
        """Test extracting only correction messages."""
        session_data = [
            {
                "type": "user",
                "message": {
                    "content": [{"type": "text", "text": "Hello world"}]
                }
            },
            {
                "type": "user",
                "message": {
                    "content": [{"type": "text", "text": "no, use Python"}]
                }
            },
            {
                "type": "user",
                "message": {
                    "content": [{"type": "text", "text": "remember: always test"}]
                }
            },
        ]

        with open(self.session_file, "w") as f:
            for entry in session_data:
                f.write(json.dumps(entry) + "\n")

        messages = extract_user_messages(self.session_file, corrections_only=True)
        self.assertEqual(len(messages), 2)
        self.assertIn("no, use Python", messages)
        self.assertIn("remember: always test", messages)

    def test_extract_nonexistent_file(self):
        """Test extracting from nonexistent file returns empty list."""
        messages = extract_user_messages(Path("/nonexistent/file.jsonl"))
        self.assertEqual(messages, [])


class TestToolRejectionExtraction(unittest.TestCase):
    """Tests for tool rejection extraction."""

    def setUp(self):
        """Create temporary session file."""
        self.temp_dir = tempfile.mkdtemp()
        self.session_file = Path(self.temp_dir) / "test-session.jsonl"

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_tool_rejection_with_feedback(self):
        """Test extracting tool rejection with user feedback."""
        # Schema matches actual Claude Code session files:
        # type=user, message.content[].type=tool_result, is_error=true
        session_data = [
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "is_error": True,
                            "content": "The user doesn't want to proceed\nthe user said:\nDon't delete that file"
                        }
                    ]
                }
            },
        ]

        with open(self.session_file, "w") as f:
            for entry in session_data:
                f.write(json.dumps(entry) + "\n")

        rejections = extract_tool_rejections(self.session_file)
        self.assertEqual(len(rejections), 1)
        self.assertEqual(rejections[0], "Don't delete that file")

    def test_extract_tool_rejection_empty_feedback(self):
        """Test that empty feedback is skipped."""
        session_data = [
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "is_error": True,
                            "content": "The user doesn't want to proceed\nthe user said:\n"
                        }
                    ]
                }
            },
        ]

        with open(self.session_file, "w") as f:
            for entry in session_data:
                f.write(json.dumps(entry) + "\n")

        rejections = extract_tool_rejections(self.session_file)
        self.assertEqual(len(rejections), 0)

    def test_extract_non_rejection_tool_result(self):
        """Test that normal tool results are ignored."""
        session_data = [
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "is_error": False,
                            "content": "File created successfully"
                        }
                    ]
                }
            },
        ]

        with open(self.session_file, "w") as f:
            for entry in session_data:
                f.write(json.dumps(entry) + "\n")

        rejections = extract_tool_rejections(self.session_file)
        self.assertEqual(len(rejections), 0)


class TestClaudeFileDiscovery(unittest.TestCase):
    """Tests for CLAUDE.md file discovery."""

    def setUp(self):
        """Create temporary directory structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up temporary files and restore cwd."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_find_claude_files_root_only(self):
        """Test finding CLAUDE.md in root directory only."""
        # Create root CLAUDE.md
        root_claude = Path(self.temp_dir) / "CLAUDE.md"
        root_claude.write_text("# Test CLAUDE.md")

        files = find_claude_files(self.temp_dir)

        # Should find global and root (if global exists)
        root_files = [f for f in files if f["type"] == "root"]
        self.assertEqual(len(root_files), 1)
        self.assertEqual(root_files[0]["relative_path"], "./CLAUDE.md")

    def test_find_claude_files_subdirectory(self):
        """Test finding CLAUDE.md in subdirectories."""
        # Create root CLAUDE.md
        root_claude = Path(self.temp_dir) / "CLAUDE.md"
        root_claude.write_text("# Root")

        # Create subdirectory CLAUDE.md
        subdir = Path(self.temp_dir) / "src"
        subdir.mkdir()
        sub_claude = subdir / "CLAUDE.md"
        sub_claude.write_text("# Src")

        files = find_claude_files(self.temp_dir)

        subdir_files = [f for f in files if f["type"] == "subdirectory"]
        self.assertEqual(len(subdir_files), 1)
        self.assertIn("src/CLAUDE.md", subdir_files[0]["relative_path"])

    def test_find_claude_files_excludes_node_modules(self):
        """Test that node_modules is excluded from search."""
        # Create CLAUDE.md in node_modules (should be excluded)
        node_modules = Path(self.temp_dir) / "node_modules"
        node_modules.mkdir()
        excluded_claude = node_modules / "CLAUDE.md"
        excluded_claude.write_text("# Should be excluded")

        files = find_claude_files(self.temp_dir)

        # Should not find the node_modules CLAUDE.md
        all_paths = [f["path"] for f in files]
        self.assertFalse(any("node_modules" in p for p in all_paths))

    def test_find_claude_files_excludes_git(self):
        """Test that .git is excluded from search."""
        # Create CLAUDE.md in .git (should be excluded)
        git_dir = Path(self.temp_dir) / ".git"
        git_dir.mkdir()
        excluded_claude = git_dir / "CLAUDE.md"
        excluded_claude.write_text("# Should be excluded")

        files = find_claude_files(self.temp_dir)

        # Should not find the .git CLAUDE.md
        all_paths = [f["path"] for f in files]
        self.assertFalse(any(".git" in p for p in all_paths))

    def test_excluded_dirs_constant(self):
        """Test that EXCLUDED_DIRS contains expected directories."""
        self.assertIn("node_modules", EXCLUDED_DIRS)
        self.assertIn(".git", EXCLUDED_DIRS)
        self.assertIn("venv", EXCLUDED_DIRS)
        self.assertIn("__pycache__", EXCLUDED_DIRS)


class TestSuggestClaudeFile(unittest.TestCase):
    """Tests for suggest_claude_file function."""

    def test_suggest_global_for_model_names(self):
        """Test that model names suggest global CLAUDE.md."""
        files = [
            {"path": "/home/.claude/CLAUDE.md", "relative_path": "~/.claude/CLAUDE.md", "type": "global"},
            {"path": "/project/CLAUDE.md", "relative_path": "./CLAUDE.md", "type": "root"},
        ]

        result = suggest_claude_file("Use gpt-5.1 for reasoning tasks", files)
        self.assertEqual(result, "~/.claude/CLAUDE.md")

        result = suggest_claude_file("claude-opus is better for coding", files)
        self.assertEqual(result, "~/.claude/CLAUDE.md")

    def test_suggest_global_for_always_never(self):
        """Test that 'always/never' patterns suggest global."""
        files = [
            {"path": "/home/.claude/CLAUDE.md", "relative_path": "~/.claude/CLAUDE.md", "type": "global"},
            {"path": "/project/CLAUDE.md", "relative_path": "./CLAUDE.md", "type": "root"},
        ]

        result = suggest_claude_file("always run tests before committing", files)
        self.assertEqual(result, "~/.claude/CLAUDE.md")

        result = suggest_claude_file("never use force push on main", files)
        self.assertEqual(result, "~/.claude/CLAUDE.md")

    def test_suggest_subdirectory_when_mentioned(self):
        """Test suggestion based on directory name in learning."""
        files = [
            {"path": "/home/.claude/CLAUDE.md", "relative_path": "~/.claude/CLAUDE.md", "type": "global"},
            {"path": "/project/CLAUDE.md", "relative_path": "./CLAUDE.md", "type": "root"},
            {"path": "/project/api/CLAUDE.md", "relative_path": "./api/CLAUDE.md", "type": "subdirectory"},
        ]

        result = suggest_claude_file("The api module uses REST conventions", files)
        self.assertEqual(result, "./api/CLAUDE.md")

    def test_suggest_none_for_ambiguous(self):
        """Test that ambiguous learnings return None (let Claude decide)."""
        files = [
            {"path": "/home/.claude/CLAUDE.md", "relative_path": "~/.claude/CLAUDE.md", "type": "global"},
            {"path": "/project/CLAUDE.md", "relative_path": "./CLAUDE.md", "type": "root"},
        ]

        result = suggest_claude_file("Use database connection pooling", files)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
