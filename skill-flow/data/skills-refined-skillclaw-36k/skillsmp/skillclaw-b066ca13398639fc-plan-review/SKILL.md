---
name: plan-review
description: Use this skill when you need a second opinion on an implementation plan, whether from Codex or Gemini, to ensure completeness and identify potential risks before proceeding.
---

# Plan Review via Codex or Gemini

Have Codex or Gemini critique implementation plans for a second perspective.

## CRITICAL: Default Model

**ALWAYS use `model: "gpt-5.2"`** for Codex unless the user explicitly requests a different model. For Gemini, ensure the appropriate tools are allowed.

## Instructing the Model

Every prompt sent to Codex or Gemini MUST include these instructions:

> "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately."

## Quick Start (Codex)

If the `codex` MCP tool is available, read the plan and pass it to Codex:

```bash
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview this implementation plan:\n\n[PLAN CONTENT HERE]\n\nConsider:\n1. Are there gaps or missing steps?\n2. Are there risks not addressed?\n3. Is the approach optimal?\n4. What alternatives should be considered?",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

## Quick Start (Gemini)

If using Gemini, pipe the plan content via stdin:

```bash
cat ~/.claude/plans/example-plan.md | gemini "Review this implementation plan:

\$(cat)

Consider:
1. Are there gaps or missing steps?
2. Are there risks not addressed?
3. Is the approach optimal?
4. What alternatives should be considered?

Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

## With Source Context

Include source files for context in the prompt:

For Codex:
```bash
mcp__plugin_codex_cli__codex({
  "prompt": "You are running non-interactively as part of a script. Do not ask questions or wait for input. Do not make any changes. Provide your complete feedback immediately.\n\nReview this implementation plan:\n\n[PLAN CONTENT HERE]\n\nAlso read these source files for context:\n- [SOURCE FILES HERE]",
  "sandbox": "read-only",
  "model": "gpt-5.2"
})
```

For Gemini:
```bash
cat ~/.claude/plans/example-plan.md | gemini "Review this implementation plan:

\$(cat)

Also read these source files for context:
- [SOURCE FILES HERE]

Evaluate if the plan addresses the actual codebase structure. Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

## Focused Reviews

**Risk assessment:**
```bash
cat ~/.claude/plans/migration.md | gemini "Review this plan for risks:

\$(cat)

Evaluate:
- Breaking changes
- Data loss potential
- Rollback complexity
- Dependencies that could fail

Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```

**Completeness check:**
```bash
cat ~/.claude/plans/feature.md | gemini "Review this plan for completeness:

\$(cat)

Evaluate:
- Are all edge cases covered?
- Is testing addressed?
- Are there missing steps?

Do not make any changes. Respond with feedback only." --allowed-tools read_file,codebase_investigator,glob,search_file_content,list_directory,write_todos -o text 2>&1
```