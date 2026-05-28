---
name: step-06-tasks
description: Create actionable implementation tasks from PRD and Architecture
prev_step: steps/step-05-architecture.md
next_step: null
---

# Step 6: Task Creation

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER create vague tasks - each must be actionable
- ✅ ALWAYS base tasks on PRD features and Architecture
- ✅ ALWAYS respond in `{user_language}`
- 📋 YOU ARE A project manager, breaking work into doable chunks
- 💬 FOCUS on tasks that can be done in 1-4 hours each
- 🚫 FORBIDDEN to create tasks not traceable to PRD/Architecture

## EXECUTION PROTOCOLS:

- 🎯 Create tasks folder with numbered task files
- 💾 Each task has: context, requirements, acceptance criteria
- 📖 Tasks should be completable by Claude Code
- 🚫 FORBIDDEN to skip task file creation (if save_mode)

## CONTEXT BOUNDARIES:

- Variables from previous steps: `{validated_idea}`, `{prd_content}`, `{architecture}`, `{user_language}`, `{output_dir}`, `{save_mode}`
- Tasks should reference PRD features and Architecture decisions

## REFERENCE:

Load `../references/task-template.md` for:

- Task file structure
- Standard task categories
- Task sizing guide
- Acceptance criteria patterns

## YOUR TASK:

Create a structured set of implementation tasks that Claude Code can execute to build the MVP.

---

## TASK STRUCTURE:

### Task File Template

Each task file follows this structure:

```markdown
---
task_id: { NN }
title: { Task Title }
status: pending
priority: P0|P1|P2
estimated_hours: { 1-4 }
prd_features: [{ feature references }]
archi_sections: [{ architecture references }]
depends_on: [{ task_ids }]
---

# Task {NN}: {Title}

## Context

{Brief context from PRD and Architecture - what this task is building and why}

## Requirements

- [ ] {Specific requirement 1}
- [ ] {Specific requirement 2}
- [ ] {Specific requirement 3}

## Technical Details

{Any specific technical instructions from Architecture}

**Files to create/modify:**

- `{file path 1}` - {purpose}
- `{file path 2}` - {purpose}

## Acceptance Criteria

- [ ] {Criterion 1 - testable}
- [ ] {Criterion 2 - testable}
- [ ] {Criterion 3 - testable}

## Notes

{Any additional context or gotchas}
```

---

## STANDARD TASK CATEGORIES:

### Category 1: Foundation (Tasks 01-03)

**Task 01: Project Setup**

- Clone/initialize project
- Install dependencies
- Configure environment variables
- Verify dev server runs

**Task 02: Database Setup**

- Configure Prisma
- Create initial schema
- Run first migration
- Seed initial data (if needed)

**Task 03: Authentication Setup**

- Configure Better Auth
- Create auth pages (login, signup)
- Setup session handling
- Test auth flow

### Category 2: Core Feature (Tasks 04-06)

**Task 04: {Core Feature} - Data Layer**

- Create Prisma models for core feature
- Create server actions
- Setup API routes (if needed)

**Task 05: {Core Feature} - UI**

- Create components for core feature
- Implement main user flow
- Connect to data layer

**Task 06: {Core Feature} - Polish**

- Add loading states
- Add error handling
- Add empty states

### Category 3: Supporting Features (Tasks 07-09)

**Task 07: {Supporting Feature 1}**

- Implement feature per PRD spec

**Task 08: {Supporting Feature 2}**

- Implement feature per PRD spec

**Task 09: Dashboard/Overview**

- Create main dashboard view
- Display relevant data

### Category 4: Pages & UI (Tasks 10-12)

**Task 10: Landing Page**

- Hero section
- Features section
- Call to action

**Task 11: Settings Page**

- User profile settings
- Account management

**Task 12: Layout & Navigation**

- Header/sidebar navigation
- Responsive design
- Mobile optimization

### Category 5: Integration (Tasks 13-15)

**Task 13: Email Notifications** (if needed)

- Configure Resend
- Create email templates
- Trigger emails on actions

**Task 14: Payment Integration** (if needed)

- Configure Stripe
- Create pricing page
- Handle webhooks

**Task 15: Final Polish**

- SEO meta tags
- Loading performance
- Error boundaries

---

## EXECUTION SEQUENCE:

### 1. Analyze PRD and Architecture

**Extract from PRD:**

- All must-have features
- User flows
- Pages required

**Extract from Architecture:**

- Implementation order
- Technical decisions
- Folder structure

### 2. Create Tasks Folder

**If `{save_mode}` = true:**

```bash
mkdir -p {output_dir}/tasks
```

### 3. Generate Task Files

**Create each task file:**

**`{output_dir}/tasks/01-project-setup.md`:**

```markdown
---
task_id: 01
title: Project Setup
status: pending
priority: P0
estimated_hours: 1
prd_features: []
archi_sections: ["Foundation"]
depends_on: []
---

# Task 01: Project Setup

## Context

Set up the Next.js project with the nowts stack. This is the foundation for {Product Name}.

## Requirements

- [ ] Initialize Next.js 15 project with TypeScript
- [ ] Install core dependencies (Tailwind, shadcn/ui)
- [ ] Configure environment variables
- [ ] Set up basic folder structure per Architecture

## Technical Details

**Based on Architecture:**

- Use App Router
- Configure Tailwind CSS v4
- Initialize shadcn/ui

**Files to create:**

- `.env.local` - environment variables
- `tailwind.config.ts` - Tailwind configuration
- `components.json` - shadcn configuration

## Acceptance Criteria

- [ ] `pnpm dev` runs without errors
- [ ] Tailwind styles work
- [ ] shadcn/ui components can be added
- [ ] TypeScript compiles without errors

## Notes

Use NOW.TS boilerplate as reference for stack patterns
```

**Continue for all tasks based on PRD features...**

### 4. Create Task Overview

**Generate `{output_dir}/tasks/README.md`:**

```markdown
# Implementation Tasks: {Product Name}

## Overview

Total tasks: {N}
Estimated total hours: {X}
Suggested timeline: {Y} days

## Task List

| #   | Task                  | Priority | Hours | Depends On | Status |
| --- | --------------------- | -------- | ----- | ---------- | ------ |
| 01  | Project Setup         | P0       | 1     | -          | ⬜     |
| 02  | Database Setup        | P0       | 2     | 01         | ⬜     |
| 03  | Authentication        | P0       | 3     | 02         | ⬜     |
| 04  | {Core Feature} - Data | P0       | 3     | 03         | ⬜     |
| 05  | {Core Feature} - UI   | P0       | 4     | 04         | ⬜     |
| ... | ...                   | ...      | ...   | ...        | ⬜     |

## Dependency Graph
```

01 → 02 → 03 → 04 → 05 → 06
↓
07 → 08
↓
10 → 11 → 12
↓
15

```

## How to Use

1. Work through tasks in order (respecting dependencies)
2. Use Claude Code to implement each task
3. Mark tasks as done: ⬜ → ✅
4. Reference PRD and Architecture for context

## Status Legend

- ⬜ Pending
- 🔄 In Progress
- ✅ Complete
- ⏸️ Blocked
```

### 5. Present Summary

**Display in `{user_language}`:**

```
📋 Tasks Created for {Product Name}

Total: {N} tasks
Estimated: {X} hours (~{Y} days)

Task breakdown:
- Foundation: {X} tasks ({Y} hours)
- Core Feature: {X} tasks ({Y} hours)
- Supporting: {X} tasks ({Y} hours)
- Polish: {X} tasks ({Y} hours)

Files created:
- tasks/README.md - Overview & tracking
- tasks/01-project-setup.md
- tasks/02-database-setup.md
- ... (all task files)

Suggested workflow:
1. Start with task 01, work sequentially
2. Use /apex or Claude Code for each task
3. Reference PRD.md and ARCHI.md for context
4. Update task status as you complete them
```

### 6. Provide Next Steps

**Display in `{user_language}`:**

```
🎉 SaaS Planning Complete!

You now have everything you need to build {Product Name}:

📁 Output folder: {output_dir}/
- idea.md - Validated idea with research
- prd.md - Product Requirements Document
- archi.md - Technical Architecture
- tasks/ - Implementation tasks

To start building:
1. Open the tasks folder
2. Start with 01-project-setup.md
3. Use Claude Code: "Implement task 01 from {output_dir}/tasks/01-project-setup.md"
4. Work through tasks in order

Pro tips:
- Keep PRD and Architecture open for reference
- Mark tasks ✅ as you complete them
- Ship fast, iterate based on feedback

Good luck building {Product Name}! 🚀
```

### 7. Workflow Complete

**Update all document frontmatters with `stepsCompleted: [0, 1, 2, 3, 4, 5, 6]`**

**Final AskUserQuestion (optional):**

```yaml
questions:
  - header: "Start"
    question: "Would you like me to start implementing the first task?"
    options:
      - label: "Yes, start task 01"
        description: "Begin project setup immediately"
      - label: "No, I'll do it myself"
        description: "I'll implement tasks on my own"
      - label: "Review documents first"
        description: "Let me review the generated docs"
    multiSelect: false
```

---

## SUCCESS METRICS:

✅ All PRD features have corresponding tasks
✅ Tasks are in logical order with dependencies
✅ Each task is 1-4 hours of work
✅ Each task has clear acceptance criteria
✅ README.md with overview and tracking
✅ All task files created (if save_mode)

## FAILURE MODES:

❌ Creating vague tasks like "Build the app"
❌ Tasks not traceable to PRD features
❌ Missing dependencies between tasks
❌ Tasks too large (>4 hours)
❌ No acceptance criteria
❌ **CRITICAL**: Not creating task files when save_mode is true

## TASK CREATION PROTOCOLS:

- Every task must be actionable by Claude Code
- Include file paths where possible
- Reference PRD and Architecture sections
- Keep tasks focused on one thing
- Clear acceptance criteria = can be verified

---

## WORKFLOW COMPLETE

**This is the final step of the create-saas workflow.**

The user now has:

1. ✅ Validated idea with market research
2. ✅ Product Requirements Document
3. ✅ Technical Architecture
4. ✅ Implementation tasks

**Output folder structure:**

```
~/.claude/output/saas/{project_id}/
├── idea.md
├── prd.md
├── archi.md
├── marketing.md
└── tasks/
    ├── README.md
    ├── 01-project-setup.md
    ├── 02-database-setup.md
    ├── 03-authentication.md
    ├── 04-core-feature-data.md
    ├── 05-core-feature-ui.md
    └── ... (more tasks)
```

<critical>
Congratulations! The SaaS planning workflow is complete.
The user can now use Claude Code with /apex or similar to implement each task.
</critical>
