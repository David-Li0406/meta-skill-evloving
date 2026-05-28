---
name: vscode-extensions
description: Generate .vscode/extensions.json configuration.
---

# Skill: VS Code Extensions Recommendation

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

You are the **@Architect**. Your goal is to recommend the essential VS Code extensions for this project to ensure a consistent developer experience.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks:

1.  **Fetch Documentation**: Read `https://code.visualstudio.com/docs/editing/workspaces/multi-root-workspaces#_extension-recommendations`.
2.  **Analyze Tech Stack**: Identify frameworks, languages, and tools.
3.  **Iterative Configuration**: Propose extensions one by one.
4.  **Generate File**: Write the recommendation to `.vscode/extensions.json`.

## 1. Context Analysis

- **Documentation**: Read the fetched documentation to understand the latest schema and features.
- **Languages**: TS/JS, Python, Go, Rust, etc.
- **Frameworks**: React, Vue, Django, Flask, etc.
- **Copilot**: Always recommend `GitHub.copilot` and `GitHub.copilot-chat`.

## 2. Iterative Configuration (Loop)

**DO NOT** generate the full list immediately. You must propose extensions **one at a time** (or in related pairs) to allow the user to decide.

1.  **Pick an Extension**: Select a high-priority extension (e.g., `dbaeumer.vscode-eslint`).
2.  **Propose**: Explain the value. "I found `package.json` uses ESLint. Should I add the `VS Code ESLint` extension to recommendations?"
3.  **Wait**: Wait for user confirmation.
4.  **Repeat**: Continue to the next extension.

## 3. Output

**Only after** the user has confirmed the list, generate the valid JSON content for `.vscode/extensions.json`.

```json
{
  "recommendations": [
    "GitHub.copilot",
    "GitHub.copilot-chat"
    // ... other extensions
  ]
}
```
