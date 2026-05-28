---
name: prd-spec
description: PRD workflow for building products from idea to implementation. Use when (1) starting a new product, (2) creating PRD documentation, (3) generating BDD scenarios, (4) building UI specs, (5) TDD implementation. Guides through 18-step process: PRD -> BDD -> UI -> TDD.
---

# PRD-Spec Workflow

A comprehensive workflow for building products from idea to implementation through structured phases.

## Quick Start

```bash
# Standard workflow (new products)
/prd-spec                    # Check state, run next step
/prd-spec status             # Show progress only
/prd-spec init "My App"      # Start with product description
/prd-spec bdd-scenarios      # Jump to specific step
/prd-spec redo prd-init      # Re-run a completed step
/prd-spec verify US-001-S01  # Verify specific scenario
/prd-spec export             # Concatenate all PRD files into one document

# Import workflow (existing complete PRDs)
/prd-spec import             # Import from PRD-COMPLETE.md or PRD.md
/prd-spec import docs/other/Complete.md  # Import from specific path
/prd-spec import --dry-run   # Preview without writing files
/prd-spec import --force     # Overwrite existing files

# Backfill workflow (existing codebases)
/prd-spec backfill           # Start backfill from current directory
/prd-spec backfill ./src     # Backfill from specific path
/prd-spec backfill validate  # Human validation gate (after draft)
/prd-spec backfill skip      # Skip to Phase 1 with current state
```

## Invocation Patterns

| Command | Behavior |
|---------|----------|
| `/prd-spec` or `/prd-spec next` | Check state, run next step |
| `/prd-spec <step>` | Run specific step (use hyphens) |
| `/prd-spec status` | Show workflow progress only |
| `/prd-spec init "description"` | Start with inline description |
| `/prd-spec redo <step>` | Re-run a previous step |
| `/prd-spec verify <id>` | Verify scenario (`US-001-S01`, `all`, or `failing`) |
| `/prd-spec export` | Create PRD-COMPLETE.md from all 4 PRD files |
| `/prd-spec import [path]` | Split complete PRD into 4-file structure |
| `/prd-spec backfill [path]` | Start backfill mode |
| `/prd-spec backfill validate` | Complete human validation |

## Workflow Phases

### Phase 0: Backfill (Optional - for existing codebases)

| Step | Name | Output |
|------|------|--------|
| 0.0 | `backfill-init` | Project detection & inventory structure |
| 0.1 | `backfill-behavior` | Behavioral inventory (routes, UI, data) |
| 0.2 | `backfill-tests` | Test coverage annotations |
| 0.3 | `backfill-draft` | Draft PRD with validation markers |
| **GATE** | **Human Validation** | **User marks items as INTENDED/BUG/DEPRECATED** |
| 0.4 | `backfill-finalize` | Validated PRD + user stories |

**Key Principle:** Code shows BEHAVIOR, not INTENT. Human validation required.

### Phase 1: PRD (10 steps)

| Step | Name | Output |
|------|------|--------|
| 1.0 | `prd-init` | Initial PRD structure |
| 1.1 | `prd-user-personas` | User personas & pain points |
| 1.2 | `prd-generate-features` | Epics, features, prioritization |
| 1.3 | `prd-user-journeys` | User journey maps |
| 1.4 | `prd-functional-requirements` | Functional requirements |
| 1.5 | `prd-nfr` | Non-functional requirements |
| 1.6 | `prd-data-model` | Data model design |
| 1.7 | `prd-api-endpoints` | API specifications |
| 1.8 | `prd-technical-architecture` | Technical architecture |
| 1.9 | `prd-redteam-analysis` | Risk analysis & gaps |

### Phase 2: BDD & UI (5 steps)

| Step | Name | Output |
|------|------|--------|
| 2.0 | `bdd-scenarios` | BDD Gherkin scenarios |
| 2.1 | `bdd-amigos` | Three Amigos review |
| 2.2 | `bdd-feature-split` | Split into .feature files |
| 2.3 | `ui-spec` | UI specification document |
| 2.4 | `ui-implementation` | Implement UI from spec |

### Phase 3: TDD (3 steps)

| Step | Name | Output |
|------|------|--------|
| 3.0 | `tdd-redtest` | Failing tests (Red) |
| 3.1 | `tdd-green-code` | Minimal implementation (Green) |
| 3.2 | `tdd-refactor` | Refactor with tests passing |

> **Alternative: Use `/build-it` skill**
> After generating `features-manifest.json` in Phase 2, you can use the standalone `/build-it` skill for TDD implementation. It provides:
> - Smart scenario selection based on priority and dependencies
> - Automated RED-GREEN-REFACTOR cycle
> - Automatic manifest updates when scenarios pass
> - Run `/build-it status` to see progress

## State Management

Progress tracked in `docs/prd/.prd-workflow-state.json`. See `references/workflow-state.md` for full details.

State is determined by:
1. Reading state file if exists
2. Falling back to file existence checks (PRD.md, scenarios.md, etc.)
3. Creating state file on first step

## Execution Instructions

When the user invokes `/prd-spec`:

1. **Parse Arguments** - Determine action: `next`, `status`, `step`, `redo`, `backfill`
2. **Check/Create State** - Read `docs/prd/.prd-workflow-state.json` or create if missing
3. **Determine Next Step** - Use `getNextStep(state)` logic from `references/workflow-state.md`
4. **Execute Step**:
   - Read prompt from `references/prompts/{step-name}.md`
   - Replace `$ARGUMENTS` with any provided arguments
   - If arguments required but not provided, ask the user
   - Execute the prompt instructions
   - Update state file on completion

## Step Prompts

### Phase 0: Backfill

| Step | Prompt File |
|------|-------------|
| `backfill-init` | `references/prompts/0.0-backfill-init.md` |
| `backfill-behavior` | `references/prompts/0.1-backfill-behavior.md` |
| `backfill-tests` | `references/prompts/0.2-backfill-tests.md` |
| `backfill-draft` | `references/prompts/0.3-backfill-draft.md` |
| `backfill-finalize` | `references/prompts/0.4-backfill-finalize.md` |

### Phase 1-3: Standard

| Step | Prompt File |
|------|-------------|
| `prd-init` | `references/prompts/1.0-prd-init.md` |
| `prd-user-personas` | `references/prompts/1.1-prd-user-personas.md` |
| `prd-generate-features` | `references/prompts/1.2-prd-generate-features.md` |
| `prd-user-journeys` | `references/prompts/1.3-prd-user-journeys.md` |
| `prd-functional-requirements` | `references/prompts/1.4-prd-functional-requirements.md` |
| `prd-nfr` | `references/prompts/1.5-prd-nfr.md` |
| `prd-data-model` | `references/prompts/1.6-prd-data-model.md` |
| `prd-api-endpoints` | `references/prompts/1.7-prd-api-endpoints.md` |
| `prd-technical-architecture` | `references/prompts/1.8-prd-technical-architecture.md` |
| `prd-redteam-analysis` | `references/prompts/1.9-prd-redteam-analysis.md` |
| `bdd-scenarios` | `references/prompts/2.0-bdd-scenarios.md` |
| `bdd-amigos` | `references/prompts/2.1-bdd-amigos.md` |
| `bdd-feature-split` | `references/prompts/2.2-bdd-feature-split.md` |
| `ui-spec` | `references/prompts/2.3-ui-spec.md` |
| `ui-implementation` | `references/prompts/2.4-ui-implementation.md` |
| `tdd-redtest` | `references/prompts/3.0-tdd-redtest.md` |
| `tdd-green-code` | `references/prompts/3.1-tdd-green-code.md` |
| `tdd-refactor` | `references/prompts/3.2-tdd-refactor.md` |
| `verify` | `references/prompts/verify.md` |
| `import` | `references/prompts/import.md` |

## Arguments

| Step | Arguments |
|------|-----------|
| `prd-init` | Product description (required) |
| `prd-generate-features` | Additional feature ideas (optional) |
| `tdd-redtest` | Scenario ID (required) |
| `tdd-green-code` | Scenario ID (required) |
| `tdd-refactor` | Scenario ID (required) |
| `verify` | Scenario ID, `all`, or `failing` (optional, defaults to `failing`) |
| `import` | Source path (optional), `--dry-run`, `--force` |
| `backfill` | Source path (optional, defaults to cwd) |

If required arguments not provided, prompt the user.

## Output Files

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

### Export Command

Use `/prd-spec export` to create a single `PRD-COMPLETE.md` by concatenating:
1. PRD.md
2. product-vision.md
3. requirements.md
4. technical-spec.md

This is useful for sharing with stakeholders who want one document.

## References

- **State Management**: `references/workflow-state.md` - Full state format, step names, getNextStep() logic
- **Example Sessions**: `references/examples.md` - Standard and backfill workflow examples
- **Step Prompts**: `references/prompts/*.md` - Individual step instructions
