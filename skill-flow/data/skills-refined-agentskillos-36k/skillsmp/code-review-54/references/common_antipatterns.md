# Common Anti-Patterns

Level 3 resource for code-review skill - load for anti-pattern detection.

## Go Anti-Patterns

### 1. Error Handling

```go
// ❌ Anti-pattern: Ignoring errors
result, _ := doSomething()

// ✅ Fix: Handle or explicitly ignore with comment
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doing something: %w", err)
}

// ❌ Anti-pattern: Naked returns
if err != nil {
    return err
}

// ✅ Fix: Wrap with context
if err != nil {
    return fmt.Errorf("processing user %s: %w", userID, err)
}
```

### 2. Goroutine Leaks

```go
// ❌ Anti-pattern: Goroutine without exit condition
go func() {
    for {
        doWork()  // Never exits!
    }
}()

// ✅ Fix: Use context for cancellation
go func(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        default:
            doWork()
        }
    }
}(ctx)

// ❌ Anti-pattern: Unbounded channel sends
ch := make(chan int)
go func() {
    for i := 0; ; i++ {
        ch <- i  // Blocks forever if no receiver
    }
}()

// ✅ Fix: Buffered channel or select with done
ch := make(chan int, 100)
go func(ctx context.Context) {
    for i := 0; ; i++ {
        select {
        case ch <- i:
        case <-ctx.Done():
            return
        }
    }
}(ctx)
```

### 3. Interface Pollution

```go
// ❌ Anti-pattern: God interface
type UserService interface {
    GetUser(id string) (*User, error)
    CreateUser(u *User) error
    UpdateUser(u *User) error
    DeleteUser(id string) error
    GetUserPosts(id string) ([]*Post, error)
    GetUserComments(id string) ([]*Comment, error)
    SendUserEmail(id, subject, body string) error
    // ... 20 more methods
}

// ✅ Fix: Small, focused interfaces
type UserGetter interface {
    GetUser(id string) (*User, error)
}

type UserWriter interface {
    CreateUser(u *User) error
    UpdateUser(u *User) error
}
```

### 4. init() Abuse

```go
// ❌ Anti-pattern: Complex init with side effects
func init() {
    db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
    if err != nil {
        log.Fatal(err)  // Crashes on import!
    }
    globalDB = db
}

// ✅ Fix: Explicit initialization
func NewService(dbURL string) (*Service, error) {
    db, err := sql.Open("postgres", dbURL)
    if err != nil {
        return nil, fmt.Errorf("connecting to database: %w", err)
    }
    return &Service{db: db}, nil
}
```

### 5. Slice Gotchas

```go
// ❌ Anti-pattern: Modifying slice in range
for i, v := range slice {
    slice[i] = v * 2  // Works, but confusing
}

// ✅ Fix: Be explicit
for i := 0; i < len(slice); i++ {
    slice[i] = slice[i] * 2
}

// ❌ Anti-pattern: Append to passed slice
func addItems(items []int) []int {
    return append(items, 1, 2, 3)  // May modify original!
}

// ✅ Fix: Copy first if modifying
func addItems(items []int) []int {
    result := make([]int, len(items), len(items)+3)
    copy(result, items)
    return append(result, 1, 2, 3)
}
```

## TypeScript Anti-Patterns

### 1. Any Type Abuse

```typescript
// ❌ Anti-pattern: any everywhere
function process(data: any): any {
    return data.foo.bar;  // No type safety
}

// ✅ Fix: Proper typing
interface ProcessInput {
    foo: { bar: string };
}

function process(data: ProcessInput): string {
    return data.foo.bar;
}

// ✅ Fix: Use unknown for truly unknown types
function process(data: unknown): string {
    if (isProcessInput(data)) {
        return data.foo.bar;
    }
    throw new Error('Invalid input');
}
```

### 2. Callback Hell

```typescript
// ❌ Anti-pattern: Nested callbacks
getUser(id, (user) => {
    getPosts(user.id, (posts) => {
        getComments(posts[0].id, (comments) => {
            // Deep nesting...
        });
    });
});

// ✅ Fix: async/await
async function getUserData(id: string) {
    const user = await getUser(id);
    const posts = await getPosts(user.id);
    const comments = await getComments(posts[0].id);
    return { user, posts, comments };
}
```

### 3. Mutable Exports

```typescript
// ❌ Anti-pattern: Mutable exported state
export let config = { apiUrl: 'http://localhost' };

// Somewhere else:
import { config } from './config';
config.apiUrl = 'https://evil.com';  // Mutates for everyone!

// ✅ Fix: Immutable or factory
export const config = Object.freeze({ apiUrl: 'http://localhost' });

// Or factory pattern
export function createConfig() {
    return { apiUrl: process.env.API_URL };
}
```

## Kubernetes Controller Anti-Patterns

### 1. Non-Idempotent Reconciliation

```go
// ❌ Anti-pattern: Creates on every reconcile
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Creates new ConfigMap every time!
    cm := &corev1.ConfigMap{...}
    if err := r.Create(ctx, cm); err != nil {
        return ctrl.Result{}, err
    }
    return ctrl.Result{}, nil
}

// ✅ Fix: Check existence first
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    cm := &corev1.ConfigMap{}
    err := r.Get(ctx, types.NamespacedName{Name: "my-cm", Namespace: req.Namespace}, cm)
    if errors.IsNotFound(err) {
        cm = &corev1.ConfigMap{...}
        return ctrl.Result{}, r.Create(ctx, cm)
    }
    if err != nil {
        return ctrl.Result{}, err
    }
    // Update if needed
    return ctrl.Result{}, nil
}
```

### 2. Missing Finalizers

```go
// ❌ Anti-pattern: No cleanup on deletion
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    obj := &v1.MyResource{}
    if err := r.Get(ctx, req.NamespacedName, obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    // Does work but no cleanup when deleted!
    return ctrl.Result{}, nil
}

// ✅ Fix: Use finalizers
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    obj := &v1.MyResource{}
    if err := r.Get(ctx, req.NamespacedName, obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // Handle deletion
    if !obj.DeletionTimestamp.IsZero() {
        if controllerutil.ContainsFinalizer(obj, finalizerName) {
            if err := r.cleanup(ctx, obj); err != nil {
                return ctrl.Result{}, err
            }
            controllerutil.RemoveFinalizer(obj, finalizerName)
            return ctrl.Result{}, r.Update(ctx, obj)
        }
        return ctrl.Result{}, nil
    }

    // Add finalizer
    if !controllerutil.ContainsFinalizer(obj, finalizerName) {
        controllerutil.AddFinalizer(obj, finalizerName)
        return ctrl.Result{}, r.Update(ctx, obj)
    }

    // Normal reconciliation
    return r.reconcile(ctx, obj)
}
```

### 3. Status Update in Same Transaction

```go
// ❌ Anti-pattern: Update spec and status together
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    obj.Spec.Replicas = 3
    obj.Status.Ready = true
    return ctrl.Result{}, r.Update(ctx, obj)  // Status change may be lost!
}

// ✅ Fix: Separate calls
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    obj.Spec.Replicas = 3
    if err := r.Update(ctx, obj); err != nil {
        return ctrl.Result{}, err
    }

    obj.Status.Ready = true
    return ctrl.Result{}, r.Status().Update(ctx, obj)
}
```

## General Anti-Patterns

### 1. Premature Optimization

- Optimizing before measuring
- Complex caching without proof of need
- Micro-optimizations that harm readability

### 2. Magic Numbers/Strings

```go
// ❌ Anti-pattern
if retries > 3 {

// ✅ Fix
const maxRetries = 3
if retries > maxRetries {
```

### 3. God Objects

- Single class/struct with many responsibilities
- Hundreds of lines in one file
- Everything depends on one component

### 4. Shotgun Surgery

- Single change requires edits in many places
- Indicates poor separation of concerns
- Fix: Extract shared functionality

### 5. Feature Envy

- Method uses another object's data more than its own
- Fix: Move method to the object it uses most
