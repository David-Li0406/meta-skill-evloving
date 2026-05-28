---
name: agent-development
description: Use this skill when you need to create, modify, or understand the structure and behavior of agents in Claude Code plugins, including guidance on triggering conditions and best practices.
---

# Agent Development for Claude Code Plugins

## Overview

Agents are autonomous subprocesses that handle complex, multi-step tasks independently. Understanding agent structure, triggering conditions, and system prompt design enables the creation of powerful autonomous capabilities.

**Key concepts:**

- Agents are for autonomous work; commands are for user-initiated actions.
- Use Markdown file format with YAML frontmatter.
- Triggering is defined via the description field with examples.
- The system prompt defines agent behavior.
- Model and color customization are available.

## Quick Start

### Minimal Working Agent

```markdown
---
name: my-reviewer
description: Use this agent when the user asks to review code. Examples:

<example>
Context: User wrote new code
user: "Review my changes"
assistant: "I'll use the my-reviewer agent to analyze the code."
<commentary>
Code review request triggers the agent.
</commentary>
</example>

model: inherit
color: blue
---

You are a code reviewer. Analyze code for issues and provide feedback.

**Process:**

1. Read the code.
2. Identify issues.
3. Provide recommendations.

**Output:** Summary with file:line references for each finding.
```

## Agent File Structure

### Complete Format

```markdown
---
name: agent-identifier
description: Use this agent when [triggering conditions]. Examples:

<example>
Context: [Situation description]
user: "[User request]"
assistant: "[How assistant should respond and use this agent]"
<commentary>
[Why this agent should be triggered]
</commentary>
</example>

<example>
[Additional example...]
</example>

model: inherit
color: blue
tools: ["Read", "Write", "Grep"]
---

You are [agent role description]...

**Your Core Responsibilities:**
1. [Responsibility 1]
2. [Responsibility 2]

**Analysis Process:**
[Step-by-step workflow]

**Output Format:**
[What to return]
```

## Frontmatter Fields

### name (required)

Agent identifier used for namespacing and invocation.

**Format:** lowercase, numbers, hyphens only  
**Length:** 3-50 characters  
**Pattern:** Must start and end with alphanumeric

**Good examples:**
- `code-reviewer`
- `test-generator`
- `api-docs-writer`
- `security-analyzer`

**Bad examples:**
- `helper` (too generic)
- `-agent-` (starts/ends with hyphen)
- `my_agent` (underscores not allowed)
- `ag` (too short, < 3 chars)

### description (required)

Defines when Claude should trigger this agent. **This is the most critical field.**

**Must include:**
1. Triggering conditions ("Use this agent when...")
2. Multiple `<example>` blocks showing usage
3. Context, user request, and assistant response in each example
4. `<commentary>` explaining why the agent triggers