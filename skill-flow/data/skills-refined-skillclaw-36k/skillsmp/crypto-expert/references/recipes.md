# Crypto Recipes (Goal → Construction)

Use this as a minimal decision guide. Always prefer standard protocols and library recipes.

## Confidentiality + Integrity (general data encryption)
- Prefer AEAD: AES-GCM or ChaCha20-Poly1305.
- Require unique nonce/IV per key; store nonce and algorithm/version metadata with ciphertext.
- Use Associated Data (AAD) for headers or context that must be authenticated.

## Integrity only
- HMAC (SHA-256/512) for symmetric integrity.
- AEAD tag if you already use AEAD for encryption.

## Authenticity / Non-repudiation
- Sign with Ed25519 or ECDSA using modern curves.
- Store signature + algorithm + key id + version.

## Password storage
- Use Argon2id (preferred), scrypt or bcrypt (acceptable) with tuned parameters.
- Always salt; consider pepper stored separately (KMS/secret manager).

## Key derivation
- Use HKDF for deriving multiple sub-keys from a master key.
- Use a password-based KDF (Argon2id/scrypt/bcrypt/PBKDF2) for user passwords.

## Transport security
- Use TLS with modern configurations and managed libraries.
- Pinning is risky; only if a strong operational plan exists.

## Key storage
- Use KMS/HSM or OS keychain; avoid raw keys in app configs.
- Rotate keys; support decryption with prior key versions.

## FIPS / FedRAMP considerations (high-level)
- If FIPS or FedRAMP applies, require FIPS 140-3 validated cryptographic modules via CMVP and approved modes.
- FIPS 140-3 aligns with ISO/IEC 19790 and ISO/IEC 24759; implementation/testing guidance is in the SP 800-140 series.
- Use provider/libraries that offer validated builds and documented compliance boundaries.
- Ensure config, deployment, and operational controls meet the policy requirements.
- Always verify current requirements with compliance/security teams before final guidance.

## NIST PQC (high-level)
- NIST standardized ML-KEM (FIPS 203) for key establishment/encryption and ML-DSA (FIPS 204) plus SLH-DSA (FIPS 205) for signatures.
- FN-DSA (FALCON) is in the standardization pipeline; treat as draft until finalized.
- Prefer migration plans that support hybrid (classical + PQC) where required by policy.
