# TypeScript with React

TypeScript adds type safety to React applications, catching errors at compile time.

## Component Types

### Function Components

```tsx
// Props interface
type ButtonProps = {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
  disabled?: boolean;
};

// Component
export function Button({ children, variant = 'primary', onClick, disabled }: ButtonProps) {
  return (
    <button className={variant} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

// With generics
type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
};

export function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map((item, i) => <li key={i}>{renderItem(item)}</li>)}</ul>;
}
```

### Event Handlers

```tsx
// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// Click events
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.currentTarget);
};
```

## Hooks TypeScript Patterns

### useState

```tsx
// Inferred type
const [count, setCount] = useState(0); // number

// Explicit type
const [user, setUser] = useState<User | null>(null);

// With initial value
const [items, setItems] = useState<string[]>([]);
```

### useRef

```tsx
// DOM ref
const inputRef = useRef<HTMLInputElement>(null);

// Mutable value
const countRef = useRef<number>(0);
```

### useContext

```tsx
type AuthContextType = {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Custom Hooks

```tsx
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  const setValue = (value: T) => {
    setStoredValue(value);
    localStorage.setItem(key, JSON.stringify(value));
  };

  return [storedValue, setValue];
}
```

## React Query Types

```tsx
// Query
export function useUser(userId: string) {
  return useQuery<User, Error>({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
  });
}

// Mutation
export function useCreateUser() {
  return useMutation<User, Error, CreateUserInput>({
    mutationFn: createUser,
  });
}
```

## Children Types

```tsx
// ReactNode - anything renderable
type Props = {
  children: React.ReactNode;
};

// Specific child type
type Props = {
  children: React.ReactElement<ChildProps>;
};

// Render prop
type Props = {
  render: (data: Data) => React.ReactNode;
};
```

## Utility Types

```tsx
// Extract component props
type ButtonProps = React.ComponentProps<typeof Button>;

// HTML element props
type DivProps = React.HTMLAttributes<HTMLDivElement>;
type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

// Omit/Pick props
type CustomButtonProps = Omit<ButtonProps, 'onClick'> & {
  onCustomClick: () => void;
};
```

TypeScript catches errors early and improves IDE autocomplete. Always type your props, state, and API responses.
