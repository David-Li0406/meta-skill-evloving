# Common Error Patterns and Solutions

## JavaScript/TypeScript Errors

### TypeError: Cannot read property 'x' of undefined
```javascript
// Problem
const user = getUser();
console.log(user.name);  // user is undefined

// Solutions
// 1. Optional chaining
console.log(user?.name);

// 2. Nullish coalescing
const name = user?.name ?? 'Unknown';

// 3. Guard clause
if (!user) {
    throw new Error('User not found');
}
```

### TypeError: x is not a function
```javascript
// Problem
import { useState } from 'react';
useState();  // Works
useStaet();  // Typo - not a function

// Solutions
// 1. Check spelling
// 2. Check import statement
// 3. Check if it's actually exported
```

### ReferenceError: x is not defined
```javascript
// Problem
console.log(myVariable);  // Never declared

// Solutions
// 1. Declare the variable
// 2. Check scope (block scope with let/const)
// 3. Check import
```

### Maximum call stack exceeded
```javascript
// Problem - infinite recursion
function bad() {
    bad();  // Calls itself forever
}

// Problem - infinite re-render
function Component() {
    const [count, setCount] = useState(0);
    setCount(count + 1);  // Triggers re-render, which triggers...
    return <div>{count}</div>;
}

// Solution - add base case or dependency array
function Component() {
    const [count, setCount] = useState(0);
    useEffect(() => {
        setCount(c => c + 1);
    }, []);  // Empty deps - runs once
    return <div>{count}</div>;
}
```

## Python Errors

### AttributeError: 'NoneType' object has no attribute 'x'
```python
# Problem
user = get_user()  # Returns None
print(user.name)  # None has no .name

# Solutions
# 1. Check before access
if user is not None:
    print(user.name)

# 2. Use getattr with default
name = getattr(user, 'name', 'Unknown')

# 3. Fix the source - why is it None?
```

### KeyError: 'x'
```python
# Problem
data = {"name": "Alice"}
print(data["age"])  # Key doesn't exist

# Solutions
# 1. Use .get()
age = data.get("age", 0)

# 2. Check first
if "age" in data:
    print(data["age"])
```

### IndentationError
```python
# Problem
def foo():
print("hello")  # Wrong indentation

# Solution
def foo():
    print("hello")  # Correct - 4 spaces
```

### ImportError / ModuleNotFoundError
```python
# Problem
from mymodule import something
# ModuleNotFoundError: No module named 'mymodule'

# Solutions
# 1. Install the package
pip install mymodule

# 2. Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/module"

# 3. Check spelling and case
```

## Database Errors

### Connection refused
```
psycopg2.OperationalError: could not connect to server: Connection refused

# Check:
# 1. Is database running?
docker ps | grep postgres
systemctl status postgresql

# 2. Correct host/port?
# localhost vs container name vs IP

# 3. Firewall/security group?
```

### Constraint violation
```sql
-- IntegrityError: UNIQUE constraint failed
INSERT INTO users (email) VALUES ('alice@example.com');
-- Email already exists

-- Solutions:
-- 1. Check before insert
SELECT * FROM users WHERE email = 'alice@example.com';

-- 2. Use ON CONFLICT
INSERT INTO users (email) VALUES ('alice@example.com')
ON CONFLICT (email) DO UPDATE SET updated_at = NOW();
```

### Deadlock
```sql
-- Transaction 1 locks A, wants B
-- Transaction 2 locks B, wants A
-- Both wait forever

-- Solutions:
-- 1. Lock in consistent order
-- 2. Use shorter transactions
-- 3. Add retry logic with backoff
```

## HTTP Errors

### 400 Bad Request
```
# Request body is malformed or missing required fields

# Check:
# 1. Content-Type header correct?
Content-Type: application/json

# 2. JSON valid?
echo '{"name": "test"}' | jq .

# 3. Required fields present?
```

### 401 Unauthorized
```
# Authentication failed

# Check:
# 1. Token present?
Authorization: Bearer <token>

# 2. Token valid?
# - Not expired
# - Correctly signed
# - Right format

# 3. User exists and active?
```

### 403 Forbidden
```
# Authenticated but not authorized

# Check:
# 1. User has required role/permission?
# 2. Resource belongs to user?
# 3. Feature enabled for user's plan?
```

### 404 Not Found
```
# Resource doesn't exist

# Check:
# 1. URL correct? (typos, case sensitivity)
# 2. ID exists in database?
# 3. Route registered? (order matters)
# 4. HTTP method correct? (GET vs POST)
```

### 500 Internal Server Error
```
# Unhandled exception on server

# Check logs for:
# 1. Stack trace
# 2. Error message
# 3. Request that caused it

# Common causes:
# - Null pointer / undefined access
# - Database connection lost
# - External service failure
# - Out of memory
```

## React Errors

### Invalid hook call
```javascript
// Problem: Hook called outside component
function notAComponent() {
    const [x, setX] = useState(0);  // Error!
}

// Solution: Only call hooks in components/custom hooks
function MyComponent() {
    const [x, setX] = useState(0);  // OK
}
```

### Cannot update during render
```javascript
// Problem: State update in render
function Component({ value }) {
    const [state, setState] = useState(0);
    if (value > 0) {
        setState(value);  // Error! Updates during render
    }
    return <div>{state}</div>;
}

// Solution: Use useEffect
function Component({ value }) {
    const [state, setState] = useState(0);
    useEffect(() => {
        if (value > 0) {
            setState(value);
        }
    }, [value]);
    return <div>{state}</div>;
}
```

### Missing key prop
```javascript
// Warning: Each child should have unique "key" prop
items.map(item => <div>{item.name}</div>);

// Solution: Add key
items.map(item => <div key={item.id}>{item.name}</div>);
```

## Docker Errors

### Container exits immediately
```bash
# Check logs
docker logs container_name

# Common causes:
# 1. Command fails
# 2. Missing environment variable
# 3. File not found
# 4. Permission denied

# Debug: Run interactively
docker run -it --entrypoint /bin/sh image_name
```

### Port already in use
```bash
# Error: port 8080 already allocated

# Find what's using it
lsof -i :8080
netstat -tlnp | grep 8080

# Kill it or use different port
docker run -p 8081:8080 image_name
```

### Volume permission denied
```bash
# Error: Permission denied accessing mounted volume

# Solutions:
# 1. Match user IDs
docker run -u $(id -u):$(id -g) image_name

# 2. Fix permissions
chmod -R 777 ./data  # Not recommended for production

# 3. Use named volumes
docker volume create mydata
docker run -v mydata:/app/data image_name
```

## Git Errors

### Merge conflict
```bash
# Auto-merge failed; fix conflicts and commit

# Steps:
# 1. Open conflicted files
# 2. Look for <<<<<<< ======= >>>>>>>
# 3. Choose correct code, remove markers
# 4. Stage and commit
git add .
git commit -m "Resolve merge conflicts"
```

### Detached HEAD
```bash
# You are in 'detached HEAD' state

# To keep changes:
git checkout -b new-branch-name

# To discard and go back:
git checkout main
```

### Push rejected (non-fast-forward)
```bash
# error: failed to push some refs

# Someone else pushed first
# Solution:
git pull --rebase origin main
git push origin main
```

## Quick Lookup Table

| Error Pattern | Likely Cause | First Step |
|---------------|--------------|------------|
| undefined/null | Missing data | Check data source |
| not a function | Wrong import/typo | Check spelling |
| connection refused | Service down | Check if running |
| 401/403 | Auth issue | Check token |
| 500 | Server exception | Check logs |
| timeout | Slow/stuck | Profile code |
| out of memory | Memory leak | Profile memory |
| permission denied | Wrong user/mode | Check permissions |
