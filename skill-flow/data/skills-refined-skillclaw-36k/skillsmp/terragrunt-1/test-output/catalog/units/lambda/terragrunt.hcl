include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  # Module in separate repo - use Git URL with version from values
  source = "git::git@github.com:YOUR_ORG/modules/lambda.git//app?ref=${values.version}"
}

# Optional dependency on S3 for deployment package
dependency "s3" {
  enabled      = try(values.use_s3_package, false)
  config_path  = try(values.s3_path, "../s3")
  mock_outputs = {
    s3_bucket_id  = "mock-bucket"
    s3_bucket_arn = "arn:aws:s3:::mock-bucket"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

# Optional dependency on VPC for VPC-enabled Lambda
dependency "vpc" {
  enabled      = try(values.vpc_enabled, false)
  config_path  = try(values.vpc_path, "../vpc")
  mock_outputs = {
    vpc_id          = "vpc-mock"
    private_subnets = ["subnet-mock1", "subnet-mock2"]
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  # Required inputs
  function_name = values.function_name
  handler       = values.handler
  runtime       = values.runtime

  # Source code location
  source_path = try(values.source_path, null)

  # S3 deployment package (if using S3)
  s3_bucket = try(values.use_s3_package, false) ? dependency.s3.outputs.s3_bucket_id : try(values.s3_bucket, null)
  s3_key    = try(values.s3_key, null)

  # Memory and timeout
  memory_size = try(values.memory_size, 128)
  timeout     = try(values.timeout, 30)

  # Environment variables
  environment_variables = try(values.environment_variables, {})

  # VPC configuration
  vpc_subnet_ids         = try(values.vpc_enabled, false) ? dependency.vpc.outputs.private_subnets : try(values.vpc_subnet_ids, null)
  vpc_security_group_ids = try(values.vpc_security_group_ids, null)

  # IAM role
  create_role = try(values.create_role, true)
  role_name   = try(values.role_name, null)

  # Layers
  layers = try(values.layers, [])

  # CloudWatch Logs
  cloudwatch_logs_retention_in_days = try(values.cloudwatch_logs_retention_in_days, 14)

  # Tags
  tags = try(values.tags, {})
}
