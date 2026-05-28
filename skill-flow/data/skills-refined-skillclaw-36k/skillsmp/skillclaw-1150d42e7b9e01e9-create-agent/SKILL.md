---
name: create-agent
description: Use this skill when creating and configuring custom agents or subagents for Claude Code, ensuring they are tailored for specific tasks and contexts.
---

# Skill Body

## Overview

This skill provides a comprehensive guide for creating and configuring agents and subagents in Claude Code. It covers the necessary structure, tools, models, and best practices to ensure effective agent design.

## Quick Start: Create an Agent

To create a new agent, use the following template:

```markdown
---
name: my-agent
description: What this agent does. Use PROACTIVELY for [tasks].
tools: Read, Write, Edit  # Optional
model: sonnet             # Optional
skills: skill1, skill2    # Optional
---

You are an expert in [domain].

## Core Expertise
- Skill 1
- Skill 2

## Workflow

When invoked:
1. Step 1
2. Step 2
3. Deliver results

## Quality Checklist
- ✅ Check 1
- ✅ Check 2
```

## Required Fields

- **name**: Unique identifier (lowercase-with-hyphens)
- **description**: When to use this agent (natural language)

## Optional Fields

- **tools**: Specific tools (or omit to inherit all)
- **model**: sonnet/opus/haiku/inherit (default: sonnet)
- **skills**: Auto-load reference documentation
- **permissionMode**: Permission handling strategy

## Agent Archetypes

1. **Analyzer/Reviewer**: Reviews and provides feedback.
2. **Generator/Creator**: Creates new code/content.
3. **Debugger/Fixer**: Fixes problems.
4. **Researcher/Explorer**: Searches and gathers information.
5. **Tester/QA**: Tests and verifies.

## System Prompt Sections

Essential sections for agent system prompts:

1. **Core Expertise**: What the agent knows.
2. **Workflow**: Step-by-step process.
3. **Patterns**: Common code patterns.
4. **Best Practices**: Do's and don'ts.
5. **Quality Checklist**: Verification steps.

## Tool Selection

| Tools | Use For |
|-------|---------|
| Read, Grep, Glob, Bash | Analyzers, reviewers |
| Read, Write, Edit, Bash | Generators, creators |
| (omit field) | Full access, general-purpose |

## Model Selection

| Model | Use When |
|-------|----------|
| **sonnet** | General tasks, balanced |
| **opus** | Complex reasoning required |
| **haiku** | Fast searches, simple tasks |
| **inherit** | Match main conversation |

## Activation Strategies

### Proactive (Automatic)

When creating subagents, consider the following:

- **Context Preservation**: Subagents operate in their own context window.
- **Specialized Expertise**: Use subagents for tasks requiring focused instructions.
- **Tool Permissions**: Different tasks may need different tool permissions.

## Formatting Rules for Subagents

Subagents must follow strict formatting rules to ensure they load correctly:

- **Single-line description**: Must be one line, no `\n`.
- **No literal `\n`**: Use actual newlines in the body.
- **Valid models only**: Use `sonnet`, `opus`, `haiku`, or `inherit`.

## Example of Creating a Subagent

```markdown
---
name: my-subagent
description: Handles specific tasks related to [task].
tools: Read, Write
model: sonnet
---

You are a specialized subagent for [task].
When invoked:
1. Step 1
2. Step 2
3. Deliver results
```

## Conclusion

Use this skill to effectively create and configure agents and subagents tailored to your specific needs in Claude Code, ensuring they are optimized for their intended tasks.