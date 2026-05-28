# Component Patterns

## Table of Contents

- [Plugin Manifest (plugin.json)](#plugin-manifest-pluginjson)
- [Component Type Patterns](#component-type-patterns)
- [Key sections:](#key-sections)
- [Pattern Selection Guide](#pattern-selection-guide)
- [Component Relationships](#component-relationships)
- [Auto-Discovery Rules](#auto-discovery-rules)
- [Path Resolution Patterns](#path-resolution-patterns)
- [Maintenance Patterns](#maintenance-patterns)

## Plugin Manifest (plugin.json)

### Required Fields

```json
{
  "name": "plugin-name"
}
```

**Name requirements:**
- Use kebab-case format (lowercase with hyphens)
- Must be unique across installed plugins
- No spaces or special characters
- Example: `code-review-assistant`, `test-runner`, `api-docs`

### Recommended Metadata

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin-name",
  "license": "MIT",
  "keywords": ["testing", "automation", "ci-cd"]
}
```

**Version format**: Follow semantic versioning (MAJOR.MINOR.PATCH)
**Keywords**: Use for plugin discovery and categorization

### Component Path Configuration

Specify custom paths for components (supplements default directories):

```json
{
  "name": "plugin-name",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Important**: Custom paths supplement defaults—they don't replace them. Components in both default directories and custom paths will load.

**Path rules:**
- Must be relative to plugin root
- Must start with `./`
- Cannot use absolute paths
- Support arrays for multiple locations

## Component Type Patterns

### Skills Pattern

**Format**: Each skill in its own directory with `SKILL.md` file

**Structure**:
```
skills/
├── api-testing/
│   ├── SKILL.md              # Core skill definition (~2,000 words)
│   ├── references/           # Tier 3: Detailed docs
│   │   ├── patterns.md
│   │   ├── api-specs.md
│   │   └── best-practices.md
│   ├── examples/            # Tier 3: Working examples
│   │   ├── basic-usage.md
│   │   └── advanced-scenarios.md
│   └── scripts/             # Tier 3: Utility scripts
│       ├── test-runner.sh
│       └── report-generator.py
└── database-migrations/
    ├── SKILL.md
    ├── examples/
    │   └── migration-template.sql
    └── scripts/
        └── validate-migration.sh
```

**SKILL.md Requirements**:
```markdown
---
name: skill-name
description: "WHAT + WHEN + NOT formula"
version: 2.0.0
context: standard
tags: [tag1, tag2]
---

# Core skill guidance
## Key sections:
- Overview
- When to use
- How to use
- Examples
- Best practices
```

### Commands Pattern

**Format**: Markdown files with YAML frontmatter in `commands/` directory

**Structure**:
```
commands/
├── review.md        # /review command
├── test.md          # /test command
└── deploy.md        # /deploy command
```

**File format**:
```markdown
---
name: command-name
description: "Use when [user scenario]"
allowed-tools: ["skill-name"]
---

Execute workflow:
1. Use skill-name
2. Process results
3. Confirm completion
```

**Usage**: Orchestrate skills for explicit user-initiated workflows

### Agents Pattern

**Format**: Markdown files with YAML frontmatter in `agents/` directory

**Structure**:
```
agents/
├── code-reviewer.md      # Specialized worker
├── test-generator.md     # Autonomous task executor
└── refactorer.md       # Domain expert
```

**File format**:
```markdown
---
name: agent-name
description: "Use when [triggering condition]"
model: inherit
color: blue
tools: ["Read", "Grep"]
---

You are [agent role] specializing in [domain].

**Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]

**Coordination Pattern**: [if applicable]
**State Management**: [if applicable]

**Process:**
1. [Step 1]
2. [Step 2]

**Output Format:**
[What to provide]
```

**Usage**: Specialized workers for isolation, parallelism, or domain expertise

### Hooks Pattern

**Format**: JSON configuration in `hooks/hooks.json` or inline in `plugin.json`

**Structure**:
```
hooks/
├── hooks.json           # Hook configuration
└── scripts/
    ├── validate.sh      # Hook script
    └── check-style.sh   # Hook script
```

**Configuration format**:
```json
{
  "PermissionRequest": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
      "timeout": 30,
      "once": true
    }]
  }],
  "SessionStart": [{
    "matcher": "*",
    "hooks": [{
      "type": "prompt",
      "template": "Initialize project context"
    }]
  }]
}
```

**2026 Events**:
- `PermissionRequest` (NEW): Before Claude requests permission
- `SessionStart`: When new session begins
- `SessionEnd`: When session ends
- `Notification`: Notification events (subtypes: info, success, warning, error)

**Usage**: Infrastructure automation, event-driven workflows, MCP/LSP configuration

### MCP Servers Pattern

**Format**: JSON configuration in `.mcp.json` or inline in `plugin.json`

**Structure**:
```json
{
  "server-name": {
    "type": "streamable-http",  // 2026: stdio or streamable-http
    "url": "https://mcp.example.com/stream",
    "version": "2026-01-20",   // 2026: Date-based versioning
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    },
    "resources": [              // 2026: Resources primitive
      {
        "name": "user-profile",
        "uri": "data://user/profile",
        "description": "Current user profile"
      }
    ],
    "prompts": [               // 2026: Prompts primitive
      {
        "name": "code-review",
        "description": "Generate comprehensive code review",
        "arguments": [
          {
            "name": "file-path",
            "description": "Path to file",
            "required": true
          }
        ]
      }
    ]
  }
}
```

**Transport Types**:
- `stdio`: Local process execution
- `streamable-http`: Hosted services with bidirectional streaming

**2026 Features**:
- Streamable HTTP transport (NOT WebSocket)
- Resources primitive (read-only data)
- Prompts primitive (predefined workflows)
- Date-based versioning (YYYY-MM-DD)
- Security-by-design framework

**Usage**: External service integration with Tools, Resources, and Prompts

## Pattern Selection Guide

### When to Use Skills
- Domain expertise and reusable capabilities
- Autonomous execution (80-95% completion without questions)
- Auto-discovery through description matching
- Self-sufficient building blocks

### When to Add Commands
- User explicitly triggers workflows
- Multiple skills need coordination
- Clear starting/ending points required
- User needs explicit control

### When to Add Agents
- Isolation from main conversation needed
- Parallel execution beneficial
- Specialized expertise required
- Complex coordination patterns

### When to Add Hooks
- Infrastructure automation required
- Event-driven workflows needed
- MCP/LSP configuration needed
- System-level integration

### When to Add MCP
- External service integration
- API access required
- Tools/Resources/Prompts needed
- OAuth authentication required

## Component Relationships

```
┌─────────────────────────────────────────┐
│         User Request/Task              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Commands/Agents (Orchestrators)      │
│  - User-initiated workflows             │
│  - Skill coordination                   │
│  - Isolation when needed                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Skills (Primary Building Blocks)   │
│  - Domain expertise                     │
│  - Self-sufficient capabilities         │
│  - Auto-discovery                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Hooks/MCP (Infrastructure)            │
│  - Event automation                     │
│  - External services                    │
│  - System configuration                 │
└─────────────────────────────────────────┘
```

## Auto-Discovery Rules

Claude Code automatically discovers and loads components:

1. **Plugin manifest**: Reads `.claude-plugin/plugin.json` when plugin enables
2. **Commands**: Scans `commands/` directory for `.md` files
3. **Agents**: Scans `agents/` directory for `.md` files
4. **Skills**: Scans `skills/` for subdirectories containing `SKILL.md`
5. **Hooks**: Loads configuration from `hooks/hooks.json` or manifest
6. **MCP servers**: Loads configuration from `.mcp.json` or manifest

**Discovery timing**:
- Plugin installation: Components register with Claude Code
- Plugin enable: Components become available for use
- No restart required: Changes take effect on next Claude Code session

**Override behavior**: Custom paths in `plugin.json` supplement (not replace) default directories

## Path Resolution Patterns

### In Manifest JSON Fields

**hooks.json**:
```json
{
  "PreToolUse": [{
    "hooks": [{
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/tool.sh"
    }]
  }]
}
```

**.mcp.json**:
```json
{
  "server-name": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/server.js"
  }
}
```

### In Component Files

**commands/example.md**:
```markdown
Reference scripts at: ${CLAUDE_PLUGIN_ROOT}/scripts/helper.py
```

**agents/worker.md**:
```markdown
Use utility: ${CLAUDE_PLUGIN_ROOT}/scripts/utils.sh
```

### In Executed Scripts

**scripts/tool.sh**:
```bash
#!/bin/bash
# ${CLAUDE_PLUGIN_ROOT} available as environment variable
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

**scripts/generator.py**:
```python
#!/usr/bin/env python3
# ${CLAUDE_PLUGIN_ROOT} available as environment variable
import os
plugin_root = os.environ['CLAUDE_PLUGIN_ROOT']
```

## Maintenance Patterns

### Version Management
1. **Semantic versioning**: Update version in plugin.json for releases
2. **Skill versions**: Each skill can have its own version
3. **Consistent updates**: Keep all versions synchronized

### Deprecation Strategy
1. **Mark clearly**: Mark old components before removal
2. **Grace period**: Give users time to migrate
3. **Document changes**: Note breaking changes affecting users

### Testing Strategy
1. **Component tests**: Verify each component works independently
2. **Integration tests**: Test component interactions
3. **Cross-platform**: Test on macOS, Linux, Windows
4. **Version compatibility**: Test with different Claude Code versions
