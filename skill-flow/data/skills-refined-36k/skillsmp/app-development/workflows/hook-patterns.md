# React Hook Patterns

Templates and patterns for custom React hooks.

## Basic State Hook

```typescript
// src/hooks/useMyHook.ts
import { useState, useEffect } from "react";

export function useMyHook(initialValue: string) {
  const [value, setValue] = useState(initialValue);

  useEffect(() => {
    // Side effects here
  }, [value]);

  return { value, setValue };
}
```

## Data Fetching Hook

Use React Query for server state:

```typescript
// src/query/my-feature/useMyQuery.ts
import { useQuery } from "@tanstack/react-query";
import { fetchData } from "@actions/my-feature/fetch-data";

export function useMyQuery(id: string) {
  return useQuery({
    queryKey: ["myFeature", id],
    queryFn: () => fetchData(id),
    enabled: !!id, // Only run if id exists
  });
}
```

## Mutation Hook

```typescript
// src/query/my-feature/useMyMutation.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateData } from "@actions/my-feature/update-data";

export function useMyMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateData,
    onSuccess: () => {
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ["myFeature"] });
    },
    onError: (error) => {
      console.error("Mutation failed:", error);
    },
  });
}
```

## Form Hook with Zod Validation

```typescript
// src/hooks/useFormWithValidation.ts
import { useState, useCallback } from "react";
import { z } from "zod";

export function useFormWithValidation<T extends z.ZodType>(
  schema: T,
  initialValues: Partial<z.infer<T>> = {}
) {
  const [values, setValues] = useState<Partial<z.infer<T>>>(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const setValue = useCallback((field: string, value: unknown) => {
    setValues((prev) => ({ ...prev, [field]: value }));
    // Clear error when field changes
    setErrors((prev) => ({ ...prev, [field]: "" }));
  }, []);

  const validate = useCallback(() => {
    const result = schema.safeParse(values);
    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.errors.forEach((err) => {
        const path = err.path.join(".");
        fieldErrors[path] = err.message;
      });
      setErrors(fieldErrors);
      return false;
    }
    setErrors({});
    return true;
  }, [schema, values]);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
  }, [initialValues]);

  return { values, setValue, errors, validate, reset };
}
```

## LocalStorage Hook

```typescript
// src/hooks/useLocalStorage.ts
import { useState, useEffect } from "react";

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;

    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  useEffect(() => {
    if (typeof window === "undefined") return;

    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue] as const;
}
```

## Toggle Hook

```typescript
// src/hooks/useToggle.ts
import { useState, useCallback } from "react";

export function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue((v) => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse };
}
```

## Debounced Value Hook

```typescript
// src/hooks/useDebounce.ts
import { useState, useEffect } from "react";

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

## Best Practices

1. **Naming**: Always prefix with `use`
2. **Single Responsibility**: One hook, one purpose
3. **Return Objects**: Return `{ value, setValue }` not arrays for clarity
4. **Memoization**: Use `useCallback` for functions, `useMemo` for expensive values
5. **TypeScript**: Always type inputs and outputs
6. **Server State**: Use React Query, not useState, for server data
