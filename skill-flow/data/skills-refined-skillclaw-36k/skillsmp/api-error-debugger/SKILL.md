---
name: api-error-debugger
description: Debug API 500 errors and unexpected responses. Use when mobile apps get server errors, when API returns wrong data, or when investigating failed requests. Checks server logs, common error patterns, and Prisma query issues.
allowed-tools: Read, Grep, Bash, Glob
---

# API Error Debugger

## Purpose
Quickly diagnose and fix API errors when mobile apps receive 500 errors, unexpected responses, or failed requests.

## Quick Diagnosis Flow

### 1. Identify the Failing Endpoint

From mobile error logs, find the endpoint:
```bash
# Android logs
~/Library/Android/sdk/platform-tools/adb logcat -d -t 100 | grep -E "(HTTP|api|error|Error)"

# iOS - check Xcode console or:
xcrun simctl spawn booted log show --last 5m --predicate 'subsystem == "com.constructionpro.app"'
```

### 2. Check Server Logs

If running locally:
```bash
# Check Next.js dev server output for errors
# Look for stack traces and Prisma errors
```

### 3. Test Endpoint Directly
```bash
# Replace TOKEN with valid JWT
curl -X GET "http://localhost:3000/api/[endpoint]" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq
```

## Common Error Patterns

### Pattern 1: Prisma Field Not Found
**Error**: `Unknown arg 'fieldName' in where.fieldName`

**Cause**: Schema changed but client not regenerated

**Fix**:
```bash
cd apps/web
npx prisma db push
# Restart dev server
```

### Pattern 2: Missing Required Field in Response
**Error**: `Fields [X, Y] are required for type...`

**Cause**: API not returning all fields Android/iOS model requires

**Debug**:
```bash
# Find the Android model
grep -A 20 "data class [ModelName]" apps/android/**/model/*.kt

# Compare to API response
curl -s "http://localhost:3000/api/[endpoint]" -H "Authorization: Bearer $TOKEN" | jq
```

**Fix**: Add missing fields to API response

### Pattern 3: JSON Parse Error (Array vs Object)
**Error**: `Expected start of object '{', but had '['`

**Cause**: API returns raw array, mobile expects wrapped object

**Debug**:
```bash
# Check what API returns
curl -s "http://localhost:3000/api/[endpoint]" -H "Authorization: Bearer $TOKEN" | jq 'type'
# Returns "array" but should be "object"
```

**Fix**: Wrap array in object:
```typescript
// Before
return NextResponse.json(items)

// After
return NextResponse.json({ items, total: items.length, page: 1, pageSize: items.length })
```

### Pattern 4: Authentication Error
**Error**: `401 Unauthorized` or `Invalid token`

**Debug**:
```bash
# Check if token is being sent
# Android - add logging to ApiService
# iOS - check network interceptor

# Verify token manually
curl -X GET "http://localhost:3000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### Pattern 5: Prisma Relation Error
**Error**: `Cannot read property 'X' of null`

**Cause**: Relation not included in query or null relation accessed

**Debug**:
```bash
# Find the Prisma query
grep -A 20 "prisma\.[model]\.find" apps/web/src/app/api/[endpoint]/route.ts
```

**Fix**: Add include or handle null:
```typescript
// Add include
const result = await prisma.model.findMany({
  include: { relation: true }
})

// Or handle null
return {
  relationField: item.relation?.field ?? null
}
```

### Pattern 6: Type Mismatch
**Error**: `Cannot deserialize` or type coercion errors

**Cause**: API returns different type than mobile expects

**Common mismatches**:
- Date objects vs ISO strings
- Numbers as strings
- snake_case vs camelCase

**Fix**:
```typescript
// Serialize dates
createdAt: item.createdAt.toISOString()

// Ensure numbers
count: Number(item.count)

// Use camelCase
projectId: item.project_id  // Transform from snake_case
```

## Debug Commands

### Find API Route
```bash
# Find route file for endpoint
find apps/web/src/app/api -name "route.ts" | xargs grep -l "[endpoint-keyword]"
```

### Check Route Implementation
```bash
# Read the route file
cat apps/web/src/app/api/[resource]/route.ts
```

### Find Related Models
```bash
# Prisma schema
grep -A 30 "model [ModelName]" apps/web/prisma/schema.prisma

# Android model
grep -A 30 "data class [ModelName]" apps/android/**/model/*.kt

# iOS model
grep -A 30 "struct [ModelName]" apps/ios/**/Models/*.swift
```

### Test with Mock Data
```bash
# POST with test data
curl -X POST "http://localhost:3000/api/[endpoint]" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

## Checklist for Debugging

When investigating an API error:

- [ ] Identify exact endpoint and HTTP method
- [ ] Get the full error message from mobile logs
- [ ] Test endpoint directly with curl
- [ ] Compare API response structure to mobile model
- [ ] Check if all required fields are present
- [ ] Verify field types match (dates, numbers, etc.)
- [ ] Check for snake_case vs camelCase issues
- [ ] Verify authentication token is valid
- [ ] Check Prisma query includes all relations
- [ ] Ensure response wrapper format is correct

## Quick Fixes

| Error Type | Quick Fix |
|------------|-----------|
| Missing field | Add field to API response |
| Array vs Object | Wrap in `{ items: [...] }` |
| Null relation | Add `?.` and `?? null` |
| Date format | Use `.toISOString()` |
| Auth error | Check token header format |
| Prisma error | Run `npx prisma db push` |
