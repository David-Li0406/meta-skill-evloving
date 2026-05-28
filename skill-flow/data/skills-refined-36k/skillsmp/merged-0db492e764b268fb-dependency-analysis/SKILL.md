---
name: dependency-analysis
description: Use this skill to visualize and analyze issue dependencies in Linear, identifying blocking chains, circular dependencies, and critical path items.
---

# Dependency Analysis Skill

You are an expert at analyzing and visualizing software project dependencies.

## When to Use

Use this skill when:
- Understanding what's blocking an issue
- Planning work order
- Identifying circular dependencies
- Finding critical path items

## Process

1. **Visualize Dependencies**
   ```bash
   linear deps <issue_id>
   linear deps --team <team_name>
   ```

2. **Analyze Blocking Chains**
   - Find longest blocking chains
   - Identify bottleneck issues
   - Locate circular dependencies

3. **Recommend Actions**

## Dependency Types

| Type        | Meaning                                      | Example                          |
|-------------|----------------------------------------------|----------------------------------|
| blocks      | A must complete before B                     | Auth blocks Login UI             |
| blocked_by  | B cannot start until A is done               | Login UI blocked by Auth         |
| related     | Informational link                           | Two related features             |
| duplicate   | Same issue                                   | Close one, reference other       |

## Visualization Output

```
DEPENDENCY GRAPH: <issue_id>
════════════════════════════════════════
<issue_id> User Authentication Epic
├─ <sub_issue_id_1> Login flow [In Progress]
│  ├─ <sub_issue_id_2> OAuth integration [Todo]
│  │     → blocks: <sub_issue_id_3>
│  └─ <sub_issue_id_4> Session management [Todo]
├─ <sub_issue_id_5> Logout flow [Blocked]
│     ← blocked by: <sub_issue_id_1>
└─ <sub_issue_id_3> Token refresh [Blocked]
      ← blocked by: <sub_issue_id_2>
────────────────────────────────────────
<total_issues> issues, <total_dependencies> dependencies, <total_cycles> cycles
```

## Analysis Areas

### Blocking Chains
Issues that block many other issues are critical:
```
Critical blocker: <critical_blocker_id>
  → blocks <directly_blocked_count> issues directly
  → blocks <transitively_blocked_count> issues transitively
```

### Circular Dependencies
Cycles prevent any issue from completing:
```
⚠ Circular dependency detected:
  <issue_id_1> → <issue_id_2> → <issue_id_3> → <issue_id_1>
```

### Critical Path
Longest dependency chain determines minimum completion time:
```
Critical path (<issue_count> issues):
  <issue_id_1> → <issue_id_2> → <issue_id_3> → <issue_id_4>
Minimum time: <total_completion_time>
```

### Orphaned Dependencies
Issues referencing non-existent or closed issues:
```
⚠ Orphaned dependencies:
  <issue_id> blocked by <closed_issue_id> (closed)
```

## Commands Used

```bash
# Single issue dependencies
linear deps <issue_id>

# Team-wide dependencies
linear deps --team <team_name>

# Check what blocks an issue
linear issues blocked-by <issue_id>

# Check what an issue blocks
linear issues blocking <issue_id>

# Create a dependency
linear issues update <issue_id> --blocked-by <blocking_issue_id>

# Create multiple dependencies (comma-separated)
linear issues update <issue_id> --blocked-by <blocking_issue_id_1>,<blocking_issue_id_2>

# Remove a dependency (update with empty)
linear issues update <issue_id> --blocked-by ""
```

## Key Learnings

- **Issue identifiers (e.g., <issue_id>) don't require team context** - work without `linear init`
- **Team-wide analysis requires team context** - use `linear init` or `--team` flag
- Dependencies are detected automatically and shown in ASCII graph format
- Circular dependencies are detected and highlighted with warnings

## Action Recommendations

Based on analysis, recommend:

1. **Unblock critical path** - Prioritize blockers
2. **Break cycles** - Remove unnecessary dependencies
3. **Parallelize** - Find work that can happen concurrently
4. **Update stale deps** - Clean up outdated relationships

## Best Practices

1. **Keep dependencies minimal** - Only add necessary ones
2. **Use blocks, not blocked_by** - Clearer mental model
3. **Review regularly** - Dependencies become stale
4. **Document non-obvious deps** - Add comments explaining why