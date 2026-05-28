---
name: ask-codex
description: Consult Codex for questions, feedback, reviews, or discussions. Use when Claude needs a second opinion, wants to validate an approach, or the user explicitly calls /ask-codex.
---

# Ask Codex

## Overview

Consult Codex for questions, feedback, reviews, or discussions. The conversation iterates until Codex signals completion (e.g., "LGTM" for reviews, or a complete answer for questions) or until 10 rounds are reached.

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
   - If auto-invoked on plan mode exit and a plan file matching `~/.claude/plans/plan-*.md` exists, default to **plan review** (even if there are uncommitted changes).
   - If there are uncommitted changes (`git status --porcelain` is non-empty), default to **change review**.
   - Otherwise, ask the user what they want to consult about.

2. **Collect the content**
   - **Question**: Gather the user's question and any relevant context (code snippets, error messages, etc.).
   - **Discussion**: Gather the topic and relevant context for exploration.
   - **Plan review**: Read from `~/.claude/plans/plan-*.md` (use the most recently modified if multiple exist) or ask the user for the plan.
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
         size=$(stat -f%z -- "$f" 2>/dev/null || stat -c%s -- "$f" 2>/dev/null)
         if [ "$size" -lt 102400 ]; then
           echo "=== New file: $f ==="
           cat -- "$f"
         else
           echo "=== New file: $f (skipped: >100KB) ==="
         fi
       else
         echo "=== New file: $f (skipped: binary) ==="
       fi
     done
     ```
   - **Custom**: Ask the user to provide the content.
   - Also collect the original user prompt (task background) from the conversation.

3. **Prepare the plans directory**
   - Run `mkdir -p ~/.claude/plans` to ensure the directory exists.

4. **Write the consultation input file**
   - Create a file at `~/.claude/plans/consultation-input.md` with this format:
     ```
     ## Original Request
     <original user prompt>

     ## Consultation Mode
     <question | discussion | plan review | change review | custom>

     ## Content
     <question, topic, plan, diff + untracked files, or custom content>

     ## Task
     <varies by mode>
     - Question: Answer the question. When complete, output "ANSWERED" on its own line.
     - Discussion: Explore the topic. When a conclusion or actionable insight is reached, output "CONCLUDED" on its own line.
     - Plan review / Change review: Review the content. If there are problems, describe them. If OK, output "LGTM" on its own line.
     - Custom: Address the request. When complete, output "DONE" on its own line.
     ```

5. **Set up the temp environment**
   - Prepare a temp directory under `~/.claude/tmp` (same as codex-review):
     - Claude Code runs each shell command in a fresh process, so `export` does not persist across commands.
     - Always run the temp setup and `codex exec` in the same shell invocation.
     ```sh
     mkdir -p ~/.claude/tmp
     TMPDIR="$(mktemp -d ~/.claude/tmp/ask-codex.XXXXXXXX)"
     ZDOTDIR="$TMPDIR/zsh"
     mkdir -p "$ZDOTDIR"
     XCRUN_CACHE_PATH="$TMPDIR/xcrun_db"
     DARWIN_USER_TEMP_DIR="$TMPDIR"
     export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR
     ```

6. **Run Codex**
   - Execute the temp setup and `codex exec` in the same shell invocation:
     ```sh
     mkdir -p ~/.claude/tmp && \
     TMPDIR="$(mktemp -d ~/.claude/tmp/ask-codex.XXXXXXXX)" && \
     ZDOTDIR="$TMPDIR/zsh" && \
     mkdir -p "$ZDOTDIR" && \
     XCRUN_CACHE_PATH="$TMPDIR/xcrun_db" && \
     DARWIN_USER_TEMP_DIR="$TMPDIR" && \
     export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR && \
     cat ~/.claude/plans/consultation-input.md | codex exec --sandbox read-only -
     ```
   - Timeout: 5 minutes (300 seconds).

7. **Parse the result**
   - Trim whitespace from the output.
   - Check if any line matches a completion signal (case-insensitive):
     - "LGTM" → **approved** (for reviews)
     - "ANSWERED" → **answered** (for questions)
     - "CONCLUDED" → **concluded** (for discussions)
     - "DONE" → **done** (for custom)
   - If matched, mark as **responder complete**.
   - Otherwise, extract the response as **follow-up needed from responder**.

8. **Evaluate the response (questioner's perspective)**
   - After receiving Codex's response, Claude evaluates:
     - Does the response fully address the original question/concern?
     - Are there unclear points or ambiguities that need clarification?
     - Did new questions arise from the response?
   - Determine questioner status:
     - **Questioner satisfied**: No remaining questions or concerns.
     - **Questioner has follow-ups**: Additional questions or clarifications needed.

9. **Iteration loop**
   - **Continue iteration** if ANY of the following:
     - Responder signaled follow-up needed (no completion signal).
     - Questioner (Claude) has remaining questions or unclear points.
   - **Stop iteration** if BOTH:
     - Responder signaled complete (LGTM/ANSWERED/CONCLUDED/DONE), AND
     - Questioner (Claude) is satisfied (no remaining questions).
   - If continuing:
     - Report the response to the user.
     - If no completion signal was returned, explicitly ask for the completion signal (LGTM/ANSWERED/CONCLUDED/DONE) in the next reply.
     - For **question/discussion**: Formulate specific follow-up questions based on unclear points or new questions that arose.
     - For **change review**: Apply fixes to the code, then re-collect the diff and untracked files.
     - For **plan review**: Adjust the plan based on feedback, or ask for clarification on unclear feedback.
     - Update the consultation input with follow-up questions/context.
     - Return to step 4 and resubmit.
   - Maximum 10 iterations.

10. **Finish**
    - **Complete**: Report the full response content to the user (answer, conclusion, or review result), then note the completion status and proceed.
    - **Not complete after 10 rounds**: Report the current state and ask the user how to proceed.

## Auto-invocation

This skill is automatically invoked when:
- Claude Code exits plan mode (cross-review before execution).
- Claude Code completes any task with code changes (cross-review before proceeding).
- The user has not explicitly skipped the consultation.

Note: For ad-hoc consultations at any point, use `/ask-codex` manually.

## Notes

- Use `--sandbox read-only` since consultation does not require code modifications by Codex.
- Honor explicit user requests to skip the consultation.
- Plan files use the naming convention `plan-*.md` to distinguish from `consultation-input.md`.
- The consultation input file at `~/.claude/plans/consultation-input.md` persists for debugging and history.
- For change review, both `git diff` and untracked file contents are collected to ensure complete coverage.
- Completion signal detection uses exact line match (after trimming) to avoid false positives like "Not LGTM".
- Binary files and files larger than 100KB are skipped to avoid input bloat.
