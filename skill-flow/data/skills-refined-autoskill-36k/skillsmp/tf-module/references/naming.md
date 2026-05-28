# Naming Conventions

## Summary Table

| Module | Max Length | Format | Examples |
|--------|------------|--------|----------|
| tenant | ~10 chars | `<env><inc>` | `dev01`, `stg02`, `prd06`, `qa11`, `tmp45` |
| infrastructure | 16-20 chars | `<name>[<inc>]` | `nonprod01`, `production`, `useast1-prod` |
| shared | ~10 chars | `<prefix><inc>` | `shrd01`, `shared02`, `prdshr06` |
| operators | ~10 chars | `<prefix><inc>` | `ops01`, `prdop01` |
| portal | any | descriptive | `main`, `acme-portal` |
| devops | exactly `devops` | singleton | `devops` |
| app | = tenant name | matches tenant | `dev01`, `stg02`, `prd06` |

## Tenant Names

**Keep very short** (~10 chars or less).

```
dev01, dev02    # Development
stg01, stg02    # Staging  
prd01, prd06    # Production
qa11, qa12      # QA
tmp45           # Temporary/ephemeral
```

**Always use incrementor** - IAM roles with wildcards may see `dev` and `dev01` as overlaps.

## Infrastructure Names

Can be longer (16-20 chars). Incrementor optional.

```
nonprod01       # Non-production cluster
production      # Production cluster (no inc is fine)
useast1-prod    # Regional naming
```

## Shared Names

Short with incrementor.

```
shrd01, shrd02      # Standard
shared01            # Longer variant
prdshr06            # Production shared
```

## Operators Names

Short with incrementor.

```
ops01           # Standard operators
prdop01         # Production operators
```

## Portal Names

No strict convention - just descriptive for workspace identification.

```
main
acme-portal
mycompany
```

## Devops Module (Special Case)

⚠️ **The devops module is a singleton.**

- Module name: `devops`
- Workspace name: `devops` (always, only one)
- **No infrastructure reference** - uses default infra
- **No parent tenant** - standalone

```hcl
# modules/devops/tenant.tf
resource "duplocloud_tenant" "devops" {
  # No infra_name - goes to default infrastructure
  # No parent - not a child of any tenant
  plan_id     = module.ctx.plan_id
  tenant_name = "devops"
}
```

## App Workspace Naming (Critical)

⚠️ **App workspaces use the tenant name, not the app name.**

If deploying `myapp` to tenant `dev01`:
- Tenant workspace: `dev01`
- App workspace: `dev01` (NOT `myapp` or `myapp-dev01`)

```
# Tenant workspaces
config/tenant/dev01/tenant.tfvars    → workspace: dev01
config/tenant/stg01/tenant.tfvars    → workspace: stg01
config/tenant/prd01/tenant.tfvars    → workspace: prd01

# App workspaces (SAME names as tenant)
config/myapp/dev01/myapp.tfvars      → workspace: dev01
config/myapp/stg01/myapp.tfvars      → workspace: stg01
config/myapp/prd01/myapp.tfvars      → workspace: prd01
```

**Multiple apps share workspace names:**

```
config/frontend/dev01/frontend.tfvars   → workspace: dev01
config/backend/dev01/backend.tfvars     → workspace: dev01
config/worker/dev01/worker.tfvars       → workspace: dev01
```

All three apps deploy to the `dev01` tenant using workspace `dev01`.

## Why This Matters

The `module.ctx` pattern with `tenant = {}` uses the workspace name to determine the target tenant:

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  workspaces = {
    tenant = {}  # Empty = terraform.workspace IS the tenant name
  }
}
```

When workspace is `dev01`, the app deploys to tenant `dev01`.

## Examples

```
# Correct
tf ctx dev01 && tf apply -chdir=modules/myapp      # Deploys myapp to dev01
tf ctx stg01 && tf apply -chdir=modules/myapp      # Deploys myapp to stg01
tf ctx prd01 && tf apply -chdir=modules/myapp      # Deploys myapp to prd01

# Wrong - don't use app name as workspace
tf ctx myapp-dev01 && tf apply -chdir=modules/myapp   # ❌ Wrong pattern
```
