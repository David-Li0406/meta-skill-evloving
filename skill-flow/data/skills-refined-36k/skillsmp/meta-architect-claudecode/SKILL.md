---
name: meta-architect-claudecode
description: "Guide layer selection for Claude Code. Use when choosing between CLAUDE.md rules, skills, subagents, hooks, or MCP. Do not use for general coding questions or non-architecture tasks."
user-invocable: true
---

# Meta-Architect

Choose the right customization layer and build effective skills for Claude Code using official documentation.

## 🚨 MANDATORY: Read BEFORE Proceeding

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Official Skills Guide**: https://code.claude.com/docs/en/skills
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any customization layer decisions
  - **Content**: Skills architecture, progressive disclosure, best practices
  - **Cache**: 15 minutes minimum

- **[MUST READ] Subagents Guide**: https://code.claude.com/docs/en/sub-agents
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: When considering subagent usage
  - **Content**: Agent coordination patterns, state management, context: fork
  - **Cache**: 15 minutes minimum

- **[MUST READ] Plugin Architecture**: https://code.claude.com/docs/en/plugins
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before plugin structure decisions
  - **Content**: Plugin organization, component architecture
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** until you've fetched and reviewed Primary Documentation
- **REQUIRED** to understand skills-first architecture before layer selection
- **REQUIRED** to understand progressive disclosure before implementation

---

## Quick Decision Tree

### Layer Selection (START HERE)

```
START: What do you need?
│
├─ "Persistent project norms"
│  └─→ CLAUDE.md rules
│
├─ "Domain expertise to discover"
│  └─→ Skill (Minimal Pack: CLAUDE.md + Skill)
│     ├─ "Simple, focused task" → Skill (regular)
│     └─ "Complex workflow needing isolation" → Skill (context: fork)
│
├─ "Event automation"
│  └─→ Hook
│
├─ "Service integration"
│  └─→ MCP
│
└─ "Isolation/parallelism"
   └─→ Subagent (RARE/ADVANCED)
```

**Context: Fork Triggers:**
- High-volume output (extensive grep, repo traversal)
- Noisy exploration that clutters conversation
- Log analysis, full codebase audits
- Tasks benefiting from separate context window

**Context: Fork Mechanism:**
In a context: fork Skill run, the forked subagent's system prompt comes from the chosen agent (built-in or custom), while the Skill's SKILL.md becomes the task prompt that drives that subagent. If the chosen custom subagent also has `skills:` configured, those Skills' full contents are also injected into that forked subagent's context at startup—they don't get "replaced" by the forked Skill; they sit alongside it.

**Key Implementation Details**:
- **System Prompt Source**: The chosen agent type (Explore, Plan, Bash, general-purpose, or custom agent)
- **Task Instruction Source**: The Skill's SKILL.md content
- **Skills Composition**: Custom subagent skills are additive, not replaced by the forked Skill

**When NOT to use context: fork:**
- Simple, direct tasks
- User interaction is beneficial
- Low output volume

---

## Core Principles

### The Delta Standard

> **Good Customization = Expert-only Knowledge − What Claude Already Knows**

Only provide context Claude cannot infer. Focus on expert decisions, trade-offs, and domain-specific thinking frameworks.

### Minimal Pack Philosophy

> **A complete customization pack can be just CLAUDE.md + one Skill.**

Subagents are **optional enhancements**. Add them only when proven necessary (isolation/parallelism).

### Progressive Disclosure

**Tier 1**: Metadata (~100 tokens) — Always loaded
**Tier 2**: SKILL.md (<35,000 characters) — Loaded when invoked
**Tier 3**: Resources — Loaded on-demand

**Rule**: Keep core knowledge inline; disperse only when >35,000 characters or highly situational (<5% of tasks).

---

## The Five Layers

| Layer               | Purpose                | Priority           | Use For                              |
| ------------------- | ---------------------- | ------------------ | ------------------------------------ |
| **CLAUDE.md Rules** | Persistent norms       | **Foundation**     | Project standards, safety boundaries |
| **Skills**          | Discoverable expertise | **PRIMARY**        | Domain procedures, complex workflows |
| **Subagents**       | Isolation/parallelism  | **RARE**           | Noisy tasks, separate context        |
| **Hooks**           | Event automation       | **INFRASTRUCTURE** | MCP/LSP config, event handling       |
| **MCP**             | Service integration    | **EXTERNAL**       | External APIs, tools, services       |

---

## Core Values Framework

Each value represents a **design approach**, not a rigid category.

| Value            | Design Focus                               | When to Apply                               |
| ---------------- | ------------------------------------------ | ------------------------------------------- |
| **Reliability**  | Deterministic execution with validation    | "I need this done the same way, every time" |
| **Wisdom**       | Decision frameworks and trade-off analysis | "I need expert judgment"                    |
| **Consistency**  | Templates and standardized patterns        | "Everything must look the same"             |
| **Coordination** | Routing logic and state management         | "Many parts, one symphony"                  |
| **Simplicity**   | Direct path with minimal overhead          | "Keep it simple" (3 steps or fewer)         |

---

## Autonomy-First Design

Skills should be **self-sufficient by default** (80-95% autonomous):

### Autonomy Policy

1. **Classify**: Task type + criticality + variability → define budget
2. **Explore First**: Use read/grep before asking questions
3. **Execute Deterministically**: Complete workflow if path clear
4. **Question Burst** (rare): Only if info not inferrable + high impact + 3-7 questions unlock all
5. **Escalate**: Recommend command (explicit control) or fork (noise isolation)

### Question Burst Criteria (ALL 3 required)

✓ Information NOT inferrable from repo/tools
✓ High impact if wrong choice
✓ Small set (3-7 max) unlocks everything

---

## Orchestration Patterns: When to Use Which

### Linear Skill Chaining

**Use For**: Deterministic, simple, repeatable workflows

**Examples**:
- `diff → lint → commit`
- `validate → format → validate`
- `extract → transform → load`

**Pros**:
- Simple to implement
- Deterministic behavior
- Low token overhead

**Cons**:
- Brittle for complex workflows (single point of failure)
- Limited flexibility
- No error recovery between steps

**When to Avoid**:
- Workflows requiring decision-making between steps
- Dynamic problem solving where output is unpredictable
- Workflows with >3 steps that need error recovery

### Hub-and-Spoke

**Use For**: Complex, dynamic workflows requiring flexibility

**Examples**:
- `research → plan → code → test` (with decision points)
- Parallel research with aggregation
- Multi-stage analysis with branching logic

**Pros**:
- Centralized state management
- Error recovery and retry capability
- Dynamic rerouting based on results
- Resilient to individual worker failures

**Cons**:
- Higher complexity
- Token overhead (hub reads everything)
- More moving parts

**Sources**:
- [Anthropic: Building Effective Agents (Hub & Spoke)](https://www.anthropic.com/research/building-effective-agents)
- [LangChain: Chains vs Agents](https://python.langchain.com/docs/modules/chains/)
- [Microsoft: Autogen Design Patterns](https://microsoft.github.io/autogen/)

### Worker Orchestration (Noise Isolation)

**Pattern**: Router (this skill) + Worker (toolkit-worker)

** Use When**:
- Task involves high-volume output (audit, grep, log analysis)
- User asks for "Deep Analysis" or "Comprehensive Audit"
- Need to keep main context clean

**Instructions**:
1.  **Identify**: User task is "noisy" (e.g., "Audit this repo structure")
2.  **Delegate**: Spawn `toolkit-worker` subagent
3.  **Inject**: Dynamic context (repo structure, file lists)
4.  **Instructions**: "Perform audit based on your internal knowledge and this injected context."

**Example Delegation**:
```javascript
const workerResult = await Task({
  subagent_type: "toolkit-worker", // Uses agents/toolkit-worker.md configuration
  prompt: `Perform a comprehensive structural audit of the current repository.
  
  Context:
  - Repository Root: ${env.CLAUDE_PROJECT_DIR}
  - Focus: Architecture compliance, progressive disclosure checks
  
  Report Requirements:
  - Quality Score (0-10 scale)
  - Anti-patterns detected
  - Remediation list
  `,
  formatted_output: true
});
```

### Decision Tree

```
Need to orchestrate multiple skills?
│
├─ Simple, deterministic workflow?
│  ├─ Yes → Linear Chaining (≤3 steps)
│  └─ No → Continue below
│
├─ Requires decision-making between steps?
│  ├─ Yes → Hub-and-Spoke
│  └─ No → Continue below
│
├─ Parallel execution needed?
│  ├─ Yes → Hub-and-Spoke with context: fork
│  └─ No → Linear Chaining
│
└─ Error recovery required?
   ├─ Yes → Hub-and-Spoke
   └─ No → Linear Chaining
```

---

## Workflow Selection

### What do you need?

**"Choose the right layer"** → [layer-selection.md](references/layer-selection.md)
- Layer decision tree with context: fork guidance
- Comparison matrix
- When to use each layer

**"Create skill from scratch"** → **Load: skills-knowledge**
- Step-by-step building workflow
- Golden path extraction method
- Autonomy design patterns

**"Evaluate skill quality"** → **Load: skills-knowledge#evaluating-skill-quality**
- 12-dimensional evaluation framework
- Common failure patterns
- Quality scoring (160 points)

**"Learn core principles"** → [common.md](references/common.md)
- Delta Standard
- Core Values Framework
- Anti-patterns

**"Advanced patterns"** → [advanced-patterns.md](references/advanced-patterns.md)
- CLAUDE.md rules (structure, anti-patterns)
- Slash commands (creation, best practices)
- Subagents (coordination patterns, limitations)

---

## Prompt Budget Playbook

**Goal**: Complete each unit of work in 1-2 top-level prompts maximum.

### Budget Rules

1. **Define the Work Unit**: Explicitly state what "done" looks like
2. **Success Criteria Must Be Measurable**: Binary pass/fail, not "improved"
3. **Hard Stop Conditions**:
   - Max 3 subagent spawns per task
   - Max 2 correction cycles on any file
   - Immediate stop if criteria met
4. **Prefer Deterministic Commands**: For validation/format/test
5. **Anti-2nd-Turn Checklist**:
   - [ ] All inputs available or identified as missing
   - [ ] Success criteria explicitly defined
   - [ ] Expected output format specified
   - [ ] Rollback strategy known

**Budget Equation**:
```
Target Budget = 1 (plan/assess) + 1 (execute/verify)
Max Budget = 1 (plan) + 2 (execute cycles) + 1 (validate)
```

---

## Common Use Cases

### Use Case 1: Building First Skill

**Path**: Layer Selection → Build Workflow

```
1. "I need domain expertise Claude can discover"
   → Skill (Minimal Pack)
2. Follow: Load: skills-knowledge (Steps 1-9)
3. Test: Fresh Eyes Test
4. Evaluate: 12-dimension framework
```

### Use Case 2: Choosing Context: Fork

**Path**: Layer Selection → Context Fork Criteria

```
1. "Will this generate high-volume output?"
   → Yes → Consider context: fork
2. "Would output clutter the conversation?"
   → Yes → Use context: fork
3. Pattern A: Router + Worker (recommended)
   Pattern B: Single Forked (simpler)
```

### Use Case 3: Evaluating Existing Skill

**Path**: Build Workflow → Evaluation Section

```
1. Load: skills-knowledge#evaluating-skill-quality
2. Scan: D1 (Knowledge Delta) first
3. Score: All 12 dimensions
4. Grade: A (144+), B (128-143), C (112-127), D (96-111), F (<96)
5. Fix: Common failure patterns
```

### Use Case 4: Creating CLAUDE.md Rules

**Path**: Advanced Patterns → Rules Section

```
1. Location: ~/.claude/ or project root
2. Structure: Context → Standards → Principles → Safety
3. Principles: Specificity, Context, Actionability, Safety
4. Anti-patterns: Vague rules, over-prescription, static docs
```

---

## Reference Files

| Reference                                                   | When to Load               | Purpose                                            |
| ----------------------------------------------------------- | -------------------------- | -------------------------------------------------- |
| **[layer-selection.md](references/layer-selection.md)**     | **First**: Before building | Choose between layers + context: fork guidance     |
| **[skills-knowledge](skills-knowledge)**                    | Creating/evaluating        | Skill building + extraction + evaluation workflows |
| **[common.md](references/common.md)**                       | Foundational               | Core principles, archetypes, shared patterns       |
| **[advanced-patterns.md](references/advanced-patterns.md)** | Advanced                   | Subagents, hooks, MCP (consolidated)               |

**Progressive Disclosure**: Only load what you need, when you need it.

## Historical References

- **Command Patterns (Legacy)** - *Note: This guide is historical. Commands were unified with skills in 2026.*
  - *Archived in .attic/legacy-files/*

---

## Anti-Patterns to Avoid

### Development

- **Deep Nesting** — `references/v1/setup/config.md` → Flatten to `references/setup-config.md`
- **Vague Description** — "Helps with coding" → Use clear capability + use case
- **Over-Engineering** — Scripts for simple tasks → Use native tools first

### Layer Selection

- **Using subagents** for simple tasks (overkill)
- **Using all layers** for simple workflows (premature abstraction)
- **Creating skills that require commands** (violates autonomy principle)

### Skill Design

- **Kitchen Sink** — One skill tries to do everything
- **Indecisive Orchestrator** — Too many paths, unclear direction
- **Pretend Executor** — Scripts requiring constant guidance

---

## Writing Style Requirements

### Imperative Form

**Correct**: "To create a hook, define the event type."
**Incorrect**: "You should create a hook by defining the event type."

### Third-Person Description

**Correct**: `description: "This skill should be used when the user asks..."`
**Incorrect**: `description: "Use this skill when you want to..."`

---

## When in Doubt

> **Start with layer selection** → [references/layer-selection.md](references/layer-selection.md)

1. **Choosing a layer?** → layer-selection.md
2. **Building skills?** → layer-selection.md → skills-knowledge → common.md
3. **Evaluating quality?** → skills-knowledge#evaluating-skill-quality
4. **Learning fundamentals?** → common.md

**Remember**: Most customization needs are met by CLAUDE.md + one Skill.
