# Feature Detection Patterns

How to search a workspace to determine which devcontainer features to include.

## Detection Strategy

1. **Read README.md first** - Understand project purpose and stack
2. **Search for file patterns** - Find config files and code
3. **Grep for keywords** - Identify cloud providers and tools
4. **Check existing configs** - Look for CI/CD and deployment hints

## Cloud Provider Detection

### AWS Indicators

**Files to look for:**
- `*.tf` files with `provider "aws"` or `backend "s3"`
- `config/aws*`, `aws.json`, `aws-config`
- `.aws/` directory references

**Keywords to grep:**
```bash
grep -ri "aws\|s3://\|dynamodb\|lambda\|ec2\|rds\|elasticache" \
  --include="*.tf" --include="*.yaml" --include="*.yml" \
  --include="*.json" --include="*.py" --include="*.md" .
```

**Environment variable references:**
- `AWS_REGION`, `AWS_DEFAULT_REGION`
- `AWS_PROFILE`, `AWS_ACCESS_KEY_ID`

**Result:** Include `aws-cli` with JIT enabled

### GCP Indicators

**Files to look for:**
- `*.tf` files with `provider "google"` or `backend "gcs"`
- `config/gcloud*`, `gcloud.json`
- Service account JSON files

**Keywords to grep:**
```bash
grep -ri "gcloud\|gs://\|google\|gcp\|bigquery\|cloud run\|gke" \
  --include="*.tf" --include="*.yaml" --include="*.yml" \
  --include="*.json" --include="*.py" --include="*.md" .
```

**Environment variable references:**
- `GOOGLE_APPLICATION_CREDENTIALS`
- `CLOUDSDK_CONFIG`, `GCP_PROJECT`

**Result:** Include `gcloud-cli`

---

## Terraform Detection

**Files to look for:**
```bash
find . -name "*.tf" -o -name "*.tfvars" | head -20
ls -la modules/ terraform/ 2>/dev/null
```

**Directory patterns:**
- `modules/` with subdirectories
- `terraform/` directory
- `config/` with `.tfvars` files

**Result:** Include `terraform` feature

---

## Kubernetes Detection

**Files to look for:**
```bash
find . -name "*.yaml" -exec grep -l "apiVersion:\|kind:" {} \; | head -10
find . -name "kubeconfig*" -o -name "kube-config*"
```

**Keywords to grep:**
```bash
grep -ri "kubectl\|kubernetes\|k8s\|helm\|deployment\|service\|pod" \
  --include="*.yaml" --include="*.yml" --include="*.md" .
```

**File patterns:**
- `*-deployment.yaml`, `*-service.yaml`
- `values.yaml` (Helm)
- `Chart.yaml` (Helm chart)

**Result:** Include `kubernetes` with JIT enabled

---

## Git Provider Detection

### GitHub

**Indicators:**
```bash
ls -la .github/ 2>/dev/null
grep -r "github.com" . --include="*.md" --include="*.yaml" | head -5
```

**Files:**
- `.github/workflows/` directory
- References to `github.com` in code

**Result:** Include `github` feature

### GitLab

**Indicators:**
```bash
ls -la .gitlab-ci.yml 2>/dev/null
grep -r "gitlab.com\|gitlab-ci" . --include="*.md" --include="*.yaml"
```

### Bitbucket

**Indicators:**
```bash
ls -la bitbucket-pipelines.yml 2>/dev/null
grep -r "bitbucket.org" . --include="*.md" --include="*.yaml"
```

---

## AI Tools Decision

Choose AI provider based on team preference or ask user:

| Provider | Feature | VS Code Extension |
|----------|---------|-------------------|
| Claude (Anthropic) | `ai-claude` | `anthropic.claude-code` |
| Codex (OpenAI) | `ai-codex` | `openai.chatgpt` |
| Gemini (Google) | `ai-gemini` | `Google.geminicodeassist` |
| GitHub Copilot | `github` | `GitHub.copilot-chat` |

### When to include AI tools

- Complex codebase with multiple modules
- Infrastructure projects (Terraform)
- Projects benefiting from code generation
- **Ask user which AI provider** they prefer if unclear

### Skills to include

| Project Type | Recommended Skills |
|--------------|-------------------|
| Terraform/Infra | `tf-module` |
| Devcontainer work | `devcontainers` |
| General | (ask user or none) |

### Multiple AI providers

Can include multiple if team uses different tools:

```json
"features": {
  "ghcr.io/duplocloud/devcontainers/ai-claude:1": { "skills": "tf-module" },
  "ghcr.io/duplocloud/devcontainers/ai-gemini:1": { "skills": "tf-module" }
}
```

---

## 1Password Detection

### When to include onepassword-cli

- Team uses 1Password for secrets
- SSH key management needed
- User explicitly requests it

**Note:** This is often a team/org decision rather than detectable from code.

### Common configurations

**DuploCloud employees:**
```json
{
  "account": "duplocloudinc.1password.com",
  "vault": "Employee"
}
```

**Custom organization:**
```json
{
  "account": "${localEnv:OP_ACCOUNT}",
  "vault": "${localEnv:OP_VAULT_NAME}"
}
```

---

## Language/Stack Detection

### Python

```bash
ls -la requirements.txt setup.py pyproject.toml 2>/dev/null
find . -name "*.py" | head -5
```

**Base image:** `mcr.microsoft.com/vscode/devcontainers/python:3.12`

**Extensions:** `ms-python.python`

### Node.js

```bash
ls -la package.json 2>/dev/null
find . -name "*.js" -o -name "*.ts" | head -5
```

**Base image:** `mcr.microsoft.com/vscode/devcontainers/javascript-node:20`

### Go

```bash
ls -la go.mod go.sum 2>/dev/null
find . -name "*.go" | head -5
```

**Base image:** `mcr.microsoft.com/vscode/devcontainers/go:1.21`

---

## Quick Detection Script

Run these commands to quickly assess a workspace:

```bash
# Project type
echo "=== README ===" && head -50 README.md 2>/dev/null

# Cloud provider
echo "=== AWS ===" && grep -rl "aws\|s3://" --include="*.tf" . 2>/dev/null | head -3
echo "=== GCP ===" && grep -rl "gcloud\|gs://" --include="*.tf" . 2>/dev/null | head -3

# Infrastructure
echo "=== Terraform ===" && find . -name "*.tf" 2>/dev/null | head -5
echo "=== Kubernetes ===" && find . -name "*.yaml" -exec grep -l "kind:" {} \; 2>/dev/null | head -3

# Git provider
echo "=== Git ===" && ls -la .github/ .gitlab-ci.yml bitbucket-pipelines.yml 2>/dev/null

# Language
echo "=== Language ===" && ls requirements.txt package.json go.mod Cargo.toml 2>/dev/null
```

---

## Feature Decision Matrix

| Detected | Features to Add |
|----------|-----------------|
| AWS in .tf files | `aws-cli` (jit: true, jitAdmin: true) |
| GCP in .tf files | `gcloud-cli` |
| `modules/` or `terraform/` | `terraform` |
| K8s manifests or helm | `kubernetes` (jit: true) |
| `.github/` directory | `github` |
| Complex infra project | `ai-codex` with skills |
| Team uses 1Password | `onepassword-cli` (ask user) |

**Always add:** `duploctl` (required for all DuploCloud features)
