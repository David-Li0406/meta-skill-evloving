---
name: skill-builder
description: Use this skill when creating new agent skills that follow established patterns for diagnostic frameworks, CLI tools, or data-driven generators.
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
  domain: [fiction | research | agile-software | naming | etc.]
  type: diagnostic | generator | utility         # REQUIRED
  mode: diagnostic | assistive | collaborative | evaluative | application | generative  # REQUIRED
  maturity: draft | developing | stable | battle-tested  # Optional
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
| [skill] | [description] |
```