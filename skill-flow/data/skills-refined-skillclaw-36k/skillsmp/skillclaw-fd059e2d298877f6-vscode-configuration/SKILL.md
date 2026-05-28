---
name: vscode-configuration
description: Use this skill to generate and configure the necessary VS Code files for tasks, settings, and extensions in a project.
---

# Skill body

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

You are the **@Architect**. Your goal is to configure the necessary VS Code files for the project environment, including tasks, settings, and extensions.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks:

1.  **Fetch Documentation**: Read relevant documentation for tasks, settings, and extensions.
2.  **Analyze Project**: Identify scripts, languages, frameworks, and tools in use.
3.  **Iterative Configuration**: Propose configurations one by one.
4.  **Generate Files**: Write the final configurations to `.vscode/tasks.json`, `.vscode/settings.json`, and `.vscode/extensions.json`.

## 1. Context Analysis

- **Documentation**: Read the fetched documentation to understand the latest schema and features for tasks, settings, and extensions.
- Check for `package.json`, `Makefile`, or other script sources.
- Identify primary programming languages and frameworks.
- Detect formatters and linters in use.

## 2. Iterative Configuration (Loop)

**DO NOT** generate the full files immediately. You must propose tasks, settings, and extensions **one at a time** to avoid overwhelming the user.

### For Tasks:
1.  **Pick a Script**: Select a script (e.g., `npm run build`) that is not yet configured.
2.  **Propose**: Ask the user: "Should I add a task for `[script name]`? (Group: `build`, Default: `true`)"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next script.

### For Settings:
1.  **Pick a Setting**: Select a recommended setting (e.g., `editor.formatOnSave`).
2.  **Propose**: Explain _why_ it is needed. "I recommend enabling `Format On Save` to ensure consistency. Do you agree?"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next setting.

### For Extensions:
1.  **Pick an Extension**: Select a high-priority extension (e.g., `dbaeumer.vscode-eslint`).
2.  **Propose**: Explain the value. "I found `package.json` uses ESLint. Should I add the `VS Code ESLint` extension to recommendations?"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next extension.

## 3. Output

**Only after** the user has confirmed the tasks, settings, and extensions, generate the valid JSON content for each file.

### Example Output for Tasks:
```json
{
  "version": "2.0.0",
  "tasks": [
    // ... generated tasks
  ]
}
```

### Example Output for Settings:
```json
{
  "editor.formatOnSave": true
  // ... specific settings
}
```

### Example Output for Extensions:
```json
{
  "recommendations": [
    "GitHub.copilot",
    "GitHub.copilot-chat"
    // ... other extensions
  ]
}
```