---
name: session-summary-generator
description: Use this skill to generate session summaries and resume prompts for multi-session work, especially when completing features or when the user requests a summary.
---

# Session Summary Generator

## Overview

This skill creates comprehensive session summaries for complex multi-session work, enabling seamless resumption of tasks. It generates a markdown file in `docs/summaries/` with a standardized format.

## When to Use

Trigger this skill when:
- User explicitly requests a summary (e.g., "generate summary", "wrap up", "save progress", "end session").
- Completing a significant feature or refactor.
- Conversation context is reaching limits (~50% before auto-compact).
- Before starting a new chat session.
- When collaborating with team members on the same feature.

### Auto-Suggest Triggers

Proactively suggest generating a summary when:
- Multiple files have been modified in the session.
- A feature implementation is complete.
- The conversation has been long (many exchanges).
- User mentions ending their work session.

## Output Location

Session summaries are stored in: `docs/summaries/YYYY-MM-DD_feature-name.md`.

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

Create the summary using the template in `TEMPLATE.md`.

Key sections to include:
1. **Overview**: Brief description of session focus.
2. **Completed Work**: Bullet points of accomplishments.
3. **Key Files Modified**: Table of files and changes.
4. **Design Patterns Used**: Important architectural decisions.
5. **Remaining Tasks**: What's left to do.
6. **Resume Prompt**: Copy-paste instructions for next session.

### Step 3: Create Resume Prompt

The resume prompt should include:
- Context reference to the summary file.
- Specific file paths to review first.
- Current status and immediate next steps.
- Any blockers or decisions that need user input.

### Step 4: Analyze Token Usage

Review the conversation for token efficiency opportunities using `analyzers/token-analyzer.md` and `guidelines/token-optimization.md`.

**Look for:**
1. **File Reading Patterns**: Suggest caching or using Grep for files read multiple times.
2. **Search Inefficiencies**: Recommend consolidating redundant searches.
3. **Response Verbosity**: Note opportunities for conciseness.
4. **Good Practices to Acknowledge**: Effective use of Grep before Read, targeted searches, and concise responses.

**Generate token usage report with:**
- Estimated total tokens.
- Token breakdown by category.
- Efficiency score (0-100).
- Top 5 optimization opportunities.
- Notable good practices observed.

### Step 5: Analyze Command Accuracy

Review tool calls for accuracy and error patterns using `analyzers/command-analyzer.md` and `guidelines/command-accuracy.md`.

**Look for:**
1. **Failed Commands and Causes**: Identify path, import, type, and edit errors.
2. **Error Patterns**: Categorize by type and note severity.
3. **Recovery and Improvements**: Analyze how quickly errors were fixed and improvements from previous sessions.

**Generate command accuracy report with:**
- Total commands executed.
- Success rate percentage.
- Failure breakdown by category.
- Top 3 recurring issues with root cause analysis.
- Actionable recommendations for prevention.

## Example Usage

When user says: "Let's wrap up for today":

1. Analyze git changes and conversation history.
2. Create `docs/summaries/YYYY-MM-DD_feature-name.md`.
3. Provide the resume prompt for the next session.
4. Suggest: "When context gets long, consider starting a new chat with the resume prompt."

## Tips

- Keep summaries focused on a single feature or area.
- Include exact file paths for easy navigation.
- Note any environmental setup needed (database migrations, etc.).
- Flag any blocking issues or decisions made.
- Reference the CLAUDE.md file patterns when applicable.

## Quality Checklist

Before finalizing the summary, verify:
- **Resume Prompt** is copy-paste ready with all context.
- **Remaining Tasks** are numbered and actionable.
- **Options** are provided if there are multiple valid directions.
- **Self-Reflection** includes honest assessment of failures.
- **Improvements** are specific and actionable.
- **Key Files** have clickable paths for navigation.
- **Environment** notes any setup requirements.

## Anti-Patterns to Avoid

- Generic summaries like "made progress on feature".
- Resume prompts that require reading the full summary.
- Self-reflection that only mentions successes.
- Vague improvements like "be more careful".
- Missing blockers or decisions that will stall next session.