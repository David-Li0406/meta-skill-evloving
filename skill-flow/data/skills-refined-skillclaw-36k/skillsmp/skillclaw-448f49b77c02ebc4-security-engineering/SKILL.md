---
name: security-engineering
description: Use this skill when auditing code for security issues, reviewing authentication/authorization, evaluating input validation, analyzing cryptographic usage, or reviewing dependency security.
---

# Skill body

## When to Use

- Security audits and code reviews
- Authentication/authorization review
- Input validation and sanitization checks
- Cryptographic implementation review
- Dependency and supply chain security
- Threat modeling for new features

**NOT for:** performance optimization, general code review, feature implementation

## Phases

Track with a task management tool. Each phase feeds the next.

| Phase              | Trigger          | activeForm                     |
|--------------------|------------------|--------------------------------|
| Threat Model       | Session start     | "Building threat model"        |
| Attack Surface     | Model complete    | "Mapping attack surface"       |
| Vulnerability Scan  | Surface mapped    | "Scanning for vulnerabilities" |
| Risk Assessment     | Vulns identified  | "Assessing risk levels"        |
| Remediation Plan    | Risks assessed    | "Planning remediation"         |

**Critical findings:** add urgent remediation task immediately.

## Severity Levels

CVSS-aligned severity for findings:

| Indicator  | Severity | CVSS | Examples                                         |
|------------|----------|------|--------------------------------------------------|
| **Critical** | 9.0-10.0 | RCE, auth bypass, mass data exposure, admin privesc |
| **High**     | 7.0-8.9  | SQLi, stored XSS, auth weakness, sensitive data leak |
| **Medium**   | 4.0-6.9  | CSRF, reflected XSS, info disclosure, weak crypto |
| **Low**      | 0.1-3.9  | Misconfig, missing headers, verbose errors      |

**Format:** "**Critical** RCE via unsanitized shell command"

## Threat Modeling

### STRIDE Framework

Systematic threat identification by category:

| Threat            | Question                          | Check                                         |
|-------------------|-----------------------------------|----------------------------------------------|
| **S**poofing      | Can attacker impersonate?        | Auth mechanisms, tokens, sessions, API keys  |
| **T**ampering     | Can attacker modify data?        | Input validation, integrity checks, DB access |
| **R**epudiation    | Can actions be denied?           | Audit logs, signatures, timestamps           |
| **I**nfo Disclosure | Can attacker access secrets?    | Encryption, access control, logging          |
| **D**enial of Service | Can attacker disrupt?        | Rate limits, timeouts, input size           |
| **E**levation     | Can attacker gain access?        | Authz checks, RBAC, least privilege          |