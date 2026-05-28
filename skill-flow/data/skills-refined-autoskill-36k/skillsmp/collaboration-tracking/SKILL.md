---
name: collaboration-tracking
description: Instructions for checking global CLI context and logging handoffs.
---

# Collaboration Tracking

This skill ensures that all agents share a common CLI context and log their handoffs to maintain a clear chain of custody.

## Global Context (CLI)
- **File**: `agent-output/cli.md`
- **Usage**: Always check this file for shared command-line instructions or context that persists across agent sessions.
- **Action**: If you have relevant CLI output or instructions that other agents might need, append them to this file.

## Handoff Logging (BLOCKING)
- **Constraint**: You CANNOT handoff to another agent until you have successfully executed this log command.
- **File**: `agent-output/logs/handoff_history.log`
- **Action**: Run this command *immediately before* your handoff action/tool call:
  ```bash
  # Append to the handoff log
  # IMPORTANT: Replace [YourAgentName] and [TargetAgentName] with actual names (e.g., Architect -> Critic)
  mkdir -p agent-output/logs && echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [YourAgentName] -> [TargetAgentName]" >> agent-output/logs/handoff_history.log
  ```

## Tool Usage Logging
- **File**: `agent-output/logs/tool_usage_history.log`
- **Goal**: Track significant modifications and executions to understand agent actions.
- **Scope**: Log ONLY "Side-Effect" tools.
- **Method**: Use `run_command` to append via shell.
- **Command**:
  ```bash
  # IMPORTANT: Replace [YourAgentName] with your actual name (e.g., Implementer)
  echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [YourAgentName] [Tool]" >> agent-output/logs/tool_usage_history.log
  ```
- **Example**:
  ```bash
  echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] Architect write_to_file" >> agent-output/logs/tool_usage_history.log
  ```

## CLI Command Logging
- **File**: `agent-output/logs/cli_history.log`
- **Goal**: Maintain a detailed, linear history of all terminal commands executed for debugging and auditing.
- **Requirement**: Whenever you use the `run_command` tool, you MUST also log the command to this file.
- **Exclusions**: Do NOT log commands that write to collaboration tracking logs (`handoff_history.log`, `tool_usage_history.log`, `cli_history.log`) to avoid circular/redundant logging.
- **Format**: `[Timestamp] [Agent] [Tool] [Command]`
- **Command**:
  ```bash
  # Example: Logging a git commit
  echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [DevOps] [run_command] [git commit -m 'feat: init']" >> agent-output/logs/cli_history.log
  ```
- **Note**: This mimics a persistent `.bash_history` but attributed to specific agents and timestamps, excluding the logging commands themselves.
