---
name: master-workflow
description: Universal workflow wrapper that applies review-iterate-fix pattern to ANY skill with research, planning, implementation, and validation phases
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Skill
  - Task
  - TodoWrite
  - AskUserQuestion
---

# Master Workflow

**Purpose:** Universal workflow that applies the review-iterate-fix pattern to ANY skill or task.

## Universal Pattern

This workflow wraps ANY work in a 4-phase process with review loops:

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: RESEARCH           │
│   └─ [Execute] → [Review] → [Re-research if needed] (max 3x)   │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 2: PLANNING           │
│   └─ [Plan] → [Review] → [Revise if needed] (max 3x)           │
│       → [GET USER APPROVAL]                                       │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 3: IMPLEMENTATION    │
│   └─ [Implement] → [Review] → [Fix] → [Re-review] (max 3x)     │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 4: VALIDATION        │
│   └─ [Quality Gates] → [Fix failures] → [Retry] (max 2x)       │
└─────────────────────────────────────────────────────────────────┘
```

## When to Use

**Use this for EVERYTHING** except trivial one-line changes:

- Feature implementation (wrap /nestjs, /api-feature-cqrs)
- Research tasks (wrap Explore agents)
- Bug fixes (wrap /debugger)
- Refactoring (wrap /refactor)
- Code review (wrap /review itself!)

## How to Use

### Basic Usage

```
/master-workflow "Create user management with RBAC"
```

### With Specific Skill

```
/master-workflow --skill=nestjs "Implement product catalog"
/master-workflow --skill=refactor "Clean up auth module"
/master-workflow --skill=debugger "Fix login timeout issue"
```

### With Review Level

```
/master-workflow --review-level=quick "Fix typo in README"
/master-workflow --review-level=standard "Add new field to user"
/master-workflow --review-level=thorough "Implement payment system"
```

### Skip Quality Gates

```
/master-workflow --skip-tests "Update documentation"
/master-workflow --skip-lint "Quick prototype"
```

## Review Levels

| Level      | Scope                          | Max Iterations | Use For                    |
| ---------- | ------------------------------ | -------------- | -------------------------- |
| `quick`    | Critical only (security, bugs) | 1              | Trivial fixes, docs        |
| `standard` | Critical + warnings            | 2              | Normal features            |
| `thorough` | Everything                     | 3              | Complex, security-critical |

## Phase Details

### PHASE 1: RESEARCH (with review loop)

```
ITERATION 1:
├─ Execute research (Task with Explore, or read/analyze)
├─ Skill('review') - Review research for:
│  ├─ False positives (files don't exist)
│  ├─ Incomplete information (missing context)
│  ├─ Outdated patterns (old implementations)
│  └─ Incorrect conclusions
└─ If issues → ITERATION 2 (re-research with focus on gaps)

Maximum 3 research iterations before escalation
```

**Research Review Checklist:**

- [ ] All referenced files exist
- [ ] Patterns are actually used (not just defined)
- [ ] Findings cross-verified
- [ ] No outdated information
- [ ] Context is complete

### PHASE 2: PLANNING (with review loop)

```
ITERATION 1:
├─ Create implementation plan
├─ Skill('review') - Review plan for:
│  ├─ Completeness (all steps covered)
│  ├─ Feasibility (can it be done)
│  ├─ Architecture compliance (CQRS, multi-tenancy)
│  ├─ Security implications
│  └─ Performance considerations
└─ If issues → ITERATION 2 (revise plan)

Maximum 3 planning iterations before escalation
└─ GET USER APPROVAL before proceeding
```

**Plan Review Checklist:**

- [ ] All requirements addressed
- [ ] Dependencies identified
- [ ] Security considered
- [ ] Performance implications addressed
- [ ] Multi-tenancy compliant
- [ ] Test strategy included

### PHASE 3: IMPLEMENTATION (with review loop)

```
ITERATION 1:
├─ Execute implementation (Skill or manual)
├─ Skill('review') - Comprehensive code review
└─ If issues → ITERATION 2

ITERATION 2:
├─ Fix identified issues
├─ Skill('api-nestjs-reviewer') - Domain-specific review
└─ If issues → ITERATION 3

ITERATION 3 (Last):
├─ Fix remaining issues
├─ Skill('review') - Final verification
└─ If issues → ESCALATE

Maximum 3 fix iterations before escalation
```

**Implementation Review Checklist:**

- [ ] Code follows patterns (CQRS, DDD)
- [ ] No security vulnerabilities
- [ ] No performance issues
- [ ] Proper error handling
- [ ] Tests present
- [ ] Documentation complete

### PHASE 4: VALIDATION (with retry loop)

```
Quality Gates (run in parallel):
├─ pnpm nx lint api
├─ pnpm nx typecheck api
├─ pnpm nx test api (unless --skip-tests)
└─ Security scan (if applicable)

If any gate fails:
├─ Fix failures
└─ Retry (max 2 times)

After 2 failures → ESCALATE
```

## Escalation Rules

### When to Escalate

1. **3 iterations** reached in any phase
2. **Quality gate fails** 2 times
3. **User approval denied** in planning phase
4. **Critical blocker** encountered

### Escalation Format

```markdown
⚠️ Workflow Escalation: {PHASE_NAME}

**What I was doing:** {activity}

**Iterations:** {current}/{max}

**Remaining Issues:**
{numbered_list_with_severity}

**Why I can't continue:**
{specific_blocker}

**Your Options:**

1. Guide me - Tell me exactly what to do
2. Manual fix - Make changes yourself
3. Accept - Proceed with known issues
4. Different approach - Try alternative strategy
5. Stop - Abort this workflow

**What would you like to do?**
```

## Configuration

```yaml
config:
  # Research phase
  maxResearchIterations: 3

  # Planning phase
  maxPlanningIterations: 3
  requireUserApproval: true

  # Implementation phase
  maxImplementationIterations: 3

  # Validation phase
  maxValidationRetries: 2
  skipTests: false
  skipLint: false

  # Overall
  totalTimeoutMinutes: 15
  autoEscalate: true
```

## Example Workflow Traces

### Example 1: Simple Feature (Standard Review)

```
PHASE 1: RESEARCH
  ├─ Explore existing user management patterns ✓
  ├─ Review research: No issues ✓
  └─ Research complete (1 iteration)

PHASE 2: PLANNING
  ├─ Create plan for user CRUD ✓
  ├─ Review plan: Missing test strategy
  ├─ Revise plan: Add test strategy ✓
  ├─ Review plan: No issues ✓
  └─ User approval: GRANTED ✓

PHASE 3: IMPLEMENTATION
  ├─ Skill('api-feature-cqrs') for User ✓
  ├─ Review: Missing input validation
  ├─ Fix: Add validation decorators ✓
  ├─ Review: No issues ✓
  └─ Implementation complete (2 iterations)

PHASE 4: VALIDATION
  ├─ Lint: PASSED ✓
  ├─ Typecheck: PASSED ✓
  ├─ Tests: 1 failure
  ├─ Fix test assertion ✓
  ├─ Tests: PASSED ✓
  └─ Validation complete (1 retry)

✅ WORKFLOW COMPLETE
```

### Example 2: Escalation Scenario

```
PHASE 3: IMPLEMENTATION
  ├─ Skill('nestjs') for payment system ✓
  ├─ Review: Missing PCI compliance checks
  ├─ Fix: Add compliance validation
  ├─ Review: Unclear encryption method
  ├─ Fix: Specify AES-256
  ├─ Review: Need security expert review
  ├─ Cannot auto-fix - requires security expertise

⚠️ ESCALATION

Remaining Issues:
- [CRITICAL] Payment security requires expert review

Why I can't continue:
Security-critical code needs specialized expertise
beyond standard patterns.

Your Options:
1. Guide me - Tell me the security requirements
2. Manual fix - Add security code yourself
3. Defer - Skip payment processing for now
```

## Related Skills

- `nestjs` - NestJS-specific workflow
- `orchestrator` - General-purpose coordination
- `review` - Comprehensive code review

## Workflow Files

- `.claude/workflows/universal-review-loop.yaml` - Full workflow definition
- `.claude/workflows/implementation-review.yaml` - Implementation-specific
