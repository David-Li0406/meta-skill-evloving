---
name: summary-generator
description: Generates session summaries and resume prompts for multi-session work. Use when completing features, before context limits (~50% capacity), or when user says "summary", "wrap up", "save progress", "end session". Creates markdown in docs/summaries/ with completed work, files modified, and restart instructions.
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git log:*), Bash(git status:*), Write
---

# Session Summary Generator

## Overview

This skill creates comprehensive session summaries for complex multi-session work, enabling seamless resumption of tasks. It generates a markdown file in `docs/summaries/` with a standardized format.

## When to Use

Trigger this skill when:
- User explicitly requests a summary ("generate summary", "wrap up", "save progress")
- Completing a significant feature or refactor
- Conversation context is reaching limits (~50% before auto-compact)
- Before starting a new chat session
- When collaborating with team members on the same feature

### Auto-Suggest Triggers

Proactively suggest generating a summary when:
- Multiple files have been modified in the session
- A feature implementation is complete
- The conversation has been long (many exchanges)
- User mentions ending their work session

## Output Location

Session summaries are stored in: `docs/summaries/YYYY-MM-DD_feature-name.md`

## Instructions

### Step 1: Analyze Current Work

Run these commands to understand what was done:

```bash
git status
git diff --stat
git log --oneline -10
```

Review the conversation history to identify:
- What was accomplished
- Key decisions made
- Files created or modified
- Any remaining tasks

### Step 2: Generate Summary File

Create the summary using the template in [TEMPLATE.md](TEMPLATE.md).

Key sections to include:
1. **Overview**: Brief description of session focus
2. **Completed Work**: Bullet points of accomplishments
3. **Key Files Modified**: Table of files and changes
4. **Design Patterns Used**: Important architectural decisions
5. **Remaining Tasks**: What's left to do
6. **Resume Prompt**: Copy-paste instructions for next session

### Step 3: Create Resume Prompt

The resume prompt should include:
- **Token optimization directive**: Reference to token-optimization.md guidelines (MANDATORY - include at the top)
- Context reference to the summary file
- Specific file paths to review first
- Current status and immediate next steps
- Any blockers or decisions that need user input

**IMPORTANT**: Always start the resume prompt with:
```
IMPORTANT: Follow token optimization patterns from `.claude/skills/summary-generator/guidelines/token-optimization.md`:
- Use Grep before Read for searches
- Use Explore agent for multi-file exploration
- Reference this summary instead of re-reading files
- Keep responses concise
```

### Step 4: Analyze Token Usage

Review the conversation for token efficiency opportunities using [analyzers/token-analyzer.md](analyzers/token-analyzer.md) and [guidelines/token-optimization.md](guidelines/token-optimization.md).

**Look for:**
1. **File Reading Patterns**
   - Files read multiple times → Suggest caching or using Grep
   - Large files read fully when Grep would suffice
   - Reading generated files (node_modules, build artifacts)

2. **Search Inefficiencies**
   - Redundant searches → Recommend consolidating queries
   - Overly broad glob patterns
   - Multiple searches that could be combined

3. **Response Verbosity**
   - Verbose explanations → Note opportunities for conciseness
   - Repeated explanations of same concepts
   - Unnecessary multi-paragraph responses for simple tasks

4. **Good Practices to Acknowledge**
   - Effective use of Grep before Read
   - Targeted searches with appropriate scope
   - Concise, actionable responses
   - Efficient agent usage

**Generate token usage report with:**
- Estimated total tokens (use chars/4 approximation)
- Token breakdown by category (file ops, code gen, explanations, searches)
- Efficiency score (0-100) using scoring system from token-analyzer.md
- Top 5 optimization opportunities (prioritized by impact)
- Notable good practices observed

See [analyzers/token-analyzer.md](analyzers/token-analyzer.md) for detailed analysis methodology.

### Step 5: Analyze Command Accuracy

Review tool calls for accuracy and error patterns using [analyzers/command-analyzer.md](analyzers/command-analyzer.md) and [guidelines/command-accuracy.md](guidelines/command-accuracy.md).

**Look for:**
1. **Failed Commands and Causes**
   - Path errors (backslashes, wrong case, file not found)
   - Import errors (wrong module path, wrong import style)
   - Type errors (property doesn't exist, type mismatch)
   - Edit errors (string not found, whitespace issues)

2. **Error Patterns**
   - Categorize by type: path, syntax, permission, logic
   - Identify recurring issues (same mistake multiple times)
   - Note severity: critical, high, medium, low
   - Calculate time wasted on failures and retries

3. **Recovery and Improvements**
   - How quickly errors were fixed
   - Whether verification prevented errors
   - Improvements from previous sessions
   - Good patterns that prevented errors

**Generate command accuracy report with:**
- Total commands executed
- Success rate percentage
- Failure breakdown by category
- Top 3 recurring issues with root cause analysis
- Actionable recommendations for prevention
- Improvements observed from past sessions

See [analyzers/command-analyzer.md](analyzers/command-analyzer.md) for detailed analysis methodology.

## Example Usage

When user says: "Let's wrap up for today"

Response:
1. Analyze git changes and conversation history
2. Create `docs/summaries/2025-12-30_enrollment-improvements.md`
3. Provide the resume prompt with token optimization directive
4. Suggest: "When context gets long (~40% tokens), start a new chat with this resume prompt"

Example resume prompt output:
```
Resume enrollment improvements session.

IMPORTANT: Follow token optimization patterns from `.claude/skills/summary-generator/guidelines/token-optimization.md`:
- Use Grep before Read for searches
- Use Explore agent for multi-file exploration
- Reference this summary instead of re-reading files
- Keep responses concise

## Context
Previous session completed:
- Added middle name support to enrollment form
- Updated validation for optional middle name field
- Added i18n translations for new field

Session summary: docs/summaries/2025-12-30_enrollment-improvements.md
...
```

## Tips

- Keep summaries focused on a single feature or area
- Include exact file paths for easy navigation
- Note any environmental setup needed (database migrations, etc.)
- Flag any blocking issues or decisions made
- Reference the CLAUDE.md file patterns when applicable
