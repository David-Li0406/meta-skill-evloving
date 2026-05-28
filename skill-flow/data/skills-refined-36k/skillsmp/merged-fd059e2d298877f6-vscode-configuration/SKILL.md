---
name: vscode-configuration
description: Use this skill to generate and configure VS Code settings, tasks, and extensions for a project.
---

# Skill: VS Code Configuration

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

You are the **@Architect**. Your goal is to configure the build, test, automation tasks, editor settings, and recommended extensions for the project environment.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks:

1.  **Fetch Documentation**: Read relevant documentation for tasks, settings, and extensions.
2.  **Analyze Project Scripts**: Scan `package.json`, `Makefile`, or other script sources.
3.  **Analyze Tech Stack**: Identify languages, frameworks, and tools in use.
4.  **Iterative Configuration**: Propose tasks, settings, and extensions one by one.
5.  **Generate Files**: Write the final configurations to `.vscode/tasks.json`, `.vscode/settings.json`, and `.vscode/extensions.json`.

## 1. Context Analysis

- **Documentation**: Read the fetched documentation to understand the latest schema and features for tasks, settings, and extensions.
- Check for `package.json`, `Makefile`, `Justfile`, or `Rakefile`.
- Identify primary programming languages and detect formatters and linters.

## 2. Iterative Configuration (Loop)

### Tasks Configuration

1.  **Pick a Script**: Select a script (e.g., `npm run build`) that is not yet configured.
2.  **Propose**: Ask the user: "Should I add a task for `[script name]`? (Group: `build`, Default: `true`)"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next script.

### Settings Configuration

1.  **Pick a Setting**: Select a recommended setting (e.g., `editor.formatOnSave`).
2.  **Propose**: Explain _why_ it is needed. "I recommend enabling `Format On Save` to ensure consistency. Do you agree?"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next setting.

### Extensions Recommendation

1.  **Pick an Extension**: Select a high-priority extension (e.g., `dbaeumer.vscode-eslint`).
2.  **Propose**: Explain the value. "I found `package.json` uses ESLint. Should I add the `VS Code ESLint` extension to recommendations?"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next extension.

## 3. Output

**Only after** the user has confirmed the tasks, settings, and extensions, generate the valid JSON content for each configuration file.

### Tasks Output

```json
{
  "version": "2.0.0",
  "tasks": [
    // ... generated tasks
  ]
}
```

### Settings Output

```json
{
  "editor.formatOnSave": true
  // ... specific settings
}
```

### Extensions Output

```json
{
  "recommendations": [
    "GitHub.copilot",
    "GitHub.copilot-chat"
    // ... other extensions
  ]
}
```