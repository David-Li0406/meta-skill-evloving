---
name: requirement-analysis
description: Use this skill for in-depth requirement analysis to transform raw user needs into structured documentation and business rules.
---

# Skill: Requirement Analysis (需求分析)

## Skill Description

This skill is designed for in-depth analysis of user requirements, transforming raw needs into clear, actionable documentation through structured thinking.

## Applicable Scenarios

- When receiving raw user requirement descriptions.
- When needing to convert vague requirements into structured documents.
- When identifying functional modules and user scenarios.

## Core Capabilities

### 1. Requirement Decomposition
- Identify core and auxiliary functions.
- Distinguish between functional and non-functional requirements.
- Recognize implicit needs and boundary conditions.

### 2. User Analysis
- Identify target user groups.
- Define user roles and permissions.
- Analyze user scenarios and workflows.

### 3. Module Division
- Divide functional modules by business domain.
- Define module boundaries and dependencies.
- Evaluate module priorities.

### 4. Context Awareness & Optimization
- Identify data that does not need to be sent from the server again, streamlining requirements.
- Filter out client-side noise and focus on server responsibilities.

## Execution Process

```
1. Read the original requirements
   ↓
2. Extract key information (goals, users, functions)
   ↓
3. Identify user roles and permission boundaries
   ↓
4. Decompose functional modules
   ↓
5. Design core user scenarios
   ↓
6. Define non-functional requirements
   ↓
7. Output structured requirement documentation
```

## Output Template

```markdown
# {Project Name} - Requirement Document

## 1. Project Overview

### 1.1 Project Background
{2-3 sentences describing the project background}

### 1.2 Project Goals
{2-3 sentences describing the problem to be solved}

### 1.3 Core Value
{List 2-3 core value points}

## 2. User Roles

### 2.1 {Role Name}
- **Description**: {Role responsibilities}
- **Permission Scope**: {Accessible functions}
- **Typical Scenarios**: {Main usage scenarios}

## 3. Functional Modules

### 3.1 {Module Name}
**Module Description**: {One-sentence description}

**Function List**:
| Function Point | Description | Priority |
|----------------|-------------|----------|
| {Function1}    | {Description} | P0/P1/P2 |

**Business Rules**:
- {Rule1}
- {Rule2}

## 4. Core User Scenarios

### Scenario 1: {Scenario Name}
- **Preconditions**: {User status/system status}
- **Steps**:
  1. {Step1}
  2. {Step2}
- **Expected Result**: {State after success}
- **Exception Handling**: {Exception situations and handling}

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- Page load time: < {X}s
- API response time: < {X}ms
- Concurrent users: {X}

### 5.2 Security Requirements
- Authentication method: {JWT/Session, etc.}
- Data encryption: {Transmission/Storage}
- Permission control: {RBAC, etc.}

### 5.3 Usability Requirements
- System availability: {99.9%}
- Data backup: {Strategy}

## 6. Quality Check List

- [ ] Cover all key points of the original requirements
- [ ] Clear definition of user roles
- [ ] Clear boundaries of functional modules
- [ ] Complete user scenarios
- [ ] Quantifiable non-functional requirements
- [ ] Reasonable priority markings

## 7. Notes

1. **Focus on Core**: Write only project-related content, avoiding general best practices.
2. **Concise Expression**: Keep descriptions brief and avoid redundancy.
3. **Actionability**: Ensure each function point can be translated into development tasks.
4. **Consistency**: Maintain consistent terminology and naming.
```

## Interaction Guidance
After completing the task, if there are items in the "Questions" section, please explicitly prompt the user to review or respond.

## Tone
Objective, calm, and logically rigorous.