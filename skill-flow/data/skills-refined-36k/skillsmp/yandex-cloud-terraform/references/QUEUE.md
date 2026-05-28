# Message Queue (YMQ) Terraform Patterns

## Queue with Dead Letter Queue

```hcl
# Main queue
resource "yandex_message_queue" "main" {
  name        = "${local.resource_prefix}-tasks"
  folder_id   = var.yc_folder_id
  access_key  = yandex_iam_service_account_static_access_key.storage_key.access_key
  secret_key  = yandex_iam_service_account_static_access_key.storage_key.secret_key

  message_retention = 1209600  # 14 days in seconds

  # DLQ for failed messages - 3 retry attempts before DLQ
  redrive_policy = jsonencode({
    deadLetterTargetArn = yandex_message_queue.dlq.arn
    maxReceiveCount     = 3
  })
}

# Dead Letter Queue
resource "yandex_message_queue" "dlq" {
  name        = "${local.resource_prefix}-tasks-dlq"
  folder_id   = var.yc_folder_id
  access_key  = yandex_iam_service_account_static_access_key.storage_key.access_key
  secret_key  = yandex_iam_service_account_static_access_key.storage_key.secret_key

  message_retention = 1209600  # 14 days
}
```

## Queue Settings

```hcl
resource "yandex_message_queue" "main" {
  name             = "${local.resource_prefix}-webhook"
  folder_id        = var.yc_folder_id
  access_key       = var.access_key
  secret_key       = var.secret_key

  # How long messages are stored (seconds)
  message_retention = 345600  # 4 days

  # How long message is hidden after being received (seconds)
  visibility_timeout = 60

  # Wait time for long polling (seconds)
  receive_wait_time = 20

  # Maximum message size (bytes)
  max_message_size = 262144  # 256 KB
}
```

## Retention Period Examples

| Value | Seconds | Description |
|-------|---------|-------------|
| 1 day | 86400 | Short-lived queue |
| 4 days | 345600 | Development |
| 7 days | 604800 | Standard |
| 14 days | 1209600 | Production with DLQ |

## Static Access Key Pattern

```hcl
# Service account for queue operations
resource "yandex_iam_service_account" "queue" {
  name        = "${local.resource_prefix}-queue-sa"
  folder_id   = var.folder_id
  description = "Service account for message queue operations"
}

# Grant YMQ admin role
resource "yandex_resourcemanager_folder_iam_member" "queue_admin" {
  folder_id = var.folder_id
  role      = "ymq.admin"
  member    = "serviceAccount:${yandex_iam_service_account.queue.id}"
}

# Create static access key
resource "yandex_iam_service_account_static_access_key" "queue" {
  service_account_id = yandex_iam_service_account.queue.id
  description        = "Static access key for YMQ"
}

# Use in queue
resource "yandex_message_queue" "main" {
  access_key = yandex_iam_service_account_static_access_key.queue.access_key
  secret_key = yandex_iam_service_account_static_access_key.queue.secret_key
}
```

## Common Queue Patterns

### Webhook Queue (High Throughput)

```hcl
resource "yandex_message_queue" "webhook" {
  name              = "${local.prefix}-webhook"
  folder_id         = var.folder_id
  access_key        = var.access_key
  secret_key        = var.secret_key

  visibility_timeout = 30   # Short timeout for quick processing
  message_retention  = 345600  # 4 days
  receive_wait_time  = 20   # Long polling
}
```

### Background Tasks Queue

```hcl
resource "yandex_message_queue" "tasks" {
  name              = "${local.prefix}-tasks"
  folder_id         = var.folder_id
  access_key        = var.access_key
  secret_key        = var.secret_key

  visibility_timeout = 300  # 5 minutes for long-running tasks
  message_retention  = 604800  # 7 days
  receive_wait_time  = 20
}
```

### Result Queue

```hcl
resource "yandex_message_queue" "results" {
  name              = "${local.prefix}-results"
  folder_id         = var.folder_id
  access_key        = var.access_key
  secret_key        = var.secret_key

  visibility_timeout = 60
  message_retention  = 1209600  # 14 days for audit trail
  receive_wait_time  = 10
}
```
