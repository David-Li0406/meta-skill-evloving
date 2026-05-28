---
name: react-dev
description: Use this skill when building typed React components with TypeScript, implementing generic components, or utilizing React 19 features and routing integrations.
---

# React TypeScript

Type-safe React = compile-time guarantees = confident refactoring.

<when_to_use>

- Building typed React components
- Implementing generic components
- Typing event handlers, forms, refs
- Using React 19 features (Actions, Server Components, use())
- Router integration (TanStack Router, React Router)
- Custom hooks with proper typing

NOT for: non-React TypeScript, vanilla JS React

</when_to_use>

<react_19_changes>

React 19 breaking changes require migration. Key patterns:

**ref as prop** - forwardRef deprecated:

```typescript
// React 19 - ref as regular prop
type ButtonProps = {
  ref?: React.Ref<HTMLButtonElement>;
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ ref, children, ...props }: ButtonProps) {
  return <button ref={ref} {...props}>{children}</button>;
}
```

**useActionState** - replaces useFormState:

```typescript
import { useActionState } from 'react';

type FormState = { errors?: string[]; success?: boolean };

function Form() {
  const [state, formAction, isPending] = useActionState(submitAction, {});
  return <form action={formAction}>...</form>;
}
```

**use()** - unwraps promises/context:

```typescript
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspends until resolved
  return <div>{user.name}</div>;
}
```

See [react-19-patterns.md](references/react-19-patterns.md) for useOptimistic, useTransition, migration checklist.

</react_19_changes>

<component_patterns>

**Props** - extend native elements:

```typescript
type ButtonProps = {
  variant: 'primary' | 'secondary';
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ variant, children, ...props }: ButtonProps) {
  return <button className={variant} {...props}>{children}</button>;
}
```

**Children typing**:

```typescript
type Props = {
  children: React.ReactNode;          // Anything renderable
  icon: React.ReactElement;           // Single element
  render: (data: T) => React.ReactNode;  // Render prop
};
```

**Discriminated unions** for variant props:

```typescript
type ButtonProps =
  | { variant: 'link'; href: string }
  | { variant: 'button'; onClick: () => void };
```

</component_patterns>