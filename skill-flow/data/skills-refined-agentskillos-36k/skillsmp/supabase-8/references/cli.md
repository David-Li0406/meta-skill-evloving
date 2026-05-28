# Supabase - Cli

**Pages:** 3

---

## Supabase CLI config | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development/cli/config

**Contents:**
- Supabase CLI config
- General Config#
  - project_id#
- Auth Config#
  - auth.enabled#
  - auth.site_url#
  - auth.additional_redirect_urls#
  - auth.jwt_expiry#
  - auth.enable_manual_linking#
  - auth.enable_refresh_token_rotation#

A supabase/config.toml file is generated after running supabase init.

You can edit this file to change the settings for your locally running project. After you make changes, you will need to restart using supabase stop and then supabase start for the changes to take effect.

A string used to distinguish different Supabase projects on the same host. Defaults to the working directory name when running supabase init.

Enable the local GoTrue service.

The base URL of your website. Used as an allow-list for redirects and for constructing URLs used in emails.

A list of exact URLs that auth providers are permitted to redirect to post authentication.

How long tokens are valid for, in seconds. Defaults to 3600 (1 hour), maximum 604,800 seconds (one week).

Allow testing manual linking of accounts

If disabled, the refresh token will never expire.

Allows refresh tokens to be reused after expiry, up to the specified interval in seconds. Requires enable_refresh_token_rotation = true.

Number of emails that can be sent per hour. Requires auth.email.smtp to be enabled.

Number of SMS messages that can be sent per hour. Requires auth.sms to be enabled.

Number of anonymous sign-ins that can be made per hour per IP address. Requires enable_anonymous_sign_ins = true.

Number of sessions that can be refreshed in a 5 minute interval per IP address.

Number of sign up and sign-in requests that can be made in a 5 minute interval per IP address (excludes anonymous users).

Number of OTP / Magic link verifications that can be made in a 5 minute interval per IP address.

Allow/disallow new user signups to your project.

Allow/disallow anonymous sign-ins to your project.

Allow/disallow new user signups via email to your project.

If enabled, a user will be required to confirm any email change on both the old, and new email addresses. If disabled, only the new email is required to confirm.

If enabled, users need to confirm their email address before signing in.

If enabled, requires the user's current password to be provided when changing to a new password.

The minimum amount of time that must pass between email requests. Helps prevent email spam by limiting how frequently emails can be sent. Example values: "1m", "1h", "24h"

The length of the OTP code to be sent in emails. Must be between 6 and 10 digits.

The expiry time for an OTP code in seconds. Default is 3600 seconds (1 hour).

Hostname or IP address of the SMTP server.

Port number of the SMTP server.

Username for authenticating with the SMTP server.

Password for authenticating with the SMTP server.

Email used as the sender for emails sent from the application.

Display name used as the sender for emails sent from the application.

The full list of email template types are:

The full list of email template types are:

Determines whether or not to send email notifications for the given type.

The full list of email notification types are:

The subject for the given email notification type.

The full list of email notification types are:

The relative path to the content template for the given email notification type.

The full list of email notification types are:

Allow/disallow new user signups via SMS to your project.

If enabled, users need to confirm their phone number before signing in.

Use pre-defined map of phone number to OTP for testing.

Use an external SMS provider. The full list of providers are:

Twilio Message Service SID

DO NOT commit your Twilio auth token to git. Use environment variable substitution instead.

MessageBird Originator

MessageBird Access Key

DO NOT commit your MessageBird access key to git. Use environment variable substitution instead.

DO NOT commit your TextLocal API key to git. Use environment variable substitution instead.

DO NOT commit your Vonage API secret to git. Use environment variable substitution instead.

Use an external OAuth provider. The full list of providers are:

Client ID for the external OAuth provider.

Client secret for the external OAuth provider.

DO NOT commit your OAuth provider secret to git. Use environment variable substitution instead.

The base URL used for constructing the URLs to request authorization and access tokens. Used by gitlab and keycloak. For gitlab it defaults to https://gitlab.com. For keycloak you need to set this to your instance, for example: https://keycloak.example.com/realms/myrealm .

The URI a OAuth2 provider will redirect to with the code and state values.

Disables nonce validation during OIDC authentication flow for the specified provider. Enable only when client libraries cannot properly handle nonce verification. Be aware that this reduces security by allowing potential replay attacks with stolen ID tokens.

Enable Auth Hook. Possible values for hook_name are: custom_access_token, send_sms, send_email, mfa_verification_attempt, and password_verification_attempt.

URI of hook to invoke. Should be a http or https function or Postgres function taking the form: pg-functions://<database>/<schema>/<function-name>. For example, pg-functions://postgres/auth/custom-access-token-hook.

Configure when using a HTTP Hooks. Takes a list of base64 comma separated values to allow for secret rotation. Currently, Supabase Auth uses only the first value in the list.

Enable TOTP enrollment for multi-factor authentication.

Enable TOTP verification for multi-factor authentication.

Control how many MFA factors can be enrolled at once per user.

Enable Phone enrollment for multi-factor authentication.

Length of OTP code sent when using phone multi-factor authentication

The minimum amount of time that must pass between phone requests. Helps prevent spam by limiting how frequently messages can be sent. Example values: "10s", "20s", "1m"

Length of OTP sent when using phone multi-factor authentication

Enable Phone verification for multi-factor authentication.

Enable WebAuthn enrollment for multi-factor authentication.

Enable WebAuthn verification for multi-factor authentication.

Force log out after the specified duration. Sample values include: '50m', '20h'.

Force log out if the user has been inactive longer than the specified duration. Sample values include: '50m', '20h'.

Enable third party auth with AWS Cognito (Amplify)

User Pool ID for AWS Cognito (Amplify) that you are integrating with

User Pool region for AWS Cognito (Amplify) that you are integrating with. Example values: 'ap-southeast-1', 'us-east-1'

Enable third party auth with Auth0

Tenant Identifier for Auth0 instance that you are integrating with

Tenant region for Auth0 instance that you are integrating with

Enable third party auth with Firebase

Project ID for Firebase instance that you are integrating with

Enable the local PostgREST service.

Port to use for the API URL.

Schemas to expose in your API. Tables, views and functions in this schema will get API endpoints. public and storage are always included.

Extra schemas to add to the search_path of every request. public is always included.

The maximum number of rows returned from a view, table, or stored procedure. Limits payload size for accidental or malicious requests.

Port to use for the local database URL.

Port to use for the local shadow database.

The database major version to use. This has to be the same as your remote database's. Run SHOW server_version; on the remote database to check.

Enable the local PgBouncer service.

Port to use for the local connection pooler.

Specifies when a server connection can be reused by other clients. Configure one of the supported pooler modes: transaction, session.

How many server connections to allow per user/database pair.

Sets the planner's assumption about the effective size of the disk cache. This is a query planner parameter that doesn't affect actual memory allocation.

Specifies the amount of memory to be used by logical decoding, before writing data to local disk.

Specifies the maximum amount of memory to be used by maintenance operations, such as VACUUM, CREATE INDEX, and ALTER TABLE ADD FOREIGN KEY.

Determines the maximum number of concurrent connections to the database server. Note: Changing this parameter requires a database restart.

Controls the average number of object locks allocated for each transaction. Note: Changing this parameter requires a database restart.

Sets the maximum number of parallel workers that can be started by a single utility command.

Sets the maximum number of parallel workers that the system can support. Note: Changing this parameter requires a database restart.

Sets the maximum number of parallel workers that can be started by a single Gather or Gather Merge node.

Specifies the maximum number of replication slots that the server can support. Note: Changing this parameter requires a database restart.

Specifies the maximum size of WAL files that replication slots are allowed to retain in the pg_wal directory.

Sets the maximum delay before canceling queries when a hot standby server is processing archived WAL data.

Sets the maximum delay before canceling queries when a hot standby server is processing streamed WAL data.

Sets the maximum size of WAL files that the system will keep in the pg_wal directory.

Specifies the maximum number of concurrent connections from standby servers or streaming base backup clients. Note: Changing this parameter requires a database restart.

Sets the maximum number of background processes that the system can support. Note: Changing this parameter requires a database restart.

Controls whether triggers and rewrite rules are enabled. Valid values are: "origin", "replica", or "local".

Sets the amount of memory the database server uses for shared memory buffers. Note: Changing this parameter requires a database restart.

Abort any statement that takes more than the specified amount of time.

Sets the maximum size of the query string that will be tracked in pg_stat_activity.current_query field. Note: Changing this parameter requires a database restart.

Record commit time of transactions. Note: Changing this parameter requires a database restart.

Specifies the minimum size of past log file segments kept in the pg_wal directory.

Terminate replication connections that are inactive for longer than this amount of time.

Specifies the amount of memory to be used by internal sort operations and hash tables before writing to temporary disk files.

Maximum number of client connections allowed.

Enables running seeds when starting or resetting the database.

An array of files or glob patterns to find seeds in.

Enable the local Supabase Studio dashboard.

Port to use for Supabase Studio.

External URL of the API server that frontend connects to.

OpenAI API key used for AI features in the Studio dashboard. DO NOT commit your OpenAI API key to git. Use environment variable substitution instead.

Enable the local Realtime service.

Bind realtime via either IPv4 or IPv6. (default: IPv6)

Enable the local Storage service.

The maximum file size allowed for all buckets in the project.

Enable public access to the bucket.

The maximum file size allowed (e.g. "5MB", "500KB").

The list of allowed MIME types for objects in the bucket.

The local directory to upload objects to the bucket.

Enable the local Edge Runtime service for Edge Functions.

Configure the request handling policy for Edge Functions. Available options:

Port to attach the Chrome inspector for debugging Edge Functions.

Controls whether a function is deployed or served. When set to false, the function will be skipped during deployment and won't be served locally. This is useful for disabling demo functions or temporarily disabling a function without removing its code.

By default, when you deploy your Edge Functions or serve them locally, it will reject requests without a valid JWT in the Authorization header. Setting this configuration changes the default behavior.

Note that the --no-verify-jwt flag overrides this configuration.

Specify the Deno import map file to use for the Function. When not specified, defaults to supabase/functions/<function_name>/deno.json.

Note that the --import-map flag overrides this configuration.

Specify a custom entrypoint path for the function relative to the project root. When not specified, defaults to supabase/functions/<function_name>/index.ts.

Specify an array of static files to be bundled with the function. Supports glob patterns.

NOTE: only file paths within functions directory are supported at the moment.

Enable the local Logflare service.

Port to the local Logflare service.

Port to the local syslog ingest service.

Configure one of the supported backends:

Automatically enable webhook features on each new created branch Note: This is an experimental feature and may change in future releases.

Configures Postgres storage engine to use OrioleDB with S3 support. Note: This is an experimental feature and may change in future releases.

Configures S3 bucket URL for OrioleDB storage. Format example: <bucket_name>.s3-<region>.amazonaws.com Note: This is an experimental feature and may change in future releases.

Configures S3 bucket region for OrioleDB storage. Example: us-east-1 Note: This is an experimental feature and may change in future releases.

Configures AWS_ACCESS_KEY_ID for S3 bucket access. DO NOT commit your AWS access key to git. Use environment variable substitution instead. Note: This is an experimental feature and may change in future releases.

Configures AWS_SECRET_ACCESS_KEY for S3 bucket access. DO NOT commit your AWS secret key to git. Use environment variable substitution instead. Note: This is an experimental feature and may change in future releases.

Enable the local InBucket service.

Port to use for the email testing server web interface.

Emails sent with the local dev setup are not actually sent - rather, they are monitored, and you can view the emails that would have been sent from the web interface.

Port to use for the email testing server SMTP port.

Emails sent with the local dev setup are not actually sent - rather, they are monitored, and you can view the emails that would have been sent from the web interface.

If set, you can access the SMTP server from this port.

Port to use for the email testing server POP3 port.

Emails sent with the local dev setup are not actually sent - rather, they are monitored, and you can view the emails that would have been sent from the web interface.

If set, you can access the POP3 server from this port.

Email used as the sender for emails sent from the application.

Display name used as the sender for emails sent from the application.

The project reference ID for a specific persistent Supabase branch. This ID is used to configure branch-specific settings in your config.toml file for branches deployments. All other configuration options available in the root config are also supported in the remotes block. For example, you can specify branch-specific database settings like so:

**Examples:**

Example 1 (py):
```py
1[auth.sms.test_otp]
24152127777 = "123456"
```

Example 2 (py):
```py
1[api]
2port = 54321
```

Example 3 (py):
```py
1[functions.my_function]
2entrypoint = "path/to/custom/function.ts"
```

Example 4 (py):
```py
1[functions.my_function]
2static_files = [ "./functions/MY_FUNCTION_NAME/*.html", "./functions/MY_FUNCTION_NAME/custom.wasm" ]
```

---

## Local Development & CLI | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development

**Contents:**
- Local Development & CLI
- Learn how to develop locally and use the Supabase CLI
- Quickstart#
- Local development#
- CLI#

Local Development & CLI

Learn how to develop locally and use the Supabase CLI

Develop locally while running the Supabase stack on your machine.

As a prerequisite, you must install a container runtime compatible with Docker APIs.

Install the Supabase CLI:

In your repo, initialize the Supabase project:

Start the Supabase stack:

View your local Supabase instance at http://localhost:54323.

If your local development machine is connected to an untrusted public network, you should create a separate docker network and bind to 127.0.0.1 before starting the local development stack. This restricts network access to only your localhost machine.

You should never expose your local development stack publicly.

Local development with Supabase allows you to work on your projects in a self-contained environment on your local machine. Working locally has several advantages:

To get started with local development, you'll need to install the Supabase CLI and Docker. The Supabase CLI allows you to start and manage your local Supabase stack, while Docker is used to run the necessary services.

Once set up, you can initialize a new Supabase project, start the local stack, and begin developing your application using local Supabase services. This includes access to a local Postgres database, Auth, Storage, and other Supabase features.

The Supabase CLI is a powerful tool that enables developers to manage their Supabase projects directly from the terminal. It provides a suite of commands for various tasks, including:

With the CLI, you can streamline your development workflow, automate repetitive tasks, and maintain consistency across different environments. It's an essential tool for both local development and CI/CD pipelines.

See the CLI Getting Started guide for more information.

**Examples:**

Example 1 (unknown):
```unknown
1npm install supabase --save-dev
```

Example 2 (unknown):
```unknown
1npx supabase init
```

Example 3 (unknown):
```unknown
1npx supabase start
```

Example 4 (unknown):
```unknown
1docker network create -o 'com.docker.network.bridge.host_binding_ipv4=127.0.0.1' local-network2npx supabase start --network-id local-network
```

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting?products=cli

---
