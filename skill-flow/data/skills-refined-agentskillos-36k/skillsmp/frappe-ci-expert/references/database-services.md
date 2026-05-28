# Database Services Configuration

This reference covers database service configuration for Frappe CI testing, including MariaDB and PostgreSQL setup, and site configuration files.

## MariaDB Service

### Basic Configuration

Note: Official Frappe apps use `mysql` as the service name even when using MariaDB.

```yaml
services:
  mysql:  # Service name can be 'mysql' or 'mariadb'
    image: mariadb:10.6
    env:
      MARIADB_ROOT_PASSWORD: root  # Or MYSQL_ROOT_PASSWORD: root
    ports:
      - 3306:3306
    options: --health-cmd="mysqladmin ping" --health-interval=5s --health-timeout=2s --health-retries=3
```

### Configuration Details

- **Image**: `mariadb:10.6` - Stable version compatible with Frappe
- **Root Password**: `root` - Standard password used in official Frappe apps (some older examples use `travis`)
- **Port**: Maps container port 3306 to host port 3306
- **Service Name**: Can be `mysql` or `mariadb` (official apps use `mysql`)
- **Health Check**: Ensures database is ready before tests start
  - Command: `mysqladmin ping` or `mariadb-admin ping`
  - Interval: Check every 5 seconds
  - Timeout: 2 seconds per check
  - Retries: 3 attempts before marking unhealthy

### Alternative MariaDB Versions

```yaml
# MariaDB 10.6 (recommended for Frappe v14+)
image: mariadb:10.6

# MariaDB 11.0+ (for newer Frappe versions)
image: mariadb:11.0

# MariaDB 10.5 (for older Frappe versions)
image: mariadb:10.5
```

### MariaDB with Custom Configuration

If you need specific MariaDB settings:

```yaml
services:
  mariadb:
    image: mariadb:10.6.24
    env:
      MARIADB_ROOT_PASSWORD: travis
      MARIADB_INITDB_SKIP_TZINFO: 1
    ports:
      - 3306:3306
    options: >-
      --health-cmd="mysqladmin ping"
      --health-interval=5s
      --health-timeout=2s
      --health-retries=3
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
```

## PostgreSQL Service

### Basic Configuration

```yaml
services:
  postgres:
    image: postgres:12.4
    env:
      POSTGRES_PASSWORD: travis
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

### Configuration Details

- **Image**: `postgres:12.4` - Compatible PostgreSQL version
- **Password**: `travis` - Standard password for CI
- **Port**: Maps container port 5432 to host port 5432
- **Health Check**: Uses `pg_isready` to verify database is accepting connections
  - Interval: Check every 10 seconds
  - Timeout: 5 seconds per check
  - Retries: 5 attempts

### Alternative PostgreSQL Versions

```yaml
# PostgreSQL 12 (recommended)
image: postgres:12.4

# PostgreSQL 13
image: postgres:13

# PostgreSQL 14
image: postgres:14
```

### PostgreSQL with Custom Settings

```yaml
services:
  postgres:
    image: postgres:12.4
    env:
      POSTGRES_PASSWORD: travis
      POSTGRES_INITDB_ARGS: "-E UTF8"
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

## Both MariaDB and PostgreSQL

For testing against both databases in one workflow:

```yaml
services:
  mariadb:
    image: mariadb:10.6.24
    env:
      MARIADB_ROOT_PASSWORD: travis
    ports:
      - 3306:3306
    options: --health-cmd="mysqladmin ping" --health-interval=5s --health-timeout=2s --health-retries=3

  postgres:
    image: postgres:12.4
    env:
      POSTGRES_PASSWORD: travis
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

Use with matrix strategy to test both:

```yaml
strategy:
  matrix:
    db: [mariadb, postgres]
```

## Redis Service (Optional)

For apps that require Redis for caching or background jobs:

```yaml
services:
  redis:
    image: redis:alpine
    ports:
      - 6379:6379
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

## SMTP Service (Optional)

For testing email functionality:

```yaml
services:
  smtp_server:
    image: rnwood/smtp4dev:3.7.1
    ports:
      - 2525:25    # SMTP port
      - 3000:80    # Web UI port
```

## Site Configuration Files

### MariaDB Site Config

Create `.github/helper/db/mariadb.json` (or `.github/helper/site_config_mariadb.json` in some apps):

```json
{
    "db_host": "127.0.0.1",
    "db_port": 3306,
    "db_name": "test_frappe",
    "db_password": "test_frappe",
    "allow_tests": true,
    "db_type": "mariadb",
    "auto_email_id": "test@example.com",
    "mail_server": "smtp.example.com",
    "mail_login": "test@example.com",
    "mail_password": "test",
    "admin_password": "admin",
    "root_login": "root",
    "root_password": "root",
    "host_name": "http://test_site:8000",
    "install_apps": ["your_app_name"],
    "throttle_user_limit": 100,
    "monitor": 1,
    "server_script_enabled": true
}
```

### PostgreSQL Site Config

Create `.github/helper/db/postgres.json` (or `.github/helper/site_config_postgres.json`):

```json
{
    "db_host": "127.0.0.1",
    "db_port": 5432,
    "db_name": "test_frappe",
    "db_password": "test_frappe",
    "db_type": "postgres",
    "allow_tests": true,
    "auto_email_id": "test@example.com",
    "mail_server": "smtp.example.com",
    "mail_login": "test@example.com",
    "mail_password": "test",
    "admin_password": "admin",
    "root_login": "postgres",
    "root_password": "root",
    "host_name": "http://test_site:8000",
    "install_apps": ["your_app_name"],
    "throttle_user_limit": 100,
    "server_script_enabled": true
}
```

### Site Config Field Explanations

| Field | Purpose | Notes |
|-------|---------|-------|
| `db_host` | Database server address | Always `127.0.0.1` in CI |
| `db_port` | Database server port | 3306 for MariaDB, 5432 for PostgreSQL |
| `db_name` | Database name | Must match the created database |
| `db_password` | Database user password | Must match the created user's password |
| `db_type` | Database type | `mariadb` or `postgres` |
| `allow_tests` | Enable test mode | Must be `true` for CI |
| `auto_email_id` | Default email for test users | Any test email address |
| `mail_server` | SMTP server | `smtp.example.com` or `localhost` with smtp4dev |
| `mail_port` | SMTP port | `2525` for smtp4dev, `25` for standard SMTP |
| `admin_password` | Admin user password | Used for logging in |
| `root_login` | Database root user | `root` for MariaDB, `postgres` for PostgreSQL |
| `root_password` | Database root password | Must match service configuration (`root` in official apps) |
| `host_name` | Site URL | Used for URL generation |
| `install_apps` | Apps to install on site | Array of app names to auto-install |
| `throttle_user_limit` | Rate limit for testing | Set to `100` to avoid throttling in tests |
| `monitor` | Enable monitoring | Optional, helps with debugging |
| `server_script_enabled` | Enable server scripts | Required for some tests |

### Important Site Config Notes

1. **install_apps field**: Official Frappe apps include this to automatically install apps during site creation
2. **throttle_user_limit**: Prevents rate limiting during test execution
3. **Root password**: Most official apps use `root` (not `travis`) for database root password
4. **Mail server**: Use `smtp.example.com` for dummy server (no actual emails sent in tests)
| `admin_password` | Admin user password | Used for logging in |
| `root_login` | Database root user | `root` for MariaDB, `postgres` for PostgreSQL |
| `root_password` | Database root password | Must match service configuration |
| `host_name` | Site URL | Used for URL generation |
| `monitor` | Enable monitoring | Optional, helps with debugging |
| `server_script_enabled` | Enable server scripts | Required for some tests |

## Database Creation Scripts

### MariaDB Database Setup

In your install script, create the database and user:

```bash
if [ "$DB" == "mariadb" ]
then
  mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL character_set_server = 'utf8mb4'";
  mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'";

  mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE USER 'test_frappe'@'localhost' IDENTIFIED BY 'test_frappe'";
  mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE DATABASE test_frappe";
  mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "GRANT ALL PRIVILEGES ON \`test_frappe\`.* TO 'test_frappe'@'localhost'";
  mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "FLUSH PRIVILEGES";
fi
```

### PostgreSQL Database Setup

```bash
if [ "$DB" == "postgres" ]
then
  echo "root" | psql -h 127.0.0.1 -p 5432 -c "CREATE DATABASE test_frappe" -U postgres;
  echo "root" | psql -h 127.0.0.1 -p 5432 -c "CREATE USER test_frappe WITH PASSWORD 'test_frappe'" -U postgres;
fi
```

## Credentials Reference

### Standard CI Credentials

Official Frappe apps use these standard credentials:

| Component | Username/Login | Password |
|-----------|----------------|----------|
| MariaDB Root | `root` | `root` |
| PostgreSQL Root | `postgres` | `root` |
| Test Database User | `test_frappe` | `test_frappe` |
| Test Database Name | `test_frappe` | N/A |
| Frappe Admin | `Administrator` | `admin` |
| Test Site Name | `test_site` | N/A |
| SMTP (smtp4dev) | `test@example.com` | `test` |

**Note**: Older Frappe CI examples may use `travis` as the root password, but official apps now use `root`.

### Why These Credentials?

- **Standardization**: Consistent across official Frappe projects
- **Non-sensitive**: Safe for public CI environments
- **Test-only**: Never used in production
- **Easy to remember**: Simplifies debugging and maintenance

## Connection Testing

### Verify Database Connection

After service startup, verify connection before proceeding:

```yaml
      - name: Verify Database Connection
        run: |
          if [ "${{ matrix.db }}" == "mariadb" ]; then
            mysqladmin ping -h 127.0.0.1 -P 3306 -u root -ptravis
          else
            pg_isready -h 127.0.0.1 -p 5432 -U postgres
          fi
```

### Check Service Logs

If database connection fails, check service logs:

```yaml
      - name: Check Database Logs
        if: failure()
        run: |
          docker ps -a
          docker logs <container_id>
```

## Common Database Issues

### Issue: Connection Refused

**Symptoms**: Tests fail with "Connection refused" or "Can't connect to database"

**Causes**:
- Health check not passing
- Service not fully started
- Wrong port configuration

**Solutions**:
- Ensure health check is configured correctly
- Add a wait step after service startup
- Verify port mappings in service configuration

### Issue: Character Set Errors

**Symptoms**: Unicode or emoji characters fail in MariaDB

**Solutions**:
- Set global character set in database setup:
  ```bash
  mariadb -h 127.0.0.1 -u root -ptravis -e "SET GLOBAL character_set_server = 'utf8mb4'";
  mariadb -h 127.0.0.1 -u root -ptravis -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'";
  ```

### Issue: Permission Errors

**Symptoms**: "Access denied" errors during tests

**Solutions**:
- Verify GRANT statement includes backticks for database name: `` \`test_frappe\`.* ``
- Run FLUSH PRIVILEGES after creating user
- Check that credentials in site config match created user

### Issue: Database Already Exists

**Symptoms**: "Database already exists" error

**Solutions**:
- Drop database before creating if needed:
  ```bash
  mariadb -h 127.0.0.1 -u root -ptravis -e "DROP DATABASE IF EXISTS test_frappe";
  ```

## Advanced Configuration

### Custom Database Name

To use a different database name:

1. Update database creation scripts
2. Update site config JSON files
3. Ensure test site uses the correct config

### Multiple Test Sites

For testing with multiple sites:

```bash
# Create first site
mkdir ~/frappe-bench/sites/test_site_1
cp "${GITHUB_WORKSPACE}/.github/helper/db/mariadb.json" ~/frappe-bench/sites/test_site_1/site_config.json

# Create database for first site
mariadb -h 127.0.0.1 -u root -ptravis -e "CREATE DATABASE test_frappe_1";

# Create second site
mkdir ~/frappe-bench/sites/test_site_2
cp "${GITHUB_WORKSPACE}/.github/helper/db/mariadb.json" ~/frappe-bench/sites/test_site_2/site_config.json

# Create database for second site
mariadb -h 127.0.0.1 -u root -ptravis -e "CREATE DATABASE test_frappe_2";
```

Update each site's config with the correct database name.

### Database Backup and Restore

For testing migrations with production data:

```bash
# Download backup
wget https://example.com/production-backup.sql.gz

# Restore to test site
bench --site test_site --force restore ~/frappe-bench/production-backup.sql.gz

# Run migration
bench --site test_site migrate
```

## Performance Tuning

### MariaDB Performance Settings

For larger test suites, increase buffer sizes:

```yaml
services:
  mariadb:
    image: mariadb:10.6.24
    env:
      MARIADB_ROOT_PASSWORD: travis
    ports:
      - 3306:3306
    options: >-
      --health-cmd="mysqladmin ping"
      --health-interval=5s
      --health-timeout=2s
      --health-retries=3
      --innodb-buffer-pool-size=1G
      --max-allowed-packet=256M
```

### PostgreSQL Performance Settings

```yaml
services:
  postgres:
    image: postgres:12.4
    env:
      POSTGRES_PASSWORD: travis
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
      --shared-buffers=1GB
      --max-connections=200
    ports:
      - 5432:5432
```

Note: Some performance settings cannot be set via Docker options and require a custom postgresql.conf file.
