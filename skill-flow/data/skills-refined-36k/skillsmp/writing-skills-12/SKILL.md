---
name: writing-skills
description: Use when creating, editing, evaluating, testing, or verifying ANY skill or skill-related file (SKILL.md, skill resources, skill scripts, or skill assets). If you're asked to evaluate or test a skill's effectiveness, use this skill.
---

## Understand Requirements First

When asked to create or edit a skill:

1. If helpful, **ask clarifying questions** about the skill's purpose:
   - What specific problem does this skill solve?
   - What should the output/outcome be?
   - What context or inputs will the skill work with?
   - What are the key behaviors or patterns it should enforce?

2. **Summarize your understanding** and get user confirmation:
   - "Let me confirm: this skill should [summary]. Is this correct?"
   - Wait for user approval before proceeding

3. **Get approval on your first test scenario** before running the full TDD cycle:
   - Describe the test scenario you plan to run
   - Explain what failure you expect to observe
   - Ask: "Does this test scenario match what you want to address?"
   - Wait for user approval before creating test files

**You cannot create a good test without understanding what you're testing.**

## Test-Driven Development

Follow the TDD methodology when writing skills:

- **Red:** Design a scenario you expect to fail without the skill and run it with a subagent. Document the exact behavior of the agent, including what choices it made, what failed and what triggered those failures. This is equivalent to "watch the test fail"—you must see what agents naturally do before writing the skill.
- **Green:** Write a skill that addresses the behaviors you documented. Only address what you observed. Don't add extra content for hypothetical cases.
- **Refactor:** Continue to evaluate with subagents. Every time a failure or rationalization appears, add an explicit counter. Keep re-testing until the skill is bulletproof.

**THE IRON LAW: DON'T WRITE A SKILL WITHOUT A FAILING EVALUATION FIRST.** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing. This applies to NEW skills AND EDITS to existing skills.

- Did you write the skill before testing it? Delete it. Start over.
- Did you edit the skill without testing it? Delete it. Start over.

## Required Reading

**STOP. Read these documents NOW. Not later. Not "as you go." Right now.**

- [Format Guide](references/format-guide.md)
- [Getting Agents to Follow Instructions](references/getting-agents-to-follow-instructions.md)
- [Script Conventions](references/scripts.md)
- [Agent Skills](https://code.claude.com/docs/en/skills.md)
- [Skill Specification](https://raw.githubusercontent.com/agentskills/agentskills/main/docs/specification.mdx)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
- [Persuasion Principles](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/persuasion-principles.md)
