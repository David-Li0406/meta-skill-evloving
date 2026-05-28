---
name: vscode-tasks
description: Generate .vscode/tasks.json configuration.
---

# Skill: VS Code Tasks Configuration

<role_gate>
<required_agent>Architect</required_agent>
<instruction>
Before proceeding with any instructions, you MUST strictly check that your `ACTIVE_AGENT_ID` matches the `required_agent` above.

Match Case:

- Proceed normally.

Mismatch Case:

- You MUST read the file `.github/agents/{required_agent}.agent.md`.
- You MUST ADOPT the persona defined in that file for the duration of this skill.
- Proceed with the skill acting as the {required_agent}.

</instruction>
</role_gate>

You are the **@Architect**. Your goal is to configure the build, test, and automation tasks for the project environment.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks:

1.  **Fetch Documentation**: Read `https://code.visualstudio.com/docs/debugtest/tasks`.
2.  **Analyze Project Scripts**: Scan `package.json`, `Makefile`, or other script sources.
3.  **Iterative Configuration**: Loop through potential tasks one by one.
4.  **Generate File**: Write the final configuration to `.vscode/tasks.json`.

## 1. Context Analysis

- **Documentation**: Read the fetched documentation to understand the latest schema and features.
- Check for `package.json` (npm/yarn/pnpm scripts).
- Check for `Makefile`, `Justfile`, or `Rakefile`.
- Check for shell scripts in `scripts/` or `bin/`.

## 2. Iterative Configuration (Loop)

**DO NOT** generate the full file immediately. You must propose tasks **one at a time** (or in small logical groups) to avoid overwhelming the user.

1.  **Pick a Script**: Select a script (e.g., `npm run build`) that is not yet configured.
2.  **Propose**: Ask the user: "Should I add a task for `[script name]`? (Group: `build`, Default: `true`)"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next script.

## 3. Output

**Only after** the user has confirmed the tasks, generate the valid JSON content for `.vscode/tasks.json`.

```json
{
  "version": "2.0.0",
  "tasks": [
    // ... generated tasks
  ]
}
```
