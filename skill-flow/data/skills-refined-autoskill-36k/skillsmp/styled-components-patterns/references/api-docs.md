# Styled-Components - API Reference

**Version**: styled-components v5.3.5

## Official Documentation

- **Styled-Components**: https://styled-components.com/docs
- **API Reference**: https://styled-components.com/docs/api

## Basic API

### styled

Create a styled component.

```typescript
import styled from 'styled-components';

// Basic
const Button = styled.button`
  background: blue;
  color: white;
`;

// With TypeScript props
interface ButtonProps {
  variant: 'primary' | 'secondary';
}

const Button = styled.button<ButtonProps>`
  background: ${props => props.variant === 'primary' ? 'blue' : 'gray'};
`;
```

### Theme Access

```typescript
const Button = styled.button`
  background: ${({ theme }) => theme.colors.primary['500']};
  padding: ${({ theme }) => theme.space.md};
  border-radius: ${({ theme }) => theme.radii['border-radius-md']};
`;
```

### Props Interpolation

```typescript
const Button = styled.button<{ size: 'sm' | 'lg' }>`
  padding: ${({ size }) => (size === 'sm' ? '8px' : '16px')};
`;
```

### Pseudo-Classes

```typescript
const Button = styled.button`
  &:hover {
    background: blue;
  }

  &:focus {
    outline: 2px solid blue;
  }

  &:disabled {
    opacity: 0.5;
  }
`;
```

### Pseudo-Elements

```typescript
const Box = styled.div`
  &:before {
    content: '';
    display: block;
  }

  &:after {
    content: '→';
  }
`;
```

## Key Concepts

- **Tagged template literals**: `` styled.div` ` ``
- **Props access**: `${props => props.theme}`
- **TypeScript**: `styled.button<Props>`
- **Theme**: Access via `theme` prop
- **Nesting**: Use `&` for pseudo-classes/elements
