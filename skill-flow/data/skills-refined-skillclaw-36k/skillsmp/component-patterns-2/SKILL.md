---
name: component-patterns
description: "WHAT: React web component patterns with TypeScript, semantic HTML, and composition. WHEN: building reusable components, type-safe APIs, accessible web interfaces. KEYWORDS: React.FC, TypeScript, props, semantic HTML, children, composition, Box, web, interface."
---

# Component Patterns - Web

React component patterns for web applications using TypeScript, semantic HTML, and modern React practices.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use these patterns for:
- Building reusable React components
- Creating type-safe component APIs
- Semantic HTML structure
- Accessible web interfaces
- Component composition

**Note:** These are web-specific patterns using HTML elements (div, button, h1), NOT React Native (View, Text).

## Core Principles

### 1. React.FC with TypeScript Props

**Define components using React.FC with explicit prop types.**

✅ **Good:**
```typescript
// app/unified-spaces/checkout-payment/components/PaymentAnxietyBanner/PaymentAnxietyBanner.tsx:8
import React from 'react';

interface PaymentAnxietyBannerProps {
  cutoffDays?: number;
}

export const PaymentAnxietyBanner: React.FC<PaymentAnxietyBannerProps> = ({
  cutoffDays,
}) => {
  return (
    <>
      {cutoffDays && (
        <div>
          <p>Payment will be charged {cutoffDays} days before delivery</p>
        </div>
      )}
    </>
  );
};
```

**Why:** React.FC provides automatic children typing and explicit prop interfaces improve type safety.

### 2. Props Interface Naming

**Name props interfaces with the component name + "Props" suffix.**

✅ **Good:**
```typescript
interface PaymentAnxietyBannerProps {
  cutoffDays?: number;
}

export const PaymentAnxietyBanner: React.FC<PaymentAnxietyBannerProps> = (props) => {
  // ...
};
```

❌ **Bad:**
```typescript
// Don't use generic names
interface Props {
  cutoffDays?: number;
}

// Don't omit the Props suffix
interface PaymentAnxietyBanner {
  cutoffDays?: number;
}
```

**Why:** Explicit naming prevents conflicts and makes the code self-documenting.

### 3. Semantic HTML Elements

**Use semantic HTML elements for accessibility and SEO.**

✅ **Good:**
```typescript
// app/unified-spaces/registration-page/Qna/components/QnACard.tsx:42
import { Box } from '@/libs/zest';

export const QnA: React.FC<QnAProps> = ({ icon, title, body }) => {
  return (
    <Box display="flex" flexDirection="row">
      <Box as="h2" color="neutral.800">
        {title}
      </Box>
      <Box as="span" fontWeight="body-regular">
        {body}
      </Box>
    </Box>
  );
};
```

**Common semantic elements:**
```typescript
<Box as="h1">Main Heading</Box>      // <h1>
<Box as="h2">Subheading</Box>        // <h2>
<Box as="p">Paragraph</Box>          // <p>
<Box as="button">Click</Box>         // <button>
<Box as="nav">Navigation</Box>       // <nav>
<Box as="article">Content</Box>      // <article>
<Box as="section">Section</Box>      // <section>
```

❌ **Bad:**
```typescript
// Don't use React Native components
import { View, Text } from 'react-native';

<View>
  <Text>Heading</Text>
</View>
```

**Why:** Semantic HTML improves accessibility, SEO, and browser compatibility.

### 4. Destructured Props

**Destructure props in the function parameter for cleaner code.**

✅ **Good:**
```typescript
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

export const UserCard: React.FC<UserCardProps> = ({ name, email, avatar }) => {
  return (
    <div>
      {avatar && <img src={avatar} alt={name} />}
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
};
```

❌ **Bad:**
```typescript
export const UserCard: React.FC<UserCardProps> = (props) => {
  return (
    <div>
      {props.avatar && <img src={props.avatar} alt={props.name} />}
      <h3>{props.name}</h3>
      <p>{props.email}</p>
    </div>
  );
};
```

**Why:** Destructuring reduces verbosity and makes the code more readable.

### 5. Optional Props with Defaults

**Use optional props with sensible defaults.**

✅ **Good:**
```typescript
interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = 'primary',
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`button-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
};
```

**Why:** Defaults make the component API easier to use and reduce boilerplate in consumers.

### 6. Conditional Rendering

**Use conditional rendering for optional content.**

✅ **Good:**
```typescript
// app/unified-spaces/checkout-payment/components/PaymentAnxietyBanner/PaymentAnxietyBanner.tsx:22
export const PaymentAnxietyBanner: React.FC<PaymentAnxietyBannerProps> = ({
  cutoffDays,
}) => {
  return (
    <>
      {cutoffDays && (
        <div>
          <p>Payment charged {cutoffDays} days before delivery</p>
        </div>
      )}
    </>
  );
};
```

**Conditional patterns:**
```typescript
// && for simple conditions
{isVisible && <div>Content</div>}

// Ternary for if/else
{isLoading ? <Spinner /> : <Content />}

// Early return for multiple conditions
if (!data) return null;
if (error) return <Error />;
return <Content />;
```

**Why:** Conditional rendering keeps components flexible and prevents rendering unnecessary DOM elements.

## Component Composition

### Children Props

```typescript
interface CardProps {
  children: React.ReactNode;
  title: string;
}

export const Card: React.FC<CardProps> = ({ children, title }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-content">{children}</div>
    </div>
  );
};

// Usage
<Card title="User Profile">
  <UserAvatar />
  <UserDetails />
</Card>
```

### Render Props

```typescript
interface DataFetcherProps {
  render: (data: any, loading: boolean) => React.ReactNode;
}

export const DataFetcher: React.FC<DataFetcherProps> = ({ render }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data...
  }, []);

  return <>{render(data, loading)}</>;
};

// Usage
<DataFetcher
  render={(data, loading) => (
    loading ? <Spinner /> : <UserCard user={data} />
  )}
/>
```

## TypeScript Patterns

### Union Types for Props

```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}
```

### Extending HTML Attributes

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  children,
  ...htmlProps
}) => {
  return (
    <button className={`btn-${variant}`} {...htmlProps}>
      {children}
    </button>
  );
};

// Usage (supports all button attributes)
<Button variant="primary" onClick={handleClick} disabled type="submit">
  Submit
</Button>
```

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

export function List<T>({ items, renderItem }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => <UserCard user={user} />}
/>
```

## File Organization

```
components/
├── PaymentAnxietyBanner/
│   ├── PaymentAnxietyBanner.tsx      # Component
│   ├── PaymentAnxietyBanner.spec.tsx # Tests
│   └── index.ts                      # Exports
└── UserCard/
    ├── UserCard.tsx
    ├── UserCard.styles.ts            # Styled-components
    └── index.ts
```

## Common Mistakes

1. **Using React Native components** - Use HTML elements, not View/Text
2. **Generic Props interface name** - Always use ComponentNameProps
3. **Not destructuring props** - Destructure for cleaner code
4. **Missing types** - Always type props explicitly
5. **Forgetting semantic HTML** - Use h1, button, nav, etc.
6. **Not using React.FC** - Provides better type inference

## Quick Reference

### Basic Component

```typescript
import React from 'react';

interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

export const UserCard: React.FC<UserCardProps> = ({ name, email, avatar }) => {
  return (
    <div data-testid="user-card">
      {avatar && <img src={avatar} alt={name} />}
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
};

export default UserCard;
```

### With Children

```typescript
interface CardProps {
  title: string;
  children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, children }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
};
```

### With Event Handlers

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false,
}) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};
```
