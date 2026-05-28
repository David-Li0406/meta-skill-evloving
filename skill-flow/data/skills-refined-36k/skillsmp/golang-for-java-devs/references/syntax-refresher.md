# Go Syntax Refresher

Go syntax quick reference for Java developers. Clean, minimal, opinionated.

## Variables & Types

```go
// short declaration (most common)
name := "Hugo"           // inferred as string
count := 42              // inferred as int
users := []User{}        // inferred as slice of User

// explicit typing
var name string = "Hugo"
var count int = 42
var users []User

// constants
const ApiKey = "secret"  // exported (capitalized)
const apiKey = "secret"  // unexported (lowercase)
```

## Strings

```go
// concatenation
full := first + " " + last

// formatting (like String.format)
msg := fmt.Sprintf("Hello %s, you have %d messages", name, count)

// raw strings (like Java text blocks)
json := `{
    "name": "Hugo",
    "active": true
}`

// common operations
len(str)                      // str.length()
str == ""                     // str.isEmpty()
strings.Contains(str, "sub")  // str.contains("sub")
strings.HasPrefix(str, "pre") // str.startsWith("pre")
strings.Split(str, ",")       // str.split(",")
strings.TrimSpace(str)        // str.trim()
strings.ToLower(str)
strings.ToUpper(str)
```

## Collections

```go
// slices (like ArrayList)
names := []string{}
names = append(names, "Hugo")
names[0]                      // names.get(0)
len(names)                    // names.size()

// slice literal
names := []string{"Alice", "Bob"}

// maps (like HashMap)
ages := map[string]int{}
ages["Hugo"] = 30
ages["Hugo"]                  // ages.get("Hugo")
age, ok := ages["Hugo"]       // getOrDefault pattern
delete(ages, "Hugo")

// map literal
ages := map[string]int{
    "Hugo":  30,
    "Alice": 25,
}

// iterating
for _, name := range names { }         // for (String name : names)
for key, value := range ages { }       // for (var entry : map.entrySet())
for i, name := range names { }         // with index
```

## Control Flow

```go
// if (no parentheses, braces required)
if count > 0 {
    doSomething()
} else if count == 0 {
    doNothing()
} else {
    handleNegative()
}

// if with initialization
if user, err := findUser(id); err != nil {
    return err
} else {
    process(user)
}

// switch (no break needed, no fall-through by default)
switch status {
case "active":
    return "Running"
case "paused":
    return "On hold"
default:
    return "Unknown"
}

// for loops (Go only has for)
for i := 0; i < 10; i++ { }           // for (int i = 0; i < 10; i++)
for _, item := range items { }        // for (var item : items)
for condition { }                     // while (condition)
for { }                               // while (true)
```

## Functions

```go
// function definition
func greet(name string) string {
    return "Hello " + name
}

// multiple params of same type
func process(name string, count int, active bool) {}

// variadic (like Java varargs)
func log(messages ...string) {
    for _, msg := range messages {
        fmt.Println(msg)
    }
}
log("one", "two", "three")

// multiple return values (the big difference!)
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("divide by zero")
    }
    return a / b, nil
}

result, err := divide(10, 2)
if err != nil {
    return err
}
```

## Structs (like Java records/classes)

```go
// struct definition
type User struct {
    ID        string    `json:"id"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}

// creation
user := User{
    ID:    "123",
    Email: "hugo@example.com",
}

// or with new (returns pointer)
user := &User{ID: "123"}

// accessing fields
user.Email = "new@example.com"
fmt.Println(user.ID)
```

## Methods (functions on types)

```go
// method on struct (receiver)
func (u User) FullName() string {
    return u.FirstName + " " + u.LastName
}

// method with pointer receiver (can modify)
func (u *User) SetEmail(email string) {
    u.Email = email
}

// usage
user := User{FirstName: "Hugo", LastName: "Silva"}
name := user.FullName()
user.SetEmail("hugo@new.com")
```

## Interfaces

```go
// definition (small interfaces are idiomatic)
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// composition
type ReadWriter interface {
    Reader
    Writer
}

// implicit implementation (no "implements" keyword!)
type FileWriter struct {
    path string
}

func (f *FileWriter) Write(p []byte) (int, error) {
    // implementation
    return len(p), nil
}

// FileWriter now satisfies Writer interface automatically
```

## Error Handling

```go
// errors are values, not exceptions
user, err := findUser(id)
if err != nil {
    return nil, fmt.Errorf("finding user: %w", err)
}

// creating errors
err := errors.New("something went wrong")
err := fmt.Errorf("user %s not found", id)

// wrapping errors (for context)
if err != nil {
    return fmt.Errorf("processing order: %w", err)
}

// checking error types
if errors.Is(err, ErrNotFound) {
    // handle not found
}

// sentinel errors
var ErrNotFound = errors.New("not found")
var ErrInvalidInput = errors.New("invalid input")
```

## Pointers

```go
// Java: all objects are references
// Go: explicit pointers

x := 42
p := &x       // p is a pointer to x
*p = 43       // dereference to set value
fmt.Println(x) // 43

// why it matters: function arguments are copied
func double(x int) { x = x * 2 }    // doesn't change original
func double(x *int) { *x = *x * 2 } // changes original

// common pattern: return pointer for "might be nil"
func findUser(id string) *User {
    if notFound {
        return nil
    }
    return &user
}
```

## Defer (like try-with-resources)

```go
// defer runs when function returns
func readFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()  // runs at end of function

    // use f...
    return nil
}

// multiple defers run in LIFO order
defer fmt.Println("first")  // runs last
defer fmt.Println("second") // runs first
```

## Goroutines & Channels

```go
// goroutine (like virtual threads, but cheaper)
go doSomething()

// channel (typed communication)
ch := make(chan string)

// send
go func() {
    ch <- "hello"
}()

// receive
msg := <-ch

// buffered channel
ch := make(chan string, 10)

// select (like switch for channels)
select {
case msg := <-ch1:
    handle(msg)
case msg := <-ch2:
    handle(msg)
case <-time.After(5 * time.Second):
    handleTimeout()
}
```

## Packages & Imports

```go
// package declaration (must match directory name)
package user

// imports
import (
    "fmt"
    "strings"

    "github.com/go-chi/chi/v5"  // external package
)

// visibility (capitalization matters!)
func PublicFunction() {}   // exported (like public)
func privateFunction() {}  // unexported (like package-private)

type PublicStruct struct {
    PublicField  string  // exported
    privateField string  // unexported
}
```

## Struct Tags (like Java annotations, sort of)

```go
type User struct {
    ID        string `json:"id" db:"user_id" validate:"required"`
    Email     string `json:"email" validate:"required,email"`
    CreatedAt time.Time `json:"created_at,omitempty"`
}

// used by libraries for serialization, validation, ORM mapping
// not compile-time checked, be careful with typos
```

## Type Assertions & Type Switches

```go
// type assertion (like instanceof + cast)
var i interface{} = "hello"

s := i.(string)        // panics if wrong type
s, ok := i.(string)    // safe version

// type switch
switch v := i.(type) {
case string:
    fmt.Println("string:", v)
case int:
    fmt.Println("int:", v)
default:
    fmt.Println("unknown type")
}
```

## Generics (Go 1.18+)

```go
// generic function
func Map[T, U any](items []T, f func(T) U) []U {
    result := make([]U, len(items))
    for i, item := range items {
        result[i] = f(item)
    }
    return result
}

// generic type
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}

// constraints
func Min[T constraints.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}
```
