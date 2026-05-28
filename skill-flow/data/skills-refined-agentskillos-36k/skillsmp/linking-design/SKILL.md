---
name: linking-design
description: Use after completing brainstorming/design phase. Links design document to task, parses subtasks, shows preview for approval, implements smart merge with existing subtasks. Handles post-design workflow for beads tasks.
---

# Flow: After Design

## Overview

**Core principle:** Preview before creating.

This skill handles the post-design workflow: linking design documents, extracting subtasks, and creating task hierarchy. Always shows what will be created and asks for confirmation - even when structure is clear and user seems in a hurry.

## Quick Reference

| Step | Action | Key Point |
|------|--------|-----------|
| 1. Find Task | Get in_progress leaf task | Ask if multiple |
| 2. Find Design | Newest in docs/plans/ | Heuristic search |
| 3. Parse | Extract subtasks from design | Multiple formats |
| 4. **Preview** | Show what will be created | Format + dependencies |
| 5. **Confirm** | Get explicit approval | Even under pressure |
| 6. Merge | Check existing subtasks | Skip duplicates |
| 7. Create | Only new subtasks | After confirmation |
| 8. Link | Save design path | To description |

**Scope:** This skill ONLY handles design linking and subtask creation. Does NOT create branches, commit files, or update statuses - those are separate workflows.

## Workflow

Follow these steps **in order**. Do not skip steps.

### 1. Find In-Progress Leaf Task

```bash
bd list --status=in_progress
```

Filter for leaf tasks (tasks without children or where all children are closed).

**If multiple found:** Ask user which task this design is for.
**If none found:** Suggest running `flow:start` first.

### 2. Find Newest Design Document

```bash
ls -t docs/plans/*.md | head -1
```

Look in `docs/plans/` for newest markdown file (by modification time).

**Heuristics for "design" vs other docs:**
- Recent (within last hour is good signal)
- Contains sections like "Requirements", "Architecture", "Tasks", "Implementation"
- User just mentioned finishing design

**If multiple candidates:** Show list, let user choose.
**If none found:** Ask user for design file path.

### 3. Parse Subtasks from Design

**Heuristically detect multiple formats:**
- Numbered lists: `1. Do X`, `2. Do Y`
- Bullet lists: `- Do X`, `* Do Y`
- Checkboxes: `- [ ] Do X`, `- [x] Do Y`
- Headers: `## Task: Do X`, `### Do X`
- Sections: Look for "Implementation", "Tasks", "Subtasks", "Steps"

**Extract for each subtask:**
- Title (required)
- Description (if multi-line)
- Priority (inherit from parent if not specified)

**If no subtasks found:**
Ask: "No clear subtasks found in design. Should I:
1. Look in a specific section (which one?)
2. Treat this as atomic task (no subtasks needed)
3. Let you manually specify subtasks"

### 4. Show Preview (MANDATORY)

**Before creating anything**, display preview:

```
Found 5 subtasks in design docs/plans/2026-01-16-feature-x.md:

1. {parent-id}.1: Implement input component
   Description: Create React component for user input, add form validation, handle submission
   Priority: P3 (inherits from parent)

2. {parent-id}.2: Add data validation
   Description: Implement validation rules, add error handling, write validation tests
   Priority: P3

3. {parent-id}.3: Create storage layer
   Description: Database schema, CRUD operations, migration scripts
   Priority: P3

4. {parent-id}.4: Write integration tests
   Description: Test full flow end-to-end, mock external dependencies, cover edge cases
   Priority: P3

5. {parent-id}.5: Update documentation
   Description: API docs, user guide, architecture diagram
   Priority: P3

All subtasks will depend on parent task {parent-id}.
Design will be linked in task description as: Design: docs/plans/2026-01-16-feature-x.md
```

**Preview must include:**
- Count of subtasks
- Full task IDs
- Titles and descriptions
- Priority levels
- Dependencies
- Design link that will be added

### 5. Ask for Confirmation (MANDATORY)

**Always ask explicitly:**

> "Should I create these {N} subtasks? (yes/no)"

**Wait for user response.**

If user says no: Ask what they want to adjust.
If user says yes: Proceed to step 6.

**Do NOT:**
- Assume yes because "structure is clear"
- Skip because user said "asap"
- Create immediately because "being helpful"

### 6. Check Existing Subtasks (Merge Logic)

```bash
bd show {parent-id}
```

Check if parent task already has children.

**If existing subtasks found:**

```
Checking existing subtasks...

Found 2 existing:
- {parent-id}.1: Implement input component (exists)
- {parent-id}.2: Add data validation (exists)

From design (5 total):
✓ Skip: Implement input component (already exists)
✓ Skip: Add data validation (already exists)
+ New: Create storage layer
+ New: Write integration tests
+ New: Update documentation

Should I create these 3 NEW subtasks? (yes/no)
```

**Merge rules:**
- **Exact match** (title identical) → Skip
- **Close match** (title similar, >80% match) → Ask user
- **New** → Include in creation

### 7. Create Subtasks

**Only after confirmation**, create subtasks:

```bash
bd create --title="Subtask title" --description="..." --priority=P3 --parent={parent-id}
```

Create each new subtask in order.

**Output progress:**
```
Creating subtasks...
✓ Created {parent-id}.3: Create storage layer
✓ Created {parent-id}.4: Write integration tests
✓ Created {parent-id}.5: Update documentation

Created 3 new subtasks under {parent-id}.
```

### 8. Link Design to Task

Update parent task description with design link:

```bash
bd update {parent-id} --description="{existing-description}\n\nDesign: docs/plans/{design-filename}"
```

**If design link already exists:**
Ask: "Task already has design link: {old-link}. Update to new design {new-link}? (yes/no)"

## Scope Boundaries

### This Skill DOES:
✅ Find in_progress leaf task
✅ Find newest design document
✅ Parse subtasks heuristically
✅ Show preview with details
✅ Ask for confirmation
✅ Check existing subtasks (merge)
✅ Create new subtasks only
✅ Link design path to description

### This Skill Does NOT:
❌ Create git branches (use `flow:start`)
❌ Commit design document (separate workflow)
❌ Update task status (use `flow:start` or manual `bd update`)
❌ Run tests or builds
❌ Implement code
❌ Make coffee

**One skill, one job.** Stay in scope.

## Red Flags - STOP

If you're thinking any of these, STOP and follow the workflow:

- "User said asap"
- "I'll complete the setup"
- "Structure is clear from design"
- "No need to show preview"
- "Confirmation is overhead"
- "I'll just do it"
- "I'll create the branch too"
- "Let me commit the design"

**All of these mean: Follow the workflow. Show preview. Ask confirmation. Stay in scope.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "User wants to start asap" | Preview takes 5 seconds. Fixing wrong subtasks takes 5 minutes. |
| "I'll complete the setup" | Scope creep. One skill, one job. |
| "Structure is clear from design" | User might want to adjust. Always show preview. |
| "No existing subtasks" | Check anyway. Merge logic prevents duplicates. |
| "Confirmation slows things down" | Creating wrong things is slower than confirming right things. |
| "This is being helpful" | Assuming isn't helpful - consulting is. |
| "I'll create the branch too" | Out of scope. Use flow:start for branches. |

## Examples

### ❌ BAD: Skip preview and confirmation

```
User: "I finished design, run after-design please, need to implement asap"
Agent: [Reads design, creates 5 subtasks immediately]
       Created 5 subtasks under claude-tools-abc. Also created feature branch.
```

**Problems:**
- No preview shown
- No confirmation requested
- Out of scope (branch creation)
- Time pressure bypassed workflow

### ✅ GOOD: Always preview and confirm

```
User: "I finished design, run after-design please, need to implement asap"
Agent: Found 5 subtasks in docs/plans/2026-01-16-feature-x.md:

       1. claude-tools-abc.1: Implement input component
          Description: React component, form validation, submission handling
          Priority: P3

       2. claude-tools-abc.2: Add data validation
          ...

       [shows all 5 with details]

       Should I create these 5 subtasks? (yes/no)

User: yes
Agent: Creating subtasks...
       ✓ Created 5 subtasks
       ✓ Linked design to task description

       Ready to start implementation! Use flow:start to choose a subtask.
```

**Correct because:**
- Showed full preview
- Asked for confirmation despite "asap"
- Stayed in scope (no branch)
- Guided to next step

### ❌ BAD: Ignore existing subtasks

```
User: "after-design" [task already has 2 subtasks]
Agent: [Creates all 5 subtasks from design, including 2 duplicates]
```

**Problem:** No merge logic, created duplicates.

### ✅ GOOD: Smart merge

```
User: "after-design" [task already has 2 subtasks]
Agent: Checking existing subtasks...

       Found 2 existing:
       - claude-tools-abc.1: Implement input component (exists)
       - claude-tools-abc.2: Add data validation (exists)

       From design (5 total):
       ✓ Skip: Implement input component (exists)
       ✓ Skip: Add data validation (exists)
       + New: Create storage layer
       + New: Write integration tests
       + New: Update documentation

       Should I create these 3 NEW subtasks? (yes/no)
```

**Correct because:**
- Checked existing
- Showed merge logic
- Only proposes new subtasks
- Still asks confirmation

## Edge Cases

### Multiple In-Progress Tasks

```
Found 2 in_progress leaf tasks:
1. claude-tools-abc: Feature X
2. claude-tools-def: Feature Y

Which task is this design for? (enter 1 or 2, or task ID)
```

### No Subtasks in Design

```
No clear subtasks found in docs/plans/2026-01-16-design.md.

Should I:
1. Look in a specific section (which one?)
2. Treat this as atomic task (no subtasks needed)
3. Let you manually specify subtasks

What would you like to do?
```

### Design Link Already Exists

```
Task already has design link: docs/plans/old-design.md

Update to new design docs/plans/2026-01-16-new-design.md? (yes/no)
```

## The Bottom Line

Always follow the workflow. Preview before creating. Confirmation is not overhead - it's the service.

Parse heuristically, show clearly, ask explicitly, then act.

Stay in scope. One skill, one job, done well.
