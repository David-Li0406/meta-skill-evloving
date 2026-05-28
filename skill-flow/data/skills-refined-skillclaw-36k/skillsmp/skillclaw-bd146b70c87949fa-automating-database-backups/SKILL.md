---
name: automating-database-backups
description: Use this skill when you need to automate database backups, set up backup schedules, or create restore procedures for PostgreSQL, MySQL, MongoDB, and SQLite.
---

# Skill body

## Overview

This skill streamlines the creation of database backup solutions. It generates scripts, configures schedules, and provides comprehensive restore procedures, ensuring data safety and efficient recovery.

## How It Works

1. **Analyze Requirements**: Determine the database type (PostgreSQL, MySQL, MongoDB, or SQLite) and backup requirements (frequency, retention).
2. **Generate Scripts**: Create backup scripts with compression and encryption.
3. **Schedule Backups**: Set up cron jobs for automated, scheduled backups.
4. **Document Restore**: Generate clear, concise restore procedures.

## When to Use This Skill

This skill activates when you need to:
- Create a backup schedule for a database.
- Automate the database backup process.
- Generate scripts for database restoration.
- Implement a disaster recovery plan for a database.

## Examples

### Example 1: Setting up Daily Backups for PostgreSQL

User request: "Create daily backups for my PostgreSQL database."

The skill will:
1. Generate a `pg_dump` script with compression and encryption.
2. Create a cron job to run the backup script daily.

### Example 2: Automating Weekly Backups for MongoDB

User request: "Automate weekly backups for my MongoDB database."

The skill will:
1. Generate a `mongodump` script with compression and encryption.
2. Create a cron job to run the backup script weekly and implement a retention policy.

## Best Practices

- **Retention Policies**: Implement clear retention policies to manage storage space.
- **Testing Restores**: Regularly test restore procedures to ensure data integrity.
- **Secure Storage**: Store backups in secure, encrypted locations, preferably offsite.

## Integration

This skill can integrate with cloud storage plugins (S3, GCS, Azure) for offsite backup storage and monitoring plugins for backup success/failure alerts.