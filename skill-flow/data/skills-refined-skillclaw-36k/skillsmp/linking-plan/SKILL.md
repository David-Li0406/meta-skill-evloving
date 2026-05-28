---
name: linking-plan
description: Use after completing planning phase (superpowers:writing-plans). Links implementation plan document to task. Simple task - just save the link, nothing else. Handles post-planning workflow for beads tasks.
---

# Flow: After Plan

## Overview

**Core principle:** Save the link. That's all.

This is a SIMPLE task. Find plan document, save link to task description. Done.

**Do NOT add "helpful extras".** This skill does exactly one thing: save Plan link. Nothing more.

## Quick Reference

| Step | Action | Key Point |
|------|--------|-----------|
| 1. Find Task | Get in_progress leaf task | Ask if multiple |
| 2. Find Plan | Newest plan in docs/plans/ | Recent file |
| 3. **Save Link** | Add `Plan: path` to description | **PRIMARY GOAL** |
| 4. Done | Verify link saved | That's it |

**Total actions:** 1 (save link)
**Total scope:** Save Plan link only

## THE PRIMARY TASK

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  SAVE THIS TO TASK DESCRIPTION:                │
│                                                 │
│  Plan: docs/plans/{plan-filename}              │
│                                                 │
│  That's the ENTIRE task. Nothing else.         │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Workflow

Follow these steps **in order**. Do not add steps.

### 1. Find In-Progress Leaf Task

```bash
bd list --status=in_progress
```

Filter for leaf tasks (no open children).

**If multiple found:** Ask user which task this plan is for.
**If none found:** Suggest running `flow:start` first.

### 2. Find Newest Plan Document

```bash
ls -t docs/plans/*.md | head -1
```

Look for newest markdown file in `docs/plans/`.

**Heuristics:**
- Recent (within last hour)
- Contains "Plan", "Implementation", "Steps"
- User just mentioned finishing plan

**If multiple candidates:** Ask user which file.
**If none found:** Ask user for plan file path.

### 3. Save Plan Link to Description

**This is THE task. The only action.**

Get current description:
```bash
bd show {task-id}
```

Add Plan link:
```bash
bd update {task-id} --description="{current-description}\n\nPlan: docs/plans/{plan-filename}"
```

**IMPORTANT:**
- Preserve existing content
- **Preserve existing Design link** (if present)
- Add newline before Plan link
- Format: `Plan: docs/plans/...`

**If Plan link already exists:**
Ask: "Task already has Plan link: {old-link}. Update to {new-link}? (yes/no)"

### 4. Done

Verify:
- [ ] Plan link in description?
- [ ] Design link still there (if was there)?
- [ ] Did nothing else?

If all checked: Done.

## Scope Boundaries - READ THIS CAREFULLY

### This Skill DOES (4 things total):
✅ Find in_progress leaf task
✅ Find newest plan document
✅ **Save Plan link to task description**
✅ Preserve existing Design link

### This Skill Does NOT (Long list - READ IT):
❌ Create todo lists (use TodoWrite separately if needed)
❌ Commit plan file to git (separate workflow)
❌ Create subtasks (use after-design for that)
❌ Update task status (use flow:start)
❌ Create branches (use flow:start)
❌ Parse plan content
❌ Extract implementation steps
❌ Verify project structure
❌ Set up development environment
❌ Install dependencies
❌ Run builds or tests
❌ Start implementation
❌ Create any files
❌ Modify any files (except task description)
❌ "Set up" anything beyond saving the link

**If user says "set me up":**
Save Plan link. That's the setup. Done.

**If user wants todos:**
Tell them to use TodoWrite separately. Not this skill's job.

**If user wants to commit plan:**
Tell them to use git workflow. Not this skill's job.

## Red Flags - STOP

If you're thinking any of these, STOP and just save the link:

- "User wants to start coding"
- "Let me set everything up"
- "I'll create todos from the plan"
- "I should commit the plan file"
- "This task is too simple"
- "I'll add extra value"
- "Being maximally helpful"
- "I'll break down the plan"
- "Let me prepare the environment"
- "I'll verify the project structure"

**All of these mean: Save the link. Nothing else. Done.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "User wants setup" | Setup = save Plan link. Not todos or commits. |
| "Task is too simple" | Simple is good. Do it simply. Don't add extras. |
| "I'll create todos to help" | TodoWrite is separate workflow. Out of scope. |
| "Committing plan is good practice" | Git workflow is separate. Out of scope. |
| "I did helpful things" | Did you save Plan link? If no, task not done. |
| "Being maximally helpful" | Maximal help = doing THE task, not extras. |
| "Plan has steps I should track" | Not your job. Save link, user handles rest. |
| "Let me set up environment" | Out of scope. Save link only. |

## Examples

### ❌ BAD: Scope creep, missed primary task

```
User: "I finished the plan, set me up to start coding"
Agent: [Creates todo list with 9 implementation tasks]
       [Commits plan file to git]
       [Verifies project structure]

       Done! You're set up to start coding.
```

**Problems:**
- Did NOT save Plan link (PRIMARY TASK MISSED!)
- Created todos (out of scope)
- Committed file (out of scope)
- Verified structure (out of scope)
- Forgot the actual task completely

### ✅ GOOD: Simple and focused

```
User: "I finished the plan, set me up to start coding"
Agent: Saved Plan link to task claude-tools-abc:

       Plan: docs/plans/2026-01-17-implementation-plan.md

       Done. Task now has both Design and Plan links.
```

**Correct because:**
- Saved Plan link (PRIMARY TASK)
- Preserved Design link
- Did nothing else
- Simple and fast

### ❌ BAD: "Helpful" extras

```
User: "Run after-plan please"
Agent: [Saves Plan link] ✓
       [Parses plan for implementation steps]
       [Creates 5 subtasks]
       [Updates parent task status]

       I've linked the plan and created subtasks for each phase!
```

**Problems:**
- Primary task done ✓
- But added extras (subtasks, status) ✗
- Scope creep

### ✅ GOOD: Stay in scope

```
User: "Run after-plan please"
Agent: Found plan docs/plans/2026-01-17-test-plan.md

       Saved Plan link to task claude-tools-6hl.

       Done.
```

**Correct because:**
- Found plan
- Saved link
- Done
- No extras

## Edge Cases

### Multiple In-Progress Tasks

```
Found 2 in_progress leaf tasks:
1. claude-tools-abc: Feature X
2. claude-tools-def: Feature Y

Which task is this plan for? (enter 1 or 2, or task ID)
```

### Plan Link Already Exists

```
Task already has Plan link: docs/plans/old-plan.md

Update to new plan docs/plans/2026-01-17-new-plan.md? (yes/no)
```

### No Plan File Found

```
No recent plan files found in docs/plans/.

Please provide the plan file path (or 'skip' if no plan needed):
```

### Has Design, Adding Plan

```
Task description before:
  Design: docs/plans/2026-01-16-design.md

Task description after:
  Design: docs/plans/2026-01-16-design.md
  Plan: docs/plans/2026-01-17-plan.md

Both links preserved ✓
```

## The Bottom Line

**This is a simple task. Do it simply.**

1. Find task
2. Find plan
3. Save link
4. Done

Don't add "helpful extras". Don't create todos. Don't commit files. Don't parse content.

Just save the link. That's the entire job.

**Paradox of simple tasks:** They invite complexity. Resist it.

Simple task → Do it simply → Be done.
