---
name: prd-generator
description: "Generate a Product Requirements Document (PRD) for a new feature. Use when planning a feature, starting a new project, or when asked to create a PRD. Triggers on: create a prd, write prd for, plan this feature, requirements for, spec out."
---

# PRD Generator

Create detailed Product Requirements Documents that are clear, actionable, and suitable for implementation.

---

## The Job

1. Receive a feature description from the user
2. Ask 3-5 essential clarifying questions (with lettered options)
3. Generate a structured PRD based on answers
4. Save to `tasks/prd-[feature-name].md`

**Important:** Do NOT start implementing. Just create the PRD.

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
- **Acceptance Criteria:** Verifiable checklist of what "done" means (see requirements below)
- **Dependencies:** *(Optional)* Which stories must complete first
- **Implementation Hint:** *(Optional)* Guidance for developer/agent

Each story should be small enough to implement in one focused session (typically 10-20 minutes of work).

**Story Size Threshold:**
- **Simple features** (≤4 acceptance criteria): Create ONE full-stack story combining UI + backend
- **Complex features** (>4 acceptance criteria): Split into multiple layer-specific stories with clear dependencies
- **Target:** 3-5 acceptance criteria per story (including typecheck/browser verification)
- **Maximum:** Never exceed 6 criteria - if a story needs more, it must be split

**How to Split Large Features:**

Apply layer-based decomposition matching your architecture:

**Backend/API Layer:**
1. Data model/schema changes
2. Core business logic/services
3. Validation and error handling

**Frontend/UI Layer:**
1. Component structure and state
2. User interactions and events
3. Visual polish and accessibility

**Full-Stack Integration:**
1. Data persistence layer
2. Server/API endpoints
3. Client components
4. End-to-end integration

**Pattern: Break by Responsibility**
- ❌ **Too broad:** "Add [feature name]"
- ✅ **Right-sized:**
  - "Implement [feature] data model"
  - "Build [feature] API endpoints"
  - "Create [feature] UI components"

**Pattern: Break by User Journey Step**
- ❌ **Too broad:** "Build [workflow]"
- ✅ **Right-sized:**
  - "Implement [workflow] step 1: [action]"
  - "Implement [workflow] step 2: [action]"
  - "Implement [workflow] step 3: [action]"

**Pattern: Break by Complexity Layer**
- ❌ **Too broad:** "Add advanced [feature]"
- ✅ **Right-sized:**
  - "Implement basic [feature] functionality"
  - "Add [feature] configuration options"
  - "Implement [feature] edge case handling"

**Format:**
```markdown
### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
  - **Must verify:** `[command to run or condition to check]`
  - **Expected:** What success looks like
- [ ] Another criterion
  - **Must verify:** `pytest tests/test_feature.py`
  - **Expected:** All tests pass
- [ ] Typecheck/lint passes
  - **Must verify:** `pyright --project .` or `npm run typecheck`
  - **Expected:** No errors
- [ ] **[UI stories only]** Verify in browser using dev-browser skill
  - **Must verify:** Navigate to page and test interaction
  - **Expected:** Feature works as described

**Depends on:** *(Optional)* US-XXX (if this story requires another to complete first)
**Implementation hint:** *(Optional)* Check if US-XXX already implemented this. Search for [specific code pattern].
```

**CRITICAL Requirements for Acceptance Criteria:**
- Each criterion MUST include "Must verify: [command]" with a specific verification method
- Verification can be: command to run, test to execute, condition to check, browser action
- "Must verify" makes completion unambiguous for AI agents
- Avoid vague criteria like "Works correctly" - specify HOW to verify it works
- **For any story with UI changes:** Always include "Verify in browser using dev-browser skill"

**Dependency Guidelines:**
- Add "Depends on: US-XXX" when a story requires another story's completion
- Add "Implementation hint" when related work may already exist (prevents duplication)
- Use "Check if US-XXX already did this" to guide agents to verify before implementing

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

- **Format:** Markdown (`.md`)
- **Location:** `tasks/`
- **Filename:** `prd-[feature-name].md` (kebab-case)

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
  - **Must verify:** Check migration file exists and column added
  - **Expected:** Migration successful, column present in schema
- [ ] Generate and run migration successfully
  - **Must verify:** `python manage.py migrate` or equivalent
  - **Expected:** No errors, migration applied
- [ ] Typecheck passes
  - **Must verify:** `pyright --project .` or `npm run typecheck`
  - **Expected:** No errors

### US-002: Complete Priority Display and Selection (Full-Stack)
**Description:** As a user, I want to see and change task priorities so I can manage what needs attention.

**Note:** This is a simple feature (4 criteria total), so combining UI + backend in one story.

**Acceptance Criteria:**
- [ ] Each task card shows colored priority badge (red=high, yellow=medium, gray=low)
  - **Must verify:** Navigate to task list in browser
  - **Expected:** Badges visible on all tasks with correct colors
- [ ] Priority dropdown in task edit modal with current value selected
  - **Must verify:** Open edit modal and check dropdown
  - **Expected:** Dropdown shows 3 options, current priority selected
- [ ] Changing priority saves immediately and updates UI
  - **Must verify:** Change priority, verify API call and UI update
  - **Expected:** No page refresh needed, change persists
- [ ] Typecheck passes
  - **Must verify:** `npm run typecheck`
  - **Expected:** No errors
- [ ] Verify in browser using dev-browser skill
  - **Must verify:** Full flow: view badge, edit priority, verify change
  - **Expected:** All interactions work smoothly

**Depends on:** US-001 (requires priority column in database)
**Implementation hint:** Reuse existing badge component, just add color variants for priority.

### US-003: Filter tasks by priority
**Description:** As a user, I want to filter the task list to see only high-priority items when I'm focused.

**Acceptance Criteria:**
- [ ] Filter dropdown with options: All | High | Medium | Low
  - **Must verify:** Navigate to task list, check filter dropdown
  - **Expected:** 4 options visible and selectable
- [ ] Filter persists in URL params
  - **Must verify:** Select filter, check URL contains `?priority=high`
  - **Expected:** URL updates, refresh preserves filter
- [ ] Empty state message when no tasks match filter
  - **Must verify:** Filter to priority with no tasks
  - **Expected:** Shows "No tasks found" or similar message
- [ ] Typecheck passes
  - **Must verify:** `npm run typecheck`
  - **Expected:** No errors
- [ ] Verify in browser using dev-browser skill
  - **Must verify:** Test all filter options and URL persistence
  - **Expected:** Filtering works, URL updates correctly

**Depends on:** US-002 (requires priority display to filter)
**Implementation hint:** Check if existing filter pattern used elsewhere, follow same approach.

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

- [ ] Asked clarifying questions with lettered options
- [ ] Incorporated user's answers
- [ ] User stories are small and specific
- [ ] Functional requirements are numbered and unambiguous
- [ ] Non-goals section defines clear boundaries
- [ ] Saved to `tasks/prd-[feature-name].md`
