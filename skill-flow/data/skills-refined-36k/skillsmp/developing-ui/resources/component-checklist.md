# Component Development Checklist

Copy this checklist into your task plan when building a new UI component.

## 1. Interface & Scaffolding
- [ ] **Name**: PascalCase (e.g., `PrimaryButton`).
- [ ] **Props**: defined with strict types (TypeScript interfaces preferred). Avoid `any`.
- [ ] **Exports**: correctly exported from the module.

## 2. Styling & Brand
- [ ] **Design Tokens**: uses variables/utilities from `brand-identity`, no magic values.
- [ ] **Responsive**: functional on Mobile (320px), Tablet (768px), and Desktop (1024px+).
- [ ] **Dark Mode**: supports dark mode variants if the brand requires it.
- [ ] **Isolation**: styles do not leak to other components (Scoped/Modules/Tailwind).

## 3. The "5 States" Rule
- [ ] **Idle**: Default view looks correct.
- [ ] **Loading**: Skeletons or spinners are shown during data fetch.
- [ ] **Error**: Graceful error handling (messages, retries) is implemented.
- [ ] **Empty**: "No data" state is handled visually.
- [ ] **Success**: Positive feedback provided for successful actions (if applicable).

## 4. Interaction & Logic
- [ ] **Feedback**: visual feedback on user interaction (e.g., button press).
- [ ] **Focus Management**: Focus flow makes sense for keyboard users.
- [ ] **Error Boundaries**: Component doesn't crash the whole app on failure.

## 5. Accessibility (A11y)
- [ ] **Semantic HTML**: uses native elements (`<button>`, `<a>`, `<input>`) where possible.
- [ ] **Keyboard Nav**: full functionality available via keyboard only.
- [ ] **ARIA**: appropriate labels (`aria-label`, `aria-expanded`, `role`) used correctly.
- [ ] **Images**: `alt` text provided or `role="presentation"`.
- [ ] **Touch Targets**: at least 44x44px on mobile.
- [ ] **Contrast**: text contrast ratio meets WCAG AA standards.

## 6. Performance
- [ ] **Images**: Optimized (WebP/AVIF) and lazy-loaded.
- [ ] **Animations**: 60fps, using only `transform` and `opacity`.
- [ ] **Re-renders**: Memoization used where appropriate to prevent wasted renders.

## 7. Testing
- [ ] **Unit**: Logic/State covered by unit tests.
- [ ] **Browsers**: Verified on Chrome, Safari, and Firefox.
