# Task Template & Guidelines

Reference for creating implementation tasks.

---

## Task Philosophy

**Good tasks are:**

- Atomic (1-4 hours of work)
- Actionable (clear what to do)
- Testable (clear acceptance criteria)
- Traceable (linked to PRD/Architecture)

**Bad tasks are:**

- Vague ("implement the feature")
- Too big (full feature in one task)
- No acceptance criteria
- Missing context

---

## Task File Template

````markdown
---
task_id: { NN }
title: { Clear Action Title }
status: pending
priority: P0|P1|P2
estimated_hours: { 1-4 }
prd_features: [{ feature references }]
archi_sections: [{ architecture references }]
depends_on: [{ task_ids }]
---

# Task {NN}: {Title}

## Context

{1-2 paragraphs explaining:

- What this task is building
- Why it's needed (link to PRD)
- How it fits in the bigger picture}

## Requirements

- [ ] {Specific, actionable requirement 1}
- [ ] {Specific, actionable requirement 2}
- [ ] {Specific, actionable requirement 3}

## Technical Details

{Specific technical instructions from Architecture}

**Tech stack:**

- {Technology 1}: {How to use it}
- {Technology 2}: {How to use it}

**Files to create/modify:**

- `{file path 1}` - {purpose}
- `{file path 2}` - {purpose}

**Example code pattern:**

```typescript
// Example of expected implementation
```
````

## Acceptance Criteria

- [ ] {Testable criterion 1}
- [ ] {Testable criterion 2}
- [ ] {Testable criterion 3}
- [ ] No TypeScript errors
- [ ] App runs without crashes

## Notes

{Any gotchas, tips, or references}

## Dependencies

- Requires: Task {XX} to be complete
- Blocks: Task {YY}

````

---

## Standard Task Categories

### Foundation Tasks (01-03)

#### Task 01: Project Setup
- Initialize project
- Install dependencies
- Configure environment
- Verify dev server

#### Task 02: Database Setup
- Configure Prisma
- Create schema
- Run migration
- Seed data (if needed)

#### Task 03: Authentication
- Configure Better Auth
- Create auth pages
- Setup session handling
- Test auth flow

### Core Feature Tasks (04-06)

#### Task 04: {Feature} - Data Layer
- Create Prisma models
- Create server actions
- Add validation schemas

#### Task 05: {Feature} - UI
- Create components
- Implement user flow
- Connect to data layer

#### Task 06: {Feature} - Polish
- Loading states
- Error handling
- Empty states

### Supporting Features (07-09)

Similar pattern to core feature.

### Pages & UI (10-12)

#### Task 10: Landing Page
- Hero section
- Features section
- Call to action

#### Task 11: Settings Page
- User profile
- Account management

#### Task 12: Layout & Navigation
- Header/sidebar
- Responsive design

### Integration (13-15)

#### Task 13: Email
- Configure Resend
- Create templates
- Trigger on actions

#### Task 14: Payments (if needed)
- Configure Stripe
- Pricing page
- Webhooks

#### Task 15: Final Polish
- SEO meta tags
- Performance
- Error boundaries

---

## Task Sizing Guide

| Size | Hours | Examples |
|------|-------|----------|
| XS | < 1h | Add a button, fix typo |
| S | 1-2h | Create component, add validation |
| M | 2-4h | Implement feature, create page |
| L | 4-8h | Complex feature - SPLIT IT |
| XL | > 8h | Too big - MUST SPLIT |

**If task is L or XL, break it down:**
- Data layer task
- UI task
- Integration task
- Polish task

---

## Acceptance Criteria Patterns

### For UI tasks:
- [ ] Component renders without errors
- [ ] Responsive on mobile/desktop
- [ ] Loading state shows during fetch
- [ ] Error state shows on failure
- [ ] Empty state shows when no data

### For Data tasks:
- [ ] Data saves to database
- [ ] Validation rejects invalid input
- [ ] Error messages are user-friendly
- [ ] Optimistic updates work (if applicable)

### For Auth tasks:
- [ ] Users can sign up
- [ ] Users can log in
- [ ] Protected routes redirect unauthenticated users
- [ ] Session persists across refresh

### For Integration tasks:
- [ ] External service responds correctly
- [ ] Errors are handled gracefully
- [ ] Retry logic works (if applicable)
- [ ] Webhooks process correctly

---

## Task README Template

```markdown
# Implementation Tasks: {Product Name}

## Overview

- Total tasks: {N}
- Estimated hours: {X}
- Suggested timeline: {Y} days

## Task List

| # | Task | Priority | Hours | Depends On | Status |
|---|------|----------|-------|------------|--------|
| 01 | Project Setup | P0 | 1 | - | ⬜ |
| 02 | Database Setup | P0 | 2 | 01 | ⬜ |
| ... | ... | ... | ... | ... | ⬜ |

## Dependency Graph

````

01 → 02 → 03 → 04 → 05
↓
06 → 07

```

## How to Use

1. Work through tasks respecting dependencies
2. Use Claude Code for each task
3. Mark complete: ⬜ → ✅
4. Reference PRD and Architecture

## Status Legend

- ⬜ Pending
- 🔄 In Progress
- ✅ Complete
- ⏸️ Blocked
```

---

## Common Mistakes

❌ **"Build the dashboard"** - Too vague, break it down
❌ **No acceptance criteria** - How do you know it's done?
❌ **Missing dependencies** - Task 05 needs 04 first
❌ **8+ hour tasks** - Break into smaller pieces
❌ **No file paths** - Be specific about what to create
