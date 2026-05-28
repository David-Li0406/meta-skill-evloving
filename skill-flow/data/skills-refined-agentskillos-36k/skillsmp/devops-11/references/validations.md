# Devops - Validations

## Latest Docker Tag

### **Id**
devops-latest-tag
### **Severity**
error
### **Type**
regex
### **Pattern**
  - FROM\\s+\\w+:latest
  - image:\\s*\\w+:latest
### **Message**
Using :latest Docker tag. Builds will be inconsistent.
### **Fix Action**
Pin to specific version: node:20.11.0-alpine3.19
### **Applies To**
  - Dockerfile
  - *.yaml
  - *.yml

## npm install Instead of npm ci

### **Id**
devops-npm-install-in-docker
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - RUN\\s+npm\\s+install(?!.*ci)
### **Message**
Using npm install in Dockerfile. Use npm ci for deterministic builds.
### **Fix Action**
Change to: RUN npm ci
### **Applies To**
  - Dockerfile

## Publicly Accessible Database

### **Id**
devops-public-database
### **Severity**
error
### **Type**
regex
### **Pattern**
  - publicly_accessible\\s*=\\s*true
### **Message**
Database marked publicly accessible. This is a security risk.
### **Fix Action**
Set publicly_accessible = false and use private subnets
### **Applies To**
  - *.tf

## Security Group Open to Internet

### **Id**
devops-open-security-group
### **Severity**
error
### **Type**
regex
### **Pattern**
  - cidr_blocks\\s*=\\s*\\[\\s*"0\\.0\\.0\\.0/0"\\s*\\]
### **Message**
Security group allows traffic from entire internet (0.0.0.0/0).
### **Fix Action**
Restrict to specific IP ranges or security groups
### **Applies To**
  - *.tf

## Missing Resource Limits

### **Id**
devops-no-resource-limits
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - resources:\\s*\\{\\}
  - resources:\\s*\\{\\s*\\}
### **Message**
Container has no resource limits. Can cause node instability.
### **Fix Action**
Add resources.requests and resources.limits
### **Applies To**
  - *.yaml
  - *.yml

## Single Replica Deployment

### **Id**
devops-single-replica
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - replicas:\\s*1(?!\\d)
  - minReplicas:\\s*1(?!\\d)
### **Message**
Single replica has no redundancy. Deploys will cause downtime.
### **Fix Action**
Use at least 2 replicas for high availability
### **Applies To**
  - *.yaml
  - *.yml

## Terraform State in Repository

### **Id**
devops-tfstate-in-repo
### **Severity**
error
### **Type**
file
### **Pattern**
*.tfstate
### **Message**
Terraform state file should not be committed. Contains secrets.
### **Fix Action**
Add *.tfstate to .gitignore, use remote backend
### **Applies To**
  - *

## Environment File Committed

### **Id**
devops-env-file-committed
### **Severity**
error
### **Type**
file
### **Pattern**
.env
### **Message**
.env file should not be committed. May contain secrets.
### **Fix Action**
Add .env to .gitignore, use .env.example for templates
### **Applies To**
  - *

## No Backup Retention

### **Id**
devops-no-backup-retention
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backup_retention_period\\s*=\\s*0
### **Message**
Database has no backup retention. Data loss risk.
### **Fix Action**
Set backup_retention_period to at least 7 days
### **Applies To**
  - *.tf

## Hardcoded AWS Access Key

### **Id**
devops-hardcoded-aws-key
### **Severity**
error
### **Type**
regex
### **Pattern**
  - AKIA[A-Z0-9]{16}
### **Message**
AWS access key hardcoded. Use IAM roles or environment variables.
### **Fix Action**
Remove hardcoded key, use IAM roles or ${{ secrets.AWS_ACCESS_KEY_ID }}
### **Applies To**
  - *.tf
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## No Deletion Protection

### **Id**
devops-no-deletion-protection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - deletion_protection\\s*=\\s*false
### **Message**
Database has deletion protection disabled. Accidental deletion possible.
### **Fix Action**
Set deletion_protection = true for production databases
### **Applies To**
  - *.tf

## Unencrypted Storage

### **Id**
devops-unencrypted-storage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - encrypt\\s*=\\s*false
  - encrypted\\s*=\\s*false
### **Message**
Storage encryption disabled. Data at rest should be encrypted.
### **Fix Action**
Set encrypt = true
### **Applies To**
  - *.tf

## Missing Health Check

### **Id**
devops-no-health-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - spec:\\s*\\n\\s*containers:(?![\\s\\S]*(?:livenessProbe|readinessProbe))
### **Message**
Container deployment without health checks.
### **Fix Action**
Add livenessProbe and readinessProbe
### **Applies To**
  - *.yaml
  - *.yml

## Console Log for Logging

### **Id**
devops-console-log-logging
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.log\([^)]*\+[^)]*\)
  - console\.log\(`[^`]*\$\{
### **Message**
Using console.log with string concatenation. Use structured logging.
### **Fix Action**
Use structured logger: logger.info({ key: value }, 'message')
### **Applies To**
  - *.ts
  - *.js