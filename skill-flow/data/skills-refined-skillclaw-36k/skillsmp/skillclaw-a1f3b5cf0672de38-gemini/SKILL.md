---
name: gemini
description: Use this skill when the user asks to run the Gemini CLI for code review, plan review, or big context (>200k) processing, ideal for comprehensive analysis requiring large context windows.
---

# Gemini Skill Guide

## When to Use Gemini
- WHEN ASKED TO BE ACTIVATED
- **Code Review**: Comprehensive code reviews across multiple files
- **Plan Review**: Analyzing architectural plans, technical specifications, or project roadmaps
- **Big Context Processing**: Tasks requiring >200k tokens of context (entire codebases, documentation sets)
- **Multi-file Analysis**: Understanding relationships and patterns across many files

## ⚠️ Critical: Background/Non-Interactive Mode Warning

**NEVER use `--approval-mode default` in background or non-interactive shells** (like Claude Code tool calls). It will hang indefinitely waiting for approval prompts that cannot be provided.

**For automated/background reviews:**
- ✅ Use `--approval-mode yolo` for fully automated execution
- ✅ OR wrap with timeout: `timeout 300 gemini ...`
- ❌ NEVER use `--approval-mode default` without interactive terminal

**Symptoms of hung Gemini:**
- Process running 20+ minutes with 0% CPU usage
- No network activity
- Process state shows 'S' (sleeping)

**Fix hung process:**
```bash
# Check if hung
ps aux | grep gemini | grep -v grep

# Kill if necessary
pkill -9 -f "gemini.*gemini-3-pro-preview"
```

## Running a Task

1. Ask the user (via `AskUserQuestion`) which model to use in a **single prompt**. Available models:
   - `gemini-3-pro-preview` ⭐ (flagship model, best for coding & complex reasoning, 35% better at software engineering than 2.5 Pro)
   - `gemini-3-flash` (sub-second latency, distilled from 3 Pro, best for speed-critical tasks)
   - `gemini-2.5-pro` (legacy option, strong all-around performance)
   - `gemini-2.5-flash` (legacy option, cost-efficient with thinking capabilities)
   - `gemini-2.5-flash-lite` (legacy option, fastest processing)

2. Select the approval mode based on the task:
   - `default`: Prompt for approval (⚠️ ONLY for interactive terminal sessions)
   - `auto_edit`: Auto-approve edit tools only (for code reviews with suggestions)
   - `yolo`: Auto-approve all tools (✅ REQUIRED for background/automated tasks)

3. Assemble the command with appropriate options:
   - `-m, --model <MODEL>` - Model selection
   - `--approval-mode <default|auto_edit|yolo>` - Control tool approval
   - ...