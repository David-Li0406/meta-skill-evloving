# Infrastructure as Code

## Patterns


---
  #### **Name**
Remote State with Locking
  #### **Description**
Store state in a remote backend with locking to prevent concurrent corruption
  #### **When**
Any team environment, CI/CD pipelines, or production workloads
  #### **Example**
    # AWS S3 + DynamoDB backend
    terraform {
      backend "s3" {
        bucket         = "my-terraform-state"
        key            = "prod/networking/terraform.tfstate"
        region         = "us-east-1"
        encrypt        = true
        dynamodb_table = "terraform-state-lock"
      }
    }
    
    # Create the lock table first
    resource "aws_dynamodb_table" "terraform_lock" {
      name         = "terraform-state-lock"
      billing_mode = "PAY_PER_REQUEST"
      hash_key     = "LockID"
    
      attribute {
        name = "LockID"
        type = "S"
      }
    }
    

---
  #### **Name**
Environment Separation
  #### **Description**
Separate state files per environment to limit blast radius
  #### **When**
Managing dev/staging/production environments
  #### **Example**
    # Directory structure (recommended over workspaces)
    environments/
      dev/
        main.tf
        backend.tf    # key = "dev/terraform.tfstate"
      staging/
        main.tf
        backend.tf    # key = "staging/terraform.tfstate"
      prod/
        main.tf
        backend.tf    # key = "prod/terraform.tfstate"
    modules/
      networking/
      compute/
      database/
    
    # Each environment has its own state
    # Mistake in dev cannot affect prod state
    

---
  #### **Name**
Composable Modules
  #### **Description**
Small, focused modules that do one thing well
  #### **When**
Any reusable infrastructure component
  #### **Example**
    # GOOD: Focused module
    module "vpc" {
      source = "./modules/networking/vpc"
    
      name        = "production"
      cidr_block  = "10.0.0.0/16"
      environment = "prod"
    }
    
    module "rds" {
      source = "./modules/database/postgres"
    
      name            = "main"
      vpc_id          = module.vpc.vpc_id
      subnet_ids      = module.vpc.private_subnet_ids
      instance_class  = "db.r5.large"
      engine_version  = "15.4"
    }
    
    # BAD: Monolithic module that does everything
    module "infrastructure" {
      source = "./modules/everything"
      # 50+ variables, creates VPC, RDS, EC2, S3, IAM...
    }
    

---
  #### **Name**
Provider Version Pinning
  #### **Description**
Lock provider versions to prevent unexpected changes
  #### **When**
Always - every terraform configuration
  #### **Example**
    terraform {
      required_version = ">= 1.5.0"
    
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 5.0"  # Allow 5.x patches, not 6.0
        }
        random = {
          source  = "hashicorp/random"
          version = "= 3.5.1"  # Exact version for stability
        }
      }
    }
    
    # Run terraform init -upgrade to update within constraints
    # Commit .terraform.lock.hcl for reproducible builds
    

---
  #### **Name**
Destroy Protection for Critical Resources
  #### **Description**
Prevent accidental deletion of stateful or critical resources
  #### **When**
Production databases, storage, or any resource with data that can't be recreated
  #### **Example**
    resource "aws_rds_instance" "production" {
      identifier = "prod-main-db"
      # ... configuration
    
      lifecycle {
        prevent_destroy = true
      }
    }
    
    resource "aws_s3_bucket" "user_uploads" {
      bucket = "myapp-user-uploads-prod"
    
      lifecycle {
        prevent_destroy = true
      }
    }
    
    # Note: prevent_destroy doesn't help if you remove the
    # resource from config entirely - use AWS deletion protection too
    resource "aws_rds_instance" "production" {
      deletion_protection = true  # AWS-level protection
    }
    

---
  #### **Name**
Secrets via External Sources
  #### **Description**
Never store secrets in Terraform config or state - use secret managers
  #### **When**
Any secret, credential, or sensitive value
  #### **Example**
    # GOOD: Reference secrets from AWS Secrets Manager
    data "aws_secretsmanager_secret_version" "db_password" {
      secret_id = "prod/database/password"
    }
    
    resource "aws_rds_instance" "main" {
      password = data.aws_secretsmanager_secret_version.db_password.secret_string
    }
    
    # Mark outputs as sensitive
    output "db_password" {
      value     = data.aws_secretsmanager_secret_version.db_password.secret_string
      sensitive = true
    }
    
    # BAD: Hardcoded or variable secrets
    variable "db_password" {
      default = "super-secret-123"  # Will be in state file!
    }
    

## Anti-Patterns


---
  #### **Name**
Local State File
  #### **Description**
Storing terraform.tfstate on local filesystem
  #### **Why**
State gets lost, multiple engineers overwrite each other, no locking, no backup. One laptop crash and you're manually importing 200 resources.
  #### **Instead**
Always use remote backend with encryption and locking (S3+DynamoDB, GCS, Azure Blob, Terraform Cloud).

---
  #### **Name**
Single Monolithic State
  #### **Description**
One state file for all environments and all resources
  #### **Why**
Blast radius is entire infrastructure. One mistake, one corrupted state, everything affected. Plan takes 20 minutes to run.
  #### **Instead**
Separate state per environment and per logical boundary (networking, compute, data).

---
  #### **Name**
Secrets in Variables
  #### **Description**
Passing secrets via tfvars or environment variables
  #### **Why**
Secrets end up in state file unencrypted. State file in S3 means secrets in S3. Audit logs show secret values.
  #### **Instead**
Use data sources to fetch from secret managers. Mark variables as sensitive. Never commit tfvars with secrets.

---
  #### **Name**
Manual Console Changes
  #### **Description**
Making changes directly in cloud console instead of Terraform
  #### **Why**
State drift. Next terraform apply reverts your manual change. Or worse, creates conflicting resources. Debugging is nightmare.
  #### **Instead**
All changes through Terraform. Import existing resources. Use terraform refresh to detect drift.

---
  #### **Name**
No Provider Pinning
  #### **Description**
Not specifying provider versions or using "latest"
  #### **Why**
Works today, breaks tomorrow when provider updates. CI/CD fails randomly. Different engineers get different plans.
  #### **Instead**
Pin versions in required_providers. Commit .terraform.lock.hcl. Update intentionally with terraform init -upgrade.

---
  #### **Name**
Over-Scoped IAM for Terraform
  #### **Description**
Giving Terraform AdministratorAccess or Action = "*"
  #### **Why**
Blast radius is entire AWS account. One misconfiguration, attacker has full access. Compliance audit fails.
  #### **Instead**
Least privilege. Separate plan (read-only) and apply (write) credentials. Scope to specific services.