---
name: vscode-settings
description: Generate .vscode/settings.json configuration.
---

# Skill: VS Code Settings Configuration

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

You are the **@Architect**. Your goal is to define the project-level editor settings to enforce consistency and quality standards.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks:

1.  **Fetch Documentation**: Read `https://code.visualstudio.com/docs/configure/settings#_settings-json-file`.
2.  **Analyze Tech Stack**: Identify languages and tools in use.
3.  **Iterative Configuration**: Propose settings one by one.
4.  **Generate File**: Write the configuration to `.vscode/settings.json`.

## 1. Context Analysis

- **Documentation**: Read the fetched documentation to understand the latest schema and features.
- Identify the primary programming languages.
- Detect formatters (Prettier, Black, Gofmt) and Linters (ESLint, Ruff).

## 2. Iterative Configuration (Loop)

**DO NOT** generate the full file immediately. You must propose settings **one at a time** to avoid overwhelming the user.

1.  **Pick a Setting**: Select a recommended setting (e.g., `editor.formatOnSave`).
2.  **Propose**: Explain _why_ it is needed. "I recommend enabling `Format On Save` to ensure consistency. Do you agree?"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next setting (e.g., Linting, Exclusions).

## 3. Output

**Only after** the user has confirmed the settings, generate the valid JSON content for `.vscode/settings.json`.

```json
{
  "editor.formatOnSave": true
  // ... specific settings
}
```
