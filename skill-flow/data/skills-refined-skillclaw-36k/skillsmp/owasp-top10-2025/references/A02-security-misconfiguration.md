# A02 Security Misconfiguration

## Background

Security Misconfiguration has risen from **5th to 2nd** place in OWASP Top 10:2025. Some form of misconfiguration was discovered in **100%** of tested applications.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 16 |
| Max Incidence Rate | 27.70% |
| Avg Incidence Rate | 3.00% |
| Max Coverage | 100% |
| Avg Coverage | 52.35% |
| Total Occurrences | 719,084 |
| Total CVEs | 1,375 |

### Key Related Vulnerabilities
- CWE-16: Configuration
- CWE-611: Improper Restriction of XML External Entity Reference

## Description

Security misconfiguration represents improper configuration of systems, applications, or cloud services. Without a repeatable application security hardening process, systems are exposed to higher risk.

### Vulnerability Indicators

1. **Missing Security Hardening**: Missing security hardening across the application stack
2. **Cloud Service Permission Errors**: Improperly configured cloud service permissions
3. **Unnecessary Features Enabled**: Unnecessary ports, services, testing frameworks enabled
4. **Default Accounts/Passwords**: Default accounts and passwords still enabled and unchanged
5. **Improper Error Message Filtering**: Improper error message filtering that exposes stack traces
6. **Disabled Security Features on Upgrade**: Security features disabled in upgraded systems
7. **Insecure Settings in Servers/Frameworks/Libraries**: Insecure settings in servers, frameworks, libraries, databases
8. **Missing or Insecure Security Headers**: Missing or insecure security header settings

## How to Prevent

### Hardening Process
1. **Repeatable Hardening Procedures**: Implement repeatable hardening procedures for fast and secure environment deployment
2. **Identical Settings Across Environments**: Maintain identical settings with environment-specific credentials across development, QA, and production
3. **Configuration Automation**: Automate configuration to minimize manual work

### Minimization
4. **Minimal Platform Deployment**: Deploy minimal platform without unnecessary features or components
5. **Remove Unused Frameworks and Documentation**: Remove unused frameworks and documentation

### Patch Management
6. **Review and Update All Security Notes, Updates, Patches**
7. **Audit Cloud Storage Permissions**: Audit cloud storage permissions such as S3 buckets

### Architecture and Security
8. **Segmented Architecture**: Implement segmented architecture with containerization or cloud security groups
9. **Send Security Directives via Security Headers**: Send security directives to clients via security headers
10. **Use Identity Federation and Short-lived Credentials**: Use identity federation and short-lived credentials instead of embedded static keys

### Verification
11. **Automated Configuration Effectiveness Verification**: Automatically verify configuration effectiveness across all environments
12. **Centralized Error Message Blocking**: Implement centralized error message blocking
13. **Annual Manual Verification Minimum**: Minimum annual manual verification when automation is not possible

## Example Attack Scenarios

### Scenario #1: Unremoved Sample Applications
Sample applications with known vulnerabilities remain on production server. Attackers can exploit especially the admin console with unchanged default credentials to gain complete server control.

### Scenario #2: Directory Listing Enabled
```
Attacker discovers that directories can simply be listed.
Attacker finds compiled Java classes, downloads them,
decompiles and reverse engineers to view the code.
```
This exposure leads to discovering access control flaws.

### Scenario #3: Detailed Error Messages
```
Application server configuration allows detailed error messages
such as stack traces to be returned to users.
```
This exposes sensitive component versions and underlying vulnerabilities.

### Scenario #4: Cloud Storage Exposure
```
Cloud service provider (CSP) leaves sharing permissions
open to the internet by default. This allows access to
sensitive data stored in cloud storage.
```

## References

- [OWASP Testing Guide: Configuration Management](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/)
- [OWASP Testing Guide: Testing for Error Codes](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/)
- [OWASP ASVS V13 Configuration](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST General Server Hardening Guide (SP 800-123)](https://csrc.nist.gov/publications/detail/sp/800-123/final)
- [CIS Security Configuration Guides/Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [Amazon S3 Bucket Discovery and Enumeration](https://aws.amazon.com/blogs/security/how-to-use-bucket-policies-and-apply-defense-in-depth-to-help-secure-your-amazon-s3-data/)

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-5](https://cwe.mitre.org/data/definitions/5.html) | J2EE Misconfiguration: Data Transmission Without Encryption |
| [CWE-11](https://cwe.mitre.org/data/definitions/11.html) | ASP.NET Misconfiguration: Creating Debug Binary |
| [CWE-13](https://cwe.mitre.org/data/definitions/13.html) | ASP.NET Misconfiguration: Password in Configuration File |
| [CWE-15](https://cwe.mitre.org/data/definitions/15.html) | External Control of System or Configuration Setting |
| [CWE-16](https://cwe.mitre.org/data/definitions/16.html) | Configuration |
| [CWE-260](https://cwe.mitre.org/data/definitions/260.html) | Password in Configuration File |
| [CWE-315](https://cwe.mitre.org/data/definitions/315.html) | Cleartext Storage of Sensitive Information in Cookie |
| [CWE-489](https://cwe.mitre.org/data/definitions/489.html) | Active Debug Code |
| [CWE-526](https://cwe.mitre.org/data/definitions/526.html) | Sensitive Information Exposure Through Environment Variables |
| [CWE-547](https://cwe.mitre.org/data/definitions/547.html) | Use of Hardcoded Security-relevant Constants |
| [CWE-611](https://cwe.mitre.org/data/definitions/611.html) | Improper Restriction of XML External Entity Reference |
| [CWE-614](https://cwe.mitre.org/data/definitions/614.html) | Sensitive Cookie in HTTPS Session Without 'Secure' Attribute |
| [CWE-776](https://cwe.mitre.org/data/definitions/776.html) | Improper Restriction of Recursive Entity References in DTDs |
| [CWE-942](https://cwe.mitre.org/data/definitions/942.html) | Permissive Cross-domain Policy with Untrusted Domains |
| [CWE-1004](https://cwe.mitre.org/data/definitions/1004.html) | Sensitive Cookie Without 'HttpOnly' Flag |
| [CWE-1174](https://cwe.mitre.org/data/definitions/1174.html) | ASP.NET Misconfiguration: Improper Model Validation |
