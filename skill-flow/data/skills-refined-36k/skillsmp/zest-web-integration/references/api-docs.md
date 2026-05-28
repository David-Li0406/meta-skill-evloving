# Zest Design System - API Reference

**Version**: @yourcompany/design-system-components v4.1.7

## Official Documentation

- **Zest Design System**: https://zeroheight.com/43fd47df2/p/57c0b1-zest
- **YourCompany Design System**: Internal documentation
- **Component Storybook**: Internal Storybook

## Import Path

```typescript
import { Box, Text, Button, IconButton, Checkbox, TextArea } from '@/libs/zest';
import { CloseOutline16 } from '@/libs/zest-support/icons/generated/16';
import { ChevronRightOutline24 } from '@/libs/zest-support/icons/generated/24';
```

## Box Component

Foundational layout component with extensive styling props.

### Props

#### Layout Props

```typescript
interface BoxProps {
  // Display
  display?: 'flex' | 'block' | 'inline' | 'inline-block' | 'none' | 'grid';

  // Flexbox
  flexDirection?: 'row' | 'column' | 'row-reverse' | 'column-reverse';
  alignItems?: 'flex-start' | 'flex-end' | 'center' | 'stretch' | 'baseline';
  justifyContent?: 'flex-start' | 'flex-end' | 'center' | 'space-between' | 'space-around' | 'space-evenly';
  flexWrap?: 'wrap' | 'nowrap' | 'wrap-reverse';
  flexBasis?: string | number;
  flex?: string;
  order?: number | 'unset';

  // Sizing
  width?: string | number;
  height?: string | number;
  minWidth?: string | number;
  maxWidth?: string | number;
  minHeight?: string | number;
  maxHeight?: string | number;

  // Spacing - Longhand
  padding?: SpacingToken;
  paddingTop?: SpacingToken;
  paddingRight?: SpacingToken;
  paddingBottom?: SpacingToken;
  paddingLeft?: SpacingToken;
  paddingX?: SpacingToken;  // horizontal
  paddingY?: SpacingToken;  // vertical

  margin?: SpacingToken;
  marginTop?: SpacingToken;
  marginRight?: SpacingToken;
  marginBottom?: SpacingToken;
  marginLeft?: SpacingToken;
  marginX?: SpacingToken | 'auto';  // horizontal
  marginY?: SpacingToken;           // vertical

  // Spacing - Shorthand
  p?: SpacingToken;
  pt?: SpacingToken;
  pr?: SpacingToken;
  pb?: SpacingToken;
  pl?: SpacingToken;
  px?: SpacingToken;
  py?: SpacingToken;

  m?: SpacingToken;
  mt?: SpacingToken;
  mr?: SpacingToken;
  mb?: SpacingToken;
  ml?: SpacingToken;
  mx?: SpacingToken | 'auto';
  my?: SpacingToken;

  // Gap (for flex/grid)
  gap?: SpacingToken;
  columnGap?: SpacingToken;
  rowGap?: SpacingToken;

  // Positioning
  position?: 'relative' | 'absolute' | 'fixed' | 'sticky' | 'static';
  top?: SpacingToken | string;
  right?: SpacingToken | string;
  bottom?: SpacingToken | string;
  left?: SpacingToken | string;
  zIndex?: number;

  // Colors
  color?: ColorToken;
  backgroundColor?: ColorToken;

  // Visual
  opacity?: number;
  overflow?: 'visible' | 'hidden' | 'scroll' | 'auto';

  // HTML attributes
  id?: string;
  className?: string;
  children?: React.ReactNode;

  // Escape hatch (use sparingly)
  __dangerouslySetCustomCSS?: Record<string, any>;
}

type SpacingToken =
  | 'zero'
  | 'xxs'
  | 'xs'
  | 'sm-1'
  | 'sm-2'
  | 'md-1'
  | 'md-2'
  | 'lg-1'
  | 'lg-2'
  | `global.${SpacingToken}`;

type ColorToken =
  | `neutral.${100 | 200 | 300 | 400 | 500 | 600 | 700 | 800}`
  | `primary.${100 | 200 | 300 | 400 | 500 | 600 | 700 | 800}`
  | `error.${100 | 200 | 300 | 400 | 500 | 600 | 700 | 800}`;
```

### Responsive Arrays

**All props accept arrays for responsive values: `[mobile, tablet, desktop]`**

```typescript
<Box
  width={['100%', '50%', '33.33%']}
  flexDirection={['column', 'row']}
  padding={['sm-1', 'md-1', 'lg-1']}
  display={['none', 'flex']}
/>
```

### Usage Examples

```typescript
// Basic layout
<Box display="flex" flexDirection="column" padding="md-1">
  {children}
</Box>

// Responsive layout
<Box
  width={['100%', '100%', '33.33%']}
  flex={['0 0 100%', '0 0 100%', '0 0 33.33%']}
  p={['zero', 'sm-2']}
/>

// Centered container
<Box maxWidth={850} marginX="auto">
  {children}
</Box>

// Positioned element
<Box position="absolute" top="sm-1" right="sm-1">
  {children}
</Box>
```

## Text Component

Typography component with design system variants.

### Props

```typescript
interface TextProps {
  // Typography variant
  type?:
    | 'body-sm-regular'
    | 'body-sm-bold'
    | 'body-md-regular'
    | 'body-md-bold'
    | 'body-lg-regular'
    | 'body-lg-bold'
    | 'heading-1'
    | 'heading-2'
    | 'heading-3';

  // Semantic HTML element
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'p' | 'span' | 'div';

  // Color
  color?: ColorToken;

  // Error state (shorthand for error color)
  error?: boolean;

  // Spacing (same as Box)
  mt?: SpacingToken;
  mb?: SpacingToken;
  mx?: SpacingToken | 'auto';
  my?: SpacingToken;

  // Content
  children?: React.ReactNode;

  // HTML attributes
  id?: string;
  className?: string;
}
```

### Usage Examples

```typescript
// Heading with semantic HTML
<Text as="h1" type="heading-1">
  Page Title
</Text>

// Body text
<Text type="body-md-regular" color="neutral.800">
  Paragraph text
</Text>

// Bold text
<Text type="body-md-bold" color="primary.600">
  Important text
</Text>

// Error message
<Text error>
  Error message
</Text>

// Text with spacing
<Text mt="md-1" mb="sm-2" color="neutral.600">
  Spaced text
</Text>
```

## Button Components

### Button.Primary

Primary button variant.

```typescript
interface ButtonPrimaryProps {
  // State
  disabled?: boolean;
  loading?: boolean;

  // HTML button attributes
  type?: 'button' | 'submit' | 'reset';
  form?: string;  // Form ID for submit buttons

  // Event handlers
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;

  // Test identifiers
  id?: string;
  'data-test-id'?: string;

  // Content
  children: React.ReactNode;
}
```

**Usage:**
```typescript
<Button.Primary
  id="submit-button"
  data-test-id="submit-button"
  disabled={isDisabled}
  type="submit"
  form="checkout-form"
  onClick={handleSubmit}
  loading={isLoading}
>
  Submit Order
</Button.Primary>
```

### IconButton.Primary

Icon button variant.

```typescript
interface IconButtonPrimaryProps {
  // Icon
  icon: React.ReactElement;

  // Size
  size?: 'sm' | 'md' | 'lg';

  // Appearance
  appearance?: 'negative' | 'positive';

  // State
  disabled?: boolean;

  // Event handlers
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;

  // Test identifiers
  id?: string;
  'data-test-id'?: string;
}
```

**Usage:**
```typescript
import { IconButton } from '@/libs/zest';
import { CloseOutline16 } from '@/libs/zest-support/icons/generated/16';
import { ChevronRightOutline24 } from '@/libs/zest-support/icons/generated/24';

<IconButton.Primary
  size="sm"
  appearance="negative"
  icon={<CloseOutline16 />}
  onClick={handleClose}
/>

<IconButton.Primary
  size="lg"
  icon={<ChevronRightOutline24 />}
  onClick={handleNext}
/>
```

## Form Components

### Checkbox

Checkbox input with label.

```typescript
interface CheckboxProps {
  // Value
  checked: boolean;

  // Event handlers
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;

  // Label
  label: string | React.ReactNode;

  // HTML attributes
  id: string;
  name?: string;
  disabled?: boolean;

  // Test identifiers
  'data-test-id'?: string;
}
```

**Usage:**
```typescript
<Checkbox
  id="consent-checkbox"
  checked={hasConsent}
  onChange={(e) => setHasConsent(e.target.checked)}
  label="I agree to receive offers"
/>
```

### TextArea

Multi-line text input.

```typescript
interface TextAreaProps {
  // Dimensions
  rows?: number;
  cols?: number;

  // Value
  value?: string;
  defaultValue?: string;

  // Event handlers
  onChange?: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;

  // Accessibility
  'aria-label'?: string;

  // HTML attributes
  id?: string;
  name?: string;
  placeholder?: string;
  disabled?: boolean;
  readOnly?: boolean;
}
```

**Usage:**
```typescript
<TextArea
  rows={10}
  aria-label="Description"
  defaultValue={description}
  onChange={(e) => setDescription(e.target.value)}
/>
```

## Other Components

### Link

Navigation link component.

```typescript
interface LinkProps {
  href: string;
  linkColor?: ColorToken;
  children: React.ReactNode;
  target?: '_blank' | '_self';
  rel?: string;
}
```

### Spinner

Loading spinner.

```typescript
interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: ColorToken;
}
```

### Drawer

Drawer/modal component.

```typescript
interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  placement?: 'left' | 'right' | 'top' | 'bottom';
}
```

### Card

Card container component.

```typescript
interface CardProps {
  children: React.ReactNode;
  padding?: SpacingToken;
}
```

### Divider

Visual divider/separator.

```typescript
interface DividerProps {
  orientation?: 'horizontal' | 'vertical';
  color?: ColorToken;
}
```

### Tag

Tag/badge component.

```typescript
interface TagProps {
  children: React.ReactNode;
  color?: ColorToken;
}
```

## Responsive Array Syntax

**All component props that accept single values also accept arrays for responsive breakpoints.**

### Format

```typescript
[mobile, tablet, desktop]
```

### Examples

```typescript
// Layout
<Box flexDirection={['column', 'row']}>

// Sizing
<Box width={['100%', '50%', '33.33%']}>

// Spacing
<Box padding={['sm-1', 'md-1', 'lg-1']}>

// Visibility
<Box display={['none', 'flex']}>

// Order
<Box order={[1, 'unset']}>

// Conditional values
<Box display={[
  shouldHideOnMobile ? 'none' : 'flex',
  'flex',
]}>
```

## Theme Tokens Reference

### Spacing Tokens

```typescript
'zero'      // 0
'xxs'       // 2px
'xs'        // 4px
'sm-1'      // 8px
'sm-2'      // 12px
'md-1'      // 16px
'md-2'      // 24px
'lg-1'      // 32px
'lg-2'      // 48px
```

### Global Spacing

Prefix with `global.` for global spacing tokens:

```typescript
'global.sm-1'
'global.sm-2'
'global.md-1'
'global.md-2'
'global.lg-1'
'global.lg-2'
```

### Color Tokens

```typescript
// Neutral colors
'neutral.100'   // Lightest gray
'neutral.200'
'neutral.300'
'neutral.400'
'neutral.500'
'neutral.600'
'neutral.700'
'neutral.800'   // Darkest gray (text)

// Primary colors
'primary.100'   // Lightest primary
'primary.200'
'primary.300'
'primary.400'
'primary.500'
'primary.600'   // Standard primary (links, buttons)
'primary.700'
'primary.800'   // Darkest primary

// Error colors
'error.100'
'error.200'
'error.300'
'error.400'
'error.500'
'error.600'     // Standard error
'error.700'
'error.800'
```

## Breakpoints

Responsive arrays map to these breakpoints:

```typescript
[
  mobile,   // 0-768px
  tablet,   // 769-1024px
  desktop,  // 1025px+
]
```

## Custom CSS Escape Hatch

**Use only when Zest props are insufficient.**

```typescript
<Box
  // eslint-disable-next-line no-restricted-syntax
  __dangerouslySetCustomCSS={{
    animation: fadeInAnimation,
    transform: 'translateY(-10px)',
  }}
>
  {children}
</Box>
```

**Prefer:** Zest props or styled-components over custom CSS.

## Common Patterns

### Centered Container

```typescript
<Box maxWidth={850} marginX="auto">
  {children}
</Box>
```

### Flex Row with Gap

```typescript
<Box display="flex" flexDirection="row" gap="md-1">
  {children}
</Box>
```

### Responsive Column to Row

```typescript
<Box
  display="flex"
  flexDirection={['column', 'row']}
  gap={['sm-2', 'md-2']}
>
  {children}
</Box>
```

### Positioned Overlay

```typescript
<Box position="absolute" top="zero" left="zero" right="zero" bottom="zero">
  {children}
</Box>
```

### Card with Padding

```typescript
<Box
  padding="md-2"
  backgroundColor="neutral.100"
  borderRadius="md"
>
  {children}
</Box>
```
