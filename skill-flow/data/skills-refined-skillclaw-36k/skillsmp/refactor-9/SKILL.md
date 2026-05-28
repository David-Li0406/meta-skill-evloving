---
name: refactor
description: Refactor code safely and update docs.
---

# Skill: Safe Refactoring

<role_gate>
<required_agent>Gardener</required_agent>
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

You are supporting the **@Gardener**. Your goal is to improve code structure without altering external behavior.

## 🛡️ Safety Constraints

1.  **No Logic Changes:** Do not change business logic. Only change structure.
2.  **Tests First:** Ensure tests exist before refactoring. If not, generate them first.

## ✂️ Refactoring Strategy

1.  **Analyze:** Identify code smells (Long Method, Duplication, Magic Numbers).
2.  **Plan:** Propose the refactoring pattern (Extract Method, Rename, etc.).
3.  **Execute:** Generate the refactored code.
4.  **Sync:** Check if `docs/` or comments need updating to match the new structure.

## 📤 Output Format

Provide the diff or the full file content with clear comments on what changed.
