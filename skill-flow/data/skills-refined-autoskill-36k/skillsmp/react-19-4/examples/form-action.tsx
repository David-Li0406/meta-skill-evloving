// Server Action with useActionState for forms

// action.ts
"use server";

type State = { message: string; error?: string };

async function submitForm(prev: State, formData: FormData): Promise<State> {
  const name = formData.get("name") as string;
  await db.greetings.create({ name });
  return { message: `Hello, ${name}!` };
}

// form.tsx
("use client");

import { useActionState, useOptimistic } from "react";

function GreetingForm() {
  const [state, formAction, isPending] = useActionState(submitForm, { message: "" });

  const [optimisticState, addOptimistic] = useOptimistic(
    state,
    (current, optimisticMessage: string) => ({ ...current, message: optimisticMessage })
  );

  return (
    <form
      action={(formData) => {
        addOptimistic(`Hello, ${formData.get("name")}!`);
        formAction(formData);
      }}
    >
      <input name="name" required />
      <button disabled={isPending}>{isPending ? "Submitting..." : "Greet"}</button>
      <p>{optimisticState.message}</p>
    </form>
  );
}

// Types for example
declare const db: { greetings: { create: (data: { name: string }) => Promise<void> } };
export { submitForm, GreetingForm };
