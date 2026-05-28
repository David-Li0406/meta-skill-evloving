---
name: create-custom-skill
description: Create a new GitHub Copilot Agent Skill (SKILL.md) with an appropriate folder structure and usage guidance.
---

# Skill: Custom Skill Creation Assistant

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

You are an expert in creating **GitHub Copilot Agent Skills**.
Your goal is to add a **new skill** to this repository under `.github/skills/<skill-directory>/` in a way that is easy for Copilot to discover and use.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks to track your progress:

1. **Fetch Documentation**: Retrieve the latest official docs (GitHub agent skills + open standard).
2. **Requirement Hearing**: Ask one question to understand the goal and when to use the skill.
3. **Draft Skill**: Propose naming, directory structure, and write `SKILL.md`.
4. **Proposal and Review**: Present the full `SKILL.md` and confirm.
5. **Create Files**: Write the skill folder/files into the workspace.
6. **Final Check**: Ensure conventions and discoverability.

## Step 1: Fetch Documentation (Mandatory)

Fetch and read the latest references before drafting:

1. GitHub Docs (Agent Skills):
   - https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
2. Open standard repository (AgentSkills):
   - https://github.com/agentskills/agentskills

Use the fetch tool available in your environment.

## Step 2: Requirement Hearing (Sequential Inquiry)

Ask **exactly one** question first and wait for the answer:

- “What should this skill achieve, and when should Copilot use it?”

Then proceed with auto-inference. Only ask follow-ups if there is a critical ambiguity that blocks producing a correct skill.

## Step 3: Draft the Skill (Directory + SKILL.md)

### 3.1 Choose the directory and identifiers

Infer and propose (brief reasons required):

- **Skill directory name**: kebab-case, lowercase, no spaces
  - Location: `.github/skills/<skill-directory>/`
- **Frontmatter `name`**: kebab-case, lowercase, unique
- **Frontmatter `description`**: what it does + when to use it (this is what Copilot uses to decide relevance)
- **License**: omit unless the user explicitly requests it

Notes:

- Prefer a directory name that matches `name` unless this repo has an established exception you must follow.

### 3.2 Decide whether to add a role gate

Default recommendation:

- Add a `<role_gate>` block whenever the skill is intended for a specific Terraformer agent persona (Architect/Developer/etc.).

If you add a role gate, set `<required_agent>` to the most appropriate persona.

### 3.3 Write SKILL.md content

Write `SKILL.md` as a Markdown file with YAML frontmatter.

Requirements:

- Clear, specific, repeatable procedure (numbered steps)
- Tool-aware guidance (which tools to use and in what order, if relevant)
- Minimal policy text; link to repository docs instead of duplicating

Recommended sections:

- Purpose
- When to use / When not to use
- Inputs and assumptions
- Procedure
- Output / Artifacts (what files or results are produced)
- Error handling / edge cases
- Final Check (checklist)

If the skill produces durable artifacts (specs, plans, reports), prefer writing them under `docs/specs/<FeatureName>/…` and link the conventions in [AGENTS.md](../../../AGENTS.md).

### 3.4 Optional supporting files

Only add additional files when they materially improve repeatability:

- `examples/…`
- `scripts/…`
- `resources/…`

## Step 4: Proposal and Review (Before writing files)

Present a concise proposal:

- Proposed folder path
- Proposed `name` + `description`
- Whether you will include `<role_gate>` (and why)
- Any extra files you plan to add

Then present the **full `SKILL.md`** content in a single code block.

Ask for confirmation:

- “I will create this skill with the proposed structure. Any changes?”

## Step 5: Create Files

After approval:

- Create the directory under `.github/skills/…`
- Write `SKILL.md`
- Write any supporting files you proposed

## ✅ Final Check

Before finishing, confirm:

- [ ] All todo items are completed.
- [ ] You fetched and used the latest GitHub Agent Skills docs.
- [ ] The skill lives under `.github/skills/<skill-directory>/`.
- [ ] The file is named `SKILL.md`.
- [ ] YAML frontmatter includes `name` and `description`.
- [ ] The `description` clearly states when to use the skill.
- [ ] Directory and `name` are kebab-case and unique.
