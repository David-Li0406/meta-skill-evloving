---
title: Deduplicate Global Event Listeners
impact: LOW
impactDescription: single listener for N components
tags: client, event-listeners, performance, deduplication
---

## Deduplicate Global Event Listeners

Use a shared subscription pattern to share global event listeners across component instances.

**Incorrect (N instances = N listeners):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === key) callback()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

When using the `useKeyboardShortcut` hook multiple times, each instance will register a new listener.

**Correct (N instances = 1 listener):**

```tsx
// Module-level Map to track callbacks per key
const keyCallbacks = new Map<string, Set<() => void>>()
let listenerAttached = false

function ensureListener() {
  if (!listenerAttached) {
    window.addEventListener('keydown', (e: KeyboardEvent) => {
      const callbacks = keyCallbacks.get(e.key)
      if (callbacks) {
        callbacks.forEach(cb => cb())
      }
    })
    listenerAttached = true
  }
}

function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    ensureListener()
    
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set())
    }
    keyCallbacks.get(key)!.add(callback)
    
    return () => {
      keyCallbacks.get(key)?.delete(callback)
    }
  }, [key, callback])
}

function Profile() {
  // Multiple shortcuts will share the same listener
  useKeyboardShortcut('s', handleSave)
  useKeyboardShortcut('e', handleEdit)
  // ...
}
```
