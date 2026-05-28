# Common Rust Errors and Solutions

Frequently encountered errors and how to fix them.

## Borrow Checker Errors

### Cannot Borrow as Mutable More Than Once

**Error**:
```rust
let mut vec = vec![1, 2, 3];
let first = &mut vec[0];
let second = &mut vec[1];  // Error!
```

**Solutions**:
```rust
// 1. Use split_at_mut
let (left, right) = vec.split_at_mut(1);
let first = &mut left[0];
let second = &mut right[0];

// 2. Use indexing (unsafe under the hood)
vec[0] = 10;
vec[1] = 20;

// 3. Sequential access
{
    let first = &mut vec[0];
    *first = 10;
}
{
    let second = &mut vec[1];
    *second = 20;
}
```

### Cannot Borrow as Mutable Because It is Also Borrowed as Immutable

**Error**:
```rust
let mut map = HashMap::new();
let key = "count";
let value = map.get(key).unwrap_or(&0);
map.insert(key, value + 1);  // Error!
```

**Solutions**:
```rust
// 1. Clone the value
let value = map.get(key).cloned().unwrap_or(0);
map.insert(key, value + 1);

// 2. Use entry API
*map.entry(key).or_insert(0) += 1;

// 3. Split into steps
let value = map.get(key).unwrap_or(&0) + 1;
map.insert(key, value);
```

### Borrowed Value Does Not Live Long Enough

**Error**:
```rust
fn get_string() -> &str {
    let s = String::from("hello");
    &s  // Error: s is dropped at end of function
}
```

**Solutions**:
```rust
// 1. Return owned value
fn get_string() -> String {
    String::from("hello")
}

// 2. Use static lifetime
fn get_string() -> &'static str {
    "hello"
}

// 3. Pass in storage
fn get_string(buf: &mut String) {
    buf.push_str("hello");
}

// 4. Use Cow (Clone on Write)
fn get_string() -> Cow<'static, str> {
    Cow::Borrowed("hello")
}
```

## Ownership Errors

### Use of Moved Value

**Error**:
```rust
let s1 = String::from("hello");
let s2 = s1;
println!("{}", s1);  // Error: s1 was moved
```

**Solutions**:
```rust
// 1. Clone
let s1 = String::from("hello");
let s2 = s1.clone();
println!("{}", s1);  // OK

// 2. Borrow instead
let s1 = String::from("hello");
let s2 = &s1;
println!("{}", s1);  // OK

// 3. Use Copy types
let x = 5;
let y = x;
println!("{}", x);  // OK: i32 is Copy
```

### Cannot Move Out of Borrowed Content

**Error**:
```rust
fn first_element(vec: &Vec<String>) -> String {
    vec[0]  // Error: can't move out of borrowed Vec
}
```

**Solutions**:
```rust
// 1. Clone the element
fn first_element(vec: &Vec<String>) -> String {
    vec[0].clone()
}

// 2. Return a reference
fn first_element(vec: &Vec<String>) -> &str {
    &vec[0]
}

// 3. Take ownership
fn first_element(vec: Vec<String>) -> String {
    vec.into_iter().next().unwrap()
}
```

## Lifetime Errors

### Missing Lifetime Specifier

**Error**:
```rust
fn longest(x: &str, y: &str) -> &str {  // Error: which lifetime?
    if x.len() > y.len() { x } else { y }
}
```

**Solution**:
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

### Explicit Lifetime Required

**Error**:
```rust
struct Excerpt {
    part: &str,  // Error: missing lifetime
}
```

**Solution**:
```rust
struct Excerpt<'a> {
    part: &'a str,
}
```

## Trait Errors

### Trait Bound Not Satisfied

**Error**:
```rust
fn print_it<T>(value: T) {
    println!("{}", value);  // Error: T doesn't implement Display
}
```

**Solutions**:
```rust
// 1. Add trait bound
fn print_it<T: std::fmt::Display>(value: T) {
    println!("{}", value);
}

// 2. Use Debug instead
fn print_it<T: std::fmt::Debug>(value: T) {
    println!("{:?}", value);
}

// 3. impl Trait syntax
fn print_it(value: impl std::fmt::Display) {
    println!("{}", value);
}
```

### Trait Object Cannot Be Made

**Error**:
```rust
trait MyTrait {
    fn generic_method<T>(&self, value: T);  // Error: not object-safe
}
```

**Solution**:
```rust
// 1. Remove generic method
trait MyTrait {
    fn method(&self, value: String);
}

// 2. Use associated type
trait MyTrait {
    type Value;
    fn method(&self, value: Self::Value);
}
```

## Type Errors

### Type Mismatch

**Error**:
```rust
let x: i32 = 5;
let y: i64 = x;  // Error: mismatched types
```

**Solutions**:
```rust
// Explicit conversion
let y: i64 = x.into();
let y: i64 = i64::from(x);
let y = x as i64;
```

### Cannot Infer Type

**Error**:
```rust
let numbers = vec![];  // Error: cannot infer type
```

**Solutions**:
```rust
// 1. Type annotation
let numbers: Vec<i32> = vec![];

// 2. Turbofish
let numbers = Vec::<i32>::new();
let numbers = vec![1, 2, 3].into_iter().collect::<Vec<_>>();
```

## Async Errors

### `await` Outside Async

**Error**:
```rust
fn fetch_data() -> String {
    reqwest::get("url").await  // Error: await in non-async fn
}
```

**Solution**:
```rust
async fn fetch_data() -> String {
    reqwest::get("url").await.unwrap().text().await.unwrap()
}
```

### Async Block Returns Different Type

**Error**:
```rust
let future = async {
    if condition {
        return 42;
    }
    "hello"  // Error: mismatched types
};
```

**Solution**:
```rust
let future = async {
    if condition {
        return 42.to_string();
    }
    "hello".to_string()
};
```

## Common Panic Scenarios

### Index Out of Bounds

```rust
// Bad
let vec = vec![1, 2, 3];
let item = vec[10];  // Panic!

// Good
let item = vec.get(10).unwrap_or(&0);
let item = vec.get(10).ok_or(Error::NotFound)?;
```

### Unwrap on None/Err

```rust
// Bad
let value = some_option.unwrap();  // Panic if None

// Good
let value = some_option.unwrap_or(default);
let value = some_option.ok_or(Error::Missing)?;
let value = some_option.expect("value must exist");
```

### Division by Zero

```rust
// Bad
let result = x / y;  // Panic if y == 0

// Good
if y == 0 {
    return Err(Error::DivisionByZero);
}
let result = x.checked_div(y).ok_or(Error::DivisionByZero)?;
```

## Closure Errors

### Closure May Outlive Current Function

**Error**:
```rust
fn make_closure() -> impl Fn() {
    let x = String::from("hello");
    || println!("{}", x)  // Error: x would be dropped
}
```

**Solutions**:
```rust
// 1. Move ownership
fn make_closure() -> impl Fn() {
    let x = String::from("hello");
    move || println!("{}", x)
}

// 2. Use 'static data
fn make_closure() -> impl Fn() {
    let x = "hello";
    move || println!("{}", x)
}
```

### Cannot Infer Closure Type

**Error**:
```rust
let f = |x| x + 1;  // Error: cannot infer type
```

**Solution**:
```rust
let f = |x: i32| x + 1;
let f: fn(i32) -> i32 = |x| x + 1;
```

## Pattern Matching Errors

### Non-Exhaustive Patterns

**Error**:
```rust
enum Status { Active, Inactive, Pending }

match status {
    Status::Active => {},
    Status::Inactive => {},
    // Error: missing Pending
}
```

**Solutions**:
```rust
// 1. Add missing pattern
match status {
    Status::Active => {},
    Status::Inactive => {},
    Status::Pending => {},
}

// 2. Use wildcard
match status {
    Status::Active => {},
    _ => {},
}
```

## Send/Sync Errors

### `Rc` Cannot Be Sent Between Threads

**Error**:
```rust
let data = Rc::new(vec![1, 2, 3]);
thread::spawn(move || {
    println!("{:?}", data);  // Error: Rc is not Send
});
```

**Solution**:
```rust
// Use Arc instead
let data = Arc::new(vec![1, 2, 3]);
thread::spawn(move || {
    println!("{:?}", data);
});
```

### RefCell Not Sync

**Error**:
```rust
let data = Arc::new(RefCell::new(0));  // Error: RefCell is not Sync
```

**Solution**:
```rust
// Use Mutex instead
let data = Arc::new(Mutex::new(0));
```

## Quick Fixes Cheat Sheet

| Error | Quick Fix |
|-------|-----------|
| Value moved | `.clone()` or use `&` |
| Borrow checker issue | Narrow scope with `{}` blocks |
| Lifetime error | Add lifetime annotations |
| Missing trait | Add `#[derive(...)]` or impl manually |
| Type mismatch | Use `.into()` or `.try_into()?` |
| Cannot infer | Add type annotation `: Type` |
| async/await | Make function `async fn` |
| Index panic | Use `.get()` instead of `[]` |
| Thread safety | Use `Arc` instead of `Rc`, `Mutex` instead of `RefCell` |
