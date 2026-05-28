# Zest Design System - Implementation Patterns

Implementation patterns and anti-patterns for Zest design system v4.1.7 integration.

## Pattern: Box for Layout

Use Box component for all layout and spacing needs.

✅ **Good:**
```typescript
import { Box } from '@/libs/zest';

<Box
  display="flex"
  flexDirection="column"
  padding="md-1"
  gap="sm-2"
>
  <Box>Item 1</Box>
  <Box>Item 2</Box>
  <Box>Item 3</Box>
</Box>
```

❌ **Bad:**
```typescript
// Using div instead of Box
<div style={{ display: 'flex', flexDirection: 'column', padding: '16px', gap: '12px' }}>
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

**Why:** Box provides:
- Theme-aware spacing tokens
- Responsive array syntax
- Type-safe props
- Design system consistency

## Pattern: Responsive Arrays

Use arrays for responsive values that change across breakpoints.

✅ **Good:**
```typescript
<Box
  width={['100%', '100%', '33.33%']}
  flexDirection={['column', 'row']}
  padding={['sm-1', 'md-1', 'lg-1']}
  display={['none', 'flex']}
>
  {children}
</Box>
```

❌ **Bad:**
```typescript
// Media queries instead of responsive arrays
const StyledDiv = styled.div`
  width: 100%;

  @media (min-width: 769px) {
    width: 50%;
  }

  @media (min-width: 1025px) {
    width: 33.33%;
  }
`;
```

**Why:** Responsive arrays:
- Use theme breakpoints automatically
- More concise than media queries
- Type-safe
- Consistent with design system

## Pattern: Theme Spacing Tokens

Always use theme tokens for spacing, never hardcoded values.

✅ **Good:**
```typescript
<Box
  padding="md-1"
  margin="sm-2"
  paddingX="lg-1"
  marginY="zero"
  gap="global.md-2"
>
  {children}
</Box>
```

❌ **Bad:**
```typescript
<Box
  // Hardcoded pixel values
  padding="16px"
  margin="12px"
>
  {children}
</Box>

// Or using style prop
<Box style={{ padding: '16px', margin: '12px' }}>
  {children}
</Box>
```

**Why:** Theme tokens:
- Ensure consistency across the app
- Enable theme switching
- Follow design system specs
- Easier to maintain

## Pattern: Shorthand Props

Use shorthand props for common spacing patterns.

✅ **Good:**
```typescript
<Box
  p="md-1"
  pt="sm-2"
  pb="lg-1"
  px="md-2"
  py="sm-1"
  m="md-1"
  mt="sm-2"
  mb="lg-1"
  mx="auto"
  my="zero"
>
  {children}
</Box>
```

❌ **Bad:**
```typescript
// Using full property names when shorthand is clearer
<Box
  padding="md-1"
  paddingTop="sm-2"
  paddingBottom="lg-1"
  paddingX="md-2"
  paddingY="sm-1"
  margin="md-1"
  marginTop="sm-2"
  marginBottom="lg-1"
  marginX="auto"
  marginY="zero"
>
  {children}
</Box>
```

**Why:** Shorthand props:
- More concise
- Easier to read
- Standard CSS shorthand convention
- Faster to type

## Pattern: Centered Containers

Use marginX="auto" for horizontal centering.

✅ **Good:**
```typescript
<Box maxWidth={850} marginX="auto" marginY="zero">
  {children}
</Box>
```

❌ **Bad:**
```typescript
// Manual centering with flexbox parent
<Box display="flex" justifyContent="center">
  <Box maxWidth={850}>
    {children}
  </Box>
</Box>
```

**Why:** `marginX="auto"`:
- Standard CSS pattern
- More direct
- Less DOM nesting
- Better performance

## Pattern: Text Component for Typography

Use Text component for all text content with design system variants.

✅ **Good:**
```typescript
import { Text } from '@/libs/zest';

<Text as="h1" type="heading-1" color="neutral.800">
  Page Title
</Text>

<Text as="p" type="body-md-regular" color="neutral.600">
  Paragraph text
</Text>

<Text type="body-md-bold" color="primary.600">
  Bold text
</Text>

<Text error>
  Error message
</Text>
```

❌ **Bad:**
```typescript
// Using HTML elements directly
<h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#333' }}>
  Page Title
</h1>

<p style={{ fontSize: '16px', color: '#666' }}>
  Paragraph text
</p>
```

**Why:** Text component:
- Provides design system typography variants
- Ensures consistent font sizes and weights
- Type-safe props
- Semantic HTML with `as` prop

## Pattern: Conditional Responsive Display

Use responsive arrays with conditional values for complex visibility logic.

✅ **Good:**
```typescript
<Box display={[
  shouldHideOnMobile ? 'none' : 'flex',
  'flex',
]}>
  {children}
</Box>

<Box display={[
  isMobileMenuOpen ? 'flex' : 'none',
  'none',
]}>
  {children}
</Box>
```

❌ **Bad:**
```typescript
// Conditional rendering instead of display prop
{!shouldHideOnMobile && isMobile && (
  <Box display="flex">
    {children}
  </Box>
)}

{!isMobile && (
  <Box display="flex">
    {children}
  </Box>
)}
```

**Why:** Display prop with conditional values:
- Keeps element in DOM (preserves state)
- Better for accessibility
- Simpler component structure
- Works with responsive arrays

## Pattern: Button.Primary for Actions

Use Button.Primary compound component for primary actions.

✅ **Good:**
```typescript
import { Button } from '@/libs/zest';

<Button.Primary
  id="submit-order"
  data-test-id="submit-order"
  disabled={isDisabled}
  type="submit"
  form="checkout-form"
  onClick={handleSubmit}
  loading={isLoading}
>
  Submit Order
</Button.Primary>
```

❌ **Bad:**
```typescript
// Custom button with manual styling
<button
  onClick={handleSubmit}
  disabled={isDisabled}
  style={{
    background: '#007bff',
    color: 'white',
    padding: '12px 24px',
    borderRadius: '4px',
  }}
>
  {isLoading ? 'Loading...' : 'Submit Order'}
</button>
```

**Why:** Button.Primary:
- Consistent design system styling
- Built-in loading state
- Accessible
- Type-safe props

## Pattern: IconButton for Icon-Only Actions

Use IconButton.Primary for icon-only buttons.

✅ **Good:**
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

❌ **Bad:**
```typescript
// Button with icon child
<button onClick={handleClose}>
  <CloseIcon />
</button>

// Or manual icon styling
<button onClick={handleClose}>
  <span style={{ fontSize: '16px' }}>✕</span>
</button>
```

**Why:** IconButton.Primary:
- Proper sizing for icons
- Consistent appearance variants
- Accessible button states
- Built-in icon positioning

## Pattern: Mix Zest with Styled-Components

Use Zest for layout/spacing, styled-components for custom visual styling.

✅ **Good:**
```typescript
import { Box, Text } from '@/libs/zest';
import styled from 'styled-components';

const CustomCard = styled.div`
  border: 2px solid ${({ theme }) => theme.colors.neutral['300']};
  border-radius: ${({ theme }) => theme.radii['border-radius-md']};
  background: linear-gradient(
    ${({ theme }) => theme.colors.neutral['200']},
    ${({ theme }) => theme.colors.neutral['100']}
  );
`;

export const Card: React.FC = () => (
  <Box padding="md-2">
    <CustomCard>
      <Box display="flex" flexDirection="column" gap="sm-2">
        <Text type="body-md-bold">Title</Text>
        <Text type="body-md-regular">Description</Text>
      </Box>
    </CustomCard>
  </Box>
);
```

❌ **Bad:**
```typescript
// All styling in styled-components
const StyledCard = styled.div`
  padding: 24px;
  border: 2px solid #ddd;
  border-radius: 8px;

  h3 {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 12px;
  }

  p {
    font-size: 14px;
  }
`;

export const Card: React.FC = () => (
  <StyledCard>
    <h3>Title</h3>
    <p>Description</p>
  </StyledCard>
);
```

**Why:** Mixing Zest and styled-components:
- Zest handles layout/spacing with theme tokens
- styled-components handles custom visuals
- Best of both worlds
- Maintains design system consistency

## Pattern: Global Namespace for Spacing

Use `global.` prefix for certain spacing tokens.

✅ **Good:**
```typescript
<Box
  padding="global.sm-2"
  mt="global.md-1"
  columnGap="global.lg-1"
  rowGap="global.md-2"
>
  {children}
</Box>
```

❌ **Bad:**
```typescript
// Missing global prefix where needed
<Box
  padding="sm-2"
  mt="md-1"
  columnGap="lg-1"
>
  {children}
</Box>
```

**Why:** Some spacing tokens require the `global.` prefix:
- Ensures correct token resolution
- Follows Zest design system spec
- Prevents runtime errors

## Pattern: Responsive Width with Flex Basis

Combine width and flex for responsive columns.

✅ **Good:**
```typescript
<Box
  width={['100%', '100%', '33.33%']}
  flex={['0 0 100%', '0 0 100%', '0 0 33.33%']}
  p={['zero', 'sm-2']}
>
  {children}
</Box>
```

❌ **Bad:**
```typescript
// Only using width without flex basis
<Box width={['100%', '100%', '33.33%']}>
  {children}
</Box>

// Or hardcoded flex values
<Box flex="0 0 33.33%">
  {children}
</Box>
```

**Why:** Width + flex:
- More predictable column sizing
- Prevents flex item overflow
- Responsive column layouts
- Standard flexbox pattern

## Pattern: Position Absolute with Spacing Tokens

Use spacing tokens for positioned element offsets.

✅ **Good:**
```typescript
<Box
  position="absolute"
  top="sm-1"
  right="sm-1"
  bottom="sm-2"
  left="md-1"
>
  {children}
</Box>
```

❌ **Bad:**
```typescript
<Box
  position="absolute"
  top="8px"
  right="8px"
  bottom="12px"
  left="16px"
>
  {children}
</Box>

// Or using style prop
<Box
  position="absolute"
  style={{ top: '8px', right: '8px' }}
>
  {children}
</Box>
```

**Why:** Spacing tokens for positioning:
- Consistent with spacing system
- Easier to maintain
- Theme-aware
- Predictable offsets

## Anti-Pattern: Custom CSS Escape Hatch

Avoid __dangerouslySetCustomCSS unless absolutely necessary.

❌ **Bad:**
```typescript
<Box
  __dangerouslySetCustomCSS={{
    padding: '16px',
    margin: '12px',
    display: 'flex',
    flexDirection: 'column',
  }}
>
  {children}
</Box>
```

✅ **Good:**
```typescript
// Use Zest props
<Box
  padding="md-1"
  margin="sm-2"
  display="flex"
  flexDirection="column"
>
  {children}
</Box>

// Or styled-components for complex custom styles
const CustomBox = styled.div`
  animation: ${fadeIn} 0.3s ease-in;
  transform: translateY(-10px);
`;

<Box padding="md-1">
  <CustomBox>
    {children}
  </CustomBox>
</Box>
```

**Why:** Avoid __dangerouslySetCustomCSS:
- Bypasses type safety
- Loses theme integration
- Harder to maintain
- Should be last resort only

## Anti-Pattern: Hardcoded Colors

Never hardcode color values.

❌ **Bad:**
```typescript
<Box backgroundColor="#f5f5f5" color="#333">
  <Text style={{ color: '#666' }}>
    Text content
  </Text>
</Box>
```

✅ **Good:**
```typescript
<Box backgroundColor="neutral.100" color="neutral.800">
  <Text color="neutral.600">
    Text content
  </Text>
</Box>
```

**Why:** Color tokens:
- Consistent color palette
- Theme switching support
- Accessibility compliance
- Design system adherence

## Anti-Pattern: Mixing Spacing Systems

Don't mix Zest spacing with styled-components spacing.

❌ **Bad:**
```typescript
const StyledBox = styled.div`
  padding: 16px;
  margin: 12px;
`;

<Box padding="md-1">
  <StyledBox>
    <Box margin="sm-2">
      {children}
    </Box>
  </StyledBox>
</Box>
```

✅ **Good:**
```typescript
// Use only Zest spacing
<Box padding="md-1">
  <Box margin="sm-2">
    {children}
  </Box>
</Box>

// Or only styled-components spacing
const StyledWrapper = styled.div`
  padding: ${({ theme }) => theme.space['md-1']};

  > div {
    margin: ${({ theme }) => theme.space['sm-2']};
  }
`;
```

**Why:** Consistent spacing system:
- Easier to reason about
- Predictable spacing
- Avoid conflicts
- Better maintainability

## Summary

**Key Patterns:**
- Use Box for all layouts with theme tokens
- Use responsive arrays: `[mobile, tablet, desktop]`
- Use shorthand props: `p`, `m`, `pt`, `mb`, `mx`, `my`
- Use Text component for typography
- Use Button.Primary and IconButton.Primary for actions
- Mix Zest (layout/spacing) with styled-components (custom visuals)
- Use `global.` prefix for certain spacing tokens
- Use spacing tokens for positioned elements

**Anti-Patterns to Avoid:**
- Hardcoded spacing/color values
- Using div instead of Box
- Media queries instead of responsive arrays
- __dangerouslySetCustomCSS for standard props
- Mixing spacing systems (Zest + styled-components)
- Missing `global.` prefix where needed
- Not using Text component for typography
