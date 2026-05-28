---
name: analyze-visualize-dependencies
description: Use this skill when you need to visualize and analyze issue dependencies in Linear, including identifying blocking chains, circular dependencies, and critical path items.
---

# Skill body

## When to Use
Use this skill when:
- Understanding what's blocking an issue
- Planning work order
- Identifying circular dependencies
- Finding critical path items

## Process

1. **Visualize Dependencies**
   ```bash
   linear deps <issue-id>
   linear deps --team <team-name>
   ```

2. **Analyze Blocking Chains**
   - Find longest blocking chains
   - Identify bottleneck issues
   - Locate circular dependencies

3. **Recommend Actions**

## Dependency Types

| Type        | Meaning                                          | Example                          |
|-------------|--------------------------------------------------|----------------------------------|
| blocks      | A must complete before B                         | Auth blocks Login UI             |
| blocked_by  | B cannot start until A is done                  | Login UI blocked by Auth         |
| related     | Informational link                               | Two related features             |
| duplicate   | Same issue                                      | Close one, reference the other   |

## Visualization Output

```
DEPENDENCY GRAPH: <issue-id>
════════════════════════════════════════
<issue-id> User Authentication Epic
├─ <sub-issue-id-1> Login flow [In Progress]
│  ├─ <sub-issue-id-2> OAuth integration [Todo]
│  │     → blocks: <sub-issue-id-3>
│  └─ <sub-issue-id-4> Session management [Todo]
├─ <sub-issue-id-5> Logout flow [Blocked]
│     ← blocked by: <sub-issue-id-1>
└─ <sub-issue-id-3> Token refresh [Blocked]
      ← blocked by: <sub-issue-id-2>
────────────────────────────────────────
<total-issues> issues, <total-dependencies> dependencies, <total-cycles> cycles
```

## Analysis Areas

### Blocking Chains
Issues that block many other issues are critical:
```
Critical blocker: <issue-id>
  → blocks <directly-blocked-issues> issues directly
  → blocks <transitively-blocked-issues> issues transitively
```

### Circular Dependencies
Cycles prevent any issue from completing:
```
⚠ Circular dependency detected:
  <issue-id-1> → <issue-id-2> → <issue-id-3> → <issue-id-1>
```

### Critical Path
Longest dependency chain determines minimum completion time:
```
Critical path (<number-of-issues> issues):
  <issue-id> → <sub-issue-id-1> → <sub-issue-id-2> → <sub-issue-id-3>
Minimum time: <total-completion-time>
```

### Orphaned Dependencies
Issues referencing non-existent or closed issues:
```
⚠ Orphaned dependencies:
  <issue-id> blocked by <closed-issue-id> (closed)
```

## Commands Used

```bash
# Single issue dependencies
linear deps <issue-id>

# Team-wide dependencies
linear deps --team <team-name>

# Check what blocks an issue
linear issues blocked-by <issue-id>

# Check what an issue blocks
linear issues blocking <issue-id>

# Create a dependency
linear issues update <issue-id> --blocked-by <other-issue-id>
```