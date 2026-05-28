---
name: code-review
description: Use this skill to get a second opinion on code changes from either Codex or Gemini after edits are made, or as a final check before committing.
---

# Code Review via Codex or Gemini

Have Codex or Gemini review git changes for a second perspective on code quality.

## Default Model

**For Codex:** Always use `model: "gpt-5.2"` unless a different model is explicitly requested.

## Instruct the Reviewer

Every prompt sent to Codex or Gemini must include instructions to not make changes and to provide feedback only.

### Codex Instructions
> "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately."

### Gemini Instructions
> "Do not make any changes. Respond with feedback only."

## Quick Start

1. Save the diff to the project root.
2. Review the changes using the appropriate tool.
3. Clean up the diff file after review.

### For Codex
```bash
git diff --cached > codex-review.diff
mcp__plugin_codex_cli__codex({
  "prompt": "Review the code changes at codex-review.diff for bugs, security issues, and style problems.",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
rm codex-review.diff
```

### For Gemini
```bash
git diff --cached > gemini-review.diff
gemini "Review the code changes at gemini-review.diff for issues. Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
rm gemini-review.diff
```

## Focused Reviews

### Staged Changes
**Codex:**
```bash
mcp__plugin_codex_cli__codex({
  "prompt": "Review codex-review.diff for:\n1. Bugs or logic errors\n2. Security vulnerabilities\n3. Style inconsistencies\n4. Missing error handling",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

**Gemini:**
```bash
gemini "Review gemini-review.diff for:
1. Bugs or logic errors
2. Security vulnerabilities
3. Style inconsistencies
4. Missing error handling
Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

### Security Focus
**Codex:**
```bash
mcp__plugin_codex_cli__codex({
  "prompt": "Security review of codex-review.diff. Check for:\n- XSS vulnerabilities\n- SQL/command injection\n- Sensitive data exposure\n- Authentication/authorization issues",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

**Gemini:**
```bash
gemini "Security review of gemini-review.diff. Check for:
- XSS vulnerabilities
- SQL/command injection
- Sensitive data exposure
- Authentication/authorization issues
Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

### Performance Focus
**Codex:**
```bash
mcp__plugin_codex_cli__codex({
  "prompt": "Performance review of codex-review.diff. Check for:\n- Inefficient algorithms\n- N+1 queries\n- Memory leaks\n- Blocking operations",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

**Gemini:**
```bash
gemini "Performance review of gemini-review.diff. Check for:
- Inefficient algorithms
- N+1 queries
- Memory leaks
- Blocking operations
Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

## Notes

- Always use `sandbox: "read-only"` for Codex to prevent file modifications.
- Gemini respects `.gitignore` and cannot read files matching gitignore patterns.
- Requires `dangerouslyDisableSandbox: true` for Bash calls.
- Clean up the diff file after review.
- Performance may vary based on the tool used and the complexity of the review.