---
name: git-commit
description: Create a git commit with structured message
argument-hint: [message] [files...] [plan_step]
---

# Git Commit

## Overview

Create a well-structured commit with a concise title and optional bullet-point description. Commits staged changes with proper formatting and AI attribution.

## Arguments

### Definitions

- **`[message]`** (optional): Override commit title. If not provided, auto-generate from changes.
- **`[files...]`** (optional): Specific files to commit. Default: all staged.
- **`[plan_step]`** (optional): Reference to plan step being completed.

### Values

\$ARGUMENTS

## Core Principles

- Title must be short (50 chars ideal, 120 max) and focus on the main task completed
- Description is optional for small commits
- Description uses 1-5 bullet points for larger commits highlighting important aspects
- Always include AI attribution with your model name: `Co-Authored-By: Claude <model> <noreply@anthropic.com>`

## Skill-Specific Guidelines

### Plan Step Reference

When following a plan (implementation plan, milestone plan, etc.), include the current step reference at the start of the commit title in brackets:

- **Task-based plans**: `[Task N]` where N is the task number (e.g., `[Task 1]`, `[Task 8]`)
- **Milestone-based plans**: `[Milestone N]` when committing after completing a milestone
- **Nested plans**: `[Task M.N]` for tasks within milestones (e.g., `[Task 1.1]`, `[Task 2.3]`)

Only include this prefix if you are actively following a plan with numbered steps. If no plan context exists, omit the brackets entirely.

**Examples:**

- `[Task 8] Update CLI with orchestrator integration`
- `[Milestone 1] Complete authentication module`
- `[Task 2.3] Add unit tests for validation logic`
- `Add helper function for date parsing` (no plan context)

## Instructions

1. Run `git status` to verify there are changes to commit
2. Run `git diff --staged` to analyze staged changes (if none, stage all with `git add .`)
3. Analyze the changes to determine:
   - Primary purpose of the changes (the "what")
   - Impact and scope (small fix vs. larger feature)
4. Determine plan step reference (if following a plan):
   - Check if there is an active plan with numbered tasks or milestones
   - Identify which task/milestone these changes correspond to
   - Format the prefix accordingly (e.g., `[Task 3]`, `[Milestone 2]`, `[Task 1.2]`)
5. Construct commit message:
   - **Title**: `[Step Ref]` prefix (if applicable) + imperative mood, capitalize first letter, no period
   - **Description**: Only if changes are substantial; 1-5 bullets on key aspects
6. Execute commit using HEREDOC for proper formatting:

   ```bash
   git commit -m "$(cat <<'EOF'
   [Task N] <title>

   - bullet 1 (optional)
   - bullet 2 (optional)

   Co-Authored-By: Claude <model> <noreply@anthropic.com>
   EOF
   )"
   ```

7. Return JSON output with commit details

## Output Guidance

Return JSON with commit details:

```json
{
  "success": true,
  "commit_hash": "{{commit_hash}}",
  "message": "{{message}}",
  "files_committed": ["{{files}}"],
  "stats": {
    "files_changed": "{{files_changed}}",
    "insertions": "{{insertions}}",
    "deletions": "{{deletions}}"
  }
}
```

<!--
Placeholders:
- {{commit_hash}}: Short commit hash (e.g., abc1234)
- {{message}}: Commit title/message
- {{files}}: Array of committed file paths
- {{files_changed}}: Number of files changed
- {{insertions}}: Lines added
- {{deletions}}: Lines removed
-->
