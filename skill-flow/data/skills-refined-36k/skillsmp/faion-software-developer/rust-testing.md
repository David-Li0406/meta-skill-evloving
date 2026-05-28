---
id: rust-testing
name: "Testing Patterns"
domain: RUST
skill: faion-software-developer
category: "backend"
---

## Testing Patterns

### Problem
Write comprehensive tests for Rust applications.

### Framework: Unit Tests

```rust
// src/services/users.rs

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;
    use mockall::mock;

    mock! {
        Database {}

        impl Database {
            async fn fetch_user_by_id(&self, id: i32) -> Result<Option<User>, sqlx::Error>;
            async fn fetch_user_by_email(&self, email: &str) -> Result<Option<User>, sqlx::Error>;
            async fn insert_user(&self, name: &str, email: &str, password_hash: &str) -> Result<User, sqlx::Error>;
        }
    }

    fn create_test_user() -> User {
        User {
            id: 1,
            name: "John Doe".into(),
            email: "john@example.com".into(),
            password_hash: "hash".into(),
            created_at: chrono::Utc::now(),
            updated_at: chrono::Utc::now(),
        }
    }

    #[tokio::test]
    async fn test_get_by_id_returns_user() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_id()
            .with(eq(1))
            .times(1)
            .returning(|_| Ok(Some(create_test_user())));

        let service = UserService::new(&mock_db);
        let result = service.get_by_id(1).await;

        assert!(result.is_ok());
        assert_eq!(result.unwrap().name, "John Doe");
    }

    #[tokio::test]
    async fn test_get_by_id_not_found() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_id()
            .with(eq(999))
            .times(1)
            .returning(|_| Ok(None));

        let service = UserService::new(&mock_db);
        let result = service.get_by_id(999).await;

        assert!(matches!(result, Err(AppError::NotFound(_))));
    }

    #[tokio::test]
    async fn test_create_rejects_duplicate_email() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_email()
            .with(eq("john@example.com"))
            .times(1)
            .returning(|_| Ok(Some(create_test_user())));

        let service = UserService::new(&mock_db);
        let result = service.create("John", "john@example.com", "password").await;

        assert!(matches!(result, Err(AppError::Conflict(_))));
    }
}
```

### Integration Tests

```rust
// tests/api_tests.rs

use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::ServiceExt;
use serde_json::json;

async fn setup_app() -> Router {
    // Create test database, run migrations, return app
    todo!()
}

#[tokio::test]
async fn test_create_user() {
    let app = setup_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/v1/users")
                .header("Content-Type", "application/json")
                .body(Body::from(
                    json!({
                        "name": "John Doe",
                        "email": "john@example.com",
                        "password": "password123"
                    })
                    .to_string(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::CREATED);

    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let user: serde_json::Value = serde_json::from_slice(&body).unwrap();

    assert_eq!(user["name"], "John Doe");
    assert_eq!(user["email"], "john@example.com");
}

#[tokio::test]
async fn test_list_users_pagination() {
    let app = setup_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method("GET")
                .uri("/api/v1/users?page=1&per_page=10")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);

    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let result: serde_json::Value = serde_json::from_slice(&body).unwrap();

    assert!(result["data"].is_array());
    assert_eq!(result["page"], 1);
    assert_eq!(result["per_page"], 10);
}
```

### Agent

faion-backend-agent
