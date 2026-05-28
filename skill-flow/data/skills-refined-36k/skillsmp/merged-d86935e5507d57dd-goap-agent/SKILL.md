---
name: goap-agent
description: Use this skill for complex multi-step tasks requiring intelligent planning and multi-agent coordination, including decomposition, dependency mapping, and execution strategies with quality gates.
---

# GOAP Agent Skill: Goal-Oriented Action Planning

Enable intelligent planning and execution of complex multi-step tasks through systematic decomposition, dependency mapping, and coordinated multi-agent execution.

## Quick Reference

- **[Methodology](methodology.md)** - Core GOAP planning cycle and phases
- **[Skills Reference](skills.md)** - Available skills by category
- **[Agents Reference](agents.md)** - Available task agents and capabilities
- **[Patterns](patterns.md)** - Common GOAP execution patterns
- **[Examples](examples.md)** - Complete GOAP workflow examples

## When to Use

Use this skill when facing:

- **Complex Multi-Step Tasks**: Tasks requiring 5+ distinct steps or multiple specialized capabilities
- **Cross-Domain Problems**: Issues spanning multiple areas (storage, API, testing, documentation)
- **Optimization Opportunities**: Tasks that could benefit from parallel or hybrid execution
- **Quality-Critical Work**: Projects requiring validation checkpoints and quality gates
- **Resource-Intensive Operations**: Large refactors, migrations, or architectural changes
- **Ambiguous Requirements**: Tasks needing structured analysis before execution

## CRITICAL: Understanding Skills vs Task Agents

**Skills** (invoked via `Skill` tool): Instruction sets that guide Claude directly. They provide specialized knowledge and workflows.

**How to invoke**: `Skill(command="skill-name")`

**When to use**:
- Need specialized knowledge/workflow guidance
- Task requires deep domain expertise (Rust quality, architecture validation)
- Want to follow a proven methodology

**Task Agents** (invoked via `Task` tool): Autonomous sub-processes that execute tasks independently using tools.

**How to invoke**: `Task(subagent_type="agent-name", prompt="...", description="...")`

**When to use**:
- Need autonomous task execution
- Task requires tool usage (Read, Edit, Bash, etc.)
- Want parallel/independent execution

### Common Error to Avoid

**WRONG**: `Task(subagent_type="rust-code-quality", ...)` → ERROR! rust-code-quality is a Skill!

**CORRECT**: `Skill(command="rust-code-quality")` → SUCCESS

## Core GOAP Methodology

### The GOAP Planning Cycle

```
1. ANALYZE → Understand goals, constraints, resources
2. DECOMPOSE → Break into atomic tasks with dependencies
3. STRATEGIZE → Choose execution pattern (parallel/sequential/swarm/hybrid/iterative)
4. COORDINATE → Assign tasks to specialized agents
5. EXECUTE → Run with monitoring and quality gates
6. SYNTHESIZE → Aggregate results and validate success
```

## Phase 1: Task Analysis

### Initial Assessment

```markdown
## Task Analysis

**Primary Goal**: [Clear statement of what success looks like]

**Constraints**:
- Time: [Urgent / Normal / Flexible]
- Resources: [Available agents, tools, data]
- Dependencies: [External systems, prerequisites]

**Complexity Level**:
- Simple: Single agent, <3 steps
- Medium: 2-3 agents, some dependencies
- Complex: 4+ agents, mixed execution modes
- Very Complex: Multiple phases, many dependencies

**Quality Requirements**:
- Testing: [Unit / Integration / E2E]
- Standards: [AGENTS.md compliance, formatting, linting]
- Documentation: [API docs, examples, guides]
- Performance: [Speed, memory, scalability]
```

### Context Gathering

1. **Codebase Understanding**: Use Explore agent to understand relevant code
2. **Past Patterns**: Check if similar tasks have been done before
3. **Available Resources**: Identify available agents and their capabilities
4. **Current State**: Understand starting conditions and existing implementations

## Phase 2: Task Decomposition

Use the **task-decomposition** skill to break down the goal:

```markdown
## Task Decomposition: [Task Name]

### Main Goal
[Clear statement of primary objective]

### Sub-Goals
1. [Component 1] - Priority: P0
   - Success Criteria: [How to verify]
   - Dependencies: [Prerequisites]
   - Complexity: [Low/Medium/High]

2. [Component 2] - Priority: P1
   - Success Criteria: [How to verify]
   - Dependencies: [Component 1]
   - Complexity: [Low/Medium/High]

### Atomic Tasks
**Component 1: [Name]**
- Task 1.1: [Action] (Agent: type, Deps: none)
- Task 1.2: [Action] (Agent: type, Deps: 1.1)

### Dependency Graph
```
Task 1.1 → Task 1.2 → Task 2.1
                  ↘
Task 1.3 (parallel) → Task 2.2
```
```

### Key Decomposition Principles
- **Atomic**: Each task is indivisible and clear
- **Testable**: Can verify completion
- **Independent where possible**: Minimize dependencies
- **Assigned**: Each task maps to an agent capability

## Phase 3: Strategy Selection

Choose execution strategy based on task characteristics. See the GOAP Agent documentation for detailed execution patterns.

### Quick Strategy Guide

| Strategy | When to Use | Speed | Complexity |
|----------|-------------|-------|------------|
| **Parallel** | Independent tasks, time-critical | Nx | High |
| **Sequential** | Dependent tasks, order matters | 1x | Low |
| **Swarm** | Many similar tasks | ~Nx | Medium |
| **Hybrid** | Mixed requirements | 2-4x | Very High |
| **Iterative** | Progressive refinement, convergence | Varies | Medium |

### Decision Tree
```
Needs iterative refinement?
  ├─ Yes (until criteria met or converged) → ITERATIVE
  └─ No → Is time critical?
      ├─ Yes → Can tasks run in parallel?
      │   ├─ Yes → PARALLEL
      │   └─ No → SEQUENTIAL (prioritize critical path)
      └─ No → Are tasks similar?
          ├─ Yes (many similar) → SWARM
          ├─ No (mixed) → HYBRID
          └─ Simple linear → SEQUENTIAL
```

## Phase 4: Agent Assignment

### Agent Capability Matrix

| Agent Type | Capabilities | Tools Available | Best For |
|------------|--------------|-----------------|----------|
| **feature-implementer** | Design, implement, test, integrate features | Read, Write, Edit, Bash, Glob, Grep | New functionality, modules, APIs |
| **debugger** | Diagnose runtime issues, async problems | Read, Bash, Grep, Edit | Bug fixes, deadlocks, performance |
| **test-runner** | Execute tests, diagnose failures | Bash, Read, Grep, Edit | Test validation, debugging tests |
| **refactorer** | Improve structure, eliminate duplication | Read, Edit, Bash, Grep, Glob | Code quality, modernization |
| **code-reviewer** | Review quality, standards, security | Read, Glob, Grep, Bash | Quality assurance, pre-commit |
| **loop-agent** | Iterative refinement, convergence | Task, Read, TodoWrite, Glob, Grep | Progressive improvements, test-fix loops |
| **agent-creator** | Create new Task Agents | Write, Read, Glob, Grep, Edit | Building new autonomous capabilities |
| **Explore** | Fast codebase exploration | All tools | Finding files, understanding architecture |
| **memory-cli** | CLI development and testing | Read, Write, Edit, Bash, Glob, Grep | Memory CLI features and fixes |

### Assignment Principles
1. Match agent capabilities to task requirements
2. Balance workload across agents
3. Consider agent specialization
4. Plan for quality validation

## Phase 5: Execution Planning

### Create the Execution Plan

```markdown
## Execution Plan: [Task Name]

### Overview
- Strategy: [Parallel/Sequential/Swarm/Hybrid/Iterative]
- Total Tasks: [N]
- Estimated Duration: [Time]
- Quality Gates: [N checkpoints]

### Phase 1: [Phase Name]
**Tasks**:
- Task 1: [Description] (Agent: type)
- Task 2: [Description] (Agent: type)

**Quality Gate**: [Validation criteria]

### Phase 2: [Phase Name]
**Tasks**:
- Task 3: [Description] (Agent: type)

**Quality Gate**: [Validation criteria]

### Overall Success Criteria
- [ ] All tasks complete
- [ ] Quality gates passed
- [ ] Tests passing
- [ ] Documentation updated

### Contingency Plans
- If Phase 1 fails → [Recovery plan]
- If tests fail → [Diagnostic approach]
```

## Phase 6: Coordinated Execution

### Parallel Execution

```markdown
**Launching parallel agents:**
- Agent 1 (feature-implementer) → Task A
- Agent 2 (feature-implementer) → Task B
- Agent 3 (test-runner) → Task C

**Coordination**:
- All agents work simultaneously
- Monitor progress independently
- Aggregate results when all complete
```

### Sequential Execution

```markdown
**Launching sequential agents:**
Phase 1: Agent 1 (debugger) → Diagnose issue
  ↓ Quality Gate: Root cause identified
Phase 2: Agent 2 (refactorer) → Apply fix
  ↓ Quality Gate: Tests pass
Phase 3: Agent 3 (code-reviewer) → Validate
```

### Monitoring During Execution
- Track agent progress
- Monitor for failures
- Validate intermediate results
- Adjust plan if needed

### Atomic Git Commit Policy
After each successful todo completion, create an atomic git commit:
- **Commit only the changes** for that specific todo item
- Use descriptive commit messages following `[module] description` format
- Do NOT commit changes from incomplete todos
- This ensures incremental, reversible progress tracking
- Example: `feat(storage): add episode creation method`

## Phase 7: Result Synthesis

### Aggregate Results

```markdown
## Execution Summary: [Task Name]

### ✓ Completed Tasks
- [Task 1]: Success
- [Task 2]: Success

### 📦 Deliverables
- [File/Feature 1]
- [File/Feature 2]

### ✅ Quality Validation
- Tests: [Pass/Fail] ([coverage]%)
- Linting: [Pass/Fail]
- Standards: [Compliant]

### 📊 Performance Metrics
- Duration: [actual vs estimated]
- Efficiency: [parallel speedup if applicable]

### 💡 Recommendations
- [Improvement 1]
- [Improvement 2]

### 🎓 Lessons Learned
- [What worked well]
- [What to improve]
```

## Integration with Self-Learning Memory

GOAP coordination tasks can be tracked as learning episodes to improve future planning decisions.

### Starting a GOAP Episode

```markdown
**Use**: Skill(command="episode-start")

**TaskContext**:
- language: "coordination"
- domain: "goap"
- tags: ["multi-agent", "parallel", "sequential", etc.]

**Description**: "GOAP coordination for [task description]"
```

### Logging GOAP Steps

```markdown
**Use**: Skill(command="episode-log-steps")

**Log during**:
- Decomposition decisions (how goals were broken down)
- Agent assignments (which agents chosen for which tasks)
- Strategy selection (why parallel vs sequential vs swarm)
- Quality gate results (pass/fail and why)
- Recovery actions (how failures were handled)
```

### Completing a GOAP Episode

```markdown
**Use**: Skill(command="episode-complete")

**Score based on**:
- Goal achievement (all tasks completed?)
- Efficiency (parallel speedup, resource utilization)
- Quality (all quality gates passed?)
- Adaptability (how well recovered from failures?)

**Patterns extracted**:
- Successful decomposition strategies
- Effective agent assignments
- Optimal execution patterns
- Quality gate effectiveness
```

### Retrieving Past GOAP Context

```markdown
**Use**: Skill(command="context-retrieval")

**Query for**:
- Similar coordination tasks
- Past parallel/sequential decisions
- Agent assignment patterns
- Quality gate strategies

**Apply learnings**:
- Reuse successful decompositions
- Avoid past mistakes
- Apply proven strategies
- Optimize based on history
```

### Example: Learning-Enabled GOAP

```markdown
Task: Implement authentication system

Phase 0: Retrieve Context
└─ Skill(command="context-retrieval")
   Query: "authentication implementation coordination"
   → Found: 3 past auth implementations
   → Pattern: Parallel (model + middleware + endpoints) worked well
   → Lesson: Sequential integration after parallel build

Phase 1: Start Episode
└─ Skill(command="episode-start")
   Context: {domain: "goap", tags: ["auth", "parallel"]}

Phase 2-N: Execute with logging
└─ Skill(command="episode-log-steps")
   Log each: decomposition, assignment, quality gate

Phase Final: Complete Episode
└─ Skill(command="episode-complete")
   Score: High (reused successful pattern)
   Pattern: Confirmed parallel → sequential integration strategy
```

## Dynamic Capability Creation

When existing Skills and Agents are insufficient, create new capabilities dynamically.

### When to Create New Skills

**Create Skill when**:
- Recurring workflow pattern identified
- Deep domain knowledge needed
- Reusable methodology discovered
- No existing Skill covers the domain

**Examples**:
- Custom quality standards for your domain
- Specialized testing workflows
- Domain-specific architecture patterns
- Project-specific best practices

**How to create**:
```markdown
Use: Skill(command="skill-creator")

Provide:
- Skill name and description
- When to use this skill
- Step-by-step methodology
- Examples and patterns
- Integration points
```

### When to Create New Agents

**Create Agent when**:
- New autonomous execution capability needed
- Specialized tool usage pattern required
- Cross-cutting concern needs dedicated agent
- Complex multi-step execution to automate

**Examples**:
- Custom deployment agent
- Specialized migration agent
- Domain-specific analyzer agent
- Project-specific workflow agent

**How to create**:
```markdown
Use: Task(subagent_type="agent-creator", ...)

Or use: Skill(command="skill-creator") for agent definition

Provide:
- Agent purpose and capabilities
- Tools the agent needs
- Input/output specification
- Success criteria
```

### Update GOAP Knowledge

After creating new capabilities:

1. **Document in GOAP**:
   - Add to Skills or Agents list
   - Update capability matrix
   - Add to phase-specific recommendations

2. **Test the capability**:
   - Use in real scenario
   - Validate effectiveness
   - Refine as needed

3. **Share the pattern**:
   - Document in project
   - Add examples
   - Enable reuse

### Example: Creating Custom Capability

```markdown
Problem: Need specialized security audit for authentication code

Step 1: Identify gap
→ No existing Skill covers auth security audit specifically

Step 2: Create Skill
└─ Skill(command="skill-creator")
   Name: "auth-security-audit"
   Purpose: "Audit authentication code for security vulnerabilities"
   Methodology: [OWASP auth checklist, crypto review, token validation, ...]

Step 3: Integrate into GOAP
→ Add to Quality & Validation Skills
→ Add to Phase 3 and Phase 7 recommendations
→ Document in project CLAUDE.md

Step 4: Use in workflow
└─ Phase 3: Skill(command="auth-security-audit")
   → Validates auth design before implementation
```

## Common GOAP Patterns

### Pattern 1: Research → Decide → Implement → Validate (Full Stack)

```markdown
Task: Implement complex feature with architectural impact

Phase 0: Retrieve Context [Skills]
├─ Skill(command="context-retrieval")
│  Query: "similar feature implementations"
│  → Apply past learnings
└─ Skill(command="episode-start")
   → Start tracking this coordination

Phase 1: Research [