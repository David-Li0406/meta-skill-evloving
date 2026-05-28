---
title: Use Dynamic Imports for Code Splitting
impact: MEDIUM-HIGH
impactDescription: Reduces initial bundle size by loading code on demand
tags: modules, dynamic-import, code-splitting, lazy
---

## Use Dynamic Imports for Code Splitting

Static imports load all code upfront. Dynamic imports load code on demand, reducing initial bundle size and improving time-to-interactive.

**Incorrect (everything in initial bundle):**

```javascript
import { PDFViewer } from './pdf-viewer'; // 500KB library
import { ChartLibrary } from './charts';   // 300KB library
import { MarkdownEditor } from './editor'; // 200KB library

function App() {
  // All 1MB loaded even if user never uses these features
}
```

**Correct (load on demand):**

```javascript
async function showPDFViewer(file) {
  const { PDFViewer } = await import('./pdf-viewer');
  return new PDFViewer(file);
}

async function renderChart(data) {
  const { ChartLibrary } = await import('./charts');
  return ChartLibrary.render(data);
}

// With loading states
async function openEditor() {
  showLoadingSpinner();
  try {
    const { MarkdownEditor } = await import('./editor');
    hideLoadingSpinner();
    return new MarkdownEditor();
  } catch (error) {
    hideLoadingSpinner();
    showError('Failed to load editor');
  }
}
```

**Preloading for better UX:**

```javascript
// Preload on hover/focus
button.addEventListener('mouseenter', () => {
  import('./heavy-module'); // Starts loading
});

button.addEventListener('click', async () => {
  const { HeavyModule } = await import('./heavy-module');
  // Already loaded or almost loaded
});
```

**Route-based code splitting (React):**

```javascript
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

Reference: [MDN Dynamic Import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import)
