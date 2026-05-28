# Prisma DB Scripts

This directory contains utility scripts for database inspection and management.

## Related Resources

- **[../examples/](../examples/)**: Code examples demonstrating optimized queries, transactions, and schema design patterns
- **[../resources/](../resources/)**: Comprehensive guides for query optimization, inspection workflows, and best practices
- **[../SKILL.md](../SKILL.md)**: Core skill documentation with quick reference

## Raw Query Script

**File:** `raw-query.ts`

### Purpose

Execute raw SQL queries directly against PostgreSQL database for inspection, debugging, and data validation during development.

### Features

- **Automatic Connection**: Reads `DATABASE_URL` from `.env` file
- **Fallback Prompt**: Asks for credentials if `.env` is missing
- **Interactive Mode**: Run multiple queries in a session
- **JSON Output**: Results output as JSON for easy parsing
- **Error Handling**: Clear error messages with query timing

### Installation

Ensure dependencies are installed:

```bash
pnpm install
```

The script uses `pg` (PostgreSQL client) which should already be in your dependencies.

### Usage

#### Single Query Execution

```bash
tsx raw-query.ts "SELECT * FROM \"Session\" LIMIT 10"
```

#### Interactive Mode

```bash
tsx raw-query.ts --interactive
```

Then enter SQL queries at the prompt:

```sql
sql> SELECT COUNT(*) FROM "Session";
sql> \q  -- to quit
```

### Connection Behavior

1. **First**: Checks `.env` file for `DATABASE_URL`
2. **Fallback**: Prompts for credentials if needed:
   - Host (default: localhost)
   - Port (default: 5432)
   - Database name
   - Username
   - Password (hidden)

### Example Queries

For more inspection queries and workflows, see:
- **[Common Inspection Queries](../resources/common-inspection-queries.md)**: Comprehensive collection of useful SQL queries
- **[Database Inspection Workflow](../resources/database-inspection-workflow.md)**: Structured workflows for different investigation scenarios

#### Check Database Health

```bash
tsx raw-query.ts "
  SELECT
    COUNT(DISTINCT \"venueId\") as facilities,
    COUNT(*) as total_sessions,
    COUNT(*) FILTER (WHERE available = true) as available
  FROM \"Session\"
  WHERE date >= CURRENT_DATE;
"
```

#### List Tables

```bash
tsx raw-query.ts "
  SELECT table_name
  FROM information_schema.tables
  WHERE table_schema = 'public'
  ORDER BY table_name;
"
```

#### Recent Crawl Jobs

```bash
tsx raw-query.ts "
  SELECT
    id,
    status,
    \"playDate\",
    \"startedAt\",
    \"completedAt\"
  FROM \"CrawlJob\"
  ORDER BY \"startedAt\" DESC
  LIMIT 5;
"
```

### Output Format

Results are returned as JSON:

```json
[
  {
    "id": "clm1234567890",
    "status": "COMPLETED",
    "playDate": "2025-01-15",
    "startedAt": "2025-01-15T10:30:00.000Z",
    "completedAt": "2025-01-15T10:35:00.000Z"
  }
]
```

### Error Handling

If the `.env` file is missing or `DATABASE_URL` is invalid:

```
⚠️  No valid DATABASE_URL found in .env

🔑 Database Connection Required
Please provide your PostgreSQL credentials:

Host (default: localhost):
Port (default: 5432):
Database name: smartplay
Username: postgres
Password: ****

✅ Connected to database successfully
```

### Security Notes

- Password input is hidden (shown as `****`)
- Credentials are never logged or stored
- `.env` should not be committed to version control
- Connection uses connection pooling for efficiency

### Integration with AI Agents

This script is designed to be called by AI agents (like Claude Code) during:

1. **Initial Investigation** - Understanding database state
2. **Debugging** - Inspecting crawler issues and failures
3. **Performance Analysis** - Checking table sizes and index usage
4. **Data Validation** - Verifying data integrity before deployment

### Troubleshooting

**Connection fails:**

- Verify PostgreSQL is running: `psql --version`
- Check credentials in `.env`
- Test connection: `psql $DATABASE_URL`

**Permission denied:**

- Ensure user has SELECT permissions on tables
- Check database user roles: `psql -c "\du"`

**Script not found:**

- Ensure running from project root
- Use absolute path: `tsx .agent/skills/prisma-db/scripts/raw-query.ts`

**tsx command not found:**

- Install dependencies: `pnpm install`
- Or use `npx tsx` instead
