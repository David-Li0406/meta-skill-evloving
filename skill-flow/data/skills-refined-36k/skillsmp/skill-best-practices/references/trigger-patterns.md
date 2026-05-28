# Trigger Phrase Patterns

## Overview

Trigger phrases in the `description` field determine when Claude activates a skill. Effective triggers ensure skills load at the right time.

## Trigger Phrase Principles

### Be Specific and Concrete

List exact phrases users would say:

✅ **Good:**
```yaml
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", "validate tool use", or mentions hook events
(PreToolUse, PostToolUse, Stop).
```

❌ **Bad:**
```yaml
description: Use this skill for hook-related tasks.
```

### Cover Variations

Include different ways users might ask:

```yaml
description: This skill should be used when the user asks to "create a skill",
"write a new skill", "add a skill to my plugin", "how do I create SKILL.md",
"what are skill best practices", or mentions skill development, SKILL.md files,
or skill quality.
```

### Include Domain Context

Mention relevant concepts and terminology:

```yaml
description: This skill should be used when working with MCP servers,
mentions "add MCP integration", "configure stdio server", "SSE server",
or discusses Model Context Protocol, MCP tools, server authentication, or
MCP capabilities.
```

### Use Third Person

Always start with "This skill should be used when..."

✅ **Good:**
```yaml
description: This skill should be used when the user asks to...
```

❌ **Bad:**
```yaml
description: Use this skill when...
description: Load this for...
```

## Trigger Phrase Patterns

### Pattern 1: Action-Based Triggers

Focus on specific actions:

```yaml
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", "implement a PostToolUse hook", "validate hooks",
or "test hook scripts".
```

**Key verbs:** create, add, implement, validate, test, configure, setup

### Pattern 2: Question-Based Triggers

Include common question formats:

```yaml
description: This skill should be used when the user asks "how do I create a
skill", "what are skill best practices", "how do I write SKILL.md", "how do I
optimize a skill", or mentions skill development, trigger phrases, or skill
structure.
```

**Key formats:**
- "How do I..."
- "What are..."
- "How do I write..."
- "What's the best way to..."

### Pattern 3: Concept-Based Triggers

Mention domain concepts:

```yaml
description: This skill should be used when the user mentions "PDF rotation",
"PDF manipulation", "PDF editing", "merge PDF", "split PDF", or discusses PDF
processing, document transformation, or file operations.
```

### Pattern 4: Component-Based Triggers

For specific components:

```yaml
description: This skill should be used when the user asks to "create an agent",
"write agent frontmatter", "configure agent tools", "set agent model", or
mentions agent development, subagent creation, or agent capabilities.
```

## Comprehensive Examples

### Example 1: Hook Development

```yaml
---
name: Hook Development
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", "implement a PostToolUse hook", "validate tool use",
"add a Stop hook", or mentions hook events (PreToolUse, PostToolUse, Stop,
SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact,
Notification), hook scripts, or prompt-based hooks.
version: 0.1.0
---
```

**Why effective:**
- Specific actions (create, add, implement, validate)
- Lists all hook event types
- Mentions hook variants (scripts, prompt-based)
- Covers question patterns

### Example 2: Skill Development

```yaml
---
name: Skill Development
description: This skill should be used when the user asks to "create a skill",
"write a new skill", "add a skill to my plugin", "how do I create SKILL.md",
"what are skill best practices", "how do I optimize a skill", "improve skill
quality", or mentions skill development, SKILL.md files, trigger phrases,
progressive disclosure, or skill structure.
version: 0.1.0
---
```

**Why effective:**
- Action phrases (create, write, add)
- Question formats (how do I, what are)
- Domain concepts (SKILL.md, trigger phrases, progressive disclosure)
- Quality-related terms (optimize, improve)

### Example 3: MCP Integration

```yaml
---
name: MCP Integration
description: This skill should be used when the user asks to "add an MCP server",
"configure stdio server", "set up SSE server", "integrate with MCP", or
mentions Model Context Protocol, MCP servers, MCP tools, stdio, SSE, HTTP
WebSocket servers, or MCP capabilities.
version: 0.1.0
---
```

**Why effective:**
- Action phrases (add, configure, set up, integrate)
- Server types (stdio, SSE, HTTP, WebSocket)
- Protocol name (Model Context Protocol)
- Related concepts (tools, capabilities)

## Trigger Discovery Process

### Step 1: Brainstorm User Queries

List questions users might ask:

```
"How do I create a skill?"
"What's the best way to write SKILL.md?"
"How do I improve skill quality?"
"What are skill best practices?"
"How do I optimize triggers?"
```

### Step 2: Extract Key Phrases

Extract action phrases and concepts:

```
Action: create, write, improve, optimize
Concepts: skill, SKILL.md, quality, best practices, triggers
```

### Step 3: Categorize by Type

Organize into categories:

```
Actions: "create a skill", "write SKILL.md", "improve quality"
Questions: "how do I create", "what are best practices"
Concepts: skill development, trigger phrases, progressive disclosure
```

### Step 4: Construct Description

Combine into cohesive description:

```yaml
description: This skill should be used when the user asks to "create a skill",
"write a new skill", "add a skill to my plugin", "how do I create SKILL.md",
"what are skill best practices", "how do I optimize a skill", "improve skill
quality", or mentions skill development, SKILL.md files, trigger phrases,
progressive disclosure, or skill structure.
```

## Common Trigger Mistakes

### Mistake 1: Too Vague

❌ **Problem:**
```yaml
description: Provides guidance for working with skills.
```

**Issues:**
- No specific phrases
- Doesn't say what "working with skills" means
- Not third person

✅ **Fix:**
```yaml
description: This skill should be used when the user asks to "create a skill",
"write SKILL.md", "optimize a skill", or mentions skill development, trigger
phrases, or skill best practices.
```

### Mistake 2: Missing Variations

❌ **Problem:**
```yaml
description: This skill should be used when creating a skill.
```

**Issues:**
- Only one phrase
- Missing question formats
- No concept mentions

✅ **Fix:**
```yaml
description: This skill should be used when the user asks to "create a skill",
"write a new skill", "add a skill to my plugin", "how do I create SKILL.md",
or mentions skill development or SKILL.md files.
```

### Mistake 3: Second Person

❌ **Problem:**
```yaml
description: Use this skill when you want to create a skill.
```

**Issues:**
- Second person ("you")
- Not specific phrase format

✅ **Fix:**
```yaml
description: This skill should be used when the user asks to "create a skill",
"write SKILL.md", or mentions skill development.
```

### Mistake 4: No Domain Context

❌ **Problem:**
```yaml
description: This skill should be used when working with PDFs.
```

**Issues:**
- Vague ("working with")
- No specific PDF operations
- Missing PDF tool names

✅ **Fix:**
```yaml
description: This skill should be used when the user asks to "rotate PDF",
"merge PDF files", "split PDF", or mentions PDF manipulation, editing, or
transformation.
```

## Testing Trigger Phrases

### Validation Questions

Ask these questions to validate triggers:

1. **Specificity**: Are the phrases exact quotes of what users would say?
2. **Coverage**: Do we cover actions, questions, and concepts?
3. **Variety**: Are there multiple ways to trigger the skill?
4. **Clarity**: Is it clear what the skill does from the triggers?
5. **Third Person**: Does it start with "This skill should be used when..."?

### Test Scenarios

Create test scenarios:

```yaml
# Scenario 1: User asks direct question
User: "How do I create a skill?"
Expected: Skill triggers ✅

# Scenario 2: User mentions concept
User: "I need help with trigger phrases."
Expected: Skill triggers ✅

# Scenario 3: User gives command
User: "Write a new skill for PDF editing."
Expected: Skill triggers ✅

# Scenario 4: Unrelated query
User: "How do I create a hook?"
Expected: Does NOT trigger (wrong skill) ✅
```

## Trigger Phrase Templates

Use these templates for common skill types:

### Template 1: Development Skills

```yaml
description: This skill should be used when the user asks to "create {component}",
"add a {component}", "configure {component}", "how do I write {component}", or
mentions {component} development, {component} best practices, or {component}
structure.
```

**Example:**
```yaml
description: This skill should be used when the user asks to "create a command",
"add a command", "configure command arguments", "how do I write a command",
or mentions command development, command best practices, or command structure.
```

### Template 2: Domain Skills

```yaml
description: This skill should be used when the user asks to "{action1}",
"{action2}", "{action3}", or mentions {domain}, {concept1}, {concept2}, or
{concept3}.
```

**Example:**
```yaml
description: This skill should be used when the user asks to "rotate PDF",
"merge PDF files", "split PDF document", or mentions PDF manipulation, PDF
editing, or document transformation.
```

### Template 3: Tool Integration Skills

```yaml
description: This skill should be used when working with {tool}, mentions
"{action1} {tool}", "{action2} {tool}", or discusses {tool} {concept1}, {tool}
{concept2}, or {tool} {concept3}.
```

**Example:**
```yaml
description: This skill should be used when working with MCP servers, mentions
"add MCP server", "configure stdio server", "set up SSE server", or discusses
Model Context Protocol, MCP tools, or server authentication.
```

## Quick Reference

### Effective Trigger Checklist

- [ ] Starts with "This skill should be used when..."
- [ ] Includes 3-7 specific action phrases
- [ ] Covers question formats ("how do I", "what are")
- [ ] Mentions domain concepts and terminology
- [ ] Lists component names if applicable
- [ ] Avoids vague terms ("working with", "help with")
- [ ] Uses exact user phrases in quotes
- [ ] Comprehensive but not overwhelming

### Trigger Phrase Inventory

Maintain this inventory of trigger types:

**Actions:** create, write, add, configure, setup, implement, validate, test
**Questions:** "how do I", "what are", "how do I write", "what's the best way"
**Concepts:** domain-specific terms and technologies
**Components:** specific component names and types

Use these patterns to craft effective trigger descriptions that ensure skills activate reliably.
