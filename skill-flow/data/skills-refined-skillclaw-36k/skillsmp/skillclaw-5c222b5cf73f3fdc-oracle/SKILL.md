---
name: oracle
description: Use the @steipete/oracle CLI to bundle a prompt with selected files for a second-model review, enabling debugging, refactoring, design checks, or cross-validation.
---

# Oracle (CLI) — Best Use

Oracle allows you to bundle your prompt and selected files into a single request, enabling another model to provide insights with real repository context. Outputs should be treated as advisory and verified against the codebase and tests.

## When to Use
- You need a second-model review with real repository context.
- You want to perform multi-model comparisons for risk assessment.
- You require browser automation runs against ChatGPT or similar models.

## Recommended Workflow
1. **Select Files**: Choose a minimal set of files that contain the necessary context.
2. **Preview Your Request**: Use `--dry-run` to check what will be sent.
3. **Run the Command**: Execute in browser mode for the usual workflow, using API mode only when necessary.
4. **Handle Timeouts**: If the run detaches or times out, reattach to the stored session instead of re-running.

## Commands
- **Show Help**: 
  ```bash
  npx -y @steipete/oracle --help
  ```
- **Preview Request**: 
  ```bash
  npx -y @steipete/oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"
  ```
- **Run in Browser Mode**: 
  ```bash
  npx -y @steipete/oracle --engine browser --model gpt-5.2-pro -p "<task>" --file "src/**"
  ```
- **Manual Paste Fallback**: 
  ```bash
  npx -y @steipete/oracle --render --copy -p "<task>" --file "src/**"
  ```

## File Attachment Guidelines
- **Include Files**: Use `--file` to specify files, directories, or globs.
- **Exclude Files**: Prefix with `!` to exclude specific files or patterns.

## Anti-Patterns
- Avoid attaching secrets or `.env` files.
- Do not re-run after a timeout; always reattach to the session.
- Use browser mode only when necessary; prefer API mode for reliability.

## Outputs
- The Oracle response with cited context.
- Optional rendered bundle for manual pasting.
- Session metadata for reference.