---
name: typescript-rules
description: Use this skill when implementing React components or TypeScript code to ensure type safety, effective component design, and proper state management.
---

# TypeScript Development Rules (Frontend)

## Basic Principles

✅ **Aggressive Refactoring** - Prevent technical debt and maintain code health.  
❌ **Unused "Just in Case" Code** - Violates the YAGNI principle (Kent Beck).

## Comment Writing Rules
- **Function Description Focus**: Describe what the code "does".
- **No Historical Information**: Do not record development history.
- **Timeless**: Write only content that remains valid whenever read.
- **Conciseness**: Keep explanations to a necessary minimum.

## Type Safety

**Absolute Rule**: The `any` type is completely prohibited. It disables type checking and becomes a source of runtime errors.

**Alternatives to `any` (Priority Order)**:
1. **unknown Type + Type Guards**: Use for validating external input (API responses, localStorage, URL parameters).
2. **Generics**: When type flexibility is needed.
3. **Union Types / Intersection Types**: Combinations of multiple types.
4. **Type Assertions (Last Resort)**: Only when the type is certain.

**Type Guard Implementation Pattern**:
```typescript
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value && 'name' in value;
}
```

**Modern Type Features**:
- **satisfies Operator**: `const config = { apiUrl: '/api' } satisfies Config` - Preserves inference.
- **const Assertion**: `const ROUTES = { HOME: '/' } as const satisfies Routes` - Immutable and type-safe.
- **Branded Types**: `type UserId = string & { __brand: 'UserId' }` - Distinguish meaning.
- **Template Literal Types**: `type EventName = \`on\${Capitalize<string>}\`` - Express string patterns with types.

## Type Safety in Frontend Implementation
- **React Props/State**: TypeScript manages types; `unknown` is unnecessary.
- **External API Responses**: Always receive as `unknown`, validate with type guards.
- **localStorage/sessionStorage**: Treat as `unknown`, validate.
- **URL Parameters**: Treat as `unknown`, validate.
- **Form Input (Controlled Components)**: Type-safe with React synthetic events.

## Type Safety in Data Flow
- **Frontend → Backend**: Props/State (Type Guaranteed) → API Request (Serialization).
- **Backend → Frontend**: API Response (`unknown`) → Type Guard → State (Type Guaranteed).

## Type Complexity Management
- **Props Design**: Ensure props are well-defined and type-safe to prevent runtime errors.
- **State Management**: Use appropriate types for state to maintain consistency and reliability.