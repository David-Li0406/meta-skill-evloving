# Claude Code → OpenCode Plugin Conversion Guide

The definitive guide for converting Claude Code plugins to OpenCode format.

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Feature Parity](#feature-parity)
4. [Skill Classification](#skill-classification)
5. [Converting User-Invocable Skills → Commands](#converting-user-invocable-skills--commands)
6. [Converting Non-User-Invocable Skills → Skills](#converting-non-user-invocable-skills--skills)
7. [Converting Agents](#converting-agents)
8. [Converting Hooks](#converting-hooks)
9. [Prompt Content Transformations](#prompt-content-transformations)
10. [Model Mapping](#model-mapping)
11. [Plugin Manifest Conversion](#plugin-manifest-conversion)
12. [Known Plugins Classification](#known-plugins-classification)
13. [Edge Cases & Limitations](#edge-cases--limitations)
14. [Migration Checklist](#migration-checklist)

---

## Overview

Claude Code and OpenCode share similar concepts but with different implementations:

| Concept | Claude Code | OpenCode |
|---------|-------------|----------|
| User commands | Skills (user-invocable) | Commands (`command/*.md`) |
| Internal skills | Skills (non-user-invocable) | Skills (`skill/*/SKILL.md`) |
| Subagents | Agents | Agents (`agent/*.md`) |
| Event hooks | Python hooks | Hooks (`plugin/*.ts`) |
| Plugin bundles | Plugins (with plugin.json) | **No equivalent** - flat directories |
| External tools | MCP servers | MCP servers + custom tools |

**Terminology note**: OpenCode confusingly calls hooks "plugins" (stored in `plugin/` directory). There's no "plugin bundle" concept - OpenCode uses flat directories that are merged together. This repo organizes related resources into directories we call "plugins" for convenience.

---

## Directory Structure

### Claude Code Plugin Layout

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skill/
│   ├── review/
│   │   └── SKILL.md         # User-invocable skill
│   └── chunk-impl/
│       └── SKILL.md         # Non-user-invocable skill
├── agent/
│   └── bug-fixer.md         # Subagent definition
├── hooks/
│   ├── pyproject.toml
│   └── session_start.py     # Python hook
└── README.md
```

### OpenCode Plugin Layout (Source)

This is the **source** layout for plugins in this repository:

```
my-plugin/
├── package.json             # Plugin metadata (for npm publishing)
├── command/
│   └── review.md            # User-invocable command
├── skill/
│   └── chunk-impl/
│       └── SKILL.md         # Non-user-invocable skill
├── agent/
│   └── bug-fixer.md         # Subagent definition
├── plugin/
│   └── hooks.ts             # TypeScript hooks (optional)
└── README.md
```

### OpenCode Discovery (Installed)

OpenCode discovers resources from **flat directories**, not nested plugin structures. The `install.sh` script copies files with a **plugin postfix** to avoid name collisions:

```
~/.config/opencode/
├── command/
│   ├── review-vibe-workflow.md        # /review-vibe-workflow
│   ├── plan-vibe-workflow.md          # /plan-vibe-workflow
│   ├── define-vibe-experimental.md    # /define-vibe-experimental
│   └── ...
├── agent/
│   ├── bug-fixer-vibe-workflow.md
│   ├── criteria-checker-vibe-experimental.md
│   └── ...
├── skill/
│   └── verify-vibe-experimental/
│       └── SKILL.md
└── plugin/
    ├── vibe-workflow-hooks.ts
    └── vibe-experimental-hooks.ts
```

**Naming convention**: All files are postfixed with `-<plugin-name>` to:
- Avoid collisions between plugins with similar commands/agents
- Enable clean uninstall per plugin
- Support sync (deletions detected by postfix pattern)

**Installation**: Use `install.sh` which performs a full sync:
1. Cleans existing files for the plugin (by postfix pattern)
2. Copies fresh files from source
3. Updates `name:` fields to match new filenames
4. Updates internal references: `/command` → `/command-<plugin>`, `skill({ name: "x" })` → `skill({ name: "x-<plugin>" })`

### Path Mapping

| Claude Code | OpenCode (Source) | OpenCode (Installed) |
|-------------|-------------------|----------------------|
| `.claude-plugin/plugin.json` | `package.json` | N/A (metadata only) |
| `skill/<name>/SKILL.md` (user-invocable) | `command/<name>.md` | `command/<name>-<plugin>.md` |
| `skill/<name>/SKILL.md` (non-user-invocable) | `skill/<name>/SKILL.md` | `skill/<name>-<plugin>/SKILL.md` |
| `agent/<name>.md` | `agent/<name>.md` | `agent/<name>-<plugin>.md` |
| `hooks/*.py` | `plugin/hooks.ts` | `plugin/<plugin>-hooks.ts` |

---

## Feature Parity

| Feature | Claude Code | OpenCode | Parity | Notes |
|---------|-------------|----------|--------|-------|
| User-invocable skills | `skill/*/SKILL.md` | `command/*.md` | ✅ Full | Different path |
| Non-user-invocable skills | `skill/*/SKILL.md` | `skill/*/SKILL.md` | ✅ Full | Same format |
| Agents/subagents | `agent/*.md` | `agent/*.md` | ✅ Full | Different frontmatter |
| SessionStart hook | Python | TypeScript | ✅ Full | Use `event` + `experimental.chat.system.transform` |
| PreToolUse hook (observe) | Python | TypeScript | ✅ Full | `tool.execute.before` - observe/modify |
| PreToolUse hook (block) | Python | TypeScript | ⚠️ Partial | Use `permission.ask` hook instead |
| PostToolUse hook | Python | TypeScript | ⚠️ Partial | `tool.execute.after` - no additionalContext |
| Stop hook (blocking) | Python | N/A | ❌ None | Cannot block in OpenCode |
| Permission control | N/A | TypeScript | ✅+ Better | `permission.ask` hook can allow/deny/ask |
| MCP servers | `.mcp.json` | `opencode.json` | ✅ Full | Different config location |
| Custom tools | Via MCP only | `tools/*.ts` | ✅+ Better | OpenCode has native tools |
| Model routing | Auto Haiku | Manual | ⚠️ Partial | No auto-routing |
| `$ARGUMENTS` | Yes | Yes | ✅ Full | Same placeholder |
| Positional args | No | `$1`, `$2`, `$3` | ✅+ Better | OpenCode adds these |
| Bash injection | No | `` !`cmd` `` | ✅+ Better | OpenCode adds this |
| File injection | No | `@filename` | ✅+ Better | OpenCode adds this |

---

## Skill Classification

### Critical Distinction: Commands vs Skills in OpenCode

**OpenCode commands (`command/*.md`):**
- Only invocable by **users** via `/command-name` in TUI
- The model **CANNOT** call commands programmatically
- Appear in autocomplete menu

**OpenCode skills (`skill/*/SKILL.md`):**
- Loaded by the **model** via `skill({ name: "skill-name" })` tool
- Users do NOT see these in the `/` menu
- Used for programmatic/automated workflows

### Detection Rules: Skill → Command or Skill?

A Claude Code skill becomes an **OpenCode skill** (NOT command) if ANY of:
1. Has `user-invocable: false` in frontmatter
2. Is referenced by any agent, skill, or command for programmatic invocation (e.g., `Skill("plugin:verify")`)
3. Has more than just `SKILL.md` in its directory (e.g., has `references/`, scripts, etc.)
4. Description indicates it's called by another command (e.g., "called by /do, not directly")

A Claude Code skill becomes an **OpenCode command** if:
1. It's user-invocable (default) AND
2. It's NOT referenced for programmatic invocation by other resources AND
3. It only contains `SKILL.md` (no supporting files)

**Default**: If unsure, convert to **command** (user-invocable is the default).

**Note**: Internal helpers like `chunk-implementor` in vibe-workflow are **agents**, not skills. Check if the file is in `skill/` or `agent/` directory.

### Conversion Strategy

| Skill Type | → | OpenCode Target | Why |
|------------|---|-----------------|-----|
| User-invocable only | → | `command/*.md` | User invokes via `/command` |
| Referenced by other resources | → | `skill/*/SKILL.md` | Model loads via `skill()` tool |
| Has supporting files | → | `skill/*/SKILL.md` | Preserves directory structure |
| `user-invocable: false` | → | `skill/*/SKILL.md` | Explicit non-user-invocable |

---

## Converting User-Invocable Skills → Commands

### Frontmatter Transformation

**Claude Code:**
```yaml
---
name: review
description: Run all code review agents in parallel
model: sonnet
---
```

**OpenCode:**
```yaml
---
description: Run all code review agents in parallel
model: anthropic/claude-sonnet-4-5-20250929
---
```

### Frontmatter Field Mapping

| Claude Code | OpenCode | Action |
|-------------|----------|--------|
| `name:` | (filename) | **Remove** - filename is the command name |
| `description:` | `description:` | Keep as-is |
| `model:` | `model:` | Convert to full model ID |
| N/A | `agent:` | Optional - references an agent name to execute the command |
| N/A | `subtask:` | Add `true` if should run as subagent |

**Note**: The `agent:` field references an **agent name** (e.g., `agent: reviewer`), not a mode. If omitted, the command runs with the default agent.

### File Path Change

```
# Claude Code
skill/review/SKILL.md

# OpenCode
command/review.md
```

Note: OpenCode commands are flat files, not directories.

---

## Converting Non-User-Invocable Skills → Skills

### Format Comparison

Non-user-invocable skills are nearly identical between platforms.

**Claude Code:**
```yaml
---
name: verify
description: 'Manifest verification runner. Called by /do, not directly by users.'
user-invocable: false
---
```

**OpenCode:**
```yaml
---
name: verify
description: 'Manifest verification runner. Called by /do, not directly by users.'
---
```

### Key Difference

| Field | Claude Code | OpenCode | Notes |
|-------|-------------|----------|-------|
| `name:` | Required | Required | **Keep it** for skills |
| `user-invocable:` | `false` | (remove) | OpenCode skills are not in `/` menu by default |
| Path | `skill/<name>/SKILL.md` | `skill/<name>/SKILL.md` | Same! |

### OpenCode Skill Discovery Paths

OpenCode finds skills in (order of precedence):
1. `.opencode/skill/<name>/SKILL.md` (project)
2. `~/.config/opencode/skill/<name>/SKILL.md` (global)
3. `.claude/skill/<name>/SKILL.md` (Claude-compatible!)
4. `~/.claude/skill/<name>/SKILL.md` (Claude-compatible!)

This means Claude Code skills can often work without modification.

---

## Converting Agents

### Frontmatter Transformation

**Claude Code:**
```yaml
---
name: bug-fixer
description: Expert bug investigator and fixer
tools: Bash, Glob, Grep, Read, Edit, Write, WebFetch, TodoWrite, WebSearch
model: opus
---
```

**OpenCode:**
```yaml
---
description: Expert bug investigator and fixer
mode: subagent
model: openai/gpt-5.2
temperature: 0.3
tools:
  read: true
  edit: true
  bash: true
  webfetch: true
  websearch: true
---
```

### Frontmatter Field Mapping

| Claude Code | OpenCode | Action |
|-------------|----------|--------|
| `name:` | (filename) | **Remove** |
| `description:` | `description:` | Keep |
| `tools:` (comma list) | `tools:` (object) | **Convert format** |
| `model:` | `model:` | Convert to full ID |
| N/A | `mode:` | **Add** `subagent` or `primary` |
| N/A | `temperature:` | Optional, add if needed |
| N/A | `maxSteps:` | Optional iteration limit |
| N/A | `hidden:` | Optional, hide from autocomplete |
| N/A | `reasoningEffort:` | Optional, see [Reasoning Effort](#reasoning-effort) |

### Reasoning Effort

OpenCode supports `reasoningEffort` in agent frontmatter to control thinking depth for supported models (OpenAI reasoning models, Claude with extended thinking).

**Automatic for reasoning models**: When converting `model: opus` → `model: openai/gpt-5.2`, automatically add `reasoningEffort: xhigh` for agents. This enables extended reasoning capabilities that match the intent of using a high-capability model.

**When requested for other models**: If the user explicitly requests reasoning effort via the sync skill (e.g., `/sync-from-claude-plugins --reasoning-effort`), add to all agents (not just opus-mapped ones):

```yaml
reasoningEffort: medium
```

Valid values: `low`, `medium`, `high`, `xhigh`

For Claude models, you can alternatively use `thinking.budgetTokens`:

```yaml
thinking:
  type: enabled
  budgetTokens: 16000
```

### Tool Permission Mapping

| Claude Code | OpenCode | Notes |
|-------------|----------|-------|
| `Bash` | `bash: true` | |
| `Read` | `read: true` | |
| `Edit` | `edit: true` | Covers write, patch, multiedit |
| `Write` | `edit: true` | Same as edit in OpenCode |
| `Glob` | `glob: true` | |
| `Grep` | `grep: true` | |
| `WebFetch` | `webfetch: true` | |
| `WebSearch` | `websearch: true` | |
| `TodoWrite` | `todowrite: true` | |
| `TodoRead` | `todoread: true` | |
| `Task` | `task: true` | For spawning subagents |
| `Skill` | `skill: true` | For loading skills |
| `SlashCommand` | `skill: true` | Same as Skill in OpenCode |
| `NotebookEdit` | `edit: true` | No separate notebook permission |

**Additional OpenCode permissions** (no Claude Code equivalent):
- `list: true` — directory listing
- `lsp: true` — LSP queries
- `codesearch: true` — code search
- `external_directory: true` — paths outside project
- `doom_loop: true` — repeated identical calls

All tools are **enabled by default** in OpenCode. Specifying them explicitly in agent frontmatter ensures the agent has access even if global config restricts them.

**IMPORTANT**: Explicitly set interactive tools to `false` for all subagents since they run autonomously:
- `question: false` - subagents should not prompt users for input

If a Claude Code agent has no `tools:` line, add a minimal tools section with just the disabled interactive tools:
```yaml
tools:
  question: false
```

### Permission Values

Tool permissions use **boolean values**:
- `true` - Tool is permitted
- `false` - Tool is denied (or simply omit the tool)

---

## Converting Hooks

### Event Mapping

| Claude Code | OpenCode Hook | Can Block? | Notes |
|-------------|---------------|------------|-------|
| `SessionStart` | `event` + `experimental.chat.system.transform` | N/A | See below |
| `PostCompact` | `experimental.session.compacting` | N/A | Re-inject context after compaction |
| `PostToolUse` | `tool.execute.after` | No | React to tool completion |
| `PreToolUse` | `tool.execute.before` | **No** | Can modify args but NOT block |
| `Stop` | `event` (session.idle) | **No** | Cannot prevent stopping |
| `SubagentStop` | N/A | — | ❌ No equivalent |

**CRITICAL**: Session lifecycle events (`session.created`, `session.idle`) are caught via the **`event`** hook, NOT as direct hook keys. The `event` hook receives `{ event: Event }` where `event.type` can be `"session.created"`, `"session.idle"`, etc.

**IMPORTANT**: OpenCode's `tool.execute.before` **CANNOT block** execution. There is no `output.abort` field. It can only modify `output.args`. For gating logic, log warnings instead of blocking.

### Complete Hooks Interface (Reference)

From `@opencode-ai/plugin` (source: github.com/sst/opencode):

```typescript
export interface Hooks {
  // Event handler for ALL lifecycle events (session, file, message, etc.)
  event?: (input: { event: Event }) => Promise<void>

  // Configuration hook
  config?: (input: Config) => Promise<void>

  // Custom tools definition
  tool?: { [key: string]: ToolDefinition }

  // Authentication hook
  auth?: AuthHook

  // Chat manipulation hooks
  "chat.message"?: (input: { sessionID: string; agent?: string; ... }, output: { message: UserMessage; parts: Part[] }) => Promise<void>
  "chat.params"?: (input: { sessionID: string; agent: string; model: Model; ... }, output: { temperature: number; topP: number; topK: number; options: Record<string, any> }) => Promise<void>
  "chat.headers"?: (input: { sessionID: string; ... }, output: { headers: Record<string, string> }) => Promise<void>

  // Permission hook - can control allow/deny/ask
  "permission.ask"?: (input: Permission, output: { status: "ask" | "deny" | "allow" }) => Promise<void>

  // Command execution hook
  "command.execute.before"?: (input: { command: string; sessionID: string; arguments: string }, output: { parts: Part[] }) => Promise<void>

  // Tool execution hooks
  "tool.execute.before"?: (input: { tool: string; sessionID: string; callID: string }, output: { args: any }) => Promise<void>
  "tool.execute.after"?: (input: { tool: string; sessionID: string; callID: string }, output: { title: string; output: string; metadata: any }) => Promise<void>

  // Experimental hooks
  "experimental.chat.messages.transform"?: (input: {}, output: { messages: { info: Message; parts: Part[] }[] }) => Promise<void>
  "experimental.chat.system.transform"?: (input: { sessionID: string }, output: { system: string[] }) => Promise<void>
  "experimental.session.compacting"?: (input: { sessionID: string }, output: { context: string[]; prompt?: string }) => Promise<void>
  "experimental.text.complete"?: (input: { sessionID: string; messageID: string; partID: string }, output: { text: string }) => Promise<void>
}
```

### Event Types (via `event` hook)

The `event` hook receives events with `event.type` set to one of:

| Category | Event Types |
|----------|-------------|
| Session | `session.created`, `session.updated`, `session.deleted`, `session.idle`, `session.error`, `session.compacted`, `session.diff`, `session.status` |
| Message | `message.updated`, `message.removed`, `message.part.updated`, `message.part.removed` |
| File | `file.edited`, `file.watcher.updated` |
| Permission | `permission.updated`, `permission.replied` |
| Command | `command.executed` |
| Tool | `tool.execute.before`, `tool.execute.after` |
| Todo | `todo.updated` |
| Installation | `installation.updated` |
| LSP | `lsp.client.diagnostics`, `lsp.updated` |
| Server | `server.connected` |
| TUI | `tui.prompt.append`, `tui.command.execute`, `tui.toast.show` |

### Complete TypeScript Hook Template

Create `plugin/hooks.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin"

/**
 * OpenCode hooks for <plugin-name> plugin.
 * Converted from Python hooks in claude-code-plugins.
 *
 * PluginInput parameters:
 * - client: OpenCode SDK client for logging and AI interactions
 * - project: Current project information
 * - directory: Current working directory
 * - worktree: Git worktree path
 * - serverUrl: OpenCode server URL
 * - $: Bun shell API for executing commands
 *
 * CRITICAL API NOTES:
 * - Session events (session.created, session.idle) go through the `event` hook
 * - tool.execute.before/after use `input.tool` (NOT input.call.name)
 * - tool.execute.before CANNOT block - can only modify output.args
 * - No additionalContext return is supported
 */

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree, serverUrl }) => {
  return {
    /**
     * Event handler for session lifecycle events
     * Catches session.created, session.idle, etc.
     * Converted from: SessionStart and Stop hooks
     */
    event: async ({ event }) => {
      if (event.type === "session.created") {
        await client.app.log({
          service: "my-plugin",
          level: "info",
          message: "Session started"
        });
      }

      if (event.type === "session.idle") {
        // LIMITATION: Cannot block stopping in OpenCode
        await client.app.log({
          service: "my-plugin",
          level: "debug",
          message: "Session idle"
        });
      }
    },

    /**
     * System prompt transformation - inject context
     * This is the main way to add context at session start.
     * Converted from: SessionStart hook (additionalContext)
     */
    "experimental.chat.system.transform": async (input, output) => {
      output.system.push(`<system-reminder>Your reminder text here</system-reminder>`);
    },

    /**
     * Session compacting - preserve context during compaction
     * Converted from: PostCompact / SessionStart with "compact" matcher
     */
    "experimental.session.compacting": async (input, output) => {
      output.context.push(`<preserved-state>Recovery info for compacted sessions</preserved-state>`);
    },

    /**
     * After tool execution - react to tool results
     * Converted from: PostToolUse hook
     *
     * NOTE: CANNOT return additionalContext - just log or modify output
     */
    "tool.execute.after": async (input, output) => {
      // Filter by tool name using input.tool (NOT input.call.name)
      if (input.tool !== "todo") return;

      await client.app.log({
        service: "my-plugin",
        level: "info",
        message: "Todo tool executed"
      });
    },

    /**
     * Before tool execution - modify args or log warnings
     * Converted from: PreToolUse hook
     *
     * LIMITATION: CANNOT block execution. No output.abort exists.
     * Can only modify output.args or log warnings.
     */
    "tool.execute.before": async (input, output) => {
      // Use input.tool (NOT input.call.name)
      if (input.tool !== "skill") return;

      // Access args via output.args (can read and modify)
      const args = output.args as { name?: string } | undefined;

      // Example: Log a warning (cannot block)
      if (args?.name === "dangerous-skill") {
        await client.app.log({
          service: "my-plugin",
          level: "warn",
          message: "Warning: dangerous-skill invoked"
        });
      }
    },
  };
};

export default MyPlugin;
```

### Alternative: Simple Default Export

For simpler plugins:

```typescript
import type { Plugin } from "@opencode-ai/plugin"

const MyPlugin: Plugin = async ({ client }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.created") {
        await client.app.log({
          service: "my-plugin",
          level: "info",
          message: "Session started"
        });
      }
    },

    "experimental.chat.system.transform": async (input, output) => {
      output.system.push("<system-reminder>Your context here</system-reminder>");
    },
  };
};

export default MyPlugin;
```

### Tool Name Mapping in Hooks

These are the tool names seen in `input.tool` within hook callbacks.

| Claude Code Tool | OpenCode Tool Name |
|-----------------|-------------------|
| `TodoWrite` | `todowrite` |
| `TodoRead` | `todoread` |
| `Bash` | `bash` |
| `Read` | `read` |
| `Edit` | `edit` |
| `Write` | `edit` |
| `Skill` | `skill` |
| `Task` | `task` |
| `AskUserQuestion` | `question` |

**Note**: There is no single `todo` tool - it's split into `todowrite` and `todoread`.

### Context Injection

**At session start**: Use `experimental.chat.system.transform` to push to `output.system`:
```typescript
"experimental.chat.system.transform": async (input, output) => {
  output.system.push("<system-reminder>Your message</system-reminder>");
}
```

**During compaction**: Use `experimental.session.compacting` to push to `output.context`:
```typescript
"experimental.session.compacting": async (input, output) => {
  output.context.push("<system-reminder>Recovery context</system-reminder>");
}
```

**NOTE**: Unlike Claude Code, OpenCode hooks **CANNOT return additionalContext** from `tool.execute.after` or other hooks. Use the system transform hooks above instead.

### What Cannot Be Converted

| Feature | Why | Workaround |
|---------|-----|------------|
| Stop blocking | `session.idle` cannot prevent stopping | Log warning |
| **PreToolUse blocking** | `tool.execute.before` has no `output.abort` | Use `permission.ask` hook OR log warning |
| SubagentStop | No equivalent event | None |
| Subagent tool interception | Hooks don't intercept subagent tool calls | Design around this limitation |
| MCP tool interception | MCP tool calls don't trigger hooks | Use MCP server-side logic |
| Python dependencies | Different runtime | Find TypeScript alternatives |
| additionalContext returns | Hooks cannot return additionalContext | Use system transform hooks |

**IMPORTANT**: Unlike Claude Code, OpenCode's `tool.execute.before` **CANNOT block** execution - there is no `output.abort` field. It can only modify `output.args` or log warnings.

**Alternative for blocking**: Use the `permission.ask` hook to control whether tools are allowed:
```typescript
"permission.ask": async (input, output) => {
  // Can set output.status to "allow", "deny", or "ask" (prompt user)
  if (shouldBlock(input)) {
    output.status = "deny";
  }
}
```

### Logging

Use `client.app.log()` with structured format:
```typescript
await client.app.log({
  service: "my-plugin",
  level: "info",     // debug | info | warn | error
  message: "Description of what happened",
  extra: { foo: "bar" }  // optional metadata
});
```

Enable verbose logging with `opencode --verbose`.

---

## Prompt Content Transformations

### Skill/Command References

**User-invocable skills → Slash commands:**

Claude Code:
```markdown
Skill("vibe-workflow:review")
Skill("vibe-workflow:explore-codebase", "authentication system")
```

OpenCode:
```markdown
/review
/explore-codebase authentication system
```

**Non-user-invocable skills → Skill tool:**

Claude Code:
```markdown
Skill("vibe-experimental:verify")
Skill("vibe-experimental:done", "task completed")
```

OpenCode:
```markdown
Use the skill tool: skill({ name: "verify" })
Use the skill tool with arguments: skill({ name: "done", arguments: "task completed" })
```

**Note**: The `skill()` tool is OpenCode's native way to programmatically load skill content into the conversation. It returns the SKILL.md content for the agent to use.

### Task Tool References

**Claude Code:**
```markdown
Launch the bug-fixer agent using the Task tool with subagent_type="vibe-workflow:bug-fixer"
```

**OpenCode:**
```markdown
Use the bug-fixer agent (defined in agent/bug-fixer.md)
```

### Model References

**Claude Code:**
```markdown
Use `model: opus` for complex analysis
```

**OpenCode:**
```markdown
Use `model: openai/gpt-5.2` for complex analysis
```

### Regex Replacements

Apply these transformations to prompt content:

**For user-invocable skills (→ commands):**
| Pattern | Replacement | Notes |
|---------|-------------|-------|
| `Skill\("[\w-]+:([\w-]+)"(?:,\s*"([^"]*)")?\)` | `/$1 $2` | Skill calls → slash commands |

**For non-user-invocable skills (→ skill tool):**
| Pattern | Replacement | Notes |
|---------|-------------|-------|
| `Skill\("[\w-]+:([\w-]+)"\)` | `skill({ name: "$1" })` | Skill calls → skill tool |
| `Skill\("[\w-]+:([\w-]+)",\s*"([^"]*)"\)` | `skill({ name: "$1", arguments: "$2" })` | With args |

**Tool name replacements:**
| Pattern | Replacement | Notes |
|---------|-------------|-------|
| `AskUserQuestion` | `question` | User question tool |
| `TodoWrite` | `todowrite` | Todo write tool |
| `TodoRead` | `todoread` | Todo read tool |

**Other replacements:**
| Pattern | Replacement | Notes |
|---------|-------------|-------|
| `\bopus\b` (in model context) | See [Model Mapping](#model-mapping) | |
| `\bsonnet\b` (in model context) | See [Model Mapping](#model-mapping) | |
| `\bhaiku\b` (in model context) | See [Model Mapping](#model-mapping) | |
| `Task tool with subagent_type` | `the <agent> agent` | Agent references |

### OpenCode Terminology (CLAUDE.md → AGENTS.md)

OpenCode uses different terminology for project instruction files:

| Claude Code | OpenCode | Notes |
|-------------|----------|-------|
| `CLAUDE.md` | `AGENTS.md` | Project-level AI instructions file |
| `~/.claude/CLAUDE.md` | `~/.config/opencode/AGENTS.md` | Global user instructions |

**Content transformations:**

| Find | Replace |
|------|---------|
| `CLAUDE.md` | `AGENTS.md` |
| `claude-md` (in names) | `agents-md` |
| `.claude/` (directory) | `.opencode/` |
| `~/.claude/` | `~/.config/opencode/` |

**File renaming:**

Files with "claude-md" in their name should be renamed to "agents-md":
- `review-claude-md-adherence.md` → `review-agents-md-adherence.md`
- `claude-md-adherence-reviewer.md` → `agents-md-adherence-reviewer.md`
- `update-claude-md.md` → `update-agents-md.md`

**Example content transformation:**

Claude Code:
```markdown
Check CLAUDE.md for project conventions.
Use the claude-md-adherence-reviewer agent.
```

OpenCode:
```markdown
Check AGENTS.md for project conventions.
Use the agents-md-adherence-reviewer agent.
```

---

## Model Mapping

This is the **canonical reference** for model ID conversion. All other sections reference this.

### Claude Code → OpenCode Model IDs

| Claude Code | OpenCode Full ID | Notes |
|-------------|------------------|-------|
| `opus` | `openai/gpt-5.2` | Agents get `reasoningEffort: xhigh` |
| `sonnet` | `anthropic/claude-sonnet-4-5-20250929` | |
| `haiku` | `anthropic/claude-haiku-4-5-20251001` | |

### Provider Prefixes

OpenCode supports multiple providers:
- `anthropic/` - Anthropic direct
- `openai/` - OpenAI models
- `google/` - Google Gemini
- `bedrock/` - AWS Bedrock
- `vertex/` - Google Vertex AI

### Usage in Frontmatter

```yaml
# Claude Code
model: sonnet

# OpenCode
model: anthropic/claude-sonnet-4-5-20250929
```

---

## Plugin Manifest Conversion

### Claude Code plugin.json

```json
{
  "name": "vibe-workflow",
  "description": "Ship high-quality code faster",
  "version": "2.13.2",
  "author": {
    "name": "doodledood",
    "email": "email@example.com"
  },
  "homepage": "https://github.com/doodledood/claude-code-plugins",
  "repository": "https://github.com/doodledood/claude-code-plugins",
  "license": "MIT",
  "keywords": ["vibe-coding", "workflow"],
  "hooks": { ... }
}
```

### OpenCode package.json

```json
{
  "name": "opencode-vibe-workflow",
  "version": "2.13.2",
  "description": "Ship high-quality code faster",
  "author": "doodledood <email@example.com>",
  "type": "module",
  "homepage": "https://github.com/doodledood/opencode-plugins",
  "repository": {
    "type": "git",
    "url": "https://github.com/doodledood/opencode-plugins"
  },
  "license": "MIT",
  "keywords": ["opencode", "opencode-plugin", "vibe-coding", "workflow"],
  "opencode": {
    "type": "plugin",
    "hooks": ["tool.execute.before", "session.created"]
  },
  "dependencies": {
    "@opencode-ai/plugin": "^1.0.162"
  }
}
```

**Notes**:
- Use `"type": "module"` for ESM format
- The `opencode` field describes the plugin type and hooks for npm registry metadata
- Add `@opencode-ai/plugin` dependency for TypeScript types
- **Important**: This package.json is for npm publishing. OpenCode does NOT read it for discovery. Files must be installed to `~/.config/opencode/` directories

---

## Known Plugins Classification

### vibe-workflow

**Note**: All skills in vibe-workflow are user-invocable. Internal helpers are implemented as agents.

| Skill | Type | → OpenCode |
|-------|------|------------|
| `review` | User-invocable | `command/review.md` |
| `plan` | User-invocable | `command/plan.md` |
| `spec` | User-invocable | `command/spec.md` |
| `implement` | User-invocable | `command/implement.md` |
| `implement-inplace` | User-invocable | `command/implement-inplace.md` |
| `explore-codebase` | User-invocable | `command/explore-codebase.md` |
| `research-web` | User-invocable | `command/research-web.md` |
| `bugfix` | User-invocable | `command/bugfix.md` |
| `fix-review-issues` | User-invocable | `command/fix-review-issues.md` |
| `review-*` (all) | User-invocable | `command/review-*.md` |

| Agent | → OpenCode |
|-------|------------|
| `bug-fixer` | `agent/bug-fixer.md` |
| `chunk-implementor` | `agent/chunk-implementor.md` |
| `chunk-verifier` | `agent/chunk-verifier.md` |
| `codebase-explorer` | `agent/codebase-explorer.md` |
| `web-researcher` | `agent/web-researcher.md` |
| `plan-verifier` | `agent/plan-verifier.md` |
| `*-reviewer` (all) | `agent/*-reviewer.md` |

### vibe-extras

| Skill | Type | → OpenCode |
|-------|------|------------|
| `clean-slop` | User-invocable | `command/clean-slop.md` |
| `rebase-on-main` | User-invocable | `command/rebase-on-main.md` |
| `rewrite-history` | User-invocable | `command/rewrite-history.md` |
| `update-claude-md` | User-invocable | `command/update-claude-md.md` |

| Agent | → OpenCode |
|-------|------------|
| `slop-cleaner` | `agent/slop-cleaner.md` |

### vibe-experimental

**Note**: `verify`, `done`, and `escalate` have `user-invocable: false` - they're called by `/do`, not directly.

| Skill | Type | → OpenCode |
|-------|------|------------|
| `define` | User-invocable | `command/define.md` |
| `do` | User-invocable | `command/do.md` |
| `verify` | **Non-user-invocable** | `skill/verify/SKILL.md` |
| `done` | **Non-user-invocable** | `skill/done/SKILL.md` |
| `escalate` | **Non-user-invocable** | `skill/escalate/SKILL.md` |

| Agent | → OpenCode |
|-------|------------|
| `criteria-checker` | `agent/criteria-checker.md` |
| `*-reviewer` (all) | `agent/*-reviewer.md` |

---

## Edge Cases & Limitations

### Directory Naming

OpenCode uses glob patterns that accept **both** singular and plural:
- `{command,commands}/**/*.md`
- `{agent,agents}/**/*.md`
- `{plugin,plugins}/**/*.{ts,js}`

**Convention**: Official docs use **plural** (`commands/`, `agents/`, `plugins/`). Singular works for backwards compatibility.

### Cannot Convert

1. **Stop hooks that block**: `session.idle` cannot prevent stopping
2. **SubagentStop hooks**: No equivalent event in OpenCode
3. **Subagent tool interception**: Hooks don't fire for subagent tool calls
4. **MCP tool interception**: MCP tool calls don't trigger hooks
5. **Complex Python deps**: Must find TypeScript alternatives
6. **Model auto-routing**: Claude Code uses Haiku for searches automatically

### Requires Manual Work

1. **Hook logic**: Python → TypeScript rewrite required
2. **External API calls in hooks**: Need TypeScript HTTP clients
3. **File system operations in hooks**: Use Bun/Node APIs

### Known Issues

1. **Skills calling skills**: Use `skill({ name: "skill-name" })` tool for non-user-invocable skills, `/command` for user-invocable ones
2. **Agent tool restrictions**: OpenCode tool permissions are more granular
3. **Context fork**: Claude Code `context: fork` needs testing in OpenCode

---

## Migration Checklist

### Per Plugin

- [ ] Create `package.json` from `plugin.json` (use singular paths!)
- [ ] Classify each skill (see [Skill Classification](#skill-classification)):
  - [ ] Check for `user-invocable: false` → skill
  - [ ] Check if referenced by other resources via `Skill()` → skill
  - [ ] Check if has supporting files (not just SKILL.md) → skill
  - [ ] Otherwise → command (default)
- [ ] Convert command-bound skills → `command/<name>.md`
- [ ] Convert skill-bound skills → `skill/<name>/SKILL.md`
- [ ] Convert agents → `agent/<name>.md`
- [ ] Convert hooks → `plugin/hooks.ts` (see [Converting Hooks](#converting-hooks))
- [ ] Update `Skill()` references: commands → `/command`, skills → `skill({ name: "..." })`
- [ ] Update all model names to full IDs (see [Model Mapping](#model-mapping))
- [ ] Update tool lists in agents to boolean format (`true`/`false`)
- [ ] **Rename files with "claude-md" → "agents-md"** (see [OpenCode Terminology](#opencode-terminology-claudemd--agentsmd))
- [ ] **Replace CLAUDE.md → AGENTS.md in all content**
- [ ] Create README for converted plugin

### Per Skill/Command

- [ ] Remove `name:` from frontmatter (commands only)
- [ ] Add `agent:` field if command should use specific agent (optional)
- [ ] Convert `model:` to full ID
- [ ] Replace `Skill()` calls: → `/command` or → `skill({ name: "..." })`
- [ ] Replace `Task` tool references

### Per Agent

- [ ] Remove `name:` from frontmatter
- [ ] Add `mode: subagent`
- [ ] Convert `tools:` to permission object
- [ ] Convert `model:` to full ID
- [ ] Add `reasoningEffort:` if requested via sync skill (see [Reasoning Effort](#reasoning-effort))
- [ ] Update prompt content references

### Per Hook (if source has `hooks/` directory)

- [ ] Create `plugin/hooks.ts` (or `plugins/hooks.ts`)
- [ ] Add `@opencode-ai/plugin` dependency
- [ ] Use `event` hook for session lifecycle (session.created, session.idle)
- [ ] Use `experimental.chat.system.transform` for context injection at start
- [ ] Map `PostCompact` → `experimental.session.compacting`
- [ ] Map `PostToolUse` → `tool.execute.after` (use `input.tool` not `input.call.name`)
- [ ] Map `PreToolUse` → `tool.execute.before` (CANNOT block - log warnings only)
- [ ] Document any `Stop` hooks (blocking not supported)
- [ ] Document any `PreToolUse` blocking (not supported - use logging)
- [ ] Convert Python logic to TypeScript

### Testing

- [ ] Test each command via `/command-name`
- [ ] Verify agents spawn correctly
- [ ] Check skill discovery works
- [ ] Validate prompt transformations
- [ ] Verify hooks fire correctly
- [ ] Test with different OpenCode models

---

## Quick Reference Card

### Frontmatter Cheat Sheet

**Command** (user-invocable, `command/<name>.md`):
```yaml
---
description: What it does
model: <full-model-id>  # optional, see Model Mapping
agent: <agent-name>     # optional, references an agent to execute the command
subtask: true           # optional, run as subagent
---
```

**Skill** (non-user-invocable, `skill/<name>/SKILL.md`):
```yaml
---
name: skill-name
description: What it does
---
```

**Agent** (`agent/<name>.md`):
```yaml
---
description: What it does
mode: subagent
model: <full-model-id>  # see Model Mapping
reasoningEffort: medium  # optional, only if requested via sync skill
tools:
  read: true
  edit: true
  bash: true
---
```

### Content Transformations

**User-invocable skills (become commands):**

| Find | Replace (Source) | After Install |
|------|------------------|---------------|
| `Skill("plugin:foo")` | `/foo` | `/foo-<plugin>` |
| `Skill("plugin:foo", "args")` | `/foo args` | `/foo-<plugin> args` |

**Non-user-invocable skills (remain skills):**

| Find | Replace (Source) | After Install |
|------|------------------|---------------|
| `Skill("plugin:foo")` | `skill({ name: "foo" })` | `skill({ name: "foo-<plugin>" })` |
| `Skill("plugin:foo", "args")` | `skill({ name: "foo", arguments: "args" })` | `skill({ name: "foo-<plugin>", arguments: "args" })` |

**Note**: The install script automatically updates internal references (`/command` and `skill({ name: "..." })`) to include the plugin postfix.

**Other transformations:**

| Find | Replace |
|------|---------|
| `model: opus/sonnet/haiku` | See [Model Mapping](#model-mapping) |
| `tools: Bash, Read, ...` | See [Tool Permission Mapping](#tool-permission-mapping) |

**Note**: The install script adds `-<plugin>` postfix to command filenames. Skill directories also get postfixed (e.g., `skill/verify-<plugin>/SKILL.md`).

### Directory Structure

**Source** (this repo):
```
<plugin-name>/
├── package.json
├── command/       # User-invocable commands
│   └── review.md
├── agent/         # Subagent definitions
│   └── bug-fixer.md
├── skill/         # Non-user-invocable skills
│   └── verify/
│       └── SKILL.md
└── plugin/        # TypeScript hooks
    └── hooks.ts
```

**Installed** (after `./install.sh`):
```
~/.config/opencode/
├── command/
│   └── review-<plugin-name>.md
├── agent/
│   └── bug-fixer-<plugin-name>.md
├── skill/
│   └── verify-<plugin-name>/
│       └── SKILL.md
└── plugin/
    └── <plugin-name>-hooks.ts
```
