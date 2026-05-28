# Ephemeral Environments

**When to use:** PR previews, feature branches, temporary testing environments.

## What Can Be Ephemeral

| Module | Ephemeral? | Reason |
|--------|------------|--------|
| portal | ❌ No | Single instance, everything depends on it |
| infrastructure | ❌ No | Expensive, slow to provision (VPC/cluster) |
| operators | ❌ No | K8s operators must exist for workloads |
| shared | ❌ No | Stateful data (databases, caches) |
| **tenant** | ✅ Yes | Lightweight, no persistent state |
| **app** | ✅ Yes | Deploys to ephemeral tenant |

Only **tenant** and **app** modules should be ephemeral.

## ⚠️ Critical Constraint: No Variables

**Ephemeral environments cannot use variables passed at runtime.**

The only way to configure an ephemeral environment is via tfvars files in the config directory. These files must exist before `terraform apply`.

```
# This WORKS - tfvars file exists
config/tenant/pr-123/tenant.tfvars

# This DOES NOT WORK - no way to pass vars dynamically
terraform apply -var="something=value"
```

## Naming Convention

```
pr-<number>      # PR previews: pr-123, pr-456
feat-<name>      # Feature branches: feat-auth, feat-api
tmp-<name>       # Temporary: tmp-loadtest, tmp-demo
```

## Workflow Pattern

### 1. PR Opens → Create Config

```bash
# Create tfvars for the PR
mkdir -p config/tenant/pr-${PR_NUMBER}
cat > config/tenant/pr-${PR_NUMBER}/tenant.tfvars <<EOF
shared      = "shrd01"
environment = "dev"
EOF
```

### 2. Apply Tenant + Apps

```bash
tf ctx pr-${PR_NUMBER}
tf apply -chdir=modules/tenant
tf apply -chdir=modules/myapp
```

### 3. PR Closes → Destroy

```bash
tf ctx pr-${PR_NUMBER}
tf destroy -chdir=modules/myapp
tf destroy -chdir=modules/tenant
rm -rf config/tenant/pr-${PR_NUMBER}
```

## GitHub Actions Example

```yaml
name: PR Environment

on:
  pull_request:
    types: [opened, synchronize, closed]

jobs:
  create:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Create config
        run: |
          mkdir -p config/tenant/pr-${{ github.event.number }}
          echo 'shared = "shrd01"' > config/tenant/pr-${{ github.event.number }}/tenant.tfvars
          echo 'environment = "dev"' >> config/tenant/pr-${{ github.event.number }}/tenant.tfvars
      
      - name: Apply
        run: |
          tf ctx pr-${{ github.event.number }}
          tf apply -chdir=modules/tenant -auto-approve

  destroy:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Destroy
        run: |
          tf ctx pr-${{ github.event.number }}
          tf destroy -chdir=modules/tenant -auto-approve
      
      - name: Cleanup config
        run: rm -rf config/tenant/pr-${{ github.event.number }}
```

## Topology

```
Portal (permanent)
└── Infrastructure (permanent)
    ├── Shared (permanent) ─────────────┐
    ├── Operators (permanent)           │
    ├── prod01 (permanent)              │
    ├── stg01 (permanent)               │
    └── pr-123 (ephemeral) ◄────────────┤ parent = shared
        └── myapp (ephemeral)           │ inherits DB access
```

## Key Points

1. **Ephemeral = tenant + app only**
2. **No runtime variables** - must use tfvars files
3. **Config files must exist** before apply
4. **Clean up on close** - destroy resources AND delete config
5. **Share infrastructure** - ephemeral tenants use existing shared/infra
