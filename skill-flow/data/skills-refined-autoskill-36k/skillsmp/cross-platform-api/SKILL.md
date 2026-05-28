---
name: cross-platform-api
description: Verify API endpoints work across Web, Android, and iOS. Check endpoint parity, request/response format consistency, and field name alignment. Use when adding new API endpoints, fixing cross-platform bugs, or auditing API consistency.
allowed-tools: Read, Grep, Glob
---

# Cross-Platform API Consistency

## Purpose
Ensure all three platforms (Next.js Web, Android, iOS) implement API endpoints consistently with matching request/response formats.

## Platform Locations

| Platform | API Definitions |
|----------|----------------|
| **Web (Backend)** | `apps/web/src/app/api/**/*.ts` |
| **Android** | `apps/android/**/data/ApiService.kt` |
| **Android Models** | `apps/android/**/data/model/*.kt` |
| **iOS** | `apps/ios/**/Services/*.swift` |
| **iOS Models** | `apps/ios/**/Models/*.swift` |

## Checking New Endpoint

When a new API endpoint is added, verify:

### 1. Endpoint Exists in All Platforms

**Web Route**: `apps/web/src/app/api/[resource]/route.ts`
```typescript
// GET /api/jobs
export async function GET(request: NextRequest) { ... }

// POST /api/jobs
export async function POST(request: NextRequest) { ... }
```

**Android ApiService**:
```kotlin
@GET("jobs")
suspend fun getJobs(): JobsResponse

@POST("jobs")
suspend fun createJob(@Body request: CreateJobRequest): Job
```

**iOS NetworkService**:
```swift
func getJobs() async throws -> JobsResponse
func createJob(_ request: CreateJobRequest) async throws -> Job
```

### 2. Request Body Fields Match

**Web accepts**:
```typescript
const { name, projectId, dueDate } = body
```

**Android sends**:
```kotlin
data class CreateJobRequest(
    val name: String,
    val projectId: String,
    val dueDate: String?
)
```

**iOS sends**:
```swift
struct CreateJobRequest: Encodable {
    let name: String
    let projectId: String
    let dueDate: String?
}
```

### 3. Response Format Matches Models

**Web returns**:
```typescript
return NextResponse.json({
    jobs: transformedJobs,
    total: count,
    page: 1,
    pageSize: 20
})
```

**Android expects**:
```kotlin
data class JobsResponse(
    val jobs: List<Job>,
    val total: Int,
    val page: Int,
    val pageSize: Int
)
```

## Common Mismatches to Check

### Array vs Object Wrapper
```typescript
// WRONG - Android/iOS expect wrapped object
return NextResponse.json(items)

// RIGHT
return NextResponse.json({ items, total, page, pageSize })
```

### Field Name Conventions
Web API should use **camelCase** for Android compatibility:
```typescript
// RIGHT: camelCase
{ userId, projectId, createdAt }

// WRONG: snake_case (unless Android uses @SerialName)
{ user_id, project_id, created_at }
```

### Optional vs Required Fields
If Android model has required field (no default):
```kotlin
data class Report(
    val status: String,  // REQUIRED - no default
)
```

API must always return it:
```typescript
return { ...report, status: 'READY' }
```

### Nested Object Flattening
Prisma returns nested `_count`, but mobile may not support:
```typescript
// Raw Prisma
{ _count: { items: 5 } }

// Flattened for mobile
{ itemCount: 5 }
```

## Quick Audit Commands

### Find all Android API endpoints
```bash
grep -E "@(GET|POST|PUT|DELETE|PATCH)" apps/android/**/ApiService.kt
```

### Find all Web API routes
```bash
find apps/web/src/app/api -name "route.ts" -exec grep -l "export async function" {} \;
```

### Compare endpoint count
```bash
# Web routes
find apps/web/src/app/api -name "route.ts" | wc -l

# Android endpoints
grep -c "@GET\|@POST\|@PUT\|@DELETE" apps/android/**/ApiService.kt
```

## Checklist for New Endpoints

- [ ] Web route exists in `apps/web/src/app/api/`
- [ ] Android method exists in `ApiService.kt`
- [ ] iOS method exists in network service
- [ ] Request body fields match across platforms
- [ ] Response wrapper format matches (`XxxResponse` class)
- [ ] All required fields are included in response
- [ ] Field names use consistent casing
- [ ] Nested objects flattened if needed
- [ ] Error response format is consistent

## Response Format Standards

### List Endpoints
```json
{
    "items": [...],
    "total": 100,
    "page": 1,
    "pageSize": 20
}
```

### Single Item Endpoints
```json
{
    "item": { ... }
}
// OR direct object
{ "id": "...", "name": "..." }
```

### Error Responses
```json
{
    "error": "Error message here"
}
```
