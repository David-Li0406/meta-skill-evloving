---
description: Display task status summary from tasks/INDEX.md
argument-hint: [--graph] [--critical-path] [--order]
---

# Backlog Status

Display a summary table of all tasks from tasks/INDEX.md with dependency-aware status computation.

**Arguments:** $ARGUMENTS

## Instructions

### Step 1: Load Configuration

```bash
cat design.yaml 2>/dev/null
```

Extract `repo_prefix` and `repo_name`.

### Step 2: Check for Tasks

Find tasks/INDEX.md in current working directory.

**If not found or empty:** Report that no backlog is defined:
```
No backlog defined.

To create a backlog:
1. Run /design:init to create the tasks/ directory structure
2. Run /design to create your first task
```

### Step 3: Build Dependency Graph

Use the dependency utilities to build the full dependency graph:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/deps.sh"
deps_build_graph
```

This will:
- Parse tasks/INDEX.md
- Parse INDEX.md from any submodules with design.yaml (cross-repo deps)
- Build dependency and reverse-dependency graphs

### Step 4: Check for Circular Dependencies

```bash
if ! deps_check_cycles >/dev/null 2>&1; then
  echo "WARNING: Circular dependencies detected!"
  deps_check_cycles
fi
```

### Step 5: Compute Effective Status

For each task, compute the effective status based on dependencies:

```bash
for task in "${DEPS_ALL_TASKS[@]}"; do
  computed_status=$(deps_compute_status "$task")
  # May differ from stored status if deps changed
done
```

**Status computation rules:**
- If stored status is "In Progress", "In Review", or "Complete" → keep it
- If stored status is "Ready" or "Blocked":
  - Check all dependencies
  - If any dependency is not "Complete" → "Blocked"
  - If all dependencies are "Complete" → "Ready"

### Step 6: Display Status Table

```
═══════════════════════════════════════════════════════════════════
 BACKLOG STATUS: {REPO_NAME}
═══════════════════════════════════════════════════════════════════

| ID | Title | Status | Computed | Dependencies | Blockers |
|----|-------|--------|----------|--------------|----------|
| {PREFIX}-001 | ... | Complete | Complete | - | - |
| {PREFIX}-002 | ... | Ready | Ready | - | - |
| {PREFIX}-003 | ... | Ready | Blocked | {PREFIX}-002 | {PREFIX}-002 |

## Summary

- Complete: N
- In Progress: N
- In Review: N
- Ready: N (computed, all deps met)
- Blocked: N (computed, waiting on deps)

## Dependency Status

{Show any status mismatches between stored and computed}

## Ready for Agent

Tasks that can be started (all dependencies complete):
- {PREFIX}-001: {Title}
- {PREFIX}-002: {Title}

## Blocked

Tasks waiting on dependencies:
- {PREFIX}-003: Waiting on {PREFIX}-002 (In Progress)

## Next Recommended

{PREFIX}-001: {Title} - no dependencies, ready to start

═══════════════════════════════════════════════════════════════════
```

### Step 7: Optional Views

**If `--graph` argument:**
Show ASCII dependency visualization:

```bash
deps_visualize
```

Output:
```
Dependency Graph
================

[x] IDXEX-001
    -> IDXEX-003
[>] IDXEX-002
    -> IDXEX-004
[ ] IDXEX-003 <- {IDXEX-001}
[!] IDXEX-004 <- {IDXEX-002}

Legend: [x]=Complete [>]=In Progress [?]=Review [ ]=Ready [!]=Blocked
```

**If `--critical-path` argument:**
Show longest dependency chain:

```bash
deps_critical_path
```

Output:
```
Critical Path (longest dependency chain)
=========================================

Length: 3 steps

Path:
  1. IDXEX-001   [Complete   ] Core infrastructure
  2. IDXEX-003   [Ready      ] Fee collector
  3. IDXEX-005   [Blocked    ] Protocol integration
```

**If `--order` argument:**
Show recommended task order (topological sort):

```bash
deps_recommended_order
```

Output:
```
Recommended Task Order
======================

  1. IDXEX-001   [Ready      ] Core infrastructure
  2. IDXEX-002   [Ready      ] Registry system
  3. IDXEX-003   [Blocked    ] Fee collector (after: IDXEX-001)
  4. IDXEX-004   [Blocked    ] Vault types (after: IDXEX-001, IDXEX-002)
```

### Step 8: Cross-Repo Dependencies

If tasks depend on tasks in other repos (submodules), show them:

```
## Cross-Repo Dependencies

Tasks depending on external repos:
- IDXEX-003 depends on CRANE-005 (In Progress in lib/daosys/lib/crane)
- IDXEX-007 depends on DAO-012 (Complete in lib/daosys)

External tasks blocking this repo:
- CRANE-005: Slipstream utils (In Progress)
```

### Step 9: Suggest Status Updates

If computed status differs from stored status, suggest updates:

```
## Status Corrections Needed

The following tasks have incorrect stored status:

| Task | Stored | Computed | Reason |
|------|--------|----------|--------|
| IDXEX-003 | Ready | Blocked | IDXEX-001 not complete |
| IDXEX-004 | Blocked | Ready | All deps now complete |

To auto-fix: Run the dependency cascade after completing tasks.
```

## Arguments Reference

| Argument | Description |
|----------|-------------|
| `--graph` | Show ASCII dependency graph visualization |
| `--critical-path` | Show longest dependency chain |
| `--order` | Show recommended task execution order |

## Related Commands

- `/backlog:read <ID>` - Read full task details
- `/backlog:launch <ID>` - Launch agent worktree for a task
- `/backlog:review <ID>` - Transition task to review mode
- `/backlog:complete <ID>` - Complete and merge a task
- `/backlog:prune` - Archive completed tasks
- `/backlog:list` - List active worktrees
- `/design` - Create a new task
- `/design:review` - Review task definitions

## Error Handling

- **No tasks/ directory:** "Run /design:init to set up task management"
- **No design.yaml:** "Run /design:init to configure the repository"
- **Empty INDEX.md:** "No tasks defined. Use /design to create your first task"
- **Circular dependencies:** Show cycle path and affected tasks
