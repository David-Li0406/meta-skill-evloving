# Agent Definition Reference

Complete reference for Claude Code subagent definition files.

## File Structure

```markdown
---
name: agent-name
description: Natural language description of when to invoke
tools: Tool1, Tool2, Tool3
model: sonnet
permissionMode: default
skills: skill1, skill2
hooks:
  PreToolUse:
    - matcher: "ToolPattern"
      hooks:
        - type: command
          command: "script.sh"
---

System prompt content goes here.

This is the instruction set that defines the agent's
behavior, expertise, and approach to problem-solving.
```

## File Locations

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project** | `.claude/agents/` | Current project only | Highest |
| **User** | `~/.claude/agents/` | All projects | Lower |
| **CLI** | `--agents` flag | Current session | Middle |
| **Plugin** | `plugin/agents/` | When plugin active | Varies |

## YAML Frontmatter Fields

### name (Required)

Unique identifier for the agent.

**Rules:**
- Lowercase letters only
- Hyphens for word separation
- No spaces or underscores
- No numbers at start

**Examples:**
```yaml
name: code-reviewer      # Good
name: test-runner        # Good
name: db-migration       # Good
name: CodeReviewer       # Bad - uppercase
name: test_runner        # Bad - underscore
name: 123-agent          # Bad - starts with number
```

### description (Required)

Natural language description of when Claude should invoke this agent.

**Best Practices:**
- Be specific about the use case
- Include trigger phrases like "PROACTIVELY" or "MUST BE USED"
- Mention the expertise area
- Keep under 200 characters for display

**Examples:**
```yaml
# Good - specific with trigger
description: Expert code reviewer. MUST BE USED after any code changes to check quality and security.

# Good - clear use case
description: Database migration specialist. Use proactively when schema changes are needed.

# Bad - too vague
description: Helps with stuff.

# Bad - no trigger indication
description: A reviewer.
```

### tools (Optional)

Comma-separated list of tools the agent can use.

**If omitted:** Agent inherits all tools from main thread, including MCP tools.

**Available Built-in Tools:**

| Tool | Description |
|------|-------------|
| `Read` | Read file contents |
| `Write` | Create/overwrite files |
| `Edit` | Modify existing files |
| `Bash` | Execute shell commands |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `WebFetch` | Fetch web content |
| `WebSearch` | Search the web |
| `TodoWrite` | Manage todo lists |
| `Skill` | Invoke skills |
| `NotebookEdit` | Edit Jupyter notebooks |

**MCP Tools:** Format is `mcp__servername__toolname`

**Examples:**
```yaml
# Read-only agent
tools: Read, Glob, Grep

# Full file access
tools: Read, Write, Edit, Bash, Glob, Grep

# With MCP tools
tools: Read, Glob, mcp__memory__store, mcp__memory__recall

# Inherit all (omit field)
# tools field not present
```

### model (Optional)

Specifies which AI model the agent uses.

| Value | Description | When to Use |
|-------|-------------|-------------|
| `sonnet` | Default. Balanced capability/speed | Most tasks |
| `opus` | Most capable, slower | Complex reasoning |
| `haiku` | Fastest, less capable | Simple, quick tasks |
| `inherit` | Same as main conversation | Consistency needed |

**Default:** `sonnet` if not specified.

**Examples:**
```yaml
# Complex analysis needs Opus
model: opus

# Fast exploration uses Haiku
model: haiku

# Match main conversation
model: inherit

# Default (Sonnet) - can omit
model: sonnet
```

### permissionMode (Optional)

Controls how the agent handles permission requests.

| Mode | Description | Use Case |
|------|-------------|----------|
| `default` | Normal permission prompts | Standard agents |
| `acceptEdits` | Auto-accept file edits | Trusted file modifiers |
| `dontAsk` | Skip permission dialogs | Automation workflows |
| `bypassPermissions` | Bypass all permissions | Admin/maintenance tasks |
| `plan` | Plan mode (read-only) | Research-only agents |
| `ignore` | Ignore permission issues | Logging/monitoring |

**Examples:**
```yaml
# Auto-accept edits for formatter
permissionMode: acceptEdits

# Research-only agent
permissionMode: plan

# Fully automated deployment
permissionMode: bypassPermissions
```

### skills (Optional)

Comma-separated list of skills to auto-load when agent starts.

**Important:** Subagents do NOT inherit skills from parent conversation. You must explicitly list required skills.

**Examples:**
```yaml
# Load specific skills
skills: creating-hooks, writing-skills

# Multiple domain skills
skills: react-patterns, testing-strategies
```

### hooks (Optional, 2.1.0+)

Define hooks scoped to this agent's lifecycle.

**Supported Events:**
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool completion
- `Stop` - When agent finishes

**Structure:**
```yaml
hooks:
  EventName:
    - matcher: "ToolPattern"  # Optional for tool events
      hooks:
        - type: command
          command: "script-path"
          timeout: 30  # Optional, seconds
```

**Example:**
```yaml
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-write.sh"
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-command.sh"
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/agent-done.sh"
```

## System Prompt Content

Everything after the frontmatter closing `---` is the system prompt.

### Structure Recommendations

```markdown
---
[frontmatter]
---

You are [role description].

## When Invoked

1. First step
2. Second step
3. Third step

## Guidelines

- Guideline one
- Guideline two

## Output Format

[Expected output structure]

## Constraints

- Constraint one
- Constraint two
```

### Effective Prompt Elements

| Element | Purpose | Example |
|---------|---------|---------|
| **Role** | Define expertise | "You are a senior security auditor" |
| **Process** | Step-by-step workflow | "1. Scan for issues 2. Categorize 3. Report" |
| **Guidelines** | Best practices | "- Always check for SQL injection" |
| **Output** | Expected format | "Report in markdown with severity levels" |
| **Constraints** | Limitations | "- Never modify production configs" |

### System Prompt Best Practices

1. **Be specific** - Vague prompts lead to inconsistent behavior
2. **Use numbered steps** - Clear process improves reliability
3. **Include examples** - Show expected input/output pairs
4. **Set boundaries** - Define what the agent should NOT do
5. **Match tool access** - Prompt should align with available tools

## CLI Agent Definition

Define agents via the `--agents` CLI flag using JSON:

```bash
claude --agents '{
  "agent-name": {
    "description": "When to use this agent",
    "prompt": "System prompt content",
    "tools": ["Tool1", "Tool2"],
    "model": "sonnet"
  }
}'
```

### CLI JSON Schema

```typescript
interface CLIAgentDefinition {
  [agentName: string]: {
    description: string;       // Required
    prompt: string;            // Required - system prompt
    tools?: string[];          // Optional - tool list
    model?: string;            // Optional - model alias
  }
}
```

### CLI Examples

**Single agent:**
```bash
claude --agents '{
  "quick-review": {
    "description": "Quick code review. Use proactively.",
    "prompt": "Review code for obvious issues. Be concise.",
    "tools": ["Read", "Glob", "Grep"],
    "model": "haiku"
  }
}'
```

**Multiple agents:**
```bash
claude --agents '{
  "reviewer": {
    "description": "Code review specialist",
    "prompt": "You are a code reviewer...",
    "tools": ["Read", "Glob", "Grep"]
  },
  "fixer": {
    "description": "Code fix specialist",
    "prompt": "You are a code fixer...",
    "tools": ["Read", "Edit", "Bash"]
  }
}'
```

## Plugin Agents

Plugins can provide agents in their `agents/` directory.

**Plugin manifest.json:**
```json
{
  "name": "my-plugin",
  "agents": ["agents/"]
}
```

**Plugin agent file:** `plugin/agents/my-agent.md`

Plugin agents:
- Appear in `/agents` interface
- Can be invoked explicitly or automatically
- Follow same format as user/project agents

## Task Tool Interface

The Task tool is how Claude spawns subagents internally.

```typescript
interface TaskToolParams {
  description: string;      // Brief task description
  prompt: string;           // Detailed instructions
  subagent_type?: string;   // Agent name to use
  resume?: string;          // Agent ID to resume
}
```

## Resumable Agents

Agents can be resumed to continue previous work:

1. Each execution gets unique `agentId`
2. Transcript stored in `agent-{agentId}.jsonl`
3. Resume with `resume` parameter

**Usage:**
```
> Use code-analyzer to start reviewing auth module
[Agent completes, returns agentId: "abc123"]

> Resume agent abc123 and also check authorization
[Agent continues with full previous context]
```

## Complete Example

```markdown
---
name: security-auditor
description: Security audit specialist. MUST BE USED before any PR that touches authentication, authorization, or data handling code.
tools: Read, Glob, Grep, Bash
model: opus
permissionMode: plan
skills: security-patterns
hooks:
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/security-report.sh"
---

You are a senior security auditor specializing in application security.

## When Invoked

1. Identify security-sensitive code (auth, crypto, data handling)
2. Scan for common vulnerabilities
3. Check for secure coding practices
4. Generate detailed security report

## Vulnerability Checklist

- [ ] SQL injection
- [ ] XSS (cross-site scripting)
- [ ] CSRF (cross-site request forgery)
- [ ] Authentication bypass
- [ ] Authorization flaws
- [ ] Sensitive data exposure
- [ ] Security misconfiguration
- [ ] Insecure deserialization
- [ ] Known vulnerable dependencies

## Output Format

Generate a security report with:
- Summary of findings
- Severity levels (Critical, High, Medium, Low)
- Affected files and line numbers
- Remediation recommendations

## Constraints

- Never modify code (read-only audit)
- Always report findings, even if minor
- Prioritize by severity
- Include CVSS score where applicable
```
