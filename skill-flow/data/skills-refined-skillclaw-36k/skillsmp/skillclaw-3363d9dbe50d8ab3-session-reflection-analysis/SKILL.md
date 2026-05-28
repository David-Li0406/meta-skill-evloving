---
name: session-reflection-analysis
description: Use this skill when asked to reflect on how the session went.
---

# Session Reflection Analysis

Analyze recent chat history to identify improvement opportunities and reduce token waste in future sessions.

## Overview

This skill helps identify patterns of inefficiency in Claude Code sessions by analyzing session history. The analysis focuses on actionable improvements to documentation, automation, and workflows.

## Step 1: Locate Project Sessions

First, find the correct project folder. Claude Code stores sessions at `~/.claude/projects/` with folder names derived from the project path (slashes become dashes, colons become double-dashes).

**IMPORTANT**: When using the Bash tool, run each command separately (not all at once) to avoid syntax errors with command substitution.

```bash
# List available project folders
ls -la ~/.claude/projects/

# Find the current project's session folder
PROJ_PATH=$(pwd | sed 's|^/||; s|/|-|g')
PROJECT_DIR="$HOME/.claude/projects/-${PROJ_PATH}"
echo "Project directory: $PROJECT_DIR"

# Check if directory exists and list sessions
if [ -d "$PROJECT_DIR" ]; then
  echo "Found project dir!"
  ls -lah "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -5
else
  echo "No session folder found"
  echo "Available projects:"
  ls ~/.claude/projects/
fi
```

## Step 2: Generate Session Summary

**CRITICAL**: Do NOT read raw session files directly. They are massive and will consume your entire token budget.

### Recommended: Use the Helper Script

The simplest and most reliable approach is to use the provided helper script:

```bash
bash ~/.claude/skills/session-reflection-analysis/analyze.sh
```

This script handles all steps automatically: verifies jq is installed, finds the project directory, generates the summary, and displays statistics.

### Alternative: Manual Steps

If you need to run the steps manually, use the helper script's source code as a reference, or save the commands to a temporary script file and execute it:

```bash
cat > /tmp/analyze-session.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

PROJ_PATH=$(pwd | sed 's|^/||; s|/|-|g')
PROJECT_DIR="$HOME/.claude/projects/-${PROJ_PATH}"
OUTPUT="/tmp/session-summary.jsonl"

if ! command -v jq &> /dev/null; then
  echo "ERROR: jq is required"
  exit 1
fi

echo "Processing sessions from: $PROJECT_DIR"
cat "$PROJECT_DIR"/*.jsonl 2>/dev/null | jq -c 'select(.type == "user" or .type == "assistant") | {type, ts: .timestamp, content: (.message.content[0:300] // "")}'
EOF
```