# Phase 4: Diagrams & Artifacts

## Objective

Visualize user journeys, system behavior, and all pathways through the application.

## Step 1: Use Case Diagrams

Document actor-system interactions:

```markdown
### Use Case Diagram: [Feature Area]

```
┌─────────────────────────────────────────┐
│              System Boundary            │
│                                         │
│    ┌──────────┐      ┌──────────┐      │
│    │ Use Case │      │ Use Case │      │
│    │    A     │      │    B     │      │
│    └────┬─────┘      └────┬─────┘      │
│         │                  │            │
└─────────┼──────────────────┼────────────┘
          │                  │
     ┌────┴────┐        ┌────┴────┐
     │  Actor  │        │  Actor  │
     │    1    │        │    2    │
     └─────────┘        └─────────┘
```

### Use Cases Identified

| ID | Use Case | Primary Actor | Preconditions | Postconditions |
|----|----------|---------------|---------------|----------------|
| UC-001 | [Name] | [Actor] | [Before state] | [After state] |
| UC-002 | [Name] | [Actor] | [Before state] | [After state] |
```

### Use Case Detail Template

```markdown
### Use Case: [UC-ID] - [Name]

**Primary Actor**: [Who initiates]
**Secondary Actors**: [Who else involved]
**Preconditions**: [What must be true before]
**Postconditions**: [What is true after - success]

**Main Success Scenario**:
1. [Actor] [action]
2. System [response]
3. [Actor] [action]
4. System [response]
5. [End state]

**Extensions (Alternate Flows)**:
- 2a. [Condition]: System [alternate response]
- 3a. [Condition]: [Actor] [alternate action]

**Exceptions (Error Flows)**:
- 2b. [Error condition]: System [error handling]
```

## Step 2: User Flow Diagrams

Map complete user journeys:

```markdown
### User Flow: [Journey Name]

**Persona**: [Who]
**Goal**: [What they want to achieve]
**Entry Point**: [Where they start]

```
[Start]
   │
   ▼
┌─────────┐    No     ┌─────────┐
│ Decision├──────────►│ Action  │
│  Point  │           │   B     │
└────┬────┘           └────┬────┘
     │ Yes                 │
     ▼                     │
┌─────────┐                │
│ Action  │                │
│   A     │                │
└────┬────┘                │
     │                     │
     ▼                     ▼
┌─────────────────────────────┐
│        End State            │
└─────────────────────────────┘
```

**Decision Points**:
| Point | Question | Yes Path | No Path |
|-------|----------|----------|---------|
| D1 | [Condition?] | [Action A] | [Action B] |

**Exit Points**:
- Success: [Description]
- Abandon: [Where users might leave]
- Error: [Error states]
```

## Step 3: State Diagrams

Model system states and transitions:

```markdown
### State Diagram: [Entity/Component]

```
                    ┌─────────┐
         create     │         │
    ──────────────► │  Draft  │
                    │         │
                    └────┬────┘
                         │ submit
                         ▼
                    ┌─────────┐
         reject     │         │  approve
    ◄───────────────┤ Pending ├──────────►
                    │         │
                    └────┬────┘
                         │ cancel
                         ▼
                    ┌─────────┐
                    │         │
                    │ Canceled│
                    │         │
                    └─────────┘
```

### State Definitions

| State | Description | Entry Conditions | Exit Conditions |
|-------|-------------|------------------|-----------------|
| Draft | [Description] | [How to enter] | [How to leave] |
| Pending | [Description] | [How to enter] | [How to leave] |
| Approved | [Description] | [How to enter] | [How to leave] |

### Transition Rules

| From | To | Trigger | Guard Conditions | Actions |
|------|------|---------|------------------|---------|
| Draft | Pending | submit | [Conditions] | [Side effects] |
| Pending | Approved | approve | [Conditions] | [Side effects] |
```

## Step 4: Edge Case Mapping

Systematically identify edge cases:

```markdown
### Edge Case Matrix: [Feature]

| Category | Edge Case | Expected Behavior | User Impact |
|----------|-----------|-------------------|-------------|
| **Input** | Empty input | [Behavior] | [Impact] |
| **Input** | Max length exceeded | [Behavior] | [Impact] |
| **Input** | Invalid characters | [Behavior] | [Impact] |
| **Timing** | Concurrent requests | [Behavior] | [Impact] |
| **Timing** | Timeout | [Behavior] | [Impact] |
| **State** | Already exists | [Behavior] | [Impact] |
| **State** | Not found | [Behavior] | [Impact] |
| **Auth** | Expired session | [Behavior] | [Impact] |
| **Auth** | Insufficient permissions | [Behavior] | [Impact] |
| **System** | Dependency unavailable | [Behavior] | [Impact] |
```

## Step 5: Error Flow Diagrams

Map how errors propagate and resolve:

```markdown
### Error Flow: [Error Type]

```
[Normal Operation]
        │
        ▼ Error occurs
┌───────────────┐
│ Error State   │
│ [Description] │
└───────┬───────┘
        │
        ▼
┌───────────────┐      ┌───────────────┐
│ User Notified │      │ System Logs   │
│ [How]         │      │ [What]        │
└───────┬───────┘      └───────────────┘
        │
        ▼
┌───────────────┐
│ Recovery      │
│ Options       │
├───────────────┤
│ • Retry       │
│ • Cancel      │
│ • Contact     │
└───────────────┘
```

### Error Recovery Matrix

| Error | Detection | User Message | Recovery Action | Logging |
|-------|-----------|--------------|-----------------|---------|
| [Error 1] | [How detected] | [What user sees] | [What they can do] | [What's logged] |
```

## Step 6: Critical Reflection

### Coverage Check
- Does every user story have a corresponding user flow?
- Are all states reachable and escapable?
- Are all error conditions handled?

### Consistency Check
- Do diagrams align with requirements?
- Are state names consistent across diagrams?
- Do flows match use cases?

### Completeness Check
- Can users complete all goals?
- Are there orphaned states (unreachable)?
- Are there trap states (no exit)?

## Phase 4 Approval Gate

```markdown
## Phase 4 Summary: Diagrams & Artifacts

### Artifacts Created

| Type | Count | Coverage |
|------|-------|----------|
| Use Case Diagrams | [X] | [Y]% of user stories |
| User Flow Diagrams | [X] | [Y]% of journeys |
| State Diagrams | [X] | [Y]% of entities |
| Edge Case Mappings | [X] | [Y] cases identified |
| Error Flows | [X] | [Y] error types |

### Key User Journeys Documented
[List primary flows]

### Edge Cases Identified
| Priority | Count |
|----------|-------|
| Critical | [X] |
| Important | [Y] |
| Minor | [Z] |

### Open Questions
[Any flows or states needing clarification]

---

**Do you approve Phase 4? Any diagrams to revise before proceeding to Architecture & Design?**
```
