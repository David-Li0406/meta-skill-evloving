"""Tests for processor/inspectional.py"""
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestGenerateInspectionalReport:
    """Tests for generate_inspectional_report function"""

    def test_generate_report_basic(self, monkeypatch, temp_dir):
        """Test generating basic report without AI analysis"""
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import generate_inspectional_report

        report = generate_inspectional_report(
            source_id="test123",
            title="Test Video",
            author="Test Author",
            url="https://youtube.com/watch?v=test",
            duration=3661,  # 1:01:01
            transcript="This is the transcript"
        )

        assert "test123" in report
        assert "Test Video" in report
        assert "Test Author" in report
        assert "youtube.com/watch?v=test" in report
        assert "1:01:01" in report
        assert "待 AI 分析生成" in report

    def test_generate_report_with_ai_analysis(self, monkeypatch, temp_dir):
        """Test generating report with AI analysis"""
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import generate_inspectional_report

        ai_analysis = {
            "summary": "This is the AI summary",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "concepts": ["Concept A", "Concept B"],
            "questions": ["Question 1?", "Question 2?"]
        }

        report = generate_inspectional_report(
            source_id="test123",
            title="Test Video",
            author="Test Author",
            url="https://youtube.com/watch?v=test",
            duration=300,
            transcript="Transcript",
            ai_analysis=ai_analysis
        )

        assert "This is the AI summary" in report
        assert "1. Point 1" in report
        assert "2. Point 2" in report
        assert "3. Point 3" in report
        assert "[[Concept A]]" in report
        assert "[[Concept B]]" in report
        assert "Question 1?" in report
        assert "Question 2?" in report

    def test_generate_report_frontmatter(self, monkeypatch, temp_dir):
        """Test report contains proper frontmatter"""
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import generate_inspectional_report

        report = generate_inspectional_report(
            source_id="youtube_abc123",
            title="My Video",
            author="Creator",
            url="https://youtube.com/watch?v=abc123",
            duration=600,
            transcript="Text"
        )

        assert report.startswith("---")
        assert "source_type: youtube" in report
        assert "source_id: youtube_abc123" in report
        assert "status: draft" in report

    def test_generate_report_date_format(self, monkeypatch, temp_dir):
        """Test report contains today's date"""
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import generate_inspectional_report

        report = generate_inspectional_report(
            source_id="test",
            title="Test",
            author="Author",
            url="http://test",
            duration=100,
            transcript=""
        )

        today = datetime.now().strftime("%Y-%m-%d")
        assert today in report

    def test_generate_report_empty_ai_fields(self, monkeypatch, temp_dir):
        """Test report handles empty AI analysis fields"""
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import generate_inspectional_report

        ai_analysis = {
            "summary": "Summary only",
            "key_points": [],
            "concepts": [],
            "questions": []
        }

        report = generate_inspectional_report(
            source_id="test",
            title="Test",
            author="Author",
            url="http://test",
            duration=100,
            transcript="",
            ai_analysis=ai_analysis
        )

        assert "Summary only" in report
        # Should still have section headers
        assert "## 核心观点" in report
        assert "## 关键概念" in report


class TestSaveReport:
    """Tests for save_report function"""

    def test_save_report_creates_directory(self, monkeypatch, temp_dir):
        """Test save_report creates Obsidian directory"""
        sources_dir = temp_dir / "DeepReading" / "Sources"
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = sources_dir
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import save_report

        assert not sources_dir.exists()

        save_report("test123", "Test Title", "# Content")

        assert sources_dir.exists()

    def test_save_report_creates_file(self, monkeypatch, temp_dir):
        """Test save_report creates markdown file"""
        sources_dir = temp_dir / "Sources"
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = sources_dir
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import save_report

        file_path = save_report("test123", "My Video Title", "# Report Content")

        assert file_path.exists()
        assert file_path.suffix == ".md"
        assert file_path.read_text() == "# Report Content"

    def test_save_report_sanitizes_title(self, monkeypatch, temp_dir):
        """Test save_report sanitizes special characters in title"""
        sources_dir = temp_dir / "Sources"
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = sources_dir
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import save_report

        file_path = save_report("test", "Video: Test/Special|Chars?", "Content")

        # Special characters should be removed
        assert "/" not in file_path.name
        assert ":" not in file_path.name
        assert "|" not in file_path.name
        assert "?" not in file_path.name

    def test_save_report_truncates_long_title(self, monkeypatch, temp_dir):
        """Test save_report truncates very long titles"""
        sources_dir = temp_dir / "Sources"
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = sources_dir
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import save_report

        long_title = "A" * 200
        file_path = save_report("test", long_title, "Content")

        # Title should be truncated to 100 chars + .md
        assert len(file_path.stem) <= 100

    def test_save_report_returns_path(self, monkeypatch, temp_dir):
        """Test save_report returns the file path"""
        sources_dir = temp_dir / "Sources"
        mock_config = MagicMock()
        mock_config.OBSIDIAN_SOURCES = sources_dir
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'processor.inspectional' in sys.modules:
            del sys.modules['processor.inspectional']
        from processor.inspectional import save_report

        result = save_report("test", "Title", "Content")

        assert isinstance(result, Path)
        assert result.parent == sources_dir
