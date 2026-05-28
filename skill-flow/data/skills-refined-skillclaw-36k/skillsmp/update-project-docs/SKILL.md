---
name: update-project-docs
description: |
  Keep CLAUDE.md and AGENTS.md current after significant project changes. Use
  proactively when: (1) adding new modules, packages, or top-level directories,
  (2) changing build/test commands or tooling, (3) renaming/moving/deleting
  files referenced in CLAUDE.md, (4) introducing new conventions or patterns,
  (5) reorganizing document structure, (6) adding dependencies requiring setup
  steps. Invoke when user mentions CLAUDE.md, AGENTS.md, project docs update,
  or after completing architectural changes.
---

# Update Project Docs

Keep CLAUDE.md and AGENTS.md current so future AI sessions start with accurate
project context.

## When to Trigger

Activate after completing changes that affect how someone navigates or works in
the project. Both conditions must hold:

1. The project contains a CLAUDE.md or AGENTS.md (if not, skip)
2. The changes meet the significance threshold below

### Significance Threshold

**Trigger (update needed):**
- New modules, packages, or top-level directories
- Renamed/moved/deleted files that CLAUDE.md references
- Changed build commands, test commands, or tooling
- New conventions or patterns introduced
- API/interface changes affecting documented entry points
- Document structure reorganization (text projects)
- New dependencies that require setup steps

**Skip (too small to trigger):**
- Bug fixes within existing architecture
- Adding content within existing structure
- Minor refactors (rename variable, extract small helper)
- Test additions following existing patterns
- Typo fixes, formatting changes

## Workflow

1. **Check for docs** — Locate CLAUDE.md or AGENTS.md in the project root. If
   neither exists, stop.

2. **Review what changed** — Use `git diff` or recall the changes just made.
   Identify which aspects affect project navigation or workflow.

3. **Read current docs** — Load the existing CLAUDE.md/AGENTS.md to understand
   its structure and voice.

4. **Identify stale/missing sections** — Compare the current project state
   against what the docs describe. Look for:
   - Sections referencing renamed/deleted files
   - Missing entries for new modules or directories
   - Outdated build/test/lint commands
   - Conventions that no longer apply

5. **Update** — Edit the docs following the Update Principles below. Preserve
   the existing document style.

6. **Show the user** — Summarize what was updated and why, so the user can
   verify the changes make sense.

## Update Principles

### What to Add

- New module/directory descriptions (one line each)
- Changed build, test, or lint commands
- New conventions or patterns that future sessions should follow
- Setup steps for new dependencies
- Updated file paths for moved/renamed files

### What NOT to Add

- Implementation details (that's what code is for)
- Temporary workarounds or TODOs
- Information already obvious from file names
- Content that duplicates README.md

### Style Guidelines

- **Match existing voice** — If the file is terse, stay terse. If it uses full
  sentences, use full sentences.
- **Keep it scannable** — Prefer bullet lists over prose paragraphs
- **Remove stale info** — Deleting outdated content is as important as adding
  new content. A shorter, accurate file beats a longer, stale one.
- **Preserve structure** — Add new items to existing sections rather than
  creating new sections, unless the change introduces an entirely new category.
- **Be specific** — "Run `make test-integration`" not "run the integration
  tests"

### Scope

- Update only project-level CLAUDE.md/AGENTS.md, not workspace or global files
- If both CLAUDE.md and AGENTS.md exist, update whichever contains the relevant
  section (or both if the information belongs in both)
- Never create a CLAUDE.md/AGENTS.md if one doesn't already exist — that's the
  user's decision

## Reference Files

| File | Content |
|------|---------|
| `references/update-examples.md` | Before/after examples for common scenarios |
