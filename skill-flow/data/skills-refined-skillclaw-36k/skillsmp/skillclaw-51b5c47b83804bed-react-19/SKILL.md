---
name: react-19
description: Use this skill when writing React 19 components/hooks in .tsx, especially with new patterns and breaking changes from React 18.
---

# Skill body

## Key Changes in React 19

This skill focuses on the essential patterns and breaking changes introduced in React 19 compared to React 18. 

### Migration Path
- Upgrade to React 18.3 first to see deprecation warnings, then to React 19.

### React 19 Mindset
| Old Thinking | New Thinking |
|--------------|--------------|
| Client-side by default | **Server-first** (RSC default) |
| Manual memoization | **Compiler handles it** |
| `useEffect` for data | **async Server Components** |
| `useState` for forms | **Form Actions** |
| Loading state booleans | **Suspense boundaries** |
| Optimize everything | **Write correct code, compiler optimizes** |

### Key Features
| Feature | React 18 | React 19+ |
|---------|----------|-----------|
| Memoization | Manual (`useMemo`, `useCallback`, `memo`) | React Compiler (automatic) or manual |
| Forward refs | `forwardRef()` wrapper | `ref` as regular prop |
| Context provider | `<Context.Provider value={}>` | `<Context value={}>` |
| Form state | Custom with `useState` | `useActionState` hook |

## Best Practices

### No Manual Memoization (REQUIRED)
```typescript
// ✅ React Compiler handles optimization automatically
function Component({ items }) {
  const filtered = items.filter(x => x.active);
  const sorted = filtered.sort((a, b) => a.name.localeCompare(b.name));

  const handleClick = (id) => {
    console.log(id);
  };

  return <List items={sorted} onClick={handleClick} />;
}

// ❌ NEVER: Manual memoization
const filtered = useMemo(() => items.filter(x => x.active), [items]);
const handleClick = useCallback((id) => console.log(id), []);
```

### Imports (REQUIRED)
```typescript
// ✅ ALWAYS: Named imports
import { useState, useEffect, useRef } from "react";

// ❌ NEVER
import React from "react";
import * as React from "react";
```

### Server Components First
```typescript
// ✅ Server Component (default) - no directive
export default async function Page() {
  const data = await fetchData();
  return <ClientComponent data={data} />;
}

// ✅ Client Component - only when needed
"use client";
export function Interactive() {
  const [state, setState] = useState(false);
  return <button onClick={() => setState(!state)}>Toggle</button>;
}
```

### When to use "use client"
- useState, useEffect, useRef, useContext
- Event handlers (onClick, onChange)
- Browser APIs (window, localStorage)

### use() Hook
```typescript
import { use } from "react";

// Read promises (suspends until resolved)
function Comments({ promise }) {
  const comments = use(promise);
  return comments.map(c => <div key={c.id}>{c.text}</div>);
}

// Conditional context (not possible with useContext!)
function Theme({ showTheme }) {
  if (showTheme) {
    const theme = use(ThemeContext);
    return <div style={{ color: theme.primary }}>Themed</div>;
  }
  return <div>Plain</div>;
}
```

### Actions & useActionState
```typescript
"use server";
async function submitForm(formData: FormData) {
  await saveToDatabase(formData);
  revalidatePath("/");
}

// With pending state
import { useActionState } from "react";

function Form() {
  const [state, action] = useActionState();
  // Form implementation...
}
```