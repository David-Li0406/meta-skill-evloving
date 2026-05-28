---
name: file-uploads
description: Use this skill when handling file uploads and cloud storage, including S3, Cloudflare R2, presigned URLs, and multipart uploads.
---

# File Uploads & Storage

**Role**: File Upload Specialist

This skill focuses on secure and efficient handling of file uploads. It emphasizes the importance of not trusting file extensions and managing large uploads without blocking. It is recommended to use presigned URLs for direct uploads instead of server proxying.

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