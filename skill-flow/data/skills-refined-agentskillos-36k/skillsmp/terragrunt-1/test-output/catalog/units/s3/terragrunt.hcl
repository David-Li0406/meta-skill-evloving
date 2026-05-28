include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  # Module in separate repo - use Git URL with version from values
  source = "git::git@github.com:YOUR_ORG/modules/s3.git//app?ref=${values.version}"
}

inputs = {
  # Required inputs from values
  bucket = values.bucket

  # Optional inputs with defaults
  force_destroy = try(values.force_destroy, false)

  # Versioning configuration
  versioning = try(values.versioning, {
    status = "Enabled"
  })

  # Server-side encryption
  server_side_encryption_configuration = try(values.server_side_encryption_configuration, {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
      bucket_key_enabled = true
    }
  })

  # Public access block (secure defaults)
  block_public_acls       = try(values.block_public_acls, true)
  block_public_policy     = try(values.block_public_policy, true)
  ignore_public_acls      = try(values.ignore_public_acls, true)
  restrict_public_buckets = try(values.restrict_public_buckets, true)

  # Lifecycle rules
  lifecycle_rule = try(values.lifecycle_rule, [])

  # CORS configuration
  cors_rule = try(values.cors_rule, [])

  # Tags
  tags = try(values.tags, {})
}
