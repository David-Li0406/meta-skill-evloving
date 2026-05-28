---
name: patterns-reference
description: Golden implementation patterns for each effect type
user-invocable: false
---

# Patterns Reference

Complete golden patterns for the crafting skill. Loaded on-demand.

## Financial Pattern

Two-phase confirmation. No optimistic updates. Cancel always visible.

```tsx
function ClaimButton({ amount, onSuccess }) {
  const [showConfirm, setShowConfirm] = useState(false)
  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: () => claimRewards(amount),
    onSuccess: () => { setShowConfirm(false); onSuccess?.() },
    // NO onMutate - pessimistic
  })

  if (!showConfirm) {
    return <button onClick={() => setShowConfirm(true)}>Claim {amount}</button>
  }

  return (
    <div>
      <p>Confirm claiming {amount}?</p>
      <button onClick={() => setShowConfirm(false)}>Cancel</button>
      <button onClick={() => mutate()} disabled={isPending}>
        {isPending ? 'Claiming...' : 'Confirm'}
      </button>
      {isError && <p>{error.message}</p>}
    </div>
  )
}
```

## Standard Pattern

Optimistic update with rollback. No confirmation needed.

```tsx
function LikeButton({ postId, isLiked }) {
  const queryClient = useQueryClient()
  const { mutate } = useMutation({
    mutationFn: () => toggleLike(postId),
    onMutate: async () => {
      await queryClient.cancelQueries(['post', postId])
      const previous = queryClient.getQueryData(['post', postId])
      queryClient.setQueryData(['post', postId], old => ({
        ...old, isLiked: !old.isLiked
      }))
      return { previous }
    },
    onError: (_, __, ctx) => {
      queryClient.setQueryData(['post', postId], ctx?.previous)
    },
  })

  return <button onClick={() => mutate()}>{isLiked ? '❤️' : '🤍'}</button>
}
```

## Local Pattern

No server. Immediate response. Accessible.

```tsx
function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const isDark = theme === 'dark'

  return (
    <button
      onClick={() => setTheme(isDark ? 'light' : 'dark')}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
    >
      {isDark ? '🌙' : '☀️'}
    </button>
  )
}
```

## Soft Delete Pattern

Optimistic with toast and undo.

```tsx
function ArchiveButton({ itemId }) {
  const { mutate } = useMutation({
    mutationFn: () => archiveItem(itemId),
    onMutate: async () => {
      // Optimistically remove from list
    },
    onSuccess: () => {
      toast('Archived', {
        action: { label: 'Undo', onClick: () => restoreItem(itemId) },
        duration: 5000
      })
    },
    onError: () => {
      // Rollback
      toast.error('Failed to archive')
    },
  })

  return <button onClick={() => mutate()}>Archive</button>
}
```
