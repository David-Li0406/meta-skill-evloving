<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# OWASP Top 10 - 2021 Edition

**Category**: code-security/standards/owasp
**Description**: Reference guide for OWASP Top 10 web application security risks
**CWE**: CWE-284, CWE-327, CWE-89, CWE-209, CWE-16, CWE-1104, CWE-287, CWE-502, CWE-778, CWE-918

---

## A01:2021 - Broken Access Control

**Moved up from #5. 94% of applications tested for some form of broken access control.**

### Description
Access control enforces policy such that users cannot act outside of their intended permissions.

### Common Vulnerabilities
- Bypassing access control checks by modifying the URL
- Allowing viewing or editing someone else's account
- Accessing API without access controls for POST, PUT, DELETE
- Elevation of privilege (acting as admin when logged in as user)
- Metadata manipulation (JWT, cookies, hidden fields)
- CORS misconfiguration allowing unauthorized API access
- Force browsing to authenticated/privileged pages

### CWEs Mapped
- CWE-200: Exposure of Sensitive Information
- CWE-201: Insertion of Sensitive Information Into Sent Data
- CWE-352: Cross-Site Request Forgery (CSRF)
- CWE-284: Improper Access Control
- CWE-285: Improper Authorization
- CWE-639: Authorization Bypass Through User-Controlled Key

---

## A02:2021 - Cryptographic Failures

**Previously "Sensitive Data Exposure." Focus on failures related to cryptography.**

### Description
Determine the protection needs of data in transit and at rest. Use strong algorithms, protocols, and keys.

### Common Vulnerabilities
- Data transmitted in clear text (HTTP, SMTP, FTP)
- Old or weak cryptographic algorithms (MD5, SHA1, DES)
- Default crypto keys or weak key generation
- Not enforcing encryption (missing HSTS)
- Certificate validation not performed
- Passwords stored without strong adaptive functions (bcrypt, argon2)

### CWEs Mapped
- CWE-259: Use of Hard-coded Password
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm
- CWE-331: Insufficient Entropy
- CWE-321: Use of Hard-coded Cryptographic Key
- CWE-798: Use of Hard-coded Credentials

---

## A03:2021 - Injection

**Drops to #3. 94% of applications tested for some form of injection.**

### Description
Hostile data sent to an interpreter as part of a command or query.

### Common Vulnerabilities
- User-supplied data not validated, filtered, or sanitized
- Dynamic queries without parameterization
- Hostile data used in ORM search parameters
- Hostile data directly used or concatenated

### Types
- SQL Injection
- NoSQL Injection
- OS Command Injection
- LDAP Injection
- Expression Language Injection
- Object Graph Navigation Library (OGNL) Injection

### CWEs Mapped
- CWE-79: Cross-site Scripting (XSS)
- CWE-89: SQL Injection
- CWE-73: External Control of File Name or Path
- CWE-77: Command Injection
- CWE-78: OS Command Injection

---

## A04:2021 - Insecure Design

**New category for 2021. Focus on design and architectural flaws.**

### Description
Risks related to design flaws. Distinguish from implementation bugs.

### Common Vulnerabilities
- Missing or ineffective control design
- Business logic flaws
- Insufficient threat modeling
- Missing security requirements
- No secure development lifecycle

### Prevention
- Establish secure development lifecycle with AppSec professionals
- Use secure design patterns library
- Threat modeling for authentication, access control, business logic
- Write unit and integration tests for security controls

### CWEs Mapped
- CWE-209: Generation of Error Message Containing Sensitive Information
- CWE-256: Unprotected Storage of Credentials
- CWE-501: Trust Boundary Violation
- CWE-522: Insufficiently Protected Credentials

---

## A05:2021 - Security Misconfiguration

**Moved up from #6. 90% of applications tested for misconfiguration.**

### Description
Missing appropriate security hardening across any part of the application stack.

### Common Vulnerabilities
- Missing security hardening
- Unnecessary features enabled (ports, services, accounts)
- Default accounts and passwords unchanged
- Error handling reveals stack traces
- Security settings not set to secure values
- Missing security headers
- Software out of date or vulnerable

### CWEs Mapped
- CWE-16: Configuration
- CWE-611: Improper Restriction of XML External Entity Reference
- CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag
- CWE-942: Permissive Cross-domain Policy with Untrusted Domains

---

## A06:2021 - Vulnerable and Outdated Components

**Previously "Using Components with Known Vulnerabilities." Community survey #2.**

### Description
Using components (libraries, frameworks, software modules) with known vulnerabilities.

### Common Vulnerabilities
- Unknown versions of components (client and server-side)
- Vulnerable, unsupported, or out of date software
- Not scanning for vulnerabilities regularly
- Not fixing or upgrading underlying platform
- Not testing compatibility of updated libraries
- Not securing component configurations

### CWEs Mapped
- CWE-1104: Use of Unmaintained Third Party Components

---

## A07:2021 - Identification and Authentication Failures

**Previously "Broken Authentication." Drops from #2.**

### Description
Confirmation of the user's identity, authentication, and session management.

### Common Vulnerabilities
- Permits automated attacks (credential stuffing, brute force)
- Permits weak passwords
- Weak credential recovery processes
- Plain text or weakly hashed passwords
- Missing or ineffective MFA
- Exposes session identifier in URL
- Reuses session identifier after login
- Does not properly invalidate sessions

### CWEs Mapped
- CWE-287: Improper Authentication
- CWE-384: Session Fixation
- CWE-256: Unprotected Storage of Credentials
- CWE-304: Missing Critical Step in Authentication
- CWE-306: Missing Authentication for Critical Function

---

## A08:2021 - Software and Data Integrity Failures

**New category. Relates to code and infrastructure that does not protect against integrity violations.**

### Description
Code and infrastructure that does not protect against integrity violations.

### Common Vulnerabilities
- Using libraries from untrusted sources
- Insecure CI/CD pipeline
- Auto-update without integrity verification
- Insecure deserialization
- Unsigned or unencrypted serialized data sent to untrusted clients

### CWEs Mapped
- CWE-829: Inclusion of Functionality from Untrusted Control Sphere
- CWE-494: Download of Code Without Integrity Check
- CWE-502: Deserialization of Untrusted Data
- CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes

---

## A09:2021 - Security Logging and Monitoring Failures

**Previously "Insufficient Logging & Monitoring." Added from community survey.**

### Description
Without logging and monitoring, breaches cannot be detected.

### Common Vulnerabilities
- Auditable events not logged
- Warnings and errors generate no log messages
- Logs not monitored for suspicious activity
- Logs only stored locally
- Alerting thresholds not in place
- Penetration testing and DAST scans don't trigger alerts
- Application cannot detect or alert on active attacks in real-time

### CWEs Mapped
- CWE-778: Insufficient Logging
- CWE-117: Improper Output Neutralization for Logs
- CWE-223: Omission of Security-relevant Information
- CWE-532: Insertion of Sensitive Information into Log File

---

## A10:2021 - Server-Side Request Forgery (SSRF)

**New addition for 2021. Added from community survey #1.**

### Description
SSRF flaws occur when a web application fetches a remote resource without validating the user-supplied URL.

### Common Vulnerabilities
- Fetching remote resources without URL validation
- Attackers can reach internal services behind firewalls
- Access to metadata services (cloud environments)
- Port scanning internal servers
- Reading local files

### CWEs Mapped
- CWE-918: Server-Side Request Forgery (SSRF)

---

## Reference

- [OWASP Top 10 - 2021](https://owasp.org/Top10/)
- [OWASP Top 10 Mapping to CWE](https://owasp.org/Top10/A01_2021-Broken_Access_Control/#mapped-cwes)
