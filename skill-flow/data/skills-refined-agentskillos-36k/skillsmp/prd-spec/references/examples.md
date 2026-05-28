# PRD-Spec Example Sessions

This document shows example interaction sessions for the PRD-Spec workflow.

## Standard Workflow Example

```
User: /prd-spec init "A mobile app for tracking coffee consumption"

Claude: I'll start the PRD-Spec workflow for your coffee tracking app.

Creating initial PRD structure...
[Executes prd-init prompt with the description]

Created 4 PRD files:
- docs/prd/PRD.md (Executive Summary, Goals - Sections 1-2, 11-14)
- docs/prd/product-vision.md (Personas, Stories, Journeys - Sections 3-5)
- docs/prd/requirements.md (Functional, Non-Functional - Sections 6-7)
- docs/prd/technical-spec.md (Architecture, Data, APIs - Sections 8-10)

PRD.md initialized with Executive Summary and Goals.
Other sections contain placeholders for iterative development.

Next step: Run `/prd-spec` to generate user personas.
```

```
User: /prd-spec

Claude: Checking workflow state...
Next step: prd-user-personas

Generating user personas based on the PRD...
[Executes prd-user-personas prompt]

Created 3 user personas:
- Sarah (Coffee Enthusiast)
- Mike (Health-Conscious Professional)
- Emma (Cafe Owner)

Updated docs/prd/product-vision.md Section 3 with personas and pain points.
Next step: Run `/prd-spec` to generate features.
```

```
User: /prd-spec status

Claude: PRD-Spec Workflow Status
========================

Phase 1: PRD
  ✓ prd-init
  ✓ prd-user-personas
  → prd-generate-features (next)
  ○ prd-user-journeys
  ○ prd-functional-requirements
  ○ prd-nfr
  ○ prd-data-model
  ○ prd-api-endpoints
  ○ prd-technical-architecture
  ○ prd-redteam-analysis

Phase 2: BDD & UI
  ○ bdd-scenarios
  ○ bdd-amigos
  ○ bdd-feature-split
  ○ ui-spec
  ○ ui-implementation

Phase 3: TDD
  ○ tdd-redtest
  ○ tdd-green-code
  ○ tdd-refactor

Progress: 2/18 steps complete

Scenario Verification: 5/15 passing (33%)
  P0: 2/6 (33%)
  P1: 2/5 (40%)
  P2: 1/4 (25%)
```

The scenario verification summary is shown after `bdd-feature-split` generates the manifest.

## Backfill Workflow Example

```
User: /prd-spec backfill ./src

Claude: Starting backfill workflow for existing codebase at ./src

Detecting project type and structure...
[Executes backfill-init prompt]

Project Profile:
- Type: Web Application
- Framework: Next.js 14
- Language: TypeScript
- Package Manager: pnpm

Created docs/prd/backfill-inventory.md with scan targets.
Next step: Run `/prd-spec` to extract behavioral inventory.
```

```
User: /prd-spec

Claude: Checking workflow state...
Mode: backfill
Next step: backfill-behavior

Extracting behavioral inventory from codebase...
[Executes backfill-behavior prompt]

Extracted:
- 15 API routes
- 8 UI flows
- 6 data models
- 3 external integrations

Updated docs/prd/backfill-inventory.md with behavioral items.
Next step: Run `/prd-spec` to scan test coverage.
```

```
User: /prd-spec

Claude: Checking workflow state...
Mode: backfill
Next step: backfill-tests

Scanning tests for intent signals...
[Executes backfill-tests prompt]

Test coverage summary:
- 27 items tested (66%)
- 8 items partially tested
- 5 items untested
- 1 item with skipped tests

3 discrepancies found between tests and code.
Updated inventory with confidence levels.
Next step: Run `/prd-spec` to generate draft PRD.
```

```
User: /prd-spec

Claude: Checking workflow state...
Mode: backfill
Next step: backfill-draft

Generating draft PRD with validation markers...
[Executes backfill-draft prompt]

Created docs/prd/backfill-draft.md with:
- 12 [TESTED] items (high confidence)
- 5 [OBSERVED] items (needs review)
- 4 [?] items (unclear intent)

HUMAN VALIDATION REQUIRED

Please review docs/prd/backfill-draft.md and mark each item:
  [x] = INTENDED (keep as requirement)
  [-] = BUG (don't codify)
  [~] = DEPRECATED (remove)
  [?] = UNCLEAR (needs investigation)

When done, run: /prd-spec backfill validate
```

```
User: /prd-spec backfill validate

Claude: Processing human validation...
[Reads backfill-draft.md for marked items]

Validation results:
- 18 items marked INTENDED
- 2 items marked BUG
- 1 item marked DEPRECATED
- 0 items marked UNCLEAR

Generating validated PRD...
[Executes backfill-finalize prompt]

Created 4 PRD files:
- docs/prd/PRD.md (Executive Summary, Scope - Sections 1-2, 11-14)
- docs/prd/product-vision.md (User Stories from validation - Sections 3-5)
- docs/prd/requirements.md (Functional Requirements - Sections 6-7)
- docs/prd/technical-spec.md (Data Model, APIs - Sections 8-10)

Additional reports:
- docs/prd/backfill-exclusions.md (3 excluded items)
- docs/prd/backfill-test-gaps.md (coverage analysis)

Backfill complete. Workflow continues with standard Phase 1.
Next step: Run `/prd-spec` to generate user personas.
```

```
User: /prd-spec status

Claude: PRD-Spec Workflow Status (Backfill Mode)
========================================
Source: ./src

Phase 0: Backfill
  ✓ backfill-init
  ✓ backfill-behavior
  ✓ backfill-tests
  ✓ backfill-draft
  ✓ backfill-finalize

Validation Status: complete (18/21 items validated)

Phase 1: PRD
  ✓ prd-init (via backfill)
  → prd-user-personas (next)
  ○ prd-generate-features
  ...

Progress: 6/23 steps complete (backfill + standard)
```

## Export Example

```
User: /prd-spec export

Claude: Exporting PRD to single document...

Creating docs/prd/PRD-COMPLETE.md by concatenating:
1. PRD.md (Summary + Meta)
2. product-vision.md (Personas, Stories, Journeys)
3. requirements.md (Functional + Non-Functional)
4. technical-spec.md (Architecture, Data, APIs)

Export complete: docs/prd/PRD-COMPLETE.md
Total size: ~45K tokens
Use this file to share with stakeholders who want a single document.
```

## Import Workflow Example

```
User: /prd-spec import --dry-run

Claude: [DRY RUN] Import Preview
========================

Source: docs/prd/PRD-COMPLETE.md

Would create:
  - docs/prd/PRD.md (6 sections)
  - docs/prd/product-vision.md (3 sections)
  - docs/prd/requirements.md (2 sections)
  - docs/prd/technical-spec.md (3 sections + 2 supplementary)

Would backup and remove:
  docs/prd/PRD-COMPLETE.md → docs/prd/PRD-COMPLETE.md.bak (then delete original)

Section Mapping Preview:
  1. Executive Summary → PRD.md
  2. Goals and Success Metrics → PRD.md
  3. User Personas → product-vision.md
  4. Epics and User Stories → product-vision.md
  5. User Journeys → product-vision.md
  6. Functional Requirements → requirements.md
  7. Non-Functional Requirements → requirements.md
  8. Technical Architecture → technical-spec.md
  9. Data Model → technical-spec.md
  10. API Specifications → technical-spec.md
  11. MVP Scope → PRD.md
  12. Risks and Mitigations → PRD.md
  13. Timeline and Milestones → PRD.md
  14. Open Questions → PRD.md

Supplementary sections (appended to technical-spec.md):
  - Registered Workflows
  - Signals & Queries

Run without --dry-run to execute import.
```

```
User: /prd-spec import

Claude: Importing PRD from docs/prd/PRD-COMPLETE.md...

Parsing sections using topic-based matching...
Found 14 standard sections + 2 supplementary sections.

Import Complete
===============

Source: docs/prd/PRD-COMPLETE.md
Backup: docs/prd/PRD-COMPLETE.md.bak (original preserved, source removed)

Files Created:
  - docs/prd/PRD.md (Sections 1, 2, 11-14)
  - docs/prd/product-vision.md (Sections 3-5)
  - docs/prd/requirements.md (Sections 6-7)
  - docs/prd/technical-spec.md (Sections 8-10)

Sections Mapped: 14/14
Supplementary Sections: 2 (appended to technical-spec.md)
  - Registered Workflows
  - Signals & Queries

Workflow State:
  - Mode: import
  - Completed Steps: 9 (through prd-technical-architecture)
  - Next Step: prd-redteam-analysis

To verify the import:
  /prd-spec status    # View workflow progress
  /prd-spec export    # Round-trip test (should reproduce similar content)
```

```
User: /prd-spec status

Claude: PRD-Spec Workflow Status (Import Mode)
==========================================
Source: docs/prd/PRD-COMPLETE.md

Phase 1: PRD
  ✓ prd-init (via import)
  ✓ prd-user-personas (via import)
  ✓ prd-generate-features (via import)
  ✓ prd-user-journeys (via import)
  ✓ prd-functional-requirements (via import)
  ✓ prd-nfr (via import)
  ✓ prd-data-model (via import)
  ✓ prd-api-endpoints (via import)
  ✓ prd-technical-architecture (via import)
  → prd-redteam-analysis (next)

Phase 2: BDD & UI
  ○ bdd-scenarios
  ○ bdd-amigos
  ○ bdd-feature-split
  ○ ui-spec
  ○ ui-implementation

Phase 3: TDD
  ○ tdd-redtest
  ○ tdd-green-code
  ○ tdd-refactor

Progress: 9/18 steps complete
Next step: Run `/prd-spec` to perform red team analysis on imported PRD.
```

### Import from Custom Path

```
User: /prd-spec import docs/legacy/OldPRD.md --force

Claude: Importing PRD from docs/legacy/OldPRD.md...

Parsing sections using topic-based matching...
Found 12 standard sections.

Warning: 2 expected sections not found:
  - Section 13: Timeline and Milestones (will use placeholder)
  - Section 14: Open Questions (will use placeholder)

Import Complete
===============

Source: docs/legacy/OldPRD.md
Backup: docs/legacy/OldPRD.md.bak (original preserved, source removed)

Files Created (--force: overwrote existing):
  - docs/prd/PRD.md (Sections 1, 2, 11-12 + placeholders for 13-14)
  - docs/prd/product-vision.md (Sections 3-5)
  - docs/prd/requirements.md (Sections 6-7)
  - docs/prd/technical-spec.md (Sections 8-10)

Sections Mapped: 12/14 (2 placeholders added)

Next step: prd-redteam-analysis
```
