# Database Credentials

**Category**: devops/secrets/database
**Description**: Detection patterns for database connection strings and credentials
**CWE**: CWE-798, CWE-312, CWE-259

---

## Connection Strings

### PostgreSQL Connection String
**Pattern**: `postgres(ql)?://[^:]+:[^@]+@[^/]+/[^\s]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PostgreSQL connection strings with embedded credentials
- CWE-798: Use of Hard-coded Credentials

### PostgreSQL URL
**Pattern**: `postgresql://[^:]+:[^@]+@[^/]+/[^\s]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Alternative PostgreSQL URL format

### MySQL Connection String
**Pattern**: `mysql://[^:]+:[^@]+@[^/]+/[^\s]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- MySQL connection strings with embedded credentials

### MySQL PyMySQL Connection
**Pattern**: `mysql\+pymysql://[^:]+:[^@]+@[^/]+/[^\s]+`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- SQLAlchemy MySQL connection with PyMySQL driver

### MongoDB Connection String
**Pattern**: `mongodb(\+srv)?://[^:]+:[^@]+@[^\s]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- MongoDB connection strings (including Atlas srv format)

### Redis Connection String
**Pattern**: `redis://[^:]*:[^@]+@[^/]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Redis URLs may omit username (empty before first `:`)

### Redis TLS Connection String
**Pattern**: `rediss://[^:]*:[^@]+@[^/]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Redis with TLS connection strings

### SQL Server Connection String
**Pattern**: `Server=[^;]+;.*Password=[^;]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- ADO.NET SQL Server connection strings

### SQL Server Data Source
**Pattern**: `Data Source=[^;]+;.*Password=[^;]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Alternative SQL Server connection format

### Oracle Connection String
**Pattern**: `jdbc:oracle:[^:]+:@[^:]+:[^:]+:[^\s]+`
**Type**: regex
**Severity**: critical
**Languages**: [java]
- Oracle JDBC connection strings

---

## Environment Variables

### Database URL Variable
**Pattern**: `DATABASE_URL\s*[=:]\s*['"]?[^\s'"]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- DATABASE_URL environment variable with value

### Database Password Variable
**Pattern**: `DB_PASSWORD\s*[=:]\s*['"]?[^\s'"]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- DB_PASSWORD environment variable

### PostgreSQL Password Variable
**Pattern**: `POSTGRES_PASSWORD\s*[=:]\s*['"]?[^\s'"]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PostgreSQL container password

### MySQL Password Variable
**Pattern**: `MYSQL_PASSWORD\s*[=:]\s*['"]?[^\s'"]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- MySQL container password

### MySQL Root Password Variable
**Pattern**: `MYSQL_ROOT_PASSWORD\s*[=:]\s*['"]?[^\s'"]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- MySQL root password (highest privilege)

### MongoDB Password Variable
**Pattern**: `MONGO_PASSWORD\s*[=:]\s*['"]?[^\s'"]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- MongoDB password environment variable

### Redis Password Variable
**Pattern**: `REDIS_PASSWORD\s*[=:]\s*['"]?[^\s'"]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Redis password environment variable

---

## Configuration Files

### Django Database Password
**Pattern**: `['"]PASSWORD['"]\s*:\s*['"][^'"]+['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Django settings.py database password

### Rails Database Password
**Pattern**: `password:\s*[^\s#]+`
**Type**: regex
**Severity**: critical
**Languages**: [ruby]
- Rails database.yml password field

### Node.js Fallback Password
**Pattern**: `password:\s*process\.env\.[A-Z_]+\s*\|\|\s*['"][^'"]+['"]`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Fallback passwords in Node.js configs

### PHP Database Password
**Pattern**: `\$db_password\s*=\s*['"][^'"]+['"]`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- PHP database password variables

### PHP Define Password
**Pattern**: `define\(['"]DB_PASSWORD['"]\s*,\s*['"][^'"]+['"]\)`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- PHP constant database password

---

## ORM Configuration

### Prisma Database URL
**Pattern**: `DATABASE_URL\s*=\s*["']postgresql://[^:]+:[^@]+@[^/]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Prisma schema database URL

### TypeORM Password
**Pattern**: `password:\s*["'][^"']+["']`
**Type**: regex
**Severity**: critical
**Languages**: [typescript, javascript]
- TypeORM configuration password

### Sequelize Connection
**Pattern**: `new Sequelize\(['"][^'"]+['"]\s*,\s*['"][^'"]+['"]\s*,\s*['"][^'"]+['"]`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Sequelize constructor with inline credentials

### SQLAlchemy Engine
**Pattern**: `create_engine\(['"]postgresql://[^:]+:[^@]+@`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- SQLAlchemy engine with embedded credentials

---

## Cloud Database Services

### AWS RDS Hostname
**Pattern**: `[a-z]+-[a-z0-9]+\.[a-z0-9]+\.[a-z]+-[a-z]+-[0-9]\.rds\.amazonaws\.com`
**Type**: regex
**Severity**: informational
**Languages**: [all]
- AWS RDS hostname (not secret itself, indicates DB location)

### Supabase Database URL
**Pattern**: `postgresql://postgres:[^@]+@db\.[a-z]+\.supabase\.co`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Supabase database connection string

### PlanetScale Connection
**Pattern**: `mysql://[^:]+:[^@]+@[^/]+\.psdb\.cloud`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PlanetScale database connection

### MongoDB Atlas Connection
**Pattern**: `mongodb\+srv://[^:]+:[^@]+@[^/]+\.mongodb\.net`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- MongoDB Atlas connection string

### Neon Database Connection
**Pattern**: `postgresql://[^:]+:[^@]+@[^/]+\.neon\.tech`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Neon database connection string

---

## Detection Notes

### High-Risk Files
- `.env`, `.env.local`, `.env.production`
- `config/database.yml`
- `settings.py`, `local_settings.py`
- `docker-compose.yml`
- `application.properties`
- `appsettings.json`

### False Positives
- `localhost` connections in development
- Example files (`.env.example`)
- Placeholder values (`your_password_here`)
- Test database URLs

### Password in Connection String
**Pattern**: `://[^:]+:([^@]+)@`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Generic pattern capturing password between `:` and `@`

### Security Considerations
- Connection strings expose host, potentially allowing network mapping
- Credentials should use secret management
- Rotate credentials if exposed in git history

---

## References

- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-312: Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html)
- [CWE-259: Use of Hard-coded Password](https://cwe.mitre.org/data/definitions/259.html)
