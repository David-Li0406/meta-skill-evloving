---
name: zest-component-creation-web
description: "WHAT: Create Zest design system components for web with BoxWithNewTokens, variants.ts, and component tokens. WHEN: building new Zest components from Figma, adding variants, creating reusable web UI. KEYWORDS: Zest, packages/zest, BoxWithNewTokens, Variant<UseNewTokens>, data-testid, ARIA, forwardRef, variants.ts, styles.ts, types.ts."
---

# Creating Zest Components for Web

Guide for creating new components in the Zest design system for web applications (packages/zest/src/ in the web repository).

## When to Use This Skill

Use this skill when:
- Creating a new Zest component from Figma designs
- Adding a new variant to an existing Zest component
- Building reusable UI components for the web design system
- Implementing components that will be used across multiple features/brands

## Core Principles

**Components live in `packages/zest/src/`**: All Zest components for web are in the `packages/zest/src/` directory within the web monorepo. This is the single source of truth for the Zest design system on web.

**Use BoxWithNewTokens**: Build new components using `BoxWithNewTokens` (imported as `Box`). This provides support for the new component token system.

**TypeScript is required**: All components must be written in TypeScript with proper type definitions using `Variant<UseNewTokens>[]` for variants.

**Component tokens for styling**: Use component-level design tokens (e.g., `'components.badge.color.neutral.background'`) rather than global tokens where possible.

**Accessibility is mandatory**: All components must be accessible (semantic HTML, ARIA attributes, keyboard navigation, focus management).

**Theme tokens only**: Never hardcode colors, spacing, or typography. Always use design tokens from the token system.

## File Structure

### Component Directory Structure

```
packages/zest/src/
└── MyComponent/
    ├── MyComponent.tsx         # Main component file (or index.tsx for simple components)
    ├── types.ts                # TypeScript interfaces and prop types
    ├── styles.ts               # Default styles as BoxProps
    ├── variants.ts             # Variant definitions using Variant<UseNewTokens>[]
    ├── MyComponent.test.tsx    # Component tests
    └── index.ts                # Barrel export
```

### Multi-Part Component Structure (e.g., NumberStepper, Accordion)

```
packages/zest/src/
└── NumberStepper/
    ├── index.ts                        # Object.assign export pattern
    ├── Container.tsx                   # Main container component
    ├── ValueContainer.tsx              # Sub-component
    ├── Buttons/                        # Sub-component directory
    │   ├── index.tsx
    │   ├── DecrementButton.tsx
    │   └── IncrementButton.tsx
    ├── types.ts
    ├── variants.ts
    ├── styles.ts
    ├── NumberStepper.spec.tsx
    ├── NumberStepper.interactions.spec.tsx
    └── NumberStepper.accessibility.spec.tsx
```

### Example: Creating a Badge Component (Based on Real Badge Implementation)

**types.ts**:
```typescript
// packages/zest/src/Badge/types.ts
import type { Icons16 } from '@/libs/zest-support/icons';
import type { CSSProperties } from 'react';

type Size = 'xs' | 'sm';

export type BadgeProps = {
  /**
   * Visual variant of the badge
   * @default 'neutral'
   */
  variant?: 'neutral' | 'reward' | 'error' | 'success' | 'information' | 'warning';

  /**
   * Badge content - string or icon
   */
  content?: string | React.ReactElement<Icons16>;

  /**
   * Size of the badge
   * @default 'xs'
   */
  size?: Size | Size[];

  /**
   * Show/hide stroke border
   * @default 'hide'
   */
  stroke?: 'show' | 'hide';
} & Omit<React.HTMLAttributes<HTMLDivElement>, keyof CSSProperties | 'style'>;
```

**variants.ts**:
```typescript
// packages/zest/src/Badge/variants.ts
import type { Variant, UseNewTokens } from '@/libs/zest-support';

const variants: Variant<UseNewTokens>[] = [
  {
    prop: 'variant',
    variants: {
      neutral: {
        bg: 'components.badge.color.neutral.background',
        color: 'components.badge.color.foreground',
      },
      error: {
        bg: 'components.badge.color.negative.background',
        color: 'components.badge.color.foreground',
      },
      success: {
        bg: 'components.badge.color.positive.background',
        color: 'components.badge.color.foreground',
      },
      reward: {
        bg: 'components.badge.color.reward.background',
        color: 'components.badge.color.foreground',
      },
      information: {
        bg: 'components.badge.color.information.background',
        color: 'components.badge.color.foreground',
      },
      warning: {
        bg: 'components.badge.color.warning.background',
        color: 'components.badge.color.foreground',
      },
    },
  },
  {
    prop: 'badgeSize',
    variants: {
      xs: { minWidth: '1rem', height: '1rem' },
      sm: { minWidth: '1.5rem', height: '1.5rem' },
    },
  },
  {
    prop: 'stroke',
    variants: {
      show: { borderWidth: '2px', borderStyle: 'solid', borderColor: 'global.white' },
      hide: {},
    },
  },
];

export default variants;
```

**styles.ts**:
```typescript
// packages/zest/src/Badge/styles.ts
import type { BoxProps } from '../Box/BoxWithNewTokens';

export default {
  display: 'inline-flex',
  justifyContent: 'center',
  alignItems: 'center',
  borderRadius: 'components.badge.border-radius.default',
} as BoxProps;
```

**Badge.tsx**:
```typescript
// packages/zest/src/Badge/Badge.tsx
import { forwardRef, Ref } from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import variants from './variants';
import defaultStyles from './styles';
import type { BadgeProps } from './types';

/**
 * ### Badge
 * Displays a small status indicator or count.
 *
 * See the [docs](https://www-staging.yourcompany.com/zest-docs/Badge) for more information.
 *
 * #### Usage
 * ```js
 * import { Badge } from '@/libs/zest';
 *
 * return (
 *   <Badge variant="success" size="sm">
 *     3
 *   </Badge>
 * )
 * ```
 */
const Badge = forwardRef((props: BadgeProps, ref?: Ref<HTMLDivElement>) => {
  const {
    variant = 'neutral',
    size = 'xs',
    stroke = 'hide',
    content,
    ...rest
  } = props;

  return (
    <Box
      {...defaultStyles}
      variants={variants}
      variant={variant}
      badgeSize={size}
      stroke={stroke}
      ref={ref}
      {...rest}
    >
      {typeof content === 'string' ? (
        <Text type="body-sm-bold" color="inherit">
          {content}
        </Text>
      ) : (
        content
      )}
    </Box>
  );
});

Badge.displayName = 'Badge';

export default Badge;
```

**index.ts** (barrel export):
```typescript
// packages/zest/src/Badge/index.ts
import Badge from './Badge';
export default Badge;
```

**MyComponent.test.tsx**:
```typescript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from './MyComponent';
import { ThemeProvider } from 'styled-components';
import { theme } from '@/libs/zest/theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('MyComponent', () => {
  it('renders children correctly', () => {
    renderWithTheme(<MyComponent>Test Content</MyComponent>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    renderWithTheme(
      <MyComponent onClick={handleClick} data-test-id="my-component">
        Click me
      </MyComponent>
    );

    const component = screen.getByTestId('my-component');
    fireEvent.click(component);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', () => {
    const handleClick = jest.fn();
    renderWithTheme(
      <MyComponent onClick={handleClick} disabled data-test-id="my-component">
        Click me
      </MyComponent>
    );

    const component = screen.getByTestId('my-component');
    fireEvent.click(component);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('renders different variants correctly', () => {
    const { rerender } = renderWithTheme(
      <MyComponent variant="primary" data-test-id="my-component">
        Primary
      </MyComponent>
    );

    let component = screen.getByTestId('my-component');
    expect(component).toHaveStyle({ backgroundColor: 'primary.600' });

    rerender(
      <ThemeProvider theme={theme}>
        <MyComponent variant="secondary" data-test-id="my-component">
          Secondary
        </MyComponent>
      </ThemeProvider>
    );

    component = screen.getByTestId('my-component');
    expect(component).toHaveStyle({ backgroundColor: 'neutral.100' });
  });
});
```

## Design Tokens

### Component Token Naming Convention

Component tokens follow this pattern: `'components.{component}.{property}.{variant}'`

**Examples**:
```typescript
// Colors
'components.badge.color.neutral.background'
'components.badge.color.foreground'
'components.button.color.brand.primary.background.default'
'components.tag.color.interactive.primary.foreground.default'

// Border Radius
'components.badge.border-radius.default'
'components.button.border-radius.default'

// Spacing
'components.button.spacing.lg.padding-y'
'components.inline-message.spacing.asset-gap'
```

### Global Tokens

Use global tokens for values not specific to a component:

```typescript
// In variants.ts
'global.white'
'global.gray.100'

// In Box props
<Box padding="global.md-1" gap="global.sm-2">
```

### Token Access in variants.ts

```typescript
import type { Variant, UseNewTokens } from '@/libs/zest-support';

const variants: Variant<UseNewTokens>[] = [
  {
    prop: 'variant',
    variants: {
      neutral: {
        bg: 'components.badge.color.neutral.background',   // Component token
        color: 'components.badge.color.foreground',        // Component token
      },
    },
  },
  {
    prop: 'stroke',
    variants: {
      show: {
        borderWidth: '2px',
        borderColor: 'global.white',  // Global token
      },
    },
  },
];
```

### Token Access in styles.ts

```typescript
import type { BoxProps } from '../Box/BoxWithNewTokens';

export default {
  display: 'inline-flex',
  borderRadius: 'components.badge.border-radius.default',
  padding: 'components.badge.spacing.padding',
} as BoxProps;
```

## Responsive Design

### Responsive Array Syntax

Use arrays for responsive values: `[mobile, tablet, desktop]`

```typescript
<Box
  width={['100%', '50%', '33.33%']}
  flexDirection={['column', 'row']}
  padding={['sm-1', 'md-1', 'lg-1']}
  display={['none', 'flex']}
>
```

### Conditional Responsive Patterns

```typescript
<Box
  display={[
    shouldHideOnMobile ? 'none' : 'flex',
    'flex',
  ]}
>
```

## Accessibility Requirements

### Semantic HTML

Use semantic HTML elements with Box `as` prop:

```typescript
// Button
<Box as="button" onClick={handleClick}>

// Link
<Box as="a" href="/path">

// Heading
<Box as="h2">

// Section
<Box as="section">
```

### ARIA Attributes

Always provide ARIA attributes for interactive elements:

```typescript
<Box
  as="button"
  onClick={handleClick}
  role="button"
  aria-label="Close dialog"
  aria-disabled={disabled}
  aria-expanded={isExpanded}
  aria-pressed={isPressed}
>
```

### Keyboard Navigation

Ensure keyboard navigation works:

```typescript
<Box
  as="button"
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
  tabIndex={0}
>
```

### Focus Management

Provide visible focus indicators:

```typescript
<Box
  as="button"
  onClick={handleClick}
  tabIndex={0}
  __dangerouslySetCustomCSS={{
    '&:focus': {
      outline: '2px solid',
      outlineColor: 'primary.600',
      outlineOffset: '2px',
    },
  }}
>
```

## Component Export Patterns

### Simple Component Export

```typescript
// packages/zest/src/Badge/index.ts
import Badge from './Badge';
export default Badge;
```

### Multi-Part Component Export (Object.assign pattern)

For components with sub-components like NumberStepper, Accordion, Tag:

```typescript
// packages/zest/src/NumberStepper/index.ts
import NumberStepper from './Container';
import Value from './ValueContainer';
import DecrementButton from './Buttons/DecrementButton';
import IncrementButton from './Buttons/IncrementButton';

export default Object.assign(NumberStepper, {
  Value,
  DecrementButton,
  IncrementButton,
});

// Usage:
<NumberStepper>
  <NumberStepper.DecrementButton onClick={decrement} />
  <NumberStepper.Value>{count}</NumberStepper.Value>
  <NumberStepper.IncrementButton onClick={increment} />
</NumberStepper>
```

### Variant-Based Component Export

For components with distinct visual variants like Button, Tag:

```typescript
// packages/zest/src/Button/index.tsx
import PrimaryButton from './PrimaryButton';
import SecondaryButton from './SecondaryButton';
import TertiaryButton from './TertiaryButton';

const Button = {
  Primary: PrimaryButton,
  Secondary: SecondaryButton,
  Tertiary: TertiaryButton,
};

export default Button;

// Usage:
<Button.Primary onClick={handleClick}>Submit</Button.Primary>
```

### Update Main Index File

After creating a component, export it from `packages/zest/src/index.ts`:

```typescript
// packages/zest/src/index.ts
export { default as Badge } from './Badge';
export { default as Button } from './Button';
export { default as NumberStepper } from './NumberStepper';

// Types
export type { BadgeProps } from './Badge/types';
export type { BaseButtonPropsWithoutVariant as ButtonProps } from './Button/types';
```

## Testing Patterns

### Basic Component Tests

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from 'styled-components';
import { theme } from '@/libs/zest/theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('MyComponent', () => {
  it('renders correctly', () => {
    renderWithTheme(<MyComponent>Test</MyComponent>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
```

### Testing Interactions

```typescript
it('handles click events', () => {
  const handleClick = jest.fn();
  renderWithTheme(
    <MyComponent onClick={handleClick} data-test-id="my-component">
      Click me
    </MyComponent>
  );

  fireEvent.click(screen.getByTestId('my-component'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

### Testing Variants

```typescript
it('renders different variants', () => {
  const { rerender } = renderWithTheme(
    <MyComponent variant="primary" data-test-id="test">
      Primary
    </MyComponent>
  );

  expect(screen.getByTestId('test')).toHaveAttribute('variant', 'primary');

  rerender(
    <ThemeProvider theme={theme}>
      <MyComponent variant="secondary" data-test-id="test">
        Secondary
      </MyComponent>
    </ThemeProvider>
  );

  expect(screen.getByTestId('test')).toHaveAttribute('variant', 'secondary');
});
```

### Testing Accessibility

```typescript
it('has proper accessibility attributes', () => {
  renderWithTheme(
    <MyComponent onClick={handleClick} data-test-id="test">
      Click me
    </MyComponent>
  );

  const component = screen.getByTestId('test');
  expect(component).toHaveAttribute('role', 'button');
  expect(component).toHaveAttribute('tabIndex', '0');
});
```

## Common Patterns

### Compound Components

For components with variants, use compound component pattern:

```typescript
// Button.tsx
const ButtonPrimary: React.FC<ButtonProps> = (props) => (
  <BaseButton {...props} variant="primary" />
);

const ButtonSecondary: React.FC<ButtonProps> = (props) => (
  <BaseButton {...props} variant="secondary" />
);

export const Button = {
  Primary: ButtonPrimary,
  Secondary: ButtonSecondary,
};

// Usage
<Button.Primary onClick={handleClick}>Submit</Button.Primary>
<Button.Secondary onClick={handleCancel}>Cancel</Button.Secondary>
```

### Forwarding Refs

For components that need ref forwarding:

```typescript
export const MyComponent = React.forwardRef<HTMLDivElement, MyComponentProps>(
  ({ children, ...props }, ref) => {
    return (
      <Box ref={ref} {...props}>
        {children}
      </Box>
    );
  }
);

MyComponent.displayName = 'MyComponent';
```

### Polymorphic Components

For components that can render as different HTML elements:

```typescript
export interface MyComponentProps<T extends React.ElementType = 'div'> {
  as?: T;
  children: React.ReactNode;
}

export const MyComponent = <T extends React.ElementType = 'div'>({
  as,
  children,
  ...props
}: MyComponentProps<T> & Omit<React.ComponentPropsWithoutRef<T>, keyof MyComponentProps<T>>) => {
  return (
    <Box as={as} {...props}>
      {children}
    </Box>
  );
};
```

## Common Mistakes

❌ **Don't hardcode colors**:
```typescript
// Wrong
<Box backgroundColor="#ffffff" color="#333333">
```

✅ **Do use theme tokens**:
```typescript
// Correct
<Box backgroundColor="neutral.100" color="neutral.800">
```

❌ **Don't hardcode spacing**:
```typescript
// Wrong
<Box padding="16px" margin="24px">
```

✅ **Do use spacing tokens**:
```typescript
// Correct
<Box padding="md-1" margin="lg-1">
```

❌ **Don't skip accessibility**:
```typescript
// Wrong
<Box onClick={handleClick}>Click me</Box>
```

✅ **Do add proper accessibility**:
```typescript
// Correct
<Box
  as="button"
  onClick={handleClick}
  role="button"
  aria-label="Close dialog"
  tabIndex={0}
>
  Click me
</Box>
```

❌ **Don't forget tests**:
```typescript
// Wrong - no tests
```

✅ **Do write comprehensive tests**:
```typescript
// Correct
describe('MyComponent', () => {
  it('renders correctly', () => { /* ... */ });
  it('handles interactions', () => { /* ... */ });
  it('is accessible', () => { /* ... */ });
});
```

## Quick Reference

**Component file structure**:
```
MyComponent/
├── MyComponent.tsx
├── MyComponent.types.ts
├── MyComponent.styles.ts
├── MyComponent.test.tsx
└── index.ts
```

**Basic component template**:
```typescript
import React from 'react';
import { Box, Text } from '@/libs/zest';
import { MyComponentProps } from './MyComponent.types';

export const MyComponent: React.FC<MyComponentProps> = ({
  children,
  variant = 'default',
  size = 'md',
  onClick,
  disabled = false,
  'data-test-id': testId,
}) => {
  return (
    <Box
      as={onClick ? 'button' : 'div'}
      onClick={onClick}
      disabled={disabled}
      data-test-id={testId}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      <Text type="body-md-regular">{children}</Text>
    </Box>
  );
};
```

**Export pattern**:
```typescript
// packages/zest/src/index.ts
export { MyComponent } from './components/MyComponent';
export type { MyComponentProps } from './components/MyComponent';
```
