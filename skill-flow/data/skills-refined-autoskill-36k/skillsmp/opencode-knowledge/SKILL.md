---
name: opencode-knowledge
description: OpenCode concepts, configuration, and best practices. Use when answering questions about OpenCode features, configuration, or troubleshooting AI automation in this repository.
---

# OpenCode Knowledge

Comprehensive reference for OpenCode concepts, configuration, and this repository's AI automation.

## Trigger

When user asks about:
- OpenCode features, configuration, or troubleshooting
- Creating or modifying skills, agents, or commands
- AI automation best practices
- What's new in OpenCode

## Always Check Online First

**IMPORTANT**: OpenCode evolves rapidly. Always verify information by fetching the latest docs:

```
# Fetch specific documentation
webfetch https://opencode.ai/docs/<topic>/

# Check release notes for new features
webfetch https://github.com/anomalyco/opencode/releases
```

## OpenCode Architecture

### Configuration Hierarchy

```
Global (~/.config/opencode/)
├── opencode.json          # Global config
├── AGENTS.md              # Global rules
├── skills/                # Global skills
├── commands/              # Global commands
└── agents/                # Global agents

Project (.opencode/)
├── config.json            # Project config (overrides global)
├── skills/                # Project skills (symlinks to skills/)
├── commands/              # Project commands
├── agents/                # Project agents
└── tools/                 # Custom tools (TypeScript/JS)

Project Root
├── AGENTS.md              # Project rules (injected into context)
└── opencode.json          # Alternative config location
```

### Configuration Precedence (highest to lowest)
1. Project `.opencode/config.json`
2. Project `opencode.json`
3. Global `~/.config/opencode/opencode.json`
4. Environment variables
5. Defaults

## Core Concepts

### Tools

Built-in tools the LLM can use:

| Tool | Purpose | Permission Key |
|------|---------|----------------|
| `bash` | Execute shell commands | `bash` |
| `edit` | Modify files (string replacement) | `edit` |
| `write` | Create/overwrite files | `edit` |
| `read` | Read file contents | `read` |
| `grep` | Search file contents (regex) | `grep` |
| `glob` | Find files by pattern | `glob` |
| `list` | List directory contents | `list` |
| `lsp` | Code intelligence (experimental) | `lsp` |
| `patch` | Apply patches | `edit` |
| `skill` | Load skill instructions | `skill` |
| `todowrite` | Manage task lists | `todowrite` |
| `todoread` | Read task lists | `todoread` |
| `webfetch` | Fetch web content | `webfetch` |
| `question` | Ask user questions | `question` |

### Permissions

Control tool behavior:

```json
{
  "permission": {
    "edit": "allow",      // Allow without asking
    "bash": "ask",        // Prompt before use
    "webfetch": "deny"    // Disable completely
  }
}
```

Per-agent permissions override global:

```json
{
  "agent": {
    "plan": {
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    }
  }
}
```

Bash command patterns:

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git status": "allow",
      "git push*": "ask",
      "rm -rf *": "deny"
    }
  }
}
```

### Rules (AGENTS.md)

Custom instructions injected into LLM context:

- **Project**: `AGENTS.md` in project root
- **Global**: `~/.config/opencode/AGENTS.md`
- **Claude Code fallback**: `CLAUDE.md` (if no AGENTS.md)

External files via config:

```json
{
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines.md",
    "https://example.com/rules.md"
  ]
}
```

### Agents

Two types:
- **Primary**: Main assistants (Tab to switch)
- **Subagent**: Specialized assistants (@ mention or Task tool)

Built-in agents:
- **Build**: Full tool access (default)
- **Plan**: Read-only, no edits or bash
- **General**: Subagent for complex tasks
- **Explore**: Fast read-only subagent

Agent options:

```yaml
# In agents/<name>.md frontmatter
---
description: Required description for discovery
mode: primary | subagent | all
model: provider/model-id
temperature: 0.0-1.0
maxSteps: 10  # Limit iterations
hidden: true  # Hide from @ menu
tools:
  bash: false
  edit: true
permission:
  edit: ask
  task:
    "*": "deny"
    "specific-agent": "allow"
---
```

### Skills

Reusable instructions loaded on-demand via `skill` tool.

Structure:

```
skills/<category>/<skill-name>/
├── SKILL.md              # Main instructions (<500 lines)
└── reference/            # Optional detailed docs
    ├── patterns.md
    └── examples.md
```

Frontmatter:

```yaml
---
name: skill-name            # Must match directory name
description: What + when    # Max 1024 chars, critical for discovery
license: MIT                # Optional
compatibility: opencode     # Optional
metadata:                   # Optional key-value pairs
  audience: developers
---
```

Name rules:
- 1-64 characters
- Lowercase alphanumeric + hyphens
- No leading/trailing hyphens
- No consecutive hyphens

Skill permissions:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

### Commands

Custom slash commands:

```yaml
# In commands/<name>.md
---
description: Shown in command list
agent: build              # Optional: specific agent
model: provider/model     # Optional: override model
subtask: true             # Optional: run as subagent
---

Prompt template with $ARGUMENTS or $1, $2, etc.

Shell output: !`git status`
File reference: @src/file.ts
```

### MCP Servers

External tools via Model Context Protocol:

```json
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-server"],
      "environment": { "API_KEY": "{env:MY_KEY}" },
      "enabled": true,
      "timeout": 5000
    },
    "remote-server": {
      "type": "remote",
      "url": "https://mcp.example.com",
      "headers": { "Authorization": "Bearer {env:TOKEN}" },
      "oauth": {}  // Enable OAuth
    }
  }
}
```

MCP CLI commands:

```bash
opencode mcp auth <server>      # Authenticate
opencode mcp list               # List servers
opencode mcp logout <server>    # Remove credentials
opencode mcp debug <server>     # Diagnose issues
```

### Custom Tools

TypeScript/JavaScript functions the LLM can call:

```typescript
// .opencode/tools/my-tool.ts
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "What this tool does",
  args: {
    param: tool.schema.string().describe("Parameter description")
  },
  async execute(args, context) {
    const { agent, sessionID, messageID } = context
    return "result"
  }
})
```

Multiple tools per file:

```typescript
export const add = tool({ /* ... */ })      // my-tool_add
export const subtract = tool({ /* ... */ }) // my-tool_subtract
```

### ACP Support

Agent Client Protocol for IDE integration:

```bash
opencode acp  # Start as ACP subprocess
```

Configure in Zed:

```json
{
  "agent_servers": {
    "OpenCode": {
      "command": "opencode",
      "args": ["acp"]
    }
  }
}
```

## This Repository's Structure

```
ai-knowledgebase/
├── skills/                 # 31 skills in 8 categories
│   ├── research-strategy/
│   ├── github-workflow/
│   ├── frontend-development/
│   ├── testing/
│   ├── documentation/
│   ├── design/
│   ├── infrastructure/
│   └── codebase-structures/
├── commands/               # 20 commands
├── agents/                 # 7 agents (including ai-coordinator)
├── .opencode/
│   ├── config.json
│   ├── skills/             # Symlinks to skills/
│   ├── commands -> ../commands
│   └── agents -> ../agents
├── research/               # Research documents
├── opencode/               # OpenCode documentation
└── tools/
    └── check-links.sh      # Link validator
```

## Creating AI Automation

### Decision Framework

```
What are you automating?
│
├─ Detailed workflow with conventions?
│   └─ SKILL (100-500 lines, loaded on-demand)
│
├─ Quick trigger for existing skill?
│   └─ COMMAND (5-50 lines, loads skills)
│
└─ Restricted tool access persona?
    └─ AGENT (50-200 lines, tool restrictions)
```

### Creating a Skill

1. **Check for duplicates**:
   ```bash
   grep -ri "<keyword>" skills/*/SKILL.md -l
   ```

2. **Choose category**: Match existing categories

3. **Create files**:
   ```bash
   mkdir -p skills/<category>/<skill-name>
   # Write skills/<category>/<skill-name>/SKILL.md
   ```

4. **Create symlink**:
   ```bash
   cd .opencode/skills/
   ln -s ../../skills/<category>/<skill-name> <skill-name>
   ```

5. **Update README**: Add to skills/README.md

6. **Test**:
   ```bash
   ls -la .opencode/skills/<skill-name>
   ./tools/check-links.sh
   ```

### Creating an Agent

1. Create `agents/<name>.md`
2. Add frontmatter with description, mode, tools
3. Symlink already exists (agents -> .opencode/agents)

### Creating a Command

1. Create `commands/<name>.md`
2. Add frontmatter with description
3. Symlink already exists (commands -> .opencode/commands)

## Troubleshooting

### Skill Not Loading

1. Check SKILL.md exists and is capitalized
2. Verify frontmatter has `name` and `description`
3. Check symlink: `ls -la .opencode/skills/<name>`
4. Check permissions aren't denying it

### Agent Not Appearing

1. Verify description in frontmatter
2. Check mode (primary vs subagent)
3. Check hidden isn't set to true

### MCP Server Issues

```bash
opencode mcp debug <server>  # Check connectivity and auth
```

### Permission Denied

1. Check global permissions in config
2. Check agent-specific overrides
3. Verify pattern matching (last match wins)

## Resources

- Documentation: https://opencode.ai/docs/
- GitHub: https://github.com/anomalyco/opencode
- Discord: https://opencode.ai/discord
- Releases: https://github.com/anomalyco/opencode/releases

## Output to User

When answering OpenCode questions:
1. Cite the documentation source
2. Note if information might be outdated
3. Suggest checking release notes for recent changes
4. Provide actionable configuration examples
