# Rust Core Principles

This document outlines the fundamental principles that guide Rust development and differentiate it from other languages.

## The Three Pillars

### 1. Memory Safety Without Garbage Collection

**Ownership System**: Every value has a single owner. When the owner goes out of scope, the value is dropped.

```rust
// Ownership transfer (move)
let s1 = String::from("hello");
let s2 = s1; // s1 is no longer valid
```

**Borrowing Rules**:
- At any time, you can have either one mutable reference OR any number of immutable references
- References must always be valid

```rust
// Immutable borrows
let s = String::from("hello");
let r1 = &s;
let r2 = &s; // OK: multiple immutable borrows

// Mutable borrow
let mut s = String::from("hello");
let r1 = &mut s; // OK: one mutable borrow
// let r2 = &mut s; // ERROR: cannot borrow as mutable more than once
```

**Implications for Design**:
- Use `&T` for read-only access
- Use `&mut T` for exclusive write access
- Use `T` for ownership transfer
- Return owned types from functions that create new data
- Return borrowed types from functions that transform existing data

### 2. Fearless Concurrency

Rust's ownership system prevents data races at compile time.

**Key Insight**: If you can't have multiple mutable references in single-threaded code, you can't have data races in multi-threaded code.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

// Safe shared mutable state
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}
```

**Concurrency Primitives**:
- `Send`: Safe to transfer ownership between threads
- `Sync`: Safe to share references between threads
- Most types are `Send` and `Sync` by default
- Compiler enforces these traits automatically

### 3. Zero-Cost Abstractions

"What you don't use, you don't pay for. What you do use, you couldn't hand-code any better." - Bjarne Stroustrup (applied to Rust)

**Monomorphization**: Generic code is specialized at compile time.

```rust
// This generic function generates optimized machine code for each type
fn max<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

// Calling with i32 and f64 generates two optimized versions
let x = max(5, 10);      // Optimized for i32
let y = max(5.0, 10.0);  // Optimized for f64
```

**Implications**:
- Iterators compile to the same code as hand-written loops
- Trait objects have a small runtime cost (dynamic dispatch)
- Prefer static dispatch (generics) over dynamic dispatch (trait objects) when performance matters

## Design Principles

### Prefer Explicitness Over Implicitness

Rust favors explicit code that reveals intent.

**Error Handling**: No hidden exceptions or nil values.

```rust
// Bad: Hidden failure (doesn't exist in Rust)
// let result = parse_number(input); // Could panic or return null

// Good: Explicit error handling
let result: Result<i32, ParseIntError> = input.parse();
match result {
    Ok(num) => println!("Parsed: {}", num),
    Err(e) => eprintln!("Parse error: {}", e),
}
```

**Type Conversions**: No implicit coercion.

```rust
// Bad: Implicit conversion (doesn't compile)
// let x: i64 = 5i32; // ERROR

// Good: Explicit conversion
let x: i64 = 5i32.into(); // or i64::from(5i32)
```

### Make Invalid States Unrepresentable

Use the type system to prevent bugs at compile time.

```rust
// Bad: Using Option to represent connected/disconnected
struct Connection {
    socket: Option<TcpStream>,
}

// Good: Use types to represent states
enum ConnectionState {
    Disconnected,
    Connected(TcpStream),
}
```

**Builder Pattern with Type States**:

```rust
struct EmailBuilder<S> {
    state: S,
}

struct NoRecipient;
struct HasRecipient { to: String }

impl EmailBuilder<NoRecipient> {
    fn new() -> Self {
        EmailBuilder { state: NoRecipient }
    }

    fn to(self, recipient: String) -> EmailBuilder<HasRecipient> {
        EmailBuilder { state: HasRecipient { to: recipient } }
    }
}

impl EmailBuilder<HasRecipient> {
    // Can only send when we have a recipient
    fn send(self) -> Result<(), Error> {
        // Send email to self.state.to
        Ok(())
    }
}

// This won't compile - can't send without recipient
// EmailBuilder::new().send();

// This works
EmailBuilder::new().to("user@example.com".into()).send();
```

### Prefer Composition Over Inheritance

Rust has no class inheritance. Use traits and composition.

```rust
// Trait for shared behavior
trait Drawable {
    fn draw(&self);
}

// Composition
struct Button {
    label: String,
    style: Style,  // Composed field
}

impl Drawable for Button {
    fn draw(&self) {
        // Implementation
    }
}
```

### Encapsulation Through Modules

Use module visibility to control API surface.

```rust
mod database {
    pub struct Connection {
        // Private fields
        connection_string: String,
    }

    impl Connection {
        // Public constructor
        pub fn new(conn_str: String) -> Self {
            Connection { connection_string: conn_str }
        }

        // Public method
        pub fn query(&self, sql: &str) -> QueryResult {
            // Use private connection_string
            self.internal_query(sql)
        }

        // Private method
        fn internal_query(&self, sql: &str) -> QueryResult {
            // Implementation
        }
    }
}
```

## Practical Guidelines

### When to Clone vs Borrow

**Clone When**:
- You need owned data that outlives the original
- Sharing across thread boundaries (with Arc)
- The performance cost is acceptable
- Working with small Copy types (no cost)

**Borrow When**:
- Reading data temporarily
- You don't need to modify the original
- Performance is critical
- Working with large data structures

### When to Use Copy vs Clone

**Copy** (implicit, always safe):
- Small, stack-allocated types
- Types where bitwise copy is sufficient
- i32, f64, bool, char, tuples/arrays of Copy types

**Clone** (explicit, potentially expensive):
- Heap-allocated types (String, Vec, Box)
- Types with complex internal state
- Types where deep copy is needed

```rust
// Copy (implicit)
let x = 5;
let y = x; // x is still valid

// Clone (explicit)
let s1 = String::from("hello");
let s2 = s1.clone(); // Both s1 and s2 are valid
```

### Lifetime Elision Rules

The compiler can infer lifetimes in common cases:

```rust
// You write:
fn first_word(s: &str) -> &str { /* ... */ }

// Compiler infers:
fn first_word<'a>(s: &'a str) -> &'a str { /* ... */ }
```

**When to Write Explicit Lifetimes**:
- Multiple input references
- Struct definitions with references
- When elision rules don't apply

### Interior Mutability Pattern

When you need to mutate data through shared references.

```rust
use std::cell::RefCell;

struct Cache {
    data: RefCell<HashMap<String, Value>>,
}

impl Cache {
    fn get(&self, key: &str) -> Option<Value> {
        // Can mutate through &self
        self.data.borrow_mut().entry(key.to_string())
            .or_insert_with(|| expensive_computation(key))
            .clone()
    }
}
```

**Options**:
- `Cell<T>`: For Copy types, no runtime cost
- `RefCell<T>`: For any type, runtime borrow checking
- `Mutex<T>`: For thread-safe mutation
- `RwLock<T>`: For thread-safe read-heavy access

### Smart Pointers

Choose the right smart pointer for your use case:

- `Box<T>`: Single ownership, heap allocation
- `Rc<T>`: Shared ownership, single-threaded
- `Arc<T>`: Shared ownership, thread-safe
- `Cow<T>`: Clone on write, optimize for read-heavy

```rust
use std::rc::Rc;
use std::sync::Arc;

// Single-threaded shared ownership
let data = Rc::new(vec![1, 2, 3]);
let data2 = Rc::clone(&data);

// Multi-threaded shared ownership
let data = Arc::new(vec![1, 2, 3]);
let data2 = Arc::clone(&data);
thread::spawn(move || {
    println!("{:?}", data2);
});
```

## Anti-Patterns to Avoid

### Fighting the Borrow Checker

**Bad**: Using too many Rc/Arc to avoid borrow checker errors.

**Good**: Restructure your code to work with ownership.

```rust
// Bad: Over-using Arc
struct App {
    config: Arc<Config>,
    database: Arc<Database>,
    cache: Arc<Cache>,
}

// Good: Direct ownership or borrowing
struct App {
    config: Config,
    database: Database,
    cache: Cache,
}
```

### Premature Abstraction

**Bad**: Creating complex trait hierarchies before understanding the problem.

**Good**: Start concrete, extract abstractions when patterns emerge.

### Ignoring the Type System

**Bad**: Using `.unwrap()` everywhere or overly permissive types.

**Good**: Model your domain accurately with types.

```rust
// Bad: Stringly-typed
fn process_user(user_type: String) { /* ... */ }

// Good: Type-safe
enum UserType { Admin, Regular, Guest }
fn process_user(user_type: UserType) { /* ... */ }
```

### String Overuse

**Bad**: Using `String` everywhere.

**Good**: Use `&str` for borrowed string data, `String` only when you need ownership.

```rust
// Bad
fn greet(name: String) -> String {
    format!("Hello, {}", name)
}

// Good
fn greet(name: &str) -> String {
    format!("Hello, {}", name)
}
```

## Key Takeaways

1. **Ownership is not optional**: Learn to work with it, not against it
2. **The compiler is your friend**: Trust the error messages
3. **Explicit is better than implicit**: Rust favors clarity over brevity
4. **Zero-cost abstractions**: Use high-level features without performance penalty
5. **Type-driven design**: Let the type system prevent bugs
6. **Fearless refactoring**: The compiler catches most breaking changes
