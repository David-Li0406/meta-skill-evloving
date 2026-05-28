# Common Pitfalls

Avoid these frequent React mistakes.

## 1. Stale Closures

```tsx
// ❌ Bad - stale closure
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(count + 1); // Always uses initial count (0)
    }, 1000);
    return () => clearInterval(interval);
  }, []); // Missing count dependency

  return <div>{count}</div>;
}

// ✅ Good - functional update
setCount(prev => prev + 1);
```

## 2. Missing Dependencies

```tsx
// ❌ Bad
useEffect(() => {
  fetchData(userId);
}, []); // Missing userId

// ✅ Good
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

## 3. Unnecessary useEffect

```tsx
// ❌ Bad - don't use effect for derived state
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);

useEffect(() => {
  setCount(items.length);
}, [items]);

// ✅ Good - compute during render
const count = items.length;
```

## 4. Props in Initial State

```tsx
// ❌ Bad - ignores prop updates
function Component({ initialValue }) {
  const [value, setValue] = useState(initialValue);
}

// ✅ Good - use prop directly or key
function Component({ value: propValue }) {
  const [value, setValue] = useState(propValue);

  useEffect(() => {
    setValue(propValue);
  }, [propValue]);
}
```

## 5. Mutating State

```tsx
// ❌ Bad
const [items, setItems] = useState([]);
items.push(newItem); // Mutation!
setItems(items);

// ✅ Good
setItems([...items, newItem]);
```

## 6. Keys in Lists

```tsx
// ❌ Bad - index as key
{items.map((item, index) => <div key={index}>{item}</div>)}

// ✅ Good - stable unique key
{items.map(item => <div key={item.id}>{item}</div>)}
```

## 7. Fetching in useEffect

```tsx
// ❌ Bad - manual data fetching
useEffect(() => {
  fetch('/api/users').then(/* ... */);
}, []);

// ✅ Good - use React Query
const { data } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });
```

## 8. Too Many useState Calls

```tsx
// ❌ Bad - related state scattered
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [email, setEmail] = useState('');

// ✅ Good - use useReducer or object state
const [form, setForm] = useState({
  firstName: '',
  lastName: '',
  email: '',
});
```

## 9. Not Cleaning Up Effects

```tsx
// ❌ Bad - memory leak
useEffect(() => {
  const subscription = api.subscribe();
}, []);

// ✅ Good - cleanup
useEffect(() => {
  const subscription = api.subscribe();
  return () => subscription.unsubscribe();
}, []);
```

## 10. Premature Optimization

```tsx
// ❌ Bad - unnecessary memoization
const value = useMemo(() => x + y, [x, y]);

// ✅ Good - simple computation, no memo needed
const value = x + y;
```

Remember: Profile before optimizing. Most performance issues come from unnecessary re-renders, not expensive computations.
