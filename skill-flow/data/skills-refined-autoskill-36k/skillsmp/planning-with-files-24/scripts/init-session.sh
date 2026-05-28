#!/usr/bin/env bash
# Initialize planning files for a new session (Codex-compatible).
# Refactor planning session storage to hash directories for traceability. sddsa89612jk4hbwas678
#
# Usage:
#   bash .codex/skills/planning-with-files/scripts/init-session.sh [session-hash] [session-title]
#
# Behavior:
# - Stores planning files under: docs/en/developer/plans/<session-hash>/
# - Creates: task_plan.md, findings.md, progress.md
# - If session-hash is omitted, a random one is generated.

set -euo pipefail

SESSION_HASH="${1:-}"
SESSION_TITLE="${2:-}"
DATE="$(date +%Y-%m-%d)"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(cd "${SCRIPT_DIR}/../templates" && pwd)"

generate_hash() {
    # Generate a readable, filesystem-safe hash (lowercase letters + digits).
    python3 - <<'PY'
import secrets
import string

alphabet = string.ascii_lowercase + string.digits
print("".join(secrets.choice(alphabet) for _ in range(20)))
PY
}

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
PLAN_BASE_DIR="${REPO_ROOT}/docs/en/developer/plans"

if [ -z "${SESSION_HASH}" ]; then
    SESSION_HASH="$(generate_hash)"
fi

SESSION_DIR="${PLAN_BASE_DIR}/${SESSION_HASH}"

echo "Initializing planning files for session: ${SESSION_HASH}"
echo "Using templates from: ${TEMPLATE_DIR}"
echo "Planning directory: ${SESSION_DIR}"

mkdir -p "${SESSION_DIR}"

copy_if_missing() {
    local src_file="$1"
    local dest_file="$2"

    if [ -f "${dest_file}" ]; then
        echo "${dest_file} already exists, skipping"
        return 0
    fi

    if [ ! -f "${src_file}" ]; then
        echo "ERROR: Template not found: ${src_file}"
        exit 1
    fi

    cp "${src_file}" "${dest_file}"
    echo "Created ${dest_file}"
}

hydrate_template() {
    local target_file="$1"
    python3 - "$target_file" "$DATE" "$SESSION_HASH" "$SESSION_TITLE" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
date = sys.argv[2]
session_hash = sys.argv[3]
session_title = sys.argv[4]
content = path.read_text(encoding="utf-8")

content = content.replace("[DATE]", date)
content = content.replace("[SESSION_HASH]", session_hash)
content = content.replace("[SESSION_TITLE]", session_title)

path.write_text(content, encoding="utf-8")
PY
}

# Create planning files in the session directory (docs/en/developer/plans/<hash>/).
copy_if_missing "${TEMPLATE_DIR}/task_plan.md" "${SESSION_DIR}/task_plan.md"
copy_if_missing "${TEMPLATE_DIR}/findings.md" "${SESSION_DIR}/findings.md"
copy_if_missing "${TEMPLATE_DIR}/progress.md" "${SESSION_DIR}/progress.md"

# Fill common placeholders so the hash is embedded for traceability.
hydrate_template "${SESSION_DIR}/task_plan.md"
hydrate_template "${SESSION_DIR}/findings.md"
hydrate_template "${SESSION_DIR}/progress.md"

# Sync docs navigation so the new session pages are discoverable.
# Docusaurus does not require an explicit sync when using sidebar autogeneration. docs/en/developer/plans/dsim8xybp9oa18nz1gfq/task_plan.md dsim8xybp9oa18nz1gfq
if [ "${HC_SKIP_DOCS_JSON_SYNC:-}" != "1" ]; then
    if [ -f "${REPO_ROOT}/docs/docs.json" ]; then
        bash "${SCRIPT_DIR}/sync-docs-json-plans.sh"
    else
        echo "Skipping docs navigation sync: docs/docs.json not found (likely using Docusaurus)."
    fi
else
    echo "Skipping docs navigation sync (HC_SKIP_DOCS_JSON_SYNC=1)"
fi

echo ""
echo "Planning files initialized!"
echo "Files: ${SESSION_DIR}/task_plan.md, ${SESSION_DIR}/findings.md, ${SESSION_DIR}/progress.md"
echo "Tip: Keep using the session hash in inline code comments for traceability: ${SESSION_HASH}"
