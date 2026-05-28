# Complete Examples

Full working examples combining all modern patterns: React.FC, lazy loading, Suspense, useSuspenseQuery, styling, routing, and error handling.

---

## Example 1: Complete Modern Component

Combines: React.FC, useSuspenseQuery, cache-first, useCallback, styling, error handling

```typescript
/**
 * User profile display component
 * Demonstrates modern patterns with Suspense and TanStack Query
 */
import React, { useState, useCallback, useMemo } from 'react';
import { useSuspenseQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { Card, CardHeader, CardBody, CardFooter, Button, Spinner } from '@/components/ui';
import { userApi } from '../api/userApi';
import type { User } from '@/types/user';

interface UserProfileProps {
    userId: string;
    onUpdate?: () => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId, onUpdate }) => {
    const queryClient = useQueryClient();
    const [isEditing, setIsEditing] = useState(false);

    // Suspense query - no isLoading needed!
    const { data: user } = useSuspenseQuery({
        queryKey: ['user', userId],
        queryFn: () => userApi.getUser(userId),
        staleTime: 5 * 60 * 1000,
    });

    // Update mutation
    const updateMutation = useMutation({
        mutationFn: (updates: Partial<User>) =>
            userApi.updateUser(userId, updates),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['user', userId] });
            toast.success('Profile updated');
            setIsEditing(false);
            onUpdate?.();
        },

        onError: () => {
            toast.error('Failed to update profile');
        },
    });

    // Memoized computed value
    const fullName = useMemo(() => {
        return `${user.firstName} ${user.lastName}`;
    }, [user.firstName, user.lastName]);

    // Event handlers with useCallback
    const handleEdit = useCallback(() => {
        setIsEditing(true);
    }, []);

    const handleSave = useCallback(() => {
        updateMutation.mutate({
            firstName: user.firstName,
            lastName: user.lastName,
        });
    }, [user, updateMutation]);

    const handleCancel = useCallback(() => {
        setIsEditing(false);
    }, []);

    return (
        <Card variant="elevated" padding="md" className="max-w-2xl mx-auto">
            <CardHeader>
                <div className="flex items-center gap-4">
                    <img
                        src={user.avatarUrl || '/default-avatar.png'}
                        alt={fullName}
                        className="w-16 h-16 rounded-full bg-bg-secondary"
                    />
                    <div>
                        <h2 className="text-2xl font-semibold text-text-heading">{fullName}</h2>
                        <p className="text-text-secondary">{user.email}</p>
                    </div>
                </div>
            </CardHeader>

            <CardBody>
                <div className="flex flex-col gap-2 text-text-primary">
                    <p>Username: {user.username}</p>
                    <p>Roles: {user.roles.join(', ')}</p>
                </div>
            </CardBody>

            <CardFooter>
                <div className="flex gap-2">
                    {!isEditing ? (
                        <Button variant="primary" onClick={handleEdit}>
                            Edit Profile
                        </Button>
                    ) : (
                        <>
                            <Button
                                variant="primary"
                                onClick={handleSave}
                                loading={updateMutation.isPending}
                            >
                                Save
                            </Button>
                            <Button variant="secondary" onClick={handleCancel}>
                                Cancel
                            </Button>
                        </>
                    )}
                </div>
            </CardFooter>
        </Card>
    );
};

export default UserProfile;
```

**Usage:**
```typescript
<Suspense fallback={<Spinner size="lg" />}>
    <UserProfile userId='123' onUpdate={() => console.log('Updated')} />
</Suspense>
```

---

## Example 2: Complete Feature Structure

Real example based on `features/users/`:

```
features/
  users/
    api/
      userApi.ts                # API service layer
    components/
      UserProfile.tsx           # Main component (from Example 1)
      UserList.tsx              # List component
      UserForm.tsx              # Form component
      modals/
        DeleteUserModal.tsx     # Modal component
    hooks/
      useSuspenseUser.ts        # Suspense query hook
      useUserMutations.ts       # Mutation hooks
      useUserPermissions.ts     # Feature-specific hook
    helpers/
      userHelpers.ts            # Utility functions
      validation.ts             # Validation logic
    types/
      index.ts                  # TypeScript interfaces
    index.ts                    # Public API exports
```

### API Service (userApi.ts)

```typescript
import apiClient from '@/lib/apiClient';
import type { User, CreateUserPayload, UpdateUserPayload } from '../types';

export const userApi = {
    getUser: async (userId: string): Promise<User> => {
        const { data } = await apiClient.get(`/users/${userId}`);
        return data;
    },

    getUsers: async (): Promise<User[]> => {
        const { data } = await apiClient.get('/users');
        return data;
    },

    createUser: async (payload: CreateUserPayload): Promise<User> => {
        const { data } = await apiClient.post('/users', payload);
        return data;
    },

    updateUser: async (userId: string, payload: UpdateUserPayload): Promise<User> => {
        const { data } = await apiClient.put(`/users/${userId}`, payload);
        return data;
    },

    deleteUser: async (userId: string): Promise<void> => {
        await apiClient.delete(`/users/${userId}`);
    },
};
```

### Suspense Hook (useSuspenseUser.ts)

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { userApi } from '../api/userApi';
import type { User } from '../types';

export function useSuspenseUser(userId: string) {
    return useSuspenseQuery<User, Error>({
        queryKey: ['user', userId],
        queryFn: () => userApi.getUser(userId),
        staleTime: 5 * 60 * 1000,
        gcTime: 10 * 60 * 1000,
    });
}

export function useSuspenseUsers() {
    return useSuspenseQuery<User[], Error>({
        queryKey: ['users'],
        queryFn: () => userApi.getUsers(),
        staleTime: 1 * 60 * 1000,  // Shorter for list
    });
}
```

### Types (types/index.ts)

```typescript
export interface User {
    id: string;
    username: string;
    email: string;
    firstName: string;
    lastName: string;
    roles: string[];
    createdAt: string;
    updatedAt: string;
}

export interface CreateUserPayload {
    username: string;
    email: string;
    firstName: string;
    lastName: string;
    password: string;
}

export type UpdateUserPayload = Partial<Omit<User, 'id' | 'createdAt' | 'updatedAt'>>;
```

### Public Exports (index.ts)

```typescript
// Export components
export { UserProfile } from './components/UserProfile';
export { UserList } from './components/UserList';

// Export hooks
export { useSuspenseUser, useSuspenseUsers } from './hooks/useSuspenseUser';
export { useUserMutations } from './hooks/useUserMutations';

// Export API
export { userApi } from './api/userApi';

// Export types
export type { User, CreateUserPayload, UpdateUserPayload } from './types';
```

---

## Example 3: Complete Route with Lazy Loading

```typescript
/**
 * User profile route
 * Path: /users/:userId
 */

import { lazy, Suspense } from 'react';
import { useParams } from 'react-router-dom';
import { Spinner } from '@/components/ui';

// Lazy load the UserProfile component
const UserProfile = lazy(() =>
    import('@/features/users/components/UserProfile').then(
        (module) => ({ default: module.UserProfile })
    )
);

export const UserProfilePage = () => {
    const { userId } = useParams<{ userId: string }>();

    if (!userId) {
        return <div>User ID required</div>;
    }

    return (
        <div className="container mx-auto py-6">
            <Suspense fallback={<Spinner size="lg" />}>
                <UserProfile
                    userId={userId}
                    onUpdate={() => console.log('Profile updated')}
                />
            </Suspense>
        </div>
    );
};

export default UserProfilePage;
```

**React Router Setup:**
```typescript
import { Routes, Route } from 'react-router-dom';
import { UserProfilePage } from './pages/UserProfilePage';

function App() {
    return (
        <Routes>
            <Route path="/users/:userId" element={<UserProfilePage />} />
        </Routes>
    );
}
```

---

## Example 4: List with Search and Filtering

```typescript
import React, { useState, useMemo, Suspense } from 'react';
import { useDebounce } from 'use-debounce';
import { useSuspenseQuery } from '@tanstack/react-query';
import { Card, CardBody, Input, Badge } from '@/components/ui';
import { userApi } from '../api/userApi';

export const UserList: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [debouncedSearch] = useDebounce(searchTerm, 300);

    const { data: users } = useSuspenseQuery({
        queryKey: ['users'],
        queryFn: () => userApi.getUsers(),
    });

    // Memoized filtering
    const filteredUsers = useMemo(() => {
        if (!debouncedSearch) return users;

        return users.filter(user =>
            user.name.toLowerCase().includes(debouncedSearch.toLowerCase()) ||
            user.email.toLowerCase().includes(debouncedSearch.toLowerCase())
        );
    }, [users, debouncedSearch]);

    return (
        <div className="space-y-4">
            <Input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search users..."
                label="Search"
            />

            <div className="space-y-2">
                {filteredUsers.length === 0 ? (
                    <Card variant="default" padding="md">
                        <CardBody>
                            <p className="text-center text-text-secondary">
                                No users found
                            </p>
                        </CardBody>
                    </Card>
                ) : (
                    filteredUsers.map(user => (
                        <Card key={user.id} variant="default" padding="sm">
                            <CardBody>
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="font-medium text-text-heading">
                                            {user.name}
                                        </p>
                                        <p className="text-sm text-text-secondary">
                                            {user.email}
                                        </p>
                                    </div>
                                    <Badge variant={user.active ? 'success' : 'warning'}>
                                        {user.active ? 'Active' : 'Inactive'}
                                    </Badge>
                                </div>
                            </CardBody>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
};
```

---

## Example 5: Form with Validation

```typescript
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { Card, CardHeader, CardBody, CardFooter, Input, Button } from '@/components/ui';
import { userApi } from '../api/userApi';

const userSchema = z.object({
    username: z.string().min(3).max(50),
    email: z.string().email(),
    firstName: z.string().min(1),
    lastName: z.string().min(1),
});

type UserFormData = z.infer<typeof userSchema>;

interface CreateUserFormProps {
    onSuccess?: () => void;
}

export const CreateUserForm: React.FC<CreateUserFormProps> = ({ onSuccess }) => {
    const queryClient = useQueryClient();

    const { register, handleSubmit, formState: { errors }, reset } = useForm<UserFormData>({
        resolver: zodResolver(userSchema),
        defaultValues: {
            username: '',
            email: '',
            firstName: '',
            lastName: '',
        },
    });

    const createMutation = useMutation({
        mutationFn: (data: UserFormData) => userApi.createUser(data),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] });
            toast.success('User created successfully');
            reset();
            onSuccess?.();
        },

        onError: () => {
            toast.error('Failed to create user');
        },
    });

    const onSubmit = (data: UserFormData) => {
        createMutation.mutate(data);
    };

    return (
        <Card variant="elevated" padding="md" className="max-w-lg">
            <CardHeader>
                <h2 className="text-xl font-semibold text-text-heading">Create User</h2>
            </CardHeader>

            <form onSubmit={handleSubmit(onSubmit)}>
                <CardBody>
                    <div className="flex flex-col gap-4">
                        <Input
                            {...register('username')}
                            label="Username"
                            error={errors.username?.message}
                        />

                        <Input
                            {...register('email')}
                            label="Email"
                            type="email"
                            error={errors.email?.message}
                        />

                        <Input
                            {...register('firstName')}
                            label="First Name"
                            error={errors.firstName?.message}
                        />

                        <Input
                            {...register('lastName')}
                            label="Last Name"
                            error={errors.lastName?.message}
                        />
                    </div>
                </CardBody>

                <CardFooter>
                    <Button
                        type="submit"
                        variant="primary"
                        loading={createMutation.isPending}
                    >
                        Create User
                    </Button>
                </CardFooter>
            </form>
        </Card>
    );
};

export default CreateUserForm;
```

---

## Example 6: Parallel Data Fetching

```typescript
import React, { Suspense } from 'react';
import { useSuspenseQueries } from '@tanstack/react-query';
import { Card, CardHeader, CardBody, Spinner } from '@/components/ui';
import { userApi } from '../api/userApi';
import { statsApi } from '../api/statsApi';
import { activityApi } from '../api/activityApi';

const DashboardContent: React.FC = () => {
    // Fetch all data in parallel with Suspense
    const [statsQuery, usersQuery, activityQuery] = useSuspenseQueries({
        queries: [
            {
                queryKey: ['stats'],
                queryFn: () => statsApi.getStats(),
            },
            {
                queryKey: ['users', 'active'],
                queryFn: () => userApi.getActiveUsers(),
            },
            {
                queryKey: ['activity', 'recent'],
                queryFn: () => activityApi.getRecent(),
            },
        ],
    });

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card variant="elevated" padding="md">
                <CardHeader>
                    <h3 className="text-lg font-semibold text-text-heading">Stats</h3>
                </CardHeader>
                <CardBody>
                    <p className="text-2xl font-bold text-text-primary">
                        {statsQuery.data.total}
                    </p>
                    <p className="text-sm text-text-secondary">Total Users</p>
                </CardBody>
            </Card>

            <Card variant="elevated" padding="md">
                <CardHeader>
                    <h3 className="text-lg font-semibold text-text-heading">Active Users</h3>
                </CardHeader>
                <CardBody>
                    <p className="text-2xl font-bold text-text-primary">
                        {usersQuery.data.length}
                    </p>
                    <p className="text-sm text-text-secondary">Currently Online</p>
                </CardBody>
            </Card>

            <Card variant="elevated" padding="md">
                <CardHeader>
                    <h3 className="text-lg font-semibold text-text-heading">Recent Activity</h3>
                </CardHeader>
                <CardBody>
                    <p className="text-2xl font-bold text-text-primary">
                        {activityQuery.data.length}
                    </p>
                    <p className="text-sm text-text-secondary">Events Today</p>
                </CardBody>
            </Card>
        </div>
    );
};

export const Dashboard: React.FC = () => {
    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold text-text-heading mb-6">Dashboard</h1>
            <Suspense fallback={<Spinner size="lg" />}>
                <DashboardContent />
            </Suspense>
        </div>
    );
};

// Usage - no extra Suspense needed!
export default Dashboard;
```

**Benefits:**
- All three queries load in parallel
- Single loading state for all data
- Data becomes available together
- Better user experience than sequential loading

---

## Example 7: Optimistic Updates with UI

```typescript
import React from 'react';
import { useMutation, useQueryClient, useSuspenseQuery } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { Card, CardBody, Button, Badge } from '@/components/ui';
import { userApi } from '../api/userApi';
import type { User } from '../types';

const useToggleUserStatus = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (userId: string) => userApi.toggleStatus(userId),

        // Optimistic update
        onMutate: async (userId) => {
            // Cancel outgoing refetches
            await queryClient.cancelQueries({ queryKey: ['users'] });

            // Snapshot previous value
            const previousUsers = queryClient.getQueryData<User[]>(['users']);

            // Optimistically update UI
            queryClient.setQueryData<User[]>(['users'], (old) => {
                return old?.map(user =>
                    user.id === userId
                        ? { ...user, active: !user.active }
                        : user
                ) || [];
            });

            return { previousUsers };
        },

        // Rollback on error
        onError: (err, userId, context) => {
            queryClient.setQueryData(['users'], context?.previousUsers);
            toast.error('Failed to update user status');
        },

        // Refetch after mutation
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] });
        },

        onSuccess: () => {
            toast.success('User status updated');
        },
    });
};

export const UserStatusList: React.FC = () => {
    const { data: users } = useSuspenseQuery({
        queryKey: ['users'],
        queryFn: () => userApi.getUsers(),
    });

    const toggleStatus = useToggleUserStatus();

    return (
        <div className="space-y-2">
            {users.map(user => (
                <Card key={user.id} variant="default" padding="md">
                    <CardBody>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div>
                                    <p className="font-medium text-text-heading">
                                        {user.name}
                                    </p>
                                    <p className="text-sm text-text-secondary">
                                        {user.email}
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-center gap-3">
                                <Badge variant={user.active ? 'success' : 'warning'}>
                                    {user.active ? 'Active' : 'Inactive'}
                                </Badge>
                                <Button
                                    variant="secondary"
                                    onClick={() => toggleStatus.mutate(user.id)}
                                    loading={toggleStatus.isPending}
                                >
                                    Toggle
                                </Button>
                            </div>
                        </div>
                    </CardBody>
                </Card>
            ))}
        </div>
    );
};
```

**Benefits:**
- UI updates instantly (optimistic)
- Automatic rollback on error
- Background revalidation
- Toast notifications for feedback

---

## Summary

**Key Takeaways:**

1. **Component Pattern**: React.FC + Suspense + useSuspenseQuery
2. **Feature Structure**: Organized subdirectories (api/, components/, hooks/, etc.)
3. **Routing**: React Router with lazy loading and Suspense boundaries
4. **Data Fetching**: useSuspenseQuery with cache-first strategy
5. **Forms**: React Hook Form + Zod validation
6. **Error Handling**: toast notifications + onError callbacks
7. **Performance**: useMemo, useCallback, React.memo, debouncing
8. **Styling**: Tailwind classes + ActionPhase UI components (Card, Button, Input, etc.)
9. **UI Components**: Always use `@/components/ui` for consistent dark mode support

**See other resources for detailed explanations of each pattern.**
