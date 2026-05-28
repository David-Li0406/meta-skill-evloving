"""
User Preferences - Storage for user-pinned skills in layering strategy.

Pinned skills are permanently kept in the active set, regardless of
their install count ranking.
"""

import json
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger

from config import PROJECT_ROOT


# Default storage path for user preferences
DEFAULT_PREFS_PATH = PROJECT_ROOT / "data" / "user_preferences.json"


@dataclass
class UserPreferences:
    """User preferences for skill layering."""
    version: int = 1
    pinned_skill_ids: list[str] = field(default_factory=list)
    updated_at: str = ""

    def pin_skill(self, skill_id: str) -> bool:
        """Pin a skill (add to permanent active set).

        Returns:
            True if skill was newly pinned, False if already pinned.
        """
        if skill_id in self.pinned_skill_ids:
            return False
        self.pinned_skill_ids.append(skill_id)
        self.updated_at = datetime.now().isoformat()
        return True

    def unpin_skill(self, skill_id: str) -> bool:
        """Unpin a skill (remove from permanent active set).

        Returns:
            True if skill was unpinned, False if not found.
        """
        if skill_id not in self.pinned_skill_ids:
            return False
        self.pinned_skill_ids.remove(skill_id)
        self.updated_at = datetime.now().isoformat()
        return True

    def is_pinned(self, skill_id: str) -> bool:
        """Check if a skill is pinned."""
        return skill_id in self.pinned_skill_ids

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def load_user_prefs(prefs_path: Optional[Path] = None) -> UserPreferences:
    """Load user preferences from JSON file.

    Args:
        prefs_path: Path to preferences file. Defaults to data/user_preferences.json.

    Returns:
        UserPreferences instance. Returns empty prefs if file doesn't exist.
    """
    path = prefs_path or DEFAULT_PREFS_PATH

    if not path.exists():
        return UserPreferences()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return UserPreferences(
            version=data.get("version", 1),
            pinned_skill_ids=data.get("pinned_skill_ids", []),
            updated_at=data.get("updated_at", ""),
        )
    except (json.JSONDecodeError, IOError) as e:
        # Return empty prefs on error, don't crash
        logger.warning(f"Failed to load user preferences: {e}")
        return UserPreferences()


def save_user_prefs(prefs: UserPreferences, prefs_path: Optional[Path] = None) -> None:
    """Save user preferences to JSON file atomically.

    Args:
        prefs: UserPreferences instance to save.
        prefs_path: Path to preferences file. Defaults to data/user_preferences.json.
    """
    path = prefs_path or DEFAULT_PREFS_PATH

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    prefs.updated_at = datetime.now().isoformat()

    # Atomic write: temp file + rename
    temp_path = path.with_suffix(".json.tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(prefs.to_dict(), f, indent=2, ensure_ascii=False)
    temp_path.replace(path)


class UserPrefsManager:
    """Manager class for user preferences with lazy loading, auto-save, and thread safety."""

    def __init__(self, prefs_path: Optional[Path] = None):
        self.prefs_path = prefs_path or DEFAULT_PREFS_PATH
        self._prefs: Optional[UserPreferences] = None
        self._lock = threading.Lock()

    @property
    def prefs(self) -> UserPreferences:
        """Lazy load preferences."""
        if self._prefs is None:
            self._prefs = load_user_prefs(self.prefs_path)
        return self._prefs

    def pin_skill(self, skill_id: str) -> bool:
        """Pin a skill and save preferences (thread-safe)."""
        with self._lock:
            result = self.prefs.pin_skill(skill_id)
            if result:
                save_user_prefs(self.prefs, self.prefs_path)
            return result

    def unpin_skill(self, skill_id: str) -> bool:
        """Unpin a skill and save preferences (thread-safe)."""
        with self._lock:
            result = self.prefs.unpin_skill(skill_id)
            if result:
                save_user_prefs(self.prefs, self.prefs_path)
            return result

    def is_pinned(self, skill_id: str) -> bool:
        """Check if a skill is pinned."""
        with self._lock:
            return self.prefs.is_pinned(skill_id)

    def get_pinned_ids(self) -> list[str]:
        """Get list of all pinned skill IDs."""
        with self._lock:
            return list(self.prefs.pinned_skill_ids)

    def reload(self) -> None:
        """Force reload preferences from disk."""
        with self._lock:
            self._prefs = load_user_prefs(self.prefs_path)
