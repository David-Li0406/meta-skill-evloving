# Terraform CLI Wrapper (tf.sh)

**When to use this reference:** When running Terraform commands locally or understanding the project's CLI conventions.

## Overview

The `tf` command is a wrapper around Terraform that automates:
- Backend configuration based on cloud provider detection
- Workspace-based tfvars file discovery
- Environment variable setup for Duplocloud authentication

## Installation

The `tf` command is installed via the Duplocloud devcontainer feature:
```json
{
  "features": {
    "ghcr.io/duplocloud/devcontainers/terraform:1": {}
  }
}
```

Source: https://raw.githubusercontent.com/duplocloud/devcontainers/main/src/terraform/scripts/tf.sh

## Commands

### tf init

Auto-configures the backend based on the cloud provider detected from the Duplocloud portal:

```bash
tf init -chdir=modules/tenant
```

**What it does:**
1. Calls `duploctl system info --admin` to detect cloud provider
2. Sets backend config based on cloud:
   - **AWS**: `-backend-config=bucket=duplo-tfstate-<account-id> -backend-config=region=<region> -backend-config=dynamodb_table=<bucket>-lock`
   - **GCP**: `-backend-config=bucket=duplo-tfstate-<project-id>`
   - **Azure**: `-backend-config=storage_account_name=duplotfstate<account-id>`
3. Runs `terraform init` with the assembled arguments

**Equivalent terraform command (AWS):**
```bash
terraform init -chdir=modules/tenant \
  -input=false \
  -backend-config="bucket=duplo-tfstate-123456789012" \
  -backend-config="region=us-west-2" \
  -backend-config="dynamodb_table=duplo-tfstate-123456789012-lock"
```

### tf ctx

Workspace selection with interactive fuzzy finder:

```bash
tf ctx dev01           # Select or create workspace 'dev01'
tf ctx                 # Interactive selection with fzf
```

**What it does:**
1. If argument provided, uses it as workspace name
2. If no argument, shows `fzf` selection of existing workspaces
3. Runs `terraform workspace select -or-create <name>`

**Equivalent terraform command:**
```bash
terraform workspace select -or-create dev01
```

### tf plan/apply/destroy

Runs terraform commands with auto-discovered tfvars:

```bash
tf plan -chdir=modules/tenant
tf apply -chdir=modules/tenant
tf destroy -chdir=modules/tenant
```

**What it does:**
1. Discovers config directory by walking up from current dir looking for `config/`
2. Gets current workspace name from `terraform workspace show`
3. Constructs var file path: `config/<workspace>/<module>.tfvars`
4. Appends `-var-file=<path>` if file exists (also checks `.tfvars.json`)

**Equivalent terraform command:**
```bash
# Given: module=tenant, workspace=dev01
terraform plan -chdir=modules/tenant \
  -var-file=../../config/dev01/tenant.tfvars
```

## Config Directory Discovery

The `tf` wrapper walks up the directory tree to find a `config/` folder:

```
project-root/
├── config/                    # <- Discovered config root
│   ├── tenant/
│   │   └── dev01/
│   │       └── tenant.tfvars
│   └── shared/
│       └── shrd01/
│           └── shared.tfvars
└── modules/
    ├── tenant/                # <- Running tf from here
    └── shared/
```

Override with `TF_WORKSPACE_DIR` environment variable if needed.

## Var File Convention

The wrapper expects this structure:
```
config/<module>/<workspace>/<module>.tfvars
```

Examples:
- `config/tenant/dev01/tenant.tfvars`
- `config/shared/shrd01/shared.tfvars`
- `config/infrastructure/nonprod01/infrastructure.tfvars`

## Environment Variables

Required:
```bash
export DUPLO_HOST="https://portal.duplocloud.net"
export DUPLO_TOKEN="<your-admin-token>"
```

Optional:
```bash
export DUPLO_TF_BUCKET="custom-bucket-name"  # Override auto-detected bucket
export TF_WORKSPACE_DIR="/path/to/config"    # Override config discovery
```

## Typical Workflow

```bash
# Navigate to project
cd /workspace/project-infra

# Initialize module
tf init -chdir=modules/tenant

# Select workspace
tf ctx dev01

# Plan changes
tf plan -chdir=modules/tenant

# Apply changes
tf apply -chdir=modules/tenant
```

## Manual Terraform Equivalents

If you need to run terraform directly (without the wrapper), ensure:

1. **Backend is configured** - Pass appropriate `-backend-config` args to `init`
2. **Workspace is selected** - Use `terraform workspace select`
3. **Var file is specified** - Pass `-var-file` to plan/apply/destroy
4. **Environment is set** - Export `DUPLO_HOST` and `DUPLO_TOKEN` (lowercase versions: `duplo_host`, `duplo_token`)

The Duplocloud provider reads credentials from environment:
```bash
export duplo_host=$DUPLO_HOST
export duplo_token=$DUPLO_TOKEN
```
