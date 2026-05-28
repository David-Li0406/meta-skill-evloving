---
name: frontend-dev
description: Develop frontend features for the Claude Assistant Platform following established patterns. Use when implementing UI components, creating pages, adding stores, or when the user says "build UI", "add component", "frontend feature", or "create page".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Frontend Development

This skill guides frontend development following the established patterns, tech stack, and best practices for the Claude Assistant Platform.

## Tech Stack Reference

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 15 | React framework (App Router) |
| React | 18.3 | UI library |
| TypeScript | 5.6 | Type safety |
| Zustand | 5.0 | State management |
| Tailwind CSS | 3.4 | Utility-first styling |
| DaisyUI | 4.12 | Component library |

## Before You Start

### 1. Understand the Request

Determine what type of work is needed:
- **New Page**: Route under `Frontend/src/app/`
- **New Component**: Reusable UI in `Frontend/src/components/`
- **New Store**: State management in `Frontend/src/stores/`
- **API Integration**: API client in `Frontend/src/lib/api/`
- **Modification**: Enhancing existing code

### 2. Check Existing Patterns

Read these files to understand current patterns:
- `Frontend/src/components/ChatContainer.tsx` - Component structure
- `Frontend/src/stores/chatStore.ts` - Zustand store pattern
- `Frontend/src/app/layout.tsx` - App router layout
- `.claude/rules/frontend/nextjs.md` - Next.js rules
- `.claude/rules/frontend/react-components.md` - Component rules

---

## Creating a New Component

### Step 1: Create Component File

Location: `Frontend/src/components/{ComponentName}.tsx`

```tsx
"use client"; // Only if using hooks, events, or browser APIs

import { useState, useCallback } from "react";

/**
 * Props for the ComponentName component.
 */
interface ComponentNameProps {
  /** Description of this prop */
  propName: string;
  /** Optional prop with default */
  optional?: boolean;
  /** Event handler prop */
  onAction?: (value: string) => void;
}

/**
 * Brief description of what this component does.
 *
 * @example
 * <ComponentName propName="value" onAction={handleAction} />
 */
export function ComponentName({
  propName,
  optional = false,
  onAction,
}: ComponentNameProps): JSX.Element {
  // Implementation
  return (
    <div className="...">
      {/* Content */}
    </div>
  );
}
```

### Step 2: Export from Index

Add to `Frontend/src/components/index.ts`:

```tsx
export { ComponentName } from "./ComponentName";
```

### Component Checklist

- [ ] `"use client"` only if needed (hooks, events, browser APIs)
- [ ] Props interface with JSDoc comments
- [ ] Component function with JSDoc and `@example`
- [ ] Explicit return type (`: JSX.Element`)
- [ ] DaisyUI classes for styling
- [ ] Exported from `index.ts`

---

## Creating a New Page

### Step 1: Create Page Directory

Location: `Frontend/src/app/{route-name}/page.tsx`

```tsx
// Server Component (default) - no "use client" needed
import { SomeComponent } from "@/components";

/**
 * Page metadata for SEO.
 */
export const metadata = {
  title: "Page Title | Claude Assistant",
  description: "Page description",
};

/**
 * Page component for the /route-name route.
 */
export default function PageName(): JSX.Element {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Page Title</h1>
      <SomeComponent />
    </main>
  );
}
```

### Step 2: Create Layout (if needed)

Location: `Frontend/src/app/{route-name}/layout.tsx`

```tsx
interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps): JSX.Element {
  return (
    <div className="flex h-screen">
      {/* Sidebar or other persistent elements */}
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

### Page Checklist

- [ ] Page is Server Component by default
- [ ] Metadata exported for SEO
- [ ] Semantic HTML structure
- [ ] Responsive layout with Tailwind

---

## Creating a Zustand Store

### Step 1: Create Store File

Location: `Frontend/src/stores/{storeName}Store.ts`

```tsx
/**
 * State management for {feature}.
 *
 * Manages {describe what state this manages}.
 */

import { create } from "zustand";
import { persist } from "zustand/middleware"; // Optional: for persistence

/**
 * Represents a single item in the store.
 */
interface Item {
  id: string;
  name: string;
  // ... other fields
}

/**
 * Store state interface.
 */
interface StoreState {
  // State
  items: Item[];
  selectedId: string | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setItems: (items: Item[]) => void;
  addItem: (item: Item) => void;
  selectItem: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

/**
 * Initial state values.
 */
const initialState = {
  items: [],
  selectedId: null,
  isLoading: false,
  error: null,
};

/**
 * Zustand store for {feature} state.
 */
export const useStoreNameStore = create<StoreState>()(
  persist(
    (set, get) => ({
      ...initialState,

      setItems: (items) => set({ items }),

      addItem: (item) =>
        set((state) => ({ items: [...state.items, item] })),

      selectItem: (id) => set({ selectedId: id }),

      setLoading: (isLoading) => set({ isLoading }),

      setError: (error) => set({ error }),

      reset: () => set(initialState),
    }),
    {
      name: "claude-assistant-{feature}", // localStorage key
      partialize: (state) => ({
        items: state.items, // Only persist what's needed
      }),
    }
  )
);
```

### Step 2: Use in Components

```tsx
import { useStoreNameStore } from "@/stores/storeNameStore";

function Component(): JSX.Element {
  // Select only what you need (prevents unnecessary re-renders)
  const items = useStoreNameStore((state) => state.items);
  const isLoading = useStoreNameStore((state) => state.isLoading);
  const addItem = useStoreNameStore((state) => state.addItem);

  return (/* ... */);
}
```

### Store Checklist

- [ ] Interfaces for all state shapes
- [ ] JSDoc documentation
- [ ] Initial state defined separately
- [ ] Persist middleware if state should survive refresh
- [ ] Partialize to persist only necessary state
- [ ] Actions are pure and predictable

---

## Creating an API Client

### Step 1: Create API Module

Location: `Frontend/src/lib/api/{resource}.ts`

```tsx
/**
 * API client for {resource} operations.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Response type from the API.
 */
interface ResourceResponse {
  id: string;
  name: string;
  // ... fields matching backend response
}

/**
 * Request type for creating a resource.
 */
interface CreateResourceRequest {
  name: string;
  // ... fields
}

/**
 * Fetch all resources with optional filters.
 *
 * @param filters - Optional query parameters
 * @returns Array of resources
 * @throws Error if request fails
 */
export async function getResources(
  filters?: Record<string, string>
): Promise<ResourceResponse[]> {
  const params = new URLSearchParams(filters);
  const url = `${API_URL}/api/resources${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Failed to fetch resources: ${response.status}`);
  }

  return response.json();
}

/**
 * Create a new resource.
 *
 * @param data - Resource data to create
 * @returns Created resource
 * @throws Error if request fails
 */
export async function createResource(
  data: CreateResourceRequest
): Promise<ResourceResponse> {
  const response = await fetch(`${API_URL}/api/resources`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Failed to create resource: ${response.status}`);
  }

  return response.json();
}

/**
 * Update an existing resource.
 *
 * @param id - Resource ID
 * @param data - Fields to update
 * @returns Updated resource
 * @throws Error if request fails
 */
export async function updateResource(
  id: string,
  data: Partial<CreateResourceRequest>
): Promise<ResourceResponse> {
  const response = await fetch(`${API_URL}/api/resources/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Failed to update resource: ${response.status}`);
  }

  return response.json();
}

/**
 * Delete a resource.
 *
 * @param id - Resource ID to delete
 * @throws Error if request fails
 */
export async function deleteResource(id: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/resources/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Failed to delete resource: ${response.status}`);
  }
}
```

### API Client Checklist

- [ ] Uses `NEXT_PUBLIC_API_URL` environment variable
- [ ] Type definitions for request/response
- [ ] JSDoc with `@param`, `@returns`, `@throws`
- [ ] Consistent error handling
- [ ] No hardcoded URLs

---

## DaisyUI Component Quick Reference

### Buttons
```tsx
<button className="btn">Default</button>
<button className="btn btn-primary">Primary</button>
<button className="btn btn-secondary">Secondary</button>
<button className="btn btn-ghost">Ghost</button>
<button className="btn btn-sm">Small</button>
<button className="btn btn-lg">Large</button>
<button className="btn loading">Loading</button>
```

### Inputs
```tsx
<input type="text" className="input input-bordered w-full" placeholder="Text" />
<input type="text" className="input input-primary" />
<textarea className="textarea textarea-bordered" rows={3} />
<select className="select select-bordered">
  <option>Option 1</option>
</select>
```

### Cards
```tsx
<div className="card bg-base-100 shadow-xl">
  <div className="card-body">
    <h2 className="card-title">Title</h2>
    <p>Content</p>
    <div className="card-actions justify-end">
      <button className="btn btn-primary">Action</button>
    </div>
  </div>
</div>
```

### Alerts
```tsx
<div className="alert alert-info">Info message</div>
<div className="alert alert-success">Success!</div>
<div className="alert alert-warning">Warning</div>
<div className="alert alert-error">Error</div>
```

### Loading States
```tsx
<span className="loading loading-spinner loading-sm" />
<span className="loading loading-dots loading-md" />
<span className="loading loading-ring loading-lg" />
```

### Badges
```tsx
<span className="badge">Default</span>
<span className="badge badge-primary">Primary</span>
<span className="badge badge-secondary">Secondary</span>
<span className="badge badge-outline">Outline</span>
```

### Modals
```tsx
<dialog id="my_modal" className="modal">
  <div className="modal-box">
    <h3 className="font-bold text-lg">Title</h3>
    <p className="py-4">Content</p>
    <div className="modal-action">
      <form method="dialog">
        <button className="btn">Close</button>
      </form>
    </div>
  </div>
</dialog>
```

---

## Common Patterns

### Conditional Rendering
```tsx
{isLoading ? (
  <span className="loading loading-spinner" />
) : (
  <Content />
)}

{error && <div className="alert alert-error">{error}</div>}

{items.length === 0 && <EmptyState />}
```

### Event Handlers
```tsx
// Simple handler
const handleClick = () => {
  doSomething();
};

// With useCallback (when passed to children)
const handleSubmit = useCallback((e: React.FormEvent) => {
  e.preventDefault();
  onSubmit(value);
}, [value, onSubmit]);
```

### Form State
```tsx
const [formData, setFormData] = useState({
  name: "",
  email: "",
});

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setFormData((prev) => ({
    ...prev,
    [e.target.name]: e.target.value,
  }));
};
```

---

## Anti-Patterns to Avoid

- **DON'T** use `any` type - define proper interfaces
- **DON'T** add `"use client"` without needing client features
- **DON'T** subscribe to entire Zustand store - use selectors
- **DON'T** hardcode API URLs - use environment variables
- **DON'T** use inline styles - use Tailwind classes
- **DON'T** skip TypeScript interfaces for props
- **DON'T** use `useEffect` for data fetching in client components
- **DON'T** create multiple components per file
- **DON'T** use anonymous functions for performance-critical handlers

---

## Running Applications

### Standard Ports

| Application | Port | Directory | Command |
|-------------|------|-----------|---------|
| Frontend | 3000 | `Frontend/` | `make run` |
| Backend | 8000 | `Backend/` | `make run` |

### Check If Already Running

**IMPORTANT**: Applications are often already running in PowerShell terminals. Always check before starting new instances to avoid port conflicts.

```powershell
# Check if frontend is running on port 3000
Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue

# Check if backend is running on port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
```

### Starting Applications

If applications are not running:

```powershell
# Start Backend (port 8000)
cd Backend
make run

# Start Frontend (port 3000) - in separate terminal
cd Frontend
make run
```

### Hot Reload Port Changes

**CRITICAL**: Next.js hot reload may spawn new server instances on different ports if port 3000 is blocked.

```powershell
# If port 3000 is in use by another process, Next.js will use 3001, 3002, etc.
# Always verify the correct port from terminal output before testing!
# Look for output like: "Local: http://localhost:3001"
```

---

## Iterative Development & Testing

### Dev Server Management

See the "Running Applications" section above for standard commands.

### Testing with Chrome Extension

When testing via browser automation:

1. **Verify the correct port** - Check dev server output for actual port number
2. **React state isolation** - DOM manipulation doesn't trigger React state updates
3. **Click buttons via JavaScript** for reliable React event handling:
   ```javascript
   document.querySelector('button.btn-primary').click();
   ```
4. **Check for hydration** - Wait for page to fully hydrate before interacting

### Backend Dependencies

Many features require the backend API to function:

| Feature | Backend Required | Fallback Behavior |
|---------|-----------------|-------------------|
| Chat messages | Yes (`/api/chat`) | Error on send |
| Todo CRUD | Yes (`/api/todos`) | Empty state, errors |
| Statistics | Yes (`/api/todos/stats`) | Shows zeros |

**Testing Strategy:**
- Test UI rendering and interactions first (no backend needed)
- Test with mock data when possible
- Test full integration only when backend is running

### Testing Checklist

Before considering a feature complete:

- [ ] Dev server port verified (check terminal output)
- [ ] Page renders without console errors
- [ ] Empty states display correctly
- [ ] Loading states appear during async operations
- [ ] Error states handle API failures gracefully
- [ ] Button clicks trigger expected state changes
- [ ] Forms validate and submit correctly
- [ ] Navigation between pages works
- [ ] Test on correct dev server port (not cached old instance)

### Common Testing Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Clicks don't work | Testing wrong port | Check dev server output for correct port |
| Form values don't submit | DOM vs React state | Use JavaScript `element.click()` not coordinates |
| Stale UI | Hot reload on different port | Navigate to new port URL |
| Modal doesn't appear | State not updating | Verify React hydration complete |
| API errors | Backend not running | Start backend or test UI-only features |

---

## File Checklist Before Committing

- [ ] TypeScript compiles without errors (`npm run build`)
- [ ] Props interfaces documented with JSDoc
- [ ] Components exported from index.ts
- [ ] No hardcoded URLs or secrets
- [ ] "use client" only where necessary
- [ ] DaisyUI components used for consistency
- [ ] Error states handled
- [ ] Loading states handled
- [ ] Responsive design considered
- [ ] **Tested on correct dev server port**
- [ ] **Verified UI interactions work (clicks, forms)**

---

## Related Documentation

- `DOCUMENTATION/FEATURE_ROADMAP.md` - Planned features
- `.claude/rules/frontend/nextjs.md` - Next.js patterns
- `.claude/rules/frontend/react-components.md` - Component patterns
- `.claude/rules/frontend/ui-ux-guidelines.md` - **UI/UX Design System**
- `Frontend/src/stores/chatStore.ts` - Reference store implementation

---

## UI/UX Quick Reference

For complete guidelines, see `.claude/rules/frontend/ui-ux-guidelines.md`.

### Color Usage
- Use semantic colors: `primary`, `secondary`, `accent`, `error`, `success`, `warning`, `info`
- Never use raw Tailwind colors like `blue-500` directly

### Spacing (8pt Grid)
- All spacing in multiples of 8px: `p-2` (8px), `p-4` (16px), `p-6` (24px), `p-8` (32px)
- Use `gap-*` for flex/grid instead of individual margins

### Typography
- Minimum body text: 16px (`text-base`)
- Line height: 1.5 minimum (`leading-relaxed`)

### Button Hierarchy
- `btn-primary` - One per section, main action
- `btn-secondary` / `btn-ghost` - Secondary actions
- `btn-error` - Destructive actions

### Required States
Every data-driven component needs:
- Empty state (with icon, headline, description, CTA)
- Loading state (skeleton or spinner)
- Error state (what, why, how to fix)

### Accessibility
- Minimum contrast: 4.5:1 for text
- Touch targets: 44px+ on mobile
- Icon buttons need `aria-label`
- Keyboard navigation required
