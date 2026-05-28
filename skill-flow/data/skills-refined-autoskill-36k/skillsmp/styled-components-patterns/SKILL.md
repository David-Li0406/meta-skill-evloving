---
name: styled-components-patterns
description: "WHAT: styled-components v5.3.5 for CSS-in-JS with theme tokens and dynamic props. WHEN: custom styling beyond Zest, animations, conditional styles, integrating with Zest Box. KEYWORDS: styled-components, theme, css, props, keyframes, media query, TypeScript, web, tagged template."
---

# Styled-Components Patterns - Web

CSS-in-JS styling patterns using styled-components v5.3.5 for the React web application.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use styled-components for:
- Component-specific styling that doesn't exist in Zest
- Custom layouts and complex UI
- Dynamic styles based on props
- Theme-aware styling with access to design tokens
- Animations and transitions

**Prefer Zest Box/Text components for:**
- Standard layouts, spacing, typography
- Design system adherence
- Responsive design with breakpoints

## Core Principles

### 1. Basic Styled Component

**Create styled components with tagged template literals.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:37
import styled from 'styled-components';

const EmptyBox = styled.div`
  height: 408px;
  width: 100%;
  border: double 2px transparent;
  background-origin: border-box;
  background-clip: content-box, border-box;
`;
```

**Why:** Tagged template literals enable CSS syntax with JavaScript interpolation.

### 2. Theme Access

**Access theme tokens using props interpolation.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:43
import styled from 'styled-components';
import { Theme } from '@emotion/react';

const EmptyBox = styled.div`
  height: 408px;
  width: 100%;
  border: double 2px transparent;
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

**Why:** Theme tokens ensure consistency with design system and enable theming.

### 3. Simple Styled Elements

**Create simple styled elements for typography and spacing.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/components/my-deliveries-components/src/sections/edit-menu/components/MealGrid/TitleArea.tsx:14
import styled from 'styled-components';

const Subtitle = styled.p`
  margin-top: ${({ theme }) => theme.space.xxs};
  margin-bottom: 0;
`;
```

**Why:** Simple wrappers provide semantic HTML with consistent spacing from theme.

### 4. Pseudo-Elements and Pseudo-Classes

**Use CSS pseudo-elements and pseudo-classes for complex UI.**

✅ **Good:**
```typescript
// app/spaces/landing-pages/modules/section-factory/sections/modular/SocialProofSection/CardItem.tsx:11
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

**Why:** Pseudo-elements enable complex icons and decorations without extra DOM elements.

### 5. TypeScript Props with Transient Props Pattern

**Type props for styled components explicitly. Use `$` prefix for transient props to avoid DOM warnings.**

✅ **Good:**
```typescript
// app/spaces/landing-pages/modules/section-factory/sections/modular/RecipeMenuSection/components/ImageSlider.tsx
interface SlideContainerProps {
  $translateX: number;
  $animationDuration: number;
  $disableTransition?: boolean;
}

const SlideContainer = styled(Box)<SlideContainerProps>`
  display: flex;
  flex-direction: row;
  height: 100%;
  transform: translateX(${(props) => props.$translateX}px);
  transition: ${(props) =>
    props.$disableTransition
      ? 'none'
      : `transform ${props.$animationDuration}ms ease-in-out`};
`;

// Usage
<SlideContainer $translateX={-200} $animationDuration={300}>
  Content
</SlideContainer>
```

**Why:** The `$` prefix (transient props) prevents styled-components from passing these props to the DOM, avoiding React warnings. TypeScript ensures prop safety and provides autocomplete.

### 6. Integration with Zest

**Mix styled-components with Zest components when needed.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/my-deliveries/menus/EditMenuCollections/components/EmptyMenu.tsx:92
import { Box, Text } from '@/libs/zest';
import styled from 'styled-components';

const EmptyBox = styled.div`
  height: 408px;
  width: 100%;
  border-radius: ${({ theme }) => theme.radii['border-radius-md']};
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
          <Text mt="md-1">No meals selected</Text>
        </Box>
      </EmptyBox>
    </Box>
  );
};
```

**Why:** Use Zest for layout/spacing and styled-components for custom styling needs.

## Advanced Patterns

### Theme Access via useTheme Hook

**Access theme values programmatically with the useTheme hook.**

```typescript
// app/spaces/landing-pages/modules/section-factory/brand/utils/useLandingPagesGlobalStyles.ts
import { useMemo } from 'react';
import { ThemeSpecification, useTheme } from '@/libs/zest-support';

export const generateLandingPagesGlobalStyles = (
  theme: ThemeSpecification
): string => `
  html, body {
    background: ${theme.colors.neutral[100]};
    font-family: ${theme.fonts.primary};
    color: ${theme.colors.neutral[800]};
  }
`;

export const useLandingPagesGlobalStyles = (): string => {
  const theme = useTheme();
  return useMemo(() => generateLandingPagesGlobalStyles(theme), [theme]);
};
```

**Why:** useTheme provides access to theme values outside styled-components, useful for dynamic calculations.

### Using __dangerouslySetCustomCSS with Zest Box

**For cases where styled-components is overkill, use Zest Box's escape hatch.**

```typescript
// app/spaces/reactivate/modules/main/components/DiscountsAndBenefitsSection/components/PromoBoxDetails/BoxSlider/index.tsx
<Box
  // eslint-disable-next-line no-restricted-syntax
  __dangerouslySetCustomCSS={{
    scrollbarWidth: 'none', // Firefox
    '::-webkit-scrollbar': {
      display: 'none', // Safari and Chrome
    },
    WebkitOverflowScrolling: 'touch',
  }}
>
  {/* content */}
</Box>
```

**Why:** Use for simple one-off CSS that doesn't warrant a separate styled component.

### Conditional Styling

```typescript
const Card = styled.div<{ $isActive: boolean; $hasError?: boolean }>`
  padding: ${({ theme }) => theme.space['md-1']};
  border: 2px solid ${({ theme, $isActive, $hasError }) => {
    if ($hasError) return theme.colors.danger['500'];
    if ($isActive) return theme.colors.primary['500'];
    return theme.colors.neutral['300'];
  }};
  background-color: ${({ theme, $isActive }) =>
    $isActive ? theme.colors.primary['50'] : theme.colors.neutral['100']};
`;
```

### Extending Styled Components

```typescript
const BaseButton = styled.button`
  padding: ${({ theme }) => theme.space['sm-1']};
  border-radius: ${({ theme }) => theme.radii['border-radius-sm']};
  font-weight: bold;
  cursor: pointer;
`;

const PrimaryButton = styled(BaseButton)`
  background-color: ${({ theme }) => theme.colors.primary['500']};
  color: white;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primary['600']};
  }
`;

const SecondaryButton = styled(BaseButton)`
  background-color: transparent;
  border: 2px solid ${({ theme }) => theme.colors.primary['500']};
  color: ${({ theme }) => theme.colors.primary['500']};
`;
```

### Animations

```typescript
import styled, { keyframes } from 'styled-components';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const AnimatedCard = styled.div`
  animation: ${fadeIn} 0.6s ease;
  animation-delay: ${({ delay = 0 }: { delay?: number }) => `${delay}s`};
`;
```

### Media Queries

```typescript
const ResponsiveBox = styled.div`
  padding: ${({ theme }) => theme.space['sm-1']};

  @media (min-width: ${({ theme }) => theme.breakpoints.tablet}) {
    padding: ${({ theme }) => theme.space['md-1']};
  }

  @media (min-width: ${({ theme }) => theme.breakpoints.desktop}) {
    padding: ${({ theme }) => theme.space['lg-1']};
    max-width: 1200px;
    margin: 0 auto;
  }
`;
```

## Theme Structure

### Accessing Theme Properties

```typescript
const Component = styled.div`
  /* Colors */
  color: ${({ theme }) => theme.colors.neutral['800']};
  background-color: ${({ theme }) => theme.colors.primary['500']};

  /* Spacing */
  padding: ${({ theme }) => theme.space['md-1']};
  margin-top: ${({ theme }) => theme.space.xxs};

  /* Typography */
  font-size: ${({ theme }) => theme.fontSizes['body-md-regular']};
  line-height: ${({ theme }) => theme.lineHeights['line-height-md-1']};

  /* Radii */
  border-radius: ${({ theme }) => theme.radii['border-radius-md']};

  /* Shadows */
  box-shadow: ${({ theme }) => theme.shadows['shadow-sm']};

  /* Breakpoints */
  @media (min-width: ${({ theme }) => theme.breakpoints.tablet}) {
    /* Styles for tablet+ */
  }
`;
```

## File Organization

```
components/
└── MyComponent/
    ├── MyComponent.tsx       # Main component
    ├── MyComponent.styles.ts # Styled components
    └── index.ts              # Exports

// MyComponent.styles.ts
import styled from 'styled-components';

export const Container = styled.div`
  /* styles */
`;

export const Title = styled.h2`
  /* styles */
`;

export const Content = styled.div`
  /* styles */
`;

// MyComponent.tsx
import { Container, Title, Content } from './MyComponent.styles';

export const MyComponent = () => {
  return (
    <Container>
      <Title>Title</Title>
      <Content>Content</Content>
    </Container>
  );
};
```

## Common Mistakes

1. **Not using transient props** - Use `$` prefix for props that shouldn't be passed to DOM (`$isActive` not `isActive`)
2. **Not typing props** - Always add TypeScript types to styled components
3. **Hardcoding values** - Use theme tokens instead of magic numbers
4. **Overusing styled-components** - Prefer Zest components for standard layouts
5. **Missing theme parameter** - Always destructure `{ theme }` from props
6. **Not using semantic HTML** - Choose appropriate base elements (div, button, h1, etc.)
7. **Inline styles instead of styled-components** - Styled-components enable reusability
8. **Using styled-components when __dangerouslySetCustomCSS suffices** - For simple one-off CSS, use Box's escape hatch

## Quick Reference

### Basic Pattern

```typescript
import styled from 'styled-components';

const Button = styled.button`
  padding: ${({ theme }) => theme.space['sm-1']};
  background-color: ${({ theme }) => theme.colors.primary['500']};
  color: white;
  border-radius: ${({ theme }) => theme.radii['border-radius-sm']};
`;
```

### With Props

```typescript
interface CardProps {
  isActive: boolean;
}

const Card = styled.div<CardProps>`
  padding: ${({ theme }) => theme.space['md-1']};
  border: 2px solid ${({ theme, isActive }) =>
    isActive ? theme.colors.primary['500'] : theme.colors.neutral['300']};
`;
```

### Extending

```typescript
const BaseButton = styled.button`
  /* base styles */
`;

const PrimaryButton = styled(BaseButton)`
  /* additional styles */
`;
```

### Animation

```typescript
import styled, { keyframes } from 'styled-components';

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const Spinner = styled.div`
  animation: ${spin} 1s linear infinite;
`;
```

### With Zest

```typescript
import { Box } from '@/libs/zest';
import styled from 'styled-components';

const CustomBox = styled.div`
  /* custom styles */
`;

<Box display="flex">
  <CustomBox>Content</CustomBox>
</Box>
```
