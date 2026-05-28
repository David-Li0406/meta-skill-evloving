---
name: prd-brownfield
description: "Generate a PRD for adding features to an existing codebase (brownfield). Use when extending or modifying an established project with existing patterns and conventions."
---

# PRD Generator - Brownfield Projects

Create detailed Product Requirements Documents for **existing codebases**, focusing on integration with current patterns, backward compatibility, and minimal disruption.

---

## The Job

1. Receive a feature description from the user
2. **Analyze the existing codebase context** (tech stack, patterns, structure)
3. Ask 3-5 clarifying questions focused on **integration and scope**
4. Generate a structured PRD that respects existing conventions
5. Save to `tasks/prd-[feature-name].md`

**Important:** Do NOT start implementing. Just create the PRD.

---

## Step 1: Analyze Existing Context

Before asking questions, review any provided codebase context:
- Current tech stack and dependencies
- Directory structure and patterns
- Existing API routes or components
- Database schema and models
- Testing conventions

Use this information to inform your questions and requirements.

---

## Step 2: Clarifying Questions (Brownfield-Specific)

For brownfield projects, focus on integration and scope:

### Integration Questions:
```
1. What is the scope of this change?
   A. New feature (additive, no changes to existing code)
   B. Enhancement to existing feature
   C. Refactoring existing functionality
   D. Bug fix or performance improvement

2. Which existing areas will this touch?
   A. Database schema (requires migration)
   B. Existing API endpoints
   C. Existing UI components
   D. Shared utilities/libraries
   E. Multiple of the above

3. What is the backward compatibility requirement?
   A. Must be fully backward compatible
   B. Can deprecate but not remove existing functionality
   C. Breaking changes acceptable (with migration path)
   D. Internal only (no external API changes)

4. How should this integrate with existing patterns?
   A. Follow existing patterns exactly
   B. Introduce new patterns (document why)
   C. Refactor existing patterns as part of this work

5. What is the testing expectation?
   A. Add tests for new code only
   B. Update existing tests as needed
   C. Increase overall coverage
   D. No new tests required
```

---

## Step 3: PRD Structure (Brownfield)

Generate the PRD with these sections:

### 1. Introduction/Overview
Brief description of the feature and how it extends/modifies existing functionality.

### 2. Goals
Specific, measurable objectives (bullet list).

### 3. Integration Points (Brownfield-Specific)
Document how this feature integrates with existing code:

```markdown
## Integration Points

### Existing Components to Modify
- `src/components/TaskList.tsx` - Add filter dropdown
- `src/server/actions/tasks.ts` - Add status filter parameter

### Existing Components to Reuse
- `src/components/ui/Dropdown.tsx` - Use for filter UI
- `src/lib/validation.ts` - Use existing Zod schemas

### New Files to Create
- `src/components/TaskFilter.tsx` - New filter component
- `src/server/actions/filters.ts` - Filter-related actions

### Database Changes
- Add `status` column to `tasks` table
- Migration required: Yes
```

### 4. Compatibility Considerations (Brownfield-Specific)
Document any compatibility concerns:

```markdown
## Compatibility

### Backward Compatibility
- Existing API endpoints continue to work without changes
- New `status` parameter is optional with default value

### Migration Requirements
- Database migration adds column with default value
- No data migration required

### Deprecations
- None in this release
```

### 5. User Stories
Each story needs:
- **Title:** Short descriptive name
- **Description:** "As a [user], I want [feature] so that [benefit]"
- **Acceptance Criteria:** Verifiable checklist
- **Integration Notes:** Which existing code is affected (Brownfield-specific)

**Format:**
```markdown
### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
- [ ] Another criterion
- [ ] Typecheck passes
- [ ] **[If modifying existing code]** Existing tests still pass
- [ ] **[UI stories]** Verify in browser using dev-browser skill

**Integration Notes:**
- Modifies: `src/components/TaskList.tsx`
- Uses: `src/components/ui/Button.tsx`
- Adds: `src/components/TaskFilter.tsx`
```

### 6. Functional Requirements
Numbered list aligned with existing patterns.

### 7. Non-Goals (Out of Scope)
What this feature will NOT include.

### 8. Technical Considerations
- Alignment with existing architecture
- Performance impact on existing features
- Testing strategy for integration

### 9. Success Metrics
How will success be measured?

### 10. Open Questions
Remaining questions or areas needing clarification.

---

## Story Ordering for Brownfield

**Order stories to minimize integration risk:**

1. **Schema/migrations** - Database changes first (so other stories can use them)
2. **Backend changes** - API/server modifications
3. **Shared utilities** - Any new lib code
4. **UI components** - New components that use backend
5. **Integration** - Connecting new code to existing features
6. **Testing/polish** - Additional tests, edge cases

---

## Writing for Brownfield Implementation

Since there IS existing code:

- Reference specific file paths when known
- Note which existing components to reuse vs. create new
- Highlight any pattern deviations and justify them
- Include "Existing tests still pass" in acceptance criteria when modifying code
- Consider feature flags for risky changes
- Document rollback considerations

### Pattern Conformance

When the codebase has established patterns:

**Good:** "Create `TaskFilter.tsx` following the pattern in `UserFilter.tsx`"

**Bad:** "Create a filter component" (too vague, might not match existing patterns)

---

## Output

- **Format:** Markdown (`.md`)
- **Location:** `tasks/`
- **Filename:** `prd-[feature-name].md` (kebab-case)

---

## Example PRD (Brownfield)

```markdown
# PRD: Task Priority System

## Introduction

Add priority levels to the existing task management system. Users can mark tasks as high/medium/low priority with visual indicators and filtering. This extends the current task list and task editing functionality.

## Goals

- Allow assigning priority (high/medium/low) to any task
- Provide clear visual differentiation between priority levels
- Enable filtering by priority in the existing task list
- Default new tasks to medium priority

## Integration Points

### Existing Components to Modify
- `src/components/TaskCard.tsx` - Add priority badge display
- `src/components/TaskEditModal.tsx` - Add priority selector
- `src/components/TaskList.tsx` - Add priority filter to header
- `src/server/actions/tasks.ts` - Add priority to create/update actions

### Existing Components to Reuse
- `src/components/ui/Badge.tsx` - Use with color variants for priority
- `src/components/ui/Select.tsx` - Use for priority dropdown
- `src/components/ui/FilterDropdown.tsx` - Use for list filter

### New Files to Create
- `prisma/migrations/xxx_add_task_priority.sql` - Migration file
- `src/lib/priority.ts` - Priority enum and helper functions

### Database Changes
- Add `priority` column to `tasks` table: enum('high', 'medium', 'low')
- Default value: 'medium'
- Migration required: Yes (non-breaking, adds column with default)

## Compatibility

### Backward Compatibility
- Existing tasks default to 'medium' priority
- All existing API calls continue to work
- Priority parameter is optional in create/update

### Migration Requirements
- Run Prisma migration to add column
- Backfill not required (default handles existing rows)

### Deprecations
- None

## User Stories

### US-001: Add priority field to database
**Description:** As a developer, I need to store task priority so it persists.

**Acceptance Criteria:**
- [ ] Add priority column to tasks table: 'high' | 'medium' | 'low' (default 'medium')
- [ ] Update Prisma schema
- [ ] Generate and run migration successfully
- [ ] Existing tests still pass
- [ ] Typecheck passes

**Integration Notes:**
- Modifies: `prisma/schema.prisma`
- Generates: New migration file

### US-002: Display priority badge on task cards
**Description:** As a user, I want to see task priority at a glance.

**Acceptance Criteria:**
- [ ] Each task card shows colored priority badge
- [ ] Badge colors: red=high, yellow=medium, gray=low
- [ ] Uses existing Badge component with color prop
- [ ] Priority visible without hovering
- [ ] Existing tests still pass
- [ ] Typecheck passes
- [ ] Verify in browser using dev-browser skill

**Integration Notes:**
- Modifies: `src/components/TaskCard.tsx`
- Uses: `src/components/ui/Badge.tsx`

### US-003: Add priority selector to task edit
**Description:** As a user, I want to change a task's priority when editing.

**Acceptance Criteria:**
- [ ] Priority dropdown in TaskEditModal
- [ ] Shows current priority as selected
- [ ] Saves immediately on selection change
- [ ] Uses existing Select component
- [ ] Existing tests still pass
- [ ] Typecheck passes
- [ ] Verify in browser using dev-browser skill

**Integration Notes:**
- Modifies: `src/components/TaskEditModal.tsx`
- Modifies: `src/server/actions/tasks.ts` (updateTask action)
- Uses: `src/components/ui/Select.tsx`

### US-004: Filter tasks by priority
**Description:** As a user, I want to filter the task list by priority.

**Acceptance Criteria:**
- [ ] Filter dropdown with options: All | High | Medium | Low
- [ ] Follows existing filter pattern (FilterDropdown component)
- [ ] Filter persists in URL params
- [ ] Empty state when no tasks match
- [ ] Existing tests still pass
- [ ] Typecheck passes
- [ ] Verify in browser using dev-browser skill

**Integration Notes:**
- Modifies: `src/components/TaskList.tsx`
- Uses: `src/components/ui/FilterDropdown.tsx`
- Pattern reference: See existing status filter implementation

## Functional Requirements

- FR-1: Priority stored in database with enum type
- FR-2: All existing task operations continue to work unchanged
- FR-3: New tasks default to 'medium' priority if not specified
- FR-4: Badge component reused with new color variants

## Non-Goals

- No priority-based notifications
- No automatic priority based on due date
- No priority inheritance for subtasks
- No bulk priority editing (future enhancement)

## Technical Considerations

- Follow existing component patterns in src/components/ui/
- Use existing form handling pattern from TaskEditModal
- Filter state via URL params (matches existing status filter)
- No new dependencies required

## Success Metrics

- Priority change completes in under 2 clicks
- All existing tests continue to pass
- No regression in task list performance

## Open Questions

- Should priority affect default sort order?
- Should we add keyboard shortcuts (like existing status toggle)?
```

---

## Security: No Hardcoded Secrets

If the user's description mentions specific passwords, API keys, tokens, or credentials:

1. **NEVER put literal credentials in the PRD or acceptance criteria**
2. **Convert to environment variables:** e.g. "password 12345678" → "use `ADMIN_PASSWORD` from environment"
3. **Use `.env.example` pattern:** Document required env vars with placeholder values
4. **Seed data:** For initial users/admin accounts, reference env vars: `ADMIN_EMAIL`, `ADMIN_PASSWORD`

**Example transformation:**
- User says: "make user admin@foo.com with password secret123"
- PRD says: "Create admin seed using `ADMIN_EMAIL` and `ADMIN_PASSWORD` env vars, documented in `.env.example`"

---

## Checklist

Before saving the PRD:

- [ ] Reviewed existing codebase context
- [ ] Asked integration-focused questions
- [ ] Documented Integration Points section
- [ ] Documented Compatibility considerations
- [ ] Stories reference specific files to modify
- [ ] Stories include "Existing tests still pass" where applicable
- [ ] Follows existing patterns (or documents deviations)
- [ ] Non-goals prevent scope creep
- [ ] **No hardcoded secrets** - credentials use env vars
- [ ] Saved to `tasks/prd-[feature-name].md`
