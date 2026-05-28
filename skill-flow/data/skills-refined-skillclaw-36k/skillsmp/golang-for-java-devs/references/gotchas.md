# Gotchas for Java Developers

Things that will feel wrong, break unexpectedly, or just annoy you.

## 1. No Exceptions - Errors Are Values

**Java:** Exceptions bubble up automatically. Caller might catch, might not.

**Go:** Errors are return values. You must handle them explicitly.
```go
user, err := findUser(id)
if err != nil {
    return nil, err  // must handle or propagate
}
```

**The trap:** If you ignore errors with `_`, your code silently fails:
```go
user, _ := findUser(id)  // error ignored, user might be nil
user.Email  // panic: nil pointer dereference
```

**Survival tactic:** Never ignore errors in production code. The `_` is a code smell.

## 2. Nil vs Zero Values

**Java:** `null` for all reference types. NPE is your enemy.

**Go:** Zero values differ by type, and nil has specific meanings:
```go
var s string   // "" (empty string, not nil)
var i int      // 0
var b bool     // false
var p *User    // nil (pointers can be nil)
var m map[string]int  // nil (nil map!)
var sl []int   // nil (nil slice, but usable!)

// nil slice is safe for len, append
var items []string
len(items)  // 0, ok
items = append(items, "x")  // ok

// nil map panics on write
var cache map[string]int
cache["key"] = 1  // panic!
cache = make(map[string]int)  // must initialize first
```

**Survival tactic:** Always initialize maps with `make()` or a literal.

## 3. Slices vs Arrays (They're Different!)

**Java:** Arrays and Lists are clearly different types.

**Go:** Arrays have fixed size, slices are dynamic - but they look similar:
```go
arr := [3]int{1, 2, 3}  // array - fixed size
sl := []int{1, 2, 3}    // slice - dynamic

// arrays are values (copied on assignment)
arr2 := arr
arr2[0] = 99
fmt.Println(arr[0])  // still 1

// slices share underlying array
sl2 := sl
sl2[0] = 99
fmt.Println(sl[0])  // 99!
```

**The trap:** Slicing creates a view, not a copy:
```go
original := []int{1, 2, 3, 4, 5}
subset := original[1:3]  // [2, 3]
subset[0] = 99
fmt.Println(original)  // [1, 99, 3, 4, 5] - modified!
```

**Survival tactic:** Use `copy()` or `slices.Clone()` when you need independence.

## 4. Maps Are Not Thread-Safe

**Java:** ConcurrentHashMap, synchronized blocks, or framework protection.

**Go:** Maps are NOT safe for concurrent access:
```go
m := make(map[string]int)

// this can corrupt the map and crash
go func() { m["a"] = 1 }()
go func() { m["b"] = 2 }()
```

**Solutions:**
```go
// option 1: sync.Mutex
type SafeMap struct {
    mu sync.Mutex
    m  map[string]int
}

func (s *SafeMap) Set(key string, val int) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.m[key] = val
}

// option 2: sync.Map (for specific use cases)
var m sync.Map
m.Store("key", value)
val, ok := m.Load("key")
```

## 5. Implicit Interface Satisfaction

**Java:** `class Foo implements Bar` - explicit and IDE-verifiable.

**Go:** Interfaces are satisfied implicitly:
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type MyFile struct{}

func (f *MyFile) Read(p []byte) (n int, err error) {
    return 0, nil
}

// MyFile now implements Reader - no declaration needed!
```

**The trap:** If you change the interface, implementations silently stop satisfying it. No compiler error unless you try to use them.

**Survival tactic:** Add compile-time checks:
```go
var _ Reader = (*MyFile)(nil)  // fails to compile if MyFile doesn't implement Reader
```

## 6. Exported vs Unexported (Capitalization)

**Java:** `public`, `private`, `protected` keywords.

**Go:** Capitalization determines visibility:
```go
type User struct {
    ID    string  // exported (public)
    email string  // unexported (package-private)
}

func ProcessUser() {}  // exported
func helper() {}       // unexported
```

**The trap:** JSON marshaling ignores unexported fields:
```go
type User struct {
    ID    string
    email string  // lowercase = unexported
}

user := User{ID: "123", email: "test@example.com"}
json, _ := json.Marshal(user)
// {"ID":"123"} - email is missing!
```

**Survival tactic:** Use struct tags for JSON field names:
```go
type User struct {
    ID    string `json:"id"`
    Email string `json:"email"`  // exported, custom JSON name
}
```

## 7. No Method Overloading

**Java:** Multiple methods with same name, different parameters.
```java
public void process(String s) {}
public void process(String s, int n) {}
public void process(User u) {}
```

**Go:** Not allowed. One method name, one signature.
```go
func Process(s string) {}
func ProcessWithCount(s string, n int) {}  // different name
func ProcessUser(u *User) {}               // different name
```

**Survival tactic:** Use variadic functions or functional options for flexible APIs:
```go
func NewServer(opts ...Option) *Server {}
```

## 8. Goroutine Leaks

**Java:** Thread pools manage lifecycle. Threads are expensive so you're careful.

**Go:** Goroutines are cheap, so you spawn many - and forget to clean them up:
```go
// leak: goroutine blocks forever on channel
func leak() {
    ch := make(chan int)
    go func() {
        val := <-ch  // blocks forever, no sender
        fmt.Println(val)
    }()
    // function returns, goroutine still waiting
}
```

**The trap:** Leaked goroutines accumulate memory and can't be garbage collected.

**Survival tactic:** Always have an exit path:
```go
func noLeak(ctx context.Context) {
    ch := make(chan int)
    go func() {
        select {
        case val := <-ch:
            fmt.Println(val)
        case <-ctx.Done():
            return  // exit when context cancelled
        }
    }()
}
```

## 9. Channel Deadlocks

**Java:** BlockingQueue operations can timeout.

**Go:** Unbuffered channels block until both sides are ready:
```go
// deadlock: main goroutine blocks forever
func main() {
    ch := make(chan int)
    ch <- 1  // blocks waiting for receiver - but there's none!
    fmt.Println(<-ch)
}
```

**Solutions:**
```go
// option 1: buffered channel
ch := make(chan int, 1)
ch <- 1  // doesn't block (buffer has space)

// option 2: separate goroutine
ch := make(chan int)
go func() { ch <- 1 }()
fmt.Println(<-ch)

// option 3: select with timeout
select {
case ch <- 1:
    // sent
case <-time.After(time.Second):
    // timeout
}
```

## 10. Pointer vs Value Receivers

**Java:** Methods always operate on the object reference.

**Go:** Methods can have pointer or value receivers - and it matters:
```go
type Counter struct {
    count int
}

// value receiver - gets a copy
func (c Counter) IncrementBad() {
    c.count++  // modifies the copy, not the original
}

// pointer receiver - modifies original
func (c *Counter) IncrementGood() {
    c.count++
}

c := Counter{}
c.IncrementBad()
fmt.Println(c.count)  // 0 - not changed!
c.IncrementGood()
fmt.Println(c.count)  // 1
```

**Rule of thumb:** Use pointer receivers when:
- Method modifies the receiver
- Struct is large (avoid copying)
- Consistency with other methods on the type

## 11. Loop Variable Capture (Fixed in Go 1.22+)

**Java:** Lambda capture creates a new binding per iteration (since Java 8).

**Go (before 1.22):** Loop variable is reused - closure captures the variable, not the value:
```go
// bug in Go < 1.22
for _, val := range []int{1, 2, 3} {
    go func() {
        fmt.Println(val)  // all print 3!
    }()
}
```

**Fixed in Go 1.22+:** Each iteration gets its own variable.

**For older Go:**
```go
for _, val := range []int{1, 2, 3} {
    val := val  // shadow the variable
    go func() {
        fmt.Println(val)  // correct: 1, 2, 3
    }()
}
```

## 12. defer Evaluates Arguments Immediately

**Java:** Code in finally block evaluates when finally runs.

**Go:** defer arguments are evaluated when defer is called:
```go
func example() {
    x := 1
    defer fmt.Println(x)  // captures x=1
    x = 2
    // prints 1, not 2!
}
```

**Survival tactic:** Use a closure to capture current value:
```go
defer func() { fmt.Println(x) }()  // prints current x when defer runs
```

## 13. String Iteration Gives Runes, Not Bytes

**Java:** String.charAt() gives chars (UTF-16 code units).

**Go:** Range over string gives runes (Unicode code points):
```go
s := "hello"
for i, r := range s {
    // i is byte index, r is rune
    fmt.Printf("%d: %c\n", i, r)
}

// for multi-byte characters
s := "caf\u00e9"  // "cafe" with accented e
for i, r := range s {
    fmt.Printf("%d: %c\n", i, r)
    // 0: c
    // 1: a
    // 2: f
    // 3: e  (index jumps because e is multi-byte)
}
```

**Survival tactic:** Use `[]rune(s)` if you need character indexing.

## 14. No Annotations - Everything Is Explicit

**Java:** Annotations configure behavior declaratively.
```java
@Transactional
@Cacheable
@Async
public void process() {}
```

**Go:** No annotations. You write the code:
```go
func (s *Service) Process(ctx context.Context) error {
    // manual transaction
    tx, err := s.db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    // manual caching
    if cached, ok := s.cache.Get(key); ok {
        return cached, nil
    }

    // manual async
    go func() {
        // background work
    }()

    return tx.Commit()
}
```

**The upside:** You can read the code and understand exactly what it does.

**The downside:** More code to write.
