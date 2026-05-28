---
name: generate-agent
description: Generates a new OpenCode agent .md configuration file based on user requirements.
---

# Generate Agent

This skill allows the agent to create new specialized agents by generating a markdown file with the appropriate frontmatter and instructions.

## When to Use this Skill
This skill is activated when the user asks to:

- Create a new agent
- Add a specialized assistant
- "Teach you how to be a [Role]" (if implemented via a new agent)

## Instructions
When this skill is active, strictly follow these steps in order:

1.  **Requirement Analysis**: Identify the agent's name, description, mode (primary or subagent), preferred model, and tool permissions.
2.  **Destination Selection**: Determine the directory for the new agent.
    - Global: `~/.config/ai/agents/`
    - Per-project: `.opencode/agents/` (or current working directory's `agents/` folder)
3.  **Draft Frontmatter**: Construct the YAML frontmatter. Use the following fields:
    - `description`: A clear summary of the agent's role.
    - `mode`: `primary` (direct interaction) or `subagent` (invokable via @).
    - `model`: (Optional) Specify a specific model string.
    - `temperature`: (Optional) Usually 0.1 for technical agents.
    - `tools`: (Optional) Map of tool names to booleans.
4.  **Draft Instructions**: Write the system prompt/instructions for the agent. Focus on role, style, and constraints.
5.  **Write File**: Use the `write` tool to create the `.md` file. Ensure the filename matches the agent name (kebab-case).

## Critical Constraints
-   **ALWAYS** include the `---` separators for the frontmatter.
-   **NEVER** overwrite an existing agent file without explicit user confirmation.
-   **ALWAYS** verify the tool permissions are appropriate for the agent's role (e.g., read-only agents should have `write: false`, `edit: false`, `bash: false`).

## Examples

### Example 1: Creating a Documentation Agent
User: "Create a subagent called 'docs' that helps write documentation. It shouldn't be able to run bash commands."

1. **Frontmatter**:
```yaml
---
description: Specialized assistant for writing and refining documentation
mode: subagent
tools:
  bash: false
---
```
2. **Instructions**:
```markdown
You are a documentation expert. Your goal is to help the user write clear, concise, and accurate documentation.
Focus on:
- Clarity and readability
- Correct formatting (Markdown)
- Consistency in tone
```
3. **Write**: Save to `~/.config/ai/agents/docs.md`.
