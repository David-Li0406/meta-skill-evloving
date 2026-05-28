---
name: zest-component-development
description: Use this skill when creating or updating Zest design system components for web applications, ensuring adherence to design tokens, accessibility standards, and component structure.
---

# Zest Component Development

Comprehensive guide for creating and updating Zest design system components in the YourCompany `web` repository, based on established patterns and best practices.

## When to Use This Skill

Use this skill when:
- Creating a new Zest component from Figma designs.
- Adding a new variant to an existing Zest component.
- Migrating a legacy component to Zest patterns.
- Building reusable UI components for the web design system.
- Understanding Zest component architecture and conventions.

## Repository Structure

### Current Location
- **Main Package**: `packages/zest/src/`
- **Support Package**: `packages/zest-support/src/`
- **Documentation**: `apps/zest-docs/` (Storybook-based)
- **Main Export**: `packages/zest/src/index.ts`

### Import Paths
The codebase uses `@/libs/zest` as the import path (aliased to `packages/zest`). Both paths work:

```typescript
// Most common in existing code
import { Box, Text, Button } from '@/libs/zest';

// Also valid
import { Box, Text, Button } from '@/packages/zest';
```

## Core Principles

- **Components live in `packages/zest/src/`**: This is the single source of truth for the Zest design system on web.
- **Use BoxWithNewTokens**: Build new components using `BoxWithNewTokens` (imported as `Box`) for support of the new component token system.
- **TypeScript is required**: All components must be written in TypeScript with proper type definitions using `Variant<UseNewTokens>[]` for variants.
- **Component tokens for styling**: Use component-level design tokens (e.g., `'components.badge.color.neutral.background'`) rather than global tokens where possible.
- **Accessibility is mandatory**: All components must be accessible (semantic HTML, ARIA attributes, keyboard navigation, focus management).
- **Theme tokens only**: Never hardcode colors, spacing, or typography. Always use design tokens from the token system.

## Component Structure Patterns

### Simple Component (e.g., Badge, Tag, Pill)

```
packages/zest/src/Badge/
├── Badge.tsx           # Main component implementation
├── index.ts            # Export (export { default } from './Badge')
├── types.ts            # TypeScript type definitions
├── styles.ts           # Default styles object
└── variants.ts         # Variant configurations
```

**Use when**: Component has minimal complexity, few props, straightforward styling.

### Complex Component (e.g., Accordion, Modal)

```
packages/zest/src/Accordion/
├── index.tsx                    # Main component with context/composition
├── Title.tsx                    # Sub-component
├── Description.tsx              # Sub-component
├── ButtonWrapper/               # Nested sub-component directory
│   ├── index.tsx
│   └── ChevronIcon.tsx
├── types.ts                     # Type definitions
├── styles.ts                    # Style definitions
├── Accordion.test.tsx           # Tests
└── __snapshots__/               # Jest snapshot directory
    └── Accordion.test.tsx.snap
```

**Use when**: Component has multiple sub-components, uses React context, or has complex composition patterns.

### Component with Variants (e.g., Button)

```
packages/zest/src/Button/
├── BaseButton.tsx              # Base implementation
├── PrimaryButton.tsx           # Variant wrapper
├── SecondaryButton.tsx         # Variant wrapper
├── TertiaryButton.tsx          # Variant wrapper
├── index.tsx                   # Exports all variants
├── types.ts                    # Type definitions
├── defaultStyles.ts            # Base styles
├── variants/                   # Variant-specific styles
│   ├── index.ts
│   ├── brandVariants.ts
│   ├── negativeVariants.ts
│   ├── neutralVariants.ts
│   └── sizeVariants.ts
├── BaseButton.test.tsx         # Tests
└── __snapshots__/
    └── BaseButton.test.tsx.snap
```

**Use when**: Component has multiple distinct visual variants that warrant separate wrapper components.

## Core File Templates

### 1. Main Component File (`ComponentName.tsx`)

```typescript
import React, { Ref, forwardRef } from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import variants from './variants';
import defaultStyles from './styles';
import { ComponentNameProps } from './types';

/**
 * ### ComponentName
 * Brief description of component purpose.
 *
 * See the [docs](https://www-staging.yourcompany.com/zest-docs/ComponentName) for more information.
 *
 * #### Usage
 *
    ```js
    import { ComponentName } from '@/libs/zest';

    return (
      <ComponentName variant="neutral" size="md">
        Content
      </ComponentName>
    )
    ```
  */

const ComponentName = forwardRef((props: ComponentNameProps, ref?: Ref<HTMLDivElement>) => {
  const { children, variant = 'neutral', size = 'md', ...rest } = props;

  return (
    <Box
      ref={ref}
      variants={variants}
      variant={variant}
      size={size}
      {...rest}
      {...defaultStyles}
    >
      {children}
    </Box>
  );
});

ComponentName.displayName = 'ComponentName';

export default ComponentName;
```

### 2. Index File (`index.ts`)

**Simple Export**:
```typescript
import ComponentName from './ComponentName';
export default ComponentName;
```

**Complex Export (with sub-components)**:
```typescript
import React from 'react';
import Title from './Title';
import Description from './Description';
import type { ComponentProps } from './types';

const Component = {
  Primary: PrimaryVariant,
  Secondary: SecondaryVariant,
};

export default Object.assign(Component, { Title, Description });
```

### 3. Types File (`types.ts`)

```typescript
import type { Icons16, Icons24 } from '@/libs/zest-support/icons';
import type { StyledSystemComponent } from '@/libs/zest-support';
import type { CSSProperties } from 'react';

export type ComponentNameProps = {
  /**
   * Visual variant of the component
   * @default 'neutral'
   */
  variant?: 'neutral' | 'brand' | 'error' | 'success';

  /**
   * Size of the component
   * @default 'md'
   */
  size?: 'xs' | 'sm' | 'md' | 'lg';

  /**
   * Content to display
   */
  children: React.ReactNode;

  /**
   * Test identifier
   */
  'data-testid'?: string;
} & Omit<React.HTMLAttributes<HTMLDivElement>, keyof CSSProperties | 'style'>;
```

### 4. Styles File (`styles.ts`)

```typescript
import type { BoxProps } from '../Box/BoxWithNewTokens';

export default {
  display: 'inline-flex',
  justifyContent: 'center',
  alignItems: 'center',
  borderRadius: 'components.badge.border-radius.default',
  padding: 'components.badge.spacing.padding',
  gap: 'components.badge.spacing.gap',
} as BoxProps;
```

### 5. Variants File (`variants.ts`)

```typescript
import type { Variant, UseNewTokens } from '@/libs/zest-support';

const variants: Variant<UseNewTokens>[] = [
  {
    prop: 'variant',
    variants: {
      neutral: {
        bg: 'components.component.color.neutral.background',
        color: 'components.component.color.foreground',
      },
      brand: {
        bg: 'components.component.color.brand.background',
        color: 'components.component.color.foreground',
      },
      error: {
        bg: 'components.component.color.negative.background',
        color: 'components.component.color.foreground',
      },
      success: {
        bg: 'components.component.color.positive.background',
        color: 'components.component.color.foreground',
      },
    },
  },
  {
    prop: 'size',
    variants: {
      xs: {
        minWidth: '1rem',
        height: '1rem',
        fontSize: 'global.xs',
      },
      sm: {
        minWidth: '1.5rem',
        height: '1.5rem',
        fontSize: 'global.sm',
      },
      md: {
        minWidth: '2rem',
        height: '2rem',
        fontSize: 'global.md',
      },
      lg: {
        minWidth: '2.5rem',
        height: '2.5rem',
        fontSize: 'global.lg',
      },
    },
  },
];

export default variants;
```

### 6. Test File (`ComponentName.test.tsx`)

```typescript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentName from './ComponentName';

describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<ComponentName>Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('should render with different variants', () => {
    const { rerender } = render(<ComponentName variant="neutral">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();

    rerender(<ComponentName variant="brand">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('should handle click events', () => {
    const handleClick = jest.fn();
    render(<ComponentName onClick={handleClick}>Test</ComponentName>);

    fireEvent.click(screen.getByText('Test'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should match snapshot', () => {
    const { container } = render(<ComponentName variant="error">Test</ComponentName>);
    expect(container).toMatchSnapshot();
  });
});
```

## Updating Main Index

**Location**: `packages/zest/src/index.ts`

**Add Exports**:
```typescript
// Components
export { default as ComponentName } from './ComponentName';

// Types
export type { ComponentNameProps } from './ComponentName/types';
```

**Pattern**: Keep alphabetically sorted, group components and types separately.

## Storybook Documentation

**Location**: `apps/zest-docs/stories/ComponentName.stories.tsx`

```typescript
import type { Meta, StoryObj } from '@storybook/nextjs';
import { ComponentName } from '@/packages/zest';

const meta: Meta<typeof ComponentName> = {
  title: 'Components/Category/ComponentName',
  component: ComponentName,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['neutral', 'brand', 'error', 'success'],
      description: 'Visual variant of the component',
    },
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg'],
      description: 'Size of the component',
    },
  },
  parameters: {
    docs: {
      description: {
        component: 'Brief description of the component and its use cases.',
      },
    },
  },
};

export default meta;
type Story = StoryObj<typeof ComponentName>;

export const Default: Story = {
  args: {
    variant: 'neutral',
    children: 'Default Example',
  },
};

export const Variants: Story = {
  render: () => (
    <>
      <ComponentName variant="neutral">Neutral</ComponentName>
      <ComponentName variant="brand">Brand</ComponentName>
      <ComponentName variant="error">Error</ComponentName>
      <ComponentName variant="success">Success</ComponentName>
    </>
  ),
};

export const Sizes: Story = {
  render: () => (
    <>
      <ComponentName size="xs">Extra Small</ComponentName>
      <ComponentName size="sm">Small</ComponentName>
      <ComponentName size="md">Medium</ComponentName>
      <ComponentName size="lg">Large</ComponentName>
    </>
  ),
};
```

## Design Token Naming

**Component-Specific Tokens**:
```
components.[component].color.[variant].background
components.[component].color.foreground
components.[component].border-radius.[variant]
components.[component].spacing.[property]
```

**Global Tokens**:
```
global.gray.[100-900]
global.border.default
global.[xs|sm|md|lg|xl]
global.spacing.[value]
```

## Common Import Patterns

### From Zest Core
```typescript
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import Icon from '../Icon';
```

### From Zest Support
```typescript
import type { Variant, UseNewTokens, StyledSystemComponent } from '@/libs/zest-support';
import type { Icons16, Icons24 } from '@/libs/zest-support/icons';
import { useTheme } from '@/libs/zest-support';
```

### React Patterns
```typescript
import React, { forwardRef, createContext, useContext, Ref } from 'react';
```

## Accessibility Requirements

**Always Include**:
- Semantic HTML elements
- ARIA attributes (`role`, `aria-label`, `aria-describedby`, `aria-disabled`)
- Keyboard navigation (`tabIndex`, `onKeyDown`)
- Focus indicators
- Appropriate color contrast

**Example**:
```typescript
<Box
  role="status"
  aria-label={label}
  aria-disabled={disabled}
  tabIndex={disabled ? -1 : 0}
  onKeyDown={handleKeyPress}
>
  {children}
</Box>
```

## Common Mistakes

❌ **Don't hardcode styles**
```typescript
// Bad
bg: '#f0f0f0'
padding: '8px'
```

✅ **Use design tokens**
```typescript
// Good
bg: 'components.badge.color.neutral.background'
padding: 'components.badge.spacing.padding'
```

❌ **Don't use relative imports from outside packages**
```typescript
// Bad
import { Badge } from '../../packages/zest/src/Badge';
```

✅ **Use the aliased import path**
```typescript
// Good (standard)
import { Badge } from '@/libs/zest';

// Also good
import { Badge } from '@/packages/zest';
```

❌ **Don't skip TypeScript types**
```typescript
// Bad
export type BadgeProps = any;
```

✅ **Define proper types**
```typescript
// Good
export type BadgeProps = {
  variant?: 'neutral' | 'brand';
  children: React.ReactNode;
} & Omit<React.HTMLAttributes<HTMLDivElement>, keyof CSSProperties | 'style'>;
```

❌ **Don't skip tests**
```typescript
// Bad - no tests!
```

✅ **Write comprehensive tests**
```typescript
// Good - tests for rendering, variants, interactions, snapshots
describe('Badge', () => {
  it('should render correctly', () => { /* ... */ });
  it('should match snapshot', () => { /* ... */ });
});
```

## Quick Reference

### Adding New Component Checklist

- [ ] Create component directory in `packages/zest/src/[ComponentName]/`
- [ ] Create `ComponentName.tsx` with JSDoc and Figma reference comment
- [ ] Create `index.ts` with exports
- [ ] Create `types.ts` with TypeScript definitions
- [ ] Create `styles.ts` with default styles using design tokens
- [ ] Create `variants.ts` if component has variants
- [ ] Create `ComponentName.test.tsx` with comprehensive tests
- [ ] Update `packages/zest/src/index.ts` with exports
- [ ] Create `apps/zest-docs/stories/ComponentName.stories.tsx`
- [ ] Run tests: `yarn test`
- [ ] Run Storybook: `yarn storybook`

### Updating Existing Component Checklist

- [ ] Read existing component files
- [ ] Identify files that need changes
- [ ] Update component implementation
- [ ] Update types if adding new props
- [ ] Update