---
name: gh-actions-validator
description: Use this skill when you need to validate and enforce best practices for GitHub Actions workflows deploying to Google Cloud and Vertex AI, ensuring secure CI/CD pipelines with Workload Identity Federation.
---

# Skill body

## Overview

This skill validates and hardens GitHub Actions workflows for deployments to Google Cloud, particularly for Vertex AI, using Workload Identity Federation (OIDC) instead of long-lived service account keys. It helps audit existing workflows, propose secure replacements, and add CI checks to prevent common credential and permission mistakes.

## Prerequisites

Before using this skill, ensure:
- GitHub repository with Actions enabled
- Google Cloud project with billing enabled
- gcloud CLI authenticated with admin permissions
- Understanding of Workload Identity Federation concepts
- GitHub repository secrets configured
- Appropriate IAM roles for CI/CD automation

## Instructions

1. **Audit Existing Workflows**: Scan `.github/workflows/` for security issues.
2. **Validate WIF Usage**: Ensure no JSON service account keys are used.
3. **Check OIDC Permissions**: Verify `id-token: write` is present in permissions.
4. **Review IAM Roles**: Confirm least privilege (avoid owner/editor roles).
5. **Add Security Scans**: Include secret detection and vulnerability scanning.
6. **Validate Deployments**: Implement post-deployment health checks.
7. **Configure Monitoring**: Set up alerts for deployment failures.
8. **Document WIF Setup**: Provide one-time WIF configuration commands.

## Output

Example GitHub Actions configuration:
```yaml
- uses: actions/checkout@v4
- name: Authenticate to GCP (WIF)
- name: Deploy to Vertex AI
      --project=${{ secrets.GCP_PROJECT_ID }} \
      --region=us-central1
- name: Validate Deployment
```

## Error Handling

Refer to the error handling documentation for comprehensive guidance.

## Examples

See the examples section for detailed use cases.

## Resources

- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening)