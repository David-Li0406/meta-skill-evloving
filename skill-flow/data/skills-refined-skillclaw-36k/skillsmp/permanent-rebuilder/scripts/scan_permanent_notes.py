"""Scan an Obsidian vault's permanent folder and generate a Markdown report.

Non-destructive: reads Markdown files and reports frontmatter/summary/status presence plus
rough hub/leaf suggestions.

Default output: .tmp/copilot/permanent-scan.md
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


FRONTMATTER_DELIM = "---"


@dataclass(frozen=True)
class Frontmatter:
    text: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_lines(text: str) -> list[str]:
    return re.split(r"\r?\n", text)


def parse_frontmatter(lines: list[str]) -> Frontmatter | None:
    if len(lines) < 3:
        return None
    if lines[0].strip() != FRONTMATTER_DELIM:
        return None
    end_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            end_index = i
            break
    if end_index < 0:
        return None
    return Frontmatter(text="\n".join(lines[1:end_index]))


def count_headings(text: str) -> int:
    return len(re.findall(r"(?m)^#{1,6}\s+", text))


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def has_summary(frontmatter_text: str) -> bool:
    return re.search(r"(?m)^summary:\s*", frontmatter_text) is not None


def get_status(frontmatter_text: str) -> str:
    m = re.search(r"(?m)^status:\s*([A-Za-z0-9_-]+)\s*$", frontmatter_text)
    return m.group(1) if m else ""


def suggest_kind_folder(word_count: int, heading_count: int) -> str:
    if word_count >= 1500 or heading_count >= 12:
        return "hub"
    return "leaf"


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
        default=str(Path(".tmp/copilot/permanent-scan.md")),
        help="Output report path",
    )

    args = parser.parse_args()
    vault_root = Path(args.vault_root).expanduser().resolve()
    permanent_path = (vault_root / args.permanent_folder).resolve()
    out_path = Path(args.out).expanduser()

    if not permanent_path.exists():
        raise SystemExit(f"Permanent folder not found: {permanent_path}")

    files = [p for p in permanent_path.rglob("*.md") if ".obsidian" not in p.parts]

    rows: list[dict[str, object]] = []
    for f in files:
        content = read_text(f)
        lines = split_lines(content)
        fm = parse_frontmatter(lines)

        has_fm = fm is not None
        fm_text = fm.text if fm else ""

        summary_ok = has_summary(fm_text) if has_fm else False
        status = get_status(fm_text) if has_fm else ""

        headings = count_headings(content)
        words = count_words(content)
        suggest = suggest_kind_folder(words, headings)

        flags: list[str] = []
        if not has_fm:
            flags.append("no-frontmatter")
        if has_fm and not summary_ok:
            flags.append("no-summary")
        if not status:
            flags.append("no-status")

        rel_path = f.relative_to(vault_root).as_posix()
        rows.append(
            {
                "path": rel_path,
                "words": words,
                "headings": headings,
                "suggest": suggest,
                "flags": ",".join(flags),
                "has_frontmatter": has_fm,
                "has_summary": summary_ok,
                "status": status,
            }
        )

    hub_count = sum(1 for r in rows if r["suggest"] == "hub")
    leaf_count = sum(1 for r in rows if r["suggest"] == "leaf")
    missing_summary_count = sum(1 for r in rows if r["has_frontmatter"] and not r["has_summary"])
    missing_frontmatter_count = sum(1 for r in rows if not r["has_frontmatter"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    md: list[str] = []
    md.append("# permanent scan report")
    md.append("")
    md.append(f"- generated: {now}")
    md.append(f"- vaultRoot: {vault_root}")
    md.append(f"- permanentFolder: {args.permanent_folder}")
    md.append(f"- totalFiles: {len(rows)}")
    md.append(f"- hubSuggested: {hub_count}")
    md.append(f"- leafSuggested: {leaf_count}")
    md.append(f"- missingSummary: {missing_summary_count}")
    md.append(f"- missingFrontmatter: {missing_frontmatter_count}")
    md.append("")

    md.append("## Files (summary)")
    md.append("")
    md.append("| path | words | headings | suggest | flags |")
    md.append("|---|---:|---:|---|---|")

    for r in sorted(rows, key=lambda x: int(x["words"]), reverse=True):
        md.append(
            f"| {r['path']} | {r['words']} | {r['headings']} | {r['suggest']} | {r['flags']} |"
        )

    md.append("")
    md.append("## Next actions (recommended order)")
    md.append("")
    md.append("1. Add frontmatter to files with no frontmatter.")
    md.append("2. Add `summary` to all permanent notes.")
    md.append("3. Normalize `status` and role-based tags (d/t/k/s).")
    md.append("4. Move notes into 00_inbox/10_hub/20_leaf after you have a plan.")

    ensure_parent_dir(out_path)
    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
