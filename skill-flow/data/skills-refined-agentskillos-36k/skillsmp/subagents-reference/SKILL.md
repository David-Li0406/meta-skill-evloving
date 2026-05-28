---
name: subagents-reference
description: Claude Code subagents configuration reference. Use when creating custom subagents, understanding agent types, configuring agent prompts, or extending the Task tool with specialized agents.
---

# Claude Code Subagents Reference

Subagents are specialized AI assistants that Claude can spawn for specific tasks. Define custom agents to extend Claude's capabilities.

## Agent File Locations

```
~/.claude/agents/              # User agents (all projects)
.claude/agents/                # Project agents (team shared)
```

## Agent File Format

```markdown
---
name: agent-identifier
description: What this agent does and when to use it
model: sonnet
tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Agent Name

Detailed instructions for the agent's behavior.

## Capabilities
- Specific task the agent handles
- Another capability

## Approach
How the agent should tackle problems.
```

## Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | No | string | Agent identifier for Task tool |
| `description` | Yes | string | When/why to use this agent |
| `model` | No | string | haiku, sonnet, opus |
| `tools` | No | array | Available tools |
| `allowed_tools` | No | array | Alias for `tools` |

## Built-in Agent Types

| Agent | Purpose | Tools |
|-------|---------|-------|
| `Explore` | Codebase exploration | Read, Grep, Glob |
| `general-purpose` | Multi-step tasks | All tools |
| `Bash` | Command execution | Bash |
| `Plan` | Implementation planning | All tools |

## Custom Agent Example

```markdown
---
name: security-reviewer
description: Review code for security vulnerabilities. Use when checking for injection, XSS, auth issues.
model: sonnet
tools:
  - Read
  - Grep
  - Glob
---

# Security Review Agent

You are a security specialist reviewing code for vulnerabilities.

## Review Checklist
1. SQL injection
2. XSS vulnerabilities
3. Authentication bypass
4. Sensitive data exposure
5. Insecure dependencies

## Process
1. Read the target files
2. Search for common vulnerability patterns
3. Report findings with severity ratings
```

## Invoking Agents

### Via Task Tool
```
Claude uses Task tool with:
- subagent_type: "security-reviewer"
- prompt: "Review the auth module for vulnerabilities"
```

### From Skills/Instructions
Reference agent in CLAUDE.md or skills:
```
When reviewing security, use the security-reviewer agent.
```

## Tool Restrictions

Limit what agents can do:

```yaml
tools:
  - Read      # Read files
  - Grep      # Search content
  - Glob      # Find files
  # No Bash, Write, Edit = read-only agent
```

## Model Selection

| Model | Use Case |
|-------|----------|
| `haiku` | Fast, simple tasks |
| `sonnet` | Balanced (default) |
| `opus` | Complex reasoning |

## Agent Prompt Best Practices

1. **Clear identity**: State what the agent specializes in
2. **Specific instructions**: Be explicit about approach
3. **Tool guidance**: Explain which tools to use when
4. **Output format**: Specify expected output structure
5. **Boundaries**: Define what's in/out of scope

## Example: Code Reviewer

```markdown
---
name: code-reviewer
description: Review code changes for quality, patterns, and issues
model: sonnet
tools:
  - Read
  - Grep
  - Glob
---

# Code Review Agent

Review code for:
- Logic errors
- Performance issues
- Code style violations
- Missing error handling

## Output Format
For each issue found:
1. File and line number
2. Issue description
3. Severity (high/medium/low)
4. Suggested fix
```

## Example: Test Writer

```markdown
---
name: test-writer
description: Write unit tests for functions and modules
model: sonnet
tools:
  - Read
  - Write
  - Bash
---

# Test Writing Agent

Write comprehensive unit tests.

## Approach
1. Read the target code
2. Identify testable functions
3. Write test cases covering:
   - Happy path
   - Edge cases
   - Error conditions
4. Run tests to verify
```

## Agent Communication

Agents receive:
- The prompt from Task tool
- Access to specified tools
- Project context

Agents return:
- Single response to parent Claude
- Any artifacts created

## Debugging

```bash
# List available agents
/agents

# Check agent loading
claude --debug
```

---

For complete documentation, see:
- [subagents-full.md](subagents-full.md) - Complete subagents reference
