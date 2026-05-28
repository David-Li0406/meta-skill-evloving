# 6. Rendering Performance

**Impact: MEDIUM**

## 6.1 Animate SVG Wrapper Instead of SVG Element

Wrap SVG in a `<div>` and animate the wrapper instead to enable hardware acceleration.

## 6.2 CSS content-visibility for Long Lists

Apply `content-visibility: auto` to defer off-screen rendering.

## 6.3 Hoist Static JSX Elements

Extract static JSX outside components to avoid re-creation.

## 6.4 Optimize SVG Precision

Reduce SVG coordinate precision to decrease file size.

## 6.5 Prevent Hydration Mismatch Without Flickering

Use synchronous inline scripts to inject client-side state (like themes) before React hydrates.

## 6.6 Use `<Activity>` Component (React 19.2+)

**Impact: HIGH (performance for toggled UI)**

The `<Activity>` component (formerly `Offscreen`) allows you to hide a component tree while keeping it mounted and preserving its state. This is much faster than unmounting and remounting for frequently toggled UI like Tabs or Modals.

**Implementation:**

```tsx
import { Activity } from 'react';

function Dashboard({ activeTab }) {
  return (
    <>
      <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
        <HomeTab />
      </Activity>
      
      <Activity mode={activeTab === 'settings' ? 'visible' : 'hidden'}>
        <SettingsTab />
      </Activity>
    </>
  );
}
```

When `mode="hidden"`, React skips the rendering and commit phase for that tree but keeps the DOM nodes and state in memory.

## 6.7 Use Explicit Conditional Rendering

Use ternary operators (`? :`) instead of `&&` for numbers/strings to avoid rendering `0` or `NaN` (which the React Compiler might not automatically fix if types are ambiguous).

---

# 7. JavaScript Performance

**Impact: LOW-MEDIUM**

## 7.1 Batch DOM CSS Changes

Group multiple CSS changes together via classes or `cssText` to avoid multiple reflows.

## 7.2 Build Index Maps for Repeated Lookups

Use a `Map` instead of multiple `.find()` calls on the same array.

## 7.3 Cache Property Access in Loops

Cache object property lookups in hot paths.

## 7.4 Combine Multiple Array Iterations

Combine multiple `.filter()` or `.map()` calls into one loop (or use `reduce`).

## 7.5 Use `toSorted()` Instead of `sort()` for Immutability

`.sort()` mutates the array; `.toSorted()` (ES2023) creates a new one, which is essential for React state safety and Compiler compatibility.

---

# 8. Advanced Patterns

## 8.1 Stable Callbacks with `useEffectEvent`

Use `useEffectEvent` for event handlers that need reactive values but shouldn't trigger effects.

## 8.2 `useLatest` for Stable Callback Refs

Access latest values in callbacks without adding them to dependency arrays, keeping the function reference stable.
