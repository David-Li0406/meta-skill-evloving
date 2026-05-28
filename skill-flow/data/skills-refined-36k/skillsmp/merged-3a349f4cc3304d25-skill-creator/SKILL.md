---
name: skill-creator
description: Use this skill when creating or editing skills for the ai-coding-config repository.
---

# Skill Creator

## Overview

Skills are reusable reference guides for proven techniques, patterns, and tools. Write them as intelligent companions would read them - focused on goals and outcomes, not rigid procedures.

## When to Use

Create skills for techniques that weren't intuitively obvious, patterns you'd reference across projects, or broadly applicable approaches. Skip skills for one-off solutions, well-documented standard practices, or project-specific conventions.

## Core Pattern

Every skill has YAML frontmatter and markdown content:

```markdown
---
name: skill-name-with-hyphens
description: Use when [triggering conditions] - [what it does and how it helps]
---

# Skill Name

## Overview

What is this? Core principle in 1-2 sentences.

## When to Use

Clear triggers and symptoms. When NOT to use.

## Core Pattern

Show desired approach with examples. Describe alternatives in prose.

## Common Pitfalls

What goes wrong and how to avoid it.
```

### Writing Principles

- **Show, don't tell**: Demonstrate desired approaches with 5+ examples. Describe undesired alternatives in prose without code.
- **Focus on goals, not process**: Describe outcomes and constraints. Let the LLM figure out how to achieve them.
- **Positive framing**: Frame as "do this" not "avoid that." Focus on what success looks like.
- **Trust intelligence**: Assume the LLM can handle edge cases and variations. Specify boundaries, not decision trees.

### File Organization

Self-contained (preferred):
```
skill-name/
  SKILL.md    # Everything inline
```

With supporting files (when needed):
```
skill-name/
  SKILL.md           # Overview + patterns
  reference.md       # Heavy API docs (100+ lines)
  tool-example.ts    # Reusable code to adapt
```

### Optimize for Discovery

Use rich keywords: error messages, symptoms, tools, and synonyms. Put searchable terms in the description and throughout the content.

### Token Efficiency

Be concise:
- Frequently-loaded skills: under 200 words
- Other skills: under 500 words
- Reference external docs rather than duplicating them
- Use cross-references to other skills instead of repeating

### Quality Checklist

- Frontmatter with name and description (third-person, "Use when...")
- Clear overview with core principle
- Concrete "when to use" triggers
- Examples showing desired patterns (5+ for main approach)
- Goals and outcomes, not rigid procedures
- Positive framing (show what to do)
- Trust LLM intelligence (avoid over-prescription)
- Keywords for search throughout
- Common pitfalls addressed
- Self-contained in SKILL.md when possible

### Common Mistakes

- **Over-prescription**: Describe the goal, not the algorithm.
- **Showing anti-patterns**: Describe alternatives in prose instead.
- **Vague triggers**: Be specific about when to use.
- **First person**: Write "Use when..." not "I can help when..."
- **Missing keywords**: Include terms someone would actually search for.