# YDB Terraform Patterns

## Table Creation

### Basic Table

```hcl
resource "yandex_ydb_table" "users" {
  path              = "users"
  connection_string = yandex_ydb_database_serverless.this.ydb_full_endpoint

  column {
    name     = "user_id"
    type     = "Int64"
    not_null = true
  }

  column {
    name     = "username"
    type     = "Utf8"
    not_null = true
  }

  column {
    name     = "created_at"
    type     = "Utf8"
    not_null = true
  }

  primary_key = ["user_id"]

  depends_on = [time_sleep.wait_for_database]
}
```

### TTL (Time To Live)

```hcl
# TTL based on timestamp column - expire immediately when time reached
resource "yandex_ydb_table" "invites" {
  # ... columns ...

  column {
    name     = "expires_at"
    type     = "Timestamp"
    not_null = true
  }

  ttl {
    column_name     = "expires_at"
    expire_interval = "PT0S"  # Expire immediately when expires_at is reached
  }

  depends_on = [time_sleep.wait_for_database]
}

# TTL with duration from creation time
resource "yandex_ydb_table" "daily_activity_pools" {
  # ... columns ...

  column {
    name     = "created_at"
    type     = "Timestamp"
    not_null = true
  }

  ttl {
    column_name     = "created_at"
    expire_interval = "P5D"  # 5 days TTL
  }

  depends_on = [time_sleep.wait_for_database]
}
```

### Secondary Indexes

```hcl
# Index for lookups by non-primary key
resource "yandex_ydb_table_index" "pairs_user1_idx" {
  table_path        = yandex_ydb_table.pairs.path
  connection_string = yandex_ydb_database_serverless.this.ydb_full_endpoint
  name              = "user1_id_idx"
  type              = "global_async"  # or "global_sync"
  columns           = ["user1_id"]
}

# IMPORTANT: Multiple indexes on same table require depends_on
# YDB doesn't allow concurrent schema modifications on the same table
resource "yandex_ydb_table_index" "pairs_user2_idx" {
  table_path        = yandex_ydb_table.pairs.path
  connection_string = yandex_ydb_database_serverless.this.ydb_full_endpoint
  name              = "user2_id_idx"
  type              = "global_async"
  columns           = ["user2_id"]

  depends_on = [yandex_ydb_table_index.pairs_user1_idx]
}
```

## Column Types

| Type | Description | Example |
|------|-------------|---------|
| `Int64`, `Int32`, `Int8` | Signed integers | `user_id: Int64` |
| `Uint64`, `Uint32`, `Uint8` | Unsigned integers | `count: Uint32` |
| `Utf8` | String | `username: Utf8` |
| `Bool` | Boolean | `is_active: Bool` |
| `Timestamp` | DateTime | `created_at: Timestamp` |
| `Json` | JSON document | `metadata: Json` |
| `Double` | Float | `price: Double` |

## TTL Duration Format

ISO 8601 duration format:
- `PT0S` - Immediate (0 seconds)
- `PT1H` - 1 hour
- `P1D` - 1 day
- `P5D` - 5 days
- `P7D` - 7 days
- `P30D` - 30 days

Pattern: `P[n]DT[n]H[n]M[n]S` (days, hours, minutes, seconds)

## Common Patterns

### Junction Table (Many-to-Many)

```hcl
resource "yandex_ydb_table" "activity_categories" {
  path              = "activity_categories"
  connection_string = yandex_ydb_database_serverless.this.ydb_full_endpoint

  column {
    name     = "activity_id"
    type     = "Utf8"
    not_null = true
  }

  column {
    name     = "category_id"
    type     = "Utf8"
    not_null = true
  }

  primary_key = ["activity_id", "category_id"]

  depends_on = [time_sleep.wait_for_database]
}

# Index for reverse lookup
resource "yandex_ydb_table_index" "activity_categories_category_idx" {
  table_path        = yandex_ydb_table.activity_categories.path
  connection_string = yandex_ydb_database_serverless.this.ydb_full_endpoint
  name              = "category_id_idx"
  type              = "global_async"
  columns           = ["category_id"]
}
```

### Database with Wait Pattern

```hcl
resource "yandex_ydb_database_serverless" "this" {
  name        = var.database_name
  folder_id   = var.folder_id
  description = var.description

  serverless_database {
    storage_size_limit = var.storage_size_limit_gb
  }

  labels = var.labels
}

# Wait for database to be fully ready
resource "time_sleep" "wait_for_database" {
  depends_on      = [yandex_ydb_database_serverless.this]
  create_duration = "30s"
}

# All tables reference time_sleep
resource "yandex_ydb_table" "users" {
  # ...
  depends_on = [time_sleep.wait_for_database]
}
```
