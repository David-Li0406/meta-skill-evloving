#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "sqlite-vec",
#     "sentence-transformers",
# ]
# ///
"""
amnesia - save.py
Save and query conversation memories with semantic search.

Commands:
    save.py save --id SESSION_ID --title "Title" [--tags "a,b"] [--summary-file FILE]
    save.py query "search terms" [--limit N] [--full]
    save.py init
"""

import sys
import os
import json
import sqlite3
import argparse
import subprocess
import tempfile

# Lazy load heavy imports
_model = None

SUM_PROMPT_PREFIX = "You are tasked with summarizing the current conversation"


def get_current_session() -> dict:
    """Get the current session info from opencode."""
    result = subprocess.run(
        ["opencode", "session", "list", "--format", "json", "-n", "1"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get session list: {result.stderr}")

    try:
        sessions = json.loads(result.stdout)
        if not sessions:
            raise RuntimeError("No sessions found")
        return sessions[0]
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        raise RuntimeError(f"Failed to parse session list: {e}")


def get_model():
    """Lazy load the embedding model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-mpnet-base-v2")
    return _model


def get_db_path():
    return os.environ.get("AMNESIA_DB", os.path.expanduser("~/amnesia/memories.db"))


def get_connection(db_path: str):
    """Get a connection with sqlite-vec loaded."""
    import sqlite_vec

    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def get_embedding(text: str) -> list[float]:
    """Generate embedding for text."""
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def init_db(db_path: str):
    """Initialize the database and vector table."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = get_connection(db_path)

    # Create memories table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            full_content TEXT,
            tags TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at)"
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories(tags)")

    # Create vector table (768 dimensions for all-mpnet-base-v2)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_vec USING vec0(
            id TEXT PRIMARY KEY,
            embedding FLOAT[768]
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized: {db_path}")


def export_session(session_id: str) -> str:
    """Export session from opencode and extract conversation text."""
    # Export directly to temp file (avoids pipe buffering and encoding issues)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name

    try:
        with open(temp_path, "w") as f:
            result = subprocess.run(
                ["opencode", "export", session_id],
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
            )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to export session: {result.stderr}")

        # Parse and process
        with open(temp_path, "r") as f:
            data = json.load(f)

        messages = data.get("messages", [])
        if not messages:
            raise RuntimeError("Session has no messages")

        # Filter out /sum prompt and response if present at the end
        def get_text(msg):
            parts = msg.get("parts", [])
            return "".join(p.get("text", "") for p in parts if p.get("type") == "text")

        # Check last message
        if messages and get_text(messages[-1]).startswith(SUM_PROMPT_PREFIX):
            messages = messages[:-1]
        # Check second-to-last message
        elif len(messages) >= 2 and get_text(messages[-2]).startswith(
            SUM_PROMPT_PREFIX
        ):
            messages = messages[:-2]

        # Format as USER:/ASSISTANT: pairs
        lines = []
        for msg in messages:
            role = msg.get("info", {}).get("role", "unknown").upper()
            text = get_text(msg)
            lines.append(f"{role}: {text}")

        return "\n".join(lines)

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def save_memory(
    db_path: str,
    memory_id: str,
    title: str,
    content: str,
    full_content: str = "",
    tags: str = "",
):
    """Save a memory to the database."""
    conn = get_connection(db_path)

    conn.execute(
        """
        INSERT INTO memories (id, title, content, full_content, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            content = excluded.content,
            full_content = excluded.full_content,
            tags = excluded.tags,
            updated_at = datetime('now')
        """,
        (memory_id, title, content, full_content, tags),
    )
    conn.commit()

    # Save embedding for semantic search
    embed_text = f"{title}. {content}"
    embedding = get_embedding(embed_text)

    conn.execute("DELETE FROM memories_vec WHERE id = ?", (memory_id,))
    conn.execute(
        "INSERT INTO memories_vec (id, embedding) VALUES (?, ?)",
        (memory_id, json.dumps(embedding)),
    )
    conn.commit()
    conn.close()

    print(f"Memory saved: {memory_id}")


def query_memories(db_path: str, query: str, limit: int = 5, show_full: bool = False):
    """Search memories using vector similarity."""
    import math

    query_embedding = get_embedding(query)
    conn = get_connection(db_path)

    results = conn.execute(
        """
        SELECT 
            v.id,
            v.distance,
            m.title,
            m.content,
            m.full_content,
            m.tags,
            m.created_at
        FROM memories_vec v
        JOIN memories m ON v.id = m.id
        WHERE v.embedding MATCH ? AND k = ?
        ORDER BY v.distance
        """,
        (json.dumps(query_embedding), limit),
    ).fetchall()

    conn.close()

    print(f"Semantic search for: {query}\n")

    for i, (id, distance, title, content, full_content, tags, created_at) in enumerate(
        results, 1
    ):
        similarity = math.exp(-distance) * 100

        print(f"--- Result {i} (score: {similarity:.1f}) ---")
        print(f"ID: {id}")
        print(f"Title: {title}")
        print(f"Tags: {tags or '(none)'}")
        print(f"Date: {created_at}")

        if show_full and full_content:
            print(f"\n## Summary:\n{content}")
            print(f"\n## Full Conversation:\n{full_content}")
        else:
            preview = content[:200] + "..." if len(content) > 200 else content
            print(f"Preview: {preview}")
        print()

    print(f"Found {len(results)} results")


def main():
    parser = argparse.ArgumentParser(
        description="Save and query conversation memories with semantic search"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # save command
    save_parser = subparsers.add_parser("save", help="Save a memory")
    save_parser.add_argument("--id", help="Session ID (auto-detected if not provided)")
    save_parser.add_argument(
        "--title", "-t", help="Memory title (uses session title if not provided)"
    )
    save_parser.add_argument("--tags", default="", help="Comma-separated tags")
    save_parser.add_argument(
        "--summary-file", help="Read summary from file instead of stdin"
    )
    save_parser.add_argument(
        "--init", action="store_true", help="Initialize database if needed"
    )

    # query command
    query_parser = subparsers.add_parser("query", help="Search memories")
    query_parser.add_argument("search", help="Search query")
    query_parser.add_argument(
        "--limit", "-n", type=int, default=5, help="Number of results"
    )
    query_parser.add_argument(
        "--full", "-f", action="store_true", help="Show full content"
    )
    query_parser.add_argument(
        "--init", action="store_true", help="Initialize database if needed"
    )

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize the database")

    args = parser.parse_args()
    db_path = get_db_path()

    if args.command == "init":
        init_db(db_path)

    elif args.command == "save":
        # Check/init database
        if not os.path.exists(db_path):
            if args.init:
                init_db(db_path)
            else:
                print(f"Error: Database not found: {db_path}", file=sys.stderr)
                print("Run 'save.py init' to create it", file=sys.stderr)
                sys.exit(1)

        # Get session info (auto-detect if not provided)
        session_id = args.id
        title = args.title
        if not session_id or not title:
            try:
                session = get_current_session()
                if not session_id:
                    session_id = session["id"]
                if not title:
                    title = session.get("title", "Untitled Session")
            except Exception as e:
                print(f"Error: Failed to get session info: {e}", file=sys.stderr)
                sys.exit(1)

        # Read summary
        if args.summary_file:
            with open(args.summary_file, "r") as f:
                content = f.read().strip()
        else:
            content = sys.stdin.read().strip()

        if not content:
            print("Error: No summary provided", file=sys.stderr)
            sys.exit(1)

        # Export session
        try:
            full_content = export_session(session_id)
        except Exception as e:
            print(f"Error exporting session: {e}", file=sys.stderr)
            sys.exit(1)

        save_memory(db_path, session_id, title, content, full_content, args.tags)

    elif args.command == "query":
        if not os.path.exists(db_path):
            if args.init:
                init_db(db_path)
                print("No memories saved yet.\n")
                return
            else:
                print(f"Error: Database not found: {db_path}", file=sys.stderr)
                sys.exit(1)

        query_memories(db_path, args.search, args.limit, args.full)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
