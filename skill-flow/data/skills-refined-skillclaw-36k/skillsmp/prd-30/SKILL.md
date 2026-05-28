---
name: prd
description: Create, sync, and manage PRDs in Google Docs. Draft new PRDs from PM interviews, sync existing PRDs, and push discoveries back.
allowed-tools: Read, Write, Glob, Task, mcp__google-docs-mcp__readGoogleDoc, mcp__google-docs-mcp__getDocumentInfo, mcp__google-docs-mcp__appendToGoogleDoc, mcp__google-docs-mcp__insertText, mcp__google-docs-mcp__deleteRange, mcp__google-docs-mcp__createDocument
user-invocable: true
---

# /prd Skill

## Purpose

Full lifecycle management for Product Requirements Documents (PRDs):
- **Create** new PRDs from PM interviews using the standard template
- **Write** PRDs to Google Docs
- **Sync** existing PRDs from Google Docs to local spec groups
- **Push** implementation discoveries back to PRDs

## Usage

```
/prd draft                     # Start PM interview, then draft PRD to Google Doc
/prd draft <spec-group-id>     # Draft PRD from existing spec group requirements
/prd write <doc-id>            # Write/overwrite PRD to specified Google Doc
/prd write <doc-id> <spec-group-id>  # Write specific spec group's PRD to doc

/prd sync <doc-id-or-url>      # Pull PRD, extract requirements, create spec group
/prd status                    # Show all linked PRDs and their sync state
/prd status <spec-group-id>    # Show PRD status for specific spec group
/prd diff <spec-group-id>      # Show differences between local and remote PRD
/prd push <spec-group-id>      # Push local discoveries back to PRD (creates new version)
/prd link <spec-group-id> <doc-id>  # Link existing spec group to a PRD
```

## Commands

### /prd draft

Creates a new PRD by running a PM interview, then writes to Google Docs using the standard template.

**Process**:
1. If no spec-group-id provided:
   - Invoke `/pm` skill to run discovery interview
   - PM skill creates spec group with `requirements.md`
2. Prompt user for Google Doc destination:
   - Create new document
   - Write to existing document (provide doc ID)
3. Dispatch `prd-author` agent to:
   - Read `requirements.md` from spec group
   - Read PRD template from `.claude/templates/prd.template.md`
   - Transform requirements into PRD format
   - Write formatted PRD to Google Doc
4. Update `manifest.json` with PRD link

**Output**:
```
PRD drafted successfully

Title: "AI-Native Engineering Dashboard"
Spec Group: sg-ai-dashboard
Document: https://docs.google.com/document/d/1abc.../edit

Sections created:
  ✓ Overview
  ✓ Goals (3)
  ✓ Non-Goals (3)
  ✓ Requirements (10 in EARS format)
  ✓ Constraints
  ✓ Assumptions
  ✓ Success Criteria
  ✓ Open Questions (4)
  ✓ Version History

Status: v1 (DRAFT)

Next steps:
  1. Review PRD in Google Docs
  2. Mark as REVIEWED when satisfied
  3. Run /spec sg-ai-dashboard to create specs
```

### /prd write

Writes a PRD to a Google Doc using the standard template format. Can create new doc or overwrite existing.

**Input**:
- `doc-id`: Google Doc ID or "new" to create new document
- `spec-group-id` (optional): If not provided, uses most recent spec group

**Process**:
1. Resolve spec group (use provided ID or most recent)
2. If doc-id is "new":
   - Will create new Google Doc with title from spec group
3. Dispatch `prd-author` agent to:
   - Load spec group's `requirements.md`
   - Load PRD template
   - Transform requirements to PRD sections (see mapping below)
   - Clear existing content if overwriting
   - Write formatted PRD content to Google Doc
4. Update manifest with PRD link

**Template Mapping**:
```
requirements.md Section    →    PRD Template Section
─────────────────────────────────────────────────────
Source + Problem Statement →    Overview
Goals                      →    Goals
Non-Goals                  →    Non-Goals
Requirements (REQ-XXX)     →    Requirements (EARS format preserved)
Constraints                →    Constraints
Assumptions                →    Assumptions
Success Criteria           →    Success Criteria
Open Questions             →    Open Questions
Edge Cases                 →    Folded into Requirements or separate section
Priorities                 →    Requirements Priority field
                          →    User Stories (generated from requirements)
                          →    Version History (initialized)
                          →    EARS Format Reference (appended)
```

**Output**:
```
PRD written to Google Doc

Document: "AI-Native Engineering Dashboard"
URL: https://docs.google.com/document/d/1abc.../edit
Action: Created new document (or: Overwrote existing content)

Content:
  - Overview: 2 paragraphs
  - Goals: 4 items
  - Non-Goals: 3 items
  - Requirements: 10 (all EARS format)
  - Constraints: 3 categories
  - Assumptions: 4 with impact analysis
  - Success Criteria: 6 measurable outcomes
  - Open Questions: 4 (2 high priority)
  - User Stories: 7 generated
  - Version History: v1 initialized

Spec group sg-ai-dashboard linked to document.
```

### /prd sync

Creates a new spec group from an external PRD.

**Input**: Google Doc ID or full URL
- Doc ID: `1pQA7lIvofbKL7NzS4PkIRKlfBNnVsTtCMgSfJB7A17Y`
- URL: `https://docs.google.com/document/d/1pQA7.../edit`

**Process**:
1. Fetch document metadata (title, last modified)
2. Read document content
3. Dispatch `prd-reader` agent to extract:
   - Requirements (convert to EARS format)
   - Constraints
   - Assumptions
   - Success criteria
4. Create spec group directory
5. Generate `manifest.json` with PRD link
6. Generate `requirements.md` from extracted requirements
7. Set `review_state: DRAFT` (agent created, needs user review)

**Output**:
```
PRD synced successfully

Document: "Logout Feature Requirements"
Version: v1 (detected from document)
Last Modified: 2026-01-14

Created spec group: sg-logout-feature
  - 4 requirements extracted
  - requirements.md generated

Next steps:
  1. Review requirements: .claude/specs/groups/sg-logout-feature/requirements.md
  2. Run /spec to create high-level spec
  3. Run /atomize to decompose into atomic specs
```

### /prd status

Shows sync status for linked PRDs.

**Output**:
```
PRD Status

sg-logout-feature
  PRD: "Logout Feature Requirements"
  Source: google-docs (1pQA7...)
  Local Version: v1
  Remote Version: v1
  Status: IN_SYNC ✓
  Last Synced: 2026-01-14T10:00:00Z

sg-auth-revamp
  PRD: "Authentication Revamp"
  Source: google-docs (2xYz...)
  Local Version: v2
  Remote Version: v3  ← DRIFT DETECTED
  Status: OUT_OF_SYNC ✗
  Last Synced: 2026-01-10T14:00:00Z
  Action: Run /prd diff sg-auth-revamp to see changes
```

### /prd diff

Shows differences between local requirements and remote PRD.

**Output**:
```
PRD Diff: sg-auth-revamp

Remote PRD has been updated (v2 → v3)

Changes detected:
  + NEW: REQ-005 "Multi-factor authentication support"
  ~ MODIFIED: REQ-002 "Session timeout changed from 30min to 15min"
  - REMOVED: REQ-004 "Remember me functionality" (moved to separate PRD)

Local changes not in PRD:
  + REQ-006 "Rate limiting for login attempts" (discovered during implementation)

Options:
  1. /prd sync sg-auth-revamp --merge   # Merge remote changes with local
  2. /prd sync sg-auth-revamp --replace # Replace local with remote
  3. /prd push sg-auth-revamp           # Push local discoveries to PRD
```

### /prd push

Pushes local discoveries back to the PRD document.

**When to use**:
- Implementation revealed new requirements
- Assumptions were invalidated
- Constraints were discovered

**Process**:
1. Read local `requirements.md`
2. Compare with last synced state
3. Identify new/changed requirements
4. Dispatch `prd-writer` agent to:
   - Append new requirements to PRD
   - Add "Implementation Notes" section
   - Increment version marker
5. Update `manifest.json` with new PRD version
6. Set remote PRD version state to DRAFT (agent change)

**Output**:
```
PRD updated successfully

Pushed to: "Authentication Revamp" (v3 → v4)
Changes:
  + Added REQ-006: Rate limiting for login attempts
  + Added Implementation Note: "Rate limit discovered necessary during load testing"

Remote PRD version: v4 (DRAFT - needs human review)
Local spec group: sg-auth-revamp (synced to v4)
```

## PRD Format Expectations

The `/prd` skill works best with PRDs that follow a structured format. The `prd-reader` agent can handle various formats but extracts most reliably from:

### Recommended PRD Structure

```
# [Product/Feature Name]

## Overview / Summary
Brief description of what this is and why it matters.

## Goals
- Goal 1
- Goal 2

## Non-Goals
- Explicitly out of scope item 1

## Requirements
### REQ-001: [Requirement Title]
[Description in natural language]

### REQ-002: [Requirement Title]
[Description]

## Constraints
- Technical constraint 1
- Business constraint 2

## Assumptions
- Assumption 1
- Assumption 2

## Success Criteria
- Measurable outcome 1
- Measurable outcome 2

## Open Questions
- [ ] Unresolved question 1
- [x] Resolved question → Answer

## Version History
- v1 (2026-01-10): Initial draft
- v2 (2026-01-14): Added REQ-003 based on user feedback
```

### Flexible Extraction

The `prd-reader` agent can also extract from less structured documents by:
- Looking for bullet points that describe behaviors
- Identifying "must", "shall", "should" language
- Finding sections labeled "requirements", "features", "user stories"
- Converting user stories to EARS format

## Integration with Workflow

### Flow 1: Create New PRD (PM → PRD → Specs)

```
User has idea/request
    ↓
/prd draft (or /pm first)
    ↓
PM interview gathers requirements
    ↓
Spec group created with requirements.md
    ↓
PRD written to Google Doc (using template)
    ↓
User reviews PRD in Google Docs
    ↓
/spec (creates spec.md from requirements)
    ↓
/atomize
    ↓
... implementation ...
    ↓
/prd push (if new requirements discovered)
    ↓
PRD updated, new version as DRAFT
```

### Flow 2: Sync Existing PRD (External PRD → Specs)

```
PRD already exists in Google Docs
    ↓
/prd sync <doc-id>
    ↓
prd-reader extracts requirements
    ↓
Spec group created with requirements.md
review_state: DRAFT
    ↓
User reviews extracted requirements
    ↓
/spec (creates spec.md from requirements)
    ↓
/atomize
    ↓
... implementation ...
    ↓
/prd push (if new requirements discovered)
    ↓
PRD updated, new version as DRAFT
```

### PM Skill Relationship

The `/pm` skill and `/prd` skill work together:

| Skill | Purpose | Output |
|-------|---------|--------|
| `/pm` | Gather requirements via interview | `requirements.md` in spec group |
| `/prd draft` | Interview + write PRD to Google Doc | PRD in Google Docs + spec group |
| `/prd write` | Write existing requirements to PRD | PRD in Google Docs |
| `/prd sync` | Extract requirements from existing PRD | `requirements.md` in spec group |

**When to use which:**
- **Starting fresh**: `/prd draft` — runs PM interview then writes PRD
- **Have requirements, need PRD**: `/prd write <doc-id>` — formats and writes
- **PRD exists, need local requirements**: `/prd sync <doc-id>` — extracts to local
- **Just gathering requirements (no PRD yet)**: `/pm` — interview only

## Agents

The `/prd` skill uses three specialized agents:

| Agent | Purpose | Used By |
|-------|---------|---------|
| `prd-author` | Authors complete PRDs from requirements using template | `/prd draft`, `/prd write` |
| `prd-reader` | Extracts requirements from existing PRDs | `/prd sync` |
| `prd-writer` | Pushes incremental discoveries back to PRDs | `/prd push` |

### Agent Responsibilities

**prd-author** (`.claude/agents/prd-author.md`):
- Transforms `requirements.md` → full PRD document
- Follows PRD template structure exactly
- Writes to Google Docs (create new or overwrite)
- Generates User Stories from requirements
- Initializes version history

**prd-reader** (`.claude/agents/prd-reader.md`):
- Reads external PRDs from Google Docs
- Extracts requirements, constraints, assumptions
- Converts prose/user stories to EARS format
- Creates `requirements.md` in spec group

**prd-writer** (`.claude/agents/prd-writer.md`):
- Computes diff between local and last-synced state
- Appends new requirements discovered during implementation
- Updates assumptions (marks invalidated)
- Adds implementation notes
- Increments PRD version

## Version Detection

The skill attempts to detect PRD versions by:
1. Looking for explicit "Version: vX" or "v1, v2" markers
2. Checking "Version History" section
3. Using document revision history from Google Docs API
4. Falling back to date-based versioning if none found

## State Transitions

### On /prd draft (new PRD + spec group)
```json
{
  "review_state": "DRAFT",
  "work_state": "PLAN_READY",
  "updated_by": "agent",
  "prd": {
    "source": "google-docs",
    "document_id": "...",
    "version": "v1",
    "last_sync": "<now>",
    "created_by": "prd-draft"
  }
}
```
- Google Doc created/written with PRD content
- PRD version: v1 (DRAFT)
- Spec group linked to document

### On /prd write (write to existing doc)
```json
{
  "prd": {
    "source": "google-docs",
    "document_id": "...",
    "version": "v1",
    "last_sync": "<now>",
    "created_by": "prd-write"
  }
}
```
- Existing spec group's `manifest.json` updated with PRD link
- Google Doc content replaced with formatted PRD

### On /prd sync (new spec group from existing PRD)
```json
{
  "review_state": "DRAFT",
  "work_state": "PLAN_READY",
  "updated_by": "agent",
  "prd": {
    "source": "google-docs",
    "document_id": "...",
    "version": "v1",
    "last_sync": "<now>"
  }
}
```

### On /prd push
- Remote PRD gets new version (DRAFT state in PRD)
- Local `manifest.json` updated with new version reference
- Local `review_state` unchanged (local work continues)

## Error Handling

### Document Not Found
```
Error: Could not access document 1pQA7...

Possible causes:
  - Document ID is incorrect
  - Document is not shared with the service account
  - Document has been deleted

Check document sharing settings and try again.
```

### No Requirements Found
```
Warning: No clear requirements found in PRD

The document exists but doesn't contain recognizable requirements.
Consider:
  1. Adding a "Requirements" section to the PRD
  2. Using /pm to interview and generate requirements locally
  3. Manually creating requirements.md

Spec group created with empty requirements.md
```

### Permission Denied for Push
```
Error: Cannot update PRD - insufficient permissions

The service account has read-only access to this document.
Options:
  1. Grant edit access to the service account
  2. Manually copy changes to the PRD
  3. Export requirements: /prd export sg-logout-feature
```

## Edge Cases

### PRD Has Multiple Versions in One Document
Some PRDs track versions inline. The reader will:
- Extract the latest/current version's requirements
- Note previous versions in the change log
- Flag if version is ambiguous

### PRD is Actually a User Story Collection
If the document is Agile user stories rather than requirements:
- Convert "As a X, I want Y, so that Z" to EARS format
- Group related stories into single requirements where appropriate
- Flag for user review

### Linked PRD Deleted
```
Warning: Linked PRD no longer accessible

Spec group: sg-logout-feature
Previous PRD: google-docs/1pQA7...

Options:
  1. /prd unlink sg-logout-feature  # Continue with local-only
  2. /prd link sg-logout-feature <new-doc-id>  # Link to replacement
```
