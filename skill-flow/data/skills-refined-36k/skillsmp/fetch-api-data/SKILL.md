---
name: fetch-api-data
description: Generates Query hooks and services for API data fetching and mutations.
---

# Fetch API Data Skill

This skill provides instructions for implementing data fetching and mutations using TanStack Query in the Verseau frontend.

## Tech Stack
- **Library**: `@tanstack/react-query`
- **Framework**: React 19
- **API Client**: Standard `fetch` (or a wrapper if available in the project)
- **Services**: `apps/front/src/services` for reusable business logic and specialized API handlers (e.g., `authService`).

## Core Principles

### 0. Services vs. Hooks
- Use **Services** (`apps/front/src/services`) for raw API calls, authentication logic, or complex data transformations that are independent of the React lifecycle.
- Use **Hooks** (`apps/front/src/hooks`) to wrap these services with TanStack Query, managing loading states and caching within components.

### 1. Custom Hooks
- **ALWAYS** wrap API calls in custom hooks located in `apps/front/src/hooks`.
- Name hooks starting with `use` (e.g., `useProjects`, `useUpdateUser`).

### 2. useQuery for Fetching
- Use `useQuery` for read operations.
- Ensure unique and descriptive `queryKey` arrays.
- Handle loading and error states.

### 3. useMutation for Side Effects
- Use `useMutation` for CREATE, UPDATE, or DELETE operations.
- Implement `onSuccess` callbacks to invalidate related queries using `queryClient.invalidateQueries`.

### 4. Integration with UI
- Use the returned `status`, `isLoading`, `error`, and `data` objects in components.
- Map errors to DSFR `Alert` components or toast notifications.

### 5. Testing
- Hooks **SHOULD** be tested using `@testing-library/react-hooks` or similar.
- Mock the API calls using `vi.fn()` or a mocking library.
- Ensure the hook correctly transitions through states (loading -> success/error).
- Test that mutations correctly trigger invalidations.

## Example: Query Hook

```tsx
import { useQuery } from "@tanstack/react-query";

export const useMyData = (id: string) => {
    return useQuery({
        queryKey: ["myData", id],
        queryFn: async () => {
            const response = await fetch(`/api/data/${id}`);
            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }
            return response.json();
        },
    });
};
```

## Example: Mutation Hook

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

export const useUpdateData = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (newData: any) => {
            const response = await fetch("/api/data", {
                method: "POST",
                body: JSON.stringify(newData),
            });
            return response.json();
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["myData"] });
        },
    });
};
```
