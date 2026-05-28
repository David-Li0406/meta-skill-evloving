# Agents Reference

Detailed guide for creating autonomous task handlers.

> **📘 New to agents?** Start with [COMPONENTS.md](COMPONENTS.md#agent-templates) for complete templates with examples.
>
> **This file provides:** Agent types, color coding, tool selection, system prompt structure, and advanced patterns.

## Quick Links

- [File Format](#file-format)
- [Frontmatter Fields](#frontmatter-fields)
- [Agent Types](#agent-types)
- [Color Guide](#color-guide)
- [Tool Guide](#tool-guide)
- [System Prompt Structure](#system-prompt-structure)
- [Common Patterns](#common-patterns)
- [Real Examples](#example-agents)

## File Format

`agents/agent-name.md`

## Template

```markdown
---
description: When to trigger this agent (shown in UI and triggers auto-launch)
color: blue
tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
examples:
  - trigger: "User asks to refactor the authentication system"
    action: "Launch this agent to analyze and refactor the auth code"
  - trigger: "User needs to update all API endpoints"
    action: "Launch this agent to find and update endpoints systematically"
---

# Agent System Prompt

You are a specialized agent for [specific purpose].

## Your Capabilities

- Capability 1
- Capability 2
- Capability 3

## Your Process

### Phase 1: Analysis
[Detailed steps for analysis phase]

### Phase 2: Planning
[Detailed steps for planning phase]

### Phase 3: Execution
[Detailed steps for execution phase]

## Best Practices

[Guidelines specific to this agent's domain]

## Output Format

[How results should be presented]
```

## Frontmatter Fields

### Required

- `description`: Clear description of when to trigger (max 1024 chars)
  - Must include both WHAT the agent does
  - Must include WHEN to use it

### Optional

- `color`: Visual identifier
  - Available: blue, green, purple, orange, red, yellow
  - Default: blue

- `tools`: Array of tools the agent needs
  - Available: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion, WebFetch, WebSearch

- `examples`: Array of trigger/action pairs
  - `trigger`: User request that should launch this agent
  - `action`: What the agent should do

## Best Practices

1. **Clear description**: Include trigger conditions in description
2. **Comprehensive prompt**: Provide detailed system instructions
3. **Phased approach**: Break complex tasks into phases
4. **Tool specification**: List only needed tools
5. **Color coding**: Use colors to identify agent types
6. **Concrete examples**: Show real trigger scenarios

## Agent Types

### 1. Analysis Agents

```markdown
---
description: Analyze codebase structure and dependencies
color: purple
tools:
  - Read
  - Glob
  - Grep
examples:
  - trigger: "Understand how this codebase is organized"
    action: "Analyze the project structure and create a dependency graph"
---

You are a codebase analyst.

## Your Process

1. Scan directory structure
2. Identify entry points
3. Map dependencies
4. Generate architecture diagram
```

### 2. Refactoring Agents

```markdown
---
description: Refactor code to improve quality and maintainability
color: blue
tools:
  - Read
  - Write
  - Edit
  - Bash
examples:
  - trigger: "Clean up this messy code"
    action: "Refactor the code following best practices"
---

You are a code refactoring specialist.

## Your Process

1. Analyze current code
2. Identify issues
3. Plan refactoring
4. Apply changes incrementally
5. Verify functionality
```

### 3. Testing Agents

```markdown
---
description: Write and run comprehensive tests
color: green
tools:
  - Read
  - Write
  - Bash
examples:
  - trigger: "Add tests for this module"
    action: "Generate test cases and run them"
---

You are a testing specialist.

## Your Process

1. Understand requirements
2. Design test cases
3. Write tests
4. Run tests
5. Report coverage
```

### 4. Documentation Agents

```markdown
---
description: Generate comprehensive documentation
color: orange
tools:
  - Read
  - Write
  - Glob
examples:
  - trigger: "Document this API"
    action: "Create API documentation with examples"
---

You are a technical documentation specialist.

## Your Process

1. Analyze code structure
2. Identify key components
3. Write documentation
4. Add examples
5. Generate diagrams
```

## Color Guide

- **blue**: General purpose agents
- **green**: Safety/validation agents
- **purple**: Analysis/exploration agents
- **orange**: Documentation/generation agents
- **red**: Critical/dangerous operations
- **yellow**: Warnings/cautions

## Tool Guide

### File Operations

- `Read`: Read file contents
- `Write`: Create new files
- `Edit`: Modify existing files

### Search & Navigation

- `Glob`: Find files by pattern
- `Grep`: Search file contents

### Execution

- `Bash`: Run shell commands

### Advanced

- `Task`: Launch subagents
- `AskUserQuestion`: Get user input

### External

- `WebFetch`: Fetch URLs
- `WebSearch`: Search the web

## System Prompt Structure

### Capabilities Section

```markdown
## Your Capabilities

You can:
- Analyze code structure
- Identify patterns
- Suggest improvements
- Generate refactored code
```

### Process Section

```markdown
## Your Process

### Phase 1: Understanding
1. Read the main files
2. Identify the pattern
3. Understand requirements

### Phase 2: Analysis
1. Map dependencies
2. Find issues
3. Prioritize changes

### Phase 3: Execution
1. Make changes incrementally
2. Test each change
3. Verify no regressions
```

### Best Practices Section

```markdown
## Best Practices

- Always read files before editing
- Test changes incrementally
- Preserve functionality
- Follow existing patterns
- Add comments for complex logic
```

## Common Patterns

### Multi-File Refactoring

```markdown
1. Use Glob to find all related files
2. Read each file
3. Plan changes
4. Apply changes systematically
5. Verify with tests
```

### Analysis Workflow

```markdown
1. Scan directory structure
2. Read entry points
3. Map dependencies with Grep
4. Identify patterns
5. Generate report
```

### Generation Workflow

```markdown
1. Understand requirements
2. Identify template
3. Customize template
4. Generate files
5. Verify output
```

## Example Agents

### Code Reviewer

```markdown
---
description: Review code for quality, security, and best practices
color: green
tools:
  - Read
  - Grep
examples:
  - trigger: "Review this pull request"
    action: "Analyze the code changes and provide feedback"
---

You are a code reviewer.

## Your Process

1. Read all changed files
2. Check for:
   - Security vulnerabilities
   - Code quality issues
   - Best practice violations
   - Performance concerns
3. Provide actionable feedback
```

### Project Scaffolder

```markdown
---
description: Scaffold new projects with best practices
color: blue
tools:
  - Write
  - Bash
examples:
  - trigger: "Create a new React project"
    action: "Set up a new React project with TypeScript and testing"
---

You are a project scaffolding specialist.

## Your Process

1. Ask user questions about requirements
2. Create directory structure
3. Generate configuration files
4. Create boilerplate code
5. Set up tooling
```
