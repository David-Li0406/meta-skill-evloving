# A08 Software or Data Integrity Failures

## Background

This vulnerability category maintains **8th position** with a refined name that distinguishes software supply chain issues from lower-level integrity concerns. The focus is on failures in maintaining trust boundaries and integrity verification of software artifacts and data.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 14 |
| Max Incidence Rate | 8.98% |
| Avg Coverage | 45.49% |
| Total CVEs | 3,331 |

### Key Vulnerabilities
- CWE-829: Inclusion of Functionality from Untrusted Control Sphere
- CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
- CWE-502: Deserialization of Untrusted Data

## Description

This vulnerability occurs when **an application fails to protect against invalid or untrusted code/data being treated as legitimate**.

### Common Scenarios

1. **Reliance on plugins, libraries, or modules from untrusted sources**
2. **Insecure CI/CD pipelines lacking software integrity verification**
3. **Auto-update features without sufficient integrity checks**
4. **Insecure deserialization of attacker-modified objects**

> "Applications rely on plugins, libraries, or modules from untrusted sources without proper validation mechanisms."

## How to Prevent

1. **Digital Signatures**: Use digital signatures or similar mechanisms to verify software or data comes from expected sources

2. **Trusted Repositories**: Restrict library usage to verified sources; consider internal vetted repositories for high-risk profiles

3. **Code Review Process**: Implement mandatory review procedures to minimize malicious code injection

4. **CI/CD Security**: Ensure proper segregation, configuration, and access control throughout build/deployment processes

5. **Serialization Protection**: Reject unsigned or unencrypted serialized data from untrusted clients; implement integrity checks

## Example Attack Scenarios

### Scenario #1 - Untrusted Web Functionality
```
A company maps external support provider infrastructure to their own domain,
causing authentication cookies to be sent to the provider.
Compromised provider access enables session hijacking for all users.
```

### Scenario #2 - Unsigned Updates
```
Home routers and firmware lack update verification mechanisms.
Attackers distribute malicious firmware with no remediation path
until the next version release.
```

### Scenario #3 - Untrusted Package Sources
```
Developers download packages from unofficial websites
instead of trusted repositories.
Unverified packages contain malicious code without integrity verification.
```

### Scenario #4 - Insecure Deserialization
```java
// React application passing serialized user state to Spring Boot microservice
// Attacker identifies Java object signature and
// exploits deserialization for remote code execution.
```

## References

- [OWASP Software Supply Chain Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
- [OWASP Infrastructure as Code Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html)
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [SAFECode Software Integrity Controls](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)
- ["A 'Worst Nightmare' Cyberattack: The Untold Story Of The SolarWinds Hack" (NPR)](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack)
- [CodeCov Bash Uploader Compromise](https://about.codecov.io/security-update/)
- [Securing DevOps by Julien Vehent](https://www.manning.com/books/securing-devops)
- [Insecure Deserialization by Tenendo](https://www.tenendo.com/blog/insecure-deserialization)

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-345](https://cwe.mitre.org/data/definitions/345.html) | Insufficient Verification of Data Authenticity |
| [CWE-353](https://cwe.mitre.org/data/definitions/353.html) | Missing Support for Integrity Check |
| [CWE-426](https://cwe.mitre.org/data/definitions/426.html) | Untrusted Search Path |
| [CWE-427](https://cwe.mitre.org/data/definitions/427.html) | Uncontrolled Search Path Element |
| [CWE-494](https://cwe.mitre.org/data/definitions/494.html) | Download of Code Without Integrity Check |
| [CWE-502](https://cwe.mitre.org/data/definitions/502.html) | Deserialization of Untrusted Data |
| [CWE-506](https://cwe.mitre.org/data/definitions/506.html) | Embedded Malicious Code |
| [CWE-509](https://cwe.mitre.org/data/definitions/509.html) | Replicating Malicious Code (Virus or Worm) |
| [CWE-565](https://cwe.mitre.org/data/definitions/565.html) | Reliance on Cookies without Validation and Integrity Checking |
| [CWE-784](https://cwe.mitre.org/data/definitions/784.html) | Reliance on Cookies without Validation in Security Decision |
| [CWE-829](https://cwe.mitre.org/data/definitions/829.html) | Inclusion of Functionality from Untrusted Control Sphere |
| [CWE-830](https://cwe.mitre.org/data/definitions/830.html) | Inclusion of Web Functionality from an Untrusted Source |
| [CWE-915](https://cwe.mitre.org/data/definitions/915.html) | Improperly Controlled Modification of Dynamically-Determined Object Attributes |
| [CWE-926](https://cwe.mitre.org/data/definitions/926.html) | Improper Export of Android Application Components |
