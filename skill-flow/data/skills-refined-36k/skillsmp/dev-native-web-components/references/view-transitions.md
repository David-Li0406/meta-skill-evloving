# View Transitions Reference

> Use CSS View Transitions for smooth page and element animations.

---

## SPA View Transitions

```javascript
// Basic transition
document.startViewTransition(() => {
  updateDOM();
});

// With async
document.startViewTransition(async () => {
  const data = await fetch("/api/data");
  renderPage(data);
});
```

---

## MPA View Transitions (2025)

```css
/* Enable in CSS */
@view-transition {
  navigation: auto;
}
```

```html
<!-- Or per-link -->
<a href="/about" data-view-transition>About</a>
```

---

## Named Transitions

```css
/* Source page */
.hero-image {
  view-transition-name: hero;
}

/* Both pages */
::view-transition-old(hero) {
  animation: fade-out 0.3s ease-out;
}

::view-transition-new(hero) {
  animation: fade-in 0.3s ease-in;
}

@keyframes fade-out {
  to {
    opacity: 0;
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
}
```

---

## Transition Classes (2025)

```css
/* Group elements for same transition */
.card {
  view-transition-class: card;
}

::view-transition-group(*.card) {
  animation-duration: 0.4s;
}
```

---

## Custom Transition Animations

```css
/* Slide transition */
::view-transition-old(slide) {
  animation: slide-out 0.3s ease-out;
}

::view-transition-new(slide) {
  animation: slide-in 0.3s ease-in;
}

@keyframes slide-out {
  to {
    transform: translateX(-100%);
  }
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
  }
}

/* Crossfade (default) */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}
```

---

## Reduce Motion Support

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
  }
}
```

---

## Conditional Transitions

```javascript
// Only if supported
if (document.startViewTransition) {
  document.startViewTransition(() => updateDOM());
} else {
  updateDOM();
}

// With types
document.startViewTransition({
  update: () => updateDOM(),
  types: ["slide-left"],
});
```

```css
/* Type-based animations */
html:active-view-transition-type(slide-left) {
  ::view-transition-old(root) {
    animation-name: slide-out-left;
  }
}
```

---

## Element Transitions

```javascript
// Animate specific element
const card = document.querySelector(".card");
card.style.viewTransitionName = "card";

document.startViewTransition(() => {
  card.classList.toggle("expanded");
});
```

---

## Browser Support

| Browser | SPA   | MPA   | Classes |
| ------- | ----- | ----- | ------- |
| Chrome  | 111+  | 126+  | 125+    |
| Edge    | 111+  | 126+  | 125+    |
| Firefox | 135+  | 135+  | 135+    |
| Safari  | 18.0+ | 18.0+ | 18.0+   |

---

## Checklist

- [ ] Use `view-transition-name` for shared elements
- [ ] Add `prefers-reduced-motion` support
- [ ] Feature detect before using
- [ ] Keep transitions under 300ms

_Reference: [developer.chrome.com/docs/web-platform/view-transitions](https://developer.chrome.com/docs/web-platform/view-transitions)_
