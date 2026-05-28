---
name: owasp-top10-2025
description: OWASP Top 10:2025 web security vulnerability guide. A skill referenced by security specialist subagents during code review, security audits, and vulnerability analysis. Provides background, explanation, prevention methods, attack scenarios, and related CWE information for the 10 major web security threats from A01 Broken Access Control to A10 Mishandling of Exceptional Conditions.
model: opus
allowed-tools:
  - Read
  - Glob
  - Grep
---

# OWASP Top 10:2025 Web Security Guide

## Overview

This skill provides comprehensive guidance on **OWASP Top 10:2025** web application security risks. It can be utilized by security specialist subagents during code review, security audits, and vulnerability analysis.

## When to Use

- When performing security code reviews
- When analyzing and assessing security vulnerabilities
- When defining security requirements
- When conducting developer security training
- When planning penetration tests

## OWASP Top 10:2025 Summary

| Rank | Category | Description | Details |
|------|----------|-------------|---------|
| **A01** | Broken Access Control | Unauthorized data access, modification, deletion due to access control failures | [View Details](./references/A01-broken-access-control.md) |
| **A02** | Security Misconfiguration | Security configuration errors in systems, applications, cloud services | [View Details](./references/A02-security-misconfiguration.md) |
| **A03** | Software Supply Chain Failures | Supply chain compromises in software build, deployment, update processes | [View Details](./references/A03-software-supply-chain-failures.md) |
| **A04** | Cryptographic Failures | Missing encryption, weak encryption, key leakage, and other cryptographic failures | [View Details](./references/A04-cryptographic-failures.md) |
| **A05** | Injection | Injection attacks including SQL, NoSQL, OS commands, LDAP | [View Details](./references/A05-injection.md) |
| **A06** | Insecure Design | Security flaws at the design and architecture level | [View Details](./references/A06-insecure-design.md) |
| **A07** | Authentication Failures | Authentication mechanism weaknesses and session management failures | [View Details](./references/A07-authentication-failures.md) |
| **A08** | Software or Data Integrity Failures | Software/data integrity verification failures | [View Details](./references/A08-software-data-integrity-failures.md) |
| **A09** | Security Logging & Alerting Failures | Missing security logging, monitoring, and alerting mechanisms | [View Details](./references/A09-security-logging-alerting-failures.md) |
| **A10** | Mishandling of Exceptional Conditions | Improper handling of exceptional conditions (New in 2025) | [View Details](./references/A10-mishandling-exceptional-conditions.md) |

## Category Key Summaries

### A01: Broken Access Control
- **Occurrence rate**: Found in 100% of tested applications
- **Key threats**: IDOR, privilege escalation, CORS errors, forced browsing
- **Core prevention**: Default deny principle, centralized access control, record ownership model

### A02: Security Misconfiguration
- **Moved from 5th to 2nd place**
- **Key threats**: Default accounts/passwords, unnecessary features enabled, stack trace exposure
- **Core prevention**: Repeatable hardening procedures, minimal platform deployment, automated verification

### A03: Software Supply Chain Failures
- **#1 in community survey**
- **Key threats**: Component vulnerabilities, CI/CD compromises, malicious packages
- **Core prevention**: SBOM generation, dependency tracking, signed package usage

### A04: Cryptographic Failures
- **Key threats**: Weak encryption, key leakage, hardcoded keys, plaintext transmission
- **Core prevention**: TLS 1.2+, strong hashing (Argon2/scrypt), HSM usage

### A05: Injection
- **Dropped from 3rd to 5th place**
- **Key threats**: SQL, XSS, OS command, LDAP injection
- **Core prevention**: Parameterized queries, input validation, context-aware escaping

### A06: Insecure Design
- **Key threats**: Missing security requirements, no threat modeling, business logic flaws
- **Core prevention**: Secure development lifecycle, threat modeling, design pattern library

### A07: Authentication Failures
- **Key threats**: Credential stuffing, weak passwords, missing MFA, session fixation
- **Core prevention**: MFA implementation, NIST 800-63b compliance, secure session management

### A08: Software or Data Integrity Failures
- **Key threats**: Unsigned updates, insecure deserialization, untrusted sources
- **Core prevention**: Digital signatures, integrity checks, trusted repositories

### A09: Security Logging & Alerting Failures
- **Key threats**: Insufficient logging, missing monitoring, log tampering, delayed breach detection
- **Core prevention**: Auditable event logging, real-time monitoring, SIEM adoption

### A10: Mishandling of Exceptional Conditions
- **New category in 2025**
- **Key threats**: Information disclosure via error messages, resource exhaustion, incomplete transactions
- **Core prevention**: Global exception handlers, complete rollbacks, rate limiting

## Usage Guide

### During Code Review
1. Identify vulnerability categories related to the code
2. Check vulnerability patterns in detailed reference documents
3. Review whether "How to Prevent" section recommendations are applied
4. Perform additional vulnerability checks based on related CWE list

### When Defining Security Requirements
1. Review all OWASP Top 10 categories
2. Transform prevention methods for each category into requirements
3. Reference related OWASP Cheat Sheets

### When Planning Penetration Tests
1. Utilize "Example Attack Scenarios" sections
2. Derive test cases for each category
3. Establish vulnerability detection scenarios based on CWE list

## References

### Official OWASP Resources
- [OWASP Top 10:2025 Official Page](https://owasp.org/Top10/2025/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP SAMM](https://owaspsamm.org/)

### CWE Database
- [MITRE CWE](https://cwe.mitre.org/)
- [NVD - National Vulnerability Database](https://nvd.nist.gov/)

### Additional Standards
- [NIST SP 800-63b](https://pages.nist.gov/800-63-3/sp800-63b.html) - Digital Identity Guidelines
- [NIST SP 800-123](https://csrc.nist.gov/publications/detail/sp/800-123/final) - Server Security Guide
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/) - Security Configuration Benchmarks

## Version Information

- **OWASP Top 10 Version**: 2025
- **Skill Creation Date**: 2026-01-19
- **Data Source**: https://owasp.org/Top10/2025/
