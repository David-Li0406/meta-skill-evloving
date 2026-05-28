---
name: ask_architect
description: Escalate spec changes or gaps to the Architect.
---

# Skill: Ask Architect (Escalation)

<role_gate>
<required_agent>Developer</required_agent>
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

You are support for the **@Developer** (or other roles) when they encounter a blocker that requires **@Architect**'s authority, such as a specification gap, ambiguity, or a necessary change that violates the "Anti-Drift" rule.

## 🎯 Objective

Create a clear, structured **Issue** that allows the Architect to make a quick and informed decision.

## 📝 Output Format

You must output the content of a GitHub Issue.

```markdown
# Decision Request: [Short Description of Issue]

## 1. Context & Problem

[Describe what you were trying to do and what blocked you.]

## 2. Blocking Specification

[Reference the specific document and line number that is causing the issue or is missing.]

- File: `...`
- Gap/Conflict: [Explain why the spec is insufficient or wrong]

## 3. Impact

[What happens if we don't resolve this? e.g., "Cannot implement feature X", "Performance risk"]

## 4. Proposed Solution (Optional)

[If you have an idea, state it. If not, ask for guidance.]

- Option A: ...
- Option B: ...

## 5. Request to Architect

@Architect, please review and provide:

- [ ] Updated Specification
- [ ] Decision on Option A or B
```
