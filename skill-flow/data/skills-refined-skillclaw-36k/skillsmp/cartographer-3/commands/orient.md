---
model: haiku
allowed-tools: Read, Write, Bash(test:*), AskUserQuestion
argument-hint: [--reset]
description: Add minimal atlas awareness to CLAUDE.md (for human readers)
---

## Context

Arguments: `/cartographer:orient [OPTIONS]`
- **--reset** - Remove existing atlas section and regenerate
- **(empty)** - Add/update atlas section preserving existing content

Current directory: !`pwd`

## Workflow

### 1. Pre-flight Checks

**Check if CLAUDE.md exists:**
```bash
test -f "CLAUDE.md" && echo "EXISTS" || echo "NOT_FOUND"
```

**Check if atlas exists:**
```bash
test -f ".claude/skills/atlas/SKILL.md" && echo "EXISTS" || echo "NOT_FOUND"
```

### 2. Determine Action

**If CLAUDE.md doesn't exist:**
- Create new CLAUDE.md with atlas section

**If CLAUDE.md exists:**
- Check for existing atlas section markers:
  - `<!-- atlas:start -->`
  - `<!-- atlas:end -->`
- If markers exist and not --reset: Update between markers
- If markers exist and --reset: Remove section, regenerate
- If no markers: Add new section at appropriate location

### 3. Generate Atlas Section

**Create atlas section:**

```markdown
<!-- atlas:start -->
This project has an atlas skill at `.claude/skills/atlas/` for codebase navigation.
<!-- atlas:end -->
```

That's it. Claude auto-discovers the skill. This marker is for humans and for `/cartographer:health` to detect setup state.

### 4. Update CLAUDE.md

**If creating new:**
```markdown
# {Project Name}

{atlas_section}

## Development

{placeholder for user to add}
```

**If updating existing:**

1. Find insertion point:
   - After title/description
   - Before first major section
   - Or at end if structure unclear

2. Insert/replace atlas section

3. Preserve all other content

### 5. Handle Conflicts

**If malformed markers found:**
```
⚠️ Found malformed atlas section markers in CLAUDE.md

Current state:
{show markers found}

Options:
1. Fix markers and update atlas section
2. Remove all atlas markers and regenerate
3. Show me the file for manual fix
4. Abort
```

**If multiple marker pairs:**
```
⚠️ Multiple atlas sections found in CLAUDE.md

This may cause issues. Options:
1. Keep first section, remove others
2. Remove all and add single section
3. Show me the file for manual fix
4. Abort
```

### 6. Report Results

**Success:**
```markdown
## CLAUDE.md Updated

**Action:** {Created | Updated | Reset}
**Atlas section:** Lines {start}-{end}

The atlas section is intentionally minimal. Full navigation data lives in:
- `.claude/skills/atlas/SKILL.md` (auto-discovered)
- `.claude/skills/atlas/references/schema.yaml`
```

**If atlas not found:**
```markdown
## CLAUDE.md Updated (Placeholder)

**Note:** Atlas not found at `.claude/skills/atlas/`

Added placeholder section. Run `/cartographer:chart` to generate atlas.
```

---

## Section Format

The atlas section uses HTML comments as markers for reliable detection:

```markdown
<!-- atlas:start -->
{content}
<!-- atlas:end -->
```

This allows:
- Easy detection for updates
- Clean rendering (markers hidden in preview)
- Preservation during manual edits

---

## Error Handling

| Error | Action | Recovery |
|-------|--------|----------|
| Can't write CLAUDE.md | Report permission error | User fixes permissions |
| Malformed markers | Interactive prompt | User chooses fix |
| Multiple sections | Interactive prompt | User chooses resolution |
| Atlas not found | Add placeholder | User runs chart then orient |

## Responsibilities

**YOU (handler):**
- Check CLAUDE.md state
- Add/update minimal atlas awareness section
- Preserve all other CLAUDE.md content
- Handle conflicts interactively

**Keep it minimal.** The atlas section is for human readers. Claude discovers the skill automatically via `.claude/skills/atlas/SKILL.md`.
