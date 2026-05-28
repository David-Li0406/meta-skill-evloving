---
name: routing-gate
description: Bridge skill for work-type routing in CHAIN phase. Use to determine next
  cycle skill based on work item signals.
recipes:
- queue
- is-cycle-allowed
generated: 2025-12-28
last_updated: '2026-01-15T23:05:12'
---
# Routing-Gate (Bridge Skill)

This is a **Bridge Skill** that provides pure work-type routing logic for cycle skill CHAIN phases. It extracts duplicated routing from implementation-cycle, investigation-cycle, and close-work-cycle into a single reusable component.

## When to Use

**Invoked from:** Cycle skill CHAIN phases (implementation-cycle, investigation-cycle, close-work-cycle).
**Manual invocation:** `Skill(skill="routing-gate")` when determining next work routing.

---

## Design Note

**Threshold checks are NOT in this skill.** Per S137 anti-pattern analysis and E2-224 implementation, threshold checks (observation triage trigger) live in the OBSERVE phase of close-work-cycle. This skill does pure work-type routing only.

---

## The Flow

```
Input (next_work_id, has_plan)
    |
    +-> Work-Type Routing
            next_work_id is None?
                ├─ YES → await_operator
                └─ NO  → starts with "INV-"?
                            ├─ YES → invoke_investigation
                            └─ NO  → has_plan?
                                        ├─ YES → invoke_implementation
                                        └─ NO  → invoke_work_creation
```

---

## Cycle-Locking Check (E2-291)

**Before applying the decision table, check cycle-locking:**

1. Determine active queue (from survey-cycle context or "default")
2. Run `just is-cycle-allowed [queue] [cycle]`
3. If BLOCKED:
   - Return `{action: "blocked", reason: "Queue [name] only allows [cycles]"}`
   - Display warning:
     ```
     WARNING: Cycle '[cycle]' is blocked for queue '[queue]'.
     Allowed cycles: [list from config]
     Queue rationale: "[from work_queues.yaml]"
     ```
4. If ALLOWED: continue to decision table

---

## Routing Decision Table

| Signal | Action | Skill to Invoke |
|--------|--------|-----------------|
| Cycle blocked by queue | `blocked` | None - display warning |
| `next_work_id` is None | `await_operator` | None - wait for operator |
| ID starts with `INV-` | `invoke_investigation` | `investigation-cycle` |
| `has_plan` is True | `invoke_implementation` | `implementation-cycle` |
| Otherwise | `invoke_work_creation` | `work-creation-cycle` |

---

## Usage

**From cycle skill CHAIN phase:**

1. Query next work: `just queue [name]` (or `just ready` for backward compat)
2. Read first work file, check `documents.plans` field
3. **Check cycle-locking:** `just is-cycle-allowed [queue] [cycle]`
   - If BLOCKED: display warning and stop
4. Apply the decision table above:
   - `next_work_id` is None → `await_operator`
   - ID starts with `INV-` → `invoke_investigation`
   - `has_plan` is True → `invoke_implementation`
   - Otherwise → `invoke_work_creation`
5. Execute the corresponding skill invocation:
   - `invoke_investigation` → `Skill(skill="investigation-cycle")`
   - `invoke_implementation` → `Skill(skill="implementation-cycle")`
   - `invoke_work_creation` → `Skill(skill="work-creation-cycle")`
   - `await_operator` → Report "No unblocked work. Awaiting operator direction."
   - `blocked` → Report warning with allowed cycles and rationale

---

## API Reference

### determine_route()

```python
def determine_route(
    next_work_id: Optional[str],
    has_plan: bool
) -> dict:
    """
    Determine routing action based on work-type signals.

    Args:
        next_work_id: ID of next work item (None if no work available)
        has_plan: Whether work item has documents.plans populated

    Returns:
        dict with keys:
            action: str - One of: invoke_investigation, invoke_implementation,
                          invoke_work_creation, await_operator
            reason: str - Why this action was chosen
    """
```

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Pure routing only | No threshold checks | S137: Thresholds in routing cause context-switching anti-pattern |
| Return dict | {action, reason} | Self-documenting, extensible for future signals |
| Single function | determine_route() | Simple API, easy to test |
| Bridge skill | Not a cycle | Routing is a decision, not a workflow |

---

## Related

- **E2-224:** OBSERVE Phase Threshold-Triggered Triage (where thresholds live)
- **E2-222:** Routing Threshold Configuration (future - makes thresholds configurable)
- **E2-223:** Integrate Routing-Gate into Cycle Skills (consumer integration)
- **INV-048:** Routing Gate Architecture (source investigation)
- **implementation-cycle:** Consumer of this skill
- **investigation-cycle:** Consumer of this skill
- **close-work-cycle:** Consumer of this skill
