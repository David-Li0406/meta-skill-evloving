---
name: tanstack-forms
description: Use this skill when you need guidance on integrating TanStack Query with forms, including handling form submission, managing form state versus server state, and preventing double submissions.
---

# TanStack Query Forms Integration Patterns

This skill provides guidance for integrating TanStack Query with forms, addressing the challenge of mixing server state with form (client) state.

## The Core Challenge

Form data exists in a hybrid zone:
- **Initially**: Server State (fetched data)
- **During editing**: Client State (user changes)
- **After submit**: Server State again

Understanding this lifecycle is key to choosing the right pattern.

## Two Main Approaches

### Approach 1: Simple - Copy to Form State

Use server state as initial data only. The form manages its own state:

```typescript
function EditTodo({ id }: { id: string }) {
  const { data: todo, isLoading } = useQuery(todoQueries.detail(id))

  if (isLoading) return <Skeleton />

  return <TodoForm initialData={todo} />
}

function TodoForm({ initialData }: { initialData: Todo }) {
  // Form state is independent copy of server state
  const [title, setTitle] = useState(initialData.title)
  const [description, setDescription] = useState(initialData.description)

  const mutation = useMutation({
    mutationFn: (data: Partial<Todo>) =>
      api.patch(`/todos/${initialData.id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({ title, description })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button type="submit" disabled={mutation.isPending}>
        Save
      </button>
    </form>
  )
}
```

**Pros:**
- Simple to understand
- Form is in full control
- Works with any form library

**Cons:**
- Background updates won't reflect in form
- Can lead to stale data submission in collaborative apps

**Best for:** Single-user apps, short-lived forms, simple editing flows.

### Approach 2: Derived State Pattern

Keep server state and form state separate, displaying both to the user. This approach allows for real-time updates and better handling of collaborative scenarios. (Further details can be added here based on specific implementation needs.)