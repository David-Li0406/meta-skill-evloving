# Layer Selection Guide

## Table of Contents

- [The Minimal Pack Philosophy](#the-minimal-pack-philosophy)
- [Quick Decision Tree](#quick-decision-tree)
- [Layer Comparison Matrix](#layer-comparison-matrix)
- [Context: Fork Decision Criteria](#context-fork-decision-criteria)
- [Fork Patterns (Static Configuration)](#fork-patterns-static-configuration)
- [Autonomy Decision Tree](#autonomy-decision-tree)
- [CLAUDE.md Rules](#claudemd-rules)
- [Coding Standards](#coding-standards)
- [Architecture Principles](#architecture-principles)
- [Safety Boundaries](#safety-boundaries)
- [Skills (PRIMARY - Minimal Pack Foundation)](#skills-primary---minimal-pack-foundation)
- [Slash Commands (OPTIONAL Enhancement)](#slash-commands-optional-enhancement)
- [Steps](#steps)
- [Subagents (RARE/ADVANCED)](#subagents-rareadvanced)
- [Hybrid Patterns](#hybrid-patterns)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Quick Reference Checklist](#quick-reference-checklist)
- [When in Doubt](#when-in-doubt)

> Comprehensive guide for choosing between the four customization layers: CLAUDE.md rules, slash commands, skills, and subagents. **Start here** before building any customization.

---

## The Minimal Pack Philosophy

> **A complete customization pack can be just CLAUDE.md + one Skill.**

Commands and subagents are **optional enhancements**. Only add them when proven necessary.

**Minimal Pack Pattern**:
```
my-pack/
├── CLAUDE.md           # Project norms, standards
└── .claude/
    └── skills/
        └── domain-expertise/  # One focused skill
            └── SKILL.md
```

**When to add more**:
- Add **commands** when you need explicit user control over workflows
- Add **subagents** when you need isolation, parallelism, or strict tool constraints

---

## Quick Decision Tree

```
START: What do you need?
│
├─ "Persistent project norms"
│  └─→ CLAUDE.md rules
│
├─ "Domain expertise Claude should discover"
│  └─→ Skill (Minimal Pack: CLAUDE.md + Skill)
│     ├─ "Simple, focused task" → Skill (regular)
│     └─ "Complex workflow needing isolation" → Skill (context: fork)
│
├─ "Explicit workflow control I trigger manually"
│  └─→ Slash Command (OPTIONAL)
│
└─ "Isolation/parallelism/separate context"
   └─→ Subagent (RARE/ADVANCED)
```

### MCP Scope Configuration Criteria

**Before project setup or workflow changes:**

1. **Identify Task Category**
   - Plugin authoring (docs, skills, commands)
   - Web research (verification, documentation fetching)
   - Code analysis (validation, review)
   - Orchestration (multi-phase workflows)

2. **Configure MCPs at Appropriate Scope**
   - **Authoring**: Project scope → `file-search + simplewebfetch` only
   - **Research**: Project scope → `browser + deepwiki + simplewebfetch`
   - **Analysis**: Project scope → `file-search + LSP` (if available)
   - **Universal tools**: User scope → ONLY for cross-project utilities

3. **Edit `.mcp.json` and Restart**
   - Configure project-specific MCPs in `.mcp.json`
   - Use `--scope local` for personal project tools
   - Restart Claude Code to apply configuration changes
   - Tool Search activates automatically when tools exceed 10% context

**Configuration Example**:
```json
// .mcp.json for plugin authoring project
{
  "mcpServers": {
    "file-search": { "command": "..." },
    "simplewebfetch": { "command": "..." }
  }
}
```

**For detailed scope-based strategy**: See [common.md](common.md#context-window-management)

---

## Layer Comparison Matrix

| Dimension | CLAUDE.md Rules | Slash Command | Skill | Subagent |
|-----------|----------------|--------------|-------|----------|
| **Purpose** | Project norms | Explicit entrypoint | Discoverable expertise | Isolation/parallelism |
| **Trigger** | Always active | Manual `/command` | Auto-discovered + manual | Orchestrated by code |
| **Context** | Main conversation | Main conversation | Main (or forked) | Separate context |
| **Discovery** | N/A | No (manual only) | Yes (name + description) | No |
| **When to Use** | Persistent standards | User-controlled workflows | Domain procedures | Noise/isolation needs |
| **Priority** | Foundation | Optional enhancement | Primary vehicle | Rare/advanced |

---

## Context: Fork Decision Criteria

### When to Use Regular Skill (Main Context)

**Use regular skills when:**
- Task fits in main conversation context
- Low to moderate output volume
- Direct interaction with user is beneficial
- Context sharing with main conversation is valuable

**Examples:**
- Code reviews (moderate output, user feedback loop)
- Feature implementation (context sharing helpful)
- Documentation tasks (direct user interaction)

### When to Use Skill (context: fork)

**Use context: fork when:**
- Task generates **high-volume output** (extensive grep, log analysis, repo traversal)
- Exploration would clutter main conversation
- Task is naturally noisy or verbose
- Context isolation improves performance
- Task benefits from separate context window

**Examples:**
- Full codebase audits (high-volume output)
- Log triage and analysis (noisy output)
- Extensive file searches (verbose results)
- Deep research tasks (separate context beneficial)

### Context: Fork vs Subagent

**Choose context: fork when:**
- You want **auto-discovery** + isolation
- Still part of main skill architecture
- Can share skill logic with regular variant

**Choose subagent when:**
- You need **orchestration** capabilities
- Tasks can run in parallel
- Need different tool constraints per task
- Completely separate from main conversation

**Key difference:**
- **Context: fork** = Same skill, isolated context
- **Subagent** = Different execution model, orchestrated separately

## Fork Patterns (Static Configuration)

Since `context: fork` is **static configuration** (not runtime-decisionable), choose the pattern that matches your use case:

### Pattern A: Router + Worker (Recommended for Flexibility)

**Structure:**
- **Skill Router** (non-fork): Lightweight, auto-discovery, classification + minimal collection
- **Skill Worker** (fork): `context: fork` in frontmatter, heavy exploration, returns compact result

**Use when:**
- You want auto-discovery main + isolated execution for noisy cases
- Most cases are simple (classification, routing)
- Some cases require noisy execution (full repo traversal, log analysis)

**Example:**
```
codebase-auditor/ (Router, non-fork)
├── SKILL.md
└── references/
    └── worker.md

codebase-auditor-worker/ (Worker, forked)
├── SKILL.md (with context: fork)
└── references/
    └── deep-analysis-patterns.md
```

### Pattern B: Single Forked Skill (Simpler, Less Flexible)

**Structure:**
- Put `context: fork` directly in main skill frontmatter
- All executions run in fork

**Use when:**
- Most executions are structurally noisy
- Deep research, full audit, log triage
- Simpler setup is preferred

**Trade-off:** Even simple cases run in fork (adds overhead)

**Example:**
```
deep-researcher/
├── SKILL.md (with context: fork)
└── references/
    └── research-patterns.md
```

### Pattern C: Skill + Forked Command (Best for User Control)

**Structure:**
- **Skill** = expertise + decision tree (auto-discovery, non-fork)
- **Command** = explicit entry point with `context: fork` for heavy workflow

**Use when:**
- User should control when noisy phase starts
- Heavy/costly/long operations need explicit trigger
- Auto-discovery for standards + explicit button for heavy ops

**Example:**
```
security-auditor/ (Skill, non-fork)
├── SKILL.md
└── references/
    └── audit-patterns.md

.claude/commands/security-audit.md (Command, forked)
├── context: fork
└── content: "Loading security-auditor expertise..."
```

**Best compromise:** Auto-discovery for standards + explicit control for heavy operations

## Autonomy Decision Tree

Skills should be **autonomous by default** — they should complete without questions in 80-95% of expected cases.

### The 5-Step Autonomy Policy

#### Step 1: Classify (No Questions)

Before taking any action, classify the task to understand the budget and approach.

**Task Type Classification:**
- **Analysis**: Read-only exploration, pattern recognition, documentation synthesis
- **Modification**: Code changes, refactoring, feature implementation
- **Risky Execution**: Deployments, migrations, destructive operations

**Criticality Assessment:**
- **High**: Data loss, security impact, production changes, costly operations
- **Medium**: Breaking changes to non-critical systems, moderate time cost
- **Low**: Reversible changes, local development, fast operations

**Variability Assessment:**
- **Low**: Same steps every time (deployment, test execution)
- **Medium**: Some variation but predictable patterns (code review, refactoring)
- **High**: Highly contextual (creative work, architecture decisions)

**Define Budget:**
- Target: 1-2 top-level prompts maximum
- Max: 3 subagents per task, 2 correction cycles per file
- Immediate stop if criteria met mid-execution

#### Step 2: Explore First

Before asking questions, use safe, low-cost discovery actions.

**Safe Exploration Actions:**
- `Read` — Read files to understand structure
- `Grep` — Search for patterns across codebase
- `Glob` — Find files by pattern
- Structure inspection — Analyze imports, dependencies, file organization

**Resolve Ambiguity:**
- Use discovery instead of questions
- Infer from existing code patterns
- Check for similar implementations in the codebase

#### Step 3: Can Proceed Deterministically?

Ask: Do I have enough information to complete the task without questions?

**If YES:** Execute the complete workflow with explicit success criteria:
- Define what "done" looks like
- Execute all steps
- Verify against success criteria
- Report completion

**If NO:** Continue to Step 4

#### Step 4: Question Burst (Rare, Contractual)

Questions are authorized ONLY when ALL THREE conditions are true:

**Condition 1: Information NOT Inferrable**
- The information cannot be discovered through read/grep/inspection
- The information is not in documentation or code patterns
- The information is genuinely missing from the context

**Condition 2: High Impact if Wrong Choice**
- Wrong choice would cause significant rework
- Wrong choice would introduce security issues
- Wrong choice would break core functionality
- Wrong choice would be costly (time, money, data)

**Condition 3: Small Set Unlocks Everything**
- 3-7 questions maximum
- Answers enable deterministic completion
- No follow-up questions expected after burst

**Example Valid Question Burst:**
```
I need to know the deployment configuration:

1. What is the target environment? (staging/production)
2. Should database migrations run automatically? (yes/no)
3. Should the deployment trigger a health check? (yes/no)

These 3 answers will enable me to complete the deployment workflow.
```

**Example Invalid Question Burst:**
```
Which files should I refactor?  (Violates Condition 1 — can be discovered via grep)
What color should the button be?  (Violates Condition 2 — low impact)
Should I add a space here? And here? And here?  (Violates Condition 3 — not a small set)
```

#### Step 5: Escalate

When autonomy is not appropriate, recommend escalation:

**Recommend Command When:**
- User control is required (deployments, releases, migrations)
- Tool constraints are strict (read-only review, audit)
- Operation is costly/long (full repo audit, large data processing)
- Stable entrypoint needed ("run tests", "build")

**Recommend Fork/Subagent When:**
- Noise isolation is needed (exploration, log triage, extensive grep)
- Parallel execution is beneficial (independent tasks)
- Separate context window is required (state isolation)
- Long-running operations (background processing)

### Autonomy Design Checklist

**Before Building:**
- [ ] What ambiguity can be resolved through exploration (read/grep)?
- [ ] What truly requires user input (cannot be inferred)?
- [ ] What are the explicit success/stop criteria?
- [ ] Which fork pattern matches the use case?

**Question Burst Test:**
- [ ] Information NOT inferrable from repo/tools?
- [ ] High impact if wrong choice?
- [ ] Small set (3-7 max) unlocks everything?

**If any "no":** Encode decision tree instead of asking

**Escalation Criteria:**
- [ ] Explicit control needed → Recommend command
- [ ] Noise/isolation needed → Recommend fork/subagent

---

## CLAUDE.md Rules

### When to Use Rules

**Use rules when:**
- You need persistent project norms that always apply
- You want to establish coding standards or conventions
- You have safety boundaries or security requirements
- You need to override global behavior for this project

**Rules excel at:**
- File placement conventions (e.g., "components go in src/components/")
- Coding standards (e.g., "use functional components with hooks")
- Architecture principles (e.g., "avoid circular dependencies")
- Safety boundaries (e.g., "never modify files in legacy/")

**Rules limitations:**
- Always loaded — can't be toggled on/off
- No dynamic context or variables
- Can't have tool controls
- Not discoverable — Claude just "follows" them

### Rule Structure

**Core template:**
```markdown
# Project Rules

## Coding Standards
- Use functional components with hooks
- Prefer composition over inheritance

## Architecture Principles
- Avoid circular dependencies
- Keep components under 300 lines

## Safety Boundaries
- Never modify files in legacy/ without confirmation
- Always backup before database migrations
```

### File Locations

| Location | Scope | Use For |
|----------|-------|---------|
| `~/.claude/CLAUDE.md` | Global | Personal preferences across all projects |
| `{project}/CLAUDE.md` | Project | Project-specific norms and standards |
| `{project}/.claude/rules/*.md` | Module | Modular rule sets |

**Key principles:**
- **Specificity**: Be concrete, not vague
- **Context**: Explain the "why" behind rules
- **Actionability**: Make rules enforceable
- **Safety**: Define boundaries clearly

### Anti-Patterns

- **Vague rules**: "Write clean code" → "Use functional components with hooks"
- **Overly prescriptive**: Micromanaging style → Focus on behavior
- **Static documentation**: Rules are active configuration, not docs
- **Global capture**: Don't put everything in global CLAUDE.md

---

## Skills (PRIMARY - Minimal Pack Foundation)

### When to Use Skills

**Use skills when:**
- Claude should discover and use domain expertise automatically
- You need multi-step procedures with decision trees
- The workflow involves validation loops
- You want progressive disclosure (SKILL.md + references/)

**Skills excel at:**
- Domain expertise (e.g., PDF processing, frontend design)
- Complex workflows with decision trees
- Knowledge sharing and best practices
- Procedures Claude wouldn't otherwise know

**Skills limitations:**
- Main conversation context (can be noisy)
- Forked context is an option, but not default
- No strict tool controls (only guidance + hooks)

### Minimal Pack Pattern

> **Most packs only need CLAUDE.md + one Skill.**

**Example minimal pack:**
```
react-best-practices/
├── CLAUDE.md                    # "Use functional components, TypeScript"
└── .claude/
    └── skills/
        └── react-consultant/
            └── SKILL.md         # "When building hooks, check deps array"
```

This gives you:
- **Persistent norms** (CLAUDE.md)
- **Discoverable expertise** (Skill)
- **Progressive disclosure** (SKILL.md + references/)

**Add commands/subagents ONLY when proven necessary.**

### Skill Structure

```
skill-name/
├── SKILL.md              # Core workflow (<300 lines ideal)
├── references/           # Heavy content, loaded on-demand
│   ├── patterns.md
│   └── advanced.md
├── examples/             # Working code examples
│   └── basic-usage.md
└── scripts/              # Complex operations only
    └── deploy.sh
```

### Anti-Patterns

- **Over-bloated SKILL.md**: Keep core workflow inline, heavy content in references/
- **Tutorial style**: Don't teach basics Claude knows
- **Missing description**: Poor description = skill never activates
- **Over-engineering**: Scripts for simple operations → use native tools

### Autonomy-First Design

Skills should be **self-sufficient by default**:

**Autonomy Decision Tree**:
1. **Classify**: Task type + criticality + variability → define budget
2. **Explore First**: Use read/grep before asking questions
3. **Execute Deterministically**: If path clear, complete workflow
4. **Question Burst** (rare): Only if info not inferrable + high impact + 3-7 questions unlock all
5. **Escalate**: Recommend command if explicit control needed, fork if noise isolation needed

**For detailed autonomy guidance**: See [autonomy-decision-tree.md](autonomy-decision-tree.md)

### When to Add Commands (Explicit Criteria)

Create slash command if **at least ONE** is true:

| Criterion | Examples | Rationale |
|-----------|----------|-----------|
| **User control required** | Deployments, releases, migrations, destructive ops | User should explicitly trigger |
| **Tool constraints strict** | Read-only review, audit, validation | Minimal `allowed-tools` for safety |
| **Stable entrypoint needed** | "Run tests", "Build", "Deploy to prod" | Team-triggered workflow button |
| **Operation is costly/long** | Full repo audit, large data processing | User awareness of cost/duration |

**Best Practice**: Command → "activates a Skill" = best of both worlds
- Command = thin wrapper (injects context + explicit trigger + optional fork)
- Skill = retains expertise + progressive disclosure

**For detailed command patterns**: See the commands guide.

---

## Slash Commands (OPTIONAL Enhancement)

### When to Use Commands

**Use commands when:**
- You want explicit user control over workflow triggering
- The workflow should have strict tool controls via `allowed-tools`
- You want to bundle hooks (pre/post execution)
- You don't need Claude to discover it automatically

**Commands excel at:**
- Explicit workflow entrypoints (e.g., `/refactor`, `/deploy`)
- Strict tool constraints (e.g., read-only operations)
- Bundling hooks for validation
- User-controlled, deterministic workflows

**Commands limitations:**
- No auto-discovery (must invoke manually)
- Always main conversation context
- Can't be delegated to automatically

### Command Structure

```markdown
---
name: refactor
description: Refactors code using project-specific patterns. Use when cleaning up code structure or improving maintainability.
allowed-tools: Read Edit Grep Glob
context: server
---

# Refactor Workflow

## Steps
1. Analyze current structure
2. Apply refactor patterns
3. Verify tests pass
```

### Command vs Skill

| Factor | Choose Command | Choose Skill |
|--------|---------------|--------------|
| Trigger | Manual `/command` | Auto-discovery |
| Tool control | Strict `allowed-tools` | Guidance only |
| Discovery | No | Yes |
| Hooks | Pre/post execution | Via system hooks |

**Anti-pattern**: Creating a command when a skill would suffice (you lose auto-discovery).

---

## Subagents (RARE/ADVANCED)

### When to Use Subagents

**Use subagents when:**
- Task generates high-volume output (repo exploration, test logs)
- You need strict tool isolation or permission modes
- You want to route to a cheaper model (Haiku for exploration)
- Tasks are naturally separable and can run in parallel

**Subagents excel at:**
- Isolating noisy output from main conversation
- Running tasks in separate context windows
- Parallel execution of independent tasks
- Per-task tool constraints

**Subagents limitations:**
- Separate context window (must explicitly pass context)
- Orchestrated by code, not discovered
- Overkill for simple workflows

### Built-in Subagent Types

| Type | Use For | Tools |
|------|---------|-------|
| **Explore** | Fast codebase exploration | Read, Glob, Grep |
| **Plan** | Architecture planning | All tools (no Task) |
| **general-purpose** | General tasks | All tools + Task |
| **Bash** | Command execution | Bash only |

### Coordination Patterns

**Orchestrator-Worker:**
```
Main → spawns multiple workers → collects results
```

**Parallel:**
```
Main → spawns N independent tasks → waits for all
```

**Handoff:**
```
Agent A → completes phase → spawns Agent B → continues
```

### Anti-Patterns

- **Over-isolation**: Using subagents for simple tasks
- **Context starvation**: Not passing enough context to subagent
- **Orchestration complexity**: Over-complicated coordination patterns

---

## Hybrid Patterns

### Command → Skill → Subagent

These layers stack effectively:

```
User runs: /refactor component-name
    ↓
Command: Activates refactor-consultant skill
    ↓
Skill: Reads codebase, plans changes
    ↓
Skill: Delegates to custom subagent with strict tool allowlist
    ↓
Subagent: Executes, returns summary
    ↓
Main: Updates CLAUDE.md if new patterns emerged
```

### Migration Patterns

**Rules → Skill:**
- Start with rules in CLAUDE.md
- As domain expertise grows, extract to skill
- Keep core norms in CLAUDE.md

**Skill → Command:**
- Start with skill for discoverability
- If explicit control becomes critical, add command
- Skill and command can coexist

**Skill → Subagent:**
- Start with skill in main context
- If noise/isolation becomes issue, delegate to subagent
- Keep skill as orchestrator

---

## Anti-Patterns to Avoid

### Over-Engineering Anti-Pattern

**Symptom**: All four layers for simple workflows

**Example**:
```
my-app/
├── CLAUDE.md
└── .claude/
    ├── skills/
    │   └── simple-task/
    ├── commands/
    │   └── do-simple-task.md
    └── subagents/
        └── simple-task-worker.md
```

**Fix**: Start with CLAUDE.md + Skill. Add others ONLY when proven necessary.

### Premature Abstraction Anti-Pattern

**Symptom**: Creating commands/subagents "for future flexibility"

**Fix**: YAGNI — build only what you need now. Evolve as requirements emerge.

### Discovery Loss Anti-Pattern

**Symptom**: Using commands for everything (loses auto-discovery)

**Fix**: Use skills as primary vehicle. Commands for explicit control only.

---

## Quick Reference Checklist

### Before Building Any Customization

- [ ] Have I identified the specific problem I'm solving?
- [ ] Have I considered if CLAUDE.md rules suffice?
- [ ] Have I considered if a single skill (minimal pack) is enough?
- [ ] Do I have a proven need for a command (explicit control)?
- [ ] Do I have a proven need for a subagent (isolation/parallelism)?

### Layer Selection Checklist

**CLAUDE.md Rules if:**
- [ ] Need persistent project norms
- [ ] Want standards that always apply
- [ ] Have safety/security boundaries

**Skill if:**
- [ ] Claude should discover expertise automatically
- [ ] Need multi-step procedures
- [ ] Want progressive disclosure

**Command if:**
- [ ] Need explicit user control
- [ ] Want strict tool constraints
- [ ] Don't need auto-discovery

**Subagent if:**
- [ ] Need output isolation
- [ ] Want parallel execution
- [ ] Need separate context window

---

## When in Doubt

> **Start with CLAUDE.md + one Skill.**

This minimal pack handles 80% of customization needs. Add commands/subagents ONLY when you have a proven requirement.

**For detailed guidance:**
- **Layer selection** → This guide
- **Skill creation** → **Load: skills-knowledge**
- **Core principles** → [common.md](common.md)
- **Advanced patterns** (commands/subagents/rules) → [advanced-patterns.md](advanced-patterns.md)

**Remember**: Commands and subagents are optional enhancements, not required components.
