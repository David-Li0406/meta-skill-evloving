---
name: vm0
description: Use this skill to build, run, and manage AI agents in secure sandboxed environments using the VM0 platform and CLI.
---

# VM0 Skill

This skill allows you to execute AI agents in isolated environments, manage their configurations, and handle input/output files.

## When to Use

- Build and run AI agents in secure sandboxed environments.
- Manage agent configurations and deployments.
- Monitor agent runs, including status and logs.
- Handle input files (volumes) and output files (artifacts).

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
export VM0_API_KEY=vm0_live_your-api-key
```

## Quick Start

### Initialize a Project

Create a new VM0 project in the current directory:

```bash
vm0 init
```

### Configure the Agent

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

### Deploy the Agent

Deploy your agent configuration:

```bash
vm0 compose vm0.yaml
```

### Run an Agent

Execute the agent with a prompt:

```bash
vm0 run my-agent "Please analyze the codebase and suggest improvements"
```

### Check Run Status

Replace `<run-id>` with your run ID:

```bash
vm0 run status <run-id>
```

### Get Run Logs

```bash
vm0 run logs <run-id>
```

## Core Operations

### List Your Agents

```bash
vm0 agents list
```

### Get Agent Details

```bash
vm0 agents get <agent-id>
```

### Manage Input/Output Files

List and download input files (volumes):

```bash
vm0 volumes list
```

List and download output files (artifacts):

```bash
vm0 artifacts list
```