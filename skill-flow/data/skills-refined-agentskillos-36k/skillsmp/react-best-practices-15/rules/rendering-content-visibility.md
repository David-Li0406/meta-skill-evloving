---
title: CSS content-visibility for Long Lists
impact: HIGH
impactDescription: faster initial render
tags: rendering, content-visibility, css, optimization
---

## CSS content-visibility for Long Lists

Apply `content-visibility: auto` to defer off-screen rendering.

**CSS:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**Example:**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div>
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          {msg.content}
        </div>
      ))}
    </div>
  )
}
```

For 1000 messages, browser skips layout/paint for ~990 off-screen items (10× faster initial render).

Reference: [MDN content-visibility](https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility)
