---
title: Use useOptimistic for Instant Feedback
impact: HIGH
impactDescription: UI feels instant while server action completes
tags: optimistic-ui, useOptimistic, ux, performance
---

## Use useOptimistic for Instant Feedback

useOptimistic shows expected changes immediately while the server action runs in the background. Reverting automatically on error.

**Incorrect (waiting for server response):**

```typescript
'use client'

export function LikeButton({ postId, initialLikes }) {
  const [likes, setLikes] = useState(initialLikes)
  const [loading, setLoading] = useState(false)

  const handleLike = async () => {
    setLoading(true)
    // ❌ User waits for server response
    const newLikes = await likePost(postId)
    setLikes(newLikes)
    setLoading(false)
  }

  return (
    <button onClick={handleLike} disabled={loading}>
      ❤️ {likes} {loading && '...'}
    </button>
  )
}
```

**Correct (optimistic update):**

```typescript
'use client'
import { useOptimistic } from 'react'
import { likePost } from './actions'

export function LikeButton({ postId, likes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (state, newLike: number) => state + newLike
  )

  async function handleLike() {
    addOptimisticLike(1) // ✓ Instant UI update
    await likePost(postId) // Server action runs in background
    // Automatically reverts if action throws
  }

  return (
    <form action={handleLike}>
      <button type="submit">❤️ {optimisticLikes}</button>
    </form>
  )
}
```

**Optimistic list updates:**

```typescript
'use client'
import { useOptimistic } from 'react'

export function TodoList({ todos }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  )

  async function addTodo(formData: FormData) {
    const text = formData.get('text') as string
    const tempId = crypto.randomUUID()

    // Show immediately with pending state
    addOptimisticTodo({ id: tempId, text, completed: false })

    // Server action
    await createTodo(text)
  }

  return (
    <div>
      <form action={addTodo}>
        <input name="text" placeholder="New todo..." />
        <button type="submit">Add</button>
      </form>

      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id} className={todo.pending ? 'opacity-50' : ''}>
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

useOptimistic makes your app feel instant while maintaining data integrity.

Reference: [useOptimistic](https://react.dev/reference/react/useOptimistic)
