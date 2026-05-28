---
name: commit
description: Commit with user prompts from this conversation. Use when user mentions committing, wants to commit changes, asks to save their work to git, or says "commit this".
allowed-tools: Bash, Read
---

# Commit with User Prompts

Create git commits that include the user prompts that led to the changes.

## Instructions

1. **Extract User Prompts**: Collect user messages from this conversation that led to the changes. Include them in chronological order.

2. **Analyze Changes**:
   ```bash
   git status
   git diff --staged
   ```

3. **Get Session Info**:
   ```bash
   uv run {baseDir}/ai-blame.py session-info
   ```

4. **Generate Commit Message**:
   ```
   <brief summary of changes>

   User prompts:
   - "<first user prompt>"
   - "<second user prompt>" (context if prompt is ambiguous)

   AI-Session-ID: <from session-info>
   AI Agent: <from session-info>
   Model: <from session-info>
   ```

5. **Execute Commit**:
   ```bash
   git add -A && git commit -m "$(cat <<'EOF'
   <your commit message here>
   EOF
   )"
   ```

## Rules

- Only include prompts that led to file changes (not `/commit` or meta-discussion)
- Preserve exact wording, add (context) in parentheses if prompt is ambiguous
- Summary line under 50 characters
- Each prompt on a single line, no mid-sentence wrapping
