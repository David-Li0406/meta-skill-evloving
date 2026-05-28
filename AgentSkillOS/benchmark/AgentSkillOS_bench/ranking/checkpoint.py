"""Checkpoint store for persisting pairwise comparison results.

Each comparison result is saved as an individual JSON file, enabling
incremental evaluation — if a run is interrupted, already-completed
comparisons are automatically reused on the next invocation.
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional


class CheckpointStore:
    """File-backed checkpoint store using one JSON file per comparison unit."""

    def __init__(self, checkpoint_dir: Path) -> None:
        self.dir = Path(checkpoint_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Key helpers
    # ------------------------------------------------------------------

    @staticmethod
    def make_rank_key(
        label_i: str, label_j: str, task_id: str, direction: str,
    ) -> str:
        """Build a canonical checkpoint key for rank.py comparisons.

        Labels are sorted alphabetically so that the key is the same
        regardless of argument order.  When labels are swapped the
        direction is flipped accordingly (fwd <-> rev).
        """
        if label_i <= label_j:
            return f"{label_i}_vs_{label_j}___{task_id}___{direction}"
        else:
            flipped = "rev" if direction == "fwd" else "fwd"
            return f"{label_j}_vs_{label_i}___{task_id}___{flipped}"

    @staticmethod
    def make_compare_key(
        run_a_name: str, run_b_name: str, task_id: str, ordering: str,
        output_name: str = "",
    ) -> str:
        """Build a checkpoint key for compare.py comparisons.

        ``ordering`` should be ``"ab"`` or ``"ba"``.
        ``output_name`` is the output filename so that different
        ``--output`` targets use separate caches.
        """
        base = f"{run_a_name}_vs_{run_b_name}___{task_id}___{ordering}"
        if output_name:
            return f"{base}___{output_name}"
        return base

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _path_for(self, key: str) -> Path:
        # Sanitise the key so it is safe as a filename (replace path-
        # separator characters with underscores).
        safe = key.replace("/", "_").replace("\\", "_")
        return self.dir / f"{safe}.json"

    def has(self, key: str) -> bool:
        return self._path_for(key).exists()

    def load(self, key: str) -> Optional[dict]:
        path = self._path_for(key)
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # Corrupted file — treat as missing so the unit is re-run.
            return None

    def save(self, key: str, data: dict) -> None:
        """Atomically persist *data* for the given *key*.

        Writes to a temporary file in the same directory then renames,
        so a crash mid-write can never leave a half-written checkpoint.
        """
        dest = self._path_for(key)
        payload = {**data, "_checkpoint_key": key, "timestamp": datetime.now().isoformat()}

        # Write to a temp file in the same directory, then atomic rename.
        fd, tmp_path = tempfile.mkstemp(
            suffix=".tmp", dir=str(self.dir),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, str(dest))
        except BaseException:
            # Clean up the temp file on failure.
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
