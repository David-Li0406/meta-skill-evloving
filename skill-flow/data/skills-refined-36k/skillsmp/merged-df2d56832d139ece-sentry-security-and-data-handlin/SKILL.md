---
name: sentry-security-and-data-handling
description: Use this skill when configuring security settings and managing sensitive data in Sentry, including PII scrubbing and compliance with regulations like GDPR.
---

# Sentry Security and Data Handling

## Prerequisites

- Security and compliance requirements documented (GDPR, HIPAA, SOC 2, PCI-DSS)
- Sensitive data patterns known
- Access control needs defined
- Sentry project with admin access

## Instructions

1. Enable server-side data scrubbing in project settings.
2. Configure client-side scrubbing in the `beforeSend` hook for user data and request bodies.
3. Add sensitive field patterns for passwords, tokens, credit cards, SSNs, and email addresses.
4. Store DSN in environment variables; never hardcode.
5. Set `sendDefaultPii` to false in SDK configuration.
6. Configure IP address anonymization or disable IP collection.
7. Set appropriate data retention period in organization settings.
8. Implement user consent handling for GDPR compliance.
9. Create API tokens with minimal required scopes and rotate DSN keys after deployment.
10. Enable audit logging for compliance tracking.
11. Document the right to erasure process with API deletion endpoint.
12. Complete security and compliance checklists and document compliance status.

## Output
- Data scrubbing and PII handling configured.
- DSN secured in environment variables.
- Access controls and data retention policies implemented.
- Security and compliance checklists completed.

## Error Handling

See `{baseDir}/references/errors.md` for comprehensive error handling.

## Examples

See `{baseDir}/references/examples.md` for detailed examples.

## Resources
- [Sentry Security](https://docs.sentry.io/product/security/)
- [Sentry Data Privacy](https://docs.sentry.io/product/data-management-settings/data-privacy/)
- [GDPR Compliance](https://sentry.io/legal/gdpr/)
- [Data Scrubbing](https://docs.sentry.io/product/data-management-settings/scrubbing/)