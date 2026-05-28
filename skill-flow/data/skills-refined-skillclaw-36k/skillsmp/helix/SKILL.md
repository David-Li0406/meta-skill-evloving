---
name: helix
description: Structured orchestrator with integrated memory. Spawns specialized agents for exploration, planning, building, and learning extraction.
argument-hint: <objective>
---

# Helix

Orchestration with memory-driven context injection and feedback-based learning.

## When to Use

- **Complex multi-step work** requiring exploration before implementation
- **Tasks that benefit from learned context** (similar work done before)
- **Work requiring verification** at each phase

For simple single-file changes, just do the work directly.

## Architecture

```
ORCHESTRATION: EXPLORE → PLAN → BUILD → OBSERVE
                  ↓         ↓        ↓        ↓
MEMORY:      recall() → inject → feedback() → store()

Scoring: (0.5 × relevance) + (0.3 × effectiveness) + (0.2 × recency)
Decay: 2^(-days_unused / 7)
```

## Workflow

```
/helix <objective>

    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ EXPLORE │───▶│  PLAN   │───▶│  BUILD  │───▶│ OBSERVE │
    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## Phase 1: EXPLORE

**Purpose:** Gather codebase context before planning.

**Agent:** `helix:helix-explorer` (haiku, 6 tool budget)

**Process:**
1. Query memory for relevant context
2. Discover structure, framework, idioms
3. Identify target files and functions

**Output:** JSON with structure, patterns, memory, targets.

---

## Phase 2: PLAN

**Purpose:** Decompose objective into executable task DAG.

**Agent:** `helix:helix-planner` (opus)

**Process:**
1. Analyze exploration context
2. Create tasks with dependencies, deltas, verification commands
3. Register tasks in Claude Code's native task system (visible via Ctrl+T)

**Output:** Task DAG with seq, slug, objective, delta, verify, depends, budget.

**Decision points:**
- `PROCEED` - sufficient information to plan
- `CLARIFY` - need answers before proceeding

---

## Phase 3: BUILD

**Purpose:** Execute tasks in dependency order.

**Agent:** `helix:helix-builder` (opus, per-task budget)

**Per task:**
1. Create workspace with memory injection (failures to avoid, patterns to apply)
2. Execute within constraints (delta scope, tool budget)
3. Verify completion
4. Report DELIVERED or BLOCKED with UTILIZED list

**Constraints enforced:**
- Delta scope is hard - cannot modify files outside delta
- Budget is hard - must complete or block when exhausted
- Verification required - no success claims without passing verify

**Metacognition:** After 3 failed attempts with similar approach → BLOCK with analysis, don't retry.

---

## Phase 4: OBSERVE

**Purpose:** Extract learning from completed work.

**Agent:** `helix:helix-observer` (opus)

**Extracts:**
- **Failures** from blocked workspaces (trigger + resolution)
- **Patterns** from successful workspaces via SOAR chunking
- **Relationships** between memories (co_occurs, causes, solves)

**Closes the loop:**
```python
feedback(utilized, injected)
# utilized memories: helped++
# injected-but-unused: failed++
```

---

## Memory System

### Scoring Formula

```
score = (0.5 × relevance) + (0.3 × effectiveness) + (0.2 × recency)

effectiveness = helped / (helped + failed)  # default 0.5 if no feedback
recency = 2^(-days_since_use / 7)           # ACT-R decay
```

Memories that help rise in ranking. Memories that don't help sink.

### Core Operations

**Store:**
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py store \
    --trigger "Situation description" \
    --resolution "What to do" \
    --type failure  # or pattern
```

**Recall:**
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py recall "query" --limit 5
```

**Feedback:**
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py feedback \
    --utilized '["mem-1"]' \
    --injected '["mem-1", "mem-2"]'
```

**Chunk (SOAR pattern extraction):**
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py chunk \
    --task "Task objective" \
    --outcome "success" \
    --approach "Technique used"
```

**Health:**
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py health
```

### Maintenance Operations

**Consolidate** - merge similar memories:
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py consolidate
```

**Prune** - remove ineffective memories:
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py prune
```

**Decay** - find dormant memories:
```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py decay
```

---

## Cognitive Guidelines

### Before Acting

1. **Query memory first** - check for relevant failures and patterns
2. **Assess complexity** - simple tasks don't need orchestration
3. **Understand intent** - what does success actually look like?

### During Execution

1. **Stay in scope** - delta is a hard constraint
2. **Verify before claiming success** - run the verify command
3. **Block when stuck** - clear blocking info > broken code

### Reporting

**UTILIZED must be accurate.** Only report memories you actually applied:
```
UTILIZED:
- memory-name: Applied validation pattern from resolution
```

Not:
```
UTILIZED: memory-1, memory-2, memory-3  # listing everything injected
```

False positives corrupt the feedback signal.

---

## Database

Single SQLite database at `.helix/helix.db`:

| Table | Purpose |
|-------|---------|
| memory | Failures and patterns with embeddings |
| memory_edge | Relationships between memories |
| exploration | Gathered context |
| plan | Task decompositions |
| workspace | Task execution contexts |

---

## Integration Points

**PreToolUse hook** (`inject-context.py`):
- Triggers on Edit/Write
- Injects relevant memories
- Requests UTILIZED reporting

**SessionStart hook** (`setup-env.sh`):
- Initializes database
- Sets environment variables
- Reports memory health

**Native Task system**:
- Tasks visible via Ctrl+T or /todos
- Status updates during execution
- Dependencies tracked
