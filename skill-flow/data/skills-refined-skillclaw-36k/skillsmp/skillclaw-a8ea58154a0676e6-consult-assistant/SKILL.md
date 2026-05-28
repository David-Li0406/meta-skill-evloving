---
name: consult-assistant
description: Use this skill when you need to consult an AI assistant for questions, feedback, reviews, or discussions, allowing for iterative conversation until a satisfactory answer is reached.
---

# Skill body

## Overview

Consult an AI assistant for questions, feedback, reviews, or discussions. The conversation iterates until the assistant signals completion (e.g., "LGTM" for reviews, or a complete answer for questions) or until 10 rounds are reached.

## Consultation Modes

| Mode | When to use | Input source |
|------|-------------|--------------|
| Question | Need an answer or explanation | User question + context |
| Discussion | Explore ideas or trade-offs | Topic + relevant context |
| Plan review | Validate a plan before execution | Plan file (`plan-*.md`) or text |
| Change review | Validate code changes | `git diff` + untracked files |
| Custom | Any time | User-specified content |

## Workflow

1. **Determine the consultation mode**
   - If the user specifies a mode, use it.
   - If the user asks a question or requests discussion, use **question** or **discussion** mode.
   - If auto-invoked on plan mode exit and a plan file matching `~/.assistant/plans/plan-*.md` exists, default to **plan review** (even if there are uncommitted changes).
   - If there are uncommitted changes (`git status --porcelain` is non-empty), default to **change review**.
   - Otherwise, ask the user what they want to consult about.

2. **Collect the content**
   - **Question**: Gather the user's question and any relevant context (code snippets, error messages, etc.).
   - **Discussion**: Gather the topic and relevant context for exploration.
   - **Plan review**: Read from `~/.assistant/plans/plan-*.md` (use the most recently modified if multiple exist) or ask the user for the plan.
   - **Change review**: Collect both tracked and untracked changes:
     ```sh
     # Tracked changes (staged + unstaged)
     # Use fallback for repos without commits
     if git rev-parse --verify HEAD >/dev/null 2>&1; then
       git diff HEAD
     else
       git diff --cached
       git diff
     fi

     # Untracked files - safe handling for special characters
     # Skip binary files and files larger than 100KB
     git ls-files -z --others --exclude-standard | while IFS= read -r -d '' f; do
       # Skip binary files (use -- to handle filenames starting with -)
       if file -- "$f" | grep -q 'text'; then
         # Skip files larger than 100KB
         size=$(stat -f%z -- "$f" 2>/dev/null)
         if [ "$size" -le 100000 ]; then
           cat "$f"
         fi
       fi
     done
     ```