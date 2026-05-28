#!/usr/bin/env bash
set -euo pipefail

required=(tmux python3 codex)
optional=(claude git)

missing=0

for cmd in "${required[@]}"; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "❌ Missing dependency: $cmd" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "Install required deps and retry: ${required[*]}" >&2
  exit 1
fi

echo "✅ Found tmux:   $(tmux -V 2>/dev/null || echo tmux)" >&2
echo "✅ Found python: $(python3 -V 2>/dev/null || echo python3)" >&2
if codex --version >/dev/null 2>&1; then
  echo "✅ Found codex:  $(codex --version 2>/dev/null || true)" >&2
else
  echo "✅ Found codex:  $(command -v codex)" >&2
fi

for cmd in "${optional[@]}"; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "ℹ️  Optional: $cmd -> $(command -v "$cmd")" >&2
  fi
done

exit 0

