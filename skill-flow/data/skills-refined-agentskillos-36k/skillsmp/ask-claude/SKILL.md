---
name: ask-claude
description: Consult Claude for questions, feedback, reviews, or discussions. Use when Codex needs a second opinion, wants to validate an approach, or the user explicitly calls /ask-claude.
---

# Ask Claude

## Overview

Consult Claude for questions, feedback, reviews, or discussions. The conversation iterates until Claude signals completion (e.g., "LGTM" for reviews, or a complete answer for questions) or until 10 rounds are reached.

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
   - If auto-invoked on plan mode exit and a plan file matching `~/.codex/plans/plan-*.md` exists, default to **plan review** (even if there are uncommitted changes).
   - If there are uncommitted changes (`git status --porcelain` is non-empty), default to **change review**.
   - Otherwise, ask the user what they want to consult about.

2. **Collect the content**
   - **Question**: Gather the user's question and any relevant context (code snippets, error messages, etc.).
   - **Discussion**: Gather the topic and relevant context for exploration.
   - **Plan review**: Read from `~/.codex/plans/plan-*.md` (use the most recently modified if multiple exist) or ask the user for the plan.
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
- Run `mkdir -p ~/.codex/plans` to ensure the directory exists.

4. **Write the consultation input file**
   - Create a file at `~/.codex/plans/consultation-input.md` with this format:
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

5. **Run Claude**
   - Execute: `cat ~/.codex/plans/consultation-input.md | claude -p - --output-format text`
   - Timeout: 5 minutes (300 seconds).
   - Note: This runs as a separate Claude process, independent of the current session.

6. **Parse the result**
   - Trim whitespace from the output.
   - Check if any line matches a completion signal (case-insensitive):
     - "LGTM" → **approved** (for reviews)
     - "ANSWERED" → **answered** (for questions)
     - "CONCLUDED" → **concluded** (for discussions)
     - "DONE" → **done** (for custom)
   - If matched, mark as **responder complete**.
   - Otherwise, extract the response as **follow-up needed from responder**.

7. **Evaluate the response (questioner's perspective)**
   - After receiving Claude's response, Codex evaluates:
     - Does the response fully address the original question/concern?
     - Are there unclear points or ambiguities that need clarification?
     - Did new questions arise from the response?
   - Determine questioner status:
     - **Questioner satisfied**: No remaining questions or concerns.
     - **Questioner has follow-ups**: Additional questions or clarifications needed.

8. **Iteration loop**
   - **Continue iteration** if ANY of the following:
     - Responder signaled follow-up needed (no completion signal).
     - Questioner (Codex) has remaining questions or unclear points.
   - **Stop iteration** if BOTH:
     - Responder signaled complete (LGTM/ANSWERED/CONCLUDED/DONE), AND
     - Questioner (Codex) is satisfied (no remaining questions).
   - If continuing:
     - Report the response to the user.
     - If no completion signal was returned, explicitly ask for the completion signal (LGTM/ANSWERED/CONCLUDED/DONE) in the next reply.
     - For **question/discussion**: Formulate specific follow-up questions based on unclear points or new questions that arose.
     - For **change review**: Apply fixes to the code, then re-collect the diff and untracked files.
     - For **plan review**: Adjust the plan based on feedback, or ask for clarification on unclear feedback.
     - Update the consultation input with follow-up questions/context.
     - Return to step 4 and resubmit.
   - Maximum 10 iterations.

9. **Finish**
   - **Complete**: Report the full response content to the user (answer, conclusion, or review result), then note the completion status and proceed.
   - **Not complete after 10 rounds**: Report the current state and ask the user how to proceed.

## Auto-invocation

This skill is automatically invoked when:
- Codex exits plan mode (cross-review before execution).
- Codex completes any task with code changes (cross-review before proceeding).
- The user has not explicitly skipped the consultation.

Note: For ad-hoc consultations at any point, use `/ask-claude` manually.

## Command options

```sh
# Basic invocation with piped input
cat ~/.codex/plans/consultation-input.md | claude -p - --output-format text

# Alternative: direct prompt (for shorter content)
claude -p "<prompt>" --output-format text
```

## Notes

- Do not use `--dangerously-skip-permissions` for safety.
- Use `--output-format text` to get plain text output for parsing.
- Honor explicit user requests to skip the consultation.
- Plan files use the naming convention `plan-*.md` to distinguish from `consultation-input.md`.
- The consultation input file at `~/.codex/plans/consultation-input.md` persists for debugging and history.
- For change review, both `git diff` and untracked file contents are collected to ensure complete coverage.
- Completion signal detection uses exact line match (after trimming) to avoid false positives like "Not LGTM".
- Binary files and files larger than 100KB are skipped to avoid input bloat.
