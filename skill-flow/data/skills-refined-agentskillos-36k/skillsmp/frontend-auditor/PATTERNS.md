# Frontend Vulnerability Patterns by Framework

Quick reference for framework-specific vulnerabilities and common mistakes.

---

## React

### XSS via dangerouslySetInnerHTML
```jsx
// VULNERABLE: Unsanitized user content
function Comment({ content }) {
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
}

// SAFE: Sanitize with DOMPurify
import DOMPurify from 'dompurify';

function Comment({ content }) {
  const sanitized = DOMPurify.sanitize(content);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

### XSS via href
```jsx
// VULNERABLE: User-controlled href
function Link({ url, children }) {
  return <a href={url}>{children}</a>;  // javascript:alert(1)
}

// SAFE: Validate URL protocol
function Link({ url, children }) {
  const isValid = /^https?:\/\//.test(url);
  return isValid ? <a href={url}>{children}</a> : <span>{children}</span>;
}
```

### Memory Leaks in useEffect
```jsx
// VULNERABLE: No cleanup
useEffect(() => {
  const interval = setInterval(fetchData, 5000);
  // Missing cleanup - memory leak!
}, []);

// SAFE: Cleanup on unmount
useEffect(() => {
  const interval = setInterval(fetchData, 5000);
  return () => clearInterval(interval);
}, []);
```

### Race Conditions in Async Effects
```jsx
// VULNERABLE: Stale state update
useEffect(() => {
  fetch(`/api/user/${userId}`)
    .then(res => res.json())
    .then(data => setUser(data));  // May update with stale data
}, [userId]);

// SAFE: Abort stale requests
useEffect(() => {
  const controller = new AbortController();
  fetch(`/api/user/${userId}`, { signal: controller.signal })
    .then(res => res.json())
    .then(data => setUser(data))
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });
  return () => controller.abort();
}, [userId]);
```

### Missing Error Boundaries
```jsx
// VULNERABLE: Crash bubbles up
function App() {
  return (
    <Dashboard />  // If this throws, whole app crashes
  );
}

// SAFE: Error boundary catches crashes
function App() {
  return (
    <ErrorBoundary fallback={<ErrorPage />}>
      <Dashboard />
    </ErrorBoundary>
  );
}
```

---

## Next.js

### Secrets in Client Bundle
```typescript
// VULNERABLE: Server secret exposed to client
// next.config.js
module.exports = {
  env: {
    DATABASE_URL: process.env.DATABASE_URL  // Exposed!
  }
}

// SAFE: Only expose public vars
// Use NEXT_PUBLIC_ prefix for client-safe vars
const publicApiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Hydration Mismatch
```jsx
// VULNERABLE: Server/client render differently
function Time() {
  return <span>{new Date().toISOString()}</span>;  // Different on server vs client
}

// SAFE: Use client-only rendering for dynamic content
'use client';
function Time() {
  const [time, setTime] = useState<string>();
  useEffect(() => setTime(new Date().toISOString()), []);
  return <span>{time}</span>;
}
```

### Missing Auth Check in Server Components
```typescript
// VULNERABLE: Data exposed without auth
async function Dashboard() {
  const data = await fetchSensitiveData();  // No auth check!
  return <div>{data}</div>;
}

// SAFE: Check auth in server component
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

async function Dashboard() {
  const session = await auth();
  if (!session) redirect('/login');
  const data = await fetchSensitiveData();
  return <div>{data}</div>;
}
```

### Open Redirect in Callback URLs
```typescript
// VULNERABLE: Unvalidated redirect
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const callbackUrl = searchParams.get('callbackUrl');
  // Attacker: ?callbackUrl=https://evil.com
  return redirect(callbackUrl!);
}

// SAFE: Validate redirect is internal
const callbackUrl = searchParams.get('callbackUrl') || '/';
const isInternal = callbackUrl.startsWith('/') && !callbackUrl.startsWith('//');
return redirect(isInternal ? callbackUrl : '/');
```

---

## Vue

### XSS via v-html
```vue
<!-- VULNERABLE: Unsanitized HTML -->
<template>
  <div v-html="userContent"></div>
</template>

<!-- SAFE: Sanitize first -->
<script setup>
import DOMPurify from 'dompurify';
const sanitizedContent = computed(() => DOMPurify.sanitize(userContent));
</script>
<template>
  <div v-html="sanitizedContent"></div>
</template>
```

### Mutating Props
```vue
<!-- VULNERABLE: Direct prop mutation -->
<script setup>
const props = defineProps(['user']);
function updateName(name) {
  props.user.name = name;  // Anti-pattern!
}
</script>

<!-- SAFE: Emit event to parent -->
<script setup>
const emit = defineEmits(['update:user']);
function updateName(name) {
  emit('update:user', { ...props.user, name });
}
</script>
```

### Watchers Without Cleanup
```vue
<!-- VULNERABLE: Subscription not cleaned up -->
<script setup>
import { onMounted } from 'vue';
onMounted(() => {
  socket.on('message', handleMessage);
  // Never cleaned up!
});
</script>

<!-- SAFE: Cleanup in onUnmounted -->
<script setup>
import { onMounted, onUnmounted } from 'vue';
onMounted(() => socket.on('message', handleMessage));
onUnmounted(() => socket.off('message', handleMessage));
</script>
```

---

## State Management (General)

### Token in localStorage
```typescript
// VULNERABLE: XSS can steal token
localStorage.setItem('token', authToken);
fetch('/api', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }});

// SAFE: Use httpOnly cookies (set by server)
// Server sets: Set-Cookie: token=xxx; HttpOnly; Secure; SameSite=Strict
fetch('/api', { credentials: 'include' });
```

### Secrets in Redux/State
```typescript
// VULNERABLE: Secrets visible in devtools
const initialState = {
  apiKey: process.env.REACT_APP_SECRET_KEY,  // Visible in Redux DevTools!
  user: null
};

// SAFE: Never store secrets in frontend state
// Secrets should only exist on server, sent per-request if needed
```

### Race Condition in Async Actions
```typescript
// VULNERABLE: Responses arrive out of order
let currentRequestId = 0;
async function search(query) {
  const results = await api.search(query);
  dispatch({ type: 'SET_RESULTS', results });  // May be stale!
}

// SAFE: Track request ID
let currentRequestId = 0;
async function search(query) {
  const requestId = ++currentRequestId;
  const results = await api.search(query);
  if (requestId === currentRequestId) {
    dispatch({ type: 'SET_RESULTS', results });
  }
}
```

---

## Common Anti-Patterns

### Double Submit
```jsx
// VULNERABLE: Can submit multiple times
function Form() {
  const handleSubmit = async () => {
    await api.submit(data);
  };
  return <button onClick={handleSubmit}>Submit</button>;
}

// SAFE: Track loading state
function Form() {
  const [isLoading, setLoading] = useState(false);
  const handleSubmit = async () => {
    if (isLoading) return;
    setLoading(true);
    try {
      await api.submit(data);
    } finally {
      setLoading(false);
    }
  };
  return <button onClick={handleSubmit} disabled={isLoading}>Submit</button>;
}
```

### Missing Loading States
```jsx
// VULNERABLE: Flash of undefined content
function UserProfile({ userId }) {
  const [user, setUser] = useState();
  useEffect(() => { fetchUser(userId).then(setUser); }, [userId]);
  return <div>{user.name}</div>;  // TypeError!
}

// SAFE: Handle loading state
function UserProfile({ userId }) {
  const [user, setUser] = useState();
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(true);
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  if (loading) return <Skeleton />;
  return <div>{user.name}</div>;
}
```

### Accessibility: Missing Labels
```jsx
// VULNERABLE: Screen reader can't identify input
<input type="email" placeholder="Email" />

// SAFE: Proper label association
<label htmlFor="email">Email</label>
<input id="email" type="email" placeholder="email@example.com" />

// Or visually hidden label
<label htmlFor="email" className="sr-only">Email</label>
<input id="email" type="email" placeholder="Email" />
```

### Accessibility: Click Handler on Div
```jsx
// VULNERABLE: Not keyboard accessible
<div onClick={handleClick}>Click me</div>

// SAFE: Use button or add keyboard support
<button onClick={handleClick}>Click me</button>

// Or if must use div:
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</div>
```

---

## Audit Commands

```bash
# Find XSS vectors
grep -rn "dangerouslySetInnerHTML\|v-html\|innerHTML" --include="*.tsx" --include="*.jsx" --include="*.vue"

# Find localStorage usage (potential token storage)
grep -rn "localStorage\|sessionStorage" --include="*.ts" --include="*.tsx"

# Find potential secrets
grep -rn "API_KEY\|SECRET\|password\|token" --include="*.ts" --include="*.tsx" --include="*.env*"

# Check for console.log in prod
grep -rn "console\." --include="*.ts" --include="*.tsx" | grep -v test

# Find missing key props
grep -rn "\.map(" --include="*.tsx" -A 2 | grep -v "key="

# Check bundle size
npx source-map-explorer dist/**/*.js

# Run Lighthouse
npx lighthouse http://localhost:3000 --output=json --output-path=./lighthouse.json

# A11y audit
npx axe http://localhost:3000
```

---

## Severity Reference

| Issue | Severity | Fix Priority |
|-------|----------|--------------|
| XSS via dangerouslySetInnerHTML | CRITICAL | Immediate |
| Token in localStorage | HIGH | This sprint |
| Secrets in client bundle | CRITICAL | Immediate |
| Missing error boundary | MEDIUM | Soon |
| No keyboard navigation | MEDIUM | Soon |
| Missing loading state | LOW | When convenient |
| Unnecessary re-renders | LOW | When convenient |
