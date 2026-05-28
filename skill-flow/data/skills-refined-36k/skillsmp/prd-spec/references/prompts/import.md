<prompt>
<context>
The user wants to import an existing complete PRD document and split it into the 4-file structure that the prd-spec workflow expects. This is the reverse of the `export` command.

**Arguments:** $ARGUMENTS

**Argument Parsing:**
- If no path provided: Auto-detect from `docs/prd/PRD-COMPLETE.md` or `docs/prd/PRD.md` (prefer PRD-COMPLETE.md)
- If `--dry-run` flag: Preview the import without writing files
- If `--force` flag: Overwrite existing files without prompting
- If path provided: Use that specific file as the import source

</context>
<role>
You are a document processor responsible for parsing comprehensive PRD documents and distributing their content into the correct file structure for the prd-spec workflow.
</role>
<execution_strategy>

## CRITICAL: Parallel Execution for Large PRDs

PRD documents can be very large (50K+ tokens). To handle this efficiently, **use parallel sub-agents via the Task tool**.

### Execution Pattern

1. **Step 1-2 (Parse)**: Run in main agent - locate file and identify section boundaries
2. **Step 3 (Generate Files)**: Launch **4 parallel sub-agents**, one for each target file:
   - Agent 1: Generate `PRD.md` (sections 1, 2, 11-14)
   - Agent 2: Generate `product-vision.md` (sections 3-5)
   - Agent 3: Generate `requirements.md` (sections 6-7)
   - Agent 4: Generate `technical-spec.md` (sections 8-10 + supplementary)
3. **Step 5-7 (Finalize)**: Run in main agent after all sub-agents complete

### Sub-Agent Prompts

Each sub-agent receives:
- The specific sections it needs to extract (by section number or header match)
- The source file path
- The target file template
- Instructions to write the file

Example parallel invocation:
```
Launch 4 Task agents in parallel:
1. "Write PRD.md with sections 1, 2, 11-14 from [source]"
2. "Write product-vision.md with sections 3-5 from [source]"
3. "Write requirements.md with sections 6-7 from [source]"
4. "Write technical-spec.md with sections 8-10 + supplementary from [source]"
```

### Why Parallel?

- Large PRDs exceed single-context token limits
- Each target file can be generated independently
- Parallel execution reduces total import time significantly
- Sub-agents can read specific portions of the source file

</execution_strategy>
<action>

## Step 1: Locate Source File

1. Parse arguments to determine source file path
2. If no path specified, check in order:
   - `docs/prd/PRD-COMPLETE.md` (exported complete PRD)
   - `docs/prd/PRD.md` (single-file PRD)
3. Verify source file exists; if not, report error and list available .md files in `docs/prd/`

## Step 2: Parse Sections (Topic-Based)

Read the source file and identify sections using **topic-based matching** rather than strict section numbers. PRD formats vary, so match by content/heading keywords:

### Topic Classification Rules

| Topic Pattern (case-insensitive) | Target File | Section Number |
|----------------------------------|-------------|----------------|
| `executive summary`, `overview`, `introduction` | PRD.md | 1 |
| `goals`, `success metrics`, `okr`, `kpi`, `business impact` | PRD.md | 2 |
| `personas`, `user types`, `stakeholders` | product-vision.md | 3 |
| `epics`, `user stories`, `features`, `capabilities` | product-vision.md | 4 |
| `journeys`, `user flows`, `workflows` | product-vision.md | 5 |
| `functional requirements`, `functional specs` | requirements.md | 6 |
| `non-functional`, `nfr`, `performance`, `security requirements`, `scalability` | requirements.md | 7 |
| `technical architecture`, `system architecture`, `tech stack` | technical-spec.md | 8 |
| `data model`, `database`, `entities`, `schema` | technical-spec.md | 9 |
| `api spec`, `api endpoints`, `rest api`, `api design` | technical-spec.md | 10 |
| `mvp`, `scope`, `in scope`, `out of scope` | PRD.md | 11 |
| `risks`, `mitigations`, `concerns` | PRD.md | 12 |
| `timeline`, `milestones`, `roadmap`, `phases` | PRD.md | 13 |
| `open questions`, `assumptions`, `dependencies`, `decisions` | PRD.md | 14 |

### Parsing Algorithm

```
1. Split document by level-2 headers (## ...)
2. For each section:
   a. Extract header text (remove any leading number like "## 1." or "## ")
   b. Match header against topic patterns (case-insensitive, partial match)
   c. Assign to target file and section number
   d. If no match, mark as "supplementary" for technical-spec.md
3. Track sections that don't match any pattern (warn user)
```

### Handling Numbered vs Unnumbered Headers

Accept both formats:
- `## 1. Executive Summary` → Topic: "Executive Summary"
- `## Executive Summary` → Topic: "Executive Summary"
- `## Section 1: Executive Summary` → Topic: "Executive Summary"

Extract the topic by removing:
- Leading `##`
- Optional number prefix (e.g., `1.`, `1:`, `Section 1:`)
- Trim whitespace

## Step 3: Generate Target Files (Parallel Sub-Agents)

**IMPORTANT:** Launch 4 sub-agents in parallel using the Task tool. Each agent writes one file independently. This is critical for handling large PRDs efficiently.

Create/overwrite the 4 PRD files with proper structure:

### 3.1 PRD.md (Summary + Meta)

```markdown
# Product Requirements Document (PRD)

## [Product Name from source]

**Version:** [from source or 1.0]
**Last Updated:** [current date]
**Status:** Imported
**Import Source:** [source file path]

---

## Document Structure

This PRD is organized into 4 files for manageability:

| File | Contents | Sections |
|------|----------|----------|
| **PRD.md** (this file) | Summary, goals, scope, meta | 1-2, 11-14 |
| [product-vision.md](./product-vision.md) | Personas, stories, journeys | 3-5 |
| [requirements.md](./requirements.md) | Functional & non-functional | 6-7 |
| [technical-spec.md](./technical-spec.md) | Architecture, data, APIs | 8-10 |

---

[Section 1 content]

---

[Section 2 content]

---

[Section 11 content]

---

[Section 12 content]

---

[Section 13 content]

---

[Section 14 content]
```

### 3.2 product-vision.md (The "What")

```markdown
# Product Vision

**Parent Document:** [PRD.md](./PRD.md)
**Last Updated:** [current date]

This document defines WHO we're building for, WHAT we're building, and HOW users will interact with it.

---

[Section 3 content]

---

[Section 4 content]

---

[Section 5 content]
```

### 3.3 requirements.md (The "Criteria")

```markdown
# Requirements Specification

**Parent Document:** [PRD.md](./PRD.md)
**Last Updated:** [current date]

This document defines the functional and non-functional requirements that the product must satisfy.

---

[Section 6 content]

---

[Section 7 content]
```

### 3.4 technical-spec.md (The "How")

```markdown
# Technical Specification

**Parent Document:** [PRD.md](./PRD.md)
**Last Updated:** [current date]

This document defines the technical architecture, data model, and API specifications for implementing the product.

---

[Section 8 content]

---

[Section 9 content]

---

[Section 10 content]

[Any supplementary sections that didn't match standard topics]
```

### Sub-Agent Task Prompts

Use these prompts when launching parallel Task agents:

**Agent 1 - PRD.md:**
```
Import PRD sections to docs/prd/PRD.md

Source file: [source_path]
Extract sections matching: Executive Summary, Goals/Metrics, MVP/Scope, Risks, Timeline, Open Questions
Target sections: 1, 2, 11, 12, 13, 14

Read the source file and extract the specified sections. Write docs/prd/PRD.md with:
- Document header with product name, version, status "Imported"
- Document structure table linking to other 3 files
- Sections 1, 2, 11-14 content from source

Use the PRD.md template format from the import prompt.
```

**Agent 2 - product-vision.md:**
```
Import PRD sections to docs/prd/product-vision.md

Source file: [source_path]
Extract sections matching: User Personas, Epics/Stories/Features, User Journeys
Target sections: 3, 4, 5

Read the source file and extract the specified sections. Write docs/prd/product-vision.md with:
- Header linking to parent PRD.md
- Sections 3, 4, 5 content from source

Use the product-vision.md template format from the import prompt.
```

**Agent 3 - requirements.md:**
```
Import PRD sections to docs/prd/requirements.md

Source file: [source_path]
Extract sections matching: Functional Requirements, Non-Functional Requirements
Target sections: 6, 7

Read the source file and extract the specified sections. Write docs/prd/requirements.md with:
- Header linking to parent PRD.md
- Sections 6, 7 content from source

Use the requirements.md template format from the import prompt.
```

**Agent 4 - technical-spec.md:**
```
Import PRD sections to docs/prd/technical-spec.md

Source file: [source_path]
Extract sections matching: Technical Architecture, Data Model, API Specifications
Target sections: 8, 9, 10
Also include: Any sections not matching standard topics (supplementary)

Read the source file and extract the specified sections. Write docs/prd/technical-spec.md with:
- Header linking to parent PRD.md
- Sections 8, 9, 10 content from source
- Any supplementary sections appended after Section 10

Use the technical-spec.md template format from the import prompt.
Return list of supplementary section names found.
```

## Step 4: Handle Supplementary Sections

Sections that don't match standard topic patterns should be:
1. Appended to `technical-spec.md` after Section 10
2. Preserved with their original headers
3. Listed in the import report as "supplementary"

Common supplementary sections include:
- Registered Workflows
- Signals & Queries
- Integration Details
- Deployment Configuration
- Glossary (if not in PRD.md appendix)

## Step 5: Update Workflow State

Create/update `docs/prd/.prd-workflow-state.json`:

```json
{
  "mode": "import",
  "import_source": "[path to source file]",
  "import_timestamp": "[ISO-8601]",
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
  "started_at": "[ISO-8601]",
  "last_updated": "[ISO-8601]",
  "import_report": {
    "source_file": "[path]",
    "sections_found": 14,
    "sections_mapped": {
      "PRD.md": [1, 2, 11, 12, 13, 14],
      "product-vision.md": [3, 4, 5],
      "requirements.md": [6, 7],
      "technical-spec.md": [8, 9, 10]
    },
    "supplementary_sections": ["Section Name 1", "Section Name 2"],
    "unmapped_sections": []
  }
}
```

## Step 6: Backup Source File

After successful import (unless `--dry-run`):
1. **Copy** (not move) the source file to `{original-name}.bak` as a backup
2. If `.bak` already exists, use `{original-name}.bak.1`, `.bak.2`, etc.
3. **Delete** the original source file after successful copy

This ensures:
- A full backup exists before any destructive operation
- The original complete PRD is preserved as `.bak` for reference
- The source file is removed to avoid confusion with the 4 split files

Example:
```bash
# Copy first (backup)
cp docs/prd/PRD-COMPLETE.md docs/prd/PRD-COMPLETE.md.bak

# Then delete original
rm docs/prd/PRD-COMPLETE.md
```

## Step 7: Generate Import Report

Display a summary:

```
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

</action>
<dry_run_behavior>

If `--dry-run` flag is present:

1. Perform all parsing and analysis steps
2. Display what WOULD be created/modified
3. Do NOT write any files
4. Do NOT rename the source file
5. Show the import report with "[DRY RUN]" prefix

Example dry-run output:

```
[DRY RUN] Import Preview
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
  ... (etc)

Run without --dry-run to execute import.
```

</dry_run_behavior>
<force_behavior>

If `--force` flag is present:
1. Overwrite existing target files without prompting
2. Skip confirmation for file operations

If `--force` is NOT present and target files exist:
1. List existing files that would be overwritten
2. Warn user and suggest using `--force` to proceed

</force_behavior>
<error_handling>

**Source file not found:**
```
Error: Source file not found.

Checked locations:
  - docs/prd/PRD-COMPLETE.md (not found)
  - docs/prd/PRD.md (not found)

Available .md files in docs/prd/:
  - product-vision.md
  - requirements.md
  - technical-spec.md

Usage: /prd-spec import [path] [--dry-run] [--force]
```

**No recognizable sections:**
```
Error: Could not identify PRD sections in the source file.

The import expects markdown headers (## Section Name) with recognizable topic keywords.

Recognized topics:
  - Executive Summary, Goals, Personas, Features, Journeys
  - Functional Requirements, Non-Functional Requirements
  - Architecture, Data Model, API Specifications
  - MVP Scope, Risks, Timeline, Open Questions

Please check that your PRD follows a standard section structure.
```

**Files exist without --force:**
```
Warning: Target files already exist:
  - docs/prd/PRD.md
  - docs/prd/product-vision.md
  - docs/prd/requirements.md
  - docs/prd/technical-spec.md

Use --force to overwrite existing files:
  /prd-spec import --force

Or use --dry-run to preview the import first:
  /prd-spec import --dry-run
```

</error_handling>
<definition_of_done>
- Source file is identified and read successfully
- All sections are parsed and classified by topic
- 4 target files are created with correct section distribution:
  - PRD.md: Sections 1, 2, 11-14
  - product-vision.md: Sections 3-5
  - requirements.md: Sections 6-7
  - technical-spec.md: Sections 8-10 + supplementary
- Workflow state is updated with "import" mode and completed steps
- Source file is renamed to .bak (unless --dry-run)
- Import report is displayed showing mapping results
- User can run `/prd-spec status` to see workflow progress
- User can run `/prd-spec export` to verify round-trip accuracy
</definition_of_done>
</prompt>
