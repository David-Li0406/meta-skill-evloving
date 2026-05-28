---
name: skill-creator
description: Use this skill when you need to create new AI agent skills following the Agent Skills specification, particularly when documenting patterns or adding agent instructions.
---

## When to Create a Skill

Create a skill when:
- A pattern is used repeatedly and AI needs guidance.
- Project-specific conventions differ from generic best practices.
- Complex workflows need step-by-step instructions.
- Decision trees help AI choose the right approach.

**Don't create a skill when:**
- Documentation already exists (create a reference instead).
- The pattern is trivial or self-explanatory.
- It's a one-off task.

---

## Skill Structure

```
skills/{skill-name}/
├── SKILL.md              # Required - main skill file
├── assets/               # Optional - templates, schemas, examples
│   ├── template.py
│   └── schema.json
└── references/           # Optional - links to local docs
    └── docs.md           # Points to docs/developer-guide/*.mdx
```

---

## SKILL.md Template

```markdown
---
name: {skill-name}
description: >
  {One-line description of what this skill does}.
  Trigger: {When the AI should load this skill}.
license: Apache-2.0
metadata:
  author: {Your Name}
  version: "1.0"
---

## When to Use

{Bullet points of when to use this skill}

## Critical Patterns

{The most important rules - what AI MUST know}

## Code Examples

{Minimal, focused examples}

## Commands

```bash
{Common commands}
```

## Resources

- **Templates**: See [assets/](assets/) for {description}
- **Documentation**: See [references/](references/) for local docs
```

---

## Naming Conventions

| Type | Pattern | Examples |
|------|---------|----------|
| Generic skill | `{technology}` | `pytest`, `playwright`, `typescript` |
| Project-specific | `{project}-{component}` | `myproject-api`, `myproject-ui`, `myproject-sdk` |
| Testing skill | `{project}-test-{component}` | `myproject-test-sdk`, `myproject-test-api` |
| Workflow skill | `{action}-{target}` | `skill-creator`, `jira-task` |

---

## Decision: assets/ vs references/

```
Need code templates?        → assets/
Need JSON schemas?          → assets/
Need example configs?       → assets/
Link to existing docs?      → references/
Link to external guides?    → references/ (with local path)
```

**Key Rule**: `references/` should point to LOCAL files.