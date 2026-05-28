# Security & Compliance Reference

## Security Scanning Tools

### Trivy

Fast, comprehensive scanner for misconfigurations and CVEs.

```bash
# Scan Terraform directory
trivy config ./terraform/

# Scan with severity filter
trivy config --severity HIGH,CRITICAL ./terraform/

# JSON output for CI
trivy config --format json --output trivy-results.json ./terraform/

# Exit with error on findings
trivy config --exit-code 1 --severity HIGH,CRITICAL ./terraform/
```

#### Trivy Configuration

```yaml
# trivy.yaml
scan:
  scanners:
    - misconfig
  skip-dirs:
    - .terraform
    - examples

misconfig:
  terraform:
    vars:
      - terraform.tfvars
      - prod.tfvars

severity:
  - HIGH
  - CRITICAL
```

#### Trivy Ignore File

```yaml
# .trivyignore.yaml
misconfigs:
  - id: AVD-AWS-0057
    paths:
      - terraform/modules/legacy/**
    reason: "Legacy module, scheduled for refactor in Q2"
    expires: 2024-06-30

  - id: AVD-AWS-0089
    reason: "Public bucket is intentional for static website hosting"
```

### Checkov

Policy-as-code scanner with extensive rules.

```bash
# Basic scan
checkov -d ./terraform/

# Quiet mode (only failures)
checkov -d ./terraform/ --quiet

# Skip specific checks
checkov -d ./terraform/ --skip-check CKV_AWS_123,CKV_AWS_456

# Output formats
checkov -d ./terraform/ --output cli --output json --output-file-path results/

# With external checks
checkov -d ./terraform/ --external-checks-dir ./custom-policies/
```

#### Checkov Configuration

```yaml
# .checkov.yaml
branch: main
compact: true
directory:
  - terraform/
download-external-modules: true
evaluate-variables: true
framework:
  - terraform
  - terraform_plan
output:
  - cli
  - json
quiet: true
skip-check:
  - CKV_AWS_123  # Reason: Intentional public bucket
  - CKV_AWS_456  # Reason: Legacy infrastructure
soft-fail-on:
  - CKV_AWS_789  # Warning only
```

#### Custom Checkov Policy

```python
# custom-policies/ensure_encryption.py
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class EnsureS3Encryption(BaseResourceCheck):
    def __init__(self):
        name = "Ensure S3 bucket has encryption enabled"
        id = "CKV_CUSTOM_1"
        supported_resources = ['aws_s3_bucket']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, 
                         supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if 'server_side_encryption_configuration' in conf:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = EnsureS3Encryption()
```

### tfsec (Now part of Trivy)

```bash
# Basic scan
tfsec ./terraform/

# Exclude specific rules
tfsec ./terraform/ --exclude aws-s3-enable-versioning

# Custom severity threshold
tfsec ./terraform/ --minimum-severity HIGH

# Ignore file
# .tfsec/config.yml
```

---

## Secrets Management

### Never Store Secrets in Terraform

```hcl
# ❌ NEVER: Hardcoded secrets
resource "aws_db_instance" "main" {
  password = "MySecretPassword123!"  # Stored in state file!
}

# ❌ NEVER: Secrets in tfvars
# terraform.tfvars
db_password = "MySecretPassword123!"

# ❌ NEVER: Environment variables for secrets
variable "db_password" {
  default = ""  # Sourced from TF_VAR_db_password
}
```

### Recommended: External Secret Stores

```hcl
# ✅ AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}

# ✅ HashiCorp Vault
data "vault_generic_secret" "db_password" {
  path = "secret/prod/db"
}

resource "aws_db_instance" "main" {
  password = data.vault_generic_secret.db_password.data["password"]
}

# ✅ AWS SSM Parameter Store
data "aws_ssm_parameter" "db_password" {
  name            = "/prod/db/password"
  with_decryption = true
}

resource "aws_db_instance" "main" {
  password = data.aws_ssm_parameter.db_password.value
}
```

### Ephemeral Variables (Terraform 1.10+)

```hcl
# Variables marked ephemeral are never written to state
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  ephemeral   = true  # Never persisted to state
}

# Write-only attributes (1.11+)
resource "aws_db_instance" "main" {
  # Password is write-only, not readable from state
  password = var.db_password
}
```

### Random Password Generation

```hcl
# Generate password with Terraform
resource "random_password" "db" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Store in Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "prod/db/password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

# Use in database
resource "aws_db_instance" "main" {
  password = random_password.db.result
}
```

---

## State Security

### Remote State Configuration

```hcl
# backend.tf - S3 with encryption and locking
terraform {
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "prod/infrastructure/terraform.tfstate"
    region         = "us-east-1"
    
    # Encryption
    encrypt        = true
    kms_key_id     = "alias/terraform-state"
    
    # Locking
    dynamodb_table = "terraform-state-lock"
    
    # Access control
    role_arn       = "arn:aws:iam::123456789:role/TerraformStateAccess"
    
    # Prevent accidental deletion
    skip_metadata_api_check = false
  }
}
```

### State Bucket Security

```hcl
# S3 bucket for state storage
resource "aws_s3_bucket" "terraform_state" {
  bucket = "myorg-terraform-state"

  # Prevent accidental deletion
  lifecycle {
    prevent_destroy = true
  }
}

# Enable versioning
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.terraform_state.arn
    }
    bucket_key_enabled = true
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# DynamoDB for locking
resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  # Enable point-in-time recovery
  point_in_time_recovery {
    enabled = true
  }
}
```

### State Access Control

```hcl
# IAM policy for state access
resource "aws_iam_policy" "terraform_state_access" {
  name        = "TerraformStateAccess"
  description = "Allows access to Terraform state"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3StateAccess"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "${aws_s3_bucket.terraform_state.arn}/*"
        ]
      },
      {
        Sid    = "S3ListBucket"
        Effect = "Allow"
        Action = "s3:ListBucket"
        Resource = aws_s3_bucket.terraform_state.arn
      },
      {
        Sid    = "DynamoDBLocking"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem"
        ]
        Resource = aws_dynamodb_table.terraform_lock.arn
      },
      {
        Sid    = "KMSDecrypt"
        Effect = "Allow"
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = aws_kms_key.terraform_state.arn
      }
    ]
  })
}
```

---

## Compliance Frameworks

### CIS AWS Foundations Benchmark

```hcl
# Common CIS requirements
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"

  # CIS 2.1.1: Ensure S3 Bucket Policy denies HTTP requests
  # CIS 2.1.2: Ensure MFA Delete is enabled
}

resource "aws_s3_bucket_policy" "deny_http" {
  bucket = aws_s3_bucket.example.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "DenyHTTP"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.example.arn,
          "${aws_s3_bucket.example.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
```

### SOC 2 Requirements

```hcl
# Logging and monitoring
resource "aws_cloudtrail" "main" {
  name                          = "main-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true  # SOC 2 CC6.1
  kms_key_id                    = aws_kms_key.cloudtrail.arn

  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }
}

# Access reviews
resource "aws_config_config_rule" "iam_user_unused_credentials" {
  name = "iam-user-unused-credentials-check"

  source {
    owner             = "AWS"
    source_identifier = "IAM_USER_UNUSED_CREDENTIALS_CHECK"
  }

  input_parameters = jsonencode({
    maxCredentialUsageAge = "90"  # SOC 2 CC6.2
  })
}
```

---

## Security Checklist

Before deploying infrastructure:

### State Security
- [ ] Remote state with encryption enabled
- [ ] State locking with DynamoDB
- [ ] State bucket versioning enabled
- [ ] State bucket public access blocked
- [ ] IAM roles with least privilege

### Secrets
- [ ] No hardcoded secrets in code
- [ ] No secrets in tfvars files
- [ ] Using external secret stores
- [ ] Sensitive outputs marked `sensitive = true`
- [ ] Ephemeral variables for credentials (1.10+)

### Scanning
- [ ] Trivy scan passes (HIGH/CRITICAL)
- [ ] Checkov scan passes
- [ ] Pre-commit hooks configured
- [ ] CI/CD security gates in place

### Network
- [ ] Security groups with minimal rules
- [ ] No 0.0.0.0/0 ingress (except LB)
- [ ] VPC flow logs enabled
- [ ] Private subnets for databases

### Encryption
- [ ] S3 buckets encrypted
- [ ] RDS encryption enabled
- [ ] EBS volumes encrypted
- [ ] TLS for all endpoints

### Logging
- [ ] CloudTrail enabled
- [ ] VPC flow logs enabled
- [ ] Application logging configured
- [ ] Log retention policies set
