"""Build a restructure plan (JSON) for permanent reorganization.

Non-destructive: suggests destination folders (10_hub / 20_leaf) based on simple heuristics
and flags notes needing frontmatter/summary/status.

Default output: .tmp/copilot/permanent-plan.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


FRONTMATTER_DELIM = "---"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_lines(text: str) -> list[str]:
    return re.split(r"\r?\n", text)


def frontmatter_text(lines: list[str]) -> str | None:
    if len(lines) < 3:
        return None
    if lines[0].strip() != FRONTMATTER_DELIM:
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            return "\n".join(lines[1:i])
    return None


def count_headings(text: str) -> int:
    return len(re.findall(r"(?m)^#{1,6}\s+", text))


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def has_key(fm_text: str, key: str) -> bool:
    return re.search(rf"(?m)^{re.escape(key)}:\s*", fm_text) is not None


def suggest_folder(words: int, headings: int) -> tuple[str, str]:
    if words >= 1500 or headings >= 12:
        return "10_hub", "hub"
    return "20_leaf", "leaf"


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault-root", default=str(Path.cwd()), help="Vault root directory")
    parser.add_argument(
        "--permanent-folder",
        default="permanent",
        help="Permanent notes folder (relative to vault root)",
    )
    parser.add_argument(
        "--out",
        default=str(Path(".tmp/copilot/permanent-plan.json")),
        help="Output plan path (JSON)",
    )

    args = parser.parse_args()
    vault_root = Path(args.vault_root).expanduser().resolve()
    permanent_folder = args.permanent_folder
    permanent_path = (vault_root / permanent_folder).resolve()
    out_path = Path(args.out).expanduser()

    if not permanent_path.exists():
        raise SystemExit(f"Permanent folder not found: {permanent_path}")

    files = [p for p in permanent_path.rglob("*.md") if ".obsidian" not in p.parts]

    notes: list[dict[str, object]] = []

    for f in files:
        content = read_text(f)
        lines = split_lines(content)
        fm = frontmatter_text(lines)

        headings = count_headings(content)
        words = count_words(content)

        kind_folder, classification = suggest_folder(words, headings)

        needs: list[str] = []
        if fm is None:
            needs.append("add-frontmatter")
        else:
            if not has_key(fm, "summary"):
                needs.append("add-summary")
            if not has_key(fm, "status"):
                needs.append("add-status")

        source_rel = f.relative_to(vault_root).as_posix()
        destination_rel = (Path(permanent_folder) / kind_folder / f.name).as_posix()

        notes.append(
            {
                "source": source_rel,
                "destination": destination_rel,
                "suggest": {"kindFolder": kind_folder, "classification": classification},
                "metrics": {"words": words, "headings": headings},
                "needs": needs,
            }
        )

    plan: dict[str, object] = {
        "version": 1,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "vaultRoot": str(vault_root),
        "permanentFolder": permanent_folder,
        "notes": notes,
        "rules": [
            "Default to non-destructive planning and dry-runs",
            "Move first, then normalize metadata, then update MOCs",
            "Avoid renaming until after moves",
            "Require summary in every permanent note",
        ],
    }

    ensure_parent_dir(out_path)
    out_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote plan: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
