---
name: plan-writing
description: Use this skill when you need to break down work into clear, actionable tasks with verification criteria, especially during feature implementation, refactoring, or any multi-step projects.
---

# Skill body

## Overview
This skill provides a framework for structured task planning, ensuring tasks are clear, actionable, and verifiable.

## Task Breakdown Principles

### 1. Small, Focused Tasks
- Each task should take 2-5 minutes.
- One clear outcome per task.
- Tasks must be independently verifiable.

### 2. Clear Verification
- Define how you know a task is done.
- Specify what can be checked or tested.
- Outline the expected output.

### 3. Logical Ordering
- Identify dependencies.
- Allow for parallel work where possible.
- Highlight the critical path.
- **Note:** Verification should always be the last phase.

### 4. Dynamic Naming in Project Root
- Save plan files as `{task-slug}.md` in the PROJECT ROOT.
- Name derived from the task (e.g., "add auth" → `auth-feature.md`).
- **Avoid** saving in `.claude/`, `docs/`, or temporary folders.

## Planning Principles (NOT Templates!)
> 🔴 **No fixed templates. Each plan is unique to the task.**

### Principle 1: Keep It SHORT
| ❌ Wrong                    | ✅ Right              |
|-----------------------------|-----------------------|
| 50 tasks with sub-sub-tasks | 5-10 clear tasks max  |
| Every micro-step listed     | Only actionable items |
| Verbose descriptions        | One-line per task     |

> **Rule:** If the plan exceeds one page, simplify it.

### Principle 2: Be SPECIFIC, Not Generic
| ❌ Wrong             | ✅ Right                                                 |
|----------------------|----------------------------------------------------------|
| "Set up project"     | "Run `npx create-next-app`"                              |
| "Add authentication" | "Install next-auth, create `/api/auth/[...nextauth].ts`" |
| "Style the UI"      | "Add Tailwind classes to `Header.tsx`"                   |

> **Rule:** Each task should have a clear, verifiable outcome.

### Principle 3: Dynamic Content Based on Project Type
**For NEW PROJECT:**
- Determine the tech stack.
- Define the MVP (minimal features).
- Outline the file structure.

**For FEATURE ADDITION:**
- Identify affected files.
- List required dependencies.
- Describe how to verify functionality.

**For BUG FIX:**
- Analyze the root cause.
- Specify the file/line to change.
- Outline how to test the fix.

### Principle 4: Scripts Are Project-Specific
> 🔴 **Do not copy-paste script commands. Choose based on project type.**

| Project Type     | Relevant Scripts                     |
|-------------------|--------------------------------------|
| Frontend/React     | `ux_audit.py`, `accessibility_checker.py` |
| Backend/API        | `api_validator.py`, `security_scan.py`      |