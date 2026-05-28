---
name: auditing-codebase
description: Use when asked to audit, review, or document the codebase for stubs, incomplete features, or implementation status. Also use when onboarding to understand what exists vs what's missing.
---

# Auditing Codebase

Systematic audit of a codebase to document (1) the intended design, (2) what's incomplete/stubbed, and (3) what's implemented and how. Produces three Serena memories as deliverables.

## Deliverables

| Memory | Purpose |
|--------|---------|
| `design_spec` | Living spec collated from all design documents — what SHOULD exist |
| `unimplemented_features` | Gaps between design_spec and code — what's MISSING |
| `implementation_guide` | Module-by-module documentation — what DOES exist |

**IMPORTANT:** You MUST create/update memories using `mcp__serena__write_memory`. A report in the conversation is NOT a deliverable — the memories ARE the deliverables.

---

## Execution Flow

```
Phase 1: Collate Design Documents
         │
         ▼ (must complete first)
    ┌────┴────┐
    │         │
    ▼         ▼
Phase 2    Phase 3
(gaps)     (implementations)
    │         │
    ▼         ▼
  unimplemented_features    implementation_guide
```

**Phase 1 is a prerequisite** — Phase 2 needs `design_spec` for cross-referencing.

**Phase 2 and 3 can run in parallel** — they read the same codebase but produce independent memories. After Phase 1 completes, dispatch both as parallel subagents:

```
Task(subagent_type="general-purpose", prompt="Execute Phase 2 of auditing-codebase skill...")
Task(subagent_type="general-purpose", prompt="Execute Phase 3 of auditing-codebase skill...")
```

---

## Phase 1: Collate Design Documents

**Purpose:** Build or update the `design_spec` memory — the canonical reference for what was intended.

### Step 1: Check Existing Memory

```
mcp__serena__list_memories()
```

If `design_spec` exists, read it to see:
- Which documents have been processed (listed in "Source Documents" section)
- When it was last updated

### Step 2: Find Design Documents

Search for design docs in common locations:
- `docs/plans/`
- `docs/design/`
- `docs/specs/`
- `docs/architecture/`
- Root-level `DESIGN.md`, `ARCHITECTURE.md`, `SPEC.md`

Use `mcp__serena__find_file` with patterns like `*.md` in these directories.

### Step 3: Identify New Documents

Compare found documents against those already listed in `design_spec` memory.
Only process documents NOT already in the "Source Documents" section.

If no new documents and `design_spec` exists → Skip to Phase 2.

### Step 4: Extract Key Information

For each NEW design document, extract:
- **Features/Components** described
- **Data models** (schemas, structures)
- **Workflows/Flows** (how things connect)
- **Configuration options** mentioned
- **CLI commands** or APIs defined
- **Key design decisions** and rationale

### Step 5: Update design_spec Memory

Merge new information into the `design_spec` memory. Structure:

```markdown
# Design Specification

**Last updated:** YYYY-MM-DD

## Source Documents

| Document | Date Processed | Status |
|----------|----------------|--------|
| docs/plans/2026-01-20-design.md | 2026-01-21 | Archived |
| docs/plans/2026-01-25-feature-x.md | 2026-01-26 | Archived |

## Architecture

[High-level architecture from design docs]

## Components

### Component Name
- **Purpose:** [from design doc]
- **Responsibilities:** [from design doc]
- **Interfaces:** [from design doc]

## Data Models

### Table/Schema Name
[Fields, relationships, purpose]

## Configuration

| Option | Purpose | Default |
|--------|---------|---------|
| option_name | [from design doc] | [value] |

## CLI Commands

| Command | Purpose |
|---------|---------|
| command | [from design doc] |

## Workflows

### Workflow Name
[Sequence of operations from design doc]

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Why X over Y | [from design doc] |
```

### Step 6: Archive Processed Documents

Move processed design docs to an `archived/` subdirectory:
- `docs/plans/file.md` → `docs/plans/archived/file.md`

This signals the document has been incorporated into `design_spec`.

**Alternative:** If moving files isn't desired, add a header to the doc:
```markdown
<!-- Incorporated into design_spec memory: 2026-01-21 -->
```

---

## Phase 2: Find Incomplete Code

### Search Patterns

Run these searches using Serena's `search_for_pattern`:

```
# Explicit markers
TODO|FIXME|XXX|HACK|STUB|WIP

# Code stubs
NotImplementedError|raise NotImplemented

# Placeholder patterns
not.*implemented|coming soon|TBD|unimplemented

# Suspicious returns (check context)
return None$|return \[\]|return \{\}

# Empty bodies (check context)
^\s*pass\s*$
^\s*\.\.\.\s*$

# Deferred work
placeholder|temporary|later|eventually|for now
```

### Cross-Reference Against design_spec Memory

**This is the key step.** Read the `design_spec` memory and for each item:
1. Search codebase for the feature/component
2. Check if it's fully implemented, partially implemented, or missing
3. Document gaps in `unimplemented_features`

### Check Config vs Usage

For each config option in `design_spec`:
1. Find where it's defined in code
2. Search for where it's actually used
3. Flag config that's defined but never read by runtime code

### Check Schema vs Code

For each data model in `design_spec`:
1. Find the schema definition
2. Find insert/update/query functions
3. Flag tables that exist but are never written to

---

## Phase 3: Document Implementations

### For Each Module

Use `get_symbols_overview` then `find_symbol` with `include_body=true` for key classes/functions.

Document:
- **Classes**: Purpose, key methods, state they manage
- **Functions**: What they do, inputs/outputs, side effects
- **Data flow**: How data moves between components
- **External dependencies**: Subprocesses, APIs, files

### Architecture Diagram

Create ASCII diagram showing module relationships:
```
┌──────────┐    ┌──────────┐
│  Module  │───▶│  Module  │
└──────────┘    └──────────┘
```

### Key Design Decisions

Document WHY certain approaches were chosen. Cross-reference with `design_spec` for intended rationale.

---

## Memory Structures

### `design_spec` Memory

```markdown
# Design Specification

**Last updated:** YYYY-MM-DD

## Source Documents
[Table of processed docs with dates]

## Architecture
[From design docs]

## Components
[From design docs]

## Data Models
[From design docs]

## Configuration
[From design docs]

## CLI Commands
[From design docs]

## Workflows
[From design docs]

## Design Decisions
[From design docs]
```

### `unimplemented_features` Memory

```markdown
# Unimplemented Features and Stubs

**Last audited:** YYYY-MM-DD

## Explicit Stubs
[Location, current behavior, expected behavior]

## Config Defined But Not Used
[Config key, where defined, what design_spec says it should do]

## Database Tables Not Populated
[Table name, schema exists, no insert function]

## Design Spec Gaps
[Feature in design_spec, not in code — reference the spec section]

## Priority Recommendations
[High/Medium/Low with rationale]

## Verification Commands
[Shell commands to re-check this list]
```

### `implementation_guide` Memory

```markdown
# Implementation Guide

**Last updated:** YYYY-MM-DD

## Architecture Overview
[ASCII diagram]

## Module: name.py
**Purpose:** [one line]
### Classes
### Functions
### Data Flow

[Repeat for each module]

## Key Design Decisions
[Why certain approaches — cross-ref design_spec]

## Testing
[Test file locations, how to run]
```

---

## Checklist

### Phase 1: Design Collation (run first)
- [ ] Check if `design_spec` memory exists
- [ ] Find all design documents in `docs/plans/`, `docs/design/`, etc.
- [ ] Identify NEW documents not yet processed
- [ ] Extract features, schemas, config, commands, workflows from new docs
- [ ] Update `design_spec` memory with new information
- [ ] Archive or mark processed documents
- [ ] **Dispatch Phase 2 and Phase 3 as parallel subagents**

### Phase 2: Gap Analysis (can run parallel with Phase 3)
- [ ] Run all search patterns for stubs/incomplete code
- [ ] Cross-reference EACH item in `design_spec` against codebase
- [ ] Check config definitions vs usage
- [ ] Check database schema vs insert functions
- [ ] Write `unimplemented_features` memory

### Phase 3: Implementation Documentation (can run parallel with Phase 2)
- [ ] Get symbols overview for each module using `mcp__serena__get_symbols_overview`
- [ ] Read key class/function bodies using `mcp__serena__find_symbol` with `include_body=true`
- [ ] Create architecture diagram
- [ ] Write `implementation_guide` memory
- [ ] Include verification commands

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping Phase 1 | Design spec is essential for gap analysis — always collate first |
| Re-reading already-processed design docs | Check "Source Documents" in `design_spec` before reading |
| Not archiving processed docs | Archive to prevent re-processing and signal incorporation |
| Writing report to conversation | Use `mcp__serena__write_memory` — memories are the deliverables |
| Missing placeholder returns like `return (0, 0)` | Search for suspicious return patterns, check context |
| Shallow gap analysis | Cross-reference EACH design_spec item, not just search for stubs |
| Running Phase 2 and 3 sequentially | Dispatch as parallel subagents after Phase 1 completes |
