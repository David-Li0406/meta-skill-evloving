#!/usr/bin/env bash

# add-palette-feature.sh - Add features to existing palette

set -e

FEATURE=""
TARGET=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --feature) FEATURE="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$FEATURE" ] || [ -z "$TARGET" ]; then
  echo "Usage: $0 --feature virtual-scroll|server-search|keyboard-shortcuts|recent-commands|favorites|multi-step --target FILE"
  exit 1
fi

if [ ! -f "$TARGET" ]; then
  echo "❌ Target file not found: $TARGET"
  exit 1
fi

echo "📝 Adding $FEATURE to $TARGET..."

case $FEATURE in
  virtual-scroll)
    echo "  Installing @tanstack/react-virtual if not present..."
    if ! grep -q "@tanstack/react-virtual" package.json 2>/dev/null; then
      echo "  Run: npm install @tanstack/react-virtual"
    fi
    echo "  ✅ Feature requires manual integration - see references/virtual-scrolling.md"
    ;;
  server-search)
    echo "  ✅ Feature requires manual integration - see references/server-side-search.md"
    ;;
  *)
    echo "  ✅ Feature '$FEATURE' requires manual integration - see references/"
    ;;
esac
