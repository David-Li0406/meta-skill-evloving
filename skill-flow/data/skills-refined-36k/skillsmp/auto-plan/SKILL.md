---
name: auto-plan
description: ALWAYS INVOKE when user asks to plan, create a plan, or needs a development plan - spawns plan-forge agent in background
---

# Plan Skill

Automatically detect when users want to create development plans and handle them using the plan-forge MCP server.

## Trigger Patterns

This skill should be invoked when the user's request matches patterns like:

- "plan <task> in the background"
- "create a development plan for <task>"
- "start planning <task>"
- "plan out <task>"
- "make a plan for <task>"
- "I need a plan for <task>"
- "generate a plan for <task>"

## Behavior

When triggered:

1. **Extract the task** from the user's request
2. **Spawn background agent** using the Task tool with `plan-forge` agent and `run_in_background: true`
3. **Acknowledge immediately** - don't wait for planning to complete
4. **Provide status check instructions**

## Response Template

```
I've started a background planning session for: "<task>"

The plan-forge agent is now:
1. Analyzing the codebase
2. Generating a comprehensive development plan
3. Reviewing and refining until quality threshold is met

This typically takes 1-5 iterations (30 seconds to a few minutes).

**Check progress:** `/plan status`
**View results:** `/plan get plan`

I'll continue to be available while planning runs in the background.
```

## Example Interactions

### Example 1: Explicit background request
```
User: Plan adding OAuth authentication in the background

Claude: I've started a background planning session for: "adding OAuth authentication"
        [spawns plan-forge agent with run_in_background: true]
        Check progress with `/plan status`
```

### Example 2: Implicit planning request
```
User: I need a development plan for implementing user roles

Claude: I've started a background planning session for: "implementing user roles"
        [spawns plan-forge agent with run_in_background: true]
        Check progress with `/plan status`
```

### Example 3: Status check follow-up
```
User: How's that plan coming along?

Claude: [calls plan_status via MCP]
        Session: implementing-user-roles
        Status: in_progress
        Iteration: 2 of 5
        Still working on it...
```

## Integration with /plan Command

This skill works alongside the `/plan` slash command:
- Skill: Auto-detects planning intent in natural conversation
- Command: Explicit invocation with `/plan <task>`

Both use the same underlying plan-forge MCP tools and background agent.

## Handling needs_input Response

When you check on a background agent (via TaskOutput) and it returns with `status="needs_input"`:

1. **Store the agentId** for later resume
2. **Present questions clearly** to user:

   "**Planning paused** - the reviewer needs your input:

   {reason from agent response}

   Please provide your answers and I'll continue planning."

3. **When user responds**, resume the same agent:
   ```
   Task tool:
   - prompt: "User provided these answers: {user_response}"
   - subagent_type: plan-forge
   - resume: {stored agentId}
   - run_in_background: true
   ```

This uses Claude Code's resumable subagents feature - the agent continues with full context and remembers what questions it asked.

## Notes

- Always use background execution for new plans
- User can continue conversation while planning runs
- Plans are saved to `dev/active/<slug>/` when complete
- If plan needs human input, agent stops and returns with `needs_input` status
- Use the `resume` parameter to continue the same agent with user's answers
