---
name: api-response-checker
description: Check that API response format matches Android/iOS model expectations. Use when fixing JSON parsing errors, serialization issues, or when API returns unexpected format. Checks for array vs object wrappers, required fields, snake_case vs camelCase mismatches.
allowed-tools: Read, Grep, Glob
---

# API Response Checker

## Purpose
Verify that Next.js API routes return data in a format that Android (Kotlin/kotlinx.serialization) and iOS (Swift/Codable) can parse correctly.

## Common Issues This Skill Catches

### 1. Array vs Object Wrapper Mismatch
**Error**: `Expected start of object '{', but had '[' instead`

Android models often expect wrapped responses:
```kotlin
// Android expects:
data class UsersResponse(
    val users: List<User>,
    val total: Int,
    val page: Int
)
```

But API returns raw array:
```typescript
// BAD: Returns raw array
return NextResponse.json(users)

// GOOD: Returns wrapped object
return NextResponse.json({ users, total, page, pageSize })
```

### 2. Required Fields Missing
**Error**: `Fields [status, createdAt] are required but missing`

Android model has required fields without defaults:
```kotlin
data class Report(
    val id: String,
    val status: String,  // Required - no default
    val createdAt: String  // Required - no default
)
```

API must include these fields in response.

### 3. snake_case vs camelCase
Android uses `@SerialName` for snake_case mapping:
```kotlin
@SerialName("user_id") val userId: String
@SerialName("created_at") val createdAt: String
```

API should return camelCase (Retrofit handles it) OR snake_case if model expects it.

### 4. Nested Objects Causing Issues
**Error**: Parsing fails on `_count` or nested relations

Prisma returns nested `_count`:
```json
{ "_count": { "items": 5 } }
```

Android may not have matching model. Flatten in API:
```typescript
return {
    itemCount: record._count.items
}
```

## Checking Process

1. **Find the Android/iOS model** for the endpoint
2. **Note required fields** (no default values)
3. **Check API response** format matches model
4. **Verify wrapper objects** (Response suffix classes)
5. **Check field names** match or have @SerialName

## Quick Reference: Android Model Patterns

```kotlin
// List endpoints need wrapped response
data class XxxResponse(
    val items: List<Xxx>,  // or 'users', 'projects', etc.
    val total: Int = 0,
    val page: Int = 1,
    val pageSize: Int = 20
)

// Single item endpoints return item directly or wrapped
data class XxxDetailResponse(
    val item: Xxx
)

// Fields with defaults are optional
data class Xxx(
    val id: String,           // Required
    val name: String,         // Required
    val status: String = "ACTIVE",  // Optional - has default
    val notes: String? = null       // Optional - nullable
)
```

## Fix Patterns

### Wrap Array Response
```typescript
// Before
return NextResponse.json(items)

// After
return NextResponse.json({
    items: items,
    total: items.length,
    page: 1,
    pageSize: items.length
})
```

### Add Missing Required Fields
```typescript
// Before
return NextResponse.json({
    id: report.id,
    name: report.name
})

// After - add required fields
return NextResponse.json({
    id: report.id,
    name: report.name,
    status: 'READY',
    createdAt: new Date().toISOString()
})
```

### Flatten Nested Objects
```typescript
// Before - nested _count
return NextResponse.json(record)

// After - flattened
return NextResponse.json({
    ...record,
    itemCount: record._count?.items ?? 0,
    _count: undefined  // Remove nested
})
```
