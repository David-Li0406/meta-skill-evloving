# Supabase - Database

**Pages:** 192

---

## Postgres Roles | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/roles

**Contents:**
- Postgres Roles
- Managing access to your Postgres database and configuring permissions.
- Users vs roles#
- Creating roles#
- Creating users#
- Passwords#
  - Special symbols in passwords#
  - Changing your project password#
- Granting permissions#
- Revoking permissions#

Managing access to your Postgres database and configuring permissions.

Postgres manages database access permissions using the concept of roles. Generally you wouldn't use these roles for your own application - they are mostly for configuring system access to your database. If you want to configure application access, then you should use Row Level Security (RLS). You can also implement Role-based Access Control on top of RLS.

In Postgres, roles can function as users or groups of users. Users are roles with login privileges, while groups (also known as role groups) are roles that don't have login privileges but can be used to manage permissions for multiple users.

You can create a role using the create role command:

Roles and users are essentially the same in Postgres, however if you want to use password-logins for a specific role, then you can use WITH LOGIN PASSWORD:

Your Postgres database is the core of your Supabase project, so it's important that every role has a strong, secure password at all times. Here are some tips for creating a secure password:

If you use special symbols in your Postgres password, you must remember to percent-encode your password later if using the Postgres connection string, for example, postgresql://postgres.projectref:p%3Dword@aws-0-us-east-1.pooler.supabase.com:6543/postgres

When you created your project you were also asked to enter a password. This is the password for the postgres role in your database. You can update this from the Dashboard under the Database Settings page. You should never give this to third-party service unless you absolutely trust them. Instead, we recommend that you create a new user for every service that you want to give access too. This will also help you with debugging - you can see every query that each role is executing in your database within pg_stat_statements.

Changing the password does not result in any downtime. All connected services, such as PostgREST, PgBouncer, and other Supabase managed services, are automatically updated to use the latest password to ensure availability. However, if you have any external services connecting to the Supabase database using hardcoded username/password credentials, a manual update will be required.

Roles can be granted various permissions on database objects using the GRANT command. Permissions include SELECT, INSERT, UPDATE, and DELETE. You can configure access to almost any object inside your database - including tables, views, functions, and triggers.

Permissions can be revoked using the REVOKE command:

Roles can be organized in a hierarchy, where one role can inherit permissions from another. This simplifies permission management, as you can define permissions at a higher level and have them automatically apply to all child roles.

To create a role hierarchy, you first need to create the parent and child roles. The child role will inherit permissions from its parent. Child roles can be added using the INHERIT option when creating the role:

In some cases, you might want to prevent a role from having a child relationship (typically superuser roles). You can prevent inheritance relations using NOINHERIT:

Postgres comes with a set of predefined roles. Supabase extends this with a default set of roles which are configured on your database when you start a new project:

The default Postgres role. This has admin privileges.

For unauthenticated, public access. This is the role which the API (PostgREST) will use when a user is not logged in.

A special role for the API (PostgREST). It has very limited access, and is used to validate a JWT and then "change into" another role determined by the JWT verification.

For "authenticated access." This is the role which the API (PostgREST) will use when a user is logged in.

For elevated access. This role is used by the API (PostgREST) to bypass Row Level Security.

Used by the Auth middleware to connect to the database and run migration. Access is scoped to the auth schema.

Used by the Auth middleware to connect to the database and run migration. Access is scoped to the storage schema.

Used by Replication powered by Supabase ETL to replicate database changes to external destinations. Has read-all access and replication privileges for change data capture, bypasses Row Level Security, and can write to the etl schema.

For running commands via the Supabase UI.

An internal role Supabase uses for administrative tasks, such as running upgrades and automations.

**Examples:**

Example 1 (unknown):
```unknown
1create role "role_name";
```

Example 2 (unknown):
```unknown
1create role "role_name" with login password 'extremely_secure_password';
```

Example 3 (unknown):
```unknown
1REVOKE permission_type ON object_name FROM role_name;
```

Example 4 (unknown):
```unknown
1create role "child_role_name" inherit "parent_role_name";
```

---

## Automated backups using GitHub Actions | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/ci/backups

**Contents:**
- Automated backups using GitHub Actions
- Backup your database on a regular basis.
- Backup action#
- Periodic Backups Workflow#
- More resources#

Automated backups using GitHub Actions

Backup your database on a regular basis.

You can use the Supabase CLI to backup your Postgres database. The steps involve running a series of commands to dump roles, schema, and data separately. Inside your repository, create a new file inside the .github/workflows folder called backup.yml. Copy the following snippet inside the file, and the action will run whenever a new PR is created.

Never backup your data to a public repository.

You can use the GitHub Action to run periodic backups of your database. In this example, the Action workflow is triggered by push and pull_request events on the main branch, manually via workflow_dispatch, and automatically at midnight every day due to the schedule event with a cron expression. The workflow runs on the latest Ubuntu runner and requires write permissions to the repository's contents. It uses the Supabase CLI to dump the roles, schema, and data from your Supabase database, utilizing the SUPABASE_DB_URL environment variable that is securely stored in the GitHub secrets. After the backup is complete, it auto-commits the changes to the repository using the git-auto-commit-action. This ensures that the latest backup is always available in your repository. The commit message for these automated commits is "Supabase backup". This workflow provides an automated solution for maintaining regular backups of your Supabase database. It helps keep your data safe and enables easy restoration in case of any accidental data loss or corruption.

Never backup your data to a public repository.

**Examples:**

Example 1 (unknown):
```unknown
1name: 'backup-database'2on:3  pull_request:4jobs:5  build: 6    runs-on: ubuntu-latest7    env:8      supabase_db_url: ${{ secrets.SUPABASE_DB_URL }}   # For example: postgresql://postgres:[YOUR-PASSWORD]@db.<ref>.supabase.co:5432/postgres9    steps:10      - uses: actions/checkout@v211      - uses: supabase/setup-cli@v112        with:13          version: latest14      - name: Backup roles15        run: supabase db dump --db-url "$supabase_db_url" -f roles.sql --role-only16      - name: Backup schema17        run: supabase db dump --db-url "$supabase_db_url" -f schema.sql18      - name: Backup data19        run: supabase db dump --db-url "$supabase_db_url" -f data.sql --data-only --use-copy
```

Example 2 (unknown):
```unknown
1name: Supa-backup23on:4  push:5    branches: [ main ]6  pull_request:7    branches: [ main ]8  workflow_dispatch:9  schedule:10    - cron: '0 0 * * *' # Runs every day at midnight11jobs:   12  run_db_backup:13    runs-on: ubuntu-latest14    permissions:15      contents: write16    env:17      supabase_db_url: ${{ secrets.SUPABASE_DB_URL }}   # For example: postgresql://postgres:[YOUR-PASSWORD]@db.<ref>.supabase.co:5432/postgres18    steps:19      - uses: actions/checkout@v320        with:21          ref: ${{ github.head_ref }}22      - uses: supabase/setup-cli@v123        with:24          version: latest25      - name: Backup roles26        run: supabase db dump --db-url "$supabase_db_url" -f roles.sql --role-only27      - name: Backup schema28        run: supabase db dump --db-url "$supabase_db_url" -f schema.sql29      - name: Backup data30        run: supabase db dump --db-url "$supabase_db_url" -f data.sql --data-only --use-copy3132      - uses: stefanzweifel/git-auto-commit-action@v433        with:34          commit_message: Supabase backup
```

---

## PGroonga: Multilingual Full Text Search | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgroonga

**Contents:**
- PGroonga: Multilingual Full Text Search
- Enable the extension#
- Creating a full text search index#
- Full text search#
  - Match all search words#
  - Match any search words#
  - Search that matches words with negation#
- Resources#

PGroonga: Multilingual Full Text Search

PGroonga is a Postgres extension adding a full text search indexing method based on Groonga. While native Postgres supports full text indexing, it is limited to alphabet and digit based languages. PGroonga offers a wider range of character support making it viable for a superset of languages supported by Postgres including Japanese, Chinese, etc.

Given a table with a text column:

We can index the column for full text search with a pgroonga index:

To test the full text index, we'll add some data.

The Postgres query planner is smart enough to know that, for extremely small tables, it's faster to scan the whole table rather than loading an index. To force the index to be used, we can disable sequential scans:

Now if we run an explain plan on a query filtering on memos.content:

The pgroonga index is used to retrieve the result set:

The &@~ operator performs full text search. It returns any matching results. Unlike LIKE operator, pgroonga can search any text that contains the keyword case insensitive.

Take the following example:

To find all memos where content contains BOTH of the words postgres and pgroonga, we can just use space to separate each words:

To find all memos where content contain ANY of the words postgres or pgroonga, use the upper case OR:

To find all memos where content contain the word postgres but not pgroonga, use - symbol:

**Examples:**

Example 1 (unknown):
```unknown
1create table memos (2  id serial primary key,3  content text4);
```

Example 2 (unknown):
```unknown
1create index ix_memos_content ON memos USING pgroonga(content);
```

Example 3 (unknown):
```unknown
1insert into memos(content)2values3  ('PostgreSQL is a relational database management system.'),4  ('Groonga is a fast full text search engine that supports all languages.'),5  ('PGroonga is a PostgreSQL extension that uses Groonga as index.'),6  ('There is groonga command.');
```

Example 4 (unknown):
```unknown
1-- For testing only. Don't do this in production2set enable_seqscan = off;
```

---

## Supabase Queues | Supabase Docs

**URL:** https://supabase.com/docs/guides/queues

**Contents:**
- Supabase Queues
- Durable Message Queues with Guaranteed Delivery in Postgres
- Features#
- Resources#

Durable Message Queues with Guaranteed Delivery in Postgres

Supabase Queues is a Postgres-native durable Message Queue system with guaranteed delivery built on the pgmq database extension. It offers developers a seamless way to persist and process Messages in the background while improving the resiliency and scalability of their applications and services.

Queues couples the reliability of Postgres with the simplicity Supabase's platform and developer experience, enabling developers to manage Background Tasks with zero configuration.

---

## Security | Supabase Docs

**URL:** https://supabase.com/docs/guides/graphql/security

**Contents:**
- Security
- Securing your GraphQL API.
- Table/Column Visibility#
- Row Visibility#

Securing your GraphQL API.

pg_graphql fully respects builtin PostgreSQL role and row security.

Table and column visibility in the GraphQL schema are controlled by standard PostgreSQL role permissions. Revoking SELECT access from the user/role executing queries removes that entity from the visible schema.

removes the Account GraphQL type.

Similarly, revoking SELECT access on a table's column will remove that field from the associated GraphQL type/s.

The permissions SELECT, INSERT, UPDATE, and DELETE all impact the relevant sections of the GraphQL schema.

Visibility of rows in a given table can be configured using PostgreSQL's built-in row level security policies.

**Examples:**

Example 1 (unknown):
```unknown
1revoke all privileges on public."Account" from api_user;
```

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting?tags=postgres

---

## Resources | Supabase Docs

**URL:** https://supabase.com/docs/guides/resources

**Contents:**
- Resources
  - Migrate to Supabase#
      - Auth0
      - Firebase Auth
      - Firestore Data
      - Firebase Storage
      - Heroku
      - Render
      - Amazon RDS
      - Postgres

Drop all tables in schema

Select first row per group

Print PostgreSQL version

---

## Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/graphql/functions

**Contents:**
- Functions
- Using Postgres Functions with GraphQL.
- Query vs Mutation#
- Supported Return Types#
- Default Arguments#
- Limitations#

Using Postgres Functions with GraphQL.

Functions can be exposed by pg_graphql to allow running custom queries or mutations.

For example, a function to add two numbers will be available on the query type as a field:

Functions marked immutable or stable are available on the query type. Functions marked with the default volatile category are available on the mutation type:

Built-in GraphQL scalar types Int, Float, String, Boolean and custom scalar types are supported as function arguments and return types. Function types returning a table or view are supported as well. Such functions implement the Node interface:

Since Postgres considers a row/composite type containing only null values to be null, the result can be a little surprising in this case. Instead of an object with all columns null, the top-level field is null:

Functions returning multiple rows of a table or view are exposed as collections.

A set returning function with any of its argument names clashing with argument names of a collection (first, last, before, after, filter, or orderBy) will not be exposed.

Functions accepting or returning arrays of non-composite types are also supported. In the following example, the ids array is used to filter rows from the Account table:

Arguments without a default value are required in the GraphQL schema, to make them optional they should have a default value.

If there is no sensible default, and you still want to make the argument optional, consider using the default value null.

Currently, null defaults are only supported as simple expressions, as shown in the previous example.

The following features are not yet supported. Any function using these features is not exposed in the API:

**Examples:**

Example 1 (unknown):
```unknown
1create function "addNums"(a int, b int)2  returns int3  immutable4  language sql5as $$ select a + b; $$;
```

Example 2 (unknown):
```unknown
1create table account(2  id serial primary key,3  email varchar(255) not null4);56create function "addAccount"(email text)7  returns int8  volatile9  language sql10as $$ insert into account (email) values (email) returning id; $$;
```

Example 3 (unknown):
```unknown
1create table account(2  id serial primary key,3  email varchar(255) not null4);56insert into account(email)7values8  ('a@example.com'),9  ('b@example.com');1011create function "accountById"("accountId" int)12  returns account13  stable14  language sql15as $$ select id, email from account where id = "accountId"; $$;
```

Example 4 (unknown):
```unknown
1create table account(2    id int,3    email varchar(255),4    name text null5);67insert into account(id, email, name)8values9    (1, 'aardvark@x.com', 'aardvark'),10    (2, 'bat@x.com', null),11    (null, null, null);1213create function "returnsAccountWithAllNullColumns"()14    returns account language sql stable15as $$ select id, email, name from account where id is null; $$;
```

---

## Notion | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/notion

**Contents:**
- Notion
- Available Versions#
- Preparation#
  - Enable Wrappers#
  - Enable the Notion Wrapper#
  - Store your credentials (optional)#
  - Connecting to Notion#
  - Create a schema#
- Options#
- Entities#

You can enable the Notion wrapper right from the Supabase dashboard.

Notion provides a versatile, ready-to-use solution for managing your data.

The Notion Wrapper is a WebAssembly(Wasm) foreign data wrapper which allows you to read data from your Notion workspace for use within your Postgres database.

Before you can query Notion, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the Wasm foreign data wrapper:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

⚠️ ** Getting a Notion API key**

We need to provide Postgres with the credentials to access Notion and any additional options. We can do this using the create server command:

Note the fdw_package_* options are required, which specify the Wasm package metadata. You can get the available package version list from above.

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

Supported objects are listed below:

We can use SQL import foreign schema to import foreign table definitions from Notion.

For example, using below SQL can automatically create foreign tables in the notion schema.

This is an object representing Notion Block content.

This is an object representing Notion Pages.

This is an object representing Notion Databases.

This is an object representing Notion Users.

This FDW supports where clause pushdown with id as the filter. For example,

will be translated to a Notion API call: https://api.notion.com/v1/pages/5a67c86f-d0da-4d0a-9dd7-f4cf164e6247.

In addition to id column pushdown, page_id column pushdown is also supported for Block object. For example,

will recursively fetch all children blocks of the Page with id '5a67c86f-d0da-4d0a-9dd7-f4cf164e6247'. This can dramatically reduce number of API calls and improve query performance.

Below query will request ALL the blocks of ALL pages recursively, it may take very long time to run if there are many pages in Notion. So it is recommended to always query Block object with an id or page_id filter like above.

The Notion API uses JSON formatted data, please refer to Notion API docs for more details.

This section describes important limitations and considerations when using this FDW:

This example will create a "foreign table" inside your Postgres database and query its data.

attrs is a special column which stores all the object attributes in JSON format, you can extract any attributes needed from it. See more examples below.

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper wasm_wrapper2  handler wasm_fdw_handler3  validator wasm_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Notion API key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<Notion API key>', -- Notion API key, should look like ntn_589513........4  'notion',5  'Notion API key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server notion_server2  foreign data wrapper wasm_wrapper3  options (4    fdw_package_url 'https://github.com/supabase/wrappers/releases/download/wasm_notion_fdw_v0.1.1/notion_fdw.wasm',5    fdw_package_name 'supabase:notion-fdw',6    fdw_package_version '0.1.1',7    fdw_package_checksum '6dea3014f462aafd0c051c37d163fe326e7650c26a7eb5d8017a30634b5a46de',8    api_url 'https://api.notion.com/v1',  -- optional9    api_key_id '<vault key_ID>' -- the Vault key id from the previous step, not the Notion API key itself10  );
```

---

## Getting Started with Realtime | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/getting_started

**Contents:**
- Getting Started with Realtime
- Learn how to build real-time applications with Supabase Realtime
- Quick start#
  - 1. Install the client library#
  - 2. Initialize the client#
  - Get API details#
      - Changes to API keys
  - 3. Create your first Channel#
  - 4. Set up authorization#
  - 5. Send and receive messages#

Getting Started with Realtime

Learn how to build real-time applications with Supabase Realtime

Get your project URL and key.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Channels are the foundation of Realtime. Think of them as rooms where clients can communicate. Each channel is identified by a topic name and if they are public or private.

Since we're using a private channel, you need to create a basic RLS policy on the realtime.messages table to allow authenticated users to connect. Row Level Security (RLS) policies control who can access your Realtime channels based on user authentication and custom rules:

There are three main ways to send messages with Realtime:

Send and receive messages using the Supabase client:

Send messages via HTTP requests, perfect for server-side applications:

Automatically broadcast database changes using triggers. Choose the approach that best fits your needs:

Using realtime.broadcast_changes (Best for mirroring database changes)

Using realtime.send (Best for custom notifications and filtered data)

Always use private channels for production applications to ensure proper security and authorization:

Channel Topics: Use the pattern scope:id:entity

Always unsubscribe when you are done with a channel to ensure you free up resources:

Now that you understand the basics, dive deeper into each feature:

Ready to build something amazing? Start with the Broadcast guide to create your first real-time feature!

**Examples:**

Example 1 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 2 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabase = createClient('https://<project>.supabase.co', '<anon_key or sb_publishable_key>')
```

Example 3 (javascript):
```javascript
1// Create a channel with a descriptive topic name2const channel = supabase.channel('room:lobby:messages', {3  config: { private: true }, // Recommended for production4})
```

Example 4 (unknown):
```unknown
1-- Allow authenticated users to receive broadcasts2CREATE POLICY "authenticated_users_can_receive" ON realtime.messages3  FOR SELECT TO authenticated USING (true);45-- Allow authenticated users to send broadcasts6CREATE POLICY "authenticated_users_can_send" ON realtime.messages7  FOR INSERT TO authenticated WITH CHECK (true);
```

---

## ClickHouse | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/clickhouse

**Contents:**
- ClickHouse
- Preparation#
  - Enable Wrappers#
  - Enable the ClickHouse Wrapper#
  - Store your credentials (optional)#
  - Connecting to ClickHouse#
  - Create a schema#
- Options#
  - Parametrized views#
- Entities#

You can enable the ClickHouse wrapper right from the Supabase dashboard.

ClickHouse is a fast open-source column-oriented database management system that allows generating analytical data reports in real-time using SQL queries.

The ClickHouse Wrapper allows you to read and write data from ClickHouse within your Postgres database.

Before you can query ClickHouse, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the clickhouse_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to ClickHouse, and any additional options. We can do this using the create server command:

Some connection string examples:

Check out more connection string parameters.

This ClickHouse FDW only supports native protocol port 9000 and 9440, HTTP(S) port like 8123 and 8443 are not supported yet.

We recommend creating a schema to hold all the foreign tables:

The following options are available when creating ClickHouse foreign tables:

This can also be a subquery enclosed in parentheses, for example,

Parametrized view is also supported in the subquery. In this case, you need to define a column for each parameter and use where to pass values to them. For example,

The ClickHouse Wrapper supports data reads and writes from ClickHouse tables.

This FDW supports where, order by and limit clause pushdown, as well as parametrized view (see above).

This section describes important limitations and considerations when using this FDW:

This example demonstrates basic ClickHouse table operations.

Create foreign table on Postgres database:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper clickhouse_wrapper2  handler click_house_fdw_handler3  validator click_house_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your ClickHouse credential in Vault and retrieve the created `key_id`2select vault.create_secret(3  'tcp://default:@localhost:9000/default',4  'clickhouse',5  'ClickHouse credential for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server clickhouse_server2  foreign data wrapper clickhouse_wrapper3  options (4    conn_string_id '<key_ID>' -- The Key ID from above.5  );
```

---

## Performance Tuning | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/performance

**Contents:**
- Performance Tuning
- Examining query performance#
- Optimizing the number of connections#
  - Configuring clients to use fewer connections#
  - Allowing higher number of connections#
  - Enterprise#

The Supabase platform automatically optimizes your Postgres database to take advantage of the compute resources of the plan your project is on. However, these optimizations are based on assumptions about the type of workflow the project is being utilized for, and it is likely that better results can be obtained by tuning the database for your particular workflow.

Unoptimized queries are a major cause of poor database performance. To analyze the performance of your queries, see the Debugging and monitoring guide.

The default connection limits for Postgres and Supavisor is based on your compute size. See the default connection numbers in the Compute Add-ons section.

If the number of connections is insufficient, you will receive the following error upon connecting to the DB:

In such a scenario, you can consider:

You can use the pg_stat_activity view to debug which clients are holding open connections on your DB. pg_stat_activity only exposes information on direct connections to the database. Information on the number of connections to Supavisor is available via the metrics endpoint.

Depending on the clients involved, you might be able to configure them to work with fewer connections (e.g. by imposing a limit on the maximum number of connections they're allowed to use), or shift specific workloads to connect via Supavisor instead. Transient workflows, which can quickly scale up and down in response to traffic (e.g. serverless functions), can especially benefit from using a connection pooler rather than connecting to the DB directly.

You can configure Postgres connection limit among other parameters by using Custom Postgres Config.

Contact us if you need help tuning your database for your specific workflow.

**Examples:**

Example 1 (unknown):
```unknown
1$ psql -U postgres -h ...2FATAL: remaining connection slots are reserved for non-replication superuser connections
```

---

## Seeding your database | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development/seeding-your-database

**Contents:**
- Seeding your database
- Populate your database with initial data for reproducible environments across local and testing.
- What is seed data?#
- Using seed files#
  - Splitting up your seed file#
- Generating seed data#

Seeding your database

Populate your database with initial data for reproducible environments across local and testing.

Seeding is the process of populating a database with initial data, typically used to provide sample or default records for testing and development purposes. You can use this to create "reproducible environments" for local development, staging, and production.

Seed files are executed the first time you run supabase start and every time you run supabase db reset. Seeding occurs after all database migrations have been completed. As a best practice, only include data insertions in your seed files, and avoid adding schema statements.

By default, if no specific configuration is provided, the system will look for a seed file matching the pattern supabase/seed.sql. This maintains backward compatibility with earlier versions, where the seed file was placed in the supabase folder.

You can add any SQL statements to this file. For example:

If you want to manage multiple seed files or organize them across different folders, you can configure additional paths or glob patterns in your config.toml (see the next section for details).

For better modularity and maintainability, you can split your seed data into multiple files. For example, you can organize your seeds by table and include files such as countries.sql and cities.sql. Configure them in config.toml like so:

Or to include all .sql files under a specific folder you can do:

The CLI processes seed files in the order they are declared in the sql_paths array. If a glob pattern is used and matches multiple files, those files are sorted in lexicographic order to ensure consistent execution. Additionally:

You can generate seed data for local development using Snaplet.

To use Snaplet, you need to have Node.js and npm installed. You can add Node.js to your project by running npm init -y in your project directory.

If this is your first time using Snaplet to seed your project, you'll need to set up Snaplet with the following command:

This command will analyze your database and its structure, and then generate a JavaScript client which can be used to define exactly how your data should be generated using code. The init command generates a configuration file, seed.config.ts and an example script, seed.ts, as a starting point.

During init if you are not using an Object Relational Mapper (ORM) or your ORM is not in the supported list, choose node-postgres.

In most cases you only want to generate data for specific schemas or tables. This is defined with select. Here is an example seed.config.ts configuration file:

Suppose you have a database with the following schema:

You can use the seed script example generated by Snaplet seed.ts to define the values you want to generate. For example:

Running npx tsx seed.ts > supabase/seed.sql generates the relevant SQL statements inside your supabase/seed.sql file:

Whenever your database structure changes, you will need to regenerate @snaplet/seed to keep it in sync with the new structure. You can do this by running:

You can further enhance your seed script by using Large Language Models to generate more realistic data. To enable this feature, set one of the following environment variables in your .env file:

After setting the environment variables, run the following commands to sync and generate the seed data:

For more information, check out Snaplet's seed documentation

**Examples:**

Example 1 (unknown):
```unknown
1insert into countries2  (name, code)3values4  ('United States', 'US'),5  ('Canada', 'CA'),6  ('Mexico', 'MX');
```

Example 2 (unknown):
```unknown
1[db.seed]2enabled = true3sql_paths = ['./countries.sql', './cities.sql']
```

Example 3 (unknown):
```unknown
1[db.seed]2enabled = true3sql_paths = ['./seeds/*.sql']
```

Example 4 (unknown):
```unknown
1npx @snaplet/seed init
```

---

## Stripe | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/stripe

**Contents:**
- Stripe
- Preparation#
  - Enable Wrappers#
  - Enable the Stripe Wrapper#
  - Store your credentials (optional)#
  - Connecting to Stripe#
  - Create a schema#
- Entities#
  - Accounts#
    - Operations#

You can enable the Stripe wrapper right from the Supabase dashboard.

Stripe is an API driven online payment processing utility.

The Stripe Wrapper allows you to read data from Stripe within your Postgres database.

Before you can query Stripe, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the stripe_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to Stripe, and any additional options. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The Stripe Wrapper supports data read and modify from Stripe API.

We can use SQL import foreign schema to import foreign table definitions from Stripe.

For example, using below SQL can automatically create foreign tables in the stripe schema.

The full list of the foreign tables is below:

This is an object representing a Stripe account.

This is an object representing your Stripe account's current balance.

This is an object representing funds moving through your Stripe account. Balance transactions are created for every type of transaction that comes into or flows out of your Stripe account balance.

This is an object representing a charge on a credit or debit card. You can retrieve and refund individual charges as well as list all charges. Charges are identified by a unique, random ID.

This is an object representing your customer's session as they pay for one-time purchases or subscriptions through Checkout or Payment Links. We recommend creating a new Session each time your customer attempts to pay.

This is an object representing your Stripe customers. You can create, retrieve, update, and delete customers.

This is an object representing a dispute that occurs when a customer questions your charge with their card issuer.

This is an object representing events that occur in your Stripe account, letting you know when something interesting happens.

This is an object representing a file hosted on Stripe's servers.

This is an object representing a link that can be used to share the contents of a File object with non-Stripe users.

This is an object representing statements of amounts owed by a customer, which are either generated one-off or periodically from a subscription.

This is an object representing a record of the permission a customer has given you to debit their payment method.

This is an object representing a billing meter that allows you to track usage of a particular event.

This is an object representing a guide through the process of collecting a payment from your customer.

This is an object representing funds received from Stripe or initiated payouts to a bank account or debit card of a connected Stripe account.

This is an object representing pricing configurations for products to facilitate multiple currencies and pricing options.

This is an object representing all products available in Stripe.

This is an object representing refunds for charges that have previously been created but not yet refunded.

This is an object representing attempted confirmations of SetupIntents, tracking both successful and unsuccessful attempts.

This is an object representing a guide through the process of setting up and saving customer payment credentials for future payments.

This is an object representing customer recurring payment schedules.

This is an object representing a secure way to collect sensitive card, bank account, or personally identifiable information (PII) from customers.

This is an object representing a way to add funds to your Stripe balance.

This is an object representing fund movements between Stripe accounts as part of Connect.

This FDW supports where clause pushdown. You can specify a filter in where clause and it will be passed to Stripe API call.

For example, this query

will be translated to a Stripe API call: https://api.stripe.com/v1/customers/cus_xxx.

For supported filter columns for each object, please check out foreign table documents above.

This section describes important limitations and considerations when using this FDW:

Some examples on how to use Stripe foreign tables.

To insert into an object with sub-fields, we need to create the foreign table with column name exactly same as the API required. For example, to insert a subscription object we can define the foreign table following the Stripe API docs:

And then we can insert a subscription like below:

Note this foreign table is only for data insertion, it cannot be used in select statement.

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper stripe_wrapper2  handler stripe_fdw_handler3  validator stripe_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Stripe API key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<Stripe API key>',4  'stripe',5  'Stripe API key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server stripe_server2  foreign data wrapper stripe_wrapper3  options (4    api_key_id '<key_ID>', -- The Key ID from above, required if api_key_name is not specified.5    api_key_name '<key_Name>', -- The Key Name from above, required if api_key_id is not specified.6    api_url 'https://api.stripe.com/v1/',  -- Stripe API base URL, optional. Default is 'https://api.stripe.com/v1/'7    api_version '2024-06-20'  -- Stripe API version, optional. Default is your Stripe account’s default API version.8  );
```

---

## Postgres SSL Enforcement | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/ssl-enforcement

**Contents:**
- Postgres SSL Enforcement
- Manage SSL enforcement via the dashboard#
- Manage SSL enforcement via the Management API#
- Manage SSL enforcement via the CLI#
  - Check enforcement status#
  - Update enforcement#
  - A note about Postgres SSL modes#

Postgres SSL Enforcement

Your Supabase project supports connecting to the Postgres DB without SSL enabled to maximize client compatibility. For increased security, you can prevent clients from connecting if they're not using SSL.

Disabling SSL enforcement only applies to connections to Postgres and Supavisor ("Connection Pooler"); all HTTP APIs offered by Supabase (e.g., PostgREST, Storage, Auth) automatically enforce SSL on all incoming connections.

Projects need to be at least on Postgres 13.3.0 to enable SSL enforcement. You can find the Postgres version of your project in the Infrastructure Settings page. If your project is on an older version, you will need to upgrade to use this feature.

SSL enforcement can be configured via the "Enforce SSL on incoming connections" setting under the SSL Configuration section in Database Settings page of the dashboard.

You can also manage SSL enforcement using the Management API:

You can use the get subcommand of the CLI to check whether SSL is currently being enforced:

Response if SSL is being enforced:

Response if SSL is not being enforced:

The update subcommand is used to change the SSL enforcement status for your project:

Similarly, to disable SSL enforcement:

Postgres supports multiple SSL modes on the client side. These modes provide different levels of protection. Depending on your needs, it is important to verify that the SSL mode in use is performing the required level of enforcement and verification of SSL connections.

The strongest mode offered by Postgres is verify-full and this is the mode you most likely want to use when SSL enforcement is enabled. To use verify-full you will need to download the Supabase CA certificate for your database. The certificate is available through the dashboard under the SSL Configuration section in the Database Settings page.

Once the CA certificate has been downloaded, add it to the certificate authority list used by Postgres.

With the CA certificate added to the trusted certificate authorities list, use psql or your client library to connect to Supabase:

**Examples:**

Example 1 (unknown):
```unknown
1# Get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"3export PROJECT_REF="your-project-ref"45# Get current SSL enforcement status6curl -X GET "https://api.supabase.com/v1/projects/$PROJECT_REF/ssl-enforcement" \7  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN"89# Enable SSL enforcement10curl -X PUT "https://api.supabase.com/v1/projects/$PROJECT_REF/ssl-enforcement" \11  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \12  -H "Content-Type: application/json" \13  -d '{14    "requestedConfig": {15      "database": true16    }17  }'1819# Disable SSL enforcement20curl -X PUT "https://api.supabase.com/v1/projects/$PROJECT_REF/ssl-enforcement" \21  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \22  -H "Content-Type: application/json" \23  -d '{24    "requestedConfig": {25      "database": false26    }27  }'
```

Example 2 (unknown):
```unknown
1supabase ssl-enforcement --project-ref {ref} get --experimental
```

Example 3 (unknown):
```unknown
1SSL is being enforced.
```

Example 4 (unknown):
```unknown
1SSL is *NOT* being enforced.
```

---

## Listening to Postgres Changes with Flutter | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/realtime-listening-flutter

**Contents:**
- Listening to Postgres Changes with Flutter

Listening to Postgres Changes with Flutter

The Postgres Changes extension listens for database changes and sends them to clients which enables you to receive database changes in real-time.

---

## Migrate from Firebase Firestore to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/firestore-data

**Contents:**
- Migrate from Firebase Firestore to Supabase
- Migrate your Firebase Firestore database to a Supabase Postgres database.
- Set up the migration tool #
- Generate a Firebase private key #
- Command line options#
  - List all Firestore collections#
  - Dump Firestore collection to JSON file#
    - Customize the JSON file with hooks#
  - Import JSON file to Supabase (Postgres) #
- Custom hooks#

Migrate from Firebase Firestore to Supabase

Migrate your Firebase Firestore database to a Supabase Postgres database.

Supabase provides several tools to convert data from a Firebase Firestore database to a Supabase Postgres database. The process copies the entire contents of a single Firestore collection to a single Postgres table.

The Firestore collection is "flattened" and converted to a table with basic columns of one of the following types: text, numeric, boolean, or jsonb. If your structure is more complex, you can write a program to split the newly-created json file into multiple, related tables before you import your json file(s) to Supabase.

Clone the firebase-to-supabase repository:

In the /firestore directory, create a file named supabase-service.json with the following contents:

On your project dashboard, click Connect

Under the Session pooler, click on the View parameters under the connect string. Replace the Host and User fields with the values shown.

Enter the password you used when you created your Supabase project in the password entry in the supabase-service.json file.

node firestore2json.js <collectionName> [<batchSize>] [<limit>]

You can customize the way your JSON file is written using a custom hook. A common use for this is to "flatten" the JSON file, or to split nested data into separate, related database tables. For example, you could take a Firestore document that looks like this:

And split it into two files (one table for users and one table for items):

node json2supabase.js <path_to_json_file> [<primary_key_strategy>] [<primary_key_name>]

Hooks are used to customize the process of exporting a collection of Firestore documents to JSON. They can be used for:

If your Firestore collection is called users, create a file called users.js in the current folder.

The basic format of a hook file looks like this:

Flatten the users collection into separate files:

The users.js hook file:

The result is two separate JSON files:

Contact us if you need more help migrating your project.

**Examples:**

Example 1 (unknown):
```unknown
1git clone https://github.com/supabase-community/firebase-to-supabase.git
```

Example 2 (unknown):
```unknown
1{2  "host": "database.server.com",3  "password": "secretpassword",4  "user": "postgres",5  "database": "postgres",6  "port": 54327}
```

Example 3 (unknown):
```unknown
1[{ "user": "mark", "score": 100, "items": ["hammer", "nail", "glue"] }]
```

Example 4 (unknown):
```unknown
1[{ "user": "mark", "score": 100 }]
```

---

## pg_net: Async Networking | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_net

**Contents:**
- pg_net: Async Networking
- Enable the extension#
- http_get#
  - Signature #
  - Usage #
- http_post#
  - Signature #
  - Usage #
- http_delete#
  - Signature #

pg_net: Async Networking

The pg_net API is in beta. Functions signatures may change.

pg_net enables Postgres to make asynchronous HTTP/HTTPS requests in SQL. It differs from the http extension in that it is asynchronous by default. This makes it useful in blocking functions (like triggers).

It eliminates the need for servers to continuously poll for database changes and instead allows the database to proactively notify external resources about significant events.

Creates an HTTP GET request returning the request's ID. HTTP requests are not started until the transaction is committed.

This is a Postgres SECURITY DEFINER function.

Creates an HTTP POST request with a JSON body, returning the request's ID. HTTP requests are not started until the transaction is committed.

The body's character set encoding matches the database's server_encoding setting.

This is a Postgres SECURITY DEFINER function

Creates an HTTP DELETE request, returning the request's ID. HTTP requests are not started until the transaction is committed.

This is a Postgres SECURITY DEFINER function

Waiting requests are stored in the net.http_request_queue table. Upon execution, they are deleted.

Once a response is returned, by default, it is stored for 6 hours in the net._http_response table.

The responses can be observed with the following query:

The data can also be observed in the net schema with the Supabase Dashboard's SQL Editor

The Postman Echo API returns a response with the same body and content as the request. It can be used to inspect the data being sent.

Sending a post request to the echo API

Inspecting the echo API response content to ensure it contains the right body

Alternatively, by wrapping a request in a database function, sent row data can be logged or returned for inspection and debugging.

Finds all failed requests

Supabase supports reconfiguring pg*net starting from v0.12.0+. For the latest release, initiate a Postgres upgrade in the Infrastructure Settings.

The extension is configured to reliably execute up to 200 requests per second. The response messages are stored for only 6 hours to prevent needless buildup. The default behavior can be modified by rewriting config variables.

Then reload the settings and restart the pg_net background worker with:

Make a POST request to a Supabase Edge Function with auth header and JSON body payload:

The pg_cron extension enables Postgres to become its own cron server. With it you can schedule regular calls with up to a minute precision to endpoints.

Make a call to an external endpoint when a trigger event occurs.

More examples can be seen on the Extension's GitHub page

**Examples:**

Example 1 (unknown):
```unknown
1net.http_get(2    -- url for the request3    url text,4    -- key/value pairs to be url encoded and appended to the `url`5    params jsonb default '{}'::jsonb,6    -- key/values to be included in request headers7    headers jsonb default '{}'::jsonb,8    -- the maximum number of milliseconds the request may take before being canceled9    timeout_milliseconds int default 200010)11    -- request_id reference12    returns bigint1314    strict15    volatile16    parallel safe17    language plpgsql
```

Example 2 (unknown):
```unknown
1select2    net.http_get('https://news.ycombinator.com')3    as request_id;4request_id5----------6         17(1 row)
```

Example 3 (unknown):
```unknown
1net.http_post(2    -- url for the request3    url text,4    -- body of the POST request5    body jsonb default '{}'::jsonb,6    -- key/value pairs to be url encoded and appended to the `url`7    params jsonb default '{}'::jsonb,8    -- key/values to be included in request headers9    headers jsonb default '{"Content-Type": "application/json"}'::jsonb,10    -- the maximum number of milliseconds the request may take before being canceled11    timeout_milliseconds int default 200012)13    -- request_id reference14    returns bigint1516    volatile17    parallel safe18    language plpgsql
```

Example 4 (unknown):
```unknown
1select2    net.http_post(3        url:='https://httpbin.org/post',4        body:='{"hello": "world"}'::jsonb5    ) as request_id;6request_id7----------8         19(1 row)
```

---

## Debugging and monitoring | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/inspect

**Contents:**
- Debugging and monitoring
- Using the CLI#
  - The inspect db command#
  - Connect to any Postgres database#
  - Connect to a Supabase instance#
  - Inspection commands#
    - Disk storage#
    - Query performance#
    - Locks#
    - Connections#

Debugging and monitoring

Database performance is a large topic and many factors can contribute. Some of the most common causes of poor performance include:

You can examine your database and queries for these issues using either the Supabase CLI or SQL.

The Supabase CLI comes with a range of tools to help inspect your Postgres instances for potential issues. The CLI gets the information from Postgres internals. Therefore, most tools provided are compatible with any Postgres databases regardless if they are a Supabase project or not.

You can find installation instructions for the Supabase CLI here.

The inspection tools for your Postgres database are under the inspect db command. You can get a full list of available commands by running supabase inspect db help.

Most inspection commands are Postgres agnostic. You can run inspection routines on any Postgres database even if it is not a Supabase project by providing a connection string via --db-url.

For example you can connect to your local Postgres instance:

Working with Supabase, you can link the Supabase CLI with your project:

Then the CLI will automatically connect to your Supabase project whenever you are in the project folder and you no longer need to provide —db-url.

Below are the db inspection commands provided, grouped by different use cases.

Some commands might require pg_stat_statements to be enabled or a specific Postgres version to be used.

These commands are handy if you are running low on disk storage:

The commands below are useful if your Postgres database consumes a lot of resources like CPU, RAM or Disk IO. You can also use them to investigate slow queries.

Following commands require pg_stat_statements to be enabled: calls, locks, cache-hit, blocking, unused-indexes, index-usage, bloat, outliers, table-record-counts, replication-slots, seq-scans, vacuum-stats, long-running-queries.

When using pg_stat_statements also take note that it only stores the latest 5,000 statements. Moreover, consider resetting the analysis after optimizing any queries by running select pg_stat_statements_reset();

Learn more about pg_stats here.

If you're seeing an insufficient privilege error when viewing the Query Performance page from the dashboard, run this command:

Postgres collects data about its own operations using the cumulative statistics system. In addition to this, every Supabase project has the pg_stat_statements extension enabled by default. This extension records query execution performance details and is the best way to find inefficient queries. This information can be combined with the Postgres query plan analyzer to develop more efficient queries.

Here are some example queries to get you started.

This provides useful information about the queries you run most frequently. Queries that have high max_time or mean_time times and are being called often can be good candidates for optimization.

This query will show you statistics about queries ordered by the maximum execution time. It is similar to the query above ordered by calls, but this one highlights outliers that may have high executions times. Queries which have high or mean execution times are good candidates for optimization.

This query will show you statistics about queries ordered by the cumulative total execution time. It shows the total time the query has spent running as well as the proportion of total execution time the query has taken up.

Queries which are the most time consuming are not necessarily bad, you may have a very efficient and frequently ran queries that end up taking a large total % time, but it can be useful to help spot queries that are taking up more time than they should.

Generally for most applications a small percentage of data is accessed more regularly than the rest. To make sure that your regularly accessed data is available, Postgres tracks your data access patterns and keeps this in its shared_buffers cache.

Applications with lower cache hit rates generally perform more poorly since they have to hit the disk to get results rather than serving them from memory. Very poor hit rates can also cause you to burst past your Disk IO limits causing significant performance issues.

You can view your cache and index hit rate by executing the following query:

This shows the ratio of data blocks fetched from the Postgres shared_buffers cache against the data blocks that were read from disk/OS cache.

If either of your index or table hit rate are < 99% then this can indicate your compute plan is too small for your current workload and you would benefit from more memory. Upgrading your compute is easy and can be done from your project dashboard.

Postgres has built in tooling to help you optimize poorly performing queries. You can use the query plan analyzer on any expensive queries that you have identified:

When you include analyze in the explain statement, the database attempts to execute the query and provides a detailed query plan along with actual execution times. So, be careful using explain analyze with insert/update/delete queries, because the query will actually run, and could have unintended side-effects.

If you run just explain without the analyze keyword, the database will only perform query planning without actually executing the query. This approach can be beneficial when you want to inspect the query plan without affecting the database or if you encounter timeouts in your queries.

Using the query plan analyzer to optimize your queries is a large topic, with a number of online resources available:

You can pair the information available from pg_stat_statements with the detailed system metrics available via your metrics endpoint to better understand the behavior of your DB and the queries you're executing against it.

**Examples:**

Example 1 (unknown):
```unknown
1$ supabase inspect db help2Tools to inspect your Supabase database34Usage:5  supabase inspect db [command]67Available Commands:8  bloat                Estimates space allocated to a relation that is full of dead tuples9  blocking             Show queries that are holding locks and the queries that are waiting for them to be released10  cache-hit            Show cache hit rates for tables and indices1112...
```

Example 2 (unknown):
```unknown
1supabase --db-url postgresql://postgres:postgres@localhost:5432/postgres inspect db bloat
```

Example 3 (unknown):
```unknown
1supabase link --project-ref <project-id>
```

Example 4 (unknown):
```unknown
1$ grant pg_read_all_stats to postgres;
```

---

## plv8: JavaScript Language | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/plv8

**Contents:**
- plv8: JavaScript Language
- Overview#
- Enable the extension#
- Create plv8 functions#
- Examples#
  - Scalar functions#
  - Executing SQL#
  - Set-returning functions#
- Resources#

plv8: JavaScript Language

The plv8 extension is deprecated in projects using Postgres 17. It continues to be supported in projects using Postgres 15, but will need to dropped before those projects are upgraded to Postgres 17. See the Upgrading to Postgres 17 notes for more information.

The plv8 extension allows you use JavaScript within Postgres.

While Postgres natively runs SQL, it can also run other procedural languages. plv8 allows you to run JavaScript code - specifically any code that runs on the V8 JavaScript engine.

It can be used for database functions, triggers, queries and more.

Functions written in plv8 are written just like any other Postgres functions, only with the language identifier set to plv8.

You can call plv8 functions like any other Postgres function:

A scalar function is anything that takes in some user input and returns a single result.

You can execute SQL within plv8 code using the plv8.execute function.

A set-returning function is anything that returns a full set of results - for example, rows in a table.

**Examples:**

Example 1 (unknown):
```unknown
1create or replace function function_name()2returns void as $$3    // V8 JavaScript4    // code5    // here6$$ language plv8;
```

Example 2 (unknown):
```unknown
1select function_name();
```

Example 3 (javascript):
```javascript
1create or replace function hello_world(name text)2returns text as $$34    let output = `Hello, ${name}!`;5    return output;67$$ language plv8;
```

Example 4 (unknown):
```unknown
1create or replace function update_user(id bigint, first_name text)2returns smallint as $$34    var num_affected = plv8.execute(5        'update profiles set first_name = $1 where id = $2',6        [first_name, id]7    );89    return num_affected;10$$ language plv8;
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-postgres-config

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Manual Replication Monitoring | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/replication/manual-replication-monitoring

**Contents:**
- Manual Replication Monitoring
- Track replication health and performance.
  - Primary#
    - Replication status and lag#
    - Replication slot status#
    - WAL size#
    - Check the LSN#
  - Subscriber#
    - Subscription status#
    - Check the LSN#

Manual Replication Monitoring

Track replication health and performance.

Monitoring replication lag is important and there are 3 ways to do this:

The pg_stat_replication table shows the status of any replicas connected to the primary database.

A replication slot can be in one of three states:

The state can be checked using the pg_replication_slots table:

The WAL size can be checked using the pg_ls_waldir() function:

The pg_subscription table shows the status of any subscriptions on a replica and the pg_subscription_rel table shows the status of each table within a subscription.

The srsubstate column in pg_subscription_rel can be one of the following:

**Examples:**

Example 1 (unknown):
```unknown
1select pid, application_name, state, sent_lsn, write_lsn, flush_lsn, replay_lsn, sync_state2from pg_stat_replication;
```

Example 2 (unknown):
```unknown
1select slot_name, active, state from pg_replication_slots;
```

Example 3 (unknown):
```unknown
1select * from pg_ls_waldir();
```

Example 4 (unknown):
```unknown
1select pg_current_wal_lsn();
```

---

## Database Backups | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/backups

**Contents:**
- Database Backups
- Types of backups#
      - Physical backups are not enabled by default
- Frequency of backups#
- Daily backups#
  - Backup process #
    - Backup process for large databases#
  - Restoration process #
- Point-in-Time recovery#
  - Backup process #

Database backups are an integral part of any disaster recovery plan. Disasters come in many shapes and sizes. It could be as simple as accidentally deleting a table column, the database crashing, or even a natural calamity wiping out the underlying hardware a database is running on. The risks and impact brought by these scenarios can never be fully eliminated, but only minimized or even mitigated. Having database backups is a form of insurance policy. They are essentially snapshots of the database at various points in time. When disaster strikes, database backups allow the project to be brought back to any of these points in time, therefore averting the crisis.

The Supabase team regularly monitors the status of backups. In case of any issues, you can contact support. Also you can check out our status page at any time.

Once a project is deleted all associated data will be permanently removed, including any backups stored in S3. This action is irreversible and should be carefully considered before proceeding.

Database backups can be categorized into two types: logical and physical. You can learn more about them here.

To enable physical backups, you have three options:

Once a project satisfies at least one of the requirements for physical backups then logical backups are no longer made. However, your project may revert back to logical backups if you remove add-ons.

You can confirm your project's backup type by navigating to Database Backups > Scheduled backups and if you can download a backup then it is logical, otherwise it is physical.

However, if your project has the Point-in-Time Recovery (PITR) add-on then the backups are physical and you can view them in Database Backups > Point in time.

When deciding how often a database should be backed up, the key business metric Recovery Point Objective (RPO) should be considered. RPO is the threshold for how much data, measured in time, a business could lose when disaster strikes. This amount is fully dependent on a business and its underlying requirements. A low RPO would mean that database backups would have to be taken at an increased cadence throughout the day. Each Supabase project has access to two forms of backups, Daily Backups and Point-in-Time Recovery (PITR). The agreed upon RPO would be a deciding factor in choosing which solution best fits a project.

If you enable PITR, Daily Backups will no longer be taken. PITR provides a finer granularity than Daily Backups, so it's unnecessary to run both.

Database backups do not include objects stored via the Storage API, as the database only includes metadata about these objects. Restoring an old backup does not restore objects that have been deleted since then.

All Pro, Team and Enterprise Plan Supabase projects are backed up automatically on a daily basis. In terms of Recovery Point Objective (RPO), Daily Backups would be suitable for projects willing to lose up to 24 hours worth of data if disaster hits at the most inopportune time. If a lower RPO is required, enabling Point-in-Time Recovery should be considered.

For security purposes, passwords for custom roles are not stored in daily backups, and will not be found in downloadable files. As such, if you are restoring from a daily backup and are using custom roles, you will need to set their passwords once more following a completed restoration.

The Postgres utility pg_dumpall is used to perform daily backups. An SQL file is generated, zipped up, and sent to our storage servers for safe keeping.

You can access daily backups in the Scheduled backups settings in the Dashboard. Pro Plan projects can access the last 7 days' worth of daily backups. Team Plan projects can access the last 14 days' worth of daily backups, while Enterprise Plan projects can access up to 30 days' worth of daily backups. Users can restore their project to any one of the backups. If you wish to generate a logical backup on your own, you can do so through the Supabase CLI.

You can also manage backups programmatically using the Management API:

Databases larger than 15GB1, if they're on a recent build2 of the Supabase platform, get automatically transitioned3 to use daily physical backups. Physical backups are a more performant backup mechanism that lowers the overhead and impact on the database being backed up, and also avoids holding locks on objects in your database for a long period of time. While restores are unaffected, the backups created using this method cannot be downloaded from the Backups section of the dashboard.

This class of physical backups only allows for recovery to a fixed time each day, similar to daily backups. You can upgrade to PITR for access to more granular recovery options.

Once a database is transitioned to using physical backups, it continues to use physical backups, even if the database size falls back below the threshold for the transition.

When selecting a backup to restore to, select the closest available one made before the desired point in time to restore to. Earlier backups can always be chosen too but do consider the number of days' worth of data that could be lost.

The Dashboard will then prompt for a confirmation before proceeding with the restoration. The project will be inaccessible following this. As such, do ensure to allot downtime beforehand. This is dependent on the size of the database. The larger it is, the longer the downtime will be. Once the confirmation has been given, the underlying SQL of the chosen backup is then run against the project. The Postgres utility psql is used to facilitate the restoration. The Dashboard will display a notification once the restoration completes.

If your project is using subscriptions or replication slots, you will need to drop them prior to the restoration, and re-create them afterwards. The slot used by Realtime is exempted from this, and will be handled automatically.

Point-in-Time Recovery (PITR) allows a project to be backed up at much shorter intervals. This provides users an option to restore to any chosen point of up to seconds in granularity. Even with daily backups, a day's worth of data could still be lost. With PITR, backups could be performed up to the point of disaster.

Pro, Team and Enterprise Plan projects can enable PITR as an add-on.

Projects interested in PITR will also need to use at least a Small compute add-on, in order to ensure smooth functioning.

If you enable PITR, Daily Backups will no longer be taken. PITR provides a finer granularity than Daily Backups, so it's unnecessary to run both.

When you disable PITR, all new backups will still be taken as physical backups only. Physical backups can still be used for restoration, but they are not available for direct download. If you need to download a backup after PITR is disabled, you’ll need to take a manual logical backup using the Supabase CLI or pg_dump.

If PITR has been disabled, logical backups remain available until they pass the backup retention period for your plan. After that window passes, only physical backups will be shown.

As discussed here, PITR is made possible by a combination of taking physical backups of a project, as well as archiving Write Ahead Log (WAL) files. Physical backups provide a snapshot of the underlying directory of the database, while WAL files contain records of every change made in the database.

Supabase uses WAL-G, an open source archival and restoration tool, to handle both aspects of PITR. On a daily basis, a snapshot of the database is taken and sent to our storage servers. Throughout the day, as database transactions occur, WAL files are generated and uploaded.

By default, WAL files are backed up at two minute intervals. If these files cross a certain file size threshold, they are backed up immediately. As such, during periods of high amount of transactions, WAL file backups become more frequent. Conversely, when there is no activity in the database, WAL file backups are not made. Overall, this would mean that at the worst case scenario or disaster, the PITR achieves a Recovery Point Objective (RPO) of two minutes.

You can access PITR in the Point in Time settings in the Dashboard. The recovery period of a project is indicated by the earliest and latest points of recoveries displayed in your preferred timezone. If need be, the maximum amount of this recovery period can be modified accordingly.

Note that the latest restore point of the project could be significantly far from the current time. This occurs when there has not been any recent activity in the database, and therefore no WAL file backups have been made recently. This is perfectly fine as the state of the database at the latest point of recovery would still be indicative of the state of the database at the current time given that no transactions have been made in between.

A date and time picker will be provided upon pressing the Start a restore button. The process will only proceed if the selected date and time fall within the earliest and latest points of recoveries.

After locking in the desired point in time to recover to, The Dashboard will then prompt for a review and confirmation before proceeding with the restoration. The project will be inaccessible following this. As such, do ensure to allot for downtime beforehand. This is dependent on the size of the database. The larger it is, the longer the downtime will be. Once the confirmation has been given, the latest physical backup available is downloaded to the project and the database is partially restored. WAL files generated after this physical backup up to the specified point-in-time are then downloaded. The underlying records of transactions in these files are replayed against the database to complete the restoration. The Dashboard will display a notification once the restoration completes.

Pricing depends on the recovery retention period, which determines how many days back you can restore data to any chosen point of up to seconds in granularity.

For a detailed breakdown of how charges are calculated, refer to Manage Point-in-Time Recovery usage.

See the Duplicate Project docs.

During the pg_restore process, the search_path is set to an empty string for predictability, and security. Using unqualified references to functions or relations can cause restorations using logical backups to fail, as the database will not be able to locate the function or relation being referenced. This can happen even if the database functions without issues during normal operations, as the search_path is usually set to include several schemas during normal operations. Therefore, you should always use schema-qualified names within your SQL code.

You can refer to an example PR on how to update SQL code to use schema-qualified names.

Postgres requires that check constraints be:

Violating these requirements can result in numerous failure scenarios, including during logical restorations.

Common examples of check constraints that can result in such failures are:

Views that directly or indirectly reference themselves will cause logical restores to fail due to cyclic dependency errors. These views are also invalid and unusable in Postgres, and any query against them will result in a runtime error.

-- Drop the offending view from your database, or delete them from the logical backup to make it restorable.

Postgres documentation views

The threshold for transitioning will be slowly lowered over time. Eventually, all projects will be transitioned to using physical backups. ↩

Projects created or upgraded after the 14th of July 2022 are eligible. ↩

The transition to physical backups is handled transparently and does not require any user intervention. It involves a single restart of the database to pick up new configuration that can only be loaded at start; the expected downtime for the restart is a few seconds. ↩

**Examples:**

Example 1 (unknown):
```unknown
1# Get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"3export PROJECT_REF="your-project-ref"45# List all available backups6curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \7  "https://api.supabase.com/v1/projects/$PROJECT_REF/database/backups"89# Restore from a PITR (not logical) backup (replace ISO timestamp with desired restore point)10curl -X POST "https://api.supabase.com/v1/projects/$PROJECT_REF/database/backups/restore-pitr" \11  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \12  -H "Content-Type: application/json" \13  -d '{14    "recovery_time_target_unix": "1735689600"15  }'
```

Example 2 (unknown):
```unknown
1-- Direct self-reference2CREATE VIEW my_view AS3  SELECT * FROM my_view;45-- Indirect circular reference6CREATE VIEW v1 AS SELECT * FROM v2;7CREATE VIEW v2 AS SELECT * FROM v1;
```

---

## Network Restrictions | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/network-restrictions

**Contents:**
- Network Restrictions
- To get started via the Dashboard:#
- To get started via the Management API:#
- To get started via the CLI:#
  - Check restrictions#
  - Update restrictions#
  - Remove restrictions#
- Limitations#

If you can't find the Network Restrictions section at the bottom of your Database Settings, update your version of Postgres in the Infrastructure Settings.

Each Supabase project comes with configurable restrictions on the IP ranges that are allowed to connect to Postgres and its pooler ("your database"). These restrictions are enforced before traffic reaches your database. If a connection is not restricted by IP, it still needs to authenticate successfully with valid database credentials.

If direct connections to your database resolve to a IPv6 address, you need to add both IPv4 and IPv6 CIDRs to the list of allowed CIDRs. Network Restrictions will be applied to all database connection routes, whether pooled or direct. You will need to add both the IPv4 and IPv6 networks you want to allow. There are two exceptions: If you have been granted an extension on the IPv6 migration OR if you have purchased the IPv4 add-on, you need only add IPv4 CIDRs.

Network restrictions can be configured in the Database Settings page. Ensure that you have Owner or Admin permissions for the project that you are enabling network restrictions.

You can also manage network restrictions using the Management API:

You can use the get subcommand of the CLI to retrieve the restrictions currently in effect.

If restrictions have been applied, the output of the get command will reflect the IP ranges allowed to connect:

If restrictions have never been applied to your project, the list of allowed CIDRs will be empty, but they will also not have been applied ("Restrictions applied successfully: false"). As a result, all IPs are allowed to connect to your database:

The update subcommand is used to apply network restrictions to your project:

The restrictions specified (in the form of CIDRs) replaces any restrictions that might have been applied in the past. To add to the existing restrictions, you must include the existing restrictions within the list of CIDRs provided to the update command.

To remove all restrictions on your project, you can use the update subcommand with the CIDR 0.0.0.0/0:

**Examples:**

Example 1 (unknown):
```unknown
1# Get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"3export PROJECT_REF="your-project-ref"45# Get current network restrictions6curl -X GET "https://api.supabase.com/v1/projects/$PROJECT_REF/network-restrictions" \7  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN"89# Update network restrictions10curl -X POST "https://api.supabase.com/v1/projects/$PROJECT_REF/network-restrictions/apply" \11  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \12  -H "Content-Type: application/json" \13  -d '{14    "db_allowed_cidrs": [15      "192.168.0.1/24",16    ]17  }'
```

Example 2 (unknown):
```unknown
1> supabase network-restrictions --project-ref {ref} get --experimental2DB Allowed IPv4 CIDRs: &[183.12.1.1/24]3DB Allowed IPv6 CIDRs: &[2001:db8:3333:4444:5555:6666:7777:8888/64]4Restrictions applied successfully: true
```

Example 3 (unknown):
```unknown
1> supabase network-restrictions --project-ref {ref} get --experimental2DB Allowed IPv4 CIDRs: []3DB Allowed IPv6 CIDRs: []4Restrictions applied successfully: false
```

Example 4 (unknown):
```unknown
1> supabase network-restrictions --project-ref {ref} update --db-allow-cidr 183.12.1.1/24 --db-allow-cidr 2001:db8:3333:4444:5555:6666:7777:8888/64 --experimental2DB Allowed IPv4 CIDRs: &[183.12.1.1/24]3DB Allowed IPv6 CIDRs: &[2001:db8:3333:4444:5555:6666:7777:8888/64]4Restrictions applied successfully: true
```

---

## Querying Joins and Nested tables | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/joins-and-nesting

**Contents:**
- Querying Joins and Nested tables
- One-to-many joins#
  - TypeScript types for joins#
- Many-to-many joins#
- Specifying the ON clause for joins with multiple foreign keys#

Querying Joins and Nested tables

The data APIs automatically detect relationships between Postgres tables. Since Postgres is a relational database, this is a very common scenario.

Let's use an example database that stores orchestral_sections and instruments:

The APIs will automatically detect relationships based on the foreign keys:

supabase-js always returns a data object (for success), and an error object (for unsuccessful requests).

These helper types provide the result types from any query, including nested types for database joins.

Given the following schema with a relation between orchestral sections and instruments:

We can get the nested SectionsWithInstruments type like this:

The data APIs will detect many-to-many joins. For example, if you have a database which stored teams of users (where each user could belong to many teams):

In these cases you don't need to explicitly define the joining table (members). If we wanted to fetch all the teams and the members in each team:

For example, if you have a project that tracks when employees check in and out of work shifts:

In this case, you need to explicitly define the join because the joining column on shifts is ambiguous as they are both referencing the scans table.

To fetch all the shifts with scan_id_start and scan_id_end related to a specific scan, use the following syntax:

**Examples:**

Example 1 (javascript):
```javascript
1const { data, error } = await supabase.from('orchestral_sections').select(`2  id,3  name,4  instruments ( id, name )5`)
```

Example 2 (unknown):
```unknown
1create table orchestral_sections (2  "id" serial primary key,3  "name" text4);56create table instruments (7  "id" serial primary key,8  "name" text,9  "section_id" int references "orchestral_sections"10);
```

Example 3 (python):
```python
1import { QueryResult, QueryData, QueryError } from '@supabase/supabase-js'23const sectionsWithInstrumentsQuery = supabase.from('orchestral_sections').select(`4  id,5  name,6  instruments (7    id,8    name9  )10`)11type SectionsWithInstruments = QueryData<typeof sectionsWithInstrumentsQuery>1213const { data, error } = await sectionsWithInstrumentsQuery14if (error) throw error15const sectionsWithInstruments: SectionsWithInstruments = data
```

Example 4 (unknown):
```unknown
1create table users (2  "id" serial primary key,3  "name" text4);56create table teams (7  "id" serial primary key,8  "team_name" text9);1011create table members (12  "user_id" int references users,13  "team_id" int references teams,14  primary key (user_id, team_id)15);
```

---

## pgmq: Queues | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgmq

**Contents:**
- pgmq: Queues

See the Supabase Queues docs.

---

## Realtime Self-hosting Config | Supabase Docs

**URL:** https://supabase.com/docs/guides/self-hosting/realtime/config

**Contents:**
- Realtime Self-hosting Config
- General Settings
      - Parameters
- Database Settings
      - Parameters

Realtime Self-hosting Config

You can use Environment Variables to configure your Realtime Server.

General server settings.

Port which you can connect your client/listeners

Connect to database via either IPv4 or IPv6. Disregarded if database host is an IP address (e.g. '127.0.0.1') and recommended if database host is a name (e.g. 'db.abcd.supabase.co') to prevent potential non-existent domain (NXDOMAIN) errors.

A unique name for Postgres to track the Write-Ahead Logging (WAL). If the Realtime server dies then this slot can keep the changes since the last committed position.

Start logical replication slot as either temporary or permanent

Bind realtime via either IPv4 or IPv6

JSON encoded array of publication names. Realtime RLS currently accepts one publication.

Enable/Disable channels authorization via JWT verification

HS algorithm octet key (e.g. "95x0oR8jq9unl9pOIx")

Expected claim key/value pairs compared to JWT claims via equality checks in order to validate JWT. e.g. '{"iss": "Issuer", "nbf": 1610078130}'.

Expose Prometheus metrics at '/metrics' endpoint.

Specify the minimum amount of time to wait before reconnecting to database

Specify the maximum amount of time to wait before reconnecting to database

Specify how often Realtime RLS should poll the replication slot for changes

Specify how often Realtime RLS should confirm connected subscribers and the tables they're listening to

Soft limit for the number of database changes to fetch per replication poll

Controls the maximum size of a WAL record

Connecting to your database.

Database SSL connection

Connect to database via either IPv4 or IPv6. Disregarded if database host is an IP address (e.g. '127.0.0.1') and recommended if database host is a name (e.g. 'db.abcd.supabase.co') to prevent potential non-existent domain (NXDOMAIN) errors.

---

## Query Optimization | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/query-optimization

**Contents:**
- Query Optimization
- Choosing indexes to improve your query performance.
- Example query#
  - where clause:#
  - join columns#
  - order by clause#
- Key concepts#
  - Analyze the query plan#
  - Use appropriate index types#
  - Partial indexes#

Choosing indexes to improve your query performance.

When working with Postgres, or any relational database, indexing is key to improving query performance. Aligning indexes with common query patterns can speed up data retrieval by an order of magnitude.

This guide is intended to:

This is not a comprehensive resource, but rather a helpful starting point for your optimization journey.

If you're new to query optimization, you may be interested in index_advisor, our tool for automatically detecting indexes that improve performance on a given query.

Consider the following example query that retrieves customer names and purchase dates from two tables:

In this query, there are several parts that indexes could likely help in optimizing the performance:

The where clause filters rows based on certain conditions, and indexing the columns involved can improve this process:

Indexes on the columns used for joining tables can help Postgres avoid scanning tables in their entirety when connecting tables.

Sorting can also be optimized by indexing:

Here are some concepts and tools to keep in mind to help you identify the best index for the job, and measure the impact that your index had:

Use the explain command to understand the query's execution. Look for slow parts, such as Sequential Scans or high cost numbers. If creating an index does not reduce the cost of the query plan, remove it.

Postgres offers various index types like B-tree, Hash, GIN, etc. Select the type that best suits your data and query pattern. Using the right index type can make a significant difference. For example, using a BRIN index on a field that always increases and lives within a table that updates infrequently - like created_at on an orders table - routinely results in indexes that are +10x smaller than the equivalent default B-tree index. That translates into better scalability.

For queries that frequently target a subset of data, a partial index could be faster and smaller than indexing the entire column. A partial index contains a where clause to filter the values included in the index. Note that a query's where clause must match the index for it to be used.

If filtering or joining on multiple columns, a composite index prevents Postgres from referring to multiple indexes when identifying the relevant rows.

Avoid the urge to index columns you operate on infrequently. While indexes can speed up reads, they also slow down writes, so it's important to balance those factors when making indexing decisions.

Postgres maintains a set of statistics about the contents of your tables. Those statistics are used by the query planner to decide when it's is more efficient to use an index vs scanning the entire table. If the collected statistics drift too far from reality, the query planner may make poor decisions. To avoid this risk, you can periodically analyze tables.

By following this guide, you'll be able to discern where indexes can optimize queries and enhance your Postgres performance. Remember that each database is unique, so always consider the specific context and use case of your queries.

**Examples:**

Example 1 (unknown):
```unknown
1select2  a.name,3  b.date_of_purchase4from5  customers as a6  join orders as b on a.id = b.customer_id7where a.sign_up_date > '2023-01-01' and b.status = 'shipped'8order by b.date_of_purchase9limit 10;
```

Example 2 (unknown):
```unknown
1create index idx_customers_sign_up_date on customers (sign_up_date);23create index idx_orders_status on orders (status);
```

Example 3 (unknown):
```unknown
1create index idx_orders_customer_id on orders (customer_id);
```

Example 4 (unknown):
```unknown
1create index idx_orders_date_of_purchase on orders (date_of_purchase);
```

---

## Advanced Log Filtering | Supabase Docs

**URL:** https://supabase.com/docs/guides/telemetry/advanced-log-filtering

**Contents:**
- Advanced Log Filtering
- Querying the logs
- Understanding field references#
- Expanding results#
- Filtering with regular expressions#
  - Find messages that start with a phrase#
  - Find messages that end with a phrase:#
  - Ignore case sensitivity:#
  - Wildcards:#
  - Alphanumeric ranges:#

Advanced Log Filtering

The log tables are queried with a subset of BigQuery SQL syntax. They all have three columns: event_message, timestamp, and metadata.

The metadata column is an array of JSON objects that stores important details about each recorded event. For example, in the Postgres table, the metadata.parsed.error_severity field indicates the error level of an event. To work with its values, you need to unnest them using a cross join.

This approach is commonly used with JSON and array columns, so it might look a bit unfamiliar if you're not used to working with these data types.

Logs returned by queries may be difficult to read in table format. A row can be double-clicked to expand the results into more readable JSON:

The Logs use BigQuery Style regular expressions with the regexp_contains function. In its most basic form, it will check if a string is present in a specified column.

There are multiple operators that you should consider using:

^ only looks for values at the start of a string

$ only looks for values at the end of the string

(?i) ignores capitalization for all proceeding characters

. can represent any string of characters

[1-9a-zA-Z] finds any strings with only numbers and letters

x* zero or more x x+ one or more x x? zero or one x x{4,} four or more x x{3} exactly 3 x

\. interpreted as period . instead of as a wildcard

x|y any string with x or y present

and, or, and not are all native terms in SQL and can be used in conjunction with regular expressions to filter results

Each product table operates independently without the ability to join with other log tables. This may change in the future.

The parser does not yet support with and subquery statements.

Although like and other comparison operators can be used, ilike and similar to are incompatible with BigQuery's variant of SQL. regexp_contains can be used as an alternative.

The log parser is not able to parse the * operator for column selection. Instead, you can access all fields from the metadata column:

**Examples:**

Example 1 (unknown):
```unknown
1select2  event_message,3  parsed.error_severity,4  parsed.user_name5from6  postgres_logs7  -- extract first layer8  cross join unnest(postgres_logs.metadata) as metadata9  -- extract second layer10  cross join unnest(metadata.parsed) as parsed;
```

Example 2 (unknown):
```unknown
1select2  cast(timestamp as datetime) as timestamp,3  event_message,4  metadata5from postgres_logs6where regexp_contains(event_message, 'is present');
```

Example 3 (unknown):
```unknown
1-- find only messages that start with connection2regexp_contains(event_message, '^connection')
```

Example 4 (unknown):
```unknown
1-- find only messages that ends with port=123452regexp_contains(event_message, '$port=12345')
```

---

## Views | Supabase Docs

**URL:** https://supabase.com/docs/guides/graphql/views

**Contents:**
- Views
- Using Postgres Views with GraphQL.
- Primary Keys (Required)#
- Relationships#

Using Postgres Views with GraphQL.

Views, materialized views, and foreign tables can be exposed with pg_graphql.

A primary key is required for an entity to be reflected in the GraphQL schema. Tables can define primary keys with SQL DDL, but primary keys are not available for views, materialized views, or foreign tables. For those entities, you can set a "fake" primary key with a comment directive.

tells pg_graphql to treat "Person".id as the primary key for the Person entity resulting in the following GraphQL type:

Updatable views are reflected in the Query and Mutation types identically to tables. Non-updatable views are read-only and accessible via the Query type only.

pg_graphql identifies relationships among entities by inspecting foreign keys. Views, materialized views, and foreign tables do not support foreign keys. For this reason, relationships can also be defined in comment directive using the structure:

defines a relationship equivalent to the following foreign key

yielding the GraphQL types:

**Examples:**

Example 1 (unknown):
```unknown
1{"primary_key_columns": [<column_name_1>, ..., <column_name_n>]}
```

Example 2 (unknown):
```unknown
1create view "Person" as2  select3    id,4    name5  from6    "Account";78comment on view "Person" is e'@graphql({"primary_key_columns": ["id"]})';
```

Example 3 (unknown):
```unknown
1type Person {2  nodeId: ID!3  id: Int!4  name: String!5}
```

Example 4 (unknown):
```unknown
1{2  "foreign_keys": [3    {4      "local_name": "foo", // optional5      "local_columns": ["account_id"],6      "foreign_name": "bar", // optional7      "foreign_schema": "public",8      "foreign_table": "account",9      "foreign_columns": ["id"]10    }11  ]12}
```

---

## Type-Safe SQL with Kysely | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/kysely-postgres

**Contents:**
- Type-Safe SQL with Kysely
- Code#

Type-Safe SQL with Kysely

Supabase Edge Functions can connect directly to your Postgres database to execute SQL queries. Kysely is a type-safe and autocompletion-friendly typescript SQL query builder.

Combining Kysely with Deno Postgres gives you a convenient developer experience for interacting directly with your Postgres database.

Find the example on GitHub

Get your database connection credentials from the project's Connect panel and store them in an .env file:

Create a DenoPostgresDriver.ts file to manage the connection to Postgres via deno-postgres:

Create an index.ts file to execute a query on incoming requests:

**Examples:**

Example 1 (unknown):
```unknown
1DB_HOSTNAME=2DB_PASSWORD=3DB_SSL_CERT="-----BEGIN CERTIFICATE-----4GET YOUR CERT FROM YOUR PROJECT DASHBOARD5-----END CERTIFICATE-----"
```

Example 2 (python):
```python
1import {2  CompiledQuery,3  DatabaseConnection,4  Driver,5  PostgresCursorConstructor,6  QueryResult,7  TransactionSettings,8} from 'https://esm.sh/kysely@0.23.4'9import { freeze, isFunction } from 'https://esm.sh/kysely@0.23.4/dist/esm/util/object-utils.js'10import { extendStackTrace } from 'https://esm.sh/kysely@0.23.4/dist/esm/util/stack-trace-utils.js'11import { Pool, PoolClient } from 'https://deno.land/x/postgres@v0.17.0/mod.ts'1213export interface PostgresDialectConfig {14  pool: Pool | (() => Promise<Pool>)15  cursor?: PostgresCursorConstructor16  onCreateConnection?: (connection: DatabaseConnection) => Promise<void>17}1819const PRIVATE_RELEASE_METHOD = Symbol()2021export class PostgresDriver implements Driver {22  readonly #config: PostgresDialectConfig23  readonly #connections = new WeakMap<PoolClient, DatabaseConnection>()24  #pool?: Pool2526  constructor(config: PostgresDialectConfig) {27    this.#config = freeze({ ...config })28  }2930  async init(): Promise<void> {31    this.#pool = isFunction(this.#config.pool) ? await this.#config.pool() : this.#config.pool32  }3334  async acquireConnection(): Promise<DatabaseConnection> {35    const client = await this.#pool!.connect()36    let connection = this.#connections.get(client)3738    if (!connection) {39      connection = new PostgresConnection(client, {40        cursor: this.#config.cursor ?? null,41      })42      this.#connections.set(client, connection)4344      // The driver must take care of calling `onCreateConnection` when a new45      // connection is created. The `pg` module doesn't provide an async hook46      // for the connection creation. We need to call the method explicitly.47      if (this.#config?.onCreateConnection) {48        await this.#config.onCreateConnection(connection)49      }50    }5152    return connection53  }5455  async beginTransaction(56    connection: DatabaseConnection,57    settings: TransactionSettings58  ): Promise<void> {59    if (settings.isolationLevel) {60      await connection.executeQuery(61        CompiledQuery.raw(`start transaction isolation level ${settings.isolationLevel}`)62      )63    } else {64      await connection.executeQuery(CompiledQuery.raw('begin'))65    }66  }6768  async commitTransaction(connection: DatabaseConnection): Promise<void> {69    await connection.executeQuery(CompiledQuery.raw('commit'))70  }7172  async rollbackTransaction(connection: DatabaseConnection): Promise<void> {73    await connection.executeQuery(CompiledQuery.raw('rollback'))74  }7576  async releaseConnection(connection: PostgresConnection): Promise<void> {77    connection[PRIVATE_RELEASE_METHOD]()78  }7980  async destroy(): Promise<void> {81    if (this.#pool) {82      const pool = this.#pool83      this.#pool = undefined84      await pool.end()85    }86  }87}8889interface PostgresConnectionOptions {90  cursor: PostgresCursorConstructor | null91}9293class PostgresConnection implements DatabaseConnection {94  #client: PoolClient95  #options: PostgresConnectionOptions9697  constructor(client: PoolClient, options: PostgresConnectionOptions) {98    this.#client = client99    this.#options = options100  }101102  async executeQuery<O>(compiledQuery: CompiledQuery): Promise<QueryResult<O>> {103    try {104      const result = await this.#client.queryObject<O>(compiledQuery.sql, [105        ...compiledQuery.parameters,106      ])107108      if (109        result.command === 'INSERT' ||110        result.command === 'UPDATE' ||111        result.command === 'DELETE'112      ) {113        const numAffectedRows = BigInt(result.rowCount || 0)114115        return {116          numUpdatedOrDeletedRows: numAffectedRows,117          numAffectedRows,118          rows: result.rows ?? [],119        } as any120      }121122      return {123        rows: result.rows ?? [],124      }125    } catch (err) {126      throw extendStackTrace(err, new Error())127    }128  }129130  async *streamQuery<O>(131    _compiledQuery: CompiledQuery,132    chunkSize: number133  ): AsyncIterableIterator<QueryResult<O>> {134    if (!this.#options.cursor) {135      throw new Error(136        "'cursor' is not present in your postgres dialect config. It's required to make streaming work in postgres."137      )138    }139140    if (!Number.isInteger(chunkSize) || chunkSize <= 0) {141      throw new Error('chunkSize must be a positive integer')142    }143144    // stream not available145    return null146  }147148  [PRIVATE_RELEASE_METHOD](): void {149    this.#client.release()150  }151}
```

Example 3 (python):
```python
1import { serve } from 'https://deno.land/std@0.175.0/http/server.ts'2import { Pool } from 'https://deno.land/x/postgres@v0.17.0/mod.ts'3import {4  Kysely,5  Generated,6  PostgresAdapter,7  PostgresIntrospector,8  PostgresQueryCompiler,9} from 'https://esm.sh/kysely@0.23.4'10import { PostgresDriver } from './DenoPostgresDriver.ts'1112console.log(`Function "kysely-postgres" up and running!`)1314interface AnimalTable {15  id: Generated<bigint>16  animal: string17  created_at: Date18}1920// Keys of this interface are table names.21interface Database {22  animals: AnimalTable23}2425// Create a database pool with one connection.26const pool = new Pool(27  {28    tls: { caCertificates: [Deno.env.get('DB_SSL_CERT')!] },29    database: 'postgres',30    hostname: Deno.env.get('DB_HOSTNAME'),31    user: 'postgres',32    port: 5432,33    password: Deno.env.get('DB_PASSWORD'),34  },35  136)3738// You'd create one of these when you start your app.39const db = new Kysely<Database>({40  dialect: {41    createAdapter() {42      return new PostgresAdapter()43    },44    createDriver() {45      return new PostgresDriver({ pool })46    },47    createIntrospector(db: Kysely<unknown>) {48      return new PostgresIntrospector(db)49    },50    createQueryCompiler() {51      return new PostgresQueryCompiler()52    },53  },54})5556serve(async (_req) => {57  try {58    // Run a query59    const animals = await db.selectFrom('animals').select(['id', 'animal', 'created_at']).execute()6061    // Neat, it's properly typed \o/62    console.log(animals[0].created_at.getFullYear())6364    // Encode the result as pretty printed JSON65    const body = JSON.stringify(66      animals,67      (key, value) => (typeof value === 'bigint' ? value.toString() : value),68      269    )7071    // Return the response with the correct content type header72    return new Response(body, {73      status: 200,74      headers: {75        'Content-Type': 'application/json; charset=utf-8',76      },77    })78  } catch (err) {79    console.error(err)80    return new Response(String(err?.message ?? err), { status: 500 })81  }82})
```

---

## Replication Monitoring | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/replication/replication-monitoring

**Contents:**
- Replication Monitoring
- Track replication status, view logs, and troubleshoot issues.
      - Private Alpha
  - Viewing pipeline status#
    - Pipeline states#
  - Viewing detailed pipeline metrics#
    - Replication lag metrics#
    - Table states#
  - Handling errors#
    - Table errors#

Replication Monitoring

Track replication status, view logs, and troubleshoot issues.

Replication is currently in private alpha. Access is limited and features may change.

After setting up replication, you can monitor the status and health of your replication pipelines directly from the Supabase Dashboard. The pipeline is the active Postgres replication process that continuously streams changes from your database to your destination.

To monitor your replication pipelines:

Each destination shows its pipeline in one of these states:

For detailed information about a specific pipeline, click View status on the destination. This opens the pipeline status page where you can monitor replication performance and table states.

The status page shows replication lag metrics that help you determine how fast your pipeline is replicating data. These metrics are loaded directly from Postgres itself.

The pipeline status page also shows the state of individual tables being replicated. Each table can be in one of these states:

Errors can occur at two levels: per table or per pipeline.

Table errors occur during the copy phase and affect individual tables. These errors can be retried without stopping the entire pipeline.

Viewing table error details:

Recovering from table errors:

When a table encounters an error during the copy phase, you can reset the table state. This will restart the table copy from the beginning.

Pipeline errors occur during the streaming phase (Live state) and affect the entire pipeline. When streaming data, if an error occurs, the entire pipeline will stop and enter a Failed state. This prevents data loss by ensuring no changes are skipped.

When a pipeline error occurs, you'll receive an email notification immediately. This ensures you're promptly notified of any issues so you can take action to resolve them.

Viewing pipeline error details:

Recovering from pipeline errors:

To recover from a pipeline error, you'll need to:

To see detailed logs for all your replication pipelines:

Logs contain diagnostic information that may be too technical for most users. If you're experiencing issues with replication, reaching out to support with your error details is recommended.

If you see a Failed status:

To ensure optimal performance:

If you notice issues with your replication:

For more troubleshooting tips, see the Replication FAQ.

---

## Managing Environments | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/managing-environments

**Contents:**
- Managing Environments
- Manage multiple environments using Database Migrations and GitHub Actions.
- Set up a local environment#
- Create a new migration#
  - Manual migration#
  - Auto schema diff#
- Deploy a migration#
  - Configure GitHub Actions#
  - Open a PR with new migration#
  - Release to production#

Managing Environments

Manage multiple environments using Database Migrations and GitHub Actions.

This guide shows you how to set up your local Supabase development environment that integrates with GitHub Actions to automatically test and release schema changes to staging and production Supabase projects.

The first step is to set up your local repository with the Supabase CLI:

You should see a new supabase directory. Then you need to link your local repository with your Supabase project:

You can get your $PROJECT_ID from your project's dashboard URL:

If you're using an existing Supabase project, you might have made schema changes through the Dashboard. Run the following command to pull these changes before making local schema changes from the CLI:

This command creates a new migration in supabase/migrations/<timestamp>_remote_schema.sql which reflects the schema changes you have made previously.

Now commit your local changes to Git and run the local development setup:

You are now ready to develop schema changes locally and create your first migration.

There are two ways to make schema changes:

Create a new migration script by running:

You should see a new file created: supabase/migrations/<timestamp>_new_employee.sql. You can then write SQL statements in this script using a text editor:

Apply the new migration to your local database:

This command recreates your local database from scratch and applies all migration scripts under supabase/migrations directory. Now your local database is up to date.

The new migration command also supports stdin as input. This allows you to pipe in an existing script from another file or stdout:

supabase migration new new_employee < create_employees_table.sql

Unlike manual migrations, auto schema diff creates a new migration script from changes already applied to your local database.

Create an employees table under the public schema using Studio UI, accessible at localhost:54323 by default.

Next, generate a schema diff by running the following command:

You should see that a new file supabase/migrations/<timestamp>_new_employee.sql is created. Open the file and verify that the generated DDL statements are the same as below.

You may notice that the auto-generated migration script is more verbose than the manually written one. This is because the default schema diff tool does not account for default privileges added by the initial schema.

Commit the new migration script to git and you are ready to deploy.

Alternatively, you may pass in the --use-migra experimental flag to generate a more concise migration using migra.

Without the -f file flag, the output is written to stdout by default.

supabase db diff --use-migra

In a production environment, we recommend using a CI/CD pipeline to deploy new migrations with GitHub Actions rather than deploying from your local machine.

This example uses two Supabase projects, one for production and one for staging.

Prepare your environments by:

You need a new project for staging. A project which has already been modified to reflect the production project's schema can't be used because the CLI would reapply these changes.

The Supabase CLI requires a few environment variables to run in non-interactive mode.

We recommend adding these as encrypted secrets to your GitHub Actions runners.

Create the following files inside the .github/workflows directory:

The full example code is available in the demo repository.

Commit these files to git and push to your main branch on GitHub. Update these environment variables to match your Supabase projects:

When configured correctly, your repository will have CI and Release workflows that trigger on new commits pushed to main and develop branches.

Follow the migration steps to create a supabase/migrations/<timestamp>_new_employee.sql file.

Checkout a new branch feat/employee from develop , commit the migration file, and push to GitHub.

Open a PR from feat/employee to the develop branch to see that the CI workflow has been triggered.

Once the test error is resolved, merge this PR and watch the deployment in action.

After verifying your staging project has successfully migrated, create another PR from develop to main and merge it to deploy the migration to the production project.

The release job applies all new migration scripts merged in supabase/migrations directory to a linked Supabase project. You can control which project the job links to via PROJECT_ID environment variable.

When setting up a new staging project, you might need to sync the initial schema with migrations previously applied to the production project.

One way is to leverage the Release workflow:

The GitHub Actions runner will deploy your existing migrations to the staging project.

Alternatively, you can also apply migrations through your local CLI to a linked remote database.

Once pushed, check that the migration version is up to date for both local and remote databases.

If you have been using Supabase hosted projects for a long time, you might encounter the following permission error when executing db pull.

To resolve this error, you need to grant postgres role permissions to graphql schema. You can do that by running the following query from Supabase dashboard's SQL Editor.

If you created a table through Supabase dashboard, and your new migration script contains ALTER TABLE statements, you might run into permission error when applying them on staging or production databases.

This is because tables created through Supabase dashboard are owned by supabase_admin role while the migration scripts executed through CLI are under postgres role.

One way to solve this is to reassign the owner of those tables to postgres role. For example, if your table is named users in the public schema, you can run the following command to reassign owner.

Apart from tables, you also need to reassign owner of other entities using their respective commands, including types, functions, and schemas.

Sometimes your teammate may merge a new migration file to git main branch, and now you need to rebase your local schema changes on top.

We can handle this scenario gracefully by renaming your old migration file with a new timestamp.

In case reset fails, you can manually resolve conflicts by editing <t+2>_dev_A.sql file.

Once validated locally, commit your changes to Git and push to GitHub.

**Examples:**

Example 1 (unknown):
```unknown
1supabase init
```

Example 2 (unknown):
```unknown
1supabase login2supabase link --project-ref $PROJECT_ID
```

Example 3 (unknown):
```unknown
1https://supabase.com/dashboard/project/<project-id>
```

Example 4 (unknown):
```unknown
1supabase db pull
```

---

## Connecting to Metabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/metabase

**Contents:**
- Connecting to Metabase
  - Register
  - Connect to Postgres
      - connection notice
  - Explore

Connecting to Metabase

Metabase is an Open Source data visualization tool. You can use it to explore your data stored in Supabase.

Create a Metabase account or deploy locally with Docker

Deploying with Docker:

The server should be available at http://localhost:3000/setup

Connect your Postgres server to Metabase.

If you're in an IPv6 environment or have the IPv4 Add-On, you can use the direct connection string instead of Supavisor in Session mode.

Explore your data in Metabase

**Examples:**

Example 1 (unknown):
```unknown
1docker pull metabase/metabase:latest
```

Example 2 (unknown):
```unknown
1docker run -d -p 3000:3000 --name metabase metabase/metabase
```

---

## Prisma | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/prisma

**Contents:**
- Prisma
  - Create a custom user for Prisma
      - password manager
  - Create a Prisma Project
  - Add your connection information to your .env file
  - Create your migrations
  - Install the prisma client
  - Test your API

This quickly shows how to connect your Prisma application to Supabase Postgres. If you encounter any problems, reference the Prisma troubleshooting docs.

If you plan to solely use Prisma instead of the Supabase Data API (PostgREST), turn it off in the API Settings.

For security, consider using a password generator for the Prisma role.

Create a new Prisma Project on your computer

Create a new directory

Initiate a new Prisma project

If you're in an IPv6 environment or have the IPv4 Add-On, you can use the direct connection string instead of Supavisor in Session mode.

In your .env file, set the DATABASE_URL variable to your connection string

Change your string's [DB-USER] to prisma and add the password you created in step 1

If you have already modified your Supabase database, synchronize it with your migration file. Otherwise create new tables for your database

Create new tables in your prisma.schema file

commit your migration

Install the Prisma client and generate its model

Create a index.ts file and run it to test your connection

**Examples:**

Example 1 (unknown):
```unknown
1-- Create custom user2create user "prisma" with password 'custom_password' bypassrls createdb;34-- extend prisma's privileges to postgres (necessary to view changes in Dashboard)5grant "prisma" to "postgres";67-- Grant it necessary permissions over the relevant schemas (public)8grant usage on schema public to prisma;9grant create on schema public to prisma;10grant all on all tables in schema public to prisma;11grant all on all routines in schema public to prisma;12grant all on all sequences in schema public to prisma;13alter default privileges for role postgres in schema public grant all on tables to prisma;14alter default privileges for role postgres in schema public grant all on routines to prisma;15alter default privileges for role postgres in schema public grant all on sequences to prisma;
```

Example 2 (unknown):
```unknown
1-- alter prisma password if needed2alter user "prisma" with password 'new_password';
```

Example 3 (unknown):
```unknown
1mkdir hello-prisma2cd hello-prisma
```

Example 4 (unknown):
```unknown
1npm init -y2npm install prisma typescript ts-node @types/node --save-dev34npx tsc --init56npx prisma init
```

---

## Event Triggers | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/event-triggers

**Contents:**
- Event Triggers
- Automatically execute SQL on database events.
- Creating an event trigger#
  - Example trigger function - prevent dropping tables#
  - Example trigger function - auto enable Row Level Security#
  - Event trigger Functions and firing events#
- Disabling an event trigger#
- Dropping an event trigger#
- Resources#

Automatically execute SQL on database events.

In Postgres, an event trigger is similar to a trigger, except that it is triggered by database level events (and is usually reserved for superusers)

With our Supautils extension (installed automatically for all Supabase projects), the postgres user has the ability to create and manage event triggers.

Some use cases for event triggers are:

The guide covers two example event triggers:

Only the postgres user can create event triggers, so make sure you are authenticated as them. As with triggers, event triggers consist of 2 parts

This example protects any table from being dropped. You can override it by temporarily disabling the event trigger: ALTER EVENT TRIGGER dont_drop_trigger DISABLE;

Event triggers can be triggered on:

Event triggers run for each DDL command specified above and can consume resources which may cause performance issues if not used carefully.

Within each event trigger, helper functions exist to view the objects being modified or the command being run. For example, our example calls pg_event_trigger_dropped_objects() to view the object(s) being dropped. For a more comprehensive overview of these functions, read the official event trigger definition documentation

To view the matrix commands that cause an event trigger to fire, read the official event trigger matrix documentation

You can disable an event trigger using the alter event trigger command:

You can delete a trigger using the drop event trigger command:

**Examples:**

Example 1 (unknown):
```unknown
1-- Function2CREATE OR REPLACE FUNCTION dont_drop_function()3  RETURNS event_trigger LANGUAGE plpgsql AS $$4DECLARE5    obj record;6    tbl_name text;7BEGIN8    FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()9    LOOP10        IF obj.object_type = 'table' THEN11            RAISE EXCEPTION 'ERROR: All tables in this schema are protected and cannot be dropped';12        END IF;13    END LOOP;14END;15$$;1617-- Event trigger18CREATE EVENT TRIGGER dont_drop_trigger19ON sql_drop20EXECUTE FUNCTION dont_drop_function();
```

Example 2 (unknown):
```unknown
1CREATE OR REPLACE FUNCTION rls_auto_enable()2RETURNS EVENT_TRIGGER3LANGUAGE plpgsql4SECURITY DEFINER5SET search_path = pg_catalog6AS $$7DECLARE8  cmd record;9BEGIN10  FOR cmd IN11    SELECT *12    FROM pg_event_trigger_ddl_commands()13    WHERE command_tag IN ('CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO')14      AND object_type IN ('table','partitioned table')15  LOOP16     IF cmd.schema_name IS NOT NULL AND cmd.schema_name IN ('public') AND cmd.schema_name NOT IN ('pg_catalog','information_schema') AND cmd.schema_name NOT LIKE 'pg_toast%' AND cmd.schema_name NOT LIKE 'pg_temp%' THEN17      BEGIN18        EXECUTE format('alter table if exists %s enable row level security', cmd.object_identity);19        RAISE LOG 'rls_auto_enable: enabled RLS on %', cmd.object_identity;20      EXCEPTION21        WHEN OTHERS THEN22          RAISE LOG 'rls_auto_enable: failed to enable RLS on %', cmd.object_identity;23      END;24     ELSE25        RAISE LOG 'rls_auto_enable: skip % (either system schema or not in enforced list: %.)', cmd.object_identity, cmd.schema_name;26     END IF;27  END LOOP;28END;29$$;3031DROP EVENT TRIGGER IF EXISTS ensure_rls;32CREATE EVENT TRIGGER ensure_rls33ON ddl_command_end34WHEN TAG IN ('CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO')35EXECUTE FUNCTION rls_auto_enable();
```

Example 3 (unknown):
```unknown
1ALTER EVENT TRIGGER dont_drop_trigger DISABLE;
```

Example 4 (unknown):
```unknown
1DROP EVENT TRIGGER dont_drop_trigger;
```

---

## Python client | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/vecs-python-client

**Contents:**
- Python client
- Manage unstructured vector stores in PostgreSQL.
- Quick start#
  - Initialize your project#
  - Create a collection#
  - Add embeddings#
  - Query the collection#
- Deep dive#
- Resources#

Manage unstructured vector stores in PostgreSQL.

Supabase provides a Python client called vecs for managing unstructured vector stores. This client provides a set of useful tools for creating and querying collections in Postgres using the pgvector extension.

Let's see how Vecs works using a local database. Make sure you have the Supabase CLI installed on your machine.

Start a local Postgres instance in any folder using the init and start commands. Make sure you have Docker running!

Inside a Python shell, run the following commands to create a new collection called "docs", with 3 dimensions.

Now we can insert some embeddings into our "docs" collection using the upsert() command:

You can now query the collection to retrieve a relevant match:

For a more in-depth guide on vecs collections, see API.

**Examples:**

Example 1 (unknown):
```unknown
1# Initialize your project2supabase init34# Start Postgres5supabase start
```

Example 2 (unknown):
```unknown
1import vecs23# create vector store client4vx = vecs.create_client("postgresql://postgres:postgres@localhost:54322/postgres")56# create a collection of vectors with 3 dimensions7docs = vx.get_or_create_collection(name="docs", dimension=3)
```

Example 3 (unknown):
```unknown
1import vecs23# create vector store client4docs = vecs.get_or_create_collection(name="docs", dimension=3)56# a collection of vectors with 3 dimensions7vectors=[8  ("vec0", [0.1, 0.2, 0.3], {"year": 1973}),9  ("vec1", [0.7, 0.8, 0.9], {"year": 2012})10]1112# insert our vectors13docs.upsert(vectors=vectors)
```

Example 4 (unknown):
```unknown
1import vecs23docs = vecs.get_or_create_collection(name="docs", dimension=3)45# query the collection filtering metadata for "year" = 20126docs.query(7    data=[0.4,0.5,0.6],      # required8    limit=1,                         # number of records to return9    filters={"year": {"$eq": 2012}}, # metadata filters10)
```

---

## Query with PostgreSQL | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/query-with-postgres

**Contents:**
- Query with PostgreSQL
- Query analytics bucket data directly from PostgreSQL using SQL.
- Setup overview#
- Installing via Dashboard UI#
- Querying your data#
  - Common query examples#
- Manual installation#

Query with PostgreSQL

Query analytics bucket data directly from PostgreSQL using SQL.

Once your data flows into an analytics bucket—either via the Replication Pipeline or custom pipelines—you can query it directly from Postgres using standard SQL.

This is made possible by the Iceberg Foreign Data Wrapper, which creates a bridge between your Postgres database and Iceberg tables.

You have two options to enable querying:

The dashboard provides the easiest setup experience:

Once the foreign data wrapper is installed, you can query your Iceberg tables using standard SQL:

Get the latest events:

Join with transactional data:

For advanced use cases, you can manually install and configure the Iceberg Foreign Data Wrapper. See the Iceberg Foreign Data Wrapper documentation for detailed instructions.

**Examples:**

Example 1 (unknown):
```unknown
1select *2from schema_name.table_name3limit 100;
```

Example 2 (unknown):
```unknown
1select event_id, event_name, event_timestamp2from analytics.events3order by event_timestamp desc4limit 1000;
```

Example 3 (unknown):
```unknown
1SELECT2  e.event_id,3  e.event_name,4  u.user_email5FROM analytics.events e6JOIN public.users u ON e.user_id = u.id7WHERE e.event_timestamp > NOW() - INTERVAL '7 days'8LIMIT 100;
```

---

## JavaScript: Call a Postgres function | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/rpc?queryGroups=example&example=call-a-read-only-postgres-function

---

## Postgres.js | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres-js

**Contents:**
- Postgres.js
  - Connecting with Postgres.js#
  - Install
  - Connect
  - Execute commands

Postgres.js is a full-featured Postgres client for Node.js and Deno.

Install Postgres.js and related dependencies.

Create a db.js file with the connection details.

To get your connection details, go to the Connect panel. Choose Transaction pooler if you're on a platform with transient connections, such as a serverless function, and Session pooler if you have a long-lived connection. Copy the URI and save it as the environment variable DATABASE_URL.

Use the connection to execute commands.

**Examples:**

Example 1 (unknown):
```unknown
1npm i postgres
```

Example 2 (python):
```python
1// db.js2import postgres from 'postgres'34const connectionString = process.env.DATABASE_URL5const sql = postgres(connectionString)67export default sql
```

Example 3 (python):
```python
1import sql from './db.js'23async function getUsersOver(age) {4  const users = await sql`5    select name, age6    from users7    where age > ${ age }8  `9  // users = Result [{ name: "Walter", age: 80 }, { name: 'Murray', age: 68 }, ...]10  return users11}
```

---

## Postgres Changes | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/postgres-changes

**Contents:**
- Postgres Changes
- Listen to Postgres changes using Supabase Realtime.
- Quick start#
  - Set up a Supabase project with a 'todos' table
  - Allow anonymous access
  - Enable Postgres replication
  - Install the client
  - Create the client
  - Listen to changes by schema
  - Insert dummy data

Listen to Postgres changes using Supabase Realtime.

Let's explore how to use Realtime's Postgres Changes feature to listen to database events.

In this example we'll set up a database table, secure it with Row Level Security, and subscribe to all changes using the Supabase client libraries.

Create a new project in the Supabase Dashboard.

After your project is ready, create a table in your Supabase database. You can do this with either the Table interface or the SQL Editor.

In this example we'll turn on Row Level Security for this table and allow anonymous access. In production, be sure to secure your application with the appropriate permissions.

Go to your project's Publications settings, and under supabase_realtime, toggle on the tables you want to listen to.

Alternatively, add tables to the supabase_realtime publication by running the given SQL:

Install the Supabase JavaScript client.

This client will be used to listen to Postgres changes.

Listen to changes on all tables in the public schema by setting the schema property to 'public' and event name to *. The event name can be one of:

The channel name can be any string except 'realtime'.

Now we can add some data to our table which will trigger the channelA event handler.

You can use the Supabase client libraries to subscribe to database changes.

Subscribe to specific schema events using the schema parameter:

The channel name can be any string except 'realtime'.

Use the event parameter to listen only to database INSERTs:

The channel name can be any string except 'realtime'.

Use the event parameter to listen only to database UPDATEs:

The channel name can be any string except 'realtime'.

Use the event parameter to listen only to database DELETEs:

The channel name can be any string except 'realtime'.

Subscribe to specific table events using the table parameter:

The channel name can be any string except 'realtime'.

To listen to different events and schema/tables/filters combinations with the same channel:

Use the filter parameter for granular changes:

Realtime offers filters so you can specify the data your client receives at a more granular level.

To listen to changes when a column's value in a table equals a client-specified value:

This filter uses Postgres's = filter.

To listen to changes when a column's value in a table does not equal a client-specified value:

This filter uses Postgres's != filter.

To listen to changes when a column's value in a table is less than a client-specified value:

This filter uses Postgres's < filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table is less than or equal to a client-specified value:

This filter uses Postgres' <= filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table is greater than a client-specified value:

This filter uses Postgres's > filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table is greater than or equal to a client-specified value:

This filter uses Postgres's >= filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table equals any client-specified values:

This filter uses Postgres's = ANY. Realtime allows a maximum of 100 values for this filter.

By default, only new record changes are sent but if you want to receive the old record (previous values) whenever you UPDATE or DELETE a record, you can set the replica identity of your table to full:

RLS policies are not applied to DELETE statements, because there is no way for Postgres to verify that a user has access to a deleted record. When RLS is enabled and replica identity is set to full on a table, the old record contains only the primary key(s).

Postgres Changes works out of the box for tables in the public schema. You can listen to tables in your private schemas by granting table SELECT permissions to the database role found in your access token. You can run a query similar to the following:

We strongly encourage you to enable RLS and create policies for tables in private schemas. Otherwise, any role you grant access to will have unfettered read access to the table.

You may choose to sign your own tokens to customize claims that can be checked in your RLS policies.

Your project JWT secret is found with your Project API keys in your dashboard.

Do not expose the service_role token on the client because the role is authorized to bypass row-level security.

To use your own JWT with Realtime make sure to set the token after instantiating the Supabase client and before connecting to a Channel.

You will need to refresh tokens on your own, but once generated, you can pass them to Realtime.

For example, if you're using the supabase-js v2 client then you can pass your token like this:

You can't filter Delete events when tracking Postgres Changes. This limitation is due to the way changes are pulled from Postgres.

Realtime currently does not work when table names contain spaces.

Realtime systems usually require forethought because of their scaling dynamics. For the Postgres Changes feature, every change event must be checked to see if the subscribed user has access. For instance, if you have 100 users subscribed to a table where you make a single insert, it will then trigger 100 "reads": one for each user.

There can be a database bottleneck which limits message throughput. If your database cannot authorize the changes rapidly enough, the changes will be delayed until you receive a timeout.

Database changes are processed on a single thread to maintain the change order. That means compute upgrades don't have a large effect on the performance of Postgres change subscriptions. You can estimate the expected maximum throughput for your database below.

If you are using Postgres Changes at scale, you should consider using separate "public" table without RLS and filters. Alternatively, you can use Realtime server-side only and then re-stream the changes to your clients using a Realtime Broadcast.

Enter your database settings to estimate the maximum throughput for your instance:

Don't forget to run your own benchmarks to make sure that the performance is acceptable for your use case.

We are making many improvements to Realtime's Postgres Changes. If you are uncertain about the performance of your use case, reach out using Support Form and we will be happy to help you. We have a team of engineers that can advise you on the best solution for your use-case.

**Examples:**

Example 1 (unknown):
```unknown
1-- Create a table called "todos"2-- with a column to store tasks.3create table todos (4  id serial primary key,5  task text6);
```

Example 2 (unknown):
```unknown
1-- Turn on security2alter table "todos"3enable row level security;45-- Allow anonymous access6create policy "Allow anonymous access"7on todos8for select9to anon10using (true);
```

Example 3 (unknown):
```unknown
1alter publication supabase_realtime2add table your_table_name;
```

Example 4 (unknown):
```unknown
1npm install @supabase/supabase-js
```

---

## AI & Vectors | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai

**Contents:**
- AI & Vectors
- The best vector database is the database you already have.
- Search#
- Examples#
- Integrations#
- Case studies#

The best vector database is the database you already have.

Supabase provides an open source toolkit for developing AI applications using Postgres and pgvector. Use the Supabase client libraries to store, index, and query your vector embeddings at scale.

The toolkit includes:

You can use Supabase to build different types of search features for your app, including:

Check out all of the AI templates and examples in our GitHub repository.

Headless Vector Search

Image Search with OpenAI CLIP

Hugging Face inference

Building ChatGPT Plugins

Vector search with Next.js and OpenAI

Berri AI Boosts Productivity by Migrating from AWS RDS to Supabase with pgvector

Firecrawl switches from Pinecone to Supabase for PostgreSQL vector embeddings

Markprompt: GDPR-Compliant AI Chatbots for Docs and Websites

---

## Migrate from Postgres to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/postgres

**Contents:**
- Migrate from Postgres to Supabase
- Migrate your existing Postgres database to Supabase.
- Connection modes#
- Method 1: Google Colab (easiest)#
- Method 2: Manual dump/restore#
  - Prerequisites#
    - Source Postgres requirements#
    - Migration environment#
  - Pre-Migration checklist#
    - Check available extensions in Supabase#

Migrate from Postgres to Supabase

Migrate your existing Postgres database to Supabase.

This is a guide for migrating your Postgres database to Supabase. Supabase is a robust and open-source platform. Supabase provides all the backend features developers need to build a product: a Postgres database, authentication, instant APIs, edge functions, real-time subscriptions, and storage. Postgres is the core of Supabase—for example, you can use row-level security, and there are more than 40 Postgres extensions available.

This guide demonstrates how to migrate your Postgres database to Supabase to get the most out of Postgres while gaining access to all the features you need to build a project.

This guide provides three methods for migrating your Postgres database to Supabase:

Supabase provides the following connection modes:

Use Supavisor session mode for the database migration tasks (pg_dump/restore and logical replication).

Supabase provides a Google Colab migration notebook for a guided migration experience: Supabase Migration Colab Notebook

This is ideal if you prefer a step-by-step, copy-paste workflow with minimal setup.

This method works for all Postgres versions using CLI tools.

For optimal performance, run the migration from a cloud VM, not your local machine. The VM should be in the same region as either your source or target database to optimize network performance. See the Resource Requirements table in Step 2 for VM sizing recommendations.

Resource Requirements:

Also, you can temporarily increase compute size and/or disk IOPS and throughput via Settings → Compute and Disk if you want faster database restore (you can use larger -j for pg_restore if you do so).

If doing a maintenance window migration, prevent data changes:

For testing without a maintenance window, skip this step but use lower -j values.

Notes about dump flags:

Run pg_dump --help for a full list of options.

Note: For testing without a maintenance window, use lower -j values to avoid impacting production performance.

If restore fails with extension errors, check that errors are only extension-related.

For Postgres 18+, pg_dump includes statistics with --with-statistics, but you should still run VACUUM for optimal performance.

Times vary based on hardware, network, and parallelization settings

This method allows migration with minimal downtime using Postgres's logical replication feature. Requires Postgres 10+ on both source and target.

Every table receiving UPDATE/DELETE must have a replica identity (typically a PRIMARY KEY). For tables without one:

Plan a schema freeze, sequence sync before cutover, and handle LOBs separately.

Edit Postgres configuration files:

Connect to your Supabase database:

Wait until all tables show srsubstate = 'r' (ready) status.

After initial data sync is complete, but BEFORE switching to Supabase:

Stop writes to the source database (if not already read-only)

Drop subscription on Supabase:

Update application connection strings to point to Supabase

Verify application functionality

On source database (after successful migration):

For detailed restrictions, see Postgres Logical Replication Restrictions

Use Dump/Restore when:

Use Logical Replication when:

**Examples:**

Example 1 (unknown):
```unknown
1-- Check database size2select pg_size_pretty(pg_database_size(current_database())) as size;34-- Check Postgres version5select version();67-- List installed extensions8select * from pg_extension order by extname;910-- Check active connections11select count(*) from pg_stat_activity;
```

Example 2 (unknown):
```unknown
1-- Connect to your Supabase database and check available extensions2SELECT name, comment FROM pg_available_extensions ORDER BY name;34-- Compare with source database extensions5SELECT extname FROM pg_extension ORDER BY extname;67-- Install needed extensions8CREATE EXTENSION IF NOT EXISTS extension_name;
```

Example 3 (unknown):
```unknown
1# Install Postgres client and tools2sudo apt update3sudo apt install software-properties-common4sudo sh -c 'echo "deb http://apt.Postgres.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'5wget --quiet -O - https://www.Postgres.org/media/keys/ACCC4CF8.asc | sudo apt-key add -6sudo apt update7sudo apt install Postgres-client-17 tmux htop iotop moreutils89# Start or attach to tmux session10tmux a -t migration || tmux new -s migration
```

Example 4 (unknown):
```unknown
1-- Connect to source database and run:2ALTER DATABASE your_database_name SET default_transaction_read_only = true;
```

---

## Print PostgreSQL version | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/which-version-of-postgres

**Contents:**
- Print PostgreSQL version

Print PostgreSQL version

It's important to know which version of Postgres you are running as each major version has different features and may cause breaking changes. You may also need to update your schema when upgrading or downgrading to a major Postgres version.

Run the following query using the SQL Editor in the Supabase Dashboard:

Which should return something like:

This query can also be executed via psql or any other query editor if you prefer to connect directly to the database.

**Examples:**

Example 1 (unknown):
```unknown
1select2  version();
```

Example 2 (unknown):
```unknown
1PostgreSQL 15.1 on aarch64-unknown-linux-gnu, compiled by gcc (Ubuntu 10.3.0-1ubuntu1~20.04) 10.3.0, 64-bit
```

---

## Roles, superuser access and unsupported operations | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/roles-superuser

**Contents:**
- Roles, superuser access and unsupported operations
- Unsupported operations#

Roles, superuser access and unsupported operations

Supabase provides the default postgres role to all instances deployed. Superuser access is not given as it allows destructive operations to be performed on the database.

To ensure you are not impacted by this, additional privileges are granted to the postgres user to allow it to run some operations that are normally restricted to superusers.

However, this does mean that some operations, that typically require superuser privileges, are not available on Supabase. These are documented below:

---

## Database Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/functions?language=sql

**Contents:**
- Database Functions
- Quick demo#
- Getting started#
- Simple functions#
- Returning data sets#
    - Planets
    - People
- Passing parameters#
- Suggestions#
  - Database Functions vs Edge Functions#

Postgres has built-in support for SQL functions. These functions live inside your database, and they can be used with the API.

Supabase provides several options for creating database functions. You can use the Dashboard or create them directly using SQL. We provide a SQL editor within the Dashboard, or you can connect to your database and run the SQL queries yourself.

Let's create a basic Database Function which returns a string "hello world".

At it's most basic a function has the following parts:

When naming your functions, make the name of the function unique as overloaded functions are not supported.

After the Function is created, we have several ways of "executing" the function - either directly inside the database using SQL, or with one of the client libraries.

Database Functions can also return data sets from Tables or Views.

For example, if we had a database with some Star Wars data inside:

We could create a function which returns all the planets:

Because this function returns a table set, we can also apply filters and selectors. For example, if we only wanted the first planet:

Let's create a Function to insert a new planet into the planets table and return the new ID. Note that this time we're using the plpgsql language.

Once again, you can execute this function either inside your database using a select query, or with the client libraries:

For data-intensive operations, use Database Functions, which are executed within your database and can be called remotely using the REST and GraphQL API.

For use-cases which require low-latency, use Edge Functions, which are globally-distributed and can be written in Typescript.

Postgres allows you to specify whether you want the function to be executed as the user calling the function (invoker), or as the creator of the function (definer). For example:

It is best practice to use security invoker (which is also the default). If you ever use security definer, you must set the search_path. If you use an empty search path (search_path = ''), you must explicitly state the schema for every relation in the function body (e.g. from public.table). This limits the potential damage if you allow access to schemas which the user executing the function should not have.

By default, database functions can be executed by any role. There are two main ways to restrict this:

On a case-by-case basis. Specifically revoke permissions for functions you want to protect. Execution needs to be revoked for both public and the role you're restricting:

Restrict function execution by default. Specifically grant access when you want a function to be executable by a specific role.

To restrict all existing functions, revoke execution permissions from both public and the role you want to restrict:

To restrict all new functions, change the default privileges for both public and the role you want to restrict:

You can then regrant permissions for a specific function to a specific role:

You can add logs to help you debug functions. This is especially recommended for complex functions.

Good targets to log include:

To create custom logs in the Dashboard's Postgres Logs, you can use the raise keyword. By default, there are 3 observed severity levels:

You can create custom errors with the raise exception keywords.

A common pattern is to throw an error when a variable doesn't meet a condition:

Value checking is common, so Postgres provides a shorthand: the assert keyword. It uses the following format:

Error messages can also be captured and modified with the exception keyword:

For more complex functions or complicated debugging, try logging:

**Examples:**

Example 1 (unknown):
```unknown
1create or replace function hello_world() -- 12returns text -- 23language sql -- 34as $$  -- 45  select 'hello world';  -- 56$$; --6
```

Example 2 (unknown):
```unknown
1select hello_world();
```

Example 3 (unknown):
```unknown
1| id  | name     |2| --- | -------- |3| 1   | Tatooine |4| 2   | Alderaan |5| 3   | Kashyyyk |
```

Example 4 (unknown):
```unknown
1| id  | name             | planet_id |2| --- | ---------------- | --------- |3| 1   | Anakin Skywalker | 1         |4| 2   | Luke Skywalker   | 1         |5| 3   | Princess Leia    | 2         |6| 4   | Chewbacca        | 3         |
```

---

## Logging | Supabase Docs

**URL:** https://supabase.com/docs/guides/telemetry/logs?queryGroups=product&product=postgres&queryGroups=source&source=edge_logs

**Contents:**
- Logging
- Product logs#
- Working with API logs#
  - Allowed headers#
  - Additional request metadata#
- Logging Postgres queries#
  - Configuring pgaudit.log#
  - RAISEd log messages in Postgres#
- Logging realtime connections#
- Logs Explorer#

The Supabase Platform includes a Logs Explorer that allows log tracing and debugging. Log retention is based on your project's pricing plan.

Supabase provides a logging interface specific to each product. You can use simple regular expressions for keywords and patterns to search log event messages. You can also export and download the log events matching your query as a spreadsheet.

API logs show all network requests and response for the REST and GraphQL APIs. If Read Replicas are enabled, logs are automatically filtered between databases as well as the API Load Balancer endpoint. Logs for a specific endpoint can be toggled with the Source button on the upper-right section of the dashboard.

When viewing logs originating from the API Load Balancer endpoint, the upstream database or the one that eventually handles the request can be found under the Redirect Identifier field. This is equivalent to metadata.load_balancer_redirect_identifier when querying the underlying logs.

API logs run through the Cloudflare edge servers and will have attached Cloudflare metadata under the metadata.request.cf.* fields.

A strict list of request and response headers are permitted in the API logs. Request and response headers will still be received by the server(s) and client(s), but will not be attached to the API logs generated.

To attach additional metadata to a request, it is recommended to use the User-Agent header for purposes such as device or version identification.

Do not log Personal Identifiable Information (PII) within the User-Agent header, to avoid infringing data protection privacy laws. Overly fine-grained and detailed user agents may allow fingerprinting and identification of the end user through PII.

To enable query logs for other categories of statements:

The stored value under pgaudit.log determines the classes of statements that are logged by pgAudit extension. Refer to the pgAudit documentation for the full list of values.

To enable logging for function calls/do blocks, writes, and DDL statements for a single session, execute the following within the session:

To permanently set a logging configuration (beyond a single session), execute the following, then perform a fast reboot:

To help with debugging, we recommend adjusting the log scope to only relevant statements as having too wide of a scope would result in a lot of noise in your Postgres logs.

Note that in the above example, the role is set to postgres. To log user-traffic flowing through the HTTP APIs powered by PostgREST, set your configuration values for the authenticator.

By default, the log level will be set to log. To view other levels, run the following:

Note that as per the pgAudit log_level documentation, error, fatal, and panic are not allowed.

To reset system-wide settings, execute the following, then perform a fast reboot:

If any permission errors are encountered when executing alter role postgres ..., it is likely that your project has yet to receive the patch to the latest version of supautils, which is currently being rolled out.

Messages that are manually logged via RAISE INFO, RAISE NOTICE, RAISE WARNING, and RAISE LOG are shown in Postgres Logs. Note that only messages at or above your logging level are shown. Syncing of messages to Postgres Logs may take a few minutes.

If your logs aren't showing, check your logging level by running:

Note that LOG is a higher level than WARNING and ERROR, so if your level is set to LOG, you will not see WARNING and ERROR messages.

Realtime doesn't log new WebSocket connections or Channel joins by default. Enable connection logging per client by including an info log_level parameter when instantiating the Supabase client.

The Logs Explorer exposes logs from each part of the Supabase stack as a separate table that can be queried and joined using SQL.

You can access the following logs from the Sources drop-down:

The Logs Explorer uses BigQuery and supports all available SQL functions and operators.

Each log entry is stored with a timestamp as a TIMESTAMP data type. Use the appropriate timestamp function to utilize the timestamp field in a query.

Raw top-level timestamp values are rendered as unix microsecond. To render the timestamps in a human-readable format, use the DATETIME() function to convert the unix timestamp display into an ISO-8601 timestamp.

Each log event stores metadata an array of objects with multiple levels, and can be seen by selecting single log events in the Logs Explorer. To query arrays, use unnest() on each array field and add it to the query as a join. This allows you to reference the nested objects with an alias and select their individual fields.

For example, to query the edge logs without any joins:

The resulting metadata key is rendered as an array of objects in the Logs Explorer. In the following diagram, each box represents a nested array of objects:

Perform a cross join unnest() to work with the keys nested in the metadata key.

To query for a nested value, add a join for each array level:

This surfaces the following columns available for selection:

This allows you to select the method and cf_ipcountry columns. In JS dot notation, the full paths for each selected column are:

The Logs Explorer has a maximum of 1000 rows per run. Use LIMIT to optimize your queries by reducing the number of rows returned further.

Querying your entire log history might seem appealing. For Enterprise customers that have a large retention range, you run the risk of timeouts due additional time required to scan the larger dataset.

When querying large objects, the columnar storage engine selects each column associated with each nested key, resulting in a large number of columns being selected. This inadvertently impacts the query speed and may result in timeouts or memory errors, especially for projects with a lot of logs.

Instead, select only the values required.

The Logs Explorer includes Templates (available in the Templates tab or the dropdown in the Query tab) to help you get started.

For example, you can enter the following query in the SQL Editor to retrieve each user's IP address:

Refer to the full field reference for each available source below. Do note that in order to access each nested key, you would need to perform the necessary unnesting joins

**Examples:**

Example 1 (unknown):
```unknown
1node MyApp/1.2.3 (device-id:abc123)2Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 MyApp/1.2.3 (Foo v1.3.2; Bar v2.2.2)
```

Example 2 (unknown):
```unknown
1-- temporary single-session config update2set pgaudit.log = 'function, write, ddl';
```

Example 3 (unknown):
```unknown
1-- equivalent permanent config update.2alter role postgres set pgaudit.log to 'function, write, ddl';
```

Example 4 (unknown):
```unknown
1-- for API-related logs2alter role authenticator set pgaudit.log to 'write';
```

---

## pgvector: Embeddings and vector similarity | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgvector

**Contents:**
- pgvector: Embeddings and vector similarity
- Concepts#
  - Vector similarity#
  - Embeddings#
- Usage#
  - Enable the extension#
- Usage#
  - Create a table to store vectors#
  - Storing a vector / embedding#
- Specific usage cases#

pgvector: Embeddings and vector similarity

pgvector is a Postgres extension for vector similarity search. It can also be used for storing embeddings.

The name of pgvector's Postgres extension is vector.

Learn more about Supabase's AI & Vector offering.

Vector similarity refers to a measure of the similarity between two related items. For example, if you have a list of products, you can use vector similarity to find similar products. To do this, you need to convert each product into a "vector" of numbers, using a mathematical model. You can use a similar model for text, images, and other types of data. Once all of these vectors are stored in the database, you can use vector similarity to find similar items.

This is particularly useful if you're building AI applications with large language models. You can create and store embeddings for retrieval augmented generation (RAG).

In this example we'll generate a vector using Transformer.js, then store it in the database using the Supabase client.

If you use an IVFFlat or HNSW index and naively filter the results based on the value of another column, you may get fewer rows returned than requested.

For example, the following query may return fewer than 5 rows, even if 5 corresponding rows exist in the database. This is because the embedding index may not return 5 rows matching the filter.

To get the exact number of requested rows, use iterative search to continue scanning the index until enough results are found.

**Examples:**

Example 1 (unknown):
```unknown
1create table posts (2  id serial primary key,3  title text not null,4  body text not null,5  embedding extensions.vector(384)6);
```

Example 2 (python):
```python
1import { pipeline } from '@xenova/transformers'2const generateEmbedding = await pipeline('feature-extraction', 'Supabase/gte-small')34const title = 'First post!'5const body = 'Hello world!'67// Generate a vector using Transformers.js8const output = await generateEmbedding(body, {9  pooling: 'mean',10  normalize: true,11})1213// Extract the embedding output14const embedding = Array.from(output.data)1516// Store the vector in Postgres17const { data, error } = await supabase.from('posts').insert({18  title,19  body,20  embedding,21})
```

Example 3 (unknown):
```unknown
1SELECT * FROM items WHERE category_id = 123 ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
```

---

## Airtable | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/airtable

**Contents:**
- Airtable
- Preparation#
  - Enable Wrappers#
  - Enable the Airtable Wrapper#
  - Store your credentials (optional)#
  - Connecting to Airtable#
  - Create a schema#
- Entities#
  - Records#
    - Operations#

You can enable the Airtable wrapper right from the Supabase dashboard.

Airtable is an easy-to-use online platform for creating and sharing relational databases.

The Airtable Wrapper allows you to read data from your Airtable bases/tables within your Postgres database.

Before you can query Airtable, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the airtable_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

Get your token from Airtable's developer portal.

We need to provide Postgres with the credentials to connect to Airtable, and any additional options. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The Airtable Wrapper supports data reads from the Airtable API.

The Airtable Wrapper supports data reads from Airtable's Records endpoint (read only).

Get your base ID and table ID from your table's URL.

Foreign tables must be lowercase, regardless of capitalization in Airtable.

This FDW doesn't support query pushdown.

This section describes important limitations and considerations when using this FDW:

This will create a "foreign table" inside your Postgres database called airtable_table:

You can now fetch your Airtable data from within your Postgres database:

We can also create a foreign table from an Airtable View called airtable_view:

You can now fetch your Airtable data from within your Postgres database:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper airtable_wrapper2  handler airtable_fdw_handler3  validator airtable_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Airtable API key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<Airtable API Key or PAT>', -- Airtable API key or Personal Access Token (PAT)4  'airtable',5  'Airtable API key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server airtable_server2  foreign data wrapper airtable_wrapper3  options (4    api_key_id '<key_ID>' -- The Key ID from above.5  );
```

---

## Vector columns | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/vector-columns

**Contents:**
- Vector columns
- Usage#
  - Enable the extension#
  - Create a table to store vectors#
  - Storing a vector / embedding#
  - Querying a vector / embedding#
  - Indexes#

Supabase offers a number of different ways to store and query vectors within Postgres. The SQL included in this guide is applicable for clients in all programming languages. If you are a Python user see your Python client options after reading the Learn section.

Vectors in Supabase are enabled via pgvector, a Postgres extension for storing and querying vectors in Postgres. It can be used to store embeddings.

After enabling the vector extension, you will get access to a new data type called vector. The size of the vector (indicated in parenthesis) represents the number of dimensions stored in that vector.

In the above SQL snippet, we create a documents table with a column called embedding (note this is just a regular Postgres column - you can name it whatever you like). We give the embedding column a vector data type with 384 dimensions. Change this to the number of dimensions produced by your embedding model. For example, if you are generating embeddings using the open source gte-small model, you would set this number to 384 since that model produces 384 dimensions.

In general, embeddings with fewer dimensions perform best. See our analysis on fewer dimensions in pgvector.

In this example we'll generate a vector using Transformers.js, then store it in the database using the Supabase JavaScript client.

This example uses the JavaScript Supabase client, but you can modify it to work with any supported language library.

Similarity search is the most common use case for vectors. pgvector support 3 new operators for computing distance:

Choosing the right operator depends on your needs. Dot product tends to be the fastest if your vectors are normalized. For more information on how embeddings work and how they relate to each other, see What are Embeddings?.

Supabase client libraries like supabase-js connect to your Postgres instance via PostgREST. PostgREST does not currently support pgvector similarity operators, so we'll need to wrap our query in a Postgres function and call it via the rpc() method:

This function takes a query_embedding argument and compares it to all other embeddings in the documents table. Each comparison returns a similarity score. If the similarity is greater than the match_threshold argument, it is returned. The number of rows returned is limited by the match_count argument.

Feel free to modify this method to fit the needs of your application. The match_threshold ensures that only documents that have a minimum similarity to the query_embedding are returned. Without this, you may end up returning documents that subjectively don't match. This value will vary for each application - you will need to perform your own testing to determine the threshold that makes sense for your app.

If you index your vector column, ensure that the order by sorts by the distance function directly (rather than sorting by the calculated similarity column, which may lead to the index being ignored and poor performance).

To execute the function from your client library, call rpc() with the name of your Postgres function:

In this example embedding would be another embedding you wish to compare against your table of pre-generated embedding documents. For example if you were building a search engine, every time the user submits their query you would first generate an embedding on the search query itself, then pass it into the above rpc() function to match.

Be sure to use embeddings produced from the same embedding model when calculating distance. Comparing embeddings from two different models will produce no meaningful result.

Vectors and embeddings can be used for much more than search. Learn more about embeddings at What are Embeddings?.

Once your vector table starts to grow, you will likely want to add an index to speed up queries. See Vector indexes to learn how vector indexes work and how to create them.

**Examples:**

Example 1 (unknown):
```unknown
1create table documents (2  id serial primary key,3  title text not null,4  body text not null,5  embedding extensions.vector(384)6);
```

Example 2 (python):
```python
1import { pipeline } from '@xenova/transformers'2const generateEmbedding = await pipeline('feature-extraction', 'Supabase/gte-small')34const title = 'First post!'5const body = 'Hello world!'67// Generate a vector using Transformers.js8const output = await generateEmbedding(body, {9  pooling: 'mean',10  normalize: true,11})1213// Extract the embedding output14const embedding = Array.from(output.data)1516// Store the vector in Postgres17const { data, error } = await supabase.from('documents').insert({18  title,19  body,20  embedding,21})
```

Example 3 (javascript):
```javascript
1create or replace function match_documents (2  query_embedding extensions.vector(384),3  match_threshold float,4  match_count int5)6returns table (7  id bigint,8  title text,9  body text,10  similarity float11)12language sql stable13as $$14  select15    documents.id,16    documents.title,17    documents.body,18    1 - (documents.embedding <=> query_embedding) as similarity19  from documents20  where 1 - (documents.embedding <=> query_embedding) > match_threshold21  order by (documents.embedding <=> query_embedding) asc22  limit match_count;23$$;
```

Example 4 (javascript):
```javascript
1const { data: documents } = await supabaseClient.rpc('match_documents', {2  query_embedding: embedding, // Pass the embedding you want to compare3  match_threshold: 0.78, // Choose an appropriate threshold for your data4  match_count: 10, // Choose the number of matches5})
```

---

## GraphQL | Supabase Docs

**URL:** https://supabase.com/docs/guides/graphql

**Contents:**
- GraphQL
- Autogenerated GraphQL APIs with Postgres.
- Quickstart#
- Clients#
  - Supabase Studio#
  - HTTP Request#
  - cURL#
  - supabase-js#
  - GraphiQL#
- Schema & Table Visibility#

Autogenerated GraphQL APIs with Postgres.

The Supabase GraphQL API is automatically reflected from your database's schema using pg_graphql. It supports:

All requests resolve in a single round-trip leading to fast response times and high throughput.

If you haven't created a Supabase project, do that here so you can follow along with the guide.

https://<PROJECT_REF>.supabase.co/graphql/v1 is your project's GraphQL API endpoint. See PROJECT_REF for instructions on finding your project's reference. Note that the url does not allow a trailing /.

To access the API you MUST provide your project's API key as a header in every request. For example see line 2 of the cURL request below.

For user authentication, pass an Authorization header e.g.

See the auth docs to understand how to sign-up/sign-in users to your application and retrieve a JWT. The apollo and relay guides also include complete examples of using Supabase Auth with GraphQL. Supabase Auth works with row level security (RLS) allowing you to control which users can access tables/rows.

The fastest way to get started with GraphQL on Supabase is using the GraphQL IDE (GraphiQL) built directly into Supabase Studio.

If you're new to GraphQL or Supabase, we strongly recommend starting with Supabase GraphQL by following the Supabase Studio guide.

For more experienced users, or when you're ready to productionize your application, access the API using supabase-js, GraphiQL, or any HTTP client, for example cURL.

The easiest way to make a GraphQL request with Supabase is to use Supabase Studio's builtin GraphiQL IDE. You can access GraphiQL here by selecting the relevant project. Alternatively, navigate there within Studio at API Docs > GraphQL > GraphiQL.

Type queries in the central query editor and use the green icon to submit requests to the server. Results are shown in the output display to the right of the editor.

To explore the API visually, select the docs icon shown below and navigate through each type to see how they connect to the Graph.

pg_graphql mirrors the structure of the project's SQL schema in the GraphQL API. If your project is new and empty, the GraphQL API will be empty as well, with the exception of basic introspection types. For a more interesting result, go to the SQL or table editor and create a table.

Head back to GraphiQL to see the new table reflected in your GraphQL API's Query and Mutation types.

If you'd like your type and field names to match the GraphQL convention of PascalCase for types and camelCase for fields, check out the pg_graphql inflection guide.

To access the GraphQL API over HTTP, first collect your project reference and API Key.

To hit the Supabase GraphQL API using cURL, submit a POST request to your GraphQL API's URL shown below, substituting in your PROJECT_REF and passing the project's API_KEY as the apiKey header:

In that example, the GraphQL query is

and there are no variables

The JS ecosystem supports multiple prominent GraphQL frameworks. supabase-js is unopinionated about your GraphQL tooling and can integrate with all of them.

For an example integration, check out the Relay guide, complete with Supabase Auth support.

If you'd prefer to connect to Supabase GraphQL using an external IDE like GraphiQL, save the HTML snippet below as supabase_graphiql.html and open it in your browser. Be sure to substitute in your PROJECT_REF and API_KEY beneath the EDIT BELOW comment:

pg_graphql uses Postgres' search_path and permissions system to determine which schemas and entities are exposed in the GraphQL schema. By default on Supabase, tables, views, and functions in the public schema are visible to anonymous (anon) and logged in (authenticated) roles.

To remove a table from the GraphQL API, you can revoke permission on that table from the the relevant role. For example, to remove table foo from the API for anonymous users you could run:

You can similarly revoke permissions using the more granular insert, update, delete, and truncate permissions to remove individual entrypoints in the GraphQL API. For example, revoking update permission removes the updateFooCollection entrypoing in the API's Mutation type.

Adding a schema to the GraphQL API is a two step process.

First, we need to add the new schema to the API search path. In the example below, we add a comma separated value for the new app schema:

Next, make sure the schema and entities (tables/views/functions) that you intend to expose are accessible by the relevant roles. For example, to match permissions from the public schema:

Note that in practice you likely prefer a more secure set of permissions, particularly for anonymous API users.

To maximize stability, you are in control of when to upgrade your GraphQL API. To see which version of pg_graphql you have, and the highest upgrade version available, execute:

Which returns a table, for example:

The default_version is the highest version available on your database. The installed_version is the version currently enabled in your database. If the two differ, as in the example, you can upgrade your installed version by running:

To upgrade your GraphQL API with 0 downtime.

When making a decision to upgrade, you can review features of the upgraded version in the changelog.

Always test a new version of pg_graphql extensively on a development or staging instance before updating your production instance. pg_graphql follows SemVer, which makes API backwards compatibility relatively safe for minor and patch updates. Even so, it's critical to verify that changes do not negatively impact the specifics of your project's API in other ways, e.g. requests/sec or CPU load.

When starting a local project through the Supabase CLI, the output of supabase start provides the information needed to call the GraphQL API directly. You can also use the Supabase Studio url to access the builtin GraphiQL IDE.

Your Supabase project reference or PROJECT_REF is a 20 digit unique identifier for your project, for example bvykdyhlwawojivopztl. The project reference is used throughout your supabase application including the project's API URL. You can find the project reference in by logging in to Supabase Studio and navigating to Settings > General > Project Settings > Reference ID

Your Supabase API Key is a public value that must be sent with every API request. The key is visible in Supabase Studio at Settings > API > Project API keys

**Examples:**

Example 1 (unknown):
```unknown
1curl -X POST https://<PROJECT_REF>.supabase.co/graphql/v1 \2    -H 'apiKey: <API_KEY>' \3    -H 'Content-Type: application/json' \4    --data-raw '{"query": "{ accountCollection(first: 1) { edges { node { id } } } }", "variables": {}}'
```

Example 2 (unknown):
```unknown
1-H 'Authorization: Bearer <JWT>'
```

Example 3 (unknown):
```unknown
1curl -X POST https://<PROJECT_REF>.supabase.co/graphql/v1 \2    -H 'apiKey: <API_KEY>' \3    -H 'Content-Type: application/json' \4    --data-raw '{"query": "{ accountCollection(first: 1) { edges { node { id } } } }", "variables": {}}'
```

Example 4 (unknown):
```unknown
1{2  accountCollection(first: 1) {3    edges {4      node {5        id6      }7    }8  }9}
```

---

## Migrate from Render to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/render

**Contents:**
- Migrate from Render to Supabase
- Migrate your Render Postgres database to Supabase.
- Retrieve your Render database credentials #
- Retrieve your Supabase connection string #
- Migrate the database#
- Enterprise#

Migrate from Render to Supabase

Migrate your Render Postgres database to Supabase.

Render is a popular Web Hosting service in the online services category that also has a managed Postgres service. Render has a great developer experience, allowing users to deploy straight from GitHub or GitLab. This is the core of their product and they do it really well. However, when it comes to Postgres databases, it may not be the best option.

Supabase is one of the best free alternative to Render Postgres. Supabase provide all the backend features developers need to build a product: a Postgres database, authentication, instant APIs, edge functions, realtime subscriptions, and storage. Postgres is the core of Supabase—for example, you can use row-level security and there are more than 40 Postgres extensions available.

This guide demonstrates how to migrate from Render to Supabase to get the most out of Postgres while gaining access to all the features you need to build a project.

If you're new to Supabase, create a project. Make a note of your password, you will need this later. If you forget it, you can reset it here.

On your project dashboard, click Connect

Under Session pooler, Copy the connection string and replace the password placeholder with your database password.

If you're in an IPv6 environment or have the IPv4 Add-On, you can use the direct connection string instead of Supavisor in Session mode.

The fastest way to migrate your database is with the Supabase migration tool on Google Colab. Alternatively, you can use the pg_dump and psql command line tools, which are included in a full Postgres installation.

If you're planning to migrate a database larger than 6 GB, we recommend upgrading to at least a Large compute add-on. This will ensure you have the necessary resources to handle the migration efficiently.

We strongly advise you to pre-provision the disk space you will need for your migration. On paid projects, you can do this by navigating to the Compute and Disk Settings page. For more information on disk scaling and disk limits, check out our disk settings documentation.

Contact us if you need more help migrating your project.

**Examples:**

Example 1 (unknown):
```unknown
1%env PSQL_COMMAND=PGPASSWORD=RgaMDfTS_password_FTPa7 psql -h dpg-a_server_in.oregon-postgres.render.com -U my_db_pxl0_user my_db_pxl0
```

---

## Maturity Model | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/maturity-model

**Contents:**
- Maturity Model
- Prototyping#
- Collaborating#
- In production#
- Enterprise#

Supabase is great for building something very fast and for scaling up. However, it's important to note that as your application matures and your team expands, the practices you use for managing an application in production should not be the same as the practices you used for prototyping.

The Dashboard is a quick and easy tool for building applications while you are prototyping. That said, we strongly recommend using Migrations to manage your database changes. You can use our CLI to capture any changes you have made on the Dashboard so that you can commit them a version control system, like git.

As soon as you start collaborating with team members, all project changes should be in version control. At this point we strongly recommend moving away from using the Dashboard for schema changes. Use migrations to manage your database, and check them into your version control system to track every change.

Once your application is live, you should never change your database using the Dashboard - everything should be done with Migrations. Some other important things to consider at this point include:

For a more secure setup, consider running your workload across several organizations. It's a common pattern to have a Production organization which is restricted to only those team members who are qualified to have direct access to production databases.

Reach out to growth if you need help designing a secure development workflow for your organization.

---

## Partitioning tables | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/partitions

**Contents:**
- Partitioning tables
- Benefits of table partitioning#
- Partitioning methods#
- Creating partitioned tables#
- Querying partitioned tables#
  - Querying the parent table#
  - Querying specific partitions#
- When to partition your tables#
- Examples#
  - Range partitioning#

Table partitioning is a technique that allows you to divide a large table into smaller, more manageable parts called “partitions”.

Each partition contains a subset of the data based on a specified criteria, such as a range of values or a specific condition. Partitioning can significantly improve query performance and simplify data management for large datasets.

Postgres supports various partitioning methods based on how you want to partition your data. The commonly used methods are:

Let's consider an example of range partitioning for a sales table based on the order date. We'll create monthly partitions to store data for each month:

To create a partitioned table you append partition by range (<column_name>) to the table creation statement. The column that you are partitioning with must be included in any unique index, which is the reason why we specify a composite primary key here (primary key (order_date, id)).

To query a partitioned table, you have two options:

When you query the parent table, Postgres automatically routes the query to the relevant partitions based on the conditions specified in the query. This allows you to retrieve data from all partitions simultaneously.

This query will retrieve data from both the sales_2000_01 and sales_2000_02 partitions.

If you only need to retrieve data from a specific partition, you can directly query that partition instead of the parent table. This approach is useful when you want to target a specific range or condition within a partition.

This query will retrieve data only from the sales_2000_02 partition.

There is no real threshold to determine when you should use partitions. Partitions introduce complexity, and complexity should be avoided until it's needed. A few guidelines:

Here are simple examples for each of the partitioning types in Postgres.

Let's consider a range partitioning example for a table that stores sales data based on the order date. We'll create monthly partitions to store data for each month.

In this example, the sales table is partitioned into two partitions: sales_january and sales_february. The data in these partitions is based on the specified range of order dates:

Let's consider a list partitioning example for a table that stores customer data based on their region. We'll create partitions to store customers from different regions.

In this example, the customers table is partitioned into two partitions: customers_americas and customers_asia. The data in these partitions is based on the specified list of regions:

You can use hash partitioning to evenly distribute data.

In this example, the products table is partitioned into two partitions: products_one and products_two. The data is distributed across these partitions using a hash function:

There are several other tools available for Postgres partitioning, most notably pg_partman. Native partitioning was introduced in Postgres 10 and is generally thought to have better performance.

**Examples:**

Example 1 (unknown):
```unknown
1create table sales (2    id bigint generated by default as identity,3    order_date date not null,4    customer_id bigint,5    amount bigint,67    -- We need to include all the8    -- partitioning columns in constraints:9    primary key (order_date, id)10)11partition by range (order_date);1213create table sales_2000_0114	partition of sales15  for values from ('2000-01-01') to ('2000-02-01');1617create table sales_2000_0218	partition of sales19	for values from ('2000-02-01') to ('2000-03-01');
```

Example 2 (unknown):
```unknown
1select *2from sales3where order_date >= '2000-01-01' and order_date < '2000-03-01';
```

Example 3 (unknown):
```unknown
1select *2from sales_2000_02;
```

Example 4 (unknown):
```unknown
1create table sales (2    id bigint generated by default as identity,3    order_date date not null,4    customer_id bigint,5    amount bigint,67    -- We need to include all the8    -- partitioning columns in constraints:9    primary key (order_date, id)10)11partition by range (order_date);1213create table sales_2000_0114	partition of sales15  for values from ('2000-01-01') to ('2000-02-01');1617create table sales_2000_0218	partition of sales19	for values from ('2000-02-01') to ('2000-03-01');
```

---

## Advanced pgTAP Testing | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development/testing/pgtap-extended

**Contents:**
- Advanced pgTAP Testing
- Using database.dev#
  - Setting up dbdev#
  - Installing test helpers#
- Test helper benefits#
- Schema-wide Row Level Security testing#
- Test file organization#
  - Creating a pre-test hook#
  - Benefits#
- Example: Advanced RLS testing#

Advanced pgTAP Testing

While basic pgTAP provides excellent testing capabilities, you can enhance the testing workflow using database development tools and helper packages. This guide covers advanced testing techniques using database.dev and community-maintained test helpers.

Database.dev is a package manager for Postgres that allows installation and use of community-maintained packages, including testing utilities.

To use database development tools and packages, install some prerequisites:

The Test Helpers package provides utilities that simplify testing Supabase-specific features:

The test helpers package provides several advantages over writing raw pgTAP tests:

Simplified User Management

Row Level Security (RLS) Testing Utilities

When working with Row Level Security, it's crucial to ensure that RLS is enabled on all tables that need it. Create a simple test to verify RLS is enabled across an entire schema:

When working with multiple test files that share common setup requirements, it's beneficial to create a single "pre-test" file that handles the global environment setup. This approach reduces duplication and ensures consistent test environments.

Since pgTAP test files are executed in alphabetical order, create a setup file that runs first by using a naming convention like 000-setup-tests-hooks.sql:

This setup file should contain:

Here's an example setup file:

This approach provides several advantages:

Your subsequent test files (001-auth-tests.sql, 002-rls-tests.sql) can focus solely on their specific test cases, knowing that the environment is properly configured.

Here's a complete example using test helpers to verify RLS policies putting it all together:

Todo apps are great for learning, but this section explores testing a more realistic scenario: a multi-tenant content publishing platform. This example demonstrates testing complex permissions, plan restrictions, and content management.

This demo app implements:

When writing tests, verify:

The app schema tables are defined like this:

Now to setup the RLS policies for each tables:

Now everything is setup, let's write RLS test cases, note that each section could be in its own test:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists http with schema extensions;2create extension if not exists pg_tle;3drop extension if exists "supabase-dbdev";4select pgtle.uninstall_extension_if_exists('supabase-dbdev');5select6    pgtle.install_extension(7        'supabase-dbdev',8        resp.contents ->> 'version',9        'PostgreSQL package manager',10        resp.contents ->> 'sql'11    )12from extensions.http(13    (14        'GET',15        'https://api.database.dev/rest/v1/'16        || 'package_versions?select=sql,version'17        || '&package_name=eq.supabase-dbdev'18        || '&order=version.desc'19        || '&limit=1',20        array[21            ('apiKey', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtdXB0cHBsZnZpaWZyYndtbXR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODAxMDczNzIsImV4cCI6MTk5NTY4MzM3Mn0.z2CN0mvO2No8wSi46Gw59DFGCTJrzM0AQKsu_5k134s')::extensions.http_header22        ],23        null,24        null25    )26) x,27lateral (28    select29        ((row_to_json(x) -> 'content') #>> '{}')::json -> 030) resp(contents);31create extension "supabase-dbdev";32select dbdev.install('supabase-dbdev');3334-- Drop and recreate the extension to ensure a clean installation35drop extension if exists "supabase-dbdev";36create extension "supabase-dbdev";
```

Example 2 (unknown):
```unknown
1select dbdev.install('basejump-supabase_test_helpers');2create extension if not exists "basejump-supabase_test_helpers" version '0.0.6';
```

Example 3 (unknown):
```unknown
1begin;2select plan(1);34-- Verify RLS is enabled on all tables in the public schema5select tests.rls_enabled('public');67select * from finish();8rollback;
```

Example 4 (unknown):
```unknown
1supabase test new 000-setup-tests-hooks
```

---

## Customizing Postgres configs | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/custom-postgres-config

**Contents:**
- Customizing Postgres configs
  - Viewing settings#
- Configurable settings#
  - User-context settings#
  - Superuser settings#
  - CLI configurable settings#
    - CLI supported parameters#
    - Managing Postgres configuration with the CLI#
      - Read Replicas and Custom Config
  - Resetting to default config#

Customizing Postgres configs

Each Supabase project is a pre-configured Postgres cluster. You can override some configuration settings to suit your needs. This is an advanced topic, and we don't recommend touching these settings unless it is necessary.

Customizing Postgres configurations provides advanced control over your database, but inappropriate settings can lead to severe performance degradation or project instability.

To list all Postgres settings and their descriptions, run:

The pg_settings table's context column specifies the requirements for changing a setting. By default, those with a user context can be changed at the role or database level with SQL.

To list all user-context settings, run:

As an example, the statement_timeout setting can be altered:

To verify the change, execute:

Some settings can only be modified by a superuser. Supabase pre-enables the supautils extension, which allows the postgres role to retain certain superuser privileges. It enables modification of the below reserved configurations at the role level:

For example, to enable log_nested_statements for the postgres role, execute:

While many Postgres parameters are configurable directly, some configurations can be changed with the Supabase CLI at the system level.

CLI changes permanently overwrite default settings, so reset all and set to default commands won't revert to the original values.

In order to overwrite the default settings, you must have Owner or Administrator privileges within your organizations.

If a setting you need is not yet configurable, share your use case with us! Let us know what setting you'd like to control, and we'll consider adding support in future updates.

The following parameters are available for overrides:

To update Postgres configurations, use the postgres config command:

By default, the CLI will merge any provided config overrides with any existing ones. The --replace-existing-overrides flag can be used to instead force all existing overrides to be replaced with the ones being provided:

To delete specific configuration overrides, use the postgres-config delete command:

By default, CLI v2 (≥ 2.0.0) checks the parameter’s context and requests the correct action (reload or restart):

To check whether a parameter can be reloaded without a restart, see the Postgres docs.

You can verify whether changes have been applied with the following checks:

You can also pass the --no-restart flag to attempt a reload-only apply. If the parameter cannot be reloaded, the change stays pending until the next restart.

Postgres requires several parameters to be synchronized between the Primary cluster and Read Replicas.

By default, Supabase ensures that this propagation is executed correctly. However, if the --no-restart behavior is used in conjunction with parameters that cannot be reloaded without a restart, the user is responsible for ensuring that both the primaries and the read replicas get restarted in a timely manner to ensure a stable running state. Leaving the configuration updated, but not utilized (via a restart) in such a case can result in read replica failure if the primary, or a read replica, restarts in isolation (e.g. due to an out-of-memory event, or hardware failure).

To reset a setting to its default value at the database level:

For role level configurations, you can run:

**Examples:**

Example 1 (unknown):
```unknown
1select * from pg_settings;
```

Example 2 (unknown):
```unknown
1select * from pg_settings where context = 'user';
```

Example 3 (unknown):
```unknown
1alter database "postgres" set "statement_timeout" TO '60s';
```

Example 4 (unknown):
```unknown
1show "statement_timeout";
```

---

## Using Custom Schemas | Supabase Docs

**URL:** https://supabase.com/docs/guides/api/using-custom-schemas

**Contents:**
- Using Custom Schemas
- Creating custom schemas#
- Exposing custom schemas#

By default, your database has a public schema which is automatically exposed on data APIs.

You can create your own custom schema/s by running the following SQL, substituting myschema with the name you want to use for your schema:

You can expose custom database schemas - to do so you need to follow these steps:

Now you can access these schemas from data APIs:

**Examples:**

Example 1 (unknown):
```unknown
1CREATE SCHEMA myschema;
```

Example 2 (unknown):
```unknown
1GRANT USAGE ON SCHEMA myschema TO anon, authenticated, service_role;2GRANT ALL ON ALL TABLES IN SCHEMA myschema TO anon, authenticated, service_role;3GRANT ALL ON ALL ROUTINES IN SCHEMA myschema TO anon, authenticated, service_role;4GRANT ALL ON ALL SEQUENCES IN SCHEMA myschema TO anon, authenticated, service_role;5ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA myschema GRANT ALL ON TABLES TO anon, authenticated, service_role;6ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA myschema GRANT ALL ON ROUTINES TO anon, authenticated, service_role;7ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA myschema GRANT ALL ON SEQUENCES TO anon, authenticated, service_role;
```

Example 3 (python):
```python
1// Initialize the JS client2import { createClient } from '@supabase/supabase-js'3const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {4  db: { schema: 'myschema' },5})67// Make a request8const { data: todos, error } = await supabase.from('todos').select('*')910// You can also change the target schema on a per-query basis11const { data: todos, error } = await supabase.schema('myschema').from('todos').select('*')
```

---

## Dedicated IPv4 Address for Ingress | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/ipv4-address

**Contents:**
- Dedicated IPv4 Address for Ingress
- Attach an IPv4 address to your database
- Understanding IP addresses#
- When you need the IPv4 add-on:#
- Enabling the IPv4 add-on#
- Read replicas and IPv4 add-on#
- Changes and updates#
- Supabase and IPv6 compatibility#
  - Checking your network IPv6 support#
  - Checking platforms for IPv6 support:#

Dedicated IPv4 Address for Ingress

Attach an IPv4 address to your database

The Supabase IPv4 add-on provides a dedicated IPv4 address for your Postgres database connection. It can be configured in the Add-ons Settings.

The Internet Protocol (IP) addresses devices on the internet. There are two main versions:

IPv4 addresses are guaranteed to be static for ingress traffic. If your database is making outbound connections, the outbound IP address is not static and cannot be guaranteed.

You can enable the IPv4 add-on in your project's add-ons settings.

You can also manage the IPv4 add-on using the Management API:

Note that direct database connections can experience a short amount of downtime when toggling the add-on due to DNS reconfiguration and propagation. Generally, this should be less than a minute.

When using the add-on, each database (including read replicas) receives an IPv4 address. Each replica adds to the total IPv4 cost.

By default, Supabase Postgres use IPv6 addresses. If your system doesn't support IPv6, you have the following options:

You can check if your personal network is IPv6 compatible at https://test-ipv6.com.

The majority of services are IPv6 compatible. However, there are a few prominent ones that only accept IPv4 connections:

Use an IP lookup website or this command (replace <PROJECT_REF>):

The pooler and direct connection strings can be found in the project connect page:

IPv6 unless IPv4 Add-On is enabled

Always uses an IPv4 address

Always uses an IPv4 address

For a detailed breakdown of how charges are calculated, refer to Manage IPv4 usage.

**Examples:**

Example 1 (unknown):
```unknown
1# Get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"3export PROJECT_REF="your-project-ref"45# Get current IPv4 add-on status6curl -X GET "https://api.supabase.com/v1/projects/$PROJECT_REF/billing/addons" \7  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN"89# Enable IPv4 add-on10curl -X POST "https://api.supabase.com/v1/projects/$PROJECT_REF/addons" \11  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \12  -H "Content-Type: application/json" \13  -d '{14    "addon_type": "ipv4"15  }'1617# Disable IPv4 add-on18curl -X DELETE "https://api.supabase.com/v1/projects/$PROJECT_REF/billing/addons/ipv4" \19  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN"
```

Example 2 (unknown):
```unknown
1nslookup db.<PROJECT_REF>.supabase.co
```

Example 3 (unknown):
```unknown
1# Example direct connection string2postgresql://postgres:[YOUR-PASSWORD]@db.ajrbwkcuthywfihaarmflo.supabase.co:5432/postgres
```

Example 4 (unknown):
```unknown
1# Example transaction string2postgresql://postgres.ajrbwkcuthywddfihrmflo:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-database-metadata

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Postgres Triggers | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/triggers

**Contents:**
- Postgres Triggers
- Automatically execute SQL on table events.
- Creating a trigger#
- Trigger functions#
  - Example trigger function#
  - Trigger variables#
- Types of triggers#
  - Trigger before changes are made#
  - Trigger after changes are made#
- Execution frequency#

Automatically execute SQL on table events.

In Postgres, a trigger executes a set of actions automatically on table events such as INSERTs, UPDATEs, DELETEs, or TRUNCATE operations.

Creating triggers involve 2 parts:

An example of a trigger is:

A trigger function is a user-defined Function that Postgres executes when the trigger is fired.

Here is an example that updates salary_log whenever an employee's salary is updated:

Trigger functions have access to several special variables that provide information about the context of the trigger event and the data being modified. In the example above you can see the values inserted into the salary log are old.salary and new.salary - in this case old specifies the previous values and new specifies the updated values.

Here are some of the key variables and options available within trigger functions:

There are two types of trigger, BEFORE and AFTER:

Executes before the triggering event.

Executes after the triggering event.

There are two options available for executing triggers:

You can delete a trigger using the drop trigger command:

If your trigger is inside a restricted schema, you won't be able to drop it due to permission restrictions. In those cases, you can drop the function it depends on instead using the CASCADE clause to automatically remove all triggers that call it:

Make sure you take a backup of the function before removing it in case you're planning to recreate it later.

**Examples:**

Example 1 (unknown):
```unknown
1create trigger "trigger_name"2after insert on "table_name"3for each row4execute function trigger_function();
```

Example 2 (unknown):
```unknown
1-- Example: Update salary_log when salary is updated2create function update_salary_log()3returns trigger4language plpgsql5as $$6begin7  insert into salary_log(employee_id, old_salary, new_salary)8  values (new.id, old.salary, new.salary);9  return new;10end;11$$;1213create trigger salary_update_trigger14after update on employees15for each row16execute function update_salary_log();
```

Example 3 (unknown):
```unknown
1create trigger before_insert_trigger2before insert on orders3for each row4execute function before_insert_function();
```

Example 4 (unknown):
```unknown
1create trigger after_delete_trigger2after delete on customers3for each row4execute function after_delete_function();
```

---

## Drizzle | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/drizzle

**Contents:**
- Drizzle
  - Connecting with Drizzle#
  - Install
  - Create your models
  - Connect

Drizzle ORM is a TypeScript ORM for SQL databases designed with maximum type safety in mind. You can use their ORM to connect to your database.

If you plan on solely using Drizzle instead of the Supabase Data API (PostgREST), you can turn off the latter in the API Settings.

Install Drizzle and related dependencies.

Create a schema.ts file and define your models.

Connect to your database using the Connection Pooler.

From the project Connect panel, copy the URI from the "Shared Pooler" option and save it as the DATABASE_URL environment variable. Remember to replace the password placeholder with your actual database password.

In local SUPABASE_DB_URL require to be adapted to work with Docker resolver

**Examples:**

Example 1 (unknown):
```unknown
1npm i drizzle-orm postgres2npm i -D drizzle-kit
```

Example 2 (python):
```python
1import { pgTable, serial, text, varchar } from "drizzle-orm/pg-core";23export const users = pgTable('users', {4  id: serial('id').primaryKey(),5  fullName: text('full_name'),6  phone: varchar('phone', { length: 256 }),7});
```

Example 3 (python):
```python
1import 'dotenv/config'23import { drizzle } from 'drizzle-orm/postgres-js'4import postgres from 'postgres'56let connectionString = process.env.DATABASE_URL7if (host.includes('postgres:postgres@supabase_db_')) {8  const url = URL.parse(host)!9  url.hostname = url.hostname.split('_')[1]10  connectionString = url.href11}1213// Disable prefetch as it is not supported for "Transaction" pool mode14export const client = postgres(connectionString, { prepare: false })15export const db = drizzle(client);
```

---

## pg_jsonschema: JSON Schema Validation | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_jsonschema

**Contents:**
- pg_jsonschema: JSON Schema Validation
- Enable the extension#
- Functions#
- Usage#
- Resources#

pg_jsonschema: JSON Schema Validation

JSON Schema is a language for annotating and validating JSON documents. pg_jsonschema is a Postgres extension that adds the ability to validate PostgreSQL's built-in json and jsonb data types against JSON Schema documents.

Since pg_jsonschema exposes its utilities as functions, we can execute them with a select statement:

pg_jsonschema is generally used in tandem with a check constraint as a way to constrain the contents of a json/b column to match a JSON Schema.

**Examples:**

Example 1 (unknown):
```unknown
1select2  extensions.json_matches_schema(3    schema := '{"type": "object"}',4    instance := '{}'5  );
```

Example 2 (unknown):
```unknown
1create table customer(2    id serial primary key,3    ...4    metadata json,56    check (7        json_matches_schema(8            '{9                "type": "object",10                "properties": {11                    "tags": {12                        "type": "array",13                        "items": {14                            "type": "string",15                            "maxLength": 1616                        }17                    }18                }19            }',20            metadata21        )22    )23);2425-- Example: Valid Payload26insert into customer(metadata)27values ('{"tags": ["vip", "darkmode-ui"]}');28-- Result:29--   INSERT 0 13031-- Example: Invalid Payload32insert into customer(metadata)33values ('{"tags": [1, 3]}');34-- Result:35--   ERROR:  new row for relation "customer" violates check constraint "customer_metadata_check"36--   DETAIL:  Failing row contains (2, {"tags": [1, 3]}).
```

---

## Connection management | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/connection-management

**Contents:**
- Connection management
- Using your connections resourcefully
- Connections#
  - Configuring Supavisor's pool size#
- Monitoring connections#
  - Capturing historical usage#
    - Dashboard monitoring charts#
    - Grafana Dashboard#
  - Observing live connections#

Connection management

Using your connections resourcefully

Every Compute Add-On has a pre-configured direct connection count and Supavisor pool size. This guide discusses ways to observe and manage them resourcefully.

You can change how many database connections Supavisor can manage by altering the pool size in the "Connection pooling configuration" section of the Database Settings:

The general rule is that if you are heavily using the PostgREST database API, you should be conscientious about raising your pool size past 40%. Otherwise, you can commit 80% to the pool. This leaves adequate room for the Authentication server and other utilities.

These numbers are generalizations and depends on other Supabase products that you use and the extent of their usage. The actual values depend on your concurrent peak connection usage. For instance, if you were only using 80 connections in a week period and your database max connections is set to 500, then realistically you could allocate the difference of 420 (minus a reasonable buffer) to service more demand.

For Teams and Enterprise plans, Supabase provides Advanced Telemetry charts directly within the Dashboard. The Database client connections chart displays historical connection data broken down by connection type:

This chart helps you monitor connection pool usage, identify connection leaks, and plan capacity. It also shows a reference line for your compute size's maximum connection limit.

For more details on using these monitoring charts, see the Reports guide.

Supabase offers a Grafana Dashboard that records and visualizes over 200 project metrics, including connections. For setup instructions, check the metrics docs.

Its "Client Connections" graph displays connections for both Supavisor and Postgres

pg_stat_activity is a special view that keeps track of processes being run by your database, including live connections. It's particularly useful for determining if idle clients are hogging connection slots.

Query to get all live connections:

Interpreting the query:

The username can be used to identify the source:

**Examples:**

Example 1 (unknown):
```unknown
1SELECT2  pg_stat_activity.pid as connection_id,3  ssl,4  datname as database,5  usename as connected_role,6  application_name,7  client_addr as IP,8  query,9  query_start,10  state,11  backend_start12FROM pg_stat_ssl13JOIN pg_stat_activity14ON pg_stat_ssl.pid = pg_stat_activity.pid;
```

---

## Working With Arrays | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/arrays

**Contents:**
- Working With Arrays
- Create a table with an array column#
- Insert a record with an array value#
- View the results#
- Query array data#
- Resources#

Postgres supports flexible array types. These arrays are also supported in the Supabase Dashboard and in the JavaScript API.

Create a test table with a text array (an array of strings):

Postgres uses 1-based indexing (e.g., textarray[1] is the first item in the array).

To select the first item from the array and get the total length of the array:

**Examples:**

Example 1 (unknown):
```unknown
1| id  | textarray               |2| --- | ----------------------- |3| 1   | ["Harry","Larry","Moe"] |
```

Example 2 (unknown):
```unknown
1SELECT textarray[1], array_length(textarray, 1) FROM arraytest;
```

Example 3 (unknown):
```unknown
1| textarray | array_length |2| --------- | ------------ |3| Harry     | 3            |
```

---

## Migrate from MSSQL to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/mssql

**Contents:**
- Migrate from MSSQL to Supabase
- Migrate your Microsoft SQL Server database to Supabase.
- Retrieve your MSSQL database credentials#
- Retrieve your Supabase host #
- Migrate the database#
- Enterprise#

Migrate from MSSQL to Supabase

Migrate your Microsoft SQL Server database to Supabase.

This guide aims to demonstrate the process of transferring your Microsoft SQL Server database to Supabase's Postgres database. Supabase is a powerful and open-source platform offering a wide range of backend features, including a Postgres database, authentication, instant APIs, edge functions, real-time subscriptions, and storage. Migrating your MSSQL database to Supabase's Postgres enables you to leverage Postgres's capabilities and access all the features you need for your project.

Before you begin the migration, you need to collect essential information about your MSSQL database. Follow these steps:

If you're new to Supabase, create a project. Make a note of your password, you will need this later. If you forget it, you can reset it here.

On your project dashboard, click Connect

Under the Session pooler, click on the View parameters under the connect string. Note your Host ($SUPABASE_HOST).

The fastest way to migrate your database is with the Supabase migration tool on Google Colab.

Alternatively, you can use pgloader, a flexible and powerful data migration tool that supports a wide range of source database engines, including MySQL and MS SQL, and migrates the data to a Postgres database. For databases using the Postgres engine, we recommend using the pg_dump and psql command line tools, which are included in a full Postgres installation.

If you're planning to migrate a database larger than 6 GB, we recommend upgrading to at least a Large compute add-on. This will ensure you have the necessary resources to handle the migration efficiently.

We strongly advise you to pre-provision the disk space you will need for your migration. On paid projects, you can do this by navigating to the Compute and Disk Settings page. For more information on disk scaling and disk limits, check out our disk settings documentation.

Contact us if you need more help migrating your project.

---

## Storing Vectors | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/vector/storing-vectors

**Contents:**
- Storing Vectors
- Insert and update vector embeddings with metadata using the JavaScript SDK or Postgres.
      - This feature is in alpha
- Basic vector insertion#
- Storing vectors from Embeddings API#
- Updating vectors#
- Deleting vectors#
- Metadata best practices#
  - Metadata field guidelines#
- Batch processing large datasets#

Insert and update vector embeddings with metadata using the JavaScript SDK or Postgres.

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

Once you've created a bucket and index, you can start storing vectors. Vectors can include optional metadata for filtering and enrichment during queries.

Generate embeddings using an LLM API and store them directly:

Metadata makes vectors more useful by enabling filtering and context:

For storing large numbers of vectors efficiently:

Always use batch operations for better performance:

Keep metadata concise:

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabase = createClient('https://your-project.supabase.co', 'your-service-key')45// Get bucket and index6const bucket = supabase.storage.vectors.from('embeddings')7const index = bucket.index('documents-openai')89// Insert vectors10const { error } = await index.putVectors({11  vectors: [12    {13      key: 'doc-1',14      data: {15        float32: [0.1, 0.2, 0.3 /* ... rest of embedding ... */],16      },17      metadata: {18        title: 'Getting Started with Vector Buckets',19        source: 'documentation',20      },21    },22    {23      key: 'doc-2',24      data: {25        float32: [0.4, 0.5, 0.6 /* ... rest of embedding ... */],26      },27      metadata: {28        title: 'Advanced Vector Search',29        source: 'blog',30      },31    },32  ],33})3435if (error) {36  console.error('Error storing vectors:', error)37} else {38  console.log('✓ Vectors stored successfully')39}
```

Example 2 (python):
```python
1import { createClient } from '@supabase/supabase-js'2import OpenAI from 'openai'34const supabase = createClient('https://your-project.supabase.co', 'your-service-key')56const openai = new OpenAI({7  apiKey: process.env.OPENAI_API_KEY,8})910// Documents to embed and store11const documents = [12  { id: '1', title: 'How to Train Your AI', content: 'Guide for training models...' },13  { id: '2', title: 'Vector Search Best Practices', content: 'Tips for semantic search...' },14  {15    id: '3',16    title: 'Building RAG Systems',17    content: 'Implementing retrieval-augmented generation...',18  },19]2021// Generate embeddings22const embeddings = await openai.embeddings.create({23  model: 'text-embedding-3-small',24  input: documents.map((doc) => doc.content),25})2627// Prepare vectors for storage28const vectors = documents.map((doc, index) => ({29  key: doc.id,30  data: {31    float32: embeddings.data[index].embedding,32  },33  metadata: {34    title: doc.title,35    source: 'knowledge_base',36    created_at: new Date().toISOString(),37  },38}))3940// Store vectors in batches (max 500 per request)41const bucket = supabase.storage.vectors.from('embeddings')42const vectorIndex = bucket.index('documents-openai')4344for (let i = 0; i < vectors.length; i += 500) {45  const batch = vectors.slice(i, i + 500)46  const { error } = await vectorIndex.putVectors({ vectors: batch })4748  if (error) {49    console.error(`Error storing batch ${i / 500 + 1}:`, error)50  } else {51    console.log(`✓ Stored batch ${i / 500 + 1} (${batch.length} vectors)`)52  }53}
```

Example 3 (javascript):
```javascript
1const index = bucket.index('documents-openai')23// Update a vector (same key)4const { error } = await index.putVectors({5  vectors: [6    {7      key: 'doc-1',8      data: {9        float32: [0.15, 0.25, 0.35 /* ... updated embedding ... */],10      },11      metadata: {12        title: 'Getting Started with Vector Buckets - Updated',13        updated_at: new Date().toISOString(),14      },15    },16  ],17})1819if (!error) {20  console.log('✓ Vector updated successfully')21}
```

Example 4 (javascript):
```javascript
1const index = bucket.index('documents-openai')23// Delete specific vectors4const { error } = await index.deleteVectors({5  keys: ['doc-1', 'doc-2'],6})78if (!error) {9  console.log('✓ Vectors deleted successfully')10}
```

---

## Database configuration | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/configuration

**Contents:**
- Database configuration
- Updating the default configuration for your Postgres database.
- Timeouts#
- Statement optimization#
- Managing timezones#
  - Change timezone#
  - Full list of timezones#
  - Search for a specific timezone#

Database configuration

Updating the default configuration for your Postgres database.

Postgres provides a set of sensible defaults for you database size. In some cases, these defaults can be updated. We do not recommend changing these defaults unless you know what you're doing.

See the Timeouts section.

All Supabase projects come with the pg_stat_statements extension installed, which tracks planning and execution statistics for all statements executed against it. These statistics can be used in order to diagnose the performance of your project.

This data can further be used in conjunction with the explain functionality of Postgres to optimize your usage.

Every Supabase database is set to UTC timezone by default. We strongly recommend keeping it this way, even if your users are in a different location. This is because it makes it much easier to calculate differences between timezones if you adopt the mental model that everything in your database is in UTC time.

Get a full list of timezones supported by your database. This will return the following columns:

Use ilike (case insensitive search) to find specific timezones.

**Examples:**

Example 1 (unknown):
```unknown
1alter database postgres2set timezone to 'America/New_York';
```

Example 2 (unknown):
```unknown
1select name, abbrev, utc_offset, is_dst2from pg_timezone_names()3order by name;
```

Example 3 (unknown):
```unknown
1select *2from pg_timezone_names()3where name ilike '%york%';
```

---

## Cron | Supabase Docs

**URL:** https://supabase.com/docs/guides/cron

**Contents:**
- Cron
- Schedule Recurring Jobs with Cron Syntax in Postgres
- How does Cron work?#
- Resources#

Schedule Recurring Jobs with Cron Syntax in Postgres

Supabase Cron is a Postgres Module that simplifies scheduling recurring Jobs with cron syntax and monitoring Job runs inside Postgres.

Cron Jobs can be created via SQL or the Integrations -> Cron interface inside the Dashboard, and can run anywhere from every second to once a year depending on your use case.

Every Job can run SQL snippets or database functions with zero network latency or make an HTTP request, such as invoking a Supabase Edge Function, with ease.

For best performance, we recommend no more than 8 Jobs run concurrently. Each Job should run no more than 10 minutes.

Under the hood, Supabase Cron uses the pg_cron Postgres database extension which is the scheduling and execution engine for your Jobs.

The extension creates a cron schema in your database and all Jobs are stored on the cron.job table. Every Job's run and its status is recorded on the cron.job_run_details table.

The Supabase Dashboard provides an interface for you to schedule Jobs and monitor Job runs. You can also do the same with SQL.

---

## Manual Replication FAQ | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/replication/manual-replication-faq

**Contents:**
- Manual Replication FAQ
- Common questions and considerations when setting up manual replication.
- Which connection string should be used?#
- The tool in use does not support IPv6#
- What is XMIN and should it be used?#
- Can replication be configured in the Dashboard?#
- How to configure database settings for replication?#
- What are some important configuration options?#

Manual Replication FAQ

Common questions and considerations when setting up manual replication.

Always use the direct connection string for logical replication.

Connections through a pooler, such as Supavisor, will not work.

You can enable the IPv4 add-on for your project.

Xmin is a different form of replication from logical replication and should only be used if logical replication is not available for your database (i.e. older versions of Postgres).

Xmin performs replication by checking the xmin system column and determining if that row has already been synchronized.

It does not capture deletion of data and is not recommended, particularly for larger databases.

You can view publications in the Dashboard but all steps to configure replication must be done using the SQL Editor or a CLI tool of your choice.

Using the Supabase CLI, you can configure database settings to optimize them for your replication needs. These values can vary depending on your database size and activity.

Some of the more important options to be aware of are:

These settings help ensure your replication slots don't run out of space and that replicas can reconnect without requiring a full re-sync.

---

## Replication Setup | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/replication/replication-setup

**Contents:**
- Replication Setup
- Configure publications and destinations for replication.
      - Private Alpha
- Setup overview#
  - Step 1: Create a Postgres publication#
    - Creating a publication#
      - Publication for specific tables
      - Publication for all tables in a schema
      - Publication for all tables
    - Advanced publication options#

Configure publications and destinations for replication.

Replication is currently in private alpha. Access is limited and features may change.

Replication uses Postgres logical replication to stream changes from your database. Powered by Supabase ETL, an open source tool built for Postgres logical replication, it provides a managed interface through the Dashboard to configure and monitor replication pipelines.

Replication requires two main components: a Postgres publication (defines what to replicate) and a destination (where data is sent). Follow these steps to set up your replication pipeline.

If you already have a Postgres publication set up, you can skip to Step 2: Enable replication.

A Postgres publication defines which tables and change types will be replicated from your database. You create publications using SQL.

The following SQL examples assume you have users and orders tables in your database.

This publication will track all changes (INSERT, UPDATE, DELETE, TRUNCATE) for both the users and orders tables.

This will track changes for all existing and future tables in the public schema.

This will track changes for all tables in your database.

You can replicate only a subset of columns from a table:

This will only replicate the id, email, and created_at columns from the users table.

You can filter which rows to replicate using a WHERE clause:

After creating a publication via SQL, you can view it in the Supabase Dashboard:

Before adding destinations, you need to enable replication for your project:

Once replication is enabled and you have a Postgres publication, you can add a destination. The destination is where your replicated data will be stored, while the pipeline is the active Postgres replication process that continuously streams changes from your database to that destination.

Follow these steps to configure your destination. The specific configuration depends on which destination type you choose. Both Analytics Buckets and BigQuery destinations are supported, though availability varies based on the planned roll-out strategy.

Analytics Buckets are specialized storage buckets in Supabase Storage designed for analytical workloads. They provide S3-compatible storage and use the Apache Iceberg open table format, making your data accessible via standard tools like DuckDB, Spark, and other analytics platforms.

When you replicate to Analytics Buckets, your database changes are automatically written in Iceberg format, creating tables in object storage that you can query for analytics.

First, create an analytics bucket to store your replicated data:

Navigate to Storage → Analytics in your Supabase Dashboard

Fill in the bucket details:

Copy the credentials displayed after bucket creation. You'll need these in the next steps:

Navigate to Database → replication in your Supabase Dashboard

Click Add destination

Configure the general settings:

Configure Analytics Buckets settings:

Configure Advanced Settings (optional):

Click Create and start to begin replication

Your replication pipeline will now start copying data from your database to the analytics bucket in Iceberg format.

Once configured, replication to Analytics Buckets:

Replicated tables use a changelog structure:

After creating a destination, the replication pipeline will start and appear in the destinations list. You can monitor the pipeline's status and performance from the Dashboard.

For comprehensive monitoring instructions including pipeline states, metrics, and logs, see the Replication Monitoring guide.

You can manage your pipeline from the destinations list using the actions menu.

If you need to modify which tables are replicated after your replication pipeline is already running, follow these steps:

If your Postgres publication uses FOR ALL TABLES or FOR TABLES IN SCHEMA, new tables in that scope are automatically included in the publication. However, you still must restart the replication pipeline for the changes to take effect.

Add the table to your publication using SQL:

Restart the replication pipeline using the actions menu (see Managing your pipeline) for the changes to take effect.

Remove the table from your Postgres publication using SQL:

Restart the replication pipeline using the actions menu (see Managing your pipeline) for the changes to take effect.

Deleted tables are automatically recreated by the pipeline. To permanently delete a table, pause the pipeline first or remove it from the publication before deleting. See the FAQ for details.

Once configured, replication:

Changes are sent in batches to optimize performance and reduce costs. The batch size and timing can be adjusted using the advanced settings. The replication pipeline currently performs data extraction and loading only, without transformation - your data is replicated as-is to the destination.

If you encounter issues during setup:

For more troubleshooting help, see the Replication FAQ.

Replication has the following limitations:

Destination-specific limitations (such as Iceberg's append-only log format or BigQuery's row size limits) are detailed in each destination tab in Step 3 above.

Replication is actively being developed. Planned improvements include:

There are no public timelines for these features, but they represent the roadmap for making replication more robust and flexible.

**Examples:**

Example 1 (unknown):
```unknown
1-- Create publication for both tables2create publication pub_users_orders3for table users, orders;
```

Example 2 (unknown):
```unknown
1-- Create a publication for all tables in the public schema2create publication pub_all_public for tables in schema public;
```

Example 3 (unknown):
```unknown
1-- Create a publication for all tables2create publication pub_all_tables for all tables;
```

Example 4 (unknown):
```unknown
1-- Replicate only specific columns from the users table2create publication pub_users_subset3for table users (id, email, created_at);
```

---

## Roboflow | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/integrations/roboflow

**Contents:**
- Roboflow
- Learn how to integrate Supabase with Roboflow, a tool for running fine-tuned and foundation vision models.
- Project setup#
- Save computer vision predictions#
  - Preparation: Set up a model#
  - Step 1: Install and start Roboflow Inference#
  - Step 2: Run inference on an image#
  - Step 3: Save results in Supabase#
- Calculate and save CLIP embeddings#
  - Step 1: Install and start Roboflow Inference#

Learn how to integrate Supabase with Roboflow, a tool for running fine-tuned and foundation vision models.

In this guide, we will walk through two examples of using Roboflow Inference to run fine-tuned and foundation models. We will run inference and save predictions using an object detection model and CLIP.

Let's create a new Postgres database. This is as simple as starting a new Project in Supabase:

Your database will be available in less than a minute.

Finding your credentials:

You can find your project credentials on the dashboard:

Once you have a trained vision model, you need to create business logic for your application. In many cases, you want to save inference results to a file.

The steps below show you how to run a vision model locally and save predictions to Supabase.

Before you begin, you will need an object detection model trained on your data.

You can train a model on Roboflow, leveraging end-to-end tools from data management and annotation to deployment, or upload custom model weights for deployment.

All models have an infinitely scalable API through which you can query your model, and can be run locally.

For this guide, we will use a demo rock, paper, scissors model.

You will deploy our model locally using Roboflow Inference, a computer vision inference server.

To install and start Roboflow Inference, first install Docker on your machine.

An inference server will be available at http://localhost:9001.

You can run inference on images and videos. Let's run inference on an image.

Create a new Python file and add the following code:

When you run the code above, a list of predictions will be printed to the console:

To save results in Supabase, add the following code to your script:

You can then query your predictions using the following code:

Here is an example result:

You can use the Supabase vector database functionality to store and query CLIP embeddings.

Roboflow Inference provides a HTTP interface through which you can calculate image and text embeddings using CLIP.

See Step #1: Install and Start Roboflow Inference above to install and start Roboflow Inference.

Create a new Python file and add the following code:

This code will calculate CLIP embeddings for each image in the directory and print the results to the console.

You can also calculate CLIP embeddings in the cloud by setting SERVER_URL to https://infer.roboflow.com.

You can store your image embeddings in Supabase using the Supabase vecs Python package:

Next, add the following code to your script to create an index:

Replace DB_CONNECTION with the authentication information for your database. You can retrieve this from the Supabase dashboard in Project Settings > Database Settings.

You can then query your embeddings using the following code:

**Examples:**

Example 1 (unknown):
```unknown
1pip install inference inference-cli inference-sdk && inference server start
```

Example 2 (python):
```python
1from inference_sdk import InferenceHTTPClient23image = "example.jpg"4MODEL_ID = "rock-paper-scissors-sxsw/11"56client = InferenceHTTPClient(7    api_url="http://localhost:9001",8    api_key="ROBOFLOW_API_KEY"9)10with client.use_model(MODEL_ID):11    predictions = client.infer(image)1213print(predictions)
```

Example 3 (unknown):
```unknown
1{'time': 0.05402109300121083, 'image': {'width': 640, 'height': 480}, 'predictions': [{'x': 312.5, 'y': 392.0, 'width': 255.0, 'height': 110.0, 'confidence': 0.8620790839195251, 'class': 'Paper', 'class_id': 0}]}
```

Example 4 (python):
```python
1import os2from supabase import create_client, Client34url: str = os.environ.get("SUPABASE_URL")5key: str = os.environ.get("SUPABASE_KEY")6supabase: Client = create_client(url, key)78result = supabase.table('predictions') \9    .insert({"filename": image, "predictions": predictions}) \10    .execute()
```

---

## Migrate from Neon to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/neon

**Contents:**
- Migrate from Neon to Supabase
- Migrate your existing Neon database to Supabase.
- Retrieve your Neon database credentials #
- Set your OLD_DB_URL environment variable#
- Retrieve your Supabase connection string #
- Set your NEW_DB_URL environment variable#
- Migrate the database#
- Enterprise#

Migrate from Neon to Supabase

Migrate your existing Neon database to Supabase.

This guide demonstrates how to migrate your Neon database to Supabase to get the most out of Postgres while gaining access to all the features you need to build a project.

Set the OLD_DB_URL environment variable at the command line using your Neon database credentials from the clipboard.

If you're new to Supabase, create a project. Make a note of your password, you will need this later. If you forget it, you can reset it here.

On your project dashboard, click Connect

Under the Session pooler, click the Copy button to the right of your connection string to copy it to the clipboard.

Set the NEW_DB_URL environment variable at the command line using your Supabase connection string. You will need to replace [YOUR-PASSWORD] with your actual database password.

You will need the pg_dump and psql command line tools, which are included in a full Postgres installation.

Export your database to a file in console

Use pg_dump with your Postgres credentials to export your database to a file (e.g., dump.sql).

Import the database to your Supabase project

Use psql to import the Postgres database file to your Supabase project.

Run pg_dump --help for a full list of options.

If you're planning to migrate a database larger than 6 GB, we recommend upgrading to at least a Large compute add-on. This will ensure you have the necessary resources to handle the migration efficiently.

We strongly advise you to pre-provision the disk space you will need for your migration. On paid projects, you can do this by navigating to the Compute and Disk Settings page. For more information on disk scaling and disk limits, check out our disk settings documentation.

Contact us if you need more help migrating your project.

**Examples:**

Example 1 (unknown):
```unknown
1postgresql://neondb_owner:xxxxxxxxxxxxxxx-random-word-yyyyyyyy.us-west-2.aws.neon.tech/neondb?sslmode=require
```

Example 2 (unknown):
```unknown
1export OLD_DB_URL="postgresql://neondb_owner:xxxxxxxxxxxxxxx-random-word-yyyyyyyy.us-west-2.aws.neon.tech/neondb?sslmode=require"
```

Example 3 (unknown):
```unknown
1export NEW_DB_URL="postgresql://postgres.xxxxxxxxxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:5432/postgres"
```

Example 4 (unknown):
```unknown
1pg_dump "$OLD_DB_URL" \2  --clean \3  --if-exists \4  --quote-all-identifiers \5  --no-owner \6  --no-privileges \7  > dump.sql
```

---

## Flutter: Call a Postgres function | Supabase Docs

**URL:** https://supabase.com/docs/reference/dart/rpc

---

## pg_stat_statements: Query Performance Monitoring | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_stat_statements

**Contents:**
- pg_stat_statements: Query Performance Monitoring
- Enable the extension#
- Inspecting activity#
- Resources#

pg_stat_statements: Query Performance Monitoring

pg_stat_statements is a database extension that exposes a view, of the same name, to track statistics about SQL statements executed on the database. The following table shows some of the available statistics and metadata:

A full list of statistics is available in the pg_stat_statements docs.

For more information on query optimization, check out the query performance guide.

A common use for pg_stat_statements is to track down expensive or slow queries. The pg_stat_statements view contains a row for each executed query with statistics inlined. For example, you can leverage the statistics to identify frequently executed and slow queries against a given table.

From the results, we can make an informed decision about which queries to optimize or index.

**Examples:**

Example 1 (unknown):
```unknown
1select2	calls,3	mean_exec_time,4	max_exec_time,5	total_exec_time,6	stddev_exec_time,7	query8from9	pg_stat_statements10where11    calls > 50                   -- at least 50 calls12    and mean_exec_time > 2.0     -- averaging at least 2ms/call13    and total_exec_time > 60000  -- at least one minute total server time spent14    and query ilike '%user_in_organization%' -- filter to queries that touch the user_in_organization table15order by16	calls desc
```

---

## Querying Vectors | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/vector/querying-vectors

**Contents:**
- Querying Vectors
- Perform similarity search and retrieve vectors using JavaScript SDK or PostgreSQL.
      - This feature is in alpha
      - Comparison to pgvector
- Basic similarity search#
- Semantic search#
- Filtered similarity search#
- Retrieving specific vectors#
- Listing vectors#
- Hybrid search: Vectors + relational data#

Perform similarity search and retrieve vectors using JavaScript SDK or PostgreSQL.

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

Vector similarity search finds vectors most similar to a query vector using distance metrics. You can query vectors using the JavaScript SDK or directly from Postgres using SQL.

Vector buckets and any Foreign Data Wrappers (FDW) they use only support one similarity search algorithm, the <===> distance operator.

Find documents similar to a query by embedding the query text:

Combine similarity search with SQL filtering and joins:

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabase = createClient('https://your-project.supabase.co', 'your-service-key')45const index = supabase.storage.vectors.from('embeddings').index('documents-openai')67// Query with a vector embedding8const { data, error } = await index.queryVectors({9  queryVector: {10    float32: [0.1, 0.2, 0.3 /* ... embedding of 1536 dimensions ... */],11  },12  topK: 5,13  returnDistance: true,14  returnMetadata: true,15})1617if (error) {18  console.error('Query failed:', error)19} else {20  // Results are ranked by similarity (lowest distance = most similar)21  data.vectors.forEach((result, rank) => {22    console.log(`${rank + 1}. ${result.metadata?.title}`)23    console.log(`   Similarity score: ${result.distance.toFixed(4)}`)24  })25}
```

Example 2 (python):
```python
1import { createClient } from '@supabase/supabase-js'2import OpenAI from 'openai'34const supabase = createClient(...)5const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })67async function semanticSearch(query, topK = 5) {8  // Embed the query9  const queryEmbedding = await openai.embeddings.create({10    model: 'text-embedding-3-small',11    input: query12  })1314  const queryVector = queryEmbedding.data[0].embedding1516  // Search for similar vectors17  const { data, error } = await supabase.storage.vectors18    .from('embeddings')19    .index('documents-openai')20    .queryVectors({21      queryVector: { float32: queryVector },22      topK,23      returnDistance: true,24      returnMetadata: true25    })2627  if (error) {28    throw error29  }3031  return data.vectors.map((result) => ({32    id: result.key,33    title: result.metadata?.title,34    similarity: 1 - result.distance, // Convert distance to similarity (0-1)35    metadata: result.metadata36  }))37}3839// Usage40const results = await semanticSearch('How do I use vector search?')41results.forEach((result) => {42  console.log(`${result.title} (${(result.similarity * 100).toFixed(1)}% similar)`)43})
```

Example 3 (javascript):
```javascript
1const index = supabase.storage.vectors2  .from('embeddings')3  .index('documents-openai')45// Search with metadata filter6const { data } = await index.queryVectors({7  queryVector: { float32: [...embedding...] },8  topK: 10,9  filter: {10    // Filter by metadata fields11    category: 'electronics',12    in_stock: true,13    price: { $lte: 500 } // Less than or equal to 50014  },15  returnDistance: true,16  returnMetadata: true17})
```

Example 4 (javascript):
```javascript
1const index = supabase.storage.vectors.from('embeddings').index('documents-openai')23const { data, error } = await index.getVectors({4  keys: ['doc-1', 'doc-2', 'doc-3'],5  returnData: true,6  returnMetadata: true,7})89if (!error) {10  data.vectors.forEach((vector) => {11    console.log(`${vector.key}: ${vector.metadata?.title}`)12  })13}
```

---

## Creating Buckets | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/buckets/creating-buckets

**Contents:**
- Creating Buckets
- Restricting uploads#

You can create a bucket using the Supabase Dashboard. Since storage is interoperable with your Postgres database, you can also use SQL or our client libraries. Here we create a bucket called "avatars":

When creating a bucket you can add additional configurations to restrict the type or size of files you want this bucket to contain.

For example, imagine you want to allow your users to upload only images to the avatars bucket and the size must not be greater than 1MB. You can achieve the following by providing allowedMimeTypes and maxFileSize:

If an upload request doesn't meet the above restrictions it will be rejected. See File Limits for more information.

**Examples:**

Example 1 (javascript):
```javascript
1// Use the JS library to create a bucket.23const { data, error } = await supabase.storage.createBucket('avatars', {4  public: true, // default: false5})
```

Example 2 (javascript):
```javascript
1// Use the JS library to create a bucket.23const { data, error } = await supabase.storage.createBucket('avatars', {4  public: true,5  allowedMimeTypes: ['image/*'],6  fileSizeLimit: '1MB',7})
```

---

## DuckDB | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/examples/duckdb

**Contents:**
- DuckDB
      - This feature is in alpha
- Installation#
- Connecting to Analytics buckets#
- Key features with DuckDB#
  - Efficient data exploration#
  - Converting to Pandas#
  - Exporting results#
- Best practices#
- Next steps#

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

DuckDB is a high-performance SQL database system optimized for analytical workloads. It can directly query Iceberg tables stored in your analytics buckets, making it ideal for data exploration and complex analytical queries.

Install DuckDB and the Iceberg extension:

Here's a complete example of connecting to your Supabase analytics bucket and querying Iceberg tables:

DuckDB's lazy evaluation means it only scans the data you need:

Convert results to Pandas DataFrames for further analysis:

Save your analytical results to various formats:

**Examples:**

Example 1 (unknown):
```unknown
1pip install duckdb duckdb-iceberg
```

Example 2 (unknown):
```unknown
1import duckdb2import os34# Configuration5PROJECT_REF = "your-project-ref"6WAREHOUSE = "your-analytics-bucket-name"7SERVICE_KEY = "your-service-key"89# S3 credentials10S3_ACCESS_KEY = "your-access-key"11S3_SECRET_KEY = "your-secret-key"12S3_REGION = "us-east-1"1314# Construct endpoints15S3_ENDPOINT = f"https://{PROJECT_REF}.supabase.co/storage/v1/s3"16CATALOG_URI = f"https://{PROJECT_REF}.supabase.co/storage/v1/iceberg"1718# Initialize DuckDB connection19conn = duckdb.connect(":memory:")2021# Install and load the Iceberg extension22conn.install_extension("iceberg")23conn.load_extension("iceberg")2425# Configure Iceberg catalog with Supabase credentials26conn.execute(f"""27    CREATE SECRET (28        TYPE S3,29        KEY_ID '{S3_ACCESS_KEY}',30        SECRET '{S3_SECRET_KEY}',31        REGION '{S3_REGION}',32        ENDPOINT '{S3_ENDPOINT}',33        URL_STYLE 'virtual'34    );35""")3637# Configure the REST catalog38conn.execute(f"""39    ATTACH 'iceberg://{CATALOG_URI}' AS iceberg_catalog40    (41        TYPE ICEBERG_REST,42        WAREHOUSE '{WAREHOUSE}',43        TOKEN '{SERVICE_KEY}'44    );45""")4647# Query your Iceberg tables48result = conn.execute("""49    SELECT *50    FROM iceberg_catalog.default.events51    LIMIT 1052""").fetchall()5354for row in result:55    print(row)5657# Complex aggregation example58analytics = conn.execute("""59    SELECT60        event_name,61        COUNT(*) as event_count,62        COUNT(DISTINCT user_id) as unique_users63    FROM iceberg_catalog.default.events64    GROUP BY event_name65    ORDER BY event_count DESC66""").fetchdf()6768print(analytics)
```

Example 3 (unknown):
```unknown
1# This only reads the columns you select2events = conn.execute("""3    SELECT event_id, event_name, event_timestamp4    FROM iceberg_catalog.default.events5    WHERE event_timestamp > NOW() - INTERVAL '7 days'6""").fetchdf()
```

Example 4 (unknown):
```unknown
1df = conn.execute("""2    SELECT *3    FROM iceberg_catalog.default.events4""").fetchdf()56# Use pandas for visualization or further processing7print(df.describe())
```

---

## PGAudit: Postgres Auditing | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgaudit

**Contents:**
- PGAudit: Postgres Auditing
- Enable the extension#
- Configure the extension#
  - Session mode categories#
  - Session logging#
  - User logging#
  - Global logging#
  - Object logging#
- Interpreting Audit Logs#
- Finding and filtering audit logs#

PGAudit: Postgres Auditing

PGAudit extends Postgres's built-in logging abilities. It can be used to selectively track activities within your database.

PGAudit can be configured with different levels of precision.

PGAudit logging precision:

Although Session, User, and Global modes differ in their precision, they're all considered variants of Session Mode and are configured with the same input categories.

These modes can monitor predefined categories of database operations:

Below is a limited example of how to assign PGAudit to monitor specific categories.

When you are connecting in a session environment, such as a psql connection, you can configure PGAudit to record events initiated within the session.

The Dashboard is a transactional environment and won't sustain a session.

Inside a session, by default, PGAudit will log nothing:

In the session, you can set the pgaudit.log variable to record events:

There are some cases where you may want to monitor a database user's actions. For instance, let's say you connected your database to Zapier and created a custom role for it to use:

You may want to log all actions initiated by zapier, which can be done with the following command:

To remove the settings, execute the following code:

Use global logging cautiously. It can generate many logs and make it difficult to find important events. Consider limiting the scope of what is logged by using session, user, or object logging where possible.

The below SQL configures PGAudit to record all events associated with the postgres role. Since it has extensive privileges, this effectively monitors all database activity.

To check if the postgres role is auditing, execute the following command:

To remove the settings, execute the following code:

To fine-tune what object events PGAudit will record, you must create a custom database role with limited permissions:

No other Postgres user can assume or login via this role. It solely exists to securely define what PGAudit will record.

Once the role is created, you can direct PGAudit to log by assigning it to the pgaudit.role variable:

You can then assign the role to monitor only approved object events, such as select statements that include a specific table:

With this privilege granted, PGAudit will record all select statements that reference the random_table, regardless of who or what actually initiated the event. All assignable privileges can be viewed in the Postgres documentation.

If you would no longer like to use object logging, you will need to unassign the pgaudit.role variable:

PGAudit was designed for storing logs as CSV files with the following headers:

Referenced from the PGAudit official docs

A log made from the following create statement:

Generates the following log in the Dashboard's Postgres Logs:

Logs generated by PGAudit can be found in Postgres Logs. To find a specific log, you can use the log explorer. Below is a basic example to extract logs referencing CREATE TABLE events

API requests are already recorded in the API Edge Network logs.

To monitor all writes initiated by the PostgREST API roles:

In the worst case scenario, where a privileged roles' password is exposed, you can use PGAudit to monitor if the auth.users table was targeted. It should be stated that API requests are already monitored in the API Edge Network and this is more about providing greater clarity about what is happening at the database level.

Logging auth.user should be done in Object Mode and requires a custom role:

With the above code, any query involving reading or deleting from the auth.users table will be logged.

PGAudit, if not configured mindfully, can log all database events, including background tasks. This can generate an undesirably large amount of logs in a few hours.

The first step to solve this problem is to identify which database users PGAudit is observing:

To prevent PGAudit from monitoring the problematic roles, you'll want to change their pgaudit.log values to none and pgaudit.role values to empty quotes ''

Technically yes, but it is not the best approach. It is better to check out our function debugging guide instead.

In the Logs Dashboard you can download logs as CSVs.

By default, PGAudit records queries, but not the returned rows. You can modify this behavior with the pgaudit.log_rows variable:

You should not do this unless you are absolutely certain it is necessary for your use case. It can expose sensitive values to your logs that ideally should not be preserved. Furthermore, if done in excess, it can noticeably reduce database performance.

We don't currently support configuring pgaudit.log_parameter because it may log secrets in encrypted columns if you are using pgsodium orVault.

You can upvote this feature request with your use-case if you'd like this restriction lifted.

PGAudit allows settings to be applied to 3 different database scopes:

Supabase limits full privileges for file system and database variables, meaning PGAudit modifications can only occur at the role level. Assigning PGAudit to the postgres role grants it nearly complete visibility into the database, making role-level adjustments a practical alternative to configuring at the database or system level.

PGAudit's official documentation focuses on system and database level configs, but its docs officially supports role level configs, too.

**Examples:**

Example 1 (unknown):
```unknown
1-- log all CREATE, ALTER, and DROP events2... pgaudit.log = 'ddl';34-- log all CREATE, ALTER, DROP, and SELECT events5... pgaudit.log = 'read, ddl';67-- log nothing8... pgaudit.log = 'none';
```

Example 2 (unknown):
```unknown
1-- returns 'none'2show pgaudit.log;
```

Example 3 (unknown):
```unknown
1-- log CREATE, ALTER, and DROP events2set pgaudit.log = 'ddl';34-- log all CREATE, ALTER, DROP, and SELECT events5set pgaudit.log = 'read, ddl';67-- log nothing8set pgaudit.log = 'none';
```

Example 4 (unknown):
```unknown
1create user "zapier" with password '<new password>';
```

---

## Timeouts | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/timeouts

**Contents:**
- Timeouts
- Extend database timeouts to execute longer transactions
- Change Postgres timeout#
  - Session level#
  - Function level#
  - Role level#
  - Global level#
- Identifying timeouts#
  - Using the Logs Explorer#
  - Using the Query Performance page#

Extend database timeouts to execute longer transactions

Dashboard and Client queries have a max-configurable timeout of 60 seconds. For longer transactions, use Supavisor or direct connections.

You can change the Postgres timeout at the:

Session level settings persist only for the duration of the connection.

Set the session timeout by running:

Because it applies to sessions only, it can only be used with connections through Supavisor in session mode (port 5432) or a direct connection. It cannot be used in the Dashboard, with the Supabase Client API, nor with Supavisor in Transaction mode (port 6543).

This is most often used for single, long running, administrative tasks, such as creating an HSNW index. Once the setting is implemented, you can view it by executing:

See the full guide on changing session timeouts.

This works with the Database REST API when called from the Supabase client libraries:

This is mostly for recurring functions that need a special exemption for runtimes.

This sets the timeout for a specific role.

The default role timeouts are:

Run the following query to change a role's timeout:

If you are changing the timeout for the Supabase Client API calls, you will need to reload PostgREST to reflect the timeout changes by running the following script:

Unlike global settings, the result cannot be checked with SHOW statement_timeout. Instead, run:

This changes the statement timeout for all roles and sessions without an explicit timeout already set.

Check if your changes took effect:

Although not necessary, if you are uncertain if a timeout has been applied, you can run a quick test:

The Supabase Dashboard contains tools to help you identify timed-out and long-running queries.

Go to the Logs Explorer, and run the following query to identify timed-out events (statement timeout) and queries that successfully run for longer than 10 seconds (duration).

Go to the Query Performance page and filter by relevant role and query speeds. This only identifies slow-running but successful queries. Unlike the Log Explorer, it does not show you timed-out queries.

Each API server uses a designated user for connecting to the database:

Filter by the parsed.user_name field to only retrieve logs made by specific users:

**Examples:**

Example 1 (unknown):
```unknown
1set statement_timeout = '10min';
```

Example 2 (unknown):
```unknown
1SHOW statement_timeout;
```

Example 3 (unknown):
```unknown
1create or replace function myfunc()2returns void as $$3 select pg_sleep(3); -- simulating some long-running process4$$5language sql6set statement_timeout TO '4s'; -- set custom timeout
```

Example 4 (unknown):
```unknown
1alter role example_role set statement_timeout = '10min'; -- could also use seconds '10s'
```

---

## Generate types using GitHub Actions | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/ci/generating-types

**Contents:**
- Generate types using GitHub Actions
- End-to-end type safety across client, server, and database.
- Verify types#
- More resources#

Generate types using GitHub Actions

End-to-end type safety across client, server, and database.

You can use the Supabase CLI to automatically generate Typescript definitions from your Postgres database. You can then pass these definitions to your supabase-js client and get end-to-end type safety across client, server, and database.

Inside your repository, create a new file inside the .github/workflows folder called generate-types.yml. Copy this snippet inside the file, and the action will run whenever a new PR is created:

**Examples:**

Example 1 (unknown):
```unknown
1name: 'generate-types'2on:3  pull_request:45jobs:6  build: 7    runs-on: ubuntu-latest8    steps:9        - uses: supabase/setup-cli@v110          with:11            version: latest12        - run: supabase init13        - run: supabase db start14        - name: Verify generated types match Postgres schema15          run: |16            supabase gen types typescript --local > schema.gen.ts17            if ! git diff --ignore-space-at-eol --exit-code --quiet schema.gen.ts; then18              echo "Detected uncommitted changes after build. See status below:"19              git diff20              exit 121            fi
```

---

## Iceberg | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/iceberg

**Contents:**
- Iceberg
- Preparation#
  - Enable Wrappers#
  - Enable the Iceberg Wrapper#
  - Store your credentials (optional)#
  - Connecting to Iceberg#
    - Connecting to AWS S3 Tables#
    - Connecting to Iceberg REST Catalog + AWS S3 (or compatible) storage#
  - Create a schema#
- Options#

You can enable the Iceberg wrapper right from the Supabase dashboard.

Apache Iceberg is a high performance open-source format for large analytic tables.

The Iceberg Wrapper allows you to read from and write to Apache Iceberg within your Postgres database.

Before you can query Iceberg, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the iceberg_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to Iceberg. We can do this using the create server command.

For any server options need to be stored in Vault, you can add a prefix vault_ to its name and use the secret ID returned from the select vault.create_secret() statement as the option value.

For other optional S3 options, please refer to PyIceberg S3 Configuration.

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

We can use SQL import foreign schema to import foreign table definitions from Iceberg.

For example, using below SQL can automatically create foreign tables in the iceberg schema.

By default, the import foreign schema statement will silently skip all the incompatible columns. Use the option strict to prevent this behavior. For example,

This is an object representing Iceberg table.

Ref: Iceberg Table Spec

You can manually create the foreign table like below if you did not use import foreign schema.

This FDW supports where clause pushdown with below operators.

For multiple filters, only logical AND is supported. For example,

The Iceberg FDW supports inserting data into Iceberg tables using standard SQL INSERT statements.

When inserting data into partitioned Iceberg tables, the FDW automatically handles partitioning based on the table's partition spec. Data will be written to the appropriate partition directories.

This section describes important limitations and considerations when using this FDW:

First, create a server for AWS S3 Tables:

Import the foreign table:

Then query the foreign table:

First, follow the steps in Getting Started Guide to create a R2 Catalog on Cloudflare. Once it is completed, create a server like below:

Then, import all the tables in default namespace and query it:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper iceberg_wrapper2  handler iceberg_fdw_handler3  validator iceberg_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your AWS credentials in Vault and retrieve the created2-- `aws_access_key_id` and `aws_secret_access_key`3select vault.create_secret(4  '<access key id>',  -- secret to be encrypted5  'aws_access_key_id',  -- secret name6  'AWS access key for Wrappers'  -- secret description7);8select vault.create_secret(9  '<secret access key>'10  'aws_secret_access_key',11  'AWS secret access key for Wrappers'12);
```

Example 4 (unknown):
```unknown
1create server iceberg_server2  foreign data wrapper iceberg_wrapper3  options (4    -- The key id saved in Vault from above5    vault_aws_access_key_id '<key_ID>',67    -- The secret id saved in Vault from above8    vault_aws_secret_access_key '<secret_key>',910    -- AWS region11    region_name 'us-east-1',1213    -- AWS S3 table bucket ARN14    aws_s3table_bucket_arn 'arn:aws:s3tables:us-east-1:204203087419:bucket/my-table-bucket'15  );
```

---

## BigQuery | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/bigquery

**Contents:**
- BigQuery
- Preparation#
  - Enable Wrappers#
  - Enable the BigQuery Wrapper#
  - Store your credentials (optional)#
  - Connecting to BigQuery#
  - Create a schema#
- Options#
- Entites#
  - Tables#

You can enable the BigQuery wrapper right from the Supabase dashboard.

BigQuery is a completely serverless and cost-effective enterprise data warehouse that works across clouds and scales with your data, with BI, machine learning and AI built in.

The BigQuery Wrapper allows you to read and write data from BigQuery within your Postgres database.

Before you can query BigQuery, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the bigquery_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to BigQuery, and any additional options. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The following options are available when creating BigQuery foreign tables:

You can also use a subquery as the table option:

Note: When using subquery, full qualified table name must be used.

The BigQuery Wrapper supports data reads and writes from BigQuery tables and views.

This FDW supports where, order by and limit clause pushdown.

This foreign data wrapper uses BigQuery’s insertAll API method to create a streamingBuffer with an associated partition time. Within that partition time, the data cannot be updated, deleted, or fully exported. Only after the time has elapsed (up to 90 minutes according to BigQuery’s documentation), can you perform operations.

If you attempt an UPDATE or DELETE statement on rows while in the streamingBuffer, you will get an error of UPDATE or DELETE statement over table datasetName - note that tableName would affect rows in the streaming buffer, which is not supported.

This section describes important limitations and considerations when using this FDW:

Some examples on how to use BigQuery foreign tables.

Let's prepare the source table in BigQuery first:

This example will create a "foreign table" inside your Postgres database called people and query its data:

This example will modify data in a "foreign table" inside your Postgres database called people, note that rowid_column option is mandatory:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper bigquery_wrapper2  handler big_query_fdw_handler3  validator big_query_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your BigQuery service account json in Vault and retrieve the created `key_id`2select vault.create_secret(3  '4    {5      "type": "service_account",6      "project_id": "your_gcp_project_id",7      "private_key_id": "your_private_key_id",8      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",9      ...10    }11  ',12  'bigquery',13  'BigQuery service account json for Wrappers'14);
```

Example 4 (unknown):
```unknown
1create server bigquery_server2  foreign data wrapper bigquery_wrapper3  options (4    sa_key_id '<key_ID>', -- The Key ID from above.5    project_id 'your_gcp_project_id',6    dataset_id 'your_gcp_dataset_id'7  );
```

---

## Cascade Deletes | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/cascade-deletes

**Contents:**
- Cascade Deletes
- RESTRICT vs NO ACTION#
- Example#
  - RESTRICT#
  - NO ACTION#
  - NO ACTION INITIALLY DEFERRED#

There are 5 options for foreign key constraint deletes:

These options can be specified when defining a foreign key constraint using the "ON DELETE" clause. For example, the following SQL statement creates a foreign key constraint with the CASCADE option:

This means that when a row is deleted from the parent_table, all related rows in the child_table will be deleted as well.

The difference between NO ACTION and RESTRICT is subtle and can be a bit confusing.

Both NO ACTION and RESTRICT are used to prevent deletion of a row in a parent table if there are related rows in a child table. However, there is a subtle difference in how they behave.

When a foreign key constraint is defined with the option RESTRICT, it means that if a row in the parent table is deleted, the database will immediately raise an error and prevent the deletion of the row in the parent table. The database will not delete, update or set to NULL any rows in the referenced tables.

When a foreign key constraint is defined with the option NO ACTION, it means that if a row in the parent table is deleted, the database will also raise an error and prevent the deletion of the row in the parent table. However unlike RESTRICT, NO ACTION has the option to defer the check using INITIALLY DEFERRED. This will only raise the above error if the referenced rows still exist at the end of the transaction.

The difference from RESTRICT is that a constraint marked as NO ACTION INITIALLY DEFERRED is deferred until the end of the transaction, rather than running immediately. If, for example there is another foreign key constraint between the same tables marked as CASCADE, the cascade will occur first and delete the referenced rows, and no error will be thrown by the deferred constraint. Otherwise if there are still rows referencing the parent row by the end of the transaction, an error will be raised just like before. Just like RESTRICT, the database will not delete, update or set to NULL any rows in the referenced tables.

In practice, you can use either NO ACTION or RESTRICT depending on your needs. NO ACTION is the default behavior if you do not specify anything. If you prefer to defer the check until the end of the transaction, use NO ACTION INITIALLY DEFERRED.

Let's further illustrate the difference with an example. We'll use the following data:

To create these tables and their data, we run:

RESTRICT will prevent a delete and raise an error:

Even though the foreign key constraint between parent and grandparent is CASCADE, the constraint between child and father is RESTRICT. Therefore an error is raised and no records are deleted.

Let's change the child-father relationship to NO ACTION:

We see that NO ACTION will also prevent a delete and raise an error:

We'll change the foreign key constraint between child and father to be NO ACTION INITIALLY DEFERRED:

Here you will see that INITIALLY DEFFERED seems to operate like NO ACTION or RESTRICT. When we run a delete, it seems to make no difference:

But, when we combine it with other constraints, then any other constraints take precedence. For example, let's run the same but add a mother column that has a CASCADE delete:

Then let's run a delete on the grandparent table:

The mother deletion took precedence over the father, and so William was deleted. After William was deleted, there was no reference to “Charles” and so he was free to be deleted, even though previously he wasn't (without INITIALLY DEFERRED).

**Examples:**

Example 1 (unknown):
```unknown
1alter table child_table2add constraint fk_parent foreign key (parent_id) references parent_table (id)3  on delete cascade;
```

Example 2 (unknown):
```unknown
1create table grandparent (2  id serial primary key,3  name text4);56create table parent (7  id serial primary key,8  name text,9  parent_id integer references grandparent (id)10    on delete cascade11);1213create table child (14  id serial primary key,15  name text,16  father integer references parent (id)17    on delete restrict18);1920insert into grandparent21  (id, name)22values23  (1, 'Elizabeth');2425insert into parent26  (id, name, parent_id)27values28  (1, 'Charles', 1);2930insert into parent31  (id, name, parent_id)32values33  (2, 'Diana', 1);3435-- We'll just link the father for now36insert into child37  (id, name, father)38values39  (1, 'William', 1);
```

Example 3 (unknown):
```unknown
1postgres=# delete from grandparent;2ERROR: update or delete on table "parent" violates foreign key constraint "child_father_fkey" on table "child"3DETAIL: Key (id)=(1) is still referenced from table "child".
```

Example 4 (unknown):
```unknown
1alter table child2drop constraint child_father_fkey;34alter table child5add constraint child_father_fkey foreign key (father) references parent (id)6  on delete no action;
```

---

## Performance and Security Advisors | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/database-advisors

**Contents:**
- Performance and Security Advisors
- Check your database for performance and security issues
- Using the Advisors#
- Available checks#
  - Rationale#
  - What is a Foreign Key?#
  - Why Index Foreign Key Columns?#
  - How to Resolve#
  - Example#

Performance and Security Advisors

Check your database for performance and security issues

You can use the Database Performance and Security Advisors to check your database for issues such as missing indexes and improperly set-up RLS policies.

In the dashboard, navigate to Security Advisor and Performance Advisor under Database. The advisors run automatically. You can also manually rerun them after you've resolved issues.

In relational databases, indexing foreign key columns is a standard practice for improving query performance. Indexing these columns is recommended in most cases because it improves query join performance along a declared relationship.

A foreign key is a constraint on a column (or set of columns) that enforces a relationship between two tables. For example, a foreign key from book.author_id to author.id enforces that every value in book.author_id exists in author.id. Once the foriegn key is declared, it is not possible to insert a value into book.author_id that does not exist in author.id. Similarly, Postgres will not allow us to delete a value from author.id that is referenced by book.author_id. This concept is known as referential integrity.

Given that foreign keys define relationships among tables, it is common to use foreign key columns in join conditions when querying the database. Adding an index to the columns making up the foreign key improves the performance of those joins and reduces database resource consumption.

To apply the best practice of indexing foreign keys, an index is needed on the book.author_id column. We can create that index using:

In this case we used the default B-tree index type. Be sure to choose an index type that is appropriate for the data types and use case when working with your own tables.

Let's look at a practical example involving two tables: order_item and customer, where order_item references customer.

We expect the tables to be joined on the condition

Using Postgres' "explain plan" functionality, we can see how its query planner expects to execute the query.

Notice that the condition order_item.customer_id = customer.id is being serviced by a Seq Scan, a sequential scan across the order_items table. That means Postgres intends to sequentially iterate over each row in the table to identify the value of customer_id.

Next, if we index order_item.customer_id and recompute the query plan:

We get the query plan:

Note that nothing changed.

We get an identical result because Postgres' query planner is clever enough to know that a Seq Scan over an empty table is extremely fast, so theres no reason for it to reach out to an index. As more rows are inserted into the order_item table the tradeoff between sequentially scanning and retriving the index steadily tip in favor of the index. Rather than manually finding this inflection point, we can hint to the query planner that we'd like to use indexes by disabling sequentials scans except where they are the only available option. To provides that hint we can use:

We get the query plan:

The new plan services the order_item.customer_id = customer.id join condition using an Index Scan on ix_order_item_customer_id which is far more efficient at scale.

**Examples:**

Example 1 (unknown):
```unknown
1select2    book.id,3    book.title,4    author.name5from6    book7    join author8        -- Both sides of the following condition should be indexed9        -- for best performance10        on book.author_id = author.id
```

Example 2 (unknown):
```unknown
1create table book (2    id serial primary key,3    title text not null,4    author_id int references author(id) -- this defines the foreign key5);
```

Example 3 (unknown):
```unknown
1create index ix_book_author_id on book(author_id);
```

Example 4 (unknown):
```unknown
1create table customer (2    id serial primary key,3    name text not null4);56create table order_item (7    id serial primary key,8    order_date date not null,9    customer_id integer not null references customer (id)10);
```

---

## Select first row for each group in PostgreSQL | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/first-row-in-group

**Contents:**
- Select first row for each group in PostgreSQL

Select first row for each group in PostgreSQL

Given a table seasons:

We want to find the rows containing the maximum number of points per team.

The expected output we want is:

From the SQL Editor, you can run a query like:

The important bits here are:

This query can also be executed via psql or any other query editor if you prefer to connect directly to the database.

**Examples:**

Example 1 (unknown):
```unknown
1select distinct2  on (team) id,3  team,4  points5from6  seasons7order BY8  id,9  points desc,10  team;
```

---

## pgTAP: Unit Testing | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgtap

**Contents:**
- pgTAP: Unit Testing
- Overview#
- Enable the extension#
- Testing tables#
- Testing columns#
- Testing RLS policies#
- Testing functions#
- Resources#

pgTAP is a unit testing extension for Postgres.

Let's cover some basic concepts:

You can also use the results_eq() method to test that a Policy returns the correct data:

**Examples:**

Example 1 (unknown):
```unknown
1begin;2select plan( 1 );34select has_table( 'profiles' );56select * from finish();7rollback;
```

Example 2 (unknown):
```unknown
1begin;2select plan( 2 );34select has_column( 'profiles', 'id' ); -- test that the "id" column exists in the "profiles" table5select col_is_pk( 'profiles', 'id' ); -- test that the "id" column is a primary key67select * from finish();8rollback;
```

Example 3 (unknown):
```unknown
1begin;2select plan( 1 );34select policies_are(5  'public',6  'profiles',7  ARRAY [8    'Profiles are public', -- Test that there is a policy called  "Profiles are public" on the "profiles" table.9    'Profiles can only be updated by the owner'  -- Test that there is a policy called  "Profiles can only be updated by the owner" on the "profiles" table.10  ]11);1213select * from finish();14rollback;
```

Example 4 (unknown):
```unknown
1begin;2select plan( 1 );34select results_eq(5    'select * from profiles()',6    $$VALUES ( 1, 'Anna'), (2, 'Bruce'), (3, 'Caryn')$$,7    'profiles() should return all users'8);91011select * from finish();12rollback;
```

---

## Logflare | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/logflare

**Contents:**
- Logflare
- Preparation#
  - Enable Wrappers#
  - Enable the Logflare Wrapper#
  - Store your credentials (optional)#
  - Connecting to Logflare#
  - Create a schema#
- Options#
- Entities#
  - Logflare#

You can enable the Logflare wrapper right from the Supabase dashboard.

Logflare is a centralized web-based log management solution to easily access Cloudflare, Vercel & Elixir logs.

The Logflare Wrapper allows you to read data from Logflare endpoints within your Postgres database.

Before you can query Logflare, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the logflare_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to Logflare, and any additional options. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

This is an object representing Logflare endpoint data.

This FDW doesn't support query pushdown.

This section describes important limitations and considerations when using this FDW:

Given a Logflare endpoint response:

You can create and query a foreign table:

For an endpoint accepting parameters:

With response format:

Create and query the table with parameters:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper logflare_wrapper2  handler logflare_fdw_handler3  validator logflare_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Logflare API key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<YOUR_SECRET>',4  'logflare',5  'Logflare API key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server logflare_server2  foreign data wrapper logflare_wrapper3  options (4    api_key_id '<key_ID>' -- The Key ID from above.5  );
```

---

## Database Webhooks | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/webhooks

**Contents:**
- Database Webhooks
- Trigger external payloads on database events.
- Webhooks vs triggers#
- Creating a webhook#
- Payload#
- Monitoring#
- Local development#
- Resources#

Trigger external payloads on database events.

Database Webhooks allow you to send real-time data from your database to another system whenever a table event occurs.

You can hook into three table events: INSERT, UPDATE, and DELETE. All events are fired after a database row is changed.

Database Webhooks are very similar to triggers, and that's because Database Webhooks are just a convenience wrapper around triggers using the pg_net extension. This extension is asynchronous, and therefore will not block your database changes for long-running network requests.

This video demonstrates how you can create a new customer in Stripe each time a row is inserted into a profiles table:

Since webhooks are just database triggers, you can also create one from SQL statement directly.

We currently support HTTP webhooks. These can be sent as POST or GET requests with a JSON payload.

The payload is automatically generated from the underlying table record:

Logging history of webhook calls is available under the net schema of your database. For more info, see the GitHub Repo.

When using Database Webhooks on your local Supabase instance, you need to be aware that the Postgres database runs inside a Docker container. This means that localhost or 127.0.0.1 in your webhook URL will refer to the container itself, not your host machine where your application is running.

To target services running on your host machine, use host.docker.internal. If that doesn't work, you may need to use your machine's local IP address instead.

For example, if you want to trigger an edge function when a webhook fires, your webhook URL would be:

If you're experiencing connection issues with webhooks locally, verify you're using the correct hostname instead of localhost.

**Examples:**

Example 1 (unknown):
```unknown
1create trigger "my_webhook" after insert2on "public"."my_table" for each row3execute function "supabase_functions"."http_request"(4  'http://host.docker.internal:3000',5  'POST',6  '{"Content-Type":"application/json"}',7  '{}',8  '1000'9);
```

Example 2 (unknown):
```unknown
1type InsertPayload = {2  type: 'INSERT'3  table: string4  schema: string5  record: TableRecord<T>6  old_record: null7}8type UpdatePayload = {9  type: 'UPDATE'10  table: string11  schema: string12  record: TableRecord<T>13  old_record: TableRecord<T>14}15type DeletePayload = {16  type: 'DELETE'17  table: string18  schema: string19  record: null20  old_record: TableRecord<T>21}
```

Example 3 (unknown):
```unknown
1http://host.docker.internal:54321/functions/v1/my-function-name
```

---

## pg_cron: Schedule Recurring Jobs with Cron Syntax in Postgres | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_cron

**Contents:**
- pg_cron: Schedule Recurring Jobs with Cron Syntax in Postgres

pg_cron: Schedule Recurring Jobs with Cron Syntax in Postgres

See the Supabase Cron docs.

---

## GraphQL API | Supabase Docs

**URL:** https://supabase.com/docs/guides/graphql/api

**Contents:**
- GraphQL API
- Understanding the core concepts of the GraphQL API.
- Primary Keys (Required)#
- QueryType#
  - Node#
  - Collections#
    - Aggregates#
    - Pagination#
      - Keyset Pagination
      - Offset Pagination

Understanding the core concepts of the GraphQL API.

In our API, each SQL table is reflected as a set of GraphQL types. At a high level, tables become types and columns/foreign keys become fields on those types.

By default, PostgreSQL table and column names are not inflected when reflecting GraphQL names. For example, an account_holder table has GraphQL type name account_holder. In cases where SQL entities are named using snake_case, enable inflection to match GraphQL/Javascript conventions e.g. account_holder -> AccountHolder.

Individual table, column, and relationship names may also be manually overridden.

Every table must have a primary key for it to be exposed in the GraphQL schema. For example, the following Blog table will be available in the GraphQL schema as blogCollection since it has a primary key named id:

But the following table will not be exposed because it doesn't have a primary key:

The Query type is the entrypoint for all read access into the graph.

The node interface allows for retrieving records that are uniquely identifiable by a globally unique nodeId: ID! field. For more information about nodeId, see nodeId.

To query the node interface effectively, use inline fragments to specify which fields to return for each type.

Each table has top level entry in the Query type for selecting records from that table. Collections return a connection type and can be paginated, filtered, and sorted using the available arguments.

Connection types are the primary interface to returning records from a collection.

Connections wrap a result set with some additional metadata.

The totalCount field is disabled by default because it can be expensive on large tables. To enable it use a comment directive

Aggregate functions are available on the collection's aggregate field when enabled via comment directive. These allow you to perform calculations on the collection of records that match your filter criteria.

The supported aggregate operations are:

The aggregate field is disabled by default because it can be expensive on large tables. To enable it use a comment directive

Paginating forwards and backwards through collections is handled using the first, last, before, and after parameters, following the relay spec.

Metadata relating to the current page of a result set is available on the pageInfo field of the connection type returned from a collection.

To paginate forward in the collection, use the first and after arguments. To retrieve the first page, the after argument should be null or absent.

To retrieve the next page, provide the cursor value from data.blogCollection.pageInfo.endCursor to the after argument of another query.

once the collection has been fully enumerated, data.blogConnection.pageInfo.hasNextPage returns false.

To paginate backwards through a collection, repeat the process substituting first -> last, after -> before, hasNextPage -> hasPreviousPage

In addition to keyset pagination, collections may also be paged using first and offset, which operates like SQL's limit and offset to skip offset number of records in the results.

offset based pagination becomes inefficient the offset value increases. For this reason, prefer cursor based pagination where possible.

To filter the result set, use the filter argument.

Where the <Table>Filter type enumerates filterable fields and their associated <Type>Filter.

The following list shows the operators that may be available on <Type>Filter types.

Not all operators are available on every <Type>Filter type. For example, UUIDFilter only supports eq and neq because UUIDs are not ordered.

Example: array column

The contains filter is used to return results where all the elements in the input array appear in the array column.

The contains filter can also accept a single scalar.

The containedBy filter is used to return results where every element of the array column appears in the input array.

The containedBy filter can also accept a single scalar. In this case, only results where the only element in the array column is the input scalar are returned.

The overlaps filter is used to return results where the array column and the input array have at least one element in common.

Multiple filters can be combined with and, or and not operators. The and and or operators accept a list of <Type>Filter.

not accepts a single <Type>Filter.

Example: nested composition

The and, or and not operators can be arbitrarily nested inside each other.

Empty filters are ignored, i.e. they behave as if the operator was not specified at all.

Example: implicit and

Multiple column filters at the same level will be implicitly combined with boolean and. In the following example the id: {eq: 1} and name: {eq: "A: Blog 1"} will be anded.

This means that an and filter can be often be simplified. In the following example all queries are equivalent and produce the same result.

Be aware that the above simplification only works for the and operator. If you try it with an or operator it will behave like an and.

This is because according to the rules of GraphQL list input coercion, if a value passed to an input of list type is not a list, then it is coerced to a list of a single item. So in the above example or: {id: {eq: 1}, name: {eq: "A: Blog 2}} will be coerced into or: [{id: {eq: 1}, name: {eq: "A: Blog 2}}] which is equivalent to or: [and: [{id: {eq: 1}}, {name: {eq: "A: Blog 2}}}] due to implicit anding.

Avoid naming your columns and, or or not. If you do, the corresponding filter operator will not be available for use.

The and, or and not operators also work with update and delete mutations.

The default order of results is defined by the underlying table's primary key column in ascending order. That default can be overridden by passing an array of <Table>OrderBy to the collection's orderBy argument.

Note, only one key value pair may be provided to each element of the input array. For example, [{name: AscNullsLast}, {id: AscNullFirst}] is valid. Passing multiple key value pairs in a single element of the input array e.g. [{name: AscNullsLast, id: AscNullFirst}], is invalid.

The Mutation type is the entrypoint for mutations/edits.

Each table has top level entry in the Mutation type for inserting insertInto<Table>Collection, updating update<Table>Collection and deleting deleteFrom<Table>Collection.

To add records to a collection, use the insertInto<Table>Collection field on the Mutation type.

Where elements in the objects array are inserted into the underlying table.

To update records in a collection, use the update<Table>Collection field on the Mutation type.

Where the set argument is a key value pair describing the values to update, filter controls which records should be updated, and atMost restricts the maximum number of records that may be impacted. If the number of records impacted by the mutation exceeds the atMost parameter the operation will return an error.

To remove records from a collection, use the deleteFrom<Table>Collection field on the Mutation type.

Where filter controls which records should be deleted and atMost restricts the maximum number of records that may be deleted. If the number of records impacted by the mutation exceeds the atMost parameter the operation will return an error.

The base GraphQL type for every table with a primary key is automatically assigned a nodeId: ID! field. That value, can be passed to the node entrypoint of the Query type to retrieve its other fields. nodeId may also be used as a caching key.

Relationships between collections in the Graph are derived from foreign keys.

A foreign key on table A referencing table B defines a one-to-many relationship from table A to table B.

Where blogPostCollection exposes the full Query interface to BlogPosts.

A foreign key on table A referencing table B defines a many-to-one relationship from table B to table A.

Where blog exposes the Blog record associated with the BlogPost.

A one-to-one relationship is defined by a foreign key on table A referencing table B where the columns making up the foreign key on table A are unique.

Due to differences among the types supported by PostgreSQL, JSON, and GraphQL, pg_graphql adds several new Scalar types to handle PostgreSQL builtins that require special handling.

pg_graphql serializes json and jsonb data types as String under the custom scalar name JSON.

The returns the following data. Note that config is serialized as a string

Use serialized JSON strings when updating or inserting JSON fields via the GraphQL API.

JSON does not currently support filtering.

PostgreSQL bigint and bigserial types are 64 bit integers. In contrast, JSON supports 32 bit integers.

Since PostgreSQL bigint values may be outside the min/max range allowed by JSON, they are represented in the GraphQL schema as BigInts and values are serialized as strings.

The returns the following data. Note that id is serialized as a string

PostgreSQL's numeric type supports arbitrary precision floating point values. JSON's float is limited to 64-bit precision.

Since a PostgreSQL numeric may require more precision than can be handled by JSON, numeric types are represented in the GraphQL schema as BigFloat and values are serialized as strings.

The returns the following data. Note that amount is serialized as a string

PostgreSQL's type system is extensible and not all types handle all operations e.g. filtering with like. To account for these, pg_graphql introduces a scalar Opaque type. The Opaque type uses PostgreSQL's to_json method to serialize values. That allows complex or unknown types to be included in the schema by delegating handling to the client.

**Examples:**

Example 1 (unknown):
```unknown
1create table "Blog"(2  id serial primary key,3  name varchar(255) not null,4);
```

Example 2 (unknown):
```unknown
1create table "Blog"(2  id int,3  name varchar(255) not null,4);
```

Example 3 (unknown):
```unknown
1create table "Blog"(2  id serial primary key,3  name varchar(255) not null,4  description varchar(255),5  "createdAt" timestamp not null,6  "updatedAt" timestamp not null7);
```

Example 4 (unknown):
```unknown
1"""The root type for querying data"""2type Query {34  """Retrieve a record by its `ID`"""5  node(nodeId: ID!): Node67}
```

---

## RUM: improved inverted index for full-text search based on GIN index | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/rum

**Contents:**
- RUM: improved inverted index for full-text search based on GIN index
- Usage#
  - Enable the extension#
  - Syntax#
    - For type: tsvector#
    - For type: anyarray#
- Limitations#
- Resources#

RUM: improved inverted index for full-text search based on GIN index

RUM is an extension which adds a RUM index to Postgres.

RUM index is based on GIN that stores additional per-entry information in a posting tree. For example, positional information of lexemes or timestamps. In comparison to GIN it can use this information to make faster index-only scans for:

RUM works best in scenarios when the possible keys are highly repeatable. I.e. all texts are composed of a limited amount of words, so per-lexeme indexing gives significant speed-up in searching texts containing word combinations or phrases.

Main operators for ordering are:

tsvector <=> tsquery | float4 | Distance between tsvector and tsquery. value <=> value | float8 | Distance between two values.

Where value is timestamp, timestamptz, int2, int4, int8, float4, float8, money and oid

You can get started with rum by enabling the extension in your Supabase dashboard.

To understand the following you may need first to see Official Postgres documentation on text search

And we can execute tsvector selects with ordering by text distance operator:

rum_tsvector_addon_ops

Now we can execute the selects with ordering distance operator on attached column:

This operator class stores anyarray elements with length of the array. It supports operators &&, @>, <@, =, % operators. It also supports ordering by <=> operator.

Now we can execute the query using index scan:

rum_anyarray_addon_ops

The does the same with anyarray index as rum_tsvector_addon_ops i.e. allows to order select results using distance operator by attached column.

RUM has slower build and insert times than GIN due to:

**Examples:**

Example 1 (unknown):
```unknown
1CREATE TABLE test_rum(t text, a tsvector);23CREATE TRIGGER tsvectorupdate4BEFORE UPDATE OR INSERT ON test_rum5FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger('a', 'pg_catalog.english', 't');67INSERT INTO test_rum(t) VALUES ('The situation is most beautiful');8INSERT INTO test_rum(t) VALUES ('It is a beautiful');9INSERT INTO test_rum(t) VALUES ('It looks like a beautiful place');1011CREATE INDEX rumidx ON test_rum USING rum (a rum_tsvector_ops);
```

Example 2 (javascript):
```javascript
1SELECT t, a `<=>` to_tsquery('english', 'beautiful | place') AS rank2    FROM test_rum3    WHERE a @@ to_tsquery('english', 'beautiful | place')4    ORDER BY a `<=>` to_tsquery('english', 'beautiful | place');5                t                |  rank6---------------------------------+---------7 It looks like a beautiful place | 8.224678 The situation is most beautiful | 16.44939 It is a beautiful               | 16.449310(3 rows)
```

Example 3 (unknown):
```unknown
1CREATE TABLE tsts (id int, t tsvector, d timestamp);2CREATE INDEX tsts_idx ON tsts USING rum (t rum_tsvector_addon_ops, d)3    WITH (attach = 'd', to = 't');
```

Example 4 (javascript):
```javascript
1SELECT id, d, d `<=>` '2016-05-16 14:21:25' FROM tsts WHERE t @@ 'wr&qh' ORDER BY d `<=>` '2016-05-16 14:21:25' LIMIT 5;2 id  |                d                |   ?column?3-----+---------------------------------+---------------4 355 | Mon May 16 14:21:22.326724 2016 |      2.6732765 354 | Mon May 16 13:21:22.326724 2016 |   3602.6732766 371 | Tue May 17 06:21:22.326724 2016 |  57597.3267247 406 | Wed May 18 17:21:22.326724 2016 | 183597.3267248 415 | Thu May 19 02:21:22.326724 2016 | 215997.3267249(5 rows)
```

---

## Securing your API | Supabase Docs

**URL:** https://supabase.com/docs/guides/api/securing-your-api

**Contents:**
- Securing your API
- Enabling row level security#
- Disable the API or restrict to custom schema#
- Enforce additional rules on each request#
  - Accessing request information#
  - Examples#

The data APIs are designed to work with Postgres Row Level Security (RLS). If you use Supabase Auth, you can restrict data based on the logged-in user.

To control access to your data, you can use Policies.

Any table you create in the public schema will be accessible via the Supabase Data API.

To restrict access, enable Row Level Security (RLS) on all tables, views, and functions in the public schema. You can then write RLS policies to grant users access to specific database rows or functions based on their authentication token.

Always enable Row Level Security on tables, views, and functions in the public schema to protect your data.

Any table created through the Supabase Dashboard will have RLS enabled by default. If you created the tables via the SQL editor or via another way, enable RLS like so:

With RLS enabled, you can create Policies that allow or disallow users to access and update data. We provide a detailed guide for creating Row Level Security Policies in our Authorization documentation.

Any table without RLS enabled in the public schema will be accessible to the public, using the anon role. Always make sure that RLS is enabled or that you've got other security measures in place to avoid unauthorized access to your project's data!

If you don't use the Data API, or if you don't want to expose the public schema, you can either disable it entirely or change the automatically exposed schema to one of your choice. See Hardening the Data API for instructions.

Using Row Level Security policies may not always be adequate or sufficient to protect APIs.

Here are some common situations where additional protections are necessary:

You can build these cases in your application by creating a Postgres function that will read information from the request and perform additional checks, such as counting the number of requests received or checking that an API key is already registered in your database before serving the response.

Define a function like so:

And register it to run on every Data API request using:

This configures the public.check_request function to run on every Data API request. To have the changes take effect, you should run:

The pgrst.db_pre_request configuration only works with the Data API (PostgREST). It does not work with Realtime, Storage, or other Supabase products.

If you're using db_pre_request to call a function (like set_information()) that sets up context or performs checks on every request, and you need similar behavior for other Supabase products, you must call the function directly in your Row Level Security (RLS) policies instead.

If you have a db_pre_request function that calls set_information() that returns true to set up context or perform checks, and you have an RLS policy like:

To achieve the same behavior with other Supabase products, you need to call the function directly in your RLS policy:

This ensures the function is called when evaluating RLS policies for all products, not just Data API requests.

Performance consideration:

Be aware that calling functions directly in RLS policies can impact database performance, as the function is evaluated for each row when the policy is checked. Consider optimizing your function or using caching strategies if performance becomes an issue.

Inside the function you can perform any additional checks on the request headers or JWT and raise an exception to prevent the request from completing. For example, this exception raises a HTTP 402 Payment Required response with a hint and additional X-Powered-By header:

When raised within the public.check_request function, the resulting HTTP response will look like:

Use the JSON operator functions to build rich and dynamic responses from exceptions.

If you use a custom HTTP status code like 419, you can supply the status_text key in the detail clause of the exception to describe the HTTP status.

If you're using PostgREST version 11 or lower (find out your PostgREST version) a different and less powerful syntax needs to be used.

Like with RLS policies, you can access information about the request by using the current_setting() Postgres function. Here are some examples on how this works:

To access the IP address of the client look up the X-Forwarded-For header in the request.headers setting. For example:

Read more about PostgREST's pre-request function.

You can only rate-limit POST, PUT, PATCH and DELETE requests. This is because GET and HEAD requests run in read-only mode, and will be served by Read Replicas which do not support writing to the database.

The private schema is used as it cannot be accessed over the API!

Create the public.check_request function:

Finally, configure the public.check_request() function to run on every Data API request:

The pgrst.db_pre_request configuration only works with the Data API (PostgREST). It does not work with Realtime, Storage, or other Supabase products.

If you're using db_pre_request to call a function (like set_information()) that sets up context or performs checks on every request, and you need similar behavior for other Supabase products, you must call the function directly in your Row Level Security (RLS) policies instead.

If you have a db_pre_request function that calls set_information() that returns true to set up context or perform checks, and you have an RLS policy like:

To achieve the same behavior with other Supabase products, you need to call the function directly in your RLS policy:

This ensures the function is called when evaluating RLS policies for all products, not just Data API requests.

Performance consideration:

Be aware that calling functions directly in RLS policies can impact database performance, as the function is evaluated for each row when the policy is checked. Consider optimizing your function or using caching strategies if performance becomes an issue.

To clear old entries in the private.rate_limits table, set up a pg_cron job to clean them up.

**Examples:**

Example 1 (unknown):
```unknown
1create function public.check_request()2  returns void3  language plpgsql4  security definer5  as $$6begin7  -- your logic here8end;9$$;
```

Example 2 (unknown):
```unknown
1alter role authenticator2  set pgrst.db_pre_request = 'public.check_request';
```

Example 3 (unknown):
```unknown
1notify pgrst, 'reload config';
```

Example 4 (unknown):
```unknown
1create policy "Individuals can view their own todos."2on todos for select3using ( (select auth.uid()) = user_id );
```

---

## Auth0 | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/auth0

**Contents:**
- Auth0
- Preparation#
  - Enable Wrappers#
  - Enable the Auth0 Wrapper#
  - Store your credentials (optional)#
  - Connecting to Auth0#
  - Create a schema#
- Entities#
  - Users#
    - Operations#

You can enable the Auth0 wrapper right from the Supabase dashboard.

Auth0 is a flexible, drop-in solution to add authentication and authorization services to your applications

The Auth0 Wrapper allows you to read data from your Auth0 tenant for use within your Postgres database.

Before you can query Auth0, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the auth0_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to Auth0, and any additional options. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The Auth0 Wrapper supports data reads from Auth0 API.

The Auth0 Wrapper supports data reads from Auth0's Management API List users endpoint endpoint (read only).

This FDW doesn't support query pushdown.

This section describes important limitations and considerations when using this FDW:

This example demonstrates querying Auth0 users data.

You can now fetch your Auth0 data from within your Postgres database:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper auth0_wrapper2  handler auth0_fdw_handler3  validator auth0_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Auth0 API key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<Auth0 API Key or PAT>', -- Auth0 API key or Personal Access Token (PAT)4  'auth0',5  'Auth0 API key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server auth0_server2  foreign data wrapper auth0_wrapper3  options (4    url 'https://dev-<tenant-id>.us.auth0.com/api/v2/users',5    api_key_id '<key_ID>' -- The Key ID from above.6  );
```

---

## Database Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/functions?language=js

**Contents:**
- Database Functions
- Quick demo#
- Getting started#
- Simple functions#
- Returning data sets#
    - Planets
    - People
- Passing parameters#
- Suggestions#
  - Database Functions vs Edge Functions#

Postgres has built-in support for SQL functions. These functions live inside your database, and they can be used with the API.

Supabase provides several options for creating database functions. You can use the Dashboard or create them directly using SQL. We provide a SQL editor within the Dashboard, or you can connect to your database and run the SQL queries yourself.

Let's create a basic Database Function which returns a string "hello world".

At it's most basic a function has the following parts:

When naming your functions, make the name of the function unique as overloaded functions are not supported.

After the Function is created, we have several ways of "executing" the function - either directly inside the database using SQL, or with one of the client libraries.

Database Functions can also return data sets from Tables or Views.

For example, if we had a database with some Star Wars data inside:

We could create a function which returns all the planets:

Because this function returns a table set, we can also apply filters and selectors. For example, if we only wanted the first planet:

Let's create a Function to insert a new planet into the planets table and return the new ID. Note that this time we're using the plpgsql language.

Once again, you can execute this function either inside your database using a select query, or with the client libraries:

For data-intensive operations, use Database Functions, which are executed within your database and can be called remotely using the REST and GraphQL API.

For use-cases which require low-latency, use Edge Functions, which are globally-distributed and can be written in Typescript.

Postgres allows you to specify whether you want the function to be executed as the user calling the function (invoker), or as the creator of the function (definer). For example:

It is best practice to use security invoker (which is also the default). If you ever use security definer, you must set the search_path. If you use an empty search path (search_path = ''), you must explicitly state the schema for every relation in the function body (e.g. from public.table). This limits the potential damage if you allow access to schemas which the user executing the function should not have.

By default, database functions can be executed by any role. There are two main ways to restrict this:

On a case-by-case basis. Specifically revoke permissions for functions you want to protect. Execution needs to be revoked for both public and the role you're restricting:

Restrict function execution by default. Specifically grant access when you want a function to be executable by a specific role.

To restrict all existing functions, revoke execution permissions from both public and the role you want to restrict:

To restrict all new functions, change the default privileges for both public and the role you want to restrict:

You can then regrant permissions for a specific function to a specific role:

You can add logs to help you debug functions. This is especially recommended for complex functions.

Good targets to log include:

To create custom logs in the Dashboard's Postgres Logs, you can use the raise keyword. By default, there are 3 observed severity levels:

You can create custom errors with the raise exception keywords.

A common pattern is to throw an error when a variable doesn't meet a condition:

Value checking is common, so Postgres provides a shorthand: the assert keyword. It uses the following format:

Error messages can also be captured and modified with the exception keyword:

For more complex functions or complicated debugging, try logging:

**Examples:**

Example 1 (unknown):
```unknown
1create or replace function hello_world() -- 12returns text -- 23language sql -- 34as $$  -- 45  select 'hello world';  -- 56$$; --6
```

Example 2 (unknown):
```unknown
1select hello_world();
```

Example 3 (unknown):
```unknown
1| id  | name     |2| --- | -------- |3| 1   | Tatooine |4| 2   | Alderaan |5| 3   | Kashyyyk |
```

Example 4 (unknown):
```unknown
1| id  | name             | planet_id |2| --- | ---------------- | --------- |3| 1   | Anakin Skywalker | 1         |4| 2   | Luke Skywalker   | 1         |5| 3   | Princess Leia    | 2         |6| 4   | Chewbacca        | 3         |
```

---

## Connect to your database | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/connecting-to-postgres

**Contents:**
- Connect to your database
- Supabase provides multiple methods to connect to your Postgres database, whether you’re working on the frontend, backend, or utilizing serverless functions.
- How to connect to your Postgres databases#
- Quickstarts#
- Data APIs and client libraries#
- Direct connection#
- Poolers#
  - Pooler session mode#
  - Pooler transaction mode#
- Dedicated pooler#

Connect to your database

Supabase provides multiple methods to connect to your Postgres database, whether you’re working on the frontend, backend, or utilizing serverless functions.

How you connect to your database depends on where you're connecting from:

The Data APIs allow you to interact with your database using REST or GraphQL requests. You can use these APIs to fetch and insert data from the frontend, as long as you have RLS enabled.

For convenience, you can also use the Supabase client libraries, which wrap the Data APIs with a developer-friendly interface and automatically handle authentication:

The direct connection string connects directly to your Postgres instance. It is ideal for persistent servers, such as virtual machines (VMs) and long-lasting containers. Examples include AWS EC2 machines, Fly.io VMs, and DigitalOcean Droplets.

Direct connections use IPv6 by default. If your environment doesn't support IPv6, use Supavisor session mode or get the IPv4 add-on.

The connection string looks like this:

Get your project's direct connection string from your project dashboard by clicking Connect.

Every Supabase project includes a connection pooler. This is ideal for persistent servers when IPv6 is not supported.

The session mode connection string connects to your Postgres instance via a proxy. This is only recommended as an alternative to a Direct Connection, when connecting via an IPv4 network.

The connection string looks like this:

Get your project's Session pooler connection string from your project dashboard by clicking Connect.

The transaction mode connection string connects to your Postgres instance via a proxy which serves as a connection pooler. This is ideal for serverless or edge functions, which require many transient connections.

Transaction mode does not support prepared statements. To avoid errors, turn off prepared statements for your connection library.

The connection string looks like this:

Get your project's Transaction pooler connection string from your project dashboard by clicking Connect.

For paying customers, we provision a Dedicated Pooler (PgBouncer) that's co-located with your Postgres database. This will require you to connect with IPv6 or, if that's not an option, you can use the IPv4 add-on.

The Dedicated Pooler ensures best performance and latency, while using up more of your project's compute resources. If your network supports IPv6 or you have the IPv4 add-on, we encourage you to use the Dedicated Pooler over the Shared Pooler.

Get your project's Dedicated pooler connection string from your project dashboard by clicking Connect.

PgBouncer always runs in Transaction mode and the current version does not support prepared statement (will be added in a few weeks).

Connection pooling improves database performance by reusing existing connections between queries. This reduces the overhead of establishing connections and improves scalability.

You can use an application-side pooler or a server-side pooler (Supabase automatically provides one called Supavisor), depending on whether your backend is persistent or serverless.

Application-side poolers are built into connection libraries and API servers, such as Prisma, SQLAlchemy, and PostgREST. They maintain several active connections with Postgres or a server-side pooler, reducing the overhead of establishing connections between queries. When deploying to static architecture, such as long-standing containers or VMs, application-side poolers are satisfactory on their own.

Postgres connections are like a WebSocket. Once established, they are preserved until the client (application server) disconnects. A server might only make a single 10 ms query, but needlessly reserve its database connection for seconds or longer.

Serverside-poolers, such as Supabase's Supavisor in transaction mode, sit between clients and the database and can be thought of as load balancers for Postgres connections.

They maintain hot connections with the database and intelligently share them with clients only when needed, maximizing the amount of queries a single connection can service. They're best used to manage queries from auto-scaling systems, such as edge and serverless functions.

You should connect to your database using SSL wherever possible, to prevent snooping and man-in-the-middle attacks.

You can obtain your connection info and Server root certificate from your application's dashboard:

Below are answers to common challenges and queries.

A “Connection refused” error typically means your database isn’t reachable. Ensure your Supabase project is running, confirm your database’s connection string, check firewall settings, and validate network permissions.

This error occurs when your credentials are incorrect. Double-check your username and password from the Supabase dashboard. If the problem persists, reset your database password from the project settings.

Supabase’s default direct connection supports IPv6 only. To connect over IPv4, consider using the Supavisor session or transaction modes, or a connection pooler (shared or dedicated), which support both IPv4 and IPv6.

Your connection string is located in the Supabase Dashboard. Click the Connect button at the top of the page.

You can technically use both, but it’s not recommended unless you’re specifically trying to increase the total number of concurrent client connections. In most cases, it is better to choose either PgBouncer or Supavisor for pooled or transaction-based traffic. Direct connections remain the best choice for long-lived sessions, and, if IPv4 is required for those sessions, Supavisor session mode can be used as an alternative. Running both poolers simultaneously increases the risk of hitting your database’s maximum connection limit on smaller compute tiers.

Supavisor and PgBouncer work independently, but both reference the same pool size setting. For example, If you set the pool size to 30, Supavisor can open up to 30 server side connections to Postgres. These connections are shared between the session mode port (5432) and the transaction mode port (6543). Each mode can use up to 30 connections independently, or split them between both, but the total combined connections across both modes cannot exceed 30. PgBouncer can also open up to 30 connections under the same limit. If both poolers are active and reach their roles/modes limits at the same time, you could have as many as 60 backend connections hitting your database, in addition to any direct connections. You can adjust the pool size in Database settings in the dashboard.

There are two different limits to understand when working with poolers. The first is client connections, which refers to how many clients can connect to a pooler at the same time. This number is capped by your compute tier’s “max pooler clients” limit, and it applies independently to Supavisor and PgBouncer. The second is backend connections, which is the number of active connections a pooler opens to Postgres. This number is set by the pool size for that pooler.

The “max pooler clients” limit for your compute tier applies separately to Supavisor and PgBouncer. One pooler reaching its client limit does not affect the other. When a pooler reaches this limit, it stops accepting new client connections until existing ones are closed, but the other pooler remains unaffected. You can check your tier’s connection limits in the compute and disk limits documentation.

You can track connection usage from the Observability section in your project dashboard. There are three key reports:

Keep in mind that the Roles page is not real-time, it shows the connection count from the last refresh. If you need up-to-the-second data, set up Grafana or run the query against pg_stat_activity directly in SQL Editor. We have a few helpful queries for checking connections.

Even if your application isn’t making queries, some Supabase services keep persistent connections to your database. For example, Storage, PostgREST, and our health checker all maintain long-lived connections. You usually see a small baseline of active connections from these services.

Different modes use different ports:

The port helps route the connection to the right pooler/mode.

Because the dedicated pooler is hosted on the same machine as your database, it connects with lower latency than the shared pooler, which is hosted on a separate server. Direct connections have no pooler overhead but require IPv6 unless you have the IPv4 add-on.

Dedicated pooler (paid tier):

You can follow the decision flow in the connection method diagram to quickly choose the right option for your environment.

**Examples:**

Example 1 (unknown):
```unknown
1postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnopqrst.supabase.co:5432/postgres
```

Example 2 (unknown):
```unknown
1postgres://postgres.apbkobhfnmcqqzqeeqss:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

Example 3 (unknown):
```unknown
1postgres://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnopqrst.supabase.co:6543/postgres
```

Example 4 (unknown):
```unknown
1Total backend load on Postgres =2 Direct connections +3 Supavisor backend connections (≤ supavisor_pool_size) +4 PgBouncer backend connections (≤ pgbouncer_pool_size)5≤ Postgres max connections for your compute instance
```

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting?products=database

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-enable-database-webhook

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Database Migrations | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/database-migrations

**Contents:**
- Database Migrations
- How to manage schema migrations for your Supabase project.
- Schema migrations#
  - Create your first migration file
        - Terminal
  - Add the SQL to your migration file
        - supabase/migrations/<timestamp>_create_employees_table.sql
  - Apply your first migration
        - Terminal
  - Modify your employees table

How to manage schema migrations for your Supabase project.

Database migrations are SQL statements that create, update, or delete your existing database schemas. They are a common way of tracking changes to your database over time.

For this guide, we'll create a table called employees and see how we can make changes to it.

You will need to install the Supabase CLI and start the local development stack.

To get started, generate a new migration to store the SQL needed to create our employees table.

This creates a new migration file in supabase/migrations directory.

To that file, add the SQL to create this employees table.

Run this migration to create the employees table.

Now you can visit your new employees table in the local Dashboard.

Next, modify your employees table by adding a column for department.

To that new migration file, add the SQL to create a new department column.

Run this migration to update your existing employees table.

Finally, you should see the department column added to your employees table in the local Dashboard.

View the complete code for this example on GitHub.

Now that you are managing your database with migrations scripts, it would be great have some seed data to use every time you reset the database.

Create a seed script in supabase/seed.sql.

To that file, add the SQL to insert data into your employees table.

Reset your database to reapply migrations and populate with seed data.

You should now see the employees table, along with your seed data in the Dashboard! All of your database changes are captured in code, and you can reset to a known state at any time, complete with seed data.

This workflow is great if you know SQL and are comfortable creating tables and columns. If not, you can still use the Dashboard to create tables and columns, and then use the CLI to diff your changes and create migrations.

Create a new table called cities, with columns id, name and population.

Then generate a schema diff.

A new migration file is created for you.

Alternately, you can copy the table definitions directly from the Table Editor.

Test your new migration file by resetting your local database.

The last step is deploying these changes to a live Supabase project.

You've been developing your project locally, making changes to your tables via migrations. It's time to deploy your project to the Supabase Platform and start scaling up to millions of users!

Head over to Supabase and create a new project to deploy to.

Login to the Supabase CLI using an auto-generated Personal Access Token.

Link to your remote project by selecting from the on-screen prompt.

Push your migrations to the remote database.

Push your migrations and seed the remote database.

Visiting your live project on Supabase, you'll see a new employees table, complete with the department column you added in the second migration above.

**Examples:**

Example 1 (unknown):
```unknown
1supabase migration new create_employees_table
```

Example 2 (unknown):
```unknown
1create table if not exists employees (2  id bigint primary key generated always as identity,3  name text not null,4  email text,5  created_at timestamptz default now()6);
```

Example 3 (unknown):
```unknown
1supabase migration up
```

Example 4 (unknown):
```unknown
1supabase migration new add_department_column
```

---

## Full Text Search | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/full-text-search

**Contents:**
- Full Text Search
- How to use full text search in PostgreSQL.
- Preparation#
- Usage#
  - to_tsvector()#
  - to_tsquery()#
  - Match: @@#
- Basic full text queries#
  - Search a single column#
  - Search multiple columns#

How to use full text search in PostgreSQL.

Postgres has built-in functions to handle Full Text Search queries. This is like a "search engine" within Postgres.

For this guide we'll use the following example data:

The functions we'll cover in this guide are:

Converts your data into searchable tokens. to_tsvector() stands for "to text search vector." For example:

Collectively these tokens are called a "document" which Postgres can use for comparisons.

Converts a query string into tokens to match. to_tsquery() stands for "to text search query."

This conversion step is important because we will want to "fuzzy match" on keywords. For example if a user searches for eggs, and a column has the value egg, we probably still want to return a match.

Postgres provides several functions to create tsquery objects:

The @@ symbol is the "match" symbol for Full Text Search. It returns any matches between a to_tsvector result and a to_tsquery result.

Take the following example:

The equality symbol above (=) is very "strict" on what it matches. In a full text search context, we might want to find all "Harry Potter" books and so we can rewrite the example above:

To find all books where the description contain the word big:

Right now there is no direct way to use JavaScript or Dart to search through multiple columns but you can do it by creating computed columns on the database.

To find all books where description or title contain the word little:

To find all books where description contains BOTH of the words little and big, we can use the & symbol:

To find all books where description contain ANY of the words little or big, use the | symbol:

Notice how searching for big includes results with the word bigger (or biggest, etc).

Partial search is particularly useful when you want to find matches on substrings within your data.

You can use the :* syntax with to_tsquery(). Here's an example that searches for any book titles beginning with "Lit":

To make the partial search functionality accessible through the API, you can wrap the search logic in a stored procedure.

After creating this function, you can invoke it from your application using the SDK for your platform. Here's an example:

This function takes a prefix parameter and returns all books where the title contains a word starting with that prefix. The :* operator is used to denote a prefix match in the to_tsquery() function.

When you want the search term to include a phrase or multiple words, you can concatenate words using a + as a placeholder for space:

The websearch_to_tsquery() function provides an intuitive search syntax similar to popular web search engines, making it ideal for user-facing search interfaces.

Use quotes to search for exact phrases:

Use "or" (case-insensitive) to search for multiple terms:

Use a dash (-) to exclude terms:

Combine multiple operators for sophisticated searches:

Now that you have Full Text Search working, create an index. This allows Postgres to "build" the documents preemptively so that they don't need to be created at the time we execute the query. This will make our queries much faster.

Let's create a new column fts inside the books table to store the searchable index of the title and description columns.

We can use a special feature of Postgres called Generated Columns to ensure that the index is updated any time the values in the title and description columns change.

Now that we've created and populated our index, we can search it using the same techniques as before:

Visit Postgres: Text Search Functions and Operators to learn about additional query operators you can use to do more advanced full text queries, such as:

The proximity symbol is useful for searching for terms that are a certain "distance" apart. For example, to find the phrase big dreams, where the a match for "big" is followed immediately by a match for "dreams":

We can also use the <-> to find words within a certain distance of each other. For example to find year and school within 2 words of each other:

The negation symbol can be used to find phrases which don't contain a search term. For example, to find records that have the word big but not little:

Postgres provides ranking functions to sort search results by relevance, helping you present the most relevant matches first. Since ranking functions need to be computed server-side, use RPC functions and generated columns.

First, create a Postgres function that handles search and ranking:

Now you can call this function from your client:

Postgres allows you to assign different importance levels to different parts of your documents using weight labels. This is especially useful when you want matches in certain fields (like titles) to rank higher than matches in other fields (like descriptions).

Postgres uses four weight labels: A, B, C, and D, where:

First, create a weighted tsvector column that gives titles higher priority than descriptions:

Now create a search function that uses this weighted column:

You can also specify custom weights by providing a weight array to ts_rank():

This example uses custom weights where:

Say you search for "Harry". With weighted columns:

This ensures that books with "Harry" in the title ranks significantly higher than books that only mention "Harry" in the description, providing more relevant search results for users.

When using the fts column you created earlier, ranking becomes more efficient. Create a function that uses the indexed column:

You can also create a function that combines websearch_to_tsquery() with ranking for user-friendly search:

**Examples:**

Example 1 (unknown):
```unknown
1select to_tsvector('green eggs and ham');2-- Returns 'egg':2 'green':1 'ham':4
```

Example 2 (unknown):
```unknown
1select *2from books3where title = 'Harry';
```

Example 3 (unknown):
```unknown
1select *2from books3where to_tsvector(title) @@ to_tsquery('Harry');
```

Example 4 (unknown):
```unknown
1select2  *3from4  books5where6  to_tsvector(description)7  @@ to_tsquery('big');
```

---

## Converting SQL to JavaScript API | Supabase Docs

**URL:** https://supabase.com/docs/guides/api/sql-to-api

**Contents:**
- Converting SQL to JavaScript API
- Select statement with basic clauses#
- Select statement with complex Boolean logic clause#
- Resources#

Converting SQL to JavaScript API

Many common SQL queries can be written using the JavaScript API, provided by the SDK to wrap Data API calls. Below are a few examples of conversions between SQL and JavaScript patterns.

Select a set of columns from a single table with where, order by, and limit clauses.

Select all columns from a single table with a complex where clause: OR AND OR

Select all columns from a single table with a complex where clause: AND OR AND

**Examples:**

Example 1 (unknown):
```unknown
1select first_name, last_name, team_id, age2from players3where age between 20 and 24 and team_id != 'STL'4order by last_name, first_name desc5limit 20;
```

Example 2 (javascript):
```javascript
1const { data, error } = await supabase2  .from('players')3  .select('first_name,last_name,team_id,age')4  .gte('age', 20)5  .lte('age', 24)6  .not('team_id', 'eq', 'STL')7  .order('last_name', { ascending: true }) // or just .order('last_name')8  .order('first_name', { ascending: false })9  .limit(20)
```

Example 3 (unknown):
```unknown
1select *2from players3where ((team_id = 'CHN' or team_id is null) and (age > 35 or age is null));
```

Example 4 (javascript):
```javascript
1const { data, error } = await supabase2  .from('players')3  .select() // or .select('*')4  .or('team_id.eq.CHN,team_id.is.null')5  .or('age.gt.35,age.is.null') // additional filters imply "AND"
```

---

## Replication FAQ | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/replication/replication-faq

**Contents:**
- Replication FAQ
- Common questions and answers about replication.
      - Private Alpha
- What destinations are supported?#
- Why is a table not being replicated?#
- Why aren't publication changes reflected after adding or removing tables?#
- Why is a pipeline in failed state?#
- Why is a table in error state?#
- How to verify replication is working#
- How to stop or pause replication#

Common questions and answers about replication.

Replication is currently in private alpha. Access is limited and features may change.

Replication currently supports Analytics Buckets (Iceberg format) and BigQuery. See the destination tabs in the Setup guide for configuration details.

Availability varies based on the planned roll-out strategy. The destinations you can access depend on your project and access level.

Check your publication settings and verify your table meets the requirements.

After modifying your Postgres publication, you must restart the replication pipeline for changes to take effect. See Adding or removing tables for instructions.

Pipeline failures occur during the streaming phase when an error happens while replicating live data. This prevents data loss. To recover:

See Handling errors for more details.

Table errors occur during the copy phase. To recover, click View status, find the affected table, and reset the table state. This will restart the table copy from the beginning.

Check the Database → replication page:

See the Replication Monitoring guide for comprehensive monitoring instructions.

You can manage your pipeline using the actions menu in the destinations list. See Managing your pipeline for details on available actions.

Note: Stopping replication will cause changes to queue up in the WAL.

If a table is deleted downstream at the destination (e.g., in your Analytics Bucket or BigQuery dataset), the replication pipeline will automatically recreate it.

This behavior is by design to prevent the pipeline from breaking if tables are accidentally deleted. The pipeline ensures that all tables in your publication are always present at the destination.

To permanently remove a table from your destination:

You have two options:

Option 1: Pause the pipeline first

Option 2: Remove from publication first

Note: Removing a table from the publication and restarting the pipeline does not delete the table downstream, it only stops replicating new changes to it.

Yes, data duplicates can occur in certain scenarios when stopping a pipeline.

When you stop a pipeline (for restarts or updates), the replication process tries to finish processing any transactions that are currently being sent to your destination. It waits up to a few minutes to allow these in-progress transactions to complete cleanly before stopping.

However, if a transaction in your database takes longer than this waiting period to complete, the pipeline will stop before that entire transaction has been fully processed. When the pipeline starts again, it must restart the incomplete transaction from the beginning to maintain transaction boundaries, which results in some data being sent twice to your destination.

Understanding transaction boundaries: A transaction is a group of database changes that happen together (for example, all changes within a BEGIN...COMMIT block). Postgres logical replication must process entire transactions - it cannot process part of a transaction, stop, and then continue from the middle. This means if a transaction is interrupted, the whole transaction must be replayed when the pipeline resumes.

Example scenario: Suppose you have a batch operation that updates 10,000 rows within a single transaction. If this operation takes 10 minutes to complete and you stop the pipeline after 5 minutes (when 5,000 rows have been processed), the pipeline cannot resume from row 5,001. Instead, when it restarts, it must reprocess all 10,000 rows from the beginning, resulting in the first 5,000 rows being sent to your destination twice.

Important: There are currently no plans to implement automatic deduplication. If your use case requires guaranteed exactly-once delivery, you should implement deduplication logic in your downstream systems based on primary keys or other unique identifiers.

Navigate to Logs → Replication to see all pipeline logs. Logs contain diagnostic information. If you're experiencing issues, contact support with your error details.

If you need assistance:

---

## Supabase Docs

**URL:** https://supabase.com/docs/reference

**Contents:**
- API References
- Client Libraries
      - JavaScript
      - Flutter
      - C#
      - Swift
      - Kotlin
      - Python
- Management API and CLI
      - Management API

The Supabase client libraries help you interact with Supabase products, such as the Postgres Database, Auth, and Realtime. They are available in several popular programming languages.

Supabase also has a Management API to help with managing your Supabase Platform, and a CLI for local development and CI workflows.

---

## JavaScript: Call a Postgres function | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/rpc

---

## Integrating with Supabase Database (Postgres) | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/connect-to-postgres

**Contents:**
- Integrating with Supabase Database (Postgres)
- Connect to your Postgres database from Edge Functions.
- Using supabase-js#
- Using a Postgres client#
- Using Drizzle#
- SSL connections#
  - Production#
  - Local development#

Integrating with Supabase Database (Postgres)

Connect to your Postgres database from Edge Functions.

Connect to your Postgres database from an Edge Function by using the supabase-js client. You can also use other Postgres clients like Deno Postgres

The supabase-js client handles authorization with Row Level Security and automatically formats responses as JSON. This is the recommended approach for most applications:

Because Edge Functions are a server-side technology, it's safe to connect directly to your database using any popular Postgres client. This means you can run raw SQL from your Edge Functions.

Here is how you can connect to the database using Deno Postgres driver and run raw SQL. Check out the full example.

You can use Drizzle together with Postgres.js. Both can be loaded directly from npm:

Set up dependencies in import_map.json:

Use in your function:

You can find the full example on GitHub.

Deployed edge functions are pre-configured to use SSL for connections to the Supabase database. You don't need to add any extra configurations.

If you want to use SSL connections during local development, follow these steps:

Then, restart your local development server:

**Examples:**

Example 1 (python):
```python
1import { createClient } from 'npm:@supabase/supabase-js@2'23Deno.serve(async (req) => {4  try {5    const supabase = createClient(6      Deno.env.get('SUPABASE_URL') ?? '',7      Deno.env.get('SUPABASE_PUBLISHABLE_KEY') ?? '',8      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }9    )1011    const { data, error } = await supabase.from('countries').select('*')1213    if (error) {14      throw error15    }1617    return new Response(JSON.stringify({ data }), {18      headers: { 'Content-Type': 'application/json' },19      status: 200,20    })21  } catch (err) {22    return new Response(String(err?.message ?? err), { status: 500 })23  }24})
```

Example 2 (python):
```python
1import { Pool } from 'https://deno.land/x/postgres@v0.17.0/mod.ts'23// Create a database pool with one connection.4const pool = new Pool(5  {6    tls: { enabled: false },7    database: 'postgres',8    hostname: Deno.env.get('DB_HOSTNAME'),9    user: Deno.env.get('DB_USER'),10    port: 6543,11    password: Deno.env.get('DB_PASSWORD'),12  },13  114)1516Deno.serve(async (_req) => {17  try {18    // Grab a connection from the pool19    const connection = await pool.connect()2021    try {22      // Run a query23      const result = await connection.queryObject`SELECT * FROM animals`24      const animals = result.rows // [{ id: 1, name: "Lion" }, ...]2526      // Encode the result as pretty printed JSON27      const body = JSON.stringify(28        animals,29        (_key, value) => (typeof value === 'bigint' ? value.toString() : value),30        231      )3233      // Return the response with the correct content type header34      return new Response(body, {35        status: 200,36        headers: {37          'Content-Type': 'application/json; charset=utf-8',38        },39      })40    } finally {41      // Release the connection back into the pool42      connection.release()43    }44  } catch (err) {45    console.error(err)46    return new Response(String(err?.message ?? err), { status: 500 })47  }48})
```

Example 3 (unknown):
```unknown
1{2  "imports": {3    "drizzle-orm": "npm:drizzle-orm@0.29.1",4    "drizzle-orm/": "npm:/drizzle-orm@0.29.1/",5    "postgres": "npm:postgres@3.4.3"6  }7}
```

Example 4 (python):
```python
1import { drizzle } from 'drizzle-orm/postgres-js'2import postgres from 'postgres'3import { countries } from '../_shared/schema.ts'45const connectionString = Deno.env.get('SUPABASE_DB_URL')!67Deno.serve(async (_req) => {8  // Disable prefetch as it is not supported for "Transaction" pool mode9  const client = postgres(connectionString, { prepare: false })10  const db = drizzle(client)11  const allCountries = await db.select().from(countries)1213  return Response.json(allCountries)14})
```

---

## AWS Cognito | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/cognito

**Contents:**
- AWS Cognito
- Preparation#
  - Enable Wrappers#
  - Enable the Cognito Wrapper#
  - Store your credentials (optional)#
  - Connecting to Cognito#
  - Create a schema#
- Entities#
  - Users#
    - Operations#

You can enable the AWS Cognito wrapper right from the Supabase dashboard.

AWS Cognito is an identity platform for web and mobile apps.

The Cognito wrapper allows you to read data from your Cognito Userpool within your Postgres database.

Before you can query AWS Cognito, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the cognito_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers are designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to Cognito, and any additional options. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

We can use SQL import foreign schema to import foreign table definitions from Cognito.

For example, using below SQL can automatically create foreign table in the cognito schema.

The foreign table will be created as below:

This is an object representing Cognito User Records.

Ref: AWS Cognito User Records

This FDW doesn't support query pushdown.

This section describes important limitations and considerations when using this FDW:

This will create a "foreign table" inside your Postgres database called cognito_table:

You can now fetch your Cognito data from within your Postgres database:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper cognito_wrapper2  handler cognito_fdw_handler3  validator cognito_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Cognito secret access key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<secret access key>',4  'cognito',5  'Cognito secret key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server cognito_server2  foreign data wrapper cognito_wrapper3  options (4    aws_access_key_id '<your_access_key>',5    api_key_id '<your_secret_key_id_in_vault>',6    region '<your_aws_region>',7    user_pool_id '<your_user_pool_id>'8  );
```

---

## Migrate from MySQL to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/mysql

**Contents:**
- Migrate from MySQL to Supabase
- Migrate your MySQL database to Supabase Postgres database.
- Retrieve your MySQL database credentials#
- Retrieve your Supabase host #
- Migrate the database#
- Enterprise#

Migrate from MySQL to Supabase

Migrate your MySQL database to Supabase Postgres database.

This guide aims to exhibit the process of transferring your MySQL database to Supabase's Postgres database. Supabase is a robust and open-source platform offering a wide range of backend features, including a Postgres database, authentication, instant APIs, edge functions, real-time subscriptions, and storage. Migrating your MySQL database to Supabase's Postgres enables you to leverage PostgreSQL's capabilities and access all the features you need for your project.

Before you begin the migration, you need to collect essential information about your MySQL database. Follow these steps:

Log in to your MySQL database provider.

Locate and note the following database details:

If you're new to Supabase, create a project. Make a note of your password, you will need this later. If you forget it, you can reset it here.

On your project dashboard, click Connect

Under the Session pooler, click on the View parameters under the connect string. Note your Host ($SUPABASE_HOST).

The fastest way to migrate your database is with the Supabase migration tool on Google Colab.

Alternatively, you can use pgloader, a flexible and powerful data migration tool that supports a wide range of source database engines, including MySQL and MS SQL, and migrates the data to a Postgres database. For databases using the Postgres engine, we recommend using the pg_dump and psql command line tools, which are included in a full Postgres installation.

If you're planning to migrate a database larger than 6 GB, we recommend upgrading to at least a Large compute add-on. This will ensure you have the necessary resources to handle the migration efficiently.

We strongly advise you to pre-provision the disk space you will need for your migration. On paid projects, you can do this by navigating to the Compute and Disk Settings page. For more information on disk scaling and disk limits, check out our disk settings documentation.

Contact us if you need more help migrating your project.

---

## Firebase | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/firebase

**Contents:**
- Firebase
- Preparation#
  - Enable Wrappers#
  - Enable the Firebase Wrapper#
  - Store your credentials (optional)#
  - Connecting to Firebase#
  - Create a schema#
- Options#
- Entities#
  - Authentication Users#

You can enable the Firebase wrapper right from the Supabase dashboard.

Firebase is an app development platform built around non-relational technologies. The Firebase Wrapper supports connecting to below objects.

Before you can query Firebase, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the firebase_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to Firebase, and any additional options. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

object - Object name in Firebase, required.

For Authenciation users, the object name is fixed to auth/users. For Firestore documents, its format is firestore/<collection_id>, note that collection id must be a full path id. For example,

This is an object representing Firebase Authentication Users.

Ref: Firebase Authentication Users

This is an object representing Firestore Database Documents.

Ref: Firestore Database

This FDW doesn't support query pushdown.

This section describes important limitations and considerations when using this FDW:

Some examples on how to use Firebase foreign tables.

To map a Firestore collection provide its location using the format firestore/<collection_id> as the object option as shown below.

Note that name, created_at, and updated_at, are automatic metadata fields on all Firestore collections.

The auth/users collection is a special case with unique metadata. The following shows how to map Firebase users to PostgreSQL table.

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper firebase_wrapper2  handler firebase_fdw_handler3  validator firebase_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Firebase credentials in Vault and retrieve the created `key_id`2select vault.create_secret(3  '{4      "type": "service_account",5      "project_id": "your_gcp_project_id",6      ...7  }',8  'firebase',9  'Firebase API key for Wrappers'10);
```

Example 4 (unknown):
```unknown
1create server firebase_server2  foreign data wrapper firebase_wrapper3  options (4    sa_key_id '<key_ID>', -- The Key ID from above.5    project_id '<firebase_project_id>'6);
```

---

## Realtime Data Sync to Analytics Buckets | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/replication

**Contents:**
- Realtime Data Sync to Analytics Buckets
- Replicate your PostgreSQL data to analytics buckets in real-time.
      - This feature is in alpha
- How it works#
- Setup steps#
  - Step 1: Create an Analytics bucket#
  - Step 2: Create a publication#
  - Step 3: Create the replication pipeline#
- Monitoring your pipeline#
- Next steps#

Realtime Data Sync to Analytics Buckets

Replicate your PostgreSQL data to analytics buckets in real-time.

Expect rapid changes, limited features, and possible breaking updates. Share feedback as the experience is refined and access is expanded.

By combining replication powered by Supabase ETL with Analytics Buckets, you can build an end-to-end data warehouse solution that automatically syncs changes from your Postgres database to Iceberg tables.

This guide provides a quickstart for replicating to Analytics Buckets. For complete replication configuration including other destinations, see the Replication Setup Guide.

The replication pipeline captures changes (INSERT, UPDATE, DELETE) from your Postgres database in real-time using Postgres logical replication and writes them to your analytics bucket. This allows you to maintain an always-up-to-date data warehouse without impacting your production workloads.

First, create a new analytics bucket to store your replicated data:

A publication defines which tables and change types will be replicated. Create one using SQL in the Supabase SQL Editor:

This publication will track all changes (INSERT, UPDATE, DELETE) for the specified tables. For advanced publication options like column filtering and row predicates, see the Replication Setup Guide.

Now set up the pipeline to sync data to your analytics bucket:

Once started, you can monitor the pipeline status directly in the Database > Replication section:

Deleted tables are automatically recreated by the pipeline. To permanently delete a table, pause the pipeline first or remove it from the publication before deleting. See the FAQ for details.

Once data is flowing to your analytics bucket, you can:

For detailed replication configuration and advanced topics:

**Examples:**

Example 1 (unknown):
```unknown
1-- Create publication for tables you want to replicate2CREATE PUBLICATION pub_warehouse3  FOR TABLE users, orders, products;
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-postgres-upgrade-eligibility

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Securing your data | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/secure-data

**Contents:**
- Securing your data
- Connecting your app securely#
      - Never expose your service role key on the frontend
- More information#

Supabase helps you control access to your data. With access policies, you can protect sensitive data and make sure users only access what they're allowed to see.

Supabase allows you to access your database using the auto-generated Data APIs. This speeds up the process of building web apps, since you don't need to write your own backend services to pass database queries and results back and forth.

You can keep your data secure while accessing the Data APIs from the frontend, so long as you:

Your anon key is safe to expose with RLS enabled, because row access permission is checked against your access policies and the user's JSON Web Token (JWT). The JWT is automatically sent by the Supabase client libraries if the user is logged in using Supabase Auth.

Unlike your anon key, your service role key is never safe to expose because it bypasses RLS. Only use your service role key on the backend. Treat it as a secret (for example, import it as a sensitive environment variable instead of hardcoding it).

Supabase and Postgres provide you with multiple ways to manage security, including but not limited to Row Level Security. See the Access and Security pages for more information:

---

## Managing Enums in Postgres | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/enums

**Contents:**
- Managing Enums in Postgres
- Creating enums#
- When to use enums#
- Using enums in tables#
  - Inserting data with enums#
  - Querying data with enums#
- Managing enums#
  - Updating enum values#
  - Adding enum values#
  - Removing enum values#

Managing Enums in Postgres

Enums in Postgres are a custom data type. They allow you to define a set of values (or labels) that a column can hold. They are useful when you have a fixed set of possible values for a column.

You can define a Postgres Enum using the create type statement. Here's an example:

In this example, we've created an Enum called "mood" with four possible values.

There is a lot of overlap between Enums and foreign keys. Both can be used to define a set of values for a column. However, there are some advantages to using Enums:

There are also some disadvantages to using Enums:

In general you should only use Enums when the list of values is small, fixed, and unlikely to change often. Things like "a list of continents" or "a list of departments" are good candidates for Enums.

To use the Enum in a table, you can define a column with the Enum type. For example:

Here, the current_mood column can only have values from the "mood" Enum.

You can insert data into a table with Enum columns by specifying one of the Enum values:

When querying data, you can filter and compare Enum values as usual:

You can manage your Enums using the alter type statement. Here are some examples:

You can update the value of an Enum column:

To add new values to an existing Postgres Enum, you can use the ALTER TYPE statement. Here's how you can do it:

Let's say you have an existing Enum called mood, and you want to add a new value, content:

Even though it is possible, it is unsafe to remove enum values once they have been created. It's better to leave the enum value in place.

Read the Postgres mailing list for more information:

There is no ALTER TYPE DELETE VALUE in Postgres. Even if you delete every occurrence of an Enum value within a table (and vacuumed away those rows), the target value could still exist in upper index pages. If you delete the pg_enum entry you'll break the index.

Check your existing Enum values by querying the enum_range function:

**Examples:**

Example 1 (unknown):
```unknown
1create type mood as enum (2  'happy',3  'sad',4  'excited',5  'calm'6);
```

Example 2 (unknown):
```unknown
1create table person (2  id serial primary key,3  name text,4  current_mood mood5);
```

Example 3 (unknown):
```unknown
1insert into person2  (name, current_mood)3values4  ('Alice', 'happy');
```

Example 4 (unknown):
```unknown
1select * 2from person 3where current_mood = 'sad';
```

---

## Connecting with DBeaver | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/dbeaver

**Contents:**
- Connecting with DBeaver
  - Create a new database connection
  - Select PostgreSQL
  - Get Your Credentials
  - Fill out credentials
  - Download certificate
  - Secure your connection
  - Connect

Connecting with DBeaver

If you do not have DBeaver, you can download it from its website.

Create a new database connection

On your project dashboard, click Connect, note your session pooler's:

You will also need your database's password. If you forgot it, you can generate a new one in the settings.

If you're in an IPv6 environment or have the IPv4 Add-On, you can use the direct connection string instead of Supavisor in Session mode.

In DBeaver's Main menu, add your host, username, and password

In the Database Settings, download your SSL certificate.

In DBeaver's SSL tab, add your SSL certificate

Test your connection and then click finish. You should now be able to interact with your database with DBeaver

---

## LangChain | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/langchain

**Contents:**
- LangChain
- Initializing your database#
- Usage#
  - Simple metadata filtering#
  - Advanced metadata filtering#
- Hybrid search#
- Resources#

LangChain is a popular framework for working with AI, Vectors, and embeddings. LangChain supports using Supabase as a vector store, using the pgvector extension.

Prepare you database with the relevant tables:

You can now search your documents using any Node.js application. This is intended to be run on a secure server route.

Given the above match_documents Postgres function, you can also pass a filter parameter to only return documents with a specific metadata field value. This filter parameter is a JSON object, and the match_documents function will use the Postgres JSONB Containment operator @> to filter documents by the metadata field values you specify. See details on the Postgres JSONB Containment operator for more information.

You can also use query builder-style filtering (similar to how the Supabase JavaScript library works) instead of passing an object. Note that since the filter properties will be in the metadata column, you need to use arrow operators (-> for integer or ->> for text) as defined in PostgREST API documentation and specify the data type of the property (e.g. the column should look something like metadata->some_int_value::int).

LangChain supports the concept of a hybrid search, which combines Similarity Search with Full Text Search. Read the official docs to get started: Supabase Hybrid Search.

You can install the LangChain Hybrid Search function though our database.dev package manager.

**Examples:**

Example 1 (python):
```python
1import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase'2import { OpenAIEmbeddings } from '@langchain/openai'3import { createClient } from '@supabase/supabase-js'45const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY6if (!supabaseKey) throw new Error(`Expected SUPABASE_SERVICE_ROLE_KEY`)78const url = process.env.SUPABASE_URL9if (!url) throw new Error(`Expected env var SUPABASE_URL`)1011export const run = async () => {12  const client = createClient(url, supabaseKey)1314  const vectorStore = await SupabaseVectorStore.fromTexts(15    ['Hello world', 'Bye bye', "What's this?"],16    [{ id: 2 }, { id: 1 }, { id: 3 }],17    new OpenAIEmbeddings(),18    {19      client,20      tableName: 'documents',21      queryName: 'match_documents',22    }23  )2425  const resultOne = await vectorStore.similaritySearch('Hello world', 1)2627  console.log(resultOne)28}
```

Example 2 (python):
```python
1import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase'2import { OpenAIEmbeddings } from '@langchain/openai'3import { createClient } from '@supabase/supabase-js'45// First, follow set-up instructions above67const privateKey = process.env.SUPABASE_SERVICE_ROLE_KEY8if (!privateKey) throw new Error(`Expected env var SUPABASE_SERVICE_ROLE_KEY`)910const url = process.env.SUPABASE_URL11if (!url) throw new Error(`Expected env var SUPABASE_URL`)1213export const run = async () => {14  const client = createClient(url, privateKey)1516  const vectorStore = await SupabaseVectorStore.fromTexts(17    ['Hello world', 'Hello world', 'Hello world'],18    [{ user_id: 2 }, { user_id: 1 }, { user_id: 3 }],19    new OpenAIEmbeddings(),20    {21      client,22      tableName: 'documents',23      queryName: 'match_documents',24    }25  )2627  const result = await vectorStore.similaritySearch('Hello world', 1, {28    user_id: 3,29  })3031  console.log(result)32}
```

Example 3 (python):
```python
1import { SupabaseFilterRPCCall, SupabaseVectorStore } from '@langchain/community/vectorstores/supabase'2import { OpenAIEmbeddings } from '@langchain/openai'3import { createClient } from '@supabase/supabase-js'45// First, follow set-up instructions above67const privateKey = process.env.SUPABASE_SERVICE_ROLE_KEY8if (!privateKey) throw new Error(`Expected env var SUPABASE_SERVICE_ROLE_KEY`)910const url = process.env.SUPABASE_URL11if (!url) throw new Error(`Expected env var SUPABASE_URL`)1213export const run = async () => {14  const client = createClient(url, privateKey)1516  const embeddings = new OpenAIEmbeddings()1718  const store = new SupabaseVectorStore(embeddings, {19    client,20    tableName: 'documents',21  })2223  const docs = [24    {25      pageContent:26        'This is a long text, but it actually means something because vector database does not understand Lorem Ipsum. So I would need to expand upon the notion of quantum fluff, a theoretical concept where subatomic particles coalesce to form transient multidimensional spaces. Yet, this abstraction holds no real-world application or comprehensible meaning, reflecting a cosmic puzzle.',27      metadata: { b: 1, c: 10, stuff: 'right' },28    },29    {30      pageContent:31        'This is a long text, but it actually means something because vector database does not understand Lorem Ipsum. So I would need to proceed by discussing the echo of virtual tweets in the binary corridors of the digital universe. Each tweet, like a pixelated canary, hums in an unseen frequency, a fascinatingly perplexing phenomenon that, while conjuring vivid imagery, lacks any concrete implication or real-world relevance, portraying a paradox of multidimensional spaces in the age of cyber folklore.',32      metadata: { b: 2, c: 9, stuff: 'right' },33    },34    { pageContent: 'hello', metadata: { b: 1, c: 9, stuff: 'right' } },35    { pageContent: 'hello', metadata: { b: 1, c: 9, stuff: 'wrong' } },36    { pageContent: 'hi', metadata: { b: 2, c: 8, stuff: 'right' } },37    { pageContent: 'bye', metadata: { b: 3, c: 7, stuff: 'right' } },38    { pageContent: "what's this", metadata: { b: 4, c: 6, stuff: 'right' } },39  ]4041  await store.addDocuments(docs)4243  const funcFilterA: SupabaseFilterRPCCall = (rpc) =>44    rpc45      .filter('metadata->b::int', 'lt', 3)46      .filter('metadata->c::int', 'gt', 7)47      .textSearch('content', `'multidimensional' & 'spaces'`, {48        config: 'english',49      })5051  const resultA = await store.similaritySearch('quantum', 4, funcFilterA)5253  const funcFilterB: SupabaseFilterRPCCall = (rpc) =>54    rpc55      .filter('metadata->b::int', 'lt', 3)56      .filter('metadata->c::int', 'gt', 7)57      .filter('metadata->>stuff', 'eq', 'right')5859  const resultB = await store.similaritySearch('hello', 2, funcFilterB)6061  console.log(resultA, resultB)62}
```

---

## Declarative database schemas | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development/declarative-database-schemas

**Contents:**
- Declarative database schemas
- Manage your database schemas in one place and generate versioned migrations.
- Overview#
- Schema migrations#
  - Declaring your schema#
  - Create your first schema file
  - Generate a migration file
  - Start the local database and apply migrations
  - Updating your schema#
  - Add a new column

Declarative database schemas

Manage your database schemas in one place and generate versioned migrations.

Declarative schemas provide a developer-friendly way to maintain schema migrations.

Migrations are traditionally managed imperatively (you provide the instructions on how exactly to change the database). This can lead to related information being scattered over multiple migration files. With declarative schemas, you instead declare the state you want your database to be in, and the instructions are generated for you.

Schema migrations are SQL statements written in Data Definition Language. They are versioned in your supabase/migrations directory to ensure schema consistency between local and remote environments.

Create a SQL file in supabase/schemas directory that defines an employees table.

Generate a migration file by diffing against your declared schema.

Start the local database first. Then, apply the migration manually to see your schema changes in the local Dashboard.

Edit supabase/schemas/employees.sql file to add a new column to employees table.

Some entities like views and enums expect columns to be declared in a specific order. To avoid messy diffs, always append new columns to the end of the table.

Diff existing migrations against your declared schema.

Verify that the generated migration contain a single incremental change.

Start the database locally and apply the pending migration.

Log in via the Supabase CLI.

Follow the on-screen prompts to link your remote project.

Push your changes to the remote database.

As your database schema evolves, you will probably start using more advanced entities like views and functions. These entities are notoriously verbose to manage using plain migrations because the entire body must be recreated whenever there is a change. Using declarative schema, you can now edit them in-place so it’s much easier to review.

Your schema files are run in lexicographic order by default. The order is important when you have foreign keys between multiple tables as the parent table must be created first. For example, your supabase directory may end up with the following structure.

For small projects with only a few tables, the default schema order may be sufficient. However, as your project grows, you might need more control over the order in which schemas are applied. To specify a custom order for applying the schemas, you can declare them explicitly in config.toml. Any glob patterns will evaluated, deduplicated, and sorted in lexicographic order. For example, the following pattern ensures employees.sql is always executed first.

To set up declarative schemas on a existing project, you can pull in your production schema by running:

From there, you can start breaking down your schema into smaller files and generate migrations. You can do this all at once, or incrementally as you make changes to your schema.

During development, you may want to rollback a migration to keep your new schema changes in a single migration file. This can be done by resetting your local database to a previous version.

After a reset, you can edit the schema and regenerate a new migration file. Note that you should not reset a version that's already deployed to production.

If you need to rollback a migration that's already deployed, you should first revert changes to the schema files. Then you can generate a new migration file containing the down migration. This ensures your production migrations are always rolling forward.

SQL statements generated in a down migration are usually destructive. You must review them carefully to avoid unintentional data loss.

The migra diff tool used for generating schema diff is capable of tracking most database changes. However, there are edge cases where it can fail.

If you need to use any of the entities below, remember to add them through versioned migrations instead.

**Examples:**

Example 1 (unknown):
```unknown
1create table "employees" (2  "id" integer not null,3  "name" text4);
```

Example 2 (unknown):
```unknown
1supabase db diff -f create_employees_table
```

Example 3 (unknown):
```unknown
1supabase start2supabase migration up
```

Example 4 (unknown):
```unknown
1create table "employees" (2  "id" integer not null,3  "name" text,4  "age" smallint not null5);
```

---

## http: RESTful Client | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/http

**Contents:**
- http: RESTful Client
- Quick demo#
- Overview#
- Usage#
  - Enable the extension#
  - Available functions#
  - Returned values#
- Examples#
  - Simple GET example#
  - Simple POST example#

The http extension allows you to call RESTful endpoints within Postgres.

Let's cover some basic concepts:

You can use the http extension to make these network requests from Postgres.

While the main usage is http('http_request'), there are 5 wrapper functions for specific functionality:

A successful call to a web URL from the http extension returns a record with the following fields:

**Examples:**

Example 1 (unknown):
```unknown
1select2  "status", "content"::jsonb3from4  extensions.http_get('https://jsonplaceholder.typicode.com/todos/1');
```

Example 2 (unknown):
```unknown
1select2  "status", "content"::jsonb3from4  extensions.http_post(5    'https://jsonplaceholder.typicode.com/posts',6    '{ "title": "foo", "body": "bar", "userId": 1 }',7    'application/json'8  );
```

---

## Understanding Database and Disk Size | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/database-size

**Contents:**
- Understanding Database and Disk Size
- Database size#
  - Disk space usage#
  - Vacuum operations#
  - Preoccupied space#
- Disk size#
  - Paid plan behavior#
  - Free Plan behavior#
  - Read-only mode#
  - Disabling read-only mode#

Understanding Database and Disk Size

Disk metrics refer to the storage usage reported by Postgres. These metrics are updated daily. As you read through this document, we will refer to "database size" and "disk size":

Database size: Displays the actual size of the data within your Postgres database. This can be found on the Database Reports page.

Disk size: Shows the overall disk space usage, which includes both the database size and additional files required for Postgres to function like the Write Ahead Log (WAL) and other system log files. You can view this on the Database Settings page.

This SQL query will show the size of all databases in your Postgres cluster:

This value is reported in the database report page.

Database size is consumed primarily by your data, indexes, and materialized views. You can reduce your database size by removing any of these and running a Vacuum operation.

Depending on your billing plan, your database can go into read-only mode which can prevent you inserting and deleting data. There are instructions for managing read-only mode in the Disk Management section.

Your database size is part of the disk usage for your Supabase project, there are many components to Postgres that consume additional disk space. One of the primary components, is the Write Ahead Log (WAL). Postgres will store database changes in log files that are cleared away after they are applied to the database. These same files are also used by Read Replicas or other replication methods.

If you would like to determine the size of the WAL files stored on disk, Postgres provides pg_ls_waldir as a helper function; the following query can be run:

Postgres does not immediately reclaim the physical space used by dead tuples (i.e., deleted rows) in the DB. They are marked as "removed" until a vacuum operation is executed. As a result, deleting data from your database may not immediately reduce the reported disk usage. You can use the Supabase CLI inspect db bloat command to view all dead tuples in your database. Alternatively, you can run the query found in the CLI's GitHub repo in the SQL Editor

If you find a table you would like to immediately clean, you can run the following in the SQL Editor:

Vacuum operations can temporarily increase resource utilization, which may adversely impact the observed performance of your project until the maintenance is completed. The vacuum full command will lock the table until the operation concludes.

Supabase projects have automatic vacuuming enabled, which ensures that these operations are performed regularly to keep the database healthy and performant. It is possible to fine-tune the autovacuum parameters, or manually initiate vacuum operations. Running a manual vacuum after deleting large amounts of data from your DB could help reduce the database size reported by Postgres.

New Supabase projects have a database size of ~40-60mb. This space includes pre-installed extensions, schemas, and default Postgres data. Additional database size is used when installing extensions, even if those extensions are inactive.

Supabase uses network-attached storage to balance performance with scalability. The disk scaling behavior depends on your billing plan.

Projects on the Pro Plan and higher have auto-scaling disks.

Disk size expands automatically when the database reaches 90% of the allocated disk size. The disk is expanded to be 50% larger (for example, 8 GB -> 12 GB). Auto-scaling can only take place once every 6 hours. If within those 6 hours you reach 95% of the disk space, your project will enter read-only mode.

The automatic resize operation will add an additional 50% capped to a maximum of 200 GB. If 50% of your current usage is more than 200 GB then only 200 GB will be added to your disk (for example a size of 1500 GB will resize to 1700 GB).

Disk size can also be manually expanded on the Database Settings page. The maximum disk size for the Pro/Team Plan is 60 TB. If you need more than this, contact us to learn more about the Enterprise Plan.

You may want to import a lot of data into your database which requires multiple disk expansions. for example, uploading more than 1.5x the current size of your database storage will put your database into read-only mode. If so, it is highly recommended you increase the disk size manually on the Database Settings page.

Due to restrictions on the underlying cloud provider, disk expansions can occur only once every six hours. During the six hour cool down window, the disk cannot be resized again.

Free Plan projects enter read-only mode when you exceed the 500 MB limit. Once in read-only mode, you have these options:

In some cases Supabase may put your database into read-only mode to prevent your database from exceeding the billing or disk limitations.

In read-only mode, clients will encounter errors such as cannot execute INSERT in a read-only transaction. Regular operation (read-write mode) is automatically re-enabled once usage is below 95% of the disk size,

You manually override read-only mode to reduce disk size. To do this, run the following in the SQL Editor:

First, change the transaction access mode:

This allows you to delete data from within the session. After deleting data, consider running a vacuum to reclaim as much space as possible:

Once you have reclaimed space, you can run the following to disable read-only mode:

You can check the distribution of your disk size on your project's compute and disk page.

Your disk size usage falls in three categories:

Disks don't automatically downsize during normal operation. Once you have reduced your database size, they will automatically "right-size" during a project upgrade. The final disk size after the upgrade is 1.2x the size of the database with a minimum of 8 GB. For example, if your database size is 100GB, and you have a 200GB disk, the size after a project upgrade will be 120 GB.

In case you have a large WAL directory, you may modify WAL settings such as max_wal_size. Use at your own risk as changing these settings can have side effects. To query your current WAL size, use SELECT SUM(size) FROM pg_ls_waldir().

In the event that your project is already on the latest version of Postgres and cannot be upgraded, a new version of Postgres will be released approximately every week which you can then upgrade to once it becomes available.

**Examples:**

Example 1 (unknown):
```unknown
1select2  pg_size_pretty(sum(pg_database_size(pg_database.datname)))3from pg_database;
```

Example 2 (unknown):
```unknown
1select pg_size_pretty(sum(size)) as wal_size from pg_ls_waldir();
```

Example 3 (unknown):
```unknown
1# Login to the CLI2npx supabase login34# Initialize a local supabase directory5npx supabase init67# Link a project8npx supabase link910# Detect bloat11npx supabase inspect db bloat --linked
```

Example 4 (unknown):
```unknown
1vacuum full <table name>;
```

---

## Migrate from Vercel Postgres to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/vercel-postgres

**Contents:**
- Migrate from Vercel Postgres to Supabase
- Migrate your existing Vercel Postgres database to Supabase.
- Retrieve your Vercel Postgres database credentials #
- Set your OLD_DB_URL environment variable#
- Retrieve your Supabase connection string #
- Set your NEW_DB_URL environment variable#
- Migrate the database#
- Enterprise#

Migrate from Vercel Postgres to Supabase

Migrate your existing Vercel Postgres database to Supabase.

This guide demonstrates how to migrate your Vercel Postgres database to Supabase to get the most out of Postgres while gaining access to all the features you need to build a project.

Copy this part to your clipboard:

Set the OLD_DB_URL environment variable at the command line using your Vercel Postgres Database credentials.

If you're new to Supabase, create a project. Make a note of your password, you will need this later. If you forget it, you can reset it here.

On your project dashboard, click Connect

Under the Session pooler, click the Copy button to the right of your connection string to copy it to the clipboard.

Set the NEW_DB_URL environment variable at the command line using your Supabase connection string. You will need to replace [YOUR-PASSWORD] with your actual database password.

You will need the pg_dump and psql command line tools, which are included in a full Postgres installation.

Export your database to a file in console

Use pg_dump with your Postgres credentials to export your database to a file (e.g., dump.sql).

Import the database to your Supabase project

Use psql to import the Postgres database file to your Supabase project.

Run pg_dump --help for a full list of options.

If you're planning to migrate a database larger than 6 GB, we recommend upgrading to at least a Large compute add-on. This will ensure you have the necessary resources to handle the migration efficiently.

We strongly advise you to pre-provision the disk space you will need for your migration. On paid projects, you can do this by navigating to the Compute and Disk Settings page. For more information on disk scaling and disk limits, check out our disk settings documentation.

Contact us if you need more help migrating your project.

**Examples:**

Example 1 (unknown):
```unknown
1psql "postgres://default:xxxxxxxxxxxx@yy-yyyyy-yyyyyy-yyyyyyy.us-west-2.aws.neon.tech:5432/verceldb?sslmode=require"
```

Example 2 (unknown):
```unknown
1"postgres://default:xxxxxxxxxxxx@yy-yyyyy-yyyyyy-yyyyyyy.us-west-2.aws.neon.tech:5432/verceldb?sslmode=require"
```

Example 3 (unknown):
```unknown
1export OLD_DB_URL="postgres://default:xxxxxxxxxxxx@yy-yyyyy-yyyyyy-yyyyyyy.us-west-2.aws.neon.tech:5432/verceldb?sslmode=require"
```

Example 4 (unknown):
```unknown
1export NEW_DB_URL="postgresql://postgres.xxxxxxxxxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:5432/postgres"
```

---

## DuckDB | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/duckdb

**Contents:**
- DuckDB
- Preparation#
  - Enable Wrappers#
  - Enable the DuckDB Wrapper#
  - Store your credentials (optional)#
  - Connecting to DuckDB#
    - AWS S3#
    - AWS S3 Tables#
    - Cloudflare R2#
    - Cloudflare R2 Data Catalog#

DuckDB is an open-source column-oriented Relational Database Management System.

The DuckDB Wrapper allows you to read data from DuckDB within your Postgres database.

Before you can query DuckDB, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the duckdb_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

DuckDB can connect to many data sources, the credential to be saved in Vault depends on which data source you're going to use. For example, to store AWS credentials for S3 connection, you can run below SQL and note down the secret IDs returned:

We need to provide Postgres with the credentials to connect to DuckDB. We can do this using the create server command. Depends on the data source, there are different server options needs to be specified. Below is the list of supported data sources and their corresponding server options.

For any server options need to be stored in Vault, you can add a prefix vault_ to its name and use the secret ID returned from the select vault.create_secret() statement as the option value.

A create server statement example:

This s3 server type can also be used for other S3-compatible storage services such like Supabase Storage. For example,

A create server statement example:

This is to access Cloudflare R2 using the S3 Compatibility API.

A create server statement example:

This is to access Cloudflare R2 Data Catalog.

A create server statement example:

This is to access Apache Polaris Iceberg service.

A create server statement example:

This is to access Lakekeeper Iceberg service.

A create server statement example:

This is to access generic Iceberg services. Check above for other specific Iceberg services like S3 Tables, R2 Data Catalog and etc. All the S3 options are supported with below additional options.

Reading from Iceberg REST Catalogs backed by remote storage that is not S3 or S3 compatible is not supported yet.

A create server statement example used to access local Iceberg service:

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

This can also be a subquery enclosed in parentheses, for example,

or, an URI points to remote file or a function (with corresponding type of server),

We can use SQL import foreign schema to import foreign table definitions from DuckDB.

For example, using below SQL can automatically create foreign tables in the duckdb schema.

Currently only Iceberg-like servers, such as S3 Tables, R2 Data Catalog and etc., support import foreign schema without specifying source tables. For other types of servers, source tables must be explicitly specified in options. For example,

The imported table name format from Iceberg-like server is:

For example, the above statement will import a table name s3_tables_docs_example_guides.

For other types of server with explicitly specified sources tables, the imported foreign table names have the schema and sequence number as prefix with this format:

For example, by using belew statement,

The imported foreign table names are:

By default, the import foreign schema statement will silently skip all the incompatible columns. Use the option strict to prevent this behavior. For example,

This is an object representing DuckDB table.

You can manually create the foreign table like below if you did not use import foreign schema.

This FDW supports where, order by and limit clause pushdown.

This section describes important limitations and considerations when using this FDW:

First, create a s3 server:

Then import foreign table from a parquet file and query it:

This is the same as creating the foreign table manually like below,

First, create a s3_tables server:

Then, import all the tables in docs_example namespace and query it:

First, follow the steps in Getting Started Guide to create a R2 Catalog on Cloudflare. Once it is completed, create a r2_catalog server like below:

Then, import all the tables in default namespace and query it:

Follow the above Read R2 Data Catalog example, below are some query pushdown examples:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper duckdb_wrapper2  handler duckdb_fdw_handler3  validator duckdb_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your AWS credentials in Vault and retrieve the created2-- `aws_access_key_id` and `aws_secret_access_key`3select vault.create_secret(4  '<access key id>',  -- secret to be encrypted5  'aws_access_key_id',  -- secret name6  'AWS access key for Wrappers'  -- secret description7);8select vault.create_secret(9  '<secret access key>'10  'aws_secret_access_key',11  'AWS secret access key for Wrappers'12);
```

Example 4 (unknown):
```unknown
1create server duckdb_server2  foreign data wrapper duckdb_wrapper3  options (4    type 's3',56    -- The key id saved in Vault7    vault_key_id '<key_ID>',89    -- The secret saved in Vault10    vault_secret '<secret_key>',1112    -- AWS region13    region 'us-east-1'14  );
```

---

## postgres_fdw | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/postgres_fdw

**Contents:**
- postgres_fdw
- Enable the extension#
- Create a connection to another database#
  - Create a foreign server
  - Create a server mapping
  - Import tables
  - Query foreign table
  - Configuring execution options#
    - Fetch_size#
    - Batch_size#

The extension enables Postgres to query tables and views on a remote Postgres server.

Define the remote database address

Set the user credentials for the remote server

Import tables from the foreign database

Example: Import all tables from a schema

Example: Import specific tables

Maximum rows fetched per operation. For example, fetching 200 rows with fetch_size set to 100 requires 2 requests.

Maximum rows inserted per cycle. For example, inserting 200 rows with batch_size set to 100 requires 2 requests.

Lists shared extensions. Without them, queries involving unlisted extension functions or operators may fail or omit references.

For more server options, check the extension's official documentation

**Examples:**

Example 1 (unknown):
```unknown
1create server "<foreign_server_name>"2    foreign data wrapper postgres_fdw3    options (4        host '<host>',5        port '<port>',6        dbname '<dbname>'7    );
```

Example 2 (unknown):
```unknown
1create user mapping for "<dbname>"2server "<foreign_server_name>"3options (4    user '<db_user>',5    password '<password>'6);
```

Example 3 (python):
```python
1import foreign schema "<foreign_schema>"2from server "<foreign_server>"3into "<host_schema>";
```

Example 4 (python):
```python
1import foreign schema "<foreign_schema>"2limit to (3    "<table_name1>",4    "<table_name2>"5)6from server "<foreign_server>"7into "<host_schema>";
```

---

## RAG with Permissions | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/rag-with-permissions

**Contents:**
- RAG with Permissions
- Fine-grain access control with Retrieval Augmented Generation.
- Example#
- Alternative scenarios#
  - Documents owned by multiple people#
  - User and document data live outside of Supabase#
    - Direct Postgres connection#
    - Custom JWT with REST API#
  - Other scenarios#

Fine-grain access control with Retrieval Augmented Generation.

Since pgvector is built on top of Postgres, you can implement fine-grain access control on your vector database using Row Level Security (RLS). This means you can restrict which documents are returned during a vector similarity search to users that have access to them. Supabase also supports Foreign Data Wrappers (FDW) which means you can use an external database or data source to determine these permissions if your user data doesn't exist in Supabase.

Use this guide to learn how to restrict access to documents when performing retrieval augmented generation (RAG).

In a typical RAG setup, your documents are chunked into small subsections and similarity is performed over those sections:

Notice how we record the owner_id on each document. Let's create an RLS policy that restricts access to document_sections based on whether or not they own the linked document:

In this example, the current user is determined using the built-in auth.uid() function when the query is executed through your project's auto-generated REST API. If you are connecting to your Supabase database through a direct Postgres connection, see Direct Postgres Connection below for directions on how to achieve the same access control.

Now every select query executed on document_sections will implicitly filter the returned sections based on whether or not the current user has access to them.

For example, executing:

as an authenticated user will only return rows that they are the owner of (as determined by the linked document). More importantly, semantic search over these sections (or any additional filtering for that matter) will continue to respect these RLS policies:

The above example only configures select access to users. If you wanted, you could create more RLS policies for inserts, updates, and deletes in order to apply the same permission logic for those other operations. See Row Level Security for a more in-depth guide on RLS policies.

Every app has its own unique requirements and may differ from the above example. Here are some alternative scenarios we often see and how they are implemented in Supabase.

Instead of a one-to-many relationship between users and documents, you may require a many-to-many relationship so that multiple people can access the same document. Let's reimplement this using a join table:

Then your RLS policy would change to:

Instead of directly querying the documents table, we query the join table.

You may have an existing system that stores users, documents, and their permissions in a separate database. Let's explore the scenario where this data exists in another Postgres database. We'll use a foreign data wrapper (FDW) to connect to the external DB from within your Supabase DB:

RLS is latency-sensitive, so extra caution should be taken before implementing this method. Use the query plan analyzer to measure execution times for your queries to ensure they are within expected ranges. For enterprise applications, contact enterprise@supabase.io.

For data sources other than Postgres, see Foreign Data Wrappers for a list of external sources supported today. If your data lives in a source not provided in the list, contact support and we'll be happy to discuss your use case.

Let's assume your external DB contains a users and documents table like this:

In your Supabase DB, let's create foreign tables that link to the above tables:

This example maps the authenticated role in Supabase to the postgres user in the external DB. In production, it's best to create a custom user on the external DB that has the minimum permissions necessary to access the information you need.

On the Supabase DB, we use the built-in authenticated role which is automatically used when end users make authenticated requests over your auto-generated REST API. If you plan to connect to your Supabase DB over a direct Postgres connection instead of the REST API, you can change this to any user you like. See Direct Postgres Connection for more info.

We'll store document_sections and their embeddings in Supabase so that we can perform similarity search over them via pgvector.

We maintain a reference to the foreign document via document_id, but without a foreign key reference since foreign keys can only be added to local tables. Be sure to use the same ID data type that you use on your external documents table.

Since we're managing users and authentication outside of Supabase, we have two options:

You can directly connect to your Supabase Postgres DB using the connection info on a project page. To use RLS with this method, we use a custom session variable that contains the current user's ID:

The session variable is accessed through the current_setting() function. We name the variable app.current_user_id here, but you can modify this to any name you like. We also cast it to a bigint since that was the data type of the user.id column. Change this to whatever data type you use for your ID.

Now for every request, we set the user's ID at the beginning of the session:

Then all subsequent queries will inherit the permission of that user:

You might be tempted to discard RLS completely and simply filter by user within the where clause. Though this will work, we recommend RLS as a general best practice since RLS is always applied even as new queries and application logic is introduced in the future.

If you would like to use the auto-generated REST API to query your Supabase database using JWTs from an external auth provider, you can get your auth provider to issue a custom JWT for Supabase.

See the Clerk Supabase docs for an example of how this can be done. Modify the instructions to work with your own auth provider as needed.

Now we can use the same RLS policy from our first example:

Under the hood, auth.uid() references current_setting('request.jwt.claim.sub') which corresponds to the JWT's sub (subject) claim. This setting is automatically set at the beginning of each request to the REST API.

All subsequent queries will inherit the permission of that user:

There are endless approaches to this problem based on the complexities of each system. Luckily Postgres comes with all the primitives needed to provide access control in the way that works best for your project.

If the examples above didn't fit your use case or you need to adjust them slightly to better fit your existing system, feel free to reach out to support and we'll be happy to assist you.

**Examples:**

Example 1 (unknown):
```unknown
1-- Track documents/pages/files/etc2create table documents (3  id bigint primary key generated always as identity,4  name text not null,5  owner_id uuid not null references auth.users (id) default auth.uid(),6  created_at timestamp with time zone not null default now()7);89-- Store the content and embedding vector for each section in the document10-- with a reference to original document (one-to-many)11create table document_sections (12  id bigint primary key generated always as identity,13  document_id bigint not null references documents (id),14  content text not null,15  embedding extensions.vector (384)16);
```

Example 2 (unknown):
```unknown
1-- enable row level security2alter table document_sections enable row level security;34-- setup RLS for select operations5create policy "Users can query their own document sections"6on document_sections for select to authenticated using (7  document_id in (8    select id9    from documents10    where (owner_id = (select auth.uid()))11  )12);
```

Example 3 (unknown):
```unknown
1select * from document_sections;
```

Example 4 (unknown):
```unknown
1-- Perform inner product similarity based on a match_threshold2select *3from document_sections4where document_sections.embedding <#> embedding < -match_threshold5order by document_sections.embedding <#> embedding;
```

---

## Subscribing to Database Changes | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/subscribing-to-database-changes

**Contents:**
- Subscribing to Database Changes
- Listen to database changes in real-time from your website or application.
- Using Broadcast#
  - Broadcast authorization#
  - Create a trigger function#
  - Create a trigger#
    - Listening on client side#
- Using Postgres Changes#
  - Enable Postgres Changes#
  - Streaming inserts#

Subscribing to Database Changes

Listen to database changes in real-time from your website or application.

You can use Supabase to subscribe to real-time database changes. There are two options available:

To automatically send messages when a record is created, updated, or deleted, we can attach a Postgres trigger to any table. Supabase Realtime provides a realtime.broadcast_changes() function which we can use in conjunction with a trigger. This function will use a private channel and needs broadcast authorization RLS policies to be met.

Realtime Authorization is required for receiving Broadcast messages. This is an example of a policy that allows authenticated users to listen to messages from topics:

Let's create a function that we can call any time a record is created, updated, or deleted. This function will make use of some of Postgres's native trigger variables. For this example, we want to have a topic with the name topic:<record id> to which we're going to broadcast events.

Let's set up a trigger so the function is executed after any changes to the table.

Finally, on the client side, listen to the topic topic:<record_id> to receive the events. Remember to set the channel as a private channel, since realtime.broadcast_changes uses Realtime Authorization.

Postgres Changes are simple to use, but have some limitations as your application scales. We recommend using Broadcast for most use cases.

You'll first need to create a supabase_realtime publication and add your tables (that you want to subscribe to) to the publication:

You can use the INSERT event to stream all new rows.

You can use the UPDATE event to stream all updated rows.

**Examples:**

Example 1 (unknown):
```unknown
1create policy "Authenticated users can receive broadcasts"2on "realtime"."messages"3for select4to authenticated5using ( true );
```

Example 2 (unknown):
```unknown
1create or replace function public.your_table_changes()2returns trigger3security definer4language plpgsql5as $$6begin7  perform realtime.broadcast_changes(8    'topic:' || coalesce(NEW.id, OLD.id) ::text,       -- topic - the topic to which you're broadcasting where you can use the topic id to build the topic name9    TG_OP,                                             -- event - the event that triggered the function10    TG_OP,                                             -- operation - the operation that triggered the function11    TG_TABLE_NAME,                                     -- table - the table that caused the trigger12    TG_TABLE_SCHEMA,                                   -- schema - the schema of the table that caused the trigger13    NEW,                                               -- new record - the record after the change14    OLD                                                -- old record - the record before the change15  );16  return null;17end;18$$;
```

Example 3 (unknown):
```unknown
1create trigger handle_your_table_changes2after insert or update or delete3on public.your_table4for each row5execute function your_table_changes ();
```

Example 4 (javascript):
```javascript
1const gameId = 'id'2await supabase.realtime.setAuth() // Needed for Realtime Authorization3const changes = supabase4  .channel(`topic:${gameId}`, {5    config: { private: true },6  })7  .on('broadcast', { event: 'INSERT' }, (payload) => console.log(payload))8  .on('broadcast', { event: 'UPDATE' }, (payload) => console.log(payload))9  .on('broadcast', { event: 'DELETE' }, (payload) => console.log(payload))10  .subscribe()
```

---

## AWS S3 Vectors | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/s3_vectors

**Contents:**
- AWS S3 Vectors
- Preparation#
  - Enable Wrappers#
  - Enable the S3 Vectors Wrapper#
  - Store your credentials (optional)#
  - Connecting to S3 Vectors#
  - Create a schema#
- Options#
- Entities#
  - S3 Vector Tables#

You can enable the AWS S3 Vectors wrapper right from the Supabase dashboard.

AWS S3 Vectors is a managed service that stores and queries high-dimensional vectors at scale, optimized for machine learning and artificial intelligence applications.

The S3 Vectors Wrapper allows you to read, write, and perform vector similarity search operations on S3 Vectors within your Postgres database.

Before you can query S3 Vectors, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the s3_vectors_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to S3 Vectors. We can do this using the create server command.

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

We can use SQL import foreign schema to import foreign table definitions from S3 Vectors.

For example, using below SQL can automatically create foreign tables in the s3_vectors schema.

This is an object representing S3 Vector index.

Ref: S3 Vectors API Reference

You can also manually create the foreign table like below if you did not use import foreign schema.

The embd type is a custom PostgreSQL data type designed to store and work with high-dimensional vectors for machine learning and AI applications.

The embd type internally contains:

The embd type accepts input in JSON array format:

When displayed, the embd type shows a summary format:

See the following sections for complete examples:

Returns the distance score from the most recent vector similarity search operation.

This FDW supports limited query pushdown with specific operators based on the type of operation:

For approximate nearest neighbor search using the <==> operator:

Metadata Filtering Syntax:

The json_filter uses S3 Vectors metadata filtering expressions with the following operators:

For more details on metadata filtering syntax, see the AWS S3 Vectors metadata filtering documentation.

For exact key lookups:

List all vectors (no WHERE clause):

Get a specific vector by key:

Vector similarity search:

Vector search with metadata filtering:

Only above specific query patterns are supported. Complex queries with unsupported operators or combinations may result in errors.

This section describes important limitations and considerations when using this FDW:

First, create a server for S3 Vectors:

Import the foreign table:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper s3_vectors_wrapper2  handler s3_vectors_fdw_handler3  validator s3_vectors_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your AWS credentials in Vault and retrieve the created2-- `vault_access_key_id` and `vault_secret_access_key`3select vault.create_secret(4  '<access key id>',  -- secret to be encrypted5  'vault_access_key_id',  -- secret name6  'AWS access key for Wrappers'  -- secret description7);8select vault.create_secret(9  '<secret access key>',10  'vault_secret_access_key',11  'AWS secret access key for Wrappers'12);
```

Example 4 (unknown):
```unknown
1create server s3_vectors_server2  foreign data wrapper s3_vectors_wrapper3  options (4    -- The key id saved in Vault from above5    vault_access_key_id '<key_ID>',67    -- The secret id saved in Vault from above8    vault_secret_access_key '<secret_key>',910    -- AWS region11    aws_region 'us-east-1',1213    -- Optional: Custom endpoint URL for alternative S3 services14    endpoint_url 'http://localhost:8080'15  );
```

---

## Troubleshooting prisma errors | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/prisma/prisma-troubleshooting

**Contents:**
- Troubleshooting prisma errors
- Understanding connection string parameters: #
- Errors
- ... prepared statement already exists#
  - Solution: #
- Can't reach database server at:#
  - Possible causes: #
  - Solutions: #
- Timed out fetching a new connection from the connection pool:#
  - Possible causes: #

Troubleshooting prisma errors

This guide addresses common Prisma errors that you might encounter while using Supabase.

A full list of errors can be found in Prisma's official docs.

Unlike other libraries, Prisma lets you configure its settings through special options appended to your connection string.

These options, called "query parameters," can be used to address specific errors.

Supavisor in transaction mode (port 6543) does not support prepared statements, which Prisma will try to create in the background.

Prisma couldn't establish a connection with Postgres or Supavisor before the timeout

Prisma is unable to allocate connections to pending queries fast enough to meet demand.

According to this GitHub Issue for Prisma, this error may be related to large return values for queries. It may also be caused by significant database strain.

Prisma relies on migration files to ensure your database aligns with Prisma's model. External schema changes are detected as "drift", which Prisma will try to overwrite, potentially causing data loss.

Postgres or Supavisor rejected a request for more connections

A Prisma migration is referencing a schema it is not permitted to manage.

An alternative strategy to reference these tables is to duplicate values into Prisma managed table with triggers. Below is an example for duplicating values from auth.users into a table called profiles.

**Examples:**

Example 1 (unknown):
```unknown
1# Example of query parameters23connection_string.../postgres?KEY1=VALUE&KEY2=VALUE&KEY3=VALUE
```

Example 2 (unknown):
```unknown
1.../postgres?pgbouncer=true
```

Example 3 (unknown):
```unknown
1.../postgres?connect_timeout=30
```

Example 4 (unknown):
```unknown
1generator client {2  provider        = "prisma-client-js"3  previewFeatures = ["multiSchema"]  //Add line4}56datasource db {7  provider  = "postgresql"8  url       = env("DATABASE_URL")9  directUrl = env("DIRECT_URL")10  schemas   = ["public", "other_schema"] //list out relevant schemas11}
```

---

## uuid-ossp: Unique Identifiers | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/uuid-ossp

**Contents:**
- uuid-ossp: Unique Identifiers
- Overview#
- Enable the extension#
- The uuid type#
- uuid_generate_v1()#
- uuid_generate_v4()#
- Examples#
  - Within a query#
  - As a primary key#
- Resources#

uuid-ossp: Unique Identifiers

The uuid-ossp extension can be used to generate a UUID.

A UUID is a "Universally Unique Identifier" and it is, for practical purposes, unique. This makes them particularly well suited as Primary Keys. It is occasionally referred to as a GUID, which stands for "Globally Unique Identifier".

Note: Currently uuid-ossp extension is enabled by default and cannot be disabled.

Once the extension is enabled, you now have access to a uuid type.

Creates a UUID value based on the combination of computer’s MAC address, current timestamp, and a random value.

UUIDv1 leaks identifiable details, which might make it unsuitable for certain security-sensitive applications.

Creates UUID values based solely on random numbers. You can also use Postgres's built-in gen_random_uuid() function to generate a UUIDv4.

Automatically create a unique, random ID in a table:

**Examples:**

Example 1 (unknown):
```unknown
1select uuid_generate_v4();
```

Example 2 (unknown):
```unknown
1create table contacts (2  id uuid default uuid_generate_v4(),3  first_name text,4  last_name text,5  primary key (id)6);
```

---

## Redis | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/redis

**Contents:**
- Redis
- Preparation#
  - Enable Wrappers#
  - Enable the Redis Wrapper#
  - Store your credentials (optional)#
  - Connecting to Redis#
  - Create a schema#
- Options#
- Entities#
  - List#

You can enable the Redis wrapper right from the Supabase dashboard.

Redis is an open-source in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.

The Redis Wrapper allows you to read data from Redis within your Postgres database.

Before you can query Redis, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the redis_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

To connect to Redis over SSL/TLS, you can use rediss:// protocol. For example,

We need to provide Postgres with the credentials to connect to Redis. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The following options are available when creating Redis foreign tables:

This can be one of below types,

This key can be a pattern for multi_* type of foreign table. For other types, this key must return exact one value. For example,

This is an object representing a Redis List.

This is an object representing a Redis Set.

This is an object representing a Redis Hash.

This is an object representing a Redis Sorted Set.

This is an object representing a Redis Stream.

Redis wrapper supports querying multiple objects of the same type using pattern matching.

This FDW doesn't support pushdown.

All Redis values will be stored as text or jsonb columns in Postgres, below are the supported Redis data types:

This section describes important limitations and considerations when using this FDW:

Some examples on how to use Redis foreign tables.

Let's prepare some source data in Redis CLI first:

This example will create foreign tables inside your Postgres database and query their data:

This example will create several foreign tables using pattern in key and query multiple objects from Redis:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper redis_wrapper2  handler redis_fdw_handler3  validator redis_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Redis connection URL in Vault and retrieve the created `key_id`2select vault.create_secret(3  'redis://username:password@127.0.0.1:6379/db',4  'redis',5  'Redis connection URL for Wrappers'6);
```

Example 4 (unknown):
```unknown
1rediss://username:password@my-redis-12345.upstash.io:6379/#insecure
```

---

## Column Level Security | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/column-level-security

**Contents:**
- Column Level Security
- Policies at the row level#
- Privileges at the column level#
- Manage column privileges in the Dashboard#
- Manage column privileges in migrations#
  - Create a migration file
  - Add the SQL to your migration file
- Considerations when using column-level privileges#

Column Level Security

PostgreSQL's Row Level Security (RLS) gives you granular control over who can access rows of data. However, it doesn't give you control over which columns they can access within rows. Sometimes you want to restrict access to specific columns in your database. Column Level Privileges allows you to do just that.

This is an advanced feature. We do not recommend using column-level privileges for most users. Instead, we recommend using RLS policies in combination with a dedicated table for handling user roles.

Restricted roles cannot use the wildcard operator (*) on the affected table. Instead of using SELECT * FROM <restricted_table>; or its API equivalent, you must specify the column names explicitly.

Policies in Row Level Security (RLS) are used to restrict access to rows in a table. Think of them like adding a WHERE clause to every query.

For example, let's assume you have a posts table with the following columns:

You can restrict updates to just the user who created it using RLS, with the following policy:

However, this gives the post owner full access to update the row, including all of the columns.

To restrict access to columns, you can use Privileges.

There are two types of privileges in Postgres:

You can have both types of privileges on the same table. If you have both, and you revoke the column-level privilege, the table-level privilege will still be in effect.

By default, our table will have a table-level UPDATE privilege, which means that the authenticated role can update all the columns in the table.

In the above example, we are revoking the table-level UPDATE privilege from the authenticated role and granting a column-level UPDATE privilege on just the title and content columns.

If we want to restrict access to updating the title column:

This time, we are revoking the column-level UPDATE privilege of the title column from the authenticated role. We didn't need to revoke the table-level UPDATE privilege because it's already revoked.

Column-level privileges are a powerful tool, but they're also quite advanced and in many cases, not the best fit for common access control needs. For that reason, we've intentionally moved the UI for this feature under the Feature Preview section in the dashboard.

You can view and edit the privileges in the Supabase Studio.

While you can manage privileges directly from the Dashboard, as your project grows you may want to manage them in your migrations. Read about database migrations in the Local Development guide.

To get started, generate a new migration to store the SQL needed to create your table along with row and column-level privileges.

This creates a new migration: supabase/migrations/<timestamp> _create_posts_table.sql.

To that file, add the SQL to create this posts table with row and column-level privileges.

**Examples:**

Example 1 (unknown):
```unknown
1create policy "Allow update for owners" on posts for2update3  using ((select auth.uid()) = user_id);
```

Example 2 (unknown):
```unknown
1revoke2update3  on table public.posts4from5  authenticated;67grant8update9  (title, content) on table public.posts to authenticated;
```

Example 3 (unknown):
```unknown
1revoke2update3  (title) on table public.posts4from5  authenticated;
```

Example 4 (unknown):
```unknown
1supabase migration new create_posts_table
```

---

## Supabase Docs | Troubleshooting | How to change max database connections

**URL:** https://supabase.com/docs/guides/troubleshooting/how-to-change-max-database-connections-_BQ8P5

**Contents:**
- How to change max database connections
- Changing max database connections:
- Configuring direct connections limits#
- Dangers of increasing the direct connection limits
  - Process schedulers and Postgres internals:#
  - Memory#
    - Each direct connection is a running process that will consume active memory#
  - CPU#
- Metadata
  - Products

Last edited: 9/9/2025

WARNING: Manually configuring the connection count hard codes it. This means if you upgrade or downgrade your database, the connection count will not auto-resize. You will have to make sure to manually update it.

Each compute instance has a default direct connection and pooler connection settings. You can find the most recent settings in the compute docs:

Note: the Supavisor connection limits are hard-coded and cannot be changed without upgrading the compute size:

You can configure the maximum amount of connections that Postgres will tolerate with the Supabase CLI.

You can run the following commands:

Then you could run the following SQL in the SQL Editor to see if the changes went through:

Three factors must be taken into consideration when adjusting the direct connection limit:

Allowing too many direct connections in your database can overburden Postgres schedulers and other internal modules. This will result in a noticeable decrease in query throughput, despite having more connections available. EnterpriseDB wrote a wonderful article that outlines some of the considerations.

The default connection values are set based on a solid understanding of Postgres architecture, and straying too far from them is likely to hinder performance. However, with some experimentation, you might discover a value better suited to your specific needs. Still, unless there's a compelling reason to adjust the setting, it's generally advisable to stick with the defaults or change the values judiciously.'

If you do not know how to monitor memory and CPU with Supabase Grafana, check here.

This is a Grafana Chart of unhealthy memory usage:

The cache in Postgres is important because the database will store frequently accessed data in it for rapid retrieval. If too much active memory is needed, it runs the risk of excessively displacing cache. This will force queries to check disk, which is slow.

Most data in a database is idle. However, when there is little available memory or uncached data is rapidly accessed, thrashing can occur.

To avoid displacing cache or straining system resources, it is advised to not increase your direct connections unless you have a clear excess of unclaimed memory (green).

Postgres will allow you to overcommit memory. You can run the below query to find out the hypothetical max value you could change it to without risking memory failure:

NOTE: You can find your server memory in the compute add-ons docs

The below chart is an example of what can occur to the CPU if 100s of connections are inappropriately opened/closed every second or many CPU intensive queries are run in parallel

If you plan on increasing your direct connection numbers, your database should have relatively predictable or low CPU usage, such as what the example displays below:

**Examples:**

Example 1 (unknown):
```unknown
1npx supabase login23npx supabase --experimental --project-ref <PROJECT REF> postgres-config update --config max_connections=<INTEGER VALUE>
```

Example 2 (unknown):
```unknown
1SHOW max_connections;
```

Example 3 (unknown):
```unknown
1select2  '(SERVER MEMORY - ' || current_setting('shared_buffers') || ' - (' || current_setting(3    'autovacuum_max_workers'4  ) || ' * ' || current_setting('maintenance_work_mem') || ')) / ' || current_setting('work_mem');
```

---

## REST API | Supabase Docs

**URL:** https://supabase.com/docs/guides/api

**Contents:**
- REST API
- Features #
- API URL and keys#

Supabase auto-generates an API directly from your database schema allowing you to connect to your database through a restful interface, directly from the browser.

The API is auto-generated from your database and is designed to get you building as fast as possible, without writing a single line of code.

You can use them directly from the browser (two-tier architecture), or as a complement to your own API server (three-tier architecture).

Supabase provides a RESTful API using PostgREST. This is a very thin API layer on top of Postgres. It exposes everything you need from a CRUD API at the URL https://<project_ref>.supabase.co/rest/v1/.

The REST interface is automatically reflected from your database's schema and is:

The reflected API is designed to retain as much of Postgres' capability as possible including:

The REST API resolves all requests to a single SQL statement leading to fast response times and high throughput.

You can find the API URL and Keys in the Dashboard.

---

## Vault | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/vault

**Contents:**
- Vault
- Managing secrets in Postgres.
- Using Vault#
  - Adding secrets#
  - Viewing secrets#
  - Updating secrets#
- Deep dive#
  - Authenticated encryption with associated data#
  - Encryption key location#
  - Resources#

Managing secrets in Postgres.

Vault is a Postgres extension and accompanying Supabase UI that makes it safe and easy to store encrypted secrets and other data in your database. This opens up a lot of possibilities to use Postgres in ways that go beyond what is available in a stock distribution.

Under the hood, the Vault is a table of Secrets that are stored using Authenticated Encryption on disk. They are then available in decrypted form through a Postgres view so that the secrets can be used by applications from SQL. Because the secrets are stored on disk encrypted and authenticated, any backups or replication streams also preserve this encryption in a way that can't be decrypted or forged.

Supabase provides a dashboard UI for the Vault that makes storing secrets easy. Click a button, type in your secret, and save.

You can use Vault to store secrets - everything from Environment Variables to API Keys. You can then use these secrets anywhere in your database: Postgres Functions, Triggers, and Webhooks. From a SQL perspective, accessing secrets is as easy as querying a table (or in this case, a view). The underlying secrets tables will be stored in encrypted form.

You can manage secrets from the UI or using SQL.

There is also a handy function for creating secrets called vault.create_secret():

The function returns the UUID of the new secret.

Secrets can also have an optional unique name and an optional description. These are also arguments to vault.create_secret():

If you look in the vault.secrets table, you will see that your data is stored encrypted. To decrypt the data, there is an automatically created view vault.decrypted_secrets. This view will decrypt secret data on the fly:

Notice how this view has a decrypted_secret column that contains the decrypted secrets. Views are not stored on disk, they are only run at query time, so the secret remains encrypted on disk, and in any backup dumps or replication streams.

You should ensure that you protect access to this view with the appropriate SQL privilege settings at all times, as anyone that has access to the view has access to decrypted secrets.

A secret can be updated with the vault.update_secret() function, this function makes updating secrets easy, just provide the secret UUID as the first argument, and then an updated secret, updated optional unique name, or updated description:

As we mentioned, Vault uses Transparent Column Encryption (TCE) to store secrets in an authenticated encrypted form. There are some details around that you may be curious about. What does authenticated mean? Where is the encryption key stored? This section explains those details.

The first important feature of TCE is that it uses an Authenticated Encryption with Associated Data encryption algorithm (based on libsodium).

Authenticated Encryption means that in addition to the data being encrypted, it is also signed so that it cannot be forged. You can guarantee that the data was encrypted by someone you trust, which you wouldn't get with encryption alone. The decryption function verifies that the signature is valid before decrypting the value.

Associated Data means that you can include any other columns from the same row as part of the signature computation. This doesn't encrypt those other columns - rather it ensures that your encrypted value is only associated with columns from that row. If an attacker were to copy an encrypted value from another row to the current one, the signature would be rejected (assuming you used a unique column in the associated data).

Another important feature is that the encryption key is never stored in the database alongside the encrypted data. Even if an attacker can capture a dump of your entire database, they will see only encrypted data, never the encryption key itself.

This is an important safety precaution - there is little value in storing the encryption key in the database itself as this would be like locking your front door but leaving the key in the lock! Storing the key outside the database fixes this issue.

Where is the key stored? Supabase creates and manages the encryption key in our secured backend systems. We keep this key safe and separate from your data. You remain in control of your key - a separate API endpoint is available that you can use to access the key if you want to decrypt your data outside of Supabase.

Which roles should have access to the vault.secrets table should be carefully considered. There are two ways to grant access, the first is that the postgres user can explicitly grant access to the vault table itself.

**Examples:**

Example 1 (unknown):
```unknown
1select vault.create_secret('my_s3kre3t');
```

Example 2 (unknown):
```unknown
1-[ RECORD 1 ]-+-------------------------------------2create_secret | c9b00867-ca8b-44fc-a81d-d20b8169be17
```

Example 3 (unknown):
```unknown
1select vault.create_secret('another_s3kre3t', 'unique_name', 'This is the description');
```

Example 4 (unknown):
```unknown
1-[ RECORD 1 ]-----------------------------------------------------------------2id          | 7095d222-efe5-4cd5-b5c6-5755b451e2233name        | unique_name4description | This is the description5secret      | 3mMeOcoG84a5F2uOfy2ugWYDp9sdxvCTmi6kTeT97bvA8rCEsG5DWWZtTU8VVeE=6key_id      |7nonce       | \x9f2d60954ba5eb566445736e0760b0e38created_at  | 2022-12-14 02:34:23.85159+009updated_at  | 2022-12-14 02:34:23.85159+00
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-postgres-config

**Contents:**
- Supabase CLI
  - Additional links#
- Global flags
  - Flags
- supabase bootstrap
  - Usage
  - Flags
- supabase init
  - Usage
  - Flags

The Supabase CLI provides tools to develop your project locally and deploy to the Supabase Platform. The CLI is still under development, but it contains all the functionality for working with your Supabase projects and the Supabase Platform.

Supabase CLI supports global flags for every command.

create a support ticket for any CLI error

output debug logs to stderr

lookup domain names using the specified resolver

enable experimental features

use the specified docker network instead of a generated one

output format of status variables

use a specific profile for connecting to Supabase API

path to a Supabase project directory

answer yes to all prompts

Password to your remote Postgres database.

Initialize configurations for Supabase local development.

A supabase/config.toml file is created in your current working directory. This configuration is specific to each local project.

You may override the directory path by specifying the SUPABASE_WORKDIR environment variable or --workdir flag.

In addition to config.toml, the supabase directory may also contain other Supabase objects, such as migrations, functions, tests, etc.

Overwrite existing supabase/config.toml.

Use OrioleDB storage engine for Postgres.

Generate IntelliJ IDEA settings for Deno.

Generate VS Code settings for Deno.

Connect the Supabase CLI to your Supabase account by logging in with your personal access token.

Your access token is stored securely in native credentials storage. If native credentials storage is unavailable, it will be written to a plain text file at ~/.supabase/access-token.

If this behavior is not desired, such as in a CI environment, you may skip login by specifying the SUPABASE_ACCESS_TOKEN environment variable in other commands.

The Supabase CLI uses the stored token to access Management APIs for projects, functions, secrets, etc.

Name that will be used to store token in your settings

Do not open browser automatically

Use provided token instead of automatic login flow

Link your local development project to a hosted Supabase project.

PostgREST configurations are fetched from the Supabase platform and validated against your local configuration file.

Optionally, database settings can be validated if you provide a password. Your database password is saved in native credentials storage if available.

If you do not want to be prompted for the database password, such as in a CI environment, you may specify it explicitly via the SUPABASE_DB_PASSWORD environment variable.

Some commands like db dump, db push, and db pull require your project to be linked first.

Password to your remote Postgres database.

Project ref of the Supabase project.

Use direct connection instead of pooler.

Starts the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All service containers are started by default. You can exclude those not needed by passing in -x flag. To exclude multiple containers, either pass in a comma separated string, such as -x gotrue,imgproxy, or specify -x flag multiple times.

It is recommended to have at least 7GB of RAM to start all services.

Health checks are automatically added to verify the started containers. Use --ignore-health-check flag to ignore these errors.

Names of containers to not start. [gotrue,realtime,storage-api,imgproxy,kong,mailpit,postgrest,postgres-meta,studio,edge-runtime,logflare,vector,supavisor]

Ignore unhealthy services and exit 0

Stops the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All Docker resources are maintained across restarts. Use --no-backup flag to reset your local development data between restarts.

Use the --all flag to stop all local Supabase projects instances on the machine. Use with caution with --no-backup as it will delete all supabase local projects data.

Stop all local Supabase instances from all projects across the machine.

Deletes all data volumes after stopping.

Local project ID to stop.

Shows status of the Supabase local development stack.

Requires the local development stack to be started by running supabase start or supabase db start.

You can export the connection parameters for initializing supabase-js locally by specifying the -o env flag. Supported parameters include JWT_SECRET, ANON_KEY, and SERVICE_ROLE_KEY.

Override specific variable names.

Executes pgTAP tests against the local database.

Requires the local development stack to be started by running supabase start.

Runs pg_prove in a container with unit test files volume mounted from supabase/tests directory. The test file can be suffixed by either .sql or .pg extension.

Since each test is wrapped in its own transaction, it will be individually rolled back regardless of success or failure.

Tests the database specified by the connection string (must be percent-encoded).

Runs pgTAP tests on the linked project.

Runs pgTAP tests on the local database.

Template framework to generate.

Automatically generates type definitions based on your Postgres database schema.

This command connects to your database (local or remote) and generates typed definitions that match your database tables, views, and stored procedures. By default, it generates TypeScript definitions, but also supports Go and Swift.

Generated types give you type safety and autocompletion when working with your database in code, helping prevent runtime errors and improving developer experience.

The types respect relationships, constraints, and custom types defined in your database schema.

Securely generate a private JWT signing key for use in the CLI or to import in the dashboard.

Supported algorithms: ES256 - ECDSA with P-256 curve and SHA-256 (recommended) RS256 - RSA with SHA-256

Algorithm for signing key generation.

Append new key to existing keys file instead of overwriting.

Generate types from a database url.

Output language of the generated types.

Generate types from the linked project.

Generate types from the local dev database.

Generate types compatible with PostgREST v9 and below.

Generate types from a project ID.

Maximum timeout allowed for the database query.

Comma separated list of schema to include.

Access control for Swift generated types.

Pulls schema changes from a remote database. A new migration file will be created under supabase/migrations directory.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Optionally, a new row can be inserted into the migration history table to reflect the current state of the remote database.

If no entries exist in the migration history table, pg_dump will be used to capture all contents of the remote schemas you have created. Otherwise, this command will only diff schema changes against the remote database, similar to running db diff --linked.

Pulls from the database specified by the connection string (must be percent-encoded).

Pulls from the linked project.

Pulls from the local database.

Password to your remote Postgres database.

Comma separated list of schema to include.

Pushes all local migrations to a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

The first time this command is run, a migration history table will be created under supabase_migrations.schema_migrations. After successfully applying a migration, a new row will be inserted into the migration history table with timestamp as its unique id. Subsequent pushes will skip migrations that have already been applied.

If you need to mutate the migration history table, such as deleting existing entries or inserting new entries without actually running the migration, use the migration repair command.

Use the --dry-run flag to view the list of changes before applying.

Pushes to the database specified by the connection string (must be percent-encoded).

Print the migrations that would be applied, but don't actually apply them.

Include all migrations not found on remote history table.

Include custom roles from supabase/roles.sql.

Include seed data from your config.

Pushes to the linked project.

Pushes to the local database.

Password to your remote Postgres database.

Resets the local database to a clean state.

Requires the local development stack to be started by running supabase start.

Recreates the local Postgres container and applies all local migrations found in supabase/migrations directory. If test data is defined in supabase/seed.sql, it will be seeded after the migrations are run. Any other data or schema changes made during local development will be discarded.

When running db reset with --linked or --db-url flag, a SQL script is executed to identify and drop all user created entities in the remote database. Since Postgres roles are cluster level entities, any custom roles created through the dashboard or supabase/roles.sql will not be deleted by remote reset.

Resets the database specified by the connection string (must be percent-encoded).

Reset up to the last n migration versions.

Resets the linked project with local migrations.

Resets the local database with local migrations.

Skip running the seed script after reset.

Reset up to the specified version.

Dumps contents from a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Runs pg_dump in a container with additional flags to exclude Supabase managed schemas. The ignored schemas include auth, storage, and those created by extensions.

The default dump does not contain any data or custom roles. To dump those contents explicitly, specify either the --data-only and --role-only flag.

Dumps only data records.

Dumps from the database specified by the connection string (must be percent-encoded).

Prints the pg_dump script that would be executed.

List of schema.tables to exclude from data-only dump.

File path to save the dumped contents.

Keeps commented lines from pg_dump output.

Dumps from the linked project.

Dumps from the local database.

Password to your remote Postgres database.

Dumps only cluster roles.

Comma separated list of schema to include.

Use copy statements in place of inserts.

Diffs schema changes made to the local or remote database.

Requires the local development stack to be running when diffing against the local database. To diff against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs djrobstep/migra in a container to compare schema differences between the target database and a shadow database. The shadow database is created by applying migrations in local supabase/migrations directory in a separate container. Output is written to stdout by default. For convenience, you can also save the schema diff as a new migration file by passing in -f flag.

By default, all schemas in the target database are diffed. Use the --schema public,extensions flag to restrict diffing to a subset of schemas.

While the diff command is able to capture most schema changes, there are cases where it is known to fail. Currently, this could happen if you schema contains:

Diffs against the database specified by the connection string (must be percent-encoded).

Saves schema diff to a new migration file.

Diffs local migration files against the linked project.

Diffs local migration files against the local database.

Comma separated list of schema to include.

Use migra to generate schema diff.

Use pg-schema-diff to generate schema diff.

Use pgAdmin to generate schema diff.

Lints local database for schema errors.

Requires the local development stack to be running when linting against the local database. To lint against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs plpgsql_check extension in the local Postgres container to check for errors in all schemas. The default lint level is warning and can be raised to error via the --level flag.

To lint against specific schemas only, pass in the --schema flag.

The --fail-on flag can be used to control when the command should exit with a non-zero status code. The possible values are:

This flag is particularly useful in CI/CD pipelines where you want to fail the build based on certain lint conditions.

Lints the database specified by the connection string (must be percent-encoded).

Error level to exit with non-zero status.

Lints the linked project for schema errors.

Lints the local database for schema errors.

Comma separated list of schema to include.

Path to a logical backup file.

Creates a new migration file locally.

A supabase/migrations directory will be created if it does not already exists in your current workdir. All schema migration files must be created in this directory following the pattern <timestamp>_<name>.sql.

Outputs from other commands like db diff may be piped to migration new <name> via stdin.

Lists migration history in both local and remote databases.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Note that URL strings must be escaped according to RFC 3986.

Local migrations are stored in supabase/migrations directory while remote migrations are tracked in supabase_migrations.schema_migrations table. Only the timestamps are compared to identify any differences.

In case of discrepancies between the local and remote migration history, you can resolve them using the migration repair command.

Lists migrations of the database specified by the connection string (must be percent-encoded).

Lists migrations applied to the linked project.

Lists migrations applied to the local database.

Password to your remote Postgres database.

Fetches migrations from the database specified by the connection string (must be percent-encoded).

Fetches migration history from the linked project.

Fetches migration history from the local database.

Repairs the remote migration history table.

Requires your local project to be linked to a remote database by running supabase link.

If your local and remote migration history goes out of sync, you can repair the remote history by marking specific migrations as --status applied or --status reverted. Marking as reverted will delete an existing record from the migration history table while marking as applied will insert a new record.

For example, your migration history may look like the table below, with missing entries in either local or remote.

To reset your migration history to a clean state, first delete your local migration file.

Then mark the remote migration 20230103054303 as reverted.

Now you can run db pull again to dump the remote schema as a local migration file.

Repairs migrations of the database specified by the connection string (must be percent-encoded).

Repairs the migration history of the linked project.

Repairs the migration history of the local database.

Password to your remote Postgres database.

Version status to update.

Squashes local schema migrations to a single migration file.

The squashed migration is equivalent to a schema only dump of the local database after applying existing migration files. This is especially useful when you want to remove repeated modifications of the same schema from your migration history.

However, one limitation is that data manipulation statements, such as insert, update, or delete, are omitted from the squashed migration. You will have to add them back manually in a new migration file. This includes cron jobs, storage buckets, and any encrypted secrets in vault.

By default, the latest <timestamp>_<name>.sql file will be updated to contain the squashed migration. You can override the target version using the --version <timestamp> flag.

If your supabase/migrations directory is empty, running supabase squash will do nothing.

Squashes migrations of the database specified by the connection string (must be percent-encoded).

Squashes the migration history of the linked project.

Squashes the migration history of the local database.

Password to your remote Postgres database.

Squash up to the specified version.

Applies migrations to the database specified by the connection string (must be percent-encoded).

Include all migrations not found on remote history table.

Applies pending migrations to the linked project.

Applies pending migrations to the local database.

Seeds the linked project.

Seeds the local database.

This command displays an estimation of table "bloat" - Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will asynchronously clean the dead tuples. Sometimes the autovaccum is unable to work fast enough to reduce or prevent tables from becoming bloated. High bloat can slow down queries, cause excessive IOPS and waste space in your database.

Tables with a high bloat ratio should be investigated to see if there are vacuuming is not quick enough or there are other issues.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows you statements that are currently holding locks and blocking, as well as the statement that is being blocked. This can be used in conjunction with inspect db locks to determine which statements need to be terminated in order to resolve lock contention.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command is much like the supabase inspect db outliers command, but ordered by the number of times a statement has been called.

You can use this information to see which queries are called most often, which can potentially be good candidates for optimisation.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays queries that have taken out an exclusive lock on a relation. Exclusive locks typically prevent other operations on that relation from taking place, and can be a cause of "hung" queries that are waiting for a lock to be granted.

If you see a query that is hanging for a very long time or causing blocking issues you may consider killing the query by connecting to the database and running SELECT pg_cancel_backend(PID); to cancel the query. If the query still does not stop you can force a hard stop by running SELECT pg_terminate_backend(PID);

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays currently running queries, that have been running for longer than 5 minutes, descending by duration. Very long running queries can be a source of multiple issues, such as preventing DDL statements completing or vacuum being unable to update relfrozenxid.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays statements, obtained from pg_stat_statements, ordered by the amount of time to execute in aggregate. This includes the statement itself, the total execution time for that statement, the proportion of total execution time for all statements that statement has taken up, the number of times that statement has been called, and the amount of time that statement spent on synchronous I/O (reading/writing from the file system).

Typically, an efficient query will have an appropriate ratio of calls to total execution time, with as little time spent on I/O as possible. Queries that have a high total execution time but low call count should be investigated to improve their performance. Queries that have a high proportion of execution time being spent on synchronous I/O should also be investigated.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows information about logical replication slots that are setup on the database. It shows if the slot is active, the state of the WAL sender process ('startup', 'catchup', 'streaming', 'backup', 'stopping') the replication client address and the replication lag in GB.

This command is useful to check that the amount of replication lag is as low as possible, replication lag can occur due to network latency issues, slow disk I/O, long running transactions or lack of ability for the subscriber to consume WAL fast enough.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command analyzes table I/O patterns to show read/write activity ratios based on block-level operations. It combines data from PostgreSQL's pg_stat_user_tables (for tuple operations) and pg_statio_user_tables (for block I/O) to categorize each table's workload profile.

The command classifies tables into categories:

Note: This command only displays tables that have had both read and write activity. Tables with no I/O operations are not shown. The classification ratio threshold (default: 5:1) determines when a table is considered "heavy" in one direction versus balanced.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This shows you stats about the vacuum activities for each table. Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will aysnchronously clean the dead tuples.

The command lists when the last vacuum and last auto vacuum took place, the row count on the table as well as the count of dead rows and whether autovacuum is expected to run or not. If the number of dead rows is much higher than the row count, or if an autovacuum is expected but has not been performed for some time, this can indicate that autovacuum is not able to keep up and that your vacuum settings need to be tweaked or that you require more compute or disk IOPS to allow autovaccum to complete.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Path to save CSV files in

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Create an organization for the logged-in user.

List all organizations the logged-in user belongs.

Provides tools for creating and managing your Supabase projects.

This command group allows you to list all projects in your organizations, create new projects, delete existing projects, and retrieve API keys. These operations help you manage your Supabase infrastructure programmatically without using the dashboard.

Project management via CLI is especially useful for automation scripts and when you need to provision environments in a repeatable way.

Database password of the project.

Organization ID to create the project in.

Select a region close to you for the best performance.

Select a desired instance size for your project.

List all Supabase projects the logged-in user can access.

Project ref of the Supabase project.

Updates the configurations of a linked Supabase project with the local supabase/config.toml file.

This command allows you to manage project configuration as code by defining settings locally and then pushing them to your remote project.

Project ref of the Supabase project.

Create a preview branch for the linked project.

URL to notify when branch is active healthy.

Whether to create a persistent branch.

Select a region to deploy the branch database.

Select a desired instance size for the branch database.

Whether to clone production data to the branch database.

Project ref of the Supabase project.

List all preview branches of the linked project.

Project ref of the Supabase project.

Retrieve details of the specified preview branch.

Project ref of the Supabase project.

Update a preview branch by its name or ID.

Change the associated git branch.

Rename the preview branch.

URL to notify when branch is active healthy.

Switch between ephemeral and persistent branch.

Override the current branch status.

Project ref of the Supabase project.

Project ref of the Supabase project.

Project ref of the Supabase project.

Delete a preview branch by its name or ID.

Project ref of the Supabase project.

Manage Supabase Edge Functions.

Supabase Edge Functions are server-less functions that run close to your users.

Edge Functions allow you to execute custom server-side code without deploying or scaling a traditional server. They're ideal for handling webhooks, custom API endpoints, data validation, and serving personalized content.

Edge Functions are written in TypeScript and run on Deno compatible edge runtime, which is a secure runtime with no package management needed, fast cold starts, and built-in security.

Creates a new Edge Function with boilerplate code in the supabase/functions directory.

This command generates a starter TypeScript file with the necessary Deno imports and a basic function structure. The function is created as a new directory with the name you specify, containing an index.ts file with the function code.

After creating the function, you can edit it locally and then use supabase functions serve to test it before deploying with supabase functions deploy.

List all Functions in the linked Supabase project.

Project ref of the Supabase project.

Download the source code for a Function from the linked Supabase project.

Project ref of the Supabase project.

Unbundle functions server-side without using Docker.

Serve all Functions locally.

supabase functions serve command includes additional flags to assist developers in debugging Edge Functions via the v8 inspector protocol, allowing for debugging via Chrome DevTools, VS Code, and IntelliJ IDEA for example. Refer to the docs guide for setup instructions.

--inspect-mode [ run | brk | wait ]

Additionally, the following properties can be customized via supabase/config.toml under edge_runtime section.

Path to an env file to be populated to the Function environment.

Path to import map file.

Alias of --inspect-mode brk.

Allow inspecting the main worker.

Activate inspector capability for debugging.

Disable JWT verification for the Function.

Deploy a Function to the linked Supabase project.

Path to import map file.

Maximum number of parallel jobs.

Disable JWT verification for the Function.

Project ref of the Supabase project.

Delete Functions that exist in Supabase project but not locally.

Bundle functions server-side without using Docker.

Delete a Function from the linked Supabase project. This does NOT remove the Function locally.

Project ref of the Supabase project.

Provides tools for managing environment variables and secrets for your Supabase project.

This command group allows you to set, unset, and list secrets that are securely stored and made available to Edge Functions as environment variables.

Secrets management through the CLI is useful for:

Secrets can be set individually or loaded from .env files for convenience.

Set a secret(s) to the linked Supabase project.

Read secrets from a .env file.

Project ref of the Supabase project.

List all secrets in the linked project.

Project ref of the Supabase project.

Unset a secret(s) from the linked Supabase project.

Project ref of the Supabase project.

Recursively list a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Custom Cache-Control header for HTTP upload.

Custom Content-Type header for HTTP upload.

Maximum number of parallel jobs.

Recursively copy a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively move a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively remove a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Add and configure a new connection to a SSO identity provider to your Supabase project.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Comma separated list of email domains to associate with the added identity provider.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Type of identity provider (according to supported protocol).

Project ref of the Supabase project.

List all connections to a SSO identity provider to your Supabase project.

Project ref of the Supabase project.

Provides the information about an established connection to an identity provider. You can use --metadata to obtain the raw SAML 2.0 Metadata XML document stored in your project's configuration.

Show SAML 2.0 XML Metadata only

Project ref of the Supabase project.

Returns all of the important SSO information necessary for your project to be registered with a SAML 2.0 compatible identity provider.

Project ref of the Supabase project.

Update the configuration settings of a already added SSO identity provider.

Add this comma separated list of email domains to the identity provider.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Replace domains with this comma separated list of email domains.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Remove this comma separated list of email domains from the identity provider.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Project ref of the Supabase project.

Remove a connection to an already added SSO identity provider. Removing the provider will prevent existing users from logging in. Please treat this command with care.

Project ref of the Supabase project.

Manage custom domain names for Supabase projects.

Use of custom domains and vanity subdomains is mutually exclusive.

Activates the custom hostname configuration for a project.

This reconfigures your Supabase project to respond to requests on your custom hostname.

After the custom hostname is activated, your project's third-party auth providers will no longer function on the Supabase-provisioned subdomain. Please refer to Prepare to activate your domain section in our documentation to learn more about the steps you need to follow.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Create a custom hostname for your Supabase project.

Expects your custom hostname to have a CNAME record to your Supabase project's subdomain.

The custom hostname to use for your Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Retrieve the custom hostname config for your project, as stored in the Supabase platform.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Manage vanity subdomains for Supabase projects.

Usage of vanity subdomains and custom domains is mutually exclusive.

Activate a vanity subdomain for your Supabase project.

This reconfigures your Supabase project to respond to requests on your vanity subdomain. After the vanity subdomain is activated, your project's auth services will no longer function on the {project-ref}.{supabase-domain} hostname.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

Deletes the vanity subdomain for a project, and reverts to using the project ref for routing.

enable experimental features

Project ref of the Supabase project.

Network bans are IPs that get temporarily blocked if their traffic pattern looks abusive (e.g. multiple failed auth attempts).

The subcommands help you view the current bans, and unblock IPs if desired.

enable experimental features

Project ref of the Supabase project.

IP to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Append to existing restrictions instead of replacing them.

Bypass some of the CIDR validation checks.

CIDR to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Whether the DB should disable SSL enforcement for all external connections.

Whether the DB should enable SSL enforcement for all external connections.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Overriding the default Postgres config could result in unstable database behavior. Custom configuration also overrides the optimizations generated based on the compute add-ons in use.

Config overrides specified as a 'key=value' pair

Do not restart the database after updating config.

If true, replaces all existing overrides with the ones provided. If false (default), merges existing overrides with the ones provided.

enable experimental features

Project ref of the Supabase project.

Delete specific config overrides, reverting them to their default values.

Config keys to delete (comma-separated)

Do not restart the database after deleting config.

enable experimental features

Project ref of the Supabase project.

List all SQL snippets of the linked project.

Project ref of the Supabase project.

Download contents of the specified SQL snippet.

Project ref of the Supabase project.

Generate the autocompletion script for supabase for the specified shell. See each sub-command's help for details on how to use the generated script.

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need to enable it. You can execute the following once:

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for powershell.

To load completions in your current shell session:

To load completions for every new session, add the output of the above command to your powershell profile.

disable completion descriptions

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package. If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

**Examples:**

Example 1 (unknown):
```unknown
1supabase bootstrap [template] [flags]
```

Example 2 (unknown):
```unknown
1supabase init [flags]
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1Finished supabase init.
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-update-postgrest-service-config

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## HNSW indexes | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/vector-indexes/hnsw-indexes

**Contents:**
- HNSW indexes
- Usage#
  - Euclidean L2 distance (vector_l2_ops)#
  - Inner product (vector_ip_ops)#
  - Cosine distance (vector_cosine_ops)#
- Example with high-dimensional vectors#
- How does HNSW work?#
  - Hierarchical#
  - Navigable Small World#
  - Hierarchical + Navigable Small World#

HNSW is an algorithm for approximate nearest neighbor search. It is a frequently used index type that can improve performance when querying highly-dimensional vectors, like those representing embeddings.

The way you create an HNSW index depends on the distance operator you are using. pgvector includes 3 distance operators:

Use the following SQL commands to create an HNSW index for the operator(s) used in your queries.

For pgvector versions 0.7.0 and above, it's possible to create indexes on vectors with the following maximum dimensions:

You can check your current pgvector version by running: SELECT * FROM pg_extension WHERE extname = 'vector'; or by navigating to the Extensions tab in your Supabase project dashboard.

If you are on an earlier version of pgvector, you should upgrade your project here.

For vectors with more than 2,000 dimensions, you can use the halfvec type to create indexes. Here's an example with 3,072 dimensions:

HNSW uses proximity graphs (graphs connecting nodes based on distance between them) to approximate nearest-neighbor search. To understand HNSW, we can break it down into 2 parts:

The hierarchical aspect of HNSW builds off of the idea of skip lists.

Skip lists are multi-layer linked lists. The bottom layer is a regular linked list connecting an ordered sequence of elements. Each new layer above removes some elements from the underlying layer (based on a fixed probability), producing a sparser subsequence that “skips” over elements.

When searching for an element, the algorithm begins at the top layer and traverses its linked list horizontally. If the target element is found, the algorithm stops and returns it. Otherwise if the next element in the list is greater than the target (or NULL), the algorithm drops down to the next layer below. Since each layer below is less sparse than the layer above (with the bottom layer connecting all elements), the target will eventually be found. Skip lists offer O(log n) average complexity for both search and insertion/deletion.

A navigable small world (NSW) is a special type of proximity graph that also includes long-range connections between nodes. These long-range connections support the “small world” property of the graph, meaning almost every node can be reached from any other node within a few hops. Without these additional long-range connections, many hops would be required to reach a far-away node.

The “navigable” part of NSW specifically refers to the ability to logarithmically scale the greedy search algorithm on the graph, an algorithm that attempts to make only the locally optimal choice at each hop. Without this property, the graph may still be considered a small world with short paths between far-away nodes, but the greedy algorithm tends to miss them. Greedy search is ideal for NSW because it is quick to navigate and has low computational costs.

HNSW combines these two concepts. From the hierarchical perspective, the bottom layer consists of a NSW made up of short links between nodes. Each layer above “skips” elements and creates longer links between nodes further away from each other.

Just like skip lists, search starts at the top layer and works its way down until it finds the target element. However, instead of comparing a scalar value at each layer to determine whether or not to descend to the layer below, a multi-dimensional distance measure (such as Euclidean distance) is used.

HNSW should be your default choice when creating a vector index. Add the index when you don't need 100% accuracy and are willing to trade a small amount of accuracy for a lot of throughput.

Unlike IVFFlat indexes, you are safe to build an HNSW index immediately after the table is created. HNSW indexes are based on graphs which inherently are not affected by the same limitations as IVFFlat. As new data is added to the table, the index will be filled automatically and the index structure will remain optimal.

Read more about indexing on pgvector's GitHub page.

**Examples:**

Example 1 (unknown):
```unknown
1create index on items using hnsw (column_name vector_l2_ops);
```

Example 2 (unknown):
```unknown
1create index on items using hnsw (column_name vector_ip_ops);
```

Example 3 (unknown):
```unknown
1create index on items using hnsw (column_name vector_cosine_ops);
```

Example 4 (unknown):
```unknown
1CREATE TABLE documents (2    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,3    content text,4    embedding vector(3072)5);67CREATE INDEX ON documents8    USING hnsw ((embedding::halfvec(3072)) halfvec_cosine_ops);
```

---

## Database Replication | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/replication

**Contents:**
- Database Replication
- An introduction to database replication and change data capture.
- Use cases#
- Replication methods#
  - Replication#
      - Private Alpha
  - Manual replication#
- Related features#
- Concepts and terms#
  - Write-Ahead Log (WAL)#

An introduction to database replication and change data capture.

Replication is the process of copying changes from your database to another location. It's also referred to as change data capture (CDC): capturing all the changes that occur to your data.

You might use database replication for:

Supabase supports two methods for replicating your database to external destinations:

Replication is currently in private alpha. Access is limited and features may change.

Replication powered by Supabase ETL automatically replicates data to supported systems.

Configure your own replication using external tools and Postgres's native logical replication. This gives you full control over the replication process and allows you to use any tool that supports Postgres logical replication.

Choose the data syncing method based on your use case:

Postgres uses a system called the Write-Ahead Log (WAL) to manage changes to the database. As you make changes, they are appended to the WAL, which is a series of files (also called "segments") where the file size can be specified. Once one segment is full, Postgres will start appending to a new segment. After a period of time, a checkpoint occurs and Postgres synchronizes the WAL with your database. Once the checkpoint is complete, then the WAL files can be removed from disk and free up space.

Logical replication is a method of replication where Postgres uses the WAL files and transmit those changes to another Postgres database, or a system that supports reading WAL files.

LSN is a Log Sequence Number that is used to identify the position of a WAL file in the WAL directory. It is often used to determine the progress of replication in subscribers and calculate the lag of a replication slot.

When setting up logical replication, three key components are involved:

Logical replication is typically output in 2 forms, pgoutput and wal2json. The output method is how Postgres sends changes to any active replication slot.

When using logical replication, Postgres is then configured to keep WAL files around for longer than it needs them. If the files are removed too quickly, then your replication slot will become inactive and, if the database receives a large number of changes in a short time, then the replication slot can become lost as it was not able to keep up.

In order to mitigate this, Postgres has many options and settings that can be tweaked to manage the WAL usage effectively. Not all of these settings are user configurable as they can impact the stability of your database. For those that are, these should be considered as advanced configuration and not changed without understanding that they can cause additional disk space and resources to be used, as well as incur additional costs.

---

## Connecting with pgAdmin | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/pgadmin

**Contents:**
- Connecting with pgAdmin
- What is pgAdmin?#
- Connecting pgAdmin with your Postgres database#
  - Register
  - Name
  - Connect
  - SSL
- Why connect to pgAdmin#

Connecting with pgAdmin

pgAdmin is a GUI tool for managing Postgres databases. You can use it to connect to your database via SSL.

Register a new Postgres server.

Add the connection info. Click the "Connect" button at the top of the page to open the connect Modal. Scroll down to "session pooler", click "view parameters" to toggle the parameters menu open and copy your connection parameters. Fill in your Database password that you made when creating your project (It can be reset in Database Settings above if you don't have it).

Download your SSL certificate from Dashboard's Database Settings.

In pgAdmin, navigate to the Parameters tab and select connection parameter as Root Certificate. Next navigate to the Root certificate input, it will open up a file-picker modal. Select the certificate you downloaded earlier and save the server details. pgAdmin should now be able to connect to your Postgres via SSL.

Connecting your Postgres instance to pgAdmin gives you a free, cross-platform GUI that makes tasks such as browsing objects, writing queries with autocomplete, running backups, and monitoring performance much faster and safer than using psql alone.

It acts as a single control panel where you can manage multiple servers, inspect locks and slow queries in real time, and perform maintenance operations with a click.

For scripted migrations or ultra-light remote work you’ll still lean on plain SQL or CLI tools, but most teams find pgAdmin invaluable for exploration and routine administration.

---

## PGMQ Extension | Supabase Docs

**URL:** https://supabase.com/docs/guides/queues/pgmq

**Contents:**
- PGMQ Extension
- Features#
- Enable the extension#
- Usage #
  - Queue management#
    - create#
    - create_unlogged#
    - detach_archive#
    - drop_queue#
  - Sending messages#

pgmq is a lightweight message queue built on Postgres.

Creates an unlogged table. This is useful when write throughput is more important than durability. See Postgres documentation for unlogged tables for more information.

Drop the queue's archive table as a member of the PGMQ extension. Useful for preventing the queue's archive table from being dropped when drop extension pgmq is executed. This does not prevent the further archives() from appending to the archive table.

Deletes a queue and its archive table.

Send a single message to a queue.

Send 1 or more messages to a queue.

Read 1 or more messages from a queue. The VT specifies the duration of time in seconds that the message is invisible to other consumers. At the end of that duration, the message is visible again and could be read by other consumers.

Same as read(). Also provides convenient long-poll functionality. When there are no messages in the queue, the function call will wait for max_poll_seconds in duration before returning. If messages reach the queue during that duration, they will be read and returned immediately.

Reads a single message from a queue and deletes it upon read.

Note: utilization of pop() results in at-most-once delivery semantics if the consuming application does not guarantee processing of the message.

Deletes a single message from a queue.

Delete one or many messages from a queue.

Delete two messages that exist.

Delete two messages, one that exists and one that does not. Message 999 does not exist.

Permanently deletes all messages in a queue. Returns the number of messages that were deleted.

Purge the queue when it contains 8 messages;

Removes a single requested message from the specified queue and inserts it into the queue's archive.

Returns Boolean value indicating success or failure of the operation.

Example; remove message with ID 1 from queue my_queue and archive it:

Deletes a batch of requested messages from the specified queue and inserts them into the queue's archive. Returns an array of message ids that were successfully archived.

Delete messages with ID 1 and 2 from queue my_queue and move to the archive.

Delete messages 4, which exists and 999, which does not exist.

Sets the visibility timeout of a message to a specified time duration in the future. Returns the record of the message that was updated.

Set the visibility timeout of message 1 to 30 seconds from now.

List all the queues that currently exist.

Get metrics for a specific queue.

| Attribute | Type | Description | | :------------------- | :------------------------- | :------------------------------------------------------------------------ | -------------------------------------------------- | | queue_name | text | The name of the queue | | queue_length | bigint | Number of messages currently in the queue | | newest_msg_age_sec | integer | null | Age of the newest message in the queue, in seconds | | oldest_msg_age_sec | integer | null | Age of the oldest message in the queue, in seconds | | total_messages | bigint | Total number of messages that have passed through the queue over all time | | scrape_time | timestamp with time zone | The current timestamp |

Get metrics for all existing queues.

| Attribute | Type | Description | | :------------------- | :------------------------- | :------------------------------------------------------------------------ | -------------------------------------------------- | | queue_name | text | The name of the queue | | queue_length | bigint | Number of messages currently in the queue | | newest_msg_age_sec | integer | null | Age of the newest message in the queue, in seconds | | oldest_msg_age_sec | integer | null | Age of the oldest message in the queue, in seconds | | total_messages | bigint | Total number of messages that have passed through the queue over all time | | scrape_time | timestamp with time zone | The current timestamp |

The complete representation of a message in a queue.

**Examples:**

Example 1 (unknown):
```unknown
1create extension pgmq;
```

Example 2 (unknown):
```unknown
1pgmq.create(queue_name text)2returns void
```

Example 3 (unknown):
```unknown
1select from pgmq.create('my_queue');2 create3--------
```

Example 4 (unknown):
```unknown
1pgmq.create_unlogged(queue_name text)2returns void
```

---

## Storage Self-hosting Config | Supabase Docs

**URL:** https://supabase.com/docs/guides/self-hosting/storage/config

**Contents:**
- Storage Self-hosting Config
- General
      - Parameters
- Multi-tenant
      - Parameters

Storage Self-hosting Config

A sample .env file is located in the storage repository.

Use this file to configure your environment variables for your Storage server.

A long-lived JWT with anonymous Postgres privileges.

A long-lived JWT with Postgres privileges to bypass Row Level Security.

The ID of a Storage tenant.

Region of your S3 bucket.

Name of your S3 bucket.

The URL of your PostgREST server.

A JWT Secret for the PostgREST database.

The URL of your Postgres database.

Additional configuration parameters for Postgres startup.

The maximum file size allowed.

The storage provider.

The location storage when the "STORAGE_BACKEND" is set to "file".

Configuration items for multi-tenant servers.

Operate across multiple tenants.

The URL of the multitenant Postgres database.

The suffix for the PostgREST instance.

Secure API key for administrative endpoints.

An key for encryting/decrypting secrets.

---

## Debugging performance issues | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/debugging-performance

**Contents:**
- Debugging performance issues
- Debug slow-running queries using the Postgres execution planner.
- Enabling explain()#
- Using explain()#
  - Example data#
  - Expected response#
- Production use with pre-request protection#
- Disabling explain#

Debugging performance issues

Debug slow-running queries using the Postgres execution planner.

explain() is a method that provides the Postgres EXPLAIN execution plan of a query. It is a powerful tool for debugging slow queries and understanding how Postgres will execute a given query. This feature is applicable to any query, including those made through rpc() or write operations.

explain() is disabled by default to protect sensitive information about your database structure and operations. We recommend using explain() in a non-production environment. Run the following SQL to enable explain():

To get the execution plan of a query, you can chain the explain() method to a Supabase query:

To illustrate, consider the following setup of a instruments table:

The response would typically look like this:

By default, the execution plan is returned in TEXT format. However, you can also retrieve it as JSON by specifying the format parameter.

If you need to enable explain() in a production environment, ensure you protect your database by restricting access to the explain() feature. You can do so by using a pre-request function that filters requests based on the IP address:

The pgrst.db_pre_request configuration only works with the Data API (PostgREST). It does not work with Realtime, Storage, or other Supabase products.

If you're using db_pre_request to call a function (like set_information()) that sets up context or performs checks on every request, and you need similar behavior for other Supabase products, you must call the function directly in your Row Level Security (RLS) policies instead.

If you have a db_pre_request function that calls set_information() that returns true to set up context or perform checks, and you have an RLS policy like:

To achieve the same behavior with other Supabase products, you need to call the function directly in your RLS policy:

This ensures the function is called when evaluating RLS policies for all products, not just Data API requests.

Performance consideration:

Be aware that calling functions directly in RLS policies can impact database performance, as the function is evaluated for each row when the policy is checked. Consider optimizing your function or using caching strategies if performance becomes an issue.

Replace '123.123.123.123' with your actual IP address.

To disable the explain() method after use, execute the following SQL commands:

**Examples:**

Example 1 (unknown):
```unknown
1-- enable explain2alter role authenticator3set pgrst.db_plan_enabled to 'true';45-- reload the config6notify pgrst, 'reload config';
```

Example 2 (javascript):
```javascript
1const { data, error } = await supabase2  .from('instruments')3  .select()4  .explain()
```

Example 3 (unknown):
```unknown
1create table instruments (2  id int8 primary key,3  name text4);56insert into books7  (id, name)8values9  (1, 'violin'),10  (2, 'viola'),11  (3, 'cello');
```

Example 4 (unknown):
```unknown
1Aggregate  (cost=33.34..33.36 rows=1 width=112)2  ->  Limit  (cost=0.00..18.33 rows=1000 width=40)3        ->  Seq Scan on instruments  (cost=0.00..22.00 rows=1200 width=40)
```

---

## Managing JSON and unstructured data | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/json

**Contents:**
- Managing JSON and unstructured data
- Using the JSON data type in Postgres.
- JSON vs JSONB#
- When to use JSON/JSONB#
- Create JSONB columns#
- Inserting JSON data#
- Query JSON data#
- Validating JSON data#
- Resources#

Managing JSON and unstructured data

Using the JSON data type in Postgres.

Postgres supports storing and querying unstructured data.

Postgres supports two types of JSON columns: json (stored as a string) and jsonb (stored as a binary). The recommended type is jsonb for almost all cases.

Generally you should use a jsonb column when you have data that is unstructured or has a variable schema. For example, if you wanted to store responses for various webhooks, you might not know the format of the response when creating the table. Instead, you could store the payload as a jsonb object in a single column.

Don't go overboard with json/jsonb columns. They are a useful tool, but most of the benefits of a relational database come from the ability to query and join structured data, and the referential integrity that brings.

json/jsonb is just another "data type" for Postgres columns. You can create a jsonb column in the same way you would create a text or int column:

You can insert JSON data in the same way that you insert any other data. The data must be valid JSON.

Querying JSON data is similar to querying other data, with a few other features to access nested values.

Postgres support a range of JSON functions and operators. For example, the -> operator returns values as jsonb data. If you want the data returned as text, use the ->> operator.

Supabase provides the pg_jsonschema extension that adds the ability to validate json and jsonb data types against JSON Schema documents.

Once you have enabled the extension, you can add a "check constraint" to your table to validate the JSON data:

**Examples:**

Example 1 (unknown):
```unknown
1create table books (2  id serial primary key,3  title text,4  author text,5  metadata jsonb6);
```

Example 2 (javascript):
```javascript
1insert into books2  (title, author, metadata)3values4  (5    'The Poky Little Puppy',6    'Janette Sebring Lowrey',7    '{"description":"Puppy is slower than other, bigger animals.","price":5.95,"ages":[3,6]}'8  ),9  (10    'The Tale of Peter Rabbit',11    'Beatrix Potter',12    '{"description":"Rabbit eats some vegetables.","price":4.49,"ages":[2,5]}'13  ),14  (15    'Tootle',16    'Gertrude Crampton',17    '{"description":"Little toy train has big dreams.","price":3.99,"ages":[2,5]}'18  ),19  (20    'Green Eggs and Ham',21    'Dr. Seuss',22    '{"description":"Sam has changing food preferences and eats unusually colored food.","price":7.49,"ages":[4,8]}'23  ),24  (25    'Harry Potter and the Goblet of Fire',26    'J.K. Rowling',27    '{"description":"Fourth year of school starts, big drama ensues.","price":24.95,"ages":[10,99]}'28  );
```

Example 3 (unknown):
```unknown
1select2  title,3  metadata ->> 'description' as description, -- returned as text4  metadata -> 'price' as price,5  metadata -> 'ages' -> 0 as low_age,6  metadata -> 'ages' -> 1 as high_age7from books;
```

Example 4 (unknown):
```unknown
1create table customers (2  id serial primary key,3  metadata json4);56alter table customers7add constraint check_metadata check (8  json_matches_schema(9    '{10        "type": "object",11        "properties": {12            "tags": {13                "type": "array",14                "items": {15                    "type": "string",16                    "maxLength": 1617                }18            }19        }20    }',21    metadata22  )23);
```

---

## pgsodium (pending deprecation): Encryption Features | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgsodium

**Contents:**
- pgsodium (pending deprecation): Encryption Features
- Get the root encryption key for your Supabase project#
- Resources#
- Resources#

pgsodium (pending deprecation): Encryption Features

Supabase DOES NOT RECOMMEND any new usage of pgsodium.

The pgsodium extension is expected to go through a deprecation cycle in the near future. We will reach out to owners of impacted projects to assist with migrations away from pgsodium once the deprecation process begins.

The Vault extension won’t be impacted. Its internal implementation will shift away from pgsodium, but the interface and API will remain unchanged.

pgsodium is a Postgres extension which provides SQL access to libsodium's high-level cryptographic algorithms.

Supabase previously documented two features derived from pgsodium. Namely Server Key Management and Transparent Column Encryption. At this time, we do not recommend using either on the Supabase platform due to their high level of operational complexity and misconfiguration risk.

Note that Supabase projects are encrypted at rest by default which likely is sufficient for your compliance needs e.g. SOC2 & HIPAA.

Encryption requires keys. Keeping the keys in the same database as the encrypted data would be unsafe. For more information about managing the pgsodium root encryption key on your Supabase project see encryption key location. This key is required to decrypt values stored in Supabase Vault and data encrypted with Transparent Column Encryption.

---

## Paddle | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/paddle

**Contents:**
- Paddle
- Available Versions#
- Preparation#
  - Enable Wrappers#
  - Enable the Paddle Wrapper#
  - Store your credentials (optional)#
  - Connecting to Paddle#
  - Create a schema#
- Options#
- Entities#

You can enable the Paddle wrapper right from the Supabase dashboard.

Paddle is a merchant of record that acts to provide a payment infrastructure to thousands of software companies around the world.

The Paddle Wrapper is a WebAssembly(Wasm) foreign data wrapper which allows you to read and write data from Paddle within your Postgres database.

Before you can query Paddle, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the Wasm foreign data wrapper:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to access Paddle, and any additional options. We can do this using the create server command:

Note the fdw_package_* options are required, which specify the Wasm package metadata. You can get the available package version list from above.

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

Supported objects are listed below:

We can use SQL import foreign schema to import foreign table definitions from Paddle.

For example, using below SQL can automatically create foreign tables in the paddle schema.

This is an object representing Paddle Products.

This is an object representing Paddle Customers.

This is an object representing Paddle Subscriptions.

This FDW supports where clause pushdown with id as the filter. For example,

The Paddle API uses JSON formatted data, please refer to Paddle docs for more details.

This section describes important limitations and considerations when using this FDW:

This example will create a "foreign table" inside your Postgres database and query its data.

attrs is a special column which stores all the object attributes in JSON format, you can extract any attributes needed or its associated sub objects from it. See more examples below.

This example will modify data in a "foreign table" inside your Postgres database, note that rowid_column option is mandatory for data modify:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper wasm_wrapper2  handler wasm_fdw_handler3  validator wasm_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Paddle API key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<Paddle API key>', -- Paddle API key4  'paddle',5  'Paddle API key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server paddle_server2  foreign data wrapper wasm_wrapper3  options (4    fdw_package_url 'https://github.com/supabase/wrappers/releases/download/wasm_paddle_fdw_v0.2.0/paddle_fdw.wasm',5    fdw_package_name 'supabase:paddle-fdw',6    fdw_package_version '0.2.0',7    fdw_package_checksum 'e788b29ae46c158643e1e1f229d94b28a9af8edbd3233f59c5a79053c25da213',8    api_url 'https://sandbox-api.paddle.com', -- Use https://api.paddle.com for live account9    api_key_id '<key_ID>' -- The Key ID from above.10  );
```

---

## Tables and Data | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/tables

**Contents:**
- Tables and Data
- Creating tables#
- Columns#
  - Data types#
  - Primary keys#
- Loading data#
  - Basic data loading#
  - Bulk data loading#
- Joining tables with foreign keys#
- Schemas#

Tables are where you store your data.

Tables are similar to excel spreadsheets. They contain columns and rows. For example, this table has 3 "columns" (id, name, description) and 4 "rows" of data:

There are a few important differences from a spreadsheet, but it's a good starting point if you're new to Relational databases.

When creating a table, it's best practice to add columns at the same time.

You must define the "data type" of each column when it is created. You can add and remove columns at any time after creating a table.

Supabase provides several options for creating tables. You can use the Dashboard or create them directly using SQL. We provide a SQL editor within the Dashboard, or you can connect to your database and run the SQL queries yourself.

When naming tables, use lowercase and underscores instead of spaces (e.g., table_name, not Table Name).

You must define the "data type" when you create a column.

Every column is a predefined type. Postgres provides many default types, and you can even design your own (or use extensions) if the default types don't fit your needs. You can use any data type that Postgres supports via the SQL editor. We only support a subset of these in the Table Editor in an effort to keep the experience simple for people with less experience with databases.

You can "cast" columns from one type to another, however there can be some incompatibilities between types. For example, if you cast a timestamp to a date, you will lose all the time information that was previously saved.

A table can have a "primary key" - a unique identifier for every row of data. A few tips for Primary Keys:

In the example above, we have:

We could also use generated by default as identity, which would allow us to insert our own unique values.

There are several ways to load data in Supabase. You can load data directly into the database or using the APIs. Use the "Bulk Loading" instructions if you are loading large data sets.

When inserting large data sets it's best to use PostgreSQL's COPY command. This loads data directly from a file into a table. There are several file formats available for copying data: text, CSV, binary, JSON, etc.

For example, if you wanted to load a CSV file into your movies table:

You would connect to your database directly and load the file with the COPY command:

Additionally use the DELIMITER, HEADER and FORMAT options as defined in the Postgres COPY docs.

If you receive an error FATAL: password authentication failed for user "postgres", reset your database password in the Database Settings and try again.

Tables can be "joined" together using Foreign Keys.

This is where the "Relational" naming comes from, as data typically forms some sort of relationship.

In our "movies" example above, we might want to add a "category" for each movie (for example, "Action", or "Documentary"). Let's create a new table called categories and "link" our movies table.

You can also create "many-to-many" relationships by creating a "join" table. For example if you had the following situations:

Tables belong to schemas. Schemas are a way of organizing your tables, often for security reasons.

If you don't explicitly pass a schema when creating a table, Postgres will assume that you want to create the table in the public schema.

We can create schemas for organizing tables. For example, we might want a private schema which is hidden from our API:

Now we can create tables inside the private schema:

A View is a convenient shortcut to a query. Creating a view does not involve new tables or data. When run, an underlying query is executed, returning its results to the user.

Say we have the following tables from a database of a university:

Creating a view consisting of all the three tables will look like this:

Once done, we can now access the underlying query with:

By default, views are accessed with their creator's permission ("security definer"). If a privileged role creates a view, others accessing it will use that role's elevated permissions. To enforce row level security policies, define the view with the "security invoker" modifier.

Views provide several benefits:

As a query becomes more complex, it can be a hassle to call it over and over - especially when we run it regularly. In the example above, instead of repeatedly running:

We can run this instead:

Additionally, a view behaves like a typical table. We can safely use it in table JOINs or even create new views using existing views.

Views ensure that the likelihood of mistakes decreases when repeatedly executing a query. In our example above, we may decide that we want to exclude the course Introduction to Postgres. The query would become:

Without a view, we would need to go into every dependent query to add the new rule. This would increase in the likelihood of errors and inconsistencies, as well as introducing a lot of effort for a developer. With views, we can alter just the underlying query in the view transcripts. The change will be applied to all applications using this view.

With views, we can give our query a name. This is extremely useful for teams working with the same database. Instead of guessing what a query is supposed to do, a well-named view can explain it. For example, by looking at the name of the view transcripts, we can infer that the underlying query might involve the students, courses, and grades tables.

Views can restrict the amount and type of data presented to a user. Instead of allowing a user direct access to a set of tables, we provide them a view instead. We can prevent them from reading sensitive columns by excluding them from the underlying query.

A materialized view is a form of view but it also stores the results to disk. In subsequent reads of a materialized view, the time taken to return its results would be much faster than a conventional view. This is because the data is readily available for a materialized view while the conventional view executes the underlying query each time it is called.

Using our example above, a materialized view can be created like this:

Reading from the materialized view is the same as a conventional view:

Unfortunately, there is a trade-off - data in materialized views are not always up to date. We need to refresh it regularly to prevent the data from becoming too stale. To do so:

It's up to you how regularly refresh your materialized views, and it's probably different for each view depending on its use-case.

Materialized views are useful when execution times for queries or views are too slow. These could likely occur in views or queries involving multiple tables and billions of rows. When using such a view, however, there should be tolerance towards data being outdated. Some use-cases for materialized views are internal dashboards and analytics.

Creating a materialized view is not a solution to inefficient queries. You should always seek to optimize a slow running query even if you are implementing a materialized view.

**Examples:**

Example 1 (unknown):
```unknown
1create table movies (2  id bigint generated always as identity primary key3);
```

Example 2 (unknown):
```unknown
1create table movies (2  id bigint generated by default as identity primary key3);
```

Example 3 (unknown):
```unknown
1insert into movies2  (name, description)3values4  (5    'The Empire Strikes Back',6    'After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda.'7  ),8  (9    'Return of the Jedi',10    'After a daring mission to rescue Han Solo from Jabba the Hutt, the Rebels dispatch to Endor to destroy the second Death Star.'11  );
```

Example 4 (unknown):
```unknown
1"The Empire Strikes Back", "After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda."2"Return of the Jedi", "After a daring mission to rescue Han Solo from Jabba the Hutt, the Rebels dispatch to Endor to destroy the second Death Star."
```

---

## Manage Compute usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/compute

**Contents:**
- Manage Compute usage
- What you are charged for#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Compute Credits#
- Pricing#
      - Nano Compute size in paid plan organizations
- Billing examples#
  - One project#

Each project on the Supabase platform includes a dedicated Postgres instance running on its own server. You are charged for the Compute resources of that server, independent of your database usage.

Paused projects do not count towards Compute usage.

Compute is charged by the hour, meaning you are charged for the exact number of hours that a project is running and, therefore, incurring Compute usage. If a project runs for part of an hour, you are still charged for the full hour.

Each project you launch increases your monthly Compute costs.

Your billing cycle runs from January 1 to January 31. On January 10 at 4:30 PM, you switch your project from the Micro Compute size to the Small Compute size. At the end of the billing cycle you are billed for 233 hours of Micro Compute size and 511 hours of Small Compute size.

Usage is shown as "Compute Hours" on your invoice.

Paid plans include $10 in Compute Credits, which cover one project running on the Micro/Nano Compute size or portions of other Compute sizes. Compute Credits are applied to your Compute costs and are provided to an organization each month. They reset monthly and do not accumulate.

In paid organizations, Nano Compute are billed at the same price as Micro Compute. It is recommended to upgrade your Project from Nano Compute to Micro Compute when it's convenient for you. Compute sizes are not auto-upgraded because of the downtime incurred. See Supabase Pricing for more information. You cannot launch Nano instances on paid plans, only Micro and above - but you might have Nano instances after upgrading from Free Plan.

The project runs on the same Compute size throughout the entire billing cycle.

All projects run on the same Compute size throughout the entire billing cycle.

The project's Compute size changes throughout the billing cycle.

You can view Compute usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Compute Hours section, you can see how many hours of a specific Compute size your projects have used during the selected time period. Hover over a specific date for a daily breakdown.

No, Compute Credits apply only to Compute and do not cover other line items, including Read Replica Compute and Branching Compute.

Compute resources on the Free Plan are subject to change. ↩

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-postgres-config-delete

**Contents:**
- Supabase CLI
  - Additional links#
- Global flags
  - Flags
- supabase bootstrap
  - Usage
  - Flags
- supabase init
  - Usage
  - Flags

The Supabase CLI provides tools to develop your project locally and deploy to the Supabase Platform. The CLI is still under development, but it contains all the functionality for working with your Supabase projects and the Supabase Platform.

Supabase CLI supports global flags for every command.

create a support ticket for any CLI error

output debug logs to stderr

lookup domain names using the specified resolver

enable experimental features

use the specified docker network instead of a generated one

output format of status variables

use a specific profile for connecting to Supabase API

path to a Supabase project directory

answer yes to all prompts

Password to your remote Postgres database.

Initialize configurations for Supabase local development.

A supabase/config.toml file is created in your current working directory. This configuration is specific to each local project.

You may override the directory path by specifying the SUPABASE_WORKDIR environment variable or --workdir flag.

In addition to config.toml, the supabase directory may also contain other Supabase objects, such as migrations, functions, tests, etc.

Overwrite existing supabase/config.toml.

Use OrioleDB storage engine for Postgres.

Generate IntelliJ IDEA settings for Deno.

Generate VS Code settings for Deno.

Connect the Supabase CLI to your Supabase account by logging in with your personal access token.

Your access token is stored securely in native credentials storage. If native credentials storage is unavailable, it will be written to a plain text file at ~/.supabase/access-token.

If this behavior is not desired, such as in a CI environment, you may skip login by specifying the SUPABASE_ACCESS_TOKEN environment variable in other commands.

The Supabase CLI uses the stored token to access Management APIs for projects, functions, secrets, etc.

Name that will be used to store token in your settings

Do not open browser automatically

Use provided token instead of automatic login flow

Link your local development project to a hosted Supabase project.

PostgREST configurations are fetched from the Supabase platform and validated against your local configuration file.

Optionally, database settings can be validated if you provide a password. Your database password is saved in native credentials storage if available.

If you do not want to be prompted for the database password, such as in a CI environment, you may specify it explicitly via the SUPABASE_DB_PASSWORD environment variable.

Some commands like db dump, db push, and db pull require your project to be linked first.

Password to your remote Postgres database.

Project ref of the Supabase project.

Use direct connection instead of pooler.

Starts the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All service containers are started by default. You can exclude those not needed by passing in -x flag. To exclude multiple containers, either pass in a comma separated string, such as -x gotrue,imgproxy, or specify -x flag multiple times.

It is recommended to have at least 7GB of RAM to start all services.

Health checks are automatically added to verify the started containers. Use --ignore-health-check flag to ignore these errors.

Names of containers to not start. [gotrue,realtime,storage-api,imgproxy,kong,mailpit,postgrest,postgres-meta,studio,edge-runtime,logflare,vector,supavisor]

Ignore unhealthy services and exit 0

Stops the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All Docker resources are maintained across restarts. Use --no-backup flag to reset your local development data between restarts.

Use the --all flag to stop all local Supabase projects instances on the machine. Use with caution with --no-backup as it will delete all supabase local projects data.

Stop all local Supabase instances from all projects across the machine.

Deletes all data volumes after stopping.

Local project ID to stop.

Shows status of the Supabase local development stack.

Requires the local development stack to be started by running supabase start or supabase db start.

You can export the connection parameters for initializing supabase-js locally by specifying the -o env flag. Supported parameters include JWT_SECRET, ANON_KEY, and SERVICE_ROLE_KEY.

Override specific variable names.

Executes pgTAP tests against the local database.

Requires the local development stack to be started by running supabase start.

Runs pg_prove in a container with unit test files volume mounted from supabase/tests directory. The test file can be suffixed by either .sql or .pg extension.

Since each test is wrapped in its own transaction, it will be individually rolled back regardless of success or failure.

Tests the database specified by the connection string (must be percent-encoded).

Runs pgTAP tests on the linked project.

Runs pgTAP tests on the local database.

Template framework to generate.

Automatically generates type definitions based on your Postgres database schema.

This command connects to your database (local or remote) and generates typed definitions that match your database tables, views, and stored procedures. By default, it generates TypeScript definitions, but also supports Go and Swift.

Generated types give you type safety and autocompletion when working with your database in code, helping prevent runtime errors and improving developer experience.

The types respect relationships, constraints, and custom types defined in your database schema.

Securely generate a private JWT signing key for use in the CLI or to import in the dashboard.

Supported algorithms: ES256 - ECDSA with P-256 curve and SHA-256 (recommended) RS256 - RSA with SHA-256

Algorithm for signing key generation.

Append new key to existing keys file instead of overwriting.

Generate types from a database url.

Output language of the generated types.

Generate types from the linked project.

Generate types from the local dev database.

Generate types compatible with PostgREST v9 and below.

Generate types from a project ID.

Maximum timeout allowed for the database query.

Comma separated list of schema to include.

Access control for Swift generated types.

Pulls schema changes from a remote database. A new migration file will be created under supabase/migrations directory.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Optionally, a new row can be inserted into the migration history table to reflect the current state of the remote database.

If no entries exist in the migration history table, pg_dump will be used to capture all contents of the remote schemas you have created. Otherwise, this command will only diff schema changes against the remote database, similar to running db diff --linked.

Pulls from the database specified by the connection string (must be percent-encoded).

Pulls from the linked project.

Pulls from the local database.

Password to your remote Postgres database.

Comma separated list of schema to include.

Pushes all local migrations to a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

The first time this command is run, a migration history table will be created under supabase_migrations.schema_migrations. After successfully applying a migration, a new row will be inserted into the migration history table with timestamp as its unique id. Subsequent pushes will skip migrations that have already been applied.

If you need to mutate the migration history table, such as deleting existing entries or inserting new entries without actually running the migration, use the migration repair command.

Use the --dry-run flag to view the list of changes before applying.

Pushes to the database specified by the connection string (must be percent-encoded).

Print the migrations that would be applied, but don't actually apply them.

Include all migrations not found on remote history table.

Include custom roles from supabase/roles.sql.

Include seed data from your config.

Pushes to the linked project.

Pushes to the local database.

Password to your remote Postgres database.

Resets the local database to a clean state.

Requires the local development stack to be started by running supabase start.

Recreates the local Postgres container and applies all local migrations found in supabase/migrations directory. If test data is defined in supabase/seed.sql, it will be seeded after the migrations are run. Any other data or schema changes made during local development will be discarded.

When running db reset with --linked or --db-url flag, a SQL script is executed to identify and drop all user created entities in the remote database. Since Postgres roles are cluster level entities, any custom roles created through the dashboard or supabase/roles.sql will not be deleted by remote reset.

Resets the database specified by the connection string (must be percent-encoded).

Reset up to the last n migration versions.

Resets the linked project with local migrations.

Resets the local database with local migrations.

Skip running the seed script after reset.

Reset up to the specified version.

Dumps contents from a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Runs pg_dump in a container with additional flags to exclude Supabase managed schemas. The ignored schemas include auth, storage, and those created by extensions.

The default dump does not contain any data or custom roles. To dump those contents explicitly, specify either the --data-only and --role-only flag.

Dumps only data records.

Dumps from the database specified by the connection string (must be percent-encoded).

Prints the pg_dump script that would be executed.

List of schema.tables to exclude from data-only dump.

File path to save the dumped contents.

Keeps commented lines from pg_dump output.

Dumps from the linked project.

Dumps from the local database.

Password to your remote Postgres database.

Dumps only cluster roles.

Comma separated list of schema to include.

Use copy statements in place of inserts.

Diffs schema changes made to the local or remote database.

Requires the local development stack to be running when diffing against the local database. To diff against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs djrobstep/migra in a container to compare schema differences between the target database and a shadow database. The shadow database is created by applying migrations in local supabase/migrations directory in a separate container. Output is written to stdout by default. For convenience, you can also save the schema diff as a new migration file by passing in -f flag.

By default, all schemas in the target database are diffed. Use the --schema public,extensions flag to restrict diffing to a subset of schemas.

While the diff command is able to capture most schema changes, there are cases where it is known to fail. Currently, this could happen if you schema contains:

Diffs against the database specified by the connection string (must be percent-encoded).

Saves schema diff to a new migration file.

Diffs local migration files against the linked project.

Diffs local migration files against the local database.

Comma separated list of schema to include.

Use migra to generate schema diff.

Use pg-schema-diff to generate schema diff.

Use pgAdmin to generate schema diff.

Lints local database for schema errors.

Requires the local development stack to be running when linting against the local database. To lint against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs plpgsql_check extension in the local Postgres container to check for errors in all schemas. The default lint level is warning and can be raised to error via the --level flag.

To lint against specific schemas only, pass in the --schema flag.

The --fail-on flag can be used to control when the command should exit with a non-zero status code. The possible values are:

This flag is particularly useful in CI/CD pipelines where you want to fail the build based on certain lint conditions.

Lints the database specified by the connection string (must be percent-encoded).

Error level to exit with non-zero status.

Lints the linked project for schema errors.

Lints the local database for schema errors.

Comma separated list of schema to include.

Path to a logical backup file.

Creates a new migration file locally.

A supabase/migrations directory will be created if it does not already exists in your current workdir. All schema migration files must be created in this directory following the pattern <timestamp>_<name>.sql.

Outputs from other commands like db diff may be piped to migration new <name> via stdin.

Lists migration history in both local and remote databases.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Note that URL strings must be escaped according to RFC 3986.

Local migrations are stored in supabase/migrations directory while remote migrations are tracked in supabase_migrations.schema_migrations table. Only the timestamps are compared to identify any differences.

In case of discrepancies between the local and remote migration history, you can resolve them using the migration repair command.

Lists migrations of the database specified by the connection string (must be percent-encoded).

Lists migrations applied to the linked project.

Lists migrations applied to the local database.

Password to your remote Postgres database.

Fetches migrations from the database specified by the connection string (must be percent-encoded).

Fetches migration history from the linked project.

Fetches migration history from the local database.

Repairs the remote migration history table.

Requires your local project to be linked to a remote database by running supabase link.

If your local and remote migration history goes out of sync, you can repair the remote history by marking specific migrations as --status applied or --status reverted. Marking as reverted will delete an existing record from the migration history table while marking as applied will insert a new record.

For example, your migration history may look like the table below, with missing entries in either local or remote.

To reset your migration history to a clean state, first delete your local migration file.

Then mark the remote migration 20230103054303 as reverted.

Now you can run db pull again to dump the remote schema as a local migration file.

Repairs migrations of the database specified by the connection string (must be percent-encoded).

Repairs the migration history of the linked project.

Repairs the migration history of the local database.

Password to your remote Postgres database.

Version status to update.

Squashes local schema migrations to a single migration file.

The squashed migration is equivalent to a schema only dump of the local database after applying existing migration files. This is especially useful when you want to remove repeated modifications of the same schema from your migration history.

However, one limitation is that data manipulation statements, such as insert, update, or delete, are omitted from the squashed migration. You will have to add them back manually in a new migration file. This includes cron jobs, storage buckets, and any encrypted secrets in vault.

By default, the latest <timestamp>_<name>.sql file will be updated to contain the squashed migration. You can override the target version using the --version <timestamp> flag.

If your supabase/migrations directory is empty, running supabase squash will do nothing.

Squashes migrations of the database specified by the connection string (must be percent-encoded).

Squashes the migration history of the linked project.

Squashes the migration history of the local database.

Password to your remote Postgres database.

Squash up to the specified version.

Applies migrations to the database specified by the connection string (must be percent-encoded).

Include all migrations not found on remote history table.

Applies pending migrations to the linked project.

Applies pending migrations to the local database.

Seeds the linked project.

Seeds the local database.

This command displays an estimation of table "bloat" - Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will asynchronously clean the dead tuples. Sometimes the autovaccum is unable to work fast enough to reduce or prevent tables from becoming bloated. High bloat can slow down queries, cause excessive IOPS and waste space in your database.

Tables with a high bloat ratio should be investigated to see if there are vacuuming is not quick enough or there are other issues.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows you statements that are currently holding locks and blocking, as well as the statement that is being blocked. This can be used in conjunction with inspect db locks to determine which statements need to be terminated in order to resolve lock contention.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command is much like the supabase inspect db outliers command, but ordered by the number of times a statement has been called.

You can use this information to see which queries are called most often, which can potentially be good candidates for optimisation.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays queries that have taken out an exclusive lock on a relation. Exclusive locks typically prevent other operations on that relation from taking place, and can be a cause of "hung" queries that are waiting for a lock to be granted.

If you see a query that is hanging for a very long time or causing blocking issues you may consider killing the query by connecting to the database and running SELECT pg_cancel_backend(PID); to cancel the query. If the query still does not stop you can force a hard stop by running SELECT pg_terminate_backend(PID);

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays currently running queries, that have been running for longer than 5 minutes, descending by duration. Very long running queries can be a source of multiple issues, such as preventing DDL statements completing or vacuum being unable to update relfrozenxid.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays statements, obtained from pg_stat_statements, ordered by the amount of time to execute in aggregate. This includes the statement itself, the total execution time for that statement, the proportion of total execution time for all statements that statement has taken up, the number of times that statement has been called, and the amount of time that statement spent on synchronous I/O (reading/writing from the file system).

Typically, an efficient query will have an appropriate ratio of calls to total execution time, with as little time spent on I/O as possible. Queries that have a high total execution time but low call count should be investigated to improve their performance. Queries that have a high proportion of execution time being spent on synchronous I/O should also be investigated.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows information about logical replication slots that are setup on the database. It shows if the slot is active, the state of the WAL sender process ('startup', 'catchup', 'streaming', 'backup', 'stopping') the replication client address and the replication lag in GB.

This command is useful to check that the amount of replication lag is as low as possible, replication lag can occur due to network latency issues, slow disk I/O, long running transactions or lack of ability for the subscriber to consume WAL fast enough.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command analyzes table I/O patterns to show read/write activity ratios based on block-level operations. It combines data from PostgreSQL's pg_stat_user_tables (for tuple operations) and pg_statio_user_tables (for block I/O) to categorize each table's workload profile.

The command classifies tables into categories:

Note: This command only displays tables that have had both read and write activity. Tables with no I/O operations are not shown. The classification ratio threshold (default: 5:1) determines when a table is considered "heavy" in one direction versus balanced.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This shows you stats about the vacuum activities for each table. Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will aysnchronously clean the dead tuples.

The command lists when the last vacuum and last auto vacuum took place, the row count on the table as well as the count of dead rows and whether autovacuum is expected to run or not. If the number of dead rows is much higher than the row count, or if an autovacuum is expected but has not been performed for some time, this can indicate that autovacuum is not able to keep up and that your vacuum settings need to be tweaked or that you require more compute or disk IOPS to allow autovaccum to complete.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Path to save CSV files in

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Create an organization for the logged-in user.

List all organizations the logged-in user belongs.

Provides tools for creating and managing your Supabase projects.

This command group allows you to list all projects in your organizations, create new projects, delete existing projects, and retrieve API keys. These operations help you manage your Supabase infrastructure programmatically without using the dashboard.

Project management via CLI is especially useful for automation scripts and when you need to provision environments in a repeatable way.

Database password of the project.

Organization ID to create the project in.

Select a region close to you for the best performance.

Select a desired instance size for your project.

List all Supabase projects the logged-in user can access.

Project ref of the Supabase project.

Updates the configurations of a linked Supabase project with the local supabase/config.toml file.

This command allows you to manage project configuration as code by defining settings locally and then pushing them to your remote project.

Project ref of the Supabase project.

Create a preview branch for the linked project.

URL to notify when branch is active healthy.

Whether to create a persistent branch.

Select a region to deploy the branch database.

Select a desired instance size for the branch database.

Whether to clone production data to the branch database.

Project ref of the Supabase project.

List all preview branches of the linked project.

Project ref of the Supabase project.

Retrieve details of the specified preview branch.

Project ref of the Supabase project.

Update a preview branch by its name or ID.

Change the associated git branch.

Rename the preview branch.

URL to notify when branch is active healthy.

Switch between ephemeral and persistent branch.

Override the current branch status.

Project ref of the Supabase project.

Project ref of the Supabase project.

Project ref of the Supabase project.

Delete a preview branch by its name or ID.

Project ref of the Supabase project.

Manage Supabase Edge Functions.

Supabase Edge Functions are server-less functions that run close to your users.

Edge Functions allow you to execute custom server-side code without deploying or scaling a traditional server. They're ideal for handling webhooks, custom API endpoints, data validation, and serving personalized content.

Edge Functions are written in TypeScript and run on Deno compatible edge runtime, which is a secure runtime with no package management needed, fast cold starts, and built-in security.

Creates a new Edge Function with boilerplate code in the supabase/functions directory.

This command generates a starter TypeScript file with the necessary Deno imports and a basic function structure. The function is created as a new directory with the name you specify, containing an index.ts file with the function code.

After creating the function, you can edit it locally and then use supabase functions serve to test it before deploying with supabase functions deploy.

List all Functions in the linked Supabase project.

Project ref of the Supabase project.

Download the source code for a Function from the linked Supabase project.

Project ref of the Supabase project.

Unbundle functions server-side without using Docker.

Serve all Functions locally.

supabase functions serve command includes additional flags to assist developers in debugging Edge Functions via the v8 inspector protocol, allowing for debugging via Chrome DevTools, VS Code, and IntelliJ IDEA for example. Refer to the docs guide for setup instructions.

--inspect-mode [ run | brk | wait ]

Additionally, the following properties can be customized via supabase/config.toml under edge_runtime section.

Path to an env file to be populated to the Function environment.

Path to import map file.

Alias of --inspect-mode brk.

Allow inspecting the main worker.

Activate inspector capability for debugging.

Disable JWT verification for the Function.

Deploy a Function to the linked Supabase project.

Path to import map file.

Maximum number of parallel jobs.

Disable JWT verification for the Function.

Project ref of the Supabase project.

Delete Functions that exist in Supabase project but not locally.

Bundle functions server-side without using Docker.

Delete a Function from the linked Supabase project. This does NOT remove the Function locally.

Project ref of the Supabase project.

Provides tools for managing environment variables and secrets for your Supabase project.

This command group allows you to set, unset, and list secrets that are securely stored and made available to Edge Functions as environment variables.

Secrets management through the CLI is useful for:

Secrets can be set individually or loaded from .env files for convenience.

Set a secret(s) to the linked Supabase project.

Read secrets from a .env file.

Project ref of the Supabase project.

List all secrets in the linked project.

Project ref of the Supabase project.

Unset a secret(s) from the linked Supabase project.

Project ref of the Supabase project.

Recursively list a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Custom Cache-Control header for HTTP upload.

Custom Content-Type header for HTTP upload.

Maximum number of parallel jobs.

Recursively copy a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively move a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively remove a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Add and configure a new connection to a SSO identity provider to your Supabase project.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Comma separated list of email domains to associate with the added identity provider.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Type of identity provider (according to supported protocol).

Project ref of the Supabase project.

List all connections to a SSO identity provider to your Supabase project.

Project ref of the Supabase project.

Provides the information about an established connection to an identity provider. You can use --metadata to obtain the raw SAML 2.0 Metadata XML document stored in your project's configuration.

Show SAML 2.0 XML Metadata only

Project ref of the Supabase project.

Returns all of the important SSO information necessary for your project to be registered with a SAML 2.0 compatible identity provider.

Project ref of the Supabase project.

Update the configuration settings of a already added SSO identity provider.

Add this comma separated list of email domains to the identity provider.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Replace domains with this comma separated list of email domains.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Remove this comma separated list of email domains from the identity provider.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Project ref of the Supabase project.

Remove a connection to an already added SSO identity provider. Removing the provider will prevent existing users from logging in. Please treat this command with care.

Project ref of the Supabase project.

Manage custom domain names for Supabase projects.

Use of custom domains and vanity subdomains is mutually exclusive.

Activates the custom hostname configuration for a project.

This reconfigures your Supabase project to respond to requests on your custom hostname.

After the custom hostname is activated, your project's third-party auth providers will no longer function on the Supabase-provisioned subdomain. Please refer to Prepare to activate your domain section in our documentation to learn more about the steps you need to follow.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Create a custom hostname for your Supabase project.

Expects your custom hostname to have a CNAME record to your Supabase project's subdomain.

The custom hostname to use for your Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Retrieve the custom hostname config for your project, as stored in the Supabase platform.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Manage vanity subdomains for Supabase projects.

Usage of vanity subdomains and custom domains is mutually exclusive.

Activate a vanity subdomain for your Supabase project.

This reconfigures your Supabase project to respond to requests on your vanity subdomain. After the vanity subdomain is activated, your project's auth services will no longer function on the {project-ref}.{supabase-domain} hostname.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

Deletes the vanity subdomain for a project, and reverts to using the project ref for routing.

enable experimental features

Project ref of the Supabase project.

Network bans are IPs that get temporarily blocked if their traffic pattern looks abusive (e.g. multiple failed auth attempts).

The subcommands help you view the current bans, and unblock IPs if desired.

enable experimental features

Project ref of the Supabase project.

IP to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Append to existing restrictions instead of replacing them.

Bypass some of the CIDR validation checks.

CIDR to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Whether the DB should disable SSL enforcement for all external connections.

Whether the DB should enable SSL enforcement for all external connections.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Overriding the default Postgres config could result in unstable database behavior. Custom configuration also overrides the optimizations generated based on the compute add-ons in use.

Config overrides specified as a 'key=value' pair

Do not restart the database after updating config.

If true, replaces all existing overrides with the ones provided. If false (default), merges existing overrides with the ones provided.

enable experimental features

Project ref of the Supabase project.

Delete specific config overrides, reverting them to their default values.

Config keys to delete (comma-separated)

Do not restart the database after deleting config.

enable experimental features

Project ref of the Supabase project.

List all SQL snippets of the linked project.

Project ref of the Supabase project.

Download contents of the specified SQL snippet.

Project ref of the Supabase project.

Generate the autocompletion script for supabase for the specified shell. See each sub-command's help for details on how to use the generated script.

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need to enable it. You can execute the following once:

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for powershell.

To load completions in your current shell session:

To load completions for every new session, add the output of the above command to your powershell profile.

disable completion descriptions

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package. If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

**Examples:**

Example 1 (unknown):
```unknown
1supabase bootstrap [template] [flags]
```

Example 2 (unknown):
```unknown
1supabase init [flags]
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1Finished supabase init.
```

---

## Postgres Changes | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/postgres-changes?queryGroups=language&language=js

**Contents:**
- Postgres Changes
- Listen to Postgres changes using Supabase Realtime.
- Quick start#
  - Set up a Supabase project with a 'todos' table
  - Allow anonymous access
  - Enable Postgres replication
  - Install the client
  - Create the client
  - Listen to changes by schema
  - Insert dummy data

Listen to Postgres changes using Supabase Realtime.

Let's explore how to use Realtime's Postgres Changes feature to listen to database events.

In this example we'll set up a database table, secure it with Row Level Security, and subscribe to all changes using the Supabase client libraries.

Create a new project in the Supabase Dashboard.

After your project is ready, create a table in your Supabase database. You can do this with either the Table interface or the SQL Editor.

In this example we'll turn on Row Level Security for this table and allow anonymous access. In production, be sure to secure your application with the appropriate permissions.

Go to your project's Publications settings, and under supabase_realtime, toggle on the tables you want to listen to.

Alternatively, add tables to the supabase_realtime publication by running the given SQL:

Install the Supabase JavaScript client.

This client will be used to listen to Postgres changes.

Listen to changes on all tables in the public schema by setting the schema property to 'public' and event name to *. The event name can be one of:

The channel name can be any string except 'realtime'.

Now we can add some data to our table which will trigger the channelA event handler.

You can use the Supabase client libraries to subscribe to database changes.

Subscribe to specific schema events using the schema parameter:

The channel name can be any string except 'realtime'.

Use the event parameter to listen only to database INSERTs:

The channel name can be any string except 'realtime'.

Use the event parameter to listen only to database UPDATEs:

The channel name can be any string except 'realtime'.

Use the event parameter to listen only to database DELETEs:

The channel name can be any string except 'realtime'.

Subscribe to specific table events using the table parameter:

The channel name can be any string except 'realtime'.

To listen to different events and schema/tables/filters combinations with the same channel:

Use the filter parameter for granular changes:

Realtime offers filters so you can specify the data your client receives at a more granular level.

To listen to changes when a column's value in a table equals a client-specified value:

This filter uses Postgres's = filter.

To listen to changes when a column's value in a table does not equal a client-specified value:

This filter uses Postgres's != filter.

To listen to changes when a column's value in a table is less than a client-specified value:

This filter uses Postgres's < filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table is less than or equal to a client-specified value:

This filter uses Postgres' <= filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table is greater than a client-specified value:

This filter uses Postgres's > filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table is greater than or equal to a client-specified value:

This filter uses Postgres's >= filter, so it works for non-numeric types. Make sure to check the expected behavior of the compared data's type.

To listen to changes when a column's value in a table equals any client-specified values:

This filter uses Postgres's = ANY. Realtime allows a maximum of 100 values for this filter.

By default, only new record changes are sent but if you want to receive the old record (previous values) whenever you UPDATE or DELETE a record, you can set the replica identity of your table to full:

RLS policies are not applied to DELETE statements, because there is no way for Postgres to verify that a user has access to a deleted record. When RLS is enabled and replica identity is set to full on a table, the old record contains only the primary key(s).

Postgres Changes works out of the box for tables in the public schema. You can listen to tables in your private schemas by granting table SELECT permissions to the database role found in your access token. You can run a query similar to the following:

We strongly encourage you to enable RLS and create policies for tables in private schemas. Otherwise, any role you grant access to will have unfettered read access to the table.

You may choose to sign your own tokens to customize claims that can be checked in your RLS policies.

Your project JWT secret is found with your Project API keys in your dashboard.

Do not expose the service_role token on the client because the role is authorized to bypass row-level security.

To use your own JWT with Realtime make sure to set the token after instantiating the Supabase client and before connecting to a Channel.

You will need to refresh tokens on your own, but once generated, you can pass them to Realtime.

For example, if you're using the supabase-js v2 client then you can pass your token like this:

You can't filter Delete events when tracking Postgres Changes. This limitation is due to the way changes are pulled from Postgres.

Realtime currently does not work when table names contain spaces.

Realtime systems usually require forethought because of their scaling dynamics. For the Postgres Changes feature, every change event must be checked to see if the subscribed user has access. For instance, if you have 100 users subscribed to a table where you make a single insert, it will then trigger 100 "reads": one for each user.

There can be a database bottleneck which limits message throughput. If your database cannot authorize the changes rapidly enough, the changes will be delayed until you receive a timeout.

Database changes are processed on a single thread to maintain the change order. That means compute upgrades don't have a large effect on the performance of Postgres change subscriptions. You can estimate the expected maximum throughput for your database below.

If you are using Postgres Changes at scale, you should consider using separate "public" table without RLS and filters. Alternatively, you can use Realtime server-side only and then re-stream the changes to your clients using a Realtime Broadcast.

Enter your database settings to estimate the maximum throughput for your instance:

Don't forget to run your own benchmarks to make sure that the performance is acceptable for your use case.

We are making many improvements to Realtime's Postgres Changes. If you are uncertain about the performance of your use case, reach out using Support Form and we will be happy to help you. We have a team of engineers that can advise you on the best solution for your use-case.

**Examples:**

Example 1 (unknown):
```unknown
1-- Create a table called "todos"2-- with a column to store tasks.3create table todos (4  id serial primary key,5  task text6);
```

Example 2 (unknown):
```unknown
1-- Turn on security2alter table "todos"3enable row level security;45-- Allow anonymous access6create policy "Allow anonymous access"7on todos8for select9to anon10using (true);
```

Example 3 (unknown):
```unknown
1alter publication supabase_realtime2add table your_table_name;
```

Example 4 (unknown):
```unknown
1npm install @supabase/supabase-js
```

---

## Collections | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/python/collections

**Contents:**
- Collections

A collection is an group of vector records. Records can be added to or updated in a collection. Collections can be queried at any time, but should be indexed for scalable query performance.

Each vector record has the form:

Underneath every vecs collection is a Postgres table

where rows in the table map 1:1 with vecs vector records.

It is safe to select collection tables from outside the vecs client but issuing DDL is not recommended.

**Examples:**

Example 1 (unknown):
```unknown
1Record (2    id: String3    vec: Numeric[]4    metadata: JSON5)
```

Example 2 (unknown):
```unknown
1("vec1", [0.1, 0.2, 0.3], {"year": 1990})
```

Example 3 (unknown):
```unknown
1create table <collection_name> (2    id string primary key,3    vec vector(<dimension>),4    metadata jsonb5)
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-postgres-config-update

**Contents:**
- Supabase CLI
  - Additional links#
- Global flags
  - Flags
- supabase bootstrap
  - Usage
  - Flags
- supabase init
  - Usage
  - Flags

The Supabase CLI provides tools to develop your project locally and deploy to the Supabase Platform. The CLI is still under development, but it contains all the functionality for working with your Supabase projects and the Supabase Platform.

Supabase CLI supports global flags for every command.

create a support ticket for any CLI error

output debug logs to stderr

lookup domain names using the specified resolver

enable experimental features

use the specified docker network instead of a generated one

output format of status variables

use a specific profile for connecting to Supabase API

path to a Supabase project directory

answer yes to all prompts

Password to your remote Postgres database.

Initialize configurations for Supabase local development.

A supabase/config.toml file is created in your current working directory. This configuration is specific to each local project.

You may override the directory path by specifying the SUPABASE_WORKDIR environment variable or --workdir flag.

In addition to config.toml, the supabase directory may also contain other Supabase objects, such as migrations, functions, tests, etc.

Overwrite existing supabase/config.toml.

Use OrioleDB storage engine for Postgres.

Generate IntelliJ IDEA settings for Deno.

Generate VS Code settings for Deno.

Connect the Supabase CLI to your Supabase account by logging in with your personal access token.

Your access token is stored securely in native credentials storage. If native credentials storage is unavailable, it will be written to a plain text file at ~/.supabase/access-token.

If this behavior is not desired, such as in a CI environment, you may skip login by specifying the SUPABASE_ACCESS_TOKEN environment variable in other commands.

The Supabase CLI uses the stored token to access Management APIs for projects, functions, secrets, etc.

Name that will be used to store token in your settings

Do not open browser automatically

Use provided token instead of automatic login flow

Link your local development project to a hosted Supabase project.

PostgREST configurations are fetched from the Supabase platform and validated against your local configuration file.

Optionally, database settings can be validated if you provide a password. Your database password is saved in native credentials storage if available.

If you do not want to be prompted for the database password, such as in a CI environment, you may specify it explicitly via the SUPABASE_DB_PASSWORD environment variable.

Some commands like db dump, db push, and db pull require your project to be linked first.

Password to your remote Postgres database.

Project ref of the Supabase project.

Use direct connection instead of pooler.

Starts the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All service containers are started by default. You can exclude those not needed by passing in -x flag. To exclude multiple containers, either pass in a comma separated string, such as -x gotrue,imgproxy, or specify -x flag multiple times.

It is recommended to have at least 7GB of RAM to start all services.

Health checks are automatically added to verify the started containers. Use --ignore-health-check flag to ignore these errors.

Names of containers to not start. [gotrue,realtime,storage-api,imgproxy,kong,mailpit,postgrest,postgres-meta,studio,edge-runtime,logflare,vector,supavisor]

Ignore unhealthy services and exit 0

Stops the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All Docker resources are maintained across restarts. Use --no-backup flag to reset your local development data between restarts.

Use the --all flag to stop all local Supabase projects instances on the machine. Use with caution with --no-backup as it will delete all supabase local projects data.

Stop all local Supabase instances from all projects across the machine.

Deletes all data volumes after stopping.

Local project ID to stop.

Shows status of the Supabase local development stack.

Requires the local development stack to be started by running supabase start or supabase db start.

You can export the connection parameters for initializing supabase-js locally by specifying the -o env flag. Supported parameters include JWT_SECRET, ANON_KEY, and SERVICE_ROLE_KEY.

Override specific variable names.

Executes pgTAP tests against the local database.

Requires the local development stack to be started by running supabase start.

Runs pg_prove in a container with unit test files volume mounted from supabase/tests directory. The test file can be suffixed by either .sql or .pg extension.

Since each test is wrapped in its own transaction, it will be individually rolled back regardless of success or failure.

Tests the database specified by the connection string (must be percent-encoded).

Runs pgTAP tests on the linked project.

Runs pgTAP tests on the local database.

Template framework to generate.

Automatically generates type definitions based on your Postgres database schema.

This command connects to your database (local or remote) and generates typed definitions that match your database tables, views, and stored procedures. By default, it generates TypeScript definitions, but also supports Go and Swift.

Generated types give you type safety and autocompletion when working with your database in code, helping prevent runtime errors and improving developer experience.

The types respect relationships, constraints, and custom types defined in your database schema.

Securely generate a private JWT signing key for use in the CLI or to import in the dashboard.

Supported algorithms: ES256 - ECDSA with P-256 curve and SHA-256 (recommended) RS256 - RSA with SHA-256

Algorithm for signing key generation.

Append new key to existing keys file instead of overwriting.

Generate types from a database url.

Output language of the generated types.

Generate types from the linked project.

Generate types from the local dev database.

Generate types compatible with PostgREST v9 and below.

Generate types from a project ID.

Maximum timeout allowed for the database query.

Comma separated list of schema to include.

Access control for Swift generated types.

Pulls schema changes from a remote database. A new migration file will be created under supabase/migrations directory.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Optionally, a new row can be inserted into the migration history table to reflect the current state of the remote database.

If no entries exist in the migration history table, pg_dump will be used to capture all contents of the remote schemas you have created. Otherwise, this command will only diff schema changes against the remote database, similar to running db diff --linked.

Pulls from the database specified by the connection string (must be percent-encoded).

Pulls from the linked project.

Pulls from the local database.

Password to your remote Postgres database.

Comma separated list of schema to include.

Pushes all local migrations to a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

The first time this command is run, a migration history table will be created under supabase_migrations.schema_migrations. After successfully applying a migration, a new row will be inserted into the migration history table with timestamp as its unique id. Subsequent pushes will skip migrations that have already been applied.

If you need to mutate the migration history table, such as deleting existing entries or inserting new entries without actually running the migration, use the migration repair command.

Use the --dry-run flag to view the list of changes before applying.

Pushes to the database specified by the connection string (must be percent-encoded).

Print the migrations that would be applied, but don't actually apply them.

Include all migrations not found on remote history table.

Include custom roles from supabase/roles.sql.

Include seed data from your config.

Pushes to the linked project.

Pushes to the local database.

Password to your remote Postgres database.

Resets the local database to a clean state.

Requires the local development stack to be started by running supabase start.

Recreates the local Postgres container and applies all local migrations found in supabase/migrations directory. If test data is defined in supabase/seed.sql, it will be seeded after the migrations are run. Any other data or schema changes made during local development will be discarded.

When running db reset with --linked or --db-url flag, a SQL script is executed to identify and drop all user created entities in the remote database. Since Postgres roles are cluster level entities, any custom roles created through the dashboard or supabase/roles.sql will not be deleted by remote reset.

Resets the database specified by the connection string (must be percent-encoded).

Reset up to the last n migration versions.

Resets the linked project with local migrations.

Resets the local database with local migrations.

Skip running the seed script after reset.

Reset up to the specified version.

Dumps contents from a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Runs pg_dump in a container with additional flags to exclude Supabase managed schemas. The ignored schemas include auth, storage, and those created by extensions.

The default dump does not contain any data or custom roles. To dump those contents explicitly, specify either the --data-only and --role-only flag.

Dumps only data records.

Dumps from the database specified by the connection string (must be percent-encoded).

Prints the pg_dump script that would be executed.

List of schema.tables to exclude from data-only dump.

File path to save the dumped contents.

Keeps commented lines from pg_dump output.

Dumps from the linked project.

Dumps from the local database.

Password to your remote Postgres database.

Dumps only cluster roles.

Comma separated list of schema to include.

Use copy statements in place of inserts.

Diffs schema changes made to the local or remote database.

Requires the local development stack to be running when diffing against the local database. To diff against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs djrobstep/migra in a container to compare schema differences between the target database and a shadow database. The shadow database is created by applying migrations in local supabase/migrations directory in a separate container. Output is written to stdout by default. For convenience, you can also save the schema diff as a new migration file by passing in -f flag.

By default, all schemas in the target database are diffed. Use the --schema public,extensions flag to restrict diffing to a subset of schemas.

While the diff command is able to capture most schema changes, there are cases where it is known to fail. Currently, this could happen if you schema contains:

Diffs against the database specified by the connection string (must be percent-encoded).

Saves schema diff to a new migration file.

Diffs local migration files against the linked project.

Diffs local migration files against the local database.

Comma separated list of schema to include.

Use migra to generate schema diff.

Use pg-schema-diff to generate schema diff.

Use pgAdmin to generate schema diff.

Lints local database for schema errors.

Requires the local development stack to be running when linting against the local database. To lint against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs plpgsql_check extension in the local Postgres container to check for errors in all schemas. The default lint level is warning and can be raised to error via the --level flag.

To lint against specific schemas only, pass in the --schema flag.

The --fail-on flag can be used to control when the command should exit with a non-zero status code. The possible values are:

This flag is particularly useful in CI/CD pipelines where you want to fail the build based on certain lint conditions.

Lints the database specified by the connection string (must be percent-encoded).

Error level to exit with non-zero status.

Lints the linked project for schema errors.

Lints the local database for schema errors.

Comma separated list of schema to include.

Path to a logical backup file.

Creates a new migration file locally.

A supabase/migrations directory will be created if it does not already exists in your current workdir. All schema migration files must be created in this directory following the pattern <timestamp>_<name>.sql.

Outputs from other commands like db diff may be piped to migration new <name> via stdin.

Lists migration history in both local and remote databases.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Note that URL strings must be escaped according to RFC 3986.

Local migrations are stored in supabase/migrations directory while remote migrations are tracked in supabase_migrations.schema_migrations table. Only the timestamps are compared to identify any differences.

In case of discrepancies between the local and remote migration history, you can resolve them using the migration repair command.

Lists migrations of the database specified by the connection string (must be percent-encoded).

Lists migrations applied to the linked project.

Lists migrations applied to the local database.

Password to your remote Postgres database.

Fetches migrations from the database specified by the connection string (must be percent-encoded).

Fetches migration history from the linked project.

Fetches migration history from the local database.

Repairs the remote migration history table.

Requires your local project to be linked to a remote database by running supabase link.

If your local and remote migration history goes out of sync, you can repair the remote history by marking specific migrations as --status applied or --status reverted. Marking as reverted will delete an existing record from the migration history table while marking as applied will insert a new record.

For example, your migration history may look like the table below, with missing entries in either local or remote.

To reset your migration history to a clean state, first delete your local migration file.

Then mark the remote migration 20230103054303 as reverted.

Now you can run db pull again to dump the remote schema as a local migration file.

Repairs migrations of the database specified by the connection string (must be percent-encoded).

Repairs the migration history of the linked project.

Repairs the migration history of the local database.

Password to your remote Postgres database.

Version status to update.

Squashes local schema migrations to a single migration file.

The squashed migration is equivalent to a schema only dump of the local database after applying existing migration files. This is especially useful when you want to remove repeated modifications of the same schema from your migration history.

However, one limitation is that data manipulation statements, such as insert, update, or delete, are omitted from the squashed migration. You will have to add them back manually in a new migration file. This includes cron jobs, storage buckets, and any encrypted secrets in vault.

By default, the latest <timestamp>_<name>.sql file will be updated to contain the squashed migration. You can override the target version using the --version <timestamp> flag.

If your supabase/migrations directory is empty, running supabase squash will do nothing.

Squashes migrations of the database specified by the connection string (must be percent-encoded).

Squashes the migration history of the linked project.

Squashes the migration history of the local database.

Password to your remote Postgres database.

Squash up to the specified version.

Applies migrations to the database specified by the connection string (must be percent-encoded).

Include all migrations not found on remote history table.

Applies pending migrations to the linked project.

Applies pending migrations to the local database.

Seeds the linked project.

Seeds the local database.

This command displays an estimation of table "bloat" - Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will asynchronously clean the dead tuples. Sometimes the autovaccum is unable to work fast enough to reduce or prevent tables from becoming bloated. High bloat can slow down queries, cause excessive IOPS and waste space in your database.

Tables with a high bloat ratio should be investigated to see if there are vacuuming is not quick enough or there are other issues.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows you statements that are currently holding locks and blocking, as well as the statement that is being blocked. This can be used in conjunction with inspect db locks to determine which statements need to be terminated in order to resolve lock contention.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command is much like the supabase inspect db outliers command, but ordered by the number of times a statement has been called.

You can use this information to see which queries are called most often, which can potentially be good candidates for optimisation.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays queries that have taken out an exclusive lock on a relation. Exclusive locks typically prevent other operations on that relation from taking place, and can be a cause of "hung" queries that are waiting for a lock to be granted.

If you see a query that is hanging for a very long time or causing blocking issues you may consider killing the query by connecting to the database and running SELECT pg_cancel_backend(PID); to cancel the query. If the query still does not stop you can force a hard stop by running SELECT pg_terminate_backend(PID);

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays currently running queries, that have been running for longer than 5 minutes, descending by duration. Very long running queries can be a source of multiple issues, such as preventing DDL statements completing or vacuum being unable to update relfrozenxid.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays statements, obtained from pg_stat_statements, ordered by the amount of time to execute in aggregate. This includes the statement itself, the total execution time for that statement, the proportion of total execution time for all statements that statement has taken up, the number of times that statement has been called, and the amount of time that statement spent on synchronous I/O (reading/writing from the file system).

Typically, an efficient query will have an appropriate ratio of calls to total execution time, with as little time spent on I/O as possible. Queries that have a high total execution time but low call count should be investigated to improve their performance. Queries that have a high proportion of execution time being spent on synchronous I/O should also be investigated.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows information about logical replication slots that are setup on the database. It shows if the slot is active, the state of the WAL sender process ('startup', 'catchup', 'streaming', 'backup', 'stopping') the replication client address and the replication lag in GB.

This command is useful to check that the amount of replication lag is as low as possible, replication lag can occur due to network latency issues, slow disk I/O, long running transactions or lack of ability for the subscriber to consume WAL fast enough.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command analyzes table I/O patterns to show read/write activity ratios based on block-level operations. It combines data from PostgreSQL's pg_stat_user_tables (for tuple operations) and pg_statio_user_tables (for block I/O) to categorize each table's workload profile.

The command classifies tables into categories:

Note: This command only displays tables that have had both read and write activity. Tables with no I/O operations are not shown. The classification ratio threshold (default: 5:1) determines when a table is considered "heavy" in one direction versus balanced.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This shows you stats about the vacuum activities for each table. Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will aysnchronously clean the dead tuples.

The command lists when the last vacuum and last auto vacuum took place, the row count on the table as well as the count of dead rows and whether autovacuum is expected to run or not. If the number of dead rows is much higher than the row count, or if an autovacuum is expected but has not been performed for some time, this can indicate that autovacuum is not able to keep up and that your vacuum settings need to be tweaked or that you require more compute or disk IOPS to allow autovaccum to complete.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Path to save CSV files in

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Create an organization for the logged-in user.

List all organizations the logged-in user belongs.

Provides tools for creating and managing your Supabase projects.

This command group allows you to list all projects in your organizations, create new projects, delete existing projects, and retrieve API keys. These operations help you manage your Supabase infrastructure programmatically without using the dashboard.

Project management via CLI is especially useful for automation scripts and when you need to provision environments in a repeatable way.

Database password of the project.

Organization ID to create the project in.

Select a region close to you for the best performance.

Select a desired instance size for your project.

List all Supabase projects the logged-in user can access.

Project ref of the Supabase project.

Updates the configurations of a linked Supabase project with the local supabase/config.toml file.

This command allows you to manage project configuration as code by defining settings locally and then pushing them to your remote project.

Project ref of the Supabase project.

Create a preview branch for the linked project.

URL to notify when branch is active healthy.

Whether to create a persistent branch.

Select a region to deploy the branch database.

Select a desired instance size for the branch database.

Whether to clone production data to the branch database.

Project ref of the Supabase project.

List all preview branches of the linked project.

Project ref of the Supabase project.

Retrieve details of the specified preview branch.

Project ref of the Supabase project.

Update a preview branch by its name or ID.

Change the associated git branch.

Rename the preview branch.

URL to notify when branch is active healthy.

Switch between ephemeral and persistent branch.

Override the current branch status.

Project ref of the Supabase project.

Project ref of the Supabase project.

Project ref of the Supabase project.

Delete a preview branch by its name or ID.

Project ref of the Supabase project.

Manage Supabase Edge Functions.

Supabase Edge Functions are server-less functions that run close to your users.

Edge Functions allow you to execute custom server-side code without deploying or scaling a traditional server. They're ideal for handling webhooks, custom API endpoints, data validation, and serving personalized content.

Edge Functions are written in TypeScript and run on Deno compatible edge runtime, which is a secure runtime with no package management needed, fast cold starts, and built-in security.

Creates a new Edge Function with boilerplate code in the supabase/functions directory.

This command generates a starter TypeScript file with the necessary Deno imports and a basic function structure. The function is created as a new directory with the name you specify, containing an index.ts file with the function code.

After creating the function, you can edit it locally and then use supabase functions serve to test it before deploying with supabase functions deploy.

List all Functions in the linked Supabase project.

Project ref of the Supabase project.

Download the source code for a Function from the linked Supabase project.

Project ref of the Supabase project.

Unbundle functions server-side without using Docker.

Serve all Functions locally.

supabase functions serve command includes additional flags to assist developers in debugging Edge Functions via the v8 inspector protocol, allowing for debugging via Chrome DevTools, VS Code, and IntelliJ IDEA for example. Refer to the docs guide for setup instructions.

--inspect-mode [ run | brk | wait ]

Additionally, the following properties can be customized via supabase/config.toml under edge_runtime section.

Path to an env file to be populated to the Function environment.

Path to import map file.

Alias of --inspect-mode brk.

Allow inspecting the main worker.

Activate inspector capability for debugging.

Disable JWT verification for the Function.

Deploy a Function to the linked Supabase project.

Path to import map file.

Maximum number of parallel jobs.

Disable JWT verification for the Function.

Project ref of the Supabase project.

Delete Functions that exist in Supabase project but not locally.

Bundle functions server-side without using Docker.

Delete a Function from the linked Supabase project. This does NOT remove the Function locally.

Project ref of the Supabase project.

Provides tools for managing environment variables and secrets for your Supabase project.

This command group allows you to set, unset, and list secrets that are securely stored and made available to Edge Functions as environment variables.

Secrets management through the CLI is useful for:

Secrets can be set individually or loaded from .env files for convenience.

Set a secret(s) to the linked Supabase project.

Read secrets from a .env file.

Project ref of the Supabase project.

List all secrets in the linked project.

Project ref of the Supabase project.

Unset a secret(s) from the linked Supabase project.

Project ref of the Supabase project.

Recursively list a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Custom Cache-Control header for HTTP upload.

Custom Content-Type header for HTTP upload.

Maximum number of parallel jobs.

Recursively copy a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively move a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively remove a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Add and configure a new connection to a SSO identity provider to your Supabase project.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Comma separated list of email domains to associate with the added identity provider.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Type of identity provider (according to supported protocol).

Project ref of the Supabase project.

List all connections to a SSO identity provider to your Supabase project.

Project ref of the Supabase project.

Provides the information about an established connection to an identity provider. You can use --metadata to obtain the raw SAML 2.0 Metadata XML document stored in your project's configuration.

Show SAML 2.0 XML Metadata only

Project ref of the Supabase project.

Returns all of the important SSO information necessary for your project to be registered with a SAML 2.0 compatible identity provider.

Project ref of the Supabase project.

Update the configuration settings of a already added SSO identity provider.

Add this comma separated list of email domains to the identity provider.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Replace domains with this comma separated list of email domains.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Remove this comma separated list of email domains from the identity provider.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Project ref of the Supabase project.

Remove a connection to an already added SSO identity provider. Removing the provider will prevent existing users from logging in. Please treat this command with care.

Project ref of the Supabase project.

Manage custom domain names for Supabase projects.

Use of custom domains and vanity subdomains is mutually exclusive.

Activates the custom hostname configuration for a project.

This reconfigures your Supabase project to respond to requests on your custom hostname.

After the custom hostname is activated, your project's third-party auth providers will no longer function on the Supabase-provisioned subdomain. Please refer to Prepare to activate your domain section in our documentation to learn more about the steps you need to follow.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Create a custom hostname for your Supabase project.

Expects your custom hostname to have a CNAME record to your Supabase project's subdomain.

The custom hostname to use for your Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Retrieve the custom hostname config for your project, as stored in the Supabase platform.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Manage vanity subdomains for Supabase projects.

Usage of vanity subdomains and custom domains is mutually exclusive.

Activate a vanity subdomain for your Supabase project.

This reconfigures your Supabase project to respond to requests on your vanity subdomain. After the vanity subdomain is activated, your project's auth services will no longer function on the {project-ref}.{supabase-domain} hostname.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

Deletes the vanity subdomain for a project, and reverts to using the project ref for routing.

enable experimental features

Project ref of the Supabase project.

Network bans are IPs that get temporarily blocked if their traffic pattern looks abusive (e.g. multiple failed auth attempts).

The subcommands help you view the current bans, and unblock IPs if desired.

enable experimental features

Project ref of the Supabase project.

IP to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Append to existing restrictions instead of replacing them.

Bypass some of the CIDR validation checks.

CIDR to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Whether the DB should disable SSL enforcement for all external connections.

Whether the DB should enable SSL enforcement for all external connections.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Overriding the default Postgres config could result in unstable database behavior. Custom configuration also overrides the optimizations generated based on the compute add-ons in use.

Config overrides specified as a 'key=value' pair

Do not restart the database after updating config.

If true, replaces all existing overrides with the ones provided. If false (default), merges existing overrides with the ones provided.

enable experimental features

Project ref of the Supabase project.

Delete specific config overrides, reverting them to their default values.

Config keys to delete (comma-separated)

Do not restart the database after deleting config.

enable experimental features

Project ref of the Supabase project.

List all SQL snippets of the linked project.

Project ref of the Supabase project.

Download contents of the specified SQL snippet.

Project ref of the Supabase project.

Generate the autocompletion script for supabase for the specified shell. See each sub-command's help for details on how to use the generated script.

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need to enable it. You can execute the following once:

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for powershell.

To load completions in your current shell session:

To load completions for every new session, add the output of the above command to your powershell profile.

disable completion descriptions

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package. If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

**Examples:**

Example 1 (unknown):
```unknown
1supabase bootstrap [template] [flags]
```

Example 2 (unknown):
```unknown
1supabase init [flags]
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1Finished supabase init.
```

---

## pg_hashids: Short UIDs | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_hashids

**Contents:**
- pg_hashids: Short UIDs
- Enable the extension#
- Usage#
- Resources#

pg_hashids: Short UIDs

pg_hashids provides a secure way to generate short, unique, non-sequential ids from numbers. The hashes are intended to be small, easy-to-remember identifiers that can be used to obfuscate data (optionally) with a password, alphabet, and salt. For example, you may wish to hide data like user IDs, order numbers, or tracking codes in favor of pg_hashid's unique identifiers.

Suppose we have a table that stores order information, and we want to give customers a unique identifier without exposing the sequential id column. To do this, we can use pg_hashid's id_encode function.

To reverse the short_id back into an id, there is an equivalent function named id_decode.

**Examples:**

Example 1 (unknown):
```unknown
1create table orders (2  id serial primary key,3  description text,4  price_cents bigint5);67insert into orders (description, price_cents)8values ('a book', 9095);910select11  id,12  id_encode(id) as short_id,13  description,14  price_cents15from16  orders;1718  id | short_id | description | price_cents19----+----------+-------------+-------------20  1 | jR       | a book      |        909521(1 row)
```

---

## PostGIS: Geo queries | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/postgis

**Contents:**
- PostGIS: Geo queries
- Overview#
- Enable the extension#
- Examples#
  - Inserting data#
    - Restaurants
  - Order by distance#
  - Finding all data points within a bounding box#
- Troubleshooting#
- Resources#

PostGIS is a Postgres extension that allows you to interact with Geo data within Postgres. You can sort your data by geographic location, get data within certain geographic boundaries, and do much more with it.

While you may be able to store simple lat/long geographic coordinates as a set of decimals, it does not scale very well when you try to query through a large data set. PostGIS comes with special data types that are efficient, and indexable for high scalability.

The additional data types that PostGIS provides include Point, Polygon, LineString, and many more to represent different types of geographical data. In this guide, we will mainly focus on how to interact with Point type, which represents a single set of latitude and longitude. If you are interested in digging deeper, you can learn more about different data types on the data management section of PostGIS docs.

You can get started with PostGIS by enabling the PostGIS extension in your Supabase dashboard.

Now that we are ready to get started with PostGIS, let’s create a table and see how we can utilize PostGIS for some typical use cases. Let’s imagine we are creating a simple restaurant-searching app.

Let’s create our table. Each row represents a restaurant with its location stored in location column as a Point type.

We can then set a spatial index on the location column of this table.

You can insert geographical data through SQL or through our API.

Notice the order in which you pass the latitude and longitude. Longitude comes first, and is because longitude represents the x-axis of the location. Another thing to watch for is when inserting data from the client library, there is no comma between the two values, just a single space.

At this point, if you go into your Supabase dashboard and look at the data, you will notice that the value of the location column looks something like this.

We can query the restaurants table directly, but it will return the location column in the format you see above. We will create database functions so that we can use the st_y() and st_x() function to convert it back to lat and long floating values.

Sorting datasets from closest to farthest, sometimes called nearest-neighbor sort, is a very common use case in Geo-queries. PostGIS can handle it with the use of the <-> operator. <-> operator returns the two-dimensional distance between two geometries and will utilize the spatial index when used within order by clause. You can create the following database function to sort the restaurants from closest to farthest by passing the current locations as parameters.

Now you can call this function from your client using rpc() like this:

When you are working on a map-based application where the user scrolls through your map, you might want to load the data that lies within the bounding box of the map every time your users scroll. PostGIS can return the rows that are within the bounding box just by supplying the bottom left and the top right coordinates. Let’s look at what the function would look like:

The && operator used in the where statement here returns a boolean of whether the bounding box of the two geometries intersect or not. We are basically creating a bounding box from the two points and finding those points that fall under the bounding box. We are also utilizing a few different PostGIS functions:

You can call this function from your client using rpc() like this:

As of PostGIS 2.3 or newer, the PostGIS extension is no longer relocatable from one schema to another. If you need to move it from one schema to another for any reason (e.g. from the public schema to the extensions schema for security reasons), you would normally run a ALTER EXTENSION to relocate the schema. However, you will now to do the following steps:

Backup your Database to prevent data loss - You can do this through the CLI or Postgres backup tools such as pg_dumpall

Drop all dependencies you created and the PostGIS extension - DROP EXTENSION postgis CASCADE;

Enable PostGIS extension in the new schema - CREATE EXTENSION postgis SCHEMA extensions;

Restore dropped data via the Backup if necessary from step 1 with your tool of choice.

Alternatively, you can contact the Supabase Support Team and ask them to run the following SQL on your instance:

**Examples:**

Example 1 (unknown):
```unknown
1create table if not exists public.restaurants (2	id int generated by default as identity primary key,3	name text not null,4	location extensions.geography(POINT) not null5);
```

Example 2 (unknown):
```unknown
1create index restaurants_geo_index2  on public.restaurants3  using GIST (location);
```

Example 3 (unknown):
```unknown
10101000020E6100000A4DFBE0E9C91614044FAEDEBC0494240
```

Example 4 (unknown):
```unknown
1create or replace function nearby_restaurants(lat float, long float)2returns table (id public.restaurants.id%TYPE, name public.restaurants.name%TYPE, lat float, long float, dist_meters float)3set search_path = ''4language sql5as $$6  select id, name, extensions.st_y(location::extensions.geometry) as lat, extensions.st_x(location::extensions.geometry) as long, extensions.st_distance(location, extensions.st_point(long, lat)::extensions.geography) as dist_meters7  from public.restaurants8  order by location operator(extensions.<->) extensions.st_point(long, lat)::extensions.geography;9$$;
```

---

## Supavisor | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/supavisor

**Contents:**
- Supavisor
- Troubleshooting Supavisor errors

Troubleshooting Supavisor errors

Supavisor logs are available under Pooler Logs in the Dashboard. The following are common errors and their solutions:

---

## MSSQL | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/mssql

**Contents:**
- MSSQL
- Preparation#
  - Enable Wrappers#
  - Enable the SQL Server Wrapper#
  - Store your credentials (optional)#
  - Connecting to SQL Server#
  - Create a schema#
- Options#
- Entities#
  - SQL Server Tables#

You can enable the MSSQL wrapper right from the Supabase dashboard.

Microsoft SQL Server is a proprietary relational database management system developed by Microsoft.

The SQL Server Wrapper allows you to read data from Microsoft SQL Server within your Postgres database.

Before you can query SQL Server, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the mssql_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

The connection string is an ADO.NET connection string, which specifies connection parameters in semicolon-delimited string.

All parameter keys are handled case-insensitive.

We need to provide Postgres with the credentials to connect to SQL Server. We can do this using the create server command:

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

This can also be a subquery enclosed in parentheses, for example,

This is an object representing SQL Server tables and views.

Ref: Microsoft SQL Server docs

This FDW supports where, order by and limit clause pushdown.

This section describes important limitations and considerations when using this FDW:

First, create a source table in SQL Server:

Then create and query the foreign table in PostgreSQL:

Create a foreign table using a subquery:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper mssql_wrapper2  handler mssql_fdw_handler3  validator mssql_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your SQL Server connection string in Vault and retrieve the created `key_id`2select vault.create_secret(3  'Server=localhost,1433;User=sa;Password=my_password;Database=master;IntegratedSecurity=false;TrustServerCertificate=true;encrypt=DANGER_PLAINTEXT;ApplicationName=wrappers',4  'mssql',5  'MS SQL Server connection string for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server mssql_server2  foreign data wrapper mssql_wrapper3  options (4    conn_string_id '<key_ID>' -- The Key ID from above.5  );
```

---

## Supabase Docs | Database Troubleshooting

**URL:** https://supabase.com/docs/guides/database/troubleshooting

---

## Managing Indexes in PostgreSQL | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/indexes

**Contents:**
- Managing Indexes in PostgreSQL
- Create an index#
- Partial indexes#
- Ordering indexes#
- Reindexing#
- Index Advisor#
  - Understanding Index Advisor results#

Managing Indexes in PostgreSQL

An index makes your Postgres queries faster. The index is like a "table of contents" for your data - a reference list which allows queries to quickly locate a row in a given table without needing to scan the entire table (which in large tables can take a long time).

Indexes can be structured in a few different ways. The type of index chosen depends on the values you are indexing. By far the most common index type, and the default in Postgres, is the B-Tree. A B-Tree is the generalized form of a binary search tree, where nodes can have more than two children.

Even though indexes improve query performance, the Postgres query planner may not always make use of a given index when choosing which optimizations to make. Additionally indexes come with some overhead - additional writes and increased storage - so it's useful to understand how and when to use indexes, if at all.

Let's take an example table:

All the queries in this guide can be run using the SQL Editor in the Supabase Dashboard, or via psql if you're connecting directly to the database.

We might want to frequently query users based on their age:

Without an index, Postgres will scan every row in the table to find equality matches on age.

You can verify this by doing an explain on the query:

To add a simple B-Tree index you can run:

It can take a long time to build indexes on large datasets and the default behaviour of create index is to lock the table from writes.

Luckily Postgres provides us with create index concurrently which prevents blocking writes on the table, but does take a bit longer to build.

Here is a simplified diagram of the index we just created (note that in practice, nodes actually have more than two children).

You can see that in any large data set, traversing the index to locate a given value can be done in much less operations (O(log n)) than compared to scanning the table one value at a time from top to bottom (O(n)).

If you are frequently querying a subset of rows then it may be more efficient to build a partial index. In our example, perhaps we only want to match on age where deceased is false. We could build a partial index:

By default B-Tree indexes are sorted in ascending order, but sometimes you may want to provide a different ordering. Perhaps our application has a page featuring the top 10 oldest people. Here we would want to sort in descending order, and include NULL values last. For this we can use:

After a while indexes can become stale and may need rebuilding. Postgres provides a reindex command for this, but due to Postgres locks being placed on the index during this process, you may want to make use of the concurrent keyword.

Alternatively you can reindex all indexes on a particular table:

Take note that reindex can be used inside a transaction, but reindex [index/table] concurrently cannot.

Indexes can improve query performance of your tables as they grow. The Supabase Dashboard offers an Index Advisor, which suggests potential indexes to add to your tables.

For more information on the Index Advisor and its suggestions, see the index_advisor extension.

To use the Dashboard Index Advisor:

The Indexes tab shows the existing indexes used in the selected query. Note that indexes suggested in the "New Index Recommendations" section may not be used when you create them. Postgres' query planner may intentionally ignore an available index if it determines that the query will be faster without. For example, on a small table, a sequential scan might be faster than an index scan. In that case, the planner will switch to using the index as the table size grows, helping to future proof the query.

If additional indexes might improve your query, the Index Advisor shows the suggested indexes with the estimated improvement in startup and total costs:

Costs are in arbitrary units, where a single sequential page read costs 1.0 units.

**Examples:**

Example 1 (unknown):
```unknown
1create table persons (2  id bigint generated by default as identity primary key,3  age int,4  height int,5  weight int,6  name text,7  deceased boolean8);
```

Example 2 (unknown):
```unknown
1select name from persons where age = 32;
```

Example 3 (unknown):
```unknown
1explain select name from persons where age = 32;
```

Example 4 (unknown):
```unknown
1Seq Scan on persons  (cost=0.00..22.75 rows=x width=y)2Filter: (age = 32)
```

---

## The Storage Schema | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/schema/design

**Contents:**
- The Storage Schema
- Learn about the storage schema
- Modifying the schema#

Learn about the storage schema

Storage uses Postgres to store metadata regarding your buckets and objects. Users can use RLS (Row-Level Security) policies for access control. This data is stored in a dedicated schema within your project called storage.

When working with SQL, it's crucial to consider all records in Storage tables as read-only. All operations, including uploading, copying, moving, and deleting, should exclusively go through the API.

This is important because the storage schema only stores the metadata and the actual objects are stored in a provider like S3. Deleting the metadata doesn't remove the object in the underlying storage provider. This results in your object being inaccessible, but you'll still be billed for it.

Here is the schema that represents the Storage service:

You have the option to query this table directly to retrieve information about your files in Storage without the need to go through our API.

We strongly recommend refraining from making any alterations to the storage schema and treating it as read-only. This approach is important because any modifications to the schema on your end could potentially clash with our future updates, leading to downtime.

However, we encourage you to add custom indexes as they can significantly improve the performance of the RLS policies you create for enforcing access control.

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-update-postgres-config

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Import data into Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/import-data

**Contents:**
- Import data into Supabase
- How to import data into Supabase#
  - Option 1: CSV import via Supabase dashboard#
  - Option 2: Bulk import using pgloader#
  - Option 3: Using Postgres copy command#
  - Option 4: Using the Supabase API#
- Preparing to import data#
  - 1. Back up your data#
  - 2. Increase statement timeouts#
  - 3. Estimate your required disk size#

Import data into Supabase

You can import data into Supabase in multiple ways. The best method depends on your data size and app requirements.

If you're working with small datasets in development, you can experiment quickly using CSV import in the Supabase dashboard. If you're working with a large dataset in production, you should plan your data import to minimize app latency and ensure data integrity.

You have multiple options for importing your data into Supabase:

If you're importing a large dataset or importing data into production, plan ahead and prepare your database.

Supabase dashboard provides a user-friendly way to import data. However, for very large datasets, this method may not be the most efficient choice, given the size limit is 100MB. It's generally better suited for smaller datasets and quick data imports. Consider using alternative methods like pgloader for large-scale data imports.

pgloader is a powerful tool for efficiently importing data into a Postgres database that supports a wide range of source database engines, including MySQL and MS SQL.

You can use it in conjunction with Supabase by following these steps:

Install pgloader on your local machine or a server. For more info, you can refer to the official pgloader installation page.

Create a configuration file that specifies the source data and the target Supabase database (e.g., config.load). Here's an example configuration file:

Customize the source and Supabase database URL and options to fit your specific use case:

Run pgloader with the configuration file.

For databases using the Postgres engine, we recommend using the pg_dump and psql command line tools.

Read more about Bulk data loading.

The Supabase API allows you to programmatically import data into your tables. You can use various client libraries to interact with the API and perform data import operations. This approach is useful when you need to automate data imports, and it gives you fine-grained control over the process. Refer to our API guide for more details.

When importing data via the Supabase API, it's advisable to refrain from bulk imports. This helps ensure a smooth data transfer process and prevents any potential disruptions.

Read more about Rate Limiting, Resource Allocation, & Abuse Prevention.

Large data imports can affect your database performance. Failed imports can also cause data corruption. Importing data is a safe and common operation, but you should plan ahead if you're importing a lot of data, or if you're working in a production environment.

Backups help you restore your data if something goes wrong. Databases on Pro, Team and Enterprise Plans are automatically backed up on schedule, but you can also take your own backup. See Database Backups for more information.

By default, Supabase enforces query statement timeouts to ensure fair resource allocation and prevent long-running queries from affecting the overall system. When importing large datasets, you may encounter timeouts. To address this:

Large datasets consume disk space. Ensure your Supabase project has sufficient disk capacity to accommodate the imported data. If you know how big your database is going to be, you can manually increase the size in your projects database settings.

Read more about disk management.

When importing large datasets, it's often beneficial to disable triggers temporarily. Triggers can significantly slow down the import process, especially if they involve complex logic or referential integrity checks. After the import, you can re-enable the triggers.

To disable triggers, use the following SQL commands:

Indexing is crucial for query performance, but building indices while importing a large dataset can be time-consuming. Consider building or rebuilding indices after the data import is complete. This approach can significantly speed up the import process and reduce the overall time required.

To build an index after the data import:

Read more about Managing Indexes in Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1$ apt-get install pgloader
```

Example 2 (unknown):
```unknown
1LOAD DATABASE2    FROM sourcedb://USER:PASSWORD@HOST/SOURCE_DB3    INTO postgres://postgres.xxxx:password@xxxx.pooler.supabase.com:6543/postgres4ALTER SCHEMA 'public' OWNER TO 'postgres';5set wal_buffers = '64MB', max_wal_senders = 0, statement_timeout = 0, work_mem to '2GB';
```

Example 3 (unknown):
```unknown
1pgloader config.load
```

Example 4 (unknown):
```unknown
1-- Disable triggers on a specific table2ALTER TABLE table_name DISABLE TRIGGER ALL;34-- To re-enable triggers5ALTER TABLE table_name ENABLE TRIGGER ALL;
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-update-database-password

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-inspect-db-long-running-queries

**Contents:**
- Supabase CLI
  - Additional links#
- Global flags
  - Flags
- supabase bootstrap
  - Usage
  - Flags
- supabase init
  - Usage
  - Flags

The Supabase CLI provides tools to develop your project locally and deploy to the Supabase Platform. The CLI is still under development, but it contains all the functionality for working with your Supabase projects and the Supabase Platform.

Supabase CLI supports global flags for every command.

create a support ticket for any CLI error

output debug logs to stderr

lookup domain names using the specified resolver

enable experimental features

use the specified docker network instead of a generated one

output format of status variables

use a specific profile for connecting to Supabase API

path to a Supabase project directory

answer yes to all prompts

Password to your remote Postgres database.

Initialize configurations for Supabase local development.

A supabase/config.toml file is created in your current working directory. This configuration is specific to each local project.

You may override the directory path by specifying the SUPABASE_WORKDIR environment variable or --workdir flag.

In addition to config.toml, the supabase directory may also contain other Supabase objects, such as migrations, functions, tests, etc.

Overwrite existing supabase/config.toml.

Use OrioleDB storage engine for Postgres.

Generate IntelliJ IDEA settings for Deno.

Generate VS Code settings for Deno.

Connect the Supabase CLI to your Supabase account by logging in with your personal access token.

Your access token is stored securely in native credentials storage. If native credentials storage is unavailable, it will be written to a plain text file at ~/.supabase/access-token.

If this behavior is not desired, such as in a CI environment, you may skip login by specifying the SUPABASE_ACCESS_TOKEN environment variable in other commands.

The Supabase CLI uses the stored token to access Management APIs for projects, functions, secrets, etc.

Name that will be used to store token in your settings

Do not open browser automatically

Use provided token instead of automatic login flow

Link your local development project to a hosted Supabase project.

PostgREST configurations are fetched from the Supabase platform and validated against your local configuration file.

Optionally, database settings can be validated if you provide a password. Your database password is saved in native credentials storage if available.

If you do not want to be prompted for the database password, such as in a CI environment, you may specify it explicitly via the SUPABASE_DB_PASSWORD environment variable.

Some commands like db dump, db push, and db pull require your project to be linked first.

Password to your remote Postgres database.

Project ref of the Supabase project.

Use direct connection instead of pooler.

Starts the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All service containers are started by default. You can exclude those not needed by passing in -x flag. To exclude multiple containers, either pass in a comma separated string, such as -x gotrue,imgproxy, or specify -x flag multiple times.

It is recommended to have at least 7GB of RAM to start all services.

Health checks are automatically added to verify the started containers. Use --ignore-health-check flag to ignore these errors.

Names of containers to not start. [gotrue,realtime,storage-api,imgproxy,kong,mailpit,postgrest,postgres-meta,studio,edge-runtime,logflare,vector,supavisor]

Ignore unhealthy services and exit 0

Stops the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All Docker resources are maintained across restarts. Use --no-backup flag to reset your local development data between restarts.

Use the --all flag to stop all local Supabase projects instances on the machine. Use with caution with --no-backup as it will delete all supabase local projects data.

Stop all local Supabase instances from all projects across the machine.

Deletes all data volumes after stopping.

Local project ID to stop.

Shows status of the Supabase local development stack.

Requires the local development stack to be started by running supabase start or supabase db start.

You can export the connection parameters for initializing supabase-js locally by specifying the -o env flag. Supported parameters include JWT_SECRET, ANON_KEY, and SERVICE_ROLE_KEY.

Override specific variable names.

Executes pgTAP tests against the local database.

Requires the local development stack to be started by running supabase start.

Runs pg_prove in a container with unit test files volume mounted from supabase/tests directory. The test file can be suffixed by either .sql or .pg extension.

Since each test is wrapped in its own transaction, it will be individually rolled back regardless of success or failure.

Tests the database specified by the connection string (must be percent-encoded).

Runs pgTAP tests on the linked project.

Runs pgTAP tests on the local database.

Template framework to generate.

Automatically generates type definitions based on your Postgres database schema.

This command connects to your database (local or remote) and generates typed definitions that match your database tables, views, and stored procedures. By default, it generates TypeScript definitions, but also supports Go and Swift.

Generated types give you type safety and autocompletion when working with your database in code, helping prevent runtime errors and improving developer experience.

The types respect relationships, constraints, and custom types defined in your database schema.

Securely generate a private JWT signing key for use in the CLI or to import in the dashboard.

Supported algorithms: ES256 - ECDSA with P-256 curve and SHA-256 (recommended) RS256 - RSA with SHA-256

Algorithm for signing key generation.

Append new key to existing keys file instead of overwriting.

Generate types from a database url.

Output language of the generated types.

Generate types from the linked project.

Generate types from the local dev database.

Generate types compatible with PostgREST v9 and below.

Generate types from a project ID.

Maximum timeout allowed for the database query.

Comma separated list of schema to include.

Access control for Swift generated types.

Pulls schema changes from a remote database. A new migration file will be created under supabase/migrations directory.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Optionally, a new row can be inserted into the migration history table to reflect the current state of the remote database.

If no entries exist in the migration history table, pg_dump will be used to capture all contents of the remote schemas you have created. Otherwise, this command will only diff schema changes against the remote database, similar to running db diff --linked.

Pulls from the database specified by the connection string (must be percent-encoded).

Pulls from the linked project.

Pulls from the local database.

Password to your remote Postgres database.

Comma separated list of schema to include.

Pushes all local migrations to a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

The first time this command is run, a migration history table will be created under supabase_migrations.schema_migrations. After successfully applying a migration, a new row will be inserted into the migration history table with timestamp as its unique id. Subsequent pushes will skip migrations that have already been applied.

If you need to mutate the migration history table, such as deleting existing entries or inserting new entries without actually running the migration, use the migration repair command.

Use the --dry-run flag to view the list of changes before applying.

Pushes to the database specified by the connection string (must be percent-encoded).

Print the migrations that would be applied, but don't actually apply them.

Include all migrations not found on remote history table.

Include custom roles from supabase/roles.sql.

Include seed data from your config.

Pushes to the linked project.

Pushes to the local database.

Password to your remote Postgres database.

Resets the local database to a clean state.

Requires the local development stack to be started by running supabase start.

Recreates the local Postgres container and applies all local migrations found in supabase/migrations directory. If test data is defined in supabase/seed.sql, it will be seeded after the migrations are run. Any other data or schema changes made during local development will be discarded.

When running db reset with --linked or --db-url flag, a SQL script is executed to identify and drop all user created entities in the remote database. Since Postgres roles are cluster level entities, any custom roles created through the dashboard or supabase/roles.sql will not be deleted by remote reset.

Resets the database specified by the connection string (must be percent-encoded).

Reset up to the last n migration versions.

Resets the linked project with local migrations.

Resets the local database with local migrations.

Skip running the seed script after reset.

Reset up to the specified version.

Dumps contents from a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Runs pg_dump in a container with additional flags to exclude Supabase managed schemas. The ignored schemas include auth, storage, and those created by extensions.

The default dump does not contain any data or custom roles. To dump those contents explicitly, specify either the --data-only and --role-only flag.

Dumps only data records.

Dumps from the database specified by the connection string (must be percent-encoded).

Prints the pg_dump script that would be executed.

List of schema.tables to exclude from data-only dump.

File path to save the dumped contents.

Keeps commented lines from pg_dump output.

Dumps from the linked project.

Dumps from the local database.

Password to your remote Postgres database.

Dumps only cluster roles.

Comma separated list of schema to include.

Use copy statements in place of inserts.

Diffs schema changes made to the local or remote database.

Requires the local development stack to be running when diffing against the local database. To diff against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs djrobstep/migra in a container to compare schema differences between the target database and a shadow database. The shadow database is created by applying migrations in local supabase/migrations directory in a separate container. Output is written to stdout by default. For convenience, you can also save the schema diff as a new migration file by passing in -f flag.

By default, all schemas in the target database are diffed. Use the --schema public,extensions flag to restrict diffing to a subset of schemas.

While the diff command is able to capture most schema changes, there are cases where it is known to fail. Currently, this could happen if you schema contains:

Diffs against the database specified by the connection string (must be percent-encoded).

Saves schema diff to a new migration file.

Diffs local migration files against the linked project.

Diffs local migration files against the local database.

Comma separated list of schema to include.

Use migra to generate schema diff.

Use pg-schema-diff to generate schema diff.

Use pgAdmin to generate schema diff.

Lints local database for schema errors.

Requires the local development stack to be running when linting against the local database. To lint against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs plpgsql_check extension in the local Postgres container to check for errors in all schemas. The default lint level is warning and can be raised to error via the --level flag.

To lint against specific schemas only, pass in the --schema flag.

The --fail-on flag can be used to control when the command should exit with a non-zero status code. The possible values are:

This flag is particularly useful in CI/CD pipelines where you want to fail the build based on certain lint conditions.

Lints the database specified by the connection string (must be percent-encoded).

Error level to exit with non-zero status.

Lints the linked project for schema errors.

Lints the local database for schema errors.

Comma separated list of schema to include.

Path to a logical backup file.

Creates a new migration file locally.

A supabase/migrations directory will be created if it does not already exists in your current workdir. All schema migration files must be created in this directory following the pattern <timestamp>_<name>.sql.

Outputs from other commands like db diff may be piped to migration new <name> via stdin.

Lists migration history in both local and remote databases.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Note that URL strings must be escaped according to RFC 3986.

Local migrations are stored in supabase/migrations directory while remote migrations are tracked in supabase_migrations.schema_migrations table. Only the timestamps are compared to identify any differences.

In case of discrepancies between the local and remote migration history, you can resolve them using the migration repair command.

Lists migrations of the database specified by the connection string (must be percent-encoded).

Lists migrations applied to the linked project.

Lists migrations applied to the local database.

Password to your remote Postgres database.

Fetches migrations from the database specified by the connection string (must be percent-encoded).

Fetches migration history from the linked project.

Fetches migration history from the local database.

Repairs the remote migration history table.

Requires your local project to be linked to a remote database by running supabase link.

If your local and remote migration history goes out of sync, you can repair the remote history by marking specific migrations as --status applied or --status reverted. Marking as reverted will delete an existing record from the migration history table while marking as applied will insert a new record.

For example, your migration history may look like the table below, with missing entries in either local or remote.

To reset your migration history to a clean state, first delete your local migration file.

Then mark the remote migration 20230103054303 as reverted.

Now you can run db pull again to dump the remote schema as a local migration file.

Repairs migrations of the database specified by the connection string (must be percent-encoded).

Repairs the migration history of the linked project.

Repairs the migration history of the local database.

Password to your remote Postgres database.

Version status to update.

Squashes local schema migrations to a single migration file.

The squashed migration is equivalent to a schema only dump of the local database after applying existing migration files. This is especially useful when you want to remove repeated modifications of the same schema from your migration history.

However, one limitation is that data manipulation statements, such as insert, update, or delete, are omitted from the squashed migration. You will have to add them back manually in a new migration file. This includes cron jobs, storage buckets, and any encrypted secrets in vault.

By default, the latest <timestamp>_<name>.sql file will be updated to contain the squashed migration. You can override the target version using the --version <timestamp> flag.

If your supabase/migrations directory is empty, running supabase squash will do nothing.

Squashes migrations of the database specified by the connection string (must be percent-encoded).

Squashes the migration history of the linked project.

Squashes the migration history of the local database.

Password to your remote Postgres database.

Squash up to the specified version.

Applies migrations to the database specified by the connection string (must be percent-encoded).

Include all migrations not found on remote history table.

Applies pending migrations to the linked project.

Applies pending migrations to the local database.

Seeds the linked project.

Seeds the local database.

This command displays an estimation of table "bloat" - Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will asynchronously clean the dead tuples. Sometimes the autovaccum is unable to work fast enough to reduce or prevent tables from becoming bloated. High bloat can slow down queries, cause excessive IOPS and waste space in your database.

Tables with a high bloat ratio should be investigated to see if there are vacuuming is not quick enough or there are other issues.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows you statements that are currently holding locks and blocking, as well as the statement that is being blocked. This can be used in conjunction with inspect db locks to determine which statements need to be terminated in order to resolve lock contention.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command is much like the supabase inspect db outliers command, but ordered by the number of times a statement has been called.

You can use this information to see which queries are called most often, which can potentially be good candidates for optimisation.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays queries that have taken out an exclusive lock on a relation. Exclusive locks typically prevent other operations on that relation from taking place, and can be a cause of "hung" queries that are waiting for a lock to be granted.

If you see a query that is hanging for a very long time or causing blocking issues you may consider killing the query by connecting to the database and running SELECT pg_cancel_backend(PID); to cancel the query. If the query still does not stop you can force a hard stop by running SELECT pg_terminate_backend(PID);

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays currently running queries, that have been running for longer than 5 minutes, descending by duration. Very long running queries can be a source of multiple issues, such as preventing DDL statements completing or vacuum being unable to update relfrozenxid.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays statements, obtained from pg_stat_statements, ordered by the amount of time to execute in aggregate. This includes the statement itself, the total execution time for that statement, the proportion of total execution time for all statements that statement has taken up, the number of times that statement has been called, and the amount of time that statement spent on synchronous I/O (reading/writing from the file system).

Typically, an efficient query will have an appropriate ratio of calls to total execution time, with as little time spent on I/O as possible. Queries that have a high total execution time but low call count should be investigated to improve their performance. Queries that have a high proportion of execution time being spent on synchronous I/O should also be investigated.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows information about logical replication slots that are setup on the database. It shows if the slot is active, the state of the WAL sender process ('startup', 'catchup', 'streaming', 'backup', 'stopping') the replication client address and the replication lag in GB.

This command is useful to check that the amount of replication lag is as low as possible, replication lag can occur due to network latency issues, slow disk I/O, long running transactions or lack of ability for the subscriber to consume WAL fast enough.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command analyzes table I/O patterns to show read/write activity ratios based on block-level operations. It combines data from PostgreSQL's pg_stat_user_tables (for tuple operations) and pg_statio_user_tables (for block I/O) to categorize each table's workload profile.

The command classifies tables into categories:

Note: This command only displays tables that have had both read and write activity. Tables with no I/O operations are not shown. The classification ratio threshold (default: 5:1) determines when a table is considered "heavy" in one direction versus balanced.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This shows you stats about the vacuum activities for each table. Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will aysnchronously clean the dead tuples.

The command lists when the last vacuum and last auto vacuum took place, the row count on the table as well as the count of dead rows and whether autovacuum is expected to run or not. If the number of dead rows is much higher than the row count, or if an autovacuum is expected but has not been performed for some time, this can indicate that autovacuum is not able to keep up and that your vacuum settings need to be tweaked or that you require more compute or disk IOPS to allow autovaccum to complete.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Path to save CSV files in

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Create an organization for the logged-in user.

List all organizations the logged-in user belongs.

Provides tools for creating and managing your Supabase projects.

This command group allows you to list all projects in your organizations, create new projects, delete existing projects, and retrieve API keys. These operations help you manage your Supabase infrastructure programmatically without using the dashboard.

Project management via CLI is especially useful for automation scripts and when you need to provision environments in a repeatable way.

Database password of the project.

Organization ID to create the project in.

Select a region close to you for the best performance.

Select a desired instance size for your project.

List all Supabase projects the logged-in user can access.

Project ref of the Supabase project.

Updates the configurations of a linked Supabase project with the local supabase/config.toml file.

This command allows you to manage project configuration as code by defining settings locally and then pushing them to your remote project.

Project ref of the Supabase project.

Create a preview branch for the linked project.

URL to notify when branch is active healthy.

Whether to create a persistent branch.

Select a region to deploy the branch database.

Select a desired instance size for the branch database.

Whether to clone production data to the branch database.

Project ref of the Supabase project.

List all preview branches of the linked project.

Project ref of the Supabase project.

Retrieve details of the specified preview branch.

Project ref of the Supabase project.

Update a preview branch by its name or ID.

Change the associated git branch.

Rename the preview branch.

URL to notify when branch is active healthy.

Switch between ephemeral and persistent branch.

Override the current branch status.

Project ref of the Supabase project.

Project ref of the Supabase project.

Project ref of the Supabase project.

Delete a preview branch by its name or ID.

Project ref of the Supabase project.

Manage Supabase Edge Functions.

Supabase Edge Functions are server-less functions that run close to your users.

Edge Functions allow you to execute custom server-side code without deploying or scaling a traditional server. They're ideal for handling webhooks, custom API endpoints, data validation, and serving personalized content.

Edge Functions are written in TypeScript and run on Deno compatible edge runtime, which is a secure runtime with no package management needed, fast cold starts, and built-in security.

Creates a new Edge Function with boilerplate code in the supabase/functions directory.

This command generates a starter TypeScript file with the necessary Deno imports and a basic function structure. The function is created as a new directory with the name you specify, containing an index.ts file with the function code.

After creating the function, you can edit it locally and then use supabase functions serve to test it before deploying with supabase functions deploy.

List all Functions in the linked Supabase project.

Project ref of the Supabase project.

Download the source code for a Function from the linked Supabase project.

Project ref of the Supabase project.

Unbundle functions server-side without using Docker.

Serve all Functions locally.

supabase functions serve command includes additional flags to assist developers in debugging Edge Functions via the v8 inspector protocol, allowing for debugging via Chrome DevTools, VS Code, and IntelliJ IDEA for example. Refer to the docs guide for setup instructions.

--inspect-mode [ run | brk | wait ]

Additionally, the following properties can be customized via supabase/config.toml under edge_runtime section.

Path to an env file to be populated to the Function environment.

Path to import map file.

Alias of --inspect-mode brk.

Allow inspecting the main worker.

Activate inspector capability for debugging.

Disable JWT verification for the Function.

Deploy a Function to the linked Supabase project.

Path to import map file.

Maximum number of parallel jobs.

Disable JWT verification for the Function.

Project ref of the Supabase project.

Delete Functions that exist in Supabase project but not locally.

Bundle functions server-side without using Docker.

Delete a Function from the linked Supabase project. This does NOT remove the Function locally.

Project ref of the Supabase project.

Provides tools for managing environment variables and secrets for your Supabase project.

This command group allows you to set, unset, and list secrets that are securely stored and made available to Edge Functions as environment variables.

Secrets management through the CLI is useful for:

Secrets can be set individually or loaded from .env files for convenience.

Set a secret(s) to the linked Supabase project.

Read secrets from a .env file.

Project ref of the Supabase project.

List all secrets in the linked project.

Project ref of the Supabase project.

Unset a secret(s) from the linked Supabase project.

Project ref of the Supabase project.

Recursively list a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Custom Cache-Control header for HTTP upload.

Custom Content-Type header for HTTP upload.

Maximum number of parallel jobs.

Recursively copy a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively move a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively remove a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Add and configure a new connection to a SSO identity provider to your Supabase project.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Comma separated list of email domains to associate with the added identity provider.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Type of identity provider (according to supported protocol).

Project ref of the Supabase project.

List all connections to a SSO identity provider to your Supabase project.

Project ref of the Supabase project.

Provides the information about an established connection to an identity provider. You can use --metadata to obtain the raw SAML 2.0 Metadata XML document stored in your project's configuration.

Show SAML 2.0 XML Metadata only

Project ref of the Supabase project.

Returns all of the important SSO information necessary for your project to be registered with a SAML 2.0 compatible identity provider.

Project ref of the Supabase project.

Update the configuration settings of a already added SSO identity provider.

Add this comma separated list of email domains to the identity provider.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Replace domains with this comma separated list of email domains.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Remove this comma separated list of email domains from the identity provider.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Project ref of the Supabase project.

Remove a connection to an already added SSO identity provider. Removing the provider will prevent existing users from logging in. Please treat this command with care.

Project ref of the Supabase project.

Manage custom domain names for Supabase projects.

Use of custom domains and vanity subdomains is mutually exclusive.

Activates the custom hostname configuration for a project.

This reconfigures your Supabase project to respond to requests on your custom hostname.

After the custom hostname is activated, your project's third-party auth providers will no longer function on the Supabase-provisioned subdomain. Please refer to Prepare to activate your domain section in our documentation to learn more about the steps you need to follow.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Create a custom hostname for your Supabase project.

Expects your custom hostname to have a CNAME record to your Supabase project's subdomain.

The custom hostname to use for your Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Retrieve the custom hostname config for your project, as stored in the Supabase platform.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Manage vanity subdomains for Supabase projects.

Usage of vanity subdomains and custom domains is mutually exclusive.

Activate a vanity subdomain for your Supabase project.

This reconfigures your Supabase project to respond to requests on your vanity subdomain. After the vanity subdomain is activated, your project's auth services will no longer function on the {project-ref}.{supabase-domain} hostname.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

Deletes the vanity subdomain for a project, and reverts to using the project ref for routing.

enable experimental features

Project ref of the Supabase project.

Network bans are IPs that get temporarily blocked if their traffic pattern looks abusive (e.g. multiple failed auth attempts).

The subcommands help you view the current bans, and unblock IPs if desired.

enable experimental features

Project ref of the Supabase project.

IP to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Append to existing restrictions instead of replacing them.

Bypass some of the CIDR validation checks.

CIDR to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Whether the DB should disable SSL enforcement for all external connections.

Whether the DB should enable SSL enforcement for all external connections.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Overriding the default Postgres config could result in unstable database behavior. Custom configuration also overrides the optimizations generated based on the compute add-ons in use.

Config overrides specified as a 'key=value' pair

Do not restart the database after updating config.

If true, replaces all existing overrides with the ones provided. If false (default), merges existing overrides with the ones provided.

enable experimental features

Project ref of the Supabase project.

Delete specific config overrides, reverting them to their default values.

Config keys to delete (comma-separated)

Do not restart the database after deleting config.

enable experimental features

Project ref of the Supabase project.

List all SQL snippets of the linked project.

Project ref of the Supabase project.

Download contents of the specified SQL snippet.

Project ref of the Supabase project.

Generate the autocompletion script for supabase for the specified shell. See each sub-command's help for details on how to use the generated script.

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need to enable it. You can execute the following once:

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for powershell.

To load completions in your current shell session:

To load completions for every new session, add the output of the above command to your powershell profile.

disable completion descriptions

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package. If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

**Examples:**

Example 1 (unknown):
```unknown
1supabase bootstrap [template] [flags]
```

Example 2 (unknown):
```unknown
1supabase init [flags]
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1Finished supabase init.
```

---

## Learn how to integrate Supabase with LlamaIndex, a data framework for your LLM applications. | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/integrations/llamaindex

**Contents:**
- Learn how to integrate Supabase with LlamaIndex, a data framework for your LLM applications.
- Learn how to integrate Supabase with LlamaIndex, a data framework for your LLM applications.
- Project setup#
- Launching a notebook#
- Fill in your OpenAI credentials#
- Connecting to your database#
- Stepping through the notebook#
- Resources#

Learn how to integrate Supabase with LlamaIndex, a data framework for your LLM applications.

Learn how to integrate Supabase with LlamaIndex, a data framework for your LLM applications.

This guide will walk you through a basic example using the LlamaIndex SupabaseVectorStore.

Let's create a new Postgres database. This is as simple as starting a new Project in Supabase:

Your database will be available in less than a minute.

Finding your credentials:

You can find your project credentials on the dashboard:

Launch our LlamaIndex notebook in Colab:

At the top of the notebook, you'll see a button Copy to Drive. Click this button to copy the notebook to your Google Drive.

Inside the Notebook, add your OPENAI_API_KEY key. Find the cell which contains this code:

Inside the Notebook, find the cell which specifies the DB_CONNECTION. It will contain some code like this:

Replace the DB_CONNECTION with your own connection string. You can find the connection string on your project dashboard by clicking Connect.

SQLAlchemy requires the connection string to start with postgresql:// (instead of postgres://). Don't forget to rename this after copying the string from the dashboard.

You must use the "connection pooling" string (domain ending in *.pooler.supabase.com) with Google Colab since Colab does not support IPv6.

Now all that's left is to step through the notebook. You can do this by clicking the "execute" button (ctrl+enter) at the top left of each code cell. The notebook guides you through the process of creating a collection, adding data to it, and querying it.

You can view the inserted items in the Table Editor, by selecting the vecs schema from the schema dropdown.

**Examples:**

Example 1 (unknown):
```unknown
1import os2os.environ['OPENAI_API_KEY'] = "[your_openai_api_key]"
```

Example 2 (unknown):
```unknown
1DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"23# create vector store client4vx = vecs.create_client(DB_CONNECTION)
```

---

## pg_repack: Physical storage optimization and maintenance | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_repack

**Contents:**
- pg_repack: Physical storage optimization and maintenance
- Requirements#
- Usage#
  - Enable the extension#
  - Install the CLI#
  - Syntax#
- Example#
- Limitations#
- Resources#

pg_repack: Physical storage optimization and maintenance

pg_repack is a Postgres extension to remove bloat from tables and indexes, and optionally restore the physical order of clustered indexes. Unlike CLUSTER and VACUUM FULL, pg_repack runs "online" and does not hold a exclusive locks on the processed tables that could prevent ongoing database operations. pg_repack's efficiency is comparable to using CLUSTER directly.

pg_repack provides the following methods to optimize physical storage:

pg_repack has 2 components, the database extension and a client-side CLI to control it.

pg_repack requires the Postgres superuser role by default. That role is not available to users on the Supabase platform. To avoid that requirement, use the -k or --no-superuser-check flags on every pg_repack CLI command.

The first version of pg_repack with full support for non-superuser repacking is 1.5.2. You can check the version installed on your Supabase instance using

If pg_repack is not present, or the version is < 1.5.2, upgrade to the latest version of Supabase to gain access.

Get started with pg_repack by enabling the extension in the Supabase Dashboard.

Select an option from the pg_repack docs to install the client CLI.

All pg_repack commands should include the -k flag to skip the client-side superuser check.

Perform an online VACUUM FULL on the tables public.foo and public.bar in the database postgres:

See the official pg_repack documentation for the full list of options.

**Examples:**

Example 1 (unknown):
```unknown
1select default_version2from pg_available_extensions3where name = 'pg_repack';
```

Example 2 (unknown):
```unknown
1pg_repack -k [OPTION]... [DBNAME]
```

Example 3 (unknown):
```unknown
1pg_repack -k -h db.<PROJECT_REF>.supabase.co -p 5432 -U postgres -d postgres --no-order --table public.foo --table public.bar
```

---

## index_advisor: query optimization | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/index_advisor

**Contents:**
- index_advisor: query optimization
- Installation#
- API#
- Usage#
- Limitations#
- Resources#

index_advisor: query optimization

Index advisor is a Postgres extension for recommending indexes to improve query performance.

index_advisor is accessible directly through Supabase Studio by navigating to the Query Performance Report and selecting a query and then the "indexes" tab.

Alternatively, you can use index_advisor directly via SQL.

To get started, enable index_advisor by running

Index advisor exposes a single function index_advisor(query text) that accepts a query and searches for a set of SQL DDL create index statements that improve the query's execution time.

The function's signature is:

As a minimal example, the index_advisor function can be given a single table query with a filter on an unindexed column.

and will return a row recommending an index on the unindexed column.

More complex queries may generate additional suggested indexes:

**Examples:**

Example 1 (unknown):
```unknown
1select2    *3from4  index_advisor('select book.id from book where title = $1');56 startup_cost_before | startup_cost_after | total_cost_before | total_cost_after |                  index_statements                   | errors7---------------------+--------------------+-------------------+------------------+-----------------------------------------------------+--------8 0.00                | 1.17               | 25.88             | 6.40             | {"CREATE INDEX ON public.book USING btree (title)"},| {}9(1 row)
```

Example 2 (unknown):
```unknown
1create extension index_advisor;
```

Example 3 (unknown):
```unknown
1index_advisor(query text)2returns3    table  (4        startup_cost_before jsonb,5        startup_cost_after jsonb,6        total_cost_before jsonb,7        total_cost_after jsonb,8        index_statements text[],9        errors text[]10    )
```

Example 4 (unknown):
```unknown
1create extension if not exists index_advisor cascade;23create table book(4  id int primary key,5  title text not null6);78select9  *10from11  index_advisor('select book.id from book where title = $1');1213 startup_cost_before | startup_cost_after | total_cost_before | total_cost_after |                  index_statements                   | errors14---------------------+--------------------+-------------------+------------------+-----------------------------------------------------+--------15 0.00                | 1.17               | 25.88             | 6.40             | {"CREATE INDEX ON public.book USING btree (title)"},| {}16(1 row)
```

---

## pgjwt: JSON Web Tokens | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgjwt

**Contents:**
- pgjwt: JSON Web Tokens
- Enable the extension#
- API#
- Usage#
- Resources#

pgjwt: JSON Web Tokens

The pgjwt extension is deprecated in projects using Postgres 17. It continues to be supported in projects using Postgres 15, but will need to dropped before those projects are upgraded to Postgres 17. See the Upgrading to Postgres 17 notes for more information.

The pgjwt (Postgres JSON Web Token) extension allows you to create and parse JSON Web Tokens (JWTs) within a Postgres database. JWTs are commonly used for authentication and authorization in web applications and services.

Once the extension is installed, you can use its functions to create and parse JWTs. Here's an example of how you can use the sign function to create a JWT:

The pgjwt_encode function returns a string that represents the JWT, which can then be safely transmitted between parties.

To parse a JWT and extract its claims, you can use the verify function. Here's an example:

Which returns the decoded contents and some associated metadata.

**Examples:**

Example 1 (unknown):
```unknown
1select2  extensions.sign(3    payload   := '{"sub":"1234567890","name":"John Doe","iat":1516239022}',4    secret    := 'secret',5    algorithm := 'HS256'6  );
```

Example 2 (unknown):
```unknown
1sign2---------------------------------3 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX4 VCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiw5 ibmFtZSI6IkpvaG4gRG9lIiwiaWF0Ijo6 xNTE2MjM5MDIyfQ.XbPfbIHMI6arZ3Y97 22BhjWgQzWXcXNrz0ogtVhfEd2o8(1 row)
```

Example 3 (unknown):
```unknown
1select2  extensions.verify(3    token := 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiRm9vIn0.Q8hKjuadCEhnCPuqIj9bfLhTh_9QSxshTRsA5Aq4IuM',4    secret    := 'secret',5    algorithm := 'HS256'6  );
```

Example 4 (unknown):
```unknown
1header            |    payload     | valid2-----------------------------+----------------+-------3 {"alg":"HS256","typ":"JWT"} | {"name":"Foo"} | t4(1 row)
```

---

## Replicate to another Postgres database using Logical Replication | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/setup-replication-external

**Contents:**
- Replicate to another Postgres database using Logical Replication

Replicate to another Postgres database using Logical Replication

For this example, you will need:

You will be running commands on both of these databases to publish changes from the Supabase database to the external database.

This needs a direct connection (not a Connection Pooler) to your database and you can find the connection info in the Connect panel in the Direct connection section.

You will also need to ensure that IPv6 is supported by your replication destination (or you can enable the IPv4 add-on)

If you would prefer not to use the postgres user, then you can run CREATE ROLE <user> WITH REPLICATION; using the postgres user.

For projects running Postgres 17+, it is possible to subscribe to a Read Replica by using your Read Replica's connection string.

create_slot is set to false because slot_name is provided and the slot was already created in Step 2. To copy data from before the slot was created, set copy_data to true.

You can add more tables to the initial publication, but you're going to need to do a REFRESH on the subscribing database. See https://www.postgresql.org/docs/current/sql-alterpublication.html

**Examples:**

Example 1 (unknown):
```unknown
1CREATE PUBLICATION example_pub;
```

Example 2 (unknown):
```unknown
1select pg_create_logical_replication_slot('example_slot', 'pgoutput');
```

Example 3 (unknown):
```unknown
1CREATE SUBSCRIPTION example_sub2CONNECTION 'host=db.oaguxblfdassqxvvwtfe.supabase.co user=postgres password=YOUR_PASS dbname=postgres'3PUBLICATION example_pub4WITH (copy_data = true, create_slot=false, slot_name=example_slot);
```

Example 4 (unknown):
```unknown
1ALTER PUBLICATION example_pub ADD TABLE example_table;
```

---

## SQL to REST API Translator | Supabase Docs

**URL:** https://supabase.com/docs/guides/api/sql-to-rest

**Contents:**
- SQL to REST API Translator
- Translate SQL queries to HTTP requests and Supabase client code

SQL to REST API Translator

Translate SQL queries to HTTP requests and Supabase client code

Sometimes it's challenging to translate SQL queries to the equivalent PostgREST request or Supabase client code. Use this tool to help with this translation.

PostgREST supports a subset of SQL, so not all SQL queries will translate.

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-rollback-migrations

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Database Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/functions

**Contents:**
- Database Functions
- Quick demo#
- Getting started#
- Simple functions#
- Returning data sets#
    - Planets
    - People
- Passing parameters#
- Suggestions#
  - Database Functions vs Edge Functions#

Postgres has built-in support for SQL functions. These functions live inside your database, and they can be used with the API.

Supabase provides several options for creating database functions. You can use the Dashboard or create them directly using SQL. We provide a SQL editor within the Dashboard, or you can connect to your database and run the SQL queries yourself.

Let's create a basic Database Function which returns a string "hello world".

At it's most basic a function has the following parts:

When naming your functions, make the name of the function unique as overloaded functions are not supported.

After the Function is created, we have several ways of "executing" the function - either directly inside the database using SQL, or with one of the client libraries.

Database Functions can also return data sets from Tables or Views.

For example, if we had a database with some Star Wars data inside:

We could create a function which returns all the planets:

Because this function returns a table set, we can also apply filters and selectors. For example, if we only wanted the first planet:

Let's create a Function to insert a new planet into the planets table and return the new ID. Note that this time we're using the plpgsql language.

Once again, you can execute this function either inside your database using a select query, or with the client libraries:

For data-intensive operations, use Database Functions, which are executed within your database and can be called remotely using the REST and GraphQL API.

For use-cases which require low-latency, use Edge Functions, which are globally-distributed and can be written in Typescript.

Postgres allows you to specify whether you want the function to be executed as the user calling the function (invoker), or as the creator of the function (definer). For example:

It is best practice to use security invoker (which is also the default). If you ever use security definer, you must set the search_path. If you use an empty search path (search_path = ''), you must explicitly state the schema for every relation in the function body (e.g. from public.table). This limits the potential damage if you allow access to schemas which the user executing the function should not have.

By default, database functions can be executed by any role. There are two main ways to restrict this:

On a case-by-case basis. Specifically revoke permissions for functions you want to protect. Execution needs to be revoked for both public and the role you're restricting:

Restrict function execution by default. Specifically grant access when you want a function to be executable by a specific role.

To restrict all existing functions, revoke execution permissions from both public and the role you want to restrict:

To restrict all new functions, change the default privileges for both public and the role you want to restrict:

You can then regrant permissions for a specific function to a specific role:

You can add logs to help you debug functions. This is especially recommended for complex functions.

Good targets to log include:

To create custom logs in the Dashboard's Postgres Logs, you can use the raise keyword. By default, there are 3 observed severity levels:

You can create custom errors with the raise exception keywords.

A common pattern is to throw an error when a variable doesn't meet a condition:

Value checking is common, so Postgres provides a shorthand: the assert keyword. It uses the following format:

Error messages can also be captured and modified with the exception keyword:

For more complex functions or complicated debugging, try logging:

**Examples:**

Example 1 (unknown):
```unknown
1create or replace function hello_world() -- 12returns text -- 23language sql -- 34as $$  -- 45  select 'hello world';  -- 56$$; --6
```

Example 2 (unknown):
```unknown
1select hello_world();
```

Example 3 (unknown):
```unknown
1| id  | name     |2| --- | -------- |3| 1   | Tatooine |4| 2   | Alderaan |5| 3   | Kashyyyk |
```

Example 4 (unknown):
```unknown
1| id  | name             | planet_id |2| --- | ---------------- | --------- |3| 1   | Anakin Skywalker | 1         |4| 2   | Luke Skywalker   | 1         |5| 3   | Princess Leia    | 2         |6| 4   | Chewbacca        | 3         |
```

---

## plpgsql_check: PL/pgSQL Linter | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/plpgsql_check

**Contents:**
- plpgsql_check: PL/pgSQL Linter
- Enable the extension#
- API#
- Usage#
- Resources#

plpgsql_check: PL/pgSQL Linter

plpgsql_check is a Postgres extension that lints plpgsql for syntax, semantic and other related issues. The tool helps developers to identify and correct errors before executing the code. plpgsql_check is most useful for developers who are working with large or complex SQL codebases, as it can help identify and resolve issues early in the development cycle.

plpgsql_check_function is highly customizable. For a complete list of available arguments see the docs

To demonstrate plpgsql_check we can create a function with a known error. In this case we create a function some_func, that references a non-existent column place.created_at.

Note that executing the function would not catch the invalid reference error because the loop does not execute if no rows are present in the table.

Now we can use plpgsql_check's plpgsql_check_function function to identify the known error.

**Examples:**

Example 1 (unknown):
```unknown
1create table place(2  x float,3  y float4);56create or replace function public.some_func()7  returns void8  language plpgsql9as $$10declare11  rec record;12begin13  for rec in select * from place14  loop15    -- Bug: There is no column `created_at` on table `place`16    raise notice '%', rec.created_at;17  end loop;18end;19$$;
```

Example 2 (unknown):
```unknown
1select public.some_func();2  some_func3 ───────────45 (1 row)
```

Example 3 (unknown):
```unknown
1select plpgsql_check_function('public.some_func()');23                   plpgsql_check_function4------------------------------------------------------------5 error:42703:8:RAISE:record "rec" has no field "created_at"6 Context: SQL expression "rec.created_at"
```

---

## Connecting with Beekeeper Studio | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/beekeeper-studio

**Contents:**
- Connecting with Beekeeper Studio
  - Create a new connection
  - Get your connection credentials
  - Download your SSL Certificate
  - Test and connect

Connecting with Beekeeper Studio

Beekeeper Studio Community is a free GUI tool for interacting with databases.

In Beekeeper, create a new Postgres connection.

Get your connection credentials from the Connect panel. You will need:

Add your credentials to Beekeeper's connection form

Download your SSL certificate from the Dashboard's Database Settings

Add your SSL to the connection form

Test your connection and then connect

---

## Clerk | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/clerk

**Contents:**
- Clerk
- Available Versions#
- Preparation#
  - Enable Wrappers#
  - Enable the Clerk Wrapper#
  - Store your credentials (optional)#
  - Connecting to Clerk#
  - Create a schema#
- Options#
- Entities#

You can enable the Clerk wrapper right from the Supabase dashboard.

Clerk is a complete suite of embeddable UIs, flexible APIs, and admin dashboards to authenticate and manage users.

The Clerk Wrapper is a WebAssembly(Wasm) foreign data wrapper which allows you to read data from Clerk for use within your Postgres database.

Before you can query Clerk, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the Wasm foreign data wrapper:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to access Clerk and any additional options. We can do this using the create server command:

Note the fdw_package_* options are required, which specify the Wasm package metadata. You can get the available package version list from above.

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

Supported objects are listed below:

We can use SQL import foreign schema to import foreign table definitions from Clerk.

For example, using below SQL can automatically create foreign tables in the clerk schema.

This is a list of all identifiers allowed to sign up to an instance.

This is a list of all identifiers which are not allowed to access an instance.

This is a list of all domains for an instance.

This is a list of all non-revoked invitations for your application.

This is a list of all JWT templates.

This is a list of OAuth applications for an instance.

This is a list of organizations for an instance.

This is a list of organization invitations for an instance.

This is a list of organization user memberships for an instance.

This is a list of all whitelisted redirect urls for the instance.

This is a list of SAML Connections for an instance.

This is a list of all users.

This FDW doesn't support query pushdown.

The Clerk API uses JSON formatted data, please refer to Clerk Backend API docs for more details.

This section describes important limitations and considerations when using this FDW:

Below are some examples on how to use Clerk foreign tables.

This example will create a "foreign table" inside your Postgres database and query its data.

attrs is a special column which stores all the object attributes in JSON format, you can extract any attributes needed from it. See more examples below.

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper wasm_wrapper2  handler wasm_fdw_handler3  validator wasm_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Clerk API key in Vault and retrieve the created `key_id`2select vault.create_secret(3  '<Clerk API key>', -- Clerk API key4  'clerk',5  'Clerk API key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server clerk_server2  foreign data wrapper wasm_wrapper3  options (4    fdw_package_url 'https://github.com/supabase/wrappers/releases/download/wasm_clerk_fdw_v0.1.0/clerk_fdw.wasm',5    fdw_package_name 'supabase:clerk-fdw',6    fdw_package_version '0.1.0',7    fdw_package_checksum '613be26b59fa4c074e0b93f0db617fcd7b468d4d02edece0b1f85fdb683ebdc4',8    api_url 'https://api.clerk.com/v1',  -- optional9    api_key_id '<key_ID>' -- The Key ID from above.10  );
```

---

## Hardening the Data API | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/hardening-data-api

**Contents:**
- Hardening the Data API
- Shared responsibility#
- Private schemas#
- Managing the public schema#
- Disabling the Data API#
- Exposing a custom schema instead of public#
  - Step 1: Remove public from exposed schemas#
  - Step 2: Create an api schema and expose it#

Hardening the Data API

Your database's auto-generated Data API exposes the public schema by default. You can change this to any schema in your database, or even disable the Data API completely.

Any tables that are accessible through the Data API must have Row Level Security enabled. Row Level Security (RLS) is enabled by default when you create tables from the Supabase Dashboard. If you create a table using the SQL editor or your own SQL client or migration runner, youmust enable RLS yourself.

Your application's security is your responsibility as a developer. This includes RLS, falling under the Shared Responsibility model. To help you:

We highly recommend creating a private schema for storing tables that you do not want to expose via the Data API. These tables can be accessed via Supabase Edge Functions or any other serverside tool. In this model, you should implement your security model in your serverside code. Although it's not required, we still recommend enabling RLS for private tables and then connecting to your database using a Postgres role with bypassrls privileges.

If your public schema is used by other tools as a default space, you might want to lock down this schema. This helps prevent accidental exposure of data that's automatically added to public.

There are two levels of security hardening for the Data API:

You can disable the Data API entirely if you never intend to use the Supabase client libraries or the REST and GraphQL data endpoints. For example, if you only access your database via a direct connection on the server, disabling the Data API gives you the greatest layer of protection.

If you want to use the Data API but with increased security, you can expose a custom schema instead of public. By not using public, which is often used as a default space and has laxer default permissions, you get more conscious control over your exposed data.

Any data, views, or functions that should be exposed need to be deliberately put within your custom schema (which we will call api), rather than ending up there by default.

Connect to your database. You can use psql, the Supabase SQL Editor, or the Postgres client of your choice.

Create a new schema named api:

Grant the anon and authenticated roles usage on this schema.

Go to API Settings in the Supabase Dashboard.

Under Data API Settings, add api to Exposed schemas. Make sure it is the first schema in the list, so that it will be searched first by default.

Under these new settings, anon and authenticated can execute functions defined in the api schema, but they have no automatic permissions on any tables. On a table-by-table basis, you can grant them permissions. For example:

**Examples:**

Example 1 (unknown):
```unknown
1create schema if not exists api;
```

Example 2 (unknown):
```unknown
1grant usage on schema api to anon, authenticated;
```

Example 3 (unknown):
```unknown
1grant select on table api.<your_table> to anon;2grant select, insert, update, delete on table api.<your_table> to authenticated;
```

---

## Migrate from Amazon RDS to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/amazon-rds

**Contents:**
- Migrate from Amazon RDS to Supabase
- Migrate your Amazon RDS MySQL or MS SQL database to Supabase.
- Retrieve your Amazon RDS database credentials #
- Retrieve your Supabase host #
- Migrate the database#
- Enterprise#

Migrate from Amazon RDS to Supabase

Migrate your Amazon RDS MySQL or MS SQL database to Supabase.

This guide aims to exhibit the process of transferring your Amazon RDS database from any of these engines Postgres, MySQL or MS SQL to Supabase's Postgres database. Although Amazon RDS is a favored managed database service provided by AWS, it may not suffice for all use cases. Supabase, on the other hand, provides an excellent free and open source option that encompasses all the necessary backend features to develop a product: a Postgres database, authentication, instant APIs, edge functions, real-time subscriptions, and storage.

Supabase's core is Postgres, enabling the use of row-level security and providing access to over 40 Postgres extensions. By migrating from Amazon RDS to Supabase, you can leverage Postgres to its fullest potential and acquire all the features you need to complete your project.

The fastest way to migrate your database is with the Supabase migration tool on Google Colab.

Alternatively, you can use pgloader, a flexible and powerful data migration tool that supports a wide range of source database engines, including MySQL and MS SQL, and migrates the data to a Postgres database. For databases using the Postgres engine, we recommend using the pg_dump and psql command line tools, which are included in a full Postgres installation.

If you're planning to migrate a database larger than 6 GB, we recommend upgrading to at least a Large compute add-on. This will ensure you have the necessary resources to handle the migration efficiently.

We strongly advise you to pre-provision the disk space you will need for your migration. On paid projects, you can do this by navigating to the Compute and Disk Settings page. For more information on disk scaling and disk limits, check out our disk settings documentation.

Contact us if you need more help migrating your project.

---

## pg_graphql: GraphQL for PostgreSQL | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_graphql

**Contents:**
- pg_graphql: GraphQL for PostgreSQL
- Enable the extension#
- Usage#
- API#
- Resources#

pg_graphql: GraphQL for PostgreSQL

pg_graphql is Postgres extension for interacting with the database using GraphQL instead of SQL.

The extension reflects a GraphQL schema from the existing SQL schema and exposes it through a SQL function, graphql.resolve(...). This enables any programming language that can connect to Postgres to query the database via GraphQL with no additional servers, processes, or libraries.

The pg_graphql resolve method is designed to interop with PostgREST, the tool that underpins the Supabase API, such that the graphql.resolve function can be called via RPC to safely and performantly expose the GraphQL API over HTTP/S.

For more information about how the SQL schema is reflected into a GraphQL schema, see the pg_graphql API docs.

The reflected GraphQL schema can be queried immediately as

Note that pg_graphql fully supports schema introspection so you can connect any GraphQL IDE or schema inspection tool to see the full set of fields and arguments available in the API.

**Examples:**

Example 1 (unknown):
```unknown
1create table "Blog"(2  id serial primary key,3  name text not null,4  description text5);67insert into "Blog"(name)8values ('My Blog');
```

Example 2 (unknown):
```unknown
1select2  graphql.resolve($$3    {4      blogCollection(first: 1) {5        edges {6          node {7            id,8            name9          }10        }11      }12    }13  $$);
```

Example 3 (unknown):
```unknown
1{2  "data": {3    "blogCollection": {4      "edges": [5        {6          "node": {7            "id": 18            "name": "My Blog"9          }10        }11      ]12    }13  }14}
```

---

## timescaledb: Time-Series data | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/timescaledb

**Contents:**
- timescaledb: Time-Series data
- Enable the extension#
- Usage#
- Resources#

timescaledb: Time-Series data

The timescaledb extension is deprecated in projects using Postgres 17. It continues to be supported in projects using Postgres 15, but will need to dropped before those projects are upgraded to Postgres 17. See the Upgrading to Postgres 17 notes for more information.

timescaledb is a Postgres extension designed for improved handling of time-series data. It provides a scalable, high-performance solution for storing and querying time-series data on top of a standard Postgres database.

timescaledb uses a time-series-aware storage model and indexing techniques to improve performance of Postgres in working with time-series data. The extension divides data into chunks based on time intervals, allowing it to scale efficiently, especially for large data sets. The data is then compressed, optimized for write-heavy workloads, and partitioned for parallel processing. timescaledb also includes a set of functions, operators, and indexes that work with time-series data to reduce query times, and make data easier to work with.

Supabase projects come with TimescaleDB Apache 2 Edition. Functionality only available under the Community Edition is not available.

Even though the SQL code is create extension, this is the equivalent of "enabling the extension". To disable an extension you can call drop extension.

It's good practice to create the extension within a separate schema (like extensions) to keep your public schema clean.

To demonstrate how timescaledb works, let's consider a simple example where we have a table that stores temperature data from different sensors. We will create a table named "temperatures" and store data for two sensors.

First we create a hypertable, which is a virtual table that is partitioned into chunks based on time intervals. The hypertable acts as a proxy for the actual table and makes it easy to query and manage time-series data.

Next, we can populate some values

And finally we can query the table using timescaledb's time_bucket function to divide the time-series into intervals of the specified size (in this case, 1 hour) averaging the temperature reading within each group.

**Examples:**

Example 1 (unknown):
```unknown
1create table temperatures (2  time timestamptz not null,3  sensor_id int not null,4  temperature double precision not null5);67select create_hypertable('temperatures', 'time');
```

Example 2 (unknown):
```unknown
1insert into temperatures (time, sensor_id, temperature)2values3    ('2023-02-14 09:00:00', 1, 23.5),4    ('2023-02-14 09:00:00', 2, 21.2),5    ('2023-02-14 09:05:00', 1, 24.5),6    ('2023-02-14 09:05:00', 2, 22.3),7    ('2023-02-14 09:10:00', 1, 25.1),8    ('2023-02-14 09:10:00', 2, 23.9),9    ('2023-02-14 09:15:00', 1, 24.9),10    ('2023-02-14 09:15:00', 2, 22.7),11    ('2023-02-14 09:20:00', 1, 24.7),12    ('2023-02-14 09:20:00', 2, 23.5);
```

Example 3 (unknown):
```unknown
1select2    time_bucket('1 hour', time) AS hour,3    avg(temperature) AS average_temperature4from5    temperatures6where7    sensor_id = 18    and time > NOW() - interval '1 hour'9group by10    hour;
```

---

## Manual Replication Setup | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/replication/manual-replication-setup

**Contents:**
- Manual Replication Setup
- Set up replication with Airbyte, Estuary, Fivetran, and other tools.
  - Prerequisites#

Manual Replication Setup

Set up replication with Airbyte, Estuary, Fivetran, and other tools.

This guide covers setting up manual logical replication using external tools. If you prefer a simpler, managed solution, read the Replication setup docs instead.

This guide is for replicating data to external systems using your own tools. For deploying read-only databases across multiple regions, see Read Replicas instead.

To set up replication, the following is recommended:

To create a replication slot, you will need to use the postgres user and follow the instructions in the external replication setup guide.

If you are running Postgres 17 or higher, you can create a new user and grant them replication permissions with the postgres user. For versions below 17, you will need to use the postgres user.

If you are replicating to an external system and using any of the tools below, check their documentation first. Additional information is provided where the setup with Supabase can vary.

Estuary has the following documentation for setting up Postgres as a source.

---

## Custom Claims & Role-based Access Control (RBAC) | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/custom-claims-and-role-based-access-control-rbac

**Contents:**
- Custom Claims & Role-based Access Control (RBAC)
- Create a table to track user roles and permissions#
- Create Auth Hook to apply user role#
  - Enable the hook#
- Accessing custom claims in RLS policies#
- Accessing custom claims in your application#
- Conclusion#
- More resources#

Custom Claims & Role-based Access Control (RBAC)

Custom Claims are special attributes attached to a user that you can use to control access to portions of your application. For example:

To implement Role-Based Access Control (RBAC) with custom claims, use a Custom Access Token Auth Hook. This hook runs before a token is issued. You can use it to add additional claims to the user's JWT.

This guide uses the Slack Clone example to demonstrate how to add a user_role claim and use it in your Row Level Security (RLS) policies.

In this example, you will implement two user roles with specific permissions:

For the full schema, see the example application on GitHub.

You can now manage your roles and permissions in SQL. For example, to add the mentioned roles and permissions from above, run:

The Custom Access Token Auth Hook runs before a token is issued. You can use it to edit the JWT.

In the dashboard, navigate to Authentication > Hooks (Beta) and select the appropriate Postgres function from the dropdown menu.

When developing locally, follow the local development instructions.

To learn more about Auth Hooks, see the Auth Hooks docs.

To utilize Role-Based Access Control (RBAC) in Row Level Security (RLS) policies, create an authorize method that reads the user's role from their JWT and checks the role's permissions:

You can read more about using functions in RLS policies in the RLS guide.

You can then use the authorize method within your RLS policies. For example, to enable the desired delete access, you would add the following policies:

The auth hook will only modify the access token JWT but not the auth response. Therefore, to access the custom claims in your application, e.g. your browser client, or server-side middleware, you will need to decode the access_token JWT on the auth session.

In a JavaScript client application you can for example use the jwt-decode package:

For server-side logic you can use packages like express-jwt, koa-jwt, PyJWT, dart_jsonwebtoken, Microsoft.AspNetCore.Authentication.JwtBearer, etc.

You now have a robust system in place to manage user roles and permissions within your database that automatically propagates to Supabase Auth.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "user_role": "admin",3  "plan": "TRIAL",4  "user_level": 100,5  "group_name": "Super Guild!",6  "joined_on": "2022-05-20T14:28:18.217Z",7  "group_manager": false,8  "items": ["toothpick", "string", "ring"]9}
```

Example 2 (unknown):
```unknown
1-- Custom types2create type public.app_permission as enum ('channels.delete', 'messages.delete');3create type public.app_role as enum ('admin', 'moderator');45-- USER ROLES6create table public.user_roles (7  id        bigint generated by default as identity primary key,8  user_id   uuid references auth.users on delete cascade not null,9  role      app_role not null,10  unique (user_id, role)11);12comment on table public.user_roles is 'Application roles for each user.';1314-- ROLE PERMISSIONS15create table public.role_permissions (16  id           bigint generated by default as identity primary key,17  role         app_role not null,18  permission   app_permission not null,19  unique (role, permission)20);21comment on table public.role_permissions is 'Application permissions for each role.';
```

Example 3 (unknown):
```unknown
1insert into public.role_permissions (role, permission)2values3  ('admin', 'channels.delete'),4  ('admin', 'messages.delete'),5  ('moderator', 'messages.delete');
```

Example 4 (unknown):
```unknown
1-- Create the auth hook function2create or replace function public.custom_access_token_hook(event jsonb)3returns jsonb4language plpgsql5stable6as $$7  declare8    claims jsonb;9    user_role public.app_role;10  begin11    -- Fetch the user role in the user_roles table12    select role into user_role from public.user_roles where user_id = (event->>'user_id')::uuid;1314    claims := event->'claims';1516    if user_role is not null then17      -- Set the claim18      claims := jsonb_set(claims, '{user_role}', to_jsonb(user_role));19    else20      claims := jsonb_set(claims, '{user_role}', 'null');21    end if;2223    -- Update the 'claims' object in the original event24    event := jsonb_set(event, '{claims}', claims);2526    -- Return the modified or original event27    return event;28  end;29$$;3031grant usage on schema public to supabase_auth_admin;3233grant execute34  on function public.custom_access_token_hook35  to supabase_auth_admin;3637revoke execute38  on function public.custom_access_token_hook39  from authenticated, anon, public;4041grant all42  on table public.user_roles43to supabase_auth_admin;4445revoke all46  on table public.user_roles47  from authenticated, anon, public;4849create policy "Allow auth admin to read user roles" ON public.user_roles50as permissive for select51to supabase_auth_admin52using (true)
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-postgres-upgrade-status

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Drop all tables in a PostgreSQL schema | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/dropping-all-tables-in-schema

**Contents:**
- Drop all tables in a PostgreSQL schema

Drop all tables in a PostgreSQL schema

Execute the following query to drop all tables in a given schema. Replace my-schema-name with the name of your schema. In Supabase, the default schema is public.

This deletes all tables and their associated data. Ensure you have a recent backup before proceeding.

This query works by listing out all the tables in the given schema and then executing a drop table for each (hence the for... loop).

You can run this query using the SQL Editor in the Supabase Dashboard, or via psql if you're connecting directly to the database.

**Examples:**

Example 1 (unknown):
```unknown
1do $$ declare2    r record;3begin4    for r in (select tablename from pg_tables where schemaname = 'my-schema-name') loop5        execute 'drop table if exists ' || quote_ident(r.tablename) || ' cascade';6    end loop;7end $$;
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-postgrest-service-config

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-upgrade-postgres-version

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## AWS S3 | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/s3

**Contents:**
- AWS S3
- Preparation#
  - Enable Wrappers#
  - Enable the S3 Wrapper#
  - Store your credentials (optional)#
  - Connecting to S3#
    - Required S3 permissions#
  - Connecting to S3-compliant Providers - Supabase Storage#
  - Connecting to S3-compliant Providers - Wasabi#
  - Create a schema#

You can enable the AWS S3 wrapper right from the Supabase dashboard.

AWS S3 is an object storage service offering industry-leading scalability, data availability, security, and performance. It is read-only and supports below file formats:

The S3 Wrapper allows you to read data of below formats from S3 within your Postgres database.

The S3 Wrapper also supports below compression algorithms:

Note for CSV and JSONL files: currently all columns in S3 files must be defined in the foreign table and their types must be text type.

Note for Parquet files: the whole Parquet file will be loaded into local memory if it is compressed, so keep the file size as small as possible.

Before you can query S3, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the s3_wrapper FDW:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

We need to provide Postgres with the credentials to connect to S3, and any additional options. We can do this using the create server command:

The full list of options are below:

Below S3 permissions are needed:

If the bucket is versioned, we also need:

We recommend creating a schema to hold all the foreign tables:

The following options are available when creating S3 foreign tables:

This is an object representing CSV files in S3.

This is an object representing JSONL files in S3.

This is an object representing Parquet files in S3.

This FDW doesn't support query pushdown.

The S3 Wrapper uses Parquet file data types from arrow_array::types, below are their mappings to Postgres data types.

This section describes important limitations and considerations when using this FDW:

This will create some "foreign table" inside your Postgres database can read data from S3:

This example will read a CSV file stored on Supabase Storage. The access information can be found on Supabase Storage settings page.

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper s3_wrapper2  handler s3_fdw_handler3  validator s3_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your AWS credentials in Vault and retrieve the created `s3_access_key_id` and `s3_secret_access_key`2select vault.create_secret(3  '<access key id>',4  's3_access_key_id',5  'AWS access key for Wrappers'6);7select vault.create_secret(8  '<secret access key>'9  's3_secret_access_key',10  'AWS secret access key for Wrappers'11);
```

Example 4 (unknown):
```unknown
1create server s3_server2  foreign data wrapper s3_wrapper3  options (4    vault_access_key_id '<your s3_access_key_id from above>',5    vault_secret_access_key '<your s3_secret_access_key from above>',6    aws_region 'us-east-1'7  );
```

---

## pgTAP: Unit Testing | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgtap?queryGroups=database-method&database-method=sql

**Contents:**
- pgTAP: Unit Testing
- Overview#
- Enable the extension#
- Testing tables#
- Testing columns#
- Testing RLS policies#
- Testing functions#
- Resources#

pgTAP is a unit testing extension for Postgres.

Let's cover some basic concepts:

You can also use the results_eq() method to test that a Policy returns the correct data:

**Examples:**

Example 1 (unknown):
```unknown
1begin;2select plan( 1 );34select has_table( 'profiles' );56select * from finish();7rollback;
```

Example 2 (unknown):
```unknown
1begin;2select plan( 2 );34select has_column( 'profiles', 'id' ); -- test that the "id" column exists in the "profiles" table5select col_is_pk( 'profiles', 'id' ); -- test that the "id" column is a primary key67select * from finish();8rollback;
```

Example 3 (unknown):
```unknown
1begin;2select plan( 1 );34select policies_are(5  'public',6  'profiles',7  ARRAY [8    'Profiles are public', -- Test that there is a policy called  "Profiles are public" on the "profiles" table.9    'Profiles can only be updated by the owner'  -- Test that there is a policy called  "Profiles can only be updated by the owner" on the "profiles" table.10  ]11);1213select * from finish();14rollback;
```

Example 4 (unknown):
```unknown
1begin;2select plan( 1 );34select results_eq(5    'select * from profiles()',6    $$VALUES ( 1, 'Anna'), (2, 'Bruce'), (3, 'Caryn')$$,7    'profiles() should return all users'8);91011select * from finish();12rollback;
```

---

## pgrouting: Geospatial Routing | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pgrouting

**Contents:**
- pgrouting: Geospatial Routing
- Enable the extension#
- Example#
- Resources#

pgrouting: Geospatial Routing

pgRouting is Postgres and PostGIS extension adding geospatial routing functionality.

The core functionality of pgRouting is a set of path finding algorithms including:

As an example, we'll solve the traveling salesperson problem using the pgRouting's pgr_TSPeuclidean function from some PostGIS coordinates.

A summary of the traveling salesperson problem is, given a set of city coordinates, solve for a path that goes through each city and minimizes the total distance traveled.

First we populate a table with some X, Y coordinates

Next we use the pgr_TSPeuclidean function to find the best path.

**Examples:**

Example 1 (unknown):
```unknown
1create table wi29 (2  id bigint,3  x float,4  y float,5  geom gis.geometry6);78insert into wi29 (id, x, y)9values10  (1,20833.3333,17100.0000),11  (2,20900.0000,17066.6667),12  (3,21300.0000,13016.6667),13  (4,21600.0000,14150.0000),14  (5,21600.0000,14966.6667),15  (6,21600.0000,16500.0000),16  (7,22183.3333,13133.3333),17  (8,22583.3333,14300.0000),18  (9,22683.3333,12716.6667),19  (10,23616.6667,15866.6667),20  (11,23700.0000,15933.3333),21  (12,23883.3333,14533.3333),22  (13,24166.6667,13250.0000),23  (14,25149.1667,12365.8333),24  (15,26133.3333,14500.0000),25  (16,26150.0000,10550.0000),26  (17,26283.3333,12766.6667),27  (18,26433.3333,13433.3333),28  (19,26550.0000,13850.0000),29  (20,26733.3333,11683.3333),30  (21,27026.1111,13051.9444),31  (22,27096.1111,13415.8333),32  (23,27153.6111,13203.3333),33  (24,27166.6667,9833.3333),34  (25,27233.3333,10450.0000),35  (26,27233.3333,11783.3333),36  (27,27266.6667,10383.3333),37  (28,27433.3333,12400.0000),38  (29,27462.5000,12992.2222);
```

Example 2 (unknown):
```unknown
1select2    *3from4     pgr_TSPeuclidean($$select * from wi29$$)
```

Example 3 (unknown):
```unknown
1seq | node |       cost       |     agg_cost     2-----+------+------------------+------------------3   1 |    1 |                0 |                04   2 |    2 |  74.535614157127 |  74.5356141571275   3 |    6 | 900.617093380362 | 975.1527075374896   4 |   10 | 2113.77757765045 | 3088.930285187937   5 |   11 | 106.718669615254 | 3195.648954803198   6 |   12 | 1411.95293791574 | 4607.601892718939   7 |   13 | 1314.23824873744 | 5921.8401414563710   8 |   14 | 1321.76283931305 | 7243.6029807694211   9 |   17 | 1202.91366735569 |  8446.516648125112  10 |   18 | 683.333268292684 | 9129.8499164177913  11 |   15 | 1108.05137466134 | 10237.901291079114  12 |   19 | 772.082339448903 |  11009.98363052815  13 |   22 | 697.666150054665 | 11707.649780582716  14 |   23 | 220.141999627513 | 11927.791780210217  15 |   21 | 197.926372783442 | 12125.718152993718  16 |   29 | 440.456596290771 | 12566.174749284419  17 |   28 | 592.939989005405 | 13159.114738289820  18 |   26 | 648.288376333318 | 13807.403114623121  19 |   20 | 509.901951359278 | 14317.305065982422  20 |   25 | 1330.83095428717 | 15648.136020269623  21 |   27 |  74.535658878487 | 15722.671679148124  22 |   24 | 559.016994374947 |  16281.68867352325  23 |   16 | 1243.87392358622 | 17525.562597109226  24 |    9 |  4088.0585364911 | 21613.621133600427  25 |    7 |  650.85409697993 | 22264.475230580328  26 |    3 | 891.004385199336 | 23155.479615779629  27 |    4 | 1172.36699411442 |  24327.84660989430  28 |    8 | 994.708187806297 | 25322.554797700331  29 |    5 | 1188.01888359478 | 26510.573681295132  30 |    1 | 2266.91173136004 | 28777.4854126552
```

---

## Connecting with PSQL | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/psql

**Contents:**
- Connecting with PSQL
- Connecting with SSL#

psql is a command-line tool that comes with Postgres.

You should connect to your database using SSL wherever possible, to prevent snooping and man-in-the-middle attacks.

You can obtain your connection info and Server root certificate from your application's dashboard:

Download your SSL certificate to /path/to/prod-supabase.cer.

Find your connection settings. Go to the project Connect panel and copy the URL from the Session pooler section, and copy the parameters into the connection string:

**Examples:**

Example 1 (unknown):
```unknown
1psql "sslmode=verify-full sslrootcert=/path/to/prod-supabase.cer host=[CLOUD_PROVIDER]-0-[REGION].pooler.supabase.com dbname=postgres user=postgres.[PROJECT_REF]"
```

---

## Creating API Routes | Supabase Docs

**URL:** https://supabase.com/docs/guides/api/creating-routes

**Contents:**
- Creating API Routes
- Create a table#
- API URL and keys#
      - Changes to API keys
- Using the API#

API routes are automatically created when you create Postgres Tables, Views, or Functions.

Let's create our first API route by creating a table called todos to store tasks. This creates a corresponding route todos which can accept GET, POST, PATCH, & DELETE requests.

Every Supabase project has a unique API URL. Your API is secured behind an API gateway which requires an API Key for every request.

To do this, you need to get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

The REST API is accessible through the URL https://<project_ref>.supabase.co/rest/v1

Both of these routes require the key to be passed through an apikey header.

You can interact with your API directly via HTTP requests, or you can use the client libraries which we provide.

Let's see how to make a request to the todos table which we created in the first step, using the API URL (SUPABASE_URL) and Key (SUPABASE_PUBLISHABLE_KEY) we provided:

JS Reference: select(), insert(), update(), upsert(), delete(), rpc() (call Postgres functions).

**Examples:**

Example 1 (python):
```python
1// Initialize the JS client2import { createClient } from '@supabase/supabase-js'3const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)45// Make a request6const { data: todos, error } = await supabase.from('todos').select('*')
```

---

## pg_plan_filter: Restrict Total Cost | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/pg_plan_filter

**Contents:**
- pg_plan_filter: Restrict Total Cost
- Enable the extension#
- API#
- Example#
- Resources#

pg_plan_filter: Restrict Total Cost

pg_plan_filter is Postgres extension to block execution of statements where query planner's estimate of the total cost exceeds a threshold. This is intended to give database administrators a way to restrict the contribution an individual query has on database load.

The extension is already enabled by default via shared_preload_libraries setting.

You can follow the instructions below.

plan_filter.statement_cost_limit: restricts the maximum total cost for executed statements plan_filter.limit_select_only: restricts to select statements

Note that limit_select_only = true is not the same as read-only because select statements may modify data, for example, through a function call.

To demonstrate total cost filtering, we'll compare how plan_filter.statement_cost_limit treats queries that are under and over its cost limit. First, we set up a table with some data:

Next, we can review the explain plans for a single record select, and a whole table select.

Now we can choose a statement_cost_filter value between the total cost for the single select (2.49) and the whole table select (135.0) so one statement will succeed and one will fail.

**Examples:**

Example 1 (unknown):
```unknown
1create table book(2  id int primary key3);4-- CREATE TABLE56insert into book(id) select * from generate_series(1, 10000);7-- INSERT 0 10000
```

Example 2 (unknown):
```unknown
1explain select * from book where id =1;2                                QUERY PLAN3---------------------------------------------------------------------------4 Index Only Scan using book_pkey on book  (cost=0.28..2.49 rows=1 width=4)5   Index Cond: (id = 1)6(2 rows)78explain select * from book;9                       QUERY PLAN10---------------------------------------------------------11 Seq Scan on book  (cost=0.00..135.00 rows=10000 width=4)12(1 row)
```

Example 3 (unknown):
```unknown
1set plan_filter.statement_cost_limit = 50; -- between 2.49 and 135.023select * from book where id = 1;4 id5----6  17(1 row)8-- SUCCESS
```

Example 4 (unknown):
```unknown
1select * from book;23ERROR:  plan cost limit exceeded4HINT:  The plan for your query shows that it would probably have an excessive run time. This may be due to a logic error in the SQL, or it maybe just a very costly query. Rewrite your query or increase the configuration parameter "plan_filter.statement_cost_limit".5-- FAILURE
```

---

## Migrate from Heroku to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/heroku

**Contents:**
- Migrate from Heroku to Supabase
- Migrate your Heroku Postgres database to Supabase.
- Quick demo#
- Retrieve your Heroku database credentials #
- Retrieve your Supabase connection string #
- Export your Heroku database to a file #
- Import the database to your Supabase project #
- Additional options#
- Enterprise#

Migrate from Heroku to Supabase

Migrate your Heroku Postgres database to Supabase.

Supabase is one of the best free alternatives to Heroku Postgres. This guide shows how to migrate your Heroku Postgres database to Supabase. This migration requires the pg_dump and psql CLI tools, which are installed automatically as part of the complete Postgres installation package.

Alternatively, use the Heroku to Supabase migration tool to migrate in just a few clicks.

Use pg_dump with your Heroku credentials to export your Heroku database to a file (e.g., heroku_dump.sql).

Use psql to import the Heroku database file to your Supabase project.

Run pg_dump --help for a full list of options.

If you're planning to migrate a database larger than 6 GB, we recommend upgrading to at least a Large compute add-on. This will ensure you have the necessary resources to handle the migration efficiently.

We strongly advise you to pre-provision the disk space you will need for your migration. On paid projects, you can do this by navigating to the Compute and Disk Settings page. For more information on disk scaling and disk limits, check out our disk settings documentation.

Contact us if you need more help migrating your project.

**Examples:**

Example 1 (unknown):
```unknown
1pg_dump --clean --if-exists --quote-all-identifiers \2 -h $HEROKU_HOST -U $HEROKU_USER -d $HEROKU_DATABASE \3 --no-owner --no-privileges > heroku_dump.sql
```

Example 2 (unknown):
```unknown
1psql -d "$YOUR_CONNECTION_STRING" -f heroku_dump.sql
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-postgres-config-get

**Contents:**
- Supabase CLI
  - Additional links#
- Global flags
  - Flags
- supabase bootstrap
  - Usage
  - Flags
- supabase init
  - Usage
  - Flags

The Supabase CLI provides tools to develop your project locally and deploy to the Supabase Platform. The CLI is still under development, but it contains all the functionality for working with your Supabase projects and the Supabase Platform.

Supabase CLI supports global flags for every command.

create a support ticket for any CLI error

output debug logs to stderr

lookup domain names using the specified resolver

enable experimental features

use the specified docker network instead of a generated one

output format of status variables

use a specific profile for connecting to Supabase API

path to a Supabase project directory

answer yes to all prompts

Password to your remote Postgres database.

Initialize configurations for Supabase local development.

A supabase/config.toml file is created in your current working directory. This configuration is specific to each local project.

You may override the directory path by specifying the SUPABASE_WORKDIR environment variable or --workdir flag.

In addition to config.toml, the supabase directory may also contain other Supabase objects, such as migrations, functions, tests, etc.

Overwrite existing supabase/config.toml.

Use OrioleDB storage engine for Postgres.

Generate IntelliJ IDEA settings for Deno.

Generate VS Code settings for Deno.

Connect the Supabase CLI to your Supabase account by logging in with your personal access token.

Your access token is stored securely in native credentials storage. If native credentials storage is unavailable, it will be written to a plain text file at ~/.supabase/access-token.

If this behavior is not desired, such as in a CI environment, you may skip login by specifying the SUPABASE_ACCESS_TOKEN environment variable in other commands.

The Supabase CLI uses the stored token to access Management APIs for projects, functions, secrets, etc.

Name that will be used to store token in your settings

Do not open browser automatically

Use provided token instead of automatic login flow

Link your local development project to a hosted Supabase project.

PostgREST configurations are fetched from the Supabase platform and validated against your local configuration file.

Optionally, database settings can be validated if you provide a password. Your database password is saved in native credentials storage if available.

If you do not want to be prompted for the database password, such as in a CI environment, you may specify it explicitly via the SUPABASE_DB_PASSWORD environment variable.

Some commands like db dump, db push, and db pull require your project to be linked first.

Password to your remote Postgres database.

Project ref of the Supabase project.

Use direct connection instead of pooler.

Starts the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All service containers are started by default. You can exclude those not needed by passing in -x flag. To exclude multiple containers, either pass in a comma separated string, such as -x gotrue,imgproxy, or specify -x flag multiple times.

It is recommended to have at least 7GB of RAM to start all services.

Health checks are automatically added to verify the started containers. Use --ignore-health-check flag to ignore these errors.

Names of containers to not start. [gotrue,realtime,storage-api,imgproxy,kong,mailpit,postgrest,postgres-meta,studio,edge-runtime,logflare,vector,supavisor]

Ignore unhealthy services and exit 0

Stops the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All Docker resources are maintained across restarts. Use --no-backup flag to reset your local development data between restarts.

Use the --all flag to stop all local Supabase projects instances on the machine. Use with caution with --no-backup as it will delete all supabase local projects data.

Stop all local Supabase instances from all projects across the machine.

Deletes all data volumes after stopping.

Local project ID to stop.

Shows status of the Supabase local development stack.

Requires the local development stack to be started by running supabase start or supabase db start.

You can export the connection parameters for initializing supabase-js locally by specifying the -o env flag. Supported parameters include JWT_SECRET, ANON_KEY, and SERVICE_ROLE_KEY.

Override specific variable names.

Executes pgTAP tests against the local database.

Requires the local development stack to be started by running supabase start.

Runs pg_prove in a container with unit test files volume mounted from supabase/tests directory. The test file can be suffixed by either .sql or .pg extension.

Since each test is wrapped in its own transaction, it will be individually rolled back regardless of success or failure.

Tests the database specified by the connection string (must be percent-encoded).

Runs pgTAP tests on the linked project.

Runs pgTAP tests on the local database.

Template framework to generate.

Automatically generates type definitions based on your Postgres database schema.

This command connects to your database (local or remote) and generates typed definitions that match your database tables, views, and stored procedures. By default, it generates TypeScript definitions, but also supports Go and Swift.

Generated types give you type safety and autocompletion when working with your database in code, helping prevent runtime errors and improving developer experience.

The types respect relationships, constraints, and custom types defined in your database schema.

Securely generate a private JWT signing key for use in the CLI or to import in the dashboard.

Supported algorithms: ES256 - ECDSA with P-256 curve and SHA-256 (recommended) RS256 - RSA with SHA-256

Algorithm for signing key generation.

Append new key to existing keys file instead of overwriting.

Generate types from a database url.

Output language of the generated types.

Generate types from the linked project.

Generate types from the local dev database.

Generate types compatible with PostgREST v9 and below.

Generate types from a project ID.

Maximum timeout allowed for the database query.

Comma separated list of schema to include.

Access control for Swift generated types.

Pulls schema changes from a remote database. A new migration file will be created under supabase/migrations directory.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Optionally, a new row can be inserted into the migration history table to reflect the current state of the remote database.

If no entries exist in the migration history table, pg_dump will be used to capture all contents of the remote schemas you have created. Otherwise, this command will only diff schema changes against the remote database, similar to running db diff --linked.

Pulls from the database specified by the connection string (must be percent-encoded).

Pulls from the linked project.

Pulls from the local database.

Password to your remote Postgres database.

Comma separated list of schema to include.

Pushes all local migrations to a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

The first time this command is run, a migration history table will be created under supabase_migrations.schema_migrations. After successfully applying a migration, a new row will be inserted into the migration history table with timestamp as its unique id. Subsequent pushes will skip migrations that have already been applied.

If you need to mutate the migration history table, such as deleting existing entries or inserting new entries without actually running the migration, use the migration repair command.

Use the --dry-run flag to view the list of changes before applying.

Pushes to the database specified by the connection string (must be percent-encoded).

Print the migrations that would be applied, but don't actually apply them.

Include all migrations not found on remote history table.

Include custom roles from supabase/roles.sql.

Include seed data from your config.

Pushes to the linked project.

Pushes to the local database.

Password to your remote Postgres database.

Resets the local database to a clean state.

Requires the local development stack to be started by running supabase start.

Recreates the local Postgres container and applies all local migrations found in supabase/migrations directory. If test data is defined in supabase/seed.sql, it will be seeded after the migrations are run. Any other data or schema changes made during local development will be discarded.

When running db reset with --linked or --db-url flag, a SQL script is executed to identify and drop all user created entities in the remote database. Since Postgres roles are cluster level entities, any custom roles created through the dashboard or supabase/roles.sql will not be deleted by remote reset.

Resets the database specified by the connection string (must be percent-encoded).

Reset up to the last n migration versions.

Resets the linked project with local migrations.

Resets the local database with local migrations.

Skip running the seed script after reset.

Reset up to the specified version.

Dumps contents from a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Runs pg_dump in a container with additional flags to exclude Supabase managed schemas. The ignored schemas include auth, storage, and those created by extensions.

The default dump does not contain any data or custom roles. To dump those contents explicitly, specify either the --data-only and --role-only flag.

Dumps only data records.

Dumps from the database specified by the connection string (must be percent-encoded).

Prints the pg_dump script that would be executed.

List of schema.tables to exclude from data-only dump.

File path to save the dumped contents.

Keeps commented lines from pg_dump output.

Dumps from the linked project.

Dumps from the local database.

Password to your remote Postgres database.

Dumps only cluster roles.

Comma separated list of schema to include.

Use copy statements in place of inserts.

Diffs schema changes made to the local or remote database.

Requires the local development stack to be running when diffing against the local database. To diff against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs djrobstep/migra in a container to compare schema differences between the target database and a shadow database. The shadow database is created by applying migrations in local supabase/migrations directory in a separate container. Output is written to stdout by default. For convenience, you can also save the schema diff as a new migration file by passing in -f flag.

By default, all schemas in the target database are diffed. Use the --schema public,extensions flag to restrict diffing to a subset of schemas.

While the diff command is able to capture most schema changes, there are cases where it is known to fail. Currently, this could happen if you schema contains:

Diffs against the database specified by the connection string (must be percent-encoded).

Saves schema diff to a new migration file.

Diffs local migration files against the linked project.

Diffs local migration files against the local database.

Comma separated list of schema to include.

Use migra to generate schema diff.

Use pg-schema-diff to generate schema diff.

Use pgAdmin to generate schema diff.

Lints local database for schema errors.

Requires the local development stack to be running when linting against the local database. To lint against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs plpgsql_check extension in the local Postgres container to check for errors in all schemas. The default lint level is warning and can be raised to error via the --level flag.

To lint against specific schemas only, pass in the --schema flag.

The --fail-on flag can be used to control when the command should exit with a non-zero status code. The possible values are:

This flag is particularly useful in CI/CD pipelines where you want to fail the build based on certain lint conditions.

Lints the database specified by the connection string (must be percent-encoded).

Error level to exit with non-zero status.

Lints the linked project for schema errors.

Lints the local database for schema errors.

Comma separated list of schema to include.

Path to a logical backup file.

Creates a new migration file locally.

A supabase/migrations directory will be created if it does not already exists in your current workdir. All schema migration files must be created in this directory following the pattern <timestamp>_<name>.sql.

Outputs from other commands like db diff may be piped to migration new <name> via stdin.

Lists migration history in both local and remote databases.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Note that URL strings must be escaped according to RFC 3986.

Local migrations are stored in supabase/migrations directory while remote migrations are tracked in supabase_migrations.schema_migrations table. Only the timestamps are compared to identify any differences.

In case of discrepancies between the local and remote migration history, you can resolve them using the migration repair command.

Lists migrations of the database specified by the connection string (must be percent-encoded).

Lists migrations applied to the linked project.

Lists migrations applied to the local database.

Password to your remote Postgres database.

Fetches migrations from the database specified by the connection string (must be percent-encoded).

Fetches migration history from the linked project.

Fetches migration history from the local database.

Repairs the remote migration history table.

Requires your local project to be linked to a remote database by running supabase link.

If your local and remote migration history goes out of sync, you can repair the remote history by marking specific migrations as --status applied or --status reverted. Marking as reverted will delete an existing record from the migration history table while marking as applied will insert a new record.

For example, your migration history may look like the table below, with missing entries in either local or remote.

To reset your migration history to a clean state, first delete your local migration file.

Then mark the remote migration 20230103054303 as reverted.

Now you can run db pull again to dump the remote schema as a local migration file.

Repairs migrations of the database specified by the connection string (must be percent-encoded).

Repairs the migration history of the linked project.

Repairs the migration history of the local database.

Password to your remote Postgres database.

Version status to update.

Squashes local schema migrations to a single migration file.

The squashed migration is equivalent to a schema only dump of the local database after applying existing migration files. This is especially useful when you want to remove repeated modifications of the same schema from your migration history.

However, one limitation is that data manipulation statements, such as insert, update, or delete, are omitted from the squashed migration. You will have to add them back manually in a new migration file. This includes cron jobs, storage buckets, and any encrypted secrets in vault.

By default, the latest <timestamp>_<name>.sql file will be updated to contain the squashed migration. You can override the target version using the --version <timestamp> flag.

If your supabase/migrations directory is empty, running supabase squash will do nothing.

Squashes migrations of the database specified by the connection string (must be percent-encoded).

Squashes the migration history of the linked project.

Squashes the migration history of the local database.

Password to your remote Postgres database.

Squash up to the specified version.

Applies migrations to the database specified by the connection string (must be percent-encoded).

Include all migrations not found on remote history table.

Applies pending migrations to the linked project.

Applies pending migrations to the local database.

Seeds the linked project.

Seeds the local database.

This command displays an estimation of table "bloat" - Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will asynchronously clean the dead tuples. Sometimes the autovaccum is unable to work fast enough to reduce or prevent tables from becoming bloated. High bloat can slow down queries, cause excessive IOPS and waste space in your database.

Tables with a high bloat ratio should be investigated to see if there are vacuuming is not quick enough or there are other issues.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows you statements that are currently holding locks and blocking, as well as the statement that is being blocked. This can be used in conjunction with inspect db locks to determine which statements need to be terminated in order to resolve lock contention.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command is much like the supabase inspect db outliers command, but ordered by the number of times a statement has been called.

You can use this information to see which queries are called most often, which can potentially be good candidates for optimisation.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays queries that have taken out an exclusive lock on a relation. Exclusive locks typically prevent other operations on that relation from taking place, and can be a cause of "hung" queries that are waiting for a lock to be granted.

If you see a query that is hanging for a very long time or causing blocking issues you may consider killing the query by connecting to the database and running SELECT pg_cancel_backend(PID); to cancel the query. If the query still does not stop you can force a hard stop by running SELECT pg_terminate_backend(PID);

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays currently running queries, that have been running for longer than 5 minutes, descending by duration. Very long running queries can be a source of multiple issues, such as preventing DDL statements completing or vacuum being unable to update relfrozenxid.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays statements, obtained from pg_stat_statements, ordered by the amount of time to execute in aggregate. This includes the statement itself, the total execution time for that statement, the proportion of total execution time for all statements that statement has taken up, the number of times that statement has been called, and the amount of time that statement spent on synchronous I/O (reading/writing from the file system).

Typically, an efficient query will have an appropriate ratio of calls to total execution time, with as little time spent on I/O as possible. Queries that have a high total execution time but low call count should be investigated to improve their performance. Queries that have a high proportion of execution time being spent on synchronous I/O should also be investigated.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows information about logical replication slots that are setup on the database. It shows if the slot is active, the state of the WAL sender process ('startup', 'catchup', 'streaming', 'backup', 'stopping') the replication client address and the replication lag in GB.

This command is useful to check that the amount of replication lag is as low as possible, replication lag can occur due to network latency issues, slow disk I/O, long running transactions or lack of ability for the subscriber to consume WAL fast enough.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command analyzes table I/O patterns to show read/write activity ratios based on block-level operations. It combines data from PostgreSQL's pg_stat_user_tables (for tuple operations) and pg_statio_user_tables (for block I/O) to categorize each table's workload profile.

The command classifies tables into categories:

Note: This command only displays tables that have had both read and write activity. Tables with no I/O operations are not shown. The classification ratio threshold (default: 5:1) determines when a table is considered "heavy" in one direction versus balanced.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This shows you stats about the vacuum activities for each table. Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will aysnchronously clean the dead tuples.

The command lists when the last vacuum and last auto vacuum took place, the row count on the table as well as the count of dead rows and whether autovacuum is expected to run or not. If the number of dead rows is much higher than the row count, or if an autovacuum is expected but has not been performed for some time, this can indicate that autovacuum is not able to keep up and that your vacuum settings need to be tweaked or that you require more compute or disk IOPS to allow autovaccum to complete.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Path to save CSV files in

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Create an organization for the logged-in user.

List all organizations the logged-in user belongs.

Provides tools for creating and managing your Supabase projects.

This command group allows you to list all projects in your organizations, create new projects, delete existing projects, and retrieve API keys. These operations help you manage your Supabase infrastructure programmatically without using the dashboard.

Project management via CLI is especially useful for automation scripts and when you need to provision environments in a repeatable way.

Database password of the project.

Organization ID to create the project in.

Select a region close to you for the best performance.

Select a desired instance size for your project.

List all Supabase projects the logged-in user can access.

Project ref of the Supabase project.

Updates the configurations of a linked Supabase project with the local supabase/config.toml file.

This command allows you to manage project configuration as code by defining settings locally and then pushing them to your remote project.

Project ref of the Supabase project.

Create a preview branch for the linked project.

URL to notify when branch is active healthy.

Whether to create a persistent branch.

Select a region to deploy the branch database.

Select a desired instance size for the branch database.

Whether to clone production data to the branch database.

Project ref of the Supabase project.

List all preview branches of the linked project.

Project ref of the Supabase project.

Retrieve details of the specified preview branch.

Project ref of the Supabase project.

Update a preview branch by its name or ID.

Change the associated git branch.

Rename the preview branch.

URL to notify when branch is active healthy.

Switch between ephemeral and persistent branch.

Override the current branch status.

Project ref of the Supabase project.

Project ref of the Supabase project.

Project ref of the Supabase project.

Delete a preview branch by its name or ID.

Project ref of the Supabase project.

Manage Supabase Edge Functions.

Supabase Edge Functions are server-less functions that run close to your users.

Edge Functions allow you to execute custom server-side code without deploying or scaling a traditional server. They're ideal for handling webhooks, custom API endpoints, data validation, and serving personalized content.

Edge Functions are written in TypeScript and run on Deno compatible edge runtime, which is a secure runtime with no package management needed, fast cold starts, and built-in security.

Creates a new Edge Function with boilerplate code in the supabase/functions directory.

This command generates a starter TypeScript file with the necessary Deno imports and a basic function structure. The function is created as a new directory with the name you specify, containing an index.ts file with the function code.

After creating the function, you can edit it locally and then use supabase functions serve to test it before deploying with supabase functions deploy.

List all Functions in the linked Supabase project.

Project ref of the Supabase project.

Download the source code for a Function from the linked Supabase project.

Project ref of the Supabase project.

Unbundle functions server-side without using Docker.

Serve all Functions locally.

supabase functions serve command includes additional flags to assist developers in debugging Edge Functions via the v8 inspector protocol, allowing for debugging via Chrome DevTools, VS Code, and IntelliJ IDEA for example. Refer to the docs guide for setup instructions.

--inspect-mode [ run | brk | wait ]

Additionally, the following properties can be customized via supabase/config.toml under edge_runtime section.

Path to an env file to be populated to the Function environment.

Path to import map file.

Alias of --inspect-mode brk.

Allow inspecting the main worker.

Activate inspector capability for debugging.

Disable JWT verification for the Function.

Deploy a Function to the linked Supabase project.

Path to import map file.

Maximum number of parallel jobs.

Disable JWT verification for the Function.

Project ref of the Supabase project.

Delete Functions that exist in Supabase project but not locally.

Bundle functions server-side without using Docker.

Delete a Function from the linked Supabase project. This does NOT remove the Function locally.

Project ref of the Supabase project.

Provides tools for managing environment variables and secrets for your Supabase project.

This command group allows you to set, unset, and list secrets that are securely stored and made available to Edge Functions as environment variables.

Secrets management through the CLI is useful for:

Secrets can be set individually or loaded from .env files for convenience.

Set a secret(s) to the linked Supabase project.

Read secrets from a .env file.

Project ref of the Supabase project.

List all secrets in the linked project.

Project ref of the Supabase project.

Unset a secret(s) from the linked Supabase project.

Project ref of the Supabase project.

Recursively list a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Custom Cache-Control header for HTTP upload.

Custom Content-Type header for HTTP upload.

Maximum number of parallel jobs.

Recursively copy a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively move a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively remove a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Add and configure a new connection to a SSO identity provider to your Supabase project.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Comma separated list of email domains to associate with the added identity provider.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Type of identity provider (according to supported protocol).

Project ref of the Supabase project.

List all connections to a SSO identity provider to your Supabase project.

Project ref of the Supabase project.

Provides the information about an established connection to an identity provider. You can use --metadata to obtain the raw SAML 2.0 Metadata XML document stored in your project's configuration.

Show SAML 2.0 XML Metadata only

Project ref of the Supabase project.

Returns all of the important SSO information necessary for your project to be registered with a SAML 2.0 compatible identity provider.

Project ref of the Supabase project.

Update the configuration settings of a already added SSO identity provider.

Add this comma separated list of email domains to the identity provider.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Replace domains with this comma separated list of email domains.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Remove this comma separated list of email domains from the identity provider.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Project ref of the Supabase project.

Remove a connection to an already added SSO identity provider. Removing the provider will prevent existing users from logging in. Please treat this command with care.

Project ref of the Supabase project.

Manage custom domain names for Supabase projects.

Use of custom domains and vanity subdomains is mutually exclusive.

Activates the custom hostname configuration for a project.

This reconfigures your Supabase project to respond to requests on your custom hostname.

After the custom hostname is activated, your project's third-party auth providers will no longer function on the Supabase-provisioned subdomain. Please refer to Prepare to activate your domain section in our documentation to learn more about the steps you need to follow.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Create a custom hostname for your Supabase project.

Expects your custom hostname to have a CNAME record to your Supabase project's subdomain.

The custom hostname to use for your Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Retrieve the custom hostname config for your project, as stored in the Supabase platform.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Manage vanity subdomains for Supabase projects.

Usage of vanity subdomains and custom domains is mutually exclusive.

Activate a vanity subdomain for your Supabase project.

This reconfigures your Supabase project to respond to requests on your vanity subdomain. After the vanity subdomain is activated, your project's auth services will no longer function on the {project-ref}.{supabase-domain} hostname.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

Deletes the vanity subdomain for a project, and reverts to using the project ref for routing.

enable experimental features

Project ref of the Supabase project.

Network bans are IPs that get temporarily blocked if their traffic pattern looks abusive (e.g. multiple failed auth attempts).

The subcommands help you view the current bans, and unblock IPs if desired.

enable experimental features

Project ref of the Supabase project.

IP to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Append to existing restrictions instead of replacing them.

Bypass some of the CIDR validation checks.

CIDR to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Whether the DB should disable SSL enforcement for all external connections.

Whether the DB should enable SSL enforcement for all external connections.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Overriding the default Postgres config could result in unstable database behavior. Custom configuration also overrides the optimizations generated based on the compute add-ons in use.

Config overrides specified as a 'key=value' pair

Do not restart the database after updating config.

If true, replaces all existing overrides with the ones provided. If false (default), merges existing overrides with the ones provided.

enable experimental features

Project ref of the Supabase project.

Delete specific config overrides, reverting them to their default values.

Config keys to delete (comma-separated)

Do not restart the database after deleting config.

enable experimental features

Project ref of the Supabase project.

List all SQL snippets of the linked project.

Project ref of the Supabase project.

Download contents of the specified SQL snippet.

Project ref of the Supabase project.

Generate the autocompletion script for supabase for the specified shell. See each sub-command's help for details on how to use the generated script.

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need to enable it. You can execute the following once:

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for powershell.

To load completions in your current shell session:

To load completions for every new session, add the output of the above command to your powershell profile.

disable completion descriptions

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package. If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

**Examples:**

Example 1 (unknown):
```unknown
1supabase bootstrap [template] [flags]
```

Example 2 (unknown):
```unknown
1supabase init [flags]
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1Finished supabase init.
```

---

## API | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/python/api

**Contents:**
- API
- Installation#
- Usage#
- Connecting#
- Get or Create a Collection#
- Upserting vectors#
- Deleting vectors#
- Create an index#
- Query#
  - Basic#

vecs is a python client for managing and querying vector stores in PostgreSQL with the pgvector extension. This guide will help you get started with using vecs.

If you don't have a Postgres database with the pgvector ready, see hosting for easy options.

You can install vecs using pip:

Before you can interact with vecs, create the client to communicate with Postgres. If you haven't started a Postgres instance yet, see hosting.

You can get a collection (or create if it doesn't exist), specifying the collection's name and the number of dimensions for the vectors you intend to store.

vecs combines the concepts of "insert" and "update" into "upsert". Upserting records adds them to the collection if the id is not present, or updates the existing record if the id does exist.

Deleting records removes them from the collection. To delete records, specify a list of ids or metadata filters to the delete method. The ids of the sucessfully deleted records are returned from the method. Note that attempting to delete non-existent records does not raise an error.

Collections can be queried immediately after being created. However, for good throughput, the collection should be indexed after records have been upserted.

Only one index may exist per-collection. By default, creating an index will replace any existing index.

You may optionally provide a distance measure and index method.

Available options for distance measure are:

which correspond to different methods for comparing query vectors to the vectors in the database.

If you aren't sure which to use, the default of cosine_distance is the most widely compatible with off-the-shelf embedding methods.

Available options for index method are:

Where auto selects the best available index method, hnsw uses the HNSW method and ivfflat uses IVFFlat.

HNSW and IVFFlat indexes both allow for parameterization to control the speed/accuracy tradeoff. vecs provides sane defaults for these parameters. For a greater level of control you can optionally pass an instance of vecs.IndexArgsIVFFlat or vecs.IndexArgsHNSW to create_index's index_arguments argument. Descriptions of the impact for each parameter are available in the pgvector docs.

When using IVFFlat indexes, the index must be created after the collection has been populated with records. Building an IVFFlat index on an empty collection will result in significantly reduced recall. You can continue upserting new documents after the index has been created, but should rebuild the index if the size of the collection more than doubles since the last index operation.

HNSW indexes can be created immediately after the collection without populating records.

To manually specify method, measure, and index_arguments add them as arguments to create_index for example:

Given a collection docs with several records:

The simplest form of search is to provide a query vector.

If you do not create an index, every query will return a warning

that incldues the IndexMeasure you should index.

Which returns a list of vector record ids.

The metadata that is associated with each record can also be filtered during a query.

As an example, {"year": {"$eq": 2005}} filters a year metadata key to be equal to 2005

For a complete reference, see the metadata guide.

When you're done with a collection, be sure to disconnect the client from the database.

alternatively, use the client as a context manager and it will automatically close the connection on exit.

Adapters are an optional feature to transform data before adding to or querying from a collection. Adapters make it possible to interact with a collection using only your project's native data type (eg. just raw text), rather than manually handling vectors.

For a complete list of available adapters, see built-in adapters.

As an example, we'll create a collection with an adapter that chunks text into paragraphs and converts each chunk into an embedding vector using the all-MiniLM-L6-v2 model.

First, install vecs with optional dependencies for text embeddings:

Then create a collection with an adapter to chunk text into paragraphs and embed each paragraph using the all-MiniLM-L6-v2 384 dimensional text embedding model.

With the adapter registered against the collection, we can upsert records into the collection passing in text rather than vectors.

Similarly, we can query the collection using text.

You can create a collection to store vectors specifying the collections name and the number of dimensions in the vectors you intend to store.

To access a previously created collection, use get_collection to retrieve it by name

**Examples:**

Example 1 (unknown):
```unknown
1pip install vecs
```

Example 2 (unknown):
```unknown
1import vecs23DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"45# create vector store client6vx = vecs.create_client(DB_CONNECTION)
```

Example 3 (unknown):
```unknown
1docs = vx.get_or_create_collection(name="docs", dimension=3)
```

Example 4 (unknown):
```unknown
1# add records to the collection2docs.upsert(3    records=[4        (5         "vec0",           # the vector's identifier6         [0.1, 0.2, 0.3],  # the vector. list or np.array7         {"year": 1973}    # associated  metadata8        ),9        (10         "vec1",11         [0.7, 0.8, 0.9],12         {"year": 2012}13        )14    ]15)
```

---

## Snowflake | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/snowflake

**Contents:**
- Snowflake
- Available Versions#
- Preparation#
  - Enable Wrappers#
  - Enable the Snowflake Wrapper#
  - Store your credentials (optional)#
  - Connecting to Snowflake#
  - Create a schema#
- Options#
- Entities#

You can enable the Snowflake wrapper right from the Supabase dashboard.

Snowflake is a cloud-based data platform provided as a DaaS (Data-as-a-Service) solution with data storage and analytics service.

The Snowflake Wrapper is a WebAssembly(Wasm) foreign data wrapper which allows you to read and write data from Snowflake within your Postgres database.

Before you can query Snowflake, you need to enable the Wrappers extension and store your credentials in Postgres.

Make sure the wrappers extension is installed on your database:

Enable the Wasm foreign data wrapper:

By default, Postgres stores FDW credentials inside pg_catalog.pg_foreign_server in plain text. Anyone with access to this table will be able to view these credentials. Wrappers is designed to work with Vault, which provides an additional level of security for storing credentials. We recommend using Vault to store your credentials.

This FDW uses key-pair authentication to access Snowflake SQL Rest API, please refer to Snowflake docs for more details about the key-pair authentication.

We need to provide Postgres with the credentials to connect to Snowflake, and any additional options. We can do this using the create server command:

Note the fdw_package_* options are required, which specify the Wasm package metadata. You can get the available package version list from above.

We recommend creating a schema to hold all the foreign tables:

The full list of foreign table options are below:

table - Source table or view name in Snowflake, required.

This option can also be a subquery enclosed in parentheses.

rowid_column - Primary key column name, optional for data scan, required for data modify

This is an object representing a Snowflake table or view.

This FDW supports where, order by and limit clause pushdown.

This section describes important limitations and considerations when using this FDW:

Let's prepare the source table in Snowflake first:

This example will create a "foreign table" inside your Postgres database and query its data.

This example will modify data in a "foreign table" inside your Postgres database, note that rowid_column option is required for data modify:

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists wrappers with schema extensions;
```

Example 2 (unknown):
```unknown
1create foreign data wrapper wasm_wrapper2  handler wasm_fdw_handler3  validator wasm_fdw_validator;
```

Example 3 (unknown):
```unknown
1-- Save your Snowflake private key in Vault and retrieve the created `key_id`2select vault.create_secret(3  E'-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----',4  'snowflake',5  'Snowflake private key for Wrappers'6);
```

Example 4 (unknown):
```unknown
1create server snowflake_server2  foreign data wrapper wasm_wrapper3  options (4    fdw_package_url 'https://github.com/supabase/wrappers/releases/download/wasm_snowflake_fdw_v0.1.1/snowflake_fdw.wasm',5    fdw_package_name 'supabase:snowflake-fdw',6    fdw_package_version '0.1.1',7    fdw_package_checksum '7aaafc7edc1726bc93ddc04452d41bda9e1a264a1df2ea9bf1b00b267543b860',8    account_identifier 'MYORGANIZATION-MYACCOUNT',9    user 'MYUSER',10    public_key_fingerprint 'SizgPofeFX0jwC8IhbOfGFyOggFgo8oTOS1uPLZhzUQ=',11    private_key_id '<key_ID>' -- The Key ID from above.12  );
```

---

## Permissions | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/permissions

**Contents:**
- Permissions

The Supabase platform offers additional services (e.g. Storage) on top of the Postgres database that comes with each project. These services default to storing their operational data within your database, to ensure that you retain complete control over it.

However, these services assume a base level of access to their data, in order to e.g. be able to run migrations over it. Breaking these assumptions runs the risk of rendering these services inoperational for your project:

It is possible for violations of these assumptions to not cause an immediate outage, but take effect at a later time when a newer migration becomes available.

---

## Testing Your Database | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/testing

**Contents:**
- Testing Your Database
- Testing using the Supabase CLI
- Creating a test#
- Writing tests#
- Running tests#
- More resources#

Testing Your Database

To ensure that queries return the expected data, RLS policies are correctly applied and etc., we encourage you to write automated tests. There are essentially two approaches to testing:

Firstly, you can write tests that interface with a Supabase client instance (same way you use Supabase client in your application code) in the programming language(s) you use in your application and using your favorite testing framework.

Secondly, you can test through the Supabase CLI, which is a more low-level approach where you write tests in SQL.

You can use the Supabase CLI to test your database. The minimum required version of the CLI is v1.11.4. To get started:

Create a tests folder inside the supabase folder:

Create a new file with the .sql extension which will contain the test.

All sql files use pgTAP as the test runner.

Let's write a simple test to check that our auth.users table has an ID column. Open hello_world.test.sql and add the following code:

To run the test, you can use:

This will produce the following output:

**Examples:**

Example 1 (unknown):
```unknown
1mkdir -p ./supabase/tests/database
```

Example 2 (unknown):
```unknown
1touch ./supabase/tests/database/hello_world.test.sql
```

Example 3 (unknown):
```unknown
1begin;2select plan(1); -- only one statement to run34SELECT has_column(5    'auth',6    'users',7    'id',8    'id should exist'9);1011select * from finish();12rollback;
```

Example 4 (unknown):
```unknown
1supabase test db
```

---

## HypoPG: Hypothetical indexes | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/hypopg

**Contents:**
- HypoPG: Hypothetical indexes
- Enable the extension#
  - Speeding up a query#
- Functions#
- Resources#

HypoPG: Hypothetical indexes

HypoPG is Postgres extension for creating hypothetical/virtual indexes. HypoPG allows users to rapidly create hypothetical/virtual indexes that have no resource cost (CPU, disk, memory) that are visible to the Postgres query planner.

The motivation for HypoPG is to allow users to quickly search for an index to improve a slow query without consuming server resources or waiting for them to build.

Given the following table and a simple query to select from the table by id:

We can generate an explain plan for a description of how the Postgres query planner intends to execute the query.

Using HypoPG, we can create a hypothetical index on the account(id) column to check if it would be useful to the query planner and then re-run the explain plan.

Note that the virtual indexes created by HypoPG are only visible in the Postgres connection that they were created in. Supabase connects to Postgres through a connection pooler so the hypopg_create_index statement and the explain statement should be executed in a single query.

The query plan has changed from a Seq Scan to an Index Scan using the newly created virtual index, so we may choose to create a real version of the index to improve performance on the target query:

**Examples:**

Example 1 (unknown):
```unknown
1create table account (2  id int,3  address text4);56insert into account(id, address)7select8  id,9  id || ' main street'10from11  generate_series(1, 10000) id;
```

Example 2 (unknown):
```unknown
1explain select * from account where id=1;23                      QUERY PLAN4-------------------------------------------------------5 Seq Scan on account  (cost=0.00..180.00 rows=1 width=13)6   Filter: (id = 1)7(2 rows)
```

Example 3 (unknown):
```unknown
1select * from hypopg_create_index('create index on account(id)');23explain select * from account where id=1;45                                     QUERY PLAN6------------------------------------------------------------------------------------7 Index Scan using <13504>btree_account_id on hypo  (cost=0.29..8.30 rows=1 width=13)8   Index Cond: (id = 1)9(2 rows)
```

Example 4 (unknown):
```unknown
1create index on account(id);
```

---

## Row Level Security | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/row-level-security

**Contents:**
- Row Level Security
- Secure your data using Postgres Row Level Security.
- Row Level Security in Supabase#
- Policies#
- Enabling Row Level Security#
      - `auth.uid()` Returns `null` When Unauthenticated
- Authenticated and unauthenticated roles#
      - Anonymous user vs the anon key
- Creating policies#
  - SELECT policies#

Secure your data using Postgres Row Level Security.

When you need granular authorization rules, nothing beats Postgres's Row Level Security (RLS).

Supabase allows convenient and secure data access from the browser, as long as you enable RLS.

RLS must always be enabled on any tables stored in an exposed schema. By default, this is the public schema.

RLS is enabled by default on tables created with the Table Editor in the dashboard. If you create one in raw SQL or with the SQL editor, remember to enable RLS yourself:

RLS is incredibly powerful and flexible, allowing you to write complex SQL rules that fit your unique business needs. RLS can be combined with Supabase Auth for end-to-end user security from the browser to the database.

RLS is a Postgres primitive and can provide "defense in depth" to protect your data from malicious actors even when accessed through third-party tooling.

Policies are Postgres's rule engine. Policies are easy to understand once you get the hang of them. Each policy is attached to a table, and the policy is executed every time a table is accessed.

You can just think of them as adding a WHERE clause to every query. For example a policy like this ...

.. would translate to this whenever a user tries to select from the todos table:

You can enable RLS for any table using the enable row level security clause:

Once you have enabled RLS, no data will be accessible via the API when using the public anon key, until you create policies.

When a request is made without an authenticated user (e.g., no access token is provided or the session has expired), auth.uid() returns null.

This means that a policy like:

will silently fail for unauthenticated users, because:

is always false in SQL.

To avoid confusion and make your intention clear, we recommend explicitly checking for authentication:

Supabase maps every request to one of the roles:

These are actually Postgres Roles. You can use these roles within your Policies using the TO clause:

Using the anon Postgres role is different from an anonymous user in Supabase Auth. An anonymous user assumes the authenticated role to access the database and can be differentiated from a permanent user by checking the is_anonymous claim in the JWT.

Policies are SQL logic that you attach to a Postgres table. You can attach as many policies as you want to each table.

Supabase provides some helpers that simplify RLS if you're using Supabase Auth. We'll use these helpers to illustrate some basic policies:

You can specify select policies with the using clause.

Let's say you have a table called profiles in the public schema and you want to enable read access to everyone.

Alternatively, if you only wanted users to be able to see their own profiles:

You can specify insert policies with the with check clause. The with check expression ensures that any new row data adheres to the policy constraints.

Let's say you have a table called profiles in the public schema and you only want users to be able to create a profile for themselves. In that case, we want to check their User ID matches the value that they are trying to insert:

You can specify update policies by combining both the using and with check expressions.

The using clause represents the condition that must be true for the update to be allowed, and with check clause ensures that the updates made adhere to the policy constraints.

Let's say you have a table called profiles in the public schema and you only want users to be able to update their own profile.

You can create a policy where the using clause checks if the user owns the profile being updated. And the with check clause ensures that, in the resultant row, users do not change the user_id to a value that is not equal to their User ID, maintaining that the modified profile still meets the ownership condition.

If no with check expression is defined, then the using expression will be used both to determine which rows are visible (normal USING case) and which new rows will be allowed to be added (WITH CHECK case).

To perform an UPDATE operation, a corresponding SELECT policy is required. Without a SELECT policy, the UPDATE operation will not work as expected.

You can specify delete policies with the using clause.

Let's say you have a table called profiles in the public schema and you only want users to be able to delete their own profile:

Views bypass RLS by default because they are usually created with the postgres user. This is a feature of Postgres, which automatically creates views with security definer.

In Postgres 15 and above, you can make a view obey the RLS policies of the underlying tables when invoked by anon and authenticated roles by setting security_invoker = true.

In older versions of Postgres, protect your views by revoking access from the anon and authenticated roles, or by putting them in an unexposed schema.

Supabase provides some helper functions that make it easier to write Policies.

Returns the ID of the user making the request.

Not all information present in the JWT should be used in RLS policies. For instance, creating an RLS policy that relies on the user_metadata claim can create security issues in your application as this information can be modified by authenticated end users.

Returns the JWT of the user making the request. Anything that you store in the user's raw_app_meta_data column or the raw_user_meta_data column will be accessible using this function. It's important to know the distinction between these two:

The auth.jwt() function is extremely versatile. For example, if you store some team data inside app_metadata, you can use it to determine whether a particular user belongs to a team. For example, if this was an array of IDs:

Keep in mind that a JWT is not always "fresh". In the example above, even if you remove a user from a team and update the app_metadata field, that will not be reflected using auth.jwt() until the user's JWT is refreshed.

Also, if you are using Cookies for Auth, then you must be mindful of the JWT size. Some browsers are limited to 4096 bytes for each cookie, and so the total size of your JWT should be small enough to fit inside this limitation.

The auth.jwt() function can be used to check for Multi-Factor Authentication. For example, you could restrict a user from updating their profile unless they have at least 2 levels of authentication (Assurance Level 2):

Supabase provides special "Service" keys, which can be used to bypass RLS. These should never be used in the browser or exposed to customers, but they are useful for administrative tasks.

Supabase will adhere to the RLS policy of the signed-in user, even if the client library is initialized with a Service Key.

You can also create new Postgres Roles which can bypass Row Level Security using the "bypass RLS" privilege:

This can be useful for system-level access. You should never share login credentials for any Postgres Role with this privilege.

Every authorization system has an impact on performance. While row level security is powerful, the performance impact is important to keep in mind. This is especially true for queries that scan every row in a table - like many select operations, including those using limit, offset, and ordering.

Based on a series of tests, we have a few recommendations for RLS:

Make sure you've added indexes on any columns used within the Policies which are not already indexed (or primary keys). For a Policy like this:

You can add an index like:

You can use select statement to improve policies that use functions. For example, instead of this:

This method works well for JWT functions like auth.uid() and auth.jwt() as well as security definer Functions. Wrapping the function causes an initPlan to be run by the Postgres optimizer, which allows it to "cache" the results per-statement, rather than calling the function on each row.

You can only use this technique if the results of the query or function do not change based on the row data.

Policies are "implicit where clauses," so it's common to run select statements without any filters. This is a bad pattern for performance. Instead of doing this (JS client example):

You should always add a filter:

Even though this duplicates the contents of the Policy, Postgres can use the filter to construct a better query plan.

A "security definer" function runs using the same role that created the function. This means that if you create a role with a superuser (like postgres), then that function will have bypassrls privileges. For example, if you had a policy like this:

We can instead create a security definer function which can scan roles_table without any RLS penalties:

Security-definer functions should never be created in a schema in the "Exposed schemas" inside your API settings`.

You can often rewrite your Policies to avoid joins between the source and the target table. Instead, try to organize your policy to fetch all the relevant data from the target table into an array or set, then you can use an IN or ANY operation in your filter.

For example, this is an example of a slow policy which joins the source test_table to the target team_user:

We can rewrite this to avoid this join, and instead select the filter criteria into a set:

In this case you can also consider using a security definer function to bypass RLS on the join table:

If the list exceeds 1000 items, a different approach may be needed or you may need to analyze the approach to ensure that the performance is acceptable.

Always use the Role of inside your policies, specified by the TO operator. For example, instead of this query:

This prevents the policy ( (select auth.uid()) = user_id ) from running for any anon users, since the execution stops at the to authenticated step.

**Examples:**

Example 1 (unknown):
```unknown
1alter table <schema_name>.<table_name>2enable row level security;
```

Example 2 (unknown):
```unknown
1create policy "Individuals can view their own todos."2on todos for select3using ( (select auth.uid()) = user_id );
```

Example 3 (unknown):
```unknown
1select *2from todos3where auth.uid() = todos.user_id;4-- Policy is implicitly added.
```

Example 4 (unknown):
```unknown
1alter table "table_name" enable row level security;
```

---
