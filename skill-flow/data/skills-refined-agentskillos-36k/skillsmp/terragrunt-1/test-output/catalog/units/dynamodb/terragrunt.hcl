include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  # Module in separate repo - use Git URL with version from values
  source = "git::git@github.com:YOUR_ORG/modules/dynamodb.git//app?ref=${values.version}"
}

inputs = {
  # Required inputs
  name     = values.name
  hash_key = values.hash_key

  # Optional range key
  range_key = try(values.range_key, null)

  # Attributes
  attributes = values.attributes

  # Billing mode (PAY_PER_REQUEST or PROVISIONED)
  billing_mode = try(values.billing_mode, "PAY_PER_REQUEST")

  # Provisioned capacity (only if billing_mode = PROVISIONED)
  read_capacity  = try(values.read_capacity, null)
  write_capacity = try(values.write_capacity, null)

  # Auto-scaling (only if billing_mode = PROVISIONED)
  autoscaling_enabled = try(values.autoscaling_enabled, false)
  autoscaling_read    = try(values.autoscaling_read, null)
  autoscaling_write   = try(values.autoscaling_write, null)

  # Global Secondary Indexes
  global_secondary_indexes = try(values.global_secondary_indexes, [])

  # Local Secondary Indexes
  local_secondary_indexes = try(values.local_secondary_indexes, [])

  # Encryption
  server_side_encryption_enabled     = try(values.server_side_encryption_enabled, true)
  server_side_encryption_kms_key_arn = try(values.server_side_encryption_kms_key_arn, null)

  # Point-in-time recovery
  point_in_time_recovery_enabled = try(values.point_in_time_recovery_enabled, true)

  # TTL
  ttl_enabled        = try(values.ttl_enabled, false)
  ttl_attribute_name = try(values.ttl_attribute_name, null)

  # Stream
  stream_enabled   = try(values.stream_enabled, false)
  stream_view_type = try(values.stream_view_type, null)

  # Tags
  tags = try(values.tags, {})
}
