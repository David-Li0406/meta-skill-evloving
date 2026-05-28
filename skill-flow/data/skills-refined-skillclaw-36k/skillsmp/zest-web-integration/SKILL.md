---
name: zest-web-integration
description: "WHAT: Zest web integration with Box, Text, Button from @/libs/zest and ZestProvider from @/libs/zest-support. WHEN: creating layouts with Box, responsive design, using theme tokens for colors and spacing. KEYWORDS: Box, Text, Button.Primary, IconButton, @/libs/zest, @/libs/zest-support, ZestProvider, useTheme, responsive array, theme tokens."
---

# Zest Design System Integration - Web

Integration patterns for the Zest design system (`@/libs/zest` components + `@/libs/zest-support` utilities) in React web applications.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use Zest components for:
- Standard layouts, spacing, and typography
- Design system adherence and consistency
- Responsive design with breakpoint arrays
- Theme-aware components with design tokens
- Form inputs and interactive elements

**Use styled-components for:**
- Custom styling that doesn't exist in Zest
- Complex animations and transitions
- Component-specific styles beyond Zest capabilities

## Provider Setup

Zest components require `ZestProvider` at the app root:

```typescript
// app/spaces/_app/modules/shell/index.tsx
import { ZestProvider } from '@/libs/zest-support';

<ZestProvider
  {...(ssrPayload?.customBrand && {
    customBrand: ssrPayload.customBrand,
  })}
>
  {children}
</ZestProvider>
```

## Core Principles

### 1. Box Component for Layout

**Box is the foundational layout component with extensive styling props.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/cancellation/src/pages/Cancellation.tsx
import { Box, Text, Divider } from '@/libs/zest';

<Box
  display="flex"
  gap="md-1"
  alignItems="stretch"
  flexDirection={['column', 'column', 'row']}
>
  {deflectionCardsToRender.map((deflectionCardKey) => (
    <Box flex="1" alignSelf="stretch" key={deflectionCardKey}>
      <CardComponent />
    </Box>
  ))}
</Box>

// With padding and border radius
<Box
  py={['md-1', 'md-1', 'md-3']}
  px={['sm-1', 'sm-2', 'sm-2']}
  backgroundColor="neutral.100"
  borderRadius="border-radius-lg"
  boxShadow="shadow-xl"
>
  {/* Content */}
</Box>
```

**Why:** Box provides all layout props (flexbox, grid, spacing, positioning) with theme tokens.

### 2. Responsive Array Syntax

**Use arrays for responsive values: [mobile, tablet, desktop].**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:22
<Box
  width={['100%', '100%', '33.33%']}
  flex={['0 0 100%', '0 0 100%', '0 0 33.33%']}
  p={['zero', 'sm-2']}
  pb="sm-2"
>
  {/* Content */}
</Box>
```

**Common responsive patterns:**
```typescript
// Layout changes
<Box flexDirection={['column', 'row']}>

// Visibility
<Box display={['none', 'flex']}>

// Conditional display based on state
<Box display={[
  shouldHideOnMobile ? 'none' : 'flex',
  'flex',
]}>

// Spacing
<Box
  marginBottom={['md-2', 'lg-2']}
  paddingX={['sm-1', 'md-1', 'lg-1']}
>

// Sizing
<Box width={['100%', '50%', '33.33%']}>

// Order
<Box order={[1, 'unset']}>
```

**Why:** Array syntax automatically applies responsive breakpoints from the theme.

### 3. Theme Tokens for Spacing

**Use theme spacing tokens instead of hardcoded values.**

✅ **Good:**
```typescript
// app/spaces/checkout/modules/single-page/CheckoutFooter.tsx:34
import { Box } from '@/libs/zest';

<Box
  padding={isMobile ? 'global.sm-2' : 'global.md-2'}
  pt={'zero'}
  backgroundColor="neutral.100"
>
  {/* Content */}
</Box>
```

**Spacing token patterns:**
```typescript
// Longhand props
<Box padding="md-1" margin="sm-2">

// Shorthand props
<Box p="md-1" m="sm-2">

// Directional spacing
<Box
  paddingX="sm-2"    // horizontal padding
  paddingY="md-1"    // vertical padding
  marginX="auto"     // horizontal margin
  marginY="zero"     // vertical margin
>

// Individual sides
<Box
  pt="sm-2"    // paddingTop
  pb="md-1"    // paddingBottom
  mt="lg-1"    // marginTop
  mb="zero"    // marginBottom
>

// Global namespace
<Box
  padding="global.sm-2"
  mt="global.md-1"
  columnGap="global.lg-1"
>
```

**Common spacing values:**
- `zero`, `xxs`, `xs`, `sm-1`, `sm-2`, `md-1`, `md-2`, `lg-1`, `lg-2`
- Prefix with `global.` for global spacing tokens

**Why:** Theme tokens ensure consistency and enable theme switching.

### 4. Theme Tokens for Colors

**Use theme color tokens for all colors.**

✅ **Good:**
```typescript
// app/operations/state-definitions/use-product-details-state/OperationPlayground.tsx:62
<Box
  backgroundColor="error.600"
  color="primary.100"
>
  <Text color="primary.100" type="body-md-bold">
    Error: {error}
  </Text>
</Box>
```

**Color token patterns:**
```typescript
// Neutral colors
<Box color="neutral.800" backgroundColor="neutral.100">

// Primary colors
<Text color="primary.600">
<Link linkColor="primary.600">

// Error/semantic colors
<Box backgroundColor="error.600">
<Text error>  {/* Boolean shorthand for error color */}
```

**Why:** Color tokens maintain design consistency and support theme modes.

### 5. Text Component

**Use Text component for typography with type variants.**

✅ **Good:**
```typescript
// app/operations/state-definitions/use-product-details-state/OperationPlayground.tsx:69
import { Text } from '@/libs/zest';

<Text color="primary.100" type="body-md-bold">
  Error: {error}
</Text>

<Text as="h1">useProductDetailsState</Text>

<Text type="body-md-regular">
  Use this playground to test the state and actions
</Text>
```

**Text props:**
```typescript
// Typography variant
<Text type="body-md-regular">
<Text type="body-md-bold">

// Semantic HTML
<Text as="h1">Heading</Text>
<Text as="h2">Subheading</Text>
<Text as="p">Paragraph</Text>

// Color
<Text color="neutral.800">

// Error state
<Text error>Error message</Text>

// Spacing
<Text mt="md-1" mb="sm-2">
```

**Why:** Text component provides consistent typography and semantic HTML.

### 6. Button Components

**Use Button.Primary and IconButton.Primary compound components.**

✅ **Good:**
```typescript
// app/spaces/checkout/modules/single-page/CheckoutFooter.tsx:48
import { Button } from '@/libs/zest';

<Button.Primary
  id="upm-playground.btn.submit"
  data-test-id="upm-playground.btn.submit"
  disabled={isDisabled}
  type="submit"
  form={ADDRESS_FORM_ID}
  onClick={onClickButton}
  loading={isPlacingOrder}
>
  {CTALabel}
</Button.Primary>
```

**Icon and IconButton pattern:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/toasts/Toast.tsx
import { Box, Icon, Text } from '@/libs/zest';
import { CloseOutline24, CircleCheckmarkFilled24 } from '@/libs/zest-support/icons/generated/24';

// Define icon colors with theme tokens
const toastIconColor: Record<ToastTypes, Color> = {
  success: 'success.600',
  error: 'error.700',
};

// Usage
<Box display="flex" gap="xs">
  <Icon icon={toastIcon[type]} color={toastIconColor[type]} />
  <Text color={toastTextColor[type]}>{text}</Text>
</Box>

<Icon icon={<CloseOutline24 />} color="neutral.700" />
```

**Button props:**
- `disabled` - Boolean to disable button
- `type` - HTML button type ("submit", "button", "reset")
- `form` - Form ID for submit buttons
- `onClick` - Click handler
- `loading` - Show loading spinner
- `id`, `data-test-id` - Test identifiers

**IconButton props:**
- `size` - "sm", "md", "lg"
- `appearance` - "negative", etc.
- `icon` - React element for icon
- `onClick` - Click handler

**Why:** Compound components provide variant-specific styling with type safety.

### 7. Form Components

**Use Zest form components for inputs.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/payment/src/components/AdyenIdealForm/index.tsx
import { Box, Checkbox, Text, useTheme } from '@/libs/zest';

const theme = useTheme();
const borderColor = theme.colors.primary['600'];

<Box
  mb="sm-1"
  __dangerouslySetCustomCSS={{
    input: {
      marginRight: 'sm-1',
    },
  }}
>
  <Checkbox
    onChange={onChange}
    checked={!!values.idealTermsAndConditions}
    label={agreementText}
  />
</Box>
```

**TextArea pattern:**
```typescript
import { TextArea } from '@/libs/zest';

<TextArea
  rows={30}
  aria-label="Description"
  defaultValue={input}
  onChange={(e) => setInput(e.target.value)}
/>
```

**Why:** Form components provide consistent styling and accessibility.

## Advanced Patterns

### Flexbox Layout

```typescript
// app/unified-spaces/registration-page/steps/index.tsx:122
<Box
  display="flex"
  flexDirection={['column', 'row']}
  alignItems="center"
  justifyContent="center"
  flexBasis={['100%', '50%']}
  maxWidth={['100%', '50%']}
>
  {/* Content */}
</Box>
```

### Positioning

```typescript
// app/operations/state-definitions/use-product-details-state/OperationPlayground.tsx:59
<Box position="absolute" bottom="sm-1" left="sm-1">
  {/* Positioned content */}
</Box>
```

### Conditional Styling

```typescript
// app/spaces/checkout/modules/single-page/CheckoutFooter.tsx:36
<Box
  padding={isMobile ? 'global.sm-2' : 'global.md-2'}
  opacity={!isMobile && isDisabled ? 0.6 : 1}
>
  {/* Content */}
</Box>
```

### Custom CSS Escape Hatch

```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:29
<Box
  // eslint-disable-next-line no-restricted-syntax
  __dangerouslySetCustomCSS={{
    animation: fadeInBoxAnimation,
  }}
>
  {/* Content */}
</Box>
```

**Why:** Use only when Zest props are insufficient. Prefer Zest props or styled-components.

### Mixing with Styled Components

```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:92
import { Box, Text } from '@/libs/zest';
import styled from 'styled-components';

const EmptyBox = styled.div`
  height: 408px;
  width: 100%;
  border-radius: ${({ theme }) => theme.radii['border-radius-md']};
`;

export const EmptyMenu: React.FC = () => (
  <Box display="flex" flexDirection="column">
    <EmptyBox>
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        height="100%"
      >
        <Text mt="md-1">No meals selected</Text>
      </Box>
    </EmptyBox>
  </Box>
);
```

**Why:** Use Box for layout/spacing, styled-components for custom visual styling.

## Available Components

### Layout Components
- `Box` - Foundational layout component with all styling props
- `Divider` - Visual divider/separator
- `Card` - Card container component

### Typography
- `Text` - Typography component with variants

### Buttons
- `Button.Primary` - Primary button variant
- `IconButton.Primary` - Icon button variant

### Forms
- `Checkbox` - Checkbox input with label
- `TextArea` - Multi-line text input
- `Switch` - Toggle switch
- `Item` - List item / form item

### Navigation
- `Link` - Navigation link component

### Feedback
- `Spinner` - Loading spinner
- `Drawer` - Drawer/modal component

### Data Display
- `Carousel` - Carousel component
- `Tag` - Tag/badge component
- `Icon` - Icon wrapper

## File Organization

```
components/
└── MyComponent/
    ├── MyComponent.tsx       # Use Zest components
    ├── MyComponent.styles.ts # styled-components if needed
    └── index.ts              # Exports
```

## Common Mistakes

1. **Hardcoding spacing values** - Use theme tokens: `padding="md-1"` not `padding="16px"`
2. **Not using responsive arrays** - Use `width={['100%', '50%']}` for responsive sizing
3. **Hardcoding colors** - Use theme tokens: `color="neutral.800"` not `color="#333"`
4. **Using div instead of Box** - Box provides theme-aware props
5. **Not using shorthand props** - Use `p`, `mt`, `mb` instead of full names when convenient
6. **Mixing spacing systems** - Use Zest spacing OR styled-components, not both
7. **Forgetting global namespace** - Some tokens need `global.` prefix

## Quick Reference

### Basic Layout

```typescript
import { Box } from '@/libs/zest';

<Box
  display="flex"
  flexDirection="column"
  padding="md-1"
  margin="sm-2"
  backgroundColor="neutral.100"
>
  {/* Content */}
</Box>
```

### Responsive Layout

```typescript
<Box
  width={['100%', '50%', '33.33%']}
  flexDirection={['column', 'row']}
  padding={['sm-1', 'md-1', 'lg-1']}
  display={['none', 'flex']}
>
  {/* Content */}
</Box>
```

### Typography

```typescript
import { Text } from '@/libs/zest';

<Text type="body-md-bold" color="neutral.800">
  Heading
</Text>

<Text as="p" type="body-md-regular">
  Body text
</Text>

<Text error>Error message</Text>
```

### Button

```typescript
import { Button } from '@/libs/zest';

<Button.Primary
  disabled={isDisabled}
  loading={isLoading}
  onClick={handleClick}
>
  Submit
</Button.Primary>
```

### IconButton

```typescript
import { IconButton } from '@/libs/zest';
import { CloseOutline16 } from '@/libs/zest-support/icons/generated/16';

<IconButton.Primary
  size="sm"
  appearance="negative"
  icon={<CloseOutline16 />}
  onClick={handleClose}
/>
```

### Form Components

```typescript
import { Checkbox, TextArea } from '@/libs/zest';

<Checkbox
  id="checkbox-id"
  checked={isChecked}
  onChange={handleChange}
  label="Label text"
/>

<TextArea
  rows={5}
  aria-label="Description"
  defaultValue={value}
  onChange={(e) => setValue(e.target.value)}
/>
```

### Spacing Shorthand

```typescript
// Padding
<Box p="md-1" pt="sm-2" pb="lg-1" px="md-2" py="sm-1">

// Margin
<Box m="md-1" mt="sm-2" mb="lg-1" mx="auto" my="zero">

// Gap (for flex/grid)
<Box columnGap="global.sm-1" rowGap="md-1">
```

## Theme Token Reference

### Spacing
- `zero`, `xxs`, `xs`, `sm-1`, `sm-2`, `md-1`, `md-2`, `lg-1`, `lg-2`
- Prefix with `global.` when needed: `global.sm-2`, `global.md-1`

### Colors
- Neutral: `neutral.100`, `neutral.200`, `neutral.300`, `neutral.800`
- Primary: `primary.100`, `primary.600`
- Error: `error.600`

### Breakpoints (Array Indices)
- `[mobile, tablet, desktop]`
- Example: `width={['100%', '50%', '33.33%']}`
