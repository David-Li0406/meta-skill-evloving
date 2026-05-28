---
name: file-uploads
description: Use this skill when you need to handle file uploads securely and efficiently, particularly with cloud storage solutions like S3 and Cloudflare R2.
---

# File Uploads & Storage

**Role**: File Upload Specialist

This skill focuses on the secure and efficient handling of file uploads, particularly for large files. It emphasizes the importance of security and performance, advocating for the use of presigned URLs and careful validation of file types.

## Principles
- Never trust client file type claims; always validate file types.
- Use presigned URLs for direct uploads to enhance security.
- Stream large files to avoid blocking; never buffer them entirely.
- Validate files upon upload and optimize them afterward.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Trusting client-provided file type | critical | # CHECK MAGIC BYTES |
| No upload size restrictions | high | # SET SIZE LIMITS |
| User-controlled filename allows path traversal | critical | # SANITIZE FILENAMES |
| Presigned URL shared or cached incorrectly | medium | # CONTROL PRESIGNED URL DISTRIBUTION |

## Reference System Usage
Always consult the provided reference files for guidance on creation, diagnosis, and review to ensure adherence to best practices and avoid common pitfalls.