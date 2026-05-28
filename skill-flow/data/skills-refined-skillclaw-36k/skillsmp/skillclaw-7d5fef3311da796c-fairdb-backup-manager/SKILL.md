---
name: fairdb-backup-manager
description: Use this skill when you need to manage PostgreSQL backups for FairDB databases, including scheduling, verification, and restoration with pgBackRest and Wasabi S3 storage.
---

# FairDB Backup Manager

## Purpose
I automatically handle all backup-related operations for FairDB PostgreSQL databases, including scheduling, verification, restoration, and monitoring of pgBackRest backups with Wasabi S3 storage.

## Activation Triggers
I activate when you:
- Mention "backup", "restore", "pgbackrest", or "recovery" in context of FairDB
- Work with PostgreSQL backup configurations
- Need to verify backup integrity
- Discuss disaster recovery or data protection
- Experience data loss or corruption issues

## Core Capabilities

### Backup Operations
- Configure pgBackRest with Wasabi S3
- Execute full, differential, and incremental backups
- Manage backup schedules and retention policies
- Compress and encrypt backup data
- Monitor backup health and success rates

### Restore Operations
- Perform point-in-time recovery (PITR)
- Restore specific databases or tables
- Test restore procedures without impacting production
- Validate restored data integrity
- Document recovery time objectives (RTO)

### Monitoring & Verification
- Check backup completion status
- Verify backup integrity with test restores
- Monitor backup size and growth trends
- Alert on backup failures or delays
- Generate backup compliance reports

## Automated Workflows

When activated, I will:

1. **Assess Current State**
   - Check existing backup configuration
   - Review backup history and success rate
   - Identify any failed or missing backups
   - Analyze storage usage and costs

2. **Optimize Configuration**
   - Adjust retention policies based on requirements
   - Configure optimal compression settings
   - Set up parallel backup processes
   - Implement incremental backup strategies

3. **Execute Operations**
   - Run scheduled backups automatically
   - Perform test restores monthly
   - Clean up old backups per retention policy
   - Monitor and alert on issues

4. **Document & Report**
   - Maintain backup/restore runbooks
   - Generate compliance reports
   - Track metrics and trends
   - Document recovery procedures

## Integration with FairDB Commands

I work seamlessly with these FairDB commands:
- `/fairdb-setup-backup` - Initial configuration
- `/fairdb-onboard-customer` - Customer-specific backups
- `/fairdb-emergency-response` - Disaster recovery
- `/fairdb-health-check` - Backup health monitor