---
name: encrypted-tunnel
description: Security pattern for channel-level encryption (TLS/SSH). Use when implementing HTTPS, securing all communication between endpoints, setting up TLS connections, or when infrastructure should handle encryption transparently. Addresses "Leak action request or data in transit" problem.
---

# Encrypted Tunnel Security Pattern

Entities set up a communication channel where ALL exchanges are encrypted. The channel infrastructure handles encryption transparently. Common implementations: TLS and SSH.

## Problem Addressed

**Leak action request or data in transit**: Any data transmitted over the channel could be observed. Encrypt everything at the channel level.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Sender** | Entity | Initiates communication |
| **Receiver** | Entity | Receives communication |
| **EndpointS** | Entity | Manages sending end of tunnel |
| **EndpointR** | Entity | Manages receiving end of tunnel |
| **CryptographerS** | Cryptographic Primitive | Encrypts for Sender |
| **CryptographerR** | Cryptographic Primitive | Decrypts for Receiver |
| **EndpointManagerS** | Entity | Configures sender endpoint |
| **EndpointManagerR** | Entity | Configures receiver endpoint |

### Data Elements

- **action/data**: Plaintext communication
- **{x}_k**: Encrypted communication
- **config**: Cipher configuration, certificates, keys

## Pattern Flow

### Setup Phase
```
EndpointManagerS → [initialise(config)] → EndpointS
EndpointManagerR → [initialise(config)] → EndpointR
```

### Communication Phase
```
Sender → [action/data] → EndpointS
EndpointS ↔ EndpointR: [negotiate cipher/key] (if needed)
EndpointS → [encrypt] → CryptographerS → [{x}_k] → EndpointS
EndpointS → [{x}_k] → EndpointR (over channel)
EndpointR → [decrypt] → CryptographerR → [data] → EndpointR
EndpointR → [action/data] → Receiver
```

## Key Characteristics

### Transparent Encryption
- Sender/Receiver don't manage encryption directly
- Endpoints handle cryptographic operations
- Application sees plaintext

### All-or-Nothing
- Everything through the tunnel is encrypted
- No selective encryption at this level
- Simpler mental model

### Infrastructure Managed
- TLS libraries handle complexity
- Standardized protocols
- Well-tested implementations

## TLS Implementation (Most Common)

### Configuration Options
- Protocol version: TLS 1.2 minimum, TLS 1.3 preferred
- Cipher suites: Modern, authenticated encryption
- Certificate validation: Enable and configure properly

### Mozilla SSL Configuration Generator
Use for safe defaults: https://ssl-config.mozilla.org/

### TLS 1.3 Benefits
- Simplified handshake
- Stronger cipher suites only
- Forward secrecy required
- Removed vulnerable options

## Security Considerations

### Never Implement Custom Protocols
- Use TLS/SSH, not custom encryption
- Use established libraries (OpenSSL, BoringSSL, etc.)
- Never implement your own handshake

### Certificate Validation
**Critical**: Always validate certificates
- Verify certificate chain
- Check certificate not expired
- Verify hostname matches
- Check revocation status (OCSP, CRL)

Disabling certificate validation defeats TLS security.

### Cipher Suite Selection
- Disable weak ciphers (RC4, DES, export ciphers)
- Prefer authenticated encryption (GCM modes)
- Prefer forward secrecy (ECDHE, DHE)
- Disable SSL 2.0, SSL 3.0, TLS 1.0, TLS 1.1

### Private Key Protection
- Protect server private key
- Restrict file permissions
- Consider HSM for high-security applications
- Rotate keys periodically

### Certificate Management
- Use certificates from trusted CAs
- Automate renewal (Let's Encrypt)
- Monitor expiration
- Implement certificate pinning for mobile apps (carefully)

### HSTS (HTTP Strict Transport Security)
For web applications:
- Force HTTPS connections
- Prevent downgrade attacks
- Include subdomains
- Consider preloading

## Comparison with Selective Encryption

| Aspect | Encrypted Tunnel | Selective Encryption |
|--------|-----------------|---------------------|
| Scope | All communication | Specific data |
| Control | Infrastructure | Application |
| Complexity | Lower for application | Higher for application |
| Flexibility | Less | More |

**Recommendation**: Use encrypted tunnel (TLS) as baseline. Add selective encryption for data that needs additional protection (e.g., encrypted at rest AND in transit).

## Implementation Checklist

- [ ] TLS 1.2+ (prefer 1.3)
- [ ] Strong cipher suites only
- [ ] Certificate validation enabled
- [ ] Hostname verification enabled
- [ ] Certificate from trusted CA
- [ ] Private key protected
- [ ] HSTS enabled (web apps)
- [ ] Automatic certificate renewal
- [ ] No custom protocol implementation
- [ ] Forward secrecy enabled

## Common Misconfigurations

| Misconfiguration | Risk |
|-----------------|------|
| Certificate validation disabled | MITM attacks |
| Old TLS versions enabled | Protocol downgrade |
| Weak cipher suites | Cryptographic attacks |
| Expired certificates | Connection failures, user warnings |
| Self-signed certs in production | Trust issues |

## Related Patterns

- Selective encrypted transmission (alternative: selective encryption)
- Encryption (underlying operations)
- Cryptographic key management (certificate/key handling)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/06_01_002__encrypted_tunnel/
- Mozilla SSL Configuration Generator
- OWASP TLS Cheat Sheet
