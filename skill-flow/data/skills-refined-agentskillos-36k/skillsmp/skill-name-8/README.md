---
template: readme
status: active
date: 2025-12-06
component: templates
generated: 2025-12-23
last_updated: '2025-12-28T22:01:22'
---
# Template Files

Templates for scaffolding commands. Used by `ScaffoldTemplate.ps1` to create new files without LLM generation.

@.claude/hooks/ScaffoldTemplate.ps1
@.claude/commands/README.md

## Available Templates

| Template | Output | Variables | Status |
|----------|--------|-----------|--------|
| `checkpoint` | Session checkpoint | SESSION, TITLE, DATE | Active |
| `implementation_plan` | Implementation plan | TITLE, ID, DATE | Active |
| `architecture_decision_record` | ADR | NUMBER, TITLE, DATE | Active |
| `investigation` | Investigation (DISCOVERY phase) | BACKLOG_ID, TITLE, DATE | **NEW (ADR-034)** |
| `work_item` | Work item file (M6-WorkCycle) | BACKLOG_ID, TITLE, TIMESTAMP | **NEW (E2-150)** |
| `skill` | Skill implementation | SKILL_NAME, DESCRIPTION, DATE | **NEW (E2-285)** |
| `report` | Report document | TITLE, DATE | Active |
| `readme` | README template | COMPONENT | Active |
| `backlog_item` | Backlog entry | ID, TITLE | Active |
| `directive` | Operational directive | TITLE | Active |
| `guide` | Reference guide | TITLE | Active |
| `proposal` | Proposal document | TITLE | Active |
| `verification` | Verification doc | TITLE | Active |
| `meta_template` | Template for templates | - | Active |
| `handoff` | Generic handoff | TITLE, TYPE, DATE | **DEPRECATED** |
| `handoff_investigation` | Investigation handoff | TITLE, DATE | **DEPRECATED** |

### Deprecated Templates (ADR-034)

The following templates are deprecated but kept for backward compatibility:

- **`handoff`** - Replaced by: checkpoint + backlog + memory + `/coldstart`
- **`handoff_investigation`** - Replaced by: `investigation` template

Use `/new-investigation` instead of `/new-handoff investigation`.

## Variable Syntax

Variables use `{{VARIABLE}}` placeholder syntax.

Example: `{{SESSION}}` replaced with "36"

## Usage

```powershell
powershell.exe -ExecutionPolicy Bypass -File .claude/hooks/ScaffoldTemplate.ps1 `
  -Template "checkpoint" `
  -Output "docs/checkpoints/2025-12-06-SESSION-36-example.md" `
  -Variables @{SESSION="36"; TITLE="Example Title"}
```

## RFC 2119 Governance Sections (E2-086)

**Session 141 (2025-12-28):** Five templates now include RFC 2119 governance sections that guide agents with explicit MUST/SHOULD/MAY requirements.

| Template | Section Name | Key Requirements |
|----------|--------------|------------------|
| `checkpoint` | Session Hygiene | MUST: Store WHY, update memory_refs |
| `implementation_plan` | Pre-Implementation Checklist | MUST: Tests before code, design decisions |
| `investigation` | Discovery Protocol | MUST: Use investigation-agent, capture findings |
| `report` | Verification Requirements | MUST: Include evidence, list artifacts |
| `architecture_decision_record` | Decision Criteria | MUST: Document alternatives, explain WHY |

**Purpose:** RFC 2119 signals (MUST/SHOULD/MAY) are semantic governance that Claude understands. These sections guide agents toward proper behavior without requiring mechanical enforcement.

**Reference:** ADR-035 (RFC 2119 Governance Signaling), E2-037 (implementation)

---

## Design Rationale

**Session 36 (2025-12-06):** Templates were created to replace LLM-based file generation. Benefits:
- No LLM cost per file creation
- Consistent output every time
- Faster execution
- Aligns with "Doing right should be easy" principle

---
