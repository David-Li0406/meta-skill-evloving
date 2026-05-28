---
name: drime-api
description: Knowledge about Drime Cloud API endpoints, authentication, file operations, workspaces, vault encryption, and S3 upload flow. Use when working with API integration, adding new endpoints, or debugging API issues.
---

# Drime Cloud API Integration

This skill provides knowledge about the Drime Cloud REST API for the shell application.

## API Base

- **Production**: `https://app.drime.cloud/api/v1`
- **Authentication**: `Authorization: Bearer <token>`

## Core Concepts

### IDs vs Hashes
- **Numeric IDs**: Used for mutations (move, delete, copy, rename)
- **Base64 Hashes**: Used for downloads and shareable links
- **Hash calculation**: `base64(id + "|")` with trailing `=` stripped

### Workspace ID
- `0` = Default personal workspace
- Always pass `workspaceId` query param for scoped operations

### Pagination
- Use `perPage=9999999999` to fetch all in one request
- Simplifies client logic, API handles large result sets

## Key Endpoints

### Authentication
```
GET /cli/loggedUser → User info
POST /auth/login → { email, password, token_name } → { user, access_token }
```

### File Listing
```
GET /users/{id}/folders?workspaceId={id}&perPage=9999999999 → All folders (tree)
GET /drive/file-entries?parentIds[]={id}&workspaceId={id} → Children of folder
```

### File Operations
```
POST /folders → Create folder { name, parentId?, workspaceId }
POST /file-entries/move → { entryIds[], destinationId?, workspaceId }
POST /file-entries/duplicate → Copy files
POST /file-entries/delete → { entryIds[], deleteForever?, emptyTrash? }
PUT /file-entries/{id} → Rename { name }
```

## S3 Upload Flow

Uploads use a 4-step process to offload bandwidth to S3/R2.

### Upload Constants
```go
const (
    ChunkSize          = 60 * 1024 * 1024  // 60MB per part
    MultipartThreshold = 65 * 1024 * 1024  // Use multipart above 65MB
    BatchSize          = 8                  // Sign URLs in batches of 8
    PartUploadRetries  = 5                  // Retry individual parts
)
```

### Flow

1. **Validate**: `POST /uploads/validate`
   - Checks for duplicates and quota
   - Handle duplicates via policy: `ask`, `replace`, `rename`, `skip`

2. **Presign**:
   - **Small (<65MB)**: `POST /s3/simple/presign` → Single PUT URL
   - **Large (>=65MB)**: `POST /s3/multipart/create` → `uploadId` + `key`
     - Then `POST /s3/multipart/batch-sign-part-urls` for part URLs

3. **Transfer**: PUT binary to presigned URL(s)
   - For multipart: collect ETags, complete via `POST /s3/multipart/complete`
   - On failure: `POST /s3/multipart/abort`

4. **Finalize**: `POST /s3/entries`
   - Creates FileEntry in database
   - Requires: `filename`, `size`, `clientName`, `relativePath`

## Hash Calculation

The Drime hash is computed from the file ID:

```go
// Encode: ID → Hash
func CalculateDrimeHash(fileID int64) string {
    hashStr := fmt.Sprintf("%d|", fileID)
    encoded := base64.StdEncoding.EncodeToString([]byte(hashStr))
    return strings.TrimRight(encoded, "=")
}

// Decode: Hash → ID
func DecodeDrimeHash(hash string) (int64, error) {
    padding := (4 - len(hash)%4) % 4
    hash += strings.Repeat("=", padding)
    decoded, _ := base64.StdEncoding.DecodeString(hash)
    idStr := strings.TrimSuffix(string(decoded), "|")
    return strconv.ParseInt(idStr, 10, 64)
}
```

## Vault Encryption (Client-Side)

Zero-knowledge encryption using AES-256-GCM:

- **Key Derivation**: PBKDF2-SHA256 (250k iterations) with user password + vault salt
- **Encryption**: AES-256-GCM with random 12-byte IV per file
- **Auth Tag**: 16 bytes appended to ciphertext
- **Uploads**: Encrypt before S3 upload, set `isEncrypted=1` in `POST /s3/entries`
- **Downloads**: `GET /file-entries/download/{hash}?encrypted=true`

### Vault Endpoints
```
GET /vault                     → Metadata (salt, iv, check)
POST /vault                    → Initialize { password, password_confirmation }
GET /vault/file-entries        → List vault entries (?parentHash={hash})
POST /vault/delete-entries     → Permanent delete (no trash in vault)
```

## Workspaces

```
GET /me/workspaces                      → List workspaces
GET /workspace/{id}                     → Details with members
POST /workspace                         → Create { name }
PUT /workspace/{id}                     → Update
DELETE /workspace/{id}                  → Delete
POST /workspace/{id}/invite             → { email, roleId }
DELETE /workspace/{id}/member/{id}      → Kick member
GET /workspace_roles                    → Available roles
```

## Sharing

```
POST /file-entries/{id}/shareable-link  → Create public link
PUT /file-entries/{id}/shareable-link   → Update settings
DELETE /file-entries/{id}/shareable-link → Remove link
POST /file-entries/{id}/share           → { emails[], roleId } (email invites)
```

## Starring & Tracking

```
POST /file-entries/{id}/star            → Star
DELETE /file-entries/{id}/star          → Unstar
PUT /file-entries/{id}/add-tracking     → Start tracking
DELETE /file-entries/{id}/tracking      → Stop tracking
GET /track/infos/{id}                   → Get tracking stats
```

## Error Handling

### Error Response Codes

| Code | Meaning | Client Action |
|------|---------|---------------|
| `401 Unauthorized` | Token expired or invalid | Prompt re-login, clear stored token |
| `403 Forbidden` | Permission denied | Check workspace membership, entry permissions |
| `404 Not Found` | Entry doesn't exist or no access | Verify path, check cache staleness |
| `429 Too Many Requests` | Rate limited | Read `Retry-After` header, back off |
| `500+ Server Error` | Backend issue | Retry with exponential backoff |

### Client-Side Error Handling

```go
// Check for token expiration
if errors.Is(err, api.ErrTokenExpired) {
    return fmt.Errorf("session expired, please run: login")
}

// Retry transient failures
func withRetry(fn func() error) error {
    for i := 0; i < 3; i++ {
        if err := fn(); err != nil {
            if isTransient(err) {
                time.Sleep(time.Duration(i+1) * time.Second)
                continue
            }
            return err
        }
        return nil
    }
    return fmt.Errorf("max retries exceeded")
}
```

## Reference

See [drime-openapi.yaml](../../../drime-openapi.yaml) for complete API specification.
