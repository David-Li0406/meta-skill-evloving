# RxJS Migration Patterns

Comprehensive guide for migrating RxJS Observable patterns to React state management.

## Observable → React Query/SWR

### Basic Data Fetching

**Before (Angular with RxJS)**:
```typescript
// user.service.ts
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }

  getUser(id: string): Observable<User> {
    return this.http.get<User>(`/api/users/${id}`);
  }
}

// user-list.component.ts
export class UserListComponent implements OnInit, OnDestroy {
  users: User[] = [];
  private destroy$ = new Subject<void>();

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.userService.getUsers()
      .pipe(takeUntil(this.destroy$))
      .subscribe(users => this.users = users);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

**After (Next.js with SWR)**:
```typescript
// hooks/useUsers.ts
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export function useUsers() {
  const { data, error, isLoading, mutate } = useSWR<User[]>(
    '/api/users',
    fetcher
  )

  return {
    users: data ?? [],
    error,
    isLoading,
    refresh: mutate
  }
}

export function useUser(id: string) {
  const { data, error, isLoading } = useSWR<User>(
    id ? `/api/users/${id}` : null,
    fetcher
  )

  return { user: data, error, isLoading }
}

// components/user-list.tsx
'use client'

import { useUsers } from '@/hooks/useUsers'

export function UserList() {
  const { users, isLoading, error } = useUsers()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading users</div>

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

---

## RxJS Operators → React Patterns

### Operator Mapping Table

| RxJS Operator | React Equivalent | Notes |
|---------------|------------------|-------|
| `map()` | `useMemo` / inline transform | Derived state |
| `filter()` | `useMemo` with filter | Array filtering |
| `tap()` | `useEffect` side effects | Side effects |
| `switchMap()` | `useEffect` with deps | Dependent queries |
| `combineLatest()` | Multiple `useSWR` calls | Parallel data |
| `debounceTime()` | `useDebouncedValue` hook | Input debouncing |
| `distinctUntilChanged()` | `useMemo` with comparison | Skip duplicate updates |
| `catchError()` | SWR `onError` / try-catch | Error handling |
| `retry()` | SWR `errorRetryCount` | Retry logic |
| `shareReplay()` | SWR built-in cache | Caching |

### switchMap → Dependent useEffect

**Before (Angular)**:
```typescript
// search.component.ts
searchControl = new FormControl('');

ngOnInit(): void {
  this.searchControl.valueChanges.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.searchService.search(term)),
    takeUntil(this.destroy$)
  ).subscribe(results => this.results = results);
}
```

**After (React)**:
```typescript
// hooks/useSearch.ts
import { useState, useEffect } from 'react'
import useSWR from 'swr'

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}

export function useSearch(term: string) {
  const debouncedTerm = useDebounce(term, 300)

  const { data, error, isLoading } = useSWR(
    debouncedTerm ? `/api/search?q=${debouncedTerm}` : null,
    fetcher
  )

  return { results: data ?? [], error, isLoading }
}

// components/search.tsx
'use client'

import { useState } from 'react'
import { useSearch } from '@/hooks/useSearch'

export function Search() {
  const [term, setTerm] = useState('')
  const { results, isLoading } = useSearch(term)

  return (
    <div>
      <input
        type="text"
        value={term}
        onChange={(e) => setTerm(e.target.value)}
        placeholder="Search..."
      />
      {isLoading && <span>Searching...</span>}
      <ul>
        {results.map(result => (
          <li key={result.id}>{result.title}</li>
        ))}
      </ul>
    </div>
  )
}
```

### combineLatest → Multiple SWR Calls

**Before (Angular)**:
```typescript
// dashboard.component.ts
ngOnInit(): void {
  combineLatest([
    this.userService.getProfile(),
    this.orderService.getRecentOrders(),
    this.notificationService.getUnread()
  ]).pipe(
    takeUntil(this.destroy$)
  ).subscribe(([profile, orders, notifications]) => {
    this.profile = profile;
    this.orders = orders;
    this.notifications = notifications;
  });
}
```

**After (React)**:
```typescript
// hooks/useDashboard.ts
import useSWR from 'swr'

export function useDashboard() {
  const { data: profile, isLoading: profileLoading } = useSWR('/api/profile', fetcher)
  const { data: orders, isLoading: ordersLoading } = useSWR('/api/orders/recent', fetcher)
  const { data: notifications, isLoading: notificationsLoading } = useSWR('/api/notifications/unread', fetcher)

  return {
    profile,
    orders: orders ?? [],
    notifications: notifications ?? [],
    isLoading: profileLoading || ordersLoading || notificationsLoading
  }
}

// components/dashboard.tsx
'use client'

import { useDashboard } from '@/hooks/useDashboard'

export function Dashboard() {
  const { profile, orders, notifications, isLoading } = useDashboard()

  if (isLoading) return <div>Loading dashboard...</div>

  return (
    <div>
      <ProfileCard profile={profile} />
      <OrdersList orders={orders} />
      <NotificationsBadge count={notifications.length} />
    </div>
  )
}
```

---

## BehaviorSubject → useState + Context

### Global State Pattern

**Before (Angular)**:
```typescript
// auth.service.ts
@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUser$ = new BehaviorSubject<User | null>(null);
  readonly user$ = this.currentUser$.asObservable();

  login(credentials: LoginCredentials): Observable<User> {
    return this.http.post<User>('/api/auth/login', credentials).pipe(
      tap(user => this.currentUser$.next(user))
    );
  }

  logout(): void {
    this.currentUser$.next(null);
  }

  getCurrentUser(): User | null {
    return this.currentUser$.getValue();
  }
}
```

**After (React with Context)**:
```typescript
// contexts/auth-context.tsx
'use client'

import { createContext, useContext, useState, useCallback, ReactNode } from 'react'

interface AuthContextType {
  user: User | null
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = useCallback(async (credentials: LoginCredentials) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    })
    const userData = await response.json()
    setUser(userData)
  }, [])

  const logout = useCallback(() => {
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

---

## Subject Patterns → Event Handling

### Event Bus Pattern

**Before (Angular)**:
```typescript
// event-bus.service.ts
@Injectable({ providedIn: 'root' })
export class EventBusService {
  private events$ = new Subject<AppEvent>();

  emit(event: AppEvent): void {
    this.events$.next(event);
  }

  on<T extends AppEvent>(eventType: string): Observable<T> {
    return this.events$.pipe(
      filter(event => event.type === eventType)
    ) as Observable<T>;
  }
}
```

**After (React with Custom Hook)**:
```typescript
// hooks/useEventBus.ts
import { useEffect, useCallback } from 'react'

type EventHandler<T> = (payload: T) => void
const eventHandlers = new Map<string, Set<EventHandler<unknown>>>()

export function useEventBus() {
  const emit = useCallback(<T>(eventType: string, payload: T) => {
    const handlers = eventHandlers.get(eventType)
    handlers?.forEach(handler => handler(payload))
  }, [])

  const on = useCallback(<T>(eventType: string, handler: EventHandler<T>) => {
    if (!eventHandlers.has(eventType)) {
      eventHandlers.set(eventType, new Set())
    }
    eventHandlers.get(eventType)!.add(handler as EventHandler<unknown>)

    return () => {
      eventHandlers.get(eventType)?.delete(handler as EventHandler<unknown>)
    }
  }, [])

  return { emit, on }
}

// Usage in component
export function NotificationListener() {
  const { on } = useEventBus()

  useEffect(() => {
    const unsubscribe = on<NotificationEvent>('notification', (event) => {
      toast.show(event.message)
    })
    return unsubscribe
  }, [on])

  return null
}
```

---

## Subscription Management

### Angular Subscription vs React Cleanup

**Before (Angular)**:
```typescript
export class DataComponent implements OnDestroy {
  private subscriptions: Subscription[] = [];

  ngOnInit(): void {
    this.subscriptions.push(
      this.dataService.getData().subscribe(data => this.data = data),
      this.eventService.onUpdate().subscribe(() => this.refresh())
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }
}
```

**After (React) - No manual cleanup needed with SWR**:
```typescript
// SWR handles cleanup automatically
export function DataComponent() {
  // No manual subscription management needed
  const { data } = useSWR('/api/data', fetcher)

  // For custom subscriptions, use useEffect cleanup
  useEffect(() => {
    const unsubscribe = eventService.onUpdate(() => mutate('/api/data'))
    return () => unsubscribe()
  }, [])

  return <div>{data?.value}</div>
}
```

---

## Error Handling Migration

### catchError → SWR Error Handling

**Before (Angular)**:
```typescript
this.userService.getUser(id).pipe(
  catchError(error => {
    console.error('Failed to load user:', error);
    return of(null);
  })
).subscribe(user => this.user = user);
```

**After (React)**:
```typescript
const { data: user, error } = useSWR(`/api/users/${id}`, fetcher, {
  onError: (err) => {
    console.error('Failed to load user:', err)
  },
  errorRetryCount: 3,
  errorRetryInterval: 1000
})

if (error) return <ErrorFallback error={error} />
```

---

## Real-time Data Migration

### WebSocket with RxJS → WebSocket Hook

**Before (Angular)**:
```typescript
@Injectable({ providedIn: 'root' })
export class WebSocketService {
  private socket$: WebSocketSubject<Message>;

  connect(): void {
    this.socket$ = webSocket('wss://api.example.com/ws');
  }

  messages$(): Observable<Message> {
    return this.socket$.asObservable();
  }

  send(message: Message): void {
    this.socket$.next(message);
  }
}
```

**After (React Hook)**:
```typescript
// hooks/useWebSocket.ts
import { useEffect, useState, useCallback, useRef } from 'react'

export function useWebSocket(url: string) {
  const [messages, setMessages] = useState<Message[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const socket = new WebSocket(url)

    socket.onopen = () => setIsConnected(true)
    socket.onclose = () => setIsConnected(false)
    socket.onmessage = (event) => {
      const message = JSON.parse(event.data)
      setMessages(prev => [...prev, message])
    }

    socketRef.current = socket

    return () => {
      socket.close()
    }
  }, [url])

  const send = useCallback((message: Message) => {
    socketRef.current?.send(JSON.stringify(message))
  }, [])

  return { messages, isConnected, send }
}
```

---

Version: 1.0.0
Source: jikime-migration-angular-to-nextjs SKILL.md
