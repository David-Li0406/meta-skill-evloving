---
name: myggv-gps-project-management
description: Use this skill for managing the MyGGV GPS project, including database operations with Supabase and project documentation in Archon.
---

# Skill body

## Objective

Manage the MyGGV GPS project, including database operations with Supabase and project documentation in Archon.

## Scope

### Included

- **Database Management** (using Supabase):
  - Execute SQL queries
  - Create and apply migrations
  - List tables and extensions
  - Check advisors for security and performance
  - Consult logs
  - Generate TypeScript types

- **Project Management** (using Archon):
  - Manage project documentation (specs, notes, guides)
  - Manage tasks (to-do, doing, review, done)
  - Search in the knowledge base for documentation and code examples

### Excluded

- Deployment → use `netlify-deploy`
- Code navigation → use `maplibre-navigation`

## Database Operations with Supabase

### Check Database Status

```javascript
mcp__supabase__list_tables(); // List tables
mcp__supabase__get_advisors({ type: "security" }); // Check RLS
mcp__supabase__get_advisors({ type: "performance" }); // Check optimizations
```

### Create a Migration

```javascript
// Analyze the need
mcp__supabase__apply_migration({
  name: "add_poi_category",
  query: "ALTER TABLE public_pois ADD COLUMN category TEXT;"
});
// Verify with execute_sql
```

### Query Data

```javascript
mcp__supabase__execute_sql({
  query: "SELECT * FROM locations WHERE name LIKE 'Block%' LIMIT 10;"
});
```

## Project Management with Archon

### Find the Project

```javascript
mcp__archon__find_projects({
  query: "ggv gps",
});
```

### Create/Update the Project

```javascript
mcp__archon__manage_project({
  action: "create",
  title: "MyGGV GPS",
  description: "Web GPS application for Garden Grove Village",
  github_repo: "https://github.com/user/new-ggv-gps",
});
```

### Manage Tasks

```javascript
// Create a task
mcp__archon__manage_task({
  action: "create",
  title: "New Feature Development",
  description: "Develop new features for the MyGGV GPS application.",
});
```

## Best Practices

1. Always check advisors after a DDL migration.
2. Use snake_case for migration names.
3. Never hardcode IDs in data migrations.
4. Verify RLS on all public tables.
5. Use Archon for documentation searches instead of direct Supabase documentation queries.