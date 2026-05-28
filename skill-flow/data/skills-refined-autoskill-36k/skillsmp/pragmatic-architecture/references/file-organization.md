# File Organization Patterns

Concrete examples of colocated vs scattered code organization.

## Feature-Based vs Type-Based

### ❌ Type-Based (Scattered)

```
src/
├── components/
│   └── UserProfile.tsx
├── hooks/
│   └── useUser.ts
├── types/
│   └── user.ts
├── utils/
│   └── userHelpers.ts
├── constants/
│   └── userConstants.ts
└── services/
    └── userService.ts
```

Problems:
- 6 files for one feature
- Changes require navigating 6 directories
- Hard to see what belongs to "user"
- Easy to create orphaned files

### ✅ Feature-Based (Colocated)

```
src/
└── features/
    └── user/
        ├── UserProfile.tsx      # Component + hook + types
        ├── UserProfile.test.tsx # Tests colocated
        └── user-service.ts      # API + helpers
```

Benefits:
- 2-3 files for entire feature
- Everything in one place
- Easy to delete/move feature
- Clear ownership

## Component Organization

### ❌ Over-Split Component

```
Button/
├── Button.tsx
├── Button.types.ts
├── Button.styles.ts
├── Button.hooks.ts
├── Button.utils.ts
├── Button.constants.ts
├── Button.test.tsx
└── index.ts
```

8 files for a button. Each file likely under 30 lines.

### ✅ Colocated Component

```
Button/
├── Button.tsx        # Component, types, styles, small helpers inline
└── Button.test.tsx   # Tests
```

Everything in `Button.tsx`:

```tsx
// Types inline at top
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: ReactNode;
  onClick?: () => void;
}

// Constants inline if small
const SIZE_CLASSES = {
  sm: 'px-2 py-1 text-sm',
  md: 'px-4 py-2',
  lg: 'px-6 py-3 text-lg',
};

// Component
export function Button({ variant, size = 'md', children, onClick }: ButtonProps) {
  return (
    <button
      className={`${VARIANT_CLASSES[variant]} ${SIZE_CLASSES[size]}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

## When to Split Files

Split ONLY when:
- File exceeds ~300 lines of meaningful code
- Clear separation of concerns (not just "types go in types file")
- Multiple components that are truly independent
- Shared utilities used by 3+ unrelated features

## API/Service Organization

### ❌ Scattered API Layer

```
api/
├── client.ts
├── endpoints.ts
├── types.ts
├── interceptors.ts
├── transformers.ts
└── errors.ts
```

### ✅ Colocated API

```
api/
└── api-client.ts   # Everything in one file
```

Or feature-scoped:

```
features/
├── users/
│   └── users-api.ts    # User-specific API calls
├── orders/
│   └── orders-api.ts   # Order-specific API calls
└── shared/
    └── api-client.ts   # Only truly shared (auth, base config)
```

## State Management

### ❌ Centralized Everything

```
store/
├── index.ts
├── rootReducer.ts
├── users/
│   ├── userSlice.ts
│   ├── userSelectors.ts
│   ├── userActions.ts
│   └── userTypes.ts
└── orders/
    └── ...
```

### ✅ Colocated State

```
features/
└── users/
    └── UserProfile.tsx  # Uses local state or React Query
                         # Only lift to context/store when truly needed
```

## The File Count Test

For any new feature, count proposed files:

| Files | Assessment |
|-------|------------|
| 1-2 | Good - properly colocated |
| 3-4 | Acceptable - verify each is necessary |
| 5-6 | Warning - likely over-engineered |
| 7+ | Reject - split files, not features |

## Migration Path

If inheriting scattered codebase:

1. Don't scatter further
2. When touching a feature, consolidate its files
3. Gradually move toward feature-based structure
4. Delete empty type/utils/constants folders as they empty

## Naming Conventions

### ❌ Generic Names

```
utils.ts        # Utils for what?
helpers.ts      # Helps with what?
types.ts        # Types for what?
constants.ts    # Constants for what?
```

### ✅ Specific Names

```
user-profile.ts           # Clear domain
date-formatting.ts        # Clear purpose
api-client.ts             # Clear role
order-validation.ts       # Clear feature + purpose
```
