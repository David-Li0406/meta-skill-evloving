---
name: skill-creator
description: This skill should be used when the user asks to "create a skill", "add a new command", "make a custom agent", "extend Claude capabilities", or wants to add automation to their workflow.
---

# /skill-creator

Create effective skills and agents that extend Claude Code capabilities.

## Reference

See `.claude/AGENT_CLAUDE.md` for comprehensive guidelines on skill and agent development.

## Quick Start

### Create a Skill

1. **Create directory**: `.claude/skills/<skill-name>/`
2. **Add SKILL.md** with YAML frontmatter and instructions
3. **Test**: Invoke with `/skill-name` or describe the trigger scenario

### Create an Agent

1. **Create file**: `.claude/agents/<agent-name>.md`
2. **Add YAML frontmatter** with name, description (with examples), and tools
3. **Write system prompt** defining persona, responsibilities, and output format

## Skill Template

```markdown
---
name: skill-name
description: This skill should be used when the user asks to "trigger phrase 1", "trigger phrase 2", or "trigger phrase 3". Be specific about when to activate.
disable-model-invocation: true # Set true for side effects (deploy, commit)
allowed-tools: Read, Grep, Glob # Restrict tools if needed
---

# /skill-name

Brief description of what this skill does.

## Instructions

1. First step - what to do
2. Second step - what to do
3. Third step - what to do

## Examples

Input: `$ARGUMENTS`
Expected output: ...
```

## Agent Template

```markdown
---
name: agent-name
description: Use this agent when [specific conditions]. Examples:

<example>
Context: [Situation]
user: "[Request]"
assistant: "[Response pattern]"
<commentary>
[Why this agent fits]
</commentary>
</example>

tools: ["Read", "Grep", "Glob"]
model: sonnet
---

You are [expert persona with domain knowledge].

**Core Responsibilities:**

1. [Primary task]
2. [Secondary task]

**Process:**

1. [Step one]
2. [Step two]

**Output Format:**
[What to return]
```

## Best Practices Checklist

**Skills:**

- [ ] Description uses third-person ("This skill should be used when...")
- [ ] Includes exact trigger phrases in quotes
- [ ] Has `disable-model-invocation: true` if it has side effects
- [ ] Instructions are step-by-step and actionable
- [ ] Under 500 lines (use supporting files for details)

**Agents:**

- [ ] Description includes `<example>` blocks with `<commentary>`
- [ ] Tools array contains only what's needed
- [ ] System prompt uses second person ("You are...")
- [ ] Defines clear output format
- [ ] Has quality criteria or success conditions
