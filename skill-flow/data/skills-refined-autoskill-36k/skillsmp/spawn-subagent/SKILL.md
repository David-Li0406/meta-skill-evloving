---
name: spawn-subagent
description: Spawn subagents with fresh context and bounded scope.
---

# Spawn-Subagent Skill

## What this skill does
Provides a consistent pattern for spawning subagents with fresh context, bounded scope, and explicit inputs/outputs, then integrating their results back into the main workflow.

## OpenCode (Primary)
- Spawn as a background task using the OpenCode subagent API.
- Always provide a self-contained prompt with all required context and constraints.
- Wait for the subagent to finish before proceeding.
- Integrate results into the main response and cite any sources provided.

## Spawning Protocol
1. Detect the need for a subagent (research, exploration, specialized review).
2. Prepare a concise prompt with required inputs and constraints.
3. Spawn the subagent in a fresh context.
4. Wait for completion and validate the output against the requested format.
5. Integrate findings, resolving conflicts or gaps as needed.

## Future Adapters

### Cursor
- Interface: `Switch to subagent` via Cursor agent picker.
- Inputs: include task goal, required files, and constraints.
- Output: paste results back into the main thread with citations.

### Codex CLI
- Interface: spawn with a dedicated task prompt and wait for completion.
- Inputs: include file paths and explicit output format.
- Output: summarize results and capture actionable steps.

### GitHub Copilot
- Interface: open a new agent session with a scoped prompt.
- Inputs: include artifacts (proposal, tasks, code diffs) and constraints.
- Output: return a concise result with prioritized actions.
