# React Hooks for Server Actions

## Table of Contents

1. [useActionState](#useactionstate)
2. [useFormStatus](#useformstatus)
3. [useTransition](#usetransition)
4. [useOptimistic](#useoptimistic)
5. [React Hook Form Integration](#react-hook-form-integration)
6. [Combined Patterns](#combined-patterns)

---

## useActionState

React 19's `useActionState` hook manages form state and integrates seamlessly with server actions.

### Basic Usage

```typescript
// Server action
// features/posts/server/actions/create-post.ts
"use server";

type CreatePostState = {
  success: boolean;
  error?: string;
  fieldErrors?: Record<string, string[]>;
};

export async function createPost(
  previousState: CreatePostState | null,
  formData: FormData
): Promise<CreatePostState> {
  const title = formData.get("title") as string;

  if (!title || title.length < 3) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: { title: ["Title must be at least 3 characters"] }
    };
  }

  // Create post...
  return { success: true };
}
```

```typescript
// Client component
// features/posts/components/create-post-form.tsx
"use client";

import { useActionState } from "react";
import { createPost } from "../server/actions/create-post";

export function CreatePostForm() {
  const [state, formAction, isPending] = useActionState(createPost, null);

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="title">Title</label>
        <input
          id="title"
          name="title"
          type="text"
          required
          disabled={isPending}
          aria-invalid={!!state?.fieldErrors?.title}
          aria-describedby={state?.fieldErrors?.title ? "title-error" : undefined}
        />
        {state?.fieldErrors?.title && (
          <p id="title-error" className="text-red-500 text-sm">
            {state.fieldErrors.title[0]}
          </p>
        )}
      </div>

      {state?.error && !state.fieldErrors && (
        <p className="text-red-500" role="alert">
          {state.error}
        </p>
      )}

      {state?.success && (
        <p className="text-green-500" role="status">
          Post created successfully!
        </p>
      )}

      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create Post"}
      </button>
    </form>
  );
}
```

### With Initial State

```typescript
"use client";

import { useActionState } from "react";
import { updateSettings } from "../server/actions/settings";

type SettingsState = {
  success: boolean;
  error?: string;
  data?: {
    theme: string;
    notifications: boolean;
  };
};

const initialState: SettingsState = {
  success: false,
  data: {
    theme: "light",
    notifications: true
  }
};

export function SettingsForm() {
  const [state, formAction, isPending] = useActionState(updateSettings, initialState);

  return (
    <form action={formAction}>
      <select
        name="theme"
        defaultValue={state.data?.theme}
        disabled={isPending}
      >
        <option value="light">Light</option>
        <option value="dark">Dark</option>
        <option value="system">System</option>
      </select>

      <label>
        <input
          type="checkbox"
          name="notifications"
          defaultChecked={state.data?.notifications}
          disabled={isPending}
        />
        Enable notifications
      </label>

      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Save Settings"}
      </button>
    </form>
  );
}
```

### Reset Form After Success

```typescript
"use client";

import { useActionState, useRef, useEffect } from "react";
import { createComment } from "../server/actions/comments";

export function CommentForm({ postId }: { postId: string }) {
  const formRef = useRef<HTMLFormElement>(null);
  const [state, formAction, isPending] = useActionState(createComment, null);

  // Reset form on success
  useEffect(() => {
    if (state?.success) {
      formRef.current?.reset();
    }
  }, [state?.success]);

  return (
    <form ref={formRef} action={formAction}>
      <input type="hidden" name="postId" value={postId} />
      <textarea
        name="content"
        placeholder="Write a comment..."
        required
        disabled={isPending}
      />
      <button type="submit" disabled={isPending}>
        {isPending ? "Posting..." : "Post Comment"}
      </button>
    </form>
  );
}
```

---

## useFormStatus

`useFormStatus` provides information about the parent form's submission status.

### Basic Usage

```typescript
"use client";

import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
}

// Usage in form
export function MyForm() {
  return (
    <form action={myServerAction}>
      <input name="email" type="email" required />
      <SubmitButton />
    </form>
  );
}
```

### Loading States

```typescript
"use client";

import { useFormStatus } from "react-dom";

function FormFields() {
  const { pending } = useFormStatus();

  return (
    <>
      <input
        name="name"
        type="text"
        disabled={pending}
        className={pending ? "opacity-50" : ""}
      />
      <input
        name="email"
        type="email"
        disabled={pending}
        className={pending ? "opacity-50" : ""}
      />
    </>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button
      type="submit"
      disabled={pending}
      className="flex items-center gap-2"
    >
      {pending && <Spinner className="h-4 w-4" />}
      {pending ? "Creating account..." : "Create account"}
    </button>
  );
}

export function SignupForm() {
  return (
    <form action={signupAction}>
      <FormFields />
      <SubmitButton />
    </form>
  );
}
```

### Access Form Data During Submission

```typescript
"use client";

import { useFormStatus } from "react-dom";

function SubmitFeedback() {
  const { pending, data } = useFormStatus();

  if (!pending) return null;

  // Access form data during submission
  const email = data?.get("email");

  return (
    <p className="text-gray-500">
      Creating account for {email}...
    </p>
  );
}
```

---

## useTransition

Use `useTransition` for non-form actions or when you need more control.

### Basic Usage

```typescript
"use client";

import { useTransition } from "react";
import { deletePost } from "../server/actions/posts";

export function DeleteButton({ postId }: { postId: string }) {
  const [isPending, startTransition] = useTransition();

  function handleDelete() {
    startTransition(async () => {
      const result = await deletePost(postId);
      if (!result.success) {
        alert(result.error);
      }
    });
  }

  return (
    <button
      onClick={handleDelete}
      disabled={isPending}
      className="text-red-500"
    >
      {isPending ? "Deleting..." : "Delete"}
    </button>
  );
}
```

### With Error Handling

```typescript
"use client";

import { useTransition, useState } from "react";
import { toggleFavorite } from "../server/actions/favorites";

export function FavoriteButton({ itemId, initialFavorited }: {
  itemId: string;
  initialFavorited: boolean;
}) {
  const [isPending, startTransition] = useTransition();
  const [isFavorited, setIsFavorited] = useState(initialFavorited);
  const [error, setError] = useState<string | null>(null);

  function handleToggle() {
    setError(null);

    startTransition(async () => {
      const result = await toggleFavorite(itemId);

      if (result.success) {
        setIsFavorited(result.data.favorited);
      } else {
        setError(result.error);
      }
    });
  }

  return (
    <div>
      <button
        onClick={handleToggle}
        disabled={isPending}
        aria-pressed={isFavorited}
      >
        {isPending ? "..." : isFavorited ? "❤️" : "🤍"}
      </button>
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </div>
  );
}
```

### Multiple Actions

```typescript
"use client";

import { useTransition } from "react";
import { archivePost, deletePost, restorePost } from "../server/actions/posts";

export function PostActions({ postId, isArchived }: {
  postId: string;
  isArchived: boolean;
}) {
  const [isPending, startTransition] = useTransition();

  async function handleAction(action: () => Promise<{ success: boolean; error?: string }>) {
    startTransition(async () => {
      const result = await action();
      if (!result.success) {
        // Handle error (toast, alert, etc.)
        console.error(result.error);
      }
    });
  }

  return (
    <div className="flex gap-2">
      {isArchived ? (
        <button
          onClick={() => handleAction(() => restorePost(postId))}
          disabled={isPending}
        >
          Restore
        </button>
      ) : (
        <button
          onClick={() => handleAction(() => archivePost(postId))}
          disabled={isPending}
        >
          Archive
        </button>
      )}
      <button
        onClick={() => handleAction(() => deletePost(postId))}
        disabled={isPending}
        className="text-red-500"
      >
        Delete
      </button>
    </div>
  );
}
```

---

## useOptimistic

`useOptimistic` provides instant UI feedback while the action executes.

### Toggle Example

```typescript
"use client";

import { useOptimistic, useTransition } from "react";
import { toggleLike } from "../server/actions/likes";

export function LikeButton({ postId, initialLiked, initialCount }: {
  postId: string;
  initialLiked: boolean;
  initialCount: number;
}) {
  const [isPending, startTransition] = useTransition();

  const [optimisticState, setOptimisticState] = useOptimistic(
    { liked: initialLiked, count: initialCount },
    (currentState, newLiked: boolean) => ({
      liked: newLiked,
      count: newLiked ? currentState.count + 1 : currentState.count - 1
    })
  );

  function handleToggle() {
    startTransition(async () => {
      // Optimistically update
      setOptimisticState(!optimisticState.liked);

      // Perform actual action
      const result = await toggleLike(postId);

      if (!result.success) {
        // Error handling - optimistic state will revert automatically
        // on next render since server state doesn't match
        console.error(result.error);
      }
    });
  }

  return (
    <button onClick={handleToggle} disabled={isPending}>
      {optimisticState.liked ? "❤️" : "🤍"} {optimisticState.count}
    </button>
  );
}
```

### List with Optimistic Add

```typescript
"use client";

import { useOptimistic, useTransition, useRef } from "react";
import { addTodo } from "../server/actions/todos";

type Todo = {
  id: string;
  text: string;
  completed: boolean;
};

export function TodoList({ initialTodos }: { initialTodos: Todo[] }) {
  const formRef = useRef<HTMLFormElement>(null);
  const [isPending, startTransition] = useTransition();

  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    initialTodos,
    (state, newTodo: Todo) => [...state, newTodo]
  );

  async function handleSubmit(formData: FormData) {
    const text = formData.get("text") as string;

    // Create optimistic todo
    const optimisticTodo: Todo = {
      id: `temp-${Date.now()}`,
      text,
      completed: false
    };

    startTransition(async () => {
      addOptimisticTodo(optimisticTodo);
      formRef.current?.reset();

      const result = await addTodo(text);

      if (!result.success) {
        // Handle error - list will revert on next server render
        console.error(result.error);
      }
    });
  }

  return (
    <div>
      <form ref={formRef} action={handleSubmit}>
        <input name="text" placeholder="Add todo..." required />
        <button type="submit" disabled={isPending}>
          Add
        </button>
      </form>

      <ul>
        {optimisticTodos.map((todo) => (
          <li
            key={todo.id}
            className={todo.id.startsWith("temp-") ? "opacity-50" : ""}
          >
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## React Hook Form Integration

Integration with React Hook Form for complex forms.

> **Note:** For comprehensive React Hook Form documentation including dynamic fields (useFieldArray), multi-step forms, UI library integration, and advanced patterns, see [react-hook-form.md](./react-hook-form.md).

### Basic Integration

```typescript
// Client component with React Hook Form
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useTransition } from "react";
import { createUserSchema, type CreateUserData } from "../schemas/user";
import { createUser } from "../server/actions/users";

export function UserForm() {
  const [isPending, startTransition] = useTransition();

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
    reset
  } = useForm<CreateUserData>({
    resolver: zodResolver(createUserSchema)
  });

  async function onSubmit(data: CreateUserData) {
    startTransition(async () => {
      const result = await createUser(data);

      if (!result.success) {
        // Set server-side errors
        if (result.fieldErrors) {
          Object.entries(result.fieldErrors).forEach(([field, messages]) => {
            setError(field as keyof CreateUserData, {
              type: "server",
              message: messages[0]
            });
          });
        } else {
          setError("root", { message: result.error });
        }
      } else {
        reset();
        // Handle success (toast, redirect, etc.)
      }
    });
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          {...register("name")}
          disabled={isPending}
          aria-invalid={!!errors.name}
        />
        {errors.name && (
          <p className="text-red-500 text-sm">{errors.name.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register("email")}
          disabled={isPending}
          aria-invalid={!!errors.email}
        />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}
      </div>

      {errors.root && (
        <p className="text-red-500" role="alert">
          {errors.root.message}
        </p>
      )}

      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create User"}
      </button>
    </form>
  );
}
```

### With Server Action Callback

```typescript
// Page component passing bound action to form
// app/users/new/page.tsx
import { UserForm } from "~/features/users/components/user-form";
import { createUser } from "~/features/users/server/actions/users";
import type { CreateUserData } from "~/features/users/schemas/user";

export default function NewUserPage() {
  async function handleCreate(data: CreateUserData) {
    "use server";
    return await createUser(data);
  }

  return <UserForm onSubmitAction={handleCreate} />;
}
```

```typescript
// Client component accepting action as prop
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useTransition } from "react";
import { createUserSchema, type CreateUserData } from "../schemas/user";
import type { ActionResponse } from "~/lib/action-types";
import type { User } from "../types/user";

type UserFormProps = {
  onSubmitAction: (data: CreateUserData) => ActionResponse<User>;
  defaultValues?: Partial<CreateUserData>;
};

export function UserForm({ onSubmitAction, defaultValues }: UserFormProps) {
  const [isPending, startTransition] = useTransition();

  const form = useForm<CreateUserData>({
    resolver: zodResolver(createUserSchema),
    defaultValues
  });

  async function onSubmit(data: CreateUserData) {
    startTransition(async () => {
      const result = await onSubmitAction(data);

      if (!result.success) {
        form.setError("root", { message: result.error });
      }
      // Success handled by redirect in action
    });
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

---

## Combined Patterns

### Form with Multiple Actions

```typescript
"use client";

import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { saveDraft, publishPost } from "../server/actions/posts";

function FormButtons() {
  const { pending } = useFormStatus();

  return (
    <div className="flex gap-2">
      <button
        type="submit"
        name="action"
        value="draft"
        disabled={pending}
        className="bg-gray-200"
      >
        Save Draft
      </button>
      <button
        type="submit"
        name="action"
        value="publish"
        disabled={pending}
        className="bg-blue-500 text-white"
      >
        Publish
      </button>
    </div>
  );
}

async function handleSubmit(
  prevState: { success: boolean; error?: string } | null,
  formData: FormData
) {
  const action = formData.get("action");

  if (action === "draft") {
    return await saveDraft(prevState, formData);
  } else {
    return await publishPost(prevState, formData);
  }
}

export function PostEditor() {
  const [state, formAction] = useActionState(handleSubmit, null);

  return (
    <form action={formAction}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Write your post..." required />

      {state?.error && (
        <p className="text-red-500">{state.error}</p>
      )}

      <FormButtons />
    </form>
  );
}
```

### Form with Confirmation

```typescript
"use client";

import { useTransition, useState } from "react";
import { deleteAccount } from "../server/actions/account";

export function DeleteAccountButton() {
  const [isPending, startTransition] = useTransition();
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleDelete() {
    setError(null);

    startTransition(async () => {
      const result = await deleteAccount();

      if (!result.success) {
        setError(result.error);
        setShowConfirm(false);
      }
      // On success, user will be redirected by the action
    });
  }

  if (!showConfirm) {
    return (
      <button
        onClick={() => setShowConfirm(true)}
        className="text-red-500"
      >
        Delete Account
      </button>
    );
  }

  return (
    <div className="p-4 border border-red-500 rounded">
      <p className="text-red-500 font-bold">Are you sure?</p>
      <p className="text-sm text-gray-500">
        This action cannot be undone.
      </p>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      <div className="flex gap-2 mt-4">
        <button
          onClick={() => setShowConfirm(false)}
          disabled={isPending}
        >
          Cancel
        </button>
        <button
          onClick={handleDelete}
          disabled={isPending}
          className="bg-red-500 text-white"
        >
          {isPending ? "Deleting..." : "Yes, Delete"}
        </button>
      </div>
    </div>
  );
}
```

### Inline Editing

```typescript
"use client";

import { useTransition, useState, useRef, useEffect } from "react";
import { updateTitle } from "../server/actions/posts";

export function EditableTitle({ postId, initialTitle }: {
  postId: string;
  initialTitle: string;
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(initialTitle);
  const [isPending, startTransition] = useTransition();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
      inputRef.current?.select();
    }
  }, [isEditing]);

  async function handleSave() {
    if (title === initialTitle) {
      setIsEditing(false);
      return;
    }

    startTransition(async () => {
      const result = await updateTitle(postId, title);

      if (result.success) {
        setIsEditing(false);
      } else {
        // Revert on error
        setTitle(initialTitle);
        alert(result.error);
      }
    });
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter") {
      handleSave();
    } else if (e.key === "Escape") {
      setTitle(initialTitle);
      setIsEditing(false);
    }
  }

  if (!isEditing) {
    return (
      <h1
        onClick={() => setIsEditing(true)}
        className="cursor-pointer hover:bg-gray-100 p-1 rounded"
      >
        {title}
      </h1>
    );
  }

  return (
    <input
      ref={inputRef}
      value={title}
      onChange={(e) => setTitle(e.target.value)}
      onBlur={handleSave}
      onKeyDown={handleKeyDown}
      disabled={isPending}
      className="text-2xl font-bold w-full p-1"
    />
  );
}
```
