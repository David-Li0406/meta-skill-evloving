# React Bug Patterns Reference

This document contains common bug patterns to include in React debugging practice projects.

## Table of Contents

1. [State Management Bugs](#state-management-bugs)
2. [Effect Hook Issues](#effect-hook-issues)
3. [Props and Event Handler Bugs](#props-and-event-handler-bugs)
4. [Conditional Rendering Issues](#conditional-rendering-issues)
5. [List Rendering Problems](#list-rendering-problems)
6. [Async State Updates](#async-state-updates)

---

## State Management Bugs

### Missing State Update
**Bug Type**: Logic Error
**Difficulty**: Beginner

```jsx
// Bug: Incrementing without setState
function Counter() {
  let count = 0;

  const increment = () => {
    count = count + 1; // Bug: Direct mutation won't trigger re-render
    console.log(count);
  };

  return <button onClick={increment}>Count: {count}</button>;
}
```

**Fix**: Use `useState` hook
```jsx
const [count, setCount] = useState(0);
const increment = () => setCount(count + 1);
```

---

### Stale Closure in setState
**Bug Type**: Logic Error
**Difficulty**: Intermediate

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  const incrementTwice = () => {
    setCount(count + 1); // Bug: Both use same stale count value
    setCount(count + 1);
  };

  return <button onClick={incrementTwice}>Count: {count}</button>;
}
```

**Fix**: Use functional setState
```jsx
setCount(prev => prev + 1);
setCount(prev => prev + 1);
```

---

## Effect Hook Issues

### Missing Dependency Array
**Bug Type**: Effect Hook
**Difficulty**: Intermediate

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser); // Bug: Runs on every render
  }); // Missing dependency array

  return <div>{user?.name}</div>;
}
```

**Fix**: Add dependency array
```jsx
useEffect(() => {
  fetchUser(userId).then(setUser);
}, [userId]); // Only re-run when userId changes
```

---

### Stale Dependency in Effect
**Bug Type**: Effect Hook
**Difficulty**: Advanced

```jsx
function Timer() {
  const [count, setCount] = useState(0);
  const [delay, setDelay] = useState(1000);

  useEffect(() => {
    const interval = setInterval(() => {
      console.log(count); // Bug: count is stale, always logs 0
      setCount(count + 1);
    }, delay);

    return () => clearInterval(interval);
  }, [delay]); // Bug: Missing count in dependency array

  return <div>Count: {count}</div>;
}
```

**Fix**: Include all dependencies or use functional setState
```jsx
useEffect(() => {
  const interval = setInterval(() => {
    setCount(prev => prev + 1); // Use functional update
  }, delay);

  return () => clearInterval(interval);
}, [delay]);
```

---

## Props and Event Handler Bugs

### Incorrect Event Handler Invocation
**Bug Type**: Logic Error
**Difficulty**: Beginner

```jsx
function TodoItem({ todo, onDelete }) {
  return (
    <div>
      {todo.text}
      <button onClick={onDelete(todo.id)}>Delete</button>
      {/* Bug: Calls onDelete immediately on render */}
    </div>
  );
}
```

**Fix**: Wrap in arrow function
```jsx
<button onClick={() => onDelete(todo.id)}>Delete</button>
```

---

### Missing Key Prop Warning
**Bug Type**: List Rendering
**Difficulty**: Beginner

```jsx
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <li>{todo.text}</li> // Bug: Missing key prop
      ))}
    </ul>
  );
}
```

**Fix**: Add unique key
```jsx
{todos.map(todo => (
  <li key={todo.id}>{todo.text}</li>
))}
```

---

## Conditional Rendering Issues

### Incorrect Falsy Check
**Bug Type**: Logic Error
**Difficulty**: Intermediate

```jsx
function UserList({ users }) {
  return (
    <div>
      {users.length && <p>Found {users.length} users</p>}
      {/* Bug: Renders "0" when array is empty */}
    </div>
  );
}
```

**Fix**: Use boolean expression
```jsx
{users.length > 0 && <p>Found {users.length} users</p>}
```

---

## List Rendering Problems

### Index as Key Anti-pattern
**Bug Type**: List Rendering
**Difficulty**: Intermediate

```jsx
function TodoList({ todos }) {
  const [items, setItems] = useState(todos);

  const deleteItem = (index) => {
    setItems(items.filter((_, i) => i !== index));
  };

  return (
    <ul>
      {items.map((todo, index) => (
        <li key={index}> {/* Bug: Index as key causes incorrect re-renders */}
          {todo.text}
          <button onClick={() => deleteItem(index)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
```

**Fix**: Use stable unique identifier
```jsx
<li key={todo.id}>
```

---

## Async State Updates

### Race Condition in Fetch
**Bug Type**: Async Issue
**Difficulty**: Advanced

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(data => {
      setUser(data); // Bug: May set stale data if userId changes mid-fetch
    });
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

**Fix**: Use cleanup function with abort controller
```jsx
useEffect(() => {
  let cancelled = false;

  fetchUser(userId).then(data => {
    if (!cancelled) {
      setUser(data);
    }
  });

  return () => {
    cancelled = true;
  };
}, [userId]);
```

---

### Missing Error Handling in Fetch
**Bug Type**: Async Issue
**Difficulty**: Intermediate

```jsx
function DataFetcher() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData); // Bug: No error handling
  }, []);

  return <div>{data?.value}</div>;
}
```

**Fix**: Add error handling
```jsx
const [error, setError] = useState(null);

useEffect(() => {
  fetch('/api/data')
    .then(res => res.json())
    .then(setData)
    .catch(err => {
      console.error('Fetch error:', err);
      setError(err.message);
    });
}, []);

if (error) return <div>Error: {error}</div>;
```
