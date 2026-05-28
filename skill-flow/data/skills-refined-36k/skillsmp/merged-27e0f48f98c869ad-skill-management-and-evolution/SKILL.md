---
name: skill-management-and-evolution
description: Use this skill when you need to manage, update, and evolve AI skills from GitHub repositories, including creating new skills and checking their health status.
---

# Skill Management and Evolution

This skill combines the functionalities of managing AI skills, evolving them based on user interactions, and creating new skills from GitHub repositories.

## Core Capabilities

1. **Skill Lifecycle Management**: Automates the detection of updates, refactoring, and health checks for skills.
2. **Skill Creation**: Converts GitHub repositories into standardized AI skills with necessary metadata.
3. **Skill Evolution**: Coordinates the evolution of skills based on user interactions and programming tasks.

## Skill Lifecycle Management

### Core Functions

- **Audit**: Scans local skills for metadata.
- **Check**: Compares local skills against the latest versions on GitHub.
- **Report**: Generates a status report for skills.
- **Update Workflow**: Provides a structured process for upgrading skills.
- **Inventory Management**: Lists, enables, disables, and deletes skills.
- **Health Check**: Monitors skill health status.

### Usage Triggers

- `/skill-manager check` or "Scan my skills for updates"
- `/skill-manager list` or "List my skills"
- `/skill-manager delete <skill_name>` or "Delete skill <skill_name>"
- `/skill-manager enable <skill_name>` or "Enable skill <skill_name>"
- `/skill-manager disable <skill_name>` or "Disable skill <skill_name>"
- `/skill-manager health` or "Run health check"

### Workflows

#### Check for Updates

1. Run a scanner to analyze all skills.
2. Review the generated report.

#### Update a Skill

1. Fetch the new README from the remote repository.
2. Compare the new README with the existing SKILL.md.
3. Refactor the SKILL.md and update the metadata.
4. Verify the updates.

#### Enable/Disable a Skill

1. Move the skill directory to/from a `.disabled/` subdirectory.

#### Health Check

1. Run a health check script to analyze all skills.
2. Review the health report and take action based on the findings.

## Skill Creation

### Core Functions

- **Information Retrieval**: Fetches commit hashes and README content from GitHub.
- **Directory Generation**: Creates a standardized skill directory structure.
- **Metadata Injection**: Automatically fills in required metadata fields.

### Usage Triggers

- `/skill-factory <github_url>`
- "Create skill from GitHub: <url>"

### Workflow

1. Retrieve repository information.
2. Analyze the README for functionality and usage.
3. Generate the skill directory structure.
4. Populate the SKILL.md and implement the wrapper script.

## Skill Evolution

### Core Functions

- **Learning Triggers**: Detects GitHub URLs and initiates learning processes.
- **Evolution Triggers**: Automatically triggers evolution processes after programming tasks.
- **Session Management**: Tracks session states and persists context information.

### Usage Triggers

- User inputs containing GitHub URLs.
- Commands related to skill management.

### Workflows

1. **Learning Workflow**: Initiates learning from a GitHub repository.
2. **Evolution Workflow**: Automatically evolves skills based on user interactions and programming tasks.

## Best Practices

1. **Non-Intrusive**: The coordinator does not modify user code directly.
2. **Observability**: All operations are logged for debugging.
3. **Fault Tolerance**: Failure of one component does not affect others.
4. **User Control**: Automation features can be configured or disabled.

## Example Scenarios

### Example 1: Creating a New Skill

```
User: /skill-factory https://github.com/example/repo

Agent:
1. Fetch repository information.
2. Analyze README for functionality.
3. Create skill directory structure.
4. Populate SKILL.md and implement wrapper script.
```

### Example 2: Checking Skill Health

```
User: /skill-manager health

Agent:
1. Run health check on all skills.
2. Generate and present health report.
```

### Example 3: Evolving a Skill

```
User: Help me fix this bug.

Agent:
1. Analyze and fix the bug.
2. Check if the session meets evolution criteria.
3. Trigger evolution process if applicable.
```

## Metadata Requirements

Each skill must include the following metadata:

```yaml
---
name: skill-name
description: Detailed description including usage conditions
source_url: https://github.com/owner/repo
source_hash: abc123def456...
version: 0.1.0
created_at: 2026-01-23
updated_at: 2026-01-23
evolution_enabled: true
entry_point: scripts/wrapper.py
dependencies:
  - dependency1
  - dependency2
---
```