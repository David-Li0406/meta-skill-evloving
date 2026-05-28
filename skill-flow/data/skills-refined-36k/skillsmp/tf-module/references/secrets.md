# Secrets Management Pattern

**When to use:** Always. Never pass secrets through Terraform variables.

## Principle

Only `DUPLO_TOKEN` should be required to run any module. All other secrets are:
1. Created as empty placeholders by Terraform
2. Populated manually (or by separate process)
3. Read via `data` blocks when needed

This eliminates secret sprawl in CI/CD and simplifies module usage.

## AWS Pattern (SSM Parameter Store)

### Module A: Create placeholder (portal/devops module)

```hcl
# The value here is ignored - user populates manually
resource "aws_ssm_parameter" "github_app_id" {
  name  = "/github/app_id"
  type  = "String"
  value = "PLACEHOLDER"
  
  lifecycle {
    ignore_changes = [value]  # Don't overwrite manual updates
  }
}

resource "aws_ssm_parameter" "github_private_key" {
  name  = "/github/private_key"
  type  = "SecureString"
  value = "PLACEHOLDER"
  
  lifecycle {
    ignore_changes = [value]
  }
}
```

### Module B: Read and use (tenant module)

```hcl
data "aws_ssm_parameter" "github_app_id" {
  name = "/github/app_id"
}

data "aws_ssm_parameter" "github_private_key" {
  name            = "/github/private_key"
  with_decryption = true
}

provider "github" {
  owner = var.github_org
  app_auth {
    id              = data.aws_ssm_parameter.github_app_id.value
    installation_id = var.github_installation_id
    pem_file        = data.aws_ssm_parameter.github_private_key.value
  }
}
```

## GCP Pattern (Secret Manager)

### Module A: Create placeholder

```hcl
resource "google_secret_manager_secret" "github_app_id" {
  project   = module.ctx.account_id
  secret_id = "github-app-id"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "github_app_id" {
  secret      = google_secret_manager_secret.github_app_id.id
  secret_data = "PLACEHOLDER"
  
  lifecycle {
    ignore_changes = [secret_data]
  }
}
```

### Module B: Read and use

```hcl
data "google_secret_manager_secret_version" "github_app_id" {
  project = module.ctx.account_id
  secret  = "github-app-id"
}

# Use: data.google_secret_manager_secret_version.github_app_id.secret_data
```

## Duplocloud Tenant Secrets

For secrets scoped to a tenant:

### Create in shared module

```hcl
resource "duplocloud_tenant_secret" "db_credentials" {
  tenant_id   = module.tenant.id
  secret_name = "db-credentials"
  secret_data = jsonencode({
    host     = duplocloud_rds_instance.main.host
    port     = 5432
    username = "postgres"
    password = random_password.db.result
  })
}
```

### Read in app module

```hcl
data "duplocloud_tenant_secret" "db_credentials" {
  tenant_id   = local.shared.tenant_id
  secret_name = "db-credentials"
}

locals {
  db = jsondecode(data.duplocloud_tenant_secret.db_credentials.secret_data)
}

# Use: local.db.host, local.db.password, etc.
```

## Database Credentials Pattern

Shared module creates RDS + stores creds. App modules read creds for provider config:

```hcl
# In app module needing postgresql provider
locals {
  db = jsondecode(data.duplocloud_tenant_secret.db.secret_data)
}

provider "postgresql" {
  host     = local.db.host
  port     = local.db.port
  username = local.db.username
  password = local.db.password
  sslmode  = "require"
}
```

## Key Benefits

| Approach | Secrets in CI/CD | Module Complexity |
|----------|------------------|-------------------|
| Variables | Many | High (all secrets required upfront) |
| Data blocks | Only DUPLO_TOKEN | Low (self-discovering) |

## Workflow

1. Run portal/devops module → creates empty SSM/Secret Manager entries
2. Admin manually populates secrets (one-time setup)
3. All other modules read secrets via data blocks
4. CI/CD only needs `DUPLO_TOKEN`
