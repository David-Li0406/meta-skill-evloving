# IAM Roles Terraform Patterns

## Service Account Creation

```hcl
resource "yandex_iam_service_account" "main" {
  name        = "${local.resource_prefix}-sa"
  description = "Service account for application"
  folder_id   = var.folder_id
}
```

## Static Access Keys

```hcl
resource "yandex_iam_service_account_static_access_key" "main" {
  service_account_id = yandex_iam_service_account.main.id
  description        = "Static key for S3/YMQ access"
}
```

## Common IAM Roles

### Storage Roles

```hcl
# Full S3 access
resource "yandex_resourcemanager_folder_iam_member" "storage_editor" {
  folder_id = var.folder_id
  role      = "storage.editor"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}

# Read-only S3 access
resource "yandex_resourcemanager_folder_iam_member" "storage_viewer" {
  folder_id = var.folder_id
  role      = "storage.viewer"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}
```

### Message Queue Roles

```hcl
# Full YMQ access
resource "yandex_resourcemanager_folder_iam_member" "ymq_admin" {
  folder_id = var.folder_id
  role      = "ymq.admin"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}

# Write-only access
resource "yandex_resourcemanager_folder_iam_member" "ymq_writer" {
  folder_id = var.folder_id
  role      = "ymq.writer"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}
```

### YDB Roles

```hcl
# Full YDB access
resource "yandex_resourcemanager_folder_iam_member" "ydb_editor" {
  folder_id = var.folder_id
  role      = "ydb.editor"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}

# Read-only YDB access
resource "yandex_resourcemanager_folder_iam_member" "ydb_viewer" {
  folder_id = var.folder_id
  role      = "ydb.viewer"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}
```

### Serverless Roles

```hcl
# Invoke Cloud Functions
resource "yandex_resourcemanager_folder_iam_member" "functions_invoker" {
  folder_id = var.folder_id
  role      = "serverless.functions.invoker"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}

# Invoke Containers
resource "yandex_resourcemanager_folder_iam_member" "containers_invoker" {
  folder_id = var.folder_id
  role      = "serverless.containers.invoker"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}
```

### Lockbox Roles

```hcl
# Read secrets from Lockbox
resource "yandex_resourcemanager_folder_iam_member" "lockbox_viewer" {
  folder_id = var.folder_id
  role      = "lockbox.payloadViewer"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}
```

### Service Account Roles

```hcl
# Allow using this service account
resource "yandex_resourcemanager_folder_iam_member" "sa_user" {
  folder_id = var.folder_id
  role      = "iam.serviceAccounts.user"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}

# Allow creating IAM tokens
resource "yandex_resourcemanager_folder_iam_member" "token_creator" {
  folder_id = var.folder_id
  role      = "iam.serviceAccounts.tokenCreator"
  member    = "serviceAccount:${yandex_iam_service_account.main.id}"
}
```

## Role Reference Table

| Role | Description | Use Case |
|------|-------------|----------|
| `storage.editor` | Full S3 access | Upload/download files |
| `storage.viewer` | Read-only S3 | Download only |
| `ymq.admin` | Full YMQ access | Queue operations |
| `ymq.writer` | Write-only YMQ | Send messages |
| `ydb.editor` | Full YDB access | Database operations |
| `ydb.viewer` | Read-only YDB | Read from database |
| `serverless.functions.invoker` | Invoke functions | Trigger functions |
| `serverless.containers.invoker` | Invoke containers | Trigger containers |
| `lockbox.payloadViewer` | Read secrets | Access Lockbox |
| `iam.serviceAccounts.user` | Use SA | Containers/functions use SA |
| `iam.serviceAccounts.tokenCreator` | Create tokens | Programmatic auth |

## Common Role Combinations

### For Cloud Functions

```hcl
# Functions need YDB access, Lockbox access, and YMQ write
resource "yandex_resourcemanager_folder_iam_member" "ydb_editor" {
  role   = "ydb.editor"
  member = "serviceAccount:${yandex_iam_service_account.functions_sa.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "lockbox_viewer" {
  role   = "lockbox.payloadViewer"
  member = "serviceAccount:${yandex_iam_service_account.functions_sa.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "ymq_writer" {
  role   = "ymq.writer"
  member = "serviceAccount:${yandex_iam_service_account.functions_sa.id}"
}
```

### For API Gateway

```hcl
# API Gateway needs to invoke functions and containers
resource "yandex_resourcemanager_folder_iam_member" "functions_invoker" {
  role   = "serverless.functions.invoker"
  member = "serviceAccount:${yandex_iam_service_account.apigw_sa.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "containers_invoker" {
  role   = "serverless.containers.invoker"
  member = "serviceAccount:${yandex_iam_service_account.apigw_sa.id}"
}
```

### For Storage Operations

```hcl
# S3/YMQ with static keys
resource "yandex_resourcemanager_folder_iam_member" "storage_editor" {
  role   = "storage.editor"
  member = "serviceAccount:${yandex_iam_service_account.storage_sa.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "ymq_admin" {
  role   = "ymq.admin"
  member = "serviceAccount:${yandex_iam_service_account.storage_sa.id}"
}
```
