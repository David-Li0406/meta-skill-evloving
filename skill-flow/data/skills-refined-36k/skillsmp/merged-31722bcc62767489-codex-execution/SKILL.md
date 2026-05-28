---
name: codex-execution
description: Use this skill when you need to execute development tasks involving code analysis, refactoring, and automated editing with OpenAI Codex CLI.
---

# Codex Execution Skill

## Prerequisites
- Codex CLI installed and configured (`~/.codex/config.toml`)
- Verify availability: `codex --version` on first use per session

## When to Use
- User requests to "add", "create", "implement", or "generate" code
- User wants to refactor existing code
- User needs to fix a bug
- User asks for code analysis or review
- User requests automated code transformations

## Workflow Checklist

1. **Detect Environment**:
   - Check if running on HPC cluster (look for `/home/woody/`, `/home/hpc/`, Slurm env vars)
   - If HPC detected: **Always use `--yolo` flag to bypass Landlock sandbox restrictions**

2. **Gather Execution Parameters**:
   - Ask user for model and reasoning effort (e.g., `gpt-5.2`, `high`)

3. **Determine Sandbox Mode**:
   - `read-only`: For code analysis and review
   - `workspace-write`: For code modifications
   - `danger-full-access`: For system operations (use with caution)

4. **Build Command**:
   ```bash
   codex exec [OPTIONS] "PROMPT"
   ```
   Essential flags:
   - `-m <MODEL>` (if overriding default)
   - `-c model_reasoning_effort="<LEVEL>"`
   - `-s <SANDBOX_MODE>` (skip on HPC)
   - `--skip-git-repo-check` (if outside git repo)

5. **Execute with Stderr Suppression**:
   - Append `2>/dev/null` to hide thinking tokens unless user requests verbose output.

6. **Validate Execution**:
   - Check exit code (0 = success)
   - Summarize output for user
   - Report errors with actionable solutions

7. **Inform about Resume Capability**:
   - "Resume this session anytime: `codex resume`"

## Command Patterns

### Read-Only Analysis
```bash
codex exec -m gpt-5.2 -c model_reasoning_effort="medium" -s read-only \
  --skip-git-repo-check --full-auto "review @file.py for security issues" 2>/dev/null
```

### Code Modification
```bash
codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" -s workspace-write \
  --skip-git-repo-check --full-auto "refactor @module.py to async/await" 2>/dev/null
```

### HPC/Slurm Environment (YOLO Mode)
```bash
codex exec --yolo -m gpt-5.2 -c model_reasoning_effort="high" --skip-git-repo-check \
  "Analyze this code: $(cat /path/to/file.py)" 2>/dev/null
```

### Resume Session
```bash
echo "fix the remaining issues" | codex exec --skip-git-repo-check resume --last 2>/dev/null
```

## Best Practices

- Be specific in task descriptions, including file paths and expected behavior.
- Always verify changes with `git diff` and run linter/tests.
- Use `--yolo` on HPC clusters to avoid Landlock errors.
- Avoid using `--full-auto` with `--yolo` as they are incompatible.

## Error Handling

1. **If execution fails**:
   - Check the error message and verify Codex authentication.
   - Try with more specific instructions or break the task into smaller steps.

2. **If changes are incorrect**:
   - Revert: `git restore .` or `git restore <file>`
   - Re-execute with better instructions or fix manually.

3. **If tests fail**:
   - Review what broke and ask Codex to fix the test failures or fix manually.

## Safety Guidelines

- Always verify before using `danger-full-access` sandbox.
- Request user approval for high-impact flags and destructive operations.

## Common Workflows

### Code Review Workflow
1. Ask user for model and reasoning effort.
2. Run read-only analysis.
3. Present findings and propose changes if needed.
4. Validate changes and inform about resume capability.

### Refactoring Workflow
1. Analyze current code (read-only).
2. Propose changes and get user approval.
3. Apply changes (workspace-write) and run validation/tests.

### Security Audit Workflow
1. Run comprehensive analysis (read-only).
2. Document findings and propose fixes.
3. Apply fixes if approved (workspace-write) and re-audit to verify.

**Remember**: This skill MODIFIES code and performs analysis. Always review changes before committing!