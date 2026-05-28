---
name: image-verification
description: Validates image file signatures using Magic Bytes and calculates SHA-256 cryptographic hash
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I verify image authenticity before processing. I check file signatures (Magic Bytes) to confirm the file is a valid image type and calculate a SHA-256 hash for audit trails and duplicate detection.

## When to use me

Use this when:

- An image is uploaded and needs validation
- You need to ensure the file is actually an image (not malicious content)
- You need a cryptographic hash for the image (audit/duplicate check)

## Key Concepts

- **Magic Bytes**: File signature bytes that identify the format (e.g., `FF D8 FF` for JPEG)
- **SHA-256 Hash**: 256-bit cryptographic hash for integrity and identification
- **Crypto Subtle**: Browser Web Crypto API for cryptographic operations

## Source Files

- `services/crypto.ts`: Cryptographic operations
- `services/vision.ts`: Image validation helpers

## Code Patterns

- Use `crypto.subtle.digest('SHA-256', ...)` for hashing
- Check first bytes of ArrayBuffer for magic bytes
- Reject invalid files immediately with clear error messages

## Operational Constraints

- Must reject non-image files before any processing
- Hash is used for deduplication and audit trail
- Always log verification results for traceability
