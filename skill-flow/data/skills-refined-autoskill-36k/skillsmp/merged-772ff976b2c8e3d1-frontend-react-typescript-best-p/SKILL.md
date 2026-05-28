---
name: frontend-react-typescript-best-practices
description: Use this skill for implementing consistent and accessible UI components in React and TypeScript.
---

# Frontend React/TypeScript Best Practices Skill

## Overview

Provide implementation standards for consistent UI behavior using React and TypeScript.

## Usage

```
/frontend-react-typescript-best-practices
```

## Identity
**Role**: Frontend Lead  
**Objective**: Guide the implementation of React components and logic to ensure consistency, performance, and accessibility.

## Tech Stack
- **Framework**: React 18+
- **Language**: TypeScript
- **State Management**: TanStack Query (Server State), Zustand (Client State)
- **Styling**: Tailwind CSS or CSS Modules
- **Routing**: TanStack Router or React Router

## Rules

### 1. Component Structure
**Feature-based Folders**:
```
src/features/auth/
  ├── components/    # Dumb UI components
  ├── hooks/         # Custom hooks
  ├── api/           # Fetchers
  └── routes/        # Route definitions
```
**Generic UI**: `src/components/ui` (Buttons, Inputs).

### 2. Rendering & Effects
- **Data Fetching**: Use `useQuery` instead of `useEffect`.
- **State Management**: Avoid derived state in `useState`; calculate during render.
  - Bad: `const [fullName, setFullName] = useState(f + l)`
  - Good: `const fullName = firstName + " " + lastName`

### 3. Accessibility (A11y)
- **Semantic HTML**: Use `<button>` instead of `<div onClick>`.
- **Forms**: Labels are mandatory (`htmlFor`).
- **Interaction**: Ensure keyboard navigability.

## Workflow

### Feature Implementation
1. **Route**: Define the route.
2. **State**: Define data requirements (Zod Schemas).
3. **UI**: Build components (Mobile-First responsive).
4. **Integration**: Wire up `useQuery`.

## Error Handling
- **Boundaries**: Wrap features in `ErrorBoundary`.
- **Fallbacks**: Always include Loading and Error states in UI.

## Outputs

- Frontend implementation aligned with UI and accessibility standards.

## Related Skills

- `/ui-design-system` - Design system reference