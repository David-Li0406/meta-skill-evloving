---
name: crank
description: 'Fully autonomous epic execution. Runs until ALL children are CLOSED. Loops through beads issues, runs /implement on each, validates with /vibe. NO human prompts, NO stopping.'
---

# crank: Autonomous Epic Execution

> **Runs until epic is CLOSED. Auto-adapts to Mayor (parallel) or Crew (sequential) mode.**

## Philosophy: The Brownian Ratchet (FIRE Loop)

Crank is the full implementation of the Brownian Ratchet pattern via the **FIRE loop**:

| FIRE Phase | Ratchet Role | Description |
|------------|--------------|-------------|
| **FIND** | Read state | Identify ready work, burning work, reaped work |
| **IGNITE** | **Chaos** | Spark parallel polecats (Mayor) or start work (Crew) |
| **REAP** | **Filter + Ratchet** | Validate, merge (permanent), close issues |
| **ESCALATE** | Recovery | Retry failures or escalate blockers to human |

The FIRE loop IS the ratchet:
```
FIND → IGNITE (chaos) → REAP (filter + ratchet) → ESCALATE → loop
```

**Key insight:** Polecats can fail independently. Each successful merge ratchets forward.
The system extracts progress from parallel attempts, filtering failures automatically.

See [fire.md](fire.md) for full loop specification.

## Role Detection

Crank auto-detects execution mode based on current context:

```bash
# Check role by directory structure
if [[ "$PWD" == */mayor/* ]] || [[ "$PWD" == ~/gt ]]; then
    ROLE="mayor"    # Can spawn polecats
else
    ROLE="crew"     # Execute directly
fi
```

| Role | Execution Style | Parallelism | Command |
|------|-----------------|-------------|---------|
| **Mayor** | Dispatch to polecats via `gt sling` | Up to 8 concurrent | `gt sling <issue> <rig>` |
| **Crew** | Execute directly via `/implement` | Sequential | `/implement <issue>` |

## Quick Start

```bash
# Auto-discover epic (finds open epic in current context)
/crank

# Explicit epic - USE IT DIRECTLY, NO DISCOVERY
/crank <epic-id>

# Force a specific mode
/crank <epic-id> --mode=crew     # Sequential, no polecats
/crank <epic-id> --mode=mayor    # Parallel via polecats
```

## CRITICAL: Argument Handling

**RULE: If an epic ID is provided, USE IT IMMEDIATELY. Do NOT run discovery.**

```python
def parse_args(args):
    """Parse crank arguments."""
    if args and args[0].startswith(('ol-', 'ap-', 'gt-', 'be-', 'he-', 'ho-')):
        # Explicit epic ID provided - USE IT, NO QUESTIONS
        return {'epic': args[0], 'mode': parse_mode(args)}

    # Only run discovery if NO epic ID provided
    return {'epic': discover_epic(), 'mode': parse_mode(args)}
```

**Anti-pattern (DO NOT DO):**
```
User: /crank ol-rg3p
Claude: "I found multiple epics, which one?" <- WRONG! User said ol-rg3p!
```

**Correct behavior:**
```
User: /crank ol-rg3p
Claude: [Immediately starts cranking ol-rg3p, no questions]
```

## Discovery (ONLY when no epic ID provided)

When invoked with just `/crank` (no arguments), infer the target:

### Priority 1: Conversational Context

If the user mentions a topic (e.g., "/crank flywheel"), search:

```bash
bd search "flywheel" --type epic --status open
```

### Priority 2: Beads Discovery

```bash
EPICS=$(bd list --type epic --status open 2>/dev/null | head -5)
EPIC_COUNT=$(echo "$EPICS" | grep -c '^' 2>/dev/null || echo 0)

if [[ "$EPIC_COUNT" -eq 1 ]]; then
    EPIC_ID=$(echo "$EPICS" | awk '{print $1}')
    # USE IT - one epic, no ambiguity
elif [[ "$EPIC_COUNT" -gt 1 ]]; then
    # ASK - multiple epics, need clarification
    echo "[CRANK] Multiple open epics. Please specify: /crank <epic-id>"
fi
```

### Priority 3: Recent Context

Check conversation history for recently-mentioned epic IDs.

## The ODMCR Loop

Both modes use the same reconciliation loop, just different dispatch mechanisms:

```
┌─────────────────────────────────────────────────────────┐
│                    ODMCR LOOP                           │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │ OBSERVE  │───►│ DISPATCH │───►│ MONITOR  │          │
│  └──────────┘    └──────────┘    └──────────┘          │
│       ▲                               │                 │
│       │          ┌──────────┐         │                 │
│       │          │  RETRY   │◄────────┤                 │
│       │          └──────────┘         │                 │
│       │               │               ▼                 │
│       │          ┌──────────┐    ┌──────────┐          │
│       └──────────│ (loop)   │◄───│ COLLECT  │          │
│                  └──────────┘    └──────────┘          │
│                                                         │
│  EXIT: All children status=closed                       │
└─────────────────────────────────────────────────────────┘
```
