# A07 Authentication Failures

## Background

Authentication Failures maintains **7th position** with a refined name and 36 mapped CWEs. Key vulnerabilities include hardcoded passwords, certificate validation failures, improper authentication, session fixation, and credential misuse.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 36 |
| Max Incidence Rate | 15.80% |
| Avg Incidence Rate | 2.92% |
| Total Occurrences | 1,120,673 |
| Total CVEs | 7,147 |

## Description

### Vulnerability Conditions

Applications are vulnerable when:

1. **Allowing Automated Attacks**: Permits credential stuffing where attackers have lists of valid usernames and passwords, or hybrid password spray variants (Password1!, Password2!, etc.)
2. **Lack of Rate Limiting**: Permits brute force or scripted attacks without rapid blocking
3. **Accepting Weak Credentials**: Allows default/weak passwords like "admin/admin" or "Password1"
4. **Allowing Compromised Credential Account Creation**: Permits signup with known compromised credentials
5. **Weak Password Recovery**: Uses ineffective processes like knowledge-based answers
6. **Poor Credential Storage**: Stores passwords in plaintext, encrypted, or weakly hashed formats
7. **Insufficient MFA**: Missing or ineffective multi-factor authentication implementation
8. **Weak MFA Fallback**: Ineffective alternatives when MFA is unavailable
9. **Insecure Session Management**: Exposes session IDs in URLs or reuses identifiers after login
10. **Improper Session Invalidation**: Fails to properly invalidate tokens on logout or inactivity
11. **Credential Scope Issues**: Fails to assert intended audience/scope of credentials

## How to Prevent

### Strengthen Authentication

1. **Implement Multi-Factor Authentication**: Implement MFA to block credential stuffing and reuse attacks
2. **Encourage Password Managers**: Encourage password managers for stronger user choices
3. **Do Not Deploy with Default Credentials**: Especially for admin accounts

### Improve Password Policy

4. **Implement Weak Password Checks**: Test new or changed passwords against top 10,000 worst passwords list
5. **Verify Against Compromised Credential Databases**: Verify new passwords against haveibeenpwned.com
6. **Follow NIST Guidelines**: Align policies with NIST 800-63b guidelines
7. **Remove Forced Rotation**: Remove forced rotation unless compromise is suspected; reset immediately if compromised

### Account Protection

8. **Harden Registration/Recovery Paths**: Harden registration/recovery paths against enumeration with consistent messaging: "Invalid username or password."
9. **Limit/Delay Failed Login Attempts**: Limit/delay while avoiding denial of service

### Session Management

10. **Use Server-Side Session Manager**: Use server-side, secure, built-in session manager that generates new random session IDs with high entropy after login
11. **Store Sessions Securely in Cookies**: Store sessions in cookies, not URLs
12. **Invalidate After Logout, Idle Timeout, and Absolute Timeout**

### Risk Transfer

13. **Leverage Established, Well-Tested Authentication Systems**: Buy rather than build yourself
14. **Validate JWT Claims**: Including `aud`, `iss`, and scopes

## Example Attack Scenarios

### Scenario #1 - Hybrid Credential Stuffing
```
Attackers adjust known passwords according to patterns
(Winter2025→Winter2026, ILoveMyDog6→ILoveMyDog7).
Without automated threat defenses, the application serves as a
"password oracle" that validates credentials
and enables unauthorized access.
```

### Scenario #2 - Multi-Factor Authentication Gap
```
"Most successful authentication attacks occur because
passwords continue to be used as the sole authentication factor."
NIST recommends abandoning rotation/complexity requirements that encourage
password reuse and instead enforcing MFA.
```

### Scenario #3 - Session Timeout Failure
```
A user closes the browser without logging out on a public computer.
Single Sign-On (SSO) systems that fail to implement proper Single Logout (SLO)
keep users authenticated across multiple services,
allowing colleagues/attackers to access unlocked systems.
```

## References

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Secure Coding Practices Quick Reference Guide](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [NIST SP 800-63b: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

## List of Mapped CWEs

### Credential and Password Issues
| CWE ID | Description |
|--------|-------------|
| [CWE-258](https://cwe.mitre.org/data/definitions/258.html) | Empty Password in Configuration File |
| [CWE-259](https://cwe.mitre.org/data/definitions/259.html) | Use of Hardcoded Password |
| [CWE-521](https://cwe.mitre.org/data/definitions/521.html) | Weak Password Requirements |
| [CWE-798](https://cwe.mitre.org/data/definitions/798.html) | Use of Hardcoded Credentials |
| [CWE-1391](https://cwe.mitre.org/data/definitions/1391.html) | Use of Weak Credentials |
| [CWE-1392](https://cwe.mitre.org/data/definitions/1392.html) | Use of Default Credentials |
| [CWE-1393](https://cwe.mitre.org/data/definitions/1393.html) | Use of Default Password |

### Authentication Bypass
| CWE ID | Description |
|--------|-------------|
| [CWE-287](https://cwe.mitre.org/data/definitions/287.html) | Improper Authentication |
| [CWE-288](https://cwe.mitre.org/data/definitions/288.html) | Authentication Bypass Using an Alternate Path or Channel |
| [CWE-289](https://cwe.mitre.org/data/definitions/289.html) | Authentication Bypass by Alternate Name |
| [CWE-290](https://cwe.mitre.org/data/definitions/290.html) | Authentication Bypass by Spoofing |
| [CWE-302](https://cwe.mitre.org/data/definitions/302.html) | Authentication Bypass by Assumed-Immutable Data |
| [CWE-305](https://cwe.mitre.org/data/definitions/305.html) | Authentication Bypass by Primary Weakness |

### Authentication Mechanisms
| CWE ID | Description |
|--------|-------------|
| [CWE-304](https://cwe.mitre.org/data/definitions/304.html) | Missing Critical Step in Authentication |
| [CWE-306](https://cwe.mitre.org/data/definitions/306.html) | Missing Authentication for Critical Function |
| [CWE-307](https://cwe.mitre.org/data/definitions/307.html) | Improper Restriction of Excessive Authentication Attempts |
| [CWE-308](https://cwe.mitre.org/data/definitions/308.html) | Use of Single-factor Authentication |
| [CWE-309](https://cwe.mitre.org/data/definitions/309.html) | Use of Password System for Primary Authentication |
| [CWE-1390](https://cwe.mitre.org/data/definitions/1390.html) | Weak Authentication |

### Certificate and Channel Validation
| CWE ID | Description |
|--------|-------------|
| [CWE-295](https://cwe.mitre.org/data/definitions/295.html) | Improper Certificate Validation |
| [CWE-297](https://cwe.mitre.org/data/definitions/297.html) | Improper Validation of Certificate with Host Mismatch |
| [CWE-298](https://cwe.mitre.org/data/definitions/298.html) | Improper Validation of Certificate Expiration |
| [CWE-299](https://cwe.mitre.org/data/definitions/299.html) | Improper Check for Certificate Revocation |
| [CWE-300](https://cwe.mitre.org/data/definitions/300.html) | Channel Accessible by Non-Endpoint |
| [CWE-346](https://cwe.mitre.org/data/definitions/346.html) | Origin Validation Error |
| [CWE-350](https://cwe.mitre.org/data/definitions/350.html) | Reliance on Reverse DNS Resolution for Security-Critical Action |
| [CWE-940](https://cwe.mitre.org/data/definitions/940.html) | Improper Verification of Source of Communication Channel |
| [CWE-941](https://cwe.mitre.org/data/definitions/941.html) | Incorrectly Specified Destination in Communication Channel |

### Session and Recovery Issues
| CWE ID | Description |
|--------|-------------|
| [CWE-291](https://cwe.mitre.org/data/definitions/291.html) | Reliance on IP Address for Authentication |
| [CWE-293](https://cwe.mitre.org/data/definitions/293.html) | Using Referer Field for Authentication |
| [CWE-294](https://cwe.mitre.org/data/definitions/294.html) | Authentication Bypass by Capture-replay |
| [CWE-303](https://cwe.mitre.org/data/definitions/303.html) | Incorrect Implementation of Authentication Algorithm |
| [CWE-384](https://cwe.mitre.org/data/definitions/384.html) | Session Fixation |
| [CWE-613](https://cwe.mitre.org/data/definitions/613.html) | Insufficient Session Expiration |
| [CWE-620](https://cwe.mitre.org/data/definitions/620.html) | Unverified Password Change |
| [CWE-640](https://cwe.mitre.org/data/definitions/640.html) | Weak Password Recovery Mechanism for Forgotten Password |
