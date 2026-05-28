# Database Pattern

**When to use:** Setting up databases in shared tenant with access from child tenants.

## Overview

1. Shared tenant creates database with Duplocloud provider
2. Credentials stored as tenant secret
3. Child tenants inherit access via `parent` + `security_rules`
4. App modules read credentials via data block, configure postgresql provider

## Parent-Child Tenant Relationship

Tenants can be children of shared to inherit network access:

```hcl
# modules/tenant/tenant.tf
module "tenant" {
  source  = "duplocloud/components/duplocloud//modules/tenant-gh-aws"
  version = "0.0.36"
  parent  = var.shared  # Makes this tenant a child of shared
  
  # Allow access to parent's database port
  security_rules = [{
    to_port = nonsensitive(local.db_creds.port)
  }]
  
  # Grant S3 access to parent's buckets
  grants = [{
    area = "s3"
  }]
  
  settings = {
    enable_service_on_any_host = "true"
    delete_protection          = "true"
  }
}
```

## Database Resources

Create databases in shared module using Duplocloud provider:

| Cloud | Resource |
|-------|----------|
| AWS | [duplocloud_rds_instance](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/rds_instance) |
| Azure | [duplocloud_azure_mssql_database](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/azure_mssql_database) |
| GCP | [duplocloud_gcp_sql_database_instance](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/gcp_sql_database_instance) |

### AWS RDS Example

```hcl
# modules/shared/rds.tf
resource "random_password" "db" {
  length  = 24
  special = false
}

resource "duplocloud_rds_instance" "main" {
  tenant_id       = module.tenant.id
  name            = "main"
  engine          = 1  # PostgreSQL
  engine_version  = var.rds.engine_version
  size            = var.rds.instance_class
  encrypt_storage = true
  master_username = "postgres"
  master_password = random_password.db.result
}
```

## Storing Credentials as Secrets

Store credentials in tenant secret for downstream access:

```hcl
# modules/shared/secrets.tf
resource "duplocloud_tenant_secret" "db_credentials" {
  tenant_id   = module.tenant.id
  secret_name = "db-credentials"
  secret_data = jsonencode({
    host     = duplocloud_rds_instance.main.host
    port     = 5432
    username = duplocloud_rds_instance.main.master_username
    password = random_password.db.result
    database = "postgres"
  })
}
```

Secret resources:
- [duplocloud_tenant_secret](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/tenant_secret)
- [duplocloud_k8_secret](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/k8_secret)

## Reading Credentials in Downstream Modules

App or tenant modules read credentials via data block:

```hcl
# modules/tenant/main.tf or modules/myapp/main.tf
data "duplocloud_tenant_secret" "db" {
  tenant_id   = local.shared.tenant_id
  secret_name = "db-credentials"
}

locals {
  db_creds = jsondecode(data.duplocloud_tenant_secret.db.secret_data)
}
```

## PostgreSQL Provider Configuration

Configure postgresql provider for app-specific database operations:

```hcl
# modules/myapp/providers.tf
provider "postgresql" {
  host     = local.db_creds.host
  port     = local.db_creds.port
  username = local.db_creds.username
  password = local.db_creds.password
  sslmode  = "require"
}
```

Create app-specific database:

```hcl
# modules/myapp/database.tf
resource "postgresql_database" "app" {
  name  = local.name
  owner = local.db_creds.username
}

resource "postgresql_role" "app" {
  name     = "${local.name}_user"
  login    = true
  password = random_password.app_db.result
}
```

## Flow Diagram

```
shared module
├── Creates RDS instance
├── Stores creds in duplocloud_tenant_secret
└── Exports tenant_id in outputs

tenant module  
├── parent = var.shared (inherits network access)
├── security_rules = [{ to_port = db_port }]
├── Reads db creds via data block
└── Passes to child apps via outputs

app module
├── Reads creds from tenant or shared
├── Configures postgresql provider
└── Creates app-specific database/roles
```

## Key Points

- **No secrets in variables** - Only DUPLO_TOKEN needed
- **Parent relationship** - Enables security_rules to work
- **JIT not needed for secrets** - duplocloud_tenant_secret data source works with DUPLO_TOKEN
- **Credentials flow down** - shared → tenant → app via data blocks
