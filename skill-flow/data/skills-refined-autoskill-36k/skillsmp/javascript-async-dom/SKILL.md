---
name: javascript-async-dom
description: Best practices for Fetch API, event delegation, and DOM manipulation.
---

# JavaScript Async & DOM

## When to use this skill
- Manipulating usage of `fetch` or `XMLHttpRequest`.
- Adding event listeners to DOM elements.
- Interacting with browser APIs (Local Storage, Navigator).

## 1. Async Data Fetching
- **Fetch API**: Use `fetch()` with async/await. Always check `res.ok` before parsing JSON.
  ```javascript
  const res = await fetch('/api/data');
  if (!res.ok) throw new Error('Failed');
  const data = await res.json();
  ```
- **AbortController**: Use `AbortController` to cancel pending requests when components unmount or fast interactions occur.

## 2. event Delegation
- **Listener Attachment**: Attach listeners to a parent container rather than individual items for lists.
  ```javascript
  list.addEventListener('click', (e) => {
    if (e.target.matches('.item-btn')) { ... }
  });
  ```
- **Cleanup**: Always use `removeEventListener` if listeners are attached to transient elements (or use ` { once: true }` where applicable).

## 3. DOM Manipulation
- **Performance**: Minimize reflows. Read layout properties (offsetWidth, etc.) in a batch, then write styles in a batch.
- **Fragments**: Use `DocumentFragment` when appending multiple elements to the DOM at once.
