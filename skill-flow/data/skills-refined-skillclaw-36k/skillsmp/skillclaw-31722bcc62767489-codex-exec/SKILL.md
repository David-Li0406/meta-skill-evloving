---
name: codex-exec
description: Use this skill to execute development tasks with OpenAI Codex CLI for code generation, refactoring, and bug fixes. Ideal when users request code modifications or automated code transformations.
---

# Skill body

## Prerequisites

- Ensure Codex CLI is installed and configured. Verify availability with:
  ```bash
  codex --version  # Should display installed version
  ```

## Workflow Checklist

1. **Understand the Task**
   - Clarify what needs to be created or modified.
   - Identify affected files and expected outcomes.

2. **Gather Context**
   - Check for uncommitted changes:
     ```bash
     git status
     ```
   - Review existing modifications:
     ```bash
     git diff
     ```

3. **Determine Execution Parameters**
   - Ask the user for execution parameters, including model and reasoning effort.

4. **Build Command**
   - Construct the command based on the task type:
     - For code modifications:
       ```bash
       codex exec --sandbox=workspace-write "[TASK]"
       ```
     - For code analysis or documentation:
       ```bash
       codex exec --sandbox=read-only "[TASK]"
       ```

5. **Execute Codex**
   - Run the command with appropriate flags:
     ```bash
     codex exec [OPTIONS] "PROMPT"
     ```
   - Essential flags may include:
     - `-m <MODEL>` for model selection
     - `-c model_reasoning_effort="<LEVEL>"`
     - `--skip-git-repo-check` if outside a git repository

6. **Verify Changes**
   - After execution, check for modifications:
     ```bash
     git status
     git diff
     ```
   - Validate code quality and run tests as necessary.

7. **Report Results**
   - Summarize the changes made, including modified files and verification results.

## Example Tasks

### Generate New Code
```bash
codex exec --sandbox=workspace-write "Create a UserProfile component in src/components/ with:
- Props: name (string), email (string), avatar (string optional)
- Display user info in a card layout
- Use TypeScript types"
```

### Analyze Existing Code
```bash
codex exec --sandbox=read-only "Analyze this code: $(cat /path/to/file.py)"
```