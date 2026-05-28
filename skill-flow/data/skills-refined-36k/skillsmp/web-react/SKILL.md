---
name: web-react
description: React patterns for vanilla React with Apollo Client - components, hooks, state management
user-invocable: false
---

# Web React Skill

**Version:** 1.0
**Stack:** React (vanilla) + Apollo Client

> React patterns optimized for Apollo-powered applications. No framework abstractions—just clean React.

---

## Core Principles

1. **Components Stay Small** — Under 200 lines. If larger, split it.
2. **Hooks for Logic** — Extract business logic into custom hooks.
3. **Apollo for Server State** — Don't duplicate server state in local state.
4. **Props Down, Events Up** — Clear data flow, no prop drilling beyond 2 levels.
5. **Colocation** — Keep related code together (component + styles + tests).

---

## Component Patterns

### File Size Guidelines

| Size | Status | Action |
|------|--------|--------|
| < 100 lines | ✅ Ideal | Keep it |
| 100-200 lines | ⚠️ Watch | Consider splitting if growing |
| > 200 lines | ❌ Too big | Split into smaller components |
| > 300 lines | 🚨 Critical | Immediate refactor needed |

### Component Structure

```jsx
// ✅ Good - Clear structure
function ProductCard({ product, onAddToCart }) {
  const [quantity, setQuantity] = useState(1);

  const handleAdd = () => {
    onAddToCart(product.id, quantity);
  };

  return (
    <article className="product-card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <div className="product-card__actions">
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(Number(e.target.value))}
          min={1}
        />
        <button onClick={handleAdd}>Add to Cart</button>
      </div>
    </article>
  );
}
```

### When to Split Components

Split when you see:
- Multiple responsibilities in one component
- Reusable UI patterns
- Complex conditional rendering
- Deeply nested JSX (> 4 levels)

```jsx
// ❌ Too much in one component
function ProductPage() {
  // 50 lines of hooks...
  // 100 lines of handlers...
  // 200 lines of JSX...
}

// ✅ Split by responsibility
function ProductPage() {
  return (
    <main>
      <ProductHeader />
      <ProductGallery />
      <ProductDetails />
      <ProductReviews />
      <RelatedProducts />
    </main>
  );
}
```

---

## Hooks Patterns

### Custom Hooks for Logic

Extract logic that:
- Uses multiple hooks together
- Contains business logic
- Could be reused
- Makes components hard to read

```jsx
// ✅ Good - Logic extracted to hook
function useProductQuantity(initialQuantity = 1) {
  const [quantity, setQuantity] = useState(initialQuantity);

  const increment = () => setQuantity(q => q + 1);
  const decrement = () => setQuantity(q => Math.max(1, q - 1));
  const reset = () => setQuantity(initialQuantity);

  return { quantity, setQuantity, increment, decrement, reset };
}

// Component stays clean
function QuantitySelector({ onChange }) {
  const { quantity, increment, decrement } = useProductQuantity();

  useEffect(() => {
    onChange(quantity);
  }, [quantity, onChange]);

  return (
    <div className="quantity-selector">
      <button onClick={decrement}>-</button>
      <span>{quantity}</span>
      <button onClick={increment}>+</button>
    </div>
  );
}
```

### Hook Rules (Enforced)

1. Only call hooks at the top level
2. Only call hooks from React functions
3. Custom hooks must start with `use`
4. Dependencies must be exhaustive (ESLint rule)

---

## Apollo Client Patterns

### Server State vs Local State

| Data Type | Where to Store | Example |
|-----------|---------------|---------|
| User data from API | Apollo cache | Profile, preferences |
| List data from API | Apollo cache | Products, orders |
| Form input before submit | Local state | Input values |
| UI state | Local state | Modal open, sidebar collapsed |
| Derived from server data | Computed | Filtered list, totals |

### Query Patterns

```jsx
// ✅ Good - Using Apollo hooks
function ProductList({ categoryId }) {
  const { data, loading, error } = useQuery(GET_PRODUCTS, {
    variables: { categoryId },
    // Stale-while-revalidate pattern
    fetchPolicy: 'cache-and-network',
  });

  if (loading && !data) return <ProductListSkeleton />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <ul className="product-list">
      {data.products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </ul>
  );
}
```

### Mutation Patterns

```jsx
// ✅ Good - Optimistic updates
function AddToCartButton({ productId }) {
  const [addToCart, { loading }] = useMutation(ADD_TO_CART, {
    variables: { productId },
    optimisticResponse: {
      addToCart: {
        __typename: 'CartItem',
        id: 'temp-id',
        productId,
        quantity: 1,
      },
    },
    update(cache, { data: { addToCart } }) {
      // Update cart cache
      cache.modify({
        fields: {
          cart(existingCart = []) {
            const newItemRef = cache.writeFragment({
              data: addToCart,
              fragment: CART_ITEM_FRAGMENT,
            });
            return [...existingCart, newItemRef];
          },
        },
      });
    },
  });

  return (
    <button onClick={() => addToCart()} disabled={loading}>
      {loading ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

### Don't Duplicate Server State

```jsx
// ❌ Bad - Duplicating Apollo data in local state
function ProductList() {
  const { data } = useQuery(GET_PRODUCTS);
  const [products, setProducts] = useState([]); // Why?

  useEffect(() => {
    if (data) setProducts(data.products); // Duplication!
  }, [data]);
}

// ✅ Good - Use Apollo cache directly
function ProductList() {
  const { data, loading } = useQuery(GET_PRODUCTS);

  // Filter/transform inline or with useMemo
  const activeProducts = useMemo(
    () => data?.products.filter(p => p.active) ?? [],
    [data]
  );
}
```

---

## State Management

### When to Use What

| Need | Solution |
|------|----------|
| Server data | Apollo Client (useQuery, useMutation) |
| Global UI state | React Context |
| Component UI state | useState |
| Complex component state | useReducer |
| Form state | useState or form library |

### Context Pattern (When Needed)

```jsx
// ✅ Good - Focused context for specific concern
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const toggle = useCallback(() => {
    setTheme(t => t === 'light' ? 'dark' : 'light');
  }, []);

  const value = useMemo(() => ({ theme, toggle }), [theme, toggle]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

### Avoid Context for Frequently Changing Data

```jsx
// ❌ Bad - Causes unnecessary re-renders
const AppContext = createContext();
// Contains: user, theme, cart, notifications, sidebar state...
// Every change re-renders everything!

// ✅ Good - Split by concern
const UserContext = createContext();
const ThemeContext = createContext();
const SidebarContext = createContext();
```

---

## File Organization

### Recommended Structure

```
src/
├── components/           # Shared/reusable components
│   ├── Button/
│   │   ├── Button.jsx
│   │   ├── Button.css
│   │   └── Button.test.jsx
│   └── Modal/
├── features/             # Feature-based organization
│   ├── products/
│   │   ├── components/   # Feature-specific components
│   │   ├── hooks/        # Feature-specific hooks
│   │   ├── graphql/      # Queries and mutations
│   │   └── ProductsPage.jsx
│   └── cart/
├── hooks/                # Shared custom hooks
├── graphql/              # Shared GraphQL (fragments, client setup)
├── utils/                # Pure utility functions
└── App.jsx
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `ProductCard.jsx` |
| Hooks | camelCase with `use` prefix | `useProductQuantity.js` |
| Utils | camelCase | `formatPrice.js` |
| GraphQL queries | SCREAMING_SNAKE | `GET_PRODUCTS` |
| GraphQL files | camelCase | `products.graphql` or `products.js` |

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Giant components** | Hard to read, test, maintain | Split by responsibility |
| **Prop drilling > 2 levels** | Tight coupling, verbose | Use composition or context |
| **useEffect for derived state** | Unnecessary renders | Use useMemo or compute inline |
| **Duplicating Apollo cache** | Double source of truth | Query directly from cache |
| **Business logic in components** | Hard to test, can't reuse | Extract to hooks |
| **Inline functions in JSX** | New reference each render | useCallback or extract |
| **Missing loading/error states** | Bad UX | Always handle all states |
| **Fetching in useEffect** | Race conditions, no caching | Use Apollo useQuery |

---

## Performance Checklist

- [ ] Components < 200 lines
- [ ] Heavy computations wrapped in useMemo
- [ ] Callbacks wrapped in useCallback when passed as props
- [ ] Lists have stable `key` props
- [ ] Large lists use virtualization
- [ ] Images lazy loaded
- [ ] Code split by route (React.lazy)

---

## When to Consider Alternatives

While this stack works well, consider alternatives when:

| Situation | Consider |
|-----------|----------|
| Need SSR/SSG | Next.js or Remix |
| Very simple app | Plain React without Apollo |
| Real-time heavy | Consider subscriptions or WebSockets |
| Complex forms | Form library (React Hook Form) |

---

## Quick Reference

### Import Order

```jsx
// 1. React
import React, { useState, useCallback } from 'react';

// 2. Third-party
import { useQuery, useMutation } from '@apollo/client';
import { format } from 'date-fns';

// 3. Internal modules
import { useAuth } from '@/hooks/useAuth';
import { GET_PRODUCTS } from '@/graphql/products';

// 4. Components
import { Button } from '@/components/Button';
import { ProductCard } from './ProductCard';

// 5. Styles
import './ProductList.css';
```
