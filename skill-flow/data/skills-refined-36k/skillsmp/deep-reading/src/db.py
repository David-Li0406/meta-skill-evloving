"""Database connection and initialization"""
import sqlite3
from pathlib import Path

# Import config
import sys
sys.path.insert(0, str(Path.home() / ".deep-reading"))
from config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schema"""
    conn = get_connection()
    conn.executescript("""
        -- Content sources
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            url TEXT,
            title TEXT,
            author TEXT,
            duration INTEGER,
            cache_path TEXT,
            processing_state TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Chapters (semantic segments)
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL,
            start_time INTEGER NOT NULL,
            end_time INTEGER NOT NULL,
            title TEXT,
            type TEXT DEFAULT 'core',
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );

        -- User marks during playback
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            type TEXT NOT NULL,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );

        -- Generated notes
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            obsidian_path TEXT,
            status TEXT DEFAULT 'draft',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );

        -- Note links
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_note_id INTEGER NOT NULL,
            to_note_id INTEGER NOT NULL,
            type TEXT DEFAULT 'auto',
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (from_note_id) REFERENCES notes(id),
            FOREIGN KEY (to_note_id) REFERENCES notes(id)
        );

        -- Indexes
        CREATE INDEX IF NOT EXISTS idx_sources_state ON sources(processing_state);
        CREATE INDEX IF NOT EXISTS idx_chapters_source ON chapters(source_id);
        CREATE INDEX IF NOT EXISTS idx_marks_source ON marks(source_id);
        CREATE INDEX IF NOT EXISTS idx_notes_source ON notes(source_id);
        CREATE INDEX IF NOT EXISTS idx_notes_status ON notes(status);
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
