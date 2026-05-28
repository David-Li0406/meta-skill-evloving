# Idle Scheduler Drop-In Module (wf-6pe)

This document summarizes the implementation tracked in Beads issue `wf-6pe`.

## Overview

This drop-in Bash module executes a user-defined task whenever the terminal becomes idle. Idle detection is achieved by hooking into `PROMPT_COMMAND`, so the task only runs immediately before Bash renders a prompt (i.e., no foreground job is running).

Key properties:

- **Per-terminal isolation** — each shell session tracks its own schedule.
- **Randomized intervals** — after each execution, the next run occurs between 20 and 40 seconds (default; configurable).
- **User-overridable task** — define an `idle_task()` function before sourcing to customize the action.
- **Safe chaining** — existing `PROMPT_COMMAND` logic is preserved (arrays and strings supported).
- **Interactive-only** — exits early when not in an interactive shell.

## Installation

1. Copy `scripts/idle-scheduler.sh` to a module directory such as `~/.bashrc.d/`.
2. Source it from your shell rc file, optionally passing frequency/variance arguments:

   ```bash
   # ~/.bashrc or ~/.bashrc.d/loader.sh
   #                frequency variance
   source "$HOME/.bashrc.d/idle-scheduler.sh" 30 10
   ```

3. Optionally define a custom `idle_task()` before sourcing:

   ```bash
   idle_task() {
     waif next --json > "$HOME/.cache/last-waif-recommendation.json"
   }

   source "$HOME/.bashrc.d/idle-scheduler.sh" 45 15
   ```

4. The tmux workflow helper (`scripts/start-workflow-tmux.sh`) automatically loads this module based on the `config/workflow_agents.yaml` configuration. For agents with an `idle` block, it defines:

   ```bash
   idle_task() { <configured task command>; }
   source "$REPO_ROOT/scripts/idle-scheduler.sh" <frequency> <variance>
   ```

   For example, the default PM agent config:

   ```yaml
   - name: pm
     idle:
       task: "clear; waif in-progress"
       frequency: 30
       variance: 10
   ```

   Results in the PM terminal periodically refreshing the in-progress table even while idle.

## Configuration

You can configure intervals via either positional arguments (frequency, variance) or environment variables (which provide defaults and support legacy behavior). When both are provided, positional arguments win.

| Input | Default | Description |
|-------|---------|-------------|
| positional argument 1 / `IDLE_SCHEDULER_FREQUENCY` | `30` | Target seconds between task runs |
| positional argument 2 / `IDLE_SCHEDULER_VARIANCE` | `10` | ± variance applied to the target interval |
| `IDLE_SCHEDULER_MIN_INTERVAL` | derived | Minimum seconds between runs (overridden directly only if you need explicit bounds) |
| `IDLE_SCHEDULER_MAX_INTERVAL` | derived | Maximum seconds between runs |

## Behaviour

- The module installs `__idle_scheduler_run` into `PROMPT_COMMAND`.
- Each time the prompt is about to render, it checks elapsed time since the last execution.
- When the elapsed time meets or exceeds the randomly selected interval, it runs `idle_task`, updates the last run timestamp, and draws a new randomized interval.
- Foreground commands (e.g., `vim`, `top`) suppress execution because `PROMPT_COMMAND` is only invoked after they exit.

## Example Output

```
[idle task] Running at Mon Jan 01 12:00:00 UTC 2024
waif> 
```

Override `idle_task()` to change the output destination or action.

## Testing Notes

- Since the module is sourced in Bash, automated tests can simulate execution by invoking a test Bash instance with the module sourced, manipulating environment variables, and invoking `__idle_scheduler_run` manually.
- Manual test steps:
  1. Source the module in a new interactive shell.
  2. Press Enter repeatedly; observe randomized `idle_task` output between prompts.
  3. Run a long-lived command (e.g., `sleep 30`) to confirm no mid-command invocations.
  4. Open a second terminal to confirm per-session independence.

## Config-Driven Integration (wf-urb)

The idle scheduler is now integrated with `config/workflow_agents.yaml`. Each agent can optionally define an `idle` block:

```yaml
agents:
  - name: my_agent
    idle:
      task: "echo 'Idle task running'"  # Shell command to execute
      frequency: 30                      # Target interval (seconds)
      variance: 10                       # +/- randomization range
```

When `start-workflow-tmux.sh` spawns the agent pane, it:
1. Defines an `idle_task()` function with the configured command
2. Sources `scripts/idle-scheduler.sh` with the configured frequency/variance
3. The scheduler then runs the task at randomized intervals

If no `idle` block is specified, no idle scheduler is loaded for that agent.

See `docs/Workflow.md` for the full config schema and examples.
