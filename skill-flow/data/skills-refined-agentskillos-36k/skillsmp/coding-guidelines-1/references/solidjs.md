# SolidJS Patterns

Reference patterns for projects using SolidJS.

## Component Structure

### Props Pattern
Extend JSX HTML attributes for proper typing and prop forwarding:

```tsx
import type { JSX } from "solid-js";

type Props = JSX.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary";
};

const Button = ({ class: classNames = "", ...props }: Props) => (
  <button
    classList={{ btn: true, [classNames]: true }}
    type="button"
    {...props}
  />
);
```

### splitProps for Local vs Pass-through
Use `splitProps` to separate component-specific props from HTML attributes:

```tsx
import { splitProps, type JSX } from "solid-js";

type Props = JSX.InputHTMLAttributes<HTMLInputElement> & {
  error?: string;
  label?: string;
};

const Input = (props: Props) => {
  const [local, rest] = splitProps(props, ["class", "error", "label"]);
  
  return (
    <input
      classList={{
        input: true,
        [local.class ?? ""]: true,
        "input-error": !!local.error,
      }}
      {...rest}
    />
  );
};
```

## Reactive Patterns

### classList for Conditional Classes
Use `classList` object instead of template literals:

```tsx
// Correct - SolidJS pattern
<div classList={{
  "chat": true,
  "chat-start": isAgent,
  "chat-end": !isAgent,
}} />

// Avoid - React pattern (not reactive)
<div class={`chat ${isAgent ? "chat-start" : "chat-end"}`} />
```

### Show for Conditional Rendering
Use `Show` component instead of ternary or &&:

```tsx
import { Show } from "solid-js";

<Show when={error}>
  <p class="text-error">{error}</p>
</Show>

<Show when={isLoading} fallback={<Content />}>
  <LoadingSpinner />
</Show>
```

### For for List Rendering
Use `For` component instead of map:

```tsx
import { For } from "solid-js";

<For each={items}>
  {(item, index) => <li>{index()}: {item.name}</li>}
</For>
```

## Composition Patterns

### Slots Pattern
Use slots object for flexible component composition:

```tsx
import { type JSX, type ParentProps } from "solid-js";

type Props = ParentProps<{
  slots?: {
    header?: JSX.Element;
    footer?: JSX.Element;
  };
}>;

const Card = (props: Props) => (
  <div class="card">
    {props.slots?.header}
    <div class="card-body">{props.children}</div>
    {props.slots?.footer}
  </div>
);
```

### Refs Pattern
Use callback refs for DOM access:

```tsx
import { createEffect } from "solid-js";

const Modal = (props: Props) => {
  let ref: HTMLDialogElement | undefined;

  createEffect(() => {
    props.isOpen ? ref?.showModal() : ref?.close();
  });

  return <dialog ref={ref}>{props.children}</dialog>;
};
```

## Icons

Use Lucide icons with solid-js bindings:

```tsx
import X from "lucide-solid/icons/x";
import Menu from "lucide-solid/icons/menu";

<button>
  <X class="size-4" />
</button>
```
