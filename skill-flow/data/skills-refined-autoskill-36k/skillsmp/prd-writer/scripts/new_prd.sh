#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 \"PRD Title\""
  exit 1
fi

TITLE="$*"
DATE="$(date +%F)"

# slugify (ascii only)
SLUG="$(echo "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g' \
  | sed -E 's/^-+|-+$//g')"

DIR="docs/prd"
TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../resources" && pwd)"
TEMPLATE_FILE="${TEMPLATE_DIR}/universal_prd_template.md"

mkdir -p "$DIR"
OUT="${DIR}/${DATE}-${SLUG}.md"

if [ -e "$OUT" ]; then
  echo "Already exists: $OUT"
  exit 1
fi

cp "$TEMPLATE_FILE" "$OUT"

# Replace first title line
perl -0777 -i -pe "s/^# Universal PRD — <Title>\$/# Universal PRD — ${TITLE}/m" "$OUT"

echo "Created: $OUT"
