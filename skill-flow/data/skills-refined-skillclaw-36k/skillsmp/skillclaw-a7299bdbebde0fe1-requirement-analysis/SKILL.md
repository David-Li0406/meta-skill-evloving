---
name: requirement-analysis
description: Use this skill when you need to analyze user requirements and produce a structured requirements document or business rules for a project.
---

# Skill body

## Core Capabilities

### 1. Requirement Breakdown
- Identify core and auxiliary functionalities.
- Distinguish between functional and non-functional requirements.
- Recognize implicit requirements and boundary conditions.

### 2. User Analysis
- Identify target user groups.
- Define user roles and permissions.
- Analyze user scenarios and workflows.

### 3. Module Division
- Categorize functionalities by business domain.
- Define module boundaries and dependencies.
- Assess module priorities.

## Execution Process

```
1. Read the original requirements document.
   ↓
2. Extract key information (goals, users, functionalities).
   ↓
3. Identify user roles and permission boundaries.
   ↓
4. Divide functionalities into modules.
   ↓
5. Design core user scenarios.
   ↓
6. Define non-functional requirements.
   ↓
7. Output a structured requirements document or business rules.
```

## Output Template

```markdown
# {Project Name} - Requirements Document

## 1. Project Overview

### 1.1 Background
{2-3 sentences describing the project background}

### 1.2 Objectives
{2-3 sentences describing the problem to be solved}

### 1.3 Core Value
{List 2-3 core value points}

## 2. User Roles

### 2.1 {Role Name}
- **Description**: {Role responsibilities}
- **Permission Scope**: {Accessible functionalities}
- **Typical Scenarios**: {Main usage scenarios}

## 3. Functional Modules

### 3.1 {Module Name}
**Module Description**: {One-sentence description}

**Functionality List**:
| Functionality | Description | Priority |
|---------------|-------------|----------|
| {Function1}   | {Description} | P0/P1/P2 |

**Business Rules**:
- {Rule1}
- {Rule2}

## 4. Core User Scenarios

### Scenario 1: {Scenario Name}
- **Pre-conditions**: {User/system state}
- **Steps**:
  1. {Step1}
  2. {Step2}
- **Expected Result**: {State after success}
- **Exception Handling**: {Exceptions and handling}

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- Page load time: < {X}s
- API response time: < {X}ms
- Concurrent users: {X}

### 5.2 Security Requirements
- Authentication method: {JWT/Session, etc.}
- Data encryption: {Transport/Storage}
- Permission control: {RBAC, etc.}

### 5.3 Usability Requirements
- System availability: {99.9%}
- Data backup: {Strategy}
```

## Quality Check List

- [ ] Covers all key points of the original requirements.
- [ ] User roles are clearly defined.
- [ ] Functional module boundaries are clear.
- [ ] User scenarios include complete processes.
- [ ] Non-functional requirements have quantifiable metrics.
- [ ] Priority markings are reasonable.

## Notes

1. **Focus on Core**: Write only project-related content, avoiding general best practices.
2. **Concise Expression**: Keep each description as brief as possible, avoiding redundancy.
3. **Actionability**: Ensure each functionality can be translated into development tasks.
4. **Consistency**: Maintain consistent terminology and naming conventions.