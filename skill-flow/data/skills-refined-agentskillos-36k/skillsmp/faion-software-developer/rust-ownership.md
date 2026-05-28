---
id: rust-ownership
name: "Rust Ownership Model"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Rust Ownership Model

## Overview

Rust's ownership system is its most distinctive feature, enabling memory safety without garbage collection. This methodology covers ownership rules, borrowing, lifetimes, and common patterns for working with Rust's unique memory model.

## When to Use

- All Rust projects
- Systems programming
- Performance-critical applications
- Memory-safe concurrent code
- When avoiding garbage collection overhead

## Key Principles

1. **Each value has one owner** - Only one variable owns a value at a time
2. **Ownership can be transferred** - Move semantics by default
3. **Borrowing enables sharing** - References allow temporary access
4. **Lifetimes ensure safety** - Compiler tracks reference validity
5. **RAII for resources** - Resources released when owner goes out of scope

## Best Practices

### Ownership Rules

```rust
fn main() {
    // Rule 1: Each value has exactly one owner
    let s1 = String::from("hello"); // s1 owns the String

    // Rule 2: When owner goes out of scope, value is dropped
    {
        let s2 = String::from("world");
    } // s2 dropped here

    // Rule 3: Assignment moves ownership (for non-Copy types)
    let s3 = s1; // s1 moved to s3, s1 no longer valid
    // println!("{}", s1); // ERROR: s1 was moved

    // Copy types are copied, not moved
    let x = 5;
    let y = x; // x is copied, both valid
    println!("{} {}", x, y);
}
```

### Borrowing and References

```rust
// Immutable borrow: multiple allowed
fn calculate_length(s: &String) -> usize {
    s.len()
}

// Mutable borrow: only one at a time
fn append_world(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let mut s = String::from("hello");

    // Multiple immutable borrows OK
    let len1 = calculate_length(&s);
    let len2 = calculate_length(&s);

    // Mutable borrow
    append_world(&mut s);

    // Can't have mutable and immutable borrows simultaneously
    let r1 = &s;
    let r2 = &s;
    // let r3 = &mut s; // ERROR: can't borrow mutably while borrowed immutably
    println!("{} {}", r1, r2);

    // After last use of r1 and r2, mutable borrow OK
    let r3 = &mut s;
    r3.push_str("!");
}
```

### Lifetimes

```rust
// Explicit lifetime annotation
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Lifetime in struct
struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    fn level(&self) -> i32 {
        3
    }

    fn announce_and_return(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.part
    }
}

// Static lifetime
fn get_static_str() -> &'static str {
    "I live forever"
}

// Multiple lifetimes
fn complex<'a, 'b>(x: &'a str, y: &'b str) -> &'a str {
    x
}
```

### Smart Pointers

```rust
use std::rc::Rc;
use std::cell::RefCell;
use std::sync::Arc;

// Box: heap allocation with single ownership
fn box_example() {
    let b = Box::new(5);
    println!("b = {}", b);

    // Recursive types need Box
    enum List {
        Cons(i32, Box<List>),
        Nil,
    }

    use List::{Cons, Nil};
    let list = Cons(1, Box::new(Cons(2, Box::new(Nil))));
}

// Rc: reference counting (single-threaded)
fn rc_example() {
    let data = Rc::new(vec![1, 2, 3]);
    let data2 = Rc::clone(&data); // Increment reference count
    let data3 = Rc::clone(&data);

    println!("Reference count: {}", Rc::strong_count(&data)); // 3
}

// RefCell: interior mutability
fn refcell_example() {
    let data = RefCell::new(vec![1, 2, 3]);

    // Borrow mutably at runtime
    data.borrow_mut().push(4);

    // Borrow immutably
    println!("{:?}", data.borrow());
}

// Rc<RefCell<T>>: shared mutable state
fn rc_refcell_example() {
    let shared = Rc::new(RefCell::new(vec![1, 2, 3]));
    let shared2 = Rc::clone(&shared);

    shared.borrow_mut().push(4);
    shared2.borrow_mut().push(5);

    println!("{:?}", shared.borrow()); // [1, 2, 3, 4, 5]
}

// Arc: thread-safe reference counting
use std::sync::Mutex;
use std::thread;

fn arc_example() {
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

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

### Ownership Patterns in Structs

```rust
// Owned data
struct User {
    name: String,
    email: String,
}

impl User {
    fn new(name: String, email: String) -> Self {
        Self { name, email }
    }

    // Takes ownership of self
    fn into_name(self) -> String {
        self.name
    }

    // Borrows self
    fn name(&self) -> &str {
        &self.name
    }

    // Mutably borrows self
    fn set_name(&mut self, name: String) {
        self.name = name;
    }
}

// Builder pattern with ownership
struct RequestBuilder {
    url: String,
    method: String,
    headers: Vec<(String, String)>,
}

impl RequestBuilder {
    fn new(url: impl Into<String>) -> Self {
        Self {
            url: url.into(),
            method: "GET".to_string(),
            headers: vec![],
        }
    }

    fn method(mut self, method: impl Into<String>) -> Self {
        self.method = method.into();
        self
    }

    fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.push((key.into(), value.into()));
        self
    }

    fn build(self) -> Request {
        Request {
            url: self.url,
            method: self.method,
            headers: self.headers,
        }
    }
}

let request = RequestBuilder::new("https://api.example.com")
    .method("POST")
    .header("Content-Type", "application/json")
    .build();
```

### Clone and Copy Traits

```rust
// Copy: simple bitwise copy (stack-only types)
#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

// Clone: explicit deep copy
#[derive(Debug, Clone)]
struct Config {
    name: String,
    values: Vec<i32>,
}

fn main() {
    // Copy types
    let p1 = Point { x: 1, y: 2 };
    let p2 = p1; // Copied, p1 still valid
    println!("{:?} {:?}", p1, p2);

    // Clone types
    let c1 = Config {
        name: "test".to_string(),
        values: vec![1, 2, 3],
    };
    let c2 = c1.clone(); // Explicit clone
    // let c3 = c1; // Would move c1
}
```

### Cow (Clone-on-Write)

```rust
use std::borrow::Cow;

// Avoid cloning when not needed
fn process_text(input: &str) -> Cow<str> {
    if input.contains("bad") {
        // Only clone if modification needed
        Cow::Owned(input.replace("bad", "good"))
    } else {
        // No clone, just borrow
        Cow::Borrowed(input)
    }
}

fn main() {
    let text1 = "hello world";
    let result1 = process_text(text1); // Borrowed

    let text2 = "bad word";
    let result2 = process_text(text2); // Owned

    // Both can be used as &str
    println!("{} {}", result1, result2);
}
```

### Ownership in Closures

```rust
fn main() {
    let s = String::from("hello");

    // Borrow by reference
    let closure1 = || println!("{}", s);
    closure1();

    // Move ownership into closure
    let closure2 = move || {
        println!("{}", s);
    };
    closure2();
    // s no longer accessible here

    // FnOnce: takes ownership, can only be called once
    let s = String::from("hello");
    let consume = move || {
        drop(s);
    };
    consume();
    // consume(); // ERROR: closure moved
}
```

## Anti-patterns

### Avoid: Fighting the Borrow Checker

```rust
// BAD - trying to keep references too long
fn bad_example() {
    let mut v = vec![1, 2, 3];
    let first = &v[0]; // immutable borrow
    v.push(4); // ERROR: can't mutate while borrowed
    println!("{}", first);
}

// GOOD - restructure to satisfy borrow checker
fn good_example() {
    let mut v = vec![1, 2, 3];
    println!("{}", v[0]); // Use immediately
    v.push(4); // Now safe to mutate
}
```

### Avoid: Overusing Clone

```rust
// BAD - unnecessary clones
fn process_bad(data: &Vec<String>) -> Vec<String> {
    data.clone() // Clone entire vector
        .into_iter()
        .filter(|s| !s.is_empty())
        .collect()
}

// GOOD - work with references
fn process_good(data: &[String]) -> Vec<&str> {
    data.iter()
        .filter(|s| !s.is_empty())
        .map(|s| s.as_str())
        .collect()
}
```

### Avoid: Returning References to Local Data

```rust
// BAD - returns dangling reference
fn bad_return() -> &String {
    let s = String::from("hello");
    &s // ERROR: s will be dropped
}

// GOOD - return owned value
fn good_return() -> String {
    String::from("hello")
}
```

## References

- [The Rust Book - Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
- [Rust by Example - Ownership](https://doc.rust-lang.org/rust-by-example/scope.html)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/)
- [Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/)
