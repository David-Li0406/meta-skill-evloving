#!/usr/bin/env bash
# Smoke test for append-changelog.sh behavior. l290bb7v758opd6uxu6r

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPENDER="${SCRIPT_DIR}/append-changelog.sh"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

cd "${TMP_DIR}"
git init -q

mkdir -p docs/en/change-log
cat > docs/en/change-log/0.0.0.md <<'MD'
# 0.0.0

## Changes
MD

SESSION_HASH="testhash1234567890ab"
# Ensure MDX comment-wrapped summaries are unwrapped before writing the changelog entry. docs/en/developer/plans/mintmdxcomment20260122/task_plan.md mintmdxcomment20260122
SUMMARY="{/* Fix Vite \`/api\` proxy target to avoid SSE 404 in local dev. ${SESSION_HASH} */}"

printf '%s' "${SUMMARY}" | bash "${APPENDER}" "${SESSION_HASH}" >/dev/null

if rg -n "<!--" docs/en/change-log/0.0.0.md >/dev/null; then
    echo "FAIL: changelog contains an HTML comment line"
    exit 1
fi

if rg -n --fixed-strings "{/*" docs/en/change-log/0.0.0.md >/dev/null; then
    echo "FAIL: changelog contains an MDX comment wrapper"
    exit 1
fi

EXPECTED_LINK="([${SESSION_HASH}](../developer/plans/${SESSION_HASH}/task_plan))"
if ! rg -n --fixed-strings "${EXPECTED_LINK}" docs/en/change-log/0.0.0.md >/dev/null; then
    echo "FAIL: changelog entry missing expected plan link: ${EXPECTED_LINK}"
    exit 1
fi

if rg -n --fixed-strings " ${SESSION_HASH} ([" docs/en/change-log/0.0.0.md >/dev/null; then
    echo "FAIL: changelog summary still contains the trailing session hash token"
    exit 1
fi

COUNT="$(rg -c --fixed-strings "${EXPECTED_LINK}" docs/en/change-log/0.0.0.md || true)"
if [ "${COUNT}" -ne 1 ]; then
    echo "FAIL: expected exactly 1 appended entry, got: ${COUNT}"
    exit 1
fi

echo "PASS"
