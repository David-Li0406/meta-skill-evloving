# A01 Broken Access Control

## Background

Broken Access Control maintains **#1** position in OWASP Top 10:2025. Some form of access control failure was discovered in **100%** of tested applications.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 40 |
| Max Incidence Rate | 20.15% |
| Avg Incidence Rate | 3.74% |
| Max Coverage | 100% |
| Avg Coverage | 42.93% |
| Total Occurrences | 1,839,701 |
| Total CVEs | 32,654 |

### Key Related Vulnerabilities
- CWE-200: Exposure of Sensitive Information
- CWE-201: Information Exposure Through Sent Data
- CWE-918: Server-Side Request Forgery (SSRF)
- CWE-352: Cross-Site Request Forgery (CSRF)

## Description

Access control enforces policies such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized data disclosure, modification, destruction, or execution of unauthorized business functions.

### Common Vulnerability Types

1. **Violation of Least Privilege Principle**: Granting access to anyone instead of specific capabilities, roles, or users
2. **Access Control Bypass**: Bypassing checks through URL, application state, HTML, or API request modification
3. **Insecure Direct Object References (IDOR)**: Accessing another user's account through unique identifiers
4. **Missing API Access Control**: Insufficient restrictions on POST, PUT, DELETE operations
5. **Privilege Escalation**: Unauthorized access without login or exceeding permitted privilege levels
6. **Metadata Manipulation**: JWT tampering, cookie abuse, or token misuse
7. **CORS Misconfiguration**: API access from unauthorized origins
8. **Forced Browsing**: Accessing authenticated or privileged pages through URL guessing

## How to Prevent

1. **Default Deny Principle**: Enforce "default deny" policy unless resource is public
2. **Centralized Access Control**: Implement centralized access control mechanisms with minimal CORS usage
3. **Record Ownership Model**: Use record ownership model instead of allowing unrestricted data operations
4. **Business Constraint Requirements**: Enforce business constraint requirements through domain models
5. **Disable Web Server Directory Listing**: Remove metadata and backup files from web root
6. **Log Access Failures**: Log access failures and alert administrators appropriately
7. **Rate Limiting**: Implement rate limiting on APIs to mitigate automated attacks
8. **Session Identifier Invalidation**: Invalidate server-side session identifiers on logout; use short-lived JWT tokens
9. **Declarative Access Control Tools**: Deploy established toolkits that provide declarative access control
10. **Functional Access Control Testing**: Include functional access control tests in unit and integration tests

## Example Attack Scenarios

### Scenario #1 - Unvalidated SQL Parameter
```java
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery();
```
Attacker modifies browser parameter:
```
https://example.com/app/accountInfo?acct=notmyacct
```
Without proper validation, unauthorized account access is possible.

### Scenario #2 - Forced Browsing
```
https://example.com/app/admin_getappInfo
```
Admin access page is exposed to unauthenticated users or non-admins through direct URL access.

### Scenario #3 - Frontend-Only Access Control
Despite JavaScript restrictions, attacker bypasses protection with direct curl command:
```bash
$ curl https://example.com/app/admin_getappInfo
```

## References

- [OWASP Proactive Controls: C1 - Implement Access Control](https://owasp.org/www-project-proactive-controls/)
- [OWASP ASVS: V8 Authorization](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Testing Guide: Authorization Testing](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [PortSwigger: Exploiting CORS Misconfiguration](https://portswigger.net/web-security/cors)
- [OAuth 2.0: Access Revocation Standard](https://oauth.net/2/)

## List of Mapped CWEs

### Path Traversal and File Access
- [CWE-22](https://cwe.mitre.org/data/definitions/22.html): Path Traversal
- [CWE-23](https://cwe.mitre.org/data/definitions/23.html): Relative Path Traversal
- [CWE-36](https://cwe.mitre.org/data/definitions/36.html): Absolute Path Traversal
- [CWE-59](https://cwe.mitre.org/data/definitions/59.html): Link Following
- [CWE-61](https://cwe.mitre.org/data/definitions/61.html): UNIX Symbolic Link
- [CWE-65](https://cwe.mitre.org/data/definitions/65.html): Windows Hard Link

### Information Exposure
- [CWE-200](https://cwe.mitre.org/data/definitions/200.html): Exposure of Sensitive Information
- [CWE-201](https://cwe.mitre.org/data/definitions/201.html): Information Exposure Through Sent Data
- [CWE-219](https://cwe.mitre.org/data/definitions/219.html): Storage of Sensitive Data Under Web Root
- [CWE-359](https://cwe.mitre.org/data/definitions/359.html): Privacy Violation
- [CWE-497](https://cwe.mitre.org/data/definitions/497.html): Exposure of System Data to Unauthorized Client
- [CWE-538](https://cwe.mitre.org/data/definitions/538.html): File and Directory Information Exposure
- [CWE-540](https://cwe.mitre.org/data/definitions/540.html): Inclusion of Sensitive Information in Source Code
- [CWE-548](https://cwe.mitre.org/data/definitions/548.html): Information Exposure Through Directory Listing
- [CWE-552](https://cwe.mitre.org/data/definitions/552.html): Externally Accessible Files/Directories
- [CWE-615](https://cwe.mitre.org/data/definitions/615.html): Inclusion of Sensitive Information in Comments
- [CWE-668](https://cwe.mitre.org/data/definitions/668.html): Exposure of Resource to Wrong Sphere
- [CWE-922](https://cwe.mitre.org/data/definitions/922.html): Insecure Storage of Sensitive Information

### Permissions and Ownership
- [CWE-276](https://cwe.mitre.org/data/definitions/276.html): Incorrect Default Permissions
- [CWE-281](https://cwe.mitre.org/data/definitions/281.html): Improper Preservation of Permissions
- [CWE-282](https://cwe.mitre.org/data/definitions/282.html): Improper Ownership Management
- [CWE-283](https://cwe.mitre.org/data/definitions/283.html): Unverified Ownership

### Access Control and Authorization
- [CWE-284](https://cwe.mitre.org/data/definitions/284.html): Improper Access Control
- [CWE-285](https://cwe.mitre.org/data/definitions/285.html): Improper Authorization
- [CWE-352](https://cwe.mitre.org/data/definitions/352.html): Cross-Site Request Forgery (CSRF)
- [CWE-425](https://cwe.mitre.org/data/definitions/425.html): Direct Request (Forced Browsing)
- [CWE-441](https://cwe.mitre.org/data/definitions/441.html): Unintended Proxy/Intermediary
- [CWE-566](https://cwe.mitre.org/data/definitions/566.html): Authorization Bypass Through User-Controlled SQL Primary Key
- [CWE-601](https://cwe.mitre.org/data/definitions/601.html): URL Redirection to Untrusted Site
- [CWE-639](https://cwe.mitre.org/data/definitions/639.html): Authorization Bypass Through User-Controlled Key
- [CWE-749](https://cwe.mitre.org/data/definitions/749.html): Exposed Dangerous Method/Function
- [CWE-862](https://cwe.mitre.org/data/definitions/862.html): Missing Authorization
- [CWE-863](https://cwe.mitre.org/data/definitions/863.html): Incorrect Authorization
- [CWE-918](https://cwe.mitre.org/data/definitions/918.html): Server-Side Request Forgery (SSRF)

### Resource Security
- [CWE-377](https://cwe.mitre.org/data/definitions/377.html): Insecure Temporary File
- [CWE-379](https://cwe.mitre.org/data/definitions/379.html): Creation of Temp File With Improper Permissions
- [CWE-402](https://cwe.mitre.org/data/definitions/402.html): Transmission of Private Resources into New Sphere
- [CWE-424](https://cwe.mitre.org/data/definitions/424.html): Improper Protection of Trust Boundary
- [CWE-732](https://cwe.mitre.org/data/definitions/732.html): Incorrect Permission Assignment for Critical Resource
- [CWE-1275](https://cwe.mitre.org/data/definitions/1275.html): Sensitive Cookie with Improper SameSite Attribute
