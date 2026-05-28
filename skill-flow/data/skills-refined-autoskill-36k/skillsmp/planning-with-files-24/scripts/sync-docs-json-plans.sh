#!/usr/bin/env bash
# Sync docs/docs.json navigation entries for planning session files. docsjsonindex20260121
#
# Usage:
#   bash .codex/skills/planning-with-files/scripts/sync-docs-json-plans.sh
#
# Behavior:
# - Scans: docs/en/developer/plans/<session-hash>/{task_plan,findings,progress}.md
# - Updates: docs/docs.json -> Developer Docs -> group "plans" -> pages[]
# - Skips missing files to avoid broken navigation links.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
DOCS_JSON="${REPO_ROOT}/docs/docs.json"
PLANS_DIR="${REPO_ROOT}/docs/en/developer/plans"

if [ ! -f "${DOCS_JSON}" ]; then
  echo "docs.json not found: ${DOCS_JSON} (skipping; Docusaurus does not use docs.json). docs/en/developer/plans/dsim8xybp9oa18nz1gfq/task_plan.md dsim8xybp9oa18nz1gfq" >&2
  exit 0
fi

if [ ! -d "${PLANS_DIR}" ]; then
  echo "ERROR: plans directory not found: ${PLANS_DIR}" >&2
  exit 1
fi

python3 - "${DOCS_JSON}" "${PLANS_DIR}" <<'PY'
import json
import sys
from pathlib import Path
from datetime import date

docs_json_path = Path(sys.argv[1])
plans_dir = Path(sys.argv[2])

data = json.loads(docs_json_path.read_text(encoding="utf-8"))

nav = data.get("navigation") or {}
languages = nav.get("languages")
if not isinstance(languages, list) or not languages:
    raise SystemExit("ERROR: docs.json missing navigation.languages[]")

lang = next((l for l in languages if isinstance(l, dict) and l.get("language") == "en"), None)
if lang is None:
    lang = next((l for l in languages if isinstance(l, dict) and l.get("default") is True), None) or languages[0]

tabs = lang.get("tabs")
if not isinstance(tabs, list):
    raise SystemExit("ERROR: docs.json missing navigation.languages[].tabs[]")

dev_tab = next((t for t in tabs if isinstance(t, dict) and t.get("tab") == "Developer Docs"), None)
if dev_tab is None:
    dev_tab = {"tab": "Developer Docs", "groups": []}
    tabs.append(dev_tab)

groups = dev_tab.get("groups")
if not isinstance(groups, list):
    dev_tab["groups"] = []
    groups = dev_tab["groups"]

plans_group = next(
    (
        g
        for g in groups
        if isinstance(g, dict) and isinstance(g.get("group"), str) and g.get("group").lower() == "plans"
    ),
    None,
)
if plans_group is None:
    plans_group = {"group": "Plans", "pages": []}
    groups.append(plans_group)
else:
    # Normalize group label to improve sidebar display. docs/en/developer/plans/mintmdxcomment20260122/task_plan.md mintmdxcomment20260122
    plans_group["group"] = "Plans"

expected_stems = ["task_plan", "findings", "progress"]

def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_first_heading(md: str) -> str | None:
    lines = md.splitlines()

    i = 0
    # Skip YAML frontmatter if present.
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("# "):
            return line[2:].strip()
        i += 1
    return None


def _extract_created_date(md: str) -> date | None:
    for raw_line in md.splitlines():
        line = raw_line.strip()
        if not line.startswith("- **Created:**"):
            continue
        # Example: "- **Created:** 2026-01-17"
        value = line.split(":", 2)[-1].strip()
        try:
            return date.fromisoformat(value)
        except Exception:
            return None
    return None


def _extract_session_title_from_task_plan(md: str) -> str | None:
    heading = _extract_first_heading(md)
    if not heading:
        return None
    # Common patterns:
    # - "Task Plan: <title>"
    # - "Task Plan: <title> (something)"
    if ":" in heading:
        prefix, rest = heading.split(":", 1)
        if prefix.strip().lower() == "task plan":
            return rest.strip()
    return heading.strip()


session_entries: list[tuple[date | None, str, list[str], str]] = []

for session_dir in [p for p in plans_dir.iterdir() if p.is_dir()]:
    session = session_dir.name
    session_pages: list[str] = []
    found_any = False

    for stem in expected_stems:
        md_path = session_dir / f"{stem}.md"
        if not md_path.exists():
            continue
        found_any = True
        session_pages.append(f"en/developer/plans/{session}/{stem}")

    if not found_any:
        continue

    missing = [stem for stem in expected_stems if not (session_dir / f"{stem}.md").exists()]
    if missing:
        sys.stderr.write(
            f"WARNING: session '{session}' is missing files: {', '.join(missing)} (skipping missing pages)\n"
        )

    task_plan_path = session_dir / "task_plan.md"
    task_plan_text = _read_text(task_plan_path) if task_plan_path.exists() else ""
    created = _extract_created_date(task_plan_text)
    session_title = _extract_session_title_from_task_plan(task_plan_text) or session

    # Group the 3 plan files under a single session label so the sidebar doesn't show repeated
    # "Task plan / Findings / Progress" entries without context. docs/en/developer/plans/mintmdxcomment20260122/task_plan.md mintmdxcomment20260122
    group_label = f"{session_title} ({session})"
    session_entries.append((created, session, session_pages, group_label))


def _sort_key(entry: tuple[date | None, str, list[str], str]):
    created_date, session_hash, _, _ = entry
    # Newest first; unknown dates last; tie-break by session hash.
    return (
        created_date is not None,
        created_date or date.min,
        session_hash,
    )


pages: list[object] = []
total_page_count = 0
for created, session, session_pages, group_label in sorted(session_entries, key=_sort_key, reverse=True):
    pages.append({"group": group_label, "pages": session_pages, "expanded": False})
    total_page_count += len(session_pages)

plans_group["pages"] = pages

docs_json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Synced {total_page_count} plan pages into: {docs_json_path}")
PY
