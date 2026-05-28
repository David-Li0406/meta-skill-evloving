# Serverless Containers Terraform Patterns

## Container Registry

```hcl
resource "yandex_container_registry" "main" {
  name      = "${local.resource_prefix}-registry"
  folder_id = var.yc_folder_id

  labels = {
    project     = var.project_name
    environment = var.environment
  }
}
```

## IAM for Container Registry

```hcl
# Pull images
resource "yandex_container_registry_iam_binding" "puller" {
  registry_id = yandex_container_registry.main.id
  role        = "container-registry.images.puller"
  members     = ["serviceAccount:${yandex_iam_service_account.storage_sa.id}"]
}

# Push images
resource "yandex_container_registry_iam_binding" "pusher" {
  registry_id = yandex_container_registry.main.id
  role        = "container-registry.images.pusher"
  members     = ["serviceAccount:${yandex_iam_service_account.storage_sa.id}"]
}
```

## Serverless Container

```hcl
resource "yandex_serverless_container" "main" {
  name               = "${local.resource_prefix}-my-container"
  folder_id          = var.yc_folder_id
  service_account_id = yandex_iam_service_account.storage_sa.id
  description        = "Container description"

  # Resource limits
  memory            = 2048  # MB
  cores             = 2     # CPU cores
  core_fraction     = 100   # % of CPU (100 = full core)
  execution_timeout = "600s"  # 10 minutes
  concurrency       = 4     # Max concurrent requests

  # Docker image
  image {
    url = "cr.yandex/${yandex_container_registry.main.id}/my-image:${var.image_tag}"

    # Environment variables
    environment = {
      YDB_CONNECTION_STRING = yandex_ydb_database_serverless.main.ydb_full_endpoint
      S3_ENDPOINT           = "https://storage.yandexcloud.net"
      S3_REGION             = "ru-central1"
      S3_BUCKET             = yandex_storage_bucket.main.bucket
      S3_ACCESS_KEY_ID      = yandex_iam_service_account_static_access_key.storage_key.access_key
      S3_SECRET_ACCESS_KEY  = yandex_iam_service_account_static_access_key.storage_key.secret_key
      YMQ_ENDPOINT          = "https://message-queue.api.cloud.yandex.net"
      YMQ_REGION            = "ru-central1"
      YMQ_ACCESS_KEY_ID     = yandex_iam_service_account_static_access_key.storage_key.access_key
      YMQ_SECRET_ACCESS_KEY = yandex_iam_service_account_static_access_key.storage_key.secret_key
    }
  }

  # Logging
  log_options {
    disabled = false
  }

  labels = {
    project     = var.project_name
    environment = var.environment
  }

  depends_on = [
    yandex_container_registry.main,
    yandex_container_registry_iam_binding.puller,
  ]
}
```

## Docker Image URL Format

```
cr.yandex/${registry_id}/${image_name}:${tag}
```

Example: `cr.yandex/crp123abc456/my-app:latest`

## Resource Sizing

| Workload | Memory | Cores | Timeout | Concurrency |
|----------|--------|-------|---------|-------------|
| Video Processing | 2048-4096 MB | 2 | 600s | 1-4 |
| Video Rendering | 4098-8192 MB | 2-4 | 300s | 1-2 |
| Image Processing | 1024-2048 MB | 1-2 | 120s | 4-8 |
| API Worker | 512-1024 MB | 1 | 60s | 8-16 |

## YMQ Trigger for Container

```hcl
resource "yandex_function_trigger" "container_trigger" {
  name        = "${local.resource_prefix}-container-trigger"
  description = "Trigger to invoke container from queue"

  message_queue {
    queue_id           = yandex_message_queue.tasks.arn
    service_account_id = yandex_iam_service_account.storage_sa.id
    batch_size         = 5
    batch_cutoff       = 10
  }

  container {
    id                 = yandex_serverless_container.main.id
    service_account_id = yandex_iam_service_account.storage_sa.id
    path               = "/process"  # Optional: specific path
  }
}
```

## Variables Pattern

```hcl
# Container Settings
variable "my_container_memory" {
  description = "Memory allocation in MB"
  type        = number
  default     = 2048
}

variable "my_container_cores" {
  description = "CPU cores"
  type        = number
  default     = 2
}

variable "my_container_timeout" {
  description = "Execution timeout (format: {number}s, e.g., 600s)"
  type        = string
  default     = "600s"
}

variable "my_container_concurrency" {
  description = "Max concurrent requests"
  type        = number
  default     = 4
}

variable "my_container_image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}
```

## Outputs

```hcl
# Container URL (for HTTP invokes)
output "my_container_url" {
  description = "Container invoke URL"
  value       = yandex_serverless_container.main.url
}

# Container ID (for monitoring)
output "my_container_id" {
  description = "Container ID"
  value       = yandex_serverless_container.main.id
}

# Registry ID (for Docker push)
output "container_registry_id" {
  description = "Container Registry ID"
  value       = yandex_container_registry.main.id
}
```

## Docker Build and Push

### CRITICAL: Platform

Yandex Cloud Serverless Containers support **only linux/amd64**.

**When building on Apple Silicon (ARM64) or other ARM platforms:**

```bash
# ALWAYS specify platform
docker build --platform=linux/amd64 -t my-image .
```

**Check architecture:**
```bash
docker inspect my-image --format='{{.Architecture}}'
# Should output: amd64
```

**Common Error:**
If image is built for arm64, Terraform apply will fail with:
```
ERROR: rpc error: code = Internal desc = Internal error
```

### Build and Push Process

```bash
# 1. Build with correct platform
docker build --platform=linux/amd64 -t my-image .

# 2. Tag for registry
docker tag my-image cr.yandex/${REGISTRY_ID}/my-image:latest

# 3. Login (if not logged in)
docker login --username oauth --password $(yc iam create-token) cr.yandex

# 4. Push
docker push cr.yandex/${REGISTRY_ID}/my-image:latest

# 5. Apply terraform
cd terraform && terraform apply
```

## Logging

```hcl
log_options {
  disabled = false

  # Optional: specific log group
  log_group_id = yandex_logging_group.main.id

  # Optional: minimum level
  min_level = "INFO"  # TRACE, DEBUG, INFO, WARN, ERROR, FATAL
}
```

## Common Pitfalls

1. **Wrong platform** - Always use `--platform=linux/amd64` when building on ARM
2. **Missing IAM bindings** - Container needs `container-registry.images.puller` role
3. **Timeout too short** - Video processing may need 600s+ timeout
4. **Memory too low** - Large videos need 4GB+ memory
5. **Forgot `depends_on`** - Add `depends_on` for registry and IAM bindings
6. **Wrong image URL format** - Must be `cr.yandex/${registry_id}/image:tag`
