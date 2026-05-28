# GitHub Actions Workflow Patterns

**When to use this reference:** When creating or modifying CI/CD workflows for Terraform modules.

## Overview

Duplocloud Terraform modules use a two-tier workflow pattern:
1. **Base workflow** (`tf-module.yml`) - Reusable workflow with common logic
2. **Module workflows** (`<module>.yml`) - Module-specific triggers and configuration

## Directory Structure

```
.github/workflows/
├── tf-module.yml      # Reusable base workflow
├── portal.yml         # Portal module workflow
├── infrastructure.yml # Infrastructure workflow
├── shared.yml         # Shared module workflow
├── tenant.yml         # Tenant module workflow
└── <app>.yml          # App-specific workflows
```

## Base Workflow (tf-module.yml)

```yaml
name: 🏗️ Terraform Module Runner

on:
  workflow_call:
    inputs:
      cmd:
        description: "Terraform command (plan, apply, destroy)"
        type: string
        default: plan
      module:
        description: "Module directory name"
        type: string
        required: true
      workspace:
        description: "Terraform workspace name"
        type: string
        required: true
      portal:
        description: "Duplocloud portal environment name"
        type: string
        required: true
    secrets:
      DUPLO_TOKEN:
        description: "Duplocloud API token"
        required: true

jobs:
  terraform:
    name: ${{ inputs.cmd }} - ${{ inputs.workspace }}
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.portal }}
    env:
      DUPLO_HOST: ${{ vars.DUPLO_HOST }}
      DUPLO_TOKEN: ${{ secrets.DUPLO_TOKEN }}
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Duplocloud
        uses: duplocloud/actions/setup@main
        with:
          admin: true
      
      - name: Setup Terraform
        uses: duplocloud/actions/setup-terraform@main
      
      - name: Terraform Init
        uses: duplocloud/actions/terraform-module@main
        with:
          module: modules/${{ inputs.module }}
      
      - name: Terraform ${{ inputs.cmd }}
        uses: duplocloud/actions/terraform-exec@main
        with:
          module: modules/${{ inputs.module }}
          command: ${{ inputs.cmd }}
          workspace: ${{ inputs.workspace }}
          config: config/${{ inputs.module }}
      
      - name: Comment Plan on PR
        if: inputs.cmd == 'plan' && github.event_name == 'pull_request'
        uses: duplocloud/actions/terraform-comment@main
        with:
          module: modules/${{ inputs.module }}
```

## Module-Specific Workflows

### Tenant Module

```yaml
# tenant.yml
name: 🗃️ Tenant Module

on:
  pull_request:
    paths:
      - modules/tenant/**
      - config/tenant/**
      - .github/workflows/tenant.yml
  push:
    paths:
      - modules/tenant/**
      - config/tenant/**
    branches: [main]
  workflow_dispatch:
    inputs:
      workspace:
        description: "Tenant workspace"
        type: choice
        options:
          - dev01
          - dev02
          - stg01
          - prod01
      cmd:
        description: "Terraform command"
        type: choice
        options:
          - plan
          - apply
          - destroy
        default: plan

jobs:
  detect-workspaces:
    if: github.event_name != 'workflow_dispatch'
    runs-on: ubuntu-latest
    outputs:
      workspaces: ${{ steps.detect.outputs.workspaces }}
    steps:
      - uses: actions/checkout@v4
      - id: detect
        run: |
          # Detect changed workspaces from config/tenant/*/
          workspaces=$(ls -1 config/tenant/ | jq -R -s -c 'split("\n")[:-1]')
          echo "workspaces=$workspaces" >> $GITHUB_OUTPUT

  terraform:
    needs: [detect-workspaces]
    if: always() && (needs.detect-workspaces.outputs.workspaces != '[]' || github.event_name == 'workflow_dispatch')
    strategy:
      matrix:
        workspace: ${{ github.event_name == 'workflow_dispatch' && fromJson(format('["{0}"]', inputs.workspace)) || fromJson(needs.detect-workspaces.outputs.workspaces) }}
      fail-fast: false
    uses: ./.github/workflows/tf-module.yml
    secrets: inherit
    with:
      cmd: ${{ github.event_name == 'pull_request' && 'plan' || inputs.cmd || 'apply' }}
      module: tenant
      workspace: ${{ matrix.workspace }}
      portal: ${{ vars.DUPLO_PORTAL }}
```

### App Module

```yaml
# myapp.yml
name: 📦 MyApp Module

on:
  pull_request:
    paths:
      - modules/myapp/**
      - config/myapp/**
  push:
    paths:
      - modules/myapp/**
      - config/myapp/**
    branches: [main]
  workflow_dispatch:
    inputs:
      workspace:
        description: "Target tenant"
        type: choice
        options:
          - dev01
          - stg01
          - prod01
      cmd:
        type: choice
        options:
          - plan
          - apply
          - destroy

jobs:
  module:
    uses: ./.github/workflows/tf-module.yml
    secrets: inherit
    with:
      cmd: ${{ github.event_name == 'pull_request' && 'plan' || inputs.cmd || 'apply' }}
      module: myapp
      workspace: ${{ inputs.workspace || vars.DEFAULT_TENANT }}
      portal: ${{ vars.DUPLO_PORTAL }}
```

### Infrastructure Module

```yaml
# infrastructure.yml
name: 🌐 Infrastructure Module

on:
  pull_request:
    paths:
      - modules/infrastructure/**
      - config/infrastructure/**
  push:
    paths:
      - modules/infrastructure/**
      - config/infrastructure/**
    branches: [main]
  workflow_dispatch:
    inputs:
      workspace:
        type: choice
        options:
          - nonprod01
          - prod01
      cmd:
        type: choice
        options:
          - plan
          - apply
          - destroy

jobs:
  module:
    uses: ./.github/workflows/tf-module.yml
    secrets: inherit
    with:
      cmd: ${{ github.event_name == 'pull_request' && 'plan' || inputs.cmd || 'apply' }}
      module: infrastructure
      workspace: ${{ inputs.workspace || 'nonprod01' }}
      portal: ${{ vars.DUPLO_PORTAL }}
```

## GitHub Environments

Configure environments in GitHub repository settings:

| Environment | Variables | Secrets |
|-------------|-----------|---------|
| `myportal` | `DUPLO_HOST` | `DUPLO_TOKEN` |

Environment protection rules:
- **Production**: Require reviewers
- **Staging**: Optional reviewers
- **Development**: No protection

## Duplocloud Actions

| Action | Purpose |
|--------|---------|
| `duplocloud/actions/setup` | Configure Duplocloud CLI and auth |
| `duplocloud/actions/setup-terraform` | Install Terraform with cache |
| `duplocloud/actions/terraform-module` | Run terraform init with backend config |
| `duplocloud/actions/terraform-exec` | Run terraform commands with workspace/config |
| `duplocloud/actions/terraform-comment` | Post plan output to PR |

## PR Plan Comments

When a PR contains module changes:
1. Workflow runs `terraform plan` against the default workspace
2. Plan output is posted as a **comment on the PR**
3. **Multiple modules = multiple comments** (one per module)

This allows reviewers to see:
- Code changes in the PR diff
- Terraform plan showing infrastructure impact

## Command Flow

### On Pull Request
1. Trigger: PR opened/updated with module changes
2. Command: `plan`
3. Output: Plan commented on PR

### On Push to Main
1. Trigger: PR merged to main
2. Command: `apply`
3. Output: Changes applied

### Manual Dispatch
1. Trigger: Workflow dispatch with inputs
2. Command: Selected (plan/apply/destroy)
3. Output: Command executed

## GitHub Variables

Module workflows use GitHub variables for default workspace names:

```yaml
# Repository variables (Settings → Secrets and variables → Actions → Variables)
vars:
  DUPLO_HOST: "https://portal.duplocloud.net"
  DUPLO_PORTAL: "myportal"           # Environment name for secrets
  DEFAULT_TENANT: "dev01"            # Default tenant for automated runs
  DEFAULT_SHARED: "shrd01"           # Default shared workspace
  DEFAULT_INFRA: "nonprod01"         # Default infrastructure workspace

# Repository secrets
secrets:
  DUPLO_TOKEN: "<admin-api-token>"
```

**Usage in workflows:**

```yaml
# Fallback to GitHub variable if no input provided
workspace: ${{ inputs.workspace || vars.DEFAULT_TENANT }}
portal: ${{ vars.DUPLO_PORTAL }}
```

This enables automated PR plans to run against a consistent default environment.

## Matrix Strategy for Multiple Workspaces

Deploy to multiple workspaces in parallel:

```yaml
jobs:
  terraform:
    strategy:
      matrix:
        workspace: [dev01, dev02, stg01]
      fail-fast: false
    uses: ./.github/workflows/tf-module.yml
    with:
      workspace: ${{ matrix.workspace }}
      # ...
```

## Dependency Between Modules

Use `needs` for ordered execution:

```yaml
jobs:
  shared:
    uses: ./.github/workflows/tf-module.yml
    with:
      module: shared
      # ...
  
  tenant:
    needs: [shared]
    uses: ./.github/workflows/tf-module.yml
    with:
      module: tenant
      # ...
```

## Path Filtering

Only run when relevant files change:

```yaml
on:
  pull_request:
    paths:
      - modules/mymodule/**     # Module source
      - config/mymodule/**      # Module config
      - .github/workflows/mymodule.yml  # This workflow
```
