#!/bin/bash

echo "--- PRE-COMMIT REVIEW REPORT ---"
echo "Target Branch: $(git branch --show-current)"
echo ""
echo "Files Staged for Commit:"
git diff --cached --name-only | sed 's/^/  - /'
echo ""
echo "Summary of Changes:"
# Generates a high-level summary of additions/deletions
git diff --cached --stat
echo ""
echo "--------------------------------"
