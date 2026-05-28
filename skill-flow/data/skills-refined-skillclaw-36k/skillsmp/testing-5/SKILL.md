---
name: testing
description: Test creation and mocking (mockall, unit tests, integration tests, cargo test, AAA pattern). Use when writing tests, creating mocks, running cargo test, debugging test failures, asking about testing strategies, mockall usage, or test coverage.
---

# Testing Guide

## Tech Stack

- **Test Framework**: Standard `#[test]` / `#[tokio::test]`
- **Mocking**: mockall
- **Async Testing**: tokio-test

## Test Structure

### Unit Tests

Place in modules with `#[cfg(test)]`

```rust
// src/services/user_service.rs
pub struct UserService {
    repository: Arc<dyn UserRepository>,
}

impl UserService {
    pub async fn create(&self, data: UserData) -> Result<User> {
        // Implementation
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_create_user_success() {
        // Test code
    }
}
```

### Integration Tests

Place in `tests/` directory

```rust
// tests/integration_test.rs
use my_app::prelude::*;

#[tokio::test]
async fn test_full_workflow() {
    // Integration test code
}
```

## AAA Pattern

**Arrange-Act-Assert** pattern recommended

```rust
#[tokio::test]
async fn test_create_user_success() {
    // Arrange: Setup
    let mut mock_repository = MockUserRepository::new();
    mock_repository
        .expect_create_with_txn()
        .returning(|_, data| Ok(User {
            id: 1,
            name: data.name,
            email: data.email,
        }));

    let service = UserService::new(Arc::new(mock_repository));
    let user_data = UserData {
        name: "太郎".to_string(),
        email: "taro@example.com".to_string(),
    };

    // Act: Execute
    let result = service.create(user_data).await;

    // Assert: Verify
    assert!(result.is_ok());
    let user = result.unwrap();
    assert_eq!(user.name, "太郎");
    assert_eq!(user.email, "taro@example.com");
}
```

## Mocking (mockall)

### Trait Definition

```rust
use mockall::automock;

#[automock]
pub trait UserRepository: Send + Sync {
    async fn create_with_txn(
        &self,
        txn: &DatabaseTransaction,
        data: UserData,
    ) -> Result<User, RepositoryError>;

    async fn find_by_id(
        &self,
        txn: &DatabaseTransaction,
        id: i32,
    ) -> Result<Option<User>, RepositoryError>;
}
```

### Using Mocks

```rust
#[tokio::test]
async fn test_with_mock() {
    // Create mock
    let mut mock_repo = MockUserRepository::new();

    // Set expectations
    mock_repo
        .expect_create_with_txn()
        .times(1)  // Called once
        .with(eq(txn), eq(user_data))  // Argument verification
        .returning(|_, data| Ok(User {
            id: 1,
            name: data.name,
            email: data.email,
        }));

    // Run test
    let service = UserService::new(Arc::new(mock_repo));
    let result = service.create(user_data).await;

    assert!(result.is_ok());
}
```

### Multiple Call Mocks

```rust
#[tokio::test]
async fn test_multiple_calls() {
    let mut mock_repo = MockUserRepository::new();

    // Set multiple expectations
    mock_repo
        .expect_find_by_id()
        .times(2)
        .returning(|_, id| {
            if id == 1 {
                Ok(Some(User { id: 1, name: "太郎".to_string() }))
            } else {
                Ok(None)
            }
        });

    let service = UserService::new(Arc::new(mock_repo));

    let user1 = service.find_by_id(1).await.unwrap();
    assert!(user1.is_some());

    let user2 = service.find_by_id(2).await.unwrap();
    assert!(user2.is_none());
}
```

### Error Case Mocks

```rust
#[tokio::test]
async fn test_error_case() {
    let mut mock_repo = MockUserRepository::new();

    // Mock returning error
    mock_repo
        .expect_create_with_txn()
        .returning(|_, _| Err(RepositoryError::DatabaseError("接続エラー".to_string())));

    let service = UserService::new(Arc::new(mock_repo));
    let result = service.create(user_data).await;

    assert!(result.is_err());
    match result.unwrap_err() {
        ServiceError::RepositoryError(_) => (),
        _ => panic!("Unexpected error type"),
    }
}
```

## Running Tests

### Commands

```bash
# Run all tests
cargo test

# Run specific test
cargo test test_create_user

# Show output
cargo test -- --nocapture

# Disable parallel execution
cargo test -- --test-threads=1

# Run integration tests only
cargo test --test integration_test
```

### Debug

```rust
#[tokio::test]
async fn test_with_logging() {
    // Enable logging in test
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::DEBUG)
        .init();

    // Test code
    let result = service.create(data).await;

    // Debug output
    println!("Result: {:?}", result);

    assert!(result.is_ok());
}
```

## Test Patterns

### Success Case

```rust
#[tokio::test]
async fn test_success_case() {
    // Arrange
    let mock = setup_mock_success();

    // Act
    let result = function_under_test(mock).await;

    // Assert
    assert!(result.is_ok());
}
```

### Failure Case

```rust
#[tokio::test]
async fn test_failure_case() {
    // Arrange
    let mock = setup_mock_failure();

    // Act
    let result = function_under_test(mock).await;

    // Assert
    assert!(result.is_err());
}
```

### Boundary Value Testing

```rust
#[tokio::test]
async fn test_boundary_values() {
    // Empty string
    assert!(validate("").is_err());

    // Minimum length
    assert!(validate("a").is_ok());

    // Maximum length
    assert!(validate(&"a".repeat(255)).is_ok());

    // Maximum length + 1
    assert!(validate(&"a".repeat(256)).is_err());
}
```

### Parameterized Tests

```rust
#[tokio::test]
async fn test_validation() {
    let test_cases = vec![
        ("", false),
        ("a", true),
        ("valid@example.com", true),
        ("invalid", false),
    ];

    for (input, expected) in test_cases {
        let result = validate_email(input);
        assert_eq!(result.is_ok(), expected, "Failed for input: {}", input);
    }
}
```

## Best Practices

### Test Names

```rust
// ✅ Good: Clear what is tested
#[tokio::test]
async fn test_create_user_with_valid_data_returns_user() { }

#[tokio::test]
async fn test_create_user_with_duplicate_email_returns_error() { }

// ❌ Bad: Vague
#[tokio::test]
async fn test1() { }

#[tokio::test]
async fn test_user() { }
```

### Test Independence

```rust
// ✅ Create independent mocks per test
#[tokio::test]
async fn test_a() {
    let mock = MockRepo::new();
    // Test A
}

#[tokio::test]
async fn test_b() {
    let mock = MockRepo::new();
    // Test B (independent from test_a)
}
```

### Assertion Messages

```rust
// ✅ Provide details on failure
assert_eq!(
    result.len(),
    expected_len,
    "User count mismatch. Expected: {}, Actual: {}",
    expected_len,
    result.len()
);
```

## Common Patterns

### Setup Helpers

```rust
#[cfg(test)]
mod tests {
    use super::*;

    fn setup_mock_repository() -> MockUserRepository {
        let mut mock = MockUserRepository::new();
        mock.expect_create_with_txn()
            .returning(|_, data| Ok(create_test_user(data)));
        mock
    }

    fn create_test_user(data: UserData) -> User {
        User {
            id: 1,
            name: data.name,
            email: data.email,
            created_at: Utc::now(),
        }
    }

    #[tokio::test]
    async fn test_example() {
        let mock = setup_mock_repository();
        // Test code
    }
}
```

### Async Tests

```rust
#[tokio::test]
async fn test_async_function() {
    let result = async_function().await;
    assert!(result.is_ok());
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_concurrent_operations() {
    // Concurrent test
}
```
