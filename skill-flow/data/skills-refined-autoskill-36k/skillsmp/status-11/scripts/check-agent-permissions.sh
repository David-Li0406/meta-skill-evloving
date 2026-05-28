#!/bin/bash
set -e
# Fail if any agent file allows destructive commands without ask
# List of destructive patterns to detect when allowed
DESTRUCTIVE_PATTERNS=(
  "rm -rf"
  "rm -r"
  "rm \*"
  "git reset --hard"
  "git push --force"
  "git push -f"
  "dd if="
  "sh -c '"
)


FOUND=0
for p in "${DESTRUCTIVE_PATTERNS[@]}"; do
  if rg -n "\"$p\"\s*:\s*allow" .opencode/agent >/dev/null 2>&1; then
    echo "Found destructive allow pattern: $p"
    rg -n "\"$p\"\s*:\s*allow" .opencode/agent || true
    FOUND=1
  fi
done

if [ $FOUND -eq 1 ]; then
  exit 1
else
  echo 'No destructive allow patterns found.'
fi
