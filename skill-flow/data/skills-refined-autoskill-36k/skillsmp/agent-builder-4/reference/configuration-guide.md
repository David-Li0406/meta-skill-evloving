# Agent Configuration Guide

Complete reference for configuring Claude Code sub-agents.

## File Format

Agents are markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: When to use this agent
tools: Read, Edit, Bash
model: sonnet
---

# System Prompt

Agent instructions here...
```

## Configuration Fields

### name (Required)

**Type**: String
**Format**: Lowercase with hyphens
**Example**: `code-reviewer`, `sql-analyst`, `bug-hunter`

**Rules**:
- Use descriptive, action-oriented names
- Avoid generic names like "helper" or "assistant"
- Must be unique within scope (project or user)

**Good Examples**:
- `rails-code-reviewer`
- `security-auditor`
- `performance-analyzer`

**Bad Examples**:
- `MyAgent` (not lowercase-with-hyphens)
- `helper` (too generic)
- `agent1` (not descriptive)

### description (Required)

**Type**: String
**Purpose**: Tells Claude when to invoke this agent

**Best Practices**:
- Start with action phrase: "Use this agent when...", "Analyze X to Y", "Review Z for..."
- Include specific trigger keywords
- Use "PROACTIVELY" or "MUST BE USED" for automatic invocation
- Describe the task, not the agent

**Examples**:

```yaml
# Good: Specific triggers
description: Use PROACTIVELY to review Rails code changes for style violations, security issues, and performance problems

# Good: Clear use case
description: Analyze SQL queries for performance bottlenecks and suggest optimizations using EXPLAIN plans

# Bad: Too generic
description: A helpful agent for code tasks

# Bad: Describes agent, not task
description: An expert programmer who knows many languages
```

### tools (Optional)

**Type**: Comma-separated string
**Default**: Inherits all tools from main conversation

**Available Tools**:
- `Read` - Read files
- `Write` - Create new files
- `Edit` - Modify existing files
- `Bash` - Execute shell commands
- `Grep` - Search file contents
- `Glob` - Find files by pattern
- MCP server tools (if installed)

**Examples**:

```yaml
# Read-only agent
tools: Read, Grep, Glob

# Code modifier
tools: Read, Edit, Bash

# Full access
tools: Read, Write, Edit, Bash, Grep, Glob

# No tools specified = inherit all
# (omit the tools field)
```

**When to Limit Tools**:
- Security-sensitive agents (e.g., only Read for auditing)
- Prevent accidental modifications (exclude Write/Edit)
- Focused agents (e.g., only Grep for searching)

### model (Optional)

**Type**: String
**Default**: `inherit` (uses main conversation model)

**Options**:
- `sonnet` - Claude Sonnet (balanced performance)
- `opus` - Claude Opus (highest capability)
- `haiku` - Claude Haiku (fastest, most economical)
- `inherit` - Use main conversation's model

**Examples**:

```yaml
# Use faster model for simple tasks
model: haiku

# Use most capable model for complex analysis
model: opus

# Default to main conversation model
model: inherit

# Omit field to inherit
# (no model field = inherit)
```

**When to Specify**:
- Use `haiku` for simple, repetitive tasks (fast + cheap)
- Use `opus` for complex reasoning or critical decisions
- Use `sonnet` for balanced performance (default recommended)

## System Prompt Guidelines

The markdown body after frontmatter is the agent's system prompt.

### Structure

```markdown
---
name: my-agent
description: Agent description here
---

# Agent Purpose

High-level overview of what this agent does.

## Core Responsibilities

1. Responsibility 1
2. Responsibility 2
3. Responsibility 3

## Approach

How the agent should approach tasks:
- Step 1: What to do first
- Step 2: How to analyze
- Step 3: What to output

## Output Format

Expected output structure:
- Format specifications
- Required sections
- Example outputs

## Constraints

What the agent should NOT do:
- Constraint 1
- Constraint 2

## Examples

### Example 1: [Scenario]
**Input**: [Example input]
**Output**: [Expected output]

### Example 2: [Another scenario]
...
```

### Best Practices

1. **Be Specific**: Detailed instructions yield better results
2. **Include Examples**: Show the agent what good outputs look like
3. **Set Constraints**: Explicitly state what NOT to do
4. **Define Output Format**: Specify structure and style
5. **Break Down Steps**: Guide the agent's reasoning process

### Good System Prompt Example

```markdown
---
name: test-failure-analyzer
description: Use when tests fail to identify root cause and suggest fixes
tools: Read, Grep, Bash
model: sonnet
---

# Test Failure Analyzer

Systematically analyze test failures to identify root causes and propose fixes.

## Core Responsibilities

1. Read test output to identify failing tests
2. Examine test code and implementation
3. Identify the root cause (not just symptoms)
4. Propose specific, minimal fixes
5. Suggest additional test cases if needed

## Analysis Approach

### Step 1: Gather Context
- Read the full test output
- Identify all failing test names
- Note error messages and stack traces

### Step 2: Examine Code
- Read failing test file
- Read implementation being tested
- Identify the assertion that failed

### Step 3: Root Cause Analysis
- Determine if it's a test issue or implementation bug
- Check for timing issues, environment dependencies
- Look for recent changes that might have caused it

### Step 4: Propose Fix
- Suggest minimal code change
- Explain why this fixes the root cause
- Note any side effects or risks

## Output Format

```
## Test Failure Analysis

**Failing Tests**: [List of test names]

**Root Cause**: [One-sentence summary]

**Details**: [Explanation of why tests are failing]

**Proposed Fix**:
[Specific code changes]

**Reasoning**: [Why this fix addresses root cause]

**Risks**: [Any potential side effects]
```

## Constraints

- DO NOT modify tests to make them pass if implementation is wrong
- DO NOT propose fixes without understanding root cause
- DO NOT suggest multiple approaches - pick the best one
- DO NOT rewrite large sections - minimal changes only

## Examples

### Example 1: Assertion Failure

**Input**: Test output showing "Expected 5, got 4"

**Analysis**:
1. Read test to see what's being tested
2. Check implementation logic
3. Identify off-by-one error in loop
4. Propose boundary fix

**Output**:
```
Root Cause: Off-by-one error in loop condition
Fix: Change `i < length` to `i <= length` in file.py:42
Reasoning: Loop exits one iteration early
```
```

### Bad System Prompt Example

```markdown
---
name: helper
description: Helps with tasks
---

You are a helpful assistant. Do whatever the user asks.
```

**Problems**:
- Generic name and description won't trigger correctly
- No specific guidance on approach
- No constraints or output format
- No examples

## File Locations

### Project Agents
**Path**: `.claude/agents/` (in project root)
**Scope**: Available only in this project
**Version Control**: Commit to share with team

### User Agents
**Path**: `~/.claude/agents/` (in home directory)
**Scope**: Available in all projects
**Version Control**: Personal, not shared

### Priority
Project agents override user agents with the same name.

## Validation Checklist

Before deploying your agent, verify:

- [ ] Name is lowercase-with-hyphens
- [ ] Name is descriptive (not generic)
- [ ] Description includes specific trigger conditions
- [ ] Description uses action-oriented language
- [ ] Tools are limited to what's needed (or omitted for full access)
- [ ] Model is appropriate for task complexity (or omitted to inherit)
- [ ] System prompt is detailed and specific
- [ ] Output format is clearly defined
- [ ] Examples are included
- [ ] Constraints are explicit
- [ ] File is in correct location (.claude/agents/ or ~/.claude/agents/)
- [ ] YAML frontmatter is valid

## Common Issues

### Agent Never Triggers
- Description too generic
- Missing trigger keywords
- Name conflicts with another agent

**Fix**: Add specific keywords to description, use "PROACTIVELY" or "MUST BE USED"

### Agent Has Wrong Permissions
- Tools not specified correctly
- Typo in tool names

**Fix**: Check available tool names, use comma-separated list

### Agent Produces Wrong Outputs
- System prompt too vague
- Missing examples
- No output format specified

**Fix**: Add detailed instructions, examples, and explicit output format

### Agent Not Found
- Wrong file location
- File naming issue

**Fix**: Ensure file is in `.claude/agents/` (project) or `~/.claude/agents/` (user)

---

**Related**:
- [Agent Examples](./agent-examples.md)
- [Best Practices](./best-practices.md)
- [Troubleshooting](./troubleshooting.md)
