**Skill**: [ClickHouse Cloud Management](../SKILL.md)

# SQL Patterns Reference

Comprehensive SQL patterns for ClickHouse Cloud user and permission management via HTTP interface.

## Connection Format

All commands use curl with HTTP basic auth:

```bash
curl -s "https://USER:PASSWORD@HOST:443/" --data-binary "SQL_COMMAND"
```

**Variables**:

- `USER` - Database username (typically `default` for admin operations)
- `PASSWORD` - User password
- `HOST` - ClickHouse Cloud instance hostname (e.g., `abc123.clickhouse.cloud`)

## User Management

### Create User

```bash
# Basic user creation
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "CREATE USER username IDENTIFIED BY 'password'"

# Read-only user (cannot modify data)
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "CREATE USER reader IDENTIFIED BY 'ReaderPass@2025!' SETTINGS readonly = 1"

# User with specific default database
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "CREATE USER app_user IDENTIFIED BY 'AppPass@2025!' DEFAULT DATABASE mydb"
```

### List Users

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "SHOW USERS"
```

### Show User Grants

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "SHOW GRANTS FOR username"
```

### Delete User

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "DROP USER username"

# Delete if exists (no error if missing)
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "DROP USER IF EXISTS username"
```

### Alter User Password

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "ALTER USER username IDENTIFIED BY 'NewPassword@2025!'"
```

## Permission Management

### Grant SELECT (Read Access)

```bash
# Single database
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT ON mydb.* TO username"

# Single table
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT ON mydb.mytable TO username"

# All databases (use carefully)
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT ON *.* TO username"
```

### Grant INSERT (Write Access)

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT INSERT ON mydb.* TO username"
```

### Grant Multiple Permissions

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT, INSERT, ALTER ON mydb.* TO username"
```

### Revoke Permissions

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "REVOKE SELECT ON mydb.* FROM username"
```

### Grant Admin Privileges

```bash
# Full admin (use sparingly)
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT ALL ON *.* TO admin_user"
```

## Common Permission Patterns

### Pattern: Application Read-Only User

```bash
# Create user
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "CREATE USER app_reader IDENTIFIED BY 'AppReader@2025!' SETTINGS readonly = 1"

# Grant read access to specific database
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT ON production.* TO app_reader"
```

### Pattern: Application Read-Write User

```bash
# Create user
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "CREATE USER app_writer IDENTIFIED BY 'AppWriter@2025!'"

# Grant read/write access
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT, INSERT ON production.* TO app_writer"
```

### Pattern: Analytics User (Read + Create Temp Tables)

```bash
# Create user
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "CREATE USER analyst IDENTIFIED BY 'Analyst@2025!'"

# Grant read access + ability to create temporary tables
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT ON production.* TO analyst"

curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT CREATE TEMPORARY TABLE ON *.* TO analyst"
```

## Database Operations

### List Databases

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "SHOW DATABASES"
```

### List Tables in Database

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "SHOW TABLES FROM mydb"
```

### Describe Table Schema

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "DESCRIBE TABLE mydb.mytable"
```

## Testing and Verification

### Test Connection

```bash
# Simple connectivity test
curl -s "https://user:password@$HOST:443/" --data-binary "SELECT 1"
# Expected output: 1

# Get server version
curl -s "https://user:password@$HOST:443/" --data-binary "SELECT version()"
```

### Verify User Permissions

```bash
# Check current user
curl -s "https://user:password@$HOST:443/" --data-binary "SELECT currentUser()"

# Check if user can read specific table
curl -s "https://user:password@$HOST:443/" --data-binary "SELECT count() FROM mydb.mytable"
```

### Test Insert Permission

```bash
# Attempt insert (will fail if no INSERT grant)
curl -s "https://user:password@$HOST:443/" --data-binary \
  "INSERT INTO mydb.test_table (id) VALUES (1)"
```

## Error Handling

### Common Errors

| Error Message           | Cause               | Solution                          |
| ----------------------- | ------------------- | --------------------------------- |
| `Authentication failed` | Wrong credentials   | Verify username/password          |
| `Code: 497`             | Password too weak   | Use 12+ chars, uppercase, special |
| `Code: 60`              | Unknown database    | Check database name spelling      |
| `Code: 81`              | Table doesn't exist | Verify table exists               |
| `Code: 82`              | No permission       | Add GRANT for operation           |

### Check Error Details

```bash
# Add FORMAT Vertical for readable errors
curl -s "https://user:password@$HOST:443/" --data-binary \
  "SELECT * FROM nonexistent FORMAT Vertical"
```

## Best Practices

### Password Generation

Generate compliant passwords (12+ chars, uppercase, special):

```bash
# Using openssl
openssl rand -base64 16 | tr -d '/+=' | head -c 16
# Then manually add uppercase and special char

# Example format: Base16Chars@2025!
```

### Naming Conventions

| User Type       | Naming Pattern     | Example            |
| --------------- | ------------------ | ------------------ |
| Application     | `app_<service>`    | `app_dashboard`    |
| Read-only       | `reader_<purpose>` | `reader_analytics` |
| Admin           | `admin_<name>`     | `admin_terry`      |
| Service account | `svc_<service>`    | `svc_ingestion`    |

### Audit Commands

```bash
/usr/bin/env bash << 'SQL_PATTERNS_SCRIPT_EOF'
# List all users and their grants
for user in $(curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "SHOW USERS" | tr '\n' ' '); do
  echo "=== $user ==="
  curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "SHOW GRANTS FOR $user"
done
SQL_PATTERNS_SCRIPT_EOF
```
