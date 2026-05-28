---
name: react-engineering
description: React best practices and patterns for building maintainable, performant applications with modern React features
---

# React Engineering Best Practices

This skill covers modern React patterns and best practices for building high-quality applications.

## Core Principles

- **Composition over inheritance**: Build with components
- **Unidirectional data flow**: Props down, events up
- **Declarative UI**: Describe what, not how
- **Single responsibility**: One component, one job
- **Immutability**: Don't mutate state
- **Side effects isolation**: Keep them contained

## Component Patterns

### Pattern 1: Functional Components

Always use functional components:

```typescript
// ✅ Do: Functional component
export function UserCard({ user }: { user: User }) {
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}

// ❌ Don't: Class component
class UserCard extends React.Component {
  render() {
    return <div>...</div>;
  }
}
```

### Pattern 2: Component Composition

Break down complex components:

```typescript
// ✅ Do: Compose smaller components
export function PostCard({ post }: { post: Post }) {
  return (
    <article>
      <PostHeader post={post} />
      <PostContent content={post.content} />
      <PostFooter likes={post.likes} comments={post.comments} />
    </article>
  );
}

function PostHeader({ post }: { post: Post }) {
  return (
    <header>
      <h2>{post.title}</h2>
      <PostMeta author={post.author} date={post.createdAt} />
    </header>
  );
}

// ❌ Don't: Monolithic component
export function PostCard({ post }: { post: Post }) {
  return (
    <article>
      <header>
        <h2>{post.title}</h2>
        <div>
          <img src={post.author.avatar} />
          <span>{post.author.name}</span>
          <time>{post.createdAt}</time>
        </div>
      </header>
      {/* 100 more lines... */}
    </article>
  );
}
```

### Pattern 3: Props Interface

Use TypeScript for props:

```typescript
// ✅ Do: Explicit props interface
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

export function Button({
  children,
  onClick,
  variant = "primary",
  disabled = false
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  );
}

// Usage with full type safety
<Button onClick={() => console.log("clicked")} variant="primary">
  Click me
</Button>
```

## State Management

### Pattern 1: useState

For local component state:

```typescript
export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)}>Decrement</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

**Functional updates for derived state:**

```typescript
// ✅ Do: Use functional update
setCount((prev) => prev + 1);

// ❌ Don't: Use stale state
setCount(count + 1); // May be wrong if count changes
```

### Pattern 2: useReducer

For complex state logic:

```typescript
type State = {
  items: Item[];
  filter: string;
  sortBy: "name" | "date";
};

type Action =
  | { type: "ADD_ITEM"; item: Item }
  | { type: "REMOVE_ITEM"; id: string }
  | { type: "SET_FILTER"; filter: string }
  | { type: "SET_SORT"; sortBy: "name" | "date" };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "ADD_ITEM":
      return { ...state, items: [...state.items, action.item] };
    case "REMOVE_ITEM":
      return {
        ...state,
        items: state.items.filter((item) => item.id !== action.id)
      };
    case "SET_FILTER":
      return { ...state, filter: action.filter };
    case "SET_SORT":
      return { ...state, sortBy: action.sortBy };
  }
}

export function ItemList() {
  const [state, dispatch] = useReducer(reducer, {
    items: [],
    filter: "",
    sortBy: "name"
  });

  return (
    <div>
      <input
        value={state.filter}
        onChange={(e) =>
          dispatch({ type: "SET_FILTER", filter: e.target.value })
        }
      />
      {/* ... */}
    </div>
  );
}
```

### Pattern 3: Context for Shared State

```typescript
// Create context
const ThemeContext = createContext<{
  theme: "light" | "dark";
  toggleTheme: () => void;
} | null>(null);

// Provider component
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Custom hook
export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider");
  }
  return context;
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Header />
      <Main />
    </ThemeProvider>
  );
}

function Header() {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className={theme}>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  );
}
```

## Effects and Side Effects

### Pattern 1: useEffect Basics

```typescript
export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Fetch user when userId changes
    async function fetchUser() {
      const data = await getUser(userId);
      setUser(data);
    }
    fetchUser();
  }, [userId]); // Dependency array

  if (!user) return <div>Loading...</div>;

  return <div>{user.name}</div>;
}
```

### Pattern 2: Cleanup Functions

```typescript
export function WebSocketComponent() {
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8080");

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    // Cleanup function
    return () => {
      ws.close();
    };
  }, []); // Empty deps = run once on mount

  return (
    <ul>
      {messages.map((msg, i) => (
        <li key={i}>{msg}</li>
      ))}
    </ul>
  );
}
```

### Pattern 3: Avoid Effect Waterfalls

```typescript
// ❌ Don't: Effect waterfall
function Profile({ userId }) {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(`/users/${userId}`).then(setUser);
  }, [userId]);

  useEffect(() => {
    if (user) {
      fetch(`/posts?author=${user.id}`).then(setPosts);
    }
  }, [user]); // Waits for first effect

  // ...
}

// ✅ Do: Fetch in parallel
function Profile({ userId }) {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    Promise.all([
      fetch(`/users/${userId}`),
      fetch(`/posts?author=${userId}`)
    ]).then(([userData, postsData]) => {
      setUser(userData);
      setPosts(postsData);
    });
  }, [userId]);

  // ...
}
```

## Custom Hooks

### Pattern 1: Extract Reusable Logic

```typescript
// Custom hook for form input
export function useInput(initialValue: string) {
  const [value, setValue] = useState(initialValue);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  };

  const reset = () => setValue(initialValue);

  return {
    value,
    onChange: handleChange,
    reset
  };
}

// Usage
function LoginForm() {
  const email = useInput("");
  const password = useInput("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(email.value, password.value);
    email.reset();
    password.reset();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" {...email} />
      <input type="password" {...password} />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Pattern 2: Data Fetching Hook

```typescript
export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error("Fetch failed");
        const json = await response.json();
        if (!cancelled) {
          setData(json);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      cancelled = true;
    };
  }, [url]);

  return { data, loading, error };
}

// Usage
function Posts() {
  const { data: posts, loading, error } = useFetch<Post[]>("/api/posts");

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!posts) return null;

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

## Performance Optimization

### Pattern 1: useMemo

Memoize expensive calculations:

```typescript
export function ProductList({ products, filter }: Props) {
  // Only recalculate when products or filter changes
  const filteredProducts = useMemo(() => {
    return products.filter((product) =>
      product.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [products, filter]);

  return (
    <ul>
      {filteredProducts.map((product) => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}
```

### Pattern 2: useCallback

Memoize callback functions:

```typescript
export function TodoList({ todos }: { todos: Todo[] }) {
  const [filter, setFilter] = useState("");

  // Memoize callback to prevent child re-renders
  const handleToggle = useCallback((id: string) => {
    toggleTodo(id);
  }, []); // Empty deps if using stable functions

  return (
    <div>
      <input value={filter} onChange={(e) => setFilter(e.target.value)} />
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle} // Same reference across renders
        />
      ))}
    </div>
  );
}
```

### Pattern 3: React.memo

Prevent unnecessary re-renders:

```typescript
// Only re-render if props change
export const TodoItem = React.memo(function TodoItem({
  todo,
  onToggle
}: {
  todo: Todo;
  onToggle: (id: string) => void;
}) {
  return (
    <li>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      {todo.title}
    </li>
  );
});
```

### Pattern 4: Code Splitting

```typescript
// Lazy load components
const Dashboard = lazy(() => import("./Dashboard"));
const Settings = lazy(() => import("./Settings"));

export function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

## Lists and Keys

### Pattern 1: Stable Keys

```typescript
// ✅ Do: Use stable unique IDs
{items.map((item) => (
  <Item key={item.id} item={item} />
))}

// ❌ Don't: Use array index (unstable on reorder)
{items.map((item, index) => (
  <Item key={index} item={item} />
))}

// ❌ Don't: Use random values
{items.map((item) => (
  <Item key={Math.random()} item={item} />
))}
```

## Forms

### Pattern 1: Controlled Components

```typescript
export function ContactForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: ""
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submitForm(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
      />
      <input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
      />
      <textarea
        name="message"
        value={formData.message}
        onChange={handleChange}
      />
      <button type="submit">Send</button>
    </form>
  );
}
```

## Error Boundaries

```typescript
import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <div>Something went wrong</div>;
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <MyComponent />
</ErrorBoundary>
```

## Best Practices

### 1. Component Organization

```typescript
// 1. Imports
import { useState, useEffect } from "react";
import { User } from "../types";
import { getUser } from "../api";

// 2. Types/Interfaces
interface Props {
  userId: string;
}

// 3. Component
export function UserProfile({ userId }: Props) {
  // 4. Hooks
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    getUser(userId).then(setUser);
  }, [userId]);

  // 5. Event handlers
  const handleRefresh = () => {
    getUser(userId).then(setUser);
  };

  // 6. Early returns
  if (!user) return <div>Loading...</div>;

  // 7. Render
  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={handleRefresh}>Refresh</button>
    </div>
  );
}
```

### 2. Naming Conventions

```typescript
// Components: PascalCase
function UserCard() {}

// Hooks: camelCase with "use" prefix
function useUser() {}

// Event handlers: "handle" prefix
const handleClick = () => {};

// Props: descriptive names
interface ButtonProps {
  onClick: () => void;
  isLoading: boolean;
}
```

### 3. Prop Drilling Solutions

```typescript
// ❌ Don't: Prop drill through many layers
<App>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserMenu user={user} />
    </Sidebar>
  </Layout>
</App>

// ✅ Do: Use Context
<UserProvider value={user}>
  <App>
    <Layout>
      <Sidebar>
        <UserMenu /> {/* Uses useUser() hook */}
      </Sidebar>
    </Layout>
  </App>
</UserProvider>
```

## Common Anti-Patterns

❌ **Don't:**
- Mutate state directly
- Use index as key in dynamic lists
- Put side effects in render
- Create components inside components
- Forget cleanup in useEffect
- Use inline functions as props without memo

✅ **Do:**
- Use immutable updates
- Use stable unique keys
- Use useEffect for side effects
- Define components at module level
- Return cleanup functions
- Memoize callbacks passed to children

## Further Reading

- React Docs: https://react.dev/
- React TypeScript Cheatsheet: https://react-typescript-cheatsheet.netlify.app/
- Patterns.dev: https://www.patterns.dev/
