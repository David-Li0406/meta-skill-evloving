# Skill Structure

**Core reference for Qara skill structure requirements and canonical template**

This document defines the mandatory structural requirements for all Qara skills and provides the canonical SKILL.md template. All skills must follow these rules for proper routing and discoverability.

**See also:**
- [skill-archetypes.md](./skill-archetypes.md) - Directory structure patterns for Minimal, Standard, and Complex skills
- [routing-patterns.md](./routing-patterns.md) - The 4-level routing hierarchy and routing patterns

---

## MANDATORY SKILL STRUCTURE REQUIREMENTS

**READ THIS FIRST - FAILURE TO FOLLOW THESE RULES BREAKS THE ENTIRE SKILL SYSTEM**

### Rule 1: EVERY Workflow MUST Be Routed in SKILL.md

**MANDATORY:** Create a "Workflow Routing (SYSTEM PROMPT)" section immediately after the YAML frontmatter.

**For EVERY workflow file in the skill:**
```markdown
When user requests [action]:
Examples: "actual user phrases", "variations they say", "synonyms"
→ READ: ${PAI_DIR}/skills/[skill]/workflows/[workflow-file].md
→ EXECUTE: Brief description of what to do
```

**If you don't route a workflow, it will NEVER be used. Period.**

### Rule 2: EVERY Secondary File MUST Be Linked from Main Body

**MANDATORY:** Every .md file in your skill directory MUST be referenced in the main body sections of SKILL.md.

**For each file:**
- Link it from the appropriate Extended Context section
- Include the file path
- Explain what it contains
- Explain when to use it

**If you don't link a file, it's invisible and useless.**

### Rule 3: Workflow Routing Goes FIRST in SKILL.md Content

**Structure order (MANDATORY):**
1. YAML frontmatter (name, description)
2. **Workflow Routing (SYSTEM PROMPT)** section ← THIS GOES FIRST
3. "When to Activate This Skill" section
4. Main body content / Extended Context sections

**Why:** Claude sees workflow routing immediately when skill loads.

### Consequences of Violating These Rules

❌ **No workflow routing** = Workflows never execute
❌ **No file links** = Files never discovered
❌ **Wrong order** = Claude misses critical routing logic

**These aren't suggestions. These are requirements.**

---

## Canonical SKILL.md Structure Template

**For a regular skill (not CORE), this is the complete structure:**

```markdown
---
name: skill-name
description: |
  What this skill does and when to use it.

  USE WHEN: user says "trigger phrase", "another trigger", or any related request.
---

## Workflow Routing (SYSTEM PROMPT)

**When user requests [action 1]:**
Examples: "actual user phrases", "variations", "synonyms"
→ **READ:** ${PAI_DIR}/skills/skill-name/workflows/workflow1.md
→ **EXECUTE:** What to do with this workflow

**When user requests [action 2]:**
Examples: "actual user phrases", "variations", "synonyms"
→ **READ:** ${PAI_DIR}/skills/skill-name/workflows/workflow2.md
→ **EXECUTE:** What to do with this workflow

[Route EVERY workflow file in workflows/ directory]

---

## When to Activate This Skill

- Condition 1 for activating this skill
- Condition 2 for activating this skill
- Specific triggers and use cases

---

## Extended Context / Main Body

[Detailed information about using the skill]
[Links to any secondary documentation files]
[Examples, configuration, additional context]
```

**Key Points:**
1. **YAML description** = What skill does (appears in system prompt)
2. **Workflow Routing** = First section, routes EVERY workflow
3. **When to Activate** = Detailed activation conditions
4. **Main Body** = Everything else

**CORE skill is different** (it's the base context loaded at every session start), but for regular skills this is the mandatory structure.

---

## YAML Frontmatter Fields (CC 2.1.x)

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Skill identifier (lowercase, hyphenated) |
| `description` | What skill does, including USE WHEN triggers |

### Optional Fields

| Field | Values | Description |
|-------|--------|-------------|
| `context` | `fork` or `same` | Execution context. `fork` = isolated subagent (default for most skills), `same` = main conversation |
| `model` | `sonnet`, `opus`, `haiku` | Model routing for cost/performance optimization. Use `sonnet` for compute-intensive skills |
| `agent` | Agent name from `.claude/agents/` | Specify which agent definition to use when executing this skill (CC 2.1.x feature) |

### Example with All Fields

```yaml
---
name: research
context: fork
model: sonnet
agent: researcher
description: |
  Deep research and analysis skill.

  USE WHEN: user says "research", "investigate", "find information about"
---
```

### When to Use Each Field

- **`context: fork`** - Most skills should use this for isolated execution
- **`context: same`** - Only for skills that modify main conversation context (like CORE)
- **`model: sonnet`** - For skills needing quality reasoning (research, analysis, content creation)
- **`model: haiku`** - For simple, fast skills (validation, formatting)
- **`agent`** - When skill requires specific agent capabilities (rarely needed)

---

## What is a Skill?

In Qara's architecture, **skills are the primary organizational primitive** - self-contained packages of context, workflows, and capabilities that enable specialized functionality.

**Skills are NOT just documentation.** They are **active orchestrators** that:
- Route user requests to appropriate workflows
- Provide context for task execution
- Manage domain-specific state and tools
- Integrate with external services and applications

## What is Routing?

**Routing** is the multi-level process of directing a user request from initial input to final execution:

```
User Request
    ↓
System Prompt Routing (Level 1: Which skill?)
    ↓
Skill Activation (Level 2: Should this skill load?)
    ↓
Internal Context Routing (Level 3: What section of SKILL.md?)
    ↓
Workflow Invocation (Level 4: Which specific procedure?)
    ↓
Execution
```

This guide explains **how to structure skills** to enable effective routing at all levels.

---

## Naming Conventions

### Files

- **Root skill definition:** `SKILL.md` (UPPERCASE, singular)
- **Root documentation:** `UPPERCASE.md` (METHODOLOGY, ARCHITECTURE, etc.)
- **Workflows:** `kebab-case.md` (lowercase with hyphens)
- **Migrations:** `MIGRATION-YYYY-MM-DD.md`
- **Scripts:** `kebab-case.ts` or `kebab-case.sh`

### Directories

- **Single word:** `lowercase` (workflows, tools, state, testing)
- **Compound:** `lowercase-with-hyphens` (design-standards, consulting-templates)
- **Always plural for containers:** workflows, references, tools, assets
- **Always singular for specific items:** state, documentation

### Special Cases

- `.archive/` - Hidden directory with dated subdirectories
- `documentation/` vs `references/` - documentation is nested, references is flat
- Backup files: `.bak`, `.bak2` suffixes (prefer archiving instead)

---

## Workflow File Structure

**Standard workflow format:**

```markdown
# Workflow Name

**Purpose:** One-line description of what this workflow does

**When to Use:**
- Specific trigger condition 1
- Specific trigger condition 2

**Prerequisites:**
- Required tool or configuration
- Required state or artifact

**Steps:**

1. First action
   - Sub-step or detail
   - Expected outcome

2. Second action
   - Sub-step or detail
   - Expected outcome

3. Final action
   - Verification step
   - Success criteria

**Outputs:**
- What this workflow produces
- Where outputs are stored

**Related Workflows:**
- next-workflow.md - What to do after this
- alternative-workflow.md - Alternative approach
```

**Code + Markdown Workflows:**

When workflow includes automation:

```
workflows/
├── post-to-x.md        # Human-readable documentation
└── post-to-x.ts        # Executable implementation
```

The .md file explains WHAT and WHEN, the .ts file provides HOW (executable code).
