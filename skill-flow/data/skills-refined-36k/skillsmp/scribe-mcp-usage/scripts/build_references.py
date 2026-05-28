#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


def _extract_tool_section(src_lines: list[str], tool_name: str) -> str | None:
    heading = f"### `{tool_name}`"
    start = None
    for i, line in enumerate(src_lines):
        if line.strip() == heading:
            start = i
            break
    if start is None:
        return None

    end = len(src_lines)
    for i in range(start + 1, len(src_lines)):
        if src_lines[i].startswith("### `"):
            end = i
            break
    return "\n".join(src_lines[start:end]).rstrip() + "\n"


def _extract_skill_ref_section(src_lines: list[str], ref_name: str) -> str | None:
    heading = f"### Skill Reference: {ref_name}"
    start = None
    for i, line in enumerate(src_lines):
        if line.strip() == heading:
            start = i
            break
    if start is None:
        return None

    end = len(src_lines)
    for i in range(start + 1, len(src_lines)):
        if src_lines[i].startswith("### Skill Reference: "):
            end = i
            break
        if src_lines[i].startswith("## ") and not src_lines[i].startswith("### "):
            end = i
            break
    return "\n".join(src_lines[start:end]).rstrip() + "\n"


def _write_skill_ref(path: Path, title: str, extracted: str) -> None:
    # Replace the leading "### Skill Reference: ..." heading with a file-level H1.
    lines = extracted.splitlines()
    if lines and lines[0].startswith("### Skill Reference: "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    content = "\n".join([f"# {title}", ""] + lines).rstrip() + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _slugify(value: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"`([^`]+)`", r"\\1", slug)
    slug = re.sub(r"[^a-z0-9]+", "_", slug).strip("_")
    return slug or "section"


def _extract_h2_sections(src_lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    start = None
    current_title = None
    for idx, line in enumerate(src_lines):
        if line.startswith("## ") and not line.startswith("### "):
            if start is not None and current_title is not None:
                sections.append((current_title, src_lines[start:idx]))
            current_title = line[3:].strip()
            start = idx
    if start is not None and current_title is not None:
        sections.append((current_title, src_lines[start:]))
    return sections


def _write_section_pack(skill_root: Path, src_lines: list[str]) -> None:
    out_dir = skill_root / "references" / "sections"
    out_dir.mkdir(parents=True, exist_ok=True)

    sections = _extract_h2_sections(src_lines)
    index_lines: list[str] = [
        "# Sections Index (Generated from Scribe_Usage)",
        "",
        "These files are generated from `references/Scribe_Usage.md` (which is generated from `docs/Scribe_Usage.md`).",
        'Use `read_file(mode="search")` on a specific section file when you want a tighter search scope.',
        "",
        "## Sections",
    ]
    seen: dict[str, int] = {}
    for title, body_lines in sections:
        base = _slugify(title)
        seen[base] = seen.get(base, 0) + 1
        slug = base if seen[base] == 1 else f"{base}_{seen[base]}"
        out_path = out_dir / f"{slug}.md"
        section_content = "\n".join(body_lines).rstrip() + "\n"
        out_path.write_text(section_content, encoding="utf-8")
        index_lines.append(f"- `references/sections/{slug}.md` — {title}")

    index_content = "\n".join(index_lines).rstrip() + "\n"
    (out_dir / "INDEX.md").write_text(index_content, encoding="utf-8")
    print(f"built: references/sections/ ({len(sections)} h2 sections)")
    print("built: references/sections/INDEX.md")


def _write(path: Path, title: str, sections: list[tuple[str, str]]) -> None:
    parts: list[str] = [f"# {title}", ""]
    parts.append("## Contents")
    for tool_name, _ in sections:
        parts.append(f"- `{tool_name}`")
    parts.append("")
    for tool_name, body in sections:
        parts.append(body.rstrip())
        parts.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build grouped reference docs from references/Scribe_Usage.md.")
    parser.add_argument(
        "--skill-root",
        default=None,
        help="Path to skill root (defaults to auto-detect from this script location).",
    )
    args = parser.parse_args()

    skill_root = (
        Path(args.skill_root).expanduser().resolve()
        if args.skill_root
        else Path(__file__).resolve().parents[1]
    )
    src_path = skill_root / "references" / "Scribe_Usage.md"
    if not src_path.exists():
        raise SystemExit(f"Missing {src_path}")

    src_lines = src_path.read_text(encoding="utf-8").splitlines()

    # Skill reference sheets extracted from Scribe_Usage (single source of truth).
    skill_refs: list[tuple[str, str, Path]] = [
        ("quickstart", "Scribe MCP Quickstart", skill_root / "references" / "quickstart.md"),
        ("index", "Skill Index (How to Search Fast)", skill_root / "references" / "INDEX.md"),
        ("modes", "Modes: Project vs Sentinel", skill_root / "references" / "modes.md"),
        ("logging", "Logging Discipline", skill_root / "references" / "logging.md"),
        ("doc_naming", "Document Naming and Categories", skill_root / "references" / "doc_naming.md"),
        ("sentinel_cases", "Sentinel Cases (Repo-wide)", skill_root / "references" / "sentinel_cases.md"),
        ("troubleshooting", "Troubleshooting", skill_root / "references" / "troubleshooting.md"),
    ]
    for ref_key, ref_title, out_path in skill_refs:
        extracted = _extract_skill_ref_section(src_lines, ref_key)
        if extracted is None:
            raise SystemExit(f"Missing skill reference section in Scribe_Usage.md: {ref_key}")
        _write_skill_ref(out_path, ref_title, extracted)
        print(f"built: {out_path.relative_to(skill_root)} (skill ref: {ref_key})")

    _write_section_pack(skill_root, src_lines)

    groups: list[tuple[Path, str, list[str]]] = [
        (
            skill_root / "references" / "projects.md",
            "Projects",
            ["set_project", "get_project", "list_projects", "delete_project"],
        ),
        (
            skill_root / "references" / "logging_tool.md",
            "Logging (append_entry)",
            ["append_entry"],
        ),
        (
            skill_root / "references" / "querying.md",
            "Querying Logs",
            ["read_recent", "query_entries"],
        ),
        (
            skill_root / "references" / "files.md",
            "File Reading (read_file)",
            ["read_file"],
        ),
        (
            skill_root / "references" / "docs_management.md",
            "Documentation (manage_docs + templates)",
            ["manage_docs", "generate_doc_templates"],
        ),
        (
            skill_root / "references" / "maintenance.md",
            "Maintenance (rotation + doctor)",
            ["rotate_log", "verify_rotation_integrity", "get_rotation_history", "scribe_doctor"],
        ),
    ]

    missing: list[str] = []
    for path, title, tools in groups:
        sections: list[tuple[str, str]] = []
        for tool in tools:
            extracted = _extract_tool_section(src_lines, tool)
            if extracted is None:
                missing.append(tool)
                continue
            sections.append((tool, extracted))
        _write(path, title, sections)
        print(f"built: {path.relative_to(skill_root)} ({len(sections)} sections)")

    if missing:
        print("WARN: missing tool sections:", ", ".join(sorted(set(missing))))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
