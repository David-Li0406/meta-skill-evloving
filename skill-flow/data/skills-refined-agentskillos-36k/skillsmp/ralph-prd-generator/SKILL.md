---
name: ralph-prd-generator
description: "Generate a Product Requirements Document (PRD) for a new feature using Claude Haiku for cost-effective planning. Can convert GitHub issues into PRDs or create from scratch. Use when planning a feature, starting a new project, or when asked to create a PRD. Triggers on: create a prd, write prd for, plan this feature, requirements for, spec out, convert issue to prd."
model: claude-haiku-4-5-20251001
---

# Ralph PRD Generator (Haiku-Powered)

Create detailed Product Requirements Documents that are clear, actionable, and suitable for implementation. This skill uses Claude Haiku for cost-effective planning.

---

## Usage Modes

### Mode 1: Create PRD from Description

User provides a feature description, you ask clarifying questions, then generate PRD.

### Mode 2: Convert GitHub Issue to PRD

User provides a GitHub issue URL or content, you convert it to a structured PRD format.

---

## Mode 1: Create PRD from Description

### Step 1: Clarifying Questions

Ask only critical questions where the initial prompt is ambiguous. Focus on:

- **Problem/Goal:** What problem does this solve?
- **Core Functionality:** What are the key actions?
- **Scope/Boundaries:** What should it NOT do?
- **Success Criteria:** How do we know it's done?

**Format Questions Like This:**

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

## Mode 2: Convert GitHub Issue to PRD

When user provides a GitHub issue URL or says "convert this issue to PRD":

### Step 1: Analyze the Issue

- Extract the issue title and description
- Identify core requirements from the issue body
- Note any acceptance criteria already defined
- Check for linked resources (mockups, related issues)

### Step 2: Ask Clarifying Questions (if needed)

If the issue lacks critical details, ask 2-3 focused questions:

```
The GitHub issue provides a good starting point. A few clarifying questions:

1. Priority/Scope?
   A. MVP - minimal functionality
   B. Full-featured

2. Target completion timeframe?
   A. This sprint (small scope)
   B. Next 2-3 sprints (medium)
   C. Long-term feature (large)

3. Any technical constraints not mentioned in the issue?
```

### Step 3: Generate PRD from Issue

Convert the issue into the full PRD structure, preserving:

- Original issue title (as feature name)
- Issue description (as context)
- Any existing acceptance criteria
- Referenced mockups or specifications

---

## PRD Structure

Generate the PRD with these sections:

### 1. Introduction/Overview

Brief description of the feature and the problem it solves.

**If converting from GitHub issue:** Include a reference to the original issue:

```markdown
**Source:** GitHub Issue #123 - [Issue Title](issue-url)
```

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
- [ ] **[UI stories only]** Verify in browser using agent-browser skill
```

**Important:**

- Acceptance criteria must be verifiable, not vague. "Works correctly" is bad. "Button shows confirmation dialog before deleting" is good.
- **For any story with UI changes:** Always include "Verify in browser using agent-browser skill" as acceptance criteria. This ensures visual verification of frontend work.
- **For backend stories:** Always include PEST test coverage as acceptance criteria. Backend features are NOT complete without passing tests.

---

## Test Coverage Requirements

### Backend Features: PEST Tests (MANDATORY)

**ALL backend features MUST have PEST test coverage.**

For backend stories (models, controllers, services, APIs, database changes), include:

```markdown
- [ ] Write PEST tests in app/Modules/{Module}/Tests/Feature/ or Tests/Unit/
- [ ] Tests cover all new functionality and edge cases
- [ ] Tests pass when run with 'cd site && composer test'
```

**Note**: Tests run via `composer test` which uses `scripts/test.sh` (auto-detects Sail environment).

### Frontend Features: Test Coverage Rules

**For UI stories, you MUST add:**

1. **Agent-Browser Verification (ALWAYS REQUIRED)** - Visual confirmation for ALL UI changes
2. **E2E Test Story (REQUIRED for complex frontend tasks)** - Automated tests for critical user flows

**When to add E2E tests:**
- Complex user interactions (multi-step workflows, forms with validation)
- Critical user paths (authentication, checkout, data submission)
- Features with significant business logic in the UI
- Components with conditional rendering or state management

**When E2E tests may not be needed:**
- Simple visual changes (styling updates, layout tweaks)
- Static content updates
- Minor UI adjustments
- Non-interactive components

---

## Additional Story Templates for UI Changes

**For UI stories that require E2E test coverage, add these additional stories:**

### 1. E2E Test Story (Required)

After each UI story, add a corresponding e2e test story:

```markdown
### US-XXX-02: E2E Test: [Original Story Title]

**Description:** Create an e2e test to verify [what the original story does].

**Acceptance Criteria:**

- [ ] Create a Playwright e2e test in site/tests/e2e/
- [ ] Test navigates to the relevant page
- [ ] Test performs the user action (click, input, etc.)
- [ ] Test verifies the expected outcome
- [ ] Build assets before testing with 'cd site && bun run build'
- [ ] Test must pass when run with 'cd site && composer e2e'
```

**Note**: E2E tests run via `cd site && composer e2e` which executes `bun run test:e2e`.

**Debugging Note:** If e2e tests fail repeatedly, use the agent-browser skill for debugging:
- Start server: `~/.claude/skills/agent-browser/server.sh &`
- Use `getAISnapshot()` to inspect page structure
- Take debug screenshots to understand failures
- Check for timing issues or selector problems

### 2. Dev-Browser Verification Story (Required)

After the e2e test story, add a agent-browser verification story:

```markdown
### US-XXX-03: Dev-Browser Verification: [Original Story Title]

**Description:** Verify [original story] using the agent-browser skill for visual confirmation.

**Acceptance Criteria:**

- [ ] Check if agent-browser server is running (curl -s http://localhost:9222), start with '~/.claude/skills/agent-browser/server.sh &' if not
- [ ] Navigate to the relevant page
- [ ] Perform the user action and verify visually
- [ ] Take a screenshot as evidence (save to .claude/skills/agent-browser/tmp/)
- [ ] Verification must be documented in notes with screenshot path
```

### Story Grouping Pattern

For each UI-related fix or feature, the story sequence should be:

1. **US-XXX-01**: The actual fix/feature implementation
2. **US-XXX-02**: E2E test for the fix/feature
3. **US-XXX-03**: Dev-browser visual verification

This ensures:
- Automated regression testing via e2e tests
- Visual confirmation via agent-browser
- Complete verification coverage

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
- **Location:** `tasks/` directory in project root
- **Filename:** `prd-[feature-name].md` (kebab-case)

**After creating the PRD:**

1. Save the file to `tasks/prd-[feature-name].md`
2. Confirm the file was created successfully
3. Provide a brief summary of what was included

---

## Example PRD

```markdown
# PRD: Task Priority System

**Source:** Created from scratch

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
- [ ] Verify in browser using agent-browser skill

### US-003: Add priority selector to task edit

**Description:** As a user, I want to change a task's priority when editing it.

**Acceptance Criteria:**

- [ ] Priority dropdown in task edit modal
- [ ] Shows current priority as selected
- [ ] Saves immediately on selection change
- [ ] Typecheck passes
- [ ] Verify in browser using agent-browser skill

### US-004: Filter tasks by priority

**Description:** As a user, I want to filter the task list to see only high-priority items when I'm focused.

**Acceptance Criteria:**

- [ ] Filter dropdown with options: All | High | Medium | Low
- [ ] Filter persists in URL params
- [ ] Empty state message when no tasks match filter
- [ ] Typecheck passes
- [ ] Verify in browser using agent-browser skill

### US-004-02: E2E Test: Filter tasks by priority

**Description:** Create an e2e test to verify the priority filter works correctly.

**Acceptance Criteria:**

- [ ] Create a Playwright e2e test in site/tests/e2e/
- [ ] Test navigates to task list page
- [ ] Test selects each filter option and verifies filtered results
- [ ] Test verifies filter persists in URL
- [ ] Build assets before testing with 'cd site && bun run build'
- [ ] Test must pass when run with 'cd site && composer e2e'

### US-004-03: Dev-Browser Verification: Filter tasks by priority

**Description:** Verify the filter functionality using agent-browser skill for visual confirmation.

**Acceptance Criteria:**

- [ ] Start agent-browser server with `~/.claude/skills/agent-browser/server.sh &`
- [ ] Navigate to task list page
- [ ] Use getAISnapshot() to identify filter dropdown
- [ ] Select each filter option and verify visible tasks
- [ ] Take screenshots before and after filtering
- [ ] Document verification in notes with screenshot paths

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

- [ ] Asked clarifying questions with lettered options (or used GitHub issue content)
- [ ] Incorporated user's answers
- [ ] User stories are small and specific
- [ ] Functional requirements are numbered and unambiguous
- [ ] Non-goals section defines clear boundaries
- [ ] If from GitHub issue, included source reference
- [ ] Saved to `tasks/prd-[feature-name].md`
- [ ] Confirmed file creation to user

---

## Model Usage Note

This skill uses **Claude Haiku (claude-haiku-4-5-20251001)** for cost-effective PRD generation. Haiku is excellent for structured document creation and provides fast, economical results while maintaining quality for planning documents.
