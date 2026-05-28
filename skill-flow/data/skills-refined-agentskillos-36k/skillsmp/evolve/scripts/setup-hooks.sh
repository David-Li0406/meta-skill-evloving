#!/bin/bash
# Setup Git Hooks for self-evolving-agent
# Run this once after cloning the repo

set -e

echo "🔧 Setting up Git hooks..."

# Get the repo root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Configure git to use .githooks directory
git config core.hooksPath .githooks

# Make hooks executable
chmod +x .githooks/*

echo ""
echo "✅ Git hooks configured successfully!"
echo ""
echo "The following hooks are now active:"
echo "  - pre-commit: Validates SKILL.md, checks for large files, etc."
echo ""
echo "To disable hooks temporarily, use: git commit --no-verify"
echo "To disable hooks permanently, run: git config --unset core.hooksPath"
