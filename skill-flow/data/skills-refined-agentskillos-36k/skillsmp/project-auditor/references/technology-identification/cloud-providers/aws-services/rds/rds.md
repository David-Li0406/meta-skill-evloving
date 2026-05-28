# Amazon RDS (Relational Database Service)

**Category**: cloud-providers/aws-services
**Description**: Managed relational database service
**Homepage**: https://aws.amazon.com/rds

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Database packages (work with RDS)*

- `mysql2` - MySQL driver
- `pg` - PostgreSQL driver
- `tedious` - SQL Server driver
- `oracledb` - Oracle driver
- `@aws-sdk/client-rds` - RDS SDK v3

#### PYPI
*Database packages (work with RDS)*

- `boto3` - AWS SDK (includes RDS)
- `pymysql` - MySQL driver
- `psycopg2` - PostgreSQL driver
- `sqlalchemy` - ORM (works with RDS)

#### GO
*Database packages (work with RDS)*

- `github.com/aws/aws-sdk-go-v2/service/rds` - RDS SDK v2
- `github.com/go-sql-driver/mysql` - MySQL driver
- `github.com/lib/pq` - PostgreSQL driver

---

## TIER 2: Deep Detection (File-based)

### Code Patterns

**Pattern**: `rds\.amazonaws\.com|rds-[a-z0-9-]+\.amazonaws\.com`
- RDS endpoints
- Example: `mydb.abc123.us-east-1.rds.amazonaws.com`

**Pattern**: `RDS_HOSTNAME|RDS_DB_NAME|RDS_USERNAME|RDS_PASSWORD`
- RDS environment variables
- Example: `RDS_HOSTNAME=mydb.abc123.us-east-1.rds.amazonaws.com`

**Pattern**: `arn:aws:rds:[a-z0-9-]+:[0-9]+:db:`
- RDS DB ARN
- Example: `arn:aws:rds:us-east-1:123456789:db:mydb`

**Pattern**: `Type:\s*['"]?AWS::RDS::DBInstance`
- CloudFormation RDS resource

**Pattern**: `:[0-9]+\.rds\.amazonaws\.com:[0-9]+`
- RDS connection string pattern
- Example: `mydb.abc123.us-east-1.rds.amazonaws.com:3306`

---

## Environment Variables

- `RDS_HOSTNAME` - RDS hostname
- `RDS_DB_NAME` - Database name
- `RDS_USERNAME` - Database username
- `RDS_PASSWORD` - Database password
- `RDS_PORT` - Database port
- `DATABASE_URL` - Connection URL (often RDS)

## Detection Notes

- Supports MySQL, PostgreSQL, MariaDB, Oracle, SQL Server
- Aurora is Amazon's cloud-native database
- IAM authentication available
- Proxy for connection pooling
- Multi-AZ for high availability

---

## Secrets Detection

### Credentials

#### RDS Password
**Pattern**: `(?:RDS|rds).*(?:password|PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: RDS database password
**Example**: `RDS_PASSWORD=mypassword`

#### Database URL with Credentials
**Pattern**: `(?:mysql|postgresql|postgres|oracle|sqlserver)://([^:]+):([^@]+)@[a-z0-9.-]+\.rds\.amazonaws\.com`
**Severity**: critical
**Description**: RDS connection URL with embedded credentials
**Example**: `postgresql://user:pass@mydb.abc123.us-east-1.rds.amazonaws.com/dbname`

---

## TIER 3: Configuration Extraction

### Hostname Extraction

**Pattern**: `(?:host|hostname|RDS_HOSTNAME)\s*[=:]\s*['"]?([a-z0-9.-]+\.rds\.amazonaws\.com)['"]?`
- RDS hostname
- Extracts: `hostname`
- Example: `RDS_HOSTNAME=mydb.abc123.us-east-1.rds.amazonaws.com`

### Database Name Extraction

**Pattern**: `(?:database|dbname|RDS_DB_NAME)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Database name
- Extracts: `db_name`
- Example: `RDS_DB_NAME=myapp`

### Port Extraction

**Pattern**: `(?:port|RDS_PORT)\s*[=:]\s*['"]?([0-9]+)['"]?`
- Database port
- Extracts: `port`
- Example: `RDS_PORT=5432`
