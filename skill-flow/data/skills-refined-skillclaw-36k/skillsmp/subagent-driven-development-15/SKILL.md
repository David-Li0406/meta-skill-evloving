---
name: subagent-driven-development
description: "Use for complex features requiring multi-stage review, architectural work, or multi-file changes. Orchestrates specialized agents for coordinated implementation."
---

# Subagent-Driven Development

**Iron Law:** Complex features require specialized expertise, coordinated execution, and multi-stage verification.

## When to Use

| Scenario | Use This Skill |
|----------|----------------|
| Multi-file changes (5+ files) | YES |
| Architectural decisions needed | YES |
| Multiple domain expertise required | YES |
| Cross-cutting concerns (security, performance) | YES |
| Simple single-file fix | NO - execute directly |
| Clear scope, single domain | NO - use direct agent |

## The Process

```
1. DECOMPOSE  -> Break feature into subtasks
2. SELECT     -> Assign agents to subtasks
3. SEQUENCE   -> Define execution order
4. DELEGATE   -> Invoke agents with full context
5. AGGREGATE  -> Collect and integrate results
6. VERIFY     -> Final quality check
```

## Step 1: Decompose

Break the feature into discrete, testable subtasks:

```markdown
## Feature: User Invitation System

### Subtasks:
1. Database schema for invitations (supabase-specialist)
2. RLS policies for invitation access (security-auditor)
3. API endpoints for invite CRUD (backend-engineer)
4. Email notification service (backend-engineer)
5. Invitation UI components (frontend-specialist)
6. Integration tests (quality-engineer)
```

**Requirements:**
- Each subtask is independently testable
- Clear inputs and outputs defined
- Dependencies between subtasks identified
- Estimated scope per subtask (small/medium/large)

## Step 2: Agent Selection

| Domain | Agent | When to Use |
|--------|-------|-------------|
| Database design | supabase-specialist | Schema, migrations, RLS |
| Security review | security-auditor | Auth, permissions, vulnerabilities |
| Backend logic | backend-engineer | APIs, server actions, integrations |
| Frontend UI | frontend-specialist | Components, forms, UX |
| Testing | quality-engineer | Unit, integration, E2E tests |
| Performance | performance-optimizer | Bundle, queries, Core Web Vitals |
| Research | deep-researcher | Documentation, patterns, analysis |
| Debugging | debugger-detective | Root cause analysis, tracing |

**Selection Criteria:**
- Match agent expertise to subtask domain
- Consider agent tool permissions
- Prefer specialists over generalists
- Use orchestrator for coordination-heavy tasks

## Step 3: Sequence Planning

**Dependency Chain Example:**

```
[1] Database Schema (supabase-specialist)
    ↓
[2] Security Policies (security-auditor) - depends on [1]
    ↓
[3] Backend APIs (backend-engineer) - depends on [1], [2]
    ↓
[4] Email Service (backend-engineer) - parallel with [3]
    ↓
[5] Frontend UI (frontend-specialist) - depends on [3]
    ↓
[6] Integration Tests (quality-engineer) - depends on [3], [4], [5]
```

**Sequencing Rules:**
- Database before API
- Security review before implementation
- Backend before frontend (for API contracts)
- Implementation before testing
- Parallelize independent subtasks

## Step 4: Delegation Protocol

**Task Tool Invocation Format:**

```markdown
Task: @[agent-name]

## Context
[Background information about the feature]

## Your Subtask
[Specific work to complete]

## Required Skills
Load skills: [skill-1], [skill-2]

## Inputs
[Data/files from previous subtasks]

## Expected Output
[Specific deliverables expected]

## Quality Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Handoff Instructions
[What to prepare for next agent]
```

**Delegation Rules:**
- Provide FULL context (don't assume agent knows background)
- Include all relevant file paths
- Specify exact skills to load
- Define clear success criteria
- Include handoff instructions for next agent

## Step 5: Result Aggregation

After each agent completes:

```markdown
## Subtask [N] Complete

### Agent: [agent-name]
### Status: SUCCESS | PARTIAL | BLOCKED

### Deliverables:
- [x] File created: /path/to/file.ts
- [x] Migration added: /path/to/migration.sql
- [ ] Documentation updated (pending)

### Key Decisions:
- Decision 1: Chose approach A because [reason]
- Decision 2: Used pattern B for [reason]

### Issues/Blockers:
- None | [Description of issue]

### Handoff Data:
[Information needed by subsequent agents]
```

**Aggregation Rules:**
- Document all deliverables with paths
- Record key architectural decisions
- Track any blockers or issues
- Prepare handoff data for next agent
- Update session file with progress

## Step 6: Final Verification

```markdown
## Feature Verification Checklist

### Functional
- [ ] All subtasks completed successfully
- [ ] Integration points working
- [ ] User flows tested end-to-end

### Quality
- [ ] Tests pass (unit, integration, E2E)
- [ ] No TypeScript errors
- [ ] Lint rules satisfied
- [ ] Security review passed

### Documentation
- [ ] API documentation updated
- [ ] Architecture decisions recorded
- [ ] README updated if needed
```

## Handoff Protocols

**Between Agents:**

```
Agent A → Agent B
├── Summary of completed work
├── Files created/modified (full paths)
├── Interfaces/types defined
├── Environment variables needed
└── Known constraints or decisions
```

**Back to Orchestrator:**

```
Agent → Orchestrator
├── Completion status
├── All deliverables listed
├── Issues encountered
├── Recommendations for next steps
└── Estimated impact on timeline
```

## Common Patterns

### Pattern: Security-First Feature

```
1. Research → Requirements
2. Security Audit → Risk assessment
3. Database → Schema with RLS
4. Security Review → Policy verification
5. Backend → Secure implementation
6. Frontend → Secure UI
7. Quality → Security tests
```

### Pattern: Performance-Critical Feature

```
1. Research → Best practices
2. Performance → Baseline metrics
3. Database → Optimized schema
4. Backend → Efficient queries
5. Frontend → Optimized rendering
6. Performance → Verification
7. Quality → Load tests
```

## Red Flags

- Skipping decomposition -> Unclear scope, missed dependencies
- Single agent for complex feature -> Missing expertise
- No handoff data -> Lost context between agents
- Skipping verification -> Integration failures
- Parallel when sequential needed -> Race conditions

## Decision Criteria

| Situation | Action |
|-----------|--------|
| Agent blocked | Document blocker, try alternative agent or approach |
| Subtask scope creep | Split into smaller subtasks, reassess |
| Integration failure | Invoke debugger-detective, trace boundaries |
| Performance issues | Add performance-optimizer to pipeline |

## Integration

**Pairs with:** dispatching-parallel-agents (for independent subtasks), verification (final check), session (complex workflows)
