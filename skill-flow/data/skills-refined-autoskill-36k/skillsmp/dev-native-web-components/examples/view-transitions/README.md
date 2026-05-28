# View Transition Toggle

Layout toggle using the View Transition API with minimal JavaScript.

## Features Used

- **View Transition API** - `document.startViewTransition`
- **`view-transition-name`** - Named elements for animation
- **Reduced motion** - `prefers-reduced-motion`

## Key Patterns

### Start a View Transition

```js
if ("startViewTransition" in document) {
  document.startViewTransition(updateLayout);
} else {
  updateLayout();
}
```

### Named Transition Targets

```css
.hero {
  view-transition-name: hero;
}
```

## Browser Support (Baseline 2024 - newly)

| Browser | Status   |
| ------- | -------- |
| Chrome  | 111+ ✅   |
| Edge    | 111+ ✅   |
| Firefox | 135+ ✅   |
| Safari  | 18.0+ ✅  |
