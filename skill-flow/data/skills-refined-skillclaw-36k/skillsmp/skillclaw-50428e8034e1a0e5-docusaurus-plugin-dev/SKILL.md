---
name: docusaurus-plugin-dev
description: Use this skill when you want to develop and build Docusaurus plugins using a starter template.
---

# Docusaurus Plugin Dev

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

## Reference Files

For detailed documentation, see references in this skill directory:

- `references/client-modules-guide.md` - Comprehensive client modules guide
- `README.md` - Plugin documentation