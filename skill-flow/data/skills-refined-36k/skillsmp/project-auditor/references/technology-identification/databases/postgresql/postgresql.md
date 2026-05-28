# PostgreSQL

**Category**: databases
**Description**: PostgreSQL relational database drivers and ORMs
**Homepage**: https://www.postgresql.org

## Package Detection

### NPM
*Node.js PostgreSQL clients and ORMs*

- `pg`
- `pg-promise`
- `postgres`
- `sequelize`
- `typeorm`
- `prisma`
- `drizzle-orm`
- `knex`

### PYPI
*Python PostgreSQL drivers*

- `psycopg2`
- `psycopg2-binary`
- `psycopg`
- `asyncpg`
- `sqlalchemy`
- `databases`

### RUBYGEMS
*Ruby PostgreSQL drivers*

- `pg`
- `activerecord-postgresql-adapter`

### MAVEN
*Java PostgreSQL JDBC driver*

- `org.postgresql:postgresql`

### GO
*Go PostgreSQL drivers*

- `github.com/lib/pq`
- `github.com/jackc/pgx`

### Related Packages
- `pg-pool`
- `pg-cursor`
- `pg-query-stream`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]pg['"]`
- Type: esm_import

**Pattern**: `require\(['"]pg['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]postgres['"]`
- Type: esm_import

**Pattern**: `from\s+['"]pg-promise['"]`
- Type: esm_import

### Python

**Pattern**: `import\s+psycopg2`
- Type: python_import

**Pattern**: `from\s+psycopg2`
- Type: python_import

**Pattern**: `import\s+asyncpg`
- Type: python_import

**Pattern**: `from\s+asyncpg`
- Type: python_import

### Go

**Pattern**: `"github\.com/lib/pq"`
- Type: go_import

**Pattern**: `"github\.com/jackc/pgx`
- Type: go_import

### Ruby

**Pattern**: `require\s+['"]pg['"]`
- Type: ruby_require

## Environment Variables

*PostgreSQL connection URL*

*PostgreSQL host*

*PostgreSQL port*

*PostgreSQL database name*

*PostgreSQL username*

*PostgreSQL password*

*PostgreSQL connection URL (alternative)*


## Detection Notes

- Check for DATABASE_URL containing postgres://
- Look for .pgpass files
- Common with ORMs like Prisma, TypeORM, Sequelize

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
