---
name: sentry-data-security
description: Use this skill when configuring security settings and data handling in Sentry, particularly for managing sensitive data and ensuring compliance with regulations like GDPR.
---

# Sentry Data Security

## Prerequisites

- Sentry project with admin access
- Security and compliance requirements documented (GDPR, HIPAA, SOC 2, PCI-DSS)
- List of sensitive data patterns to scrub (e.g., passwords, tokens, credit cards, SSNs)
- Understanding of data retention requirements and access control needs

## Instructions

1. Enable server-side data scrubbing in Project Settings > Security & Privacy.
2. Configure client-side scrubbing in the `beforeSend` hook for user data and request bodies.
3. Add sensitive field patterns for passwords, tokens, API keys, credit cards, and email addresses.
4. Disable `sendDefaultPii` in SDK configuration.
5. Configure IP address anonymization or disable IP collection as needed.
6. Set appropriate data retention periods in organization settings.
7. Implement user consent handling for GDPR compliance, including documenting the right to erasure process with API deletion endpoints.
8. Create API tokens with minimal required scopes and configure team permissions with the principle of least privilege.
9. Rotate DSN keys and disable old ones after deployment.
10. Enable audit logging for compliance tracking.
11. Complete security and compliance checklists and document compliance status.

## Output
- Data scrubbing configured
- DSN secured in environment variables
- Access controls implemented
- Compliance documentation completed

## Error Handling

See `{baseDir}/references/errors.md` for comprehensive error handling.

## Examples

See `{baseDir}/references/examples.md` for detailed examples.

## Resources
- [Sentry Security](https://docs.sentry.io/product/security/)
- [Sentry Data Privacy](https://docs.sentry.io/product/data-management-settings/data-privacy/)
- [GDPR Compliance](https://sentry.io/legal/gdpr/)
- [Data Scrubbing](https://docs.sentry.io/product/data-management-settings/scrubbing/)