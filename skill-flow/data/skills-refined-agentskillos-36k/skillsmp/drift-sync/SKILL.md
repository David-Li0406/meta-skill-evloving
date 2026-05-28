---
name: drift-sync
description: 'Drift-sync governance workflow for keeping SSOT instructions aligned with codebase reality. Use when conventions change, repeated review comments indicate hidden rules, or codebase behavior diverges from documented instructions. Triggers: drift, sync, convention change, SSOT update, rule change, instruction update.'
---

# Drift-Sync Workflow

Operational workflow for detecting and resolving drift between codebase reality and SSOT instruction files.

## When to Use This Skill

- PO decides a convention change (e.g., translation key casing, naming, folder placement)
- A repeated review comment indicates a "hidden rule" not in SSOT
- The team starts doing something different than instructions say
- Emergency patch needed that diverges from documented conventions

## Prerequisites

- Access to SSOT instruction files (`.github/instructions/`)
- Access to KYORA_AGENT_OS.md for changelog updates
- PO availability for approval (if convention change)

## What is Drift?

Drift is any mismatch between:

- How the codebase actually behaves / is implemented today
- What SSOT instructions or KYORA_AGENT_OS.md say should happen

### Common Drift Examples

- Translation key casing convention changes
- New form/error-handling pattern becomes de-facto standard
- New folder placement rules emerge
- UI tokens/components change and older guidance becomes wrong
- Backend error handling evolves past documented pattern

## Drift-Sync Protocol (6 Steps)

### Step 1: Identify SSOT Owner File

Determine which `.instructions.md` file governs the rule.

| Domain | SSOT File |
|--------|-----------|
| Backend architecture | `backend-core.instructions.md` |
| Backend patterns | `go-backend-patterns.instructions.md` |
| Error handling | `errors-handling.instructions.md` |
| DTOs/Swagger | `responses-dtos-swagger.instructions.md` |
| Portal architecture | `frontend/projects/portal-web/architecture.instructions.md` |
| Portal structure | `frontend/projects/portal-web/code-structure.instructions.md` |
| UI/RTL | `frontend/_general/ui-patterns.instructions.md` |
| Forms | `frontend/_general/forms.instructions.md` |
| i18n | `frontend/_general/i18n.instructions.md` |
| HTTP/Query | `frontend/_general/http-client.instructions.md` |

If unclear, check [KYORA_AGENT_OS.md Section 2.1](../../../KYORA_AGENT_OS.md) for SSOT entry points.

### Step 2: Prepare Drift Ticket

Create a Drift Ticket (use `/create-drift-ticket` prompt) documenting:

- What changed
- Why it changed
- Blast radius
- Proposed new rule

See [Drift Ticket format](./references/rule-change-ledger.md#drift-ticket-template).

### Step 3: Get PO Approval

**PO gate is required** if the change affects conventions.

Present:
- Current reality vs current documentation
- Proposed new rule
- Impact assessment

### Step 4: Update SSOT File(s) Only

- Update only the owning SSOT file
- Do NOT scatter the same rule elsewhere
- Do NOT duplicate rules across files

### Step 5: Update OS Changelog

Add 1–3 bullets to KYORA_AGENT_OS.md under Versioning/Changelog:

```markdown
## Versioning

- **Version**: YYYY-MM-DD
- **Changelog**:
  - [Your change summary here]
```

### Step 6: Run Validation Loop

Run the smallest relevant validation:

```bash
# Backend changes
make test.quick
make openapi.check

# Portal changes
make portal.check

# Full validation
make test
make portal.build
```

## Emergency Patch Path

**Allowed when**: A mismatch is actively breaking work today.

Steps:

1. Apply minimal fix in code (emergency only)
2. Immediately open Drift Ticket
3. Schedule SSOT sync in next cycle

**Do not**: Quietly diverge without opening a ticket.

## Rule Change Ledger

When a rule/convention changes, append to the ledger table in KYORA_AGENT_OS.md:

```markdown
| Date | Rule changed | SSOT owner file | PO approved | Validation |
|------|--------------|-----------------|-------------|------------|
| YYYY-MM-DD | [rule] | [file] | Yes/No | [commands] |
```

See [Rule Change Ledger Reference](./references/rule-change-ledger.md).

## Success Checklist

- [ ] Drift identified and documented
- [ ] SSOT owner file identified
- [ ] Drift Ticket created
- [ ] PO approval obtained (if convention change)
- [ ] SSOT file updated (single source, no duplicates)
- [ ] OS changelog updated
- [ ] Validation loop run successfully
- [ ] No surprise docs created
- [ ] Stop-and-ask triggers checked

## Stop-and-Ask Triggers

**MUST ask PO before proceeding** if:

- Rule change affects multiple teams/areas
- Change could break existing code patterns
- Emergency patch bypasses normal approval
- Blast radius is large (>10 files affected)

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Can't find SSOT owner file | Rule doesn't exist yet | Check if new instruction file needed |
| PO gate unclear | Convention vs documentation-only | If behavior changes, it's a convention = PO gate |
| Drift recurring | Rule not enforced | Add to validation commands or lint rules |
| Multiple files claim ownership | SSOT violation | Consolidate to single file, remove duplicates |

## Validation Commands

```bash
# Check affected area
make test.quick        # Backend unit tests
make portal.check      # Portal lint/typecheck

# Full validation (if broad change)
make test              # All backend tests
make portal.build      # Portal build
```

## References

- [Rule Change Ledger](./references/rule-change-ledger.md)
- [Artifact Prune Checklist](./references/artifact-prune.md)

## SSOT References

- Drift-sync governance: [KYORA_AGENT_OS.md#L1030-L1065](../../../KYORA_AGENT_OS.md#L1030-L1065)
- Drift Ticket template: [KYORA_AGENT_OS.md#L1173-L1196](../../../KYORA_AGENT_OS.md#L1173-L1196)
- Rule change ledger: [KYORA_AGENT_OS.md#L1067-L1071](../../../KYORA_AGENT_OS.md#L1067-L1071)
