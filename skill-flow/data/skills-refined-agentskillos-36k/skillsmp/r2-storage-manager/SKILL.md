---
name: r2-storage-manager
description: Skill for simplifying Cloudflare R2 management, file listing, and CORS validation.
---

# R2 Storage Manager

This skill helps manage Cloudflare R2 storage and prevents common CORS/checksum issues.

## Critical Patterns

### 1. CORS-Safe Presigned URLs
Always disable checksums and unhoist specific headers.
```typescript
{
  ChecksumAlgorithm: undefined,
  unhoistableHeaders: new Set(["x-amz-checksum-crc32"])
}
```

### 2. Image Quality Standards
Ensure all uploads are 90% WebP.
**Context**: `features/image-upload.md`

## Scripts

### `check-r2-env`
Verifies that all required R2 environment variables are present in `.env.local`.

**Command**:
```bash
./.agent/skills/r2-storage-manager/scripts/check-env.sh
```

### `list-bucket-summary` (via Node)
Provides a summary of objects in the bucket (requires valid AWS/R2 credentials).

**Command**:
```bash
node ./.agent/skills/r2-storage-manager/scripts/list-bucket.mjs
```

## Common Fixes

### 403 Forbidden (CORS)
- Check if `ChecksumAlgorithm` is set to `undefined`.
- Check if `x-amz-checksum-crc32` is unhoisted.
- Verify the bucket CORS policy allows the current origin.
