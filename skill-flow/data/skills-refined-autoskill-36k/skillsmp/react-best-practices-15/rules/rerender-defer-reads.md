---
title: Defer State Reads to Usage Point
impact: MEDIUM
impactDescription: avoids unnecessary subscriptions
tags: rerender, state, subscriptions, optimization
---

## Defer State Reads to Usage Point

Don't subscribe to dynamic state (URL params, localStorage) if you only read it inside callbacks.

**Incorrect (subscribes to all URL changes):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const [searchParams] = useSearchParams()
  
  const handleShare = () => {
    const url = `${window.location.origin}/chat/${chatId}?${searchParams}`
    navigator.clipboard.writeText(url)
  }
  
  return <button onClick={handleShare}>Share</button>
}
```

**Correct (reads on demand, no subscription):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const url = `${window.location.href}`
    navigator.clipboard.writeText(url)
  }
  
  return <button onClick={handleShare}>Share</button>
}
```
