# GitHub Actions

**Category**: developer-tools/cicd
**Description**: GitHub's built-in CI/CD automation platform
**Homepage**: https://github.com/features/actions

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `@actions/core` - Core functions for GitHub Actions
- `@actions/github` - GitHub API client for Actions
- `@actions/exec` - Command execution for Actions
- `@actions/io` - I/O functions for Actions
- `@actions/tool-cache` - Tool caching for Actions
- `@actions/artifact` - Artifact upload/download
- `@actions/cache` - Caching for Actions
- `@actions/glob` - Glob matching for Actions

#### PYPI
- `actions-toolkit` - Python toolkit for GitHub Actions

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### Configuration Files
*Known configuration files that indicate GitHub Actions*

- `.github/workflows/*.yml` - Workflow definition files
- `.github/workflows/*.yaml` - Workflow definition files (alternate extension)
- `.github/actions/*/action.yml` - Custom action definitions
- `.github/actions/*/action.yaml` - Custom action definitions (alternate extension)

### Configuration Directories
*Known directories that indicate GitHub Actions*

- `.github/workflows/` - Workflow directory (strong indicator)
- `.github/actions/` - Custom actions directory

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `import\s+.*\s+from\s+['"]@actions/core['"]`
- Actions core import
- Example: `import * as core from '@actions/core';`

**Pattern**: `import\s+.*\s+from\s+['"]@actions/github['"]`
- Actions github import
- Example: `import { context } from '@actions/github';`

**Pattern**: `require\(['"]@actions/core['"]\)`
- Actions core require
- Example: `const core = require('@actions/core');`

**Pattern**: `require\(['"]@actions/github['"]\)`
- Actions github require
- Example: `const github = require('@actions/github');`

### Code Patterns
*GitHub Actions YAML patterns in workflow files*

**Pattern**: `^name:\s*`
- Workflow name declaration
- Example: `name: CI`

**Pattern**: `^on:\s*`
- Workflow trigger declaration
- Example: `on: push`

**Pattern**: `^\s*jobs:\s*$`
- Jobs section
- Example: `jobs:`

**Pattern**: `^\s*runs-on:\s*`
- Runner specification
- Example: `runs-on: ubuntu-latest`

**Pattern**: `^\s*uses:\s*`
- Action reference
- Example: `uses: actions/checkout@v4`

**Pattern**: `^\s*steps:\s*$`
- Steps section
- Example: `steps:`

**Pattern**: `\$\{\{\s*`
- Expression syntax
- Example: `${{ secrets.GITHUB_TOKEN }}`

**Pattern**: `actions/checkout@`
- Checkout action usage
- Example: `uses: actions/checkout@v4`

**Pattern**: `actions/setup-node@`
- Node setup action
- Example: `uses: actions/setup-node@v4`

**Pattern**: `actions/setup-python@`
- Python setup action
- Example: `uses: actions/setup-python@v5`

---

## Environment Variables

- `GITHUB_ACTIONS` - Set to true in GitHub Actions
- `GITHUB_WORKFLOW` - Workflow name
- `GITHUB_RUN_ID` - Unique run ID
- `GITHUB_RUN_NUMBER` - Run number
- `GITHUB_JOB` - Job ID
- `GITHUB_ACTION` - Action name
- `GITHUB_ACTOR` - User who triggered the workflow
- `GITHUB_REPOSITORY` - Repository name
- `GITHUB_EVENT_NAME` - Event that triggered workflow
- `GITHUB_SHA` - Commit SHA
- `GITHUB_REF` - Branch or tag ref
- `GITHUB_TOKEN` - Authentication token
- `RUNNER_OS` - Runner operating system
- `RUNNER_TEMP` - Temporary directory
- `RUNNER_TOOL_CACHE` - Tool cache directory

## Detection Notes

- `.github/workflows/` directory is the strongest indicator
- Workflow files use YAML format with specific schema
- Actions are referenced using `uses:` syntax
- Expressions use `${{ }}` syntax
- Many first-party actions from `actions/*` org
- Custom actions can be in `.github/actions/` directory

---

## TIER 3: Configuration Extraction

These patterns extract specific configuration values from GitHub Actions workflows.

### Secrets Reference Extraction

**Pattern**: `\$\{\{\s*secrets\.([A-Z_][A-Z0-9_]*)\s*\}\}`
- GitHub secrets referenced in workflow
- Extracts: `secret_name`
- Example: `${{ secrets.AWS_ACCESS_KEY_ID }}`

### AWS OIDC Role Extraction

**Pattern**: `role-to-assume:\s*arn:aws:iam::([0-9]{12}):role/([^\s'"]+)`
- AWS IAM role for OIDC authentication
- Extracts: `aws_account_id`, `role_name`
- Example: `role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole`

**Pattern**: `aws-region:\s*['"]?([a-z]{2}-[a-z]+-[0-9])['"]?`
- AWS region configuration
- Extracts: `aws_region`
- Example: `aws-region: us-west-2`

### Environment Extraction

**Pattern**: `environment:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- GitHub deployment environment
- Extracts: `environment_name`
- Example: `environment: production`

**Pattern**: `url:\s*['"]?(https?://[^'"]+)['"]?`
- Environment URL
- Extracts: `environment_url`
- Example: `url: https://app.example.com`

### Container Registry Extraction

**Pattern**: `registry:\s*['"]?([a-z0-9.-]+)['"]?`
- Container registry for Docker login action
- Extracts: `registry_url`
- Example: `registry: ghcr.io`

**Pattern**: `ECR_REGISTRY:\s*['"]?([0-9]{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com)['"]?`
- AWS ECR registry
- Extracts: `ecr_registry`
- Example: `ECR_REGISTRY: 123456789012.dkr.ecr.us-west-2.amazonaws.com`

### Action References Extraction

**Pattern**: `uses:\s*([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)@([^\s]+)`
- Third-party actions used
- Extracts: `action_repo`, `version`
- Example: `uses: actions/checkout@v4`

### Runner Extraction

**Pattern**: `runs-on:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- GitHub runner type
- Extracts: `runner`
- Example: `runs-on: ubuntu-latest`

**Pattern**: `runs-on:\s*\[self-hosted,\s*([^\]]+)\]`
- Self-hosted runner labels
- Extracts: `runner_labels`
- Example: `runs-on: [self-hosted, linux, x64]`

### Terraform State Backend Extraction

**Pattern**: `terraform.*backend-config="bucket=([^"]+)"`
- Terraform S3 backend bucket
- Extracts: `tf_state_bucket`
- Example: `terraform init -backend-config="bucket=my-terraform-state"`

### Deployment Target Extraction

**Pattern**: `aws-account-id:\s*['"]?([0-9]{12})['"]?`
- AWS account ID for deployment
- Extracts: `aws_account_id`
- Example: `aws-account-id: '123456789012'`

**Pattern**: `cluster:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- ECS/EKS cluster name
- Extracts: `cluster_name`
- Example: `cluster: prod-cluster`

**Pattern**: `service:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- ECS service name
- Extracts: `service_name`
- Example: `service: web-service`

### Extraction Output Example

```json
{
  "extractions": {
    "secrets_referenced": [
      "AWS_ACCESS_KEY_ID",
      "AWS_SECRET_ACCESS_KEY",
      "DOCKERHUB_TOKEN",
      "SLACK_WEBHOOK"
    ],
    "aws_oidc_roles": [
      {
        "account_id": "123456789012",
        "role_name": "GitHubActionsRole",
        "region": "us-west-2",
        "source_file": ".github/workflows/deploy.yml",
        "line": 25
      }
    ],
    "environments": [
      {
        "name": "production",
        "url": "https://app.example.com",
        "source_file": ".github/workflows/deploy.yml"
      }
    ],
    "container_registries": [
      {
        "type": "ecr",
        "url": "123456789012.dkr.ecr.us-west-2.amazonaws.com",
        "source_file": ".github/workflows/build.yml"
      }
    ],
    "third_party_actions": [
      {"repo": "actions/checkout", "version": "v4"},
      {"repo": "actions/setup-node", "version": "v4"},
      {"repo": "aws-actions/configure-aws-credentials", "version": "v4"},
      {"repo": "docker/build-push-action", "version": "v5"}
    ]
  }
}
```
