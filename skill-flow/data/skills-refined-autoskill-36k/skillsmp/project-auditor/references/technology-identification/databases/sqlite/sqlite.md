# SQLite

**Category**: databases
**Description**: SQLite embedded database
**Homepage**: https://www.sqlite.org

## Package Detection

### NPM
*SQLite Node.js clients*

- `better-sqlite3`
- `sql.js`
- `sqlite3`
- `@libsql/client`

### PYPI
*SQLite Python clients*

- `sqlite3`
- `aiosqlite`
- `sqlalchemy`

### GO
*SQLite Go clients*

- `github.com/mattn/go-sqlite3`
- `modernc.org/sqlite`

### RUBYGEMS
*SQLite Ruby client*

- `sqlite3`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]better-sqlite3['"]`
- Type: esm_import

**Pattern**: `require\(['"]better-sqlite3['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]@libsql/client['"]`
- Type: esm_import

### Python

**Pattern**: `import\s+sqlite3`
- Type: python_import

**Pattern**: `import\s+aiosqlite`
- Type: python_import

## Environment Variables

*SQLite database URL*

*SQLite database path*

*Turso (LibSQL) database URL*

*Turso auth token*


## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
