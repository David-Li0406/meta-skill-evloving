---
name: gh-actions-validator
description: Use this skill to validate and enforce best practices for GitHub Actions workflows deploying to Google Cloud and Vertex AI, ensuring security and compliance with Workload Identity Federation.
---

# GitHub Actions Validator

## Overview

This skill validates and hardens GitHub Actions workflows for deployments to Google Cloud, particularly for Vertex AI, using Workload Identity Federation (WIF) instead of long-lived service account keys. It audits existing workflows, proposes secure replacements, and adds CI checks to prevent common credential and permission mistakes.

## Prerequisites

Before using this skill, ensure:
- GitHub repository with Actions enabled
- Google Cloud project with billing enabled
- gcloud CLI authenticated with admin permissions
- Understanding of Workload Identity Federation concepts
- GitHub repository secrets configured
- Appropriate IAM roles for CI/CD automation

## Trigger Phrases
- "Validate GitHub Actions"
- "Setup Workload Identity Federation"
- "Deploy agent with CI/CD"
- "Automate Vertex AI deployment"
- "Create GitHub Actions workflow for Vertex AI"
- "Validate GitHub Actions security for GCP"

## Instructions

1. **Audit Existing Workflows**: Scan `.github/workflows/` for security issues.
2. **Validate WIF Usage**: Ensure no JSON service account keys are used.
3. **Check OIDC Permissions**: Verify `id-token: write` is present.
4. **Review IAM Roles**: Confirm least privilege (no owner/editor roles).
5. **Add Security Scans**: Include secret detection and vulnerability scanning.
6. **Validate Deployments**: Add post-deployment health checks.
7. **Configure Monitoring**: Set up alerts for deployment failures.
8. **Document WIF Setup**: Provide one-time WIF configuration commands.

## Validation Rules Enforced

### 1. Workload Identity Federation (WIF) Mandatory
- **NEVER use JSON service account keys**.
- **ALWAYS use WIF** with OIDC permissions.

### 2. OIDC Permissions Required
- Ensure `id-token: write` is included in permissions.

### 3. IAM Least Privilege
- Avoid overly permissive roles (e.g., roles/owner, roles/editor).

### 4. Vertex AI Agent Engine Deployment Validation
- Implement mandatory post-deployment checks to ensure agent status and configuration.

### 5. Security Scanning
- Conduct security validation before deployment, including secret scanning and vulnerability checks.

### 6. Agent Configuration Validation
- Validate agent configuration before deployment to ensure compliance with best practices.

## Workflow Templates

### Template 1: Vertex AI Agent Engine Deployment
```yaml
name: Deploy Vertex AI Agent

on:
  push:
    branches: [main]
    paths:
      - 'agent/**'
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

jobs:
  validate-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to GCP (WIF)
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Validate Agent Configuration
        run: |
          python scripts/validate-agent-config.py

      - name: Deploy to Vertex AI Engine
        run: |
          python scripts/deploy-agent.py \
            --project-id=${{ secrets.GCP_PROJECT_ID }} \
            --location=${{ env.REGION }} \
            --agent-id=${{ env.AGENT_ID }}

      - name: Post-Deployment Validation
        run: |
          python scripts/validate-deployment.py \
            --project-id=${{ secrets.GCP_PROJECT_ID }} \
            --agent-id=${{ env.AGENT_ID }}
```

### Template 2: Security Validation (Pre-Deployment)
```yaml
name: Security Validation

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  security-checks:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main

      - name: Vulnerability scanning
        uses: aquasecurity/trivy-action@master

      - name: Validate no service account keys
        run: |
          if find . -name "*service-account*.json"; then
            echo "❌ Service account key files detected"
            exit 1
          fi
```

## Tool Permissions

This skill uses:
- **Read**: Analyze workflow files and configurations.
- **Write**: Create GitHub Actions workflows.
- **Edit**: Update existing workflows for compliance.
- **Grep**: Search for security issues (JSON keys, etc.).
- **Glob**: Find workflow files across the repository.
- **Bash**: Execute validation scripts and gcloud commands.

## Best Practices Summary

### Security (MANDATORY)
- Use WIF (Workload Identity Federation) - never JSON keys.
- Require `id-token: write` permission for OIDC.
- IAM least privilege (never owner/editor roles).
- Scan for secrets in code (Trufflehog).
- Vulnerability scanning (Trivy).

### Vertex AI Specific (MANDATORY)
- Code Execution Sandbox: 7-14 day TTL.
- Memory Bank enabled for stateful agents.
- Post-deployment validation (agent status, endpoints).

## Version History

- **1.0.0**: Initial release with WIF enforcement, Vertex AI validations, security scanning.

## References

- **Workload Identity Federation**: https://cloud.google.com/iam/docs/workload-identity-federation
- **GitHub OIDC**: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments
- **Vertex AI Agent Engine**: https://cloud.google.com/vertex-ai/docs/agent-engine