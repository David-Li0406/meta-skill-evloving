---
template: skill
name: {{SKILL_NAME}}
description: {{DESCRIPTION}}
recipes: []
generated: {{DATE}}
last_updated: {{DATE}}
---
# {{SKILL_NAME}}

[Brief description of what this skill does - ONE thing]

## When to Use

**Invoked by:** [Command, skill, or manual invocation pattern]

**Purpose:** [One sentence describing when to use this skill]

---

## Instructions

[Step-by-step instructions for the single task this skill performs]

### Step 1: [Action]

[Description of what to do in this step]

**Actions:**
- [Specific action]
- [Specific action]

**Tools:** [List tools used]

### Step 2: [Action]

[Description of what to do in this step]

**Actions:**
- [Specific action]
- [Specific action]

**Tools:** [List tools used]

---

## Gate (Optional)

> Use this section if the skill has a hard binary gate (pass/fail).
> Remove if the skill is purely procedural without blocking conditions.

**MUST provide:**
- [Required output or condition]

**BLOCKS if:**
- [Blocking condition]

---

## Output

[Description of what this skill produces]

**Format:** [Structure of output if applicable]

**Location:** [Where output is stored if applicable]

---

## Principle Alignment

> **S20: "Each skill does ONE thing"** - smaller containers, harder boundaries

**S20 Compliance:**
- [ ] This skill does ONE thing (describe what: _____________)
- [ ] Skill is atomic and cannot be decomposed further without losing coherence
- [ ] If multi-phase, justification provided below

**Related Principles:**
- [Reference to relevant S-sections, ADRs, or architectural principles]

---

## When Multi-Phase is Justified

> **DEFAULT: Skills should be single-phase.** The "Instructions" section above assumes a single task.
>
> Multi-phase design is **ONLY** justified when:
> 1. **Phases have fundamentally different pressure** (volumous vs tight per S20)
> 2. **Early exit is required** (fail fast before later phases - save work)
> 3. **Phases cannot be extracted to separate skills** due to tight coupling
>
> **MUST provide explicit rationale below if using multi-phase structure.**

**Justification for Multi-Phase:**

[If this skill has multiple phases, explain WHY they cannot be separate skills]

**Phase Structure:**

[Only include this section if justified above]

```
PHASE1 [volumous/tight] --> PHASE2 [volumous/tight] --> PHASE3 [volumous/tight]
       |                            |                            |
    [inhale]                    [exhale]                    [inhale]
```

### Phase 1: [Name]

**Goal:** [What this phase achieves]

**Pressure:** [volumous/tight] - [Why this pressure level]

**Actions:**
1. [Step]
2. [Step]

**Tools:** [List tools]

### Phase 2: [Name]

**Goal:** [What this phase achieves]

**Pressure:** [volumous/tight] - [Why this pressure level]

**Actions:**
1. [Step]
2. [Step]

**Tools:** [List tools]

---

## Composition Map (Optional)

> Use this section if the skill composes multiple tools or subagents.

| Phase/Step | Primary Tool | Optional Subagent | Output |
|------------|--------------|-------------------|--------|
| [Step 1] | [Tool] | [Agent if used] | [What's produced] |
| [Step 2] | [Tool] | [Agent if used] | [What's produced] |

---

## Quick Reference (Optional)

> Use this section for complex skills with decision trees.

| Phase/Step | Question to Ask | If NO |
|------------|-----------------|-------|
| [Step 1] | [Check] | [Action] |
| [Step 2] | [Check] | [Action] |

---

## Related

- **[Related skill]:** [How they compose or when to use instead]
- **[Command/Template]:** [Integration point]
- **[ADR/Spec]:** [Reference document]

---
