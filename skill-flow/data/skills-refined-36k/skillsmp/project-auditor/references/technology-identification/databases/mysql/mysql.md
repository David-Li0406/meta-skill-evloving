# MySQL

**Category**: databases
**Description**: MySQL relational database drivers and ORMs
**Homepage**: https://www.mysql.com

## Package Detection

### NPM
*Node.js MySQL clients and ORMs*

- `mysql`
- `mysql2`
- `sequelize`
- `typeorm`
- `prisma`
- `knex`

### PYPI
*Python MySQL drivers*

- `mysql-connector-python`
- `mysqlclient`
- `pymysql`
- `aiomysql`
- `sqlalchemy`

### RUBYGEMS
*Ruby MySQL drivers*

- `mysql2`
- `activerecord-mysql2-adapter`

### MAVEN
*Java MySQL JDBC driver*

- `mysql:mysql-connector-java`
- `com.mysql:mysql-connector-j`

### GO
*Go MySQL driver*

- `github.com/go-sql-driver/mysql`

### Related Packages
- `mysql2-promise`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]mysql2?['"]`
- Type: esm_import

**Pattern**: `require\(['"]mysql2?['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]mysql2/promise['"]`
- Type: esm_import

### Python

**Pattern**: `import\s+mysql\.connector`
- Type: python_import

**Pattern**: `import\s+pymysql`
- Type: python_import

**Pattern**: `from\s+pymysql`
- Type: python_import

**Pattern**: `import\s+MySQLdb`
- Type: python_import

### Go

**Pattern**: `"github\.com/go-sql-driver/mysql"`
- Type: go_import

## Environment Variables

*MySQL connection URL*

*MySQL host*

*MySQL port*

*MySQL database name*

*MySQL username*

*MySQL password*

*MySQL root password (Docker)*

*Database URL with MySQL protocol*


## Detection Notes

- Check for MYSQL_URL or DATABASE_URL containing mysql://
- Also covers MariaDB (compatible driver)
- Common with ORMs like Sequelize, TypeORM

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
