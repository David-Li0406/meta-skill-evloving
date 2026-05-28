---
name: creating-and-configuring-opencode-agents
description: Use this skill when creating and configuring specialized OpenCode agents and subagents for various tasks, ensuring best practices in agent orchestration and management.
---

# Creating and Configuring OpenCode Agents

This skill encompasses the creation and configuration of specialized OpenCode agents (both primary and subagents) tailored for specific tasks and workflows. It is useful when the user wants to create, modify, or configure agents, mentions agent modes, tool permissions, or task delegation.

## What are OpenCode Agents?

OpenCode agents are specialized AI assistants designed for specific tasks and workflows. They can be configured with custom prompts, models, and tool access.

### Agent Types

- **Primary Agents**: Main assistants users interact with directly. Switch between them using the **Tab** key or configured keybind.
- **Subagents**: Specialized assistants invoked by primary agents or via **@ mention**.

### Built-in Agents

1. **Build**: Default agent with all tools enabled for full development work.
2. **Plan**: Restricted agent for planning/analysis without making changes.
3. **General**: General-purpose for complex questions and multi-step tasks.
4. **Explore**: Fast, read-only agent for exploring codebases.

## Configuration Methods

Agents can be configured in two ways:

### 1. JSON Configuration

Add agents to `opencode.json` config file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "agent-name": {
      "description": "What the agent does and when to use it",
      "mode": "primary",
      "model": "provider/model-id",
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

### 2. Markdown Files

Place markdown files in:
- Global: `~/.config/opencode/agents/`
- Per-project: `.opencode/agents/`

The filename becomes the agent name (e.g., `review.md` creates `review` agent).

```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: provider/model-id
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
---

You are in code review mode. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
```

## Creating Agents Step-by-Step

### Using the CLI Command

The fastest way to create an agent:

```bash
opencode agent create
```

This interactive command will:
1. Ask where to save (global or project-specific)
2. Prompt for description
3. Generate appropriate system prompt and identifier
4. Let you select which tools can be accessed
5. Create a markdown file with the configuration

### Manual Creation Process

1. **Gather Requirements**: Ask the user about the agent's purpose, mode, tools, and permissions.
2. **Choose Agent Name**: Use lowercase with hyphens (e.g., `review`, `security-audit`).
3. **Write Clear Description**: Include what the agent does and when to use it.
4. **Select Mode**: Choose between primary, subagent, or all.
5. **Configure Tools and Permissions**: Decide which tools to enable/disable and set permissions.
6. **Choose Model and Temperature**: Select appropriate models and temperature settings.
7. **Write Custom Prompt (Optional)**: Create a prompts directory and reference it in the configuration.
8. **Decide on Configuration Format**: Choose between JSON and Markdown based on the agent's needs.
9. **Create the Configuration**: Use the appropriate commands to create the configuration files.
10. **Validate Configuration**: Ensure all fields are correctly set and the agent can perform its tasks.

## Workflow Patterns

Design subagents around proven workflow patterns:

### Evaluator-Optimizer (Iterative)

Best for agents that iterate until success (e.g., test fixers, quality auditors).

### Read-Only Reviewer

Best for analysis without side effects (e.g., code review, security audit).

### Orchestrator-Workers

Best for complex multi-step tasks delegated to specialists.

## Best Practices

1. **Single Responsibility**: Each agent should have a clear, focused purpose.
2. **Descriptive Names**: Use names that clearly indicate the agent's role.
3. **Rich Descriptions**: Include what the agent does AND when to use it.
4. **Appropriate Permissions**: Grant only the tools needed for the task.
5. **Temperature Matching**: Lower for deterministic tasks, higher for creative work.

## Troubleshooting

### Common Issues

- **Agent Not Appearing**: Check if the agent is disabled or hidden.
- **Agent Can't Perform Needed Actions**: Verify tools and permissions.
- **Agent Asks for Approval Too Often**: Adjust permission settings.
- **Agent Makes Unwanted Changes**: Set permissions to ask or deny.

## References

- [OpenCode Agents Documentation](https://opencode.ai/docs/agents/)
- [OpenCode Configuration](https://opencode.ai/docs/config/)
- [OpenCode Permissions](https://opencode.ai/docs/permissions/)
- [OpenCode Tools](https://opencode.ai/docs/tools/)
- [OpenCode Models](https://opencode.ai/docs/models/)

Run `opencode models` to see available models for your configured providers.