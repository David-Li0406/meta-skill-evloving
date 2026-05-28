# Advanced Patterns

## Table of Contents

- [When to Use Rules (vs Commands/Skills)](#when-to-use-rules-vs-commandsskills)
- [File Locations](#file-locations)
- [Core Structure Template](#core-structure-template)
- [Project Context](#project-context)
- [Coding Standards](#coding-standards)
- [Architecture Principles](#architecture-principles)
- [Safety Boundaries](#safety-boundaries)
- [Tool Preferences](#tool-preferences)
- [Key Principles](#key-principles)
- [File Organization](#file-organization)
- [Safety Boundaries](#safety-boundaries)
- [Common Patterns](#common-patterns)
- [Component Structure](#component-structure)
- [Preferred Commands](#preferred-commands)
- [Module Boundaries](#module-boundaries)
- [Evolution Strategy](#evolution-strategy)
- [Anti-Patterns](#anti-patterns)
- [Quality](#quality)
- [Code Quality](#code-quality)
- [Quick Validation Checklist](#quick-validation-checklist)
- [When to Use Commands (vs Skills)](#when-to-use-commands-vs-skills)
- [Command Structure](#command-structure)
- [Dynamic Context with `!` Syntax](#dynamic-context-with-syntax)
- [Argument Patterns](#argument-patterns)
- [Examples](#examples)
- [Step 1: Read Files](#step-1-read-files)
- [Step 2: Check Patterns](#step-2-check-patterns)
- [Step 3: Report Findings](#step-3-report-findings)
- [Best Practices](#best-practices)
- [Step 1: Validate](#step-1-validate)
- [Step 2: Build](#step-2-build)
- [Step 3: Deploy](#step-3-deploy)
- [If Build Fails](#if-build-fails)
- [If Deploy Fails](#if-deploy-fails)
- [Anti-Patterns](#anti-patterns)
- [Command + Skill Pattern](#command-skill-pattern)
- [Activate Skill](#activate-skill)
- [Execute Refactor](#execute-refactor)
- [Quick Validation Checklist](#quick-validation-checklist)
- [When to Use Subagents](#when-to-use-subagents)
- [Built-in Subagent Types](#built-in-subagent-types)
- [Coordination Patterns](#coordination-patterns)
- [Key Principles](#key-principles)
- [Best Practices](#best-practices)
- [Anti-Patterns](#anti-patterns)
- [When to Use Each Type](#when-to-use-each-type)
- [Quick Validation Checklist](#quick-validation-checklist)

> Reference for advanced customization layers: CLAUDE.md rules, slash commands, and subagents. For core principles, see [common.md](common.md). For layer selection, see [layer-selection.md](layer-selection.md).

> **Note**: Commands and subagents are optional enhancements. Most customization needs are met by CLAUDE.md + Skills.

---

# CLAUDE.md Rules

## When to Use Rules (vs Commands/Skills)

**Use rules when:**
- You need persistent project norms that **always apply**
- You want to establish coding standards or conventions
- You have safety boundaries or security requirements
- You need to override global behavior for this project

**Rules vs other layers:**
| Use Case | Layer | Why |
|----------|-------|-----|
| Project-wide coding standards | Rules | Always active, no discovery needed |
| Domain expertise to discover | Skill | Auto-discovery, progressive disclosure |
| Explicit workflow I trigger | Command | Manual control, strict tool constraints |
| Noisy exploration tasks | Subagent | Output isolation, separate context |

## File Locations

| Location | Scope | Use For |
|----------|-------|---------|
| `~/.claude/CLAUDE.md` | Global | Personal preferences across all projects |
| `{project}/CLAUDE.md` | Project | Project-specific norms and standards |
| `{project}/.claude/rules/*.md` | Module | Modular rule sets |

**Hierarchy**: Global → Project → Module (later scopes override earlier)

## Core Structure Template

```markdown
# Project Rules

## Project Context
[Brief description of project type, tech stack, goals]

## Coding Standards
- [Specific conventions, not vague "clean code"]
- [Framework-specific patterns]
- [File organization rules]

## Architecture Principles
- [Design patterns to follow]
- [Anti-patterns to avoid]
- [Module boundaries]

## Safety Boundaries
- [Files/directories to never modify]
- [Operations requiring confirmation]
- [Security considerations]

## Tool Preferences
- [Preferred commands/tools]
- [Testing requirements]
- [Build/deployment workflows]
```

## Key Principles

### 1. Specificity

**Bad**: "Write clean code"
**Good**: "Use functional components with hooks; avoid class components"

**Bad**: "Follow best practices"
**Good**: "Always define PropTypes for components; use TypeScript for new files"

### 2. Context

Explain the **why** behind rules:

```markdown
## File Organization
Components go in `src/components/` because:
- Keeps UI code isolated from business logic
- Enables easier component reuse
- Matches our import path conventions
```

### 3. Actionability

Rules should be **enforceable**:

**Bad**: "Be careful with dependencies"
**Good**: "Never add dependencies without team approval; check existing libs first"

### 4. Safety

Define **clear boundaries**:

```markdown
## Safety Boundaries
- NEVER modify files in `legacy/` without explicit confirmation
- ALWAYS run tests before committing
- ALWAYS backup database before migrations
```

## Common Patterns

### Pattern 1: Example-Driven Rules

```markdown
## Component Structure

**Good:**
```tsx
function UserProfile({ userId }: Props) {
  const data = useUserData(userId);
  return <div>{data.name}</div>;
}
```

**Bad:**
```tsx
class UserProfile extends Component {
  // ...
}
```
```

### Pattern 2: Command Reference

```markdown
## Preferred Commands

**Linting**: `bun run lint` (not `npm run lint`)
**Testing**: `bun test` (not `vitest` directly)
**Building**: `bun run build` (uses esbuild)
```

### Pattern 3: Boundary Definition

```markdown
## Module Boundaries

**UI Layer** (`src/components/`): Can import from `src/lib/`
**Business Logic** (`src/lib/`): Cannot import from components
**Data Layer** (`src/api/`): No imports from UI layers
```

## Evolution Strategy

**Start lean, add iteratively:**

1. **V1**: Core coding standards (5-10 rules)
2. **V2**: Add architecture principles after patterns emerge
3. **V3**: Add safety boundaries based on failures
4. **V4**: Refactor to modular rules if growing large

**When to modularize:**
- CLAUDE.md exceeds 500 lines
- Distinct rule domains emerge (e.g., testing vs deployment)
- Multiple developers need separate rule domains

## Anti-Patterns

### Anti-Pattern 1: Vague Rules

**Bad**:
```markdown
## Quality
- Write clean code
- Follow best practices
- Be careful with bugs
```

**Good**:
```markdown
## Code Quality
- Use functional components with hooks
- Define PropTypes or use TypeScript
- Keep components under 300 lines
- Extract reusable logic to custom hooks
```

### Anti-Pattern 2: Over-Prescriptive Style

**Bad**: Dictating indentation, spacing, minor style details

**Good**: Focus on **behavioral** rules, not cosmetic preferences

**Rationale**: Let formatters (Prettier) handle style; rules should govern behavior.

### Anti-Pattern 3: Static Documentation

**Bad**: Treating CLAUDE.md like README.md with project docs

**Good**: CLAUDE.md is **active configuration**, not passive documentation

**Rationale**: Rules directly impact AI behavior. Keep docs separate.

### Anti-Pattern 4: Global Capture

**Bad**: Putting project-specific rules in global `~/.claude/CLAUDE.md`

**Good**: Global rules should be **truly universal** preferences

### Anti-Pattern 5: Linear Chain Brittleness

**Bad**: A -> B -> C -> D (for reasoning tasks) where C depends on B's specific output format.

**Good**: Hub -> A; Hub -> B; Hub -> C. The Hub validates and routes, handling errors if B fails.

## Quick Validation Checklist

- [ ] Rules are specific, not vague
- [ ] Rules include context/why
- [ ] Rules are actionable/enforceable
- [ ] Safety boundaries are clearly defined
- [ ] No style over-prescription (let formatters handle)
- [ ] File is lean (<500 lines ideally)
- [ ] Rules are behavioral, not documentary
- [ ] Global rules are truly universal

---

# Slash Commands

## When to Use Commands (vs Skills)

**Use commands when:**
- You want **explicit user control** over workflow triggering
- The workflow should have **strict tool controls** via `allowed-tools`
- You want to bundle **hooks** (pre/post execution)
- You **don't need** Claude to discover it automatically

**Commands vs Skills:**
| Factor | Choose Command | Choose Skill |
|--------|---------------|--------------|
| Discovery | No (manual only) | Yes (auto-discovery) |
| Tool control | Strict `allowed-tools` | Guidance only |
| Trigger | Manual `/command` | Auto + manual |
| Hooks | Pre/post execution | Via system hooks |
| Use case | User-controlled workflows | Domain expertise |

**Anti-pattern**: Creating a command when a skill would suffice (you lose auto-discovery).

### Command Creation Criteria

**Create slash command if at least ONE is true**:

| Criterion | Examples | Rationale |
|-----------|----------|-----------|
| **User control required** | Deployments, releases, migrations, destructive ops | User should explicitly trigger |
| **Tool constraints strict** | Read-only review, audit, validation | Minimal `allowed-tools` for safety |
| **Stable entrypoint needed** | "Run tests", "Build", "Deploy to prod" | Team-triggered workflow button |
| **Operation is costly/long** | Full repo audit, large data processing | User awareness of cost/duration |

**Best Practice**: Command as "thin wrapper" that activates a Skill:
```markdown
---
name: deploy
description: Deploys application with validation. Use for production deployments.
allowed-tools: Bash Read
context: server
---

# Deploy Workflow

**Loading deployment expertise skill...**

Following deployment patterns with validation gates.
```

This gives: explicit control (command) + discoverable expertise (skill) + progressive disclosure (skill references).

**Autonomy Escalation**: When a Skill identifies that explicit control is needed, it should recommend creating a command.

## Command Structure

### Frontmatter

```yaml
---
name: refactor
description: Refactors code using project-specific patterns to improve maintainability and readability.
allowed-tools: Read Edit Grep Glob
disallowed-tools: Bash Write
context: server
---

# Command content...
```

### Required Fields

**`name`**: Command identifier (lowercase, hyphens)
- Max 64 characters
- Must match filename: `refactor.md` → `name: refactor`
- Use gerund/active form: `refactoring`, `deploying`, `validating`

**`description`**: What + when + negative constraint
- Format: `"{{CAPABILITY}}. Use when {{TRIGGERS}}."`
- Include specific trigger keywords
- Mention exclusions

### Optional Fields

**`allowed-tools`**: Space-delimited tool allowlist
- Restricts which tools command can use
- Example: `allowed-tools: Read Edit Grep`

**`disallowed-tools`**: Tool denylist
- Explicitly forbids specific tools
- Example: `disallowed-tools: Bash Write`

**`context`**: Execution context
- `client` (default): Runs on client-side
- `server`: Requires server execution

## Dynamic Context with `!` Syntax

Commands can inject dynamic context using the `!` prefix:

```yaml
---
name: inspect
description: Inspects the current file or selection.
---
```

**Usage**: `/inspect` → automatically includes current file/selection

**Available dynamic variables**:
- `!` : Current file/selection
- `!{file}` : Specific file path
- `!{selection}` : Current selection only

## Argument Patterns

### Pattern 1: No Arguments

```yaml
---
name: status
description: Shows git status and recent commits.
---
```

**Usage**: `/status`

### Pattern 2: Single Argument

```yaml
---
name: test
description: Runs tests for specified package. Use with package name.
---

# Usage: /test @package-name
```

**Usage**: `/test @auth-service`

### Pattern 3: Multiple Arguments

```yaml
---
name: migrate
description: Runs database migration with direction. Use: /migrate [up|down] [version]
---

# Direction: {{0}}
# Version: {{1}}
```

**Usage**: `/migrate up 001`

## Examples

### Example 1: Simple Command

```markdown
---
name: format
description: Formats code using project formatter. Use when cleaning up code style.
---

Run formatter:
```bash
bun run format
```

Verify no files changed.
```

### Example 2: Command with Arguments

```markdown
---
name: test
description: Runs tests for specified package or all. Use: /test [@package-name]
---

# Test Workflow

{{0 ? "## Testing: " + {{0}} : "## Testing all packages"}}

{{0 ? "bun test " + {{0}} : "bun test"}}
```

### Example 3: Command with Tool Control

```markdown
---
name: review
description: Reviews code for issues and patterns. Use when checking code quality.
allowed-tools: Read Grep Glob
disallowed-tools: Write Bash
---

# Code Review

## Step 1: Read Files
Read all files in scope.

## Step 2: Check Patterns
Run pattern checks...

## Step 3: Report Findings
List issues found, grouped by severity.
```

### Example 4: Command with Hooks

```markdown
---
name: deploy
description: Deploys application with validation. Use for production deployments.
allowed-tools: Bash Read
hooks:
  preToolUse:
    - shell: |
        # Pre-deployment validation
        bun run test && bun run build
  postToolUse:
    - shell: |
        # Post-deployment verification
        curl -f $DEPLOY_URL/health || exit 1
---

# Deployment

Deploying to {{env}}...
```

## Best Practices

### 1. Clear Description

**Bad**:
```yaml
description: Helps with deployment.
```

**Good**:
```yaml
description: Deploys application to specified environment with health checks and rollback. Use when deploying to production or staging. Do not use for local development.
```

### 2. Appropriate Tool Constraints

**Good constraints match the task**:
- **Read-only review**: `allowed-tools: Read Grep Glob` + `disallowed-tools: Write Bash`
- **Code modification**: `allowed-tools: Read Edit Write`
- **Testing**: `allowed-tools: Bash Read`

### 3. Explicit Workflow

Commands should be **deterministic**:
```markdown
## Step 1: Validate
Run `bun run lint`

## Step 2: Build
Run `bun run build`

## Step 3: Deploy
Run `bun run deploy`
```

### 4. Error Handling

```markdown
## If Build Fails
- Check lint errors
- Fix TypeScript issues
- Re-run command

## If Deploy Fails
- Check logs in `logs/deploy.log`
- Rollback using `/rollback`
```

## Anti-Patterns

### Anti-Pattern 1: Discovery Loss

**Problem**: Using commands for everything (loses auto-discovery)

**Fix**: Use skills for domain expertise. Commands for explicit control only.

### Anti-Pattern 2: Vague Description

**Bad**: `description: Helps with code`

**Good**: `description: Refactors code using project patterns. Use when improving maintainability.`

### Anti-Pattern 3: Over-Constraining

**Problem**: `allowed-tools: Read` for a refactor task

**Fix**: Only constrain tools when safety/security requires it

### Anti-Pattern 4: Premature Command

**Problem**: Creating command before skill exists

**Fix**: Start with skill. Add command only if explicit control is needed.

## Command + Skill Pattern

Commands can activate skills for best of both worlds:

```markdown
---
name: refactor
description: Refactors code using project patterns. Use when cleaning up code structure.
---

# Refactor Workflow

## Activate Skill
Loading skills-knowledge...

## Execute Refactor
Following refactor patterns from skill...
```

**This gives you**:
- **Explicit control** (command)
- **Discoverable expertise** (skill)
- **Progressive disclosure** (skill references)

## Quick Validation Checklist

- [ ] Name is lowercase with hyphens
- [ ] Description answers: WHAT + WHEN + negative
- [ ] Tool constraints match task requirements
- [ ] Workflow is explicit and deterministic
- [ ] Error handling is documented
- [ ] Command solves real user need
- [ ] Skill alternative was considered (for auto-discovery)

---

# Subagents

## When to Use Subagents

**Use subagents when:**
- Task generates **high-volume output** (repo exploration, test logs)
- You need **strict tool isolation** or permission modes
- You want to route to a **cheaper model** (Haiku for exploration)
- Tasks are **naturally separable** and can run in parallel
- **Context Rot Prevention**: Long workflows degrade performance; forks start fresh.

**Subagents excel at:**
- Isolating noisy output from main conversation
- Running tasks in **separate context windows**
- Parallel execution of independent tasks
- Per-task tool constraints

**Subagents limitations:**
- Separate context window (must explicitly pass context)
- Orchestrated by code, not auto-discovered
- Overkill for simple workflows

**Most customization packs don't need subagents.** Only use when proven necessary.

## Built-in Subagent Types

| Type | Use For | Tools | Model |
|------|---------|-------|-------|
| **Explore** | Fast codebase exploration | Read, Glob, Grep | Usually Haiku |
| **Plan** | Architecture planning | All tools (no Task) | Any |
| **general-purpose** | General tasks | All tools + Task | Any |
| **Bash** | Command execution | Bash only | Any |

### Explore Subagent

**Purpose**: Fast, thorough codebase exploration without cluttering main conversation.

**Best for**:
- Finding files matching patterns
- Searching code for keywords
- Understanding codebase structure
- High-volume read operations

**Example**:
```typescript
const exploreAgent = await Task({
  subagent_type: "Explore",
  prompt: "Find all TypeScript files containing 'interface'"
});
```

### Plan Subagent

**Purpose**: Architecture planning without executing changes.

**Best for**:
- Designing implementation strategies
- Analyzing architectural trade-offs
- Creating step-by-step plans

**Key constraint**: Cannot spawn other subagents (no Task tool).

### General-Purpose Subagent

**Purpose**: General autonomous task execution.

**Best for**:
- Multi-step tasks
- Complex decision-making
- Tasks requiring multiple tool types

**Includes**: Task tool for spawning additional subagents if needed.

### Bash Subagent

**Purpose**: Shell command execution.

**Best for**:
- Git operations
- Build/test runs
- Deployment scripts

**Constraint**: Bash tool only.

## Coordination Patterns

### Pattern 1: Orchestrator-Worker

```
Main → spawns multiple workers → collects results
```

**Use when**: You have one main task that requires multiple parallel subtasks.

**Example**:
```typescript
const results = await Promise.all([
  Task({ subagent_type: "Explore", prompt: "Find React components" }),
  Task({ subagent_type: "Explore", prompt: "Find utility functions" }),
  Task({ subagent_type: "Explore", prompt: "Find API calls" })
]);

// Aggregate results
```

### Pattern 2: Parallel Execution

```
Main → spawns N independent tasks → waits for all
```

**Use when**: Tasks are independent and can run simultaneously.

**Example**:
```typescript
// Run tests and lint in parallel
const [testResults, lintResults] = await Promise.all([
  runTestsAgent(),
  runLintAgent()
]);
```

### Pattern 3: Sequential Handoff

```
Agent A → completes phase → spawns Agent B → continues
```

**Use when**: Phases must execute in order but benefit from context isolation.

**Example**:
```typescript
// Phase 1: Explore
const exploreResult = await Task({
  subagent_type: "Explore",
  prompt: "Find all API endpoints"
});

// Phase 2: Document (uses explore result)
const docResult = await Task({
  subagent_type: "general-purpose",
  prompt: `Document these endpoints: ${exploreResult}`
});
```

## Key Principles

### 1. Context Passing

**Problem**: Subagents have separate context windows.

**Solution**: Explicitly pass relevant context:

```typescript
// Bad: No context passed
const result = await Task({
  subagent_type: "Explore",
  prompt: "Find the bug"
});

// Good: Explicit context
const result = await Task({
  subagent_type: "Explore",
  prompt: `Find the bug in this function: ${functionCode}`
});
```

### 2. Cost Considerations

**Problem**: Each subagent spawn consumes quota.

**Solution**: Minimize spawns, batch work when possible:

```typescript
// Bad: Spawns 10 agents
for (const file of files) {
  await Task({ prompt: `Analyze ${file}` });
}

// Good: One agent handles all files
await Task({
  prompt: `Analyze these files: ${files.join(", ")}`
});
```

### 3. Tool Constraints

**Problem**: Subagent may use tools you didn't intend.

**Solution**: Use appropriate subagent type:

```typescript
// For read-only exploration
Task({ subagent_type: "Explore" })  // No Write/Bash

// For general tasks
Task({ subagent_type: "general-purpose" })  // All tools
```

### 4. Result Aggregation

**Problem**: Multiple subagent results can be hard to combine.

**Solution**: Design clear result contracts:

```typescript
interface SearchResult {
  file: string;
  matches: string[];
}

const results = await Task({
  subagent_type: "Explore",
  prompt: "Return JSON with file and matches array"
});
```

## Best Practices

### 1. Use for Output Isolation

**Good**: Exploring codebase without cluttering main conversation

**Bad**: Using subagent for simple task main thread could handle

### 2. Parallelize Independent Tasks

**Good**: Running test and lint in parallel

**Bad**: Running dependent tasks in parallel (order matters)

### 3. Model Selection

**Good**: Use Haiku for exploration (cheaper, faster)

**Bad**: Using Opus for simple grep/search

### 4. Clear Purpose

**Good**: "Explore codebase to find React components"

**Bad**: "Help with code" (too vague)

## Anti-Patterns

### Anti-Pattern 1: Over-Isolation

**Problem**: Using subagents for simple tasks

**Example**:
```typescript
// Bad: Simple task doesn't need subagent
await Task({ prompt: "Read one file" });

// Good: Just use Read tool directly
await Read(file_path);
```

**Fix**: Use subagents only when isolation or parallelism is genuinely needed.

### Anti-Pattern 2: Context Starvation

**Problem**: Not passing enough context to subagent

**Example**:
```typescript
// Bad: Subagent has no context
await Task({ prompt: "Fix the bug" });

// Good: Explicit context
await Task({
  prompt: `Fix this bug: ${bugDescription} in this file: ${fileContent}`
});
```

**Fix**: Always pass relevant context explicitly.

### Anti-Pattern 3: Orchestration Complexity

**Problem**: Over-complicated coordination patterns

**Example**: Spawning 5 subagents that each spawn 3 more

**Fix**: Keep orchestration simple. Prefer fewer subagents with clearer tasks.

### Anti-Pattern 4: Premature Subagent

**Problem**: Creating subagent before skill exists

**Example**: Starting with subagent for domain expertise

**Fix**: Start with skill. Add subagent only if noise/isolation becomes issue.

## When to Use Each Type

| Scenario | Use Type | Why |
|----------|----------|-----|
| Find all files matching pattern | Explore | Fast, read-only, high-volume |
| Plan refactoring strategy | Plan | No execution needed, architecture focus |
| Multi-step deployment | general-purpose | Needs multiple tool types |
| Run shell commands | Bash | Shell operations only |
| Parallel file analysis | Explore (parallel) | Independent tasks, isolation |

## Quick Validation Checklist

- [ ] Have I considered if a skill would suffice?
- [ ] Is the task genuinely noisy or high-volume?
- [ ] Do I need strict tool isolation?
- [ ] Can I batch work to minimize spawns?
- [ ] Am I passing sufficient context?
- [ ] Is the subagent type appropriate for the task?
- [ ] Would parallel execution help?

---

## Pattern: Clean Fork Pipeline

**Problem**: Linear skill chains accumulate "context rot" - intermediate outputs, thinking noise, and token bloat that make later steps less effective.

**Solution**: Use `context: fork` for worker skills in multi-step pipelines to create isolated, clean contexts for each step.

### Architecture

```
┌─────────────────────────────────────┐
│     Hub Skill (Main Context)          │
│  - Orchestrates workflow              │
│  - Maintains state                    │
│  - Spawns forked workers              │
└─────────────┬─────────────────────────┘
              │
      ┌───────┴───────┐
      │               │
      ▼               ▼
┌───────────┐  ┌───────────┐
│ Worker A  │  │ Worker B  │
│(fork)     │  │(fork)     │
│Clean ctx  │  │Clean ctx  │
└───────────┘  └───────────┘
      │               │
      └───────┬───────┘
              ▼
      ┌─────────────┐
      │ Worker C    │
      │ (fork)      │
      │Uses A+B     │
      └─────────────┘
```

### Benefits

1. **Prevents Context Rot**: Each worker starts with clean, focused context
2. **Enables Parallelism**: Workers can run simultaneously in isolated contexts
3. **Reduces Hallucinations**: Constrained context prevents confusion from irrelevant history
4. **Modular & Reusable**: Worker skills can be called from any hub skill
5. **Error Isolation**: Failure in one worker doesn't corrupt others' contexts

### Implementation Example

**Hub Skill** (main context, orchestrates):
```yaml
---
name: analysis-pipeline
description: "Orchestrate multi-step analysis workflow"
disable-model-invocation: true
---

# Analysis Pipeline

1. Spawn research-worker (context: fork)
   - Task: Deep research on $ARGUMENTS
   - Output: Research findings (clean result, no noise)

2. Spawn analysis-worker (context: fork, parallel)
   - Task: Analyze research findings
   - Output: Analysis results

3. Aggregate results from both workers

4. Spawn report-worker (context: fork)
   - Task: Generate final report
   - Input: Aggregated research + analysis
   - Output: Final report
```

**Worker Skill** (forked, isolated context):
```yaml
---
name: research-worker
description: "Deep research in isolated context"
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find all relevant files using Glob and Grep
2. Read and analyze content
3. Generate comprehensive research findings

# This creates significant noise and intermediate output,
# but it's isolated from the main conversation context
```

### When to Use Forked Workers

| Scenario | Pattern | Why |
|----------|---------|-----|
| Multi-step pipeline (>3 steps) | Hub + Forked Workers | Prevents context rot |
| High-volume intermediate output | Forked Workers | Keeps main context clean |
| Parallel execution needed | Forked Workers | Isolation enables parallelism |
| Complex reasoning tasks | Forked Workers | Reduces confusion from irrelevant history |
| Simple deterministic chain | Linear | Low overhead, simple enough |

### When NOT to Use Forked Workers

| Scenario | Reason |
|----------|--------|
| Simple one-off tasks | Overhead not justified |
| Tasks needing conversation context | Forked context lacks history |
| Low-volume operations | No benefit to isolation |
| Single-step operations | Unnecessary complexity |

### Sources
- Context isolation prevents context rot (verified via agent-browser research)
- Fork pattern enables parallel execution (official Claude Code docs)
- Hub-and-spoke pattern for complex workflows (Anthropic research)
