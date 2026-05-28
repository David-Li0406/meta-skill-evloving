---
name: ground-cycle
description: HAIOS Ground Cycle for loading architectural context before cognitive
  work. Use before plan-authoring, investigation, or implementation cycles.
generated: 2026-01-06
last_updated: '2026-01-06T21:07:54'
---
# Ground Cycle

This skill defines the PROVENANCE-ARCHITECTURE-MEMORY-CONTEXT MAP cycle for loading context before any cognitive work begins.

## When to Use

**Automatically invoked** at the start of:
- plan-authoring-cycle (before AMBIGUITY phase)
- investigation-cycle (before HYPOTHESIZE phase)
- implementation-cycle (before PLAN phase)

**Manual invocation:** `Skill(skill="ground-cycle", args="{work_id}")`

---

## The Cycle

```
PROVENANCE --> ARCHITECTURE --> MEMORY --> CONTEXT MAP --> [return GroundedContext]
     |               |              |              |
  Read WORK.md   Load epoch    Query prior     Build output
  Traverse      architecture   patterns       for caller
  spawned_by
```

---

## 1. PROVENANCE Phase

**Goal:** Traverse spawned_by chain to find source investigations.

**Actions:**
1. Read work item: `docs/work/active/{work_id}/WORK.md`
2. Extract `spawned_by_investigation` field
3. If set, read source investigation's key findings
4. Recursively traverse: E2-271 -> INV-057 -> INV-052
5. Collect provenance chain

**Exit Criteria:**
- [ ] Work item WORK.md read
- [ ] spawned_by_investigation traversed (if set)
- [ ] Provenance chain collected

**Tools:** Read, Glob

---

## 2. ARCHITECTURE Phase

**Goal:** Load epoch architecture for the work item.

**Actions:**
1. Extract `epoch` field from work item (e.g., "E2")
2. Load epoch definition: `.claude/haios/epochs/{epoch}/EPOCH.md`
3. Load REQUIRED READING from epoch's architecture/
4. Extract `chapter` and `arc` fields if present
5. Load chapter/arc REQUIRED READING if applicable

**Exit Criteria:**
- [ ] EPOCH.md loaded
- [ ] Architecture documents loaded
- [ ] REQUIRED READING section parsed

**Tools:** Read

---

## 3. MEMORY Phase

**Goal:** Query memory for relevant strategies and prior work.

**Actions:**
1. Query memory for epoch architecture: `"Epoch 2.2 architecture modules"`
2. Query memory for provenance chain topics
3. Query memory for work item related concepts
4. Collect relevant strategies

**Exit Criteria:**
- [ ] Memory queried with epoch context
- [ ] Strategies collected

**Tools:** mcp__haios-memory__memory_search_with_experience

---

## 4. CONTEXT MAP Phase

**Goal:** Build and output GroundedContext.

**Actions:**
1. Assemble GroundedContext object:
   ```yaml
   GroundedContext:
     epoch: E2
     chapter: C3-WorkInfra
     arc: ARC-001-ground-cycle
     provenance_chain: [E2-271, INV-057, INV-052]
     architectural_refs:
       - .claude/haios/epochs/E2/EPOCH.md
       - .claude/haios/epochs/E2/architecture/S17-modular-architecture.md
     memory_concepts: [80858, 80866, 80918]
     required_reading_loaded: true
   ```
2. Return to calling cycle

**Exit Criteria:**
- [ ] GroundedContext assembled
- [ ] Returned to calling cycle

**Tools:** (internal)

---

## GroundedContext Output Schema

```yaml
GroundedContext:
  # Work item context
  epoch: str                      # E2
  chapter: str | null             # C3-WorkInfra
  arc: str | null                 # ARC-001-ground-cycle

  # Provenance
  provenance_chain: list[str]     # [E2-271, INV-057, INV-052]

  # Architectural documents loaded
  architectural_refs: list[str]   # File paths loaded

  # Memory context
  memory_concepts: list[int]      # Concept IDs from memory query

  # Status
  required_reading_loaded: bool   # True if REQUIRED READING parsed
```

---

## Composition Map

| Phase | Primary Tool | Memory Integration |
|-------|--------------|-------------------|
| PROVENANCE | Read, Glob | - |
| ARCHITECTURE | Read | - |
| MEMORY | memory_search_with_experience | Query epoch + provenance |
| CONTEXT MAP | (internal) | - |

---

## Integration Points

### Calling Cycles

ground-cycle is invoked as "Phase 0" before cognitive work:

| Cycle | When Called | Before Phase |
|-------|-------------|--------------|
| plan-authoring-cycle | Work item enters `plan` node | AMBIGUITY |
| investigation-cycle | Work item enters `discovery` node | HYPOTHESIZE |
| implementation-cycle | Work item enters `implement` node | PLAN |

### Invocation Pattern

```python
# In plan-authoring-cycle, before AMBIGUITY phase:
Skill(skill="ground-cycle", args="{work_id}")
# ground-cycle returns GroundedContext
# plan-authoring-cycle continues with architectural awareness
```

### Call Chain Context

```
/new-plan E2-XXX (or /implement, /new-investigation)
    |
    +-> plan-authoring-cycle
            |
            +-> ground-cycle        # <-- THIS SKILL
            |       Input: work_id
            |       Output: GroundedContext
            |
            +-> AMBIGUITY phase (with grounded context)
            +-> ANALYZE phase
            +-> AUTHOR phase
            +-> VALIDATE phase
```

---

## Edge Cases

| Case | Handling |
|------|----------|
| No spawned_by_investigation | Skip PROVENANCE traversal, continue |
| No epoch field in work item | Default to "E2" (current epoch) |
| Epoch directory missing | Warn and continue without architecture |
| Memory MCP timeout | Warn and continue without strategies |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Separate skill | Not inline code | Reusable by multiple cycles |
| 4 phases | PROVENANCE->ARCHITECTURE->MEMORY->CONTEXT MAP | Logical progression |
| Return GroundedContext | Structured output | Downstream cycles consume consistently |
| No state persistence | In-memory only | Context is session-scoped |
| Token budget aware | Reference S15 | GroundedContext fits within L4 budget |

---

## Related

- **ARC-001-ground-cycle:** Arc containing this and related work items
- **S17-modular-architecture.md:** Module interfaces ground-cycle loads
- **S2C-work-item-directory.md:** Portal system for provenance traversal
- **S14-bootstrap-architecture.md:** Context loading hierarchy
- **S15-information-architecture.md:** Token budgets
- **plan-authoring-cycle:** Consumer - invokes ground-cycle before AMBIGUITY
- **investigation-cycle:** Consumer - invokes ground-cycle before HYPOTHESIZE
- **implementation-cycle:** Consumer - invokes ground-cycle before PLAN

---

*Created Session 179, E2-276*
