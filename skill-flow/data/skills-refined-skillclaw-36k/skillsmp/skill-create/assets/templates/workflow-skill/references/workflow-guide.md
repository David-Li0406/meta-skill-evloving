# Workflow Skill Guide

Use this template for skills that guide sequential, repeatable procedures (deployments, code reviews, migrations).

## Structure
- Frontmatter: name + third-person description with clear triggers
- When to Use: triggers and anti-patterns
- Workflow: numbered steps with checkpoints and inputs/outputs
- Verification: commands or checks to confirm completion
- References/Scripts: point to deeper docs or helpers

## Checklist
- [ ] Steps are ordered and actionable
- [ ] Each step notes expected inputs/outputs
- [ ] Verification commands are runnable
- [ ] Long-form guidance moved to references/
- [ ] Scripts referenced for repeated actions

## Example Triggers
- "This skill should be used when performing a multi-env deploy"
- "Use when auditing a PR end-to-end (tests, diff review, rollout plan)"

## Example Steps
1. Collect context (branch, ticket, owner)
2. Outline scope and risks
3. Execute actions with checkpoints (e.g., run tests, apply migrations)
4. Verify outcomes and capture results
5. Record follow-ups

## Anti-Patterns
- Single-step tasks that don't benefit from structure
- Embedding long rationales in SKILL.md (move to references)
- Vague descriptions that don't mention triggers
