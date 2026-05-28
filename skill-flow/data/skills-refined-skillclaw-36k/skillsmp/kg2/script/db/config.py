"""Config operations for the database."""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import sqlite3

from ..models import Config


def save_config(conn: sqlite3.Connection, key: str, value: Any) -> None:
    """Save config value."""
    conn.execute(
        "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
        (key, json.dumps(value))
    )


def get_config(conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
    """Get config value."""
    row = conn.execute(
        "SELECT value FROM config WHERE key = ?", (key,)
    ).fetchone()
    if not row:
        return default
    value = row['value']
    if isinstance(value, str):
        return json.loads(value)
    return value


def load_config(conn: sqlite3.Connection) -> Config | None:
    """Load full config. Returns None if not initialized."""
    seed_ids = get_config(conn, 'seed_ids')
    if seed_ids is None:
        return None
    return Config(
        seed_ids=seed_ids,
        max_papers=get_config(conn, 'max_papers', 2000),
    )


def save_full_config(conn: sqlite3.Connection, config: Config) -> None:
    """Save full config."""
    for key, value in config.to_dict().items():
        save_config(conn, key, value)
    save_config(conn, 'created_at', datetime.now().isoformat())
