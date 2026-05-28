---
name: plan-generator
description: Use this skill to create structured plans from requirements, generating comprehensive plans with steps, dependencies, risks, and success criteria while coordinating with specialist agents for input and validating plan completeness.
---

# Body of the merged SKILL.md

## Identity
Plan Generator Skill - Creates structured, validated plans from requirements by coordinating with specialist agents and generating comprehensive planning artifacts.

## Capabilities
- Creating plans for new features
- Planning refactoring efforts
- Planning system migrations
- Planning architecture changes
- Breaking down complex requirements
- Validating existing plans

## Instructions
### Execution Process

#### Step 1: Analyze Requirements
Parse user requirements:
- Extract explicit requirements
- Identify implicit requirements
- Determine planning scope
- Assess complexity

#### Step 2: Coordinate Specialists
Request planning input from relevant agents:
- **Analyst**: Business requirements and market context
- **PM**: Product requirements and user stories
- **Architect**: Technical architecture and design
- **Database Architect**: Data requirements
- **UX Expert**: Interface requirements

#### Step 3: Generate Plan Structure
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

#### Phase N Error Handling
If any task fails:
1. Run rollback commands for completed tasks (reverse order)
2. Document error: `echo "Phase N failed: [error]" >> .claude/context/memory/issues.md`
3. Do NOT proceed to Phase N+1

#### Phase N Verification Gate
```bash
# All must pass before proceeding
[verification commands]
```
````

#### Step 4: Assess Risks
Identify risks and mitigation:
- Technical risks
- Resource risks
- Timeline risks
- Dependency risks
- Mitigation strategies

#### Step 5: Validate Plan
Validate plan completeness:
- All requirements addressed
- Dependencies mapped
- Success criteria defined
- Risks identified
- Plan is feasible

#### Step 6: Generate Artifacts
Create plan artifacts:
- Plan markdown: `.claude/context/artifacts/plan-<id>.md`
- Plan JSON: `.claude/context/artifacts/plan-<id>.json`
- Plan summary

## Plan Types
**Feature Development Plan**:
- Objectives: Feature goals
- Steps: Analysis -> Design -> Implementation -> Testing
- Agents: Analyst -> PM -> Architect -> Developer -> QA

**Refactoring Plan**:
- Objectives: Code quality goals
- Steps: Analysis -> Planning -> Implementation -> Validation
- Agents: Code Reviewer -> Refactoring Specialist -> Developer -> QA

**Migration Plan**:
- Objectives: Migration goals
- Steps: Analysis -> Planning -> Execution -> Validation
- Agents: Architect -> Legacy Modernizer -> Developer -> QA

**Architecture Plan**:
- Objectives: Architecture goals
- Steps: Analysis -> Design -> Validation -> Documentation
- Agents: Architect -> Database Architect -> Security Architect -> Technical Writer

## Integration
**Integration with Planner Agent**:
Planner agent uses this skill to:
- Generate plans from requirements
- Coordinate specialist input
- Validate plan completeness
- Track plan execution

## Best Practices
1. **Coordinate Early**: Get specialist input before finalizing plan
2. **Keep Steps Focused**: ≤7 steps per plan section
3. **Map Dependencies**: Clearly identify prerequisites
4. **Assess Risks**: Identify and mitigate risks proactively
5. **Validate Thoroughly**: Ensure plan is complete and feasible

## Examples
**Example Plan Output**

**Command**: "Generate plan for user authentication feature"

**Generated Plan**:

```markdown
# Plan: User Authentication Feature

## Executive Summary
Add JWT-based authentication with login/logout endpoints. Includes password hashing, session management, and security testing.

## Objectives
- Implement JWT-based authentication
- Support login, logout, and session management
- Provide secure password handling

## Phases

### Phase 1: Setup & Design
**Dependencies**: None
**Parallel OK**: Partial

#### Tasks
- [ ] **1.1** Create feature branch (~2 min)
  - **Command**: `git checkout -b feature/auth`
  - **Verify**: `git branch --show-current | grep feature/auth`

- [ ] **1.2** Create auth module directory (~1 min) [⚡ parallel OK]
  - **Command**: `mkdir -p src/auth`
  - **Verify**: `ls -d src/auth`

- [ ] **1.3** Design auth architecture (~15 min)
  - **Command**: `Task({ agent: "architect", prompt: "Design JWT auth..." })`
  - **Verify**: `ls .claude/context/artifacts/auth-design.md`

#### Phase 1 Verification Gate
```bash
git branch --show-current | grep feature/auth && ls src/auth && ls .claude/context/artifacts/auth-design.md
```

### Phase 2: Implementation
**Dependencies**: Phase 1
**Parallel OK**: No (sequential TDD)

#### Tasks
- [ ] **2.1** Write auth endpoint tests (~10 min)
  - **Command**: `Task({ agent: "developer", prompt: "TDD: Write failing tests for /login endpoint" })`
  - **Verify**: `npm test -- --grep "login" 2>&1 | grep -E "failing|FAIL"`
  - **Rollback**: `git checkout -- src/auth/__tests__/`

- [ ] **2.2** Implement login endpoint (~15 min)
  - **Command**: `Task({ agent: "developer", prompt: "Implement login to pass tests" })`
  - **Verify**: `npm test -- --grep "login" 2>&1 | grep -E "passing|PASS"`

- [ ] **2.3** Implement logout endpoint (~10 min)
  - **Command**: `Task({ agent: "developer", prompt: "TDD: logout endpoint" })`
  - **Verify**: `npm test -- --grep "logout" 2>&1 | grep -E "passing|PASS"`

#### Phase 2 Error Handling
If any task fails:
1. Run: `git stash && git checkout -- src/auth/`
2. Document: `echo "Phase 2 failed: $(date)" >> .claude/context/memory/issues.md`
3. Do NOT proceed to Phase 3

#### Phase 2 Verification Gate
```bash
npm test -- --grep "auth" && echo "All auth tests passing"
```

### Phase 3: Security Review
**Dependencies**: Phase 2
**Parallel OK**: Yes

#### Tasks
- [ ] **3.1** Security audit (~20 min) [⚡ parallel OK]
  - **Command**: `Task({ agent: "security-architect", prompt: "Audit auth implementation" })`
  - **Verify**: `ls .claude/context/reports/security-audit.md`

- [ ] **3.2** Run security tests (~5 min) [⚡ parallel OK]
  - **Command**: `npm run test:security`
  - **Verify**: `echo $?` (exit code 0)

## Risks
| Risk                | Impact | Mitigation            | Rollback                  |
| ------------------- | ------ | --------------------- | ------------------------- |
| JWT secret exposure | High   | Use env vars          | Rotate secret immediately |
| SQL injection       | High   | Parameterized queries | `git revert HEAD`         |

## Timeline Summary
| Phase     | Tasks | Est. Time   | Parallel? |
| --------- | ----- | ----------- | --------- |
| 1         | 3     | 18 min      | Partial   |
| 2         | 3     | 35 min      | No        |
| 3         | 2     | 25 min      | Yes       |
| **Total** | **8** | **~78 min** |           |

```