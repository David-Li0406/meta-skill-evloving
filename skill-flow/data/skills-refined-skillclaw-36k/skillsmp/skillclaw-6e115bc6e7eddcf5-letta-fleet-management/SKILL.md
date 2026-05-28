---
name: letta-fleet-management
description: Use this skill when creating, updating, or managing multiple Letta AI agents with shared configurations, memory blocks, tools, and folders using a kubectl-style CLI.
---

# Skill body

## Core Workflow

1. Define agents in `fleet.yaml`.
2. Apply configuration with:
   ```bash
   lettactl apply -f fleet.yaml              # Create/update agents
   lettactl apply -f fleet.yaml --dry-run    # Preview changes
   lettactl apply -f fleet.yaml --match "*-draper"  # Template mode
   ```
3. Verify the deployment with:
   ```bash
   lettactl get agents                        # List all agents
   lettactl describe agent <name>            # Full agent details
   ```

## Fleet YAML Structure

```yaml
shared_blocks:
  - name: company-context
    description: Shared company knowledge
    limit: 5000
    from_file: ./context/company.md

agents:
  - name: support-agent
    description: Customer support assistant
    system_prompt:
      from_file: ./prompts/support.md
    llm_config:
      model: gpt-4o
      context_window: 128000
    memory_blocks:
      - name: persona
        description: Agent personality
        limit: 2000
        value: "You are a helpful support agent."
    shared_blocks:
      - company-context
    tools:
      - send_email
      - search_docs
```

## CLI Commands

### Inspect Resources
```bash
lettactl get agents                    # List all agents
lettactl get agents -o wide            # With details
lettactl get blocks --shared           # Shared blocks only
lettactl get tools --orphaned          # Unused tools
```

### Messaging
```bash
lettactl send <agent> "Hello"          # Send message
lettactl send <agent> "Hi" --stream    # Stream response
lettactl messages list <agent>         # View history
lettactl messages reset <agent>        # Clear history
```

### Observability
```bash
lettactl health                        # Server connectivity
lettactl files <agent>                 # Attached files
lettactl context <agent>               # Context window usage
```

## Template Mode

Apply configuration to existing agents matching a pattern:
```bash
lettactl apply -f template.yaml --match "*-draper"
```
This uses a three-way merge to preserve user-added resources while updating managed ones.