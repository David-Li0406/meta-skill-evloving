---
name: api-endpoint-audit
description: Audit all API endpoints to find missing mobile implementations and inconsistencies. Use before releases, when adding features, or to verify cross-platform parity. Compares Web API routes against Android and iOS implementations.
allowed-tools: Read, Grep, Glob, Bash
---

# API Endpoint Audit

## Purpose
Find gaps between Web API endpoints and mobile implementations. Ensure all platforms support the same features.

## Quick Audit

### 1. List All Web API Routes
```bash
# Find all route.ts files
find apps/web/src/app/api -name "route.ts" -exec dirname {} \; | sort

# Count endpoints
find apps/web/src/app/api -name "route.ts" | wc -l
```

### 2. List All Android API Methods
```bash
# Find ApiService methods
grep -E "@(GET|POST|PUT|DELETE|PATCH)" apps/android/**/data/ApiService.kt

# Count endpoints
grep -c "@GET\|@POST\|@PUT\|@DELETE\|@PATCH" apps/android/**/data/ApiService.kt
```

### 3. List All iOS API Methods
```bash
# Find network service methods
grep -E "func (get|post|put|delete|create|update|fetch)" apps/ios/**/Services/*.swift

# Or find URL paths
grep -E "\"[a-z-]+\"" apps/ios/**/Services/NetworkService.swift
```

## Detailed Comparison

### Generate Endpoint Lists

**Web Routes**:
```bash
# Extract HTTP methods from routes
for route in $(find apps/web/src/app/api -name "route.ts"); do
  endpoint=$(dirname $route | sed 's|.*api/||')
  methods=$(grep -o "export async function \(GET\|POST\|PUT\|DELETE\|PATCH\)" $route | awk '{print $4}')
  echo "$endpoint: $methods"
done
```

**Android Endpoints**:
```bash
grep -E "@(GET|POST|PUT|DELETE|PATCH)" apps/android/**/ApiService.kt | \
  sed 's/.*@\(GET\|POST\|PUT\|DELETE\|PATCH\)("\([^"]*\)").*/\2: \1/'
```

### Compare Side by Side

Create comparison table manually or use:
```bash
echo "=== WEB ROUTES ==="
find apps/web/src/app/api -name "route.ts" -exec dirname {} \; | sed 's|.*api/||' | sort

echo ""
echo "=== ANDROID ENDPOINTS ==="
grep -oE '@(GET|POST|PUT|DELETE)\("[^"]*"\)' apps/android/**/ApiService.kt | \
  sed 's/@[A-Z]*("\([^"]*\)")/\1/' | sort

echo ""
echo "=== iOS ENDPOINTS ==="
grep -oE '"[a-z/-]+"' apps/ios/**/Services/NetworkService.swift | tr -d '"' | sort | uniq
```

## Common Gaps to Check

### Missing Endpoints by Feature

| Feature | Web Route | Android | iOS |
|---------|-----------|---------|-----|
| Projects | `/api/projects` | ✓ Check | ✓ Check |
| Daily Logs | `/api/daily-logs` | ✓ Check | ✓ Check |
| Time Entries | `/api/time-entries` | ✓ Check | ✓ Check |
| Inspections | `/api/inspections` | ✓ Check | ✓ Check |
| Reports | `/api/reports` | ✓ Check | ✓ Check |
| Analytics | `/api/analytics` | ✓ Check | ✓ Check |

### Check Specific Endpoint

```bash
# Does Android have this endpoint?
grep "projects" apps/android/**/ApiService.kt

# Does iOS have this endpoint?
grep "projects" apps/ios/**/Services/*.swift
```

## Response Format Audit

### Check Response Structure Matches

For each endpoint, verify response structure:

```bash
# 1. Check Web API response shape
grep -A 30 "return NextResponse.json" apps/web/src/app/api/[endpoint]/route.ts

# 2. Check Android model
grep -A 20 "data class [Response]" apps/android/**/model/*.kt

# 3. Check iOS model
grep -A 20 "struct [Response]" apps/ios/**/Models/*.swift
```

### Common Response Issues

| Issue | How to Find |
|-------|-------------|
| Missing wrapper | API returns `[...]`, mobile expects `{ items: [...] }` |
| Wrong field name | API uses `cert_name`, mobile expects `certName` |
| Missing field | API doesn't return field mobile requires |
| Extra nesting | API returns `{ _count: { items: 5 } }`, mobile expects `{ itemCount: 5 }` |

## Feature Parity Check

### List Features by Platform

```bash
# Web features (by route groups)
ls -la apps/web/src/app/api/

# Android screens
ls -la apps/android/**/ui/screens/

# iOS views
ls -la apps/ios/**/Views/
```

### Cross-Reference Features

| Feature | Web | Android | iOS | Notes |
|---------|-----|---------|-----|-------|
| Dashboard | ✓ | ✓ | ✓ | |
| Projects | ✓ | ✓ | ✓ | |
| Daily Logs | ✓ | ✓ | ✓ | |
| Time Tracking | ✓ | ✓ | ✓ | |
| Safety | ✓ | ✓ | ✓ | |
| Reports | ✓ | ✓ | ? | Check iOS |
| Analytics | ✓ | ✓ | ? | Check iOS |
| Admin | ✓ | ✓ | ? | Check iOS |

## Audit Checklist

Before release, verify:

### Endpoint Coverage
- [ ] All Web routes have Android implementation
- [ ] All Web routes have iOS implementation
- [ ] No orphaned mobile endpoints (calling non-existent routes)

### Response Consistency
- [ ] All responses use camelCase field names
- [ ] List endpoints return wrapped objects `{ items, total, page, pageSize }`
- [ ] All required fields present in responses
- [ ] Date fields serialized as ISO strings
- [ ] Nested `_count` objects flattened

### Error Handling
- [ ] All endpoints return consistent error format `{ error: string }`
- [ ] HTTP status codes are appropriate
- [ ] Auth errors return 401
- [ ] Validation errors return 400

### Authentication
- [ ] All protected routes check auth
- [ ] Token refresh handled on mobile
- [ ] Proper error on expired tokens

## Automated Checks

### Find Unimplemented Android Endpoints
```bash
# Get web routes
WEB_ROUTES=$(find apps/web/src/app/api -name "route.ts" -exec dirname {} \; | sed 's|.*api/||' | sort)

# For each, check if Android has it
for route in $WEB_ROUTES; do
  if ! grep -q "$route" apps/android/**/ApiService.kt 2>/dev/null; then
    echo "Missing in Android: $route"
  fi
done
```

### Find Response Shape Mismatches
```bash
# Look for raw array returns (potential issues)
grep -rn "NextResponse.json(\[" apps/web/src/app/api/
grep -rn "NextResponse.json(result)" apps/web/src/app/api/
```

## Quick Reference

| Task | Command |
|------|---------|
| Count web routes | `find apps/web/src/app/api -name "route.ts" \| wc -l` |
| Count Android endpoints | `grep -c "@GET\|@POST" apps/android/**/ApiService.kt` |
| Find missing implementations | Compare route lists manually |
| Check response shape | `grep -A 20 "NextResponse.json" [route.ts]` |
| Find array returns | `grep "NextResponse.json(\[" apps/web/src/app/api/**/*.ts` |
