# Skills Guide

## Table of Contents

- [When to Use Skills](#when-to-use-skills)
- [Three-Tier Loading Model](#three-tier-loading-model)
- [Autonomy-First Design](#autonomy-first-design)
- [Skill Structure](#skill-structure)
- [SKILL.md Template](#skillmd-template)
- [Quick Start](#quick-start)
- [Core Workflow](#core-workflow)
- [Decision Tree](#decision-tree)
- [Examples](#examples)
- [Resources](#resources)
- [Core Values Framework](#core-values-framework)
- [Description Engineering](#description-engineering)
- [Progressive Disclosure](#progressive-disclosure)
- [Resources](#resources)
- [Complex Workflow](#complex-workflow)
- [Quick Task](#quick-task)
- [Best Practices](#best-practices)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Quick Validation Checklist](#quick-validation-checklist)
- [When in Doubt](#when-in-doubt)

> Guidance for creating and managing skills — the **PRIMARY** customization layer.

> **For comprehensive reference**, see this guide.

> **Remember**: A complete customization pack can be just CLAUDE.md + one Skill.

---

## When to Use Skills

**Use skills when:**
- Claude should **discover and use** domain expertise automatically
- You need multi-step procedures with decision trees
- The workflow involves validation loops or complex choices
- You want **progressive disclosure** (SKILL.md + references/)

**Skills excel at:**
- Domain expertise (e.g., PDF processing, frontend design, API integration)
- Complex workflows with decision trees
- Knowledge sharing and best practices
- Procedures Claude wouldn't otherwise know

**Skills limitations:**
- Main conversation context (can be noisy for exploration tasks)
- Forked context available but not default
- No strict tool controls (only guidance + system hooks)

---

## Three-Tier Loading Model

Skills use progressive disclosure for optimal token economics:

**Tier 1: Metadata** (~100 tokens)
- `name` and `description` fields
- **Always loaded** at startup for discovery

**Tier 2: SKILL.md** (<35,000 characters)
- Complete operational instructions
- Loaded when skill is **invoked**

**Tier 3: Resources** (as needed)
- Files in `references/`, `examples/`, `scripts/`
- Loaded on **specific demand only**

**Design implication**: Keep core workflow in SKILL.md, heavy content in references/.

---

## Autonomy-First Design

Skills should be **self-sufficient by default** — they should complete without questions in 80-95% of expected cases.

### The Autonomy Decision Tree

```
START: Task received
│
├─ 1) CLASSIFY (no questions)
│   ├─ Task type: analysis / modification / risky execution
│   ├─ Criticality: high / medium / low
│   ├─ Variability: low / medium / high
│   └─ Define budget: 1-2 prompts target, max 3 subagents, max 2 corrections
│
├─ 2) EXPLORE FIRST (before asking)
│   ├─ Use safe, low-cost actions: read, grep, structure inspection
│   ├─ If noisy execution expected → use forked variant or command
│   └─ Resolve ambiguity through discovery, not questions
│
├─ 3) CAN PROCEED DETERMINISTICALLY?
│   ├─ YES → Execute complete workflow with explicit success criteria
│   └─ NO → Continue to step 4
│
├─ 4) QUESTION BURST (rare, contractual)
│   └─ Authorized ONLY if ALL 3 true:
│       ├─ Information NOT inferrable from repo/tools
│       ├─ High impact if wrong choice
│       └─ Small set (3-7 questions) unlocks everything
│
└─ 5) ESCALATE
    ├─ Recommend command if explicit control needed
    └─ Recommend fork/subagent if noise isolation needed
```

### Fork Patterns (Static Configuration)

Since `context: fork` is **static configuration** (not runtime-decisionable), choose the pattern that matches your use case:

**Pattern A: Router + Worker** (Recommended for flexibility)
- **Skill Router** (non-fork): Lightweight, auto-discovery, classification + minimal collection
- **Skill Worker** (fork): `context: fork` in frontmatter, heavy exploration, returns compact result
- **Use when**: You want auto-discovery main + isolated execution for noisy cases

**Pattern B: Single Forked Skill** (Simpler, less flexible)
- Put `context: fork` directly in main skill frontmatter
- **Use when**: Most executions are structurally noisy (deep research, full audit, log triage)
- **Trade-off**: Even simple cases run in fork

**Pattern C: Skill + Forked Command** (Best for user control)
- **Skill** = expertise + decision tree (auto-discovery, non-fork)
- **Command** = explicit entry point with `context: fork` for heavy workflow
- **Use when**: User should control when noisy phase starts
- **Best compromise**: Auto-discovery for standards + explicit button for heavy/costly/long ops

**For detailed autonomy guidance**: See [autonomy-decision-tree.md](autonomy-decision-tree.md)

---

## Skill Structure

```
skill-name/
├── SKILL.md              # Core workflow (<300 lines ideal)
├── references/           # Heavy content, loaded on-demand
│   ├── patterns.md
│   └── advanced.md
├── examples/             # Working code examples
│   └── basic-usage.md
└── scripts/              # Complex operations ONLY
    └── deploy.sh
```

**Content placement**:
- Core workflow → SKILL.md
- Deep domain knowledge → references/
- Reusable patterns → examples/
- Complex operations → scripts/

**The "Rule of Three"**:
- Mentioned once → Keep in SKILL.md
- Mentioned twice → Reference it
- Mentioned three times → Extract to dedicated file

---

## SKILL.md Template

```markdown
---
name: skill-name
description: {{CAPABILITY}}. Use when {{TRIGGERS}}. Do not use for {{EXCLUSIONS}}.
---

# Skill Name

## Quick Start
[2-3 sentences for immediate context]

## Core Workflow
[Main decision tree or procedure]

## Decision Tree
[Key choices the agent needs to make]

## Examples
[Concrete examples of the skill in action]

## Resources
[References to additional files]
```

---

## Core Values Framework

Each value represents a **design approach**, not a rigid category.

| Value | Design Focus | When to Apply |
|-------|-------------|---------------|
| **Reliability** | Deterministic execution with validation | "I need this done the same way, every time" |
| **Wisdom** | Decision frameworks and trade-off analysis | "I need expert judgment" |
| **Consistency** | Templates and standardized patterns | "Everything must look the same" |
| **Coordination** | Routing logic and state management | "Many parts, one symphony" |
| **Simplicity** | Direct path with minimal overhead | "Keep it simple" (3 steps or fewer) |

### Designing for Reliability

**When to apply**: Tasks requiring deterministic, repeatable execution

**Design approach**:
- Exact steps with validation checkpoints
- Rollback patterns for safe recovery
- Clear verification at each stage

**Example use cases**:
- Database migrations
- Security validations
- Deployment pipelines

### Designing for Wisdom

**When to apply**: Tasks requiring expert judgment and adaptation

**Design approach**:
- Decision frameworks for trade-offs
- Examples with reasoning
- Clear guidance on when rules apply

**Example use cases**:
- Architecture reviews
- Code guidance
- Strategic decisions

### Designing for Consistency

**When to apply**: Tasks requiring standardized output

**Design approach**:
- Templates and scaffolds
- Pattern matching for structure
- Validation against specifications

**Example use cases**:
- Code generation
- Documentation templates
- Production patterns

### Designing for Coordination

**When to apply**: Tasks involving multiple workflows

**Design approach**:
- Routing logic between processes
- State management and tracking
- Pipeline sequencing

**Example use cases**:
- Multi-step deployments
- Parallel processing
- Complex orchestrations

### Designing for Simplicity

**When to apply**: Direct, straightforward tasks

**Design approach**:
- 3 steps or fewer
- Inline guidance in SKILL.md
- Minimal overhead

**Example use cases**:
- Simple transformations
- Quick conversions
- Straightforward utilities

---

## Description Engineering

The `description` field is critical for skill activation.

**Format**: `"{{CAPABILITY}}. Use when {{TRIGGERS}}. Do not use for {{EXCLUSIONS}}."`

**Three components**:
1. **Capability**: What the skill does
2. **Triggers**: When to use it (specific scenarios)
3. **Negative**: What NOT to use it for

**Bad**:
```yaml
description: Helps with PDFs.
```

**Good**:
```yaml
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF documents, extracting data from forms, or converting PDFs to other formats. Do not use for viewing PDFs or simple PDF reading.
```

**Key principles**:
- Use **third person**: "This skill should be used when..."
- Include **specific trigger phrases**: "create X", "configure Y"
- Mention **file extensions**: .pdf, .xlsx, .csv
- Include **negative constraints**: "Do not use for..."

---

## Progressive Disclosure

**Core concept**: Load heavy content only when needed.

**In SKILL.md**:
```markdown
## Resources

### For detailed patterns
See [references/patterns.md](references/patterns.md)

### For advanced workflows
See [references/advanced.md](references/advanced.md)

### For examples
See [examples/basic.md](examples/basic.md)
```

**Loading triggers**:
```markdown
## Complex Workflow

**Before proceeding**, read entire file:
Example: [references/complex-workflow.md](references/complex-workflow.md)

Then execute the following steps...
```

**Anti-loading**:
```markdown
## Quick Task

**Do NOT load references** for this simple task.

Execute directly:
1. Step 1
2. Step 2
```

---

## Best Practices

### 1. Delta Standard

Only provide context Claude cannot infer.

**Bad**: Explaining what PDFs are or how `import` works

**Good**: Specific column mappings for proprietary formats

**Test**: "Would any agent know this?" If yes, don't write it.

### 2. Native-First Principle

**Question**: "Can the agent do this with existing tools?"

If yes → Let the agent write it directly

If no → Provide a script (rare)

**Example**: Don't create scripts for reading files — use native Read tool.

### 3. Trust the Agent's Native Capacities

The agent already knows how to:
- Read and write files
- Run bash commands
- Parse data structures
- Format output
- Organize directories
- Search and analyze code

**Don't teach basics**. Focus on domain-specific expertise.

### 4. Description Quality

**Bad**: `description: Helps with coding`

**Good**: `description: Refactors React components using hooks and TypeScript. Use when modernizing class components or improving component structure. Do not use for initial component creation.`

### 5. Anti-Patterns

**The "Kitchen Sink"**: One skill tries to do everything
**The "Tutorial"**: Teaches basics instead of providing expertise
**The "Orphan References"**: References exist but are never loaded
**The "Script Envy"**: Scripts for operations Claude handles natively

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: The Tutorial

**Symptom**: Explains what PDF is, how Python works, basic library usage

**Fix**: Claude already knows this. Focus on expert decisions, trade-offs, anti-patterns.

### Anti-Pattern 2: The Dump

**Symptom**: SKILL.md is 800+ lines with everything included

**Fix**: Core routing in SKILL.md (<300 lines). Heavy content in references/.

### Anti-Pattern 3: The Orphan References

**Symptom**: References directory exists but files are never loaded

**Fix**: Add "MANDATORY - READ ENTIRE FILE" at workflow decision points.

### Anti-Pattern 4: The Vague Description

**Symptom**: `description: Provides guidance for working with hooks`

**Fix**: `description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", or mentions hook events.`

### Anti-Pattern 5: The Ask-First Skill

**Symptom**: Skill immediately asks user questions before any exploration

**Fix**: Implement "explore first" — use read/grep/inspection to resolve ambiguity

**Test**: Can the skill handle 80-95% of cases without questions?

---

## Quick Validation Checklist

### Frontmatter
- [ ] `name` is lowercase, ≤64 chars, gerund form
- [ ] `description` uses third person
- [ ] `description` includes specific trigger phrases
- [ ] `description` states what NOT to use for
- [ ] `description` mentions file extensions (.pdf, .xlsx)

### Content
- [ ] SKILL.md uses imperative/infinitive form
- [ ] SKILL.md is focused and lean (<300 lines ideal)
- [ ] No basic explanations Claude already knows
- [ ] Expert knowledge is front and center
- [ ] Clear design approach is followed

### Structure
- [ ] Core workflow in SKILL.md
- [ ] Heavy content in references/
- [ ] Examples in examples/
- [ ] Complex operations in scripts/
- [ ] Loading triggers embedded where needed

### Progressive Disclosure
- [ ] Tier 1: Metadata is discoverable
- [ ] Tier 2: SKILL.md is complete
- [ ] Tier 3: Resources referenced with triggers

### Autonomy Design
- [ ] Skill can complete without questions in 80-95% of expected cases
- [ ] Has "explore first" path (read/grep) before "ask"
- [ ] Has explicit success/stop criteria
- [ ] Fork pattern chosen matches use case (Router+Worker / Single / Skill+Command)
- [ ] Knows when to recommend command for explicit control

---

## When in Doubt

> **Skills are the PRIMARY customization layer.**

For most customization needs:
1. Start with **CLAUDE.md** for project norms
2. Add **one Skill** for domain expertise
3. Only add commands/subagents if proven necessary

**Remember**: A minimal pack (CLAUDE.md + Skill) handles 80% of customization needs.
