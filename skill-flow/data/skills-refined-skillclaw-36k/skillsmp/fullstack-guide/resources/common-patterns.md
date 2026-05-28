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
import { TextField, Button } from '@mui/material';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

// Zod schema for validation
const formSchema = z.object({
    username: z.string().min(3, 'Username must be at least 3 characters'),
    email: z.string().email('Invalid email address'),
});

type FormData = z.infer<typeof formSchema>;

export const MyForm: React.FC = () => {
    const { showSnackbar } = useMuiSnackbar();
    
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<FormData>({
        resolver: zodResolver(formSchema),
    });

    const onSubmit = async (data: FormData) => {
        try {
            await submitData(data);
            showSnackbar('Success!', 'success');
        } catch (error) {
            showSnackbar('Error occurred', 'error');
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <TextField
                {...register('username')}
                error={!!errors.username}
                helperText={errors.username?.message}
            />
            <TextField
                {...register('email')}
                error={!!errors.email}
                helperText={errors.email?.message}
            />
            <Button type="submit">Submit</Button>
        </form>
    );
};
```

---

## Dialogs

### Standard Dialog Pattern

```typescript
import { Dialog, DialogTitle, DialogContent, DialogActions, IconButton, Button } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

interface MyDialogProps {
    open: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
}

export const MyDialog: React.FC<MyDialogProps> = ({ open, onClose, title, children }) => {
    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                {title}
                <IconButton onClick={onClose} size="small">
                    <CloseIcon />
                </IconButton>
            </DialogTitle>
            <DialogContent dividers>
                {children}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button variant="contained" onClick={onClose}>Confirm</Button>
            </DialogActions>
        </Dialog>
    );
};
```

---

## State Management

### TanStack Query for Server State

```typescript
// Use TanStack Query for ALL server state
const { data } = useSuspenseQuery({
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

---

## Summary

**Common Patterns:**
- ✅ useAuth hook for current user
- ✅ React Hook Form + Zod for forms
- ✅ Dialog with icon + close button
- ✅ TanStack Query for server state
- ✅ useState for UI state
- ✅ Zustand for global client state (minimal)

**See Also:**
- [data-fetching.md](data-fetching.md) - TanStack Query patterns
- [component-patterns.md](component-patterns.md) - Component structure
- [loading-and-error-states.md](loading-and-error-states.md) - Error handling
