---
name: skill-builder
description: Build new agent skills. Use when creating diagnostic frameworks, CLI tools, or data-driven generators that follow the established skill patterns.
---

# Skill-Builder: Meta-Skill for Creating Skills

You help create new agent skills that follow established patterns. Your role is to guide skill design, generate scaffolding, and validate completeness.

## Core Principle

**Skills are diagnostic frameworks with tools, not feature checklists.**

A skill diagnoses a problem space, identifies states, and provides interventions. Scripts provide randomization and structure; the LLM provides judgment. Each does what it's best at.

## Skill Anatomy

Every skill has these components:

```
skill-name/
├── SKILL.md           # Diagnostic framework + documentation
├── scripts/           # Deno TypeScript tools
│   └── *.ts
├── data/              # JSON datasets (if needed)
│   └── *.json
└── references/        # Supporting documentation (optional)
    └── *.md
```

### SKILL.md Structure

```markdown
---
name: skill-name
description: One sentence starting with action verb
license: MIT
metadata:
  author: your-name
  version: "1.0"
  maturity_score: [0-20]                          # Optional
---

# Skill Name: Subtitle

You [role description]. Your role is to [specific function].

## Core Principle
**Bold statement capturing diagnostic essence.**

## The States
### State X1: Name
**Symptoms:** What the user notices  
**Key Questions:** What to ask  
**Interventions:** What framework/tool to apply  

[Repeat for each state]

## Diagnostic Process
1. Step one
2. Step two
...

## Key Questions
### For Category A
- Question?
- Question?

## Anti-Patterns
### The [Problem Name]
**Problem:** Description  
**Fix:** Solution  

## Available Tools
### script.ts
Description of what it does.
```bash
deno run --allow-read scripts/script.ts [args]
```

## Example Interaction
**User:** "Problem description"  
**Your approach:**
1. Action
2. Action

## What You Do NOT Do
- List of boundaries
- Things the skill never does

## Integration Graph

### Inbound (From Other Skills)
| Source Skill | Source State | Leads to State |
|--------------|--------------|----------------|
| [skill] | [state] | [state] |

### Outbound (To Other Skills)
| This State | Leads to Skill | Target State |
|------------|----------------|--------------|
| [state] | [skill] | [state] |

### Complementary Skills
| Skill | Relationship |
|-------|--------------|
| [skill] | [how they relate] |
```

## Skill Types

### Type D: Diagnostic Skills
**Purpose:** Identify problems, recommend interventions  
**Pattern:** States → Questions → Interventions  
**Examples:** story-sense, worldbuilding, conlang  

Key characteristics:
- Problem states with symptoms/questions
- Cross-references to intervention tools
- "What you do NOT do" section enforces boundaries
- Integration tables mapping to other skills

### Type G: Generator Skills
**Purpose:** Produce structured output from parameters  
**Pattern:** Parameters → Generation → Output  
**Examples:** Functions in story-sense, phonology in conlang  

Key characteristics:
- Input parameters with defaults
- Randomization with optional seeding
- Multiple output formats (human, JSON, brief)
- Quality levels (starter → comprehensive)

### Type U: Utility Skills
**Purpose:** Support other skills, build infrastructure  
**Pattern:** Input → Analysis/Transformation → Report  
**Examples:** list-builder, skill-builder  

Key characteristics:
- Meta-level operation
- Quality metrics and validation
- Templates and scaffolding
- Cross-skill applicability

### Type O: Orchestrator Skills
**Purpose:** Coordinate multiple skills into autonomous workflows  
**Pattern:** Input → Multi-Pass Evaluation Loop → Polished Output  
**Examples:** chapter-drafter  

Key characteristics:
- Invokes multiple sub-skills sequentially
- Iterates until quality thresholds met
- Accumulates context across work units
- Operates autonomously without human checkpoints

Required frontmatter:
```yaml
metadata:
  orchestrates:           # Sub-skills to coordinate
    - skill-one
    - skill-two
  pass_order:             # Evaluation sequence
    - skill-one
    - skill-two
  pass_weights:           # Weight per skill (sum to 100)
    skill-one: 50
    skill-two: 50
  max_iterations: 3       # Per-pass iteration limit
  global_max_iterations: 50  # Total cap
```

See `skills/fiction/orchestrators/README.md` for architectural details.

## Skill Maturity Scoring (24 points)

Skills are evaluated on a 24-point scale parallel to the framework 24-point system.

### Completeness (11 points)

| Check | Points | Criteria |
|-------|--------|----------|
| Core Principle | 1 | Bold statement capturing diagnostic essence |
| States | 2 | 3-7 states for diagnostic skills (N/A for generator/utility) |
| State Components | 2 | Symptoms, Key Questions, Interventions for each state |
| Diagnostic Process | 1 | Step-by-step process documented |
| Anti-Patterns | 2 | 3+ anti-patterns with Problem/Fix structure |
| Examples | 2 | 2+ worked examples showing skill application |
| Boundaries | 1 | "What You Do NOT Do" section |

### Quality (5 points)

| Check | Points | Criteria |
|-------|--------|----------|
| Self-Contained | 1 | Can be used without reading other skills |
| Type+Mode Declared | 1 | Required frontmatter fields present |
| State Naming | 1 | Consistent state prefix matching skill abbreviation |
| Integration Map | 1 | Documents connections to other skills |
| Tools Documented | 1 | All scripts have usage documentation |

### Usability (4 points)

| Check | Points | Criteria |
|-------|--------|----------|
| Output Persistence | 1 | Customized (not boilerplate) persistence section |
| Progressive Disclosure | 1 | Quick reference section for at-a-glance use |
| Decision Tree | 1 | Routing logic for common scenarios |
| Actionability | 1 | Clear next steps for each diagnosis |

### Execution Intelligence (4 points) — NEW

| Check | Points | Criteria |
|-------|--------|----------|
| Reasoning Requirements | 1 | Specifies when extended thinking benefits the task |
| Execution Strategy | 1 | Documents sequential vs. parallelizable work |
| Subagent Guidance | 1 | Identifies when to spawn specialized subagents |
| Context Management | 1 | Documents token footprint and optimization strategies |

### Maturity Levels

| Level | Score | Description |
|-------|-------|-------------|
| Draft | 0-8 | Missing core elements |
| Developing | 9-14 | Functional but incomplete |
| Stable | 15-20 | Production-ready |
| Battle-Tested | 21-24 | Has case studies + full execution intelligence |

## Required Metadata

### Type (Required)

Every skill must declare its type in frontmatter:

```yaml
metadata:
```

| Type | Definition | Required Sections |
|------|------------|-------------------|
| **diagnostic** | Identifies problems, recommends interventions | States, Diagnostic Process, Anti-Patterns |
| **generator** | Produces structured output from parameters | Parameters, Generation Logic, Output Formats |
| **utility** | Supports other skills, builds infrastructure | Process, Templates, Validation |
| **orchestrator** | Coordinates multiple skills into autonomous workflows | Orchestration Loop, Pass Criteria, Iteration Limits |

### Mode (Required)

Every skill must declare its mode in frontmatter:

```yaml
metadata:
```

| Mode | Definition | User Relationship |
|------|------------|-------------------|
| **diagnostic** | Identifies problem states and recommends | Agent diagnoses, user decides |
| **assistive** | Guides without producing content | Agent asks questions, user creates |
| **collaborative** | Works alongside user | Agent produces, user guides |
| **evaluative** | Assesses existing work | Agent reviews, user responds |
| **application** | Operates in real-time context | Agent runs, user participates |
| **generative** | Creates output from parameters | Agent produces, user selects |

**Compound modes** (e.g., `diagnostic+generative`) are allowed when skills perform multiple functions.

### Optional Metadata

```yaml
metadata:
  maturity_score: 15
```

## State Naming Convention

States must follow a consistent naming pattern:

**Convention:** `{ABBREV}{NUMBER}: {State Name}`

**Rules:**
1. Abbreviation is 1-3 uppercase letters derived from skill name
2. Numbers start at 0 (for "no X exists" states) or 1
3. State names are descriptive, not just numbers
4. Sub-states use decimal notation (4.5, 5.75) when inserting between existing states

**Standard Abbreviations:**

| Skill | Abbreviation | Example |
|-------|--------------|---------|
| story-sense | SS | State SS1: Concept Without Foundation |
| dialogue | D | State D1: Identical Voices |
| conlang | L | State L1: No Language |
| worldbuilding | W | State W1: Backdrop World |
| revision | R | State R1: Overwhelmed |
| endings | E | State E1: Arbitrary Ending |
| character-arc | CA | State CA1: Static Character |
| scene-sequencing | SQ | State SQ1: Scene-Only Pacing |
| brainstorming | B | State B1: Convergent Ideas |
| research | RS | State RS1: No Research |
| requirements-analysis | RA | State RA1: Vague Requirements |
| system-design | SD | State SD1: No Architecture |
| chapter-drafter | CD | (Orchestrator - uses pass scores, not states) |

New skills should claim an unused abbreviation and document it here.

## Integration Graph Requirements

Every skill must document its connections to other skills.

**Required Format:**

```markdown
## Integration Graph

### Inbound (From Other Skills)
| Source Skill | Source State | Leads to State |
|--------------|--------------|----------------|
| story-sense | SS5: Plot Without Purpose | D4: No Subtext |

### Outbound (To Other Skills)
| This State | Leads to Skill | Target State |
|------------|----------------|--------------|
| D6: Pacing Mismatch | scene-sequencing | SQ2: Sequel Missing |

### Complementary Skills
| Skill | Relationship |
|-------|--------------|
| character-arc | Voice reflects transformation |
| worldbuilding | Speech reflects culture |
```

**Requirements:**
- Minimum 1 inbound OR 1 outbound connection
- Complementary skills list for context
- State-level specificity (not just skill-to-skill)
- Bidirectional documentation (if A references B, B should reference A)

## Execution Intelligence Requirements

Skills should document how they're best executed by Claude Code.

### Reasoning Requirements Section

Document when extended thinking (`ultrathink`) benefits the skill:

```markdown
## Reasoning Requirements

### Standard Reasoning
- Initial diagnosis and symptom matching
- Simple state identification
- Script execution and output interpretation

### Extended Reasoning (ultrathink)
Use extended thinking for:
- Multi-framework synthesis - [Why: requires holding multiple models simultaneously]
- Complex worldbuilding systems - [Why: many interdependent variables]
- Cascade analysis across states - [Why: second-order effects compound]

**Trigger phrases:** "deep analysis", "comprehensive review", "multi-framework synthesis"
```

**Why this matters:** LLMs have a completion reward bias—they rush toward visible goals. Extended thinking allocates reasoning time before output, improving quality on complex tasks. This aligns with the LLM Process Design Framework principle.

### Execution Strategy Section

Document sequential vs. parallel work:

```markdown
## Execution Strategy

### Sequential (Default)
- Diagnosis must complete before intervention
- State identification before framework selection

### Parallelizable
- Multiple script runs (entropy + functions) can run concurrently
- Research across multiple frameworks can parallelize
- Use when: Tasks are independent and can merge results

### Subagent Candidates
| Task | Agent Type | When to Spawn |
|------|------------|---------------|
| Codebase exploration | Explore | When skill needs project context |
| Framework research | general-purpose | When synthesizing across 3+ frameworks |
```

### Context Management Section

Document token usage and optimization:

```markdown
## Context Management

### Approximate Token Footprint
- **Skill base:** ~2k tokens
- **With full state definitions:** ~4k tokens
- **With scripts inline:** ~8k tokens (avoid unless debugging)

### Context Optimization
- Load scripts on-demand rather than including inline
- Reference framework documentation by name rather than embedding
- Use Quick Reference section for common cases

### When Context Gets Tight
- Prioritize: Current state diagnosis and immediate intervention
- Defer: Integration graph, full anti-patterns list
- Drop: Script source code, historical examples
```

## Anti-Pattern Requirements

Every skill must document common mistakes.

**Minimum Requirements:**
- 3 anti-patterns for diagnostic skills
- 2 anti-patterns for generator/utility skills

**Required Structure:**

```markdown
### The {Anti-Pattern Name}
**Pattern:** What the problematic behavior looks like  
**Problem:** Why this causes harm  
**Fix:** How to resolve it  
**Detection:** [Optional] How to recognize this happening  
```

**Common Anti-Pattern Categories:**

| Category | Example Names |
|----------|---------------|
| Scope Creep | The Kitchen Sink, The Mission Creep |
| Missing Depth | The Surface Treatment, The Checklist |
| Wrong Level | The Bottom-Up Edit, The Premature Optimization |
| User Relationship | The Puppet Master, The Passive Recipient |
| Integration | The Orphan Skill, The Boundary Ignorer |

## Script Patterns

### Standard Script Template

```typescript
#!/usr/bin/env -S deno run --allow-read

/**
 * Script Name
 *
 * Description of what it does.
 *
 * Usage:
 *   deno run --allow-read script.ts [args]
 */

// === INTERFACES ===
interface ResultType {
  field: string;
  // ...
}

// === DATA ===
const DATA: Record<string, string[]> = {
  category: ["item1", "item2"],
};

// === UTILITIES ===
function randomFrom<T>(arr: T[], count: number = 1): T[] {
  const shuffled = [...arr].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, arr.length));
}

// === CORE LOGIC ===
function generate(/* params */): ResultType {
  // Generation logic
}

// === FORMATTING ===
function formatResult(result: ResultType): string {
  const lines: string[] = [];
  // Format output
  return lines.join("\n");
}

// === MAIN ===
function main(): void {
  const args = Deno.args;

  // Help
  if (args.includes("--help") || args.includes("-h")) {
    console.log(`Script Name

Usage:
  deno run --allow-read script.ts [options]

Options:
  --flag     Description
  --json     Output as JSON
`);
    Deno.exit(0);
  }

  // Parse arguments
  const flagIndex = args.indexOf("--flag");
  const flagValue = flagIndex !== -1 ? args[flagIndex + 1] : null;
  const jsonOutput = args.includes("--json");

  // Skip indices for positional arg detection
  const skipIndices = new Set<number>();
  if (flagIndex !== -1) {
    skipIndices.add(flagIndex);
    skipIndices.add(flagIndex + 1);
  }

  // Find positional argument
  let positionalArg: string | null = null;
  for (let i = 0; i < args.length; i++) {
    if (!args[i].startsWith("--") && !skipIndices.has(i)) {
      positionalArg = args[i];
      break;
    }
  }

  // Generate
  const result = generate(/* params */);

  // Output
  if (jsonOutput) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(formatResult(result));
  }
}

main();
```

### Argument