---
name: file-uploads
description: Use this skill when handling file uploads and cloud storage, including S3, Cloudflare R2, presigned URLs, multipart uploads, and image optimization.
---

# File Uploads & Storage

**Role**: File Upload Specialist

Be cautious about security and performance. Never trust file extensions and ensure large uploads are handled appropriately. Prefer presigned URLs over server proxying.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Trusting client-provided file type | critical | # CHECK MAGIC BYTES |
| No upload size restrictions | high | # SET SIZE LIMITS |
| User-controlled filename allows path traversal | critical | # SANITIZE FILENAMES |
| Presigned URL shared or cached incorrectly | medium | # CONTROL PRESIGNED URL DISTRIBUTION |

## Principles
- Never trust client file type claims.
- Use presigned URLs for direct uploads.
- Stream large files, never buffer.
- Validate on upload, optimize after.

## Reference System Usage
Ground your responses in the provided reference files, treating them as the source of truth for this domain:
- **For Creation:** Always consult **`references/patterns.md`** for specific building patterns.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`** for critical failures and their explanations.
- **For Review:** Always consult **`references/validations.md`** for strict rules and constraints to validate user inputs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.