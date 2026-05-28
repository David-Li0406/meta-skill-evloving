---
name: privacy-encryption
description: Encrypts patient payload using AES-256-GCM cryptographic algorithm for HIPAA compliance
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I encrypt the patient payload using AES-256-GCM (Galois/Counter Mode) to protect sensitive health information. I generate a unique initialization vector (IV) and produce ciphertext for secure storage and transmission.

## When to use me

Use this when:

- Learning update is complete and you need to encrypt patient data
- You're preparing data for secure storage or transmission
- You need AES-256 encryption for HIPAA compliance

## Key Concepts

- **AES-256-GCM**: Authenticated encryption with 256-bit key
- **Initialization Vector (IV)**: Unique random value for each encryption
- **Ciphertext**: Encrypted output (Base64 encoded)
- **data_encrypted**: State flag after encryption complete

## Source Files

- `services/crypto.ts`: Encryption implementation
- `types.ts`: AnalysisResult with securityContext

## Code Patterns

- Use crypto.subtle for AES-256-GCM encryption
- Generate unique IV for each encryption operation
- Return ciphertext, IV, and algorithm metadata

## Operational Constraints

- Must use AES-256-GCM for HIPAA compliance
- Unique IV required for each encryption
- Never log plaintext patient data
