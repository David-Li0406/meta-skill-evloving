---
name: creating-and-configuring-opencode-agents
description: Use this skill when creating and configuring specialized OpenCode agents and subagents for various tasks, ensuring best practices in agent orchestration and management.
---

## When to use this skill

Use this skill when:
- You want to create a new OpenCode agent or subagent.
- You need to modify or configure an existing agent.
- You are implementing multi-agent workflows or orchestration.
- You mention agent modes (primary, subagent) or task delegation.
- You require specialized agents for specific tasks (e.g., review, security, documentation).

## What OpenCode agents are

OpenCode agents are specialized AI assistants configured for specific tasks and workflows. They allow you to create focused tools with custom prompts, models, and tool access.

### Agent types

**Primary agents**: Main assistants you interact with directly. Switch between them using the **Tab** key or configured keybind.
- Examples: Build (default with all tools), Plan (restricted for analysis)

**Subagents**: Specialized assistants invoked by primary agents or via **@ mention**.
- Examples: General (multi-step tasks), Explore (read-only codebase exploration)

### Built-in agents

1. **Build** (primary): Default agent with all tools enabled for full development work.
2. **Plan** (primary): Restricted agent for planning/analysis without making changes.
3. **General** (subagent): General-purpose for complex questions and multi-step tasks.
4. **Explore** (subagent): Fast, read-only agent for exploring codebases.

## Configuration methods

Agents can be configured in two ways:

### 1. JSON configuration

Add agents to `opencode.json` config file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "agent-name": {
      "description": "What the agent does and when to use it",
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.3,
      "prompt": "{file:./prompts/agent-name.txt}",
      "tools": {
        "write": true,
        "edit": true,
        "bash": true
      },
      "permission": {
        "edit": "ask",
        "bash": {
          "*": "ask",
          "git status *": "allow"
        }
      }
    }
  }
}
```

### 2. Markdown files

Place markdown files in:
- Global: `~/.config/opencode/agents/`
- Per-project: `.opencode/agents/`

The filename becomes the agent name (e.g., `review.md` creates `review` agent).

```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
  webfetch: deny
---

You are in code review mode. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
```

## Configuration options

### Required fields

#### description
Brief description of what the agent does and when to use it.
- **Required**: Yes (for custom agents)
- **Constraints**: Clear, actionable description with keywords

### Optional fields

#### mode
Determines how the agent can be used.
- **Values**: `"primary"`, `"subagent"`, `"all"` (default if not specified)

#### temperature
Control randomness and creativity of responses.
- **Range**: 0.0 to 1.0

#### tools
Control which tools are available to this agent.
- **Values**: `true` (enable), `false` (disable)

#### permission
Manage what actions an agent can take.
- **Values**: `"ask"` (prompt for approval), `"allow"` (no approval needed), `"deny"` (disable)

### Creating agents step-by-step

1. **Gather requirements**: Ask the user what the agent should do, when it should be used, and what tools it needs access to.
2. **Choose agent name**: Use lowercase with hyphens (for markdown files).
3. **Write clear description**: Include what the agent does and when to use it.
4. **Select mode**: Decide if it should be a primary agent or subagent.
5. **Configure tools and permissions**: Decide which tools to enable/disable and set permissions.
6. **Choose model and temperature**: Select appropriate models and temperature settings.
7. **Write custom prompt (optional)**: Create a prompts directory and reference it in the configuration.
8. **Decide on configuration format**: Choose between JSON and Markdown based on complexity.
9. **Validate configuration**: Ensure all fields are correctly filled and the agent can perform its tasks.

## Workflow Patterns

Design subagents around proven workflow patterns:

### Evaluator-Optimizer (Iterative)

Best for agents that iterate until success (test fixers, quality auditors).

### Read-Only Reviewer

Best for analysis without side effects (code review, security audit).

### Orchestrator-Workers

Best for complex multi-step tasks delegated to specialists.

## Best practices

1. **Single responsibility**: Each agent should have a clear, focused purpose.
2. **Descriptive names**: Use names that clearly indicate the agent's role.
3. **Rich descriptions**: Include what the agent does AND when to use it.
4. **Appropriate permissions**: Grant only the tools needed for the task.
5. **Temperature matching**: Lower for deterministic tasks, higher for creative work.

## Troubleshooting

### Agent not appearing
- Check `disable: false` is set.
- Ensure config file is in the correct location.

### Agent can't perform needed actions
- Check `tools` configuration includes needed tools.
- Verify `permission` settings allow the operations.

## Example configurations

See [assets/templates/](assets/templates/) for complete example configurations.

## Resources

- [OpenCode Agents Documentation](https://opencode.ai/docs/agents/)
- [OpenCode Configuration](https://opencode.ai/docs/config/)
- [OpenCode Permissions](https://opencode.ai/docs/permissions/)
- [OpenCode Tools](https://opencode.ai/docs/tools/)
- [OpenCode Models](https://opencode.ai/docs/models/)

Run `opencode models` to see available models for your configured providers.