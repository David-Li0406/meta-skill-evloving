# Frontend Performance Checklist

## 🏎️ Core Web Vitals (The Big Three)

### LCP (Largest Contentful Paint) - < 2.5s
- [ ] **Images**: Is the LCP image preloaded? `<link rel="preload" as="image">`
- [ ] **Format**: Are you using WebP/AVIF?
- [ ] **Server**: Is the server response time (TTFB) fast enough?
- [ ] **Render-Blocking**: Are JS/CSS files deferring the paint?

### INP (Interaction to Next Paint) - < 200ms
- [ ] **JS Bloat**: Is the main thread blocked by heavy JS execution?
- [ ] **Event Handlers**: Are click handlers doing too much work synchronously?
- [ ] **Transitions**: Are you using `useTransition` (React 18+) for non-urgent updates?

### CLS (Cumulative Layout Shift) - < 0.1
- [ ] **Dimensions**: Do all `<img>` and video elements have explicit `width` and `height`?
- [ ] **Fonts**: Are you using `font-display: swap`?
- [ ] **Dynamic Content**: Are you reserving space (skeleton loaders) for content that loads late?

## 📦 Bundle & Assets
- [ ] **Code Splitting**: Are routes lazy-loaded? `const Page = lazy(() => import('./Page'))`
- [ ] **Tree Shaking**: Are you importing huge libs just for one function? (e.g. `lodash` -> `lodash-es`)
- [ ] **Dep Check**: Run `npm audit` and check bundle visualization.

## ⚛️ React Specific
- [ ] **Re-renders**: Use React DevTools "Highlight updates". Fix wasted renders.
- [ ] **Memo**: Use `useMemo` for heavy calculations, `useCallback` for stable function references.
- [ ] **Virtualization**: Use `tanstack/react-virtual` for lists > 50 items.
