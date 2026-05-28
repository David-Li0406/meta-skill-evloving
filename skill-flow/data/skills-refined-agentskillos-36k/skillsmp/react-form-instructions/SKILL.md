---
name: react-form-instructions
description: This guide describes the best practices for creating forms in React using modern hooks (useActionState, useFormStatus) with a component-based architecture that optimizes re-rendering and maintains clean separation of concerns. Use this when asked to create or update forms in "react".
---

# React Form Implementation Guide for AI Agent

## When to use this skill

Use this skill when I say some like this:

- Create or update form with fields [enumeration of fields]. Where [enumeration of fields] are names of fields with types (text, number, checkbox and so on)

## Core Principles

### 1. Form Field Isolation

Each form field must be extracted into a separate component. This ensures:

- Independent re-rendering for each field
- Isolated state management per field
- Prevention of unnecessary parent form re-renders
- Better performance and maintainability

### 2. Hook Usage

- **useActionState**: Manage form submission and server actions
- **useFormStatus**: Track form submission status (pending, errors)
- Custom hooks: Extract all state logic from components

### 3. Data Flow

Form field data must be accessible through the `FormData` parameter in the `useActionState` callback function. All fields should use native HTML input names to ensure data is automatically collected in `FormData`.

## Implementation Pattern

### Type Definitions (types.ts)

```
export type TFormState = {
  errors?: Record<string, string[]>;
  message?: string;
  success?: boolean;
};

export type TEmailFieldProps = {
  defaultValue?: string;
  error?: string[];
};

export type TPasswordFieldProps = {
  error?: string[];
};

export type TSubmitButtonProps = {
  label?: string;
};

export type TLoginFormProps = {
  onSuccess?: () => void;
};
```

### Server Action Example

```
async function loginAction(
  prevState: TFormState,
  formData: FormData
): Promise<TFormState> {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  if (!email || !email.includes("@")) {
    return {
      errors: { email: ["Invalid email address"] },
      success: false,
    };
  }

  if (!password || password.length < 8) {
    return {
      errors: { password: ["Password must be at least 8 characters"] },
      success: false,
    };
  }

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      return {
        message: "Login failed",
        success: false,
      };
    }

    return {
      message: "Login successful",
      success: true,
    };
  } catch (error) {
    return {
      message: "Network error",
      success: false,
    };
  }
}
```

### Custom Hook for Form Logic (useLoginForm.ts)

```
import { useActionState } from "react";

export const useLoginForm = () => {
  const initialState: TFormState = {
    errors: {},
    message: "",
    success: false,
  };

  const [state, formAction] = useActionState(loginAction, initialState);

  return {
    state,
    formAction,
  };
};
```

### Main Form Component (LoginForm.tsx)

```
import { memo } from "react";
import { useLoginForm } from "@/hooks/useLoginForm";
import { EmailField } from "./fields/EmailField";
import { PasswordField } from "./fields/PasswordField";
import { SubmitButton } from "./fields/SubmitButton";

export const LoginForm = memo((props: TLoginFormProps) => {
  const { state, formAction } = useLoginForm();

  return (
    <form action={formAction}>
      <EmailField error={state.errors?.email} defaultValue="" />

      <PasswordField error={state.errors?.password} />

      <SubmitButton label="Login" />

      {state.message && (
        <div className={state.success ? "success" : "error"}>
          {state.message}
        </div>
      )}
    </form>
  );
});
```

### Field Component Example (EmailField.tsx)

```
import { memo } from "react";
import { useEmailField } from "../../hooks/useEmailField";
import { TextField } from "@components/TextField";

export const EmailField = memo((props: TEmailFieldProps) => {
  const { value, handleChange, isTouched, localError } = useEmailField(
    props.defaultValue
  );

  const displayError =
    props.error || (isTouched && localError ? [localError] : undefined);
  const isError = Boolean(displayError);

  return (
    <TextField
      label="Email"
      placeholder="Type something"
      type="email"
      value={value}
      onChange={handleChange}
      isError={isError}
      textError={isError ? displayError.map((error, index) => error + ",") : ""}
      dataTestId="email-field"
    />
  );
});
```

### Field Hook Example (useEmailField.ts)

```
import { useState, useCallback } from "react";

export const useEmailField = (initialValue = "") => {
  const [value, setValue] = useState(initialValue);
  const [isTouched, setIsTouched] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setValue(newValue);
    setIsTouched(true);

    if (!newValue.includes("@")) {
      setLocalError("Invalid email format");
    } else {
      setLocalError(null);
    }
  }, []);

  return {
    value,
    handleChange,
    isTouched,
    localError,
  };
};
```

### Password Field Component (PasswordField.tsx)

```
import { memo, useState, useCallback } from "react";
import { TextField } from "@components/TextField";

export const PasswordField = memo((props: TPasswordFieldProps) => {
  const [value, setValue] = useState("");

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  }, []);
  const isError = Boolean(props.error);

  return (
    <TextField
      label="Password"
      placeholder="Type something"
      type="password"
      value={value}
      onChange={handleChange}
      isError={isError}
      textError={isError ? {props.error.map((error, index) => error + ",") : ""}
      dataTestId="password-field"
    />
  );
});
```

### Submit Button Component (SubmitButton.tsx)

```
import { memo } from "react";
import { useFormStatus } from "react-dom";

export const SubmitButton = memo((props: TSubmitButtonProps) => {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending} aria-busy={pending}>
      {pending ? "Submitting..." : props.label || "Submit"}
    </button>
  );
});
```

## Key Rules

### 1. Component Architecture

- Each field is a separate memoized component
- Use `memo()` to prevent unnecessary re-renders
- Extract field logic to custom hooks
- Keep form component minimal (composition only)

### 2. Data Collection

- Always use `name` attribute on inputs
- Data automatically collected in `FormData`
- Access via `formData.get('fieldName')` in action
- No manual state aggregation needed

### 3. Hook Integration

- `useActionState` for form submission and state
- `useFormStatus` for submit button status
- Custom hooks for field-specific logic
- Separate state management from UI

### 4. Error Handling

- Server errors from action returned in state
- Client-side validation in field hooks
- Display errors at field level
- Use ARIA attributes for accessibility

### 5. TypeScript

- All types in separate `types.ts` file
- Use `type` keyword, not `interface`
- Prefix types with `T` (e.g., `TFormState`)
- Props types: `TComponentNameProps`

### 6. Performance

- Memoize all field components
- Use `useCallback` for event handlers
- Avoid prop drilling with composition
- Let native FormData handle collection

## Advanced Example: Dynamic Field List

```
export type TDynamicFieldProps = {
  index: number;
  onRemove: (index: number) => void;
};

export const DynamicField = memo((props: TDynamicFieldProps) => {
  const [value, setValue] = useState("");

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  }, []);

  const handleRemove = useCallback(() => {
    props.onRemove(props.index);
  }, [props.index, props.onRemove]);

  return (
    <div>
      <input
        type="text"
        name={`items[${props.index}]`}
        value={value}
        onChange={handleChange}
      />
      <button type="button" onClick={handleRemove}>
        Remove
      </button>
    </div>
  );
});
```

## Benefits of This Approach

1. **Performance**: Each field re-renders independently
2. **Maintainability**: Clear separation of concerns
3. **Scalability**: Easy to add new fields
4. **Type Safety**: Full TypeScript coverage
5. **Accessibility**: Built-in ARIA support
6. **Native Web APIs**: Leverages FormData standard
7. **Server Integration**: Seamless with server actions

## Checklist for Implementation

- Create `types.ts` with all form types
- Define server action with FormData parameter
- ate custom hook for form logic (useActionState)
- Build main form component (composition only)
- Extract each field to separate component
- Create custom hooks for field logic
- Add submit button with useFormStatus
- Implement error display
- Add memoization to all components
- Use named exports throughout
- Ensure all inputs have `name` attribute
- Test FormData collection in action

## Common Patterns

### Conditional Field Display

```
export const ConditionalForm = memo((props: TConditionalFormProps) => {
  const { state, formAction } = useConditionalForm();
  const [showExtra, setShowExtra] = useState(false);

  return (
    <form action={formAction}>
      <EmailField error={state.errors?.email} />

      <button type="button" onClick={() => setShowExtra((prev) => !prev)}>
        {showExtra ? "Hide" : "Show"} Extra Fields
      </button>

      {showExtra && <PhoneField error={state.errors?.phone} />}

      <SubmitButton />
    </form>
  );
});
```

### Multi-Step Form

```
export const MultiStepForm = memo((props: TMultiStepFormProps) => {
  const { state, formAction, step, nextStep, prevStep } = useMultiStepForm();

  return (
    <form action={formAction}>
      {step === 1 && <EmailField error={state.errors?.email} />}
      {step === 2 && <PasswordField error={state.errors?.password} />}
      {step === 3 && <ProfileFields errors={state.errors} />}

      <div>
        {step > 1 && (
          <button type="button" onClick={prevStep}>
            Back
          </button>
        )}
        {step < 3 ? (
          <button type="button" onClick={nextStep}>
            Next
          </button>
        ) : (
          <SubmitButton label="Complete Registration" />
        )}
      </div>
    </form>
  );
});
```

## Critical Mistakes to Avoid

### ❌ Inline Arrow Functions

```
<input onChange={(e) => setValue(e.target.value)} />
<button onClick={() => handleAction()}>Click</button>
```

### ✅ Correct: useCallback References

```
const handleChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
}, []);

const handleClick = useCallback(() => {
  handleAction();
}, [handleAction]);

<input onChange={handleChange} />
<button onClick={handleClick}>Click</button>
```

### ❌ Anonymous Functions

```
<select onChange={function(e) { handleSelect(e.target.value); }}>
```

### ✅ Correct: Named useCallback Function

```
const handleSelect = useCallback((e: ChangeEvent<HTMLSelectElement>) => {
  handleSelectValue(e.target.value);
}, [handleSelectValue]);

<select onChange={handleSelect}>
```

This architecture ensures optimal performance, maintainability, and follows React best practices for form handling with modern hooks.
