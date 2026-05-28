"""Data models for Deep Reading"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SourceType(Enum):
    YOUTUBE = "youtube"
    PODCAST = "podcast"
    WEB = "web"
    PDF = "pdf"

class ProcessingState(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    READY = "ready"
    REVIEWED = "reviewed"
    ERROR = "error"

class ChapterType(Enum):
    INTRO = "intro"
    CORE = "core"
    SKIP = "skip"
    OUTRO = "outro"

class MarkType(Enum):
    HIGHLIGHT = "highlight"
    QUESTION = "question"
    NOTE = "note"

class NoteType(Enum):
    SOURCE = "source"
    CARD = "card"

class NoteStatus(Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    SYNCED = "synced"

@dataclass
class Source:
    id: str
    type: SourceType
    url: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[int] = None  # seconds
    cache_path: Optional[str] = None
    processing_state: ProcessingState = ProcessingState.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Chapter:
    id: Optional[int]
    source_id: str
    start_time: int  # seconds
    end_time: int    # seconds
    title: str
    type: ChapterType = ChapterType.CORE

@dataclass
class Mark:
    id: Optional[int]
    source_id: str
    timestamp: int  # seconds
    type: MarkType
    content: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Note:
    id: Optional[int]
    source_id: Optional[str]
    type: NoteType
    title: str
    content: Optional[str] = None
    obsidian_path: Optional[str] = None
    status: NoteStatus = NoteStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
