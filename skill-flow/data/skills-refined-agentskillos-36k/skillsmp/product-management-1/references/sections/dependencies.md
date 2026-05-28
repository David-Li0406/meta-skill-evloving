# Dependency Graph

**CRITICAL SECTION** - This defines task execution order and blockers.

## Dependency Notation

```
## Task Dependencies

### Task 1.1: Setup Auth Module
- blockedBy: none (foundation task)
- enables: 1.2, 1.3

### Task 1.2: Implement Login
- blockedBy: 1.1
- enables: 2.1

### Task 1.3: Implement Registration
- blockedBy: 1.1
- enables: 2.2

### Task 2.1: Add Login UI
- blockedBy: 1.2
- enables: 3.1

### Task 2.2: Add Registration UI
- blockedBy: 1.3
- enables: 3.1

### Task 3.1: Integration Testing
- blockedBy: 2.1, 2.2
- enables: none (terminal task)
```

## Dependency Graph Visualization

```
1.1 (Auth Setup)
├── 1.2 (Login) ────┐
│   └── 2.1 (Login UI) ──┐
│                        ├── 3.1 (Integration)
└── 1.3 (Register) ──┐   │
    └── 2.2 (Reg UI) ────┘
```

## Dependency Types

| Type | Format | Example |
|------|--------|---------|
| Hard | blockedBy: X | Can't start without X complete |
| Soft | after: X | Should follow X, but not required |
| Parallel | with: X | Can run simultaneously |

## Rules for Task Creation

1. **Use explicit IDs** - `1.1`, `1.2`, not just names
2. **List all blockers** - `blockedBy: 1.1, 1.2`
3. **Identify foundation** - Tasks with `blockedBy: none` (create first)
4. **Identify terminals** - Tasks with `enables: none` (final tasks)
5. **Use TaskUpdate** - Set addBlockedBy after creating tasks

## Dependency Matrix

For complex projects:

```
| Task | 1.1 | 1.2 | 1.3 | 2.1 | 2.2 | 3.1 |
|------|-----|-----|-----|-----|-----|-----|
| 1.1  | -   |     |     |     |     |     |
| 1.2  | X   | -   |     |     |     |     |
| 1.3  | X   |     | -   |     |     |     |
| 2.1  |     | X   |     | -   |     |     |
| 2.2  |     |     | X   |     | -   |     |
| 3.1  |     |     |     | X   | X   | -   |
```

X = depends on

## Anti-Patterns

**Circular dependency:**
```
A → B → C → A  ❌ Invalid
```

**Orphan task:**
```
Task X: No blockedBy, no enables ❌ Disconnected
```

**Implicit dependency:**
```
"Task B should be done after A" ❌ Use blockedBy
```

## Validation Checklist

- [ ] All tasks have IDs
- [ ] No circular dependencies
- [ ] At least one foundation task (blockedBy: none)
- [ ] At least one terminal task (enables: none)
- [ ] Every task connects to the graph
