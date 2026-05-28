# Zest Design System - Production Examples

Real-world examples of Zest (@yourcompany/design-system-components v4.1.7) integration.

## Example 1: Box Layout with Responsive Arrays

**File**: `app/unified-spaces/registration-page/steps/index.tsx:115`

```typescript
import { Box } from '@/libs/zest';

<Box
  id="umk-registration-steps-container"
  maxWidth={850}
  marginX="auto"
  marginY="zero"
>
  <Box
    display="flex"
    flexDirection={['column', 'row']}  // Mobile: column, Desktop: row
    paddingX="sm-2"
    paddingTop="sm-2"
    paddingBottom="zero"
    marginBottom={['md-2', 'lg-2']}  // Mobile: md-2, Desktop: lg-2
  >
    {/* Content */}
  </Box>
</Box>
```

**Key patterns:**
- Responsive flexDirection: `['column', 'row']`
- Auto horizontal margin: `marginX="auto"`
- Responsive spacing: `marginBottom={['md-2', 'lg-2']}`

## Example 2: Responsive Width and Flex

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:22`

```typescript
<Box
  width={['100%', '100%', '33.33%']}      // Mobile/Tablet: 100%, Desktop: 33.33%
  flex={['0 0 100%', '0 0 100%', '0 0 33.33%']}
  p={['zero', 'sm-2']}                    // Mobile: no padding, Desktop: sm-2
  pb="sm-2"
>
  {/* Content */}
</Box>
```

**Key patterns:**
- Three breakpoints: `[mobile, tablet, desktop]`
- Flex basis with width
- Conditional padding

## Example 3: Theme Spacing Tokens

**File**: `app/spaces/checkout/modules/single-page/CheckoutFooter.tsx:34`

```typescript
<Box
  padding={isMobile ? 'global.sm-2' : 'global.md-2'}
  pt={'zero'}
  backgroundColor="neutral.100"
>
  {/* Content */}
</Box>
```

**Spacing patterns:**
```typescript
// Standard tokens
<Box padding="md-1" margin="sm-2">

// Global namespace
<Box padding="global.sm-2" mt="global.md-1">

// Shorthand
<Box p="md-1" m="sm-2">

// Directional
<Box paddingX="sm-2" marginY="md-1">

// Individual sides
<Box pt="sm-2" pb="md-1" mt="lg-1" mb="zero">
```

## Example 4: Text Component

```typescript
import { Text } from '@/libs/zest';

<Text
  as="h2"
  fontSize="heading-3"
  fontWeight="heading-medium"
  color="neutral.800"
>
  Heading Text
</Text>

<Text
  as="p"
  fontSize="body-medium"
  fontWeight="body-regular"
  color="neutral.600"
>
  Body text
</Text>
```

## Example 5: Conditional Display

```typescript
<Box display={[
  shouldHideOnMobile ? 'none' : 'flex',
  'flex',
]}>
  {/* Hidden on mobile when condition is true */}
</Box>
```

## Summary

**Key Patterns:**
- `Box` for layouts with theme spacing tokens
- Responsive arrays: `[mobile, tablet, desktop]`
- Theme spacing: `sm-1`, `md-2`, `lg-1`
- `Text` for typography with design tokens
- `as` prop for semantic HTML
