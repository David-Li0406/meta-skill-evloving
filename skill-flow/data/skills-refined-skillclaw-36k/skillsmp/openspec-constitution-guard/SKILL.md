---
name: openspec-constitution-guard
description: This skill composes project AGENTS.md constitution files into openspec commands (apply, archive, proposal) to enforce quality validation gates before handoff. Use this skill when initializing openspec for the first time in a project or when AGENTS.md files are updated. The skill ensures openspec artifacts are validated against project-specific quality criteria from constitutions.
tags:
  - openspec
  - constitution
  - meta-skill
  - close-loop
---

# OpenSpec Constitution Guard

This skill ensures openspec commands enforce project-specific quality assurance criteria derived from AGENTS.md constitution files.

## Purpose

OpenSpec commands (`apply`, `archive`, `proposal`) include generic validation. This skill enriches them with **project-specific quality gates** extracted from AGENTS.md files across the workspace, ensuring all artifacts pass the project's defined testing and QA criteria before handoff.

## When to Use

Trigger this skill when:
- Initializing openspec for the first time in a project (`openspec init`)
- An AGENTS.md file is created, modified, or deleted in the project
- User explicitly requests to sync constitution quality gates with openspec commands
- Validating that openspec commands are up-to-date with constitution requirements

## Detection: When to Run

To detect if guards need composition:
1. Check if `.claude/commands/openspec/*.md` files exist
2. Look for `<!-- CONSTITUTION:START` marker in each command file
3. If marker is missing → first-time setup needed
4. If AGENTS.md files have changed since `Last Updated` date → refresh needed

## Workflow

### Step 1: Locate All Constitution Files

Find all AGENTS.md files in the workspace:
```bash
find . -name "AGENTS.md" -type f | grep -v node_modules | grep -v .venv | grep -v target | grep -v openspec/AGENTS.md
```

**Exclude** `openspec/AGENTS.md` as it contains OpenSpec usage instructions already referenced by the commands, not project-specific quality criteria.

Read each remaining file to understand its scope (root project, backend, frontend, specific module, etc.).

### Step 2: Read and Understand Quality Criteria

For each AGENTS.md file, identify sections related to quality assurance. Look for:
- Headings containing: "Quality", "Testing", "Checks", "Validation", "Assurance", "Checklist"
- Command examples (typically in backticks or code blocks)
- Goals or acceptance criteria (e.g., "Zero errors", "All tests pass")
- Architecture patterns and coding standards that should be enforced

**Key information to extract:**
1. **Automated commands** - What tools/commands must be run (e.g., `pytest`, `npm run lint`)
2. **Success criteria** - What constitutes passing (e.g., "zero warnings")
3. **Architecture rules** - Patterns that must be followed (e.g., "service layer separation")
4. **Testing requirements** - Coverage expectations, test types needed
5. **Stack identification** - What technology stack does this constitution govern

### Step 3: Interpret Criteria for Each Command

Map the extracted criteria to specific OpenSpec actions:

#### For `proposal` Command
Extract rules that validate **design decisions**:
- Architecture patterns that must be followed
- Type safety requirements
- Naming conventions
- What requires a proposal vs direct fix
- Breaking change documentation requirements

#### For `apply` Command
Extract rules that validate **implementation quality**:
- All automated check commands (linters, type checkers, test runners)
- Per-stack commands with their success criteria
- Code style requirements
- Documentation requirements

#### For `archive` Command
Extract rules that validate **completion criteria**:
- Task verification requirements
- Test coverage expectations
- Integration/E2E test requirements
- Manual verification scenarios (if mentioned)
- Spec accuracy validation

### Step 4: Compose the Guard Block

For each openspec command file, create a constitution guard block following this template:

```markdown
<!-- CONSTITUTION:START - Auto-generated from AGENTS.md files -->
**Quality Gate (from Project Constitutions)**

Before completing this command, verify against project quality criteria:

[ACTION-SPECIFIC QUALITY GATE CONTENT]

**Source Constitutions:**
- [List each AGENTS.md file path]

**Last Updated:** [YYYY-MM-DD]
<!-- CONSTITUTION:END -->
```

The `[ACTION-SPECIFIC QUALITY GATE CONTENT]` should be a clear, actionable checklist derived from the constitutions.

### Step 5: Update Command Files

For each command in `.claude/commands/openspec/`:

1. Read the current content of the command file
2. Locate the `<!-- OPENSPEC:END -->` marker
3. Check for existing constitution block (`<!-- CONSTITUTION:START` to `<!-- CONSTITUTION:END -->`)
4. If existing block found, replace it entirely
5. If no existing block, append after `<!-- OPENSPEC:END -->`
6. Ensure exactly one blank line between `<!-- OPENSPEC:END -->` and the constitution block

**Critical**: Place the guard block AFTER `<!-- OPENSPEC:END -->` so it survives `openspec update` operations.

## Example Outputs

### Example: Proposal Guard

After reading constitutions that mention "service layer separation", "strict typing", and "Pydantic models":

```markdown
<!-- CONSTITUTION:START - Auto-generated from AGENTS.md files -->
**Quality Gate (from Project Constitutions)**

Before completing this command, verify against project quality criteria:

**Proposal Quality Gate:**
Before finalizing the proposal, verify alignment with project constitutions:

1. Verify service layer separation is maintained (business logic in services/, not api/)
2. Ensure strict typing requirements are addressed in design (no `Any`/`any` types)
3. Use Pydantic models for new data structures
4. Verify breaking changes are marked with **BREAKING** in proposal.md

**Source Constitutions:**
- AGENTS.md
- backend/AGENTS.md

**Last Updated:** 2026-01-15
<!-- CONSTITUTION:END -->
```

### Example: Apply Guard

After reading constitutions with Python, TypeScript, and Rust commands:

```markdown
<!-- CONSTITUTION:START - Auto-generated from AGENTS.md files -->
**Quality Gate (from Project Constitutions)**

Before completing this command, verify against project quality criteria:

**Apply Quality Gate:**
Before marking tasks complete, run all relevant checks based on changed code:

**Python (backend/):**
- `uv run pytest` - All tests must pass
- `uv run ruff check .` - Zero linting errors
- `uv run pyright .` - Zero type errors

**TypeScript/React (frontend/):**
- `npm run lint` - Fix all ESLint errors
- `npm run tsc` - Zero transpilation errors
- `npx playwright test` - E2E tests pass for affected features

**Cross-Cutting:**
- Verify service layer separation (logic in services/, not api/)
- Confirm strict typing (no `any`/`Any` types)
- Add unit tests for new service logic

**Source Constitutions:**
- AGENTS.md
- backend/AGENTS.md
- frontend/AGENTS.md

**Last Updated:** 2026-01-15
<!-- CONSTITUTION:END -->
```

### Example: Archive Guard

```markdown
<!-- CONSTITUTION:START - Auto-generated from AGENTS.md files -->
**Quality Gate (from Project Constitutions)**

Before completing this command, verify against project quality criteria:

**Archive Quality Gate:**
Before archiving, confirm all acceptance criteria are met:

1. All tasks in `tasks.md` are marked `[x]` and verified complete
2. All automated checks pass (run the Apply Quality Gate checks)
3. Integration tests cover the new behavior
4. No regression in existing tests
5. Spec deltas accurately reflect the implemented changes
6. `openspec validate <id> --strict` passes
7. Manual sanity verification performed for UI/streaming scenarios (if applicable)

**Source Constitutions:**
- AGENTS.md
- backend/AGENTS.md
- frontend/AGENTS.md

**Last Updated:** 2026-01-15
<!-- CONSTITUTION:END -->
```

## Interpretation Guidelines

When reading AGENTS.md files with varying structures:

1. **Look for imperative language**: "MUST", "SHALL", "required", "always"
2. **Identify command patterns**: Anything in backticks that looks like a shell command
3. **Find success criteria**: Phrases like "zero errors", "all pass", "no warnings"
4. **Recognize stack indicators**: Framework names, file extensions, folder names
5. **Extract checklists**: Bullet points with checkboxes or numbered items

If a constitution section is ambiguous, interpret conservatively—include the check rather than omit it.

All command level constitution items should derived from project AGENTS.md files only, **DO NOT** include OpenSpec's own AGENTS.md or any common sense or best practices from other materials.

## Maintenance

When updating guards:
1. Re-read all AGENTS.md files
2. Compare with existing guard blocks
3. Update only what has changed
4. Preserve any manual additions (if marked with comments)
5. Update the `Last Updated` timestamp
