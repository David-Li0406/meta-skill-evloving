# Common Doc Update Patterns

## Pattern: New Server Action

1. Feature doc → Server Actions table (add new action)
2. Feature doc → Data Model (if new table access)
3. Feature doc → Testing Checklist (add verification)
4. FEATURE_INDEX → Coupling notes (if crosses features)

## Pattern: New Route/Page

1. Feature doc → User Surfaces table (add new route)
2. Workflow docs → Add step for new page
3. Component Index (if new components created)

## Pattern: Schema Migration

1. Feature doc → Data Model section (new columns/tables)
2. Feature doc → Testing Checklist (migration verification)
3. Provide → Production SQL with rollback procedure
4. FEATURE_INDEX → Coupling notes (if new dependencies)

## Pattern: Bug Fix

1. Feature doc → Invariants (add rule that was violated)
2. Feature doc → Testing Checklist (add regression test)
3. Workflow docs (if workflow step was broken)

## Pattern: RLS/Permission Change

1. Feature doc → Permissions & Security section
2. Feature doc → Invariants (permission constraints)
3. Provide → Production SQL for policy changes

## Pattern: UI Component Change

1. Feature doc → User Surfaces (if new/modified)
2. Component Index → Update component entry
3. Style Guide (if new patterns introduced)
