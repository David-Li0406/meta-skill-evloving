# Subagent Decision Guide

## Table of Contents

- [🚨 MANDATORY: Read BEFORE Using Subagents](#mandatory-read-before-using-subagents)
- [When to Use Subagents](#when-to-use-subagents)
- [Decision Matrix](#decision-matrix)
- [Context: Fork Scenarios (2026)](#context-fork-scenarios-2026)
- [Subagent Types](#subagent-types)
- [Subagent Invocation](#subagent-invocation)
- [Cost Considerations](#cost-considerations)
- [Common Patterns](#common-patterns)
- [When NOT to Use Subagents](#when-not-to-use-subagents)
- [Alternative Approaches](#alternative-approaches)
- [Decision Tree](#decision-tree)
- [Best Practices](#best-practices)
- [Next Steps](#next-steps)

Determine when to use subagents for specialized autonomous workers in Claude Code.

## 🚨 MANDATORY: Read BEFORE Using Subagents

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Official Subagents Guide**: https://code.claude.com/docs/en/sub-agents
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any subagent creation
  - **Content**: Agent coordination, state management, autonomy requirements
  - **Cache**: 15 minutes minimum

- **[MUST READ] Task Tool Documentation**: https://code.claude.com/docs/en/cli-reference
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before using Task tool to invoke subagents
  - **Content**: Task tool usage, subagent types, invocation patterns
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** without understanding when subagents are appropriate
- **MUST validate** need for isolation before using subagents
- **REQUIRED** to understand cost implications

## When to Use Subagents

### ✅ Use Subagents When
- Complex multi-step tasks requiring focus
- Need isolation from main conversation
- High-volume output (extensive grep, repo traversal)
- Noisy exploration that would clutter conversation
- Parallel execution needed
- Long-running tasks
- Domain-specific expertise required
- Context: fork scenarios (2026 best practice)

### ❌ Don't Use Subagents For
- Simple file operations (use Read, Grep, Glob)
- Direct file reads (use Read tool)
- Basic searches (use Grep, Glob)
- Single-step operations
- Tasks requiring conversation context
- User interaction workflows
- Quick lookups

## Decision Matrix

| Need                      | Use Subagent? | Alternative      |
| ------------------------- | ------------- | ---------------- |
| Complex codebase analysis | ✅ Yes         | Read/Grep        |
| Simple file read          | ❌ No          | Read tool        |
| High-volume grep          | ✅ Yes         | Grep tool        |
| Single file operation     | ❌ No          | Native tools     |
| Isolated context needed   | ✅ Yes         | Inline execution |
| User-interactive task     | ❌ No          | Regular workflow |

## Context: Fork Scenarios (2026)

Use `context: fork` when:

### High-Volume Output
- Extensive grep operations
- Full codebase traversal
- Large log file analysis
- Comprehensive audits

**Example**:
```yaml
---
name: codebase-audit
description: "Comprehensive codebase audit"
context: fork
agent: Explore
---
```

### Noisy Exploration
- Multi-file searches
- Deep code analysis
- Pattern discovery
- Architecture exploration

**Example**:
```yaml
---
name: pattern-discovery
description: "Discover architectural patterns"
context: fork
agent: Explore
---
```

### Isolation Benefits
- Separate context window
- No conversation clutter
- Dedicated computation
- Clean result handoff

### How Context: Fork Works

**CRITICAL MECHANISM**: Understanding the context: fork execution model:

In a context: fork Skill run, the forked subagent's system prompt comes from the chosen agent (built-in or custom), while the Skill's SKILL.md becomes the task prompt that drives that subagent. If the chosen custom subagent also has `skills:` configured, those Skills' full contents are also injected into that forked subagent's context at startup—they don't get "replaced" by the forked Skill; they sit alongside it.

**Key Points**:
1. **System Prompt**: Derived from the chosen agent type (Explore, Plan, Bash, general-purpose, or custom agent)
2. **Task Prompt**: The Skill's SKILL.md content drives what the subagent does
3. **Skills Injection**: If using a custom subagent with `skills:` configured, those Skills are loaded into the forked subagent's context at startup
4. **Additive, Not Replacement**: The forked Skill's SKILL.md doesn't replace the custom subagent's skills—they combine

**Example Flow**:
```yaml
---
name: codebase-audit
description: "Comprehensive codebase audit"
context: fork
agent: Explore
---

# SKILL.md content becomes task prompt
# Explore agent's system prompt remains base system
# All actions follow SKILL.md instructions
```

## Subagent Types

### 1. Explore Agent
**Purpose**: Fast agent specialized for exploring codebases

**Use When**:
- Quickly finding files by patterns
- Searching code for keywords
- Answering questions about codebase structure
- Comprehensive analysis across multiple locations

**Tools Available**:
- Read, Grep, Glob (file operations)
- NOT Task, Edit, Write, NotebookEdit

**Example**:
```yaml
---
name: code-search
description: "Search codebase for patterns"
context: fork
agent: Explore
---
```

### 2. Plan Agent
**Purpose**: Software architect agent for designing implementation plans

**Use When**:
- Planning implementation strategy
- Designing architecture
- Breaking down complex tasks
- Identifying critical files

**Tools Available**:
- All tools except Task, Edit, Write, NotebookEdit

**Example**:
```yaml
---
name: architecture-planner
description: "Plan software architecture"
context: fork
agent: Plan
---
```

### 3. General-Purpose Agent
**Purpose**: Full capabilities for any task

**Use When**:
- No specific specialization needed
- Complex multi-step workflows
- Research and execution combined

**Tools Available**:
- All tools (full access)

**Example**:
```yaml
---
name: complex-task
description: "Execute complex workflow"
context: fork
agent: general-purpose
---
```

### 4. Bash Agent
**Purpose**: Command execution specialist

**Use When**:
- Git operations
- Command execution
- Terminal tasks

**Tools Available**:
- Bash (command execution)

**Example**:
```yaml
---
name: git-specialist
description: "Handle git operations"
context: fork
agent: Bash
---
```

## Subagent Invocation

### Via Task Tool
```yaml
Task(
  subagent_type: Explore,
  prompt: "Analyze codebase...",
  description: "Analyze codebase structure"
)
```

### Via Skill
```yaml
---
name: my-analysis
description: "Complex analysis task"
context: fork
agent: Explore
---

Analyze $ARGUMENTS:
1. Find relevant files
2. Analyze code
3. Generate report
```

### Direct Invocation
User can invoke with `/my-analysis topic`

## Cost Considerations

### Token Usage
Subagents consume tokens for:
- New context window
- Agent initialization
- Task execution
- Result handoff

### Budget Targets (2026)
- **Target**: <$50 per 5-hour session
- **Warning**: >$75 per 5-hour session
- **Critical**: >$100 per 5-hour session

### Optimization Strategies
1. Use native tools when possible
2. Limit parallel subagent spawns
3. Keep tasks focused and specific
4. Use context: fork judiciously

## Common Patterns

### Pattern 1: Single Analysis
```yaml
---
name: security-audit
description: "Security audit of codebase"
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

1. Find security files
2. Search for vulnerabilities
3. Review authentication
4. Generate security report
```

### Pattern 2: Coordinated Workflow
```yaml
---
name: comprehensive-audit
description: "Full codebase audit"
context: fork
agent: Plan
---

1. Security audit (delegate to Explore)
2. Performance audit (delegate to Explore)
3. Quality audit (delegate to Explore)
4. Combine results
```

### Pattern 3: Parallel Execution
```yaml
# In Plan agent
Parallel execution:
- Task A: Frontend analysis (Explore)
- Task B: Backend analysis (Explore)
- Task C: Database analysis (Explore)
- Combine all results
```

## When NOT to Use Subagents

### Simple Operations
**Wrong**:
```yaml
# This is overkill
---
name: read-file
context: fork
agent: Explore
---

Read a single file...
```

**Right**:
```bash
# Use Read tool directly
Read file_path
```

### Interactive Tasks
**Wrong**:
```yaml
# User needs to guide this
---
name: interactive-task
context: fork
agent: Explore
---
```

**Right**:
```bash
# Handle inline
Ask user questions → Execute based on answers
```

### Quick Lookups
**Wrong**:
```yaml
# Wasteful subagent usage
---
name: find-variable
context: fork
agent: Explore
---

Find variable usage...
```

**Right**:
```bash
# Use Grep tool
Grep "variable_name" output_mode: files_with_matches
```

## Alternative Approaches

### Native Tools First
1. **File Operations**: Read, Edit, Write
2. **Search**: Grep, Glob
3. **Analysis**: Direct execution
4. **Bash Commands**: Direct execution

### Skills for Workflows
Use skills for:
- Complex workflows with multiple steps
- Domain expertise requirements
- Reusable capabilities
- Progressive disclosure needs

### Commands for Simple Wrappers
Use commands for:
- Bash script execution
- File operation wrappers
- Quick workflows
- User-triggered actions

## Decision Tree

```
START: What do you need?
│
├─ Simple file operation?
│  └─→ Use native tools (Read, Grep)
│
├─ Complex multi-step task?
│  ├─ Need isolation?
│  │  └─→ Use subagent
│  └─ Inline execution OK?
│     └─→ Use skill or inline
│
├─ High-volume output?
│  └─→ Use subagent (context: fork)
│
├─ Domain expertise?
│  └─→ Use skill (auto-discoverable)
│
└─ User-triggered workflow?
   └─→ Use command or skill with disable-model-invocation
```

## Best Practices

### DO ✅
- Use when isolation truly needed
- Choose appropriate agent type
- Keep tasks focused
- Consider cost implications
- Use context: fork judiciously
- Prefer native tools when possible

### DON'T ❌
- Don't use for simple operations
- Don't create unnecessary subagents
- Don't ignore cost considerations
- Don't use for user interaction
- Don't over-engineer solutions

## Next Steps

If subagents are appropriate:
- See **[coordination.md](coordination.md)** for coordination patterns
- Review **meta-architect-claudecode** for layer selection
- Consider if skills would be more appropriate
