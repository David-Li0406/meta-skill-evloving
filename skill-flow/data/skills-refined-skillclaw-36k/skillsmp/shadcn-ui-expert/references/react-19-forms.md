# React 19 Form Patterns with shadcn/ui (2026)

React 19 simplifies form management through native hooks and Server Actions integration.

## 1. Native Status Handling
Use `useFormStatus` inside shadcn/ui buttons to provide immediate feedback.

```tsx
import { useFormStatus } from "react-dom";
import { Button } from "@/components/ui/button";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button disabled={pending}>
      {pending ? "Submitting..." : "Save"}
    </Button>
  );
}
```

## 2. Server Action State
Combine `useFormState` with Zod validation for robust backend-to-frontend communication.

```tsx
const [state, formAction] = useFormState(myAction, { errors: {} });
// Pass action to <form action={formAction}>
```

## 3. Optimistic Updates
Use `useOptimistic` for instantaneous UI changes during long-running tasks like file uploads or database writes.

---
*Updated: January 23, 2026*
