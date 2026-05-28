---
name: nuxt-ui
description: Use this skill when building styled UI with @nuxt/ui v4 components (Button, Modal, Form, Table, etc.) - it provides ready-to-use components with Tailwind Variants theming.
---

# Nuxt UI v4

Component library for Vue 3 and Nuxt 4+ built on Reka UI (headless) + Tailwind CSS v4 + Tailwind Variants.

**Current stable version:** v4.3.0 (December 2025)

## When to Use

- Installing/configuring @nuxt/ui
- Using UI components (Button, Card, Table, Form, etc.)
- Customizing theme (colors, variants, CSS variables)
- Building forms with validation
- Using overlays (Modal, Toast, CommandPalette)
- Working with composables (useToast, useOverlay)

**For Vue component patterns:** use `vue` skill  
**For Nuxt routing/server:** use `nuxt` skill

## Available Guidance

| File                                                         | Topics                                                                           |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **[references/installation.md](references/installation.md)** | Nuxt/Vue setup, pnpm gotchas, UApp wrapper, module options, prefix, tree-shaking |
| **[references/theming.md](references/theming.md)**           | Semantic colors, CSS variables, app.config.ts, Tailwind Variants                 |
| **[references/components.md](references/components.md)**     | Component index by category (125+ components)                                    |
| **components/\*.md**                                         | Per-component details (button.md, modal.md, etc.)                                |
| **[references/forms.md](references/forms.md)**               | Form components, validation (Zod/Valibot), useFormField                          |
| **[references/overlays.md](references/overlays.md)**         | Toast, Modal, Slideover, Drawer, CommandPalette                                  |
| **[references/composables.md](references/composables.md)**   | useToast, useOverlay, defineShortcuts, useScrollspy                              |

## Usage Pattern

**Load based on context:**

- Installing Nuxt UI? → [references/installation.md](references/installation.md)
- Customizing theme? → [references/theming.md](references/theming.md)
- Component index → [references/components.md](references/components.md)
- Specific component → [components/button.md](components/button.md), [components/modal.md](components/modal.md), etc.
- Building forms? → [references/forms.md](references/forms.md)
- Using overlays? → [references/overlays.md](references/overlays.md)