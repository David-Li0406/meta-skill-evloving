# Rule Change Ledger Reference

How to maintain the rule change ledger and create drift tickets in Kyora Agent OS.

## Rule Change Ledger

The ledger lives inside [KYORA_AGENT_OS.md](../../../KYORA_AGENT_OS.md) under Section 9 (Governance and Maintenance).

### Ledger Table Format

```markdown
| Date | Rule changed | SSOT owner file | PO approved | Validation |
|------|--------------|-----------------|-------------|------------|
| YYYY-MM-DD | Brief description of rule change | filename.instructions.md | Yes | make test.quick |
```

### When to Add an Entry

Add a row when:

- A convention or coding standard changes
- An SSOT instruction file is updated with new rules
- Emergency patches diverge from documented behavior

### Entry Guidelines

1. **Date**: Use ISO format (YYYY-MM-DD)
2. **Rule changed**: Brief, scannable description (1 line)
3. **SSOT owner file**: The `.instructions.md` file that was updated
4. **PO approved**: "Yes" if PO gate was obtained, "No" if emergency patch
5. **Validation**: Command(s) run to verify change didn't break anything

### Example Entries

```markdown
| Date | Rule changed | SSOT owner file | PO approved | Validation |
|------|--------------|-----------------|-------------|------------|
| 2026-01-15 | Translation keys now use dot.case | frontend/_general/i18n.instructions.md | Yes | make portal.check |
| 2026-01-10 | Form validation uses onBlur by default | frontend/_general/forms.instructions.md | Yes | make portal.check |
| 2026-01-05 | API errors include request_id | errors-handling.instructions.md | Yes | make test.quick |
```

## Drift Ticket Template

Use this template (also available via `/create-drift-ticket` prompt):

```
DRIFT TICKET

What drifted:
-

Current reality (what code does today):
-

Current SSOT guidance (what instructions say):
-

Proposed new rule:
-

Why (benefit + risk):
-

Blast radius (what areas/files/users affected):
-

PO gate required?: yes | no

Validation plan:
-
```

### Drift Ticket Fields

| Field | Description |
|-------|-------------|
| What drifted | The specific rule or convention that has diverged |
| Current reality | How the codebase actually behaves today |
| Current SSOT guidance | What the instruction files say should happen |
| Proposed new rule | The new rule that should replace the old one |
| Why | Rationale for the change (benefits and risks) |
| Blast radius | Files, areas, or users affected by the change |
| PO gate required? | "yes" if convention change, "no" if documentation-only |
| Validation plan | Commands to run after SSOT update |

### Example Drift Ticket

```
DRIFT TICKET

What drifted:
- Translation key casing convention

Current reality (what code does today):
- New code uses dot.case: "orders.status.pending"
- Old code uses snake_case: "orders_status_pending"

Current SSOT guidance (what instructions say):
- frontend/_general/i18n.instructions.md says use snake_case

Proposed new rule:
- Use dot.case for all new keys
- Migrate existing keys progressively (not big-bang)

Why (benefit + risk):
- Benefit: dot.case is more readable and matches i18next convention
- Risk: Mixed casing during migration period

Blast radius (what areas/files/users affected):
- All portal-web i18n keys
- Translation files in portal-web/src/i18n/

PO gate required?: yes

Validation plan:
- make portal.check
- Verify no broken translation keys in UI
```

## SSOT File Lookup Table

Quick reference for which SSOT owns which rules:

| Domain | SSOT Owner File |
|--------|-----------------|
| Repo baseline | `.github/copilot-instructions.md` |
| Artifact selection | `ai-artifacts.instructions.md` |
| Backend architecture | `backend-core.instructions.md` |
| Backend patterns | `go-backend-patterns.instructions.md` |
| Backend testing | `backend-testing.instructions.md` |
| Error handling | `errors-handling.instructions.md` |
| DTOs/Swagger | `responses-dtos-swagger.instructions.md` |
| Portal architecture | `frontend/projects/portal-web/architecture.instructions.md` |
| Portal structure | `frontend/projects/portal-web/code-structure.instructions.md` |
| UI/RTL | `frontend/_general/ui-patterns.instructions.md` |
| Design tokens | `kyora/design-system.instructions.md` |
| Forms | `frontend/_general/forms.instructions.md` |
| i18n | `frontend/_general/i18n.instructions.md` |
| HTTP/Query | `frontend/_general/http-client.instructions.md` |
| Charts | `frontend/projects/portal-web/charts.instructions.md` |

## Workflow Integration

1. **Detect drift**: Review comment, team behavior, or explicit PO decision
2. **Create Drift Ticket**: Use template above or `/create-drift-ticket`
3. **Get PO approval**: If convention change
4. **Update SSOT**: Single file only
5. **Add ledger row**: In KYORA_AGENT_OS.md
6. **Add changelog bullet**: In KYORA_AGENT_OS.md Versioning section
7. **Run validation**: Appropriate make targets
