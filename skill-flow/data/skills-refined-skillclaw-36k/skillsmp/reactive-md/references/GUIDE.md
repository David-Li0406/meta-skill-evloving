# Reactive MD User Guide

Practical solutions for common issues and best practices for reliable previews.

## About Code Examples

Code blocks in this guide use different markers:

- **`jsx live` / `css live`** - Executable examples that render in preview
- **`jsx` / `css`** - Reference patterns (syntax examples, won't execute)
- **Markdown fences** - Literal markdown syntax (showing fence usage itself)

## Component Development

### React Imports

React is global - don't import it. Hooks must be imported:

```jsx live
// ✅ Correct pattern
import { useState, useEffect } from 'react';

export default function MyComponent() {
  const [count, setCount] = useState(0);
  return <div>Count: {count}</div>;
}
```

### Quick Diagnosis

When components show error cards instead of rendering:

**File Extension**: Only `.jsx` and `.tsx` files work (VS Code needs this to recognize JSX syntax)

**Syntax Errors**: Check the Problems panel (`View → Problems`), or use Interactive Preview (`Cmd+K P`) for detailed messages

**Export Patterns**: Use simple `export default function` or `export function`. Avoid `memo()`, conditional exports, or dynamic exports

### Component Structure Best Practices

#### For Single Components with Helpers
```jsx live
// ✅ Recommended: Helpers before or after main export
import { useState } from 'react';

function HelperComponent() {
  return <div>Helper content</div>;
}

export default function MainComponent() {
  return (
    <div>
      <HelperComponent />
      Main content
    </div>
  );
}
```

#### For Multiple Components
```jsx
// ✅ Recommended: Named exports for libraries
export function Button({ children }) {
  return <button className="btn">{children}</button>;
}

export function Card({ title, children }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {children}
    </div>
  );
}
```

#### For Inline Markdown Live Fences

Always wrap everything in a single parent component. The reactive-md renderer needs one clear entry point.

```jsx live
// ✅ CORRECT: Single parent component wraps all content
function Demo() {
  function Button({ children, variant = 'primary' }) {
    return <button className="btn">{children}</button>;
  }

  return (
    <div className="flex gap-4">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
    </div>
  );
}
```

**What NOT to do:**

These patterns will fail because the renderer can't determine the entry point:

````markdown
<!-- ❌ WRONG: Top-level JSX mixed with helper function -->
```jsx live
function Button({ children }) {
  return <button>{children}</button>;
}

<div>
  <Button>Click me</Button>
</div>
```

<!-- ❌ WRONG: Top-level JSX mixed with import statement -->
```jsx live
import Card from './Card.jsx';

<Card />
```
````

**Why wrapping matters:** The renderer executes a single component function. Helpers + top-level JSX = ambiguous entry point (is it the function? the JSX? both?). A single wrapper removes all ambiguity.

#### What to Avoid
- Mixed `export default` with named exports in the same file
- Complex exports: `export default memo(Component)` or conditional exports
- Helper functions + top-level JSX in inline fences

## Device Emulation & Responsive Storytelling (v3.0)

Reactive MD uses a **Document-Level Authority** model. As an agent, you must follow these rules when structuring responsive documents.

### Baseline Dimensions (Standard Requirements)
Always design for the lowest common denominator first.
- **Mobile**: 375x667 (iPhone SE)
- **Tablet**: 768x1024 (Classic iPad)
- **Desktop**: 1440x900 (13" Notebook)

### The Document Bus (🔗 vs 📌)
- **Synced (🔗)**: Default. Use for cohesive narratives where all components shared a breakpoint.
- **Pinned (📌)**: Set in UI. Prevents a component from changing when the document-level device changes.

### Authoritative DSL Modifiers
Use these in code fence headers to guide the reader's view. Resolution priority is **`mid` > `model` > `device`**.

| Modifier | Values | Default | Agent Usage |
| :--- | :--- | :--- | :--- |
| **`device`** | `mobile`, `tablet`, `desktop` | `mobile` | Use for generic category previews. |
| **`mid`** | `iphone-15-pro`, `ipad-air-2024` | N/A | Use for high-precision, specific hardware tests. |
| **`orientation`** | `portrait`, `landscape`, `auto` | `auto` | Use to show specific layout orientations. |
| **`lock-view`** | (Flag) | N/A | **Critical for Narratives**. Use to hide UI controls (🚫). |
| `no-placeholder` | (Flag) | N/A | Disables display of helpful cards (EIP and BAP) in static preview |

**Example Narrative Step**:
`​``jsx live mid=iphone-15-pro orientation=portrait lock-view
// Force the reader to see the mobile implementation
`​``

### Responsive Design: Container Queries (Agent Requirement)
**CRITICAL**: Since the `ViewportFrame` provides `container-type: inline-size`, you must prefer **Container Queries** over Media Queries for component responsiveness.

- **Why?**: Media queries target the global VS Code window. Container queries target the emulated device viewport.
- **Tailwind v4 builtin**:
    1.  Mark your root element or wrapper with the `@container` class.
    2.  Use responsive variants: `<div class="@container"><div class="grid-cols-1 @md:grid-cols-2"></div></div>`
    3.  Arbitrary values: `<div class="flex-col @[400px]:flex-row">`
- **CSS**: Use standard `@container (min-width: ...)` blocks.

#### Pixel-Perfect Scaling
Reactive MD uses a "Double-Wrapper" architecture. The component always "thinks" it is in a fixed logical viewport (e.g. 375px), but scales fluidly using CSS Container Query units (`cqw`) to fit any screen size.

## Data Files

### Local Files

**Don't use `fetch()` for local files** (security restrictions block it). Use import statements instead:

```jsx
// ✅ Correct: Import local JSON
import data from './data.json';

export default function MyComponent() {
  return <div>{data.items.map(item => <span>{item.name}</span>)}</div>;
}
```

```jsx
// ❌ Wrong: fetch() doesn't work
export default function MyComponent() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('./data.json').then(r => r.json()).then(setData);
  }, []);

  return <div>{data?.items.map(item => <span>{item.name}</span>)}</div>;
}
```

### Remote Data

- **Markdown Preview**: No network access - use static data or imports
- **Interactive Preview**: Full network access - `fetch()` works normally

## Package and Dependency Management

### Bundled Packages (Both Preview Modes)
Always available in both Markdown Preview and Interactive Preview:
- `lucide-react` - SVG icons
- `motion/react` - Animations (import from `motion/react`)
- `dayjs` - Date formatting (relativeTime plugin included)
- `clsx` - Conditional CSS classes
- `uuid` - Unique ID generation
- `es-toolkit` - Modern lodash replacement

### CDN Packages (Interactive Preview Only)
Require `Cmd+K P` to load from esm.sh:
- `@heroicons/react` - Icon set (Tailwind team)
- `zustand` - State management
- `jotai` - Atomic state
- `tailwind-merge` - Merge Tailwind classes
- `react-hook-form` - Form handling

### Known Limitations
These packages cannot be loaded via esm.sh:
- **`recharts`** - Missing transitive dependency (`clsx` not resolved)
- **`swr`** - Missing React context shim (`use-sync-external-store`)
- **`@tanstack/react-query`** - React instance conflicts

**Workaround**: For these use cases, use `fetch()` directly or `zustand`/`jotai` for state.

### Styling Approaches

**Choose ONE approach per file**:

- **Tailwind CSS** - Utility-first, built into Reactive MD (easiest for quick prototypes)
- **Inline styles** - Simple, self-contained (good for minimal examples)
- **CSS classes** - Plain CSS with semantic names (good for maintainable styles)

**Recommendation**: Use Tailwind for speed, but keep CSS files simple and readable.

## Platform APIs and Browser Features

### Supported
**Interactive Preview** (`Cmd+K P`) supports:
- `localStorage` / `sessionStorage` - Persistent storage
- `fetch()` - Remote API calls
- `Canvas` API - Drawing and charts
- Timers: `setTimeout()`, `setInterval()`

**Both Preview Modes** support:
- `import` statements for local JSON files
- Bundled packages (see Package and Dependency Management)

### Limitations
**Markdown Preview** uses static rendering with limited browser APIs:
- ❌ No `localStorage`/`sessionStorage` (use Interactive Preview)
- ❌ No WebSockets (use `fetch()` polling)
- ❌ No Service Workers (use `localStorage` for persistence)

**Both Modes**:
- ❌ Cannot fetch local files at runtime (use `import` instead)

## Performance

### Live Reload
Default debounce: 300ms. Increase via `reactiveMd.debounceMs` if updates feel too frequent.

### Module-Level Side Effects
Avoid side effects at module level (they run multiple times on hot reload):

```jsx
// ❌ Wrong: Runs on every hot reload
console.log('Module loaded');
const timestamp = Date.now();

export default function Demo() { ... }
```

```jsx live
// ✅ Correct: Side effects in useEffect
import { useEffect } from 'react';

export default function Demo() {
  useEffect(() => {
    console.log('Component mounted');
  }, []);

  return <div>Demo Component</div>;
}
```

### Large Files
Very large JSX files may slow parsing - consider splitting into multiple components.

## Troubleshooting

### Quick Checklist

1. ✅ File extension is `.jsx` or `.tsx`?
2. ✅ Not importing React (`import React from 'react'`)?
3. ✅ Using `import` not `fetch()` for local files?
4. ✅ Simple export pattern (`export default function`)?
5. ✅ Single entry point in inline fences?
6. ✅ Check Output panel (`View → Output → "Reactive MD"`)?
7. ✅ Try Interactive Preview (`Cmd+K P`) for detailed errors?

**When in doubt**: Simplify to a basic component, then add complexity gradually.

### When Things Still Don't Work

1. **Check the Output Panel**: `View → Output → "Reactive MD"` for extension logs
2. **Reload VS Code**: `Cmd+Shift+P` → "Developer: Reload Window"
3. **Verify File Type**: Ensure `.jsx` or `.tsx` extension
4. **Simplify**: Remove complex patterns and test with basic component

## Creating Your Own Examples

### Folder Structure

Create self-contained examples that demonstrate a concept:

```
my-example/
├── README.md           # Overview and problem statement
├── spec.md             # Interactive demonstration
├── Component.jsx       # Reusable component
├── styles.css          # Custom styles (if needed)
└── data.json           # Sample data (if needed)
```

### What Makes a Good Example

- **Tell a story** — Start with the problem, then show the solution
- **Be interactive** — Demonstrate actual behavior with `jsx live` blocks
- **Document decisions** — Explain why you chose this approach
- **Show edge cases** — Loading states, errors, empty states
- **Use local imports** — Keep components and styles together

### Example Template

````markdown
# Feature Name

## Problem
What user problem does this solve?

## Solution
How does this feature address the problem?

## Interactive Demo
```jsx live
import Component from './Component.jsx';
import './styles.css';

export default function Demo() {
  return <Component />;
}
```

## Edge Cases
- Loading state
- Error state
- Empty state
```jsx live
// Show these states
```
````

### Quality Standards

- **Accurate**: Code examples actually work (test them!)
- **Self-contained**: No external dependencies beyond bundled pamentation
- **Progressive**: Start simple, show advanced patterns
- **Accessible**: Include ARIA labels and keyboard navigation
- **Performant**: Efficient rendering, minimal re-renders

**Best practice**: Start simple, add complexity gradually.