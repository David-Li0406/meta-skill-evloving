---
name: ticket-workflow
description: Global skill for ticket resolution workflow with state machine and resume capability. Coordinates fetch-ticket, analyze-ticket skills and integrates with AEP/Architect for planning.
---

# Ticket Workflow Skill

This skill provides the state machine and coordination logic for the complete ticket resolution workflow.

## State Machine

```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐
│ pending │───►│ fetched │───►│ analyzed │───►│ planned │
└─────────┘    └─────────┘    └──────────┘    └─────────┘
                    │              │               │
                    ▼              ▼               ▼
               ┌─────────────────────────────────────────┐
               │                failed                    │
               └─────────────────────────────────────────┘
                                   │
                                   │ (resume)
                                   ▼
┌─────────────────┐    ┌───────────────┐    ┌───────────┐
│ plan_validated  │───►│ implementing  │───►│ completed │
└─────────────────┘    └───────────────┘    └───────────┘
```

## States

| State | Description | Next States |
|-------|-------------|-------------|
| `pending` | Workflow just started | `fetched`, `failed` |
| `fetched` | Ticket data retrieved | `analyzed`, `failed` |
| `analyzed` | Complexity determined | `planned`, `failed` |
| `planned` | Implementation plan ready | `plan_validated`, `failed` |
| `plan_validated` | Plan approved by user | `implementing`, `failed` |
| `implementing` | Auto-implementation in progress | `completed`, `failed` |
| `completed` | All phases finished | (terminal) |
| `failed` | Error occurred | (can resume) |

## Phase Mapping

| State Transition | Phase | Skill Used |
|------------------|-------|------------|
| pending → fetched | fetch | fetch-ticket |
| fetched → analyzed | analyze | analyze-ticket |
| analyzed → analyzed | explore | (AEP agents) |
| analyzed → planned | plan | (Architect) |
| planned → plan_validated | validation | plan-validation |
| plan_validated → implementing | implement | solo-implement.sh |

## Status File Management

### Location
```
.claude/feature/{ticket-id}/status.json
```

### Initialize Status
```json
{
  "ticket_id": "PROJ-123",
  "source": "youtrack",
  "started_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "state": "pending",
  "phases": {
    "fetch": "pending",
    "analyze": "pending",
    "explore": "pending",
    "plan": "pending",
    "implement": "pending"
  },
  "options": {}
}
```

### Update Status
After each phase completion:
```json
{
  "state": "fetched",
  "updated_at": "2024-01-15T10:31:00Z",
  "phases": {
    "fetch": "completed",
    "analyze": "pending",
    ...
  }
}
```

### Mark Failed
On error:
```json
{
  "state": "failed",
  "updated_at": "2024-01-15T10:32:00Z",
  "phases": {
    "fetch": "completed",
    "analyze": "failed",
    ...
  },
  "error": {
    "phase": "analyze",
    "message": "Could not determine complexity",
    "timestamp": "2024-01-15T10:32:00Z"
  }
}
```

## Resume Logic

### Check for Existing Status
```bash
if [ -f ".claude/feature/{ticket-id}/status.json" ]; then
    # Load and check state
fi
```

### Resume from State
```python
def get_resume_point(status):
    # Find last completed phase
    phase_order = ['fetch', 'analyze', 'explore', 'plan', 'implement']

    for phase in phase_order:
        if status['phases'][phase] in ['pending', 'failed']:
            return phase

    return None  # All completed
```

### Display Resume Info
```markdown
# Reprise du Workflow

**Ticket**: {ticket-id}
**Etat precedent**: {state}
**Derniere mise a jour**: {updated_at}

## Phases

| Phase | Statut |
|-------|--------|
| Fetch | completed |
| Analyze | completed |
| Explore | skipped |
| Plan | pending |
| Implement | pending |

## Point de Reprise

Reprise depuis: **plan**
Erreur precedente: {error.message}

Continuer ? [O/n]
```

## Workflow Orchestration

### Phase: Fetch
1. Check if status exists and fetch completed → skip
2. Invoke fetch-ticket skill
3. Save ticket.md
4. Update status: `state = "fetched"`, `phases.fetch = "completed"`

### Phase: Analyze
1. Check if status exists and analyze completed → skip
2. Invoke analyze-ticket skill
3. Determine complexity
4. Save analysis.md
5. Update status: `state = "analyzed"`, `phases.analyze = "completed"`, `complexity = ...`

### Phase: Explore
1. Check complexity level
2. If SIMPLE: skip, mark `phases.explore = "skipped"`
3. If MEDIUM: launch 1 explore agent
4. If COMPLEX: launch 3 explore agents in parallel
5. Append findings to analysis.md
6. Update status: `phases.explore = "completed"`

### Phase: Plan
1. If COMPLEX and not --skip-architect: invoke Architect skill
2. Generate implementation plan
3. Save plan.md
4. Update status: `state = "planned"`, `phases.plan = "completed"`

### Phase: Plan Validation
**AUTO mode**: Auto-validate, continue to implement
**INTERACTIVE mode**: Validation loop (Valider et implémenter / Valider et arrêter / Modifier / Régénérer)
- Update status: `state = "plan_validated"`, `plan_validated_at = "{timestamp}"`

### Phase: Implement
**AUTO mode**: Always executed after plan validation
**INTERACTIVE mode**: Via "Valider et implémenter" choice or `--continue` flag
1. Execute `/compact` to clear context
2. Call solo-implement.sh --feature {ticket-id}
3. Update status: `state = "implementing"` → `phases.implement = "completed"`

## Configuration Integration

Read from project's `.claude/ticket-config.json`:
- Merge with default config from references/default-config.json
- Override with command-line options

Priority order:
1. Command-line options
2. Project config
3. Default config

## Error Recovery

### Transient Errors
- Network timeout → retry with backoff
- MCP unavailable → fallback or prompt user

### Persistent Errors
- Ticket not found → mark failed, clear instructions
- Permission denied → mark failed, suggest resolution

### Recovery Actions
```markdown
## Erreur Recuperable

L'erreur "{error.message}" peut etre resolue.

**Actions suggerees**:
1. {action 1}
2. {action 2}

**Pour reprendre**:
```bash
/resolve {ticket-id}  # Reprend automatiquement
```
```

## Files Generated

```
.claude/feature/{ticket-id}/
├── status.json     # Workflow state
├── ticket.md       # Original ticket content
├── analysis.md     # Complexity analysis + exploration findings
└── plan.md         # Implementation plan (for solo-implement.sh)
```

## Integration Points

### With AEP Skill
- Used for COMPLEX tickets during explore phase
- Applies ANALYSE-EXPLORE-PLAN methodology

### With Architect Skill
- Used for COMPLEX tickets during plan phase
- Ensures plan follows best practices

### With solo-implement.sh
- Plans saved in compatible format
- --feature option for direct access

## Language

- Status file: English (machine-readable)
- User messages: French
- Technical output: English
