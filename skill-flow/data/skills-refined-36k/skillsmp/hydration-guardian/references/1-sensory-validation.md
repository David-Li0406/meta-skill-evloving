# Reference: Sensory Validation Protocol (SVP) 2026

## Overview
Sensory Validation is the practice of using automated agents (like Squaads AI) to verify that the rendered DOM exactly matches the expected React state, especially in complex SSR/ISR environments.

## The "Invisible" Hydration Bug
Many hydration errors in React 19.3 are "soft" failures. React might recover by re-rendering the entire sub-tree, which preserves functionality but destroys performance (TTI) and causes a visual flash.

### Key Indicators of Soft Failures:
1.  **Increased TTI:** Time to Interactive spikes because the main thread is busy re-rendering.
2.  **State Loss:** Input focus or scroll position is lost during the "flash".
3.  **Lighthouse Score Drop:** "Total Blocking Time" increases.

---

## 🔬 SSSV (Server-Side Sensory Validation)
Next.js 16.2 introduces SSSV, allowing the server to generate a "checksum" of the expected client-side DOM.

```javascript
// next.config.ts (Experimental 2026)
export default {
  experimental: {
    sssv: {
      strictMode: true,
      warnOnExtensionConflict: true
    }
  }
}
```

## 🛠️ Automated Audit Tooling
The Guardian uses the following internal toolset to verify hydration:

### 1. The DOM Hash Check
Comparing the raw HTML sent by the server with the HTML structure after the first React effect.

### 2. The "Flash" Detector
A specialized script that monitors for DOM mutations within the first 100ms of the `DOMContentLoaded` event. If a significant percentage of the DOM changes, a "Hydration Flash" is flagged.

```javascript
// Automated Flash Detection Script
let mutations = 0;
const observer = new MutationObserver((list) => {
  mutations += list.length;
});
observer.observe(document.body, { childList: true, subtree: true });

window.addEventListener('load', () => {
  setTimeout(() => {
    observer.disconnect();
    if (mutations > 50) { // Threshold for a large hydration mismatch
      console.warn(`SQUAAD_SVP: High Mutation Count (${mutations}) detected during hydration.`);
    }
  }, 500);
});
```

---

## 🌍 Global Consistency Checks
In 2026, the Squaads AI Core enforces "Universal Determinism."

### Date/Time Traps
**Wrong:**
`<div>{new Date().toLocaleTimeString()}</div>`

**Right (2026 Standard):**
```tsx
import { useDate } from '@/hooks/use-deterministic';

function Clock() {
  const date = useDate(); // Returns a stable date from the server-synced context
  return <div>{date.toLocaleTimeString()}</div>;
}
```

### Currency/Locale Traps
Always use the `Intl` API with an explicit locale passed from the server metadata, never relying on the browser's default locale.

---

## 🏁 Validation Checklist for SVP
- [ ] Browser console is free of `react-dom` warnings.
- [ ] Mutation Observer count is below 10 for static sections.
- [ ] Input focus is maintained if hydration happens while typing.
- [ ] CSS-in-JS styles are injected before the first paint to prevent "Unstyled Flash".
