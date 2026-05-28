# Skill Authoring Best Practices

Distilled from Anthropic's official documentation and real-world testing (updated Jan 2026).

---

## How Skills Are Actually Loaded

**Start by understanding the mechanism:**

Skills are loaded via **"match to description"** logic. When you send a message:
1. Copilot reads each skill's name + description (Level 1)
2. Evaluates whether your request matches
3. If matched, loads the SKILL.md body (Level 2) into context
4. Optionally loads Level 3 references if the skill instructions request them

**Key insight:** Your description is the "trigger surface." Write it carefully.

For detailed research on skill loading, discovery, and technical details, see:
**`SKILL_LOADING_RESEARCH.md`** in this directory.

---

## Core Principle: The Context Window is a Public Good

Your skill shares context with:
- System prompt
- Conversation history  
- Other skills' metadata
- The user's actual request

**Every token counts.** Be concise.

## The Golden Rule

> Default assumption: Claude is already very smart.
> Only add context Claude doesn't already have.

Before adding anything, ask:
- Does Claude already know this?
- Is this truly necessary for the task?
- Could this be in a reference file instead?

## Progressive Disclosure

Skills load in three levels:

1. **Metadata** (always loaded): `name` and `description` only
2. **SKILL.md body** (loaded when relevant): Core instructions
3. **Bundled files** (loaded on-demand): references/, scripts/, assets/

**Design for level 1.** Write descriptions that help Claude decide when to use the skill.

## Description Formula

A great description answers TWO questions:
1. What does this skill DO? (capabilities)
2. When should Claude USE it? (triggers)

### Good Example
```
Extract text and tables from PDF files, fill PDF forms, merge documents. 
Use when working with PDF documents or when the user mentions PDFs, forms, 
or document extraction.
```

### Bad Example
```
Helps with documents
```

## Body Structure

Keep SKILL.md focused. Recommended sections:

```markdown
# Skill Name

## When to Use
[Specific trigger conditions]

## Commands
[Executable commands with flags]

## Process
[Step-by-step workflow]

## Examples
[Concrete input/output examples]

## Boundaries
[What to always/never do]
```

## Size Guidelines

| Component | Guideline |
|-----------|-----------|
| SKILL.md body | < 500 lines |
| Estimated tokens | < 5000 |
| Individual reference files | Focused, single-topic |
| Total bundled content | Effectively unlimited (loaded on-demand) |

## The Two-Claude Method

Iterate using two instances:
- **Claude A**: Helps you write/refine the skill
- **Claude B**: Tests the skill with real tasks

Cycle:
1. Draft skill with Claude A
2. Test with Claude B on real tasks
3. Observe Claude B's behavior
4. Return to Claude A with observations
5. Refine and repeat

## Common Mistakes

❌ Over-explaining things Claude already knows
❌ Vague descriptions that don't trigger correctly
❌ Putting everything in SKILL.md
❌ Not including concrete examples
❌ Forgetting to set boundaries
❌ Using non-portable frontmatter fields

## Source Attribution

This document distills best practices from:
- [Anthropic Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Agent Skills Standard](https://agentskills.io)
