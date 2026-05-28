# Disaster Recovery - Validations

## Unencrypted Backup

### **Id**
no-backup-encryption
### **Severity**
error
### **Type**
regex
### **Pattern**
  - backup.*encryption.*false
  - pg_dump(?!.*--no-password)
  - mysqldump(?!.*--ssl)
### **Message**
Backup may not be encrypted - security risk.
### **Fix Action**
Enable encryption for all backups
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.yaml

## Same Region Backup

### **Id**
same-region-backup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backup.*region.*=.*primary
  - s3.*bucket.*same.*region
  - backup_region.*=.*source_region
### **Message**
Backup may be in same region as primary - DR risk.
### **Fix Action**
Configure cross-region backup replication
### **Applies To**
  - **/*.py
  - **/*.yaml
  - **/*.tf

## Missing Backup Verification

### **Id**
no-backup-verification
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - create_backup\((?!.*verify)
  - backup\.run\((?!.*validate)
### **Message**
Backup may not be verified after creation.
### **Fix Action**
Add backup verification step
### **Applies To**
  - **/*.py
  - **/*.sh

## Manual Failover Steps

### **Id**
manual-failover
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ssh.*promote
  - manual.*step
  - run.*script.*manually
### **Message**
Failover contains manual steps - consider automation.
### **Fix Action**
Automate failover procedure
### **Applies To**
  - **/*.md
  - **/*.sh
  - **/*.yaml

## Missing RTO/RPO Definition

### **Id**
no-rto-rpo-defined
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - disaster.*recovery(?!.*rto|.*rpo)
  - dr_config(?!.*recovery_time)
### **Message**
DR configuration may lack RTO/RPO definitions.
### **Fix Action**
Define RTO and RPO for all services
### **Applies To**
  - **/*.yaml
  - **/*.py

## Missing Backup Retention Policy

### **Id**
no-backup-retention
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backup(?!.*retention)
  - create_snapshot(?!.*expire)
### **Message**
Backup may lack retention policy - storage cost risk.
### **Fix Action**
Define backup retention and cleanup policy
### **Applies To**
  - **/*.py
  - **/*.yaml
  - **/*.tf

## Hardcoded DR Credentials

### **Id**
hardcoded-dr-credentials
### **Severity**
error
### **Type**
regex
### **Pattern**
  - dr_password\s*=\s*['"]
  - failover_key\s*=\s*['"]
  - backup_secret\s*=\s*['"]
### **Message**
DR credentials may be hardcoded - security risk.
### **Fix Action**
Use secrets manager for DR credentials
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.yaml