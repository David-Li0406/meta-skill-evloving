---
name: session-summary-generator
description: Use this skill to generate comprehensive session summaries and resume prompts for multi-session work, especially when completing features or when the user requests a summary.
---

# Skill body

## Overview

This skill creates detailed session summaries for complex multi-session work, enabling seamless resumption of tasks. It generates a markdown file in `docs/summaries/` with a standardized format.

## When to Use

Trigger this skill when:
- The user explicitly requests a summary (e.g., "generate summary", "wrap up", "save progress", "end session").
- Completing a significant feature or refactor.
- The conversation context is reaching limits (~50% before auto-compact).
- Before starting a new chat session.
- Collaborating with team members on the same feature.

### Auto-Suggest Triggers

Proactively suggest generating a summary when:
- Multiple files have been modified in the session.
- A feature implementation is complete.
- The conversation has been long (many exchanges).
- The user mentions ending their work session.

## Instructions

### Step 1: Analyze Current Work

Run these commands to understand what was done:

```bash
git status
git diff --stat
git log --oneline -10
```

Review the conversation history to identify:
- What was accomplished.
- Key decisions made.
- Files created or modified.
- Any remaining tasks.

### Step 2: Generate Summary File

Create the summary using a standardized template. Key sections to include:
1. **Overview**: Brief description of session focus.
2. **Completed Work**: Bullet points of accomplishments.
3. **Key Files Modified**: Table of files and changes.
4. **Remaining Tasks**: What's left to do.
5. **Resume Prompt**: Copy-paste instructions for the next session.

### Step 3: Create Resume Prompt

The resume prompt should include:
- Context reference to the summary file.
- Specific file paths to review first.
- Current status and immediate next steps.
- Any blockers or decisions that need user input.

## Output Location

Session summaries are stored in: `docs/summaries/YYYY-MM-DD_feature-name.md`