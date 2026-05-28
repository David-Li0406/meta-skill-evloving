"""Tests for models.py"""
import pytest
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import (
    SourceType, ProcessingState, ChapterType, MarkType, NoteType, NoteStatus,
    Source, Chapter, Mark, Note
)


class TestEnums:
    """Tests for enum classes"""

    def test_source_type_values(self):
        """Test SourceType enum values"""
        assert SourceType.YOUTUBE.value == "youtube"
        assert SourceType.PODCAST.value == "podcast"
        assert SourceType.WEB.value == "web"
        assert SourceType.PDF.value == "pdf"

    def test_processing_state_values(self):
        """Test ProcessingState enum values"""
        assert ProcessingState.PENDING.value == "pending"
        assert ProcessingState.DOWNLOADING.value == "downloading"
        assert ProcessingState.PROCESSING.value == "processing"
        assert ProcessingState.READY.value == "ready"
        assert ProcessingState.REVIEWED.value == "reviewed"
        assert ProcessingState.ERROR.value == "error"

    def test_chapter_type_values(self):
        """Test ChapterType enum values"""
        assert ChapterType.INTRO.value == "intro"
        assert ChapterType.CORE.value == "core"
        assert ChapterType.SKIP.value == "skip"
        assert ChapterType.OUTRO.value == "outro"

    def test_mark_type_values(self):
        """Test MarkType enum values"""
        assert MarkType.HIGHLIGHT.value == "highlight"
        assert MarkType.QUESTION.value == "question"
        assert MarkType.NOTE.value == "note"

    def test_note_type_values(self):
        """Test NoteType enum values"""
        assert NoteType.SOURCE.value == "source"
        assert NoteType.CARD.value == "card"

    def test_note_status_values(self):
        """Test NoteStatus enum values"""
        assert NoteStatus.DRAFT.value == "draft"
        assert NoteStatus.REVIEWED.value == "reviewed"
        assert NoteStatus.SYNCED.value == "synced"


class TestSourceDataclass:
    """Tests for Source dataclass"""

    def test_source_with_required_fields(self):
        """Test creating Source with only required fields"""
        source = Source(id="test123", type=SourceType.YOUTUBE)
        assert source.id == "test123"
        assert source.type == SourceType.YOUTUBE
        assert source.url is None
        assert source.title is None
        assert source.processing_state == ProcessingState.PENDING

    def test_source_with_all_fields(self):
        """Test creating Source with all fields"""
        now = datetime.now()
        source = Source(
            id="test123",
            type=SourceType.PODCAST,
            url="https://example.com/podcast",
            title="Test Podcast",
            author="Test Author",
            duration=3600,
            cache_path="/tmp/cache",
            processing_state=ProcessingState.READY,
            created_at=now,
            updated_at=now
        )
        assert source.id == "test123"
        assert source.type == SourceType.PODCAST
        assert source.url == "https://example.com/podcast"
        assert source.title == "Test Podcast"
        assert source.author == "Test Author"
        assert source.duration == 3600
        assert source.cache_path == "/tmp/cache"
        assert source.processing_state == ProcessingState.READY
        assert source.created_at == now
        assert source.updated_at == now

    def test_source_default_timestamps(self):
        """Test that Source has default timestamps"""
        source = Source(id="test", type=SourceType.WEB)
        assert isinstance(source.created_at, datetime)
        assert isinstance(source.updated_at, datetime)


class TestChapterDataclass:
    """Tests for Chapter dataclass"""

    def test_chapter_with_required_fields(self):
        """Test creating Chapter with required fields"""
        chapter = Chapter(
            id=1,
            source_id="test123",
            start_time=0,
            end_time=300,
            title="Introduction"
        )
        assert chapter.id == 1
        assert chapter.source_id == "test123"
        assert chapter.start_time == 0
        assert chapter.end_time == 300
        assert chapter.title == "Introduction"
        assert chapter.type == ChapterType.CORE

    def test_chapter_with_custom_type(self):
        """Test Chapter with custom type"""
        chapter = Chapter(
            id=None,
            source_id="test123",
            start_time=0,
            end_time=60,
            title="Intro",
            type=ChapterType.INTRO
        )
        assert chapter.type == ChapterType.INTRO


class TestMarkDataclass:
    """Tests for Mark dataclass"""

    def test_mark_with_required_fields(self):
        """Test creating Mark with required fields"""
        mark = Mark(
            id=1,
            source_id="test123",
            timestamp=120,
            type=MarkType.HIGHLIGHT
        )
        assert mark.id == 1
        assert mark.source_id == "test123"
        assert mark.timestamp == 120
        assert mark.type == MarkType.HIGHLIGHT
        assert mark.content is None

    def test_mark_with_content(self):
        """Test Mark with content"""
        mark = Mark(
            id=None,
            source_id="test123",
            timestamp=60,
            type=MarkType.NOTE,
            content="This is important"
        )
        assert mark.content == "This is important"

    def test_mark_default_timestamp(self):
        """Test that Mark has default created_at"""
        mark = Mark(id=None, source_id="test", timestamp=0, type=MarkType.QUESTION)
        assert isinstance(mark.created_at, datetime)


class TestNoteDataclass:
    """Tests for Note dataclass"""

    def test_note_with_required_fields(self):
        """Test creating Note with required fields"""
        note = Note(
            id=1,
            source_id="test123",
            type=NoteType.SOURCE,
            title="Test Note"
        )
        assert note.id == 1
        assert note.source_id == "test123"
        assert note.type == NoteType.SOURCE
        assert note.title == "Test Note"
        assert note.content is None
        assert note.obsidian_path is None
        assert note.status == NoteStatus.DRAFT

    def test_note_with_all_fields(self):
        """Test Note with all fields"""
        now = datetime.now()
        note = Note(
            id=1,
            source_id="test123",
            type=NoteType.CARD,
            title="Concept Card",
            content="Card content here",
            obsidian_path="/path/to/note.md",
            status=NoteStatus.SYNCED,
            created_at=now,
            updated_at=now
        )
        assert note.content == "Card content here"
        assert note.obsidian_path == "/path/to/note.md"
        assert note.status == NoteStatus.SYNCED

    def test_note_default_timestamps(self):
        """Test that Note has default timestamps"""
        note = Note(id=None, source_id=None, type=NoteType.SOURCE, title="Test")
        assert isinstance(note.created_at, datetime)
        assert isinstance(note.updated_at, datetime)
