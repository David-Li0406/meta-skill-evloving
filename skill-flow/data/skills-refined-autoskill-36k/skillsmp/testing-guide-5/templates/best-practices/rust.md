# Rust Testing 最佳实践

Rust 语言测试框架的配置和最佳实践指南。

## 目录

- [项目配置](#项目配置)
- [测试结构](#测试结构)
- [断言最佳实践](#断言最佳实践)
- [参数化测试](#参数化测试)
- [Mock 策略](#mock-策略)
- [异步测试](#异步测试)
- [集成测试](#集成测试)
- [覆盖率配置](#覆盖率配置)

---

## 项目配置

### Cargo.toml 配置

```toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"

[dependencies]
# 项目依赖

[dev-dependencies]
# 测试框架增强
pretty_assertions = "1.4"     # 更好的断言输出
rstest = "0.18"               # 参数化测试和 fixtures
mockall = "0.12"              # Mock 框架
tokio-test = "0.4"            # 异步测试工具
test-case = "3.3"             # 简单参数化测试
proptest = "1.4"              # 属性测试
fake = "2.9"                  # 假数据生成

# 异步运行时测试支持
[dev-dependencies.tokio]
version = "1"
features = ["full", "test-util"]
```

### 目录结构

```
myproject/
├── src/
│   ├── lib.rs
│   ├── user/
│   │   ├── mod.rs
│   │   └── service.rs
│   └── main.rs
├── tests/                    # 集成测试
│   ├── common/
│   │   └── mod.rs            # 共享测试工具
│   ├── user_integration.rs
│   └── api_integration.rs
├── benches/                  # 基准测试
│   └── benchmarks.rs
└── Cargo.toml
```

---

## 测试结构

### 单元测试 (内嵌模块)

```rust
// src/user/service.rs
pub struct UserService {
    repository: Box<dyn UserRepository>,
}

impl UserService {
    pub fn new(repository: Box<dyn UserRepository>) -> Self {
        Self { repository }
    }

    pub fn create_user(&self, request: CreateUserRequest) -> Result<User, UserError> {
        if self.repository.exists_by_email(&request.email)? {
            return Err(UserError::DuplicateEmail);
        }

        let user = User {
            id: uuid::Uuid::new_v4(),
            email: request.email,
            name: request.name,
        };

        self.repository.save(&user)?;
        Ok(user)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;

    #[test]
    fn create_user_should_create_user_when_input_valid() {
        // Arrange
        let mut mock_repo = MockUserRepository::new();
        mock_repo
            .expect_exists_by_email()
            .with(eq("test@example.com"))
            .returning(|_| Ok(false));
        mock_repo
            .expect_save()
            .returning(|_| Ok(()));

        let service = UserService::new(Box::new(mock_repo));

        // Act
        let result = service.create_user(CreateUserRequest {
            email: "test@example.com".to_string(),
            name: "Test User".to_string(),
        });

        // Assert
        assert!(result.is_ok());
        let user = result.unwrap();
        assert_eq!(user.email, "test@example.com");
        assert_eq!(user.name, "Test User");
    }

    #[test]
    fn create_user_should_return_error_when_email_exists() {
        // Arrange
        let mut mock_repo = MockUserRepository::new();
        mock_repo
            .expect_exists_by_email()
            .returning(|_| Ok(true));

        let service = UserService::new(Box::new(mock_repo));

        // Act
        let result = service.create_user(CreateUserRequest {
            email: "existing@example.com".to_string(),
            name: "New User".to_string(),
        });

        // Assert
        assert!(matches!(result, Err(UserError::DuplicateEmail)));
    }
}
```

### 测试命名规范

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // ❌ 不好的命名
    #[test]
    fn test1() {}

    #[test]
    fn test_create() {}

    // ✅ 好的命名 - 方法_场景_预期结果
    #[test]
    fn create_user_when_input_valid_returns_user() {}

    #[test]
    fn create_user_when_email_exists_returns_error() {}

    // ✅ 好的命名 - should 风格
    #[test]
    fn should_create_user_when_input_is_valid() {}

    #[test]
    fn should_return_error_when_email_already_exists() {}
}
```

---

## 断言最佳实践

### 标准断言

```rust
#[test]
fn test_assertions() {
    // 相等性
    assert_eq!(expected, actual);
    assert_ne!(unexpected, actual);

    // 布尔值
    assert!(condition);
    assert!(!condition);

    // Option
    assert!(result.is_some());
    assert!(result.is_none());
    assert_eq!(result, Some(expected));

    // Result
    assert!(result.is_ok());
    assert!(result.is_err());

    // 自定义消息
    assert_eq!(expected, actual, "值不匹配: expected={}, actual={}", expected, actual);
}
```

### 使用 pretty_assertions

```rust
use pretty_assertions::{assert_eq, assert_ne};

#[test]
fn test_with_pretty_output() {
    let expected = User {
        id: 1,
        name: "Alice".to_string(),
        email: "alice@example.com".to_string(),
    };

    let actual = get_user(1);

    // 失败时会显示清晰的差异对比
    assert_eq!(expected, actual);
}
```

### 禁止弱断言

```rust
// ❌ 弱断言 - 几乎不验证任何东西
assert!(result.is_some());
assert!(result.is_ok());
assert!(!list.is_empty());

// ✅ 强断言 - 验证具体值
assert_eq!(result, Some(expected_value));
assert_eq!(result.unwrap().status, Status::Success);
assert_eq!(list.len(), 3);
assert!(list.contains(&expected_item));
```

### Result 和 Option 断言

```rust
#[test]
fn test_result_handling() {
    let result: Result<User, UserError> = service.get_user(1);

    // ✅ 解包并验证
    let user = result.expect("should return user");
    assert_eq!(user.name, "Test");

    // ✅ 验证错误类型
    let err_result: Result<User, UserError> = service.get_user(-1);
    let error = err_result.expect_err("should return error");
    assert!(matches!(error, UserError::InvalidId));
}

#[test]
fn test_option_handling() {
    let result: Option<User> = repository.find_by_id(1);

    // ✅ 解包并验证
    let user = result.expect("user should exist");
    assert_eq!(user.id, 1);

    // ✅ 验证 None
    let none_result = repository.find_by_id(999);
    assert!(none_result.is_none());
}
```

### 自定义断言宏

```rust
macro_rules! assert_user_eq {
    ($expected:expr, $actual:expr) => {
        assert_eq!($expected.id, $actual.id, "user id mismatch");
        assert_eq!($expected.email, $actual.email, "user email mismatch");
        assert_eq!($expected.name, $actual.name, "user name mismatch");
    };
}

#[test]
fn test_with_custom_assertion() {
    let expected = User { id: 1, email: "test@example.com".into(), name: "Test".into() };
    let actual = service.get_user(1).unwrap();

    assert_user_eq!(expected, actual);
}
```

---

## 参数化测试

### 使用 rstest

```rust
use rstest::rstest;

#[rstest]
#[case("", false)]
#[case(" ", false)]
#[case("invalid", false)]
#[case("test@", false)]
#[case("test@example.com", true)]
fn test_validate_email(#[case] email: &str, #[case] expected: bool) {
    assert_eq!(validate_email(email), expected);
}

#[rstest]
#[case(100, 0, 100)]
#[case(100, 10, 90)]
#[case(200, 25, 150)]
#[case(1000, 50, 500)]
fn test_apply_discount(
    #[case] price: i32,
    #[case] discount_percent: i32,
    #[case] expected: i32,
) {
    assert_eq!(apply_discount(price, discount_percent), expected);
}
```

### rstest Fixtures

```rust
use rstest::*;

#[fixture]
fn user_service() -> UserService {
    let repo = InMemoryUserRepository::new();
    UserService::new(Box::new(repo))
}

#[fixture]
fn test_user() -> User {
    User {
        id: uuid::Uuid::new_v4(),
        email: "test@example.com".to_string(),
        name: "Test User".to_string(),
    }
}

#[rstest]
fn should_create_user(user_service: UserService) {
    let result = user_service.create_user(CreateUserRequest {
        email: "new@example.com".to_string(),
        name: "New User".to_string(),
    });

    assert!(result.is_ok());
}

#[rstest]
fn should_find_user_by_id(user_service: UserService, test_user: User) {
    // 使用 fixtures
}
```

### 使用 test-case

```rust
use test_case::test_case;

#[test_case("" => false ; "empty string")]
#[test_case(" " => false ; "whitespace")]
#[test_case("test@example.com" => true ; "valid email")]
fn validate_email_returns_expected(email: &str) -> bool {
    validate_email(email)
}

#[test_case(0, 0 => 0 ; "zero plus zero")]
#[test_case(1, 1 => 2 ; "one plus one")]
#[test_case(-1, 1 => 0 ; "negative plus positive")]
fn add_returns_sum(a: i32, b: i32) -> i32 {
    add(a, b)
}
```

### 属性测试 (Property-Based Testing)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_add_is_commutative(a: i32, b: i32) {
        prop_assert_eq!(add(a, b), add(b, a));
    }

    #[test]
    fn test_reverse_twice_is_identity(s in "\\PC*") {
        let reversed_twice: String = s.chars().rev().collect::<String>().chars().rev().collect();
        prop_assert_eq!(s, reversed_twice);
    }

    #[test]
    fn test_parse_then_format_is_identity(n in 0i32..1000) {
        let formatted = n.to_string();
        let parsed: i32 = formatted.parse().unwrap();
        prop_assert_eq!(n, parsed);
    }
}
```

---

## Mock 策略

### 使用 mockall

```rust
use mockall::{automock, predicate::*};

#[automock]
pub trait UserRepository {
    fn save(&self, user: &User) -> Result<(), RepositoryError>;
    fn find_by_id(&self, id: i32) -> Result<Option<User>, RepositoryError>;
    fn exists_by_email(&self, email: &str) -> Result<bool, RepositoryError>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_with_mock() {
        let mut mock = MockUserRepository::new();

        // 设置期望
        mock.expect_exists_by_email()
            .with(eq("test@example.com"))
            .times(1)
            .returning(|_| Ok(false));

        mock.expect_save()
            .withf(|user| user.email == "test@example.com")
            .times(1)
            .returning(|_| Ok(()));

        let service = UserService::new(Box::new(mock));
        let result = service.create_user(CreateUserRequest {
            email: "test@example.com".to_string(),
            name: "Test".to_string(),
        });

        assert!(result.is_ok());
    }
}
```

### Mock 序列调用

```rust
#[test]
fn test_retry_on_failure() {
    let mut mock = MockExternalService::new();

    // 按顺序返回不同结果
    let mut seq = mockall::Sequence::new();

    mock.expect_call()
        .times(1)
        .in_sequence(&mut seq)
        .returning(|| Err(ServiceError::Timeout));

    mock.expect_call()
        .times(1)
        .in_sequence(&mut seq)
        .returning(|| Err(ServiceError::Timeout));

    mock.expect_call()
        .times(1)
        .in_sequence(&mut seq)
        .returning(|| Ok(Response::new()));

    let client = RetryClient::new(Box::new(mock));
    let result = client.call_with_retry(3);

    assert!(result.is_ok());
}
```

### 参数捕获

```rust
#[test]
fn test_capture_arguments() {
    use std::sync::{Arc, Mutex};

    let captured = Arc::new(Mutex::new(Vec::new()));
    let captured_clone = captured.clone();

    let mut mock = MockNotificationService::new();
    mock.expect_send_email()
        .returning(move |email, message| {
            captured_clone.lock().unwrap().push((email.to_string(), message.to_string()));
            Ok(())
        });

    let service = UserService::new(Box::new(mock));
    service.register_user(CreateUserRequest {
        email: "test@example.com".to_string(),
        name: "Test".to_string(),
    }).unwrap();

    let captured = captured.lock().unwrap();
    assert_eq!(captured.len(), 1);
    assert_eq!(captured[0].0, "test@example.com");
    assert!(captured[0].1.contains("Welcome"));
}
```

---

## 异步测试

### tokio 异步测试

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tokio;

    #[tokio::test]
    async fn test_async_function() {
        let result = async_get_user(1).await;
        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_async_with_timeout() {
        let result = tokio::time::timeout(
            std::time::Duration::from_secs(5),
            slow_operation()
        ).await;

        assert!(result.is_ok());
    }
}
```

### 异步 Mock

```rust
use mockall::automock;
use async_trait::async_trait;

#[async_trait]
#[automock]
pub trait AsyncUserRepository {
    async fn find_by_id(&self, id: i32) -> Result<Option<User>, Error>;
    async fn save(&self, user: &User) -> Result<(), Error>;
}

#[tokio::test]
async fn test_async_service() {
    let mut mock = MockAsyncUserRepository::new();

    mock.expect_find_by_id()
        .with(eq(1))
        .returning(|_| Box::pin(async { Ok(Some(User::default())) }));

    let service = AsyncUserService::new(Box::new(mock));
    let result = service.get_user(1).await;

    assert!(result.is_ok());
}
```

### 测试并发代码

```rust
#[tokio::test]
async fn test_concurrent_access() {
    use std::sync::Arc;
    use tokio::sync::Mutex;

    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..100 {
        let counter = counter.clone();
        handles.push(tokio::spawn(async move {
            let mut count = counter.lock().await;
            *count += 1;
        }));
    }

    for handle in handles {
        handle.await.unwrap();
    }

    let final_count = *counter.lock().await;
    assert_eq!(final_count, 100);
}
```

---

## 集成测试

### 集成测试结构

```rust
// tests/common/mod.rs
use myproject::{UserService, InMemoryRepository};

pub fn setup_service() -> UserService {
    let repo = InMemoryRepository::new();
    UserService::new(Box::new(repo))
}

pub fn create_test_user() -> myproject::User {
    myproject::User {
        id: uuid::Uuid::new_v4(),
        email: "test@example.com".to_string(),
        name: "Test User".to_string(),
    }
}
```

```rust
// tests/user_integration.rs
mod common;

use myproject::{CreateUserRequest, UserError};

#[test]
fn test_user_creation_flow() {
    let service = common::setup_service();

    // 创建用户
    let result = service.create_user(CreateUserRequest {
        email: "new@example.com".to_string(),
        name: "New User".to_string(),
    });

    assert!(result.is_ok());
    let user = result.unwrap();

    // 验证可以查询到
    let found = service.get_user(user.id);
    assert!(found.is_ok());
    assert_eq!(found.unwrap().email, "new@example.com");
}

#[test]
fn test_duplicate_email_prevention() {
    let service = common::setup_service();

    // 创建第一个用户
    service.create_user(CreateUserRequest {
        email: "duplicate@example.com".to_string(),
        name: "First".to_string(),
    }).unwrap();

    // 尝试创建相同邮箱的用户
    let result = service.create_user(CreateUserRequest {
        email: "duplicate@example.com".to_string(),
        name: "Second".to_string(),
    });

    assert!(matches!(result, Err(UserError::DuplicateEmail)));
}
```

---

## 覆盖率配置

### 使用 cargo-tarpaulin

```bash
# 安装
cargo install cargo-tarpaulin

# 运行覆盖率
cargo tarpaulin

# 生成 HTML 报告
cargo tarpaulin --out Html

# 设置覆盖率门禁
cargo tarpaulin --fail-under 80

# 排除文件
cargo tarpaulin --exclude-files "src/generated/*"
```

### 使用 cargo-llvm-cov

```bash
# 安装
cargo install cargo-llvm-cov

# 运行覆盖率
cargo llvm-cov

# 生成 HTML 报告
cargo llvm-cov --html

# 生成 lcov 格式
cargo llvm-cov --lcov --output-path lcov.info
```

### CI 配置

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable

      - name: Run tests
        run: cargo test --all-features

      - name: Install tarpaulin
        run: cargo install cargo-tarpaulin

      - name: Generate coverage
        run: cargo tarpaulin --out Xml --fail-under 80

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: cobertura.xml
```

---

## 常用命令

```bash
# 运行所有测试
cargo test

# 运行特定测试
cargo test test_name

# 运行特定模块的测试
cargo test module_name::

# 运行集成测试
cargo test --test integration_test_name

# 显示输出
cargo test -- --nocapture

# 运行被忽略的测试
cargo test -- --ignored

# 并行度控制
cargo test -- --test-threads=1

# 运行文档测试
cargo test --doc

# 运行基准测试
cargo bench

# 覆盖率
cargo tarpaulin
cargo llvm-cov
```

---

## 参考资源

- [Rust Book - Writing Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [rstest Documentation](https://docs.rs/rstest/)
- [mockall Documentation](https://docs.rs/mockall/)
- [proptest Documentation](https://proptest-rs.github.io/proptest/intro.html)
- [cargo-tarpaulin](https://github.com/xd009642/tarpaulin)
