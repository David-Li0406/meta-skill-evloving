---
name: agent-creator
description: Complete guide for creating Claude Code subagents including structure, patterns, archetypes, tools, models, and best practices. Use when creating new agents, designing agent systems, or understanding agent architecture.
---

# Agent Creator Skill

Comprehensive guide for creating professional Claude Code subagents.

## Quick Start: Create an Agent

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

## Agent Structure

### Required Fields
- **name**: Unique identifier (lowercase-with-hyphens)
- **description**: When to use this agent (natural language)

### Optional Fields
- **tools**: Specific tools (or omit to inherit all)
- **model**: sonnet/opus/haiku/inherit (default: sonnet)
- **skills**: Auto-load reference documentation
- **permissionMode**: Permission handling strategy

## Agent Archetypes

### 1. Analyzer/Reviewer
Reviews and provides feedback

```yaml
tools: Read, Grep, Glob, Bash
model: sonnet
```

### 2. Generator/Creator
Creates new code/content

```yaml
tools: Read, Write, Glob, Bash
model: sonnet
```

### 3. Debugger/Fixer
Fixes problems

```yaml
tools: Read, Edit, Bash
model: sonnet
```

### 4. Researcher/Explorer
Searches and gathers info

```yaml
tools: Read, Glob, Grep, Bash
model: haiku  # Fast
```

### 5. Tester/QA
Tests and verifies

```yaml
tools: Read, Write, Edit, Bash
model: sonnet
```

## System Prompt Sections

Essential sections for agent system prompts:

1. **Core Expertise**: What agent knows
2. **Workflow**: Step-by-step process
3. **Patterns**: Common code patterns
4. **Best Practices**: Do's and don'ts
5. **Quality Checklist**: Verification steps

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
```yaml
description: Use PROACTIVELY after code changes
description: MUST BE USED for all UI tasks
```

### Domain-Specific
```yaml
description: Expert React developer
# Auto-invoked for React tasks
```

## File Locations

```bash
# Project-level (priority 1)
.claude/agents/agent-name.md

# User-level (priority 2)
~/.claude/agents/agent-name.md
```

## Best Practices

✅ **Focused purpose** - Single responsibility  
✅ **Clear triggers** - When to activate  
✅ **Concrete examples** - Code patterns  
✅ **Quality checks** - Verification steps  
✅ **Right tools** - Minimal necessary  

❌ Too broad scope  
❌ Vague description  
❌ No examples  
❌ Missing quality checks  

## Quick Templates

### Code Reviewer
```markdown
---
name: code-reviewer
description: Reviews code. Use after changes.
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer.
When invoked: check quality, security, best practices.
```

### Component Creator
```markdown
---
name: component-creator
description: Creates components. Use for new features.
tools: Read, Write, Glob, Bash
skills: architecture-patterns
---

You are a component expert.
When invoked: generate following project patterns.
```

## References

See `references/agent-structure.md` for complete documentation on:
- YAML fields reference
- All agent archetypes
- Tool selection guide
- Skills integration
- Permission modes
- Multi-agent workflows
- Testing strategies
- Domain examples

## Workflow

1. Define purpose and trigger
2. Choose archetype
3. Select tools and model
4. Write system prompt
5. Add skills if needed
6. Test agent
7. Iterate based on usage
