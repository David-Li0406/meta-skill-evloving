---
name: database-skill
description: Design and manage databases including tables, migrations, and schema structure. Use for backend and full-stack projects.
---

# Database Design & Management

## Instructions

1. **Schema design**
   - Identify entities and relationships
   - Normalize data where needed
   - Define primary and foreign keys

2. **Tables creation**
   - Use clear and meaningful table names
   - Define proper data types
   - Add constraints (NOT NULL, UNIQUE)

3. **Migrations**
   - Create versioned migrations
   - Support rollback and re-run
   - Keep migrations small and focused

4. **Indexes & performance**
   - Add indexes on frequently queried columns
   - Avoid over-indexing
   - Optimize for read/write balance

## Best Practices
- Follow consistent naming conventions
- Keep schema simple and scalable
- Always use migrations (no manual DB changes)
- Document schema changes
- Test migrations before production

## Example Structure
```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
