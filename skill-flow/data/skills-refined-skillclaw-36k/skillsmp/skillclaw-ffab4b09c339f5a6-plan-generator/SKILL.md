---
name: plan-generator
description: Use this skill when you need to create structured, validated plans from requirements by coordinating with specialist agents and generating comprehensive planning artifacts.
---

# Skill body

## Capabilities
- Creating plans for new features
- Planning refactoring efforts
- Planning system migrations
- Planning architecture changes
- Breaking down complex requirements
- Validating existing plans

## Best Practices
- Coordinate with Analyst, PM, Architect for planning input
- Break down requirements into actionable steps (≤7 per section)
- Identify dependencies and sequencing
- Assess risks with mitigation strategies
- Validate plan completeness and feasibility

## Execution Process

### Step 1: Analyze Requirements
- Extract explicit requirements
- Identify implicit requirements
- Determine planning scope
- Assess complexity

### Step 2: Coordinate Specialists
Request planning input from relevant agents:
- **Analyst**: Business requirements and market context
- **PM**: Product requirements and user stories
- **Architect**: Technical architecture and design
- **Database Architect**: Data requirements
- **UX Expert**: Interface requirements

### Step 3: Generate Plan Structure
Create plan following this **EXECUTABLE** structure:
````markdown
# Plan: [Title]

## Executive Summary
[2-3 sentence overview]

## Objectives
- [Objective 1]
- [Objective 2]

## Phases
### Phase N: [Phase Title]
**Dependencies**: [Phase numbers or 'None']
**Parallel OK**: [Yes/No - can tasks run concurrently?]

#### Tasks
- [ ] **N.1** [Task description] (~X min)
  - **Command**: `actual shell command here`
  - **Verify**: `command to verify success`
  - **Rollback**: `command to undo if needed`

- [ ] **N.2** [Task description] (~X min) [⚡ parallel OK]
  - **Command**: `...`
  - **Verify**: `...`
````

### Step 4: Assess Risks
Identify risks and mitigation:
- Technical risks
- Resource risks
- Timeline risks
- Dependency risks
- Mitigation strategies

### Step 5: Validate Plan
Validate plan completeness:
- All requirements addressed
- Dependencies mapped
- Success criteria defined
- Risks identified
- Plan is feasible

### Step 6: Generate Artifacts
Create plan artifacts:
- Plan markdown: `.cursor/context/artifacts/plan-<id>.md`
- Plan JSON: `.cursor/context/artifacts/plan-<id>.json`
- Plan summary