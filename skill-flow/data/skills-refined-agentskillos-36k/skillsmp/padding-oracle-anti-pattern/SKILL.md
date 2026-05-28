---
name: "padding-oracle-anti-pattern"
description: "Security anti-pattern for padding oracle vulnerabilities (CWE-649). Use when generating or reviewing code that decrypts CBC-mode ciphertext, handles decryption errors, or returns different errors for padding vs other failures. Detects error message oracles."
---

# Padding Oracle Anti-Pattern

**Severity:** High

## Summary

Applications leak padding correctness during decryption through different error messages ("Invalid Padding" vs. "Decryption Failed") or timing differences. Attackers manipulate ciphertext and observe responses to decrypt entire messages byte-by-byte without knowing the key, breaking confidentiality.

## The Anti-Pattern

The anti-pattern is using CBC mode and returning different responses based on decryption error type.

### BAD Code Example

```python
# VULNERABLE: The decryption function returns different error messages.
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from flask import request

KEY = b'sixteen byte key' # Should be randomly generated and managed securely

@app.route("/decrypt")
def decrypt_data():
    encrypted_data = request.args.get('data').decode('hex')
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv))
    decryptor = cipher.decryptor()

    try:
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Check padding
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_padded) + unpadder.finalize()

        return "Decryption successful!", 200

    except ValueError as e:
        # ORACLE: Different error responses leak information.
        # Wrong padding raises ValueError with "Invalid padding".
        # Other corruption causes different errors.
        if "padding" in str(e).lower():
            return "Error: Invalid padding.", 400
        else:
            return "Error: Decryption failed.", 500

# Attacker sends modified ciphertext, observes 400 vs. 500 errors,
# deduces plaintext information.
```

### GOOD Code Example

```python
# SECURE: Use an Authenticated Encryption with Associated Data (AEAD) mode like GCM.
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flask import request

KEY = AESGCM.generate_key(bit_length=128) # Generate a secure key

def encrypt_gcm(data):
    aesgcm = AESGCM(KEY)
    nonce = os.urandom(12) # GCM uses a nonce
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext

@app.route("/decrypt/secure")
def decrypt_data_secure():
    encrypted_data = request.args.get('data').decode('hex')
    nonce = encrypted_data[:12]
    ciphertext_with_tag = encrypted_data[12:]

    aesgcm = AESGCM(KEY)

    try:
        # AEAD mode automatically verifies integrity (authentication tag).
        # Tampering fails with single generic exception before padding step.
        # (No padding in AEAD modes.)
        decrypted_data = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
        return "Decryption successful!", 200
    except InvalidTag:
        # Any failure (tampering, corruption) → single generic error.
        # No useful information for attacker.
        return "Error: Decryption failed or data is corrupt.", 400

# If using CBC: Use "Encrypt-then-MAC" scheme.
# Compute MAC (HMAC-SHA256) of ciphertext, verify BEFORE decryption.
# Invalid MAC → reject without decryption.
```

## Detection

- **Review decryption code:** Look for any code that decrypts data using CBC mode.
- **Examine error handling:** Check the `try...except` blocks around decryption logic. Does the code catch different exceptions (e.g., `PaddingError`, `CryptoError`) and return different HTTP responses, status codes, or error messages for each?
- **Look for timing differences:** In some rare cases, the oracle can be a timing side channel, where valid padding checks take slightly longer than invalid ones. This is much harder to detect via code review.
- **Perform active testing:** Use a tool like `padbuster` to actively test an endpoint for a padding oracle vulnerability.

## Prevention

- [ ] **Use AEAD cipher modes:** Best solution. AES-GCM or ChaCha20-Poly1305 combine encryption and authentication. Not vulnerable to padding oracles.
- [ ] **Use Encrypt-then-MAC with CBC:** Encrypt data, compute MAC (HMAC-SHA256) of ciphertext+IV. Verify MAC before decryption. Invalid MAC → reject immediately without decrypting.
- [ ] **Handle all errors identically:** Same generic error message and status code for bad padding, corrupt blocks, or invalid MACs.

## Related Security Patterns & Anti-Patterns

- [Weak Encryption Anti-Pattern](../weak-encryption/): Choosing a vulnerable mode like CBC without a MAC is a common weak encryption pattern.
- [Timing Attacks Anti-Pattern](../timing-attacks/): A related side-channel attack where information is leaked through how long an operation takes.
- [Verbose Error Messages Anti-Pattern](../verbose-error-messages/): A padding oracle is a specific type of verbose error message vulnerability.

## References

- [OWASP Top 10 A04:2025 - Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)
- [OWASP GenAI LLM10:2025 - Unbounded Consumption](https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/)
- [CWE-649: Reliance on Obfuscation](https://cwe.mitre.org/data/definitions/649.html)
- [CAPEC-463: Padding Oracle Crypto Attack](https://capec.mitre.org/data/definitions/463.html)
- [Padding Oracle Attack (Wikipedia)](https://en.wikipedia.org/wiki/Padding_oracle_attack)
- [BlueKrypt - Cryptographic Key Length Recommendation](https://www.keylength.com/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
