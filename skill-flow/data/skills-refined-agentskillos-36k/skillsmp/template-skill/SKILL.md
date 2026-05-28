---
name: template-skill
description: Starter template for authoring new skills. Use when creating or updating a skill folder with SKILL.md plus optional scripts, references, and assets.
---

# Template Skill

Use this template to stand up a new skill quickly. Follow the progressive-disclosure model: load only name/description for discovery, read full instructions on activation, and defer references/scripts/assets until needed.

## How to create a new skill
1) Copy this folder and rename it to your skill name.
2) Update the frontmatter name and description to match the new skill trigger conditions.
3) Replace this body with concise, actionable instructions the agent should follow when the skill is activated.
4) Keep instructions tight—assume the agent is capable and only add details that change behavior.

## Bundle optional resources
- scripts/ – Executable helpers the agent can run (see scripts/example_script.py for a CLI stub).
- references/ – Longer docs kept out of the main instructions to save context (see references/example_reference.md for guidance).
- assets/ – Templates or static resources to reuse (see assets/skill_skeleton.md for a SKILL.md scaffold).

## Authoring tips (from agentskills.io)
- Minimal metadata first; instructions live in SKILL.md; everything else is optional and loaded on demand.
- Keep the description narrowly scoped so activation is predictable.
- Design instructions so they are self-documenting and portable—skills are just files.
- Prefer concise examples over long exposition; link to references when detail is needed.
