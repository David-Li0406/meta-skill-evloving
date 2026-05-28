---
name: diff-review
description: Use this skill when you want a second opinion on code changes from either Codex or Gemini, especially as a final check before committing.
---

# Diff Review via Codex or Gemini

Have Codex or Gemini review git changes for a second perspective on code quality.

## CRITICAL: Default Model

**ALWAYS use `model: "gpt-5.2"` for Codex** unless the user explicitly requests a different model. For Gemini, use the appropriate command as specified.

## CRITICAL: Instruct the Reviewer

Every prompt sent to Codex or Gemini MUST include these instructions:

> "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately."

## Quick Start (Codex)

If the `codex` MCP tool is available, first save the diff then review:

```bash
git diff --cached > codex-review.diff
```

```
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview the code changes at codex-review.diff for bugs, security issues, and style problems.",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

```bash
rm codex-review.diff
```

## Quick Start (Gemini)

If using Gemini, save the diff and review:

```bash
git diff --cached > gemini-review.diff
gemini "Review the code changes at gemini-review.diff for issues. Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
rm gemini-review.diff
```

## Patterns

**Staged changes:**
For Codex:
```bash
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview codex-review.diff for:\n1. Bugs or logic errors\n2. Security vulnerabilities\n3. Style inconsistencies\n4. Missing error handling",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

For Gemini:
```bash
git diff --cached > gemini-review.diff
gemini "Review gemini-review.diff for:
1. Bugs or logic errors
2. Security vulnerabilities
3. Style inconsistencies
4. Missing error handling
Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
rm gemini-review.diff
```

**All uncommitted changes (Gemini):**
```bash
git diff HEAD > gemini-review.diff
gemini "Review gemini-review.diff. Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
rm gemini-review.diff
```

**Specific commit (Gemini):**
```bash
git show abc123 > gemini-review.diff
gemini "Review the commit at gemini-review.diff. Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
rm gemini-review.diff
```

## Focused Reviews

**Security focus (Codex):**
```bash
git diff --cached > codex-review.diff
mcp__plugin_codex_cli__codex({
  "prompt": "Security review of codex-review.diff. Check for:\n- XSS vulnerabilities\n- SQL/command injection\n- Sensitive data exposure\n- Authentication/authorization issues\nDo not make any changes. Provide your complete feedback immediately.",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

**Security focus (Gemini):**
```bash
git diff --cached > gemini-review.diff
gemini "Security review of gemini-review.diff. Check for:
- XSS vulnerabilities
- SQL/command injection
- Sensitive data exposure
- Authentication/authorization issues
Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
rm gemini-review.diff
```