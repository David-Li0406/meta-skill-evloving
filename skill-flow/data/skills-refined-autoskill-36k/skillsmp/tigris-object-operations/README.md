# Tigris Object Operations

This skill helps you work with objects in Tigris Storage - uploading, downloading, deleting, listing, and generating presigned URLs.

## What It Covers

All object operations in Tigris Storage:

- **Upload** - Put objects with access controls and content types
- **Download** - Get objects as string, file, or stream
- **Delete** - Remove objects from buckets
- **List** - Enumerate objects with prefix filtering
- **Metadata** - Get object info without downloading
- **Presigned URLs** - Generate time-limited access URLs

## Installation

### Claude Code

```bash
cp -r skills/tigris-object-operations ~/.claude/skills/
```

### claude.ai

Add the `SKILL.md` file to your project knowledge or paste its contents into the conversation.

## Usage

Claude automatically uses this skill for object operations. Trigger phrases include:

- "Upload this file to Tigris"
- "Download object from..."
- "List objects in bucket"
- "Generate a presigned URL"
- "Delete this object"

## Quick Reference

| Operation | Function | Key Parameters |
|-----------|----------|----------------|
| Upload | `put(path, body, options)` | path, body, access, contentType |
| Download | `get(path, format, options)` | path, format (string/file/stream) |
| Delete | `remove(path, options)` | path |
| List | `list(options)` | prefix, limit, paginationToken |
| Metadata | `head(path, options)` | path |
| Presigned URL | `getPresignedUrl(path, options)` | path, operation (get/put) |

## Example

```typescript
import { put, get, list, getPresignedUrl } from "@tigrisdata/storage";

// Upload
await put("photos/vacation.jpg", fileData, { contentType: "image/jpeg" });

// Download
const data = await get("photos/vacation.jpg", "string");

// List with prefix
const files = await list({ prefix: "photos/" });

// Presigned URL for direct browser upload
const url = await getPresignedUrl("uploads/doc.pdf", { operation: "put" });
```

## License

MIT
