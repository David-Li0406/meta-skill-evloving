---
name: aico-frontend-init
description: Use this skill when you need to initialize a frontend environment by creating design system and constraints documents from templates.
---

# Frontend Init

Initialize frontend engineer configuration files: design system and constraints.

## Language Configuration

Before generating any content, check `aico.json` in the project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Check existing**: Look for `docs/reference/frontend/design-system.md` and `constraints.md`.
2. **Create directory structure**:
   ```
   docs/reference/frontend/
   ├── design-system.md
   ├── constraints.md
   ├── designs/
   └── tasks/
   ```
3. **Design System Setup**:
   - **Option A**: Extract from a reference website using the `aico-frontend-style-extraction` skill.
   - **Option B**: Use the template from `references/design-system.template.md`.
4. **Constraints Setup**:
   - Guide the user through tech stack questions.
   - Use the template from `references/constraints.template.md`.
5. **Save output**: Write to `docs/reference/frontend/`.

## Document Header Format

All generated documents MUST use this unified header format:

```markdown
# [Document Title]

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
```

## Design System Options

### Option A: Extract from Reference Website

If the user provides a reference URL:

1. Check if Playwright MCP is available.
2. Navigate to the URL → take a screenshot → analyze.
3. Extract design tokens using the `aico-frontend-style-extraction` skill.

### Option B: Fill Template

If no reference is provided:

1. Read the template from `references/design-system.template.md`.
2. Ask about color preferences (light/dark, accent color).
3. Ask about typography (serif/sans-serif).
4. Fill in reasonable defaults.

## Constraints Questions

| Question          | Options                                      |
| ----------------- | -------------------------------------------- |
| Framework         | React, Vue, Next.js, Svelte                  |
| TypeScript        | Yes (recommended), No                        |
| Component Library | shadcn/ui, Ant Design, MUI, None             |
| Styling           | Tailwind CSS, CSS Modules, styled-components  |