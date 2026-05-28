# A03 Software Supply Chain Failures

## Background

Software Supply Chain Failures ranked **#1 with 50% of respondents selecting it as top risk** in the community survey. Evolved from "A9 – Using Components with Known Vulnerabilities" in 2013, the scope has been expanded to include all types of supply chain compromises.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 6 |
| Max Incidence Rate | 9.56% |
| Avg Incidence Rate | 5.72% |
| Total Occurrences | 215,248 |
| Total CVEs | 11 |

### Key Characteristics
- Highest incidence rate at **5.19% average** during testing
- Despite broader scope, only 11 CVEs mapped to related CWEs

## Description

**"Software supply chain failures are breakdowns or other compromises in the process of building, deploying, or updating software."**

### Vulnerability Conditions

Organizations become vulnerable when:

1. **Failure to Track Component Versions**: Not comprehensively tracking component versions including direct and transitive dependencies
2. **Deploying Outdated Software**: Deploying unsupported or outdated software (OS, servers, databases, libraries, runtimes)
3. **Lack of Regular Vulnerability Scanning**: Lack of regular vulnerability scanning or security bulletin subscriptions
4. **Lack of Change Management Documentation**: Lack of change management documentation for CI/CD, repositories, IDEs, artifact stores
5. **Insufficient Access Control**: Insufficient access control and permission restrictions across the supply chain
6. **Missing Separation of Duties**: Missing separation of duties in code promotion workflows
7. **Untrusted Source Components**: Using untrusted source components in production environments
8. **Delayed Patches**: Delayed patches due to infrequent change control cycles (monthly/quarterly)
9. **Skipped Compatibility Testing**: Skipped compatibility testing for library updates
10. **Weak CI/CD Security**: Weak CI/CD security compared to production systems

## How to Prevent

### Patch Management Process

1. **Centralized SBOM Generation**: Generate centralized Software Bill of Materials (SBOM)
2. **Comprehensive Transitive Dependency Tracking**: Comprehensive tracking including transitive dependencies
3. **Remove Unused Components**: Reduce attack surface by removing unused components
4. **Continuous Version Inventory**: Continuous inventory of client/server component versions using tools like OWASP Dependency Track, OWASP Dependency Check, retire.js
5. **Monitor Vulnerability Databases**: Monitor CVE, NVD, Open Source Vulnerabilities (OSV) databases
6. **Source Components Only from Official Trusted Sources**: Source components only from official trusted sources through secure links
7. **Prefer Signed Packages**: Prefer signed packages to prevent malicious modifications
8. **Intentional Dependency Version Management**: Upgrade only when necessary
9. **Monitor Unmaintained Libraries**: Monitor unmaintained libraries; consider virtual patching as alternative
10. **Regularly Update CI/CD and Developer Tools**
11. **Implement Staged/Canary Deployments**: Implement staged/canary deployments to limit exposure

### Change Management Tracking

Document all modifications to:
- CI/CD configurations
- Code repositories
- Sandboxes
- Developer IDEs
- SBOM tools
- Logging systems
- Third-party integrations
- Artifact repositories
- Container registries

### Hardening Requirements

- **Code Repositories**: Disable secret check-ins, branch protection, enable backups
- **Developer Workstations**: Regular patching, MFA, monitoring
- **Build Servers/CI/CD**: Enforce separation of duties, access control, signed builds, environment-scoped secrets
- **Artifacts**: Ensure integrity through provenance, signatures, timestamps; promote instead of rebuild
- **Infrastructure as Code**: Manage through PR and version control

## Example Attack Scenarios

### Scenario #1 - Vendor Compromise (SolarWinds)
The 2019 SolarWinds breach **infected approximately 18,000 organizations** when a trusted vendor distributed malware through software updates.
- Reference: [NPR Investigation](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack)

### Scenario #2 - Conditional Malware (Bybit)
The 2025 Bybit **$1.5 billion theft** originated from wallet software containing malicious code that only executed under specific conditions.
- Reference: [Sygnia Investigation](https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/)

### Scenario #3 - Self-propagating Worm (Shai-Hulud)
The 2025 Shai-Hulud npm attack used post-install scripts to spread malicious package versions that collected sensitive data and exfiltrated npm tokens to GitHub repositories, reaching **over 500 package versions** before being stopped.

### Scenario #4 - Known Vulnerability Exploitation
- **CVE-2017-5638**: Apache Struts 2 remote code execution enabling arbitrary server execution
- **CVE-2021-44228 ("Log4Shell")**: Apache Log4j zero-day enabling ransomware and cryptomining campaigns

## References

### OWASP Resources
- [OWASP ASVS: V15](https://owasp.org/www-project-application-security-verification-standard/)
- [Dependency Graph SBOM Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html)
- [Vulnerable Dependency Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)
- [OWASP Dependency-Track Project](https://owasp.org/www-project-dependency-track/)
- [OWASP CycloneDX Project](https://owasp.org/www-project-cyclonedx/)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [Virtual Patching Best Practices](https://owasp.org/www-community/Virtual_Patching_Best_Practices)

### External References
- [MITRE CVE Search](https://www.cve.org)
- [National Vulnerability Database](https://nvd.nist.gov)
- [Retire.js](https://retirejs.github.io/retire.js/)
- [GitHub Advisory Database](https://github.com/advisories)
- [SAFECode Software Integrity Controls](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-447](https://cwe.mitre.org/data/definitions/447.html) | Use of Obsolete Functions |
| [CWE-1035](https://cwe.mitre.org/data/definitions/1035.html) | 2017 Top 10 A9 - Using Components with Known Vulnerabilities |
| [CWE-1104](https://cwe.mitre.org/data/definitions/1104.html) | Use of Unmaintained Third Party Components |
| [CWE-1329](https://cwe.mitre.org/data/definitions/1329.html) | Reliance on Component That is Not Updateable |
| [CWE-1357](https://cwe.mitre.org/data/definitions/1357.html) | Reliance on Insufficiently Trustworthy Component |
| [CWE-1395](https://cwe.mitre.org/data/definitions/1395.html) | Dependency on Vulnerable Third-Party Component |
