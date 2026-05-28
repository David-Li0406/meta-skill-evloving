---
name: plan-review
description: Use this skill when you need a second opinion on implementation plans from either Codex or Gemini, especially after creating a plan file that requires validation before implementation.
---

# Plan Review via Codex and Gemini

Have Codex or Gemini critique implementation plans for a second perspective.

## Default Model for Codex

**ALWAYS use `model: "gpt-5.2"`** for Codex unless a different model is explicitly requested. Do NOT choose `o3` or other models on your own.

## Instructing Codex

Every prompt sent to Codex MUST include these instructions:

> "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately."

Codex acts as a consultant, while Claude Code handles all file modifications.

## Quick Start for Codex

If the `codex` MCP tool is available, read the plan and pass it to Codex:

```javascript
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview this implementation plan:\n\n[PLAN CONTENT HERE]\n\nConsider:\n1. Are there gaps or missing steps?\n2. Are there risks not addressed?\n3. Is the approach optimal?\n4. What alternatives should be considered?",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

If MCP is unavailable, use the Bash fallback:

```bash
codex exec "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.

Review the implementation plan at <path_to_plan_file>

Consider:
1. Are there gaps or missing steps?
2. Are there risks not addressed?
3. Is the approach optimal?" --sandbox read-only -m gpt-5.2-codex 2>&1
```

## Quick Start for Gemini

For Gemini, pipe the plan content via stdin since it cannot read files outside the project directory:

```bash
cat <path_to_plan_file> | gemini "Review this implementation plan:

\$(cat)

Consider:
1. Are there gaps or missing steps?
2. Are there risks not addressed?
3. Is the approach optimal?
4. What alternatives should be considered?

Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

## With Source Context

For both Codex and Gemini, include source files for context in the prompt:

```javascript
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview this implementation plan:\n\n[PLAN CONTENT]\n\nAlso read these source files for context:\n- src/auth/login.ts\n- src/middleware/session.ts\n\nEvaluate if the plan addresses the actual codebase structure.",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

For Gemini:

```bash
cat <path_to_plan_file> | gemini "Review this implementation plan:

\$(cat)

Also read these source files for context:
- src/auth/login.ts
- src/middleware/session.ts

Evaluate if the plan addresses the actual codebase structure. Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

## Focused Reviews

### Risk Assessment

For Codex:

```javascript
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview this plan for risks:\n\n[PLAN CONTENT]\n\nEvaluate:\n- Breaking changes\n- Data loss potential\n- Rollback complexity\n- Dependencies that could fail",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

For Gemini:

```bash
cat <path_to_plan_file> | gemini "Review this plan for risks:

\$(cat)

Evaluate:
- Breaking changes
- Data loss potential
- Rollback complexity
- Dependencies that could fail

Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

### Completeness Check

For Codex:

```javascript
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview this plan for completeness:\n\n[PLAN CONTENT]\n\nEvaluate:\n- Are all edge cases covered?\n- Is testing addressed?\n- Are there missing steps?",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

For Gemini:

```bash
cat <path_to_plan_file> | gemini "Review this plan for completeness:

\$(cat)

Evaluate:
- Are all edge cases covered?
- Is testing addressed?
- Are there missing steps?

Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

## Notes

- **Always use `sandbox: "read-only"`** for Codex to prevent file modifications.
- **Gemini must not make any changes, provide feedback ONLY.**
- Ensure to pipe plan content via stdin for Gemini using `$(cat)` as it cannot read files directly.
- Both tools may take 2-3 minutes for thorough reviews, especially with source analysis.
- See `references/setup.md` for troubleshooting.