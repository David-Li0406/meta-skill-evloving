---
id: rust-tokio-async
name: "Tokio Async Patterns"
domain: RUST
skill: faion-software-developer
category: "backend"
---

## Tokio Async Patterns

### Problem
Handle concurrent operations efficiently.

### Framework: Async Service

```rust
// src/services/users.rs

use crate::{
    db::Database,
    error::AppError,
    models::User,
};
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHasher, SaltString},
    Argon2,
};

pub struct UserService<'a> {
    db: &'a Database,
}

impl<'a> UserService<'a> {
    pub fn new(db: &'a Database) -> Self {
        Self { db }
    }

    pub async fn list(&self, page: u32, per_page: u32) -> Result<(Vec<User>, i64), AppError> {
        let offset = ((page - 1) * per_page) as i64;

        // Run count and fetch in parallel
        let (users, total) = tokio::try_join!(
            self.db.fetch_users(per_page as i64, offset),
            self.db.count_users()
        )?;

        Ok((users, total))
    }

    pub async fn get_by_id(&self, id: i32) -> Result<User, AppError> {
        self.db
            .fetch_user_by_id(id)
            .await?
            .ok_or(AppError::NotFound("User not found".into()))
    }

    pub async fn create(
        &self,
        name: &str,
        email: &str,
        password: &str,
    ) -> Result<User, AppError> {
        // Check if email already exists
        if self.db.fetch_user_by_email(email).await?.is_some() {
            return Err(AppError::Conflict("Email already exists".into()));
        }

        // Hash password (CPU-intensive, use spawn_blocking)
        let password_hash = tokio::task::spawn_blocking({
            let password = password.to_string();
            move || {
                let salt = SaltString::generate(&mut OsRng);
                Argon2::default()
                    .hash_password(password.as_bytes(), &salt)
                    .map(|h| h.to_string())
            }
        })
        .await??;

        self.db.insert_user(name, email, &password_hash).await
    }

    pub async fn update(&self, id: i32, name: Option<&str>) -> Result<User, AppError> {
        let user = self.get_by_id(id).await?;

        let new_name = name.unwrap_or(&user.name);
        self.db.update_user(id, new_name).await
    }

    pub async fn delete(&self, id: i32) -> Result<(), AppError> {
        let deleted = self.db.delete_user(id).await?;
        if !deleted {
            return Err(AppError::NotFound("User not found".into()));
        }
        Ok(())
    }
}
```

### Concurrent Processing

```rust
// src/services/batch.rs

use futures::stream::{self, StreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;

pub struct BatchProcessor {
    concurrency: usize,
}

impl BatchProcessor {
    pub fn new(concurrency: usize) -> Self {
        Self { concurrency }
    }

    pub async fn process_items<T, F, Fut, R, E>(
        &self,
        items: Vec<T>,
        processor: F,
    ) -> Vec<Result<R, E>>
    where
        T: Send + 'static,
        F: Fn(T) -> Fut + Send + Sync + 'static,
        Fut: std::future::Future<Output = Result<R, E>> + Send,
        R: Send + 'static,
        E: Send + 'static,
    {
        let semaphore = Arc::new(Semaphore::new(self.concurrency));
        let processor = Arc::new(processor);

        stream::iter(items)
            .map(|item| {
                let semaphore = semaphore.clone();
                let processor = processor.clone();

                async move {
                    let _permit = semaphore.acquire().await.unwrap();
                    processor(item).await
                }
            })
            .buffer_unordered(self.concurrency)
            .collect()
            .await
    }
}

// Usage
let processor = BatchProcessor::new(10);
let results = processor.process_items(
    user_ids,
    |id| async move { fetch_user(id).await }
).await;
```

### Agent

faion-backend-agent
