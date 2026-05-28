# Skill Starter Reference

Use this as a quick-fill guide when standing up a new skill.

## Trigger examples
- "Summarize meeting notes into action items and decisions."
- "Generate a polished one-page PDF fact sheet from given bullets."
- "Create a React component with specified props and styling."

## Input checklist
- Required: files/text/links the skill must have before working.
- Ask for if missing: audience, tone, constraints, deadline, format.

## Output patterns
- Bullet summary plus next steps.
- Draft doc with sections (Intro, Body, Next steps).
- Code with inline comments and a one-paragraph usage note.

## Quality checks (pick what fits)
- Does the output match the ask? If not, fix it.
- Verify formatting, links, and paths; remove placeholders.
- If code: format/lint if possible; include a tiny test or usage snippet.

## Folder layout reminder
```
my-skill/
├── SKILL.md          # Instructions + metadata (required)
├── scripts/          # Optional helpers (document usage)
├── references/       # Optional deeper guidance
└── assets/           # Optional templates/resources
```
