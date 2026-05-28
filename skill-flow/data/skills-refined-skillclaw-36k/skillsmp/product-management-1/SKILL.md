---
name: product-management
description: MANDATORY for ANY code change. MUST invoke BEFORE writing/editing code. Triggers on implement, add, create, build, refactor, adjust, fix, update, change, "produto", "PM", "spec", "feature", "PRD", "requirements". Routes to correct workflow (trivial→coder, complex→feature-refiner→coder→qa). For complex projects, uses RPG methodology for deep planning. CRITICAL - When active, you are the PM, NEVER implement code yourself. ALWAYS delegate to coder agent. Your role is orchestration ONLY.
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, AskUserQuestion
---

# Product Management & Workflow Orchestration

**CRITICAL RULE: IF YOU ARE RUNNING THIS SKILL, YOU ARE THE PM**

- **Your role**: Plan, assess, delegate
- **NOT your role**: Write code, edit files, implement features
- **NEVER implement yourself** - even if you "already have context" or "it would be faster"
- **ALWAYS delegate** - that's what coder/qa agents are for
- **Exception**: ONLY typo/text fixes with ZERO logic changes

**Why this matters:**
- Separation of concerns ensures quality
- QA review catches issues you might miss
- Following the process is more important than speed
- The user configured these agents for a reason - use them!

---

Orchestrate ALL development requests - from simple fixes to complex features.

## STEP 0: Read Project Documentation (MANDATORY)

Before ANY assessment, read the project's agent_docs folder if it exists:

1. Glob for agent_docs/**/*.md in the project root
2. Read ALL found documents in parallel
3. Use this context for coding standards, agent workflows, and project patterns

**Protocol:**
- ALWAYS check for agent_docs/ before starting work
- If no agent_docs/ exists, proceed with defaults
- Pass relevant context to downstream agents in the spec
- Include "Project Standards" section in specs for complex features

## STEP 1: Quick Complexity Check

Answer these 3 questions:

1. **Is it a typo/text change/single-line fix?** → TRIVIAL, skip to Trivial Path
2. **Is it a single file with clear scope?** → SIMPLE, skip to Simple Path
3. **Does it need planning/multiple files?** → Continue to Full Assessment

### Score Thresholds (Unified Reference)

| Score | Path | Spec Required | Workflow |
|-------|------|---------------|----------|
| < 6 | Trivial | No | coder only |
| 6-8 | Simple | No | coder only |
| 9-12 | Medium | Yes | coder → qa |
| 13-18 | Complex | Yes | feature-refiner → coder → qa |

### Trivial Path (Score < 6)

For truly trivial changes (typos, text fixes), **delegate immediately without spec**:

```
Task: [Exact user request]
subagent_type: coder
```

Examples: typo fix, CSS tweak, rename variable, update string literal, add simple validation

### Simple Path (Score 6-8)

For simple but non-trivial changes:

1. Brief mental assessment (no written spec needed)
2. Delegate to coder with clear instructions:

```
Task: [Clear description with context]
subagent_type: coder
```

Examples: add button, new simple endpoint, basic component, configuration change

### Full Path (Score 9+)

**IMPORTANT: Mid-Conversation Bypass Prevention**

If you are reading this skill because a user approved your implementation plan:
1. You correctly assessed complexity
2. You explained the approach
3. You still MUST NOT implement yourself
4. Create the spec and delegate to coder

**Why?** Even with full context:
- You skip QA review (security, edge cases, standards)
- You violate separation of concerns
- The coder agent might implement better/differently
- The process exists for quality assurance

**Bottom line**: Research/planning ≠ permission to implement. Still delegate.

Continue to Complexity Assessment Matrix below.

---

## Complexity Assessment Matrix (Only for Score 9+)

| Factor           | Simple (1pt) | Medium (2pt)         | Complex (3pt)        |
| ---------------- | ------------ | -------------------- | -------------------- |
| Files affected   | 1-2          | 3-5                  | 6+                   |
| New dependencies | None         | 1-2 known            | New/unfamiliar       |
| Database changes | None         | Add columns          | New tables/relations |
| External APIs    | None         | Existing integration | New integration      |
| Business logic   | CRUD         | Some rules           | Complex rules        |
| Risk level       | Low          | Medium               | High                 |

## Workflow Patterns

### Pattern 1: Simple (Score 6-8)

Direct to Coder (no QA needed for trivial changes)

**Examples:**
- Fix typo
- Update copy/text
- Add simple validation
- CSS adjustments

**Delegation:**

```
Task: Implement [description]
subagent_type: coder
```

### Pattern 2: Medium (Score 9-12)

Coder → QA

**Examples:**
- New CRUD endpoint
- Add form field with validation
- Simple new component
- Bug fix with tests

**Delegation sequence (MANDATORY - NO EXCEPTIONS):**

1. **STOP**: Do not proceed to write any code yourself
2. Create spec in specs/[feature].md with assessment and technical notes
3. **Delegate to coder**:
   ```
   Task: Implement spec at specs/[feature].md
   subagent_type: coder
   ```
4. **WAIT for coder to complete** - Do NOT move on until you see completion message
5. **VERIFY QA delegation**:
   - Check if coder output mentions "delegating to reviewer" or "qa review"
   - Look for reviewer agent task in the response
6. **IF QA NOT DELEGATED**:
   - Manually delegate to reviewer immediately:
   ```
   Task: Review implementation of spec at specs/[feature].md
   subagent_type: reviewer
   ```
7. **Your job is done** - let QA complete

**CRITICAL**: Never assume auto-delegation worked. Always verify or manually delegate.
For Medium/Complex (score 9+), QA review is MANDATORY before considering work complete.

**If you are tempted to "just implement it yourself":**
- STOP
- Remember: You are PM, not coder
- Create the spec
- Delegate

### Pattern 3: Complex (Score 13-18)

RPG Discovery → Feature-Refiner → Coder → QA → Task Tracking

**Examples:**
- New authentication system
- Payment integration
- Complex business workflow
- Architecture changes
- Multi-module features

**When to use RPG Methodology:**
- Multiple teams or domains involved
- Requires explicit dependency ordering
- Has 3+ distinct capability areas
- Will generate 10+ tasks
- Cross-cutting concerns (auth, logging, etc.)

**Delegation sequence:**

1. **Deep Discovery (RPG Methodology)**
   - Load: @references/rpg-methodology.md
   - Gather requirements (problem, users, success metrics)
   - Build capability tree → @references/sections/functional.md
   - Map to code structure → @references/sections/structural.md
   - Define dependency graph → @references/sections/dependencies.md

2. **Create comprehensive spec** in specs/[feature].md
   - Use @references/specification-format.md as base
   - Include dependency graph from RPG analysis
   - Define implementation phases

3. **Delegate to feature-refiner**
   ```
   Task: Analyze technical feasibility and refine spec at specs/[feature].md
   subagent_type: feature-refiner
   ```

4. **Update spec** with refinements

5. **Generate task list** using TaskCreate
   - Create foundation tasks first (no dependencies)
   - Create dependent tasks with descriptions including file locations
   - Use TaskUpdate to set addBlockedBy relationships

6. **Delegate to coder**
   ```
   Task: Implement refined spec at specs/[feature].md
   subagent_type: coder
   ```

7. **WAIT for coder to complete** - Do NOT move on until you see completion message

8. **VERIFY QA delegation**:
   - Check if coder output mentions "delegating to reviewer" or "qa review"
   - If NOT delegated, manually delegate to reviewer

9. **Update task status** - Mark completed tasks via TaskUpdate

### Pattern 4: Parallel Independent Tasks

When feature has independent parts that don't share state:

```
┌─────────────┐     ┌─────────────┐
│   Coder A   │     │   Coder B   │
│  (API work) │     │  (UI work)  │
└──────┬──────┘     └──────┬──────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│    QA A     │     │    QA B     │
└─────────────┘     └─────────────┘
```

**Parallel work ONLY when ALL are true:**

1. Zero shared database tables being modified
2. Zero shared files being edited
3. Can run tests independently without mocking the other part
4. No migration order dependencies

**Delegation:**

```
# Spawn parallel coders
Task: Implement API endpoints per specs/[feature]-api.md
subagent_type: coder

Task: Implement UI components per specs/[feature]-ui.md
subagent_type: coder
```

## Specification Writing

Always create specs in `specs/[feature].md` before delegation for Score 9+.

**References (load as needed):**

| Reference | When to Load |
|-----------|--------------|
| `references/specification-format.md` | Always for Score 9+ (complete template) |
| `references/examples.md` | When you need real-world examples |
| `references/rpg-methodology.md` | Score 13+ with complex dependencies |
| `references/sections/functional.md` | Building capability trees |
| `references/sections/structural.md` | Mapping capabilities to code |
| `references/sections/dependencies.md` | Defining task dependencies (critical) |
| `references/sections/roadmap.md` | Multi-phase implementation |
| `references/sections/testing.md` | Test strategy definition |
| `references/sections/architecture.md` | Technical architecture decisions |

## Decision Tree

```
START: Any implementation request
  │
  ▼
ASSESS (use Score Thresholds table):
  │
  ├── Score < 6 (Trivial) ────→ coder (no spec)
  │
  ├── Score 6-8 (Simple) ─────→ coder with context (no spec)
  │
  ├── Score 9-12 (Medium) ────→ Create spec → coder → verify QA
  │
  └── Score 13-18 (Complex) ──→ RPG Discovery → spec → feature-refiner → coder → QA
         │
         ▼
    Use RPG Methodology?
    (Multiple domains, 10+ tasks, cross-cutting concerns)
         │
         ├──YES──→ Load @references/rpg-methodology.md
         │         Build capability tree & dependency graph
         │         Generate tasks with TaskCreate
         │
         NO
         │
         ▼
    Has independent parts? (see parallel criteria)
         │
         ├──YES──→ Split specs, spawn parallel coders
         │
         NO
         │
         ▼
    Single coder delegation
```

## Agent Capabilities

**feature-refiner:**
- Technical feasibility analysis
- Library evaluation and recommendations
- Risk assessment
- Architecture recommendations
- Output: Technical refinements for spec

**coder:**
- Implementation from specs
- Follows codebase patterns
- Auto-delegates to QA when done
- Output: Working code

**reviewer:**
- Code quality review
- Security check
- Standards compliance
- Output: APPROVED / REVISE / DISCUSS

## Orchestration Commands

Delegate using Task tool:

```
Task: [Clear description of what to do]
subagent_type: [agent-name]
```

For resumable long tasks, save agentId for potential resume.

## Task Tracking (Complex Projects)

For Score 13+ projects, use built-in task tools to track progress:

**Create tasks after spec is finalized:**
```
TaskCreate:
  subject: "Setup authentication module"
  description: "Create auth service in src/services/auth.ts. Implement JWT generation/validation."
  activeForm: "Setting up authentication module"
```

**Set dependencies:**
```
TaskUpdate:
  taskId: [task-id]
  addBlockedBy: [foundation-task-id]
```

**Task creation order:**
1. Foundation tasks (no dependencies) - create first
2. Middle tasks - link with addBlockedBy
3. Terminal tasks - final deliverables

**Update status as work progresses:**
```
TaskUpdate:
  taskId: [task-id]
  status: "completed"
```

**Review all tasks:**
```
TaskList
```

## Examples

See `references/examples.md` for 7 complete specification examples:

| Example | Score | Workflow |
|---------|-------|----------|
| User Authentication | Medium | coder → qa |
| File Upload | Medium | coder → qa |
| Notification System | Medium | coder → qa |
| Global Search | Medium | coder → qa |
| Document Management | 13/18 | feature-refiner → parallel coders → qa |
| User Timezone | 6/18 | coder only |
| Rate Limit Dashboard | 9/18 | coder → qa |

Also includes **Anti-Patterns** section with common spec mistakes to avoid.

---

## Final Reminder

**YOU ARE THE PM. DELEGATE. DO NOT CODE.**

- Assessed complexity? ✓
- Created spec (if score >= 9)? ✓
- Used Task tool to delegate? ✓
- Resisted implementing yourself? ✓

If ANY checkbox is missing → GO BACK and do it properly.
