---
name: validate-skills
description: This skill should be used when the user asks to "validate skills", "check skill format", "verify agents", or "audit .claude directory".
---

# /validate-skills

Validate that all skills and agents in `.claude/` follow best practices from `.claude/AGENT_CLAUDE.md`.

## Instructions

1. **Scan for skill and agent files**:
   - List all `.md` files in `.claude/skills/` (flat files or `SKILL.md` in subdirectories)
   - List all `.md` files in `.claude/agents/`

2. **Validate Skills** against these criteria:

   **Required:**

   ```yaml
   ---
   name: skill-name # Lowercase, hyphens only, max 64 chars
   description: ... # Should use third-person and include trigger phrases
   ---
   ```

   **Best Practices:**
   - Description uses "This skill should be used when..." format
   - Description includes specific trigger phrases in quotes
   - Has `disable-model-invocation: true` if skill has side effects
   - Instructions are step-by-step and actionable
   - Content under 500 lines

3. **Validate Agents** against these criteria:

   **Required:**

   ```yaml
   ---
   name: agent-name # Lowercase, hyphens only
   description: ... # Should include <example> blocks
   tools: ["Read", "Grep"] # Array of allowed tools
   ---
   ```

   **Best Practices:**
   - Description includes `<example>` blocks with `<commentary>`
   - System prompt uses second person ("You are...")
   - Defines clear responsibilities and process
   - Specifies output format
   - Has quality criteria or success conditions

4. **Report findings**:

   **Valid:**
   - List each valid skill/agent with name and brief assessment

   **Issues Found:**
   - List specific problems for each file:
     - Missing or malformed frontmatter
     - Missing required fields
     - Description doesn't follow third-person format (skills)
     - Missing `<example>` blocks (agents)
     - Missing tools array (agents)
     - Placeholder text or TODOs
     - Excessive length (>500 lines)

   **Recommendations:**
   - Suggest improvements based on `.claude/AGENT_CLAUDE.md` guidelines
   - Flag side-effect skills missing `disable-model-invocation: true`
   - Identify agents that could benefit from more examples

5. **Summary**:

   ```
   Skills: X valid, Y need attention
   Agents: X valid, Y need attention

   Action items:
   - [specific fixes needed]
   ```
