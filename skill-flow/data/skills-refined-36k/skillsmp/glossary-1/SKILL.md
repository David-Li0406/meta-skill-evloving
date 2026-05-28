---
name: glossary
description: Add domain terms to project glossary in the Obsidian vault. Use when defining new terms, clarifying jargon, documenting domain concepts, or when unfamiliar terminology appears in requirements.
---

# Glossary

Add domain terms to project glossaries in the Obsidian vault.

## When to Use

- New domain term encountered during planning
- Jargon needs clarification for the team
- Documenting ubiquitous language for a bounded context
- User mentions unfamiliar terminology

## Vault Location

Glossaries live in project folders:
`~/Documents/Notes/Projects/<YYYY[-MM] Project>/Glossary.md`

## Workflow

### 1. Find Project Glossary

```bash
# Find glossary file for a project
fd -t f -i "Glossary" ~/Documents/Notes/Projects/*<project>*/
```

### 2. Check for Existing Term

```bash
# Search for term in glossary
rg -i "<term>" ~/Documents/Notes/Projects/*<project>*/Glossary.md
```

### 3. Add Term

If term doesn't exist, add using the format below.

## Glossary Entry Format

```markdown
## Term Name

**Definition:** Clear, concise definition in plain language.

**Context:** Where/how this term is used in the project.

**Also known as:** Alternative names, abbreviations, or synonyms.

**Related:** [[Link to related terms or concepts]]

**Example:** Concrete example of the term in use.
```

## Minimal Entry

For simple terms:

```markdown
## Term Name

**Definition:** Clear, concise definition.
```

## Examples

### Domain Term

```markdown
## Roster

**Definition:** A scheduled assignment of workers to shifts over a defined period.

**Context:** Core concept in workforce management. A roster contains shift assignments for multiple workers across days/weeks.

**Also known as:** Schedule, rota, shift pattern

**Related:** [[Shift]], [[Worker]], [[Duty]]

**Example:** "The ward roster for January shows all nursing staff assignments."
```

### Technical Term

```markdown
## Idempotent

**Definition:** An operation that produces the same result whether executed once or multiple times.

**Context:** Important for API design and message handling. Retry-safe operations must be idempotent.

**Example:** HTTP PUT is idempotent (same resource state after multiple calls), POST is not.
```

### Abbreviation

```markdown
## MWL

**Definition:** Minimal Workforce Levels — the minimum staffing requirements for a shift or department.

**Context:** Used in Allocate/Optima systems to define required coverage.

**Related:** [[Shift]], [[Establishment]]
```

## Guidelines

1. **Plain language** — Avoid defining jargon with more jargon
2. **Project context** — Explain how the term is used in *this* project
3. **Link generously** — Connect to related terms and concepts
4. **Examples help** — Concrete examples clarify abstract definitions
5. **Keep current** — Update definitions as understanding evolves

## Integration with Planning

During the PLAN phase of XP workflow:

1. Note unfamiliar terms from requirements discussion
2. Ask user for definitions if unclear
3. Add terms to glossary before proceeding
4. Reference glossary terms in task descriptions
