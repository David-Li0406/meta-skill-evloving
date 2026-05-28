---
name: mantine-react-component-dev
description: Use this skill when creating, editing, or maintaining Mantine-based React components, implementing Styles API patterns, managing component composition, or working with TypeScript-safe component factories.
---

# Mantine React Component Development Skill

## When to Use This Skill

Apply this skill when working on:

- **Component Development**: Creating or editing React components built on Mantine's factory pattern.
- **TypeScript Patterns**: Implementing polymorphic components, type-safe props, and CSS variables.
- **Styles API**: Configuring component styling through Mantine's Styles API system (selectors, vars, modifiers).
- **Component Composition**: Building compound components with static sub-components (e.g., `Component.Target`).
- **Context Management**: Implementing safe context patterns for component state sharing.
- **Accessibility**: Ensuring ARIA compliance, keyboard navigation, and focus management.
- **Code Review**: Maintaining consistency with established patterns and conventions.
- **Documentation**: Writing component demos, MDX docs, and API references.

## Project Structure

Components are organized in a monorepo workspace structure:

- **`/package/src/`**: Main component source code
  - `ComponentName.tsx`: Main component implementation.
  - `ComponentName.module.css`: Component-scoped styles.
  - `ComponentName.context.ts`: Context providers (if needed).
  - `ComponentName.errors.ts`: Error messages.
  - `ComponentName.test.tsx`: Jest + Testing Library tests.
  - `ComponentName.story.tsx`: Storybook stories.
  - `SubComponent/SubComponent.tsx`: Sub-components in their own folders.
  - `index.ts`: Public exports.

- **`/docs/`**: Next.js documentation site
  - `demos/ComponentName.demo.*.tsx`: Interactive demos.
  - `styles-api/ComponentName.styles-api.ts`: Styles API metadata.
  - `docs.mdx`: Main documentation page.

Refer to existing components in [`./package/src/`](./package/src/) for implementation examples.

## TypeScript Patterns

### Component Factory Pattern

All components use Mantine's polymorphic factory pattern.

```typescript
import { polymorphicFactory, PolymorphicFactory, useProps, useStyles, createVarsResolver } from '@mantine/core';

export type ComponentStylesNames = 'root' | 'element';
export type ComponentCssVariables = {
  root: '--custom-var' | '--another-var';
};
```