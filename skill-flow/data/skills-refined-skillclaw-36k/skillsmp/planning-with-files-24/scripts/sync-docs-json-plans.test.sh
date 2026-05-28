#!/usr/bin/env bash
# Smoke tests for sync-docs-json-plans.sh and init-session.sh integration. docsjsonindex20260121

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNCER="${SCRIPT_DIR}/sync-docs-json-plans.sh"
INIT_SESSION="${SCRIPT_DIR}/init-session.sh"

create_min_docs_json() {
  local target="$1"
  mkdir -p "$(dirname "${target}")"
  cat > "${target}" <<'JSON'
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "Test Docs",
  "navigation": {
    "languages": [
      {
        "language": "en",
        "default": true,
        "tabs": [
          {
            "tab": "Developer Docs",
            "groups": [
              { "group": "Home", "pages": ["en/developer/index"] },
              { "group": "plans", "pages": ["en/developer/plans/stale"] }
            ]
          }
        ]
      }
    ]
  }
}
JSON
}

assert_pages_equal() {
  local docs_json="$1"
  shift
  python3 - "${docs_json}" "$@" <<'PY'
import json
import sys

docs_json_path = sys.argv[1]
expected = sys.argv[2:]

data = json.loads(open(docs_json_path, encoding="utf-8").read())
pages = (
    data["navigation"]["languages"][0]["tabs"][0]["groups"][1]["pages"]
)

if pages != expected:
    raise SystemExit(
        "FAIL: pages mismatch\n"
        f"Expected: {expected}\n"
        f"Actual:   {pages}\n"
    )
PY
}

TMP_DIR_1="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR_1}" "${TMP_DIR_2:-}"' EXIT

cd "${TMP_DIR_1}"
git init -q

mkdir -p docs/en/developer/plans
create_min_docs_json "docs/docs.json"

mkdir -p docs/en/developer/plans/aaaa
touch docs/en/developer/plans/aaaa/task_plan.md
touch docs/en/developer/plans/aaaa/findings.md
touch docs/en/developer/plans/aaaa/progress.md

mkdir -p docs/en/developer/plans/bbbb
touch docs/en/developer/plans/bbbb/task_plan.md

bash "${SYNCER}" >/dev/null

assert_pages_equal \
  "docs/docs.json" \
  "en/developer/plans/aaaa/task_plan" \
  "en/developer/plans/aaaa/findings" \
  "en/developer/plans/aaaa/progress" \
  "en/developer/plans/bbbb/task_plan"

TMP_DIR_2="$(mktemp -d)"
cd "${TMP_DIR_2}"
git init -q

mkdir -p docs/en/developer/plans
create_min_docs_json "docs/docs.json"

SESSION_HASH="testsessionhash00000001"
SESSION_TITLE="Test session"

bash "${INIT_SESSION}" "${SESSION_HASH}" "${SESSION_TITLE}" >/dev/null

python3 - "docs/docs.json" "${SESSION_HASH}" <<'PY'
import json
import sys

docs_json_path = sys.argv[1]
session_hash = sys.argv[2]

data = json.loads(open(docs_json_path, encoding="utf-8").read())
pages = data["navigation"]["languages"][0]["tabs"][0]["groups"][1]["pages"]

expected = [
    f"en/developer/plans/{session_hash}/task_plan",
    f"en/developer/plans/{session_hash}/findings",
    f"en/developer/plans/{session_hash}/progress",
]

missing = [p for p in expected if p not in pages]
if missing:
    raise SystemExit(f"FAIL: init-session did not sync expected pages: {missing}")
PY

echo "PASS"

