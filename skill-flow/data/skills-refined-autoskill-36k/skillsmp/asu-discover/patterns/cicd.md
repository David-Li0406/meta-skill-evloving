---
name: cicd
title: CI/CD Pipelines
description: Centralized CI/CD patterns for Jenkins and GitHub Actions at ASU
subtypes:
  - jenkins
  - github-actions
  - templates
---

# CI/CD Pipelines

Centralized CI/CD patterns for Jenkins and GitHub Actions at ASU.
The primary asset is the Jenkins Shared Library with 75+ reusable
Groovy functions covering Terraform, Vault, credentials, security
scanning, and notifications.

## Jenkins

**Repository**: ASU/devops-jenkins-pipeline-library
**Location**: vars/

### Terraform Functions
- `terraformInit`, `terraformPlan`, `terraformApply`
- `terraformPlanV2`, `terraformV2`
- `pipelineTerraformSingleEnvironment`

### Vault Functions
- `vaultLogin`, `caasVaultLogin`, `opsVaultLogin`
- `getVaultSecret`, `getVaultToken`, `getVaultAppRoleToken`

### Credentials Setup
- `setupGradleCredentials`, `setupMavenCredentials`
- `setupNpmCredentials`, `setupPipCredentials`
- `setupPoetryCredentials`, `setupUvCredentials`

### Security Scanning
- `bridgecrewScan`, `scanDockerImage`, `scanDockerImageWithInspector`

### Notifications
- `slackNotification`, `botNotification`, `datadogDeployment`

### ServiceNow
- `servicenow_change`, `changeFreezeCheck`

### Ansible
- `ansible`, `ansibleKubernetes`, `ansiblePlaybook`

### MuleSoft
- `mule4caasPipeline`, `mule4caasPipelineSf`
- `mulesoftBuild`, `mulesoftDeploy`

## GitHub Actions

### Reusable Workflows
**Repo**: ASU/caas-image-library
**Path**: .github/workflows/

| Workflow | Description |
|----------|-------------|
| workflow-build-image.yml | Generic container image build with Trivy scanning |
| workflow-build-image-tomcat.yml | Tomcat-specific image builds |

### Job Workflows
- job-apache-installer.yml
- job-haproxy-default-backend.yml
- job-k8s-deploy.yml
- job-sonar-scanner.yml

### OIDC Example
**Repo**: ASU/dco-github-actions-oidc-aws-example
GitHub Actions OIDC with AWS

## Templates

### CaaS Templates
**Repo**: ASU/caas-pipeline-templates
- legacy-warapps
- legacy-warapps-deployment

### Mobile Templates
**Repo**: ASU/mobile-mapp-templates
Mobile Application Publishing Pipeline Templates

### MuleSoft Templates
**Repo**: ASU/ddt-mulesoft-base-application-template
Template with container pipeline for Mulesoft apps

## Team Prefixes

dco, caas, devops, dot

## Related Commands

```bash
discover.sh pattern --name cicd --type jenkins
discover.sh pattern --name cicd --type github-actions
discover.sh pattern --name cicd --type templates
discover.sh repos --domain cicd
```
