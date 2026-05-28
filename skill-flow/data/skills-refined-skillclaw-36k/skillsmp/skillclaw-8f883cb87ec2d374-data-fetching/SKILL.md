---
name: data-fetching
description: Use this skill when implementing or debugging any network request, API call, or data fetching, including error handling and caching strategies.
---

# Skill body

## When to Use

Use this skill when:

- Implementing API requests
- Setting up data fetching (React Query, SWR)
- Debugging network failures
- Implementing caching strategies
- Handling offline scenarios
- Authentication/token management
- Configuring API URLs and environment variables

## Preferences

- Avoid axios, prefer expo/fetch

## Common Issues & Solutions

### 1. Basic Fetch Usage

**Simple GET request**:

```tsx
const fetchUser = async (userId: string) => {
  const response = await fetch(`https://api.example.com/users/${userId}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};
```

**POST request with body**:

```tsx
const createUser = async (userData: UserData) => {
  const response = await fetch("https://api.example.com/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }

  return response.json();
};
```

### 2. React Query (TanStack Query)

**Setup**:

```tsx
// app/_layout.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 2,
    },
  },
});

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <Stack />
    </QueryClientProvider>
  );
}
```

**Fetching data**:

```tsx
import { useQuery } from "@tanstack/react-query";

function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Loading />;
  if (error) return <Error message={error.message} />;

  return <Profile user={data} />;
}
```

**Mutations**:

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function CreateUserForm() {
  const queryClient = useQueryClient();
  const mutation = useMutation(createUser, {
    onSuccess: () => {
      queryClient.invalidateQueries('users');
    },
  });

  // Form handling logic here
}
```