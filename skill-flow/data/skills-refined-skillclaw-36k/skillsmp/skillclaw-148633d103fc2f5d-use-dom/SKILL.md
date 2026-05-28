---
name: use-dom
description: Use this skill when you need to run web code in a webview on native platforms using Expo DOM components, or when migrating web code to native incrementally.
---

# Skill body

## What are DOM Components?

DOM components allow web code to run verbatim in a webview on native platforms while rendering as-is on the web. This enables the use of web-only libraries like `recharts`, `react-syntax-highlighter`, or any React web library in your Expo app without modification.

## When to Use DOM Components

Use DOM components when you need:

- **Web-only libraries** — Charts (e.g., recharts, chart.js), syntax highlighters, rich text editors, or any library that depends on DOM APIs.
- **Migrating web code** — Bring existing React web components to native without rewriting.
- **Complex HTML/CSS layouts** — When CSS features aren't available in React Native.
- **iframes or embeds** — Embedding external content that requires a browser context.
- **Canvas or WebGL** — Web graphics APIs not available natively.

## When NOT to Use DOM Components

Avoid DOM components when:

- **Native performance is critical** — Webviews add overhead.
- **Simple UI** — React Native components are more efficient for basic layouts.
- **Deep native integration** — Use local modules instead for native APIs.
- **Layout routes** — `_layout` files cannot be DOM components.

## Basic DOM Component

Create a new file with the `'use dom';` directive at the top:

```tsx
// components/WebChart.tsx
"use dom";

export default function WebChart({
  data,
}: {
  data: number[];
  dom: import("expo/dom").DOMProps;
}) {
  return (
    <div style={{ padding: 20 }}>
      <h2>Chart Data</h2>
      <ul>
        {data.map((value, i) => (
          <li key={i}>{value}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Rules for DOM Components

1. **Must have `'use dom';` directive** at the top of the file.
2. **Single default export** — One React component per file.
3. **Own file** — Cannot be defined inline or combined with native components.
4. **Serializable props only** — Strings, numbers, booleans, arrays, plain objects.
5. **Include CSS in the component file** — DOM components run in an isolated context.

## The `dom` Prop

Every DOM component receives a special `dom` prop for webview configuration. Always type it in your props:

```tsx
"use dom";

interface Props {
  content: string;
  dom: import("expo/dom").DOMProps;
}

export default function MyComponent({ content }: Props) {
  return <div>{content}</div>;
}
```