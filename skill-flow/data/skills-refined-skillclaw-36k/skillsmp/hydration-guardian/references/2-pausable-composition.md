# Reference: Pausable Composition (React 19.3)

## Introduction
`Pausable` is a first-class React primitive introduced in late 2025 to replace the "hacky" hydration solutions of the previous decade. It allows a developer to explicitly "pause" the hydration of a component tree until a specific condition is met, without blocking the rest of the application.

---

## 💡 Why `Pausable`?
In the past, we used `if (!mounted) return null`. This caused:
- **Layout Shift:** The component was invisible, then suddenly appeared.
- **SEO Impact:** Search engines saw an empty hole where content should be.

`Pausable` solves this by allowing the Server-Rendered HTML to remain static and "frozen" while the rest of the app becomes interactive.

---

## 🛠️ Usage Patterns

### 1. The "Frozen State" Pattern
Useful for components that have a valid server-state but whose client-state takes time to calculate (e.g., complex charts, localized prices).

```tsx
<Pausable fallback={<StaticServerVersion />}>
  <InteractiveClientVersion />
</Pausable>
```

### 2. Nesting Pausables
You can granularly control hydration order to prioritize the "Hero" section.

```tsx
<Pausable priority="high">
  <HeroSection />
  <Pausable priority="low">
    <RecommendedProducts />
  </Pausable>
</Pausable>
```

---

## ⚙️ How it Works (Under the Hood)
1.  **Server Phase:** React renders the `InteractiveClientVersion` as static HTML.
2.  **Client Hydration Phase:** React skips the `Pausable` boundary during the initial hydration pass.
3.  **Activation Phase:** Once the main thread is idle or the `priority` condition is met, React hydraties the boundary in a background transition.

---

## 🚫 Common Pitfalls
- **Over-pausing:** If you pause everything, the app feels "dead" for several seconds.
- **Mismatched Fallbacks:** If the `fallback` doesn't visually match the `InteractiveClientVersion`, you get a "Jump" when the pause ends.

---

## 🚀 2026 Best Practices
- Use `priority="urgent"` for elements inside the viewport (LCP).
- Use `priority="background"` for footers and below-the-fold content.
- Combine with `Suspense` for a "Dual-Layer" loading experience.
