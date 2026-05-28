---
name: transparent-encrypted-storage
description: Security pattern for full-disk or database-level encryption at rest. Use when implementing Transparent Data Encryption (TDE), full-disk encryption, or when storage infrastructure should handle encryption without application changes. Addresses "Leak data at rest" problem.
---

# Transparent Encrypted Storage Security Pattern

Storage infrastructure automatically encrypts all data before writing to disk and decrypts when reading. Application is unaware of encryption—it happens transparently at the storage layer.

## Problem Addressed

**Leak data at rest**: All stored data could be exposed through physical theft, backup compromise, or unauthorized storage access.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Application** | Entity | Reads/writes data normally |
| **Storage Manager** | Entity | Intercepts I/O, manages encryption |
| **Cryptographer** | Cryptographic Primitive | Performs encryption/decryption |
| **Physical Storage** | Storage | Stores encrypted data |
| **Key Manager** | Entity | Manages encryption keys |

### Data Elements

- **data**: Plaintext data from application
- **{data}_k**: Encrypted data on disk
- **key**: Encryption key (managed by infrastructure)

## Pattern Flow

### Write Operation
```
Application → [write(data)] → Storage Manager
Storage Manager → [encrypt(data)] → Cryptographer
Cryptographer → [{data}_k] → Storage Manager
Storage Manager → [write({data}_k)] → Physical Storage
```

### Read Operation
```
Application → [read()] → Storage Manager
Storage Manager → [read()] → Physical Storage
Physical Storage → [{data}_k] → Storage Manager
Storage Manager → [decrypt({data}_k)] → Cryptographer
Cryptographer → [data] → Storage Manager
Storage Manager → [data] → Application
```

## Key Characteristics

### Transparent to Application
- No application code changes
- Encryption happens at storage layer
- Application sees plaintext

### All-or-Nothing
- Everything in storage is encrypted
- No selective encryption
- Simpler model, broader protection

### Infrastructure Managed
- Database or filesystem handles encryption
- Key management often integrated
- Operational, not developmental

## Implementation Options

### Database-Level TDE
Most databases support Transparent Data Encryption:
- **SQL Server TDE**: Encrypts data files, logs, backups
- **Oracle TDE**: Tablespace or column encryption
- **PostgreSQL**: pg_tde extension
- **MySQL**: InnoDB tablespace encryption
- **MongoDB**: Encrypted storage engine

### Filesystem/Disk Encryption
- **LUKS** (Linux)
- **BitLocker** (Windows)
- **FileVault** (macOS)
- **dm-crypt** (Linux)
- Cloud provider disk encryption (AWS EBS, Azure Disk, GCP)

### Cloud Provider Options
- AWS RDS encryption
- Azure SQL TDE
- GCP Cloud SQL encryption
- All major cloud storage services offer encryption at rest

## Security Considerations

### What TDE Protects Against
✓ Physical disk theft
✓ Decommissioned disk exposure
✓ Backup media theft
✓ Unauthorized file system access

### What TDE Does NOT Protect Against
✗ Authorized database access (data decrypted for queries)
✗ SQL injection (attacker queries through application)
✗ Application vulnerabilities
✗ Compromised database credentials
✗ Memory attacks (data decrypted in memory)

**Important**: TDE is ONE layer of defense, not complete protection.

### Key Management

**Critical**: Key security determines encryption security

Considerations:
- Key stored separately from encrypted data
- Use Hardware Security Module (HSM) where possible
- Key backup and recovery procedures
- Key rotation strategy
- Access controls on key material

Cloud providers offer:
- AWS KMS
- Azure Key Vault
- GCP Cloud KMS

### Performance Impact
- Modern CPUs have AES-NI hardware acceleration
- Typically 2-10% overhead
- Test with realistic workloads
- Consider SSD vs HDD differences

### Backup Encryption
TDE typically encrypts backups automatically:
- Verify backup encryption is enabled
- Test backup restore procedures
- Key availability for restores

## Comparison with Selective Encryption

| Aspect | Transparent | Selective |
|--------|-------------|-----------|
| Application changes | None | Required |
| Granularity | All data | Specific fields |
| Protection scope | Storage layer | End-to-end possible |
| Query on encrypted | Yes (decrypted for query) | No (unless special techniques) |
| Key management | Infrastructure | Application |

**Recommendation**: Use both when appropriate
- TDE for baseline storage protection
- Selective encryption for highly sensitive fields

## Implementation Checklist

- [ ] TDE enabled on database/storage
- [ ] Key stored in HSM/KMS
- [ ] Key backup procedures tested
- [ ] Key rotation schedule defined
- [ ] Backup encryption verified
- [ ] Performance impact measured
- [ ] Recovery procedures tested
- [ ] Access to key material audited
- [ ] Understood: TDE ≠ complete protection

## When to Use

### Use Transparent Encryption When:
- Need broad storage protection
- Cannot modify application
- Compliance requires encryption at rest
- Protecting against physical threats

### Combine with Selective Encryption When:
- Some data needs additional protection
- Data must be protected from DBAs
- End-to-end encryption required

## Related Patterns

- Selective encrypted storage (alternative: field-level)
- Encryption (underlying operations)
- Cryptographic key management (key handling)
- Cryptography as a service (KMS usage)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/07_01_002__transparent_encrypted_storage/
- OWASP Cryptographic Storage Cheat Sheet
- Database vendor TDE documentation
