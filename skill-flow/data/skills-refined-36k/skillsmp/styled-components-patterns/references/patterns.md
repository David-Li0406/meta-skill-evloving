# Styled-Components Implementation Patterns

Implementation patterns and anti-patterns for styled-components v5.3.5.

## Pattern: Theme Access

Access theme tokens for consistent styling.

✅ **Good:**
```typescript
const Button = styled.button`
  background: ${({ theme }) => theme.colors.primary['500']};
  padding: ${({ theme }) => theme.space.md};
  border-radius: ${({ theme }) => theme.radii['border-radius-md']};
`;
```

❌ **Bad:**
```typescript
const Button = styled.button`
  background: #007bff; // Hard-coded color
  padding: 16px; // Hard-coded spacing
  border-radius: 8px; // Hard-coded radius
`;
```

**Why:** Theme tokens ensure consistency with design system.

## Pattern: TypeScript Props

Type props explicitly for type safety.

✅ **Good:**
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary';
  disabled?: boolean;
}

const Button = styled.button<ButtonProps>`
  background: ${({ variant, theme }) =>
    variant === 'primary' ? theme.colors.primary['500'] : theme.colors.secondary['500']};
  opacity: ${({ disabled }) => (disabled ? 0.5 : 1)};
`;
```

❌ **Bad:**
```typescript
const Button = styled.button`
  background: ${(props: any) => (props.variant === 'primary' ? 'blue' : 'gray')};
`;
```

**Why:** TypeScript prevents prop errors and provides autocomplete.

## Pattern: Integration with Zest

Mix styled-components with Zest for custom UI.

✅ **Good:**
```typescript
import { Box, Text } from '@/libs/zest';
import styled from 'styled-components';

const CustomCard = styled.div`
  border: 2px solid ${({ theme }) => theme.colors.neutral['300']};
`;

export const Card = () => (
  <Box padding="md">
    <CustomCard>
      <Text>Content</Text>
    </CustomCard>
  </Box>
);
```

**Why:** Use Zest for standard UI, styled-components for custom styling.

## Summary

**Key Patterns:**
- Access theme: `${({ theme }) => theme.colors...}`
- Type props: `styled.button<Props>`
- Use Zest for standard UI
- Use styled-components for custom styles
