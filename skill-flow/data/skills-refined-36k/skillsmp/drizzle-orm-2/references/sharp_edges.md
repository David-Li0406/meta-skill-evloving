# Drizzle Orm - Sharp Edges

## Drizzle Relations Not Fk

### **Id**
drizzle-relations-not-fk
### **Summary**
Relations don't create foreign key constraints
### **Severity**
critical
### **Situation**
  You define relations() for your tables expecting database-level foreign keys.
  You delete a user and expect cascade to delete their posts. Posts remain orphaned.
  
### **Why**
  Drizzle separates concerns: schema defines database structure, relations define
  query patterns. Relations are for db.query API only - they're TypeScript metadata,
  not SQL constraints. Without .references() in your schema, there's no foreign key,
  no ON DELETE CASCADE, and no referential integrity.
  
### **Solution**
  # WRONG: Relation without foreign key
  export const posts = pgTable('posts', {
    authorId: uuid('author_id').notNull(), // No FK!
  });
  export const postsRelations = relations(posts, ({ one }) => ({
    author: one(users, { fields: [posts.authorId], references: [users.id] }),
  }));
  
  # RIGHT: Foreign key AND relation
  export const posts = pgTable('posts', {
    authorId: uuid('author_id')
      .notNull()
      .references(() => users.id, { onDelete: 'cascade' }), // FK!
  });
  // Then define relation separately for query API
  
### **Symptoms**
  - Orphaned records after deletion
  - No cascade behavior
  - Data integrity violations
  - "constraint violation" errors missing when expected
### **Detection Pattern**
relations\([^)]+,\s*\(\{[^}]*\}\)\s*=>\s*\(\{[^}]*one\([^)]+\)[^}]*\}\)\)
### **Version Range**
>=0.20.0

## Drizzle Limit Array Type

### **Id**
drizzle-limit-array-type
### **Summary**
limit(1) still returns an array, not a single object
### **Severity**
high
### **Situation**
  You use .limit(1) expecting a single object. You access result.name and get
  undefined because result is still an array.
  
### **Why**
  Drizzle's type system infers arrays for all select queries regardless of limit.
  This is a known limitation - TypeScript can't narrow based on runtime values.
  The team is aware (GitHub issue #5173) but it's a fundamental type inference
  limitation.
  
### **Solution**
  // WRONG: Assumes single object
  const user = await db.select().from(users).where(eq(users.id, id)).limit(1);
  console.log(user.name); // Error! user is an array
  
  // RIGHT: Destructure or use findFirst
  const [user] = await db.select().from(users).where(eq(users.id, id)).limit(1);
  console.log(user?.name); // Works!
  
  // BETTER: Use relational query findFirst
  const user = await db.query.users.findFirst({
    where: eq(users.id, id),
  });
  console.log(user?.name); // Returns single object or undefined
  
### **Symptoms**
  - Cannot read property of undefined
  - TypeScript errors about arrays vs objects
  - Accessing .property on array
### **Detection Pattern**
\.limit\(1\)\s*;?\s*\n[^[]*\.\w+
### **Version Range**
>=0.20.0

## Drizzle Push Production

### **Id**
drizzle-push-production
### **Summary**
Using drizzle-kit push in production
### **Severity**
critical
### **Situation**
  You run `drizzle-kit push` against your production database because it's
  faster than generating migrations. Schema changes apply but there's no
  record of what changed.
  
### **Why**
  push applies changes directly without migration history. When something breaks,
  you can't rollback. Team members don't know what changed. CI/CD has no
  reproducible migration to run. It's convenient for local dev, dangerous for prod.
  
### **Solution**
  # Development workflow
  npx drizzle-kit push  # Fast iteration, no files
  
  # Production workflow
  npx drizzle-kit generate  # Creates SQL migration file
  # Review the SQL in drizzle/ folder
  npx drizzle-kit migrate   # Apply with history
  
  # In CI/CD
  npx drizzle-kit migrate   # Always use migrate, never push
  
### **Symptoms**
  - No migration history
  - Can't rollback changes
  - "What changed?" confusion
  - Schema drift between environments
### **Detection Pattern**

### **Version Range**
>=0.20.0

## Drizzle Missing Schema Import

### **Id**
drizzle-missing-schema-import
### **Summary**
db.query fails without schema passed to drizzle()
### **Severity**
high
### **Situation**
  You initialize drizzle() without the schema parameter. db.select works fine.
  Then you try db.query.users.findMany() and get a runtime error.
  
### **Why**
  The relational query API (db.query) requires schema metadata to build queries.
  The basic CRUD API (db.select/insert/update/delete) doesn't need it. If you
  forget to pass schema, db.query silently fails or throws at runtime.
  
### **Solution**
  // WRONG: No schema, db.query won't work
  import { drizzle } from 'drizzle-orm/postgres-js';
  const db = drizzle(client);
  await db.query.users.findMany(); // Runtime error!
  
  // RIGHT: Pass schema for relational queries
  import { drizzle } from 'drizzle-orm/postgres-js';
  import * as schema from './schema';
  const db = drizzle(client, { schema });
  await db.query.users.findMany(); // Works!
  
### **Symptoms**
  - Cannot read property 'users' of undefined
  - db.query returns undefined
  - db.query.tableName is not a function
### **Detection Pattern**
drizzle\([^,)]+\)(?!\s*,\s*\{[^}]*schema)
### **Version Range**
>=0.20.0

## Drizzle Jsonb Default Push

### **Id**
drizzle-jsonb-default-push
### **Summary**
drizzle-kit push fails with jsonb default values
### **Severity**
high
### **Situation**
  You have a PostgreSQL jsonb column with a default value. Running drizzle-kit
  push fails with an obscure error.
  
### **Why**
  Known bug in drizzle-kit (as of early 2025). The push command doesn't handle
  jsonb columns with default values correctly. The generate command works fine.
  
### **Solution**
  # WORKAROUND: Use generate instead of push
  npx drizzle-kit generate
  npx drizzle-kit migrate
  
  # Or define without default, set in application code
  export const settings = pgTable('settings', {
    data: jsonb('data').notNull(), // No default
  });
  
  // Set default in insert
  await db.insert(settings).values({
    data: { theme: 'dark', lang: 'en' }, // Default here
  });
  
### **Symptoms**
  - push command fails
  - Error messages about jsonb parsing
  - Works with generate but not push
### **Detection Pattern**
jsonb\([^)]+\)\.default\(
### **Version Range**
>=0.20.0

## Drizzle Planetscale Lateral

### **Id**
drizzle-planetscale-lateral
### **Summary**
Relational queries don't work on PlanetScale
### **Severity**
high
### **Situation**
  You use db.query with PlanetScale (Vitess-based MySQL). Queries fail with
  SQL syntax errors.
  
### **Why**
  Drizzle's relational queries use lateral joins (subqueries in FROM clause).
  PlanetScale's Vitess-based MySQL doesn't support lateral joins. This is a
  fundamental limitation of the database, not Drizzle.
  
### **Solution**
  // CAN'T USE: Relational queries on PlanetScale
  const result = await db.query.users.findMany({
    with: { posts: true }, // Uses lateral joins - fails!
  });
  
  // MUST USE: Manual joins
  const result = await db
    .select()
    .from(users)
    .leftJoin(posts, eq(posts.authorId, users.id));
  
  // Or switch to Neon/Supabase (real PostgreSQL with lateral join support)
  
### **Symptoms**
  - SQL syntax errors
  - "Unsupported query" from PlanetScale
  - Works locally but fails in production
### **Detection Pattern**

### **Version Range**
>=0.20.0

## Drizzle N Plus One Manual

### **Id**
drizzle-n-plus-one-manual
### **Summary**
Manual N+1 queries instead of using relational API
### **Severity**
medium
### **Situation**
  You fetch users, then loop through to fetch each user's posts separately.
  100 users = 101 database queries.
  
### **Why**
  Each db.select() is a round trip to the database. With nested loops, query
  count explodes. Drizzle's relational queries (db.query) use lateral joins
  to fetch everything in a single SQL query.
  
### **Solution**
  // WRONG: N+1 queries
  const users = await db.select().from(usersTable);
  for (const user of users) {
    const posts = await db.select().from(postsTable)
      .where(eq(postsTable.authorId, user.id));
    user.posts = posts; // 101 queries for 100 users!
  }
  
  // RIGHT: Single query with relations
  const usersWithPosts = await db.query.users.findMany({
    with: { posts: true },
  });
  // 1 query total, lateral joins handle the rest
  
### **Symptoms**
  - Slow page loads
  - Database connection exhaustion
  - Query count grows with data size
### **Detection Pattern**
for\s*\([^)]+of[^)]+\)\s*\{[^}]*await\s+db\.
### **Version Range**
>=0.20.0

## Drizzle Sql Injection

### **Id**
drizzle-sql-injection
### **Summary**
Raw SQL interpolation creates injection vulnerabilities
### **Severity**
critical
### **Situation**
  You use sql`` template literal with user input interpolated directly.
  Attacker sends malicious input, executes arbitrary SQL.
  
### **Why**
  sql`` is a template literal - JavaScript string interpolation happens before
  Drizzle sees it. User input becomes part of the SQL string, not a parameter.
  Classic SQL injection, even in a "modern" ORM.
  
### **Solution**
  // WRONG: SQL injection!
  const name = req.query.name; // Could be "'; DROP TABLE users; --"
  const result = await db.execute(
    sql`SELECT * FROM users WHERE name = '${name}'`
  );
  
  // RIGHT: Use Drizzle's query builder (auto-escapes)
  const result = await db
    .select()
    .from(users)
    .where(eq(users.name, name));
  
  // RIGHT: Use sql.placeholder for dynamic values
  const result = await db.execute(
    sql`SELECT * FROM users WHERE name = ${name}`
  );
  // No quotes around ${name} - Drizzle parameterizes it
  
### **Symptoms**
  - Security audit findings
  - Unexpected query results
  - Database manipulation
### **Detection Pattern**
sql`[^`]*'\$\{[^}]+\}'[^`]*`
### **Version Range**
>=0.20.0

## Drizzle Migration Rename Drop

### **Id**
drizzle-migration-rename-drop
### **Summary**
Column rename generates DROP + CREATE, losing data
### **Severity**
high
### **Situation**
  You rename a column in your schema. drizzle-kit generate creates a migration
  that drops the old column and creates a new one. All data in that column is lost.
  
### **Why**
  Drizzle can't automatically detect renames - it sees a removed column and a
  new column. Unlike Prisma, Drizzle doesn't have rename detection by default.
  The migration file will DROP then CREATE.
  
### **Solution**
  # After running drizzle-kit generate, REVIEW the SQL!
  
  # WRONG (auto-generated):
  ALTER TABLE users DROP COLUMN old_name;
  ALTER TABLE users ADD COLUMN new_name text;
  
  # RIGHT (manually edit migration):
  ALTER TABLE users RENAME COLUMN old_name TO new_name;
  
  # Or use drizzle-kit interactive mode
  npx drizzle-kit generate
  # When prompted about potential rename, choose "rename" not "drop+create"
  
### **Symptoms**
  - Data loss after migration
  - Column values are NULL after rename
  - Wait, where did my data go?
### **Detection Pattern**

### **Version Range**
>=0.20.0

## Drizzle Serial Vs Identity

### **Id**
drizzle-serial-vs-identity
### **Summary**
Using serial instead of identity for PostgreSQL
### **Severity**
medium
### **Situation**
  You use serial() for auto-incrementing IDs in PostgreSQL. Everything works,
  but you're using a legacy approach.
  
### **Why**
  PostgreSQL recommends identity columns over serial types (since PostgreSQL 10).
  Drizzle has embraced this in 2025. identity() is more standard SQL, works
  better with COPY, and is the modern approach.
  
### **Solution**
  // OLD (still works, but legacy):
  export const users = pgTable('users', {
    id: serial('id').primaryKey(),
  });
  
  // MODERN (PostgreSQL 10+ recommendation):
  export const users = pgTable('users', {
    id: integer('id').primaryKey().generatedAlwaysAsIdentity(),
  });
  
  // Or use UUIDs (best for distributed systems):
  export const users = pgTable('users', {
    id: uuid('id').primaryKey().defaultRandom(),
  });
  
### **Symptoms**
  - Works but not following best practices
  - Issues with COPY operations
  - Sequence ownership complications
### **Detection Pattern**
serial\s*\(
### **Version Range**
>=0.30.0

## Drizzle Beta Breaking

### **Id**
drizzle-beta-breaking
### **Summary**
Beta version has breaking changes from stable
### **Severity**
medium
### **Situation**
  You upgrade to drizzle-orm@beta or 1.0.0-beta.x. Your queries break,
  especially if using db.query or other libraries that depend on Drizzle.
  
### **Why**
  The v1.0.0 beta introduced breaking changes: db.query moved to db._query,
  new relation syntax, API changes. Libraries like better-auth haven't updated
  yet. The beta is not production-ready.
  
### **Solution**
  # SAFE: Stay on stable
  npm install drizzle-orm@latest  # Gets 0.x stable version
  
  # RISKY: Beta for testing only
  npm install drizzle-orm@beta
  
  # If on beta and having issues:
  npm install drizzle-orm@0.44.7  # Last stable
  
  # Check ecosystem compatibility before upgrading
  
### **Symptoms**
  - "db.query is not a function" (moved to db._query)
  - Type errors after upgrade
  - Third-party library incompatibility
### **Detection Pattern**
"drizzle-orm":\s*"[^"]*beta
### **Version Range**
>=1.0.0-beta.1

## Drizzle Many To Many Mapping

### **Id**
drizzle-many-to-many-mapping
### **Summary**
Many-to-many through tables require manual mapping
### **Severity**
medium
### **Situation**
  You have a many-to-many relation with a junction table. You want to get
  users with their tags directly, but the query returns the junction table.
  
### **Why**
  Drizzle's relational queries can't "skip" the junction table. You get the
  through table in your results and must map to the related table yourself.
  This is a known limitation.
  
### **Solution**
  // Schema with junction table
  export const usersToTags = pgTable('users_to_tags', {
    userId: uuid('user_id').references(() => users.id),
    tagId: uuid('tag_id').references(() => tags.id),
  });
  
  // Query returns junction table
  const result = await db.query.users.findFirst({
    with: { usersToTags: { with: { tag: true } } },
  });
  // result.usersToTags is array of { tag: { name: '...' } }
  
  // Map to clean structure
  const userWithTags = {
    ...result,
    tags: result.usersToTags.map((ut) => ut.tag),
  };
  
### **Symptoms**
  - Extra nesting in query results
  - Can't get clean many-to-many
  - Junction table in response
### **Detection Pattern**

### **Version Range**
>=0.20.0