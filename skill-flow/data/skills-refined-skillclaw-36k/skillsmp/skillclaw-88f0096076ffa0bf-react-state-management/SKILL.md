---
name: react-state-management
description: Use this skill when you need to master modern React state management techniques, including global state, server state, and choosing the right library for your application.
---

# Skill body

## Overview of State Management in React

This skill covers various state management patterns in React applications, focusing on libraries like Redux Toolkit, Zustand, Jotai, and React Query. It helps you understand when to use each type of state management based on your application's needs.

## State Types Overview

| Type             | Library                 | When to Use                 |
| ---------------- | ----------------------- | --------------------------- |
| **Local State**  | useState, useReducer    | Component-specific, UI state |
| **Global State** | Redux Toolkit, Zustand, Jotai | Shared across components     |
| **Server State** | React Query, SWR        | Remote data, caching         |
| **URL State**    | React Router, nuqs      | Route parameters, search     |
| **Form State**   | React Hook Form, Formik | Input values, validation     |

## Choosing the Right Library

- **Small app, simple state** → Zustand or Jotai
- **Large app, complex state** → Redux Toolkit
- **Heavy server interaction** → React Query + light client state
- **Atomic/granular updates** → Jotai

## Quick Start with Zustand

### Basic Store Setup

```typescript
// store/useStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AppState {
  user: User | null;
  theme: 'light' | 'dark';
  setUser: (user: User | null) => void;
  toggleTheme: () => void;
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () =>
          set((state) => ({
            theme: state.theme === 'light' ? 'dark' : 'light',
          })),
      }),
      { name: 'app-storage' }
    )
  )
);
```

### Using the Store in Components

```tsx
// components/Header.tsx
import { useStore } from '@/store/useStore';

function Header() {
  const { user, theme, toggleTheme } = useStore();
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  );
}
```

## Advanced Patterns

### Zustand with Middleware

You can enhance your Zustand store with middleware for debugging and persistence. For example, using `devtools` and `persist` allows you to track state changes and save state across sessions.

```typescript
// Example of Zustand with middleware
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

// Define your store and middleware here
```

## Conclusion

This skill provides a comprehensive guide to managing state in React applications, helping you choose the right tools and patterns for your specific use case.