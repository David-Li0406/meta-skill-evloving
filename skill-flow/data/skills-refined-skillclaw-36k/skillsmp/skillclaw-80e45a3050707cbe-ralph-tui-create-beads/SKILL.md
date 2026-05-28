---
name: ralph-tui-create-beads
description: Use this skill when you have a PRD and want to convert it into beads for ralph-tui execution, creating an epic with child beads for each user story.
---

# Ralph TUI - Create Beads

This skill converts PRDs (Product Requirement Documents) into beads (epics and child tasks) for ralph-tui autonomous execution.

> **Note:** This skill is bundled with ralph-tui's Beads tracker plugin. Future tracker plugins (Linear, GitHub Issues, etc.) will bundle their own task creation skills.

## The Job

Take a PRD (markdown file or text) and create beads in `.beads/beads.jsonl`:
1. **Extract Quality Gates** from the PRD's "Quality Gates" section.
2. Create an **epic** bead for the feature.
3. Create **child beads** for each user story (with quality gates appended).
4. Set up **dependencies** between beads (schema → backend → UI).
5. Output ready for `ralph-tui run --tracker beads`.

## Step 1: Extract Quality Gates

Look for the "Quality Gates" section in the PRD:

```markdown
## Quality Gates

These commands must pass for every user story:
- `pnpm typecheck` - Type checking
- `pnpm lint` - Linting

For UI stories, also include:
- Verify in browser using dev-browser skill
```

Extract:
- **Universal gates:** Commands that apply to ALL stories (e.g., `pnpm typecheck`).
- **UI gates:** Commands that apply only to UI stories (e.g., browser verification).

**If no Quality Gates section exists:** Ask the user what commands should pass, or use a sensible default like `npm run typecheck`.

## Output Format

Beads use `bd create` command:

```bash
# Create epic (link back to source PRD)
bd create --type=epic \
  --title="[Feature Name]" \
  --description="[Feature description from PRD]" \
  --external-ref="prd:./tasks/feature-name-prd.md" \
  --labels="ralph,feature"

# Create child bead (with quality gates in acceptance criteria)
bd create \
  --parent=EPIC_ID \
  --title="[Story Title]" \
  --description="[Story description with acceptance criteria INCLUDING quality gates]" \
  --priority=[1-4] \
  --labels="ralph,task"
```

## Story Size: The #1 Rule

**Each story must be completable in ONE ralph-tui iteration (~one agent context window).**

ralph-tui spawns a fresh agent instance per iteration with no memory of previous work. If a story is too big, the agent runs out of context before finishing.

### Right-sized stories:
- Add a database column + migration.
- Add a UI component to an existing page.
- Update an existing API endpoint.