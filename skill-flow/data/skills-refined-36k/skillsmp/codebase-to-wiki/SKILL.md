---
name: codebase-to-wiki
description: >
  Convert arbitrary codebases into structured Obsidian wikis with human-in-the-loop
  iterative refinement. Use when user asks to analyze, document, or create a wiki
  for a codebase. Supports three modes: Fresh wiki (plan structure collaboratively),
  Midway wiki (continue from tracked progress), Debugging (diagnose and fix issues).
  Features user-defined nested hierarchy, mandatory mermaid graphs and index paragraphs
  at non-atomic levels, multiple node types (code-bound, code-spanning, conceptual,
  external), and optional test coverage documentation.
  
  DO NOT USE when: code is still under active development, documenting generated/minified
  code, node_modules/vendor directories, during major refactoring, or when API
  reference docs (Swagger/TypeDoc) are the actual need.
---

# Codebase to Obsidian Wiki

Convert codebases into structured, navigable Obsidian knowledge graphs through iterative collaboration with the user.

## Table of Contents

- [Key Principles](#key-principles)
- [Core Mechanism: State Persistence](#core-mechanism-state-persistence)
- [Phase Detection](#phase-detection)
- [Wiki Hierarchy](#wiki-hierarchy)
- [Node Types](#node-types)
- [Phase Workflows](#phase-workflows)
- [Index Paragraph Pattern](#index-paragraph-pattern)
- [Mermaid Requirements](#mermaid-requirements)
- [Test Coverage (Optional)](#test-coverage-optional)

---

## Key Principles

1. **Human-in-the-loop:** Never proceed past a checkpoint without user confirmation
2. **Incremental persistence:** Record every decision immediately to `.wiki-progress.md`
3. **Top-down refinement:** Hierarchy emerges through dialogue; user defines levels iteratively
4. **Composable narratives:** Module narratives are referenceable from higher levels
5. **Graceful degradation:** For large codebases (50+ units), create stubs first, fill iteratively
6. **No line-level tracking:** Minimum granularity is function/class/component

---

## Core Mechanism: State Persistence

The `.wiki-progress.md` file captures all decisions immediately after they are made. This enables continuation from any interruption point. After each checkpoint: record the decision, update status fields, log the session action.

---

## Phase Detection

On every invocation, determine the current phase:

```
1. Check: Does wiki exist at target path?
   ├─ NO  → PHASE: Fresh (Planning)
   └─ YES → Check: .wiki-progress.md exists and valid?
            ├─ YES, status: debugging   → PHASE: Debug (Fix)
            ├─ YES, status: complete    → Ask user intent (extend? debug?)
            └─ OTHERWISE                → PHASE: Midway (Continue)
```

Midway handles all continuation scenarios: valid in-progress state, missing progress file, or malformed progress file. Read whatever state exists (or infer from wiki structure) and continue.

---

## Wiki Hierarchy

User-defined depth (not enforced to 3 levels). Work top-down: define higher levels first, approach granularity iteratively.

```
wiki-root/
├── HOME.md                    # Codebase level (mermaid + index paragraph)
├── .wiki-progress.md          # Progress tracking (hidden)
├── ModuleA/
│   ├── ModuleA.md             # Module narrative (mermaid + index paragraph)
│   ├── node1.md               # Atomic node
│   └── SubModule/             # Optional deeper nesting
│       ├── SubModule.md       # Sub-narrative
│       └── subnode.md
└── ModuleB/
    └── ...
```

**Rules:**

- Non-atomic levels: MUST have mermaid graph + index paragraph
- Atomic nodes: NO mermaid required
- Narrative files: Named `<Module>.md` in their folder
- Minimum granularity: Function, class, or component level (NEVER line numbers)

---

## Node Types

Four node kinds exist. See [references/templates.md](references/templates.md) for full frontmatter schemas.

| Kind | Description | Source Field |
|------|-------------|--------------|
| `code-bound` | 1:1 mapping to file/function/class | `path` + `function`/`class` |
| `code-spanning` | Concept across multiple files | Multiple `path` entries |
| `conceptual` | No direct code (math, architecture) | Optional `related_code` globs |
| `external` | Third-party dependencies | `package` + `version` |

---

## Phase Workflows

### Fresh Wiki (Planning)

**STEP 1: Initial Scan**
- Scan codebase structure (dirs, key files, package.json/requirements.txt)
- Identify stack and dependencies
- Present findings to user
- **CHECKPOINT:** "Is this overview accurate?"
- On confirm: Record stack, codebase_path in `.wiki-progress.md`

**STEP 2: Module Definition (Top-Down)**
- Propose initial high-level module breakdown
- **CHECKPOINT:** "Does this grouping make sense?"
  - User can merge, split, rename, nest deeper
- On confirm: Record module structure in `.wiki-progress.md`

**STEP 3: Granularity Calibration**
- Pick ONE module, propose atomic breakdown
- **CHECKPOINT:** "Is this the right atomic level?"
  - Iterate until agreed (minimum: function/class level)
- Apply pattern to remaining modules
- On confirm: Record atomic_granularity in `.wiki-progress.md`

**STEP 4: Configuration Options**
- **CHECKPOINT:** "Include code snippets?" (default: yes)
- **CHECKPOINT:** "Document tests? If yes, to what granularity?"
  - Options: none | per-module | per-node
- **CHECKPOINT:** "Custom frontmatter properties to track?"
  - e.g., `tested_by`, `last_reviewed`, `complexity`
- **CHECKPOINT:** "Batch size per session?" (default: 5 nodes)
- On confirm: Record all options in `.wiki-progress.md`

**STEP 5: Generate Plan**
- Create HOME.md with structure
- Finalize `.wiki-progress.md` with full checklist (status: in-progress)
- **CHECKPOINT:** "Ready to start? Adjust priority?"

---

### Midway Wiki (Continue)

**STEP 1: Load State**

IF `.wiki-progress.md` exists and valid:
- Read progress file
- Identify next batch (default: 5 nodes)
- Show user what's next

ELSE (missing or malformed):
- Scan wiki folder structure
- Read HOME.md frontmatter for original settings
- Identify which modules/nodes exist vs. missing
- **CHECKPOINT:** "Found existing wiki without valid progress tracking. Inferred state: [summary]. Continue from here?"
- Regenerate `.wiki-progress.md` from inferred state

**STEP 2: Document Batch**
- Create/update nodes from queue
- Update parent narrative if batch completes a module
- Update `.wiki-progress.md` after each node

**STEP 3: Checkpoint**
- **CHECKPOINT:** "Continue, pause, or adjust scope?"

---

### Debug Wiki (Fix)

**STEP 1: Diagnosis**
- Scan existing wiki structure
- Cross-reference with current codebase
- Identify issues:
  - `broken_links`: Note references non-existent note
  - `orphan_notes`: Not linked from any parent
  - `stale_notes`: Source file no longer exists or was renamed
  - `missing_notes`: Code exists, no documentation
  - `structural`: Wrong hierarchy level

**STEP 2: Plan Proposal**
- Present categorized issue list
- **CHECKPOINT:** "Which issues to address?"
- Add debug queue to `.wiki-progress.md` (status: debugging)

**STEP 3: Execute**
- Fix issues one-by-one
- Update `.wiki-progress.md` after each fix

**STEP 4: Completion**
- **CHECKPOINT:** "All selected issues resolved. Delete progress file or keep for future maintenance?"

---

## Index Paragraph Pattern

Non-atomic notes MUST include a narrative paragraph with embedded wikilinks serving as both documentation AND navigation:

```markdown
## Overview

The Authentication module handles user identity verification and session
management. It consists of [[validateToken]] for JWT verification,
[[refreshSession]] for token renewal, [[logout]] for session termination,
and [[authMiddleware]] which guards protected routes. This module depends
on [[Database]] for user lookups and [[Config]] for secret management.
```

Narratives are composable: module narratives can be referenced from higher levels (e.g., `[[Vision Module|visual perception]]` in HOME.md).

---

## Mermaid Requirements

All non-atomic levels MUST include a mermaid graph. External dependencies MUST be visually distinguished using CSS class + subgraph.

See [references/mermaid-patterns.md](references/mermaid-patterns.md) for:

- Standard external dependency marking pattern
- HOME level (TB direction) examples
- Module level (LR direction) examples
- Deep nesting patterns
- Cross-module reference notation
- Node shape conventions
- Color-blind friendly styling

---

## Test Coverage (Optional)

When user enables test coverage:

- Tests are **subsections within existing nodes**, NOT separate nodes
- Tests do not help understand code logic; they verify behavior
- Include only when user explicitly requests

```markdown
## Tests

| Test | Description | Status |
|------|-------------|--------|
| `test_validate_valid_token` | Accepts well-formed JWT | ✅ |
| `test_validate_expired` | Rejects expired tokens | ✅ |
```

---

## References

- [references/templates.md](references/templates.md) - Frontmatter schemas and note templates
- [references/mermaid-patterns.md](references/mermaid-patterns.md) - Diagram patterns and conventions
