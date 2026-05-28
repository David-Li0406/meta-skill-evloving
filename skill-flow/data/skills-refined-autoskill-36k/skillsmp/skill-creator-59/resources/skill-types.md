# Skill Types and Patterns

Classification and patterns for the three main skill types.

## Overview

| Type | Purpose | Duration | Complexity | Examples |
|------|---------|----------|------------|----------|
| **Workflow** | Automate multi-step processes | <1 min | Medium | sync-feature-branch, create-pull-request |
| **Specialist** | Domain expertise (USE SUBAGENTS) | Variable | High | Use Task tool with backend-engineer, security-engineer subagents |
| **Meta** | Operate on skill system | Variable | High | skill-creator, area-context-create |

## Workflow Skills

### Characteristics

- **Automate repetitive processes**
- **Multi-step (3-7 steps typically)**
- **Clear start and end**
- **Measurable time savings**

### Pattern

```
1. Check context (prerequisites, current state)
2. Gather information (Serena, Beads, git)
3. Execute core action (main workflow)
4. Validate results (quick checks)
5. Update state (commit, update Beads, confirm)
```

### When to Create

**Good fit:**
- Task takes >5 steps manually
- Repeated multiple times per day/week
- Clear success criteria
- Involves multiple systems (git, Beads, CI)

**Not a good fit:**
- Single-step operation (use bash command)
- Rarely used (<1x per week)
- Unclear success criteria
- Highly variable workflow

### Structure Template

```markdown
---
name: workflow-name
description: Automate [X process]. MUST BE USED when [trigger].
allowed-tools:
  - Bash(git:*)
  - mcp__plugin_beads_beads__*
  - mcp__serena__*
---

## Workflow

### 1. Check Context
Verify prerequisites, fail fast if missing

### 2. Gather Information
Use Serena/Beads/git to get current state

### 3. Execute Action
Core workflow steps (3-7 steps)

### 4. Validate Results
Quick checks (<5s), trust environments

### 5. Update State
Commit, update Beads, confirm to user

## Integration Points

### With Beads
- Check issue: show(issue_id)
- Update status: update(issue_id, status)
- Close on success: close(issue_id, reason)

### With Serena
- Search: search_for_pattern()
- Navigate: find_symbol()
- Edit: replace_symbol_body()

### With Git
- Check status: git status
- Make changes: git add, git commit
- Sync remote: git push
```

### Examples

**sync-feature-branch** (25s total):
```
1. Check Feature-Key exists in branch name
2. Verify Beads issue exists
3. Quick lint (<5s)
4. Git commit with Feature-Key trailer
5. Update Beads status to in_progress
```

**create-pull-request** (10s total):
```
1. Extract Feature-Key from branch
2. Check Beads issue exists (create if missing)
3. Push branch to remote
4. Create PR with gh CLI
5. Link PR to Beads issue
```

**fix-pr-feedback** (2min per issue):
```
1. Get PR context (number, comments, CI status)
2. Categorize discoveries (CI failure, review comment, etc.)
3. Create child Beads issues (bd-pso.1, bd-pso.2)
4. Fix simple issues automatically
5. Commit fixes with child Feature-Keys
6. Close child issues on success
```

## Specialist Skills

### Characteristics

- **Domain-specific expertise**
- **Deep knowledge in one area**
- **Complex decision-making**
- **Variable execution time**

### Pattern

```
1. Analyze request (understand scope, identify constraints)
2. Research context (read relevant code, check issues)
3. Execute with expertise (apply domain patterns)
4. Verify and document (test changes, update docs)
```

### When to Create

**Good fit:**
- Task requires deep domain knowledge
- Multiple patterns/best practices
- Complex trade-offs and decisions
- Specialized tools or APIs

**Not a good fit:**
- General-purpose task
- No special expertise needed
- Simple CRUD operations
- Already covered by workflow skill

### Structure Template

```markdown
---
name: specialist-name
description: [Domain] expertise for [area]. MUST BE USED for [domain tasks].
allowed-tools:
  - Domain-specific tools
  - mcp__serena__*
  - Bash(domain-cli:*)
---

## Purpose
Expertise domain and scope

## When to Use This Skill
Task patterns requiring this expertise

## Workflow

### 1. Analyze Request
Understand scope and constraints

### 2. Research Context
Read code, check related issues, review docs

### 3. Execute with Expertise
Apply domain-specific patterns and practices

### 4. Verify and Document
Test changes, update docs, create follow-ups

## Domain Knowledge
Key patterns, practices, and constraints for this domain

## Integration Points
Standard Beads/Serena/Git integration

## Best Practices
Domain-specific do's and don'ts
```

### Examples

**backend-engineer**:
```markdown
## Domain Knowledge
- FastAPI patterns (routers, dependencies, middleware)
- Database operations (Supabase, migrations)
- API design (REST, GraphQL endpoints)
- Data validation (Pydantic models)
- Testing (pytest, fixtures, mocks)

## Workflow
1. Analyze API requirements
2. Design endpoints and data models
3. Implement with FastAPI patterns
4. Write tests (unit + integration)
5. Update API documentation
```

**security-engineer**:
```markdown
## Domain Knowledge
- Authentication/authorization patterns
- Data encryption (at rest, in transit)
- Input validation and sanitization
- OWASP top 10 vulnerabilities
- Compliance (SOX, PCI-DSS, GDPR)

## Workflow
1. Identify security requirements
2. Analyze threat model
3. Implement security controls
4. Conduct security review
5. Document security decisions
```

**frontend-engineer**:
```markdown
## Domain Knowledge
- React patterns (hooks, context, composition)
- State management (Redux, Zustand)
- UI components (Material-UI)
- TypeScript interfaces and types
- Testing (Jest, React Testing Library)

## Workflow
1. Analyze UI requirements
2. Design component hierarchy
3. Implement with React patterns
4. Add TypeScript types
5. Write component tests
```

## Meta Skills

### Characteristics

- **Operate on the skill system itself**
- **Create or modify skills**
- **System-level changes**
- **High impact, used rarely**

### Pattern

```
1. Analyze system state (what exists, what's needed)
2. Design change (how to modify skill system)
3. Generate artifacts (new skills, updates)
4. Integrate (add to system, update docs)
5. Verify (test system still works)
```

### When to Create

**Good fit:**
- Automate skill creation/maintenance
- System-wide skill operations
- Skill discovery and analysis
- Meta-patterns across skills

**Not a good fit:**
- One-time skill creation (just create directly)
- Modifying single skill (use Edit tool)
- Non-skill system operations

### Structure Template

```markdown
---
name: meta-skill-name
description: Operate on skill system. Use when [meta-operation].
allowed-tools:
  - Read
  - Write
  - Edit
  - mcp__serena__*
---

## Purpose
What this changes about the skill system

## When to Use This Skill
Meta-operation patterns

## Workflow

### 1. Analyze System
Understand current skill system state

### 2. Design Change
Plan modifications to skill system

### 3. Generate Artifacts
Create/modify skills

### 4. Integrate
Add to system, update skill-rules.json, update docs

### 5. Verify
Test skill system still works

## Safety Guardrails
How to protect skill system integrity

## Integration Points
How this fits with existing skills
```

### Examples

**skill-creator** (this skill!):
```markdown
## Purpose
Create new skills following V3 patterns

## Workflow
1. Classify skill type (workflow/specialist/meta)
2. Gather requirements
3. Create skill structure
4. Generate content using templates
5. Add auto-activation rules
6. Update documentation
7. Test and commit
```

**skill-updater** (future):
```markdown
## Purpose
Update existing skills when patterns change

## Workflow
1. Identify outdated patterns in skills
2. Generate diffs to update to V3
3. Preview changes
4. Apply updates
5. Test affected skills
6. Commit with changelog
```

**skill-analyzer** (future):
```markdown
## Purpose
Analyze skill usage and effectiveness

## Workflow
1. Scan conversation transcripts
2. Identify skill invocations
3. Measure activation success rate
4. Report bottlenecks
5. Suggest improvements
```

## Choosing the Right Type

### Decision Tree

```
Is this a repetitive multi-step process?
├─ Yes → Workflow Skill
│  └─ Examples: commit, create PR, fix PR
└─ No → Continue

Does this require deep domain expertise?
├─ Yes → Specialist Skill
│  └─ Examples: backend, security, frontend
└─ No → Continue

Does this operate on the skill system itself?
├─ Yes → Meta Skill
│  └─ Examples: skill-creator, skill-updater
└─ No → Maybe not a skill? Consider bash command or tool
```

### Comparison Matrix

| Criteria | Workflow | Specialist | Meta |
|----------|----------|------------|------|
| **Automation focus** | High | Medium | High |
| **Domain knowledge** | Low | High | System-level |
| **Execution time** | Predictable | Variable | Variable |
| **Usage frequency** | Daily/weekly | As needed | Rare |
| **Complexity** | Medium | High | High |
| **Tool integration** | Heavy (git/Beads/Serena) | Medium | Light (file ops) |

## Hybrid Patterns

### Workflow + Specialist

Some skills combine automation with expertise:

**Example: database-migration skill**
```markdown
## Type: Workflow + Specialist

Automates migration workflow (workflow pattern)
+ Requires database expertise (specialist knowledge)

### Workflow
1. Check migration prerequisites
2. Design migration (specialist knowledge)
3. Generate migration files
4. Test in dev environment
5. Apply to staging/prod

### Domain Knowledge
- Schema design patterns
- Data integrity constraints
- Rollback strategies
- Performance considerations
```

### Workflow + Meta

Some skills automate system-level operations:

**Example: skill-creator (this skill!)**
```markdown
## Type: Workflow + Meta

Automates skill creation (workflow pattern)
+ Modifies skill system (meta operation)

### Workflow
1. Classify and gather requirements
2. Generate skill artifacts
3. Integrate with system
4. Test and commit

### Meta Operation
- Creates new skills
- Updates skill-rules.json
- Modifies CLAUDE.md
```

## Anti-Patterns

### ❌ Wrong Type Choice

**Problem:** Creating workflow skill for one-time operation
```markdown
# Bad: workflow skill for installing dependencies
name: install-dependencies
# This is a one-time setup, not a workflow!
```

**Solution:** Use bash command or document in setup guide

**Problem:** Creating specialist skill for simple CRUD
```markdown
# Bad: specialist skill for basic database queries
name: database-reader
# No special expertise needed for SELECT queries
```

**Solution:** Use Serena directly, or Task(subagent_type="backend-engineer") for complex work

### ❌ Type Confusion

**Problem:** Mixing workflow and specialist patterns
```markdown
# Bad: workflow that requires deep expertise at every step
1. Analyze security architecture (needs expertise)
2. Design threat model (needs expertise)
3. Implement controls (needs expertise)
4. Conduct audit (needs expertise)
```

**Solution:** This should use Task(subagent_type="security-engineer") subagent

### ❌ Over-Generalization

**Problem:** Creating "do everything" workflow skill
```markdown
# Bad: mega-skill
name: do-all-the-things
# Handles commits, PRs, fixes, deploys, etc.
```

**Solution:** Split into focused skills (one per workflow)

## Best Practices by Type

### Workflow Skills

✅ Clear entry/exit points
✅ 3-7 steps typically
✅ Measurable time (<1 min ideal)
✅ Heavy tool integration (git/Beads/Serena)
✅ Quick validation (<5s)

### Specialist Skills

✅ Document domain knowledge
✅ Show decision patterns
✅ Provide examples
✅ Reference best practices
✅ Link to authoritative sources

### Meta Skills

✅ Safety guardrails
✅ System state validation
✅ Rollback procedures
✅ Impact analysis
✅ Integration testing

---

**Related:**
- resources/v3-philosophy.md - Core principles
- resources/examples/ - Real skill examples
- CLAUDE.md - V3 workflow reference
