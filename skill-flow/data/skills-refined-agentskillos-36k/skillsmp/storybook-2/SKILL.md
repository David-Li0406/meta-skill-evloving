---
name: storybook
description: Storybook stories and interaction tests. Use for story, stories, storybook, chromatic, visual test, interaction test, play function, component test
---

# Storybook

## Quick Start

```tsx
import { type Meta, type StoryObj } from '@storybook/react-vite';

import { Button } from './button';

const meta = {
  component: Button,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  title: 'Components/Button',
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { children: 'Button', variant: 'default' },
};
```

## Args vs Render

Prefer `args` for simple props:

```tsx
export const Default: Story = {
  args: { children: 'Button', variant: 'default' },
};
```

Use `render` for complex layouts or multiple components:

```tsx
export const AllVariants: Story = {
  render: () => (
    <div className="flex gap-4">
      <Button variant="default">Default</Button>
      <Button variant="secondary">Secondary</Button>
    </div>
  ),
};
```

## Interaction Tests

Import from `storybook/test`:

```tsx
import { expect, fn, userEvent } from 'storybook/test';
```

### Click Interaction

```tsx
export const ClickInteraction: Story = {
  args: { children: 'Click me', onPress: fn() },
  play: async ({ args, canvas }) => {
    const button = canvas.getByRole('button');
    await userEvent.click(button);
    await expect(args.onPress).toHaveBeenCalledTimes(1);
  },
};
```

### Keyboard Interaction

```tsx
export const KeyboardInteraction: Story = {
  args: { children: 'Press Enter', onPress: fn() },
  play: async ({ args, canvas }) => {
    const button = canvas.getByRole('button');
    await userEvent.tab();
    await expect(button).toHaveFocus();
    await userEvent.keyboard('{Enter}');
    await expect(args.onPress).toHaveBeenCalledTimes(1);
  },
};
```

### Disabled State

```tsx
export const DisabledInteraction: Story = {
  args: { children: 'Disabled', isDisabled: true, onPress: fn() },
  play: async ({ args, canvas }) => {
    const button = canvas.getByRole('button');
    await expect(button).toBeDisabled();
    await expect(args.onPress).not.toHaveBeenCalled();
  },
};
```

### Accessibility Test

```tsx
export const IconOnlyAccessibility: Story = {
  args: {
    'aria-label': 'Add new item',
    children: <RiAddLine data-slot="icon" />,
    size: 'icon',
  },
  play: async ({ canvas }) => {
    const button = canvas.getByRole('button', { name: 'Add new item' });
    await expect(button).toBeInTheDocument();
    await expect(button).toHaveAccessibleName('Add new item');
  },
};
```

## Query Priority

Use accessible queries (Testing Library best practices):

| Priority | Query                  | Use For                |
| -------- | ---------------------- | ---------------------- |
| 1        | `getByRole`            | Buttons, inputs, links |
| 2        | `getByLabelText`       | Form fields            |
| 3        | `getByPlaceholderText` | Inputs without labels  |
| 4        | `getByText`            | Non-interactive text   |
| 5        | `getByTestId`          | Last resort            |

## Assertions Reference

| Assertion                  | Use For               |
| -------------------------- | --------------------- |
| `toBeInTheDocument()`      | Element exists        |
| `toBeVisible()`            | Element is visible    |
| `toBeDisabled()`           | Button/input disabled |
| `toHaveFocus()`            | Element has focus     |
| `toHaveAccessibleName()`   | Accessible label      |
| `toHaveBeenCalledTimes(n)` | Callback count        |
| `not.toHaveBeenCalled()`   | Callback not fired    |

## Chromatic Modes

Light/dark mode testing via `@storybook/addon-themes`:

```tsx
// .storybook/modes.ts
export const allModes = {
  dark: { theme: 'dark' },
  light: { theme: 'light' },
} as const;

// .storybook/preview.ts
parameters: {
  chromatic: {
    modes: {
      dark: allModes.dark,
      light: allModes.light,
    },
  },
}
```

### Chromatic Parameters

```tsx
export const AnimatedComponent: Story = {
  parameters: {
    chromatic: {
      delay: 300, // Wait before capturing
      disableSnapshot: true, // Skip this story
      pauseAnimationAtEnd: true,
      diffThreshold: 0.2, // Sensitivity (0-1)
    },
  },
};
```

### Viewports

```tsx
const meta = {
  parameters: {
    chromatic: { viewports: [320, 768, 1200] },
  },
} satisfies Meta<typeof Component>;

export const MobileOnly: Story = {
  parameters: { chromatic: { viewports: [320] } },
};
```

### Ignoring Elements

```tsx
<div className="chromatic-ignore"><Clock /></div>
<video data-chromatic="ignore" src="video.mp4" />

// Or via parameters
parameters: {
  chromatic: {
    ignoreSelectors: ['.timestamp', '.random-avatar'],
  },
}
```

## ArgTypes

```tsx
const meta = {
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'secondary', 'destructive', 'outline', 'ghost'],
    },
    size: { control: 'select', options: ['sm', 'default', 'lg', 'icon'] },
    isDisabled: { control: 'boolean' },
  },
  component: Button,
} satisfies Meta<typeof Button>;
```

## Play Function Composition

Reuse interactions across stories:

```tsx
export const FilledForm: Story = {
  play: async ({ canvas, userEvent }) => {
    await userEvent.type(canvas.getByLabelText('Email'), 'test@example.com');
    await userEvent.type(canvas.getByLabelText('Password'), 'password123');
  },
};

export const SubmittedForm: Story = {
  play: async (context) => {
    const { canvas, userEvent } = context;
    await FilledForm.play?.(context);
    await userEvent.click(canvas.getByRole('button', { name: 'Submit' }));
  },
};
```

## Waiting for Async Content

Use assertions instead of fixed delays:

```tsx
export const AsyncContent: Story = {
  play: async ({ canvas }) => {
    await expect(
      await canvas.findByRole('button', { name: 'Submit' }),
    ).toBeVisible();
  },
};
```

Use `findBy*` queries (with built-in waiting) for async elements.

## Accessibility Config

In `.storybook/preview.ts`:

```tsx
parameters: {
  a11y: {
    // 'todo' - show violations in test UI only
    // 'error' - fail CI on violations
    // 'off' - skip a11y checks
    test: 'error',
  },
}
```

## Common Mistakes

| Mistake                        | Correct Pattern                     |
| ------------------------------ | ----------------------------------- |
| Using `render` for simple args | Use `args` object instead           |
| `getByTestId` as first choice  | Use `getByRole` or `getByLabelText` |
| Fixed `delay` for async        | Use `findBy*` or assertions         |
| Missing `fn()` for callbacks   | Add `onPress: fn()` for interaction |
| Hardcoded viewport in story    | Use Chromatic `viewports` parameter |

## Delegation

- **Pattern discovery**: Use `Explore` agent to find existing story patterns
- **Component design**: Use `ui-library-designer` agent
