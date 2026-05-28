#!/usr/bin/env bash
# Append a changelog entry for a planning session.
# Add session hash + summary + relative plan link to docs/en/change-log/0.0.0.md. sddsa89612jk4hbwas678
#
# Usage:
#   bash .codex/skills/planning-with-files/scripts/append-changelog.sh "<session-hash>" "<one-line-summary>"
#   printf '%s' "<one-line-summary>" | bash .codex/skills/planning-with-files/scripts/append-changelog.sh "<session-hash>"
#
# Output:
# - Updates docs/en/change-log/0.0.0.md (current version) with a markdown bullet linking to the plan.

set -euo pipefail

SESSION_HASH="${1:-}"
SUMMARY="${2:-}"

if [ -z "${SESSION_HASH}" ]; then
    echo "ERROR: missing session hash"
    echo "Usage:"
    echo "  bash .codex/skills/planning-with-files/scripts/append-changelog.sh \"<session-hash>\" \"<one-line-summary>\""
    echo "  printf '%s' \"<one-line-summary>\" | bash .codex/skills/planning-with-files/scripts/append-changelog.sh \"<session-hash>\""
    exit 1
fi

if [ -z "${SUMMARY}" ]; then
    # Allow reading summary from stdin to avoid shell expansion issues (e.g. backticks in zsh). l290bb7v758opd6uxu6r
    if [ -t 0 ]; then
        echo "ERROR: missing summary"
        echo "Usage:"
        echo "  bash .codex/skills/planning-with-files/scripts/append-changelog.sh \"<session-hash>\" \"<one-line-summary>\""
        echo "  printf '%s' \"<one-line-summary>\" | bash .codex/skills/planning-with-files/scripts/append-changelog.sh \"<session-hash>\""
        exit 1
    fi

    SUMMARY="$(cat)"
fi

if [ -z "${SUMMARY}" ]; then
    echo "ERROR: missing summary"
    exit 1
fi

normalize_summary() {
    # Normalize changelog summaries to avoid HTML comment/newline injection. l290bb7v758opd6uxu6r
    python3 - "$SESSION_HASH" "$SUMMARY" <<'PY'
import re
import sys

session_hash = sys.argv[1]
summary = sys.argv[2]

summary = summary.replace("\r", " ").replace("\n", " ").strip()

# If the whole summary is wrapped as an HTML comment, unwrap it (keep the inner text).
m = re.fullmatch(r"<!--\s*(.*?)\s*-->", summary, flags=re.DOTALL)
if m:
    summary = m.group(1).strip()

# Unwrap MDX comment wrappers so they don't swallow the changelog summary. docs/en/developer/plans/mintmdxcomment20260122/task_plan.md mintmdxcomment20260122
m = re.fullmatch(r"\{\s*/\*\s*(.*?)\s*\*/\s*\}", summary, flags=re.DOTALL)
if m:
    summary = m.group(1).strip()

# Remove a leading markdown bullet prefix so we don't end up with "- - ..." in the changelog file.
if summary.startswith("- "):
    summary = summary[2:].lstrip()

# Drop a trailing session hash token (redundant because we also add the hash as the plan link label).
if session_hash and re.search(rf"(?:\s|^){re.escape(session_hash)}$", summary):
    summary = re.sub(rf"(?:\s+){re.escape(session_hash)}$", "", summary).rstrip()

# Collapse whitespace to enforce single-line output.
summary = re.sub(r"\s+", " ", summary).strip()

print(summary)
PY
}

SUMMARY="$(normalize_summary)"
if [ -z "${SUMMARY}" ]; then
    echo "ERROR: summary is empty after normalization"
    exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CHANGELOG_FILE="${REPO_ROOT}/docs/en/change-log/0.0.0.md"

if [ ! -f "${CHANGELOG_FILE}" ]; then
    echo "ERROR: changelog not found: ${CHANGELOG_FILE}"
    exit 1
fi

# Use Mintlify page routes (no .md extension) for internal doc links. docs/en/developer/plans/mintmdxcomment20260122/task_plan.md mintmdxcomment20260122
PLAN_REL_LINK="../developer/plans/${SESSION_HASH}/task_plan"
ENTRY="- ${SUMMARY} ([${SESSION_HASH}](${PLAN_REL_LINK}))"

if rg -n --fixed-strings "${SESSION_HASH}" "${CHANGELOG_FILE}" >/dev/null 2>&1; then
    echo "Changelog already contains session hash: ${SESSION_HASH}"
    exit 0
fi

if ! rg -n --fixed-strings "## Changes" "${CHANGELOG_FILE}" >/dev/null 2>&1; then
    printf "\n## Changes\n" >> "${CHANGELOG_FILE}"
fi

printf "\n%s\n" "${ENTRY}" >> "${CHANGELOG_FILE}"
echo "Appended changelog entry to: ${CHANGELOG_FILE}"
