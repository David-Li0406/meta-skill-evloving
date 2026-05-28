# TLS Misconfiguration

**Category**: cryptography/tls-misconfig
**Description**: Detection of insecure TLS/SSL configurations
**CWE**: CWE-295, CWE-757

---

## Python TLS Issues

### Python Unverified SSL Context
**Pattern**: `ssl\._create_unverified_context`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Disabled certificate verification
- CWE-295: Improper Certificate Validation

### Python Verify False
**Pattern**: `verify\s*=\s*False`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Requests/urllib3 cert verification disabled

### Python CERT_NONE
**Pattern**: `CERT_NONE`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- SSL context with no cert verification

### Python Check Hostname False
**Pattern**: `check_hostname\s*=\s*False`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Hostname verification disabled

### Python Verify Mode CERT_NONE
**Pattern**: `verify_mode\s*=\s*ssl\.CERT_NONE`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Explicit CERT_NONE assignment

### Python SSLv2 Protocol
**Pattern**: `ssl\.PROTOCOL_SSLv2`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- SSLv2 protocol (broken)
- CWE-757: Selection of Less-Secure Algorithm

### Python SSLv3 Protocol
**Pattern**: `ssl\.PROTOCOL_SSLv3`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- SSLv3 protocol (broken - POODLE)

### Python TLSv1.0 Protocol
**Pattern**: `ssl\.PROTOCOL_TLSv1\b`
**Type**: regex
**Severity**: high
**Languages**: [python]
- TLS 1.0 protocol (deprecated)

### Python TLSv1.1 Protocol
**Pattern**: `ssl\.PROTOCOL_TLSv1_1`
**Type**: regex
**Severity**: high
**Languages**: [python]
- TLS 1.1 protocol (deprecated)

### Python Disable SSL Warnings
**Pattern**: `urllib3\.disable_warnings`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Disabling SSL warnings

---

## JavaScript/Node.js TLS Issues

### Node.js RejectUnauthorized False
**Pattern**: `rejectUnauthorized\s*:\s*false`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Node.js TLS cert verification disabled
- CWE-295: Improper Certificate Validation

### Node.js TLS Reject Unauthorized Env
**Pattern**: `NODE_TLS_REJECT_UNAUTHORIZED.*['"]?0['"]?`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Environment variable disabling TLS verification

### Node.js Custom Agent Insecure
**Pattern**: `agent:\s*new https\.Agent\(.*rejectUnauthorized`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Custom agent with disabled verification

### Node.js TLSv1.0 Minimum
**Pattern**: `minVersion\s*:\s*['"]TLSv1['"]`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Deprecated TLS 1.0 as minimum
- CWE-757: Selection of Less-Secure Algorithm

### Node.js TLSv1.1 Minimum
**Pattern**: `minVersion\s*:\s*['"]TLSv1\.1['"]`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Deprecated TLS 1.1 as minimum

### Node.js SSLv3 Protocol
**Pattern**: `secureProtocol\s*:\s*['"]SSLv3`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Broken SSLv3 protocol

### Node.js SSLv2 Protocol
**Pattern**: `secureProtocol\s*:\s*['"]SSLv2`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Broken SSLv2 protocol

### Node.js TLSv1 Method
**Pattern**: `secureProtocol\s*:\s*['"]TLSv1_method`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Deprecated TLS 1.0

### Node.js Empty Hostname Check
**Pattern**: `checkServerIdentity:\s*\(\)\s*=>`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Empty hostname verification callback

---

## Java TLS Issues

### Java Allow All Hostname Verifier
**Pattern**: `setHostnameVerifier\(.*ALLOW_ALL`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Hostname verification disabled (Apache HttpClient)
- CWE-295: Improper Certificate Validation

### Java Noop Hostname Verifier
**Pattern**: `setHostnameVerifier\(.*NoopHostnameVerifier`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Noop hostname verifier

### Java Trust All Certificates
**Pattern**: `TrustManager.*X509Certificate.*return`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Custom trust manager accepting all certs

### Java Empty Server Trust Check
**Pattern**: `checkServerTrusted.*\{\s*\}`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Empty trust check implementation

### Java Empty Client Trust Check
**Pattern**: `checkClientTrusted.*\{\s*\}`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Empty client trust check

### Java Generic SSL Context
**Pattern**: `SSLContext\.getInstance\(["']SSL["']\)`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Generic SSL protocol (may use SSLv3)

### Java SSLv3 Context
**Pattern**: `SSLContext\.getInstance\(["']SSLv3["']\)`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Broken SSLv3
- CWE-757: Selection of Less-Secure Algorithm

### Java TLSv1.0 Context
**Pattern**: `SSLContext\.getInstance\(["']TLSv1["']\)`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Deprecated TLS 1.0

### Java TLSv1.1 Context
**Pattern**: `SSLContext\.getInstance\(["']TLSv1\.1["']\)`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Deprecated TLS 1.1

### Java Enable SSLv3 Protocol
**Pattern**: `setEnabledProtocols.*SSLv3`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Enabling SSLv3

### Java Enable TLSv1.0 Protocol
**Pattern**: `setEnabledProtocols.*TLSv1[^.]`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Enabling TLS 1.0

---

## Go TLS Issues

### Go InsecureSkipVerify
**Pattern**: `InsecureSkipVerify\s*:\s*true`
**Type**: regex
**Severity**: critical
**Languages**: [go]
- Go TLS skip certificate verification
- CWE-295: Improper Certificate Validation

### Go SSL 3.0 MinVersion
**Pattern**: `MinVersion\s*:\s*tls\.VersionSSL30`
**Type**: regex
**Severity**: critical
**Languages**: [go]
- Broken SSL 3.0 in Go
- CWE-757: Selection of Less-Secure Algorithm

### Go TLS 1.0 MinVersion
**Pattern**: `MinVersion\s*:\s*tls\.VersionTLS10`
**Type**: regex
**Severity**: high
**Languages**: [go]
- Deprecated TLS 1.0 in Go

### Go TLS 1.1 MinVersion
**Pattern**: `MinVersion\s*:\s*tls\.VersionTLS11`
**Type**: regex
**Severity**: high
**Languages**: [go]
- Deprecated TLS 1.1 in Go

### Go TLS 1.0 MaxVersion
**Pattern**: `MaxVersion\s*:\s*tls\.VersionTLS10`
**Type**: regex
**Severity**: high
**Languages**: [go]
- Maximum TLS 1.0 (should support higher)

### Go Empty Verify Callback
**Pattern**: `VerifyPeerCertificate:\s*func.*nil`
**Type**: regex
**Severity**: critical
**Languages**: [go]
- Empty certificate verification function

### Go Empty ServerName
**Pattern**: `ServerName:\s*["']["']`
**Type**: regex
**Severity**: high
**Languages**: [go]
- Empty server name (disables SNI verification)

---

## Ruby TLS Issues

### Ruby VERIFY_NONE
**Pattern**: `verify_mode\s*=\s*OpenSSL::SSL::VERIFY_NONE`
**Type**: regex
**Severity**: critical
**Languages**: [ruby]
- Certificate verification disabled
- CWE-295: Improper Certificate Validation

### Ruby VERIFY_NONE Constant
**Pattern**: `VERIFY_NONE`
**Type**: regex
**Severity**: critical
**Languages**: [ruby]
- VERIFY_NONE constant usage

### Ruby SSLv3 Version
**Pattern**: `ssl_version\s*=\s*['":]*SSLv3`
**Type**: regex
**Severity**: critical
**Languages**: [ruby]
- SSLv3 in Ruby
- CWE-757: Selection of Less-Secure Algorithm

### Ruby TLSv1.0 Version
**Pattern**: `ssl_version\s*=\s*['":]*TLSv1\b`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- TLS 1.0 in Ruby

---

## PHP TLS Issues

### PHP cURL Verify Peer Disabled
**Pattern**: `CURLOPT_SSL_VERIFYPEER.*false`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- cURL SSL verification disabled
- CWE-295: Improper Certificate Validation

### PHP cURL Verify Host Disabled
**Pattern**: `CURLOPT_SSL_VERIFYHOST.*0`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- cURL hostname verification disabled

### PHP Stream Verify Peer Disabled
**Pattern**: `verify_peer.*false`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- Stream context SSL verification disabled

### PHP Stream Verify Peer Name Disabled
**Pattern**: `verify_peer_name.*false`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- Stream context peer name verification disabled

### PHP Allow Self-Signed
**Pattern**: `allow_self_signed.*true`
**Type**: regex
**Severity**: high
**Languages**: [php]
- Allowing self-signed certificates

---

## C/C++ TLS Issues

### OpenSSL SSL_VERIFY_NONE Context
**Pattern**: `SSL_CTX_set_verify.*SSL_VERIFY_NONE`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- OpenSSL verification disabled
- CWE-295: Improper Certificate Validation

### OpenSSL SSL_VERIFY_NONE Connection
**Pattern**: `SSL_set_verify.*SSL_VERIFY_NONE`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- SSL connection verification disabled

### OpenSSL SSLv3 MinVersion
**Pattern**: `SSL_CTX_set_min_proto_version.*SSL3_VERSION`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- SSLv3 minimum version
- CWE-757: Selection of Less-Secure Algorithm

### OpenSSL TLSv1.0 MinVersion
**Pattern**: `SSL_CTX_set_min_proto_version.*TLS1_VERSION\b`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- TLS 1.0 minimum version

---

## C# TLS Issues

### CSharp Certificate Callback True
**Pattern**: `ServicePointManager\.ServerCertificateValidationCallback.*true`
**Type**: regex
**Severity**: critical
**Languages**: [csharp]
- Certificate validation callback always returns true
- CWE-295: Improper Certificate Validation

### CSharp HttpClient Cert Validation Disabled
**Pattern**: `ServerCertificateCustomValidationCallback.*true`
**Type**: regex
**Severity**: critical
**Languages**: [csharp]
- HttpClient certificate validation disabled

### CSharp SSLv3 Protocol
**Pattern**: `SecurityProtocolType\.Ssl3`
**Type**: regex
**Severity**: critical
**Languages**: [csharp]
- SSLv3 in .NET
- CWE-757: Selection of Less-Secure Algorithm

### CSharp TLS 1.0 Only
**Pattern**: `SecurityProtocolType\.Tls\b`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- TLS 1.0 only in .NET

---

## Configuration Patterns

### Self-Signed Certificate Bypass
**Pattern**: `(?:self.signed|selfsigned|self_signed)\s*[=:]\s*(?:true|True|1)`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Explicitly allowing self-signed certificates

### Certificate Pinning Disabled
**Pattern**: `(?:pinning|PINNING|pin)\s*[=:]\s*(?:false|False|0|disabled|none)`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Certificate pinning explicitly disabled

### Trust All Certificates Comment
**Pattern**: `(?:trust|accept)\s*all\s*(?:cert|certificate)`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Code comment indicating trust-all behavior

---

## Environment Variables

Insecure environment variables to detect:

| Variable | Risk |
|----------|------|
| `NODE_TLS_REJECT_UNAUTHORIZED=0` | Disables all TLS verification in Node.js |
| `PYTHONHTTPSVERIFY=0` | Disables HTTPS verification in Python |
| `CURL_CA_BUNDLE=""` | Empty CA bundle in cURL |
| `REQUESTS_CA_BUNDLE=""` | Empty CA bundle in requests |

---

## Best Practices

### Minimum TLS Version
- Use TLS 1.2 minimum, TLS 1.3 preferred
- Disable SSLv2, SSLv3, TLS 1.0, TLS 1.1

### Certificate Validation
- Always verify server certificates
- Always verify hostnames
- Use system CA store or explicit trusted CAs
- Consider certificate pinning for sensitive applications

### Cipher Suites
- Use strong cipher suites (AEAD modes)
- Disable weak ciphers (RC4, DES, 3DES, export ciphers)

---

## References

- [CWE-295: Improper Certificate Validation](https://cwe.mitre.org/data/definitions/295.html)
- [CWE-757: Selection of Less-Secure Algorithm](https://cwe.mitre.org/data/definitions/757.html)
- [SSL Labs Best Practices](https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices)
