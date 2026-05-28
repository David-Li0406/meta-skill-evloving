# Workflow State Management

This document describes how to track and manage progress through the PRD-Spec workflow.

## State File Location

**Path:** `docs/prd/.prd-workflow-state.json`

The state file should be created in the project's `docs/prd/` directory to keep it alongside other PRD workflow documentation.

## State File Format

### Standard Mode (New Products)

```json
{
  "mode": "standard",
  "completed_steps": ["prd-init", "prd-user-personas"],
  "current_step": "prd-generate-features",
  "started_at": "2024-01-21T10:00:00Z",
  "last_updated": "2024-01-21T11:30:00Z"
}
```

### Backfill Mode (Existing Codebases)

```json
{
  "mode": "backfill",
  "backfill_source": "./src",
  "validation_status": "pending",
  "validated_items": 0,
  "total_items": 42,
  "completed_steps": ["backfill-init", "backfill-behavior"],
  "current_step": "backfill-tests",
  "started_at": "2024-01-21T10:00:00Z",
  "last_updated": "2024-01-21T11:30:00Z"
}
```

### Import Mode (Existing Complete PRDs)

```json
{
  "mode": "import",
  "import_source": "docs/prd/PRD-COMPLETE.md",
  "import_timestamp": "2024-01-21T10:00:00Z",
  "completed_steps": [
    "prd-init",
    "prd-user-personas",
    "prd-generate-features",
    "prd-user-journeys",
    "prd-functional-requirements",
    "prd-nfr",
    "prd-data-model",
    "prd-api-endpoints",
    "prd-technical-architecture"
  ],
  "current_step": null,
  "started_at": "2024-01-21T10:00:00Z",
  "last_updated": "2024-01-21T10:00:00Z",
  "import_report": {
    "source_file": "docs/prd/PRD-COMPLETE.md",
    "sections_found": 14,
    "sections_mapped": {
      "PRD.md": [1, 2, 11, 12, 13, 14],
      "product-vision.md": [3, 4, 5],
      "requirements.md": [6, 7],
      "technical-spec.md": [8, 9, 10]
    },
    "supplementary_sections": [],
    "unmapped_sections": []
  }
}
```

**Note:** After import, the next step is `prd-redteam-analysis` since all PRD content steps (1.0-1.8) are marked complete.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `mode` | string | Workflow mode: `standard` (default), `backfill`, or `import` |
| `completed_steps` | string[] | Array of step names that have been completed |
| `current_step` | string | The step currently in progress (if any) |
| `started_at` | ISO 8601 | When the workflow was first started |
| `last_updated` | ISO 8601 | When the state was last modified |

### Backfill-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `backfill_source` | string | Path to the codebase being analyzed |
| `validation_status` | string | Status of human validation: `pending`, `in_progress`, `complete` |
| `validated_items` | number | Count of items marked by human reviewer |
| `total_items` | number | Total items requiring validation |

### Import-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `import_source` | string | Path to the imported PRD file |
| `import_timestamp` | ISO 8601 | When the import was performed |
| `import_report` | object | Details about the import operation |

#### Import Report Schema

```json
{
  "source_file": "docs/prd/PRD-COMPLETE.md",
  "sections_found": 14,
  "sections_mapped": {
    "PRD.md": [1, 2, 11, 12, 13, 14],
    "product-vision.md": [3, 4, 5],
    "requirements.md": [6, 7],
    "technical-spec.md": [8, 9, 10]
  },
  "supplementary_sections": ["Registered Workflows", "Signals & Queries"],
  "unmapped_sections": []
}
```

## Step Names

Use these exact step names (kebab-case) for consistency:

### Phase 0: Backfill (Existing Codebase Analysis)

| Step Name | Description |
|-----------|-------------|
| `backfill-init` | Detect project type, frameworks, initialize inventory structure |
| `backfill-behavior` | Extract behavioral inventory (routes, data models, UI flows) |
| `backfill-tests` | Scan tests for intent signals, annotate inventory |
| `backfill-draft` | Generate draft PRD with validation markers |
| `backfill-finalize` | Generate validated PRD after human review |

**Note:** Phase 0 steps are only used when `/prd-spec backfill` is invoked. After `backfill-finalize`, the workflow continues to Phase 1 steps.

### Phase 1: PRD (Product Requirements Document)
| Step Name | Description |
|-----------|-------------|
| `prd-init` | Create initial PRD structure |
| `prd-user-personas` | Generate user personas and pain points |
| `prd-generate-features` | Generate features and epics |
| `prd-user-journeys` | Map user journeys |
| `prd-functional-requirements` | Define functional requirements |
| `prd-nfr` | Define non-functional requirements |
| `prd-data-model` | Design data model |
| `prd-api-endpoints` | Define API specifications |
| `prd-technical-architecture` | Design technical architecture |
| `prd-redteam-analysis` | Red team analysis and risk assessment |

### Phase 2: BDD (Behavior-Driven Development)
| Step Name | Description |
|-----------|-------------|
| `bdd-scenarios` | Generate BDD scenarios |
| `bdd-amigos` | Three Amigos review |
| `bdd-feature-split` | Split scenarios into feature files |
| `ui-spec` | Generate UI specification |
| `ui-implementation` | Implement UI from specification |

### Phase 3: TDD (Test-Driven Development)
| Step Name | Description |
|-----------|-------------|
| `tdd-redtest` | Write failing tests (Red phase) |
| `tdd-green-code` | Implement minimal code (Green phase) |
| `tdd-refactor` | Refactor while keeping tests green |

## PRD File Structure

The PRD is organized into 4 logical files to manage token limits:

```
docs/prd/
├── PRD.md                # Summary + Meta (~8K tokens)
│   ├── Section 1: Executive Summary
│   ├── Section 2: Goals and Success Metrics
│   ├── Section 11: MVP Scope
│   ├── Section 12: Risks and Mitigations
│   ├── Section 13: Timeline and Milestones
│   └── Section 14: Open Questions
│
├── product-vision.md     # The "What" (~15K tokens)
│   ├── Section 3: User Personas
│   ├── Section 4: Epics and User Stories
│   └── Section 5: User Journeys
│
├── requirements.md       # The "Criteria" (~20K tokens)
│   ├── Section 6: Functional Requirements
│   └── Section 7: Non-Functional Requirements
│
├── technical-spec.md     # The "How" (~30K tokens)
│   ├── Section 8: Technical Architecture
│   ├── Section 9: Data Model
│   └── Section 10: API Specifications
│
├── scenarios.md          # BDD Scenarios (Phase 2)
├── UI_SPEC.md            # UI Specification (Phase 2)
└── .prd-workflow-state.json  # Workflow state
```

### Step-to-File Mapping

| Step | Reads | Writes |
|------|-------|--------|
| `prd-init` | - | PRD.md, product-vision.md, requirements.md, technical-spec.md |
| `prd-user-personas` | PRD.md | product-vision.md (Section 3) |
| `prd-generate-features` | product-vision.md | product-vision.md (Section 4) |
| `prd-user-journeys` | product-vision.md | product-vision.md (Section 5) |
| `prd-functional-requirements` | product-vision.md | requirements.md (Section 6) |
| `prd-nfr` | product-vision.md, requirements.md | requirements.md (Section 7) |
| `prd-data-model` | product-vision.md, requirements.md | technical-spec.md (Section 9) |
| `prd-api-endpoints` | product-vision.md, requirements.md, technical-spec.md | technical-spec.md (Section 10) |
| `prd-technical-architecture` | product-vision.md, requirements.md, technical-spec.md | technical-spec.md (Section 8) |
| `prd-redteam-analysis` | All 4 files | PRD_REDTEAM_COMMENTS.md |
| `bdd-scenarios` | product-vision.md, requirements.md | scenarios.md |
| `bdd-amigos` | scenarios.md, product-vision.md | scenarios.md |
| `ui-spec` | product-vision.md, requirements.md, scenarios.md | UI_SPEC.md |

## State Determination Logic

When determining the current state, Claude should:

1. **Check for state file**: Read `docs/prd/.prd-workflow-state.json` if it exists
2. **Fall back to file checks**: If no state file, check for existence of:
   - `docs/prd/PRD.md` → `prd-init` completed
   - `docs/prd/product-vision.md` → `prd-init` completed
   - `docs/prd/requirements.md` → `prd-init` completed
   - `docs/prd/technical-spec.md` → `prd-init` completed
   - `docs/prd/scenarios.md` → `bdd-scenarios` completed
   - `docs/prd/features/*.feature` → `bdd-feature-split` completed
   - `docs/prd/features-manifest.json` → `bdd-feature-split` completed (manifest generated)
   - `docs/prd/UI_SPEC.md` → `ui-spec` completed
3. **Create state file**: On first step, create the state file

## Features Manifest

**Path:** `docs/prd/features-manifest.json`

The features manifest tracks all BDD scenarios with their verification status. It is:
- **Generated**: After `bdd-feature-split` step completes
- **Updated**: By the `verify` command when scenarios are verified

### Manifest Structure

```json
{
  "productName": "Product name from PRD",
  "generatedAt": "ISO-8601 timestamp",
  "lastUpdated": "ISO-8601 timestamp",
  "summary": {
    "total": 15,
    "passing": 5,
    "failing": 10,
    "byPriority": { "P0": 6, "P1": 5, "P2": 4 },
    "passingByPriority": { "P0": 2, "P1": 2, "P2": 1 }
  },
  "features": [
    {
      "scenarioId": "US-001-S01",
      "userStoryId": "US-001",
      "featureFile": "us_001_feature_name.feature",
      "scenarioTitle": "Scenario title from Gherkin",
      "priority": "P0",
      "category": "functional",
      "description": "Business context from @meta block",
      "steps": ["Setup step", "Action step", "Verification step"],
      "successMetrics": ["Metric from @meta.success_metrics"],
      "verificationMethod": "automated|browser|manual",
      "passes": false,
      "lastVerified": null,
      "testFile": null,
      "notes": ""
    }
  ]
}
```

### Verification Methods

| Method | Description | When Assigned |
|--------|-------------|---------------|
| `automated` | Run via test suite | API, database, logic scenarios |
| `browser` | Execute in browser | UI interactions, visual feedback |
| `manual` | Human verification | Visual design, subjective quality |

### Integration with TDD Cycle

**Option 1: Manual TDD via prd-spec (step by step)**

1. `tdd-redtest US-001-S01` - Write failing tests
2. `tdd-green-code US-001-S01` - Implement to pass tests
3. `tdd-refactor US-001-S01` - Clean up code
4. `verify US-001-S01` - Update manifest with pass/fail status

**Option 2: Automated TDD via build-it skill (recommended)**

Use the `/build-it` skill for automated TDD cycles:

```bash
/build-it              # Smart selection - picks best next scenario
/build-it US-001-S01   # Specific scenario
/build-it status       # Show progress
```

The `build-it` skill:
- Reads `features-manifest.json` automatically
- Runs full RED-GREEN-REFACTOR cycle
- Updates manifest with `passes=true` on completion
- Prioritizes scenarios by P0/P1/P2 and dependencies

The `verify` step is separate from TDD to allow flexibility (some scenarios need browser verification even if unit tests pass)

## Workflow Order

### Standard Mode (New Products)

Steps should be executed in this order:

```
1.  prd-init
2.  prd-user-personas
3.  prd-generate-features
4.  prd-user-journeys
5.  prd-functional-requirements
6.  prd-nfr
7.  prd-data-model
8.  prd-api-endpoints
9.  prd-technical-architecture
10. prd-redteam-analysis
11. bdd-scenarios
12. bdd-amigos
13. bdd-feature-split
14. ui-spec
15. ui-implementation
16. tdd-redtest
17. tdd-green-code
18. tdd-refactor
```

### Backfill Mode (Existing Codebases)

When using `/prd-spec backfill`, execute Phase 0 first, then continue to Phase 1:

```
Phase 0 (Backfill):
0.0 backfill-init       → Detect project, initialize inventory
0.1 backfill-behavior   → Extract behavioral inventory from code
0.2 backfill-tests      → Annotate inventory with test coverage
0.3 backfill-draft      → Generate draft PRD with validation markers
    ★ HUMAN GATE        → User runs `/prd-spec backfill validate`
0.4 backfill-finalize   → Generate validated PRD + user stories

Phase 1+ (Continue standard flow):
1.0 prd-init           → Skipped (PRD created by backfill-finalize)
1.1 prd-user-personas  → Continue from here
... (remaining steps as normal)
```

**Important:** After `backfill-draft`, the workflow STOPS and waits for human validation via `/prd-spec backfill validate`. This is a required checkpoint - the system cannot determine intent from code alone.

### Import Mode (Existing Complete PRDs)

When using `/prd-spec import`, the complete PRD is split into the 4-file structure and the workflow continues from `prd-redteam-analysis`:

```
Import:
- import              → Parse and split complete PRD into 4 files

Phase 1+ (Continue from redteam):
1.9 prd-redteam-analysis → First step after import
2.0 bdd-scenarios        → Continue as normal
... (remaining steps as normal)
```

**Note:** Import marks steps 1.0-1.8 as complete because the PRD content already exists. The workflow continues with red team analysis to validate the imported content.

## State Operations

### Reading State
```javascript
// Pseudo-code for reading state
function getWorkflowState(projectRoot) {
  const statePath = `${projectRoot}/docs/prd/.prd-workflow-state.json`
  if (fileExists(statePath)) {
    return JSON.parse(readFile(statePath))
  }
  return { completed_steps: [], current_step: null }
}
```

### Updating State
```javascript
// Pseudo-code for updating state
function updateWorkflowState(projectRoot, stepName, action) {
  const state = getWorkflowState(projectRoot)

  if (action === 'start') {
    state.current_step = stepName
  } else if (action === 'complete') {
    if (!state.completed_steps.includes(stepName)) {
      state.completed_steps.push(stepName)
    }
    state.current_step = null
  }

  state.last_updated = new Date().toISOString()
  if (!state.started_at) {
    state.started_at = state.last_updated
  }

  writeFile(statePath, JSON.stringify(state, null, 2))
}
```

### Getting Next Step
```javascript
// Pseudo-code for determining next step
function getNextStep(state) {
  // Import mode: Continue from prd-redteam-analysis (steps 1.0-1.8 already complete)
  if (state.mode === 'import') {
    const postImportSteps = [
      'prd-redteam-analysis', 'bdd-scenarios', 'bdd-amigos',
      'bdd-feature-split', 'ui-spec', 'ui-implementation',
      'tdd-redtest', 'tdd-green-code', 'tdd-refactor'
    ]
    for (const step of postImportSteps) {
      if (!state.completed_steps.includes(step)) return step
    }
    return null // All steps complete
  }

  // Backfill mode: Phase 0 first, then Phase 1+ (skip prd-init)
  if (state.mode === 'backfill') {
    const backfillSteps = [
      'backfill-init', 'backfill-behavior', 'backfill-tests',
      'backfill-draft', 'backfill-finalize'
    ]

    // Check backfill steps first
    for (const step of backfillSteps) {
      if (!state.completed_steps.includes(step)) {
        // Special: after backfill-draft, require validation
        if (step === 'backfill-finalize' &&
            state.validation_status !== 'complete') {
          return null // Blocked until validation via /prd-spec backfill validate
        }
        return step
      }
    }

    // After backfill complete, continue to Phase 1 (skip prd-init)
    const postBackfillSteps = [
      'prd-user-personas', 'prd-generate-features',
      'prd-user-journeys', 'prd-functional-requirements', 'prd-nfr',
      'prd-data-model', 'prd-api-endpoints', 'prd-technical-architecture',
      'prd-redteam-analysis', 'bdd-scenarios', 'bdd-amigos',
      'bdd-feature-split', 'ui-spec', 'ui-implementation',
      'tdd-redtest', 'tdd-green-code', 'tdd-refactor'
    ]
    for (const step of postBackfillSteps) {
      if (!state.completed_steps.includes(step)) return step
    }
    return null // All steps complete
  }

  // Standard mode: full step sequence
  const allSteps = [
    'prd-init', 'prd-user-personas', 'prd-generate-features',
    'prd-user-journeys', 'prd-functional-requirements', 'prd-nfr',
    'prd-data-model', 'prd-api-endpoints', 'prd-technical-architecture',
    'prd-redteam-analysis', 'bdd-scenarios', 'bdd-amigos',
    'bdd-feature-split', 'ui-spec', 'ui-implementation',
    'tdd-redtest', 'tdd-green-code', 'tdd-refactor'
  ]

  for (const step of allSteps) {
    if (!state.completed_steps.includes(step)) {
      return step
    }
  }
  return null // All steps complete
}
```

## Status Display Format

### Standard Mode

When showing status in standard mode, format as:

```
PRD-Spec Workflow Status
========================

Phase 1: PRD
  ✓ prd-init
  ✓ prd-user-personas
  → prd-generate-features (in progress)
  ○ prd-user-journeys
  ○ prd-functional-requirements
  ...

Phase 2: BDD
  ○ bdd-scenarios
  ○ bdd-amigos
  ...

Phase 3: TDD
  ○ tdd-redtest
  ○ tdd-green-code
  ○ tdd-refactor

Progress: 2/18 steps complete
```

### Backfill Mode

When showing status in backfill mode, format as:

```
PRD-Spec Workflow Status (Backfill Mode)
========================================
Source: ./src

Phase 0: Backfill
  ✓ backfill-init
  ✓ backfill-behavior
  → backfill-tests (in progress)
  ○ backfill-draft
  ★ HUMAN GATE (validation required after backfill-draft)
  ○ backfill-finalize

Validation Status: pending (0/42 items reviewed)

Phase 1: PRD
  ○ prd-user-personas (backfill skips prd-init)
  ...

Progress: 2/5 backfill steps complete
```

When validation is required (after backfill-draft):

```
PRD-Spec Workflow Status (Backfill Mode)
========================================
Source: ./src

Phase 0: Backfill
  ✓ backfill-init
  ✓ backfill-behavior
  ✓ backfill-tests
  ✓ backfill-draft
  ★ AWAITING VALIDATION
  ○ backfill-finalize

⚠️  Human validation required!
    Run: /prd-spec backfill validate
    Draft PRD: docs/prd/backfill-draft.md
    Items to review: 42

Validation Status: pending (0/42 items reviewed)
```

Legend:
- `✓` = completed
- `→` = in progress
- `○` = not started
- `★` = requires human action

## Redo Behavior

When redoing a step:
1. Remove the step from `completed_steps`
2. Set it as `current_step`
3. Execute the step
4. Add back to `completed_steps` when done

Steps that depend on the redone step may need to be re-executed as well.
