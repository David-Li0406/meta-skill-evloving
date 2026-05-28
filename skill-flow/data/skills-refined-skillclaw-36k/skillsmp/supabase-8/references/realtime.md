# Supabase - Realtime

**Pages:** 17

---

## Realtime Quotas | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/quotas

**Contents:**
- Realtime Quotas
- Quotas by plan#
- Quota errors#
      - Realtime Inspector
  - too_many_channels#
  - too_many_connections#
  - too_many_joins#
  - tenant_events#
- Postgres changes payload quota#

Our cluster supports millions of concurrent connections and message throughput for production workloads.

Upgrade your plan to increase your quotas. Without a spend cap, or on an Enterprise plan, some quotas are still in place to protect budgets. All quotas are configurable per project. Contact support if you need your quotas increased.

Beyond the Free and Pro Plan you can customize your quotas by contacting support.

When you exceed a quota, errors will appear in the backend logs and client-side messages in the WebSocket connection.

You can use the Realtime Inspector to reproduce an error and share those connection details with Supabase support.

Some quotas can cause a Channel join to be refused. Realtime will reply with one of the following WebSocket messages:

Too many channels currently joined for a single connection.

Too many total concurrent connections for a project.

Too many Channel joins per second.

Connections will be disconnected if your project is generating too many messages per second. supabase-js will reconnect automatically when the message throughput decreases below your plan quota. An event is a WebSocket message delivered to, or sent from a client.

When this quota is reached, the new and old record payloads only include the fields with a value size of less than or equal to 64 bytes.

---

## Settings | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/settings

**Contents:**
- Settings
- Realtime Settings that allow you to configure your Realtime usage.
- Settings#

Realtime Settings that allow you to configure your Realtime usage.

All changes made in this screen will disconnect all your connected clients to ensure Realtime starts with the appropriate settings and all changes are stored in Supabase middleware.

You can set the following settings using the Realtime Settings screen in your Dashboard:

---

## Realtime | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime

**Contents:**
- Realtime
- Send and receive messages to connected clients.
- What can you build?#
- Examples#
- Resources#

Send and receive messages to connected clients.

Supabase provides a globally distributed Realtime service with the following features:

Check the Getting Started guide to get started.

Find the source code and documentation in the Supabase GitHub repository.

Realtime: Multiplayer Edition

---

## Supabase Docs | Realtime Troubleshooting

**URL:** https://supabase.com/docs/guides/realtime/troubleshooting

---

## Using Realtime Presence with Flutter | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/realtime-user-presence

**Contents:**
- Using Realtime Presence with Flutter

Using Realtime Presence with Flutter

Use Supabase Presence to display the currently online users on your Flutter application.

Displaying the list of currently online users is a common feature for real-time collaborative applications. Supabase Presence makes it easy to track users joining and leaving the session so that you can make a collaborative app.

---

## Realtime Protocol | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/protocol

**Contents:**
- Realtime Protocol
- WebSocket connection setup#
- Protocol messages#
- 1.0.0#
- 2.0.0#
  - Text frames#
  - Binary frames#
    - User Broadcast Push#
    - User Broadcast#
- Event types#

To start the connection we use the WebSocket URL, which for:

As an example, using websocat, you would run the following command in your terminal:

During this stage you can also set other URL params:

After connecting a phx_join event must be sent to the server to join a channel. The next sections outline the different messages types and events that are supported.

Messages can be serialized in different formats. The Realtime protocol supports two versions: 1.0.0 and 2.0.0.

Version 1.0.0 is extremely simple. It uses JSON as the serialization format for messages. The underlying WebSocket messages are all text frames.

Messages contain the following fields:

Version 2.0.0 uses text and binary WebSocket frames.

Text frames are always JSON encoded, but unlike version 1.0.0, they use a JSON array where the element order must be exactly:

The two special message types have a well defined binary format where the first byte defines the type of message. Both are used to send and receive broadcast events. See the client and server sent events for more details.

Messages for all events are encoded as text frames using JSON except with the broadcast event type which can happen on both text and binary frames.

This is the initial message required to join a channel. The client sends this message to the server to join a specific topic and configure the features it wants to use, such as Postgres changes, Presence, and Broadcast. The payload of the phx_join event contains the configuration options for the channel.

Example on protocol version 2.0.0:

This message is sent by the client to leave a channel. It can be used to clean up resources or stop listening for events on that channel. Payload should be empty object.

Example on protocol version 2.0.0:

The heartbeat message should be sent at least every 25 seconds to avoid a connection timeout. Payload should be an empty object.

For heartbeat, the topic phoenix is used as this special message is not connected to a specific channel.

Example on protocol version 2.0.0:

Used to setup a new token to be used by Realtime for authentication and to refresh the token to prevent a private channel from closing when the token expires.

Example on protocol version 2.0.0:

Used to send a broadcast event to all clients in a channel.

The payload field contains the event name and the data to broadcast.

Example on protocol version 2.0.0:

See the User Broadcast Push section for the binary frame structure.

This message is a streamlined version of the text frame broadcast event that also supports non-JSON payloads. Below is the same example from the previous section, showing the binary frame structure with hexadecimal values for the header and plain text for the remaining fields:

The payload encoding is just a hint for the client to know if the payload should be treated as JSON or not.

Used to send presence metadata after joining a channel. The payload contains the presence information to be tracked by the server. This metadata is then sent back to all clients in the channel via presence_state and presence_diff events.

Example on protocol version 2.0.0:

This message is sent by the server to signal that the channel has been closed. Payload will be empty object.

Example on protocol version 2.0.0:

This message is sent by the server when an unexpected error occurs in the channel. Payload will be an empty object

The server sends these messages in response to client requests that require acknowledgment.

phx_join has a specific response structure outlined below.

Contains the status of the join request and any additional information requested in the phx_join payload.

Example on protocol version 2.0.0:

The server sends system messages to inform clients about the status of their Realtime channel subscriptions.

Example on protocol version 2.0.0:

This is the structure of broadcast events received by all clients subscribed to a channel. The payload field contains the event name and data that was broadcasted.

Example on protocol version 2.0.0:

See the User Broadcast section for the binary frame structure.

This message is a streamlined version of the text frame broadcast event that also supports non-JSON payloads. Below is the same example from the previous section, showing the binary frame structure with hexadecimal values for the header and plain text for the remaining fields:

The metadata field is JSON encoded. The payload encoding is just a hint for the client to know if the payload should be treated as JSON or not.

The server sends this message when a database change occurs in a subscribed schema and table. The payload contains the details of the change, including the schema, table, event type, and the new and old records.

After joining, the server sends a presence_state message to a client with presence information. The payload field contains keys, where each key represents a client and its value is a JSON object containing information about that client. The key is defined by the client when joining the channel. If not specified, a UUID is automatically generated.

Example on protocol version 2.0.0:

After a change to the presence state, such as a client joining or leaving, the server sends a presence_diff message to update the client's view of the presence state. The payload field contains two keys, joins and leaves, which represent clients that have joined and left, respectively. Each key is either specified by the client when joining the channel or automatically generated as a UUID.

Example on protocol version 2.0.0:

**Examples:**

Example 1 (unknown):
```unknown
1# With Supabase2websocat "wss://<PROJECT_REF>.supabase.co/realtime/v1/websocket?apikey=<API_KEY>"34# With self-hosted5websocat "wss://<HOST>:<PORT>/socket/websocket?apikey=<API_KEY>"
```

Example 2 (unknown):
```unknown
1{2  "topic": "realtime:presence-room",3  "event": "phx_join",4  "payload": {5    "config": {6      "broadcast": {7        "ack": false,8        "self": false9      },10      "presence": {11        "enabled": false12      },13      "private": false14    }15  },16  "ref": "1",17  "join_ref": "1"18}
```

Example 3 (unknown):
```unknown
1[2  "1",3  "1",4  "realtime:presence-room",5  "phx_join",6  {7    "config": {8      "broadcast": {9        "ack": false,10        "self": false11      },12      "presence": {13        "enabled": false14      },15      "private": false16    }17  }18]
```

Example 4 (unknown):
```unknown
10                   1                   2                   32 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 13+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+4|  Type (0x03)  | Join Ref Size |   Ref Size    |  Topic Size   |5+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+6|User Event Size| Metadata Size | Payload Enc.  |  Join Ref ... |7+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+8|                      Ref (variable length)                    |9+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+10|                     Topic (variable length)                   |11+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+12|                  User Event (variable length)                 |13+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+14|                   Metadata (variable length)                  |15+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+16|                User Payload (variable length)                 |17+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

---

## Manage Realtime Peak Connections usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/realtime-peak-connections

**Contents:**
- Manage Realtime Peak Connections usage
- What you are charged for#
  - Example#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Pricing#
- Billing examples#
  - Within quota#
  - Exceeding quota#

Manage Realtime Peak Connections usage

Realtime Peak Connections are measured by tracking the highest number of concurrent connections for each project during the billing cycle. Regardless of fluctuations, only the peak count per project is used for billing, and the totals from all projects are summed. Only successful connections are counted, connection attempts are not included.

For simplicity, this example assumes a billing cycle of only three days.

Total billed connections: 100 (Project A) + 150 (Project B) = 250 connections

Realtime Peak Connections are billed using Package pricing, with each package representing 1,000 peak connections. If your usage falls between two packages, you are billed for the next whole package.

For simplicity, let's assume a package size of 1,000 and a charge of $10 per package with no quota.

Usage is shown as "Realtime Peak Connections" on your invoice.

$10 per 1,000 peak connections. You are only charged for usage exceeding your subscription plan's quota.

The organization's connections are within the quota, so no charges apply.

The organization's connections exceed the quota by 1,200, incurring charges for this additional usage.

You can view Realtime Peak Connections usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Realtime Peak Connections section, you can see the usage for the selected time period.

---

## Manage Realtime Messages usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/realtime-messages

**Contents:**
- Manage Realtime Messages usage
- What you are charged for#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Pricing#
- Billing examples#
  - Within quota#
  - Exceeding quota#
- View usage#

Manage Realtime Messages usage

You are charged for the number of messages going through Supabase Realtime throughout the billing cycle. Includes database changes, Broadcast and Presence.

Database changes Each database change counts as one message per client that listens to the event. For example, if a database change occurs and 5 clients listen to that database event, it counts as 5 messages.

Broadcast Each broadcast message counts as one message sent plus one message per subscribed client that receives it. For example, if you broadcast a message and 4 clients listen to it, it counts as 5 messages—1 sent and 4 received.

Realtime Messages are billed using Package pricing, with each package representing 1 million messages. If your usage falls between two packages, you are billed for the next whole package.

For simplicity, let's assume a package size of 1,000,000 and a charge of $2.50 per package without quota.

Usage is shown as "Realtime Messages" on your invoice.

$2.50 per 1 million messages. You are only charged for usage exceeding your subscription plan's quota.

The organization's Realtime messages are within the quota, so no charges apply.

The organization's Realtime messages exceed the quota by 3.5 million, incurring charges for this additional usage.

You can view Realtime Messages usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Realtime Messages section, you can see the usage for the selected time period.

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-update-realtime-config

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

## Realtime Concepts | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/concepts

**Contents:**
- Realtime Concepts
- Concepts#
- Channels#
- Database resources#
  - Database connections#
  - Replication slots#
  - Schema and tables#
  - Functions#

There are several concepts and terminology that is useful to understand how Realtime works.

Channels are the foundation of Realtime. Think of them as rooms where clients can communicate and listen to events. Channels are identified by a topic name and if they are public or private.

For private channels, you need to use Realtime Authorization to control access to the channel and if they are able to send messages. For public channels, any user can subscribe to the channel, send and receive messages.

You can set your project to use only private channels or both private and public channels in the Realtime Settings.

If you have a private channel and a public channel with the same topic name, Realtime sees them as unique channels and won't send messages between them.

Realtime uses several database connections to perform several operations. As a user, you are able to tune some of them using Realtime Settings.

Realtime uses several database connections to perform various operations. You can configure some of these connections through Realtime Settings.

The connections include:

The number of connections varies based on your compute add-on size and configuration. The following table shows the default connection pool sizes for different compute add-on variants:

You can customize Authorization Pool Size through the Database connection pool size parameter in your Realtime configuration. If not specified, the default values shown in the table will be used.

Realtime also uses, at maximum, 2 replication slots.

The realtime schema creates the following tables:

Realtime has a cleanup process that will delete tables older than 3 days.

Realtime creates two functions on your database:

**Examples:**

Example 1 (unknown):
```unknown
1create table realtime.messages (2topic text not null, -- The topic of the message3extension text not null, -- The extension of the message (presence, broadcast)4payload jsonb null, -- The payload of the message5event text null, -- The event of the message6private boolean null default false, -- If the message is going to use a private channel7updated_at timestamp without time zone not null default now(), -- The timestamp of the message8inserted_at timestamp without time zone not null default now(), -- The timestamp of the message9id uuid not null default gen_random_uuid (), -- The id of the message10constraint messages_pkey primary key (id, inserted_at)) partition by RANGE (inserted_at);
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-get-realtime-config

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

## Using Realtime with Next.js | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/realtime-with-nextjs

**Contents:**
- Using Realtime with Next.js

Using Realtime with Next.js

In this guide, we explore the best ways to receive real-time Postgres changes with your Next.js application. We'll show both client and server side updates, and explore which option is best.

---

## Operational Error Codes | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/error_codes

**Contents:**
- Operational Error Codes
- List of operational codes to help understand your deployment and usage.

Operational Error Codes

List of operational codes to help understand your deployment and usage.

The number of channels you can create has reached its limit.

The rate of joins per second from your clients has reached the channel limits.

Database is initializing connection.

The number of connected clients has reached its limit.

Database had connection issues and connection was not able to be established.

Realtime was not able to connect to the tenant's database due to not having enough available connections.

Verify your database connection limits.

Error when trying to authorize the WebSocket connection.

Verify user information on connect.

Error when trying to connect to the WebSocket server.

Verify user information on connect.

Error executing a database transaction in tenant database.

Error when calling another realtime node.

Error when starting the Postgres CDC extension which is used for Postgres Changes.

Error when starting the Postgres CDC stream which is used for Postgres Changes.

The number of connections you have set for Realtime are not enough to handle your current use case.

Connection against Tenant database is still starting.

JWT exp claim value it's incorrect.

Scheduled task for realtime.message cleanup was unable to run.

JWT signature was not able to be validated.

Token received does not comply with the JWT format.

Check to see if we require to run migrations fails.

Error when running the migrations against the Tenant database that are required by Realtime.

Error when creating partitions for realtime.messages.

Error when pooling the replication slot.

Error when preparing the replication slot.

The configuration provided to Realtime on connect will not be able to provide you any Postgres Changes.

Verify your configuration on channel startup as you might not have your tables properly registered.

Realtime has been disabled for the tenant.

Realtime is a distributed application and this means that one the system is unable to communicate with one of the distributed nodes.

Realtime is currently restarting.

Postgres changes still waiting to be subscribed.

Maximum number of WAL senders reached in tenant database.

The replication slot is being used by another transaction.

Error on RLS policy used for authorization.

Error when starting the replication and listening of errors for database broadcasting.

Error when trying to delete a subscription for postgres changes.

Our framework to syncronize processes has failed to properly startup a connection to the database.

The table you are trying to listen to has spaces in its name which we are unable to support.

Change the table name to not have spaces in it.

The tenant you are trying to connect to does not exist.

Verify the tenant name you are trying to connect to exists in the realtime.tenants table.

RPC request within the Realtime server has timed out.

You are trying to use Realtime without a topic name set.

Error when trying to checkout a connection from the tenant pool.

Error when trying to check the processes on a remote node.

Unable to connect to Project database.

Realtime was not able to connect to the tenant's database.

Error when trying to create a counter to track rate limits for a tenant.

Error when trying to decrement a counter to track rate limits for a tenant.

Error when trying to delete subscriptions that are no longer being used.

Error when trying to delete a tenant.

An error were we are not handling correctly the response to be sent to the end user.

Error when trying to find a counter to track rate limits for a tenant.

Error when trying to increment a counter to track rate limits for a tenant.

Unable to LISTEN for notifications against the Tenant Database.

Payload sent in NOTIFY operation was JSON parsable.

Error when setting up Authorization Policies.

Error when trying to subscribe to Postgres changes.

Error when handling track presence for this socket.

Error when trying to update a counter to track rate limits for a tenant.

Unauthorized access to Realtime channel.

Unhandled message received by a Realtime process.

An unknown data type was processed by the Realtime system.

An error we are not handling correctly was triggered on a channel.

An error we are not handling correctly was triggered on a controller.

Presence event type not recognized by service.

Received a HTTP request with a body that was not able to be processed by the endpoint.

---

## Broadcast | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/broadcast

**Contents:**
- Broadcast
- Send low-latency messages using the client libs, REST, or your Database.
- How Broadcast works#
- Subscribe to messages#
  - Initialize the client#
      - Changes to API keys
  - Receiving Broadcast messages#
- Send messages#
  - Broadcast using the client libraries#
  - Broadcast from the Database#

Send low-latency messages using the client libs, REST, or your Database.

You can use Realtime Broadcast to send low-latency messages between users. Messages can be sent using the client libraries, REST APIs, or directly from your database.

The way Broadcast works changes based on the channel you are using:

The public flag (the last argument in realtime.send(payload, event, topic, is_private)) only affects who can subscribe to the topic not who can read messages from the database.

However, regardless of whether it's public or private, the Realtime service connects to your database as the authenticated Supabase Admin role.

For Authorization we do insert a message and try to read it and then we it back as way to verify that the RLS policies set by the user are being respected by the user joining the channel but this messages won't be sent to the user. You can read more about it in the Authorization docs

You can use the Supabase client libraries to receive Broadcast messages.

Get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

You can provide a callback for the broadcast channel to receive messages. This example will receive any broadcast messages that are sent to test-channel:

You can use the Supabase client libraries to send Broadcast messages.

This feature is in Public Beta. Submit a support ticket if you have any issues.

All the messages sent using Broadcast from the Database are stored in realtime.messages table and will be deleted after 3 days.

You can send messages directly from your database using the realtime.send() function:

The realtime.send function in the database includes a flag that determines whether the broadcast is private or public, and client channels also have the same configuration. For broadcasts to work correctly, these settings must match a public broadcast will only reach public channels, and a private broadcast will only reach private ones.

By default, all database broadcasts are private, meaning clients must authenticate to receive them. If the database sends a public message but the client subscribes to a private channel, the message won't be delivered since private channels only accept signed, authenticated messages.

It's a common use case to broadcast messages when a record is created, updated, or deleted. We provide a helper function specific to this use case, realtime.broadcast_changes(). For more details, check out the Subscribing to Database Changes guide.

You can send a Broadcast message by making an HTTP request to Realtime servers.

You can pass configuration options while initializing the Supabase Client.

By default, broadcast messages are only sent to other clients. You can broadcast messages back to the sender by setting Broadcast's self parameter to true.

You can confirm that the Realtime servers have received your message by setting Broadcast's ack config to true.

Use this to guarantee that the server has received the message before resolving channelD.send's promise. If the ack config is not set to true when creating the channel, the promise returned by channelD.send will resolve immediately.

You can also send a Broadcast message by making an HTTP request to Realtime servers. This is useful when you want to send messages from your server or client without having to first establish a WebSocket connection.

This is currently available only in the Supabase JavaScript client version 2.37.0 and later.

Broadcast Changes allows you to trigger messages from your database. To achieve it Realtime is directly reading your WAL (Write Append Log) file using a publication against the realtime.messages table so whenever a new insert happens a message is sent to connected users.

It uses partitioned tables per day which allows the deletion your previous messages in a performant way by dropping the physical tables of this partitioned table. Tables older than 3 days old are deleted.

Broadcasting from the database works like a client-side broadcast, using WebSockets to send JSON packages. Realtime Authorization is required and enabled by default to protect your data.

The database broadcast feature provides two functions to help you send messages:

The realtime.send function provides the most flexibility by allowing you to broadcast messages from your database without a specific format. This allows you to use database broadcast for messages that aren't necessarily tied to the shape of a Postgres row change.

Realtime Authorization is required and enabled by default. To allow your users to listen to messages from topics, create a RLS (Row Level Security) policy:

See the Realtime Authorization docs to learn how to set up more specific policies.

First, set up a trigger function that uses realtime.broadcast_changes to insert an event whenever it is triggered. The event is set up to include data on the schema, table, operation, and field changes that triggered it.

For this example use case, we want to have a topic with the name topic:<record id> to which we're going to broadcast events.

Of note are the Postgres native trigger special variables used:

You can read more about them in this guide.

Next, set up a trigger so the function runs whenever your target table has a change.

As you can see, it will be broadcasting all operations so our users will receive events when records are inserted, updated or deleted from public.your_table .

Finally, client side will requires to be set up to listen to the topic topic:<record id> to receive the events.

This feature is currently in Public Alpha. If you have any issues submit a support ticket.

Broadcast Replay enables private channels to access messages that were sent earlier. Only messages published via Broadcast From the Database are available for replay.

You can configure replay with the following options:

This is currently available only in the Supabase JavaScript client version 2.74.0 and later.

A few common use cases for Broadcast Replay include:

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const SUPABASE_URL = 'https://<project>.supabase.co'4const SUPABASE_KEY = '<sb_publishable_... or anon key>'56const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)
```

Example 2 (javascript):
```javascript
1// Join a room/topic. Can be anything except for 'realtime'.2const myChannel = supabase.channel('test-channel')34// Simple function to log any messages we receive5function messageReceived(payload) {6  console.log(payload)7}89// Subscribe to the Channel10myChannel11  .on(12    'broadcast',13    { event: 'shout' }, // Listen for "shout". Can be "*" to listen to all events14    (payload) => messageReceived(payload)15  )16  .subscribe()
```

Example 3 (javascript):
```javascript
1const myChannel = supabase.channel('test-channel')23/**4 * Sending a message before subscribing will use HTTP5 */6myChannel7  .send({8    type: 'broadcast',9    event: 'shout',10    payload: { message: 'Hi' },11  })12  .then((resp) => console.log(resp))131415/**16 * Sending a message after subscribing will use Websockets17 */18myChannel.subscribe((status) => {19  if (status !== 'SUBSCRIBED') {20    return null21  }2223  myChannel.send({24    type: 'broadcast',25    event: 'shout',26    payload: { message: 'Hi' },27  })28})
```

Example 4 (unknown):
```unknown
1select2  realtime.send(3    jsonb_build_object('hello', 'world'), -- JSONB Payload4    'event', -- Event name5    'topic', -- Topic6    false -- Public / Private flag7  );
```

---

## Realtime Architecture | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/architecture

**Contents:**
- Realtime Architecture
- Elixir & Phoenix#
- Channels#
- Global cluster#
- Connecting to a database#
- Broadcast from Postgres#
- Streaming the Write-Ahead Log#

Realtime Architecture

Realtime is a globally distributed Elixir cluster. Clients can connect to any node in the cluster via WebSockets and send messages to any other client connected to the cluster.

Realtime is written in Elixir, which compiles to Erlang, and utilizes many tools the Phoenix Framework provides out of the box.

Phoenix is fast and able to handle millions of concurrent connections.

Phoenix can handle many concurrent connections because Elixir provides lightweight processes (not OS processes) to work with.

Client-facing WebSocket servers need to handle many concurrent connections. Elixir & Phoenix let the Supabase Realtime cluster do this easily.

Channels are implemented using Phoenix Channels which uses Phoenix.PubSub with the default Phoenix.PubSub.PG2 adapter.

The PG2 adapter utilizes Erlang process groups to implement the PubSub model where a publisher can send messages to many subscribers.

Presence is an in-memory key-value store backed by a CRDT. When a user is connected to the cluster the state of that user is sent to all connected Realtime nodes.

Broadcast lets you send a message from any connected client to a Channel. Any other client connected to that same Channel will receive that message.

This works globally. A client connected to a Realtime node in the United States can send a message to another client connected to a node in Singapore. Connect two clients to the same Realtime Channel and they'll all receive the same messages.

Broadcast is useful for getting messages to users in the same location very quickly. If a group of clients are connected to a node in Singapore, the message only needs to go to that Realtime node in Singapore and back down. If users are close to a Realtime node they'll get Broadcast messages in the time it takes to ping the cluster.

Thanks to the Realtime cluster, you (an amazing Supabase user) don't have to think about which regions your clients are connected to.

If you're using Broadcast, Presence, or streaming database changes, messages will always get to your users via the shortest path possible.

Realtime allows you to listen to changes from your Postgres database. When a new client connects to Realtime and initializes the postgres_changes Realtime Extension the cluster will connect to your Postgres database and start streaming changes from a replication slot.

Realtime knows the region your database is in, and connects to it from the closest region possible.

Every Realtime region has at least two nodes so if one node goes offline the other node should reconnect and start streaming changes again.

Realtime Broadcast sends messages when changes happen in your database. Behind the scenes, Realtime creates a publication on the realtime.messages table. It then reads the Write-Ahead Log (WAL) file for this table, and sends a message whenever an insert happens. Messages are sent as JSON packages over WebSockets.

The realtime.messages table is partitioned by day. This allows old messages to be deleted performantly, by dropping old partitions. Partitions are retained for 3 days before being deleted.

Broadcast uses Realtime Authorization by default to protect your data.

A Postgres logical replication slot is acquired when connecting to your database.

Realtime delivers changes by polling the replication slot and appending channel subscription IDs to each wal record.

Subscription IDs are Erlang processes representing underlying sockets on the cluster. These IDs are globally unique and messages to processes are routed automatically by the Erlang virtual machine.

After receiving results from the polling query, with subscription IDs appended, Realtime delivers records to those clients.

---

## Benchmarks | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/benchmarks

**Contents:**
- Benchmarks
- Scalability Benchmarks for Supabase Realtime.
- Methodology#
- Workloads#
- Results#
  - Broadcast: Using WebSockets#
  - Broadcast: Using the database#
  - Broadcast: Impact of payload size#
    - 1KB payload#
    - 10KB payload#

Scalability Benchmarks for Supabase Realtime.

This guide explores the scalability of Realtime's features: Broadcast, Presence, and Postgres Changes.

The metrics collected include: message throughput, latency percentiles, CPU and memory utilization, and connection success rates. Note that performance in production environments may vary based on factors such as network conditions, hardware specifications, and specific usage patterns.

The proposed workloads are designed to demonstrate Supabase Realtime's throughput and scalability. These benchmarks focus on core functionality and common usage patterns. The benchmarking results include the following workloads:

This workload evaluates the system's capacity to handle multiple concurrent WebSocket connections and sending Broadcast messages via the WebSocket. Each virtual user (VU) in the test:

This workload evaluates the system's capacity to send Broadcast messages from the database using the realtime.broadcast_changes function. Each virtual user (VU) in the test:

This workload tests the system's performance with different message payload sizes to understand how data volume affects throughput and latency. Each virtual user (VU) follows the same connection pattern as the broadcast test, but with varying message sizes:

Note: The final column shows results with reduced load (2,000 users) for the 50KB payload test, demonstrating how the system performs with larger payloads under different concurrency levels.

This workload demonstrates Realtime's capability to handle high-scale scenarios with a large number of concurrent users and broadcast channels. The test simulates a scenario where each user participates in group communications with periodic message broadcasts. Each virtual user (VU):

This workload demonstrates Realtime's capability to handle large amounts of new connections per second and channel joins per second with Authentication Row Level Security (RLS) enabled for these channels. The test simulates a scenario where large volumes of users connect to realtime and participate in auth protected communications. Each virtual user (VU):

Realtime systems usually require forethought because of their scaling dynamics. For the Postgres Changes feature, every change event must be checked to see if the subscribed user has access. For instance, if you have 100 users subscribed to a table where you make a single insert, it will then trigger 100 "reads": one for each user.

There can be a database bottleneck which limits message throughput. If your database cannot authorize the changes rapidly enough, the changes will be delayed until you receive a timeout.

Database changes are processed on a single thread to maintain the change order. That means compute upgrades don't have a large effect on the performance of Postgres change subscriptions. You can estimate the expected maximum throughput for your database below.

If you are using Postgres Changes at scale, you should consider using a separate "public" table without RLS and filters. Alternatively, you can use Realtime server-side only and then re-stream the changes to your clients using a Realtime Broadcast.

Enter your database settings to estimate the maximum throughput for your instance:

Don't forget to run your own benchmarks to make sure that the performance is acceptable for your use case.

Supabase continues to make improvements to Realtime's Postgres Changes. If you are uncertain about your use case performance, reach out using the Support Form. The support team can advise on the best solution for each use-case.

---

## Presence | Supabase Docs

**URL:** https://supabase.com/docs/guides/realtime/presence

**Contents:**
- Presence
- Share state between users with Realtime Presence.
- Usage#
  - How Presence works#
  - Initialize the client#
      - Changes to API keys
  - Sync and track state#
  - Sending state#
  - Stop tracking#
- Presence options#

Share state between users with Realtime Presence.

Let's explore how to implement Realtime Presence to track state between multiple users.

You can use the Supabase client libraries to track Presence state between users.

Presence lets each connected client publish a small piece of state—called a “presence payload”—to a shared channel. Supabase stores each client’s payload under a unique presence key and keeps a merged view of all connected clients.

When any client subscribes, disconnects, or updates their presence payload, Supabase triggers one of three events:

The complete presence state returned by presenceState() looks like this:

Get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Listen to the sync, join, and leave events triggered whenever any client joins or leaves the channel or changes their slice of state:

You can send state to all subscribers using track():

A client will receive state from any other client that is subscribed to the same topic (in this case room_01). It will also automatically trigger its own sync and join event handlers.

You can stop tracking presence using the untrack() method. This will trigger the sync and leave event handlers.

You can pass configuration options while initializing the Supabase Client.

By default, Presence will generate a unique UUIDv1 key on the server to track a client channel's state. If you prefer, you can provide a custom key when creating the channel. This key should be unique among clients.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "client_key_1": [{ "userId": 1, "typing": false }],3  "client_key_2": [{ "userId": 2, "typing": true }]4}
```

Example 2 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const SUPABASE_URL = 'https://<project>.supabase.co'4const SUPABASE_KEY = '<sb_publishable_... or anon key>'56const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)
```

Example 3 (javascript):
```javascript
1const roomOne = supabase.channel('room_01')23roomOne4  .on('presence', { event: 'sync' }, () => {5    const newState = roomOne.presenceState()6    console.log('sync', newState)7  })8  .on('presence', { event: 'join' }, ({ key, newPresences }) => {9    console.log('join', key, newPresences)10  })11  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {12    console.log('leave', key, leftPresences)13  })14  .subscribe()
```

Example 4 (javascript):
```javascript
1const roomOne = supabase.channel('room_01')23const userStatus = {4  user: 'user-1',5  online_at: new Date().toISOString(),6}78roomOne.subscribe(async (status) => {9  if (status !== 'SUBSCRIBED') { return }1011  const presenceTrackStatus = await roomOne.track(userStatus)12  console.log(presenceTrackStatus)13})
```

---
