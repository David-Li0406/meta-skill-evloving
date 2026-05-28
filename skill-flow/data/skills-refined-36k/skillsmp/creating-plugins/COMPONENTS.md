# Plugin Components Reference

Complete documentation for all component types that plugins can include.

## Overview

Plugins can bundle any combination of these components:

| Component | Location | Invocation |
|-----------|----------|------------|
| Commands | `commands/` | User runs `/plugin:command` |
| Agents | `agents/` | Claude invokes or user selects |
| Skills | `skills/*/SKILL.md` | Claude invokes automatically |
| Hooks | `hooks/hooks.json` | Events trigger automatically |
| MCP Servers | `.mcp.json` | Tools available to Claude |
| LSP Servers | `.lsp.json` | Code intelligence for Claude |

## Commands

Slash commands that users invoke directly.

### Location

```
my-plugin/
├── commands/
│   ├── deploy.md
│   └── status.md
└── ...
```

### Format

Markdown files with optional frontmatter:

```markdown
---
description: Deploy the current project to production
---

# Deploy Command

Deploy the application following these steps:

1. Run tests to ensure everything passes
2. Build the production bundle
3. Push to the deployment target

Handle any errors gracefully and report progress.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | No | Shown in `/help` and command discovery |

### Command Arguments

Capture user input with placeholders:

```markdown
---
description: Search for files matching a pattern
---

# Search Command

Search for files matching: "$ARGUMENTS"

Use glob patterns and report all matches.
```

| Placeholder | Description |
|-------------|-------------|
| `$ARGUMENTS` | All text after command |
| `$1`, `$2`, etc. | Individual arguments |

### Naming

- Filename becomes command name
- `deploy.md` creates `/plugin-name:deploy`
- Always namespaced with plugin name

### Example Commands

**Simple command:**
```markdown
---
description: Show project status
---

Show the current project status including:
- Git status
- Running services
- Recent logs
```

**Command with arguments:**
```markdown
---
description: Create a new component
---

# Create Component

Create a new $1 component named "$2" following the project conventions.

1. Create the component file
2. Add appropriate tests
3. Export from index
```

Usage: `/my-plugin:create-component Button Header`

## Agents

Specialized subagents for specific tasks.

### Location

```
my-plugin/
├── agents/
│   ├── security-reviewer.md
│   └── performance-tester.md
└── ...
```

### Format

```markdown
---
description: Reviews code for security vulnerabilities
capabilities: ["code-review", "security-analysis", "vulnerability-detection"]
---

# Security Reviewer

You are a security-focused code reviewer. Your expertise includes:

- OWASP Top 10 vulnerabilities
- Authentication and authorization flaws
- Input validation issues
- Secrets management
- Dependency vulnerabilities

## When to Use

Claude should invoke this agent when:
- Reviewing security-sensitive code
- Auditing authentication flows
- Checking for injection vulnerabilities
- Analyzing cryptographic implementations

## Review Process

1. Identify security-relevant code sections
2. Check against common vulnerability patterns
3. Verify input validation
4. Review authentication/authorization logic
5. Scan for hardcoded secrets
6. Report findings with severity ratings
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Brief agent description |
| `capabilities` | No | Array of task tags |

### Integration

- Agents appear in `/agents` interface
- Claude can invoke based on task context
- Users can manually invoke agents
- Work alongside built-in Claude agents

## Skills

Model-invoked capabilities that Claude uses automatically.

### Location

```
my-plugin/
├── skills/
│   ├── code-review/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       ├── reference.md
│       └── scripts/
└── ...
```

### Format

```yaml
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: ["Read", "Glob", "Grep"]
---

# Code Review Skill

When reviewing code, check for:

1. **Code Organization**
   - Proper file structure
   - Logical grouping
   - Clear naming

2. **Error Handling**
   - Try/catch blocks
   - Error propagation
   - User feedback

3. **Security**
   - Input validation
   - Authentication checks
   - Data sanitization

4. **Performance**
   - Unnecessary loops
   - Memory leaks
   - Efficient algorithms

## Output Format

Provide structured review with:
- Summary (1-2 sentences)
- Issues found (severity: critical/major/minor)
- Recommendations
- Positive observations
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (kebab-case) |
| `description` | Yes | When Claude should use this skill |
| `allowed-tools` | No | Restrict available tools |
| `model` | No | Force specific model |

### Skill vs Agent vs Command

| Type | Invocation | Use Case |
|------|------------|----------|
| Command | User runs `/plugin:cmd` | User-initiated actions |
| Agent | Claude invokes or user selects | Specialized subagent tasks |
| Skill | Claude uses automatically | Extending Claude's capabilities |

## Hooks

Event handlers that respond to Claude Code events.

### Location

```
my-plugin/
├── hooks/
│   └── hooks.json
└── ...
```

Or inline in `plugin.json`.

### Format

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh $TOOL_INPUT_file_path"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Session started' >> ${CLAUDE_PLUGIN_ROOT}/logs/session.log"
          }
        ]
      }
    ]
  }
}
```

### Available Events

| Event | When Triggered |
|-------|----------------|
| `PreToolUse` | Before Claude uses any tool |
| `PostToolUse` | After Claude successfully uses any tool |
| `PostToolUseFailure` | After tool execution fails |
| `PermissionRequest` | When permission dialog shown |
| `UserPromptSubmit` | When user submits a prompt |
| `Notification` | When Claude Code sends notifications |
| `Stop` | When Claude attempts to stop |
| `SubagentStart` | When a subagent starts |
| `SubagentStop` | When a subagent stops |
| `SessionStart` | At session beginning |
| `SessionEnd` | At session end |
| `PreCompact` | Before conversation history compacted |

### Hook Types

**Command Hook:**
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
}
```

**Prompt Hook:**
```json
{
  "type": "prompt",
  "prompt": "Review the change: $ARGUMENTS"
}
```

**Agent Hook:**
```json
{
  "type": "agent",
  "agent": "Verify this change is safe: $ARGUMENTS"
}
```

### Matchers

Filter which tools trigger hooks:

```json
{
  "matcher": "Write|Edit",
  "hooks": [...]
}
```

| Pattern | Matches |
|---------|---------|
| `Write` | Only Write tool |
| `Write\|Edit` | Write or Edit |
| `.*` | Any tool |
| `Bash.*` | Tools starting with Bash |

### Environment Variables in Hooks

| Variable | Description |
|----------|-------------|
| `$TOOL_INPUT_<field>` | Tool input field value |
| `$TOOL_OUTPUT` | Tool output (PostToolUse) |
| `$CLAUDE_PLUGIN_ROOT` | Plugin installation path |
| `$FILE` | File path (Write/Edit tools) |

### Hook Script Requirements

```bash
#!/bin/bash
# scripts/lint.sh

# Make executable: chmod +x scripts/lint.sh

FILE="$1"

if [[ "$FILE" == *.ts ]] || [[ "$FILE" == *.tsx ]]; then
  npx eslint --fix "$FILE"
fi
```

### Hook Framework (YAML Alternative)

For complex hook setups, use the YAML-based Hook Framework from `claude-code-sdk`:

```yaml
# hooks/hooks.yaml
version: 1

builtins:
  session-naming:
    enabled: true
  turn-tracker:
    enabled: true
  tool-logger:
    enabled: true
    options:
      outputPath: ${CLAUDE_PLUGIN_ROOT}/logs/tools.log

handlers:
  format-on-save:
    events: [PostToolUse]
    matcher: "Write|Edit"
    command: ${CLAUDE_PLUGIN_ROOT}/scripts/format.sh
```

The framework provides:

| Feature | Description |
|---------|-------------|
| Built-in handlers | session-naming, turn-tracker, dangerous-command-guard, tool-logger |
| Environment variables | `CLAUDE_SESSION_NAME`, `CLAUDE_TURN_ID`, `CLAUDE_TURN_SEQUENCE` |
| Result sharing | Handlers can access results from other handlers |
| YAML config | Cleaner configuration than JSON |

See [creating-hooks skill](../creating-hooks/SKILL.md) for complete framework documentation.

## MCP Servers

Model Context Protocol servers providing external tools.

### Location

```
my-plugin/
├── .mcp.json
└── ...
```

Or inline in `plugin.json`.

### Format

```json
{
  "mcpServers": {
    "database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Server executable |
| `args` | No | Command-line arguments |
| `env` | No | Environment variables |
| `cwd` | No | Working directory |

### Integration

- Servers start automatically when plugin enabled
- Appear as standard MCP tools
- Integrate with Claude's existing tools
- Configurable independently of user MCP servers

## LSP Servers

Language Server Protocol servers for code intelligence.

### Location

```
my-plugin/
├── .lsp.json
└── ...
```

Or inline in `plugin.json`.

### Format

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  },
  "rust": {
    "command": "rust-analyzer",
    "extensionToLanguage": {
      ".rs": "rust"
    },
    "initializationOptions": {
      "checkOnSave": true
    }
  }
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `command` | LSP binary (must be in PATH) |
| `extensionToLanguage` | File extension to language mapping |

### Optional Fields

| Field | Description |
|-------|-------------|
| `args` | Command-line arguments |
| `transport` | `stdio` (default) or `socket` |
| `env` | Environment variables |
| `initializationOptions` | Server initialization options |
| `settings` | Workspace configuration settings |
| `workspaceFolder` | Workspace folder path |
| `startupTimeout` | Max startup wait (ms) |
| `shutdownTimeout` | Max shutdown wait (ms) |
| `restartOnCrash` | Auto-restart on crash |
| `maxRestarts` | Max restart attempts |
| `loggingConfig` | Debug logging settings |

### Logging Configuration

Enable debug logging:

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    },
    "loggingConfig": {
      "args": ["--log-level", "4"],
      "env": {
        "TSS_LOG": "-level verbose -file ${CLAUDE_PLUGIN_LSP_LOG_FILE}"
      }
    }
  }
}
```

Use `--enable-lsp-logging` flag to activate.

### Important

**Users must install the language server binary separately.** LSP plugins configure how Claude Code connects to a language server, but don't include the server itself.

If you see `Executable not found in $PATH`, install the binary:

| Plugin | Install Command |
|--------|-----------------|
| `pyright-lsp` | `pip install pyright` or `npm install -g pyright` |
| `typescript-lsp` | `npm install -g typescript-language-server typescript` |
| `rust-lsp` | See rust-analyzer installation docs |

## Component Organization

### Simple Plugin

```
simple-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── hello.md
└── README.md
```

### Complex Plugin

```
enterprise-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── core/
│   │   ├── deploy.md
│   │   └── status.md
│   └── admin/
│       └── configure.md
├── agents/
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── patterns.md
│   └── security-audit/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
├── scripts/
│   ├── format.sh
│   ├── lint.sh
│   └── deploy.sh
├── servers/
│   └── custom-mcp/
├── config/
│   └── default.json
├── LICENSE
├── CHANGELOG.md
└── README.md
```

## See Also

- [SKILL.md](./SKILL.md) - Main plugin creation guide
- [MANIFEST.md](./MANIFEST.md) - Manifest schema reference
- [DISTRIBUTION.md](./DISTRIBUTION.md) - Marketplace distribution
