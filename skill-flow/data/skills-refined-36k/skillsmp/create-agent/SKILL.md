---
name: create-agent
description: Create custom Claude Code subagents. Use when the user wants to create a new agent, add a custom subagent, define specialized agents for tasks like code review, debugging, or testing.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(mkdir:*)
---

# Creating Custom Subagents

Create subagent files that teach Claude to delegate specialized tasks.

## File Locations

| Location | Scope | Use Case |
|----------|-------|----------|
| `.claude/agents/` | Project | Team-shared, version-controlled |
| `~/.claude/agents/` | Personal | Available across all projects |

## File Format

Subagents are Markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: What this agent does and when to use it
tools: Read, Grep, Glob
model: sonnet
---

Your system prompt here describing the agent's behavior.
```

## Required Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (lowercase letters, numbers, hyphens only, max 64 chars) |
| `description` | When Claude should delegate to this agent. Include specific actions and trigger keywords. |

## Optional Frontmatter Fields

| Field | Description | Default |
|-------|-------------|---------|
| `tools` | Tools the agent can use (comma-separated or list) | Inherits all |
| `disallowedTools` | Tools to explicitly deny | None |
| `model` | `sonnet`, `opus`, `haiku`, or `inherit` | `sonnet` |
| `permissionMode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` | `default` |
| `skills` | Skills to load into the agent's context | None |
| `hooks` | Lifecycle hooks (`PreToolUse`, `PostToolUse`, `Stop`) | None |

## Available Tools

`Read`, `Edit`, `Write`, `Bash`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, plus any MCP tools from the parent.

## Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard permission checking |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny permission prompts |
| `bypassPermissions` | Skip all permission checks |
| `plan` | Read-only exploration mode |

## Writing the Description

The description is critical - Claude uses it to decide when to delegate.

**Bad**: `Helps with code`

**Good**: `Expert code reviewer for quality, security, and maintainability. Use proactively after writing or modifying code to catch issues before commit.`

Include:
1. Specific actions the agent performs
2. Keywords users would say
3. When Claude should delegate

## Writing the System Prompt

Structure the prompt with:

1. **Role definition**: Who the agent is
2. **Trigger behavior**: What to do when invoked
3. **Checklist/process**: Steps to follow
4. **Output format**: How to present results

## Examples

### Code Reviewer (Read-Only)

```markdown
---
name: code-reviewer
description: Expert code review for quality, security, and maintainability. Use proactively after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review for:
- Clarity and readability
- Proper error handling
- No exposed secrets
- Input validation
- Test coverage

Organize feedback by priority:
- Critical (must fix)
- Warnings (should fix)
- Suggestions (consider)
```

### Debugger (Can Modify Code)

```markdown
---
name: debugger
description: Debug errors, test failures, and unexpected behavior. Use when encountering issues or exceptions.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works
```

### Test Writer

```markdown
---
name: test-writer
description: Write comprehensive tests for code. Use after implementing features or when test coverage is needed.
tools: Read, Write, Bash, Grep, Glob
---

You write thorough, maintainable tests.

When invoked:
1. Analyze the code to be tested
2. Identify test cases: happy path, edge cases, error conditions
3. Follow existing test patterns in the codebase
4. Write tests and run them to verify they pass
```

### Documentation Writer

```markdown
---
name: doc-writer
description: Write and update documentation. Use when documentation is needed or outdated.
tools: Read, Write, Grep, Glob
model: haiku
---

You write clear, concise documentation.

When invoked:
1. Understand the code or feature
2. Write documentation following existing patterns
3. Include examples where helpful
4. Keep it concise and actionable
```

## Hooks Configuration

Add hooks to run scripts at specific points:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - type: command
      command: "./scripts/cleanup.sh"
```

## Key Limitations

- Subagents cannot spawn other subagents
- Background subagents don't have access to MCP tools
- Model choice affects cost and capability

## Workflow

1. Determine scope (project vs personal)
2. Create directory if needed: `.claude/agents/` or `~/.claude/agents/`
3. Create `agent-name.md` file
4. Add frontmatter with `name` and `description`
5. Write the system prompt
6. Reload with `/agents` or restart session
