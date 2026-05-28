# CycloneDX CBOM Specification Reference

## Overview

**CBOM** (Cryptography Bill of Materials) is a CycloneDX capability for documenting cryptographic assets including algorithms, keys, certificates, and protocols.

**Specification Version**: 1.6+
**Component Type**: `cryptographic-asset`
**Primary Object**: `cryptoProperties`

## Component Type

```json
{
  "type": "cryptographic-asset",
  "name": "AES-256-GCM",
  "bom-ref": "crypto/algorithm/aes-256-gcm@1.0",
  "cryptoProperties": { ... }
}
```

**Definition**: "Algorithms, protocols, certificates, keys, tokens, and secrets."

## Asset Types

The `assetType` field categorizes cryptographic components:

| Asset Type | Description | Properties Object |
|------------|-------------|-------------------|
| `algorithm` | Cryptographic algorithm | `algorithmProperties` |
| `certificate` | X.509 certificate | `certificateProperties` |
| `protocol` | Cryptographic protocol (TLS, SSH) | `protocolProperties` |
| `related-crypto-material` | Keys, tokens, secrets | `relatedCryptoMaterialProperties` |

## Algorithm Properties

```json
{
  "type": "cryptographic-asset",
  "name": "AES-256-GCM",
  "bom-ref": "crypto/algorithm/aes-256-gcm@1.0",
  "cryptoProperties": {
    "assetType": "algorithm",
    "algorithmProperties": {
      "primitive": "ae",
      "parameterSetIdentifier": "256",
      "mode": "gcm",
      "executionEnvironment": "software-plain-ram",
      "implementationPlatform": "x86_64",
      "certificationLevel": ["fips-140-3"],
      "cryptoFunctions": ["keygen", "encrypt", "decrypt"],
      "classicalSecurityLevel": 256,
      "nistQuantumSecurityLevel": 5
    },
    "oid": "2.16.840.1.101.3.4.1.46"
  }
}
```

### Algorithm Fields

| Field | Type | Description |
|-------|------|-------------|
| `primitive` | enum | `ae` (authenticated encryption), `mac`, `hash`, `pke`, `kem`, `dsa`, `xof`, `kdf`, `other` |
| `parameterSetIdentifier` | string | Key size or parameter set (128, 256, 2048) |
| `mode` | string | Mode of operation (gcm, cbc, ctr, ecb) |
| `executionEnvironment` | enum | `software-plain-ram`, `hardware`, `tee`, `hsm`, `tpm` |
| `implementationPlatform` | string | Platform (x86_64, arm64) |
| `certificationLevel` | array | Certifications (fips-140-2, fips-140-3, common-criteria) |
| `cryptoFunctions` | array | `keygen`, `encrypt`, `decrypt`, `sign`, `verify`, `hash`, `encapsulate`, `decapsulate` |
| `classicalSecurityLevel` | int | Classical security bits |
| `nistQuantumSecurityLevel` | int | NIST PQC security level (1-5) |

### Algorithm Primitives

| Primitive | Full Name | Examples |
|-----------|-----------|----------|
| `ae` | Authenticated Encryption | AES-GCM, ChaCha20-Poly1305 |
| `mac` | Message Authentication Code | HMAC-SHA256 |
| `hash` | Hash Function | SHA-256, SHA-3 |
| `pke` | Public Key Encryption | RSA-OAEP |
| `kem` | Key Encapsulation | ML-KEM (Kyber) |
| `dsa` | Digital Signature | RSA, ECDSA, ML-DSA (Dilithium) |
| `xof` | Extendable Output Function | SHAKE128 |
| `kdf` | Key Derivation Function | HKDF, PBKDF2 |

## Related Crypto Material (Keys)

```json
{
  "type": "cryptographic-asset",
  "name": "RSA-2048-public",
  "bom-ref": "crypto/key/rsa-2048@1.0",
  "cryptoProperties": {
    "assetType": "related-crypto-material",
    "relatedCryptoMaterialProperties": {
      "type": "public-key",
      "id": "2e9ef09e-dfac-4526-96b4-d02f31af1b22",
      "state": "active",
      "size": 2048,
      "algorithmRef": "crypto/algorithm/rsa@1.0",
      "creationDate": "2024-01-01T00:00:00Z",
      "activationDate": "2024-01-01T00:00:00Z",
      "expirationDate": "2026-01-01T00:00:00Z",
      "securedBy": {
        "mechanism": "HSM",
        "algorithmRef": "crypto/algorithm/aes-256@1.0"
      }
    },
    "oid": "1.2.840.113549.1.1.1"
  }
}
```

### Key Material Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum | `public-key`, `private-key`, `secret-key`, `key-pair`, `certificate`, `password`, `token` |
| `id` | string | Unique identifier (UUID) |
| `state` | enum | `pre-activation`, `active`, `suspended`, `deactivated`, `compromised`, `destroyed` |
| `size` | int | Key size in bits |
| `algorithmRef` | bom-ref | Reference to algorithm component |
| `creationDate` | datetime | Key creation timestamp |
| `activationDate` | datetime | When key became active |
| `expirationDate` | datetime | Key expiry |
| `securedBy.mechanism` | enum | `Software`, `HSM`, `TPM`, `TEE` |

## Protocol Properties

```json
{
  "type": "cryptographic-asset",
  "name": "TLSv1.3",
  "bom-ref": "crypto/protocol/tls@1.3",
  "cryptoProperties": {
    "assetType": "protocol",
    "protocolProperties": {
      "type": "tls",
      "version": "1.3",
      "cipherSuites": [
        {
          "name": "TLS_AES_256_GCM_SHA384",
          "algorithms": [
            "crypto/algorithm/aes-256-gcm@1.0",
            "crypto/algorithm/sha384@1.0"
          ],
          "identifiers": ["0x13", "0x02"]
        }
      ],
      "cryptoRefArray": [
        "crypto/certificate/server@sha256:abc123"
      ]
    },
    "oid": "1.3.18.0.2.32.104"
  }
}
```

### Protocol Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum | `tls`, `ssh`, `ipsec`, `ikev2`, `sstp`, `wpa` |
| `version` | string | Protocol version (1.2, 1.3) |
| `cipherSuites` | array | Supported cipher suite combinations |
| `cipherSuites[].name` | string | Cipher suite name (IANA format) |
| `cipherSuites[].algorithms` | array | bom-refs to algorithm components |
| `cryptoRefArray` | array | References to certificates/keys |

## Certificate Properties

```json
{
  "type": "cryptographic-asset",
  "name": "server-certificate",
  "bom-ref": "crypto/certificate/server@sha256:abc123",
  "cryptoProperties": {
    "assetType": "certificate",
    "certificateProperties": {
      "subjectName": "CN=example.com",
      "issuerName": "CN=Let's Encrypt Authority X3",
      "notValidBefore": "2024-01-01T00:00:00Z",
      "notValidAfter": "2025-01-01T00:00:00Z",
      "signatureAlgorithmRef": "crypto/algorithm/sha256-rsa@1.0",
      "subjectPublicKeyRef": "crypto/key/server-public@1.0",
      "certificateFormat": "X.509",
      "certificateExtension": "pem"
    }
  }
}
```

## Complete CBOM Example

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "serialNumber": "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
  "version": 1,
  "metadata": {
    "timestamp": "2024-12-24T10:00:00Z",
    "tools": [{
      "vendor": "Zero",
      "name": "crypto-scanner",
      "version": "3.7.0"
    }]
  },
  "components": [
    {
      "type": "cryptographic-asset",
      "name": "AES-256-GCM",
      "bom-ref": "crypto/algorithm/aes-256-gcm@1.0",
      "cryptoProperties": {
        "assetType": "algorithm",
        "algorithmProperties": {
          "primitive": "ae",
          "parameterSetIdentifier": "256",
          "mode": "gcm",
          "cryptoFunctions": ["encrypt", "decrypt"],
          "classicalSecurityLevel": 256,
          "nistQuantumSecurityLevel": 5
        }
      }
    },
    {
      "type": "cryptographic-asset",
      "name": "weak-md5-usage",
      "bom-ref": "crypto/algorithm/md5@deprecated",
      "description": "Deprecated hash algorithm found in codebase",
      "cryptoProperties": {
        "assetType": "algorithm",
        "algorithmProperties": {
          "primitive": "hash",
          "cryptoFunctions": ["hash"],
          "classicalSecurityLevel": 0
        }
      }
    }
  ],
  "vulnerabilities": [
    {
      "id": "CRYPTO-001",
      "source": { "name": "Zero Crypto Scanner" },
      "description": "Use of deprecated MD5 hash algorithm",
      "ratings": [{
        "severity": "high",
        "method": "other"
      }],
      "cwes": [328],
      "affects": [{
        "ref": "crypto/algorithm/md5@deprecated"
      }],
      "recommendation": "Replace MD5 with SHA-256 or SHA-3"
    }
  ]
}
```

## Mapping from Zero crypto Scanner

| Zero Field | CycloneDX Field |
|------------|-----------------|
| `ciphers[].algorithm` | `component.name` |
| `ciphers[].mode` | `algorithmProperties.mode` |
| `ciphers[].key_size` | `algorithmProperties.parameterSetIdentifier` |
| `ciphers[].severity` | `vulnerabilities[].ratings[].severity` |
| `keys[].type` | `relatedCryptoMaterialProperties.type` |
| `keys[].size` | `relatedCryptoMaterialProperties.size` |
| `tls[].version` | `protocolProperties.version` |
| `tls[].cipher_suite` | `protocolProperties.cipherSuites[].name` |
| `certificates[].subject` | `certificateProperties.subjectName` |
| `certificates[].expiry` | `certificateProperties.notValidAfter` |

## Quantum Readiness Indicators

CBOM supports post-quantum cryptography assessment:

| NIST Level | Classical Equivalent | Algorithms |
|------------|---------------------|------------|
| 1 | AES-128 | ML-KEM-512, ML-DSA-44 |
| 2 | SHA-256 | - |
| 3 | AES-192 | ML-KEM-768, ML-DSA-65 |
| 4 | SHA-384 | - |
| 5 | AES-256 | ML-KEM-1024, ML-DSA-87 |

## References

- [CycloneDX CBOM Capability](https://cyclonedx.org/capabilities/cbom/)
- [Cryptographic Key Use Case](https://cyclonedx.org/use-cases/cryptographic-key/)
- [Cryptographic Protocol Use Case](https://cyclonedx.org/use-cases/cryptographic-protocol/)
- [IBM CBOM Repository](https://github.com/IBM/CBOM)
- [NIST SP 1800-38B](https://www.nist.gov/programs-projects/migration-post-quantum-cryptography)
