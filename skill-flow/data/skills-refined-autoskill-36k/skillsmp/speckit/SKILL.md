---
name: speckit
description: Spec-driven development workflow (Speckit) for generating and maintaining specs, decisions, plans, tasks, and implementation guidance in repos that use specs/###-feature directories.
---

# Speckit spec-driven development

## Single command file

- The ONLY command file is `speckit/speckit.md`.
- All command routing and rules live there.

## Subcommands

- `new <feature description>` (default when no subcommand provided)
- `spec <feature folder>`
- `plan <feature folder>`
- `tasks <feature folder>`
- `implement <feature folder>`

## Question policy (strict)

- Ask questions only at the start and only for `spec.md`.
- Ask up to 5 questions total, all at once.
- After `spec.md` is written, do not ask more questions.

## Set the skill root

- Resolve repo root and set `SPECKIT_ROOT` to the absolute path of `speckit/`.
- Use `scripts/` and `assets/templates/` from this directory.

## Scripts

- Use `scripts/create-new-feature.sh` to create the feature folder and the four artifacts.

## Templates

- Only these templates are used:
  - `assets/templates/spec-template.md`
  - `assets/templates/decisions-template.md`
  - `assets/templates/plan-template.md`
  - `assets/templates/tasks-template.md`
