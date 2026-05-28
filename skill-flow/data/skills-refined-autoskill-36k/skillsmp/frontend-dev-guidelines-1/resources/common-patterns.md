# Common Patterns

Frequently used patterns for forms, authentication, DataGrid, dialogs, and other common UI elements.

---

## Authentication with useAuth

### Getting Current User

```typescript
import { useAuth } from '@/hooks/useAuth';

export const MyComponent: React.FC = () => {
    const { user } = useAuth();

    // Available properties:
    // - user.id: string
    // - user.email: string
    // - user.username: string
    // - user.roles: string[]

    return (
        <div>
            <p>Logged in as: {user.email}</p>
            <p>Username: {user.username}</p>
            <p>Roles: {user.roles.join(', ')}</p>
        </div>
    );
};
```

**NEVER make direct API calls for auth** - always use `useAuth` hook.

---

## Forms with React Hook Form

### Basic Form

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Input, Button } from '@/components/ui';
import { toast } from 'react-hot-toast';

// Zod schema for validation
const formSchema = z.object({
    username: z.string().min(3, 'Username must be at least 3 characters'),
    email: z.string().email('Invalid email address'),
    age: z.number().min(18, 'Must be 18 or older'),
});

type FormData = z.infer<typeof formSchema>;

export const MyForm: React.FC = () => {
    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: '',
            email: '',
            age: 18,
        },
    });

    const onSubmit = async (data: FormData) => {
        try {
            await api.submitForm(data);
            toast.success('Form submitted successfully');
        } catch (error) {
            toast.error('Failed to submit form');
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <Input
                {...register('username')}
                label='Username'
                error={errors.username?.message}
            />

            <Input
                {...register('email')}
                label='Email'
                error={errors.email?.message}
                type='email'
            />

            <Input
                {...register('age', { valueAsNumber: true })}
                label='Age'
                error={errors.age?.message}
                type='number'
            />

            <Button type='submit' variant='primary'>
                Submit
            </Button>
        </form>
    );
};
```

---

## Modal Component Pattern

### Standard Modal Structure

All modals should have:
- Close button (X) in header
- Title (optional)
- Action buttons at bottom
- Backdrop with blur effect

```typescript
import { Modal } from '@/components/Modal';
import { Button, Input } from '@/components/ui';
import { useState } from 'react';

interface MyModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: (data: FormData) => void;
}

export const MyModal: React.FC<MyModalProps> = ({ isOpen, onClose, onConfirm }) => {
    const [formData, setFormData] = useState({ name: '', email: '' });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onConfirm(formData);
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title="Edit Information">
            <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                    label="Name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                />

                <Input
                    label="Email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                />

                <div className="flex justify-end space-x-3 pt-4">
                    <Button type="button" variant="ghost" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button type="submit" variant="primary">
                        Confirm
                    </Button>
                </div>
            </form>
        </Modal>
    );
};
```

### Confirmation Modal Pattern

```typescript
import { Modal } from '@/components/Modal';
import { Button, Alert } from '@/components/ui';

interface ConfirmationModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: () => void;
    title: string;
    message: string;
    confirmText?: string;
    isDestructive?: boolean;
}

export const ConfirmationModal: React.FC<ConfirmationModalProps> = ({
    isOpen,
    onClose,
    onConfirm,
    title,
    message,
    confirmText = 'Confirm',
    isDestructive = false,
}) => {
    return (
        <Modal isOpen={isOpen} onClose={onClose} title={title}>
            <div className="space-y-4">
                {isDestructive && (
                    <Alert variant="warning">
                        This action cannot be undone.
                    </Alert>
                )}

                <p className="text-text-primary">{message}</p>

                <div className="flex justify-end space-x-3 pt-4">
                    <Button variant="ghost" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button
                        variant={isDestructive ? 'danger' : 'primary'}
                        onClick={onConfirm}
                    >
                        {confirmText}
                    </Button>
                </div>
            </div>
        </Modal>
    );
};
```

---

## List/Table Patterns

### Card-Based List Pattern

ActionPhase uses Card components for displaying lists of data:

```typescript
import { Card, CardBody, Badge, Button, Spinner } from '@/components/ui';
import { useSuspenseQuery } from '@tanstack/react-query';

interface ListItem {
    id: number;
    title: string;
    status: 'active' | 'pending' | 'completed';
    description: string;
}

export const ItemsList: React.FC = () => {
    const { data: items } = useSuspenseQuery({
        queryKey: ['items'],
        queryFn: () => api.getItems(),
    });

    return (
        <div className="space-y-4">
            {items.map((item) => (
                <Card key={item.id} variant="default">
                    <CardBody>
                        <div className="flex items-start justify-between">
                            <div className="flex-1">
                                <h3 className="text-lg font-semibold text-text-heading">
                                    {item.title}
                                </h3>
                                <p className="text-text-secondary mt-1">
                                    {item.description}
                                </p>
                            </div>
                            <div className="flex items-center gap-2">
                                <Badge variant={getStatusVariant(item.status)}>
                                    {item.status}
                                </Badge>
                                <Button variant="ghost" size="sm">
                                    View
                                </Button>
                            </div>
                        </div>
                    </CardBody>
                </Card>
            ))}
        </div>
    );
};

function getStatusVariant(status: string): 'success' | 'warning' | 'primary' {
    switch (status) {
        case 'completed': return 'success';
        case 'pending': return 'warning';
        default: return 'primary';
    }
}
```

### Grouped List Pattern

For categorized data:

```typescript
interface GroupedListProps {
    items: Array<{ id: number; category: string; name: string }>;
}

export const GroupedList: React.FC<GroupedListProps> = ({ items }) => {
    // Group items by category
    const grouped = items.reduce((acc, item) => {
        if (!acc[item.category]) acc[item.category] = [];
        acc[item.category].push(item);
        return acc;
    }, {} as Record<string, typeof items>);

    return (
        <div className="space-y-6">
            {Object.entries(grouped).map(([category, categoryItems]) => (
                <div key={category}>
                    <h3 className="text-lg font-semibold text-text-heading mb-3">
                        {category}
                    </h3>
                    <div className="space-y-2">
                        {categoryItems.map((item) => (
                            <Card key={item.id} variant="bordered" padding="sm">
                                <CardBody>
                                    <p className="text-text-primary">{item.name}</p>
                                </CardBody>
                            </Card>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
};
```

### Empty State Pattern

```typescript
import { Card, CardBody, Button } from '@/components/ui';

export const EmptyState: React.FC<{ onAction: () => void }> = ({ onAction }) => {
    return (
        <Card variant="bordered">
            <CardBody>
                <div className="text-center py-12">
                    <p className="text-text-secondary mb-4">
                        No items found
                    </p>
                    <Button variant="primary" onClick={onAction}>
                        Create First Item
                    </Button>
                </div>
            </CardBody>
        </Card>
    );
};
```

---

## Mutation Patterns

### Update with Cache Invalidation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';

export const useUpdateEntity = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: any }) =>
            api.updateEntity(id, data),

        onSuccess: (result, variables) => {
            // Invalidate affected queries
            queryClient.invalidateQueries({ queryKey: ['entity', variables.id] });
            queryClient.invalidateQueries({ queryKey: ['entities'] });

            toast.success('Entity updated');
        },

        onError: () => {
            toast.error('Failed to update entity');
        },
    });
};

// Usage
const updateEntity = useUpdateEntity();

const handleSave = () => {
    updateEntity.mutate({ id: 123, data: { name: 'New Name' } });
};
```

---

## State Management Patterns

### TanStack Query for Server State (PRIMARY)

Use TanStack Query for **all server data**:
- Fetching: useSuspenseQuery
- Mutations: useMutation
- Caching: Automatic
- Synchronization: Built-in

```typescript
// ✅ CORRECT - TanStack Query for server data
const { data: users } = useSuspenseQuery({
    queryKey: ['users'],
    queryFn: () => userApi.getUsers(),
});
```

### useState for UI State

Use `useState` for **local UI state only**:
- Form inputs (uncontrolled)
- Modal open/closed
- Selected tab
- Temporary UI flags

```typescript
// ✅ CORRECT - useState for UI state
const [modalOpen, setModalOpen] = useState(false);
const [selectedTab, setSelectedTab] = useState(0);
```

### Zustand for Global Client State (Minimal)

Use Zustand only for **global client state**:
- Theme preference
- Sidebar collapsed state
- User preferences (not from server)

```typescript
import { create } from 'zustand';

interface AppState {
    sidebarOpen: boolean;
    toggleSidebar: () => void;
}

export const useAppState = create<AppState>((set) => ({
    sidebarOpen: true,
    toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));
```

**Avoid prop drilling** - use context or Zustand instead.

---

## Summary

**Common Patterns:**
- ✅ useAuth hook for current user (id, email, roles, username)
- ✅ React Hook Form + Zod for forms with toast notifications
- ✅ Modal component with close button and backdrop
- ✅ Card-based list patterns for data display
- ✅ Mutations with cache invalidation and toast feedback
- ✅ TanStack Query for server state
- ✅ useState for UI state
- ✅ Zustand for global client state (minimal)

**See Also:**
- [data-fetching.md](data-fetching.md) - TanStack Query patterns
- [component-patterns.md](component-patterns.md) - Component structure
- [loading-and-error-states.md](loading-and-error-states.md) - Error handling
- [styling-guide.md](styling-guide.md) - UI component library reference
