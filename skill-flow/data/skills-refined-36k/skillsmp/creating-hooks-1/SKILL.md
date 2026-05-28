---
name: creating-hooks
description: Create custom React hooks with TypeScript for reusable logic and side effects. Use when creating hooks, extracting component logic, managing side effects, or when user mentions custom hooks, reusable logic, or use- prefix functions.
---

# Create Custom React Hooks

Create custom hooks that encapsulate reusable logic and side effects with TypeScript. Hooks extract common patterns from components, providing clean abstractions for data fetching, form handling, and browser API interactions.

## File Structure

Hooks are organized in a flat structure:

```
resources/js/hooks/use-{name}.ts
```

**Examples:**

- `resources/js/hooks/use-form-validation.ts`
- `resources/js/hooks/use-mobile.ts`
- `resources/js/hooks/use-debounce.ts`

## Core Conventions

### 1. Hook Structure

Hooks must follow these patterns:

```ts
import { useState, useEffect } from 'react'

export function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  })

  useEffect(() => {
    function handleResize() {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      })
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return size
}
```

**Key Requirements:**

- Prefix hook name with `use`
- Use function declarations for hooks (NOT arrow functions assigned to const)
- Always return a value (object, array, primitive, or function)
- Use TypeScript for parameter and return types
- Clean up side effects in `useEffect` return function
- Named export (not default export)

### 2. Function Declaration Style

**Always use function declarations for hooks:**

```ts
// ✅ Correct: Function declaration
export function useToggle(initialValue: boolean = false) {
  const [value, setValue] = useState(initialValue)

  function toggle() {
    setValue((prev) => !prev)
  }

  return { value, toggle }
}
```

**Use function declarations for helper functions within hooks:**

```ts
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    // ✅ Function declaration for helpers
    function updateValue() {
      setDebouncedValue(value)
    }

    const handler = setTimeout(updateValue, delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}
```

This pattern makes it clear what is a function versus a variable, improving code readability and maintainability.

### 3. Hook Return Types

**Return object with named properties:**

```ts
interface UseToggleReturn {
  value: boolean
  toggle: () => void
  setTrue: () => void
  setFalse: () => void
}

export function useToggle(initialValue: boolean = false): UseToggleReturn {
  const [value, setValue] = useState(initialValue)

  const toggle = () => setValue((prev) => !prev)
  const setTrue = () => setValue(true)
  const setFalse = () => setValue(false)

  return { value, toggle, setTrue, setFalse }
}
```

**Return tuple for useState-like hooks:**

```ts
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      return initialValue
    }
  })

  const setValue = (value: T) => {
    try {
      setStoredValue(value)
      window.localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue]
}
```

### 4. Hooks with Dependencies

Accept parameters and use in dependencies:

```ts
import { useEffect, useState } from 'react'

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}
```

### 5. Hooks Using Other Hooks

Compose custom hooks together:

```ts
import { useTranslation } from 'react-i18next'
import type { FieldValues, Path, UseFormReturn } from 'react-hook-form'
import { z } from 'zod'

export function useFormValidation() {
  const { t } = useTranslation()

  const passwordConfirmationMessage: z.core.$ZodCustomParams = {
    message: t('validation:confirmed', {
      attribute: t('password').toLowerCase(),
    }),
    path: ['password'],
  }

  function setFormServerErrors<T extends FieldValues>(
    form: UseFormReturn<T>,
    errors: Record<string, string>
  ): void {
    Object.entries(errors).forEach(([key, message]) => {
      form.setError(key as Path<T>, {
        type: 'server',
        message: message,
      })
    })
  }

  return { passwordConfirmationMessage, setFormServerErrors }
}
```

## Examples

### Example 1: Simple State Hook

```ts
import { useState } from 'react'

interface UseDisclosureReturn {
  isOpen: boolean
  open: () => void
  close: () => void
  toggle: () => void
}

export function useDisclosure(
  initialState: boolean = false
): UseDisclosureReturn {
  const [isOpen, setIsOpen] = useState(initialState)

  const open = () => setIsOpen(true)
  const close = () => setIsOpen(false)
  const toggle = () => setIsOpen((prev) => !prev)

  return { isOpen, open, close, toggle }
}
```

Usage:

```tsx
function Modal() {
  const { isOpen, open, close } = useDisclosure()

  return (
    <>
      <Button onClick={open}>Open Modal</Button>
      {isOpen && <ModalContent onClose={close} />}
    </>
  )
}
```

### Example 2: Hook with Side Effects

```ts
import { useEffect, useState } from 'react'

export function useMobile(breakpoint: number = 768): boolean {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < breakpoint)
    }

    // Initial check
    checkMobile()

    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [breakpoint])

  return isMobile
}
```

Usage:

```tsx
function Navigation() {
  const isMobile = useMobile()

  return isMobile ? <MobileNav /> : <DesktopNav />
}
```

### Example 3: Data Fetching Hook

```ts
import { useEffect, useState } from 'react'

interface UseAsyncReturn<T> {
  data: T | null
  loading: boolean
  error: Error | null
}

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate: boolean = true
): UseAsyncReturn<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState<boolean>(immediate)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    if (!immediate) return

    let isCancelled = false

    async function fetchData() {
      setLoading(true)
      setError(null)

      try {
        const result = await asyncFunction()
        if (!isCancelled) {
          setData(result)
        }
      } catch (err) {
        if (!isCancelled) {
          setError(err as Error)
        }
      } finally {
        if (!isCancelled) {
          setLoading(false)
        }
      }
    }

    fetchData()

    return () => {
      isCancelled = true
    }
  }, [asyncFunction, immediate])

  return { data, loading, error }
}
```

Usage:

```tsx
function UserProfile({ userId }: { userId: number }) {
  const { data, loading, error } = useAsync(() =>
    fetch(`/api/users/${userId}`).then((r) => r.json())
  )

  if (loading) return <Spinner />
  if (error) return <Error message={error.message} />
  if (!data) return null

  return <Profile user={data} />
}
```

## Anti-Patterns

### ❌ Don't Do This

```ts
// Don't use arrow functions assigned to const
export const useToggle = (initialValue: boolean = false) => {
  // ❌ Use function declaration
  const [value, setValue] = useState(initialValue)
  return { value, toggle: () => setValue(!value) }
}

// Don't return void from hooks
export function useLogger(message: string): void {
  console.log(message) // ❌ Should return something
}

// Don't forget TypeScript types
export function useDebounce(value, delay) {
  // ❌ No types
  const [debouncedValue, setDebouncedValue] = useState(value)
  // ...
}

// Don't use default exports
export default function useToggle() {} // ❌ Use named export

// Don't create hooks without the use prefix
export function toggle() {} // ❌ Should be useToggle

// Don't forget to clean up side effects
export function useInterval(callback: () => void, delay: number) {
  useEffect(() => {
    const id = setInterval(callback, delay)
    // ❌ Missing cleanup
  }, [callback, delay])
}
```

### ✅ Do This Instead

```ts
// Always return a value
export function useLogger(message: string): void {
  useEffect(() => {
    console.log(message)
  }, [message])
}

// Use TypeScript types
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)
  // ...
}

// Use named exports
export function useToggle() {}

// Always use the use prefix
export function useToggle() {}

// Always clean up side effects
export function useInterval(callback: () => void, delay: number) {
  useEffect(() => {
    const id = setInterval(callback, delay)
    return () => clearInterval(id) // ✅ Cleanup
  }, [callback, delay])
}
```

## Hook Composition

Combine multiple hooks for complex logic:

```ts
export function useForm<T>() {
  const { t } = useTranslation()
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const isMobile = useMobile()

  // ... form logic

  return { errors, loading, isMobile, submit, reset }
}
```

## Quality Standards

- All hooks must have TypeScript types for parameters and return values
- Use ESLint React hooks rules (exhaustive-deps)
- Clean up side effects (event listeners, timers, subscriptions)
- **When hooks return user-facing messages, use `useTranslation()` for i18n support**
- Document hook purpose and usage with JSDoc comments
- Keep hooks focused and single-purpose
- Test hooks with Pest browser tests or React Testing Library
- Always return a value (never `void` unless absolutely necessary)
