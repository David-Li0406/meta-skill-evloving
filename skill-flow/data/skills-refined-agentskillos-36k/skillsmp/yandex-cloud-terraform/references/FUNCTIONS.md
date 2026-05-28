# Cloud Functions Terraform Patterns

## Function with Build

```hcl
# Build trigger based on source hash
resource "null_resource" "build_function" {
  triggers = {
    source_hash = sha256(join("", [
      for f in fileset("${path.module}/../src", "**/*.ts") :
      filesha256("${path.module}/../src/${f}")
    ]))
    package_hash = filesha256("${path.module}/../package.json")
  }

  provisioner "local-exec" {
    command     = "npm install && npm run build"
    working_dir = "${path.module}/../"
  }
}

# Archive built function
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../dist"
  output_path = "${path.module}/function.zip"

  depends_on = [null_resource.build_function]
}

# Create function
resource "yandex_function" "main" {
  name        = "${local.resource_prefix}-function"
  description = "Function description"
  user_hash   = data.archive_file.function_zip.output_sha256

  runtime           = "nodejs22"
  entrypoint        = "index.handler"
  memory            = 256
  execution_timeout = "30"

  service_account_id = yandex_iam_service_account.storage_sa.id

  environment = {
    YDB_CONNECTION_STRING = yandex_ydb_database_serverless.main.ydb_full_endpoint
    API_KEY                = var.api_key
  }

  content {
    zip_filename = data.archive_file.function_zip.output_path
  }

  labels = {
    project     = var.project_name
    environment = var.environment
  }
}
```

## Function Trigger (YMQ)

```hcl
resource "yandex_function_trigger" "task_result_trigger" {
  name        = "${var.function_name}-trigger"
  description = "Trigger for processing messages from queue"

  message_queue {
    queue_id           = yandex_message_queue.task_results.arn
    service_account_id = yandex_iam_service_account.storage_sa.id
    batch_size         = 5
    batch_cutoff       = 10
  }

  function {
    id                 = yandex_function.task_result_handler.id
    service_account_id = yandex_iam_service_account.storage_sa.id
    tag                = "$latest"
  }
}
```

## Cron Trigger

```hcl
resource "yandex_function_trigger" "scheduler" {
  name        = "${local.prefix}-scheduler-trigger"
  description = "Daily activity suggestions at 12:00 MSK (09:00 UTC)"

  function {
    id                 = yandex_cloud_function.scheduler.id
    service_account_id = yandex_iam_service_account.functions_sa.id
    tag                = "$latest"
  }

  timer {
    cron_expression = "0 9 * * ? *"  # 09:00 UTC = 12:00 MSK
  }
}
```

## Runtime Options

| Runtime | Description |
|---------|-------------|
| `nodejs16` | Node.js 16 |
| `nodejs18` | Node.js 18 |
| `nodejs20` | Node.js 20 |
| `nodejs22` | Node.js 22 |
| `python37` | Python 3.7 |
| `python38` | Python 3.8 |
| `python39` | Python 3.9 |
| `python310` | Python 3.10 |
| `python311` | Python 3.11 |
| `go119` | Go 1.19 |
| `go120` | Go 1.20 |
| `java11` | Java 11 |

## Memory/Timeout Options

```hcl
memory            = 128   # 128, 256, 512, 1024, 2048 MB
execution_timeout = "30"  # 1-600 seconds
```

## Environment Variables

```hcl
environment = {
  YDB_CONNECTION_STRING = yandex_ydb_database_serverless.main.ydb_full_endpoint
  YMQ_ACCESS_KEY_ID     = yandex_iam_service_account_static_access_key.storage_key.access_key
  YMQ_SECRET_ACCESS_KEY = yandex_iam_service_account_static_access_key.storage_key.secret_key
  YMQ_REGION            = "ru-central1"
  S3_BUCKET             = yandex_storage_bucket.main.id
  API_KEY               = var.api_key
}
```
