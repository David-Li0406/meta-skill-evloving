---
name: agent-instruction-maintenance
description: "Review, update, and synchronize agent instructions and configs across Codex and Claude (and optionally VS Code/Copilot); use when creating or refactoring agent prompts, skills, or chatmodes (trigger keywords: agent instructions, prompt review, skill update, chatmode, subagent)."
---

# Agent Instruction Maintenance

## What this skill does
- Audits agent instructions for clarity, correctness, and consistency.
- Validates frontmatter and minimal schemas for detected ecosystems.
- Aligns tool-specific variants while keeping behavior consistent.

## When to use it
- Trigger phrases: "agent instructions", "prompt review", "skill update", "chatmode", "subagent".
- Use after creating or editing instructions, or when standards change.

## Step-by-step workflow
1) Discover which ecosystems exist in the repo or user config.
2) Load local guidance (AGENTS.md, CLAUDE.md, copilot-instructions) when present.
3) Validate minimal frontmatter for each file type (see references).
4) Review content for clarity, scope, and actionability; remove ambiguity.
5) Ensure intent parity across tools while avoiding contradictions.
6) Keep instructions lean; move deep details into references.
7) Propose updates with before/after snippets and rationale.

## Default prioritization
- Prefer Codex-first guidance unless the user asks for tool-specific changes.
- Prefer Skills (SKILL.md) and AGENTS.md for portable, shared behavior.
- Apply tool-specific files only when a feature is unique to that tool.

## Tool-specific references
- Codex: `references/codex.md`
- Claude Opus: `references/claude-code.md`
- VS Code/Copilot (optional): `references/copilot-vscode.md`
- Tool choice (commands vs skills vs agents): `references/tool-selection.md`

## Expected outputs / formatting
- Summary of findings and risk areas.
- Required fixes (schema/format) vs recommended improvements (clarity/consistency).
- Proposed edits with brief rationale.
- Updated files when approved.

## Example prompts
- "Review our skills and normalize naming/trigger phrases."
- "Validate agent frontmatter across Claude and Copilot files."
- "Update Codex skills to match new project standards."
