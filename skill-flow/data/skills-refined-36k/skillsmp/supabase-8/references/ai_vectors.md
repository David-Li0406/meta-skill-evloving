# Supabase - Ai Vectors

**Pages:** 48

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-activate-vanity-subdomain-config

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

**URL:** https://supabase.com/docs/reference/cli/supabase-vanity-subdomains-activate

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

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-domains-create

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

**URL:** https://supabase.com/docs/reference/api/v1-check-vanity-subdomain-availability

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

## IVFFlat indexes | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/vector-indexes/ivf-indexes

**Contents:**
- IVFFlat indexes
- Choosing an index#
- Usage#
  - Euclidean L2 distance (vector_l2_ops)#
  - Inner product (vector_ip_ops)#
  - Cosine distance (vector_cosine_ops)#
- How does IVFFlat work?#
  - Inverted lists (cell clusters)#
  - Approximate nearest neighbor#
- When should you create IVFFlat indexes?#

IVFFlat is a type of vector index for approximate nearest neighbor search. It is a frequently used index type that can improve performance when querying highly-dimensional vectors, like those representing embeddings.

Today pgvector supports two types of indexes:

In general we recommend using HNSW because of its performance and robustness against changing data. If you have a special use case that requires IVFFlat instead, keep reading.

The way you create an IVFFlat index depends on the distance operator you are using. pgvector includes 3 distance operators:

Use the following SQL commands to create an IVFFlat index for the operator(s) used in your queries.

Currently vectors with up to 2,000 dimensions can be indexed.

IVF stands for 'inverted file indexes'. It works by clustering your vectors in order to reduce the similarity search scope. Rather than comparing a vector to every other vector, the vector is only compared against vectors within the same cell cluster (or nearby clusters, depending on your configuration).

When you create the index, you choose the number of inverted lists (cell clusters). Increase this number to speed up queries, but at the expense of recall.

For example, to create an index with 100 lists on a column that uses the cosine operator:

For more info on the different operators, see Distance operations.

For every query, you can set the number of probes (1 by default). The number of probes corresponds to the number of nearby cells to probe for a match. Increase this for better recall at the expense of speed.

To set the number of probes for the duration of the session run:

To set the number of probes only for the current transaction run:

If the number of probes is the same as the number of lists, exact nearest neighbor search will be performed and the planner won't use the index.

One important note with IVF indexes is that nearest neighbor search is approximate, since exact search on high dimensional data can't be indexed efficiently. This means that similarity results will change (slightly) after you add an index (trading recall for speed).

pgvector recommends building IVFFlat indexes only after the table has sufficient data, so that the internal IVFFlat cell clusters are based on your data's distribution. Anytime the distribution changes significantly, consider rebuilding indexes.

Read more about indexing on pgvector's GitHub page.

**Examples:**

Example 1 (unknown):
```unknown
1create index on items using ivfflat (column_name vector_l2_ops) with (lists = 100);
```

Example 2 (unknown):
```unknown
1create index on items using ivfflat (column_name vector_ip_ops) with (lists = 100);
```

Example 3 (unknown):
```unknown
1create index on items using ivfflat (column_name vector_cosine_ops) with (lists = 100);
```

Example 4 (unknown):
```unknown
1create index on items using ivfflat (column_name vector_cosine_ops) with (lists = 100);
```

---

## Automatic embeddings | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/automatic-embeddings

**Contents:**
- Automatic embeddings
- Understanding the challenge#
- Understanding the architecture#
- Implementation#
  - Step 1: Enable extensions#
  - Step 2: Create utility functions#
  - Step 3: Create queue and triggers#
    - Why not generate all embeddings in a single Edge Function request?#
    - Why not one request per row?#
    - Why queue requests instead of processing them immediately?#

Vector embeddings enable powerful semantic search capabilities in Postgres, but managing them alongside your content has traditionally been complex. This guide demonstrates how to automate embedding generation and updates using Supabase Edge Functions, pgmq, pg_net, and pg_cron.

When implementing semantic search with pgvector, developers typically need to:

While Postgres full-text search can handle this internally through synchronous calls to to_tsvector and triggers, semantic search requires asynchronous API calls to a provider like OpenAI to generate vector embeddings. This guide demonstrates how to use triggers, queues, and Supabase Edge Functions to bridge this gap.

We'll leverage the following Postgres and Supabase features to create the automated embedding system:

We'll design the system to:

Be generic, so that it can be used with any table and content. This allows you to configure embeddings in multiple places, each with the ability to customize the input used for embedding generation. These will all use the same queue infrastructure and Edge Function to generate the embeddings.

Handle failures gracefully, by retrying failed jobs and providing detailed information about the status of each job.

We'll start by setting up the infrastructure needed to queue and process embedding generation requests. Then we'll create an example table with triggers to enqueue these embedding requests whenever content is inserted or updated.

First, let's enable the required extensions:

Even though the SQL code is create extension, this is the equivalent of "enabling the extension". To disable an extension, call drop extension.

Before we set up our embedding logic, we need to create some utility functions:

Every project has a unique API URL that is required to invoke Edge Functions. Let's go ahead and add the project URL secret to Vault depending on your environment.

When working with a local Supabase stack, add the following to your supabase/seed.sql file:

When deploying to the cloud platform, open the SQL editor and run the following, replacing <project-url> with your project's API URL:

Our goal is to automatically generate embeddings whenever content is inserted or updated within a table. We can use triggers and queues to achieve this. Our approach is to automatically queue embedding jobs whenever records are inserted or updated in a table, then process them asynchronously using a cron job. If a job fails, it will remain in the queue and be retried in the next scheduled task.

First we create a pgmq queue for processing embedding requests:

Next we create a trigger function to queue embedding jobs. We'll use this function to handle both insert and update events:

Our util.queue_embeddings trigger function is generic and can be used with any table and content function. It accepts two arguments:

content_function: The name of a function that returns the text content to be embedded. The function should accept a single row as input and return text (see the embedding_input example).

This allows you to customize the text input passed to the embedding model - for example, you could concatenate multiple columns together like title and content and use the result as input.

embedding_column: The name of the destination column where the embedding will be stored.

Note that the util.queue_embeddings trigger function requires a for each row clause to work correctly. See Usage for an example of how to use this trigger function with your table.

Next we'll create a function to process the embedding jobs. This function will read jobs from the queue, group them into batches, and invoke the Edge Function to generate embeddings. We'll use pg_cron to schedule this function to run every 10 seconds.

Let's discuss some common questions about this approach:

While this is possible, it can lead to long processing times and potential timeouts. Batching allows us to process multiple embeddings concurrently and handle failures more effectively.

This approach can lead to API rate limiting and performance issues. Batching provides a balance between efficiency and reliability.

Queuing allows us to handle failures gracefully, retry requests, and manage concurrency more effectively. Specifically we are using pgmq's visibility timeouts to ensure that failed requests are retried.

Every time we read a message from the queue, we set a visibility timeout which tells pgmq to hide the message from other readers for a certain period. If the Edge Function fails to process the message within this period, the message becomes visible again and will be retried by the next scheduled task.

We use pg_cron to schedule a task that reads messages from the queue and processes them. If the Edge Function fails to process a message, it becomes visible again after a timeout and can be retried by the next scheduled task.

This interval is a good starting point, but you may need to adjust it based on your workload and the time it takes to generate embeddings. You can adjust the batch_size, max_requests, and timeout_milliseconds parameters to optimize performance.

Finally we'll create the Edge Function to generate embeddings. We'll use OpenAI's API in this example, but you can replace it with any other embedding generation service.

Use the Supabase CLI to create a new Edge Function:

This will create a new directory supabase/functions/embed with an index.ts file. Replace the contents of this file with the following:

supabase/functions/embed/index.ts:

The Edge Function listens for incoming HTTP requests from pg_net and processes each embedding job. It is a generic worker that can handle embedding jobs for any table and column. It uses OpenAI's API to generate embeddings and updates the corresponding row in the database. It also deletes the job from the queue once it has been processed.

The function is designed to process multiple jobs independently. If one job fails, it will not affect the processing of other jobs. The function returns a 200 OK response with a list of completed and failed jobs. We can use this information to diagnose failed jobs. See Troubleshooting for more details.

You will need to set the OPENAI_API_KEY environment variable to authenticate with OpenAI. When running the Edge Function locally, you can add it to a .env file:

When you're ready to deploy the Edge Function, set can set the environment variable using the Supabase CLI:

Alternatively, you can replace the generateEmbedding function with your own embedding generation logic.

See Deploy to Production for more information on how to deploy the Edge Function.

Now that the infrastructure is in place, let's go through an example of how to use this system to automatically generate embeddings for a table of documents. You can use this approach with multiple tables and customize the input for each embedding generation as needed.

We'll set up a new documents table that will store our content and embeddings:

Our documents table stores the title and content of each document along with its vector embedding. We use a halfvec(1536) column to store the embeddings.

halfvec is a pgvector data type that stores float values in half precision (16 bits) to save space. Our Edge Function used OpenAI's text-embedding-3-small model which generates 1536-dimensional embeddings, so we use the same dimensionality here. Adjust this based on the number of dimensions your embedding model generates.

We use an HNSW index on the vector column. Note that we are choosing halfvec_cosine_ops as the index method, which means our future queries will need to use cosine distance (<=>) to find similar embeddings. Also note that HNSW indexes support a maximum of 4000 dimensions for halfvec vectors, so keep this in mind when choosing an embedding model. If your model generates embeddings with more than 4000 dimensions, you will need to reduce the dimensionality before indexing them. See Matryoshka embeddings for a potential solution to shortening dimensions.

Also note that the table must have a primary key column named id for our triggers to work correctly with the util.queue_embeddings function and for our Edge Function to update the correct row.

Now we'll set up the triggers to enqueue embedding jobs whenever content is inserted or updated:

We create 2 triggers:

embed_documents_on_insert: Enqueues embedding jobs whenever new rows are inserted into the documents table.

embed_documents_on_update: Enqueues embedding jobs whenever the title or content columns are updated in the documents table.

Both of these triggers use the same util.queue_embeddings function that will queue the embedding jobs for processing. They accept 2 arguments:

embedding_input: The name of the function that generates the input for embedding generation. This function allows you to customize the text input passed to the embedding model (e.g. concatenating the title and content). The function should accept a single row as input and return text.

embedding: The name of the destination column where the embedding will be stored.

Note that the update trigger only fires when the title or content columns are updated. This is to avoid unnecessary updates to the embedding column when other columns are updated. Make sure that these columns match the columns used in the embedding_input function.

Note that our trigger will enqueue new embedding jobs when content is updated, but it will not clear any existing embeddings. This means that an embedding can be temporarily out of sync with the content until the new embedding is generated and updated.

If it is more important to have accurate embeddings than any embedding, you can add another trigger to clear the existing embedding until the new one is generated:

util.clear_column is a generic trigger function we created earlier that can be used to clear any column in a table.

This example will clear the embedding column whenever the title or content columns are updated (note the of title, content clause). This ensures that the embedding is always in sync with the title and content, but it will result in temporary gaps in search results until the new embedding is generated.

We intentionally use a before trigger because it allows us to modify the record before it's written to disk, avoiding an extra update statement that would be needed with an after trigger.

Let's insert a new document and update its content to see the embedding generation in action:

You should observe that the embedding column is initially null after inserting the document. This is because the embedding generation is asynchronous and will be processed by the Edge Function in the next scheduled task.

Wait up to 10 seconds for the next task to run, then check the embedding column again:

You should see the generated embedding for the document.

Next let's update the content of the document:

You should observe that the embedding column is reset to null after updating the content. This is because of the trigger we added to clear existing embeddings whenever the content is updated. The embedding will be regenerated by the Edge Function in the next scheduled task.

Wait up to 10 seconds for the next task to run, then check the embedding column again:

You should see the updated embedding for the document.

Finally we'll update the title of the document:

You should observe that the embedding column is once again reset to null after updating the title. This is because the trigger we added to clear existing embeddings fires when either the content or title columns are updated. The embedding will be regenerated by the Edge Function in the next scheduled task.

Wait up to 10 seconds for the next task to run, then check the embedding column again:

You should see the updated embedding for the document.

The embed Edge Function processes a batch of embedding jobs and returns a 200 OK response with a list of completed and failed jobs in the body. For example:

It also returns the number of completed and failed jobs in the response headers. For example:

You can also use the x-deno-execution-id header to trace the execution of the Edge Function within the dashboard logs.

Each failed job includes an error field with a description of the failure. Reasons for a job failing could include:

pg_net stores HTTP responses in the net._http_response table, which can be queried to diagnose issues with the embedding generation process.

Automating embedding generation and updates in Postgres allow you to build powerful semantic search capabilities without the complexity of managing embeddings manually.

By combining Postgres features like triggers, queues, and other extensions with Supabase Edge Functions, we can create a robust system that handles embedding generation asynchronously and retries failed jobs automatically.

This system can be customized to work with any content and embedding generation service, providing a flexible and scalable solution for semantic search in Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1-- For vector operations2create extension if not exists vector3with4  schema extensions;56-- For queueing and processing jobs7-- (pgmq will create its own schema)8create extension if not exists pgmq;910-- For async HTTP requests11create extension if not exists pg_net12with13  schema extensions;1415-- For scheduled processing and retries16-- (pg_cron will create its own schema)17create extension if not exists pg_cron;1819-- For clearing embeddings during updates20create extension if not exists hstore21with22  schema extensions;
```

Example 2 (javascript):
```javascript
1-- Schema for utility functions2create schema util;34-- Utility function to get the Supabase project URL (required for Edge Functions)5create function util.project_url()6returns text7language plpgsql8security definer9as $$10declare11  secret_value text;12begin13  -- Retrieve the project URL from Vault14  select decrypted_secret into secret_value from vault.decrypted_secrets where name = 'project_url';15  return secret_value;16end;17$$;1819-- Generic function to invoke any Edge Function20create or replace function util.invoke_edge_function(21  name text,22  body jsonb,23  timeout_milliseconds int = 5 * 60 * 1000  -- default 5 minute timeout24)25returns void26language plpgsql27as $$28declare29  headers_raw text;30  auth_header text;31begin32  -- If we're in a PostgREST session, reuse the request headers for authorization33  headers_raw := current_setting('request.headers', true);3435  -- Only try to parse if headers are present36  auth_header := case37    when headers_raw is not null then38      (headers_raw::json->>'authorization')39    else40      null41  end;4243  -- Perform async HTTP request to the edge function44  perform net.http_post(45    url => util.project_url() || '/functions/v1/' || name,46    headers => jsonb_build_object(47      'Content-Type', 'application/json',48      'Authorization', auth_header49    ),50    body => body,51    timeout_milliseconds => timeout_milliseconds52  );53end;54$$;5556-- Generic trigger function to clear a column on update57create or replace function util.clear_column()58returns trigger59language plpgsql as $$60declare61    clear_column text := TG_ARGV[0];62begin63    NEW := NEW #= hstore(clear_column, NULL);64    return NEW;65end;66$$;
```

Example 3 (unknown):
```unknown
1select2  vault.create_secret('http://api.supabase.internal:8000', 'project_url');
```

Example 4 (unknown):
```unknown
1select2  vault.create_secret('<project-url>', 'project_url');
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-list-available-restore-versions

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

## Generate image captions using Hugging Face | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/huggingface-image-captioning

**Contents:**
- Generate image captions using Hugging Face
- Use the Hugging Face Inference API to make calls to 100,000+ Machine Learning models from Supabase Edge Functions.
- About Hugging Face#
- Setup#
- Generate TypeScript types#
- Code#

Generate image captions using Hugging Face

Use the Hugging Face Inference API to make calls to 100,000+ Machine Learning models from Supabase Edge Functions.

We can combine Hugging Face with Supabase Storage and Database Webhooks to automatically caption for any image we upload to a storage bucket.

Hugging Face is the collaboration platform for the machine learning community.

Huggingface.js provides a convenient way to make calls to 100,000+ Machine Learning models, making it easy to incorporate AI functionality into your Supabase Edge Functions.

To generate the types.ts file for the storage and public schemas, run the following command in the terminal:

Find the complete code on GitHub.

**Examples:**

Example 1 (unknown):
```unknown
1supabase gen types typescript --project-id=your-project-ref --schema=storage,public > supabase/functions/huggingface-image-captioning/types.ts
```

Example 2 (python):
```python
1import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'2import { HfInference } from 'https://esm.sh/@huggingface/inference@2.3.2'3import { createClient } from 'npm:@supabase/supabase-js@2'4import { Database } from './types.ts'56console.log('Hello from `huggingface-image-captioning` function!')78const hf = new HfInference(Deno.env.get('HUGGINGFACE_ACCESS_TOKEN'))910type SoRecord = Database['storage']['Tables']['objects']['Row']11interface WebhookPayload {12  type: 'INSERT' | 'UPDATE' | 'DELETE'13  table: string14  record: SoRecord15  schema: 'public'16  old_record: null | SoRecord17}1819serve(async (req) => {20  const payload: WebhookPayload = await req.json()21  const soRecord = payload.record22  const supabaseAdminClient = createClient<Database>(23    // Supabase API URL - env var exported by default when deployed.24    Deno.env.get('SUPABASE_URL') ?? '',25    // Supabase API SERVICE ROLE KEY - env var exported by default when deployed.26    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''27  )2829  // Construct image url from storage30  const { data, error } = await supabaseAdminClient.storage31    .from(soRecord.bucket_id!)32    .createSignedUrl(soRecord.path_tokens!.join('/'), 60)33  if (error) throw error34  const { signedUrl } = data3536  // Run image captioning with Huggingface37  const imgDesc = await hf.imageToText({38    data: await (await fetch(signedUrl)).blob(),39    model: 'nlpconnect/vit-gpt2-image-captioning',40  })4142  // Store image caption in Database table43  await supabaseAdminClient44    .from('image_caption')45    .insert({ id: soRecord.id!, caption: imgDesc.generated_text })46    .throwOnError()4748  return new Response('ok')49})
```

---

## Vector search with Next.js and OpenAI | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/nextjs-vector-search

**Contents:**
- Vector search with Next.js and OpenAI
- Learn how to build a ChatGPT-style doc search powered by Next.js, OpenAI, and Supabase.
- Create a project#
- Prepare the database#
- Pre-process the knowledge base at build time#
  - Generate Embeddings
  - Set up environment variables
  - Run script at build time
- Create text completion with OpenAI API#
  - Create Embedding for Question

Vector search with Next.js and OpenAI

Learn how to build a ChatGPT-style doc search powered by Next.js, OpenAI, and Supabase.

While our Headless Vector search provides a toolkit for generative Q&A, in this tutorial we'll go more in-depth, build a custom ChatGPT-like search experience from the ground-up using Next.js. You will:

You can read our Supabase Clippy blog post for a full example.

We assume that you have a Next.js project with a collection of .mdx files nested inside your pages directory. We will start developing locally with the Supabase CLI and then push our local database changes to our hosted Supabase project. You can find the full Next.js example on GitHub.

Let's prepare the database schema. We can use the "OpenAI Vector Search" quickstart in the SQL Editor, or you can copy/paste the SQL below and run it yourself.

With our database set up, we need to process and store all .mdx files in the pages directory. You can find the full script here, or follow the steps below:

Create a new file lib/generate-embeddings.ts and copy the code over from GitHub.

We need some environment variables to run the script. Add them to your .env file and make sure your .env file is not committed to source control! You can get your local Supabase credentials by running supabase status.

Include the script in your package.json script commands to enable Vercel to automatically run it at build time.

Anytime a user asks a question, we need to create an embedding for their question, perform a similarity search, and then send a text completion request to the OpenAI API with the query and then context content merged together into a prompt.

All of this is glued together in a Vercel Edge Function, the code for which can be found on GitHub.

In order to perform similarity search we need to turn the question into an embedding.

Using the embeddingResponse we can now perform similarity search by performing an remote procedure call (RPC) to the database function we created earlier.

With the relevant content for the user's question identified, we can now build the prompt and make a text completion request via the OpenAI API.

If successful, the OpenAI API will respond with a text/event-stream response that we can forward to the client where we'll process the event stream to smoothly print the answer to the user.

In a last step, we need to process the event stream from the OpenAI API and print the answer to the user. The full code for this can be found on GitHub.

Want to learn more about the awesome tech that is powering this?

**Examples:**

Example 1 (unknown):
```unknown
1curl \2https://raw.githubusercontent.com/supabase-community/nextjs-openai-doc-search/main/lib/generate-embeddings.ts \3-o "lib/generate-embeddings.ts"
```

Example 2 (unknown):
```unknown
1NEXT_PUBLIC_SUPABASE_URL=2NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=3SUPABASE_SERVICE_ROLE_KEY=45# Get your key at https://platform.openai.com/account/api-keys6OPENAI_API_KEY=
```

Example 3 (unknown):
```unknown
1"scripts": {2  "dev": "next dev",3  "build": "pnpm run embeddings && next build",4  "start": "next start",5  "embeddings": "tsx lib/generate-embeddings.ts"6},
```

Example 4 (javascript):
```javascript
1const embeddingResponse = await fetch('https://api.openai.com/v1/embeddings', {2  method: 'POST',3  headers: {4    Authorization: `Bearer ${openAiKey}`,5    'Content-Type': 'application/json',6  },7  body: JSON.stringify({8    model: 'text-embedding-ada-002',9    input: sanitizedQuery.replaceAll('\n', ' '),10  }),11})1213if (embeddingResponse.status !== 200) {14  throw new ApplicationError('Failed to create embedding for question', embeddingResponse)15}1617const {18  data: [{ embedding }],19} = await embeddingResponse.json()
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-migration-repair

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

## Amazon Bedrock | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/integrations/amazon-bedrock

**Contents:**
- Amazon Bedrock
- Create an environment#
- Create embeddings#
  - Store the embeddings with vecs#
  - Querying for most similar sentences#
- Resources#

Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon. Each model is accessible through a common API which implements a broad set of features to help build generative AI applications with security, privacy, and responsible AI in mind.

This guide will walk you through an example using Amazon Bedrock SDK with vecs. We will create embeddings using the Amazon Titan Embeddings G1 – Text v1.2 (amazon.titan-embed-text-v1) model, insert these embeddings into a Postgres database using vecs, and then query the collection to find the most similar sentences to a given query sentence.

First, you need to set up your environment. You will need Python 3.7+ with the vecs and boto3 libraries installed.

You can install the necessary Python libraries using pip:

Next, we will use Amazon’s Titan Embedding G1 - Text v1.2 model to create embeddings for a set of sentences.

Now that we have our embeddings, we can insert them into a Postgres database using vecs.

Now, we query the sentences collection to find the most similar sentences to a sample query sentence. First need to create an embedding for the query sentence. Next, we query the collection we created earlier to find the most similar sentences.

This returns the most similar 3 records and their distance to the query vector.

**Examples:**

Example 1 (unknown):
```unknown
1pip install vecs boto3
```

Example 2 (python):
```python
1import boto32import vecs3import json45client = boto3.client(6    'bedrock-runtime',7    region_name='us-east-1',8	# Credentials from your AWS account9    aws_access_key_id='<replace_your_own_credentials>',10    aws_secret_access_key='<replace_your_own_credentials>',11    aws_session_token='<replace_your_own_credentials>',12)1314dataset = [15    "The cat sat on the mat.",16    "The quick brown fox jumps over the lazy dog.",17    "Friends, Romans, countrymen, lend me your ears",18    "To be or not to be, that is the question.",19]2021embeddings = []2223for sentence in dataset:24    # invoke the embeddings model for each sentence25    response = client.invoke_model(26        body= json.dumps({"inputText": sentence}),27        modelId= "amazon.titan-embed-text-v1",28        accept = "application/json",29        contentType = "application/json"30    )31    # collect the embedding from the response32    response_body = json.loads(response["body"].read())33    # add the embedding to the embedding list34    embeddings.append((sentence, response_body.get("embedding"), {}))
```

Example 3 (unknown):
```unknown
1import vecs23DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"45# create vector store client6vx = vecs.Client(DB_CONNECTION)78# create a collection named 'sentences' with 1536 dimensional vectors9# to match the default dimension of the Titan Embeddings G1 - Text model10sentences = vx.get_or_create_collection(name="sentences", dimension=1536)1112# upsert the embeddings into the 'sentences' collection13sentences.upsert(records=embeddings)1415# create an index for the 'sentences' collection16sentences.create_index()
```

Example 4 (unknown):
```unknown
1query_sentence = "A quick animal jumps over a lazy one."23# create vector store client4vx = vecs.Client(DB_CONNECTION)56# create an embedding for the query sentence7response = client.invoke_model(8        body= json.dumps({"inputText": query_sentence}),9        modelId= "amazon.titan-embed-text-v1",10        accept = "application/json",11        contentType = "application/json"12    )1314response_body = json.loads(response["body"].read())1516query_embedding = response_body.get("embedding")1718# query the 'sentences' collection for the most similar sentences19results = sentences.query(20    data=query_embedding,21    limit=3,22    include_value = True23)2425# print the results26for result in results:27    print(result)
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-domains-delete

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

## Semantic search | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/semantic-search

**Contents:**
- Semantic search
- Learn how to search by meaning rather than exact keywords.
- When to use semantic search#
- How semantic search works#
- Embedding models#
- Semantic search in Postgres#
  - Similarity metric#
  - Calling from your application#
- Next steps#
- See also#

Learn how to search by meaning rather than exact keywords.

Semantic search interprets the meaning behind user queries rather than exact keywords. It uses machine learning to capture the intent and context behind the query, handling language nuances like synonyms, phrasing variations, and word relationships.

Semantic search is useful in applications where the depth of understanding and context is important for delivering relevant results. A good example is in customer support or knowledge base search engines. Users often phrase their problems or questions in various ways, and a traditional keyword-based search might not always retrieve the most helpful documents. With semantic search, the system can understand the meaning behind the queries and match them with relevant solutions or articles, even if the exact wording differs.

For instance, a user searching for "increase text size on display" might miss articles titled "How to adjust font size in settings" in a keyword-based search system. However, a semantic search engine would understand the intent behind the query and correctly match it to relevant articles, regardless of the specific terminology used.

It's also possible to combine semantic search with keyword search to get the best of both worlds. See Hybrid search for more details.

Semantic search uses an intermediate representation called an “embedding vector” to link database records with search queries. A vector, in the context of semantic search, is a list of numerical values. They represent various features of the text and allow for the semantic comparison between different pieces of text.

The best way to think of embeddings is by plotting them on a graph, where each embedding is a single point whose coordinates are the numerical values within its vector. Importantly, embeddings are plotted such that similar concepts are positioned close together while dissimilar concepts are far apart. For more details, see What are embeddings?

Embeddings are generated using a language model, and embeddings are compared to each other using a similarity metric. The language model is trained to understand the semantics of language, including syntax, context, and the relationships between words. It generates embeddings for both the content in the database and the search queries. Then the similarity metric, often a function like cosine similarity or dot product, is used to compare the query embeddings with the document embeddings (in other words, to measure how close they are to each other on the graph). The documents with embeddings most similar to the query's are deemed the most relevant and are returned as search results.

There are many embedding models available today. Supabase Edge Functions has built in support for the gte-small model. Others can be accessed through third-party APIs like OpenAI, where you send your text in the request and receive an embedding vector in the response. Others can run locally on your own compute, such as through Transformers.js for JavaScript implementations. For more information on local implementation, see Generate embeddings.

It's crucial to remember that when using embedding models with semantic search, you must use the same model for all embedding comparisons. Comparing embeddings created by different models will yield meaningless results.

To implement semantic search in Postgres we use pgvector - an extension that allows for efficient storage and retrieval of high-dimensional vectors. These vectors are numerical representations of text (or other types of data) generated by embedding models.

Enable the pgvector extension by running:

Create a table to store the embeddings:

Or if you have an existing table, you can add a vector column like so:

In this example, we create a column named embedding which uses the newly enabled vector data type. The size of the vector (as indicated in parentheses) represents the number of dimensions in the embedding. Here we use 512, but adjust this to match the number of dimensions produced by your embedding model.

For more details on vector columns, including how to generate embeddings and store them, see Vector columns.

pgvector support 3 operators for computing distance between embeddings:

These operators are used directly in your SQL query to retrieve records that are most similar to the user's search query. Choosing the right operator depends on your needs. Inner product (also known as dot product) tends to be the fastest if your vectors are normalized.

The easiest way to perform semantic search in Postgres is by creating a function:

Here we create a function match_documents that accepts three parameters:

In this example, we return a setof documents and refer to documents throughout the query. Adjust this to use the relevant tables in your application.

You'll notice we are using the cosine distance (<=>) operator in our query. Cosine distance is a safe default when you don't know whether or not your embeddings are normalized. If you know for a fact that they are normalized (for example, your embedding is returned from OpenAI), you can use negative inner product (<#>) for better performance:

Note that since <#> is negative, we negate match_threshold accordingly in the where clause. For more information on the different operators, see the pgvector docs.

Finally you can execute this function from your application. If you are using a Supabase client library such as supabase-js, you can invoke it using the rpc() method:

You can also call this method directly from SQL:

In this scenario, you'll likely use a Postgres client library to establish a direct connection from your application to the database. It's best practice to parameterize your arguments before executing the query.

As your database scales, you will need an index on your vector columns to maintain fast query speeds. See Vector indexes for an in-depth guide on the different types of indexes and how they work.

**Examples:**

Example 1 (unknown):
```unknown
1create extension vector2with3  schema extensions;
```

Example 2 (unknown):
```unknown
1create table documents (2  id bigint primary key generated always as identity,3  content text,4  embedding extensions.vector(512)5);
```

Example 3 (unknown):
```unknown
1alter table documents2add column embedding extensions.vector(512);
```

Example 4 (javascript):
```javascript
1-- Match documents using cosine distance (<=>)2create or replace function match_documents (3  query_embedding extensions.vector(512),4  match_threshold float,5  match_count int6)7returns setof documents8language sql9as $$10  select *11  from documents12  where documents.embedding <=> query_embedding < 1 - match_threshold13  order by documents.embedding <=> query_embedding asc14  limit least(match_count, 200);15$$;
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-domains-activate

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

## Engineering for Scale | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/engineering-for-scale

**Contents:**
- Engineering for Scale
- Building an enterprise-grade vector architecture.
- Simple workloads#
- Enterprise workloads#
  - Query collections using Vecs#
  - Accessing external collections using Wrappers#
    - Connecting your remote database#
    - Create a foreign table#
  - Enterprise architecture#

Engineering for Scale

Building an enterprise-grade vector architecture.

Content sources for vectors can be extremely large. As you grow you should run your Vector workloads across several secondary databases (sometimes called "pods"), which allows each collection to scale independently.

For small workloads, it's typical to store your data in a single database.

If you've used Vecs to create 3 different collections, you can expose collections to your web or mobile application using views:

For example, with 3 collections, called docs, posts, and images, we could expose the "docs" inside the public schema like this:

You can then use any of the client libraries to access your collections within your applications:

As you move into production, we recommend splitting your collections into separate projects. This is because it allows your vector stores to scale independently of your production data. Vectors typically grow faster than operational data, and they have different resource requirements. Running them on separate databases removes the single-point-of-failure.

You can use as many secondary databases as you need to manage your collections. With this architecture, you have 2 options for accessing collections within your application:

You can use both of these in tandem to suit your use-case. We recommend option 1 wherever possible, as it offers the most scalability.

Vecs provides methods for querying collections, either using a cosine similarity function or with metadata filtering.

Supabase supports Foreign Data Wrappers. Wrappers allow you to connect two databases together so that you can query them over the network.

This involves 2 steps: connecting to your remote database from the primary and creating a Foreign Table.

Inside your Primary database we need to provide the credentials to access the secondary database:

We can now create a foreign table to access the data in our secondary project.

This looks very similar to our View example above, and you can continue to use the client libraries to access your collections through the foreign table:

This diagram provides an example architecture that allows you to access the collections either with our client libraries or using Vecs. You can add as many secondary databases as you need (in this example we only show one):

**Examples:**

Example 1 (unknown):
```unknown
1create view public.docs as2select3  id,4  embedding,5  metadata, # Expose the metadata as JSON6  (metadata->>'url')::text as url # Extract the URL as a string7from vector
```

Example 2 (javascript):
```javascript
1const { data, error } = await supabase2  .from('docs')3  .select('id, embedding, metadata')4  .eq('url', '/hello-world')
```

Example 3 (unknown):
```unknown
1# cosine similarity2docs.query(query_vector=[0.4,0.5,0.6], limit=5)34# metadata filtering5docs.query(6    query_vector=[0.4,0.5,0.6],7    limit=5,8    filters={"year": {"$eq": 2012}}, # metadata filters9)
```

Example 4 (unknown):
```unknown
1create extension postgres_fdw;23create server docs_server4foreign data wrapper postgres_fdw5options (host 'db.xxx.supabase.co', port '5432', dbname 'postgres');67create user mapping for docs_user8server docs_server9options (user 'postgres', password 'password');
```

---

## Keyword search | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/keyword-search

**Contents:**
- Keyword search
- Learn how to search by words or phrases.
- When and why to use keyword search#
- Using full-text search#
- See also#

Learn how to search by words or phrases.

Keyword search involves locating documents or records that contain specific words or phrases, primarily based on the exact match between the search terms and the text within the data. It differs from semantic search, which interprets the meaning behind the query to provide results that are contextually related, even if the exact words aren't present in the text. Semantic search considers synonyms, intent, and natural language nuances to provide a more nuanced approach to information retrieval.

In Postgres, keyword search is implemented using full-text search. It supports indexing and text analysis for data retrieval, focusing on records that match the search criteria. Postgres' full-text search extends beyond simple keyword matching to address linguistic nuances, making it effective for applications that require precise text queries.

Keyword search is particularly useful in scenarios where precision and specificity matter. It's more effective than semantic search when users are looking for information using exact terminology or specific identifiers. It ensures that results directly contain those terms, reducing the chance of retrieving irrelevant information that might be semantically related but not what the user seeks.

For example in technical or academic research databases, researchers often search for specific studies, compounds, or concepts identified by certain terms or codes. Searching for a specific chemical compound using its exact molecular formula or a unique identifier will yield more focused and relevant results compared to a semantic search, which could return a wide range of documents discussing the compound in different contexts. Keyword search ensures documents that explicitly mention the exact term are found, allowing users to access the precise data they need efficiently.

It's also possible to combine keyword search with semantic search to get the best of both worlds. See Hybrid search for more details.

For an in-depth guide to Postgres' full-text search, including how to store, index, and query records, see Full text search.

---

## Video Search with Mixpeek Multimodal Embeddings | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/mixpeek-video-search

**Contents:**
- Video Search with Mixpeek Multimodal Embeddings
- Implement video search with the Mixpeek Multimodal Embed API and Supabase Vector.
- Create a new Python project with Poetry#
- Setup Supabase project#
- Install the dependencies#
- Import the necessary dependencies#
- Create embeddings for your videos#
- Perform a video search from a text query#
- Conclusion#

Video Search with Mixpeek Multimodal Embeddings

Implement video search with the Mixpeek Multimodal Embed API and Supabase Vector.

The Mixpeek Embed API allows you to generate embeddings for various types of content, including videos and text. You can use these embeddings for:

This guide demonstrates how to implement video search using Mixpeek Embed for video processing and embedding, and Supabase Vector for storing and querying embeddings.

Poetry provides packaging and dependency management for Python. If you haven't already, install poetry via pip:

Then initialize a new project:

If you haven't already, install the Supabase CLI, then initialize Supabase in the root of your newly created poetry project:

Next, start your local Supabase stack:

This will start up the Supabase stack locally and print out a bunch of environment details, including your local DB URL. Make a note of that for later use.

Add the following dependencies to your project:

At the top of your main Python script, import the dependencies and store your environment variables:

Next, create a seed method, which will create a new Supabase table, generate embeddings for your video chunks, and insert the embeddings into your database:

Add this method as a script in your pyproject.toml file:

After activating the virtual environment with poetry shell, you can now run your seed script via poetry run seed. You can inspect the generated embeddings in your local database by visiting the local Supabase dashboard at localhost:54323.

With Supabase Vector, you can query your embeddings. You can use either a video clip as search input or alternatively, you can generate an embedding from a string input and use that as the query input:

This query will return the top 5 most similar video chunks from your database.

You can now test it out by running poetry run search, and you will be presented with the most relevant video chunks to the query "a car chase scene".

With just a couple of Python scripts, you are able to implement video search as well as reverse video search using Mixpeek Embed and Supabase Vector. This approach allows for powerful semantic search capabilities that can be integrated into various applications, enabling you to search through video content using both text and video queries.

**Examples:**

Example 1 (unknown):
```unknown
1pip install poetry
```

Example 2 (unknown):
```unknown
1poetry new video-search
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1supabase start
```

---

## Structured and Unstructured | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/structured-unstructured

**Contents:**
- Structured and Unstructured
- Supabase is flexible enough to associate structured and unstructured metadata with embeddings.
- Structured#
- Unstructured#
- Hybrid#
- Choosing the right model#

Structured and Unstructured

Supabase is flexible enough to associate structured and unstructured metadata with embeddings.

Most vector stores treat metadata associated with embeddings like NoSQL, unstructured data. Supabase is flexible enough to store unstructured and structured metadata.

Notice that we've associated two pieces of metadata, content and url, with the embedding. Those fields can be filtered, constrained, indexed, and generally operated on using the full power of SQL. Structured metadata fits naturally with a traditional Supabase application, and can be managed via database migrations.

An unstructured approach does not specify the metadata fields that are expected. It stores all metadata in a flexible json/jsonb column. The tradeoff is that the querying/filtering capabilities of a schemaless data type are less flexible than when each field has a dedicated column. It also pushes the burden of metadata data integrity onto application code, which is more error prone than enforcing constraints in the database.

The unstructured approach is recommended:

Client libraries like python's vecs use this structure. For example, running:

automatically creates the unstructured SQL table during the call to get_or_create_collection.

Note that when working with client libraries that emit SQL DDL, like create table ..., you should add that SQL to your migrations when moving to production to maintain a single source of truth for your database's schema.

The structured metadata style is recommended when the fields being tracked are known in advance. If you have a combination of known and unknown metadata fields, you can accommodate the unknown fields by adding a json/jsonb column to the table. In that situation, known fields should continue to use dedicated columns for best query performance and throughput.

Both approaches create a table where you can store your embeddings and some metadata. You should choose the best approach for your use-case. In summary:

Both approaches are valid, and the one you should choose depends on your use-case.

**Examples:**

Example 1 (unknown):
```unknown
1create table docs (2  id uuid primary key,3  embedding extensions.vector(3),4  content text,5  url text6);78insert into docs9  (id, embedding, content, url)10values11  ('79409372-7556-4ccc-ab8f-5786a6cfa4f7', array[0.1, 0.2, 0.3], 'Hello world', '/hello-world');
```

Example 2 (unknown):
```unknown
1create table docs (2  id uuid primary key,3  embedding extensions.vector(3),4  meta jsonb5);67insert into docs8  (id, embedding, meta)9values10  (11    '79409372-7556-4ccc-ab8f-5786a6cfa4f7',12    array[0.1, 0.2, 0.3],13    '{"content": "Hello world", "url": "/hello-world"}'14  );
```

Example 3 (unknown):
```unknown
1#!/usr/bin/env python32import vecs34# In practice, do not hard-code your password. Use environment variables.5DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"67# create vector store client8vx = vecs.create_client(DB_CONNECTION)910docs = vx.get_or_create_collection(name="docs", dimension=1536)1112docs.upsert(vectors=[13  ('79409372-7556-4ccc-ab8f-5786a6cfa4f7', [100, 200, 300], { url: '/hello-world' })14])
```

Example 4 (unknown):
```unknown
1create table docs (2  id uuid primary key,3  embedding extensions.vector(3),4  content text,5  url string,6  meta jsonb7);89insert into docs10  (id, embedding, content, url, meta)11values12  (13    '79409372-7556-4ccc-ab8f-5786a6cfa4f7',14    array[0.1, 0.2, 0.3],15    'Hello world',16    '/hello-world',17    '{"key": "value"}'18  );
```

---

## Metadata | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/python/metadata

**Contents:**
- Metadata
- Types#
- Metadata Query Language#
  - Comparison Operators#
  - Logical Operators#
  - Performance#
  - Examples#

vecs allows you to associate key-value pairs of metadata with indexes and ids in your collections. You can then add filters to queries that reference the metadata metadata.

Metadata is stored as binary JSON. As a result, allowed metadata types are drawn from JSON primitive types.

The technical limit of a metadata field associated with a vector is 1GB. In practice you should keep metadata fields as small as possible to maximize performance.

The metadata query language is based loosely on mongodb's selectors.

vecs currently supports a subset of those operators.

Comparison operators compare a provided value with a value stored in metadata field of the vector store.

Logical operators compose other operators, and can be nested.

For best performance, use scalar key-value pairs for metadata and prefer $eq, $and and $or filters where possible. Those variants are most consistently able to make use of indexes.

year equals 2020 or gross greater than or equal to 5000.0

last_name is less than "Brown" and is_priority_customer is true

priority contained by ["enterprise", "pro"]

tags, an array, contains the string "important"

**Examples:**

Example 1 (unknown):
```unknown
1{"year": {"$eq": 2020}}
```

Example 2 (unknown):
```unknown
1{2    "$or": [3        {"year": {"$eq": 2020}},4        {"gross": {"$gte": 5000.0}}5    ]6}
```

Example 3 (unknown):
```unknown
1{2    "$and": [3        {"last_name": {"$lt": "Brown"}},4        {"is_priority_customer": {"$gte": 5000.00}}5    ]6}
```

Example 4 (unknown):
```unknown
1{2    "priority": {"$in": ["enterprise", "pro"]}3}
```

---

## Hybrid search | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/hybrid-search

**Contents:**
- Hybrid search
- Combine keyword search with semantic search.
- Use cases for hybrid search#
- When to consider hybrid search#
- How to combine search methods#
- Reciprocal Ranked Fusion (RRF)#
  - Smoothing constant k#
- Hybrid search in Postgres#
- Running hybrid search#
- See also#

Combine keyword search with semantic search.

Hybrid search combines full text search (searching by keyword) with semantic search (searching by meaning) to identify results that are both directly and contextually relevant to the user's query.

Sometimes a single search method doesn't quite capture what a user is really looking for. For example, if a user searches for "Italian recipes with tomato sauce" on a cooking app, a keyword search would pull up recipes that specifically mention "Italian," "recipes," and "tomato sauce" in the text. However, it might miss out on dishes that are quintessentially Italian and use tomato sauce but don't explicitly label themselves with these words, or use variations like "pasta sauce" or "marinara." On the other hand, a semantic search might understand the culinary context and find recipes that match the intent, such as a traditional "Spaghetti Marinara," even if they don't match the exact keyword phrase. However, it could also suggest recipes that are contextually related but not what the user is looking for, like a "Mexican salsa" recipe, because it understands the context to be broadly about tomato-based sauces.

Hybrid search combines the strengths of both these methods. It would ensure that recipes explicitly mentioning the keywords are prioritized, thus capturing direct hits that satisfy the keyword criteria. At the same time, it would include recipes identified through semantic understanding as being related in meaning or context, like different Italian dishes that traditionally use tomato sauce but might not have been tagged explicitly with the user's search terms. It identifies results that are both directly and contextually relevant to the user's query while ideally minimizing misses and irrelevant suggestions.

The decision to use hybrid search depends on what your users are looking for in your app. For a code repository where developers need to find exact lines of code or error messages, keyword search is likely ideal because it matches specific terms. In a mental health forum where users search for advice or experiences related to their feelings, semantic search may be better because it finds results based on the meaning of a query, not just specific words. For a shopping app where customers might search for specific product names yet also be open to related suggestions, hybrid search combines the best of both worlds - finding exact matches while also uncovering similar products based on the shopping context.

Hybrid search merges keyword search and semantic search, but how does this process work?

First, each search method is executed separately. Keyword search, which involves searching by specific words or phrases present in the content, will yield its own set of results. Similarly, semantic search, which involves understanding the context or meaning behind the search query rather than the specific words used, will generate its own unique results.

Now with these separate result lists available, the next step is to combine them into a single, unified list. This is achieved through a process known as “fusion”. Fusion takes the results from both search methods and merges them together based on a certain ranking or scoring system. This system may prioritize certain results based on factors like their relevance to the search query, their ranking in the individual lists, or other criteria. The result is a final list that integrates the strengths of both keyword and semantic search methods.

One of the most common fusion methods is Reciprocal Ranked Fusion (RRF). The key idea behind RRF is to give more weight to the top-ranked items in each individual result list when building the final combined list.

In RRF, we iterate over each record and assign a score (noting that each record could exist in one or both lists). The score is calculated as 1 divided by that record's rank in each list, summed together between both lists. For example, if a record with an ID of 123 was ranked third in the keyword search and ninth in semantic search, it would receive a score of 13+19=0.444\dfrac{1}{3} + \dfrac{1}{9} = 0.44431​+91​=0.444. If the record was found in only one list and not the other, it would receive a score of 0 for the other list. The records are then sorted by this score to create the final list. The items with the highest scores are ranked first, and lowest scores ranked last.

This method ensures that items that are ranked high in multiple lists are given a high rank in the final list. It also ensures that items that are ranked high in only a few lists but low in others are not given a high rank in the final list. Placing the rank in the denominator when calculating score helps penalize the low ranking records.

To prevent extremely high scores for items that are ranked first (since we're dividing by the rank), a k constant is often added to the denominator to smooth the score:

1k+rank\dfrac{1}{k+rank}k+rank1​

This constant can be any positive number, but is typically small. A constant of 1 would mean that a record ranked first would have a score of 11+1=0.5\dfrac{1}{1+1} = 0.51+11​=0.5 instead of 111. This adjustment can help balance the influence of items that are ranked very high in individual lists when creating the final combined list.

Let's implement hybrid search in Postgres using tsvector (keyword search) and pgvector (semantic search).

First we'll create a documents table to store the documents that we will search over. This is just an example - adjust this to match the structure of your application.

The table contains 4 columns:

Next we'll create indexes on the fts and embedding columns so that their individual queries will remain fast at scale:

For full text search we use a generalized inverted (GIN) index which is designed for handling composite values like those stored in a tsvector.

For semantic vector search we use an HNSW index, which is a high performing approximate nearest neighbor (ANN) search algorithm. Note that we are using the vector_ip_ops (inner product) operator with this index because we plan on using the inner product (<#>) operator later in our query. If you plan to use a different operator like cosine distance (<=>), be sure to update the index accordingly. For more information, see distance operators.

Finally we'll create our hybrid_search function:

Let's break this down:

Parameters: The function accepts quite a few parameters, but the main (required) ones are query_text, query_embedding, and match_count.

The other parameters are optional, but give more control over the fusion process.

Return type: The function returns a set of records from our documents table.

CTE: We create two common table expressions (CTE), one for full-text search and one for semantic search. These perform each query individually prior to joining them.

RRF: The final query combines the results from the two CTEs using reciprocal rank fusion (RRF).

To use this function in SQL, we can run:

In practice, you will likely be calling this from the Supabase client or through a custom backend layer. Here is a quick example of how you might call this from an Edge Function using JavaScript:

This uses OpenAI's text-embedding-3-large model to generate embeddings (shortened to 512 dimensions for faster retrieval). Swap in your preferred embedding model (and dimension size) accordingly.

To test this, make a POST request to the function's endpoint while passing in a JSON payload containing the user's query. Here is an example POST request using cURL:

For more information on how to create, test, and deploy edge functions, see Getting started.

**Examples:**

Example 1 (unknown):
```unknown
1create table documents (2  id bigint primary key generated always as identity,3  content text,4  fts tsvector generated always as (to_tsvector('english', content)) stored,5  embedding extensions.vector(512)6);
```

Example 2 (unknown):
```unknown
1-- Create an index for the full-text search2create index on documents using gin(fts);34-- Create an index for the semantic vector search5create index on documents using hnsw (embedding vector_ip_ops);
```

Example 3 (unknown):
```unknown
1create or replace function hybrid_search(2  query_text text,3  query_embedding extensions.vector(512),4  match_count int,5  full_text_weight float = 1,6  semantic_weight float = 1,7  rrf_k int = 508)9returns setof documents10language sql11as $$12with full_text as (13  select14    id,15    -- Note: ts_rank_cd is not indexable but will only rank matches of the where clause16    -- which shouldn't be too big17    row_number() over(order by ts_rank_cd(fts, websearch_to_tsquery(query_text)) desc) as rank_ix18  from19    documents20  where21    fts @@ websearch_to_tsquery(query_text)22  order by rank_ix23  limit least(match_count, 30) * 224),25semantic as (26  select27    id,28    row_number() over (order by embedding <#> query_embedding) as rank_ix29  from30    documents31  order by rank_ix32  limit least(match_count, 30) * 233)34select35  documents.*36from37  full_text38  full outer join semantic39    on full_text.id = semantic.id40  join documents41    on coalesce(full_text.id, semantic.id) = documents.id42order by43  coalesce(1.0 / (rrf_k + full_text.rank_ix), 0.0) * full_text_weight +44  coalesce(1.0 / (rrf_k + semantic.rank_ix), 0.0) * semantic_weight45  desc46limit47  least(match_count, 30)48$$;
```

Example 4 (unknown):
```unknown
1select2  *3from4  hybrid_search(5    'Italian recipes with tomato sauce', -- user query6    '[...]'::extensions.vector(512), -- embedding generated from user query7    108  );
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-vanity-subdomain-config

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

**URL:** https://supabase.com/docs/reference/api/v1-get-available-regions

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

## Image Search with OpenAI CLIP | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/image-search-openai-clip

**Contents:**
- Image Search with OpenAI CLIP
- Implement image search with the OpenAI CLIP Model and Supabase Vector.
- Create a new Python project with Poetry#
- Setup Supabase project#
- Install the dependencies#
- Import the necessary dependencies#
- Create embeddings for your images#
- Perform an image search from a text query#
- Conclusion#

Image Search with OpenAI CLIP

Implement image search with the OpenAI CLIP Model and Supabase Vector.

The OpenAI CLIP Model was trained on a variety of (image, text)-pairs. You can use the CLIP model for:

SentenceTransformers provides models that allow you to embed images and text into the same vector space. You can use this to find similar images as well as to implement image search.

You can find the full application code as a Python Poetry project on GitHub.

Poetry provides packaging and dependency management for Python. If you haven't already, install poetry via pip:

Then initialize a new project:

If you haven't already, install the Supabase CLI, then initialize Supabase in the root of your newly created poetry project:

Next, start your local Supabase stack:

This will start up the Supabase stack locally and print out a bunch of environment details, including your local DB URL. Make a note of that for later user.

We will need to add the following dependencies to our project:

At the top of your main python script, import the dependencies and store your DB URL from above in a variable:

In the root of your project, create a new folder called images and add some images. You can use the images from the example project on GitHub or you can find license free images on Unsplash.

Next, create a seed method, which will create a new Supabase Vector Collection, generate embeddings for your images, and upsert the embeddings into your database:

Add this method as a script in your pyproject.toml file:

After activating the virtual environment with poetry shell you can now run your seed script via poetry run seed. You can inspect the generated embeddings in your local database by visiting the local Supabase dashboard at localhost:54323, selecting the vecs schema, and the image_vectors database.

With Supabase Vector we can query our embeddings. We can use either an image as search input or alternative we can generate an embedding from a string input and use that as the query input:

By limiting the query to one result, we can show the most relevant image to the user. Finally we use matplotlib to show the image result to the user.

Go ahead and test it out by running poetry run search and you will be presented with an image of a "bike in front of a red brick wall".

With just a couple of lines of Python you are able to implement image search as well as reverse image search using OpenAI's CLIP model and Supabase Vector.

**Examples:**

Example 1 (unknown):
```unknown
1pip install poetry
```

Example 2 (unknown):
```unknown
1poetry new image-search
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1supabase start
```

---

## Choosing a Client | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/python-clients

**Contents:**
- Choosing a Client

As described in Structured & Unstructured Embeddings, AI workloads come in many forms.

For data science or ephemeral workloads, the Supabase Vecs client gets you started quickly. All you need is a connection string and vecs handles setting up your database to store and query vectors with associated metadata.

Click Connect at the top of any project page to get your connection string.

Copy the URI from the Shared pooler option.

For production python applications with version controlled migrations, we recommend adding first class vector support to your toolchain by registering the vector type with your ORM. pgvector provides bindings for the most commonly used SQL drivers/libraries including Django, SQLAlchemy, SQLModel, psycopg, asyncpg and Peewee.

---

## Vector indexes | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/vector-indexes

**Contents:**
- Vector indexes
- Choosing an index#
- Distance operators#
- Resources#

Once your vector table starts to grow, you will likely want to add an index to speed up queries. Without indexes, you'll be performing a sequential scan which can be a resource-intensive operation when you have many records.

Today pgvector supports two types of indexes:

In general we recommend using HNSW because of its performance and robustness against changing data.

Indexes can be used to improve performance of nearest neighbor search using various distance measures. pgvector includes 3 distance operators:

For pgvector versions 0.7.0 and above, it's possible to create indexes on vectors with the following maximum dimensions:

You can check your current pgvector version by running: SELECT * FROM pg_extension WHERE extname = 'vector'; or by navigating to the Extensions tab in your Supabase project dashboard.

If you are on an earlier version of pgvector, you should upgrade your project here.

Read more about indexing on pgvector's GitHub page.

---

## Adding generative Q&A for your documentation | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/headless-vector-search

**Contents:**
- Adding generative Q&A for your documentation
- Learn how to build a ChatGPT-style doc search powered using our headless search toolkit.
- Tech stack#
- Toolkit#
- Usage#
  - Prepare your database#
  - Ingest your documentation#
  - Add a search interface#
- Resources#

Adding generative Q&A for your documentation

Learn how to build a ChatGPT-style doc search powered using our headless search toolkit.

Supabase provides a Headless Search Toolkit for adding "Generative Q&A" to your documentation. The toolkit is "headless", so that you can integrate it into your existing website and style it to match your website theme.

You can see how this works with the Supabase docs. Just hit cmd+k and "ask" for something like "what are the features of Supabase?". You will see that the response is streamed back, using the information provided in the docs:

This toolkit consists of 2 parts:

There are 3 steps to build similarity search inside your documentation:

To prepare, create a new Supabase project and store the database and API credentials, which you can find in the project settings.

Now we can use the Headless Vector Search instructions to set up the database:

Now we need to push your documentation into the database as embeddings. You can do this manually, but to make it easier we've created a GitHub Action which can update your database every time there is a Pull Request.

In your knowledge base repository, create a new action called .github/workflows/generate_embeddings.yml with the following content:

Make sure to choose the latest version, and set your SUPABASE_SERVICE_ROLE_KEY and OPENAI_API_KEY as repository secrets in your repo settings (settings > secrets > actions).

Now inside your docs, you need to create a search interface. Because this is a headless interface, you can use it with any language. The only requirement is that you send the user query to the query Edge Function, which will stream an answer back from OpenAI. It might look something like this:

**Examples:**

Example 1 (unknown):
```unknown
1name: 'generate_embeddings'2on: # run on main branch changes3  push:4    branches:5      - main67jobs:8  generate:9    runs-on: ubuntu-latest10    steps:11      - uses: actions/checkout@v312      - uses: supabase/embeddings-generator@v0.0.x # Update this to the latest version.13        with:14          supabase-url: 'https://your-project-ref.supabase.co' # Update this to your project URL.15          supabase-service-role-key: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}16          openai-key: ${{ secrets.OPENAI_API_KEY }}17          docs-root-path: 'docs' # the path to the root of your md(x) files
```

Example 2 (javascript):
```javascript
1const onSubmit = (e: Event) => {2  e.preventDefault()3  answer.value = ""4  isLoading.value = true56  const query = new URLSearchParams({ query: inputRef.current!.value })7  const projectUrl = `https://your-project-ref.supabase.co/functions/v1`8  const queryURL = `${projectURL}/${query}`9  const eventSource = new EventSource(queryURL)1011  eventSource.addEventListener("error", (err) => {12    isLoading.value = false13    console.error(err)14  })1516  eventSource.addEventListener("message", (e: MessageEvent) => {17    isLoading.value = false1819    if (e.data === "[DONE]") {20      eventSource.close()21      return22    }2324    const completionResponse: CreateCompletionResponse = JSON.parse(e.data)25    const text = completionResponse.choices[0].text2627    answer.value += text28  });2930  isLoading.value = true31}
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-vanity-subdomains

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

## Manage Custom Domain usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/custom-domains

**Contents:**
- Manage Custom Domain usage
- What you are charged for#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Pricing#
- Billing examples#
  - One project#
  - Multiple projects#
- Optimize usage#

Manage Custom Domain usage

You can configure a custom domain for a project by enabling the Custom Domain add-on. You are charged for all custom domains configured across your projects.

Custom domains are charged by the hour, meaning you are charged for the exact number of hours that a custom domain is active. If a custom domain is active for part of an hour, you are still charged for the full hour.

Your billing cycle runs from January 1 to January 31. On January 10 at 4:30 PM, you activate a custom domain for your project. At the end of the billing cycle you are billed for 512 hours.

Usage is shown as "Custom Domain Hours" on your invoice.

$0.0137 per hour ($10 per month).

The project has a custom domain activated throughout the entire billing cycle.

All projects have a custom domain activated throughout the entire billing cycle.

---

## Hugging Face Inference API | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/hugging-face

**Contents:**
- Hugging Face Inference API
- AI tasks#
  - Natural language#
  - Computer vision#
  - Audio#
- Access token#
- Edge Functions#
- Next steps#
- Resources#

Hugging Face Inference API

Hugging Face is an open source hub for AI/ML models and tools. With over 100,000 machine learning models available, Hugging Face provides a great way to integrate specialized AI & ML tasks into your application.

There are 3 ways to use Hugging Face models in your application:

Below are some of the types of tasks you can perform with Hugging Face:

See a full list of tasks.

First generate a Hugging Face access token for your app:

https://huggingface.co/settings/tokens

Name your token based on the app its being used for and the environment. For example, if you are building an image generation app you might create 2 tokens:

Since we will be using this token for the inference API, choose the read role.

Though it is possible to use the Hugging Face inference API today without an access token, you may be rate limited.

To ensure you don't experience any unexpected downtime or errors, we recommend creating an access token.

Edge Functions are server-side TypeScript functions that run on-demand. Since Edge Functions run on a server, you can safely give them access to your Hugging Face access token.

You will need the supabase CLI installed for the following commands to work.

To create a new Edge Function, navigate to your local project and initialize Supabase if you haven't already:

Then create an Edge Function:

Create a file called .env.local to store your Hugging Face access token:

Let's modify the Edge Function to import Hugging Face's inference client and perform a text-to-image request:

This function creates a new instance of HfInference using the HUGGING_FACE_ACCESS_TOKEN environment variable.

It expects a POST request that includes a JSON request body. The JSON body should include a parameter called prompt that represents the text-to-image prompt that we will pass to Hugging Face's inference API.

Next we call textToImage(), passing in the user's prompt along with the model that we would like to use for the image generation. Today Hugging Face recommends stabilityai/stable-diffusion-2, but you can change this to any other text-to-image model. You can see a list of which models are supported for each task by navigating to their models page and filtering by task.

We set use_cache to false so that repeat queries with the same prompt will produce new images. If the task and model you are using is deterministic (will always produce the same result based on the same input), consider setting use_cache to true for faster responses.

The image result returned from the API will be a Blob. We can pass the Blob directly into a new Response() which will automatically set the content type and body of the response from the image.

Finally let's serve the Edge Function locally to test it:

Remember to pass in the .env.local file using the --env-file parameter so that the Edge Function can access the HUGGING_FACE_ACCESS_TOKEN.

For demo purposes we set --no-verify-jwt to make it easy to test the Edge Function without passing in a JWT token. In a real application you will need to pass the JWT as a Bearer token in the Authorization header.

At this point, you can make an API request to your Edge Function using your preferred frontend framework (Next.js, React, Expo, etc). We can also test from the terminal using curl:

In this example, your generated image will save to result.jpg:

You can now create an Edge Function that invokes a Hugging Face task using your model of choice.

Try running some other AI tasks.

**Examples:**

Example 1 (unknown):
```unknown
1supabase init
```

Example 2 (unknown):
```unknown
1supabase functions new text-to-image
```

Example 3 (unknown):
```unknown
1HUGGING_FACE_ACCESS_TOKEN=<your-token-here>
```

Example 4 (python):
```python
1import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'2import { HfInference } from 'https://esm.sh/@huggingface/inference@2.3.2'34const hf = new HfInference(Deno.env.get('HUGGING_FACE_ACCESS_TOKEN'))56serve(async (req) => {7  const { prompt } = await req.json()89  const image = await hf.textToImage(10    {11      inputs: prompt,12      model: 'stabilityai/stable-diffusion-2',13    },14    {15      use_cache: false,16    }17  )1819  return new Response(image)20})
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-vanity-subdomains-delete

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

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-domains-reverify

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

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-domains-get

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

## Log Drains | Supabase Docs

**URL:** https://supabase.com/docs/guides/telemetry/log-drains

**Contents:**
- Log Drains
- Supported destinations
- Generic HTTP endpoint#
- DataDog logs#
- Loki#
- Sentry#
- Pricing#

Log drains will send all logs of the Supabase stack to one or more desired destinations. It is only available for customers on Team and Enterprise Plans. Log drains is available in the dashboard under Project Settings > Log Drains.

You can read about the initial announcement here and vote for your preferred drains in this discussion.

The following table lists the supported destinations and the required setup configuration:

HTTP requests are batched with a max of 250 logs or 1 second intervals, whichever happens first. Logs are compressed via Gzip if the destination supports it.

Logs are sent as a POST request with a JSON body. Both HTTP/1 and HTTP/2 protocols are supported. Custom headers can optionally be configured for all requests.

Note that requests are unsigned.

Unsigned requests to HTTP endpoints are temporary and all requests will signed in the near future.

Logs sent to DataDog have the name of the log source set on the service field of the event and the source set to Supabase. Logs are gzipped before they are sent to DataDog.

The payload message is a JSON string of the raw log event, prefixed with the event timestamp.

To setup DataDog log drain, generate a DataDog API key here and the location of your DataDog site.

If you are interested in other log drains, upvote them here

Logs sent to the Loki HTTP API are specifically formatted according to the HTTP API requirements. See the official Loki HTTP API documentation for more details.

Events are batched with a maximum of 250 events per request.

The log source and product name will be used as stream labels.

The event_message and timestamp fields will be dropped from the events to avoid duplicate data.

Loki must be configured to accept structured metadata, and it is advised to increase the default maximum number of structured metadata fields to at least 500 to accommodate large log event payloads of different products.

Logs are sent to Sentry as part of Sentry's Logging Product. Ingesting Supabase logs as Sentry errors is currently not supported.

To setup the Sentry log drain, you need to do the following:

All fields from the log event are attached as attributes to the Sentry log, which can be used for filtering and grouping in the Sentry UI. There are no limits to cardinality or the number of attributes that can be attached to a log.

If you are self-hosting Sentry, Sentry Logs are only supported in self-hosted version 25.9.0 and later.

For a detailed breakdown of how charges are calculated, refer to Manage Log Drain usage.

---

## Going to Production | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/going-to-prod

**Contents:**
- Going to Production
- Going to production checklist for AI applications.
- Do you need indexes?#
- HNSW vs IVFFlat indexes#
- HNSW, understanding ef_construction, ef_search, and m#
- IVFFlat, understanding probes and lists#
- Performance tips when using indexes#
- Going into production#
- Useful links#

Going to production checklist for AI applications.

This guide will help you to prepare your application for production. We'll provide actionable steps to help you scale your application, ensure that it is reliable, can handle the load, and provide optimal accuracy for your use case.

See our Engineering for Scale guide for more information about engineering at scale.

Sequential scans will result in significantly higher latencies and lower throughput, guaranteeing 100% accuracy and not being RAM bound.

There are a couple of cases where you might not need indexes:

You don't have to create indexes in these cases and can use sequential scans instead. This type of workload will not be RAM bound and will not require any additional resources but will result in higher latencies and lower throughput. Extra CPU cores may help to improve queries per second, but it will not help to improve latency.

On the other hand, if you need to scale your application, you will need to create indexes. This will result in lower latencies and higher throughput, but will require additional RAM to make use of Postgres Caching. Also, using indexes will result in lower accuracy, since you are replacing exact (KNN) search with approximate (ANN) search.

pgvector supports two types of indexes: HNSW and IVFFlat. We recommend using HNSW because of its performance and robustness against changing data.

Index build parameters:

m is the number of bi-directional links created for every new element during construction. Higher m is suitable for datasets with high dimensionality and/or high accuracy requirements. Reasonable values for m are between 2 and 100. Range 12-48 is a good starting point for most use cases (16 is the default value).

ef_construction is the size of the dynamic list for the nearest neighbors (used during the construction algorithm). Higher ef_construction will result in better index quality and higher accuracy, but it will also increase the time required to build the index. ef_construction has to be at least 2 * m (64 is the default value). At some point, increasing ef_construction does not improve the quality of the index. You can measure accuracy when ef_search=ef_construction: if accuracy is lower than 0.9, then there is room for improvement.

Indexes used for approximate vector similarity search in pgvector divides a dataset into partitions. The number of these partitions is defined by the lists constant. The probes controls how many lists are going to be searched during a query.

The values of lists and probes directly affect accuracy and queries per second (QPS).

You can find more examples of how lists and probes constants affect accuracy and QPS in pgvector 0.4.0 performance blogpost.

First, a few generic tips which you can pick and choose from:

Don't forget to check out the general Production Checklist to ensure your project is secure, performant, and will remain available for your users.

You can look at our Choosing Compute Add-on guide to get a basic understanding of how much compute you might need for your workload.

Or take a look at our pgvector 0.5.0 performance and pgvector 0.4.0 performance blog posts to see what pgvector is capable of and how the above technique can be used to achieve the best results.

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-vanity-subdomains-get

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

## Generating OpenAI GPT3 completions | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/openai

**Contents:**
- Generating OpenAI GPT3 completions
- Generate GPT text completions using OpenAI and Supabase Edge Functions.
- Setup Supabase project#
- Create edge function#
- Create OpenAI key#
- Run locally#
- Deploy#
- Go deeper#

Generating OpenAI GPT3 completions

Generate GPT text completions using OpenAI and Supabase Edge Functions.

OpenAI provides a completions API that allows you to use their generative GPT models in your own applications.

OpenAI's API is intended to be used from the server-side. Supabase offers Edge Functions to make it easy to interact with third party APIs like OpenAI.

If you haven't already, install the Supabase CLI and initialize your project:

Scaffold a new edge function called openai by running:

A new edge function will now exist under ./supabase/functions/openai/index.ts.

We'll design the function to take your user's query (via POST request) and forward it to OpenAI's API.

Note that we are setting stream to false which will wait until the entire response is complete before returning. If you wish to stream GPT's response word-by-word back to your client, set stream to true.

You may have noticed we were passing OPENAI_API_KEY in the Authorization header to OpenAI. To generate this key, go to https://platform.openai.com/account/api-keys and create a new secret key.

After getting the key, copy it into a new file called .env.local in your ./supabase folder:

Serve the edge function locally by running:

Notice how we are passing in the .env.local file.

Use cURL or Postman to make a POST request to http://localhost:54321/functions/v1/openai.

You should see a GPT response come back from OpenAI!

Deploy your function to the cloud by running:

If you're interesting in learning how to use this to build your own ChatGPT, read the blog post and check out the video:

**Examples:**

Example 1 (unknown):
```unknown
1supabase init
```

Example 2 (unknown):
```unknown
1supabase functions new openai
```

Example 3 (python):
```python
1import OpenAI from 'https://deno.land/x/openai@v4.24.0/mod.ts'23Deno.serve(async (req) => {4  const { query } = await req.json()5  const apiKey = Deno.env.get('OPENAI_API_KEY')6  const openai = new OpenAI({7    apiKey: apiKey,8  })910  // Documentation here: https://github.com/openai/openai-node11  const chatCompletion = await openai.chat.completions.create({12    messages: [{ role: 'user', content: query }],13    // Choose model from here: https://platform.openai.com/docs/models14    model: 'gpt-3.5-turbo',15    stream: false,16  })1718  const reply = chatCompletion.choices[0].message.content1920  return new Response(reply, {21    headers: { 'Content-Type': 'text/plain' },22  })23})
```

Example 4 (unknown):
```unknown
1OPENAI_API_KEY=your-key-here
```

---

## Custom Domains | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/custom-domains

**Contents:**
- Custom Domains
- Custom domains#
  - Limitations#
  - Configure a custom domain using the Supabase dashboard#
  - Configure a custom domain using the Supabase CLI#
  - Add a CNAME record#
  - Verify ownership of the domain#
  - Verify your domain#
  - Prepare to activate your domain#
  - Activate your domain#

Custom domains allow you to present a branded experience to your users. These are available as a paid add-on for projects on a paid plan.

There are two types of domains supported by Supabase:

You can choose either a custom domain or vanity subdomain for each project.

Custom domains change the way your project's URLs appear to your users. This is useful when:

Custom domains help you keep your APIs portable for the long term. By using a custom domain you can migrate from one Supabase project to another, or make it easier to version APIs in the future.

Follow the Custom Domains steps in the General Settings page in the Dashboard to set up a custom domain for your project.

This example assumes your Supabase project is abcdefghijklmnopqrst with a corresponding API URL abcdefghijklmnopqrst.supabase.co and configures a custom domain at api.example.com.

You need to add a CNAME record to your domain's DNS settings to ensure your custom domain points to the Supabase project.

If your project's default domain is abcdefghijklmnopqrst.supabase.co you should:

Register your domain with Supabase to prove that you own it. You need to download two TXT records and add them to your DNS settings.

In the CLI, run domains create to register the domain and Supabase and get your verification records:

A single TXT records is returned. For example:

Add the record to your domains' DNS settings. Make sure to trim surrounding whitespace. Use a low TTL value so you can quickly change the records if you make a mistake.

Some DNS registrars automatically append your domain name to the DNS entries being created. As such, creating a DNS record for api.example.com might instead create a record for api.example.com.example.com. In such cases, remove the domain name from the records you're creating; as an example, you would create a TXT record for api, instead of api.example.com.

Make sure you've configured all required DNS settings:

Use the domains reverify command to begin the verification process of your domain. You may need to run this command a few times because DNS records take a while to propagate.

In the background, Supabase will check your DNS records and use Let's Encrypt to issue a SSL certificate for your domain. This process can take up to 30 minutes.

Before you activate your domain, prepare your applications and integrations for the domain change:

To prevent issues for your users, follow these steps:

Once you've done the necessary preparations to activate the new domain for your project, you can activate it using the domains activate CLI command.

When this step completes, Supabase will serve the requests from your new domain. The Supabase project domain continues to work and serve requests so you do not need to rush to change client code URLs.

If you wish to use the new domain in client code, change the URL used in your Supabase client libraries:

Similarly, your Edge Functions will now be available at https://api.example.com/functions/v1/your_function_name, and your Storage objects at https://api.example.com/storage/v1/object/public/your_file_path.ext.

Removing a custom domain may cause some issues when using Supabase Auth with OAuth or SAML. You may have to reverse the changes made in the Prepare to activate your domain step above.

To remove an activated custom domain you can use the domains delete CLI command.

Vanity subdomains allow you to present a basic branded experience, compared to custom domains. They allow you to host your services at a custom subdomain on Supabase (e.g., my-example-brand.supabase.co) instead of the default, randomly assigned abcdefghijklmnopqrst.supabase.co.

You can configure vanity subdomains via the CLI only.

Let's assume your Supabase project's domain is abcdefghijklmnopqrst.supabase.co and you wish to configure a vanity subdomain at my-example-brand.supabase.co.

Use the vanity-subdomains check-availability command of the CLI to check if your desired subdomain is available for use:

Before you activate your vanity subdomain, prepare your applications and integrations for the subdomain change:

To prevent issues for your users, make sure you have gone through these steps:

Once you've chosen an available subdomain and have done all the necessary preparations for it, you can reconfigure your Supabase project to start using it.

Use the vanity-subdomains activate command to activate and claim your subdomain:

If you wish to use the new domain in client code, you can set it up like so:

When using Sign in with Twitter make sure your frontend code is using the subdomain only.

Removing a subdomain may cause some issues when using Supabase Auth with OAuth or SAML. You may have to reverse the changes made in the Prepare to activate the subdomain step above.

Use the vanity-subdomains delete command of the CLI to remove the subdomain my-example-brand.supabase.co from your project.

For a detailed breakdown of how charges are calculated, refer to Manage Custom Domain usage.

**Examples:**

Example 1 (unknown):
```unknown
1supabase domains create --project-ref abcdefghijklmnopqrst --custom-hostname api.example.com
```

Example 2 (unknown):
```unknown
1[...]2Required outstanding validation records:3        _acme-challenge.api.example.com. TXT -> ca3-F1HvR9i938OgVwpCFwi1jTsbhe1hvT0Ic3efPY3Q
```

Example 3 (unknown):
```unknown
1supabase domains reverify --project-ref abcdefghijklmnopqrst
```

Example 4 (unknown):
```unknown
1supabase domains activate --project-ref abcdefghijklmnopqrst
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-vanity-subdomains-check-availability

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

**URL:** https://supabase.com/docs/reference/api/v1-deactivate-vanity-subdomain-config

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

## Indexes | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/python/indexes

**Contents:**
- Indexes

Indexes are tools for optimizing query performance of a collection.

Collections can be queried without an index, but that will emit a python warning and should never be done in production.

As each query vector must be checked against every record in the collection. When the number of dimensions and/or number of records becomes large, that becomes extremely slow and computationally expensive.

An index is a heuristic data structure that pre-computes distances between key points in the vector space. It is smaller and can be traversed more quickly than the whole collection enabling much more performant searching.

Only one index may exist per-collection. An index optimizes a collection for searching according to a selected distance measure.

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

**Examples:**

Example 1 (unknown):
```unknown
1query does not have a covering index for cosine_similarity. See Collection.create_index
```

Example 2 (unknown):
```unknown
1docs.create_index()
```

Example 3 (unknown):
```unknown
1docs.create_index(2    method=IndexMethod.hnsw,3    measure=IndexMeasure.cosine_distance,4    index_arguments=IndexArgsHNSW(m=8),5)
```

---

## Available regions | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/regions

**Contents:**
- Available regions
- General regions#
- Specific regions#

Each Supabase project is deployed to one primary region. Choose the location closest to your users for the best performance.

For most projects, we recommend choosing a general region. Supabase will deploy your project to an available AWS region within that area based on current infrastructure capacity.

Note: General regions aren’t yet supported for read replicas or management via the API.

If you prefer, you can choose an exact AWS region for your project.

---

## Building ChatGPT plugins | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/building-chatgpt-plugins

**Contents:**
- Building ChatGPT plugins
- Use Supabase as a Retrieval Store for your ChatGPT plugin.
- What is ChatGPT Retrieval Plugin?#
- Example: Chat with Postgres docs#
  - Step 1: Fork the ChatGPT Retrieval Plugin repository#
  - Step 2: Install dependencies#
  - Step 3: Create a Supabase project#
  - Step 4: Run Postgres locally#
  - Step 5: Obtain OpenAI API key#
  - Step 6: Run the plugin#

Building ChatGPT plugins

Use Supabase as a Retrieval Store for your ChatGPT plugin.

ChatGPT recently released Plugins which help ChatGPT access up-to-date information, run computations, or use third-party services. If you're building a plugin for ChatGPT, you'll probably want to answer questions from a specific source. We can solve this with “retrieval plugins”, which allow ChatGPT to access information from a database.

A Retrieval Plugin is a Python project designed to inject external data into a ChatGPT conversation. It does a few things:

It allows ChatGPT to dynamically pull relevant information into conversations from your data sources. This could be PDF documents, Confluence, or Notion knowledge bases.

Let’s build an example where we can “ask ChatGPT questions” about the Postgres documentation. Although ChatGPT already knows about the Postgres documentation because it is publicly available, this is a simple example which demonstrates how to work with PDF files.

This plugin requires several steps:

We'll be saving the Postgres documentation in Postgres, and ChatGPT will be retrieving the documentation whenever a user asks a question:

Fork the ChatGPT Retrieval Plugin repository to your GitHub account and clone it to your local machine. Read through the README.md file to understand the project structure.

Choose your desired datastore provider and remove unused dependencies from pyproject.toml. For this example, we'll use Supabase. And install dependencies with Poetry:

Create a Supabase project and database by following the instructions here. Export the environment variables required for the retrieval plugin to work:

For Postgres datastore, you'll need to export these environment variables instead:

To start quicker you may use Supabase CLI to spin everything up locally as it already includes pgvector from the start. Install supabase-cli, go to the examples/providers folder in the repo and run:

This will pull all docker images and run Supabase stack in docker on your local machine. It will also apply all the necessary migrations to set the whole thing up. You can then use your local setup the same way, just export the environment variables and follow to the next steps.

Using supabase-cli is not required and you can use any other docker image or hosted version of Postgres that includes pgvector. Just make sure you run migrations from examples/providers/supabase/migrations/20230414142107_init_pg_vector.sql.

To create embeddings Plugin uses OpenAI API and text-embedding-ada-002 model. Each time we add some data to our datastore, or try to query relevant information from it, embedding will be created either for inserted data chunk, or for the query itself. To make it work we need to export OPENAI_API_KEY. If you already have an account in OpenAI, you just need to go to User Settings - API keys and Create new secret key.

Execute the following command to run the plugin:

The plugin will start on your localhost - port :3333 by default.

For this example, we'll upload Postgres documentation to the datastore. Download the Postgres documentation and use the /upsert-file endpoint to upload it:

The plugin will split your data and documents into smaller chunks automatically. You can view the chunks using the Supabase dashboard or any other SQL client you prefer. The entire Postgres Documentation yielded 7,904 records, which is not a lot, but we can try to add index for embedding column to speed things up by a little. To do so, you should run the following SQL command:

This will create an index for the inner product distance function. Important to note that it is an approximate index. It will change the logic from performing the exact nearest neighbor search to the approximate nearest neighbor search.

We are using lists = 10, because as a general guideline, you should start looking for optimal lists constant value with the formula: rows / 1000 when you have less than 1 million records in your table.

To integrate our plugin with ChatGPT, register it in the ChatGPT dashboard. Assuming you have access to ChatGPT Plugins and plugin development, select the Plugins model in a new chat, then choose "Plugin store" and "Develop your own plugin." Enter localhost:3333 into the domain input, and your plugin is now part of ChatGPT.

You can now ask questions about Postgres and receive answers derived from the documentation.

Let's try it out: ask ChatGPT to find out when to use check and when to use using. You will be able to see what queries were sent to our plugin and what it responded to.

And after ChatGPT receives a response from the plugin it will answer your question with the data from the documentation.

**Examples:**

Example 1 (unknown):
```unknown
1poetry install
```

Example 2 (unknown):
```unknown
1export OPENAI_API_KEY=<open_ai_api_key>2export DATASTORE=supabase3export SUPABASE_URL=<supabase_url>4export SUPABASE_SERVICE_ROLE_KEY=<supabase_key>
```

Example 3 (unknown):
```unknown
1export OPENAI_API_KEY=<open_ai_api_key>2export DATASTORE=postgres3export PG_HOST=<postgres_host_url>4export PG_PASSWORD=<postgres_password>
```

Example 4 (unknown):
```unknown
1supabase start
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-domains

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

## Manage Log Drain usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/log-drains

**Contents:**
- Manage Log Drain usage
- What you are charged for#
- Log Drain Hours#
  - How charges are calculated#
    - Example#
    - Usage on your invoice#
  - Pricing#
- Log Drain Events#
  - How charges are calculated#
    - Example#

Manage Log Drain usage

You can configure log drains in the project settings to send logs to one or more destinations. You are charged for each log drain that is configured (referred to as Log Drain Hours), the log events sent (referred to as Log Drain Events), and the Egress incurred by the export—across all your projects.

You are charged by the hour, meaning you are charged for the exact number of hours that a log drain is configured for a project. If a log drain is configured for part of an hour, you are still charged for the full hour.

Your billing cycle runs from January 1 to January 31. On January 10 at 4:30 PM, you configure a log drain for your project. At the end of the billing cycle you are billed for 512 hours.

Usage is shown as "Log Drain Hours" on your invoice.

Log Drains are available as a project Add-On for all Team and Enterprise users. Each Log Drain costs $0.0822 per hour ($60 per month).

Log Drain Events are billed using Package pricing, with each package representing 1 million events. If your usage falls between two packages, you are billed for the next whole package.

Usage is shown as "Log Drain Events" on your invoice.

$0.2 per 1 million events.

The project has two log drains configured throughout the entire billing cycle with 800,000 and 1.6 million events each. In this example we assume that the organization is exceeding its Unified Egress Quota, so charges for Egress apply.

You can view Log Drain Events usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

---

## Choosing your Compute Add-on | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/choosing-compute-addon

**Contents:**
- Choosing your Compute Add-on
- Choosing the right Compute Add-on for your vector workload.
- Dimensionality#
- HNSW#
  - 384 dimensions #
  - 960 dimensions #
  - 1536 dimensions #
- IVFFlat#
  - 384 dimensions #
  - 960 dimensions #

Choosing your Compute Add-on

Choosing the right Compute Add-on for your vector workload.

You have two options for scaling your vector workload:

The number of dimensions in your embeddings is the most important factor in choosing the right Compute Add-on. In general, the lower the dimensionality the better the performance. We've provided guidance for some of the more common embedding dimensions below. For each benchmark, we used Vecs to create a collection, upload the embeddings to a single table, and create both the IVFFlat and HNSW indexes for inner-product distance measure for the embedding column. We then ran a series of queries to measure the performance of different compute add-ons:

This benchmark uses the dbpedia-entities-openai-1M dataset containing 1,000,000 embeddings of text, regenerated for 384 dimension embeddings. Each embedding is generated using gte-small.

Accuracy was 0.99 for benchmarks.

This benchmark uses the gist-960 dataset, which contains 1,000,000 embeddings of images. Each embedding is 960 dimensions.

Accuracy was 0.99 for benchmarks.

QPS can also be improved by increasing m and ef_construction. This will allow you to use a smaller value for ef_search and increase QPS.

This benchmark uses the dbpedia-entities-openai-1M dataset, which contains 1,000,000 embeddings of text. And 224,482 embeddings from Wikipedia articles for compute add-ons large and below. Each embedding is 1536 dimensions created with the OpenAI Embeddings API.

Accuracy was 0.99 for benchmarks.

QPS can also be improved by increasing m and ef_construction. This will allow you to use a smaller value for ef_search and increase QPS. For example, increasing m to 32 and ef_construction to 80 for 4XL will increase QPS to 1280.

It is possible to upload more vectors to a single table if Memory allows it (for example, 4XL plan and higher for OpenAI embeddings). But it will affect the performance of the queries: QPS will be lower, and latency will be higher. Scaling should be almost linear, but it is recommended to benchmark your workload to find the optimal number of vectors per table and per database instance.

This benchmark uses the dbpedia-entities-openai-1M dataset containing 1,000,000 embeddings of text, regenerated for 384 dimension embeddings. Each embedding is generated using gte-small.

This benchmark uses the gist-960 dataset, which contains 1,000,000 embeddings of images. Each embedding is 960 dimensions.

This benchmark uses the dbpedia-entities-openai-1M dataset, which contains 1,000,000 embeddings of text. Each embedding is 1536 dimensions created with the OpenAI Embeddings API.

For 1,000,000 vectors 10 probes results to accuracy of 0.91. And for 500,000 vectors and below 10 probes results to accuracy in the range of 0.95 - 0.99. To increase accuracy, you need to increase the number of probes.

It is possible to upload more vectors to a single table if Memory allows it (for example, 4XL plan and higher for OpenAI embeddings). But it will affect the performance of the queries: QPS will be lower, and latency will be higher. Scaling should be almost linear, but it is recommended to benchmark your workload to find the optimal number of vectors per table and per database instance.

There are various ways to improve your pgvector performance. Here are some tips:

It's useful to execute a few thousand “warm-up” queries before going into production. This helps help with RAM utilization. This can also help to determine that you've selected the right compute size for your workload.

You can increase the Requests per Second by increasing m and ef_construction or lists. This also has an important caveat: building the index takes longer with higher values for these parameters.

Check out more tips and the complete step-by-step guide in Going to Production for AI applications.

We follow techniques outlined in the ANN Benchmarks methodology. A Python test runner is responsible for uploading the data, creating the index, and running the queries. The pgvector engine is implemented using vecs, a Python client for pgvector.

Each test is run for a minimum of 30-40 minutes. They include a series of experiments executed at different concurrency levels to measure the engine's performance under different load types. The results are then averaged.

As a general recommendation, we suggest using a concurrency level of 5 or more for most workloads and 30 or more for high-load workloads.

---

## Google Colab | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/google-colab

**Contents:**
- Google Colab
- Use Google Colab to manage your Supabase Vector store.
- Create a new notebook#
- Install Vecs#
- Connect to your database#
- Create a collection#
- Query your documents#
- Resources#

Use Google Colab to manage your Supabase Vector store.

Google Colab is a hosted Jupyter Notebook service. It provides free access to computing resources, including GPUs and TPUs, and is well-suited to machine learning, data science, and education. We can use Colab to manage collections using Supabase Vecs.

In this tutorial we'll connect to a database running on the Supabase platform. If you don't already have a database, you can create one here: database.new.

Start by visiting colab.research.google.com. There you can create a new notebook.

We'll use the Supabase Vector client, Vecs, to manage our collections.

At the top of the notebook add the notebook paste the following code and hit the "execute" button (ctrl+enter):

On your project dashboard, click Connect. The connection string should look like postgres://postgres.xxxx:password@xxxx.pooler.supabase.com:6543/postgres

Create a new code block below the install block (ctrl+m b) and add the following code using the Postgres URI you copied above:

Execute the code block (ctrl+enter). If no errors were returned then your connection was successful.

Now we're going to create a new collection and insert some documents.

Create a new code block below the install block (ctrl+m b). Add the following code to the code block and execute it (ctrl+enter):

This will create a table inside your database within the vecs schema, called colab_collection. You can view the inserted items in the Table Editor, by selecting the vecs schema from the schema dropdown.

Now we can search for documents based on their similarity. Create a new code block and execute the following code:

You will see that this returns two documents in an array ['vec1', 'vec0']:

It also returns a warning:

You can lean more about creating indexes in the Vecs documentation.

**Examples:**

Example 1 (unknown):
```unknown
1pip install vecs
```

Example 2 (unknown):
```unknown
1import vecs23DB_CONNECTION = "postgres://postgres.xxxx:password@xxxx.pooler.supabase.com:6543/postgres"45# create vector store client6vx = vecs.create_client(DB_CONNECTION)
```

Example 3 (unknown):
```unknown
1collection = vx.get_or_create_collection(name="colab_collection", dimension=3)23collection.upsert(4    vectors=[5        (6         "vec0",           # the vector's identifier7         [0.1, 0.2, 0.3],  # the vector. list or np.array8         {"year": 1973}    # associated  metadata9        ),10        (11         "vec1",12         [0.7, 0.8, 0.9],13         {"year": 2012}14        )15    ]16)
```

Example 4 (unknown):
```unknown
1collection.query(2    query_vector=[0.4,0.5,0.6],  # required3    limit=5,                     # number of records to return4    filters={},                  # metadata filters5    measure="cosine_distance",   # distance measure to use6    include_value=False,         # should distance measure values be returned?7    include_metadata=False,      # should record metadata be returned?8)
```

---

## Semantic Image Search with Amazon Titan | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/examples/semantic-image-search-amazon-titan

**Contents:**
- Semantic Image Search with Amazon Titan
- Implement semantic image search with Amazon Titan and Supabase Vector in Python.
- Create a new Python project with Poetry#
- Spin up a Postgres database with pgvector#
- Install the dependencies#
- Import the necessary dependencies#
- Create embeddings for your images#
- Perform an image search from a text query#
- Conclusion#

Semantic Image Search with Amazon Titan

Implement semantic image search with Amazon Titan and Supabase Vector in Python.

Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon. Each model is accessible through a common API which implements a broad set of features to help build generative AI applications with security, privacy, and responsible AI in mind.

Amazon Titan is a family of foundation models (FMs) for text and image generation, summarization, classification, open-ended Q&A, information extraction, and text or image search.

In this guide we'll look at how we can get started with Amazon Bedrock and Supabase Vector in Python using the Amazon Titan multimodal model and the vecs client.

You can find the full application code as a Python Poetry project on GitHub.

Poetry provides packaging and dependency management for Python. If you haven't already, install poetry via pip:

Then initialize a new project:

If you haven't already, head over to database.new and create a new project. Every Supabase project comes with a full Postgres database and the pgvector extension preconfigured.

When creating your project, make sure to note down your database password as you will need it to construct the DB_URL in the next step.

You can find your database connection string on your project dashboard, click Connect. Use the Session pooler connection string which looks like this:

We will need to add the following dependencies to our project:

At the top of your main python script, import the dependencies and store your DB URL from above in a variable:

Next, get the credentials to your AWS account and instantiate the boto3 client:

In the root of your project, create a new folder called images and add some images. You can use the images from the example project on GitHub or you can find license free images on Unsplash.

To send images to the Amazon Bedrock API we need to need to encode them as base64 strings. Create the following helper methods:

Next, create a seed method, which will create a new Supabase Vector Collection, generate embeddings for your images, and upsert the embeddings into your database:

Add this method as a script in your pyproject.toml file:

After activating the virtual environment with poetry shell you can now run your seed script via poetry run seed. You can inspect the generated embeddings in your Supabase Dashboard by visiting the Table Editor, selecting the vecs schema, and the image_vectors table.

We can use Supabase Vector to query our embeddings. We can either use an image as the search input or generate an embedding from a string input:

By limiting the query to one result, we can show the most relevant image to the user. Finally we use matplotlib to show the image result to the user.

Go ahead and test it out by running poetry run search and you will be presented with an image of a "bike in front of a red brick wall".

With just a couple of lines of Python you are able to implement image search as well as reverse image search using the Amazon Titan multimodal model and Supabase Vector.

**Examples:**

Example 1 (unknown):
```unknown
1pip install poetry
```

Example 2 (unknown):
```unknown
1poetry new aws_bedrock_image_search
```

Example 3 (unknown):
```unknown
1postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

Example 4 (unknown):
```unknown
1poetry add vecs boto3 matplotlib
```

---

## Concepts | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/concepts

**Contents:**
- Concepts
- What are embeddings?#
- Human language#
- How do embeddings work?#
- Using embeddings#
- See also#

Embeddings are core to many AI and vector applications. This guide covers these concepts. If you prefer to get started right away, see our guide on Generating Embeddings.

Embeddings capture the "relatedness" of text, images, video, or other types of information. This relatedness is most commonly used for:

Let's explore an example of text embeddings. Say we have three phrases:

Your job is to group phrases with similar meaning. If you are a human, this should be obvious. Phrases 1 and 2 are almost identical, while phrase 3 has a completely different meaning.

Although phrases 1 and 2 are similar, they share no common vocabulary (besides "the"). Yet their meanings are nearly identical. How can we teach a computer that these are the same?

Humans use words and symbols to communicate language. But words in isolation are mostly meaningless - we need to draw from shared knowledge & experience in order to make sense of them. The phrase “You should Google it” only makes sense if you know that Google is a search engine and that people have been using it as a verb.

In the same way, we need to train a neural network model to understand human language. An effective model should be trained on millions of different examples to understand what each word, phrase, sentence, or paragraph could mean in different contexts.

So how does this relate to embeddings?

Embeddings compress discrete information (words & symbols) into distributed continuous-valued data (vectors). If we took our phrases from before and plot them on a chart, it might look something like this:

Phrases 1 and 2 would be plotted close to each other, since their meanings are similar. We would expect phrase 3 to live somewhere far away since it isn't related. If we had a fourth phrase, “Sally ate Swiss cheese”, this might exist somewhere between phrase 3 (cheese can go on sandwiches) and phrase 1 (mice like Swiss cheese).

In this example we only have 2 dimensions: the X and Y axis. In reality, we would need many more dimensions to effectively capture the complexities of human language.

Compared to our 2-dimensional example above, most embedding models will output many more dimensions. For example the open source gte-small model outputs 384 dimensions.

Why is this useful? Once we have generated embeddings on multiple texts, it is trivial to calculate how similar they are using vector math operations like cosine distance. A common use case for this is search. Your process might look something like this:

---
