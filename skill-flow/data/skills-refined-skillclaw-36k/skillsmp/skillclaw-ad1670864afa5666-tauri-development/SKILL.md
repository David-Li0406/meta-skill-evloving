---
name: tauri-development
description: Use this skill when creating or modifying Tauri commands, integrating Rust backend with a TypeScript frontend, or addressing Tauri-specific development challenges.
---

# Tauri Development Skill

## Overview

This skill provides comprehensive guidance for:
- Creating and modifying Tauri commands with proper specta type binding.
- Integrating Rust backend with a TypeScript frontend.
- Handling desktop-specific patterns and constraints.
- Optimizing frontend-backend communication.
- Following Tauri best practices.

## When This Skill Applies

This skill activates when:
- Creating or modifying Tauri commands.
- Setting up specta type bindings.
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
- Each command must include `#[tauri::command]` and `#[specta::specta]`.
- Input and output types must implement `specta::Type`, using `#[specta(inline)]` where necessary.
- Use a unified return type `ApiResponse<T>` for error handling.

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
        db: Arc::new(SqlitePool::connect("sqlite://db.sqlite").await?),
        material_service: Arc::new(MaterialService::new()),
    }
}
```

## Workflow
1. Design command signatures and DTOs (ensure Rust/TS fields match).
2. Implement commands and return `ApiResponse`.
3. Update `frontend/src/bindings.ts` according to project processes.
4. Ensure frontend integrates with `commands` and provides error feedback.

## Checklist
- [ ] Commands include `#[tauri::command]` and `#[specta::specta]`.
- [ ] Input/output types implement `specta::Type`.
- [ ] Use unified `ApiResponse` for error messages.
- [ ] Frontend only uses `commands`.