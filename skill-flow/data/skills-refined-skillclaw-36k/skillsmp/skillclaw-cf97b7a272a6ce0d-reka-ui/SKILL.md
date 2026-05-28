---
name: reka-ui
description: Use this skill when building with Reka UI (headless Vue components) to create accessible, unstyled components with a focus on WAI-ARIA compliance and flexible state management.
---

# Reka UI

Reka UI provides unstyled, accessible Vue 3 component primitives that are WAI-ARIA compliant. It was formerly known as Radix Vue.

**Current version:** v2.7.0 (December 2025)

## When to Use

- When building headless/unstyled components from scratch.
- When you need WAI-ARIA compliant components.
- When using Nuxt UI, shadcn-vue, or other Reka-based libraries.
- When implementing accessible forms, dialogs, menus, or popovers.

**For Vue patterns:** use the `vue` skill.

## Available Guidance

| File                                                     | Topics                                                              |
| -------------------------------------------------------- | ------------------------------------------------------------------- |
| **[references/components.md](references/components.md)** | Component index by category (Form, Date, Overlay, Menu, Data, etc.) |
| **components/\*.md**                                     | Per-component details (dialog.md, select.md, etc.)                  |

**New guides** (see [reka-ui.com](https://reka-ui.com)): Controlled State, Inject Context, Virtualization, Migration.

## Usage Pattern

**Load based on context:**

- For a component index, refer to [references/components.md](references/components.md).
- For specific components, refer to [components/dialog.md](components/dialog.md), [components/select.md](components/select.md), etc.
- For styled Nuxt components built on Reka UI, use the **nuxt-ui** skill.

## Key Concepts

| Concept                 | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `asChild`               | Render as a child element instead of a wrapper, merging props/behavior. |
| Controlled/Uncontrolled | Use `v-model` for controlled components, `default*` props for uncontrolled. |
| Parts                   | Components are split into Root, Trigger, Content, Portal, etc.       |
| `forceMount`            | Keep the element in the DOM for animation libraries.                 |
| Virtualization          | Optimize large lists (Combobox, Listbox, Tree) with virtual scrolling. |
| Context Injection       | Access component context from child components.                       |

## Installation

```ts
// nuxt.config.ts (auto-import)
```