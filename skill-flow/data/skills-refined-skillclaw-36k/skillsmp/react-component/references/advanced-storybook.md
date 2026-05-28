# Advanced Storybook Guide

Using Storybook to render component states is the first step. Mastering it transforms Storybook from a component viewer into an interactive development environment, a documentation platform, and a collaboration tool.

This guide covers advanced patterns for getting the most out of Storybook.

## Table of Contents

1. [Interactive Controls with `argTypes`](#interactive-controls-with-argtypes)
2. [Logging Events with the `actions` Addon](#logging-events-with-the-actions-addon)
3. [Documenting Components with MDX](#documenting-components-with-mdx)
4. [Mocking API Requests in Stories](#mocking-api-requests-in-stories)
5. [Organizing Stories](#organizing-stories)

---

## 1. Interactive Controls with `argTypes`

`argTypes` allow you to customize and constrain the controls for your component's props (args) in the Storybook UI. This creates a powerful playground for testing component variations.

- **Use `argTypes` to:**
  - Define the control type (e.g., `color`, `date`, `select`).
  - Provide a set of options for a prop.
  - Add descriptions and default values to your props table.

### Example: Customizing Controls for a Button

```tsx
// src/components/ui/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'
import { PlusCircle } from 'lucide-react'

const meta = {
  title: 'UI/Button',
  component: Button,
  // This tags the story for auto-generated documentation
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'destructive', 'outline', 'secondary', 'ghost', 'link'],
      description: 'The visual style of the button',
    },
    size: {
      control: 'radio',
      options: ['default', 'sm', 'lg', 'icon'],
      description: 'The size of the button',
    },
    children: {
      control: 'text',
      description: 'The content of the button',
    },
    // Disable the control for a prop that shouldn't be edited in Storybook
    asChild: {
      table: {
        disable: true,
      },
    },
  },
  args: {
    // Default values for all stories
    variant: 'default',
    size: 'default',
    children: 'Click Me',
  },
} satisfies Meta<typeof Button>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const Destructive: Story = {
  args: {
    variant: 'destructive',
  },
}

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <PlusCircle className="mr-2 h-4 w-4" />
        Add Item
      </>
    ),
  },
}
```

---

## 2. Logging Events with the `actions` Addon

To verify that components emit events correctly (like `onClick` or `onSubmit`), use the `actions` addon. It will automatically log any calls to mocked functions in the "Actions" panel in the Storybook UI.

Storybook's `test` function, powered by Vitest and Testing Library, is the modern way to interact with your component and assert that actions were called.

### Example: Testing a Form Submission

```tsx
// src/features/orders/components/CreateOrderForm.stories.tsx
import { Meta, StoryObj } from '@storybook/react'
import { CreateOrderForm } from './CreateOrderForm'
import { expect } from '@storybook/test'
import { userEvent, within } from '@storybook/testing-library'

const meta = {
  title: 'Features/Orders/CreateOrderForm',
  component: CreateOrderForm,
  // `fn()` creates a spy function that logs to the Actions panel
  args: {
    onSubmit: fn(),
  },
} satisfies Meta<typeof CreateOrderForm>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const WithInput: Story = {
  // The `play` function contains interactions and assertions
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement)

    await userEvent.type(canvas.getByLabelText('Amount'), '1.5')
    await userEvent.type(canvas.getByLabelText('Recipient'), '0x1234...abcd')
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }))

    // Assert that the onSubmit function was called with the correct data
    await expect(args.onSubmit).toHaveBeenCalledWith({
      amount: '1.5',
      recipient: '0x1234...abcd',
    })
  },
}
```

---

## 3. Documenting Components with MDX

For complex components or design system documentation, you need more than just stories. MDX allows you to write long-form Markdown documents and embed interactive Storybook stories directly within them.

- **Use MDX to:**
  - Explain the component's purpose and usage guidelines.
  - Show "Do" and "Don't" examples.
  - Document accessibility considerations.
  - Render props tables and interactive stories.

### Example: Creating a Documentation Page

Create a file named `Button.mdx` alongside your `Button.stories.tsx` file.

````mdx
{/* src/components/ui/Button.mdx */}
import { Meta, Story, Canvas, ArgTypes } from '@storybook/blocks';
import \* as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

The `Button` component is the primary interactive element for user actions.

## Usage

Import the button from the UI components library:

```tsx
import { Button } from '@/components/ui/Button'
```
````

## Variants

The button comes in several variants to suit different levels of emphasis.

<Canvas>
  <Story of={ButtonStories.Default} />
  <Story of={ButtonStories.Destructive} />
  <Story of={ButtonStories.Outline} />
  <Story of={ButtonStories.Link} />
</Canvas>

## Props

Here are the props available for the Button component.

<ArgTypes />
```

---

## 4. Mocking API Requests in Stories

For container components that fetch data, you need to mock the API requests. The `msw-storybook-addon` integrates MSW (Mock Service Worker) into Storybook, allowing you to define API mocks that are active for specific stories.

1.  **Initialize the addon:** Follow the official `msw-storybook-addon` installation guide to initialize it in `.storybook/preview.js`.

2.  **Define mocks in a story:** Use the `msw.handlers` parameter to provide an array of MSW handlers for a specific story.

### Example: Story for a Container Component

```tsx
// src/features/revenue/components/RevenueCardContainer.stories.tsx
import { Meta, StoryObj } from '@storybook/react'
import { http, HttpResponse } from 'msw'
import { RevenueCardContainer } from './RevenueCardContainer'

const meta = {
  title: 'Features/Revenue/RevenueCardContainer',
  component: RevenueCardContainer,
} satisfies Meta<typeof RevenueCardContainer>

export default meta
type Story = StoryObj<typeof meta>

export const Ready: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('/api/revenue', () => {
          return HttpResponse.json({
            value: 124500,
            previousValue: 110600,
          })
        }),
      ],
    },
  },
}

export const Loading: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('/api/revenue', async () => {
          // Add a delay to simulate loading
          await delay('infinite')
          return HttpResponse.json({})
        }),
      ],
    },
  },
}

export const Error: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('/api/revenue', () => {
          return new HttpResponse(null, { status: 500 })
        }),
      ],
    },
  },
}
```

---

## 5. Organizing Stories

As the project grows, so will your number of stories. Use a clear and consistent naming convention in the `title` field to organize them.

A good convention is `Category/SubCategory/ComponentName`.

```ts
// Good: Creates a nested structure in the Storybook sidebar
title: 'Features/Orders/Forms/CreateOrderForm'
title: 'UI/Primitives/Button'
title: 'UI/Composites/DataTable'

// Bad: Flat and hard to navigate
title: 'CreateOrderForm'
title: 'Button'
```
