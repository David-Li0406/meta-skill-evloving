---
name: server-actions
description: Mutations avec Server Actions
workflows:
  - id: server-actions-impl
    template: wf-creation
    phase: Production
    name: Implémentation Server Actions
    duration: 0.5-1 jour
---

# Server Actions

Tu es l'agent responsable des **Server Actions** pour les mutations de données.

## Ta Responsabilité Unique

Implémenter les mutations de données avec Server Actions.

## Tu NE fais PAS

- ❌ Data fetching → `data-fetching.md`
- ❌ Cache/revalidation → `revalidation.md`
- ❌ Formulaires React → `react-expert`
- ❌ Validation avancée → Backend ou Zod

## Input Attendu

- Type de mutation (create, update, delete)
- Données à modifier
- Besoin de revalidation

## Output Produit

- Code Server Action
- Intégration formulaire
- Gestion des erreurs

## Syntaxe de Base

### Inline Server Action

```tsx
// app/posts/new/page.tsx
export default function NewPostPage() {
  async function createPost(formData: FormData) {
    'use server'

    const title = formData.get('title') as string
    const content = formData.get('content') as string

    await db.post.create({
      data: { title, content }
    })

    revalidatePath('/posts')
    redirect('/posts')
  }

  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Créer</button>
    </form>
  )
}
```

### Fichier Séparé (recommandé)

```tsx
// actions/posts.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { db } from '@/lib/db'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({
    data: { title, content }
  })

  revalidatePath('/posts')
  redirect('/posts')
}

export async function deletePost(id: string) {
  await db.post.delete({ where: { id } })
  revalidatePath('/posts')
}

// app/posts/new/page.tsx
import { createPost } from '@/actions/posts'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Créer</button>
    </form>
  )
}
```

## Patterns d'Utilisation

### Avec Binding de Paramètres

```tsx
// actions/posts.ts
'use server'

export async function deletePost(id: string) {
  await db.post.delete({ where: { id } })
  revalidatePath('/posts')
}

// components/DeleteButton.tsx
import { deletePost } from '@/actions/posts'

export function DeleteButton({ postId }: { postId: string }) {
  const deletePostWithId = deletePost.bind(null, postId)

  return (
    <form action={deletePostWithId}>
      <button type="submit">Supprimer</button>
    </form>
  )
}
```

### Avec useFormState (validation)

```tsx
// actions/auth.ts
'use server'

interface FormState {
  message: string
  errors?: {
    email?: string[]
    password?: string[]
  }
}

export async function login(
  prevState: FormState,
  formData: FormData
): Promise<FormState> {
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  // Validation
  if (!email.includes('@')) {
    return {
      message: 'Erreur de validation',
      errors: { email: ['Email invalide'] }
    }
  }

  // Auth logic
  const result = await authenticate(email, password)

  if (!result.success) {
    return { message: 'Identifiants incorrects' }
  }

  redirect('/dashboard')
}

// components/LoginForm.tsx
'use client'

import { useFormState } from 'react-dom'
import { login } from '@/actions/auth'

const initialState = { message: '' }

export function LoginForm() {
  const [state, formAction] = useFormState(login, initialState)

  return (
    <form action={formAction}>
      <div>
        <input name="email" type="email" required />
        {state.errors?.email && (
          <p className="text-red-500">{state.errors.email[0]}</p>
        )}
      </div>

      <div>
        <input name="password" type="password" required />
        {state.errors?.password && (
          <p className="text-red-500">{state.errors.password[0]}</p>
        )}
      </div>

      {state.message && <p>{state.message}</p>}

      <SubmitButton />
    </form>
  )
}
```

### Avec useFormStatus (pending state)

```tsx
// components/SubmitButton.tsx
'use client'

import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Envoi...' : 'Envoyer'}
    </button>
  )
}

// Utilisation
<form action={createPost}>
  <input name="title" />
  <SubmitButton />
</form>
```

### Appel Programmatique

```tsx
// components/LikeButton.tsx
'use client'

import { useTransition } from 'react'
import { likePost } from '@/actions/posts'

export function LikeButton({ postId }: { postId: string }) {
  const [isPending, startTransition] = useTransition()

  function handleClick() {
    startTransition(async () => {
      await likePost(postId)
    })
  }

  return (
    <button onClick={handleClick} disabled={isPending}>
      {isPending ? '...' : '❤️'}
    </button>
  )
}
```

## Validation avec Zod

```tsx
// actions/posts.ts
'use server'

import { z } from 'zod'

const PostSchema = z.object({
  title: z.string().min(3, 'Titre trop court').max(100),
  content: z.string().min(10, 'Contenu trop court'),
})

export async function createPost(formData: FormData) {
  const rawData = {
    title: formData.get('title'),
    content: formData.get('content'),
  }

  const validated = PostSchema.safeParse(rawData)

  if (!validated.success) {
    return {
      success: false,
      errors: validated.error.flatten().fieldErrors,
    }
  }

  await db.post.create({ data: validated.data })

  revalidatePath('/posts')
  return { success: true }
}
```

## Optimistic Updates

```tsx
// components/LikeButton.tsx
'use client'

import { useOptimistic } from 'react'
import { likePost } from '@/actions/posts'

export function LikeButton({
  postId,
  likes,
  isLiked,
}: {
  postId: string
  likes: number
  isLiked: boolean
}) {
  const [optimisticState, addOptimistic] = useOptimistic(
    { likes, isLiked },
    (state, newIsLiked: boolean) => ({
      likes: newIsLiked ? state.likes + 1 : state.likes - 1,
      isLiked: newIsLiked,
    })
  )

  async function handleClick() {
    addOptimistic(!optimisticState.isLiked)
    await likePost(postId)
  }

  return (
    <button onClick={handleClick}>
      {optimisticState.isLiked ? '❤️' : '🤍'} {optimisticState.likes}
    </button>
  )
}
```

## Gestion des Erreurs

```tsx
// actions/posts.ts
'use server'

export async function createPost(formData: FormData) {
  try {
    const post = await db.post.create({
      data: {
        title: formData.get('title') as string,
        content: formData.get('content') as string,
      },
    })

    revalidatePath('/posts')
    return { success: true, post }
  } catch (error) {
    return {
      success: false,
      error: 'Impossible de créer le post',
    }
  }
}

// Client usage
const result = await createPost(formData)
if (!result.success) {
  setError(result.error)
}
```

## Bonnes Pratiques

```
✅ 'use server' en haut du fichier ou de la fonction
✅ Valider les données entrantes (Zod)
✅ Revalidater après mutation
✅ Retourner des états typés
✅ useFormStatus pour UX de chargement

❌ Ne pas exposer de logique sensible
❌ Éviter les Server Actions trop longues
❌ Ne pas oublier la validation
❌ Éviter les redirects sans revalidation
```

## Escalades

| Situation | Action |
|-----------|--------|
| Data fetching | → `data-fetching.md` |
| Revalidation avancée | → `revalidation.md` |
| Forms complexes | → `react-expert` |
| Auth/permissions | → Middleware ou backend |


## Livrables

| Livrable | Description |
|----------|-------------|
| Server Actions | Actions serveur pour mutations |
| Configuration | Setup Server Actions et validation |
| Documentation | Guide d'utilisation et patterns |
