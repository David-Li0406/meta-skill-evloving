---
name: docusaurus-plugin-development
description: Use this skill to develop and build Docusaurus plugins using a starter template.
---

# Docusaurus Plugin Development

## Quick Start: Automatic DOM Enhancement Plugin

```typescript
// src/plugin.ts - Register client module with getClientModules()
export default function myPlugin(context, options): Plugin {
  return {
    name: 'my-plugin',
    getClientModules() {
      return [require.resolve('./client')];
    },
  };
}

// src/client/index.ts - Enhance DOM automatically on every page
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

export default (function () {
  if (!ExecutionEnvironment.canUseDOM) return null;

  return {
    onRouteUpdate({ location }) {
      // Runs on every route change - enhance elements automatically
      document.querySelectorAll('.markdown img').forEach(img => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', () => console.log('Image clicked'));
      });
    },
  };
})();
```

## Core Principles

- **Global Execution**: Client modules via `getClientModules()` run on every page automatically—no manual imports needed in content files.
- **SSR Safety**: Always check `ExecutionEnvironment.canUseDOM` before using browser APIs to prevent SSR errors.
- **Lifecycle Hooks**: Use `onRouteUpdate` for DOM manipulation that needs to reinitialize on every SPA navigation.
- **DOM Selectors**: Use CSS selectors to find target elements (e.g., `.markdown img`, `pre code`) and enhance them.
- **Server vs Client**: Keep Node.js code in `src/plugin.ts`, browser code in `src/client/` - never mix them.

## Common Patterns

### Pattern 1: DOM Enhancement (Image Zoom, Code Copy)

Use `onRouteUpdate` with DOM selectors to enhance elements automatically without imports.

### Pattern 2: External Library Integration

Initialize third-party libraries (medium-zoom, highlight.js) and reinitialize on route changes.

### Pattern 3: Global Event Listeners

Attach keyboard shortcuts or scroll handlers once, persist across routes using initialization flags.

### Pattern 4: Plugin Options

Pass configuration from plugin to client via `setGlobalData` or inline during build.

## Quick Reference

**Plugin Hooks** (`src/plugin.ts`):

- `loadContent()` - Load/process data at build time.
- `contentLoaded()` - Inject global data with `setGlobalData()` or add routes.
- `getClientModules()` - Return array of client module paths (runs in browser).

**Client Lifecycle** (`src/client/index.ts`):

- `onRouteUpdate()` - During navigation (use for DOM manipulation).
- `onRouteDidUpdate()` - After navigation completes (use for analytics).

**Critical Guardrails**:

- ❌ Never import Node modules (`fs`, `path`) in `src/client/*`.
- ✅ Always wrap client code with `ExecutionEnvironment.canUseDOM` check.
- ✅ Use `setTimeout(() => {}, 0)` if DOM elements not immediately available.
- ✅ Clean up previous instances before reinitializing libraries.

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual
-->