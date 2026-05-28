---
name: muebleria-react
description: >
  React 19 patterns for MuebleriaIris interactive components.
  Trigger: When writing React components with hooks, forms, or state management.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating React components"
    - "Using React hooks"
    - "Building forms with validation"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Creating interactive React components
- Using hooks (useState, useEffect, etc.)
- Building forms with validation
- Managing client-side state
- Fetching data from API

---

## Tech Stack

```
React 19.2.1 | TypeScript | React Hooks
No useMemo/useCallback (React Compiler handles)
```

---

## Critical Patterns

### Pattern 1: Component Structure

```tsx
// src/components/ui/ComponentName.tsx
import { useState, useEffect } from 'react';

interface ComponentNameProps {
  title: string;
  onAction: () => void;
}

export function ComponentName({ title, onAction }: ComponentNameProps) {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    // Side effects
  }, []);
  
  return <div>{title}</div>;
}
```

### Pattern 2: API Fetching

```tsx
import { useState, useEffect } from 'react';

export function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetch('http://localhost:5000/api/productos')
      .then(res => res.json())
      .then(data => {
        setProducts(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);
  
  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      {products.map(p => <ProductCard key={p.id} {...p} />)}
    </div>
  );
}
```

### Pattern 3: Form Handling

```tsx
import { useState } from 'react';

export function ProductForm() {
  const [formData, setFormData] = useState({
    nombre: '',
    precio: 0,
    material: ''
  });
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const response = await fetch('http://localhost:5000/api/productos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    
    if (response.ok) {
      alert('Producto creado');
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        value={formData.nombre}
        onChange={e => setFormData({...formData, nombre: e.target.value})}
      />
      <button type="submit">Crear</button>
    </form>
  );
}
```

---

## React 19 Features

### No useMemo/useCallback

React Compiler auto-optimizes:

```tsx
// ❌ OLD (React 18)
const filtered = useMemo(() => {
  return items.filter(i => i.active);
}, [items]);

// ✅ NEW (React 19)
const filtered = items.filter(i => i.active);
// Compiler memoizes automatically
```

### Server Components (with Astro)

```tsx
// Client component
"use client";
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

---

## Common Hooks

```tsx
// State
const [value, setValue] = useState(initialValue);

// Side effects
useEffect(() => {
  // Runs after render
  return () => {
    // Cleanup
  };
}, [dependencies]);

// Refs
const inputRef = useRef<HTMLInputElement>(null);

// Context
const theme = useContext(ThemeContext);
```

---

## TypeScript Integration

```tsx
// Props interface
interface ProductCardProps {
  id: number;
  nombre: string;
  precio: number;
  onSelect?: (id: number) => void;
}

// State with type
const [product, setProduct] = useState<Product | null>(null);

// Event handlers
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.currentTarget);
};
```

---

## Commands

```bash
# No specific React commands (handled by Astro/npm)
npm run dev    # Starts dev server with React support
```

---

## QA Checklist

- [ ] Components use TypeScript interfaces
- [ ] Loading states for async operations
- [ ] Error handling for API calls
- [ ] No useMemo/useCallback (React 19)
- [ ] Proper cleanup in useEffect
- [ ] Keys in list rendering
- [ ] Accessibility (ARIA, keyboard nav)

---

## Resources

- **React 19 Docs**: https://react.dev
- **Hooks Reference**: https://react.dev/reference/react
