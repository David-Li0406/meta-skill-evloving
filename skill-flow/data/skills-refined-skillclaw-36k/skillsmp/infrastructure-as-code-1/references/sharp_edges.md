# Infrastructure As Code - Sharp Edges

## State Lock Orphan

### **Id**
state-lock-orphan
### **Summary**
Terraform state lock orphaned after crashed apply - nobody can deploy
### **Severity**
critical
### **Situation**
CI/CD job crashed mid-apply, engineer's laptop died, network timeout during state write
### **Why**
  State lock held in DynamoDB (or equivalent). Process that held it is gone. Lock never
  released. Every subsequent terraform plan fails with "Error acquiring state lock".
  Production hotfix blocked. Team scrambles to figure out who has the lock. It's nobody -
  the process is dead.
  
### **Solution**
  # WRONG: Blindly force-unlock without checking
  terraform force-unlock LOCK_ID
  # Risk: If another apply is actually running, you'll corrupt state
  
  # RIGHT: Investigate first
  # 1. Check if anyone is actually running terraform
  aws dynamodb get-item \
    --table-name terraform-state-lock \
    --key '{"LockID": {"S": "my-state-file.tfstate"}}'
  
  # 2. Verify the lock holder process is dead
  # 3. Then force-unlock with the lock ID from error message
  terraform force-unlock a1b2c3d4-e5f6-7890-abcd-ef1234567890
  
  # PREVENTION: Add lock timeout to CI/CD
  terraform apply -lock-timeout=10m
  
  # Set up lock monitoring alert
  # Alert if any lock held > 30 minutes
  
### **Symptoms**
  - Error acquiring the state lock
  - Lock Info: ID, Path, Operation, Who, Created
  - Deployments stuck, nobody can apply
### **Detection Pattern**
Error acquiring|state lock|force-unlock

## State File Secrets Exposed

### **Id**
state-file-secrets-exposed
### **Summary**
Secrets stored in plain text in state file, leaked via S3 or Git
### **Severity**
critical
### **Situation**
Database password in variable, API key in resource attribute, state file in public bucket
### **Why**
  Terraform state stores ALL resource attributes - including passwords, API keys,
  private keys. State file pushed to Git (common mistake) or S3 bucket made public
  (misconfiguration). All secrets exposed. One audit and you're compromised.
  2024 survey: 30% of developers reported state file breaches.
  
### **Solution**
  # WRONG: Secrets in variables or state
  variable "db_password" {
    default = "production-password-123"  # IN STATE FILE!
  }
  
  resource "aws_db_instance" "main" {
    password = var.db_password  # Password stored in state
  }
  
  # RIGHT: Fetch from secret manager at apply time
  data "aws_secretsmanager_secret_version" "db" {
    secret_id = "prod/database/master-password"
  }
  
  resource "aws_db_instance" "main" {
    password = data.aws_secretsmanager_secret_version.db.secret_string
  }
  
  # RIGHT: Mark sensitive
  variable "api_key" {
    type      = string
    sensitive = true  # Redacted in logs
  }
  
  # Encrypt state at rest
  terraform {
    backend "s3" {
      bucket  = "my-state"
      encrypt = true
      kms_key_id = "alias/terraform-state"
    }
  }
  
  # NEVER commit state or tfvars with secrets
  # .gitignore
  *.tfstate
  *.tfstate.*
  *.tfvars
  
### **Symptoms**
  - Secrets visible in terraform plan output
  - State file in Git history
  - Public S3 bucket with state files
### **Detection Pattern**
password.*=.*"|api_key.*=.*"|secret.*=.*"

## Prevent Destroy Removal Bypass

### **Id**
prevent-destroy-removal-bypass
### **Summary**
Removing resource from config bypasses prevent_destroy - resource deleted
### **Severity**
critical
### **Situation**
Engineer removes resource block thinking prevent_destroy will protect it
### **Why**
  prevent_destroy only works while the resource block exists. Remove the block entirely,
  and prevent_destroy goes with it. Terraform sees "resource no longer in config" and
  deletes it. Production database gone. Engineer thought it was protected.
  
### **Solution**
  # WRONG: Relying only on prevent_destroy
  resource "aws_rds_instance" "prod" {
    lifecycle {
      prevent_destroy = true
    }
  }
  # Delete this block -> database deleted!
  
  # RIGHT: Use BOTH Terraform and provider-level protection
  resource "aws_rds_instance" "prod" {
    deletion_protection = true  # AWS refuses to delete
  
    lifecycle {
      prevent_destroy = true  # Terraform refuses to plan delete
    }
  }
  
  # RIGHT: Use resource targeting for dangerous changes
  # Only touch specific resources
  terraform plan -target=aws_instance.web
  
  # RIGHT: State surgery instead of delete
  # Remove from state without destroying
  terraform state rm aws_rds_instance.prod
  
### **Symptoms**
  - "Resource X will be destroyed" for protected resource
  - deletion_protection not set on stateful resources
  - Team believes prevent_destroy is absolute protection
### **Detection Pattern**
prevent_destroy.*true(?![^}]*deletion_protection)

## State Drift Silent Failure

### **Id**
state-drift-silent-failure
### **Summary**
Manual console changes cause state drift - next apply reverts production fix
### **Severity**
critical
### **Situation**
Engineer adds security group rule in console during incident, forgets to update Terraform
### **Why**
  11 PM outage. Engineer adds port rule in AWS console to fix. Works. Incident resolved.
  Week later, different engineer runs terraform apply for unrelated change. Terraform
  sees rule not in config, removes it. Service breaks again during peak hours. Original
  engineer is on vacation.
  
### **Solution**
  # WRONG: Manual changes without tracking
  # (make change in console, don't update Terraform)
  
  # RIGHT: Detect drift regularly
  terraform plan -detailed-exitcode
  # Exit code 2 = changes detected (drift or pending changes)
  
  # RIGHT: Scheduled drift detection in CI
  # Run every hour, alert on differences
  terraform plan -no-color > plan.txt
  if grep -q "will be" plan.txt; then
    notify_slack "Drift detected!"
  fi
  
  # RIGHT: Import manual changes
  # 1. Make change in console (emergency)
  # 2. Immediately add to Terraform config
  # 3. Import to state
  terraform import aws_security_group_rule.emergency sg-xxx
  
  # RIGHT: Use AWS Config rules or Firefly for drift detection
  
### **Symptoms**
  - Terraform plan shows unexpected changes
  - "This will be destroyed/updated" for resources you didn't touch
  - Changes made in console disappear after apply
### **Detection Pattern**
detailed-exitcode|plan.*target

## Provider Version Surprise

### **Id**
provider-version-surprise
### **Summary**
Unpinned provider version breaks terraform apply on update
### **Severity**
high
### **Situation**
Provider releases new version with breaking changes, CI/CD pulls latest
### **Why**
  Works Monday. Friday, provider v5.0 releases with breaking API changes. CI/CD runs
  terraform init, pulls v5.0. Plan fails with cryptic errors. Or worse, plan succeeds
  but behavior changed - resource recreated instead of updated. You discover in production.
  
### **Solution**
  # WRONG: No version constraint
  terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        # No version = latest = surprise
      }
    }
  }
  
  # RIGHT: Pin version ranges
  terraform {
    required_version = ">= 1.5.0, < 2.0.0"
  
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"  # 5.x only
      }
    }
  }
  
  # Commit the lock file!
  git add .terraform.lock.hcl
  
  # Update intentionally
  terraform init -upgrade
  terraform plan  # Review changes carefully
  git add .terraform.lock.hcl
  git commit -m "Upgrade AWS provider to 5.31.0"
  
### **Symptoms**
  - "Works on my machine" but fails in CI
  - Different plans for same code
  - Errors after terraform init without code changes
### **Detection Pattern**
required_providers\\s*\\{[^}]*(?!version)

## Iam Wildcard Blast Radius

### **Id**
iam-wildcard-blast-radius
### **Summary**
IAM policy with Action = "*" gives Terraform (and attackers) god mode
### **Severity**
high
### **Situation**
Using AdministratorAccess or crafting policy with wildcard permissions
### **Why**
  Terraform needs broad permissions to manage infrastructure. Engineer thinks "just
  give it admin, it's automated anyway". Terraform state file leaked or CI compromised.
  Attacker now has full AWS access. Compliance audit fails. Crypto miners spin up.
  Invoice: $50,000.
  
### **Solution**
  # WRONG: God mode
  {
    "Effect": "Allow",
    "Action": "*",
    "Resource": "*"
  }
  
  # RIGHT: Least privilege per resource type
  {
    "Effect": "Allow",
    "Action": [
      "ec2:Describe*",
      "ec2:CreateSecurityGroup",
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:RevokeSecurityGroupIngress"
    ],
    "Resource": "*"
  }
  
  # RIGHT: Separate plan and apply roles
  # Plan role: Read-only
  # Apply role: Write, scoped to specific services
  
  # RIGHT: Use Checkov/tfsec to detect
  checkov -d . --check CKV_AWS_*
  
  # RIGHT: Service control policies as guardrails
  # Prevent any IAM policy from being created with *
  
### **Symptoms**
  - IAM policy with "*" in Action or Resource
  - AdministratorAccess attached to Terraform role
  - No SCPs limiting Terraform's power
### **Detection Pattern**
"Action":\\s*"\\*"|AdministratorAccess|PowerUserAccess

## Destroy Without Target

### **Id**
destroy-without-target
### **Summary**
Terraform destroy without -target deletes entire environment
### **Severity**
high
### **Situation**
Engineer means to destroy one resource, runs terraform destroy without flags
### **Why**
  Engineer wants to delete old EC2 instance. Types terraform destroy. Terraform asks
  "Do you want to destroy all 47 resources?" Engineer is tired, types "yes".
  Database, load balancer, S3 buckets - all gone. Friday evening. Backups exist but
  restore takes 6 hours.
  
### **Solution**
  # WRONG: Naked destroy
  terraform destroy
  # "Do you really want to destroy all resources?" -> yes -> disaster
  
  # RIGHT: Always target specific resources
  terraform destroy -target=aws_instance.old_server
  
  # RIGHT: Use workspace separation
  # Dev workspace can be destroyed freely
  # Prod workspace has additional protection
  
  # RIGHT: CI/CD blocks destroy on main branch
  # GitHub Actions example
  - name: Block destroy
    run: |
      if grep -q "destroy" <<< "${{ github.event.inputs.action }}"; then
        if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
          echo "::error::Destroy blocked on main branch"
          exit 1
        fi
      fi
  
  # RIGHT: Require approval for destroy
  # Terraform Cloud: Sentinel policies
  # Self-hosted: Manual approval step in pipeline
  
### **Symptoms**
  - terraform destroy in CI/CD without -target
  - No destroy protection in pipeline
  - History of "oops" destroys
### **Detection Pattern**
terraform destroy(?!.*-target)

## Module Version Drift

### **Id**
module-version-drift
### **Summary**
Module source without version pins - different versions across environments
### **Severity**
medium
### **Situation**
Using module from registry or Git without version constraint
### **Why**
  Dev uses latest module version. Staging pins to v1.2. Prod... nobody remembers.
  Module author releases v2.0 with breaking changes. Dev breaks immediately. Staging
  fine. Prod runs terraform apply, pulls v2.0 (no pin), breaks differently.
  Debugging across three different module versions is hell.
  
### **Solution**
  # WRONG: No version pin
  module "vpc" {
    source = "terraform-aws-modules/vpc/aws"
    # Uses latest = different across envs
  }
  
  # WRONG: Git without ref
  module "custom" {
    source = "git::https://github.com/company/module.git"
    # Always pulls HEAD
  }
  
  # RIGHT: Registry module with version
  module "vpc" {
    source  = "terraform-aws-modules/vpc/aws"
    version = "5.1.2"  # Exact version
  }
  
  # RIGHT: Git with specific ref
  module "custom" {
    source = "git::https://github.com/company/module.git?ref=v1.2.3"
  }
  
  # RIGHT: Private registry with versioning
  module "internal" {
    source  = "app.terraform.io/company/vpc/aws"
    version = "~> 1.0"
  }
  
### **Symptoms**
  - Same config produces different plans across machines
  - "Module downloaded" messages on every init
  - Different behavior in dev vs prod for same module
### **Detection Pattern**
source.*=.*"(?!.*version|\\?ref=)

## Workspace Env Confusion

### **Id**
workspace-env-confusion
### **Summary**
Workspaces used for environment separation with shared backend
### **Severity**
medium
### **Situation**
Using terraform workspace new prod, workspace new dev with same config
### **Why**
  Workspaces are for parallel deployments, not environment separation. Same backend,
  same config, different workspace names. Developer in "dev" workspace accidentally
  targets prod resource. Or terraform workspace select prod fails silently, changes
  go to dev. Conditional resources based on workspace name get messy.
  
### **Solution**
  # WRONG: Workspaces for environments
  terraform workspace new dev
  terraform workspace new prod
  # Same backend, same config, different workspace
  # Easy to forget which workspace you're in
  
  # RIGHT: Directory-based environments
  environments/
    dev/
      main.tf
      backend.tf  # key = "dev/terraform.tfstate"
      terraform.tfvars
    prod/
      main.tf
      backend.tf  # key = "prod/terraform.tfstate"
      terraform.tfvars
  
  # RIGHT: Terragrunt for DRY environment config
  terragrunt.hcl  # Common config
  environments/
    dev/
      terragrunt.hcl
    prod/
      terragrunt.hcl
  
  # If you must use workspaces, add safeguards
  locals {
    is_prod = terraform.workspace == "prod"
  }
  
  resource "aws_instance" "web" {
    instance_type = local.is_prod ? "t3.large" : "t3.micro"
    # Still risky - workspace can be wrong
  }
  
### **Symptoms**
  - terraform.workspace in many conditionals
  - "Wrong environment" incidents
  - Confusion about which workspace is active
### **Detection Pattern**
terraform\\.workspace|workspace.*new.*prod

## Count Index Shift

### **Id**
count-index-shift
### **Summary**
Removing item from count-based resources shifts all subsequent indexes
### **Severity**
medium
### **Situation**
Resources created with count, removing middle item
### **Why**
  You have 5 EC2 instances via count. Remove the third. Terraform sees index shift:
  instance[3] becomes instance[2], instance[4] becomes instance[3]. Terraform destroys
  and recreates instances 2, 3, 4 to match new indexes. Three instances replaced in
  production. Users on those instances disconnected.
  
### **Solution**
  # WRONG: Count for distinct resources
  variable "instances" {
    default = ["web1", "web2", "web3", "web4", "web5"]
  }
  
  resource "aws_instance" "web" {
    count = length(var.instances)
    tags = {
      Name = var.instances[count.index]
    }
  }
  # Remove "web3" -> web4 becomes web[2], web5 becomes web[3]
  # 3 instances recreated!
  
  # RIGHT: for_each with stable keys
  variable "instances" {
    default = {
      "web1" = {}
      "web2" = {}
      "web3" = {}
      "web4" = {}
      "web5" = {}
    }
  }
  
  resource "aws_instance" "web" {
    for_each = var.instances
    tags = {
      Name = each.key
    }
  }
  # Remove "web3" -> only web3 destroyed, others unchanged
  
  # Convert existing count to for_each
  # 1. Add for_each version
  # 2. terraform state mv aws_instance.web[0] aws_instance.web["web1"]
  # 3. Remove count version
  
### **Symptoms**
  - "X will be destroyed, Y will be created" for unchanged resources
  - Resource addresses like aws_instance.web[3]
  - Fear of removing items from lists
### **Detection Pattern**
count\\s*=\\s*length\\(

## Apply Without Plan

### **Id**
apply-without-plan
### **Summary**
Running terraform apply without reviewing plan first
### **Severity**
medium
### **Situation**
CI/CD runs terraform apply -auto-approve without plan review, or manual apply without reading
### **Why**
  Plan shows 50 changes. Engineer glances at first 5, hits yes. Change 47 is
  "aws_db_instance.prod will be destroyed". Database recreated with empty data.
  auto-approve in CI means no human eyes on destructive changes.
  
### **Solution**
  # WRONG: Blind apply
  terraform apply -auto-approve
  # Whatever plan says, it does
  
  # RIGHT: Separate plan and apply in CI/CD
  # Step 1: Plan and save
  terraform plan -out=plan.tfplan
  
  # Step 2: Human review (PR comment, manual gate)
  terraform show plan.tfplan
  
  # Step 3: Apply saved plan only
  terraform apply plan.tfplan
  
  # RIGHT: Policy checks before apply
  # Terraform Cloud Sentinel
  # Open Policy Agent (OPA)
  # Checkov in CI pipeline
  
  # RIGHT: Require approval for production
  # GitHub Actions
  environment:
    name: production
    # Requires reviewer approval
  
### **Symptoms**
  - -auto-approve in production pipelines
  - No saved plan file
  - I didn't know it would do that
### **Detection Pattern**
apply.*-auto-approve|apply(?!.*\\.tfplan)