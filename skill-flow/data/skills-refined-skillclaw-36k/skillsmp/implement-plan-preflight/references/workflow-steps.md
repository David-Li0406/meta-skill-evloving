**Skill**: [Implement Plan Preflight](../SKILL.md)

# Preflight Workflow Steps

Sequential execution steps for the Preflight phase. Execute in order - do not skip steps.

---

## Step P.0: Create Feature Branch (MUST BE FIRST)

**Only execute if `-b` or `--branch` flag is specified.**

**CRITICAL**: This step MUST happen BEFORE any file operations (ADR, design spec). Files created before `git checkout -b` stay on main/master branch.

### Generate ADR ID

```bash
/usr/bin/env bash << 'WORKFLOW_STEPS_SCRIPT_EOF'
ADR_ID="$(date +%Y-%m-%d)-<slug>"
WORKFLOW_STEPS_SCRIPT_EOF
```

### Detect Primary Branch

```bash
/usr/bin/env bash << 'GIT_EOF'
PRIMARY=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
[ -z "$PRIMARY" ] && PRIMARY="main"  # fallback
GIT_EOF
```

### Create Branch

```bash
git checkout "$PRIMARY"
git pull origin "$PRIMARY"
git checkout -b "<type>/$ADR_ID"  # e.g., feat/, fix/, refactor/, docs/, chore/
```

### Commit Uncommitted Changes

```bash
git add -A
git commit -m "wip: checkpoint before implementing <slug>" || true
```

### Branch Type Selection

| Type       | When                                   |
| ---------- | -------------------------------------- |
| `feat`     | New capability or feature              |
| `fix`      | Bug fix                                |
| `refactor` | Code restructuring, no behavior change |
| `docs`     | Documentation only                     |
| `chore`    | Maintenance, tooling, dependencies     |
| `perf`     | Performance improvement                |

---

## Step P.1: Create ADR File

**Path**: `/docs/adr/$ADR_ID.md`

### Actions

1. Create directory if needed: `mkdir -p docs/adr`
2. Create ADR file using template from [ADR Template](./adr-template.md)
3. Populate frontmatter from session context
4. Add Design Spec link in header

### Frontmatter Population

Extract from session context:

- `decision-maker`: User who approved the plan
- `consulted`: Agent perspectives used in research
- `research-method`: How research was conducted
- `clarification-iterations`: Number of AskUserQuestion rounds
- `perspectives`: Select from [Perspectives Taxonomy](./perspectives-taxonomy.md)

### Diagram Requirements (2 DIAGRAMS REQUIRED)

**⛔ MANDATORY**: Every ADR must include EXACTLY 2 diagrams. Do NOT proceed without both.

| Diagram          | Location             | Purpose                                                              |
| ---------------- | -------------------- | -------------------------------------------------------------------- |
| **Before/After** | Context section      | Shows system state change (what exists now vs. after implementation) |
| **Architecture** | Architecture section | Shows component relationships and data flow                          |

**SKILL INVOCATION (REQUIRED):**

1. **Invoke Skill tool with `adr-graph-easy-architect` NOW**
2. Create **Before/After diagram** first — embed in `## Context` section
3. Create **Architecture diagram** second — embed in `## Architecture` section
4. **VERIFY**: Search ADR for `<!-- graph-easy source:` — you must have TWO separate blocks

**BLOCKING GATE**: Do NOT proceed to Step P.2 until BOTH diagrams are embedded in ADR.

---

## Step P.2: Create Design Spec

### Create Design Folder

```bash
mkdir -p docs/design/$ADR_ID
```

### CRITICAL: Global Plan is Ephemeral

The file at `~/.claude/plans/<adj-verb-noun>.md`:

- **Replaced** when a new plan is created (same session or new)
- **Use full path** when referencing: `~/.claude/plans/floating-plotting-valiant.md`
- **After Preflight**: spec.md becomes source-of-truth, not the global plan

The `source` field in spec frontmatter preserves the original filename for traceability, but the file itself may no longer exist.

### Create Spec with YAML Frontmatter

1. **Copy global plan content**:

```bash
cp ~/.claude/plans/<adjective-verb-noun>.md docs/design/$ADR_ID/spec.md
```

2. **Prepend YAML frontmatter** to the copied spec.md:

```yaml
---
adr: YYYY-MM-DD-slug
source: ~/.claude/plans/<adjective-verb-noun>.md
implementation-status: in_progress
phase: preflight
last-updated: YYYY-MM-DD
---
```

3. **Add ADR backlink** after frontmatter:

```markdown
**ADR**: [Feature Name ADR](/docs/adr/YYYY-MM-DD-slug.md)
```

### Frontmatter Field Descriptions

| Field                   | Required | Description                                            |
| ----------------------- | -------- | ------------------------------------------------------ |
| `adr`                   | Yes      | ADR ID for programmatic linking                        |
| `source`                | Yes      | Full path to global plan (ephemeral, for traceability) |
| `implementation-status` | Yes      | `in_progress`, `blocked`, `completed`, or `abandoned`  |
| `phase`                 | Yes      | Current workflow phase                                 |
| `last-updated`          | Yes      | Date of last spec modification                         |

### Link Format Rule

Use the form `[descriptive text](/repo-root-relative/path)`, never `./` or `../` paths.

---

## Step P.3: Verify Checkpoint (MANDATORY)

**STOP. Verify artifacts exist before proceeding.**

### Verification Commands

```bash
# Verify ADR exists
[ -f "docs/adr/$ADR_ID.md" ] || { echo "ADR not created: docs/adr/$ADR_ID.md"; exit 1; }

# Verify design spec exists
[ -f "docs/design/$ADR_ID/spec.md" ] || { echo "Design spec not created: docs/design/$ADR_ID/spec.md"; exit 1; }

echo "Preflight complete: ADR and design spec created"
```

### Checklist (ALL must be true)

- [ ] ADR file exists at `/docs/adr/$ADR_ID.md`
- [ ] ADR has YAML frontmatter with all 7 required fields
- [ ] ADR has `status: proposed` (initial state)
- [ ] ADR has `**Design Spec**:` link in header
- [ ] **DIAGRAM CHECK 1**: ADR has **Before/After diagram** in Context section (graph-easy block)
- [ ] **DIAGRAM CHECK 2**: ADR has **Architecture diagram** in Architecture section (graph-easy block)

**⛔ DIAGRAM VERIFICATION**: If either diagram is missing, STOP and invoke `adr-graph-easy-architect` skill.
Search for `<!-- graph-easy source:` — you need TWO separate blocks.

- [ ] Design spec exists at `/docs/design/$ADR_ID/spec.md`
- [ ] Design spec has YAML frontmatter with all 5 required fields
- [ ] Design spec has `implementation-status: in_progress`
- [ ] Design spec has `phase: preflight`
- [ ] Design spec has `**ADR**:` backlink in header
- [ ] Feature branch created with ADR ID naming (if `-b` flag specified)

**If any item is missing**: Create it now. Do NOT proceed to Phase 1.

---

## Folder Structure Reference

```text
/docs/
  adr/
    YYYY-MM-DD-slug.md          # ADR file
  design/
    YYYY-MM-DD-slug/            # Design folder (1:1 with ADR)
      spec.md                   # Active implementation spec (SSoT)
```

**Naming Rule**: Use exact same `YYYY-MM-DD-slug` for both ADR and Design folder.

---

## Common Errors

| Error                          | Cause                    | Solution                                            |
| ------------------------------ | ------------------------ | --------------------------------------------------- |
| ADR frontmatter missing fields | Incomplete template      | Check all 7 required fields                         |
| Design spec missing backlink   | Forgot to add header     | Add `**ADR**: [...]` link                           |
| Diagrams not present           | Skipped diagram step     | Use Skill tool to invoke `adr-graph-easy-architect` |
| Wrong slug format              | Contains redundant words | Apply word economy rule                             |
| Relative paths in links        | Used `./` or `../`       | Use `/docs/adr/...` format                          |
