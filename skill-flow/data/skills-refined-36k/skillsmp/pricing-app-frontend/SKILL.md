---
name: pricing-app-frontend
description: React frontend patterns for Pricing App - Zustand, CSS Modules, Tesla Design System, permissions
license: MIT
metadata:
  author: pricing-app
  version: "1.0.0"
  scope: [frontend, root]
  auto_invoke:
    - "Creating/modifying React components"
    - "Working with Zustand store"
    - "Styling with CSS Modules or Tesla Design"
    - "Implementing dark mode"
    - "Using PermisosContext or ThemeContext"
    - "Creating custom hooks"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Pricing App Frontend - React + Zustand + CSS Modules

---

## CRITICAL RULES - NON-NEGOTIABLE

### React Imports
- ALWAYS: `import { useState, useEffect } from 'react'`
- NEVER: `import React from 'react'` or `import * as React`

### Components
- ALWAYS: Functional components with hooks
- ALWAYS: Named imports for hooks
- ALWAYS: Prop destructuring: `function Button({ label, onClick })`
- NEVER: Class components
- NEVER: Default export for multiple components in same file

### State Management
- ALWAYS: Zustand for global state (auth)
- ALWAYS: React Context for theme, permissions
- ALWAYS: Local state for component-specific data
- NEVER: Lift state unnecessarily

### Styling
- ALWAYS: CSS Modules for component styles: `import styles from './Component.module.css'`
- ALWAYS: Design tokens from `design-tokens.css`: `var(--bg-primary)`, `var(--text-primary)`
- ALWAYS: Tesla components when available (`buttons-tesla.css`, `modals-tesla.css`, `table-tesla.css`)
- NEVER: Inline styles (except dynamic values)
- NEVER: Hardcoded colors (use design tokens)
- NEVER: Tailwind utilities (project uses CSS Modules)

### API Calls
- ALWAYS: Use axios from `services/api.js`
- ALWAYS: Check token before API calls: `localStorage.getItem('token')`
- ALWAYS: Handle loading states
- ALWAYS: Show user feedback on errors
- NEVER: Fetch without error handling

### Accessibility
- ALWAYS: Alt text on images: `<img src="logo.png" alt="Company logo" />`
- ALWAYS: Semantic HTML: `<button>` not `<div onClick>`
- ALWAYS: ARIA labels for icon-only buttons: `<button aria-label="Close modal">`

---

## PROJECT STRUCTURE

```
frontend/src/
├── pages/                 # Full page components
│   ├── Productos.jsx
│   ├── Ventas.jsx
│   └── Admin.jsx
├── components/            # Reusable components
│   ├── ModalTesla.jsx
│   ├── PricingModal.jsx
│   ├── Navbar.jsx
│   └── turbo/             # Domain-specific components
├── contexts/              # React contexts
│   ├── ThemeContext.jsx   # Dark mode
│   └── PermisosContext.jsx # User permissions
├── hooks/                 # Custom hooks
│   ├── useDebounce.js
│   ├── usePermisos.js
│   └── useServerPagination.js
├── store/                 # Zustand stores
│   └── authStore.js       # Auth state
├── services/              # API client
│   └── api.js             # Axios instance
└── styles/                # Global CSS, design tokens
    ├── design-tokens.css
    ├── buttons-tesla.css
    ├── modals-tesla.css
    └── table-tesla.css
```

---

## PATTERNS

### Functional Component with Hooks

```jsx
import { useState, useEffect } from 'react';
import styles from './ProductosList.module.css';

export default function ProductosList({ onSelect }) {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProductos();
  }, []);

  const fetchProductos = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/productos');
      const data = await response.json();
      setProductos(data);
    } catch (err) {
      setError('Error al cargar productos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className={styles.loading}>Cargando...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.container}>
      {productos.map(p => (
        <div key={p.id} onClick={() => onSelect(p)}>
          {p.descripcion}
        </div>
      ))}
    </div>
  );
}
```

### Using Zustand Store

```jsx
import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  
  setUser: (user) => set({ user }),
  
  setToken: (token) => {
    localStorage.setItem('token', token);
    set({ token });
  },
  
  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, token: null });
  }
}));

// Usage in component
import { useAuthStore } from '@/store/authStore';

function Navbar() {
  const { user, logout } = useAuthStore();
  
  return (
    <nav>
      <span>{user?.nombre}</span>
      <button onClick={logout}>Salir</button>
    </nav>
  );
}
```

### Using Context (Permissions)

```jsx
import { createContext, useContext, useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';

const PermisosContext = createContext();

export function PermisosProvider({ children }) {
  const { user } = useAuthStore();
  const [permisos, setPermisos] = useState([]);

  useEffect(() => {
    if (user?.roles) {
      // Calculate permissions from roles
      const allPermisos = user.roles.flatMap(role => 
        PERMISOS_CATEGORIAS[role] || []
      );
      setPermisos([...new Set(allPermisos)]);
    }
  }, [user]);

  const tienePermiso = (categoria) => permisos.includes(categoria);

  return (
    <PermisosContext.Provider value={{ permisos, tienePermiso }}>
      {children}
    </PermisosContext.Provider>
  );
}

export const usePermisos = () => useContext(PermisosContext);

// Usage in component
function AdminPanel() {
  const { tienePermiso } = usePermisos();

  if (!tienePermiso('config')) {
    return <div>No tienes permiso</div>;
  }

  return <div>Panel de Admin</div>;
}
```

### CSS Modules with Design Tokens

```css
/* ProductosList.module.css */
.container {
  background: var(--bg-primary);
  color: var(--text-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.loading {
  color: var(--text-secondary);
  text-align: center;
  padding: var(--spacing-lg);
}

.error {
  background: var(--error-bg);
  color: var(--error-text);
  padding: var(--spacing-sm);
  border-radius: var(--radius-sm);
}

/* Dark mode support (automatic via design tokens) */
```

### Tesla Button Component

```jsx
import styles from './Button.module.css';

export default function Button({ 
  label, 
  onClick, 
  variant = 'primary', 
  disabled = false 
}) {
  return (
    <button 
      className={`${styles.btnBase} ${styles[`btn${variant.charAt(0).toUpperCase() + variant.slice(1)}`]}`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
}
```

```css
/* Button.module.css */
.btnBase {
  composes: btn-base from '../../styles/buttons-tesla.css';
}

.btnPrimary {
  composes: btn-primary from '../../styles/buttons-tesla.css';
}

.btnSecondary {
  composes: btn-secondary from '../../styles/buttons-tesla.css';
}
```

### Custom Hook

```js
// hooks/useDebounce.js
import { useState, useEffect } from 'react';

export function useDebounce(value, delay = 500) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchBar() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      fetchResults(debouncedQuery);
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

---

## NAMING CONVENTIONS

| Entity | Pattern | Example |
|--------|---------|---------|
| Component file | `PascalCase.jsx` | `ProductosList.jsx` |
| Hook file | `camelCase.js` | `useDebounce.js` |
| Utility file | `camelCase.js` | `formatCurrency.js` |
| CSS Module | `PascalCase.module.css` | `ProductosList.module.css` |
| CSS class | `camelCase` | `.btnPrimary`, `.modalHeader` |

---

## COMMON PITFALLS

### Frontend
- ❌ Don't use `useEffect` without dependencies array → Will cause infinite loops
- ❌ Don't mutate state directly → Use setState functions
- ❌ Don't forget to cleanup effects → Clear timers, unsubscribe
- ❌ Don't store sensitive data in localStorage → Only JWT token
- ❌ Don't use inline styles → Use CSS Modules with design tokens
- ❌ Don't hardcode colors → Use `var(--color-name)`

---

## COMMANDS

```bash
# Development
cd frontend
npm install
npm run dev

# Build
npm run build
npm run preview

# Linting
npm run lint
```

---

## QA CHECKLIST

- [ ] Components use functional syntax with hooks
- [ ] No `import React` statements
- [ ] Proper error handling on API calls
- [ ] Loading states shown to user
- [ ] CSS Modules used (no inline styles)
- [ ] Design tokens used (no hardcoded colors)
- [ ] Dark mode works (test ThemeContext)
- [ ] Permissions checked where needed
- [ ] Alt text on images
- [ ] Semantic HTML used

---

## REFERENCES

### External
- React docs: https://react.dev
- Zustand docs: https://zustand-demo.pmnd.rs

### Internal
- [Frontend References](references/README.md) - Links to all internal docs
- Design tokens: [design-tokens.css](../../frontend/src/styles/design-tokens.css)
- Tesla buttons: [buttons-tesla.css](../../frontend/src/styles/buttons-tesla.css)
- Tesla modals: [modals-tesla.css](../../frontend/src/styles/modals-tesla.css)
- Tesla tables: [table-tesla.css](../../frontend/src/styles/table-tesla.css)
- ThemeContext: [ThemeContext.jsx](../../frontend/src/contexts/ThemeContext.jsx)
- PermisosContext: [PermisosContext.jsx](../../frontend/src/contexts/PermisosContext.jsx)
