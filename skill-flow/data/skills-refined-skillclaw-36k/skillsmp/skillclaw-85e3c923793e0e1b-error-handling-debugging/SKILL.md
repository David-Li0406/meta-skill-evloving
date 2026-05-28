---
name: error-handling-debugging
description: Use this skill when you need to implement error handling, exception chaining, user error messages, or debugging techniques in your applications.
---

# Skill body

## Scope
- Rust error chaining and context
- Tauri command error conversion
- Frontend user error messaging and recovery

## Critical Rules
- Use `anyhow::Context` in Rust to supplement error information.
- Tauri commands should consistently return `ApiResponse<T>`.
- Frontend errors must prompt users with `message.error`.

## Rust Error Chaining Example
```rust
use anyhow::{Context, Result};
use std::path::Path;

pub fn load_config(path: &Path) -> Result<String> {
    std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read configuration: {}", path.display()))
}
```

## Tauri Command Error Conversion
```rust
#[tauri::command]
#[specta::specta]
pub async fn get_settings() -> Result<ApiResponse<SettingsData>, String> {
    match get_settings_data_service().await {
        Ok(settings_data) => Ok(ApiResponse::success(settings_data)),
        Err(e) => Ok(ApiResponse::error(format!("Failed to retrieve settings data: {}", e))),
    }
}
```

## Frontend Error Messaging
```ts
import { message } from 'antd';

export function showError(text: string) {
  message.error(text);
}
```

## Checklist
- [ ] Rust errors include context
- [ ] Tauri commands return `ApiResponse`
- [ ] Frontend uses `message.error` for user prompts