# {Feature Name}

## Overview

### Problem Statement
{Describe the core problem. Be concrete about user pain points.}

### Target Users
{Who experiences this problem and what they're trying to achieve.}

### Success Metrics
{Quantifiable outcomes. Example: "< 5% error rate", "2x faster than current"}

## Functional Decomposition

### Capability: {Name}
{Brief description of what this capability domain covers}

#### Feature: {Name}
- **Description**: {One sentence}
- **Inputs**: {What it needs}
- **Outputs**: {What it produces}
- **Behavior**: {Key logic}

#### Feature: {Name}
- **Description**:
- **Inputs**:
- **Outputs**:
- **Behavior**:

### Capability: {Name}
{...}

## Structural Decomposition

### Repository Structure

```
src/
├── {module-name}/       # Maps to: {Capability Name}
│   ├── {file}.ts        # Maps to: {Feature Name}
│   └── index.ts         # Public exports
└── {module-name}/
```

### Module: {Name}
- **Maps to capability**: {Capability from above}
- **Responsibility**: {Single clear purpose}
- **Exports**:
  - `functionName()` - {what it does}
  - `ClassName` - {what it does}

## Dependency Graph

### Foundation Layer (Phase 0)
No dependencies - built first.

- **{module-name}**: {What it provides}

### Core Layer (Phase 1)
- **{module-name}**: Depends on [{foundation-module}]

### Integration Layer (Phase 2)
- **{module-name}**: Depends on [{core-module}, {foundation-module}]

## Implementation Phases

### Phase 0: Foundation
**Goal**: {What foundational capability this establishes}

**Tasks**:
- [ ] {Task} (no deps) - Acceptance: {criteria}
- [ ] {Task} (no deps) - Acceptance: {criteria}

**Exit Criteria**: {Observable outcome}

### Phase 1: Core
**Goal**: {What this phase delivers}

**Tasks**:
- [ ] {Task} (depends on: Phase 0) - Acceptance: {criteria}

**Exit Criteria**: {Observable outcome}

### Phase 2: Integration
**Goal**: {What this phase delivers}

**Tasks**:
- [ ] {Task} (depends on: Phase 1) - Acceptance: {criteria}

**Exit Criteria**: {Observable outcome}

## Test Strategy

### Critical Scenarios
- **Happy path**: {scenario} → Expected: {outcome}
- **Edge case**: {scenario} → Expected: {outcome}
- **Error case**: {scenario} → Expected: {outcome}

## Risks

- **{Risk}**: {Mitigation strategy}
