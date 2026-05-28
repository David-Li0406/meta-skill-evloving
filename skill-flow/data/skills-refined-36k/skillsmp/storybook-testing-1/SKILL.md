---
name: storybook-testing
version: 3.0.0
lastUpdated: 2026-01-18
description: Create comprehensive Storybook stories with interactive tests for React components using CSF Next format and play functions. Use when writing component tests, interaction tests, or documenting component behavior.
tags: [testing, storybook, react, component-testing, integration-testing, play-function, csf-next]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
examples:
  - Write Storybook tests for UserProfileCard component
  - Create story tests for my LoginForm
  - Add Storybook testing to the ProductCard component
  - Generate comprehensive Storybook stories with tests for NavBar
---

# Storybook Testing Skill

Generate comprehensive Storybook stories with interactive tests using CSF Next format and `play` functions for React components.

> **Reference Files:**
> - [patterns.md](./patterns.md) - Testing patterns and examples
> - [best-practices.md](./best-practices.md) - Best practices and common pitfalls
> - [examples.md](./examples.md) - Practical code examples
> - [templates.md](./templates.md) - Component test templates
> - [design-system.md](./design-system.md) - Testing @szum-tech/design-system components
> - [api-reference.md](./api-reference.md) - Complete API documentation

## Context

This project uses **Storybook 10+ with CSF Next format** - the latest Component Story Format with factory functions for full type safety.

Stories are used for:
- **Component testing** - Test components in isolation
- **Interaction testing** - Verify user interactions (clicks, typing)
- **Validation testing** - Test form validation and error states
- **Accessibility testing** - Verify a11y with addon

## Workflow

1. **Analyze component** - Props, interactions, states, callbacks
2. **Create story file** - Same directory as component: `component.stories.tsx`
3. **Write stories** - Cover different scenarios using CSF Next format
4. **Add play functions** - Test assertions and interactions
5. **Run tests** - `npm run test:storybook`

## CSF Next Format

CSF Next uses factory functions that provide full type safety:

```
definePreview → preview.meta → meta.story
```

### Story File Structure

```typescript
import { expect, fn, waitFor } from "storybook/test";

import preview from "~/.storybook/preview";

import { ComponentName } from "./component-name";

const meta = preview.meta({
  title: "Features/[FeatureName]/ComponentName",
  component: ComponentName,
  args: {
    onAction: fn()
  }
});

export const Default = meta.story({
  play: async ({ canvas, userEvent, args, step }) => {
    const button = canvas.getByRole("button");
    await userEvent.click(button);
    await expect(args.onAction).toHaveBeenCalled();
  }
});
```

### Key Differences from CSF 3.0

| CSF 3.0 | CSF Next |
|---------|----------|
| `import type { Meta, StoryObj }` | `import preview from "~/.storybook/preview"` |
| `const meta = { } satisfies Meta<typeof C>` | `const meta = preview.meta({ })` |
| `export default meta` | No default export needed |
| `type Story = StoryObj<typeof meta>` | Types inferred automatically |
| `export const Story: Story = { }` | `export const Story = meta.story({ })` |

## Story Naming Conventions

- `InitialForm` - Empty/initial state
- `Prefilled` - Component with data
- `ValidationEmptyForm` - Validation errors
- `Interaction` - User interaction flows
- `LoadingState` - Async/loading states
- `CompleteUserFlow` - End-to-end scenarios
- `ServerErrorHandling` - Error handling

## Play Function Parameters

- `canvas` - Testing Library queries scoped to component
- `canvasElement` - Raw DOM element (for portal queries)
- `userEvent` - Pre-configured interaction methods
- `args` - Story args (props)
- `step` - Group assertions into named steps

## Using Test Builders

**Always prefer builders over inline mock data:**

```typescript
import preview from "~/.storybook/preview";

import { userBuilder } from "~/features/*/test/builders";
import { fn } from "storybook/test";

import { UserCard } from "./user-card";

const meta = preview.meta({
  component: UserCard
});

export const WithData = meta.story({
  args: {
    user: userBuilder.one(),
    onSubmit: fn()
  }
});
```

If builder doesn't exist, invoke `/builder-factory` skill first.

## Running Tests

```bash
npm run test:storybook  # Run component tests
npm run storybook:dev   # View in Storybook UI
```

## Questions to Ask

- What user interactions should be tested?
- Are there specific edge cases to cover?
- What validation rules should be tested?
- Are there server actions that need mocking?
