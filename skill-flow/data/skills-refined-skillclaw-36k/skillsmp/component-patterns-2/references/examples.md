# Component Patterns - Production Examples

Real-world examples of React component patterns from the web codebase demonstrating TypeScript, semantic HTML, and modern React practices.

## Example 1: Basic React.FC Component with Props

**File**: `app/unified-spaces/checkout-payment/components/PaymentAnxietyBanner/PaymentAnxietyBanner.tsx:8`

```typescript
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

**Key patterns:**
- Uses `React.FC` with explicit props interface
- Props interface named `ComponentNameProps` convention
- Destructured props in function parameter
- Optional prop (`cutoffDays?`)
- Conditional rendering with `&&` operator
- Fragment (`<>`) for wrapping without extra DOM nodes

**Anti-patterns to avoid:**
```typescript
// ❌ Generic Props interface name
interface Props { cutoffDays?: number; }

// ❌ Not destructuring props
export const PaymentAnxietyBanner: React.FC<PaymentAnxietyBannerProps> = (props) => {
  return <div>{props.cutoffDays}</div>;
};

// ❌ Not using React.FC
export function PaymentAnxietyBanner({ cutoffDays }: PaymentAnxietyBannerProps) {
  // Missing automatic children typing
}
```

## Example 2: Semantic HTML with Zest Box

**File**: `app/unified-spaces/registration-page/Qna/components/QnACard.tsx:42`

```typescript
import { Box } from '@/libs/zest';
import React from 'react';

interface QnAProps {
  icon: React.ReactNode;
  title: string;
  body: string;
}

export const QnA: React.FC<QnAProps> = ({ icon, title, body }) => {
  return (
    <Box display="flex" flexDirection="row">
      <Box as="h2" color="neutral.800" fontSize="heading-3" fontWeight="heading-medium">
        {title}
      </Box>
      <Box as="span" fontSize="body-medium" fontWeight="body-regular" color="neutral.600">
        {body}
      </Box>
    </Box>
  );
};
```

**Key patterns:**
- Uses semantic HTML via Zest `Box` component with `as` prop
- `as="h2"` renders a proper `<h2>` element for accessibility
- `as="span"` for inline text content
- Design tokens for colors and typography (`neutral.800`, `heading-3`)
- Clean separation of structure and styling

**Why semantic HTML matters:**
- Improves accessibility (screen readers understand heading hierarchy)
- Better SEO (search engines understand content structure)
- Native browser behaviors (h2 gets default heading styles)
- Keyboard navigation works correctly

## Example 3: Component with Children and Composition

**File**: `app/unified-spaces/components/Card/Card.tsx`

```typescript
import React from 'react';
import { Box } from '@/libs/zest';

interface CardProps {
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  variant?: 'default' | 'highlighted';
}

export const Card: React.FC<CardProps> = ({
  title,
  children,
  footer,
  variant = 'default',
}) => {
  return (
    <Box
      as="article"
      padding="lg"
      borderRadius="md"
      backgroundColor={variant === 'highlighted' ? 'primary.50' : 'white'}
      boxShadow="sm"
    >
      <Box as="h2" marginBottom="md">
        {title}
      </Box>
      <Box as="section">{children}</Box>
      {footer && <Box as="footer" marginTop="lg">{footer}</Box>}
    </Box>
  );
};

// Usage
<Card title="User Profile" footer={<Button>Edit</Button>}>
  <UserAvatar />
  <UserDetails />
</Card>
```

**Key patterns:**
- `children: React.ReactNode` for composable content
- Optional `footer` prop with conditional rendering
- Variant system using union type (`'default' | 'highlighted'`)
- Default prop value (`variant = 'default'`)
- Semantic elements: `article`, `h2`, `section`, `footer`
- Composition pattern allows flexible content

**Component composition benefits:**
- Reusable container logic
- Flexible content insertion
- Type-safe children
- Clean component API

## Example 4: Extending HTML Attributes

**File**: `app/unified-spaces/components/Button/Button.tsx`

```typescript
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  disabled,
  className,
  ...htmlProps
}) => {
  return (
    <button
      className={`btn-${variant} btn-${size} ${className || ''}`}
      disabled={disabled || isLoading}
      {...htmlProps}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
};

// Usage - supports all native button attributes
<Button
  variant="primary"
  size="lg"
  onClick={handleSubmit}
  type="submit"
  disabled={!isValid}
  aria-label="Submit form"
>
  Submit
</Button>
```

**Key patterns:**
- Extends `React.ButtonHTMLAttributes<HTMLButtonElement>` for native button props
- Custom props (`variant`, `size`, `isLoading`) merged with HTML attributes
- Spread remaining props (`...htmlProps`) to underlying element
- Type-safe access to all button attributes (onClick, disabled, type, etc.)
- Loading state with conditional rendering

**Benefits of extending HTML attributes:**
- Consumers can use all native HTML attributes
- TypeScript validates attribute types
- No need to manually type every HTML attribute
- Maintains native element behavior

## Example 5: Generic List Component

**File**: `app/unified-spaces/components/List/List.tsx`

```typescript
import React from 'react';
import { Box } from '@/libs/zest';

interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T, index: number) => string;
  emptyMessage?: string;
  loading?: boolean;
}

export function List<T>({
  items,
  renderItem,
  keyExtractor,
  emptyMessage = 'No items found',
  loading = false,
}: ListProps<T>) {
  if (loading) {
    return <Box>Loading...</Box>;
  }

  if (items.length === 0) {
    return <Box as="p" color="neutral.500">{emptyMessage}</Box>;
  }

  return (
    <Box as="ul" listStyleType="none" padding="0">
      {items.map((item, index) => (
        <Box as="li" key={keyExtractor(item, index)}>
          {renderItem(item, index)}
        </Box>
      ))}
    </Box>
  );
}

// Usage
interface User {
  id: string;
  name: string;
  email: string;
}

<List<User>
  items={users}
  renderItem={(user) => <UserCard user={user} />}
  keyExtractor={(user) => user.id}
  emptyMessage="No users found"
  loading={isLoading}
/>
```

**Key patterns:**
- Generic component with type parameter `<T>`
- Type-safe `items` array, `renderItem` function, and `keyExtractor`
- Render prop pattern for custom item rendering
- Loading and empty states
- Semantic `<ul>` and `<li>` elements
- Required `keyExtractor` for stable keys (better than index)

**Generic component benefits:**
- Reusable for any data type
- Type-safe item rendering
- No type casting needed
- IntelliSense support for item properties

## Example 6: Conditional Rendering Patterns

**File**: `app/unified-spaces/checkout-payment/components/CheckoutSummary/CheckoutSummary.tsx`

```typescript
import React from 'react';
import { Box } from '@/libs/zest';

interface CheckoutSummaryProps {
  subtotal: number;
  discount?: number;
  shipping: number;
  tax: number;
  showBreakdown?: boolean;
}

export const CheckoutSummary: React.FC<CheckoutSummaryProps> = ({
  subtotal,
  discount,
  shipping,
  tax,
  showBreakdown = true,
}) => {
  const total = subtotal - (discount || 0) + shipping + tax;

  // Early return pattern
  if (total <= 0) {
    return <Box>Invalid order total</Box>;
  }

  return (
    <Box as="section" aria-label="Order summary">
      <Box as="h2">Order Summary</Box>

      {/* Conditional with && */}
      {showBreakdown && (
        <Box>
          <div>Subtotal: ${subtotal}</div>
          {/* Conditional rendering of optional value */}
          {discount && <div>Discount: -${discount}</div>}
          <div>Shipping: ${shipping}</div>
          <div>Tax: ${tax}</div>
        </Box>
      )}

      {/* Ternary for if/else */}
      <Box fontWeight={total > 100 ? 'bold' : 'normal'}>
        Total: ${total}
      </Box>

      {/* Ternary with JSX */}
      {total > 50 ? (
        <Box color="green.600">Free shipping applied!</Box>
      ) : (
        <Box color="neutral.500">Add ${50 - total} for free shipping</Box>
      )}
    </Box>
  );
};
```

**Key patterns:**
- **Early return**: Exit early for invalid states
- **&& operator**: Render element only if condition is true
- **Ternary operator**: Choose between two render options
- **Optional prop**: `discount?` with nullish coalescing (`discount || 0`)
- **Conditional prop value**: `fontWeight={condition ? 'bold' : 'normal'}`

**Conditional rendering best practices:**
- Use early returns for error/loading states
- Use `&&` for simple show/hide
- Use ternary (`? :`) for if/else
- Avoid complex nested ternaries
- Extract complex conditionals into variables

## Example 7: Component with Event Handlers and TypeScript

**File**: `app/unified-spaces/components/SearchInput/SearchInput.tsx`

```typescript
import React, { useState, useCallback } from 'react';
import { Box } from '@/libs/zest';

interface SearchInputProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  onClear?: () => void;
  debounceMs?: number;
  minLength?: number;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  placeholder = 'Search...',
  onSearch,
  onClear,
  debounceMs = 300,
  minLength = 2,
}) => {
  const [query, setQuery] = useState('');

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setQuery(value);

      if (value.length >= minLength) {
        // Debounce search
        const timeoutId = setTimeout(() => {
          onSearch(value);
        }, debounceMs);
        return () => clearTimeout(timeoutId);
      }
    },
    [onSearch, debounceMs, minLength]
  );

  const handleClear = useCallback(() => {
    setQuery('');
    onClear?.();
  }, [onClear]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        onSearch(query);
      }
    },
    [onSearch, query]
  );

  return (
    <Box as="div" position="relative">
      <input
        type="text"
        placeholder={placeholder}
        value={query}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        aria-label="Search input"
      />
      {query && (
        <button
          onClick={handleClear}
          aria-label="Clear search"
          type="button"
        >
          ×
        </button>
      )}
    </Box>
  );
};
```

**Key patterns:**
- Typed event handlers: `React.ChangeEvent<HTMLInputElement>`, `React.KeyboardEvent<HTMLInputElement>`
- `useCallback` for memoized event handlers
- Optional callback with optional chaining: `onClear?.()`
- Controlled input with `value` and `onChange`
- Debouncing built into component logic
- Keyboard event handling (Enter key)
- Accessibility attributes (`aria-label`)

**Event handler TypeScript types:**
```typescript
React.ChangeEvent<HTMLInputElement>     // onChange
React.MouseEvent<HTMLButtonElement>     // onClick
React.KeyboardEvent<HTMLInputElement>   // onKeyDown, onKeyPress
React.FocusEvent<HTMLInputElement>      // onFocus, onBlur
React.FormEvent<HTMLFormElement>        // onSubmit
```

## Summary

These production examples demonstrate:

1. **React.FC with TypeScript**: Explicit props interfaces with `ComponentNameProps` naming
2. **Semantic HTML**: Using `Box as="h2"`, `as="button"` for accessibility and SEO
3. **Component Composition**: Children props and render patterns for flexible components
4. **Extending HTML Attributes**: Type-safe native element props with custom props
5. **Generic Components**: Reusable, type-safe components for any data type
6. **Conditional Rendering**: Early returns, && operator, ternary expressions
7. **Event Handlers**: Typed React events with useCallback for performance

**Common patterns across examples:**
- Always use `React.FC<Props>` with explicit interfaces
- Name props interfaces `ComponentNameProps`
- Destructure props in function parameters
- Use semantic HTML elements (`h1`, `button`, `nav`, etc.)
- Provide default values for optional props
- Type event handlers with React event types
- Use `useCallback` for event handlers passed to children
- Include accessibility attributes (`aria-label`, `role`, etc.)

**Anti-patterns to avoid:**
- Using React Native components (`View`, `Text`) in web code
- Generic `Props` interface names
- Not destructuring props (`props.name` instead of `{name}`)
- Missing TypeScript types on props or events
- Using `div` everywhere instead of semantic elements
- Forgetting `key` prop in lists (or using index as key)
- Complex nested ternaries in JSX
- Not memoizing callbacks passed to children
