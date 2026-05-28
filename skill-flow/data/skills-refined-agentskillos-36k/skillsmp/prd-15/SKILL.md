---
name: prd
description: Generate a Product Requirements Document (PRD) for a new feature. Use when planning a feature, starting a new project, or when asked to create a PRD.
---

# PRD Generator

Create detailed Product Requirements Documents that are clear, actionable, and suitable for implementation.

---

## The Job

1. **Extract explicit instructions** from the user's prompt (Step 0)
2. **Check project conventions** - git history, CLAUDE.md (Step 0)
3. Ask 3-5 essential clarifying questions (with lettered options)
4. Generate a structured PRD based on answers
5. Save to the global Ralph projects directory (see Output section)

**Important:** Do NOT start implementing. Just create the PRD.

---

## Step 0: Extract Context Before Asking Questions

### A. Parse User's Explicit Instructions

**CRITICAL:** Before asking clarifying questions, carefully parse the user's initial prompt for:

- **Specific files mentioned** (e.g., "add to `src/pages/playground/Playground.tsx`")
- **Tools or skills to use** (e.g., "use the staging-browser-localhost skill to test")
- **Workflows described** (e.g., "to debug it, you will have to...")
- **Integration points** (e.g., "add it to the playground page")
- **Testing requirements** (e.g., "interact with it in the browser")

These are **non-negotiable requirements** that MUST appear in the PRD as user stories. Do NOT ask the user to repeat themselves — extract and incorporate automatically.

### B. Check Project Conventions

Run these commands to understand the project's conventions:

```bash
# Check commit message format
git log --oneline -10

# Check for project instructions
cat CLAUDE.md 2>/dev/null | head -50
```

Look for:

- **Commit message format** (e.g., `feat: [US-XXX] description`, `fix: description [CI-0000]`)
- **Branch naming conventions** (e.g., `ralph/feature-name`, `feature/XXX-description`)
- **Required checks** (e.g., `pnpm ts:check`, `pnpm biome:check`, `pnpm test`)

Incorporate these conventions into the PRD's acceptance criteria.

---

## Step 1: Clarifying Questions

Ask only critical questions where the initial prompt is ambiguous. Focus on:

- **Problem/Goal:** What problem does this solve?
- **Core Functionality:** What are the key actions?
- **Scope/Boundaries:** What should it NOT do?
- **Success Criteria:** How do we know it's done?

### Format Questions Like This:

```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Other: [please specify]

2. Who is the target user?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only

3. What is the scope?
   A. Minimal viable version
   B. Full-featured implementation
   C. Just the backend/API
   D. Just the UI
```

This lets users respond with "1A, 2C, 3B" for quick iteration.

---

## Step 2: PRD Structure

Generate the PRD with these sections:

### 1. Introduction/Overview

Brief description of the feature and the problem it solves.

### 2. Goals

Specific, measurable objectives (bullet list).

### 3. User Stories

Each story needs:

- **Title:** Short descriptive name
- **Description:** "As a [user], I want [feature] so that [benefit]"
- **Acceptance Criteria:** Verifiable checklist of what "done" means

Each story should be small enough to implement in one focused session.

**Format:**

```markdown
### US-001: [Title]

**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**

- [ ] Specific verifiable criterion
- [ ] Another criterion
- [ ] Typecheck/lint passes
- [ ] **[UI stories only]** Verify in browser using dev-browser skill
```

**Important:**

- Acceptance criteria must be verifiable, not vague. "Works correctly" is bad. "Button shows confirmation dialog before deleting" is good.
- **For any story with UI changes:** Always include "Verify in browser using dev-browser skill" as acceptance criteria. This ensures visual verification of frontend work.

### 4. Functional Requirements

Numbered list of specific functionalities:

- "FR-1: The system must allow users to..."
- "FR-2: When a user clicks X, the system must..."

Be explicit and unambiguous.

### 5. Non-Goals (Out of Scope)

What this feature will NOT include. Critical for managing scope.

### 6. Design Considerations (Optional)

- UI/UX requirements
- Link to mockups if available
- Relevant existing components to reuse

### 7. Technical Considerations (Optional)

- Known constraints or dependencies
- Integration points with existing systems
- Performance requirements

### 8. Success Metrics

How will success be measured?

- "Reduce time to complete X by 50%"
- "Increase conversion rate by 10%"

### 9. Open Questions

Remaining questions or areas needing clarification.

---

## Writing for Junior Developers

The PRD reader may be a junior developer or AI agent. Therefore:

- Be explicit and unambiguous
- Avoid jargon or explain it
- Provide enough detail to understand purpose and core logic
- Number requirements for easy reference
- Use concrete examples where helpful

---

## Output

**CRITICAL: Always save to the global Ralph projects directory, never the project itself.**

1. Get project directory:

   ```bash
   ralph project-dir
   ```

2. Save to: `$(ralph project-dir)/prd.md`

---

## Example PRD

```markdown
# PRD: Task Priority System

## Introduction

Add priority levels to tasks so users can focus on what matters most. Tasks can be marked as high, medium, or low priority, with visual indicators and filtering to help users manage their workload effectively.

## Goals

- Allow assigning priority (high/medium/low) to any task
- Provide clear visual differentiation between priority levels
- Enable filtering and sorting by priority
- Default new tasks to medium priority

## User Stories

### US-001: Add priority field to database

**Description:** As a developer, I need to store task priority so it persists across sessions.

**Acceptance Criteria:**

- [ ] Add priority column to tasks table: 'high' | 'medium' | 'low' (default 'medium')
- [ ] Generate and run migration successfully
- [ ] Typecheck passes

### US-002: Display priority indicator on task cards

**Description:** As a user, I want to see task priority at a glance so I know what needs attention first.

**Acceptance Criteria:**

- [ ] Each task card shows colored priority badge (red=high, yellow=medium, gray=low)
- [ ] Priority visible without hovering or clicking
- [ ] Typecheck passes
- [ ] Verify in browser using dev-browser skill

### US-003: Add priority selector to task edit

**Description:** As a user, I want to change a task's priority when editing it.

**Acceptance Criteria:**

- [ ] Priority dropdown in task edit modal
- [ ] Shows current priority as selected
- [ ] Saves immediately on selection change
- [ ] Typecheck passes
- [ ] Verify in browser using dev-browser skill

### US-004: Filter tasks by priority

**Description:** As a user, I want to filter the task list to see only high-priority items when I'm focused.

**Acceptance Criteria:**

- [ ] Filter dropdown with options: All | High | Medium | Low
- [ ] Filter persists in URL params
- [ ] Empty state message when no tasks match filter
- [ ] Typecheck passes
- [ ] Verify in browser using dev-browser skill

## Functional Requirements

- FR-1: Add `priority` field to tasks table ('high' | 'medium' | 'low', default 'medium')
- FR-2: Display colored priority badge on each task card
- FR-3: Include priority selector in task edit modal
- FR-4: Add priority filter dropdown to task list header
- FR-5: Sort by priority within each status column (high to medium to low)

## Non-Goals

- No priority-based notifications or reminders
- No automatic priority assignment based on due date
- No priority inheritance for subtasks

## Technical Considerations

- Reuse existing badge component with color variants
- Filter state managed via URL search params
- Priority stored in database, not computed

## Success Metrics

- Users can change priority in under 2 clicks
- High-priority tasks immediately visible at top of lists
- No regression in task list performance

## Open Questions

- Should priority affect task ordering within a column?
- Should we add keyboard shortcuts for priority changes?
```

---

## Checklist

Before saving the PRD:

- [ ] **Extracted explicit instructions from user's prompt** (files, tools, workflows, testing requirements)
- [ ] **Checked project conventions** (git log, CLAUDE.md) and incorporated them
- [ ] Asked clarifying questions with lettered options
- [ ] Incorporated user's answers
- [ ] User stories are small and specific
- [ ] **User stories include all user-specified requirements** (e.g., specific files to modify, skills to use for testing)
- [ ] Functional requirements are numbered and unambiguous
- [ ] Non-goals section defines clear boundaries
- [ ] Saved to global Ralph projects directory (see Output section)
