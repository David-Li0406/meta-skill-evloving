# Form Encryption

Protect sensitive data with asymmetric encryption.

## Overview

Encrypted forms use:
- **Asymmetric encryption** (RSA public/private keys)
- **Hybrid approach**: Symmetric key encrypts data, public key encrypts symmetric key

Benefits:
- Data encrypted on device before transmission
- Server cannot read encrypted data
- Security independent of HTTPS
- Integrity verification built-in

---

## How It Works

1. Collect generates random 256-bit symmetric key
2. Form data and attachments encrypted with symmetric key
3. Symmetric key encrypted with public key
4. Encrypted submission uploaded to server
5. Server stores encrypted data (cannot decrypt)
6. Briefcase decrypts using private key

---

## Setup Process

### 1. Generate RSA Key Pair

**On Mac/Linux:**

```bash
# Generate private key
openssl genrsa -out MyPrivateKey.pem 2048

# Extract public key
openssl rsa -in MyPrivateKey.pem -pubout -out MyPublicKey.pem
```

**On Windows:**

```bash
openssl genpkey -out MyPrivateKey.pem -outform PEM -algorithm RSA -pkeyopt rsa_keygen_bits:2048
openssl rsa -in MyPrivateKey.pem -inform PEM -out MyPublicKey.pem -outform PEM -pubout
```

### 2. Get Public Key Content

Open `MyPublicKey.pem` and copy content between:
```
-----BEGIN PUBLIC KEY-----
[base64 content here]
-----END PUBLIC KEY-----
```

### 3. Configure Form

Add to settings sheet:

| form_title | form_id | public_key |
|------------|---------|------------|
| Secure Survey | secure | MIIBIjANBgkqh... |

**Note:** Only include the base64 content, not the BEGIN/END lines.

---

## Decryption Process

Use **ODK Briefcase** to decrypt:

1. Download encrypted submissions from server
2. Open Briefcase
3. Provide private key file path
4. Export data (decrypts automatically)
5. CSV includes signature validation column

---

## Settings Sheet Example

| form_title | form_id | version | public_key | submission_url |
|------------|---------|---------|------------|----------------|
| Health Survey | health_enc | 2024010100 | MIIBIjAN... | https://server.example.com/submission |

---

## Security Considerations

### Private Key Security

- Store in secure location
- Restrict access strictly
- Never share or transmit insecurely
- Consider hardware security modules for high-security needs

### Key Management

- Document key creation date
- Plan key rotation if needed
- Backup private key securely
- Test decryption before deployment

### Limitations

| Limitation | Description |
|------------|-------------|
| No prevention of fake data | Encryption doesn't verify authenticity |
| Residual data on device | Unencrypted data may remain in temp files |
| Key compromise | All data decryptable if key leaked |

### Device Security

- Establish SD card wiping protocols
- Educate enumerators on device security
- Consider device management policies

---

## Signature Validation

Briefcase export includes validation column:
- **true**: Submission verified
- **false**: Possible tampering or missing attachments

Investigate any `false` signatures.

---

## Best Practices

### Key Generation

- Use 2048-bit minimum (4096 for high security)
- Generate keys on secure system
- Verify key pair works before deployment

### Deployment

- Test full workflow before rollout
- Ensure Briefcase available for decryption
- Train staff on decryption process
- Document procedures

### Ongoing

- Monitor for decryption issues
- Audit access to private keys
- Plan for key expiration/rotation

---

## Troubleshooting

### Decryption Fails

1. Verify correct private key
2. Check key format (PEM)
3. Ensure submission not corrupted
4. Check Briefcase version compatibility

### Missing Attachments

1. Check device storage during collection
2. Verify upload completed
3. Review network conditions during submission

### Performance Issues

- Encryption adds processing time
- Large attachments take longer
- Consider network bandwidth for uploads
