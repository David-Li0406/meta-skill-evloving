# API Reference & Package Deep-Dive

This reference provides a detailed breakdown of the `@json-render` ecosystem packages and their primary exports as of January 2026.

## 📦 @json-render/core
The core library is environment-agnostic (Node.js, Edge, Browser).

### `createRenderState(options)`
Initializes the internal state machine.
- `catalog`: The Zod-validated component library.
- `initialData`: Initial state for data binding.
- `onAction`: Callback for component-triggered events.

### `applyPatch(state, patch)`
Applies a JSON Patch (RFC 6902) to the current state.
- Supports `add`, `remove`, `replace`, `move`, `copy`, and `test`.

---

## ⚛️ @json-render/react
The React 19+ optimized renderer.

### `<JSONRender />`
The primary component for dynamic rendering.
- `json`: String (JSONL) or Object.
- `catalog`: The catalog object.
- `data`: External data for binding.
- `theme`: (Optional) CSS variables or theme object.
- `components`: (Optional) Overrides for catalog implementations.

### `useJSONData(path)`
A hook to access data binding values inside your catalog components.
```tsx
const MyComponent = ({ path }) => {
  const value = useJSONData(path);
  return <div>{value}</div>;
};
```

---

## 🛠 @json-render/codegen
For static code generation.

### `generateReact(json, catalog, options)`
Returns a string of pure React code.
- `typescript`: Boolean (default: true).
- `tailwind`: Boolean (if you want tailwind classes included).
- `standalone`: If true, includes all necessary imports.

---

## 🤖 @json-render/ai-sdk
Helper package for Vercel AI SDK integration.

### `jsonRenderStream(result)`
Wraps an AI SDK `streamText` or `streamObject` result to automatically handle the JSONL patch conversion.

*Updated: January 22, 2026 - 17:50*
