# React 19 Hooks

## New Hooks Overview

React 19 introduces several new hooks for improved form handling and state management:

| Hook | Purpose | Location |
|------|---------|----------|
| `useActionState` | Form state management with actions | `react` |
| `useFormStatus` | Track form submission status | `react-dom` |
| `useOptimistic` | Optimistic UI updates | `react` |

## useActionState

Manages form state with async actions. Replaces the pattern of `useState` + `useTransition` for forms.

### Signature

```typescript
const [state, formAction, isPending] = useActionState(
  action: (previousState: State, formData: FormData) => Promise<State>,
  initialState: State,
  permalink?: string
);
```

### Returns

- `state` - Current state (result of last action)
- `formAction` - Action to pass to form's `action` prop
- `isPending` - Boolean indicating if action is in progress

### Basic Example

```typescript
"use client";

import { useActionState } from "react";

interface FormState {
  error: string | null;
  success: boolean;
}

async function submitContact(
  prevState: FormState,
  formData: FormData
): Promise<FormState> {
  const email = formData.get("email") as string;
  const message = formData.get("message") as string;

  try {
    await sendContactEmail({ email, message });
    return { error: null, success: true };
  } catch (error) {
    return { error: "Failed to send message", success: false };
  }
}

export function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitContact, {
    error: null,
    success: false
  });

  if (state.success) {
    return <p className="text-green-600">Message sent successfully!</p>;
  }

  return (
    <form action={formAction}>
      <input type="email" name="email" required />
      <textarea name="message" required />
      <button type="submit" disabled={isPending}>
        {isPending ? "Sending..." : "Send"}
      </button>
      {state.error && <p className="text-red-500">{state.error}</p>}
    </form>
  );
}
```

### With Server Actions

```typescript
"use client";

import { useActionState } from "react";
import { createBudget } from "~/features/budget/server/actions/create-budget";
import type { ActionResponse } from "~/lib/action-types";

export function BudgetForm() {
  const [state, formAction, isPending] = useActionState(
    async (prev: ActionResponse | null, formData: FormData) => {
      const result = await createBudget({
        name: formData.get("name") as string,
        amount: Number(formData.get("amount"))
      });
      return result;
    },
    null
  );

  return (
    <form action={formAction}>
      <input type="text" name="name" placeholder="Budget name" />
      <input type="number" name="amount" placeholder="Amount" />
      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create Budget"}
      </button>
      {state?.success === false && (
        <p className="text-red-500">{state.error}</p>
      )}
    </form>
  );
}
```

## useFormStatus

Provides status information about the parent form's submission.

### Signature

```typescript
const { pending, data, method, action } = useFormStatus();
```

### Returns

- `pending` - Boolean, true if form is submitting
- `data` - FormData being submitted (or null)
- `method` - HTTP method ('get' or 'post')
- `action` - Reference to form's action function

### Critical Rule

**`useFormStatus` must be called from a child component inside the `<form>`**, not from the component that renders the form.

```typescript
// ❌ WRONG - Same component as form
function Form() {
  const { pending } = useFormStatus();  // Will never be true!
  return <form action={submit}><button disabled={pending}>Submit</button></form>;
}

// ✅ CORRECT - Child component inside form
function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? "Submitting..." : "Submit"}</button>;
}

function Form() {
  return (
    <form action={submit}>
      <SubmitButton />  {/* useFormStatus works here */}
    </form>
  );
}
```

### Complete Example

```typescript
"use client";

import { useFormStatus } from "react-dom";
import { useActionState } from "react";

// Child component for submit button
function SubmitButton({ label }: { label: string }) {
  const { pending } = useFormStatus();

  return (
    <button
      type="submit"
      disabled={pending}
      className={pending ? "opacity-50 cursor-not-allowed" : ""}
    >
      {pending ? "Processing..." : label}
    </button>
  );
}

// Child component for form fields
function FormFields() {
  const { pending } = useFormStatus();

  return (
    <fieldset disabled={pending}>
      <input type="text" name="title" placeholder="Title" />
      <textarea name="description" placeholder="Description" />
    </fieldset>
  );
}

// Parent form component
export function CreatePostForm() {
  const [state, formAction] = useActionState(createPost, null);

  return (
    <form action={formAction}>
      <FormFields />
      <SubmitButton label="Create Post" />
      {state?.error && <p className="text-red-500">{state.error}</p>}
    </form>
  );
}
```

## useOptimistic

Enables optimistic UI updates - showing expected result before server confirms.

### Signature

```typescript
const [optimisticState, addOptimistic] = useOptimistic(
  state: State,
  updateFn: (currentState: State, optimisticValue: Value) => State
);
```

### Example

```typescript
"use client";

import { useOptimistic } from "react";
import { likePost } from "~/features/posts/server/actions/like-post";

interface Post {
  id: string;
  likes: number;
  isLiked: boolean;
}

export function LikeButton({ post }: { post: Post }) {
  const [optimisticPost, addOptimisticLike] = useOptimistic(
    post,
    (currentPost, optimisticValue: boolean) => ({
      ...currentPost,
      isLiked: optimisticValue,
      likes: optimisticValue
        ? currentPost.likes + 1
        : currentPost.likes - 1
    })
  );

  async function handleLike() {
    const newLikedState = !optimisticPost.isLiked;

    // Immediately show optimistic update
    addOptimisticLike(newLikedState);

    // Then perform actual action
    await likePost(post.id, newLikedState);
  }

  return (
    <button onClick={handleLike}>
      {optimisticPost.isLiked ? "❤️" : "🤍"} {optimisticPost.likes}
    </button>
  );
}
```

### With Form Actions

```typescript
"use client";

import { useOptimistic, useRef } from "react";
import { addComment } from "~/features/comments/server/actions/add-comment";

interface Comment {
  id: string;
  text: string;
  pending?: boolean;
}

export function CommentSection({ comments }: { comments: Comment[] }) {
  const formRef = useRef<HTMLFormElement>(null);

  const [optimisticComments, addOptimisticComment] = useOptimistic(
    comments,
    (currentComments, newComment: Comment) => [
      ...currentComments,
      { ...newComment, pending: true }
    ]
  );

  async function handleSubmit(formData: FormData) {
    const text = formData.get("text") as string;

    // Add optimistic comment
    addOptimisticComment({
      id: `temp-${Date.now()}`,
      text,
      pending: true
    });

    // Clear form
    formRef.current?.reset();

    // Submit to server
    await addComment({ text });
  }

  return (
    <div>
      <ul>
        {optimisticComments.map(comment => (
          <li
            key={comment.id}
            className={comment.pending ? "opacity-50" : ""}
          >
            {comment.text}
            {comment.pending && <span> (sending...)</span>}
          </li>
        ))}
      </ul>

      <form ref={formRef} action={handleSubmit}>
        <input type="text" name="text" placeholder="Add comment..." />
        <button type="submit">Post</button>
      </form>
    </div>
  );
}
```

## Combining Hooks

### Complete Form Pattern

```typescript
"use client";

import { useActionState, useOptimistic, useRef } from "react";
import { useFormStatus } from "react-dom";
import { addTodo, type Todo } from "~/features/todos/server/actions";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Adding..." : "Add Todo"}
    </button>
  );
}

export function TodoList({ initialTodos }: { initialTodos: Todo[] }) {
  const formRef = useRef<HTMLFormElement>(null);

  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    initialTodos,
    (todos, newTodo: Todo) => [...todos, { ...newTodo, pending: true }]
  );

  const [state, formAction] = useActionState(
    async (prev: null, formData: FormData) => {
      const title = formData.get("title") as string;

      // Optimistic update
      addOptimisticTodo({
        id: `temp-${Date.now()}`,
        title,
        completed: false
      });

      // Reset form
      formRef.current?.reset();

      // Server action
      await addTodo({ title });
      return null;
    },
    null
  );

  return (
    <div>
      <ul>
        {optimisticTodos.map(todo => (
          <li
            key={todo.id}
            className={todo.pending ? "opacity-50 italic" : ""}
          >
            {todo.title}
          </li>
        ))}
      </ul>

      <form ref={formRef} action={formAction}>
        <input type="text" name="title" placeholder="New todo..." required />
        <SubmitButton />
      </form>
    </div>
  );
}
```

## Migration from useTransition

### Before (React 18 Pattern)

```typescript
"use client";

import { useState, useTransition } from "react";

function OldForm() {
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    startTransition(async () => {
      const result = await submitAction(formData);
      if (!result.success) {
        setError(result.error);
      }
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" />
      <button disabled={isPending}>Submit</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

### After (React 19 Pattern)

```typescript
"use client";

import { useActionState } from "react";

function NewForm() {
  const [state, formAction, isPending] = useActionState(
    async (prev, formData: FormData) => {
      const result = await submitAction(formData);
      return result;
    },
    null
  );

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <button disabled={isPending}>Submit</button>
      {state?.error && <p>{state.error}</p>}
    </form>
  );
}
```

Benefits of React 19 pattern:
- No need for `preventDefault()`
- Progressive enhancement (works without JS)
- Cleaner state management
- Built-in pending state
