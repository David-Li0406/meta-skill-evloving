# TypeScript Anti-Patterns

Common anti-patterns to identify during TypeScript/React code review.

## Critical Anti-Patterns

### 1. Missing useEffect Dependencies

```typescript
// ANTI-PATTERN
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []);  // Missing userId - will use stale closure

  return <div>{user?.name}</div>;
}

// CORRECT
useEffect(() => {
  fetchUser(userId).then(setUser);
}, [userId]);  // All dependencies listed
```

### 2. Using 'any' Type

```typescript
// ANTI-PATTERN
function processData(data: any): any {
  return data.items.map((item: any) => item.value);
}

// CORRECT
interface DataItem {
  id: string;
  value: number;
}

interface DataResponse {
  items: DataItem[];
}

function processData(data: DataResponse): number[] {
  return data.items.map((item) => item.value);
}
```

### 3. Unhandled Promise Rejections

```typescript
// ANTI-PATTERN
async function fetchData() {
  const response = await fetch(url);  // Could throw
  return response.json();  // Could throw
}

// CORRECT
async function fetchData(): Promise<Data | null> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    return null;
  }
}
```

### 4. Memory Leaks in useEffect

```typescript
// ANTI-PATTERN
useEffect(() => {
  const subscription = eventEmitter.subscribe(handler);
  // No cleanup - memory leak!
}, []);

// CORRECT
useEffect(() => {
  const subscription = eventEmitter.subscribe(handler);
  return () => subscription.unsubscribe();  // Cleanup
}, []);
```

## High Priority Anti-Patterns

### 5. Type Assertions Overuse

```typescript
// ANTI-PATTERN
const user = JSON.parse(data) as User;  // No validation

// CORRECT
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}

const parsed = JSON.parse(data);
if (isUser(parsed)) {
  // Safe to use as User
}
```

### 6. Mutating State Directly

```typescript
// ANTI-PATTERN
function addItem(item: Item) {
  state.items.push(item);  // Direct mutation
  setState(state);
}

// CORRECT
function addItem(item: Item) {
  setState((prev) => ({
    ...prev,
    items: [...prev.items, item],
  }));
}
```

### 7. Object Identity Issues

```typescript
// ANTI-PATTERN - creates new object every render
function Component() {
  return <Child style={{ color: 'red' }} />;  // New object each render
}

// CORRECT - stable reference
const style = { color: 'red' } as const;

function Component() {
  return <Child style={style} />;
}

// Or with useMemo for dynamic values
function Component({ color }: { color: string }) {
  const style = useMemo(() => ({ color }), [color]);
  return <Child style={style} />;
}
```

### 8. Prop Drilling

```typescript
// ANTI-PATTERN - passing props through many levels
function App() {
  const [user, setUser] = useState<User | null>(null);
  return <Layout user={user} setUser={setUser} />;
}

function Layout({ user, setUser }) {
  return <Header user={user} setUser={setUser} />;
}

function Header({ user, setUser }) {
  return <UserMenu user={user} setUser={setUser} />;
}

// CORRECT - use context
const UserContext = createContext<UserContextValue | null>(null);

function App() {
  return (
    <UserProvider>
      <Layout />
    </UserProvider>
  );
}

function UserMenu() {
  const { user, setUser } = useUser();  // From context
}
```

## Medium Priority Anti-Patterns

### 9. Index as Key

```typescript
// ANTI-PATTERN
{items.map((item, index) => (
  <Item key={index} data={item} />  // Index as key
))}

// CORRECT
{items.map((item) => (
  <Item key={item.id} data={item} />  // Stable ID as key
))}
```

### 10. Inline Function in JSX

```typescript
// ANTI-PATTERN - creates new function every render
<button onClick={() => handleClick(id)}>Click</button>

// CORRECT - useCallback for stable reference
const handleButtonClick = useCallback(() => {
  handleClick(id);
}, [id, handleClick]);

<button onClick={handleButtonClick}>Click</button>
```

### 11. Conditional Hooks

```typescript
// ANTI-PATTERN - hooks must not be conditional
function Component({ shouldFetch }: { shouldFetch: boolean }) {
  if (shouldFetch) {
    const [data, setData] = useState(null);  // WRONG!
  }
}

// CORRECT
function Component({ shouldFetch }: { shouldFetch: boolean }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (shouldFetch) {
      fetchData().then(setData);
    }
  }, [shouldFetch]);
}
```

### 12. Non-Null Assertion Overuse

```typescript
// ANTI-PATTERN
function getUser(id: string): User {
  return users.find((u) => u.id === id)!;  // Assumes always found
}

// CORRECT
function getUser(id: string): User | undefined {
  return users.find((u) => u.id === id);
}

// Or with assertion only when truly safe
function getUser(id: string): User {
  const user = users.find((u) => u.id === id);
  if (!user) {
    throw new Error(`User ${id} not found`);
  }
  return user;
}
```

## Low Priority Anti-Patterns

### 13. Magic Strings/Numbers

```typescript
// ANTI-PATTERN
if (status === 'pending') { }
if (timeout > 5000) { }

// CORRECT
const Status = {
  PENDING: 'pending',
  ACTIVE: 'active',
} as const;

const TIMEOUT_MS = 5000;

if (status === Status.PENDING) { }
if (timeout > TIMEOUT_MS) { }
```

### 14. Unnecessary Type Annotations

```typescript
// ANTI-PATTERN - redundant annotation
const name: string = 'John';  // Type is obvious
const numbers: number[] = [1, 2, 3];  // Type is obvious

// CORRECT - let TypeScript infer
const name = 'John';
const numbers = [1, 2, 3];

// But DO annotate when type isn't obvious
const config: Config = getConfig();  // Good - clarifies return type
```

### 15. Boolean Blindness

```typescript
// ANTI-PATTERN
function configure(
  enableLogging: boolean,
  enableCaching: boolean,
  enableMetrics: boolean
) { }

configure(true, false, true);  // What do these mean?

// CORRECT
interface ConfigOptions {
  logging?: boolean;
  caching?: boolean;
  metrics?: boolean;
}

function configure(options: ConfigOptions) { }

configure({ logging: true, metrics: true });  // Clear
```

## Detection Tips

When reviewing TypeScript/React code, look for:

1. **`any`** - Should be avoided or justified
2. **`!`** - Non-null assertion needs justification
3. **`as`** - Type assertion should have validation
4. **Empty `[]`** - useEffect with empty deps array
5. **`.map()` without `key`** - Missing or index-based keys
6. **Inline `{{}}`** - New object in JSX props
7. **`() =>`** - Inline functions in JSX
8. **Long component files** - Consider decomposition
9. **Deep prop passing** - Consider context
10. **No error handling** - Missing try/catch or error boundaries
