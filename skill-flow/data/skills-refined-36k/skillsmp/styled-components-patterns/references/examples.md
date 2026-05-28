# Styled-Components - Production Examples

Real-world examples of styled-components v5.3.5 patterns from the web codebase.

## Example 1: Basic Styled Component with Theme

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:37`

```typescript
import styled from 'styled-components';
import { Theme } from '@emotion/react';

const EmptyBox = styled.div`
  height: 408px;
  width: 100%;
  border: double 2px transparent;
  background-origin: border-box;
  background-clip: content-box, border-box;

  ${({ theme }: { theme: Theme }) => `
    border-radius: ${theme.radii['border-radius-md']};
    background-image: linear-gradient(
      ${theme.colors.neutral['200']},
      ${theme.colors.neutral['200']}
    ),
    linear-gradient(
      to bottom,
      ${theme.colors.neutral['300']},
      transparent
    );
  `}
`;
```

**Key patterns:**
- Tagged template literal syntax
- Theme access via props: `${({ theme }) => ...}`
- Design tokens from theme: `theme.radii`, `theme.colors`
- Complex CSS (gradients, borders)

## Example 2: Simple Styled Element with Spacing

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/components/my-deliveries-components/src/sections/edit-menu/components/MealGrid/TitleArea.tsx:14`

```typescript
import styled from 'styled-components';

const Subtitle = styled.p`
  margin-top: ${({ theme }) => theme.space.xxs};
  margin-bottom: 0;
`;
```

**Key patterns:**
- Simple semantic HTML element (`<p>`)
- Theme spacing tokens: `theme.space.xxs`
- Minimal styling

## Example 3: Dynamic Props with TypeScript

**File**: Production pattern for prop-based styling

```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  disabled?: boolean;
}

const Button = styled.button<ButtonProps>`
  padding: ${({ size = 'md', theme }) => {
    const sizes = {
      sm: theme.space.xs,
      md: theme.space.sm,
      lg: theme.space.md,
    };
    return sizes[size];
  }};

  width: ${({ fullWidth }) => (fullWidth ? '100%' : 'auto')};

  background-color: ${({ variant, theme }) => {
    const colors = {
      primary: theme.colors.primary['500'],
      secondary: theme.colors.secondary['500'],
      danger: theme.colors.error['500'],
    };
    return colors[variant];
  }};

  opacity: ${({ disabled }) => (disabled ? 0.5 : 1)};
  cursor: ${({ disabled }) => (disabled ? 'not-allowed' : 'pointer')};

  &:hover:not(:disabled) {
    background-color: ${({ variant, theme }) => {
      const colors = {
        primary: theme.colors.primary['600'],
        secondary: theme.colors.secondary['600'],
        danger: theme.colors.error['600'],
      };
      return colors[variant];
    }};
  }
`;

// Usage
<Button variant="primary" size="lg" fullWidth>Submit</Button>
<Button variant="danger" disabled>Delete</Button>
```

**Key patterns:**
- TypeScript interface for props
- Generic type: `styled.button<ButtonProps>`
- Prop interpolation with destructuring
- Conditional styles based on props
- Hover state with `:hover:not(:disabled)`

## Example 4: Pseudo-Elements for Complex Icons

**File**: `app/spaces/landing-pages/modules/section-factory/sections/modular/SocialProofSection/CardItem.tsx:11`

```typescript
const SpeakerOffIcon = styled.div`
  vertical-align: middle;
  font-size: 1.5rem;
  box-sizing: border-box;
  display: inline-block;
  background: currentColor;
  background-clip: content-box;
  width: 1em;
  height: 1em;
  border: 0.333em solid transparent;
  border-right-color: currentColor;
  position: relative;
  left: -0.337em;

  &:before {
    content: '';
    width: 0.1em;
    position: absolute;
    height: 1.2em;
    margin-top: -0.333em;
    top: -0.1em;
    transform: translateX(0.333em) rotate(-45deg);
    background: #fff;
    left: 0.2em;
  }

  &:after {
    content: '';
    background: currentColor;
    width: 0.1em;
    position: absolute;
    height: 1.2em;
    margin-top: -0.333em;
    top: -0.1em;
    left: 0.1em;
    transform: translateX(0.333em) rotate(-45deg);
  }
`;
```

**Key patterns:**
- Pseudo-elements: `&:before`, `&:after`
- CSS icons without images
- em-based sizing for scalability
- Complex transforms

## Example 5: Integration with Zest

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:92`

```typescript
import { Box, Text } from '@/libs/zest';
import styled from 'styled-components';

const EmptyBox = styled.div`
  height: 408px;
  width: 100%;
  ${({ theme }) => `
    border-radius: ${theme.radii['border-radius-md']};
  `}
`;

export const EmptyMenu: React.FC = () => {
  return (
    <Box display="flex" flexDirection="column">
      <EmptyBox>
        <Box
          display="flex"
          flexDirection="column"
          justifyContent="center"
          alignItems="center"
          height="100%"
        >
          <Text fontSize="heading-3">No meals selected</Text>
          <Text fontSize="body-medium" color="neutral.600">
            Choose meals from the menu below
          </Text>
        </Box>
      </EmptyBox>
    </Box>
  );
};
```

**Key patterns:**
- Mix styled-components with Zest
- Use Zest for standard layouts (`Box`, `Text`)
- Use styled-components for custom UI (`EmptyBox`)
- Theme consistency across both

## Summary

**Common patterns:**
- Theme access: `${({ theme }) => theme.colors.primary['500']}`
- TypeScript props: `styled.button<ButtonProps>`
- Prop interpolation: `${({ variant }) => ...}`
- Pseudo-classes: `&:hover`, `&:focus`
- Pseudo-elements: `&:before`, `&:after`
- Integration with Zest for design system adherence
