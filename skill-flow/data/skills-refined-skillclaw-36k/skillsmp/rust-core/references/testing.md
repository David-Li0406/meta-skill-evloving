# Testing in Rust

Comprehensive guide to testing strategies, tools, and best practices in Rust.

## Test Organization

### Unit Tests

Place unit tests in a `tests` module within the same file as the code.

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, 1), 0);
    }
}
```

### Integration Tests

Create `tests/` directory at project root for integration tests.

```
my_project/
├── src/
│   └── lib.rs
└── tests/
    ├── integration_test.rs
    └── common/
        └── mod.rs
```

```rust
// tests/integration_test.rs
use my_project::some_function;

#[test]
fn test_public_api() {
    assert_eq!(some_function(), expected_value);
}

// tests/common/mod.rs - shared test utilities
pub fn setup() -> TestEnvironment {
    // Common setup code
}
```

### Doc Tests

Examples in documentation are automatically tested.

```rust
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// use my_crate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Test Assertions

### Basic Assertions

```rust
#[test]
fn test_assertions() {
    assert!(true);
    assert_eq!(2 + 2, 4);
    assert_ne!(2 + 2, 5);
}
```

### Custom Messages

```rust
#[test]
fn test_with_message() {
    let result = compute();
    assert_eq!(
        result, expected,
        "Computation failed: got {} expected {}",
        result, expected
    );
}
```

### Panic Testing

```rust
#[test]
#[should_panic]
fn test_panic() {
    panic!("This test should panic");
}

#[test]
#[should_panic(expected = "division by zero")]
fn test_panic_with_message() {
    divide(10, 0);
}
```

### Result in Tests

```rust
#[test]
fn test_with_result() -> Result<(), Box<dyn std::error::Error>> {
    let result = fallible_operation()?;
    assert_eq!(result, expected);
    Ok(())
}
```

## Test Attributes

### Ignoring Tests

```rust
#[test]
#[ignore]
fn expensive_test() {
    // Run with: cargo test -- --ignored
}
```

### Conditional Compilation

```rust
#[test]
#[cfg(target_os = "linux")]
fn linux_only_test() {
    // Only runs on Linux
}

#[test]
#[cfg(not(target_env = "msvc"))]
fn non_msvc_test() {
    // Doesn't run on MSVC
}
```

## Test Organization Patterns

### Nested Test Modules

```rust
#[cfg(test)]
mod tests {
    use super::*;

    mod addition {
        use super::*;

        #[test]
        fn positive_numbers() {
            assert_eq!(add(2, 3), 5);
        }

        #[test]
        fn negative_numbers() {
            assert_eq!(add(-2, -3), -5);
        }
    }

    mod subtraction {
        use super::*;

        #[test]
        fn positive_result() {
            assert_eq!(subtract(5, 3), 2);
        }
    }
}
```

### Test Fixtures

```rust
#[cfg(test)]
mod tests {
    use super::*;

    fn setup() -> TestDatabase {
        TestDatabase::new()
            .with_user("alice")
            .with_user("bob")
    }

    #[test]
    fn test_query() {
        let db = setup();
        assert_eq!(db.user_count(), 2);
    }
}
```

## Property-Based Testing with `proptest`

Test properties that should hold for all inputs.

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reversing_twice_is_identity(s in "\\PC*") {
        let reversed_twice = s.chars()
            .rev()
            .collect::<String>()
            .chars()
            .rev()
            .collect::<String>();
        assert_eq!(s, reversed_twice);
    }

    #[test]
    fn test_sort_is_idempotent(mut vec in prop::collection::vec(any::<i32>(), 0..100)) {
        vec.sort();
        let sorted = vec.clone();
        vec.sort();
        assert_eq!(vec, sorted);
    }
}
```

### Custom Strategies

```rust
use proptest::prelude::*;

#[derive(Debug, Clone)]
struct Email {
    local: String,
    domain: String,
}

fn email_strategy() -> impl Strategy<Value = Email> {
    ("[a-z]{1,10}", "[a-z]{1,10}\\.[a-z]{2,3}")
        .prop_map(|(local, domain)| Email { local, domain })
}

proptest! {
    #[test]
    fn test_email_validation(email in email_strategy()) {
        assert!(validate_email(&email));
    }
}
```

## Mocking

### Manual Mocking with Traits

```rust
pub trait EmailSender {
    fn send(&self, to: &str, message: &str) -> Result<(), Error>;
}

pub struct SmtpEmailSender;

impl EmailSender for SmtpEmailSender {
    fn send(&self, to: &str, message: &str) -> Result<(), Error> {
        // Real implementation
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    struct MockEmailSender {
        sent_emails: RefCell<Vec<(String, String)>>,
    }

    impl MockEmailSender {
        fn new() -> Self {
            MockEmailSender {
                sent_emails: RefCell::new(Vec::new()),
            }
        }

        fn get_sent(&self) -> Vec<(String, String)> {
            self.sent_emails.borrow().clone()
        }
    }

    impl EmailSender for MockEmailSender {
        fn send(&self, to: &str, message: &str) -> Result<(), Error> {
            self.sent_emails
                .borrow_mut()
                .push((to.to_string(), message.to_string()));
            Ok(())
        }
    }

    #[test]
    fn test_notification_system() {
        let sender = MockEmailSender::new();
        notify_user(&sender, "test@example.com");

        let sent = sender.get_sent();
        assert_eq!(sent.len(), 1);
        assert_eq!(sent[0].0, "test@example.com");
    }
}
```

### Using `mockall`

```rust
use mockall::*;

#[automock]
pub trait Database {
    fn get_user(&self, id: u64) -> Result<User, Error>;
    fn save_user(&mut self, user: User) -> Result<(), Error>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_service() {
        let mut mock_db = MockDatabase::new();

        // Set expectations
        mock_db
            .expect_get_user()
            .with(eq(1))
            .times(1)
            .returning(|_| Ok(User::new("Alice")));

        mock_db
            .expect_save_user()
            .times(1)
            .returning(|_| Ok(()));

        // Use mock in test
        let service = UserService::new(mock_db);
        let user = service.get_and_update_user(1).unwrap();
        assert_eq!(user.name, "Alice");
    }
}
```

## Benchmarking with Criterion

```rust
// benches/my_benchmark.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
```

```toml
# Cargo.toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "my_benchmark"
harness = false
```

### Benchmarking Comparisons

```rust
use criterion::{BenchmarkId, Criterion};

fn comparison_benchmark(c: &mut Criterion) {
    let mut group = c.benchmark_group("sorting");

    for size in [10, 100, 1000].iter() {
        group.bench_with_input(
            BenchmarkId::new("vec", size),
            size,
            |b, &size| {
                b.iter(|| {
                    let mut vec: Vec<i32> = (0..size).collect();
                    vec.sort();
                });
            },
        );

        group.bench_with_input(
            BenchmarkId::new("btreeset", size),
            size,
            |b, &size| {
                b.iter(|| {
                    let set: BTreeSet<i32> = (0..size).collect();
                });
            },
        );
    }

    group.finish();
}
```

## Snapshot Testing

Testing output against saved snapshots.

```rust
// Using insta crate
use insta::assert_snapshot;

#[test]
fn test_render_html() {
    let html = render_page(&Page {
        title: "Test Page",
        content: "Hello, world!",
    });

    assert_snapshot!(html);
}

// First run creates snapshot
// Subsequent runs compare against it
// Run `cargo insta review` to review changes
```

## Testing Async Code

```rust
#[tokio::test]
async fn test_async_function() {
    let result = async_operation().await;
    assert_eq!(result, expected);
}

#[tokio::test]
async fn test_timeout() {
    let result = tokio::time::timeout(
        Duration::from_secs(1),
        long_running_operation()
    ).await;

    assert!(result.is_ok());
}
```

### Testing Concurrent Code

```rust
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_concurrent_operations() {
    let handles: Vec<_> = (0..10)
        .map(|i| {
            tokio::spawn(async move {
                perform_operation(i).await
            })
        })
        .collect();

    for handle in handles {
        assert!(handle.await.is_ok());
    }
}
```

## Test Coverage

### Using `tarpaulin`

```bash
# Install
cargo install cargo-tarpaulin

# Run coverage
cargo tarpaulin --out Html --output-dir coverage

# With specific tests
cargo tarpaulin --test integration_test
```

### Using `llvm-cov`

```bash
# Install
rustup component add llvm-tools-preview
cargo install cargo-llvm-cov

# Generate coverage
cargo llvm-cov --html

# View coverage
open target/llvm-cov/html/index.html
```

## Testing Best Practices

### AAA Pattern (Arrange, Act, Assert)

```rust
#[test]
fn test_user_creation() {
    // Arrange
    let username = "alice";
    let email = "alice@example.com";

    // Act
    let user = User::new(username, email);

    // Assert
    assert_eq!(user.username, username);
    assert_eq!(user.email, email);
}
```

### Test Naming

```rust
#[test]
fn when_user_is_admin_then_can_delete_posts() {
    // ...
}

#[test]
fn given_empty_cart_when_checkout_then_returns_error() {
    // ...
}
```

### One Assertion Per Test

```rust
// Bad: Multiple unrelated assertions
#[test]
fn test_user() {
    let user = create_user();
    assert_eq!(user.name, "Alice");
    assert_eq!(user.age, 30);
    assert!(user.is_active);
}

// Good: Separate tests
#[test]
fn test_user_has_correct_name() {
    let user = create_user();
    assert_eq!(user.name, "Alice");
}

#[test]
fn test_user_has_correct_age() {
    let user = create_user();
    assert_eq!(user.age, 30);
}

#[test]
fn test_user_is_active() {
    let user = create_user();
    assert!(user.is_active);
}
```

### Avoid Test Interdependence

```rust
// Bad: Tests depend on execution order
#[test]
fn test_create() {
    DB.insert(user);
}

#[test]
fn test_read() {
    let user = DB.get(user_id); // Depends on test_create
}

// Good: Each test is independent
#[test]
fn test_create() {
    let db = setup_test_db();
    db.insert(user);
}

#[test]
fn test_read() {
    let db = setup_test_db();
    db.insert(user); // Setup its own data
    let retrieved = db.get(user.id);
    assert_eq!(retrieved, user);
}
```

### Test Helper Functions

```rust
#[cfg(test)]
mod tests {
    use super::*;

    fn create_test_user(name: &str) -> User {
        User {
            name: name.to_string(),
            email: format!("{}@test.com", name),
            age: 25,
            is_active: true,
        }
    }

    #[test]
    fn test_user_validation() {
        let user = create_test_user("alice");
        assert!(user.is_valid());
    }
}
```

## Common Testing Patterns

### Table-Driven Tests

```rust
#[test]
fn test_add() {
    let test_cases = vec![
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ];

    for (a, b, expected) in test_cases {
        assert_eq!(
            add(a, b),
            expected,
            "add({}, {}) should equal {}",
            a, b, expected
        );
    }
}
```

### Builder Pattern for Test Data

```rust
#[cfg(test)]
struct UserBuilder {
    name: String,
    age: u32,
    email: String,
}

#[cfg(test)]
impl UserBuilder {
    fn new() -> Self {
        UserBuilder {
            name: "default".to_string(),
            age: 25,
            email: "default@test.com".to_string(),
        }
    }

    fn name(mut self, name: &str) -> Self {
        self.name = name.to_string();
        self
    }

    fn age(mut self, age: u32) -> Self {
        self.age = age;
        self
    }

    fn build(self) -> User {
        User {
            name: self.name,
            age: self.age,
            email: self.email,
        }
    }
}

#[test]
fn test_adult_user() {
    let user = UserBuilder::new()
        .name("alice")
        .age(30)
        .build();

    assert!(user.is_adult());
}
```

## Testing CLI Applications

```rust
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_cli_help() {
    let mut cmd = Command::cargo_bin("my-app").unwrap();
    cmd.arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("Usage:"));
}

#[test]
fn test_cli_with_input() {
    let mut cmd = Command::cargo_bin("my-app").unwrap();
    cmd.arg("process")
        .arg("input.txt")
        .assert()
        .success()
        .stdout(predicate::str::contains("Processed"));
}
```

## Running Tests

```bash
# Run all tests
cargo test

# Run specific test
cargo test test_name

# Run tests in specific module
cargo test module_name

# Run ignored tests
cargo test -- --ignored

# Run with output
cargo test -- --nocapture

# Run tests in parallel
cargo test -- --test-threads=4

# Run single-threaded
cargo test -- --test-threads=1

# Run doc tests only
cargo test --doc

# Run integration tests only
cargo test --test integration_test
```

## Key Takeaways

1. **Write tests first or alongside code**: TDD helps design better APIs
2. **Test behavior, not implementation**: Tests should survive refactoring
3. **Keep tests simple**: If a test is complex, the code might be too
4. **Use property-based testing**: Catch edge cases you didn't think of
5. **Mock external dependencies**: Tests should be fast and deterministic
6. **Measure coverage**: Aim for high coverage but focus on critical paths
7. **Run tests in CI**: Automate testing to catch regressions early
