# Claude Code Extension Types: A Complete Disambiguation Guide

This document provides clear definitions and distinctions between the different extension types in Claude Code. These concepts are frequently confused, leading to incorrect implementations.

---

## Quick Reference: Comparison Table

| Type | Purpose | Invocation | Scope | Tool Access | Use When |
|------|---------|------------|-------|-------------|----------|
| **Skills** | Teach Claude specialized knowledge and workflows | **Automatic** - Claude chooses based on context | Project, Personal, Enterprise, Plugin | Full access (can restrict with `allowed-tools`) | You need Claude to automatically apply domain expertise |
| **Slash Commands** | Reusable prompt shortcuts | **Manual** - User types `/command` | Project, Personal, Plugin | Inherits from conversation (can specify in frontmatter) | You want explicit control over when a prompt runs |
| **Hooks** | Execute scripts on system events | **Automatic** - Triggered by tool events | User settings, Project settings, Plugin | N/A - runs external scripts | You need to respond to file changes, session events |
| **MCP Servers** | Connect Claude to external tools/data | **Automatic** - Claude calls tools as needed | Local, Project, User, Enterprise | Provides new tools to Claude | You need to integrate external services or databases |
| **Plugins** | Bundle and distribute multiple extension types | **Manual** - User installs via `/plugin` | Installed per-user or per-project | Contains any of the above | You want to share a collection of extensions |

---

## Decision Flowchart

Use this flowchart to determine which extension type you need:

```
START: What are you trying to accomplish?
                    |
                    v
    +---------------------------------------+
    | Need to respond to system events?     |
    | (file saves, session start, tool use) |
    +---------------------------------------+
                    |
           YES -----|-----  NO
            |               |
            v               v
        [HOOKS]     +----------------------------------+
                    | Need external service integration?|
                    | (databases, APIs, third-party)   |
                    +----------------------------------+
                                    |
                           YES -----|-----  NO
                            |               |
                            v               v
                      [MCP SERVER]  +-----------------------------+
                                    | Need a shortcut for a       |
                                    | frequently-used prompt?     |
                                    +-----------------------------+
                                                    |
                                           YES -----|-----  NO
                                            |               |
                                            v               v
                                    [SLASH COMMAND] +-------------------------+
                                                    | Need complex guidance,  |
                                                    | domain knowledge, or    |
                                                    | multi-file workflows?   |
                                                    +-------------------------+
                                                                    |
                                                           YES -----|-----  NO
                                                            |               |
                                                            v               v
                                                        [SKILL]     Consider CLAUDE.md
                                                                    for project-wide
                                                                    instructions
```

### Additional Decision Points

- **Need to bundle multiple extensions?** -> Use a **Plugin**
- **Want team-wide project instructions?** -> Use **CLAUDE.md**
- **Need to delegate tasks with tool isolation?** -> Use a **Subagent**

---

## Detailed Sections

### Skills

#### What It Is
A Skill is a markdown file (`SKILL.md`) that teaches Claude how to do something specific. Skills contain specialized knowledge, workflows, and instructions that Claude automatically applies when your request matches the Skill's description.

#### How It's Invoked
**Model-invoked (automatic)**. Claude reads all available Skill names and descriptions at startup. When your request semantically matches a Skill's description, Claude asks to activate it. You confirm, and the full Skill content loads into context.

#### What It Can Do
- Provide domain-specific knowledge and best practices
- Include supporting files (reference docs, examples, scripts)
- Restrict tool access with `allowed-tools` frontmatter
- Bundle utility scripts that Claude can execute
- Use progressive disclosure to manage context efficiently

#### Example Use Cases
- Code review following team standards
- PDF processing with form-filling workflows
- Database query patterns for your specific schema
- Documentation generation in your preferred format

#### File Structure
```
~/.claude/skills/my-skill/          # Personal
.claude/skills/my-skill/            # Project
    SKILL.md                        # Required - main instructions
    reference.md                    # Optional - detailed docs
    examples.md                     # Optional - usage examples
    scripts/                        # Optional - utility scripts
        helper.py
```

#### Common Mistakes
- Creating a `SKILL.md` and expecting to invoke it with `/skill-name` (Skills are NOT slash commands)
- Putting all content in `SKILL.md` instead of using progressive disclosure
- Writing vague descriptions that don't help Claude match requests

---

### Slash Commands

#### What It Is
A slash command is a markdown file in a `commands/` directory that defines a reusable prompt. When you type `/command-name`, Claude executes the prompt defined in that file.

#### How It's Invoked
**User-invoked (manual)**. You explicitly type `/command-name [arguments]` to run the command. Claude will NOT automatically use slash commands based on context.

#### What It Can Do
- Accept arguments via `$ARGUMENTS`, `$1`, `$2`, etc.
- Execute bash commands using `!` prefix (requires `allowed-tools` for Bash)
- Reference files using `@file-path` syntax
- Specify model, allowed-tools, and description in frontmatter
- Trigger extended thinking with specific keywords

#### Example Use Cases
- `/commit` - Generate commit messages from staged changes
- `/review` - Run a quick code review checklist
- `/deploy staging` - Execute deployment commands
- `/explain @src/utils.js` - Explain a specific file

#### File Structure
```
~/.claude/commands/                 # Personal commands
.claude/commands/                   # Project commands
    my-command.md                   # Creates /my-command
    frontend/                       # Subdirectory for namespacing
        build.md                    # Creates /build (shows "project:frontend")
```

#### Frontmatter Example
```markdown
---
allowed-tools: Bash(git:*), Read
description: Create a git commit from staged changes
argument-hint: [optional message]
model: claude-sonnet-4-20250514
---

## Context
- Current git status: !`git status`
- Staged changes: !`git diff --staged`

## Task
Create a commit message based on the staged changes.
```

#### Common Mistakes
- Expecting Claude to automatically run `/my-command` when it seems relevant (it won't)
- Confusing slash commands with Skills (slash commands are explicit, Skills are automatic)
- Forgetting to add `allowed-tools` when using bash execution

---

### Hooks

#### What It Is
A hook is a configuration that runs external scripts or commands in response to specific events in Claude Code. Hooks are defined in settings files (not markdown) and execute automatically when their trigger event occurs.

#### How It's Invoked
**Event-driven (automatic)**. Hooks fire when specific events occur:
- `PreToolUse` - Before a tool executes
- `PostToolUse` - After a tool completes
- `PermissionRequest` - When permission dialog appears
- `UserPromptSubmit` - When user submits a prompt
- `Stop` / `SubagentStop` - When Claude finishes responding
- `SessionStart` / `SessionEnd` - Session lifecycle events
- `Notification` - When Claude sends notifications
- `PreCompact` - Before context compaction

#### What It Can Do
- Run bash scripts on specific events
- Block, allow, or modify tool calls
- Inject context into conversations
- Validate user prompts before processing
- Auto-format files after edits
- Log session activity
- Use prompt-based LLM evaluation for complex decisions

#### Example Use Cases
- Auto-lint files after Write/Edit operations
- Validate bash commands before execution
- Add context at session start (load environment, recent changes)
- Send notifications when Claude needs permission

#### Configuration Structure
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint:fix",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

#### Configuration Locations
- `~/.claude/settings.json` - User settings
- `.claude/settings.json` - Project settings
- `.claude/settings.local.json` - Local project settings (not committed)
- Plugin `hooks/hooks.json` - Plugin-provided hooks

#### Common Mistakes
- Creating a `hooks/` directory with markdown files (hooks use JSON configuration)
- Expecting hooks to work like Skills (hooks run scripts, Skills provide knowledge)
- Forgetting that hooks run external commands, not Claude prompts

---

### MCP Servers

#### What It Is
An MCP (Model Context Protocol) server connects Claude to external tools, databases, and APIs. MCP servers provide new capabilities to Claude by exposing tools through a standardized protocol.

#### How It's Invoked
**Tool-invoked (automatic)**. Once connected, Claude can call MCP tools as needed to fulfill requests. MCP tools appear alongside built-in tools (Read, Write, Bash, etc.).

#### What It Can Do
- Connect to databases (PostgreSQL, SQLite, etc.)
- Integrate with external services (GitHub, Sentry, Notion, etc.)
- Provide custom tools specific to your infrastructure
- Expose resources as `@` mentions
- Expose prompts as slash commands (`/mcp__server__prompt`)

#### Example Use Cases
- Query production databases directly
- Create GitHub issues and PRs
- Monitor Sentry errors
- Access internal company APIs

#### Configuration Methods
```bash
# HTTP server (recommended for remote)
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# Stdio server (local processes)
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"

# SSE server (deprecated, use HTTP)
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

#### Installation Scopes
- `local` (default) - Private, current project only
- `project` - Shared via `.mcp.json` file (committed)
- `user` - Available across all your projects

#### Common Mistakes
- Thinking MCP servers are the same as plugins (MCP provides tools, plugins bundle extensions)
- Confusing MCP tools with Skills (MCP provides capabilities, Skills provide knowledge)
- Not understanding that MCP servers run as separate processes

---

### Plugins

#### What It Is
A plugin is a distributable package that bundles multiple extension types together. Plugins have a manifest file (`.claude-plugin/plugin.json`) and can contain slash commands, Skills, hooks, MCP servers, and LSP servers.

#### How It's Invoked
**User-installed**. You install plugins via `/plugin install` from a marketplace, or load them with `--plugin-dir` for development. Once installed, their components become available.

#### What It Can Do
- Bundle slash commands (namespaced as `/plugin-name:command`)
- Include Skills that Claude can automatically use
- Provide hooks that trigger on events
- Configure MCP servers that start automatically
- Configure LSP servers for code intelligence
- Define custom agents

#### Example Use Cases
- Distribution of team-specific tooling
- Marketplace packages for common workflows
- Language support bundles (LSP + linting hooks)
- Integration packages (MCP + Skills for a service)

#### Directory Structure
```
my-plugin/
    .claude-plugin/
        plugin.json             # Required - manifest
    commands/                   # Slash commands
        hello.md
    skills/                     # Agent Skills
        code-review/
            SKILL.md
    hooks/                      # Event hooks
        hooks.json
    agents/                     # Custom agents
        reviewer/
            AGENT.md
    .mcp.json                   # MCP server configs
    .lsp.json                   # LSP server configs
```

#### Common Mistakes
- Putting `commands/`, `skills/`, etc. inside `.claude-plugin/` (they go at plugin root)
- Confusing plugins with MCP servers (plugins are packages, MCP servers are tool providers)
- Not understanding that plugin commands are namespaced (`/plugin:command`)

---

## "NOT the Same" Section: Common Confusions

### Skills are NOT Slash Commands

| Skills | Slash Commands |
|--------|----------------|
| Model-invoked (automatic) | User-invoked (manual) |
| Claude chooses when relevant | You type `/command` explicitly |
| Located in `skills/` directory | Located in `commands/` directory |
| Uses `SKILL.md` filename | Uses any `.md` filename |
| Semantic matching on description | Exact command name matching |
| Can include multiple files | Single file only |

**Example of confusion**: "I created a Skill called `code-review` but `/code-review` doesn't work."
**Why**: Skills don't create slash commands. Claude uses Skills automatically when your request matches the Skill's description.

---

### Hooks are NOT Skills

| Hooks | Skills |
|-------|--------|
| Run external scripts | Provide Claude with knowledge |
| Configured in JSON settings | Defined in markdown files |
| Trigger on system events | Activate based on request context |
| Execute before/after tool use | Load into Claude's context |
| Can block or modify actions | Guide Claude's responses |

**Example of confusion**: "I want to auto-format files when Claude writes them, so I created a Skill."
**Why**: File formatting on save is a Hook (PostToolUse event), not a Skill. Skills don't run scripts.

---

### MCP Servers are NOT Plugins

| MCP Servers | Plugins |
|-------------|---------|
| Provide tools to Claude | Bundle extension types |
| Run as separate processes | Are file directories |
| Single-purpose integrations | Multi-component packages |
| Added with `claude mcp add` | Installed with `/plugin install` |
| Connect to external services | Contain commands, Skills, hooks |

**Example of confusion**: "I installed the GitHub MCP server, so now I have the GitHub plugin."
**Why**: MCP servers and plugins are different. The GitHub MCP server provides GitHub tools. A GitHub plugin might bundle Skills, commands, AND an MCP server.

---

### Slash Commands are NOT Agents

| Slash Commands | Subagents |
|----------------|-----------|
| Run in current context | Run in isolated context |
| Single prompt execution | Can perform multi-step tasks |
| Inherit conversation tools | Have their own tool restrictions |
| No persistent state | Can maintain task state |
| User explicitly invokes | Claude can delegate tasks |

**Example of confusion**: "I need an agent that reviews code, so I created a slash command."
**Why**: If you need task isolation or different tool access, use a subagent. Slash commands run in the current context.

---

### CLAUDE.md is NOT a Skill

| CLAUDE.md | Skills |
|-----------|--------|
| Loaded into every conversation | Loaded when contextually relevant |
| Project-wide instructions | Domain-specific knowledge |
| Always active | Activated on demand |
| Single file per scope | Directory with multiple files |
| Cannot restrict tools | Can use `allowed-tools` |

**Example of confusion**: "I put my code review guidelines in CLAUDE.md so Claude uses them automatically."
**Why**: While this works, CLAUDE.md is for project-wide settings. If code review is a specialized workflow, a Skill is more appropriate and won't consume context in unrelated conversations.

---

## Summary: When to Use What

| I want to... | Use |
|--------------|-----|
| Give Claude domain expertise that activates automatically | **Skill** |
| Create a reusable prompt I invoke explicitly | **Slash Command** |
| Run a script when Claude uses certain tools | **Hook** |
| Connect Claude to an external database or API | **MCP Server** |
| Share multiple extensions as a package | **Plugin** |
| Set project-wide coding standards | **CLAUDE.md** |
| Delegate tasks with isolated tool access | **Subagent** |

---

## Related Documentation

- [Agent Skills](/en/skills) - Complete Skill authoring guide
- [Slash Commands](/en/slash-commands) - Command syntax and features
- [Hooks Reference](/en/hooks) - Hook events and configuration
- [MCP Integration](/en/mcp) - Connecting external tools
- [Plugins](/en/plugins) - Creating and distributing plugins
- [Subagents](/en/sub-agents) - Task delegation
- [Memory (CLAUDE.md)](/en/memory) - Project instructions

---

*Last Updated: January 2025*
*Source: Official Claude Code documentation at code.claude.com*
