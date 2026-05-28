# OpenSSL

**Category**: cryptographic-libraries/tls
**Description**: Cryptographic library providing SSL/TLS implementation
**Homepage**: https://www.openssl.org

## Package Detection

### PYPI
- `pyopenssl`
- `cryptography`

### NPM
- `node-forge`
- `crypto` (built-in)

### GO
- `crypto/tls` (standard library)

### RUBYGEMS
- `openssl` (standard library)

## Import Detection

### Python
**Pattern**: `import ssl`
- Standard library SSL
- Example: `import ssl; ssl.create_default_context()`

**Pattern**: `from OpenSSL import`
- PyOpenSSL import
- Example: `from OpenSSL import crypto`

**Pattern**: `from cryptography`
- Cryptography library
- Example: `from cryptography.hazmat.primitives import hashes`

### Go
**Pattern**: `"crypto/tls"`
- Go standard TLS library
- Example: `import "crypto/tls"`

## Environment Variables

- `SSL_CERT_FILE`
- `SSL_CERT_DIR`
- `OPENSSL_CONF`

## Configuration Files

- `openssl.cnf`
- `*.pem`
- `*.crt`
- `*.key`
- `*.csr`

## Detection Notes

- Check for SSL/TLS configuration in code
- Look for certificate files
- Monitor for deprecated protocols (SSLv3, TLS 1.0, TLS 1.1)
- Check for weak cipher suites

## Security Considerations

### Deprecated Versions
- OpenSSL 1.0.x (end of life)
- OpenSSL 1.1.0 (end of life)

### Current Supported
- OpenSSL 1.1.1 (LTS until Sep 2023)
- OpenSSL 3.0.x (current LTS)
- OpenSSL 3.1.x (current)

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Certificate Files Detection**: 85% (MEDIUM)
- **Environment Variable Detection**: 80% (MEDIUM)
