# Diagram Templates

## Use Case Diagram Template

```
┌─────────────────────────────────────────────────────────────────┐
│                     System: [System Name]                        │
│                                                                  │
│   ┌────────────────┐                    ┌────────────────┐      │
│   │   Use Case 1   │                    │   Use Case 2   │      │
│   │  [Description] │                    │  [Description] │      │
│   └───────┬────────┘                    └───────┬────────┘      │
│           │                                     │                │
│           │         ┌────────────────┐         │                │
│           └────────►│   Use Case 3   │◄────────┘                │
│                     │  [Description] │                          │
│                     └───────┬────────┘                          │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
         │ Actor 1 │     │ Actor 2 │     │ Actor 3 │
         │ [Role]  │     │ [Role]  │     │ [Role]  │
         └─────────┘     └─────────┘     └─────────┘
```

## State Diagram Template

```
                          [Initial State]
                                │
                                │ [trigger]
                                ▼
                         ┌─────────────┐
              ┌──────────│   State A   │──────────┐
              │          │ [behavior]  │          │
              │          └──────┬──────┘          │
              │                 │                 │
              │ [trigger]       │ [trigger]       │ [trigger]
              ▼                 ▼                 ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │   State B   │  │   State C   │  │   State D   │
       │ [behavior]  │  │ [behavior]  │  │ [behavior]  │
       └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
              │                 │                 │
              │                 │                 │
              └────────────────►│◄────────────────┘
                                │
                                │ [trigger]
                                ▼
                          ┌───────────┐
                          │   Final   │
                          │  [state]  │
                          └───────────┘

Legend:
─────► Transition
[trigger] Event/condition causing transition
[behavior] Action performed in state
```

## Sequence Diagram Template

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Actor   │     │ Component│     │ Component│     │ Component│
│    A     │     │    B     │     │    C     │     │    D     │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │  1. Request    │                │                │
     │───────────────>│                │                │
     │                │                │                │
     │                │  2. Validate   │                │
     │                │───────────────>│                │
     │                │                │                │
     │                │  3. Result     │                │
     │                │<───────────────│                │
     │                │                │                │
     │                │  4. Process    │                │
     │                │────────────────────────────────>│
     │                │                │                │
     │                │  5. Confirm    │                │
     │                │<────────────────────────────────│
     │                │                │                │
     │  6. Response   │                │                │
     │<───────────────│                │                │
     │                │                │                │

Legend:
─────> Synchronous call
- - -> Asynchronous call
<───── Return/response
```

## Component Diagram Template

```
┌─────────────────────────────────────────────────────────────────┐
│                        System Boundary                           │
│                                                                  │
│  ┌─────────────────┐         ┌─────────────────┐                │
│  │   Component A   │         │   Component B   │                │
│  │ ┌─────────────┐ │         │ ┌─────────────┐ │                │
│  │ │  Interface  │─┼────────►│ │  Interface  │ │                │
│  │ └─────────────┘ │         │ └─────────────┘ │                │
│  │                 │         │                 │                │
│  │ [Responsibility]│         │ [Responsibility]│                │
│  └─────────────────┘         └────────┬────────┘                │
│                                       │                          │
│                                       ▼                          │
│                              ┌─────────────────┐                │
│                              │   Component C   │                │
│                              │ ┌─────────────┐ │                │
│                              │ │  Interface  │ │                │
│                              │ └─────────────┘ │                │
│                              │                 │                │
│                              │ [Responsibility]│                │
│                              └─────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ External System │
                              │    [Name]       │
                              └─────────────────┘
```

## Data Flow Diagram Template

```
                    ┌─────────────────┐
                    │  External Entity │
                    │     [Name]       │
                    └────────┬────────┘
                             │
                             │ Data Flow 1
                             │ [description]
                             ▼
┌─────────────┐      ┌───────────────┐      ┌─────────────┐
│ Data Store  │◄─────│   Process 1   │─────►│ Data Store  │
│   [Name]    │      │   [Name]      │      │   [Name]    │
└─────────────┘      └───────┬───────┘      └─────────────┘
                             │
                             │ Data Flow 2
                             │ [description]
                             ▼
                     ┌───────────────┐
                     │   Process 2   │
                     │   [Name]      │
                     └───────────────┘

Legend:
□ External Entity (source/sink outside system)
○ Process (transforms data)
═ Data Store (repository)
→ Data Flow (data in motion)
```

## Entity Relationship Diagram Template

```
┌─────────────────┐          ┌─────────────────┐
│     Entity A    │          │     Entity B    │
├─────────────────┤          ├─────────────────┤
│ PK id           │──────┐   │ PK id           │
│    attribute1   │      │   │ FK entity_a_id  │◄─┐
│    attribute2   │      │   │    attribute1   │  │
│    created_at   │      │   │    attribute2   │  │
└─────────────────┘      │   └─────────────────┘  │
                         │                        │
                         └────────────────────────┘
                              1:N relationship

Relationship Types:
─────── 1:1 (One to One)
──────< 1:N (One to Many)
>─────< N:M (Many to Many)

Cardinality Notation:
│  Exactly one
○  Zero or one
<  Many
>< Many (both sides)
```

## User Flow Diagram Template

```
    ┌─────────────┐
    │    Start    │
    │ [Entry pt]  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │   Screen 1  │
    │ [Purpose]   │
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐     No      ┌─────────────┐
    │  Decision?   ├────────────►│   Screen 3  │
    │  [Question]  │             │  [Purpose]  │
    └──────┬───────┘             └──────┬──────┘
           │ Yes                        │
           ▼                            │
    ┌─────────────┐                     │
    │   Screen 2  │                     │
    │  [Purpose]  │                     │
    └──────┬──────┘                     │
           │                            │
           └────────────┬───────────────┘
                        │
                        ▼
                 ┌─────────────┐
                 │    End      │
                 │ [Outcome]   │
                 └─────────────┘

Flow Symbols:
□ Screen/Page/State
◇ Decision point
○ Start/End point
→ Flow direction
```

## Architecture Decision Record (ADR) Template

```markdown
# ADR-XXX: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-YYY]

## Context
[What is the issue that we're seeing that is motivating this decision or change?]

## Decision
[What is the change that we're proposing and/or doing?]

## Consequences
### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Downside 1]
- [Downside 2]

### Risks
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

## Alternatives Considered

### Option A: [Name]
- Pros: [...]
- Cons: [...]
- Why not chosen: [...]

### Option B: [Name]
- Pros: [...]
- Cons: [...]
- Why not chosen: [...]

## References
- [Link to relevant documentation]
- [Link to related decisions]
```
