# Crypto Pitfalls (Red Flags)

Use this list when reviewing designs or code for high-risk mistakes.

## Nonce / IV
- Reusing a nonce/IV with the same key (GCM/CTR/ChaCha20) — catastrophic.
- Using predictable or short nonces; using timestamps or counters without ensuring uniqueness.
- Mixing up nonce length requirements or truncating nonces.

## Keys and Secrets
- Reusing one key for multiple purposes (encryption + MAC + signing).
- Hardcoded keys in source, configs, or client apps.
- Storing raw keys in databases without KMS/HSM or OS keychain.
- No rotation/versioning strategy; no migration plan.

## Algorithms and Modes
- ECB mode; raw CBC without authentication; ad-hoc “encrypt then hash.”
- Obsolete hash algorithms (MD5, SHA-1) or signature schemes.
- Using homegrown primitives instead of vetted libraries.

## Passwords
- Encrypting passwords for storage (must hash + salt with KDF).
- Unsalted hashes, fast hashes, or low-cost parameters.

## Protocol and Serialization
- Custom wire formats without versioning or algorithm identifiers.
- Ad-hoc concatenation without delimiters; ambiguous parsing.

## Operational
- Logging secrets, IVs, or raw plaintext.
- Skipping integrity checks or ignoring decryption failures.
- Non-constant-time comparisons for secrets or MACs.
