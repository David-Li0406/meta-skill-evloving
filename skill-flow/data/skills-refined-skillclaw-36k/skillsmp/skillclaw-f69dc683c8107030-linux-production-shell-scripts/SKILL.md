---
name: linux-production-shell-scripts
description: Use this skill when you need to create bash scripts for automating Linux tasks, monitoring system resources, backing up files, managing users, or writing production shell scripts.
---

# Skill body

## Purpose

Provide production-ready shell script templates for common Linux system administration tasks including backups, monitoring, user management, log analysis, and automation. These scripts serve as building blocks for security operations and penetration testing environments.

## Prerequisites

### Required Environment
- Linux/Unix system (bash shell)
- Appropriate permissions for tasks
- Required utilities installed (rsync, openssl, etc.)

### Required Knowledge
- Basic bash scripting
- Linux file system structure
- System administration concepts

## Outputs and Deliverables

1. **Backup Solutions** - Automated file and database backups
2. **Monitoring Scripts** - Resource usage tracking
3. **Automation Tools** - Scheduled task execution
4. **Security Scripts** - Password management, encryption

## Core Workflow

### Phase 1: File Backup Scripts

**Basic Directory Backup**
```bash
#!/bin/bash
backup_dir="/path/to/backup"
source_dir="/path/to/source"

# Create a timestamped backup of the source directory
tar -czf "$backup_dir/backup_$(date +%Y%m%d_%H%M%S).tar.gz" "$source_dir"
echo "Backup completed: backup_$(date +%Y%m%d_%H%M%S).tar.gz"
```

**Remote Server Backup**
```bash
#!/bin/bash
source_dir="/path/to/source"
remote_server="user@remoteserver:/path/to/backup"

# Backup files/directories to a remote server using rsync
rsync -avz --progress "$source_dir" "$remote_server"
echo "Files backed up to remote server."
```

**Backup Rotation Script**
```bash
#!/bin/bash
backup_dir="/path/to/backups"
max_backups=5

# Rotate backups by deleting the oldest if more than max_backups
while [ $(ls -1 "$backup_dir" | wc -l) -gt "$max_backups" ]; do
    oldest_backup=$(ls -1t "$backup_dir" | tail -n 1)
    rm -r "$backup_dir/$oldest_backup"
    echo "Removed old backup: $oldest_backup"
done
echo "Backup rotation completed."
```

**Database Backup Script**
```bash
#!/bin/bash
database_name="your_database"
db_user="username"
db_pass="password"
output_file="database_backup_$(date +%Y%m%d).sql"

# Perform database backup using mysqldump
mysqldump -u "$db_user" -p"$db_pass" "$database_name" > "$output_file"
gzip "$output_file"
echo "Database backup completed: $output_file.gz"
```