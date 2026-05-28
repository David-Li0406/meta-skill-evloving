# Infrastructure As Code - Validations

## Local Backend Configuration

### **Id**
iac-local-backend
### **Severity**
error
### **Type**
regex
### **Pattern**
  - backend\\s+"local"
  - backend\\s*\\{\\s*\\}
### **Message**
Local backend detected. Use remote backend with locking for team environments.
### **Fix Action**
Configure S3+DynamoDB, GCS, Azure Blob, or Terraform Cloud backend
### **Applies To**
  - *.tf
  - backend.tf

## Provider Without Version Constraint

### **Id**
iac-no-provider-version
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - required_providers\\s*\\{[^}]*source\\s*=[^}]*(?!version)[^}]*\\}
### **Message**
Provider without version constraint can cause unexpected changes.
### **Fix Action**
Add version = "~> X.0" to pin major version
### **Applies To**
  - *.tf
  - versions.tf
  - providers.tf

## Hardcoded Secret in Terraform

### **Id**
iac-hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password\\s*=\\s*"[^"$]+
  - api_key\\s*=\\s*"[^"$]+
  - secret\\s*=\\s*"[^"$]+
  - token\\s*=\\s*"[^"$]+
  - AWS_SECRET_ACCESS_KEY\\s*=\\s*"
### **Message**
Hardcoded secret detected. Secrets end up in state file unencrypted.
### **Fix Action**
Use data sources to fetch from AWS Secrets Manager, Vault, or similar
### **Applies To**
  - *.tf
  - *.tfvars

## Wildcard IAM Permissions

### **Id**
iac-wildcard-iam
### **Severity**
error
### **Type**
regex
### **Pattern**
  - "Action"\\s*:\\s*"\\*"
  - "Action"\\s*:\\s*\\[\\s*"\\*"\\s*\\]
  - "Resource"\\s*:\\s*"\\*"
  - AdministratorAccess
  - PowerUserAccess
### **Message**
Overly broad IAM permissions detected. Follow least privilege principle.
### **Fix Action**
Scope actions and resources to only what's needed
### **Applies To**
  - *.tf
  - *.json

## Storage Without Encryption

### **Id**
iac-no-encryption
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - aws_s3_bucket\\s*"[^"]*"\\s*\\{(?![^}]*server_side_encryption)
  - aws_ebs_volume\\s*"[^"]*"\\s*\\{(?![^}]*encrypted)
  - aws_rds_instance\\s*"[^"]*"\\s*\\{(?![^}]*storage_encrypted)
### **Message**
Storage resource without encryption enabled.
### **Fix Action**
Add encryption configuration to S3, EBS, or RDS resources
### **Applies To**
  - *.tf

## Public Access Enabled

### **Id**
iac-public-access
### **Severity**
error
### **Type**
regex
### **Pattern**
  - publicly_accessible\\s*=\\s*true
  - cidr_blocks\\s*=\\s*\\[\\s*"0\\.0\\.0\\.0/0"\\s*\\]
  - block_public_acls\\s*=\\s*false
  - block_public_policy\\s*=\\s*false
### **Message**
Resource configured with public access. Review if intentional.
### **Fix Action**
Remove public access or add explicit comment justifying it
### **Applies To**
  - *.tf

## Stateful Resource Without Destroy Protection

### **Id**
iac-no-prevent-destroy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - aws_rds_instance\\s*"[^"]*"\\s*\\{(?![^}]*prevent_destroy)
  - aws_db_instance\\s*"[^"]*"\\s*\\{(?![^}]*prevent_destroy)
  - aws_s3_bucket\\s*"[^"]*prod[^"]*"\\s*\\{(?![^}]*prevent_destroy)
### **Message**
Stateful resource without lifecycle.prevent_destroy protection.
### **Fix Action**
Add lifecycle { prevent_destroy = true } and deletion_protection = true
### **Applies To**
  - *.tf

## Module Without Version Pin

### **Id**
iac-module-no-version
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - module\\s*"[^"]*"\\s*\\{[^}]*source\\s*=\\s*"[^"?]*"(?![^}]*version)
  - source\\s*=\\s*"git::[^"]*(?!\\?ref=)
### **Message**
Module source without version pin can cause inconsistent behavior.
### **Fix Action**
Add version constraint for registry modules or ?ref= for Git sources
### **Applies To**
  - *.tf

## Count Used for Distinct Resources

### **Id**
iac-count-for-distinct
### **Severity**
info
### **Type**
regex
### **Pattern**
  - count\\s*=\\s*length\\(
### **Message**
count with length() can cause index shifting when items removed.
### **Fix Action**
Consider using for_each with map/set for stable resource addresses
### **Applies To**
  - *.tf

## Auto-Approve in Production Pipeline

### **Id**
iac-auto-approve-prod
### **Severity**
error
### **Type**
regex
### **Pattern**
  - terraform\\s+apply\\s+-auto-approve
  - terraform\\s+destroy\\s+-auto-approve
### **Message**
Auto-approve bypasses plan review. Dangerous in production.
### **Fix Action**
Use terraform plan -out=plan.tfplan then terraform apply plan.tfplan with review
### **Applies To**
  - *.yml
  - *.yaml
  - *.sh
  - Makefile

## Backend Without Encryption

### **Id**
iac-no-state-encryption
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backend\\s+"s3"\\s*\\{(?![^}]*encrypt\\s*=\\s*true)
### **Message**
S3 backend without encryption. State file contains sensitive data.
### **Fix Action**
Add encrypt = true and consider kms_key_id for additional security
### **Applies To**
  - *.tf
  - backend.tf

## S3 Backend Without DynamoDB Locking

### **Id**
iac-no-dynamodb-lock
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backend\\s+"s3"\\s*\\{(?![^}]*dynamodb_table)
### **Message**
S3 backend without DynamoDB locking. Concurrent applies can corrupt state.
### **Fix Action**
Add dynamodb_table for state locking
### **Applies To**
  - *.tf
  - backend.tf

## Workspace Used for Production

### **Id**
iac-terraform-workspace-prod
### **Severity**
info
### **Type**
regex
### **Pattern**
  - terraform\\.workspace\\s*==\\s*"prod
  - workspace\\s+select\\s+prod
### **Message**
Workspaces for environment separation can be error-prone.
### **Fix Action**
Consider directory-based environment separation for stronger isolation
### **Applies To**
  - *.tf
  - *.sh