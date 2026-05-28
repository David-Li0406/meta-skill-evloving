# ADR 0024: Supplement Status Categorization (Avoid List)

## Context
The application needs to educate users about supplements that are harmful or ineffective for ADHD. We need a way to categorize these items in the database and provide safety-first UI experiences to prevent accidental intake.

## Decision
We introduced a `status` field to the `Supplement` entity to categorize supplements into three states:
1. `beneficial`: Standard recommended supplements.
2. `avoid`: Known harmful or ineffective substances.
3. `neutral`: Supporting substances with no direct impact.

## Implementation
- **Domain**: Added `status` field to `Supplement` entity, defaulting to `beneficial`.
- **Infrastructure**: Updated `SeedingService` to include harmful substances (e.g., Red Dye 40).
- **Presentation**:
    - `LibraryViewModel` filters by status via a toggle.
    - `SupplementDetail` hides "Add to Stack" and displays a red warning banner for `avoid` items.

## Consequences
- **Pros**: Clear visual distinction between helpful and harmful items; hard-coded safety to prevent adding harmful items to daily stacks.
- **Cons**: Requires manual categorization of new seed data.
- **Verification**: Covered by `library_view_model_test.dart`.
