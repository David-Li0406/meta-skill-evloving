---
name: tauri-development
description: Use this skill when creating or modifying Tauri commands, integrating Rust backend with frontend, or addressing Tauri-specific issues in desktop application development.
---

# Tauri Development Skill

## Overview
This skill provides comprehensive guidance for:
- Creating and modifying Tauri commands with proper specta type binding.
- Integrating Rust backend with React TypeScript frontend.
- Handling desktop-specific patterns and constraints.
- Optimizing frontend-backend communication.
- Following Tauri 2.0 best practices.

## Applicable Scenarios
- Adding or modifying Tauri commands or State service accessors.
- Debugging frontend-backend communication issues.
- Implementing desktop-specific features.
- Optimizing Tauri application performance.
- Handling Tauri-specific error cases.

## Core Tauri Principles

### Command Definition Pattern
All Tauri commands must follow this pattern:

```rust
use serde::{Deserialize, Serialize};
use specta::Type;

#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct MyDto {
    pub field: String,
}

#[tauri::command]
#[specta::specta]
pub async fn my_command(
    dto: MyDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<ResultType> {
    // Implementation
}
```

**Key Requirements:**
- Each command must include both `#[tauri::command]` and `#[specta::specta]`.
- Parameter and return types must implement `specta::Type`, with `#[specta(inline)]` as necessary.
- Use a unified return type `Result<ApiResponse<T>, String>` for error handling.
- Frontend should only use `commands` from `frontend/src/bindings.ts`, avoiding direct `invoke`.
- Database access should prioritize `sqlx::query_as!` with explicit column names, using transactions for write operations.

### Frontend Command Usage
**✓ Correct:**
```typescript
import { commands } from '../bindings';

const result = await commands.myCommand({ field: "value" });
if (!result.success) {
    message.error(result.message);
    return;
}
const data = result.data;
```

**✗ Incorrect:**
```typescript
// ✗ Don't use raw invoke
import { invoke } from '@tauri-apps/api/core';
const result = await invoke('my_command', { dto });
```

## Common Patterns

### State Management
Use dependency injection for services:

```rust
pub struct TauriAppState {
    pub db: Arc<SqlitePool>,
    pub material_service: Arc<MaterialService>,
}

pub async fn get_state() -> TauriAppState {
    TauriAppState {
        db: Arc::new(pool),
        material_service: Arc::new(MaterialService::new(pool)),
    }
}
```

### Error Handling
Always use `ApiResponse` for top-level commands:

```rust
use crate::utils::error::{api_err, api_ok, ApiResponse};

#[tauri::command]
#[specta::specta]
pub async fn some_command() -> ApiResponse<Data> {
    match inner_logic().await {
        Ok(data) => api_ok(data),
        Err(e) => api_err(format!("操作失败: {}", e)),
    }
}
```

### Async/Await Best Practices
- Use `async` for external-facing commands.
- Use sync functions for pure computations.
- Never block the async runtime with `std::thread::sleep`.
- Use `tokio::time::sleep` instead.

## Tauri-Specific Considerations

### Desktop Application Constraints
1. **No console.log** - Use Ant Design message components.
2. **File paths** - Use `path.resolve` for cross-platform compatibility.
3. **Native dialogs** - Use Tauri APIs for file dialogs.
4. **System integration** - Leverage native OS features.

### Performance Optimization
- Use `moka::future::Cache` for frequently accessed data.
- Implement proper connection pooling for SQLite.
- Use `rayon` for CPU-intensive parallel computations.
- Minimize bridge calls between frontend and backend.

### Security Considerations
- Validate all user input on both frontend and backend.
- Use SQL parameter binding (never string concatenation).
- Sanitize file paths to prevent directory traversal.
- Implement proper error handling without exposing sensitive info.

## Quick Reference

### Essential Tauri Command Template

```rust
#[tauri::command]
#[specta::specta]
pub async fn command_name(
    dto: RequestDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<ResponseData> {
    with_service(state, |ctx| async move {
        ctx.service.do_work(dto).await
    })
    .await
}
```

### Required Attributes Checklist

- [ ] `#[tauri::command]` on all commands.
- [ ] `#[specta::specta]` on all commands.
- [ ] `#[specta(inline)]` on all DTOs.
- [ ] Return type `ApiResponse<T>`.
- [ ] Use `commands` from bindings (not `invoke`).
- [ ] Handle errors with message component.
- [ ] No console.log in desktop app.

## Additional Resources

### Official Documentation
- [Tauri 2.0 Documentation](https://tauri.app/v1/guids/)
- [specta Documentation](https://specta.quatri.dev/)