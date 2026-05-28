---
name: api-design
description: Use this skill when designing or adjusting API interfaces, DTOs, request/response structures, naming conventions, or validation rules.
---

# Skill body

## Scope
- Design or adjust Tauri command interfaces.
- Design DTOs and response structures.
- Standardize naming and validation strategies.

## Critical Rules
- Use a unified outer response structure: `ApiResponse<T>`.
- DTOs should utilize `serde` and `specta::Type`, with fields in camelCase to match the frontend.
- Perform validation at the command boundary, returning `anyhow::Result` with additional context from the business layer.
- Error messages should be user-friendly, concise, and clear.

## Standard Response
```rust
#[derive(serde::Serialize, specta::Type)]
#[specta(inline)]
pub struct ApiResponse<T: specta::Type> {
    pub success: bool,
    pub data: Option<T>,
    pub error: Option<String>,
}
```

## DTO Specification (Example)
```rust
#[derive(Debug, Clone, Serialize, Deserialize, specta::Type)]
#[serde(rename_all = "camelCase")]
pub struct CreateFactoryDto {
    pub factory_code: Code,
    pub factory_name: Name,
    pub description: Description,
    pub address: Option<String>,
    pub contact: Option<String>,
    pub phone: Option<String>,
    pub is_active: Boolean,
}
```

## Naming and Contracts
- Commands should follow the pattern: verb + noun (e.g., `get`, `create`, `update`, `delete`).
- DTOs should be named as `CreateXDto`, `UpdateXDto`, or `XDto`.
- Ensure consistency in camelCase for fields between frontend and backend, using `#[serde(rename_all = "camelCase")]` in Rust.

## Pagination and Lists
- Prefer reusing existing types: `crate::material::material_service::MaterialsPage` / `MaterialsPaginatedResult`.
- When returning lists, ensure fields are directly renderable to avoid additional assembly.

## Validation Recommendations
- Check the length of `String` fields and ensure required `Option` fields are validated.
- Perform basic validation before SQLx to prevent exposing database errors directly.

## Checklist
- [ ] Response uses `ApiResponse<T>`.
- [ ] DTO implements `specta::Type` and fields are in camelCase.
- [ ] Validation is completed at the command boundary.
- [ ] Naming is consistent with existing command styles.