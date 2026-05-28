# Frontend References

Internal documentation and resources for Pricing App frontend development.

## Architecture & Setup

- [Frontend README](../../../frontend/README.md) - Setup, build, and development workflow

## Design System

### CSS Modules & Design Tokens
- `frontend/src/styles/design-tokens.css` - Colors, spacing, shadows (theme-aware)
- `frontend/src/styles/theme.css` - Dark/light mode variables

### Tesla Components
- `frontend/src/styles/buttons-tesla.css` - Button variants (primary, secondary, danger)
- `frontend/src/styles/modals-tesla.css` - Modal styles
- `frontend/src/styles/table-tesla.css` - Table styles

## Key Patterns

### Contexts
- `frontend/src/contexts/ThemeContext.jsx` - Dark mode toggle + persistence
- `frontend/src/contexts/PermisosContext.jsx` - User permissions (role + overrides)

### Custom Hooks
- `frontend/src/hooks/useDebounce.js` - Debounce search inputs
- `frontend/src/hooks/usePermisos.js` - Permission checks
- `frontend/src/hooks/useServerPagination.js` - Server-side pagination
- `frontend/src/hooks/useKeyboardNavigation.js` - Arrow key navigation

### State Management
- `frontend/src/store/authStore.js` - Zustand auth store (user, token, logout)

### API Client
- `frontend/src/services/api.js` - Axios instance with interceptors

## Component Structure

```
src/
├── pages/           # Full page components (Productos, Ventas, Admin)
├── components/      # Reusable components
│   ├── turbo/       # Turbo delivery components
│   ├── ModalTesla.jsx
│   ├── PricingModal.jsx
│   └── ...
├── contexts/        # React contexts
├── hooks/           # Custom hooks
├── store/           # Zustand stores
└── styles/          # Global CSS + Tesla design
```

## Related Skills

- [`pricing-app-permissions`](../../pricing-app-permissions/SKILL.md) - Permission system (PermisosContext)
- [`react-19`](../../react-19/SKILL.md) - Generic React 19 patterns
- [`zustand-5`](../../zustand-5/SKILL.md) - Generic Zustand patterns
