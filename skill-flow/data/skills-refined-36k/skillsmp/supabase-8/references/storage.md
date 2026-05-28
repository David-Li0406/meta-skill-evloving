# Supabase - Storage

**Pages:** 68

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/update-properties-of-a-bucket

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/retrieve-an-object-from-a-public-bucket

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/generate-presigned-urls-to-retrieve-objects

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Bandwidth & Storage Egress | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/serving/bandwidth

**Contents:**
- Bandwidth & Storage Egress
- Bandwidth & Storage Egress
- Bandwidth & Storage egress#
  - Checking Storage egress requests in Logs Explorer#
  - Calculating egress#
  - Optimizing egress#

Bandwidth & Storage Egress

Bandwidth & Storage Egress

Free Plan Organizations in Supabase have a limit of 10 GB of bandwidth (5 GB cached + 5 GB uncached). This limit is calculated by the sum of all the data transferred from the Supabase servers to the client. This includes all the data transferred from the database, storage, and functions.

We have a template query that you can use to get the number of requests for each object in Logs Explorer.

Example of the output:

If you already know the size of those files, you can calculate the egress by multiplying the number of requests by the size of the file. You can also get the size of the file with the following cURL:

This will return the size of the file in bytes. For this example, let's say that 20230902_200037.gif has a file size of 3 megabytes and volleyball.png has a file size of 570 kilobytes.

Now, we have to sum all the egress for all the files to get the total egress:

You can see that these values can get quite large, so it's important to keep track of the egress and optimize the files.

See our scaling tips for egress.

**Examples:**

Example 1 (unknown):
```unknown
1select2  request.method as http_verb,3  request.path as filepath,4  (responseHeaders.cf_cache_status = 'HIT') as cached,5  count(*) as num_requests6from7  edge_logs8  cross join unnest(metadata) as metadata9  cross join unnest(metadata.request) as request10  cross join unnest(metadata.response) as response11  cross join unnest(response.headers) as responseHeaders12where13  (path like '%storage/v1/object/%' or path like '%storage/v1/render/%')14  and request.method = 'GET'15group by 1, 2, 316order by num_requests desc17limit 100;
```

Example 2 (unknown):
```unknown
1[2  {3    "filepath": "/storage/v1/object/sign/large%20bucket/20230902_200037.gif",4    "http_verb": "GET",5    "cached": true,6    "num_requests": 1007  },8  {9    "filepath": "/storage/v1/object/public/demob/Sports/volleyball.png",10    "http_verb": "GET",11    "cached": false,12    "num_requests": 16813  }14]
```

Example 3 (unknown):
```unknown
1curl -s -w "%{size_download}\n" -o /dev/null "https://my_project.supabase.co/storage/v1/object/large%20bucket/20230902_200037.gif"
```

Example 4 (unknown):
```unknown
1100 * 3MB = 300MB2168 * 570KB = 95.76MB3Total Egress = 395.76MB
```

---

## JavaScript: Upload a file | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/storage-from-upload

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/get-object-info

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## JavaScript: Create a bucket | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/storage-createbucket

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/delete-multiple-objects

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/generate-a-presigned-url-to-retrieve-an-object

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/delete-an-object

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Delete Objects | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/management/delete-objects

**Contents:**
- Delete Objects
- Learn about deleting objects
- Delete objects#
- RLS#

Learn about deleting objects

When you delete one or more objects from a bucket, the files are permanently removed and not recoverable. You can delete a single object or multiple objects at once.

Deleting objects should always be done via the Storage API and NOT via a SQL query. Deleting objects via a SQL query will not remove the object from the bucket and will result in the object being orphaned.

To delete one or more objects, use the remove method.

When deleting objects, there is a limit of 1000 objects at a time using the remove method.

To delete an object, the user must have the delete permission on the object. For example:

**Examples:**

Example 1 (unknown):
```unknown
1await supabase.storage.from('bucket').remove(['object-path-2', 'folder/avatar2.png'])
```

Example 2 (unknown):
```unknown
1create policy "User can delete their own objects"2on storage.objects3for delete4TO authenticated5USING (6    owner = (select auth.uid()::text)7);
```

---

## Storage CDN | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/cdn/fundamentals

**Contents:**
- Storage CDN
  - Example#
  - Public vs private buckets#

All assets uploaded to Supabase Storage are cached on a Content Delivery Network (CDN) to improve the latency for users all around the world. CDNs are a geographically distributed set of servers or nodes which cache content from an origin server. For Supabase Storage, the origin is the storage server running in the same region as your project. Aside from performance, CDNs also help with security and availability by mitigating Distributed Denial of Service (DDoS) and other application attacks.

Let's walk through an example of how a CDN helps with performance.

A new bucket is created for a Supabase project launched in Singapore. All requests to the Supabase Storage API are routed to the CDN first.

A user from the United States requests an object and is routed to the U.S. CDN. At this point, that CDN node does not have the object in its cache and pings the origin server in Singapore.

Another user, also in the United States, requests the same object and is served directly from the CDN cache in the United States instead of routing the request back to Singapore.

Note that CDNs might still evict your object from their cache if it has not been requested for a while from a specific region. For example, if no user from United States requests your object, it will be removed from the CDN cache even if we set a very long cache control duration.

The cache status of a particular request is sent in the cf-cache-status header. A cache status of MISS indicates that the CDN node did not have the object in its cache and had to ping the origin to get it. A cache status of HIT indicates that the object was sent directly from the CDN.

Objects in public buckets do not require any authorization to access objects. This leads to a better cache hit rate compared to private buckets.

For private buckets, permissions for accessing each object is checked on a per user level. For example, if two different users access the same object in a private bucket from the same region, it results in a cache miss for both the users since they might have different security policies attached to them. On the other hand, if two different users access the same object in a public bucket from the same region, it results in a cache hit for the second user.

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-storage-ls

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

**URL:** https://supabase.com/docs/reference/cli/supabase-storage-rm

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

## Storage Helper Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/schema/helper-functions

**Contents:**
- Storage Helper Functions
- Learn the storage schema
  - storage.filename()#
  - storage.foldername()#
  - storage.extension()#

Storage Helper Functions

Learn the storage schema

Supabase Storage provides SQL helper functions which you can use to write RLS policies.

Returns the name of a file. For example, if your file is stored in public/subfolder/avatar.png it would return: 'avatar.png'

This example demonstrates how you would allow any user to download a file called favicon.ico:

Returns an array path, with all of the subfolders that a file belongs to. For example, if your file is stored in public/subfolder/avatar.png it would return: [ 'public', 'subfolder' ]

This example demonstrates how you would allow authenticated users to upload files to a folder called private:

Returns the extension of a file. For example, if your file is stored in public/subfolder/avatar.png it would return: 'png'

This example demonstrates how you would allow restrict uploads to only PNG files inside a bucket called cats:

**Examples:**

Example 1 (unknown):
```unknown
1create policy "Allow public downloads"2on storage.objects3for select4to public5using (6  storage.filename(name) = 'favicon.ico'7);
```

Example 2 (unknown):
```unknown
1create policy "Allow authenticated uploads"2on storage.objects3for insert4to authenticated5with check (6  (storage.foldername(name))[1] = 'private'7);
```

Example 3 (unknown):
```unknown
1create policy "Only allow PNG uploads"2on storage.objects3for insert4to authenticated5with check (6  bucket_id = 'cats' and storage.extension(name) = 'png'7);
```

---

## Storage Image Transformations | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/serving/image-transformations

**Contents:**
- Storage Image Transformations
- Transform images with Storage
- Get a public URL for a transformed image#
- Signing URLs with transformation options#
- Downloading images#
- Automatic image optimization (WebP)#
- Next.js loader#
- Transformation options#
  - Optimizing#
  - Resizing#

Storage Image Transformations

Transform images with Storage

Supabase Storage offers the functionality to optimize and resize images on the fly. Any image stored in your buckets can be transformed and optimized for fast delivery.

Image Resizing is currently enabled for Pro Plan and above.

Our client libraries methods like getPublicUrl and createSignedUrl support the transform option. This returns the URL that serves the transformed image.

An example URL could look like this:

To share a transformed image in a private bucket for a fixed amount of time, provide the transform option when you create the signed URL:

The transformation options are embedded into the token attached to the URL — they cannot be changed once signed.

To download a transformed image, pass the transform option to the download function.

When using the image transformation API, Storage will automatically find the best format supported by the client and return that to the client, without any code change. For instance, if you use Chrome when viewing a JPEG image and using transformation options, you'll see that images are automatically optimized as webp images.

As a result, this will lower the egress that you send to your users and your application will load much faster.

We currently only support WebP. AVIF support will come in the near future.

Disabling automatic optimization:

In case you'd like to return the original format of the image and opt-out from the automatic image optimization detection, you can pass the format=origin parameter when requesting a transformed image, this is also supported in the JavaScript SDK starting from v2.2.0

You can use Supabase Image Transformation to optimize your Next.js images using a custom Loader.

To get started, create a supabase-image-loader.js file in your Next.js project which exports a default function:

In your next.config.js file add the following configuration to instruct Next.js to use our custom loader

At this point you are ready to use the Image component provided by Next.js

We currently support a few transformation options focusing on optimizing, resizing, and cropping images.

You can set the quality of the returned image by passing a value from 20 to 100 (with 100 being the highest quality) to the quality parameter. This parameter defaults to 80.

You can use width and height parameters to resize an image to a specific dimension. If only one parameter is specified, the image will be resized and cropped, maintaining the aspect ratio.

You can use different resizing modes to fit your needs, each of them uses a different approach to resize the image:

Use the resize parameter with one of the following values:

cover : resizes the image while keeping the aspect ratio to fill a given size and crops projecting parts. (default)

contain : resizes the image while keeping the aspect ratio to fit a given size.

fill : resizes the image without keeping the aspect ratio.

$5 per 1,000 origin images. You are only charged for usage exceeding your subscription plan's quota.

The count resets at the start of each billing cycle.

For a detailed breakdown of how charges are calculated, refer to Manage Storage Image Transformations usage.

Our solution to image resizing and optimization can be self-hosted as with any other Supabase product. Under the hood we use imgproxy

Deploy an imgproxy container with the following configuration:

Note: make sure that this service can only be reachable within an internal network and not exposed to the public internet

Once imgproxy is deployed we need to configure a couple of environment variables in your self-hosted storage-api service as follows:

**Examples:**

Example 1 (unknown):
```unknown
1supabase.storage.from('bucket').getPublicUrl('image.jpg', {2  transform: {3    width: 500,4    height: 600,5  },6})
```

Example 2 (unknown):
```unknown
1https://project_id.supabase.co/storage/v1/render/image/public/bucket/image.jpg?width=500&height=600`
```

Example 3 (unknown):
```unknown
1supabase.storage.from('bucket').createSignedUrl('image.jpg', 60000, {2  transform: {3    width: 200,4    height: 200,5  },6})
```

Example 4 (unknown):
```unknown
1supabase.storage.from('bucket').download('image.jpg', {2  transform: {3    width: 800,4    height: 300,5  },6})
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/retrieve-an-object-via-a-presigned-url

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-storage-mv

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

## Creating Vector Buckets | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/vector/creating-vector-buckets

**Contents:**
- Creating Vector Buckets
- Set up vector buckets and indexes using the dashboard or JavaScript SDK.
      - This feature is in alpha
- Creating a Vector bucket#
  - Using the Supabase Dashboard#
  - Using the SDK#
- Creating indexes#
  - Quick start: Creating an index via Dashboard#
  - Quick start: Creating an index via SDK#
  - Key details#

Creating Vector Buckets

Set up vector buckets and indexes using the dashboard or JavaScript SDK.

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

Vector buckets organize your vector data into logical units. Within each bucket, you create indexes that define how vectors are stored and searched based on their dimensions and distance metrics.

You can create vector buckets using either the Supabase Dashboard or the SDK.

Your vector bucket is now ready. The next step is to create indexes within it.

Indexes organize vectors within a bucket with consistent dimensions and distance metrics. For comprehensive index management documentation, see Working with Vector Indexes.

For detailed information on distance metrics, embedding dimensions, managing multiple indexes, and advanced index operations, see Working with Vector Indexes.

After creating your bucket and indexes, you can:

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabase = createClient('https://your-project.supabase.co', 'your-service-key')45// Create a vector bucket6await supabase.storage.vectors.createBucket('embeddings')78console.log('✓ Vector bucket created: embeddings')
```

Example 2 (javascript):
```javascript
1const bucket = supabase.storage.vectors.from('embeddings')23// Create an index4await bucket.createIndex({5  indexName: 'documents-openai',6  dataType: 'float32',7  dimension: 1536,8  distanceMetric: 'cosine',9})1011console.log('✓ Index created: documents-openai')
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/get-object

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## JavaScript: Create a signed URL | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/storage-from-createsignedurl

---

## Vector Bucket Limits | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/vector/limits

**Contents:**
- Vector Bucket Limits
- Understanding capacity, quotas, and billing for vector buckets.
      - This feature is in alpha
- Storage limits#

Understanding capacity, quotas, and billing for vector buckets.

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

Vector buckets have default limits during the alpha phase. These limits are designed to ensure fair resource allocation and can be adjusted on a case-by-case basis for production workloads.

---

## Storage Buckets | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/buckets/fundamentals

**Contents:**
- Storage Buckets
- Access model#
  - Private buckets#
    - Example use cases:#
  - Public buckets#
    - Example use cases:#

Buckets allow you to keep your files organized and determines the Access Model for your assets. Upload restrictions like max file size and allowed content types are also defined at the bucket level.

There are 2 access models for buckets, public and private buckets.

When a bucket is set to Private all operations are subject to access control via RLS policies. This also applies when downloading assets. Buckets are private by default.

The only ways to download assets within a private bucket is to:

When a bucket is designated as 'Public,' it effectively bypasses access controls for both retrieving and serving files within the bucket. This means that anyone who possesses the asset URL can readily access the file.

Access control is still enforced for other types of operations including uploading, deleting, moving, and copying.

Public buckets are more performant than private buckets since they are cached differently.

---

## Analytics Buckets Limits | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/limits

**Contents:**
- Analytics Buckets Limits
      - This feature is in alpha

Analytics Buckets Limits

Expect rapid changes, limited features, and possible breaking updates. share feedback as we refine the experience and expand access.

The following default limits are applied when this feature is in the alpha stage, they can be adjusted on a case-by-case basis:

---

## PyIceberg | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/examples/pyiceberg

**Contents:**
- PyIceberg
      - This feature is in alpha
- Installation#
- Basic setup#
- Creating tables#
- Writing data#
- Reading data#
- Advanced operations#
  - Listing tables and namespaces#
  - Handling errors#

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

PyIceberg is a Python client for Apache Iceberg that enables programmatic interaction with Iceberg tables. Use it to create, read, update, and delete data in your analytics buckets.

Here's a complete example showing how to connect to your Supabase analytics bucket and perform operations:

**Examples:**

Example 1 (unknown):
```unknown
1pip install pyiceberg pyarrow
```

Example 2 (python):
```python
1from pyiceberg.catalog import load_catalog2import pyarrow as pa3import datetime45# Configuration - Update with your Supabase credentials6PROJECT_REF = "your-project-ref"7WAREHOUSE = "your-analytics-bucket-name"8SERVICE_KEY = "your-service-key"910# S3 credentials from Project Settings > Storage11S3_ACCESS_KEY = "your-access-key"12S3_SECRET_KEY = "your-secret-key"13S3_REGION = "us-east-1"1415# Construct Supabase endpoints16S3_ENDPOINT = f"https://{PROJECT_REF}.supabase.co/storage/v1/s3"17CATALOG_URI = f"https://{PROJECT_REF}.supabase.co/storage/v1/iceberg"1819# Load the Iceberg REST Catalog20catalog = load_catalog(21    "supabase-analytics",22    type="rest",23    warehouse=WAREHOUSE,24    uri=CATALOG_URI,25    token=SERVICE_KEY,26    **{27        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",28        "s3.endpoint": S3_ENDPOINT,29        "s3.access-key-id": S3_ACCESS_KEY,30        "s3.secret-access-key": S3_SECRET_KEY,31        "s3.region": S3_REGION,32        "s3.force-virtual-addressing": False,33    },34)3536print("✓ Successfully connected to Iceberg catalog")
```

Example 3 (csharp):
```csharp
1# Create a namespace for organization2catalog.create_namespace_if_not_exists("analytics")34# Define the schema for your Iceberg table5schema = pa.schema([6    pa.field("event_id", pa.int64()),7    pa.field("user_id", pa.int64()),8    pa.field("event_name", pa.string()),9    pa.field("event_timestamp", pa.timestamp("ms")),10    pa.field("properties", pa.string()),11])1213# Create the table14table = catalog.create_table_if_not_exists(15    ("analytics", "events"),16    schema=schema17)1819print("✓ Created table: analytics.events")
```

Example 4 (unknown):
```unknown
1import datetime23# Prepare your data4current_time = datetime.datetime.now()5data = pa.table({6    "event_id": [1, 2, 3, 4, 5],7    "user_id": [101, 102, 101, 103, 102],8    "event_name": ["login", "view_product", "logout", "purchase", "login"],9    "event_timestamp": [current_time] * 5,10    "properties": [11        '{"browser":"chrome"}',12        '{"product_id":"123"}',13        '{}',14        '{"amount":99.99}',15        '{"browser":"firefox"}'16    ],17})1819# Append data to the table20table.append(data)21print("✓ Appended 5 rows to analytics.events")
```

---

## Storage | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage

**Contents:**
- Storage
- Use Supabase to store and serve files.
- Key features#
- Storage bucket types#
  - Files buckets#
  - Analytics buckets#
  - Vector buckets#
- Examples#
- Resources#

Use Supabase to store and serve files.

Supabase Storage is a robust, scalable solution for managing files of any size with fine-grained access controls and optimized delivery. Whether you're storing user-generated content, analytics data, or vector embeddings, Supabase Storage provides specialized bucket types to meet your specific needs.

Supabase Storage offers different bucket types optimized for specific use cases:

Store and serve traditional files including images, videos, documents, and general-purpose content. Ideal for user-generated content, media libraries, and asset management.

Use cases: Images, videos, documents, PDFs, archives

Learn more about Files Buckets

Purpose-built for storing and analyzing data in open table formats like Apache Iceberg. Perfect for time-series data, logs, and large-scale analytical workloads.

Use cases: Data lakes, analytics pipelines, ETL operations, historical data analysis

Learn more about Analytics Buckets

Specialized storage for vector embeddings and similarity search operations. Designed for AI and ML applications requiring semantic search capabilities.

Use cases: AI-powered search, semantic similarity matching, embedding storage, RAG systems

Learn more about Vector Buckets

Check out all of the Storage templates and examples in our GitHub repository.

Resumable Uploads with Uppy

Find the source code and documentation in the Supabase GitHub repository.

---

## Resumable Uploads | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/uploads/resumable-uploads

**Contents:**
- Resumable Uploads
- Learn how to upload files to Supabase Storage.
  - Upload URL#
  - Concurrency#
  - Uppy example#
  - Presigned uploads#
- Overwriting files#

Learn how to upload files to Supabase Storage.

The resumable upload method is recommended when:

Supabase Storage implements the TUS protocol to enable resumable uploads. TUS stands for The Upload Server and is an open protocol for supporting resumable uploads. The protocol allows the upload process to be resumed from where it left off in case of interruptions. This method can be implemented using the tus-js-client library, or other client-side libraries like Uppy that support the TUS protocol.

For optimal performance when uploading large files you should always use the direct storage hostname. This provides several performance enhancements that will greatly improve performance when uploading large files.

Instead of https://project-id.supabase.co use https://project-id.storage.supabase.co

Here's an example of how to upload a file using tus-js-client:

When uploading using the resumable upload endpoint, the storage server creates a unique URL for each upload, even for multiple uploads to the same path. All chunks will be uploaded to this URL using the PATCH method.

This unique upload URL will be valid for up to 24 hours. If the upload is not completed within 24 hours, the URL will expire and you'll need to start the upload again. TUS client libraries typically create a new URL if the previous one expires.

When two or more clients upload to the same upload URL only one of them will succeed. The other clients will receive a 409 Conflict error. Only 1 client can upload to the same upload URL at a time which prevents data corruption.

When two or more clients upload a file to the same path using different upload URLs, the first client to complete the upload will succeed and the other clients will receive a 409 Conflict error.

If you provide the x-upsert header the last client to complete the upload will succeed instead.

You can check a full example using Uppy.

Uppy has integrations with different frameworks:

Resumable uploads also supports using signed upload tokens to created time-limited URLs that you can share to your users by invoking the createSignedUploadUrl method on the SDK and including the returned token in the x-signature header of the resumable upload.

See this full example using Uppy with signed URLs for more context.

When uploading a file to a path that already exists, the default behavior is to return a 400 Asset Already Exists error. If you want to overwrite a file on a specific path you can set the x-upsert header to true.

We do advise against overwriting files when possible, as the CDN will take some time to propagate the changes to all the edge nodes leading to stale content. Uploading a file to a new path is the recommended way to avoid propagation delays and stale content.

To learn more, see the CDN guide.

**Examples:**

Example 1 (javascript):
```javascript
1const tus = require('tus-js-client')23const projectId = ''45async function uploadFile(bucketName, fileName, file) {6    const { data: { session } } = await supabase.auth.getSession()78    return new Promise((resolve, reject) => {9        var upload = new tus.Upload(file, {10            // Supabase TUS endpoint (with direct storage hostname)11            endpoint: `https://${projectId}.storage.supabase.co/storage/v1/upload/resumable`,12            retryDelays: [0, 3000, 5000, 10000, 20000],13            headers: {14                authorization: `Bearer ${session.access_token}`,15                'x-upsert': 'true', // optionally set upsert to true to overwrite existing files16            },17            uploadDataDuringCreation: true,18            removeFingerprintOnSuccess: true, // Important if you want to allow re-uploading the same file https://github.com/tus/tus-js-client/blob/main/docs/api.md#removefingerprintonsuccess19            metadata: {20                bucketName: bucketName,21                objectName: fileName,22                contentType: 'image/png',23                cacheControl: 3600,24                metadata: JSON.stringify({ // custom metadata passed to the user_metadata column25                   yourCustomMetadata: true,26                }),27            },28            chunkSize: 6 * 1024 * 1024, // NOTE: it must be set to 6MB (for now) do not change it29            onError: function (error) {30                console.log('Failed because: ' + error)31                reject(error)32            },33            onProgress: function (bytesUploaded, bytesTotal) {34                var percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2)35                console.log(bytesUploaded, bytesTotal, percentage + '%')36            },37            onSuccess: function () {38                console.log('Download %s from %s', upload.file.name, upload.url)39                resolve()40            },41        })424344        // Check if there are any previous uploads to continue.45        return upload.findPreviousUploads().then(function (previousUploads) {46            // Found previous uploads so we select the first one.47            if (previousUploads.length) {48                upload.resumeFromPreviousUpload(previousUploads[0])49            }5051            // Start the upload52            upload.start()53        })54    })55}
```

Example 2 (javascript):
```javascript
1// Create a signed upload URL2const { data } = await supabase.storage.from('bucket_name').createSignedUploadUrl('file_path', {3  upsert: true, // Optional: allow overwriting existing files4})56// Use the signed URL token in resumable upload headers7// Include data.token in the x-signature header
```

---

## Serving assets from Storage | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/serving/downloads

**Contents:**
- Serving assets from Storage
- Serving assets from Storage
- Public buckets#
  - Downloading#
- Private buckets#
  - Signing URLs#

Serving assets from Storage

Serving assets from Storage

As mentioned in the Buckets Fundamentals all files uploaded in a public bucket are publicly accessible and benefit a high CDN cache HIT ratio.

You can access them by using this conventional URL:

You can also use the Supabase SDK getPublicUrl to generate this URL for you

If you want the browser to start an automatic download of the asset instead of trying serving it, you can add the ?download query string parameter.

By default it will use the asset name to save the file on disk. You can optionally pass a custom name to the download parameter as following: ?download=customname.jpg

Assets stored in a non-public bucket are considered private and are not accessible via a public URL like the public buckets.

You can access them only by:

You can sign a time-limited URL that you can share to your users by invoking the createSignedUrl method on the SDK.

**Examples:**

Example 1 (unknown):
```unknown
1https://[project_id].supabase.co/storage/v1/object/public/[bucket]/[asset-name]
```

Example 2 (javascript):
```javascript
1const { data } = supabase.storage.from('bucket').getPublicUrl('filePath.jpg')23console.log(data.publicUrl)
```

Example 3 (javascript):
```javascript
1const { data, error } = await supabase.storage2  .from('bucket')3  .createSignedUrl('private-document.pdf', 3600)45if (data) {6  console.log(data.signedUrl)7}
```

---

## Apache Spark | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/examples/apache-spark

**Contents:**
- Apache Spark
      - This feature is in alpha
- Installation#
- Basic setup#
- Creating tables#
- Writing data#
- Reading data#
- Advanced operations#
  - Working with dataframes#
  - Joining tables#

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

Apache Spark enables distributed analytical processing of large datasets stored in your analytics buckets. Use it for complex transformations, aggregations, and machine learning workflows.

First, ensure you have Spark installed. For Python-based workflows:

For detailed Spark setup instructions, see the Apache Spark documentation.

Here's a complete example showing how to configure Spark with your Supabase analytics bucket:

**Examples:**

Example 1 (unknown):
```unknown
1pip install pyspark
```

Example 2 (python):
```python
1from pyspark.sql import SparkSession23# Configuration - Update with your Supabase credentials4PROJECT_REF = "your-project-ref"5WAREHOUSE = "your-analytics-bucket-name"6SERVICE_KEY = "your-service-key"78# S3 credentials from Project Settings > Storage9S3_ACCESS_KEY = "your-access-key"10S3_SECRET_KEY = "your-secret-key"11S3_REGION = "us-east-1"1213# Construct Supabase endpoints14S3_ENDPOINT = f"https://{PROJECT_REF}.supabase.co/storage/v1/s3"15CATALOG_URI = f"https://{PROJECT_REF}.supabase.co/storage/v1/iceberg"1617# Initialize Spark session with Iceberg configuration18spark = SparkSession.builder \19    .master("local[*]") \20    .appName("SupabaseIceberg") \21    .config("spark.driver.host", "127.0.0.1") \22    .config("spark.driver.bindAddress", "127.0.0.1") \23    .config(24        'spark.jars.packages',25        'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1,org.apache.iceberg:iceberg-aws-bundle:1.6.1'26    ) \27    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \28    .config("spark.sql.catalog.supabase", "org.apache.iceberg.spark.SparkCatalog") \29    .config("spark.sql.catalog.supabase.type", "rest") \30    .config("spark.sql.catalog.supabase.uri", CATALOG_URI) \31    .config("spark.sql.catalog.supabase.warehouse", WAREHOUSE) \32    .config("spark.sql.catalog.supabase.token", SERVICE_KEY) \33    .config("spark.sql.catalog.supabase.s3.endpoint", S3_ENDPOINT) \34    .config("spark.sql.catalog.supabase.s3.path-style-access", "true") \35    .config("spark.sql.catalog.supabase.s3.access-key-id", S3_ACCESS_KEY) \36    .config("spark.sql.catalog.supabase.s3.secret-access-key", S3_SECRET_KEY) \37    .config("spark.sql.catalog.supabase.s3.remote-signing-enabled", "false") \38    .config("spark.sql.defaultCatalog", "supabase") \39    .getOrCreate()4041print("✓ Spark session initialized with Iceberg")
```

Example 3 (csharp):
```csharp
1# Create a namespace for organization2spark.sql("CREATE NAMESPACE IF NOT EXISTS analytics")34# Create a new Iceberg table5spark.sql("""6    CREATE TABLE IF NOT EXISTS analytics.events (7        event_id BIGINT,8        user_id BIGINT,9        event_name STRING,10        event_timestamp TIMESTAMP,11        properties STRING12    )13    USING iceberg14""")1516print("✓ Created table: analytics.events")
```

Example 4 (unknown):
```unknown
1# Insert data into the table2spark.sql("""3    INSERT INTO analytics.events (event_id, user_id, event_name, event_timestamp, properties)4    VALUES5        (1, 101, 'login', TIMESTAMP '2024-01-15 10:30:00', '{"browser":"chrome"}'),6        (2, 102, 'view_product', TIMESTAMP '2024-01-15 10:35:00', '{"product_id":"123"}'),7        (3, 101, 'logout', TIMESTAMP '2024-01-15 10:40:00', '{}'),8        (4, 103, 'purchase', TIMESTAMP '2024-01-15 10:45:00', '{"amount":99.99}')9""")1011print("✓ Inserted 4 rows into analytics.events")
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-update-storage-config

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

## Migrated from Firebase Storage to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase/firebase-storage

**Contents:**
- Migrated from Firebase Storage to Supabase
- Migrate Firebase Storage files to Supabase Storage.
- Set up the migration tool #
- Generate a Firebase private key #
- Command line options#
  - Download Firestore Storage bucket to a local filesystem folder #
  - Upload files to Supabase Storage bucket #
- Resources#
- Migrate to Supabase#

Migrated from Firebase Storage to Supabase

Migrate Firebase Storage files to Supabase Storage.

Supabase provides several tools to convert storage files from Firebase Storage to Supabase Storage. Conversion is a two-step process:

Clone the firebase-to-supabase repository:

In the /storage directory, rename supabase-keys-sample.js to supabase-keys.js.

Go to your Supabase project's API settings in the Dashboard.

Copy the Project URL and update the SUPABASE_URL value in supabase-keys.js.

Under Project API keys, copy the service_role key and update the SUPABASE_KEY value in supabase-keys.js.

node download.js <prefix> [<folder>] [<batchSize>] [<limit>] [<token>]

To process in batches using multiple command-line executions, you must use the same parameters with a new <token> on subsequent calls. Use the token displayed on the last call to continue the process at a given point.

node upload.js <prefix> <folder> <bucket>

If the bucket doesn't exist, it's created as a non-public bucket. You must set permissions on this new bucket in the Supabase Dashboard before users can download any files.

Contact us if you need more help migrating your project.

**Examples:**

Example 1 (unknown):
```unknown
1git clone https://github.com/supabase-community/firebase-to-supabase.git
```

---

## Standard Uploads | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/uploads/standard-uploads

**Contents:**
- Standard Uploads
- Learn how to upload files to Supabase Storage.
- Uploading#
- Overwriting files#
- Content type#
- Concurrency#

Learn how to upload files to Supabase Storage.

The standard file upload method is ideal for small files that are not larger than 6MB.

It uses the traditional multipart/form-data format and is simple to implement using the supabase-js SDK. Here's an example of how to upload a file using the standard upload method:

Though you can upload up to 5GB files using the standard upload method, we recommend using TUS Resumable Upload for uploading files greater than 6MB in size for better reliability.

When uploading a file to a path that already exists, the default behavior is to return a 400 Asset Already Exists error. If you want to overwrite a file on a specific path you can set the upsert options to true or using the x-upsert header.

We do advise against overwriting files when possible, as our Content Delivery Network will take sometime to propagate the changes to all the edge nodes leading to stale content. Uploading a file to a new path is the recommended way to avoid propagation delays and stale content.

By default, Storage will assume the content type of an asset from the file extension. If you want to specify the content type for your asset, pass the contentType option during upload.

When two or more clients upload a file to the same path, the first client to complete the upload will succeed and the other clients will receive a 400 Asset Already Exists error. If you provide the x-upsert header the last client to complete the upload will succeed instead.

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23// Create Supabase client4const supabase = createClient('your_project_url', 'your_supabase_api_key')56// Upload file using standard upload7async function uploadFile(file) {8  const { data, error } = await supabase.storage.from('bucket_name').upload('file_path', file)9  if (error) {10    // Handle error11  } else {12    // Handle success13  }14}
```

Example 2 (javascript):
```javascript
1// Create Supabase client2const supabase = createClient('your_project_url', 'your_supabase_api_key')34await supabase.storage.from('bucket_name').upload('file_path', file, {5  upsert: true,6})
```

Example 3 (javascript):
```javascript
1// Create Supabase client2const supabase = createClient('your_project_url', 'your_supabase_api_key')34await supabase.storage.from('bucket_name').upload('file_path', file, {5  contentType: 'image/jpeg',6})
```

---

## File Storage | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/ephemeral-storage

**Contents:**
- File Storage
- Use persistent and ephemeral file storage
- Persistent Storage#
- Ephemeral storage#
- Common use cases#
  - Archive processing with background tasks#
  - Image manipulation#
- Using synchronous file APIs#
- Limits#

Use persistent and ephemeral file storage

Edge Functions provides two flavors of file storage:

You can use file storage to:

The persistent storage option is built on top of the S3 protocol. It allows you to mount any S3-compatible bucket, including Supabase Storage Buckets, as a directory for your Edge Functions. You can perform operations such as reading and writing files to the mounted buckets as you would in a POSIX file system.

To access an S3 bucket from Edge Functions, you must set the following for environment variables in Edge Function Secrets.

Follow this guide to enable and create an access key for Supabase Storage S3.

To access a file path in your mounted bucket from your Edge Function, use the prefix /s3/YOUR-BUCKET-NAME.

Ephemeral storage will reset on each function invocation. This means the files you write during an invocation can only be read within the same invocation.

You can use Deno File System APIs or the node:fs module to access the /tmp path.

You can use ephemeral storage with Background Tasks to handle large file processing operations that exceed memory limits.

Imagine you have a Photo Album application that accepts photo uploads as zip files. A streaming implementation will run into memory limit errors with zip files exceeding 100MB, as it retains all archive files in memory simultaneously.

You can write the zip file to ephemeral storage first, then use a background task to extract and upload files to Supabase Storage. This way, you only read parts of the zip file to the memory.

Custom image manipulation workflows using magick-wasm.

You can safely use the following synchronous Deno APIs (and their Node counterparts) during initial script evaluation:

Keep in mind that the sync APIs are available only during initial script evaluation and aren’t supported in callbacks like HTTP handlers or setTimeout.

There are no limits on S3 buckets you mount for Persistent storage.

**Examples:**

Example 1 (javascript):
```javascript
1// read from S3 bucket2const data = await Deno.readFile('/s3/my-bucket/results.csv')34// make a directory5await Deno.mkdir('/s3/my-bucket/sub-dir')67// write to S3 bucket8await Deno.writeTextFile('/s3/my-bucket/demo.txt', 'hello world')
```

Example 2 (javascript):
```javascript
1Deno.serve(async (req) => {2  if (req.headers.get('content-type') !== 'application/zip') {3    return new Response('file must be a zip file', {4      status: 400,5    })6  }78  const uploadId = crypto.randomUUID()9  await Deno.writeFile('/tmp/' + uploadId, req.body)1011  // E.g. extract and process the zip file12  const zipFile = await Deno.readFile('/tmp/' + uploadId)13  // You could use a zip library to extract contents14  const extracted = await extractZip(zipFile)1516  // Or process the file directly17  console.log(`Processing zip file: ${uploadId}, size: ${zipFile.length} bytes`)18})
```

Example 3 (python):
```python
1import { BlobWriter, ZipReader } from 'https://deno.land/x/zipjs/index.js'2import { createClient } from 'jsr:@supabase/supabase-js@2'34const supabase = createClient(5  Deno.env.get('SUPABASE_URL'),6  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')7)89async function processZipFile(uploadId: string, filepath: string) {10  const file = await Deno.open(filepath, { read: true })11  const zipReader = new ZipReader(file.readable)12  const entries = await zipReader.getEntries()1314  await supabase.storage.createBucket(uploadId, { public: false })1516  await Promise.all(17    entries.map(async (entry) => {18      if (entry.directory) return1920      // Read file entry from temp storage21      const blobWriter = new BlobWriter()22      const blob = await entry.getData(blobWriter)2324      // Upload to permanent storage25      await supabase.storage.from(uploadId).upload(entry.filename, blob)2627      console.log('uploaded', entry.filename)28    })29  )3031  await zipReader.close()32}3334Deno.serve(async (req) => {35  const uploadId = crypto.randomUUID()36  const filepath = `/tmp/${uploadId}.zip`3738  // Write zip to ephemeral storage39  await Deno.writeFile(filepath, req.body)4041  // Process in background to avoid memory limits42  EdgeRuntime.waitUntil(processZipFile(uploadId, filepath))4344  return new Response(JSON.stringify({ uploadId }), {45    headers: { 'Content-Type': 'application/json' },46  })47})
```

Example 4 (javascript):
```javascript
1Deno.serve(async (req) => {2  // Save uploaded image to temp storage3  const imagePath = `/tmp/input-${crypto.randomUUID()}.jpg`4  await Deno.writeFile(imagePath, req.body)56  // Process image with magick-wasm7  const processedPath = `/tmp/output-${crypto.randomUUID()}.jpg`8  // ... image manipulation logic910  // Read processed image and return11  const processedImage = await Deno.readFile(processedPath)12  return new Response(processedImage, {13    headers: { 'Content-Type': 'image/jpeg' },14  })15})
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/create-a-bucket

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/delete-a-bucket

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Custom Roles | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/schema/custom-roles

**Contents:**
- Custom Roles
- Learn about using custom roles with storage schema
- Create a custom role#
- Create a policy#
- Test the policy#

Learn about using custom roles with storage schema

In this guide, you will learn how to create and use custom roles with Storage to manage role-based access to objects and buckets. The same approach can be used to use custom roles with any other Supabase service.

Supabase Storage uses the same role-based access control system as any other Supabase service using RLS (Row Level Security).

Let's create a custom role manager to provide full read access to a specific bucket. For a more advanced setup, see the RBAC Guide.

Let's create a policy that gives full read permissions to all objects in the bucket teams for the manager role.

To impersonate the manager role, you will need a valid JWT token with the manager role. You can quickly create one using the jsonwebtoken library in Node.js.

Signing a new JWT requires your JWT_SECRET. You must store this secret securely. Never expose it in frontend code, and do not check it into version control.

Now you can use this token to access the Storage API.

**Examples:**

Example 1 (unknown):
```unknown
1create role 'manager';23-- Important to grant the role to the authenticator and anon role4grant manager to authenticator;5grant anon to manager;
```

Example 2 (unknown):
```unknown
1create policy "Manager can view all files in the bucket 'teams'"2on storage.objects3for select4to manager5using (6 bucket_id = 'teams'7);
```

Example 3 (javascript):
```javascript
1const jwt = require('jsonwebtoken')23const JWT_SECRET = 'your-jwt-secret' // You can find this in your Supabase project settings under API. Store this securely.4const USER_ID = '' // the user id that we want to give the manager role56const token = jwt.sign({ role: 'manager', sub: USER_ID }, JWT_SECRET, {7  expiresIn: '1h',8})
```

Example 4 (javascript):
```javascript
1const { StorageClient } = require('@supabase/storage-js')23const PROJECT_URL = 'https://your-project-id.supabase.co/storage/v1'45const storage = new StorageClient(PROJECT_URL, {6  authorization: `Bearer ${token}`,7})89await storage.from('teams').list()
```

---

## Limits | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/uploads/file-limits

**Contents:**
- Limits
- Learn how to increase Supabase file limits.
- Global file size#
- Per bucket restrictions#

Learn how to increase Supabase file limits.

You can set the maximum file size across all your buckets by setting the Global file size limit value in your Storage Settings. For Free projects, the limit can't exceed 50 MB. On the Pro Plan and up, you can set this value to up to 500 GB. If you need more than 500 GB, contact us.

This option is a global limit, which applies to all your buckets.

Additionally, you can specify the maximum file size on a per bucket level but it can't be higher than this global limit. As a good practice, the global limit should be set to the highest possible file size that your application accepts, with smaller per-bucket limits set as needed.

You can have different restrictions on a per bucket level such as restricting the file types (e.g. pdf, images, videos) or the maximum file size, which should be lower than the global limit. To apply these limits on a bucket level see Creating Buckets.

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/retrieve-an-object

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## JavaScript: Download a file | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/storage-from-download

---

## Ownership | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/security/ownership

**Contents:**
- Ownership
- Access control#

When creating new buckets or objects in Supabase Storage, an owner is automatically assigned to the bucket or object. The owner is the user who created the resource and the value is derived from the sub claim in the JWT. We store the owner in the owner_id column.

When using the service_key to create a resource, the owner will not be set and the resource will be owned by anyone. This is also the case when you are creating Storage resources via the Dashboard.

The Storage schema has 2 fields to represent ownership: owner and owner_id. owner is deprecated and will be removed. Use owner_id instead.

By itself, the ownership of a resource does not provide any access control. However, you can enforce the ownership by implementing access control against storage resources scoped to their owner.

For example, you can implement a policy where only the owner of an object can delete it. To do this, check the owner_id field of the object and compare it with the sub claim of the JWT:

The use of RLS policies is just one way to enforce access control. You can also implement access control in your server code by following the same pattern.

**Examples:**

Example 1 (unknown):
```unknown
1create policy "User can delete their own objects"2on storage.objects3for delete4to authenticated5using (6    owner_id = (select auth.uid()::text)7);
```

---

## Working with Vector Indexes | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/vector/working-with-indexes

**Contents:**
- Working with Vector Indexes
- Create, manage, and optimize vector indexes for efficient similarity search.
      - This feature is in alpha
- Understanding vector indexes#
- Creating indexes#
  - Via Dashboard#
  - Via SDK#
  - Choosing the right metric#
- Managing multiple indexes#
  - Use cases for multiple indexes#

Working with Vector Indexes

Create, manage, and optimize vector indexes for efficient similarity search.

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

Vector indexes organize embeddings within a bucket with consistent dimensions and distance metrics. Each index defines how similarity searches are performed across your vectors.

Think of an index as a table in a traditional database. It has a schema (dimension) and a query strategy (distance metric).

Most modern embedding models work best with cosine distance:

Tip: Check your embedding model's documentation for the recommended distance metric.

Important: Creating an index with incorrect dimensions will cause insert and query operations to fail.

Create multiple indexes for different use cases or embedding models:

Delete an index to free storage space:

Warning: Deleting an index is permanent and cannot be undone.

Once created, these properties cannot be changed:

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabase = createClient('https://your-project.supabase.co', 'your-service-key')45const bucket = supabase.storage.vectors.from('embeddings')67// Create an index8const { data, error } = await bucket.createIndex({9  indexName: 'documents-openai',10  dataType: 'float32',11  dimension: 1536,12  distanceMetric: 'cosine',13})1415if (error) {16  console.error('Error creating index:', error)17} else {18  console.log('Index created:', data)19}
```

Example 2 (javascript):
```javascript
1const bucket = supabase.storage.vectors.from('embeddings')23// Index for OpenAI embeddings4await bucket.createIndex({5  indexName: 'documents-openai',6  dimension: 1536,7  distanceMetric: 'cosine',8  dataType: 'float32',9})1011// Index for Cohere embeddings12await bucket.createIndex({13  indexName: 'documents-cohere',14  dimension: 1024,15  distanceMetric: 'cosine',16  dataType: 'float32',17})1819// Index for different use case20await bucket.createIndex({21  indexName: 'images-openai',22  dimension: 1536,23  distanceMetric: 'cosine',24  dataType: 'float32',25})2627// List all indexes28const { data: indexes } = await bucket.listIndexes()29console.log('All indexes:', indexes)
```

Example 3 (javascript):
```javascript
1const bucket = supabase.storage.vectors.from('embeddings')23const { data: indexes, error } = await bucket.listIndexes()45if (!error) {6  indexes?.forEach((index) => {7    console.log(`Index: ${index.name}`)8    console.log(`  Dimension: ${index.dimension}`)9    console.log(`  Distance: ${index.distanceMetric}`)10  })11}
```

Example 4 (javascript):
```javascript
1const { data: indexDetails, error } = await bucket.getIndex('documents-openai')23if (!error && indexDetails) {4  console.log(`Index: ${indexDetails.name}`)5  console.log(`Created at: ${indexDetails.createdAt}`)6  console.log(`Dimension: ${indexDetails.dimension}`)7  console.log(`Distance metric: ${indexDetails.distanceMetric}`)8}
```

---

## Manage Storage size usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/storage-size

**Contents:**
- Manage Storage size usage
- What you are charged for#
- How charges are calculated#
  - Usage on your invoice#
- Pricing#
- Billing examples#
  - Within quota#
  - Exceeding quota#
- View usage#
  - Usage page#

Manage Storage size usage

You are charged for the total size of all assets in your buckets.

Storage size is charged by Gigabyte-Hours (GB-Hrs). 1 GB-Hr represents the use of 1 GB of storage for 1 hour. For example, storing 10 GB of data for 5 hours results in 50 GB-Hrs (10 GB × 5 hours).

Usage is shown as "Storage Size GB-Hrs" on your invoice.

$0.00002919 per GB-Hr ($0.021 per GB per month). You are only charged for usage exceeding your subscription plan's quota.

The organization's Storage size usage is within the quota, so no charges for Storage size apply.

The organization's Storage size usage exceeds the quota by 257 GB, incurring charges for this additional usage.

You can view Storage size usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Storage size section, you can see how much storage your projects have used during the selected time period.

Since we designed Storage to work as an integrated part of your Postgres database on Supabase, you can query information about your Storage objects in the storage schema.

List files larger than 5 MB:

List buckets with their total size:

**Examples:**

Example 1 (unknown):
```unknown
1select2    name,3    bucket_id as bucket,4    case5        when (metadata->>'size')::int >= 1073741824 then6            ((metadata->>'size')::int / 1073741824.0)::numeric(10, 2) || ' GB'7        when (metadata->>'size')::int >= 1048576 then8            ((metadata->>'size')::int / 1048576.0)::numeric(10, 2) || ' MB'9        when (metadata->>'size')::int >= 1024 then10            ((metadata->>'size')::int / 1024.0)::numeric(10, 2) || ' KB'11        else12            (metadata->>'size')::int || ' bytes'13        end as size14from15    storage.objects16where17    (metadata->>'size')::int > 1048576 * 518order by (metadata->>'size')::int desc
```

Example 2 (unknown):
```unknown
1select2    bucket_id,3    (sum((metadata->>'size')::int) / 1048576.0)::numeric(10, 2) as total_size_megabyte4from5    storage.objects6group by7    bucket_id8order by9    total_size_megabyte desc;
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/upload-a-new-object

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-storage

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

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/moves-an-object

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Manage Storage Image Transformations usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/storage-image-transformations

**Contents:**
- Manage Storage Image Transformations usage
- What you are charged for#
  - Example#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Pricing#
- Pricing#
- Billing examples#
  - Within quota#

Manage Storage Image Transformations usage

You are charged for the number of distinct images transformed during the billing period, regardless of how many transformations each image undergoes. We refer to these images as "origin" images.

With these four transformations applied to image-1.jpg and image-2.jpg, the origin images count is 2.

Storage Image Transformations are billed using Package pricing, with each package representing 1000 origin images. If your usage falls between two packages, you are billed for the next whole package.

For simplicity, let's assume a package size of 1,000 and a charge of $5 per package with no quota.

Usage is shown as "Storage Image Transformations" on your invoice.

$5 per 1,000 origin images. You are only charged for usage exceeding your subscription plan's quota.

The count resets at the start of each billing cycle.

For a detailed breakdown of how charges are calculated, refer to Manage Storage Image Transformations usage.

The organization's number of origin images for the billing cycle is within the quota, so no charges apply.

The organization's number of origin images for the billing cycle exceeds the quota by 750, incurring charges for this additional usage.

You can view Storage Image Transformations usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Storage Image Transformations section, you can see how many origin images were transformed during the selected time period.

**Examples:**

Example 1 (unknown):
```unknown
1supabase.storage.from('bucket').createSignedUrl('image-1.jpg', 60000, {2  transform: {3    width: 200,4    height: 200,5  },6})
```

Example 2 (unknown):
```unknown
1supabase.storage.from('bucket').createSignedUrl('image-2.jpg', 60000, {2  transform: {3    width: 400,4    height: 300,5  },6})
```

Example 3 (unknown):
```unknown
1supabase.storage.from('bucket').createSignedUrl('image-2.jpg', 60000, {2  transform: {3    width: 600,4    height: 250,5  },6})
```

Example 4 (unknown):
```unknown
1supabase.storage.from('bucket').download('image-2.jpg', {2  transform: {3    width: 800,4    height: 300,5  },6})
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-list-all-buckets

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

## Storage Access Control | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/security/access-control

**Contents:**
- Storage Access Control
- Access policies#
- Policy examples#
- Bypassing access controls#

Storage Access Control

Supabase Storage is designed to work perfectly with Postgres Row Level Security (RLS).

You can use RLS to create Security Access Policies that are incredibly powerful and flexible, allowing you to restrict access based on your business needs.

By default Storage does not allow any uploads to buckets without RLS policies. You selectively allow certain operations by creating RLS policies on the storage.objects table.

You can find the documentation for the storage schema here , and to simplify the process of crafting your policies, you can utilize these helper functions .

The RLS policies required for different operations are documented here

For example, the only RLS policy required for uploading objects is to grant the INSERT permission to the storage.objects table.

To allow overwriting files using the upsert functionality you will need to additionally grant SELECT and UPDATE permissions.

An easy way to get started would be to create RLS policies for SELECT, INSERT, UPDATE, DELETE operations and restrict the policies to meet your security requirements. For example, one can start with the following INSERT policy:

and modify it to only allow authenticated users to upload assets to a specific bucket by changing it to:

This example demonstrates how you would allow authenticated users to upload files to a folder called private inside my_bucket_id:

This example demonstrates how you would allow authenticated users to upload files to a folder called with their users.id inside my_bucket_id:

Allow a user to access a file that was previously uploaded by the same user:

If you exclusively use Storage from trusted clients, such as your own servers, and need to bypass the RLS policies, you can use the service key in the Authorization header. Service keys entirely bypass RLS policies, granting you unrestricted access to all Storage APIs.

Remember you should not share the service key publicly.

**Examples:**

Example 1 (unknown):
```unknown
1create policy "policy_name"2ON storage.objects3for insert with check (4  true5);
```

Example 2 (unknown):
```unknown
1create policy "policy_name"2on storage.objects for insert to authenticated with check (3    -- restrict bucket4    bucket_id = 'my_bucket_id'5);
```

Example 3 (unknown):
```unknown
1create policy "Allow authenticated uploads"2on storage.objects3for insert4to authenticated5with check (6  bucket_id = 'my_bucket_id' and7  (storage.foldername(name))[1] = 'private'8);
```

Example 4 (unknown):
```unknown
1create policy "Allow authenticated uploads"2on storage.objects3for insert4to authenticated5with check (6  bucket_id = 'my_bucket_id' and7  (storage.foldername(name))[1] = (select auth.jwt()->>'sub')8);
```

---

## Smart CDN | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/cdn/smart-cdn

**Contents:**
- Smart CDN
- Cache duration#
- Cache eviction#
- Bypassing cache#

With Smart CDN caching enabled, the asset metadata in your database is synchronized to the edge. This automatically revalidates the cache when the asset is changed or deleted.

Moreover, the Smart CDN achieves a greater cache hit rate by shielding the origin server from asset requests that remain unchanged, even when different query strings are used in the URL.

Smart CDN caching is automatically enabled for Pro Plan and above.

When Smart CDN is enabled, the asset is cached on the CDN for as long as possible. You can still control how long assets are stored in the browser using the cacheControl option when uploading a file. Smart CDN caching works with all types of storage operations including signed URLs.

When a file is updated or deleted, the CDN cache is automatically invalidated to reflect the change (including transformed images). It can take up to 60 seconds for the CDN cache to be invalidated as the asset metadata has to propagate across all the data-centers around the globe.

When an asset is invalidated at the CDN level, browsers may not update its cache. This is where cache eviction comes into play.

Even when an asset is marked as invalidated at the CDN level, browsers may not refresh their cache for that asset.

If you have assets that undergo frequent updates, it is advisable to upload the new asset to a different path. This approach ensures that you always have the most up-to-date asset accessible.

If you anticipate that your asset might be deleted, it's advisable to set a shorter browser Time-to-Live (TTL) value using the cacheControl option. The default TTL is typically set to 1 hour, which is generally a reasonable default value.

If you need to ensure assets refresh directly from the origin server and bypass the cache, you can achieve this by adding a unique query string to the URL.

For instance, you can use a URL like /storage/v1/object/sign/profile-pictures/cat.jpg?version=1 with a long browser cache (e.g., 1 year). To update the picture, increment the version query parameter in the URL, like /storage/v1/object/sign/profile-pictures/cat.jpg?version=2. The CDN will recognize it as a new object and fetch the updated version from the origin.

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-storage-config

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

## Creating Analytics Buckets | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/creating-analytics-buckets

**Contents:**
- Creating Analytics Buckets
- Set up your first analytics bucket using the SDK or dashboard.
- Creating an Analytics bucket#
  - Using the Supabase SDK#
  - Using the Supabase Dashboard#
- Next steps#

Creating Analytics Buckets

Set up your first analytics bucket using the SDK or dashboard.

This feature is in Private Alpha. API stability and backward compatibility are not guaranteed at this stage. Request access through this form.

Analytics buckets use Apache Iceberg, an open-table format for efficient management of large analytical datasets. You can interact with analytics buckets using tools such as PyIceberg, Apache Spark, or any client supporting the Iceberg REST Catalog API.

You can create an analytics bucket using either the Supabase SDK or the Supabase Dashboard.

Once you've created your analytics bucket, you can:

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabase = createClient('https://your-project.supabase.co', 'your-service-key')45const { data, error } = await supabase.storage.analytics.createBucket('analytics-data')67if (error) {8  console.error('Failed to create analytics bucket:', error)9} else {10  console.log('Analytics bucket created:', data)11}
```

---

## S3 Compatibility | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/s3/compatibility

**Contents:**
- S3 Compatibility
- Learn about the compatibility of Supabase Storage with S3.
- Implemented endpoints#
  - Bucket operations#
  - Object operations#

Learn about the compatibility of Supabase Storage with S3.

Supabase Storage is compatible with the S3 protocol. You can use any S3 client to interact with your Storage objects.

Storage supports standard, resumable and S3 uploads and all these protocols are interoperable. You can upload a file with the S3 protocol and list it with the REST API or upload with Resumable uploads and list with S3.

Storage supports presigning a URL using query parameters. Specifically, Supabase Storage expects requests to be made using AWS Signature Version 4. To enable this feature, enable the S3 connection via S3 protocol in the Settings page for Supabase Storage.

The S3 protocol is currently in Public Alpha. If you encounter any issues or have feature requests, contact us.

The most commonly used endpoints are implemented, and more will be added. Implemented S3 endpoints are marked with ✅ in the following tables.

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-seed-buckets

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

## Integrating with Supabase Storage | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/storage-caching

**Contents:**
- Integrating with Supabase Storage
- Basic file operations#
- Cache-first pattern#

Integrating with Supabase Storage

Edge Functions work seamlessly with Supabase Storage. This allows you to:

Use the Supabase client to upload files directly from your Edge Functions. You'll need the service role key for server-side storage operations:

Always use the SUPABASE_SERVICE_ROLE_KEY for server-side operations. Never expose this key in client-side code!

Check storage before generating new content to improve performance:

**Examples:**

Example 1 (python):
```python
1import { createClient } from 'npm:@supabase/supabase-js@2'23Deno.serve(async (req) => {4  const supabaseAdmin = createClient(5    Deno.env.get('SUPABASE_URL') ?? '',6    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''7  )89  // Generate your content10  const fileContent = await generateImage()1112  // Upload to storage13  const { data, error } = await supabaseAdmin.storage14    .from('images')15    .upload(`generated/${filename}.png`, fileContent.body!, {16      contentType: 'image/png',17      cacheControl: '3600',18      upsert: false,19    })2021  if (error) {22    throw error23  }2425  return new Response(JSON.stringify({ path: data.path }))26})
```

Example 2 (javascript):
```javascript
1const STORAGE_URL = 'https://your-project.supabase.co/storage/v1/object/public/images'23Deno.serve(async (req) => {4  const url = new URL(req.url)5  const username = url.searchParams.get('username')67  try {8    // Try to get existing file from storage first9    const storageResponse = await fetch(`${STORAGE_URL}/avatars/${username}.png`)1011    if (storageResponse.ok) {12      // File exists in storage, return it directly13      return storageResponse14    }1516    // File doesn't exist, generate it17    const generatedImage = await generateAvatar(username)1819    // Upload to storage for future requests20    const { error } = await supabaseAdmin.storage21      .from('images')22      .upload(`avatars/${username}.png`, generatedImage.body!, {23        contentType: 'image/png',24        cacheControl: '86400', // Cache for 24 hours25      })2627    if (error) {28      console.error('Upload failed:', error)29    }3031    return generatedImage32  } catch (error) {33    return new Response('Error processing request', { status: 500 })34  }35})
```

---

## Storage Optimizations | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/production/scaling

**Contents:**
- Storage Optimizations
- Scaling Storage
- Egress#
    - Resize images#
    - Set a high cache-control value#
    - Limit the upload size#
    - Smart CDN#
- Optimize listing objects#
- Optimizing RLS#

Storage Optimizations

Here are some optimizations that you can consider to improve performance and reduce costs as you start scaling Storage.

If your project has high egress, these optimizations can help reducing it.

Images typically make up most of your egress. By keeping them as small as possible, you can cut down on egress and boost your application's performance. You can take advantage of our Image Transformation service to optimize any image on the fly.

Using the browser cache can effectively lower your egress since the asset remains stored in the user's browser after the initial download. Setting a high cache-control value ensures the asset stays in the user's browser for an extended period, decreasing the need to download it from the server repeatedly. Read more here

You have the option to set a maximum upload size for your bucket. Doing this can prevent users from uploading and then downloading excessively large files. You can control the maximum file size by configuring this option at the bucket level.

By leveraging our Smart CDN, you can achieve a higher cache hit rate and therefore lower your egress cached, as we charge less for cached egress (see egress pricing).

Once you have a substantial number of objects, you might observe that the supabase.storage.list() method starts to slow down. This occurs because the endpoint is quite generic and attempts to retrieve both folders and objects in a single query. While this approach is very useful for building features like the Storage viewer on the Supabase dashboard, it can impact performance with a large number of objects.

If your application doesn't need the entire hierarchy computed you can speed up drastically the query execution for listing your objects by creating a Postgres function as following:

You can then use the your Postgres function as following:

When creating RLS policies against the storage tables you can add indexes to the interested columns to speed up the lookup

**Examples:**

Example 1 (unknown):
```unknown
1create or replace function list_objects(2    bucketid text,3    prefix text,4    limits int default 100,5    offsets int default 06) returns table (7    name text,8    id uuid,9    updated_at timestamptz,10    created_at timestamptz,11    last_accessed_at timestamptz,12    metadata jsonb13) as $$14begin15    return query SELECT16        objects.name,17        objects.id,18        objects.updated_at,19        objects.created_at,20        objects.last_accessed_at,21        objects.metadata22    FROM storage.objects23    WHERE objects.name like prefix || '%'24    AND bucket_id = bucketid25    ORDER BY name ASC26    LIMIT limits27    OFFSET offsets;28end;29$$ language plpgsql stable;
```

Example 2 (unknown):
```unknown
1select * from list_objects('bucket_id', '', 100, 0);
```

Example 3 (javascript):
```javascript
1const { data, error } = await supabase.rpc('list_objects', {2  bucketid: 'yourbucket',3  prefix: '',4  limit: 100,5  offset: 0,6})
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/gets-all-buckets

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/update-the-object-at-an-existing-key

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## S3 Uploads | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/uploads/s3-uploads

**Contents:**
- S3 Uploads
- Learn how to upload files to Supabase Storage using S3.
- Single request uploads#
- Multipart uploads#
  - Upload a file in parts#
  - Aborting multipart uploads#

Learn how to upload files to Supabase Storage using S3.

You can use the S3 protocol to upload files to Supabase Storage. To get started with S3, see the S3 setup guide.

The S3 protocol supports file upload using:

The PutObject action uploads the file in a single request. This matches the behavior of the Supabase SDK Standard Upload.

Use PutObject to upload smaller files, where retrying the entire upload won't be an issue. The maximum file size on paid plans is 500 GB.

For example, using JavaScript and the aws-sdk client:

Multipart Uploads split the file into smaller parts and upload them in parallel, maximizing the upload speed on a fast network. When uploading large files, this allows you to retry the upload of individual parts in case of network issues.

This method is preferable over Resumable Upload for server-side uploads, when you want to maximize upload speed at the cost of resumability. The maximum file size on paid plans is 500 GB.

Use the Upload class from an S3 client to upload a file in parts. For example, using JavaScript:

All multipart uploads are automatically aborted after 24 hours. To abort a multipart upload before that, you can use the AbortMultipartUpload action.

**Examples:**

Example 1 (python):
```python
1import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'23const s3Client = new S3Client({...})45const file = fs.createReadStream('path/to/file')67const uploadCommand = new PutObjectCommand({8  Bucket: 'bucket-name',9  Key: 'path/to/file',10  Body: file,11  ContentType: 'image/jpeg',12})1314await s3Client.send(uploadCommand)
```

Example 2 (python):
```python
1import { S3Client } from '@aws-sdk/client-s3'2import { Upload } from '@aws-sdk/lib-storage'34const s3Client = new S3Client({...})56const file = fs.createReadStream('path/to/very-large-file')78const upload = new Upload(s3Client, {9  Bucket: 'bucket-name',10  Key: 'path/to/file',11  ContentType: 'image/jpeg',12  Body: file,13})1415await uploader.done()
```

---

## Cache Metrics | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/cdn/metrics

**Contents:**
- Cache Metrics

Cache hits can be determined via the metadata.response.headers.cf_cache_status key in our Logs Explorer. Any value that corresponds to either HIT, STALE, REVALIDATED, or UPDATING is categorized as a cache hit. The following example query will show the top cache misses from the edge_logs:

Try out this query in the Logs Explorer.

Your cache hit ratio over time can then be determined using the following query:

Try out this query in the Logs Explorer.

**Examples:**

Example 1 (unknown):
```unknown
1select2  r.path as path,3  r.search as search,4  count(id) as count5from6  edge_logs as f7  cross join unnest(f.metadata) as m8  cross join unnest(m.request) as r9  cross join unnest(m.response) as res10  cross join unnest(res.headers) as h11where12  starts_with(r.path, '/storage/v1/object')13  and r.method = 'GET'14  and h.cf_cache_status in ('MISS', 'NONE/UNKNOWN', 'EXPIRED', 'BYPASS', 'DYNAMIC')15group by path, search16order by count desc17limit 50;
```

Example 2 (unknown):
```unknown
1select2  timestamp_trunc(timestamp, hour) as timestamp,3  countif(h.cf_cache_status in ('HIT', 'STALE', 'REVALIDATED', 'UPDATING')) / count(f.id) as ratio4from5  edge_logs as f6  cross join unnest(f.metadata) as m7  cross join unnest(m.request) as r8  cross join unnest(m.response) as res9  cross join unnest(res.headers) as h10where starts_with(r.path, '/storage/v1/object') and r.method = 'GET'11group by timestamp12order by timestamp desc;
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-storage-cp

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

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/copies-an-object

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Storage Image Transformations | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/serving/image-transformations?queryGroups=language&language=js

**Contents:**
- Storage Image Transformations
- Transform images with Storage
- Get a public URL for a transformed image#
- Signing URLs with transformation options#
- Downloading images#
- Automatic image optimization (WebP)#
- Next.js loader#
- Transformation options#
  - Optimizing#
  - Resizing#

Storage Image Transformations

Transform images with Storage

Supabase Storage offers the functionality to optimize and resize images on the fly. Any image stored in your buckets can be transformed and optimized for fast delivery.

Image Resizing is currently enabled for Pro Plan and above.

Our client libraries methods like getPublicUrl and createSignedUrl support the transform option. This returns the URL that serves the transformed image.

An example URL could look like this:

To share a transformed image in a private bucket for a fixed amount of time, provide the transform option when you create the signed URL:

The transformation options are embedded into the token attached to the URL — they cannot be changed once signed.

To download a transformed image, pass the transform option to the download function.

When using the image transformation API, Storage will automatically find the best format supported by the client and return that to the client, without any code change. For instance, if you use Chrome when viewing a JPEG image and using transformation options, you'll see that images are automatically optimized as webp images.

As a result, this will lower the egress that you send to your users and your application will load much faster.

We currently only support WebP. AVIF support will come in the near future.

Disabling automatic optimization:

In case you'd like to return the original format of the image and opt-out from the automatic image optimization detection, you can pass the format=origin parameter when requesting a transformed image, this is also supported in the JavaScript SDK starting from v2.2.0

You can use Supabase Image Transformation to optimize your Next.js images using a custom Loader.

To get started, create a supabase-image-loader.js file in your Next.js project which exports a default function:

In your next.config.js file add the following configuration to instruct Next.js to use our custom loader

At this point you are ready to use the Image component provided by Next.js

We currently support a few transformation options focusing on optimizing, resizing, and cropping images.

You can set the quality of the returned image by passing a value from 20 to 100 (with 100 being the highest quality) to the quality parameter. This parameter defaults to 80.

You can use width and height parameters to resize an image to a specific dimension. If only one parameter is specified, the image will be resized and cropped, maintaining the aspect ratio.

You can use different resizing modes to fit your needs, each of them uses a different approach to resize the image:

Use the resize parameter with one of the following values:

cover : resizes the image while keeping the aspect ratio to fill a given size and crops projecting parts. (default)

contain : resizes the image while keeping the aspect ratio to fit a given size.

fill : resizes the image without keeping the aspect ratio.

$5 per 1,000 origin images. You are only charged for usage exceeding your subscription plan's quota.

The count resets at the start of each billing cycle.

For a detailed breakdown of how charges are calculated, refer to Manage Storage Image Transformations usage.

Our solution to image resizing and optimization can be self-hosted as with any other Supabase product. Under the hood we use imgproxy

Deploy an imgproxy container with the following configuration:

Note: make sure that this service can only be reachable within an internal network and not exposed to the public internet

Once imgproxy is deployed we need to configure a couple of environment variables in your self-hosted storage-api service as follows:

**Examples:**

Example 1 (unknown):
```unknown
1supabase.storage.from('bucket').getPublicUrl('image.jpg', {2  transform: {3    width: 500,4    height: 600,5  },6})
```

Example 2 (unknown):
```unknown
1https://project_id.supabase.co/storage/v1/render/image/public/bucket/image.jpg?width=500&height=600`
```

Example 3 (unknown):
```unknown
1supabase.storage.from('bucket').createSignedUrl('image.jpg', 60000, {2  transform: {3    width: 200,4    height: 200,5  },6})
```

Example 4 (unknown):
```unknown
1supabase.storage.from('bucket').download('image.jpg', {2  transform: {3    width: 800,4    height: 300,5  },6})
```

---

## Copy Objects | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/management/copy-move-objects

**Contents:**
- Copy Objects
- Learn how to copy and move objects
- Copy objects#
  - Copying objects within the same bucket#
  - Copying objects across buckets#
- Move objects#
  - Moving objects within the same bucket#
  - Moving objects across buckets#
- Permissions#

Learn how to copy and move objects

You can copy objects between buckets or within the same bucket. Currently only objects up to 5 GB can be copied using the API.

When making a copy of an object, the owner of the new object will be the user who initiated the copy operation.

To copy an object within the same bucket, use the copy method.

To copy an object across buckets, use the copy method and specify the destination bucket.

You can move objects between buckets or within the same bucket. Currently only objects up to 5GB can be moved using the API.

When moving an object, the owner of the new object will be the user who initiated the move operation. Once the object is moved, the original object will no longer exist.

To move an object within the same bucket, you can use the move method.

To move an object across buckets, use the move method and specify the destination bucket.

For a user to move and copy objects, they need select permission on the source object and insert permission on the destination object. For example:

**Examples:**

Example 1 (unknown):
```unknown
1await supabase.storage.from('avatars').copy('public/avatar1.png', 'private/avatar2.png')
```

Example 2 (unknown):
```unknown
1await supabase.storage.from('avatars').copy('public/avatar1.png', 'private/avatar2.png', {2  destinationBucket: 'avatars2',3})
```

Example 3 (javascript):
```javascript
1const { data, error } = await supabase.storage2  .from('avatars')3  .move('public/avatar1.png', 'private/avatar2.png')
```

Example 4 (unknown):
```unknown
1await supabase.storage.from('avatars').move('public/avatar1.png', 'private/avatar2.png', {2  destinationBucket: 'avatars2',3})
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/empty-a-bucket

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## JavaScript: Initializing | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/initializing?example=react-native-options-async-storage

---

## Streaming Speech with ElevenLabs | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/elevenlabs-generate-speech-stream

**Contents:**
- Streaming Speech with ElevenLabs
- Generate and stream speech through Supabase Edge Functions. Store speech in Supabase Storage and cache responses via built-in CDN.
- Introduction#
- Requirements#
- Setup#
  - Create a Supabase project locally#
  - Configure the storage bucket#
  - Configure background tasks for Supabase Edge Functions#
  - Create a Supabase Edge Function for speech generation#
  - Set up the environment variables#

Streaming Speech with ElevenLabs

Generate and stream speech through Supabase Edge Functions. Store speech in Supabase Storage and cache responses via built-in CDN.

In this tutorial you will learn how to build an edge API to generate, stream, store, and cache speech using Supabase Edge Functions, Supabase Storage, and ElevenLabs text to speech API.

Find the example project on GitHub.

After installing the Supabase CLI, run the following command to create a new Supabase project locally:

You can configure the Supabase CLI to automatically generate a storage bucket by adding this configuration in the config.toml file:

Upon running supabase start this will create a new storage bucket in your local Supabase project. Should you want to push this to your hosted Supabase project, you can run supabase seed buckets --linked.

To use background tasks in Supabase Edge Functions when developing locally, you need to add the following configuration in the config.toml file:

When running with per_worker policy, Function won't auto-reload on edits. You will need to manually restart it by running supabase functions serve.

Create a new Edge Function by running the following command:

If you're using VS Code or Cursor, select y when the CLI prompts "Generate VS Code settings for Deno? [y/N]"!

Within the supabase/functions directory, create a new .env file and add the following variables:

The project uses a couple of dependencies:

Since Supabase Edge Function uses the Deno runtime, you don't need to install the dependencies, rather you can import them via the npm: prefix.

In your newly created supabase/functions/text-to-speech/index.ts file, add the following code:

To run the function locally, run the following commands:

Once the local Supabase stack is up and running, run the following command to start the function and observe the logs:

Navigate to http://127.0.0.1:54321/functions/v1/text-to-speech?text=hello%20world to hear the function in action.

Afterwards, navigate to http://127.0.0.1:54323/project/default/storage/buckets/audio to see the audio file in your local Supabase Storage bucket.

If you haven't already, create a new Supabase account at database.new and link the local project to your Supabase account:

Once done, run the following command to deploy the function:

Now that you have all your secrets set locally, you can run the following command to set the secrets in your Supabase project:

The function is designed in a way that it can be used directly as a source for an <audio> element.

You can find an example frontend implementation in the complete code example on GitHub.

**Examples:**

Example 1 (unknown):
```unknown
1supabase init
```

Example 2 (unknown):
```unknown
1[storage.buckets.audio]2public = false3file_size_limit = "50MiB"4allowed_mime_types = ["audio/mp3"]5objects_path = "./audio"
```

Example 3 (unknown):
```unknown
1[edge_runtime]2policy = "per_worker"
```

Example 4 (unknown):
```unknown
1supabase functions new text-to-speech
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/retrieve-object-info

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/get-details-of-a-bucket

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---
