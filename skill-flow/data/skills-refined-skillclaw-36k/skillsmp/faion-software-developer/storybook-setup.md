---
id: storybook-setup
name: "Storybook Setup"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Storybook Setup

## Overview

Storybook is an open-source tool for developing UI components in isolation. It enables component-driven development, visual testing, documentation, and design system maintenance.

## When to Use

- Developing component libraries
- Documenting design systems
- Visual regression testing
- Component showcase for designers
- Isolated component development

## Key Principles

- **Stories as documentation**: Each story demonstrates a use case
- **Isolation**: Components developed without app context
- **Addons for functionality**: Extend with accessibility, interactions
- **Single source of truth**: Stories document component API
- **Visual testing**: Catch UI regressions automatically

## Best Practices

### Initial Setup

```bash
# Initialize Storybook in existing project
npx storybook@latest init

# Or with specific framework
npx storybook@latest init --type react
```

### Configuration

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: [
    '../src/**/*.mdx',
    '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)',
  ],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
    '@storybook/addon-links',
    '@chromatic-com/storybook',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  staticDirs: ['../public'],
  typescript: {
    reactDocgen: 'react-docgen-typescript',
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      propFilter: (prop) => {
        // Filter out HTML attributes from docs
        if (prop.parent) {
          return !prop.parent.fileName.includes('node_modules');
        }
        return true;
      },
    },
  },
};

export default config;
```

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import { themes } from '@storybook/theming';
import '../src/styles/globals.css';

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
        { name: 'gray', value: '#f5f5f5' },
      ],
    },
    viewport: {
      viewports: {
        mobile: {
          name: 'Mobile',
          styles: { width: '375px', height: '667px' },
        },
        tablet: {
          name: 'Tablet',
          styles: { width: '768px', height: '1024px' },
        },
        desktop: {
          name: 'Desktop',
          styles: { width: '1280px', height: '800px' },
        },
      },
    },
    docs: {
      theme: themes.light,
    },
  },
  decorators: [
    (Story) => (
      <div style={{ padding: '1rem' }}>
        <Story />
      </div>
    ),
  ],
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        icon: 'circlehollow',
        items: ['light', 'dark'],
        showName: true,
      },
    },
  },
};

export default preview;
```

### Writing Stories

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Button, ButtonProps } from './Button';

// Meta configuration
const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: `
Button component for user interactions.

## Usage

\`\`\`tsx
import { Button } from '@/components/Button';

<Button variant="primary" onClick={handleClick}>
  Click me
</Button>
\`\`\`
        `,
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'danger'],
      description: 'Visual variant of the button',
      table: {
        type: { summary: 'ButtonVariant' },
        defaultValue: { summary: 'primary' },
      },
    },
    size: {
      control: 'radio',
      options: ['sm', 'md', 'lg'],
      description: 'Size of the button',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the button is disabled',
    },
    isLoading: {
      control: 'boolean',
      description: 'Whether to show loading state',
    },
    fullWidth: {
      control: 'boolean',
      description: 'Whether button takes full width',
    },
    onClick: {
      action: 'clicked',
      description: 'Click handler',
    },
  },
  args: {
    onClick: fn(),
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// Basic stories
export const Default: Story = {
  args: {
    children: 'Button',
  },
};

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    children: 'Secondary Button',
    variant: 'secondary',
  },
};

// Story with custom render
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'All available button variants.',
      },
    },
  },
};

// Story with sizes
export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};

// Interactive story
export const Loading: Story = {
  args: {
    children: 'Submitting...',
    isLoading: true,
  },
};

// Story with play function for interaction testing
export const ClickInteraction: Story = {
  args: {
    children: 'Click Me',
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await userEvent.click(button);
    await expect(args.onClick).toHaveBeenCalled();
  },
};
```

### Component Documentation with MDX

```mdx
{/* Button.mdx */}
import { Meta, Story, Canvas, Controls, Source } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';
import { Button } from './Button';

<Meta of={ButtonStories} />

# Button

Buttons allow users to trigger actions with a single tap.

## Import

```tsx
import { Button } from '@/components/Button';
```

## Basic Usage

<Canvas of={ButtonStories.Default} />

## Variants

The button comes in several visual variants:

<Canvas of={ButtonStories.AllVariants} />

### Primary

Use for the main call to action on a page.

<Canvas of={ButtonStories.Primary} />

### Secondary

Use for secondary actions.

<Canvas of={ButtonStories.Secondary} />

## Sizes

<Canvas of={ButtonStories.Sizes} />

## States

### Loading

<Canvas of={ButtonStories.Loading} />

### Disabled

<Canvas>
  <Button disabled>Disabled</Button>
</Canvas>

## Props

<Controls />

## Accessibility

- Uses native `<button>` element
- Supports keyboard navigation
- Loading state announced to screen readers
- Focus ring visible for keyboard users

## Best Practices

### Do

- Use clear, action-oriented labels
- Use primary variant for main CTA
- Ensure sufficient color contrast

### Don't

- Don't use multiple primary buttons in close proximity
- Don't use vague labels like "Click here"
- Don't disable buttons without explanation
```

### Decorators and Context

```tsx
// .storybook/preview.tsx
import { ThemeProvider } from '../src/contexts/ThemeContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
});

// Theme decorator
const withTheme = (Story, context) => {
  const theme = context.globals.theme;
  return (
    <ThemeProvider defaultTheme={theme}>
      <Story />
    </ThemeProvider>
  );
};

// React Query decorator
const withReactQuery = (Story) => (
  <QueryClientProvider client={queryClient}>
    <Story />
  </QueryClientProvider>
);

// Router decorator (for Next.js)
const withRouter = (Story) => (
  <RouterContext.Provider value={{ push: () => {} }}>
    <Story />
  </RouterContext.Provider>
);

const preview: Preview = {
  decorators: [withTheme, withReactQuery, withRouter],
};

export default preview;
```

### Interaction Testing

```tsx
// Form.stories.tsx
import { within, userEvent, expect } from '@storybook/test';
import { Form } from './Form';

export const FormSubmission: Story = {
  play: async ({ canvasElement, step }) => {
    const canvas = within(canvasElement);

    await step('Fill in form fields', async () => {
      await userEvent.type(
        canvas.getByLabelText(/name/i),
        'John Doe'
      );
      await userEvent.type(
        canvas.getByLabelText(/email/i),
        'john@example.com'
      );
    });

    await step('Submit form', async () => {
      await userEvent.click(
        canvas.getByRole('button', { name: /submit/i })
      );
    });

    await step('Verify success message', async () => {
      await expect(
        canvas.getByText(/form submitted successfully/i)
      ).toBeInTheDocument();
    });
  },
};

export const FormValidation: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Submit without filling fields
    await userEvent.click(
      canvas.getByRole('button', { name: /submit/i })
    );

    // Check for validation errors
    await expect(
      canvas.getByText(/name is required/i)
    ).toBeInTheDocument();

    await expect(
      canvas.getByText(/email is required/i)
    ).toBeInTheDocument();
  },
};
```

### Visual Testing with Chromatic

```yaml
# .github/workflows/chromatic.yml
name: Chromatic

on:
  push:
    branches: [main]
  pull_request:

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install dependencies
        run: npm ci

      - name: Build Storybook
        run: npm run build-storybook

      - name: Publish to Chromatic
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          buildScriptName: build-storybook
          autoAcceptChanges: main
          exitOnceUploaded: true
```

### Accessibility Testing

```tsx
// Button.stories.tsx
import { expect } from '@storybook/test';

export const AccessibilityTest: Story = {
  args: {
    children: 'Accessible Button',
  },
  play: async ({ canvasElement }) => {
    const results = await axe(canvasElement);
    expect(results.violations).toHaveLength(0);
  },
};

// In preview.ts - add global a11y addon config
export const parameters = {
  a11y: {
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
        { id: 'label', enabled: true },
      ],
    },
  },
};
```

### Organizing Stories

```typescript
// .storybook/main.ts
export default {
  stories: [
    // Documentation first
    '../src/docs/**/*.mdx',
    // Then components by category
    '../src/components/**/*.stories.@(js|jsx|ts|tsx)',
  ],
};

// Story titles create hierarchy
// title: 'Components/Buttons/Button' creates:
// Components
//   └── Buttons
//       └── Button

// Use prefixes for organization:
// 'Foundation/Colors' - Design tokens
// 'Components/Button' - UI components
// 'Patterns/DataTable' - Complex patterns
// 'Pages/Dashboard' - Full page examples
```

## Anti-patterns

- **Stories without documentation**: Just code, no explanation
- **Complex stories**: Stories doing too much
- **Missing interaction tests**: Not testing component behavior
- **Inconsistent naming**: Random story organization
- **No visual regression**: Missing Chromatic or similar
- **Outdated stories**: Stories not matching component API

## References

- [Storybook Documentation](https://storybook.js.org/docs)
- [Chromatic](https://www.chromatic.com/)
- [Component Story Format](https://storybook.js.org/docs/api/csf)
- [Storybook Addons](https://storybook.js.org/addons)
