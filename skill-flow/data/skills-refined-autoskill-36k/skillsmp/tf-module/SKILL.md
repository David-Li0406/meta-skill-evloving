---
name: tf-module
description: Expert in creating Duplocloud Terraform modules following standard patterns. Use when creating terraform modules, tenants, infrastructures, app modules, or working with duplocloud/terraform-duplocloud-components. Knows module.ctx patterns, JIT credentials, workspace references, and GitHub Actions workflows.
---

# Duplocloud Terraform Module Expert

Create and manage Terraform modules following Duplocloud patterns using [terraform-duplocloud-components](https://github.com/duplocloud/terraform-duplocloud-components).

## Topological Hierarchy

```
Portal (Duplocloud instance)
  └── Infrastructure (VPC/GKE cluster)
      ├── Shared Tenant (databases, caches)
      ├── Operators Tenant (Kubernetes operators)
      └── Application Tenants (dev01, stg01, prod01)
```

Each layer maps to a Terraform module with workspace instances.

## Repository Patterns

### Pattern 1: Infra Repo (infra-starter)

Centralized infrastructure repo (e.g., `duplocloud-infra`, `<company>-infra`):

```
<project>-infra/
├── modules/
│   ├── portal/           # Required: Once per Duplocloud
│   ├── infrastructure/   # Required: VPC/cluster
│   ├── shared/           # Required: Databases, caches
│   ├── tenant/           # Required: App environments
│   ├── operators/        # Required: K8s operators
│   ├── devops/           # Optional: CI/CD secrets
│   └── <app>/            # Optional: Centralized apps
├── config/<module>/<workspace>/<module>.tfvars
└── .github/workflows/
```

### Pattern 2: Embedded App Module (Recommended for apps)

App module lives in the application's own repo:

```
<app-repo>/
├── src/                  # Application code
├── terraform/            # Embedded app module
│   ├── main.tf
│   ├── providers.tf
│   ├── variables.tf
│   └── outputs.tf
├── config/<workspace>/<module>.tfvars
└── .github/workflows/
```

### Identifying Context

| Indicator | You're in... |
|-----------|-------------|
| `modules/portal/`, `modules/tenant/`, `modules/shared/` | Infra repo |
| `terraform/` dir + app source code | Embedded app module |
| Only one module + app code | Embedded app module |

## The tf CLI

Use the `tf` wrapper command instead of raw `terraform`. It auto-configures backends and discovers tfvars.

```bash
tf init -chdir=modules/tenant     # Auto-configures backend
tf ctx dev01                      # Select/create workspace
tf plan -chdir=modules/tenant     # Auto-loads tfvars
tf apply -chdir=modules/tenant
```

**See**: [references/tf-cli.md](references/tf-cli.md) for full documentation and equivalent terraform commands.

## Core Pattern: module.ctx

Every module uses the context module for data lookups, JIT credentials, and workspace references:

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    tenant = {}  # Empty = terraform.workspace is tenant name
  }
}

locals {
  tenant = module.ctx.workspaces.tenant
}
```

**See**: [references/context-module.md](references/context-module.md) for JIT credentials, workspace references, and advanced patterns.

## Module Type Quick Reference

| Module | Use Case | Key Pattern |
|--------|----------|-------------|
| **portal** | Once per Duplocloud | `tenant = "default"` |
| **infrastructure** | VPC/cluster per env | References portal |
| **shared** | Databases, caches | `enable_host_other_tenants = true` |
| **devops** | Singleton, CI/CD secrets | No infra/parent, default infra |
| **tenant** | App environments | References shared + infra |
| **app** | Per-tenant deployments | Workspace = tenant name |
| **operators** | Kubernetes operators | JIT k8s credentials |

**Detailed patterns**: See `references/<module-type>.md` files.

## Common Patterns

- **Database setup**: [references/database.md](references/database.md) - Parent-child tenants, credential flow
- **Helm deployments**: [references/helm.md](references/helm.md) - Values templating, chart categories
- **Ephemeral envs**: [references/ephemeral.md](references/ephemeral.md) - PR previews (tenant + app only)
- **Naming conventions**: [references/naming.md](references/naming.md) - Workspace/tenant naming rules
- **AWS patterns**: [references/aws.md](references/aws.md) - S3 backend, JIT credentials
- **GCP patterns**: [references/gcp.md](references/gcp.md) - GCS backend, Cloud SQL

## Creating a New Module

### Option 1: Use the init script

```bash
python scripts/init_module.py myapp --type app --cloud aws
python scripts/init_module.py myapp --type app --cloud gcp --path ./
```

### Option 2: Copy from templates

Templates in `assets/` directory:
- `assets/app/` - App module files
- `assets/tenant/` - Tenant module files
- `assets/shared/` - Shared module files
- `assets/workflow/` - GitHub Actions templates
- `assets/config/` - Tfvars templates

### Option 3: Manual creation

1. Create `modules/<name>/` with: `main.tf`, `providers.tf`, `variables.tf`, `outputs.tf`
2. Add module.ctx with appropriate workspaces
3. Create `config/<name>/<workspace>/<name>.tfvars`
4. Create `.github/workflows/<name>.yml`

## Validating Modules

```bash
python scripts/validate_module.py modules/myapp
python scripts/validate_module.py . --all  # Validate all modules
```

## GitHub Actions

**See**: [references/workflows.md](references/workflows.md) for CI/CD patterns.

Base workflow in `assets/workflow/tf-module.yml` handles:
- Terraform init with auto-backend config
- Workspace selection
- Plan/apply/destroy commands
- PR comments with plan output

## Decision Protocol

### New Module vs New Instance?

- **New Instance**: Same resources, different config → add `config/<module>/<name>/<module>.tfvars`
- **New Module**: Different resources → create `modules/<name>/`

### Which Module Type?

1. Shared across tenants? → **shared**
2. Kubernetes operators/CRDs? → **operators**  
3. Environment (dev/stg/prod)? → **tenant**
4. App deployment? → **app** (with `tenant = {}`)

## Getting More Information

For authoritative documentation:
- Search Duplocloud docs using available documentation tools
- Web search for latest terraform-duplocloud-components version
- Check [Terraform Registry](https://registry.terraform.io/modules/duplocloud/components/duplocloud/latest)

## Secrets Pattern

**Never pass secrets through variables.** Only `DUPLO_TOKEN` should be needed.

Pattern:
1. Module A creates empty secret placeholder (value ignored)
2. User manually populates secret value
3. Module B reads secret via `data` block, injects into provider

**See**: [references/secrets.md](references/secrets.md)

## Skill Resources

| Directory | Contents |
|-----------|----------|
| `references/` | `<module-type>.md`, `database.md`, `helm.md`, `secrets.md`, `aws.md`, `gcp.md` |
| `assets/` | Templates: `app/`, `tenant/`, `shared/`, `workflow/`, `config/` |
| `scripts/` | `init_module.py`, `validate_module.py` |
