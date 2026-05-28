# Expected Markdown File Formats

This reference shows the expected structure of epic, feature, and sprint markdown files.

## Epic Format

```markdown
# Epic 1: Update Existing Services

**Epic ID**: 1
**Epic Name**: Update Existing Services
**Phase**: Phase 1 - Existing Service Enhancement
**Status**: Planning
**Priority**: CRITICAL
**Estimated Duration**: 1.5 weeks (11 hours development + testing)

---

## Epic Overview

### Purpose

[Description of what the epic does]

### Scope

[What is included in the epic]

### Out of Scope

[What is NOT included]

---

## Business Context

### Problem Statement

[Problem being solved]

### Business Impact

[Impact of the problem]

### Success Criteria

1. ✅ Criterion 1
2. ✅ Criterion 2

---

## Implementation Tasks

### Task 1.1: [Task Name]

**Objective**: [What this task accomplishes]

**Estimated Effort**: 2 hours development, 1 hour testing

[Additional task details...]

---

## Acceptance Criteria

- [x] All components installed correctly
- [ ] Tests passing
```

**Key Fields to Extract**:
- Epic ID (from bold metadata or heading)
- Epic Name
- Status (Planning, In Progress, etc.)
- Priority (CRITICAL, HIGH, MEDIUM, LOW)
- Duration
- Overview/Purpose → Description
- Tasks → For UCP calculation
- Acceptance Criteria → Add to description

## Feature Format

```markdown
# Feature 101.1: Core Architecture & TDD Implementation

**Feature ID:** 101.1
**Feature Name:** Core Architecture & TDD Implementation
**Epic:** 101 - Session-Centric Architecture Refactoring
**Status:** In Planning
**Duration:** 5 weeks
**Priority:** Critical

---

## Executive Summary

[High-level overview of the feature]

---

## Implementation Scope

### Core Components to Build

#### 1. Component Name (Week 1)
- Subcomponent A
- Subcomponent B

[More components...]

---

## Technical Requirements

### Functional Requirements

#### FR-1: Requirement Name
- **Requirement**: Description
- **Implementation**: How it's implemented
- **Validation**: How to verify

---

## Week-by-Week Breakdown

### Week 1: Foundation

#### Tasks:
1. **Create Component X**
   [Details...]

---

## Acceptance Criteria

- [ ] Functional criterion 1
- [ ] Non-functional criterion 2
```

**Key Fields to Extract**:
- Feature ID (from heading or metadata)
- Feature Name
- Epic (parent Epic ID)
- Status
- Priority
- Duration
- Executive Summary → Description
- Tasks → For UCP calculation
- Acceptance Criteria

## Sprint/User Story Format

```markdown
# Sprint 101.1.1: Global Services & Session Registry

**Sprint ID:** 101.1.1
**Sprint Name:** Global Services & Session Registry
**Feature:** 101.1 - Core Architecture TDD Implementation
**Duration:** 2 weeks (10 business days)
**Status:** Ready for Implementation

---

## Sprint Goals

1. **Goal 1**: Description
2. **Goal 2**: Description

---

## User Stories

### Story 1: Story Title
**As a** [role]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] AC 1
- [ ] AC 2

---

## Technical Tasks

### Day 1-2: Component Implementation

**TASK-001: Create Class Structure**
- Estimated: 4 hours
- Dependencies: None
- [Implementation details]

**TASK-002: Implement Logic**
- Estimated: 3 hours
- Dependencies: TASK-001
- [Implementation details]

---

## Definition of Done

- [ ] All code follows best practices
- [ ] Tests passing
```

**Key Fields to Extract**:
- Sprint ID (from heading)
- Sprint Name
- Feature (parent Feature ID)
- Status
- Duration
- Sprint Goals → Description
- User Stories → Acceptance criteria
- Tasks (TASK-001 format) → For UCP calculation and Effort field

## Common Patterns

### Task Extraction Patterns

**Pattern 1**: Bold task with estimate below
```
**TASK-001: Task Name**
- Estimated: 4 hours
```

**Pattern 2**: Heading task with effort inline
```
### Task 1.1: Task Name
**Estimated Effort**: 2 hours development, 1 hour testing
```

### ID Inference

- **Epic**: Single number (1, 2, 101)
- **Feature**: Decimal format (101.1, 1.2) → Parent is first part (101, 1)
- **Sprint**: Multi-decimal (101.1.1, 1.2.3) → Parent is first two parts (101.1, 1.2)

### Status Normalization

| Markdown | DevOps State |
|----------|--------------|
| Planning, In Planning | New |
| Ready for Implementation | New |
| In Progress, Active | Active |
| Completed, Done | Resolved |
| Closed | Closed |
