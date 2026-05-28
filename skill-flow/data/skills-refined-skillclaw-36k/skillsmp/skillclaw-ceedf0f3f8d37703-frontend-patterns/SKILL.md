---
name: frontend-patterns
description: Use this skill when building web frontends, components, or client-side apps to apply best practices in component design, state management, performance, and accessibility.
---

# Frontend Patterns

This skill provides best practices and patterns for frontend development, supporting framework-specific loading as needed.

## Trigger Conditions

- Creating or modifying frontend components
- Designing UI/UX interactions
- Implementing state management
- Performance optimization
- Accessibility development

## Framework-Specific Patterns

Load the corresponding framework-specific files based on the project tech stack:

| Tech Stack | Load File   | Framework            |
|------------|-------------|----------------------|
| Vue        | `vue.md`    | Vue 3, Nuxt 3        |
| React      | `react.md`  | React 18, Next.js    |
| Svelte     | `svelte.md` | Svelte, SvelteKit    |
| Angular    | `angular.md`| Angular 17+          |

**Loading Method**: Detect the tech stack by checking the dependencies in `package.json`.

---

## General Component Patterns

### Component Classification

```
┌─────────────────────────────────────────────────────┐
│                    Component Pyramid                │
├─────────────────────────────────────────────────────┤
│  Page Components (Pages/Views)                      │
│  ├─ Responsible for routing and layout              │
│  ├─ Composes multiple functional components          │
│  └─ Manages page-level state                         │
├─────────────────────────────────────────────────────┤
│  Functional Components (Features/Containers)        │
│  ├─ Contains business logic                           │
│  ├─ Connects to state management                     │
│  └─ Calls APIs                                       │
├─────────────────────────────────────────────────────┤
│  UI Components (UI/Presentational)                  │
│  ├─ Purely presentational, no business logic        │
│  ├─ Receives data via props                          │
│  └─ Notifies parent components through events        │
├─────────────────────────────────────────────────────┤
│  Base Components (Base/Primitives)                  │
│  ├─ Button, Input, Card, etc.                       │
│  ├─ Highly reusable                                   │
│  └─ Foundation of design systems                      │
└─────────────────────────────────────────────────────┘
```

### Component Design Principles

| Principle         | Description                                   |
|-------------------|-----------------------------------------------|
| **Single Responsibility** | A component should do one thing only.   |
| **Props Down**    | Data flows from parent components to child components. |
| **Events Up**     | Events notify parent components from child components. |
| **Composition Over Inheritance** | Use slots/children to compose components. |
| **Predictable**   | Same props should produce the same output.  |

### Naming Conventions

```
components/
├── ui/                    # Base components (PascalCase)
│   ├── Button.vue/tsx
│   ├── Input.vue/tsx
│   └── Card.vue/tsx
├── feature/               # Functional components (PascalCase)
│   ├── UserCard.vue/tsx
│   └── OrderList.vue/tsx
└── layout/
```