---
name: archiving-databases
description: Use this skill when you need to automate the archival of database records to reduce primary database size and ensure compliance with data retention policies.
---

# Skill body

## Overview

This skill automates the process of archiving database records, freeing up space on the primary database and ensuring compliance with data retention policies. It supports moving historical data to cost-effective storage solutions like S3, Azure Blob, or GCS while maintaining query access.

## How It Works

1. **Identify Archival Candidates**: The skill identifies database records that meet specified archival criteria based on age, size, or other relevant factors.
2. **Data Migration**: It migrates the identified records to archive tables within the same database or to cold storage solutions like S3, Azure Blob, or GCS.
3. **Policy Enforcement**: The skill enforces automated retention policies, ensuring that data is archived or deleted according to pre-defined rules.
4. **Verification and Reporting**: After the archival process, the skill verifies the successful migration of data and generates reports for compliance tracking.

## When to Use This Skill

This skill activates when you need to:
- Reduce the size of a primary database.
- Implement data retention policies for compliance.
- Move historical data to cost-effective storage solutions.

## Examples

### Example 1: Archiving Old Order Data

User request: "I need to archive order data older than one year from my PostgreSQL database to S3 to reduce database size and comply with retention policies."

The skill will:
1. Identify order records older than one year in the PostgreSQL database.
2. Migrate these records to an S3 bucket, compressing the data for storage efficiency.

### Example 2: Setting Up Automated Retention Policies

User request: "Set up automated retention policies for my MySQL database to archive user activity logs older than 90 days to a separate archive table."

The skill will:
1. Configure automated retention policies to archive user activity logs older than 90 days.
2. Migrate the identified records to the designated archive table.