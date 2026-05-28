---
title: Use Activity Component for Show/Hide
impact: MEDIUM
impactDescription: preserves state/DOM
tags: rendering, activity, react19, optimization
---

## Use Activity Component for Show/Hide

Use React 19's `<Activity>` component to preserve state/DOM for expensive components that frequently toggle visibility.

**Usage:**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveDropdownContent />
    </Activity>
  )
}
```

Avoids expensive re-renders and state loss when toggling visibility.

Reference: [React Activity](https://react.dev/reference/react/Activity)
