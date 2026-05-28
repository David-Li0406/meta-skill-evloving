---
name: yandex-cloud-terraform
description: Terraform IaC patterns for Yandex Cloud. Use when creating, modifying, or refactoring Terraform configurations for YDB, S3, Message Queue, Cloud Functions, API Gateway, or Serverless Containers. Provides resource patterns, naming conventions, and best practices from production projects.
---

# Terraform Yandex Cloud

## Quick Start

### Choose Structure

**Modular** (`environments/` + `modules/`): Multiple environments (dev/stage/prod), reusable components

**Flat** (functional files): Single environment, small-medium projects

### Essential Patterns

```hcl
# Resource naming with prefix
locals {
  resource_prefix = "${var.project_name}-${var.environment}"
}

# YDB tables require wait for database readiness
resource "time_sleep" "wait_for_database" {
  depends_on      = [yandex_ydb_database_serverless.this]
  create_duration = "30s"
}

# TTL on temporary data
ttl {
  column_name     = "expires_at"
  expire_interval = "PT0S"  # immediate
}

# Secondary index with concurrency guard
resource "yandex_ydb_table_index" "index2" {
  # ...
  depends_on = [yandex_ydb_table_index.index1]
}
```

## Common Tasks

- **Add YDB table**: See [YDB.md](references/YDB.md) for table patterns, TTL, indexes
- **Add S3 bucket**: See [S3.md](references/S3.md) for public/private buckets, lifecycle, CORS
- **Add Cloud Function**: See [FUNCTIONS.md](references/FUNCTIONS.md) for build+deploy patterns
- **Add Message Queue**: See [QUEUE.md](references/QUEUE.md) for DLQ and retry patterns
- **Add Serverless Container**: See [CONTAINERS.md](references/CONTAINERS.md) for Docker registry, triggers, sizing
- **IAM roles**: See [IAM.md](references/IAM.md) for common role combinations

## Key Pitfalls

1. YDB tables fail without `depends_on = [time_sleep.wait_for_database]`
2. Multiple indexes need sequential `depends_on` to avoid concurrent schema modifications
3. TTL format: `P5D` = 5 days, `PT0S` = immediate
4. Service accounts need explicit IAM role bindings
5. Functions need `user_hash` for redeployment triggers
6. **Docker images MUST be built with `--platform=linux/amd64`** (ARM images fail with "Internal error")
