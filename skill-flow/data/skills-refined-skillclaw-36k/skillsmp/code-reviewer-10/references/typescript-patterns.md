# TypeScript/React Review Patterns

## Type Safety

### Type Narrowing vs Casting

```typescript
// ❌ BAD: Type assertion (lies to compiler)
const user = data as User;
user.name.toUpperCase(); // runtime error if data is null

// ✅ GOOD: Type narrowing (proven safe)
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'name' in data &&
    typeof data.name === 'string'
  );
}

if (isUser(data)) {
  data.name.toUpperCase(); // compiler knows it's safe
}

// ✅ GOOD: Zod for runtime validation
const UserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
});

const result = UserSchema.safeParse(data);
if (result.success) {
  result.data.name; // typed and validated
}
```

### Avoid `any`

```typescript
// ❌ BAD: any defeats type checking
function process(data: any) {
  return data.foo.bar.baz; // no safety
}

// ✅ GOOD: Use unknown and narrow
function process(data: unknown): string {
  if (typeof data === 'object' && data && 'foo' in data) {
    // properly narrowed
  }
  throw new Error('Invalid data format');
}

// ✅ GOOD: Generic with constraints
function process<T extends { id: string }>(data: T): string {
  return data.id;
}
```

### Discriminated Unions

```typescript
// ✅ GOOD: Exhaustive handling
type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'loading' };

function render(result: Result<User>) {
  switch (result.status) {
    case 'success':
      return <UserCard user={result.data} />;
    case 'error':
      return <ErrorMessage message={result.error} />;
    case 'loading':
      return <Spinner />;
    default:
      const _exhaustive: never = result;
      return _exhaustive;
  }
}
```

---

## React Patterns

### Server vs Client Components

```typescript
// ❌ BAD: Unnecessary 'use client'
'use client'; // NOT needed!
export function UserList({ users }: { users: User[] }) {
  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}

// ✅ GOOD: Server component (default)
export async function UserList() {
  const users = await fetchUsers(); // server-side fetch
  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}

// ✅ GOOD: Client only when needed
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Hooks Dependency Arrays

```typescript
// ❌ BAD: Missing dependency
useEffect(() => {
  fetchUser(userId); // userId not in deps!
}, []);

// ❌ BAD: Object in deps (new ref each render)
useEffect(() => {
  search(options);
}, [options]); // infinite loop if options created inline

// ✅ GOOD: Stable dependencies
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// ✅ GOOD: Memoize objects
const stableOptions = useMemo(() => ({ query, limit }), [query, limit]);
useEffect(() => {
  search(stableOptions);
}, [stableOptions]);
```

### State Management

```typescript
// ❌ BAD: Derived state
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState(''); // derived!

useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// ✅ GOOD: Compute during render
const fullName = `${firstName} ${lastName}`;

// ❌ BAD: State for server data (should use query lib)
const [users, setUsers] = useState<User[]>([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<Error | null>(null);

// ✅ GOOD: Use React Query / SWR
const { data: users, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
});
```

### Performance

```typescript
// ❌ BAD: Inline objects causing re-renders
<Component style={{ margin: 10 }} />
<Button config={{ theme: 'dark' }} />

// ✅ GOOD: Stable references
const style = { margin: 10 }; // outside component
<Component style={style} />

const config = useMemo(() => ({ theme }), [theme]);
<Button config={config} />

// ❌ BAD: useMemo/useCallback everywhere
const value = useMemo(() => a + b, [a, b]); // simple math, not needed

// ✅ GOOD: Only for expensive operations
const sorted = useMemo(
  () => items.slice().sort((a, b) => complexSort(a, b)),
  [items]
);
```

### Component Structure

```typescript
// ❌ BAD: Giant component
export function Dashboard() {
  const [state1, setState1] = useState();
  const [state2, setState2] = useState();
  // ... 10 more states
  // ... 200 lines of JSX
}

// ✅ GOOD: Composition
export function Dashboard() {
  return (
    <DashboardLayout>
      <DashboardHeader />
      <MetricsPanel />
      <ActivityFeed />
    </DashboardLayout>
  );
}

// ✅ GOOD: Extract logic to hooks
export function Dashboard() {
  const metrics = useMetrics();
  const activities = useActivities();

  return <DashboardView metrics={metrics} activities={activities} />;
}
```

---

## Error Handling

### Async/Await

```typescript
// ❌ BAD: Unhandled promise rejection
async function fetchData() {
  const response = await fetch('/api/data'); // can throw
  return response.json();
}

// ✅ GOOD: Explicit error handling
async function fetchData(): Promise<Data | null> {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error('Failed to fetch data:', error);
    return null;
  }
}

// ✅ GOOD: Result type
async function fetchData(): Promise<Result<Data>> {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      return { status: 'error', error: `HTTP ${response.status}` };
    }
    return { status: 'success', data: await response.json() };
  } catch (error) {
    return { status: 'error', error: String(error) };
  }
}
```

### Error Boundaries

```typescript
// ✅ GOOD: Wrap sections that can fail
<ErrorBoundary fallback={<ErrorMessage />}>
  <UserProfile userId={id} />
</ErrorBoundary>

// ✅ GOOD: Loading and error states
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = useUser(userId);

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!data) return <NotFound />;

  return <ProfileCard user={data} />;
}
```

---

## Accessibility

```typescript
// ❌ BAD: Div as button
<div onClick={handleClick}>Click me</div>

// ✅ GOOD: Semantic HTML
<button onClick={handleClick}>Click me</button>

// ❌ BAD: Missing labels
<input type="text" placeholder="Email" />

// ✅ GOOD: Accessible form
<label htmlFor="email">Email</label>
<input id="email" type="email" aria-required="true" />

// ❌ BAD: Image without alt
<img src={logo} />

// ✅ GOOD: Descriptive alt (or empty for decorative)
<img src={logo} alt="Company logo" />
<img src={decoration} alt="" role="presentation" />
```

---

## Server Actions

```typescript
// ❌ BAD: No validation
'use server';
export async function updateUser(data: FormData) {
  const name = data.get('name') as string;
  await db.user.update({ name }); // trusts input!
}

// ✅ GOOD: Validate with Zod
'use server';
const UpdateSchema = z.object({
  name: z.string().min(1).max(100),
});

export async function updateUser(data: FormData) {
  const parsed = UpdateSchema.safeParse({
    name: data.get('name'),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten() };
  }

  await db.user.update(parsed.data);
  revalidatePath('/profile');
  return { success: true };
}
```

---

## Testing Patterns

### Component Testing

```typescript
// ✅ GOOD: Test behavior, not implementation
test('shows user name after loading', async () => {
  render(<UserProfile userId="123" />);

  expect(screen.getByRole('progressbar')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});

// ✅ GOOD: Test user interactions
test('submits form with valid data', async () => {
  const onSubmit = vi.fn();
  render(<ContactForm onSubmit={onSubmit} />);

  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com');
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }));

  expect(onSubmit).toHaveBeenCalledWith({ email: 'test@example.com' });
});
```

### Hook Testing

```typescript
// ✅ GOOD: Extract and test logic separately
function calculateDiscount(price: number, tier: 'bronze' | 'silver' | 'gold') {
  const rates = { bronze: 0.05, silver: 0.1, gold: 0.15 };
  return price * rates[tier];
}

// Pure function - easy to test
test('gold tier gets 15% discount', () => {
  expect(calculateDiscount(100, 'gold')).toBe(15);
});
```
