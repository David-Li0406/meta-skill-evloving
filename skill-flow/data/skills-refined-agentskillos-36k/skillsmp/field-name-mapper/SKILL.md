---
name: field-name-mapper
description: Map field names between Web API and Android/iOS when they differ. Fix issues where Android sends 'name' but API expects 'certName', or API returns 'project_name' but Android expects 'projectName'. Handle both request and response field mapping.
allowed-tools: Read, Grep, Edit
---

# Field Name Mapper

## Purpose
Fix field name mismatches between platforms when:
- Android sends field with different name than API expects
- API returns field with different name than mobile expects
- snake_case vs camelCase conversion issues

## Common Patterns

### Android Request Field Differs from API

**Problem**: Android sends `name`, API expects `certName`

**Android Model**:
```kotlin
data class CreateCertificationRequest(
    val name: String,  // Android convention
    val certificateNumber: String?
)
```

**API Expects**:
```typescript
const { certName, certNumber } = body  // Different names!
```

**Fix in API** - Accept both:
```typescript
const {
    certName,
    name,  // Android alias
    certNumber,
    certificateNumber  // Android alias
} = body

// Use whichever was provided
const finalCertName = certName || name
const finalCertNumber = certNumber || certificateNumber
```

### API Response Field Differs from Mobile Model

**Problem**: API returns `certName`, Android expects `name`

**API Returns**:
```typescript
return { certName: 'Test Cert', certNumber: '123' }
```

**Android Expects**:
```kotlin
data class Certification(
    val name: String,  // Expects 'name', not 'certName'
    val certificateNumber: String?
)
```

**Fix in API** - Transform response:
```typescript
return {
    name: cert.certName,  // Map to Android field name
    certificateNumber: cert.certNumber
}
```

## Field Mapping Reference

### Common Mappings (Prisma → Mobile)

| Prisma/Web | Android | iOS |
|------------|---------|-----|
| `certName` | `name` | `name` |
| `certNumber` | `certificateNumber` | `certificateNumber` |
| `_count.items` | `itemCount` | `itemCount` |
| `created_at` | `createdAt` | `createdAt` |
| `user_id` | `userId` | `userId` |

### Date Field Patterns

**Prisma returns Date objects**, serialize to ISO string:
```typescript
// Prisma returns: Date object
// Android expects: "2024-01-15" or "2024-01-15T10:30:00Z"

return {
    date: record.date.toISOString().split('T')[0],  // Date only
    createdAt: record.createdAt.toISOString()  // Full datetime
}
```

### Accepting Multiple Field Names

Pattern for accepting both web and mobile field names:
```typescript
const body = await request.json()
const {
    // Web naming
    certName,
    certNumber,

    // Mobile naming (aliases)
    name,
    certificateNumber,

    // Date fields - accept both
    date,
    scheduledDate,  // Android might send this

    // Title vs Name
    title,
    listName  // Web might use this
} = body

// Resolve to final values
const finalName = certName || name
const finalNumber = certNumber || certificateNumber
const finalDate = date || scheduledDate
const finalTitle = title || listName
```

## Transform Function Pattern

Create transform functions for consistent mobile responses:

```typescript
function transformCertification(cert: PrismaCert): MobileCert {
    return {
        id: cert.id,
        name: cert.certName,  // Prisma → Mobile mapping
        certificateNumber: cert.certNumber,
        issuingAuthority: cert.issuingAuthority,
        issueDate: cert.issueDate?.toISOString().split('T')[0] ?? null,
        expiryDate: cert.expiryDate?.toISOString().split('T')[0] ?? null,
        status: cert.status,
        createdAt: cert.createdAt.toISOString()
    }
}

// Use in API response
return NextResponse.json(transformCertification(cert))
```

## Debugging Field Mismatches

### Check What Android Sends
Look at server logs for request body:
```typescript
console.log('Request body:', JSON.stringify(body, null, 2))
```

### Check What API Returns
Compare API response to Android model:
```bash
# Make API call directly
curl -X GET http://localhost:3000/api/certifications \
    -H "Authorization: Bearer $TOKEN" | jq
```

### Check Android Model Requirements
```bash
# Find Android model
grep -A 30 "data class Certification" apps/android/**/model/*.kt
```

Look for:
- Fields without default values (required)
- `@SerialName` annotations (expect snake_case)
- Field names differ from Prisma

## Quick Fix Checklist

When fixing a field mismatch:

1. [ ] Identify the exact field name mismatch
2. [ ] Check if API needs to accept alias in request
3. [ ] Check if API needs to rename in response
4. [ ] Update API to handle both names
5. [ ] Add transform function if multiple fields differ
6. [ ] Test with actual mobile request
