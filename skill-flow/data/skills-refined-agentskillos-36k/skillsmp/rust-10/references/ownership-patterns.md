# Rust Ownership Patterns

## Core Ownership Rules

1. **Each value has exactly one owner**
2. **When the owner goes out of scope, the value is dropped**
3. **You can have either ONE mutable reference OR any number of immutable references**

## Borrowing Patterns

### Immutable Borrowing

```rust
fn main() {
    let s = String::from("hello");

    // Multiple immutable borrows OK
    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);
    // r1 and r2 go out of scope here
}

// Function that borrows
fn calculate_length(s: &String) -> usize {
    s.len()
}  // s goes out of scope, but doesn't drop the value
```

### Mutable Borrowing

```rust
fn main() {
    let mut s = String::from("hello");

    // Only one mutable borrow at a time
    let r1 = &mut s;
    r1.push_str(" world");
    // r1 must go out of scope before another borrow

    let r2 = &mut s;  // OK - r1 is no longer used
    println!("{}", r2);
}

// Function that mutably borrows
fn append_world(s: &mut String) {
    s.push_str(" world");
}
```

### The Slice Pattern

```rust
// Slices borrow part of a collection
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    &s[..]
}

fn main() {
    let s = String::from("hello world");
    let word = first_word(&s);  // Borrows s
    // s.clear();  // ERROR! Can't mutate while borrowed
    println!("{}", word);
}
```

## Common Ownership Patterns

### Clone When Needed

```rust
// Clone for independent copies
#[derive(Clone)]
struct Config {
    name: String,
    value: i32,
}

fn main() {
    let original = Config {
        name: String::from("test"),
        value: 42,
    };

    let copy = original.clone();  // Deep copy
    // Both original and copy are independent
}
```

### Copy for Simple Types

```rust
// Copy for stack-only data
#[derive(Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = p1;  // Copied, not moved
    // Both p1 and p2 are valid
    println!("{}, {}", p1.x, p2.x);
}
```

### Take Ownership with Into

```rust
// Accept owned or borrowed with Into
fn greet(name: impl Into<String>) {
    let name: String = name.into();
    println!("Hello, {}!", name);
}

fn main() {
    greet("World");  // &str -> String
    greet(String::from("Rust"));  // String stays String
}
```

### AsRef for Flexible Borrowing

```rust
use std::path::Path;

// Accept anything that can be referenced as a path
fn read_file(path: impl AsRef<Path>) -> std::io::Result<String> {
    std::fs::read_to_string(path)
}

fn main() {
    read_file("config.txt");  // &str
    read_file(String::from("config.txt"));  // String
    read_file(Path::new("config.txt"));  // &Path
}
```

## Interior Mutability

### RefCell for Single-Threaded Mutation

```rust
use std::cell::RefCell;

struct Cache {
    data: RefCell<Vec<String>>,
}

impl Cache {
    fn add(&self, item: String) {
        // Mutate through immutable reference
        self.data.borrow_mut().push(item);
    }

    fn get(&self, index: usize) -> Option<String> {
        self.data.borrow().get(index).cloned()
    }
}
```

### Cell for Copy Types

```rust
use std::cell::Cell;

struct Counter {
    count: Cell<i32>,
}

impl Counter {
    fn increment(&self) {
        // No borrow, just get/set
        self.count.set(self.count.get() + 1);
    }
}
```

### Mutex for Thread-Safe Mutation

```rust
use std::sync::Mutex;

struct SharedCounter {
    count: Mutex<i32>,
}

impl SharedCounter {
    fn increment(&self) {
        let mut count = self.count.lock().unwrap();
        *count += 1;
    }
}
```

## Smart Pointers

### Box for Heap Allocation

```rust
// Box for recursive types
enum List {
    Cons(i32, Box<List>),
    Nil,
}

// Box for large stack data
fn process_large_data() {
    let large = Box::new([0u8; 1_000_000]);
    // Data is on heap, only pointer on stack
}
```

### Rc for Shared Ownership

```rust
use std::rc::Rc;

struct Node {
    value: i32,
    children: Vec<Rc<Node>>,
}

fn main() {
    let shared = Rc::new(Node {
        value: 1,
        children: vec![],
    });

    let clone1 = Rc::clone(&shared);  // Increment ref count
    let clone2 = Rc::clone(&shared);

    println!("Count: {}", Rc::strong_count(&shared));  // 3
}
```

### Arc for Thread-Safe Shared Ownership

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let data = Arc::new(vec![1, 2, 3]);
    let mut handles = vec![];

    for _ in 0..3 {
        let data = Arc::clone(&data);
        handles.push(thread::spawn(move || {
            println!("{:?}", data);
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
```

## Lifetime Patterns

### Elision Rules

```rust
// Rule 1: Each parameter gets its own lifetime
fn foo(x: &i32) {}  // fn foo<'a>(x: &'a i32)

// Rule 2: If one input lifetime, output gets same
fn foo(x: &i32) -> &i32 { x }  // fn foo<'a>(x: &'a i32) -> &'a i32

// Rule 3: If &self or &mut self, output gets self's lifetime
impl Foo {
    fn bar(&self) -> &str { &self.name }
}
```

### Explicit Lifetimes

```rust
// When multiple references with different lifetimes
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct holding references
struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
}
```

### Static Lifetime

```rust
// String literals have 'static lifetime
let s: &'static str = "I live forever";

// Owned data can satisfy 'static
fn takes_static<T: 'static>(value: T) {
    // T must not contain non-static references
}

takes_static(String::from("owned"));  // OK
takes_static(42);  // OK
```

## Anti-Patterns to Avoid

### Fighting the Borrow Checker

```rust
// ❌ Cloning to satisfy borrow checker
let data = expensive_computation();
let clone = data.clone();  // Unnecessary if you restructure

// ✅ Restructure to avoid clone
fn process(data: &Data) -> Result {
    // Work with reference
}
```

### Rc/RefCell as First Resort

```rust
// ❌ Using Rc<RefCell<T>> for everything
let data = Rc::new(RefCell::new(vec![]));

// ✅ Prefer ownership and borrowing first
struct Container {
    data: Vec<i32>,  // Owned
}

impl Container {
    fn add(&mut self, item: i32) {
        self.data.push(item);
    }
}
```

### Unnecessary Lifetimes

```rust
// ❌ Explicit when elision works
fn first<'a>(s: &'a str) -> &'a str {
    &s[..1]
}

// ✅ Let elision work
fn first(s: &str) -> &str {
    &s[..1]
}
```
