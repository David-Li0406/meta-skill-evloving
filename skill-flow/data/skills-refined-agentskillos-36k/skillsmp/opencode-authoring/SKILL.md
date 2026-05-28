---
name: opencode-authoring
description: |
  Create and configure OpenCode agents and skills. Use when: "create agent", "new skill",
  "create skill", "write SKILL.md", "configure subagent", "add agent", or designing OpenCode extensions.
---

# OpenCode Authoring

Create agents and skills for OpenCode.

## Agents vs Skills

| Concept | Purpose | File | Location |
|---------|---------|------|----------|
| Agent | Specialized AI assistant with custom prompt, tools, permissions | `name.md` | `.opencode/agent/` or `~/.config/opencode/agent/` |
| Skill | On-demand instructions loaded by any agent | `SKILL.md` | `.opencode/skill/name/` or `~/.config/opencode/skill/name/` |

**Rule of thumb:**
- Agent = different persona/role (code reviewer, security auditor)
- Skill = reusable knowledge (how to use jira-cli, shell scripting patterns)

## Creating Agents

### Agent File Structure

```markdown
---
description: When to use this agent (required, shown in @-mentions)
mode: primary | subagent
model: provider/model-id
temperature: 0.0-1.0
tools:
  read: true
  write: false
  edit: false
  bash: true
permission:
  edit: deny | ask | allow
  bash:
    "*": ask
    "git status": allow
---

# Agent Name

System prompt content. What this agent does and how it behaves.

## Purpose

Clear statement of agent's role.

## Approach

1. Step one
2. Step two

## Output

What the agent returns.
```

### Agent Locations

| Scope | Path |
|-------|------|
| Global | `~/.config/opencode/agent/name.md` |
| Project | `.opencode/agent/name.md` |

### Agent Modes

- `primary`: Tab-switchable main agent (like Build, Plan)
- `subagent`: Invoked via @mention or Task tool (like Explore, General)
- `all`: Both (default)

### Agent Examples

**Read-only reviewer:**

```markdown
---
description: Code review without making changes
mode: subagent
temperature: 0.1
tools:
  write: false
  edit: false
permission:
  edit: deny
---

# Reviewer

Analyze code. Suggest improvements. No modifications.
```

**Research agent:**

```markdown
---
description: Find implementations and docs in the wild
mode: subagent
model: github-copilot/claude-sonnet-4.5
tools:
  edit: false
  write: false
  webfetch: true
---

# Researcher

Search GitHub, fetch docs, return evidence with links.
```

### Agent Frontmatter Reference

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | **Required.** When to invoke this agent |
| `mode` | string | `primary`, `subagent`, or `all` |
| `model` | string | `provider/model-id` override (see Model Selection) |
| `temperature` | number | 0.0 (deterministic) to 1.0 (creative) |
| `maxSteps` | number | Limit agentic iterations |
| `tools` | object | Enable/disable tools: `write`, `edit`, `bash`, `read`, `grep`, etc. |
| `permission` | object | Fine-grained permissions per tool |
| `hidden` | boolean | Hide from @-autocomplete (subagents only) |

## Model Selection (CRITICAL)

**Models MUST exist in either `github-copilot` or `opencode` providers.**

Before specifying a model, verify it exists:

```bash
opencode models | grep -i 'model-name'
```

Or check https://models.dev for the full list.

### Provider Configuration

The provider is determined by the `OPENCODE_PROVIDER` environment variable.
Default: `github-copilot` if unset.

```bash
export OPENCODE_PROVIDER="${OPENCODE_PROVIDER:-github-copilot}"
```

### Valid Model Format

```
provider/model-id
```

Examples:
- `github-copilot/claude-sonnet-4.5`
- `github-copilot/gpt-5.2`
- `github-copilot/gemini-3-flash`
- `opencode/claude-sonnet-4-5`
- `opencode/gpt-5.1-codex`

### Available Models (run `opencode models` for current list)

**opencode provider:**
- `opencode/claude-sonnet-4-5` - Anthropic Claude Sonnet 4.5
- `opencode/claude-opus-4-5` - Anthropic Claude Opus 4.5
- `opencode/gpt-5` - OpenAI GPT-5
- `opencode/gpt-5.1-codex` - OpenAI GPT-5.1 Codex
- `opencode/gpt-5.2` - OpenAI GPT-5.2
- `opencode/gemini-3-flash` - Google Gemini 3 Flash
- `opencode/gemini-3-pro` - Google Gemini 3 Pro
- `opencode/qwen3-coder` - Alibaba Qwen 3 Coder

**github-copilot provider:**
- Uses same model names without version suffixes
- `github-copilot/claude-sonnet-4.5`
- `github-copilot/gpt-5.2`
- `github-copilot/gemini-3-flash`

### Model Selection in Agents

When creating an agent, use environment variable expansion for provider flexibility:

```markdown
---
description: Research agent
mode: subagent
model: ${OPENCODE_PROVIDER:-github-copilot}/claude-sonnet-4.5
---
```

**Note:** YAML doesn't natively support env vars. Set model based on your configured provider:

```markdown
---
description: Research agent
mode: subagent
model: github-copilot/claude-sonnet-4.5
---
```

To use a different provider, either:
1. Edit the agent file directly
2. Configure default model in `opencode.json`

### Validation Before Creating Agents

**Always verify the model exists:**

```bash
opencode models | grep -E 'claude|gpt|gemini'
```

**If model not found:**
1. Check spelling matches exactly
2. Verify provider is configured (`/connect`)
3. Check https://models.dev for available models

## Creating Skills

### Skill File Structure

```markdown
---
name: skill-name
description: |
  What this does and when to use it. Include trigger phrases like
  "create ticket", "write test", "deploy to staging".
---

# Skill Title

## Purpose

What problem this solves.

## When to Use

- Trigger phrase one
- Trigger phrase two

## Instructions

Step-by-step guidance for the agent.

## Quick Reference

Common commands/patterns.

## Examples

Concrete usage examples.
```

### Skill Locations

| Scope | Path |
|-------|------|
| Global | `~/.config/opencode/skill/name/SKILL.md` |
| Project | `.opencode/skill/name/SKILL.md` |
| Claude-compat | `~/.claude/skills/name/SKILL.md` or `.claude/skills/name/SKILL.md` |

### Skill Name Rules

- Lowercase alphanumeric with single hyphens
- 1-64 characters
- No leading/trailing hyphens
- No consecutive hyphens (`--`)
- Directory name must match frontmatter `name`

Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

### Skill Description Rules

- 1-1024 characters
- Include WHAT it does AND WHEN to use it
- Add trigger phrases users would say
- Mention file types, tools, operations

**Good:**
```yaml
description: |
  Manage Jira tickets using jira-cli: create, update, close issues.
  Use when: "create ticket", "update issue", "close bug", "transition to done".
```

**Bad:**
```yaml
description: Jira stuff
```

### Multi-file Skills

For complex skills, use supporting files:

```
skill-name/
├── SKILL.md           # Main entry (required)
├── references/        # Detailed docs
│   ├── commands.md
│   └── examples.md
└── templates/         # Boilerplate
    └── config.yaml
```

Reference them from SKILL.md:
```markdown
See [references/commands.md](references/commands.md) for full command list.
```

### Skill Permissions

Control skill access in `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "internal-*": "deny",
      "*": "allow"
    }
  }
}
```

Values: `allow`, `deny`, `ask`

## Creating Commands

Create custom slash commands for repetitive tasks.

### Command locations

- Global: `~/.config/opencode/command/<name>.md`
- Project: `.opencode/command/<name>.md`

The filename becomes the command name. Example: `jira.md` => `/jira`.

### Command file structure

```markdown
---
description: Short help text shown in the TUI
agent: jean
subtask: true
model: opencode/gpt-5.2
---

Prompt template goes here.
```

Notes:
- The markdown body is the `template` sent to the model.
- `agent` is optional; if omitted, the current agent runs the command.
- `subtask: true` forces the command to run in a subtask, keeping the primary agent context clean.
- `model` is optional and overrides the default model for this command.

### Template helpers

- Arguments:
  - `$ARGUMENTS` - all args after the command
  - `$1`, `$2`, ... - positional args
- Shell output injection:
  - Use `!` followed by a backticked command to inline its output into the prompt.
  - Example:

    ```markdown
    Recent commits:
    !`git log --oneline -10`
    ```
  - Runs in the project root directory.
- File references:
  - `@path/to/file` injects file contents.

### When to prefer a command over a skill

Use a command when you want full control over when heavyweight context loads (e.g., Jira operator rules, deployment runbooks).

## Validation Checklist

### Agent

- [ ] File named `name.md` in agent directory
- [ ] `description` frontmatter present
- [ ] `mode` specified if not default
- [ ] **Model exists** - run `opencode models | grep model-name`
- [ ] **Model uses valid provider** - `github-copilot/` or `opencode/`
- [ ] Tools appropriately restricted
- [ ] System prompt is clear and focused

### Skill

- [ ] Directory name matches frontmatter `name`
- [ ] `SKILL.md` (uppercase) exists
- [ ] `name` follows naming rules
- [ ] `description` < 1024 chars, includes triggers
- [ ] Instructions are actionable

## Troubleshooting

**Agent doesn't appear in @-menu:**
- Check file is `.md` in correct location
- Verify `description` frontmatter exists
- For subagents, check `hidden` isn't `true`

**Model not found / ProviderModelNotFoundError:**
- Run `opencode models` to see available models
- Ensure model ID matches exactly (case-sensitive)
- Check provider is connected: `/connect`
- Verify model uses `github-copilot/` or `opencode/` prefix
- Check https://models.dev for model availability

**Skill doesn't activate:**
- Ensure `SKILL.md` is uppercase
- Check `name` matches directory
- Make description more specific with trigger phrases
- Verify no `deny` permission blocking it

**Conflicts between agents/skills:**
- Make descriptions more distinct
- Use different trigger words
- Narrow scope of each

## Quick Templates

### Minimal Agent

```markdown
---
description: Brief description for @-menu
mode: subagent
---

System prompt here.
```

### Minimal Skill

```markdown
---
name: my-skill
description: What and when. Triggers: "do thing", "run task".
---

# My Skill

Instructions for the agent.
```
