#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path


def _repo_root_from_here() -> Path:
    # .../.codex/skills/scribe-mcp-usage/scripts/sync_from_repo.py
    return Path(__file__).resolve().parents[4]


def _skill_root_from_here() -> Path:
    # .../.codex/skills/scribe-mcp-usage/scripts/sync_from_repo.py
    return Path(__file__).resolve().parents[1]


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _extract_section(src_lines: list[str], heading: str) -> str | None:
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync scribe-mcp-usage skill resources from this repo.")
    parser.add_argument("--repo-root", default=None, help="Override repo root (defaults to auto-detect).")
    parser.add_argument("--skill-root", default=None, help="Override skill root (defaults to auto-detect).")
    parser.add_argument(
        "--no-templates",
        action="store_true",
        help="Skip copying templates into assets/templates.",
    )
    parser.add_argument(
        "--no-usage",
        action="store_true",
        help="Skip copying docs/Scribe_Usage.md into references/Scribe_Usage.md.",
    )
    parser.add_argument(
        "--no-splits",
        action="store_true",
        help="Skip generating extracted reference docs from references/Scribe_Usage.md.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else _repo_root_from_here()
    skill_root = Path(args.skill_root).expanduser().resolve() if args.skill_root else _skill_root_from_here()

    docs_src = repo_root / "docs" / "Scribe_Usage.md"
    usage_upstream_dest = skill_root / "references" / "Scribe_Usage.upstream.md"
    usage_dest = skill_root / "references" / "Scribe_Usage.md"

    if not args.no_usage:
        if not docs_src.exists():
            raise SystemExit(f"Missing {docs_src}")
        usage_upstream_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(docs_src, usage_upstream_dest)
        print(
            f"copied: {docs_src.relative_to(repo_root)} -> {usage_upstream_dest.relative_to(skill_root)}"
        )

        src_hash = hashlib.sha256(docs_src.read_bytes()).hexdigest()
        upstream_hash = hashlib.sha256(usage_upstream_dest.read_bytes()).hexdigest()
        if src_hash != upstream_hash:
            raise SystemExit(
                "hash mismatch after copy (docs/Scribe_Usage.md -> references/Scribe_Usage.upstream.md)"
            )
        print(f"verified: references/Scribe_Usage.upstream.md sha256={upstream_hash[:16]}…")

        # Build a skill-local copy that doesn't point outside the skill package.
        upstream_text = usage_upstream_dest.read_text(encoding="utf-8")
        patched = upstream_text.replace("docs/Scribe_Usage.md", "references/Scribe_Usage.md")
        patched = patched.replace("docs/scribe_usage.md", "references/Scribe_Usage.md")
        header = (
            "<!--\n"
            f"source: docs/Scribe_Usage.md\n"
            f"source_sha256: {upstream_hash}\n"
            "note: This copy is patched for skill-local paths.\n"
            "-->\n\n"
        )
        usage_dest.write_text(header + patched, encoding="utf-8")
        skill_hash = hashlib.sha256(usage_dest.read_bytes()).hexdigest()
        print(f"generated: references/Scribe_Usage.md sha256={skill_hash[:16]}…")

    if not args.no_templates:
        templates_src = repo_root / "templates" / "documents"
        templates_dest = skill_root / "assets" / "templates"
        templates_dest.mkdir(parents=True, exist_ok=True)
        copied = 0
        for path in sorted(templates_src.glob("*.md")):
            shutil.copy2(path, templates_dest / path.name)
            copied += 1
        print(f"copied: {copied} templates -> assets/templates/")

    if not args.no_splits:
        if not usage_dest.exists():
            raise SystemExit(f"Missing {usage_dest} (run without --no-usage or provide an existing copy).")
        lines = usage_dest.read_text(encoding="utf-8").splitlines()
        for tool in ("manage_docs", "read_file"):
            section = _extract_section(lines, f"### `{tool}`")
            if section is None:
                raise SystemExit(f"missing section in references/Scribe_Usage.md: ### `{tool}`")
            out = skill_root / "references" / f"{tool}.md"
            _write_text(out, f"# {tool.replace('_', ' ').title()}\n\n{section}\n")
            print(f"generated: {out.relative_to(skill_root)}")

        build_script = skill_root / "scripts" / "build_references.py"
        if build_script.exists():
            import subprocess

            result = subprocess.run(
                ["python", str(build_script)],
                cwd=str(skill_root),
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                combined = "\n".join(
                    part
                    for part in [
                        (result.stdout or "").strip(),
                        (result.stderr or "").strip(),
                    ]
                    if part
                ).strip()
                raise SystemExit(combined or "build_references.py failed")
            stdout = (result.stdout or "").strip()
            if stdout:
                print(stdout)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
