---
name: security-standards
description: Use this skill when you need to implement universal security protocols for building safe and resilient software.
---

# Security Standards - High-Density Standards

Universal security protocols for building safe and resilient software across all environments.

## **Priority: P0 (CRITICAL)**

## 🛡 Data Safeguarding

- **Zero Trust**: Never trust external input. Sanitize and validate every data boundary (API, UI, CSV).
- **Least Privilege**: Grant minimum necessary permissions to users, services, and containers.
- **No Hardcoded Secrets**: Use environment variables or secret managers. Never commit keys or passwords.
- **Encryption**: Use modern, collision-resistant algorithms (AES-256 for data-at-rest; TLS 1.3 for data-in-transit).

## 🧱 Secure Coding Practices

- **Injection Prevention**: Use parameterized queries or ORMs to stop SQL, Command, and XSS injections.
- **Dependency Management**: Regularly scan (`audit`) and update third-party libraries to patch CVEs.
- **Secure Auth**: Implement Multi-Factor Authentication (MFA) and secure session management.
- **Error Privacy**: Never leak stack traces or internal implementation details to the end-user.

## 🔍 Continuous Security

- **Shift Left**: Integrate security scanners (SAST/DAST) early in the CI/CD pipeline.
- **Data Minimization**: Collect and store only the absolute minimum data required for the business logic.
- **Logging**: Maintain audit logs for sensitive operations (Auth, Deletion, Admin changes).

## 🚫 Anti-Patterns

- **Hardcoded Secrets**: No secrets in Git; use Secret Managers or environment variables.
- **Raw SQL**: No string concatenation; use parameterized queries or ORMs.
- **Leaking Context**: No stack traces in production; return generic error codes to clients.
- **Insecure Defaults**: No default passwords; force rotation and strong entropy.

## 📚 References

- [Vulnerability Remediation & Secure Patterns](references/VULNERABILITY_REMEDIATION.md)