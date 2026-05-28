---
name: vm0-api-cli
description: Use this skill to manage and run AI agents in secure sandboxed environments using the VM0 API and CLI. It covers installation, configuration, execution, and management of agents, volumes, and artifacts.
---

# VM0 API and CLI

Manage and run AI agents in secure sandboxed environments using the VM0 API and command-line interface (CLI).

## When to Use

Use this skill when you need to:

- Install and set up the VM0 CLI
- Create and configure AI agent projects
- Deploy agents to the VM0 platform
- Execute agents with prompts and inputs
- Manage input files (volumes) and output files (artifacts)
- Schedule recurring agent runs
- Monitor and manage agent runs (status, logs, metrics)

## Prerequisites

### Installation

Install the VM0 CLI globally via npm:

```bash
npm install -g @vm0/cli
```

Verify installation:

```bash
vm0 --version
```

### Authentication

Log in to your VM0 account:

```bash
vm0 auth login
```

For CI/CD environments, get your API token:

```bash
vm0 auth setup-token
```

Then set the environment variable:

```bash
export VM0_TOKEN=vm0_live_your-api-key
```

## Quick Start

### 1. Initialize a Project

Create a new VM0 project in the current directory:

```bash
vm0 init
```

### 2. Configure the Agent

Edit `vm0.yaml` to define your agent:

```yaml
version: "1.0"

agents:
  my-agent:
    framework: claude-code
    instructions: AGENTS.md
    skills:
      - https://github.com/vm0-ai/vm0-skills/tree/main/github
    environment:
      DEBUG: "${{ vars.DEBUG }}"
      API_KEY: "${{ secrets.API_KEY }}"
```

### 3. Deploy the Agent

Deploy your agent configuration:

```bash
vm0 compose vm0.yaml
```

### 4. Run the Agent

Execute the agent with a prompt:

```bash
vm0 run my-agent "Please analyze the codebase and suggest improvements"
```

### 5. List Your Agents

```bash
vm0 agent list
```

### 6. Manage Volumes (Input Files)

List volumes:

```bash
vm0 volume list
```

Push local files to cloud:

```bash
vm0 volume push
```

### 7. Manage Artifacts (Output Files)

List artifacts:

```bash
vm0 artifact list
```

Clone an artifact locally:

```bash
vm0 artifact clone my-output ./results
```

## Core Operations

### Running Agents

**Basic run:**

```bash
vm0 run my-agent "Your prompt here"
```

**Run with variables and secrets:**

```bash
vm0 run my-agent "Process data" --vars DEBUG=true --secrets API_KEY=xxx
```

### Viewing Logs

**View agent events (default):**

```bash
vm0 logs <run-id>
```

**View system logs:**

```bash
vm0 logs <run-id> --system
```

## Scheduling

Create scheduled agent runs with cron expressions.

### Initialize Schedule

**Interactive mode:**

```bash
vm0 schedule init
```

**Non-interactive mode:**

```bash
vm0 schedule init --name my-schedule --frequency daily --time 09:00 --prompt "Run daily task"
```

### Deploy Schedule

```bash
vm0 schedule deploy schedule.yaml
```

## Common Patterns

### Error Handling

All errors return a consistent format:

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "resource_not_found",
    "message": "No such agent: 'my-agent'",
    "param": "agent"
  }
}
```

| Error Type | Status | Description |
|------------|--------|-------------|
| `authentication_error` | 401 | Invalid or missing API key |
| `invalid_request_error` | 400 | Invalid parameters |
| `not_found_error` | 404 | Resource doesn't exist |
| `api_error` | 500 | Internal server error |

## Detailed References

- [VM0 API Documentation](https://docs.vm0.ai/docs/reference/api)
- [Agents API](references/agents.md) - List agents and versions
- [Runs API](references/runs.md) - Execute agents, stream events, get logs and metrics
- [Artifacts API](references/artifacts.md) - List and download agent outputs
- [Volumes API](references/volumes.md) - List and download input files

## Guidelines

1. **Always authenticate first** - Run `vm0 auth login` before using other commands.
2. **Use `vm0 init` for new projects** - Creates proper project structure.
3. **Deploy before running** - Run `vm0 compose` after modifying `vm0.yaml`.
4. **Use volumes for input data** - Push data files as volumes before running agents.
5. **Check logs for debugging** - Use `vm0 logs` to troubleshoot failed runs.
6. **Use scopes for organization** - Set appropriate scope for team collaboration.

## Troubleshooting

### Authentication Issues

```bash
# Check auth status
vm0 auth status

# Re-login if needed
vm0 auth logout
vm0 auth login
```

### Agent Not Found

```bash
# List available agents
vm0 agent list

# Check if deployed
vm0 compose vm0.yaml
```