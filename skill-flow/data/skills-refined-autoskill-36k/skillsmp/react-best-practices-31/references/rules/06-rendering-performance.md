# Rendering Performance

**Impact: MEDIUM** | Optimizing the rendering process reduces browser workload.

---

## 1. CSS content-visibility for Long Lists

Defer off-screen rendering. **10× faster initial render** for long lists.

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

For 1000 messages, browser skips layout/paint for ~990 off-screen items.

---

## 2. Animate SVG Wrapper Instead of SVG Element

Browsers lack hardware acceleration for SVG CSS animations. Wrap in `<div>`.

```tsx
// BAD: no hardware acceleration
<svg className="animate-spin"><circle /></svg>

// GOOD: hardware accelerated
<div className="animate-spin">
  <svg><circle /></svg>
</div>
```

---

## 3. Use Explicit Conditional Rendering

Use ternary (`? :`) instead of `&&` when condition can be falsy values that render.

```tsx
// BAD: renders "0" when count is 0
{count && <span className="badge">{count}</span>}

// GOOD: renders nothing when count is 0
{count > 0 ? <span className="badge">{count}</span> : null}
```

---

## 4. Prevent Hydration Mismatch Without Flickering

Inject synchronous script for client-only data (theme, preferences).

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">{children}</div>
      <script
        dangerouslySetInnerHTML={{
          __html: `(function() {
            try {
              var theme = localStorage.getItem('theme') || 'light';
              document.getElementById('theme-wrapper').className = theme;
            } catch (e) {}
          })();`,
        }}
      />
    </>
  )
}
```

---

## 5. Hoist Static JSX Elements

Extract static JSX outside components to avoid re-creation.

```tsx
// BAD: recreates element every render
function Container() {
  return <div>{loading && <div className="animate-pulse h-20 bg-gray-200" />}</div>
}

// GOOD: reuses same element
const skeleton = <div className="animate-pulse h-20 bg-gray-200" />

function Container() {
  return <div>{loading && skeleton}</div>
}
```

---

## 6. Use Activity Component for Show/Hide

Preserve state/DOM for frequently toggled expensive components.

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

---

## 7. Optimize SVG Precision

Reduce coordinate precision to decrease file size.

```svg
<!-- BAD -->
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />

<!-- GOOD -->
<path d="M 10.3 20.8 L 30.9 40.2" />
```

```bash
npx svgo --precision=1 --multipass icon.svg
```
