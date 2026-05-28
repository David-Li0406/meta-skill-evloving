# Example: React Component Analysis

## 📝 Prompt

```
Analyze this React component for code quality, best practices, and potential issues:

[paste your React component code here]

Focus on:
- Component design and structure
- Performance optimizations
- Accessibility
- TypeScript usage
- State management
- Error handling
```

## Sample Code to Analyze

```typescript
// UserList.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios.get('https://api.example.com/users')
      .then(response => {
        setUsers(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.log(error);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h1>Users</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {users.map(user => (
            <li key={user.id} onClick={() => alert(user.name)}>
              {user.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default UserList;
```

## ✅ Expected Analysis Output

### Issues Found

#### 🔴 Critical Issues

1. **Missing TypeScript Types**
   - **Location**: Line 6, useState
   - **Issue**: `users` array has implicit `any` type
   - **Impact**: No type safety, potential runtime errors
   - **Fix**:
   ```typescript
   interface User {
     id: string;
     name: string;
     email: string;
   }
   const [users, setUsers] = useState<User[]>([]);
   ```

2. **No Error State Management**
   - **Location**: catch block (line 14)
   - **Issue**: Errors are only logged, not shown to user
   - **Fix**:
   ```typescript
   const [error, setError] = useState<string | null>(null);
   // In catch: setError(error.message);
   // In render: {error && <p className="error">{error}</p>}
   ```

#### 🟡 Medium Issues

3. **Missing Accessibility**
   - **Location**: Line 21, `<li>` elements
   - **Issue**: Clickable elements without proper semantics
   - **Fix**: Use `<button>` or add `role="button"`, `tabIndex={0}`, keyboard handlers
   ```typescript
   <button onClick={() => alert(user.name)}>
     {user.name}
   </button>
   ```

4. **Missing Loading State Type**
   - **Location**: Line 7
   - **Issue**: Boolean loading state, better to use enum
   - **Fix**:
   ```typescript
   type LoadingState = 'idle' | 'loading' | 'success' | 'error';
   const [status, setStatus] = useState<LoadingState>('idle');
   ```

5. **No Cleanup for Async Operations**
   - **Location**: useEffect (line 9)
   - **Issue**: Component may unmount before request completes
   - **Fix**:
   ```typescript
   useEffect(() => {
     let cancelled = false;
     const loadUsers = async () => {
       setLoading(true);
       try {
         const response = await axios.get('...');
         if (!cancelled) {
           setUsers(response.data);
         }
       } finally {
         if (!cancelled) {
           setLoading(false);
         }
       }
     };
     loadUsers();
     return () => { cancelled = true; };
   }, []);
   ```

#### 🟢 Minor Issues

6. **Using Alerts for UI Feedback**
   - **Location**: Line 21
   - **Issue**: `alert()` blocks UI, poor UX
   - **Fix**: Use modal, toast, or navigation

7. **Hardcoded API URL**
   - **Location**: Line 10
   - **Issue**: API URL should be in environment variable
   - **Fix**: `const API_URL = process.env.REACT_APP_API_URL;`

8. **Missing Empty State**
   - **Location**: render
   - **Issue**: No message when users array is empty
   - **Fix**: Add condition for `users.length === 0`

### Metrics

- **Complexity**: 3 (Low - simple component)
- **Maintainability**: C (TypeScript issues reduce score)
- **Test Coverage**: 0% (no tests provided)
- **Lines of Code**: 30

### Recommendations

1. **Immediate Actions** (< 1 hour):
   - Add TypeScript types
   - Add error state
   - Fix accessibility issues

2. **Short-term Improvements** (< 1 day):
   - Extract data fetching to custom hook
   - Add proper error boundary
   - Implement retry logic

3. **Long-term Enhancements**:
   - Consider React Query for data fetching
   - Add unit tests (React Testing Library)
   - Implement pagination

### Refactored Version

```typescript
// UserList.tsx (Improved)
import React from 'react';
import { useUsers } from './hooks/useUsers';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';

interface User {
  id: string;
  name: string;
  email: string;
}

export const UserList: React.FC = () => {
  const { users, loading, error, refetch } = useUsers();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage error={error} onRetry={refetch} />;
  }

  if (users.length === 0) {
    return <p>No users found.</p>;
  }

  return (
    <div className="user-list">
      <h1>Users</h1>
      <ul role="list">
        {users.map((user) => (
          <li key={user.id}>
            <UserCard user={user} />
          </li>
        ))}
      </ul>
    </div>
  );
};

// hooks/useUsers.ts
import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export function useUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get<User[]>(`${API_URL}/users`);
      setUsers(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let cancelled = false;
    
    const loadData = async () => {
      await fetchUsers();
    };
    
    loadData();
    
    return () => {
      cancelled = true;
    };
  }, []);

  return { users, loading, error, refetch: fetchUsers };
}
```

### Summary

**Priority**: High - TypeScript and error handling issues should be addressed soon
**Effort**: 2-3 hours
**Impact**: Improved type safety, better UX, more maintainable code
