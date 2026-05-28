# RPG (Repository Planning Graph) Methodology

A structured approach to creating PRDs that map directly to code implementation.

## Core Principle

Every requirement should trace from:
```
Problem → Capability → Feature → Code Location → Task → Test
```

## RPG Components

### 1. Problem Space
- What pain point exists?
- Who experiences it?
- What does success look like?

### 2. Capability Tree
Hierarchical decomposition:
```
Capability (what the system can do)
├── Feature (user-facing functionality)
│   ├── Sub-feature
│   └── Sub-feature
└── Feature
    └── Sub-feature
```

### 3. Structural Map
Code organization:
```
Capability → Module/Package
Feature → File/Class
Sub-feature → Function/Method
```

### 4. Dependency Graph
Task relationships:
```
Task A (foundation)
├── Task B (depends on A)
│   └── Task D (depends on B)
└── Task C (depends on A)
    └── Task D (depends on B, C)
```

### 5. Implementation Phases
Ordered execution:
- Phase 1: Foundation (no dependencies)
- Phase 2: Core features (depends on foundation)
- Phase 3: Integration (depends on core)
- Phase 4: Polish (depends on integration)

## Dependency Rules

Critical for task generation:

1. **No Orphans** - Every task connects to another
2. **No Cycles** - A → B → C → A is invalid
3. **Explicit Markers** - Use "blockedBy: [task-id]"
4. **Foundation First** - Create tasks with no dependencies first
5. **Link After Create** - Use TaskUpdate with addBlockedBy to set dependencies

## Structural Mapping Guidelines

```
| Capability | Module | Key Files |
|------------|--------|-----------|
| Auth       | /auth  | auth.service.ts, auth.controller.ts |
| Users      | /users | user.model.ts, user.repository.ts |
```

## Task ID Convention

Format: `{phase}.{capability}.{sequence}`

Examples:
- `1.auth.1` - First auth task in phase 1
- `2.users.3` - Third user task in phase 2

## Quality Signals

Good RPG PRD:
- Every feature maps to code
- Dependencies form a DAG (Directed Acyclic Graph)
- Phases are parallelizable where possible
- Clear handoff points between phases

Bad RPG PRD:
- Abstract features with no code mapping
- Implicit dependencies ("should be done after...")
- Monolithic phases with no parallelism
- Missing test coverage definition
