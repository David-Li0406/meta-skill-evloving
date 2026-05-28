# Supabase - Edge Functions

**Pages:** 51

---

## Background Tasks | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/background-tasks

**Contents:**
- Background Tasks
- Run background tasks in an Edge Function outside of the request handler.
- Overview#
- Handling errors#
- Testing background tasks locally#

Run background tasks in an Edge Function outside of the request handler.

Edge Function instances can process background tasks outside of the request handler. Background tasks are useful for asynchronous operations like uploading a file to Storage, updating a database, or sending events to a logging service. You can respond to the request immediately and leave the task running in the background.

You can use EdgeRuntime.waitUntil(promise) to explicitly mark background tasks. The Function instance continues to run until the promise provided to waitUntil completes.

You can call EdgeRuntime.waitUntil in the request handler too. This will not block the request.

You can listen to the beforeunload event handler to be notified when the Function is about to be shut down.

We recommend using try/catch blocks within your background task function to handle errors.

You can also add an event listener to unhandledrejection to handle any promises without a rejection handler.

The maximum duration is capped based on the wall-clock, CPU, and memory limits. The function will shut down when it reaches one of these limits.

When testing Edge Functions locally with Supabase CLI, the instances are terminated automatically after a request is completed. This will prevent background tasks from running to completion.

To prevent that, you can update the supabase/config.toml with the following settings:

**Examples:**

Example 1 (javascript):
```javascript
1// Mark the asyncLongRunningTask's returned promise as a background task.2// ⚠️ We are NOT using `await` because we don't want it to block!3EdgeRuntime.waitUntil(asyncLongRunningTask())45Deno.serve(async (req) => {6  return new Response(...)7})
```

Example 2 (javascript):
```javascript
1Deno.serve(async (req) => {2  // Won't block the request, runs in background.3  EdgeRuntime.waitUntil(asyncLongRunningTask())45  return new Response(...)6})
```

Example 3 (javascript):
```javascript
1EdgeRuntime.waitUntil(asyncLongRunningTask())23// Use beforeunload event handler to be notified when function is about to shutdown4addEventListener('beforeunload', (ev) => {5  console.log('Function will be shutdown due to', ev.detail?.reason)6  // Save state or log the current progress7})89Deno.serve(async (req) => {10  return new Response(...)11})
```

Example 4 (javascript):
```javascript
1addEventListener('unhandledrejection', (ev) => {2  console.log('unhandledrejection', ev.reason)3  ev.preventDefault()4})
```

---

## Development Environment | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/development-environment

**Contents:**
- Development Environment
- Set up your local development environment for Edge Functions.
- Step 1: Install Deno CLI#
- Step 2: Set up your editor#
  - VSCode/Cursor (recommended)#
  - Multi-root workspaces#
- Recommended project structure#
- Essential CLI commands#
  - supabase start#
  - supabase functions serve [function-name]#

Development Environment

Set up your local development environment for Edge Functions.

Before getting started, make sure you have the Supabase CLI installed. Check out the CLI installation guide for installation methods and troubleshooting.

The Supabase CLI doesn't use the standard Deno CLI to serve functions locally. Instead, it uses its own Edge Runtime to keep the development and production environment consistent.

You can follow the Deno guide for setting up your development environment with your favorite editor/IDE.

The benefit of installing Deno separately is that you can use the Deno LSP to improve your editor's autocompletion, type checking, and testing. You can also use Deno's built-in tools such as deno fmt, deno lint, and deno test.

After installing, you should have Deno installed and available in your terminal. Verify with deno --version

Set up your editor environment for proper TypeScript support, autocompletion, and error detection.

Install the Deno extension from the VSCode marketplace

Option 1: Auto-generate (easiest) When running supabase init, select y when prompted "Generate VS Code settings for Deno? [y/N]"

Option 2: Manual setup

Create a .vscode/settings.json in your project root:

This configuration enables the Deno language server only for the supabase/functions folder, while using VSCode's built-in JavaScript/TypeScript language server for all other files.

The standard .vscode/settings.json setup works perfectly for projects where your Edge Functions live alongside your main application code. However, you might need multi-root workspaces if your development setup involves:

For this development workflow, create edge-functions.code-workspace:

You can find the complete example on GitHub.

It's recommended to organize your functions according to the following structure:

Get familiar with the most commonly used CLI commands for developing and deploying Edge Functions.

This command spins up your entire Supabase stack locally: database, auth, storage, and Edge Functions runtime. You're developing against the exact same environment you'll deploy to.

Develop a specific function with hot reloading. Your functions run at http://localhost:54321/functions/v1/[function-name]. When you save your file, you’ll see the changes instantly without having to wait.

Alternatively, use supabase functions serve to serve all functions at once.

If you want to serve an Edge Function without the default JWT verification. This is important for webhooks from Stripe, GitHub, etc. These services don't have your JWT tokens, so you need to skip auth verification.

Be careful when disabling JWT verification, as it allows anyone to call your function, so only use it for functions that are meant to be publicly accessible.

Deploy the function when you’re ready

**Examples:**

Example 1 (unknown):
```unknown
1{2  "deno.enablePaths": ["./supabase/functions"],3  "deno.importMap": "./supabase/functions/import_map.json"4}
```

Example 2 (unknown):
```unknown
1{2  "folders": [3    {4      "name": "project-root",5      "path": "./"6    },7    {8      "name": "test-client",9      "path": "app"10    },11    {12      "name": "supabase-functions",13      "path": "supabase/functions"14    }15  ],16  "settings": {17    "files.exclude": {18      "node_modules/": true,19      "app/": true,20      "supabase/functions/": true21    },22    "deno.importMap": "./supabase/functions/import_map.json"23  }24}
```

Example 3 (unknown):
```unknown
1└── supabase2    ├── functions3    │   ├── import_map.json     # Top-level import map4    │   ├── _shared             # Shared code (underscore prefix)5    │   │   ├── supabaseAdmin.ts # Supabase client with SERVICE_ROLE key6    │   │   ├── supabaseClient.ts # Supabase client with ANON key7    │   │   └── cors.ts         # Reusable CORS headers8    │   ├── function-one        # Use hyphens for function names9    │   │   └── index.ts10    │   └── function-two11    │       └── index.ts12    ├── tests13    │   ├── function-one-test.ts14    │   └── function-two-test.ts15    ├── migrations16    └── config.toml
```

---

## Handling Stripe Webhooks | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/stripe-webhooks

**Contents:**
- Handling Stripe Webhooks

Handling Stripe Webhooks

Handling signed Stripe Webhooks with Edge Functions. View on GitHub.

**Examples:**

Example 1 (python):
```python
1// Follow this setup guide to integrate the Deno language server with your editor:2// https://deno.land/manual/getting_started/setup_your_environment3// This enables autocomplete, go to definition, etc.45// Import via bare specifier thanks to the import_map.json file.6import Stripe from 'https://esm.sh/stripe@14?target=denonext'78const stripe = new Stripe(Deno.env.get('STRIPE_API_KEY') as string, {9  // This is needed to use the Fetch API rather than relying on the Node http10  // package.11  apiVersion: '2024-11-20'12})13// This is needed in order to use the Web Crypto API in Deno.14const cryptoProvider = Stripe.createSubtleCryptoProvider()1516console.log('Hello from Stripe Webhook!')1718Deno.serve(async (request) => {19  const signature = request.headers.get('Stripe-Signature')2021  // First step is to verify the event. The .text() method must be used as the22  // verification relies on the raw request body rather than the parsed JSON.23  const body = await request.text()24  let receivedEvent25  try {26    receivedEvent = await stripe.webhooks.constructEventAsync(27      body,28      signature!,29      Deno.env.get('STRIPE_WEBHOOK_SIGNING_SECRET')!,30      undefined,31      cryptoProvider32    )33  } catch (err) {34    return new Response(err.message, { status: 400 })35  }36  console.log(`🔔 Event received: ${receivedEvent.id}`)37  return new Response(JSON.stringify({ ok: true }), { status: 200 })38});
```

---

## Building a Discord Bot | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/discord-bot

**Contents:**
- Building a Discord Bot
- Create an application on Discord Developer portal#
- Code#
- Deploy the slash command handler#
  - Configure Discord application to use our URL as interactions endpoint URL#
- Install the slash command on your Discord server#
- Run locally#

Building a Discord Bot

A new application is created which will hold our Slash Command. Don't close the tab as we need information from this application page throughout our development.

Before we can write some code, we need to curl a discord endpoint to register a Slash Command in our app.

Fill DISCORD_BOT_TOKEN with the token available in the Bot section and CLIENT_ID with the ID available on the General Information section of the page and run the command on your terminal.

This will register a Slash Command named hello that accepts a parameter named name of type string.

Navigate to your Function details in the Supabase Dashboard to get your Endpoint URL.

The application is now ready. Let's proceed to the next section to install it.

So to use the hello Slash Command, we need to install our Greeter application on our Discord server. Here are the steps:

Open Discord, type /Promise and press Enter.

**Examples:**

Example 1 (unknown):
```unknown
1BOT_TOKEN='replace_me_with_bot_token'2CLIENT_ID='replace_me_with_client_id'3curl -X POST \4-H 'Content-Type: application/json' \5-H "Authorization: Bot $BOT_TOKEN" \6-d '{"name":"hello","description":"Greet a person","options":[{"name":"name","description":"The name of the person","type":3,"required":true}]}' \7"https://discord.com/api/v8/applications/$CLIENT_ID/commands"
```

Example 2 (python):
```python
1// Sift is a small routing library that abstracts away details like starting a2// listener on a port, and provides a simple function (serve) that has an API3// to invoke a function for a specific path.4import { json, serve, validateRequest } from 'https://deno.land/x/sift@0.6.0/mod.ts'5// TweetNaCl is a cryptography library that we use to verify requests6// from Discord.7import nacl from 'https://cdn.skypack.dev/tweetnacl@v1.0.3?dts'89enum DiscordCommandType {10  Ping = 1,11  ApplicationCommand = 2,12}1314// For all requests to "/" endpoint, we want to invoke home() handler.15serve({16  '/discord-bot': home,17})1819// The main logic of the Discord Slash Command is defined in this function.20async function home(request: Request) {21  // validateRequest() ensures that a request is of POST method and22  // has the following headers.23  const { error } = await validateRequest(request, {24    POST: {25      headers: ['X-Signature-Ed25519', 'X-Signature-Timestamp'],26    },27  })28  if (error) {29    return json({ error: error.message }, { status: error.status })30  }3132  // verifySignature() verifies if the request is coming from Discord.33  // When the request's signature is not valid, we return a 401 and this is34  // important as Discord sends invalid requests to test our verification.35  const { valid, body } = await verifySignature(request)36  if (!valid) {37    return json(38      { error: 'Invalid request' },39      {40        status: 401,41      }42    )43  }4445  const { type = 0, data = { options: [] } } = JSON.parse(body)46  // Discord performs Ping interactions to test our application.47  // Type 1 in a request implies a Ping interaction.48  if (type === DiscordCommandType.Ping) {49    return json({50      type: 1, // Type 1 in a response is a Pong interaction response type.51    })52  }5354  // Type 2 in a request is an ApplicationCommand interaction.55  // It implies that a user has issued a command.56  if (type === DiscordCommandType.ApplicationCommand) {57    const { value } = data.options.find(58      (option: { name: string; value: string }) => option.name === 'name'59    )60    return json({61      // Type 4 responds with the below message retaining the user's62      // input at the top.63      type: 4,64      data: {65        content: `Hello, ${value}!`,66      },67    })68  }6970  // We will return a bad request error as a valid Discord request71  // shouldn't reach here.72  return json({ error: 'bad request' }, { status: 400 })73}7475/** Verify whether the request is coming from Discord. */76async function verifySignature(request: Request): Promise<{ valid: boolean; body: string }> {77  const PUBLIC_KEY = Deno.env.get('DISCORD_PUBLIC_KEY')!78  // Discord sends these headers with every request.79  const signature = request.headers.get('X-Signature-Ed25519')!80  const timestamp = request.headers.get('X-Signature-Timestamp')!81  const body = await request.text()82  const valid = nacl.sign.detached.verify(83    new TextEncoder().encode(timestamp + body),84    hexToUint8Array(signature),85    hexToUint8Array(PUBLIC_KEY)86  )8788  return { valid, body }89}9091/** Converts a hexadecimal string to Uint8Array. */92function hexToUint8Array(hex: string) {93  return new Uint8Array(hex.match(/.{1,2}/g)!.map((val) => parseInt(val, 16)))94}
```

Example 3 (unknown):
```unknown
1supabase functions deploy discord-bot --no-verify-jwt2supabase secrets set DISCORD_PUBLIC_KEY=your_public_key
```

Example 4 (unknown):
```unknown
1supabase functions serve discord-bot --no-verify-jwt --env-file ./supabase/.env.local2ngrok http 54321
```

---

## Building an MCP Server with mcp-lite | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/mcp-server-mcp-lite

**Contents:**
- Building an MCP Server with mcp-lite
- What is mcp-lite?#
- Why Supabase Edge Functions + mcp-lite?#
- Prerequisites#
- Create a new MCP server#
- Understanding the project structure#
  - Minimal config.toml#
  - Two Hono apps pattern#
  - Deno import maps#
- Local development#

Building an MCP Server with mcp-lite

The Model Context Protocol (MCP) enables Large Language Models (LLMs) to interact with external tools and data sources. With mcp-lite, you can build lightweight MCP servers that run on Supabase Edge Functions, giving your AI assistants the ability to execute custom tools at the edge.

This guide shows you how to scaffold, develop, and deploy an MCP server using mcp-lite on Supabase Edge Functions.

mcp-lite is a lightweight, zero-dependency TypeScript framework for building MCP servers. It works everywhere the Fetch API is available, including Node, Bun, Cloudflare Workers, Deno, and Supabase Edge Functions.

This combination offers several advantages:

Starting with create-mcp-lite@0.3.0, you can scaffold a complete MCP server that runs on Supabase Edge Functions:

When prompted, select Supabase Edge Functions (MCP server) from the template options.

The template creates a focused structure for Edge Functions development:

The template includes a minimal config.toml that runs only Edge Functions - no database, storage, or Studio UI. This keeps your local setup lightweight:

You can always add more services as needed.

The template uses a specific pattern required by Supabase Edge Functions:

This is required because Supabase routes all requests to /<function-name>/*. The outer app handles the function-level routing, while mcpApp handles your actual MCP endpoints.

The template uses Deno's import maps in deno.json to manage dependencies:

This gives you npm package access while staying in the Deno ecosystem.

Navigate to your project directory and start Supabase services:

In a separate terminal, serve your MCP function locally:

Or use the npm script (which runs the same command):

Your MCP server is available at:

Test the MCP server by adding it to your Claude Code, Claude Desktop, Cursor, or your preferred MCP client.

You can also test it using the MCP inspector:

Then add the MCP endpoint URL in the inspector UI.

The MCP server setup is straightforward:

Extend your MCP server by adding tools directly to the mcp instance. Here's an example of adding a database search tool:

You can add tools that:

When ready, deploy to Supabase's global edge network:

Or use the npm script:

Your MCP server will be live at:

The template uses --no-verify-jwt for quick development. This means authentication is not enforced by Supabase's JWT layer.

For production, you should implement authentication at the MCP server level following the MCP Authorization specification. This gives you control over who can access your MCP tools.

When deploying MCP servers:

For more security guidance, see the MCP security guide.

With your MCP server running on Supabase Edge Functions, you can:

**Examples:**

Example 1 (unknown):
```unknown
1npm create mcp-lite@latest
```

Example 2 (unknown):
```unknown
1my-mcp-server/2├── supabase/3│   ├── config.toml                    # Minimal Supabase config (Edge Functions only)4│   └── functions/5│       └── mcp-server/6│           ├── index.ts               # MCP server implementation7│           └── deno.json              # Deno imports and configuration8├── package.json9└── tsconfig.json
```

Example 3 (unknown):
```unknown
1# Minimal config for running only Edge Functions (no DB, storage, or studio)2project_id = "starter-mcp-supabase"34[api]5enabled = true6port = 5432178[edge_runtime]9enabled = true10policy = "per_worker"11deno_version = 2
```

Example 4 (javascript):
```javascript
1// Root handler - matches the function name2const app = new Hono()34// MCP protocol handler5const mcpApp = new Hono()67mcpApp.get('/', (c) => {8  return c.json({9    message: 'MCP Server on Supabase Edge Functions',10    endpoints: {11      mcp: '/mcp',12      health: '/health',13    },14  })15})1617mcpApp.all('/mcp', async (c) => {18  const response = await httpHandler(c.req.raw)19  return response20})2122// Mount at /mcp-server (the function name)23app.route('/mcp-server', mcpApp)
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-bulk-update-functions

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

**URL:** https://supabase.com/docs/reference/cli/supabase-functions

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

## Running AI Models | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/ai-models

**Contents:**
- Running AI Models
- Run AI models in Edge Functions using the built-in Supabase AI API.
- Setup#
  - Running a model inference#
- Generate text embeddings#
- Using Large Language Models (LLM)#
- Running locally#
  - Install Ollama
  - Run the Ollama server
  - Set the function secret

Run AI models in Edge Functions using the built-in Supabase AI API.

Edge Functions have a built-in API for running AI models. You can use this API to generate embeddings, build conversational workflows, and do other AI related tasks in your Edge Functions.

There are no external dependencies or packages to install to enable the API.

Create a new inference session:

To get type hints and checks for the API, import types from functions-js:

Once the session is instantiated, you can call it with inputs to perform inferences:

Generate text embeddings using the built-in gte-small model:

gte-small model exclusively caters to English texts, and any lengthy texts will be truncated to a maximum of 512 tokens. While you can provide inputs longer than 512 tokens, truncation may affect the accuracy.

Inference via larger models is supported via Ollama and Mozilla Llamafile. In the first iteration, you can use it with a self-managed Ollama or Llamafile server.

We are progressively rolling out support for the hosted solution. To sign up for early access, fill out this form.

Install Ollama and pull the Mistral model

Set a function secret called AI_INFERENCE_API_HOST to point to the Ollama server

Once the function is working locally, it's time to deploy to production.

Deploy an Ollama or Llamafile server and set a function secret called AI_INFERENCE_API_HOST to point to the deployed server:

As demonstrated in the video above, running Ollama locally is typically slower than running it in on a server with dedicated GPUs. We are collaborating with the Ollama team to improve local performance.

In the future, a hosted LLM API, will be provided as part of the Supabase platform. Supabase will scale and manage the API and GPUs for you. To sign up for early access, fill up this form.

**Examples:**

Example 1 (javascript):
```javascript
1const model = new Supabase.ai.Session('model-name')
```

Example 2 (unknown):
```unknown
1import 'jsr:@supabase/functions-js/edge-runtime.d.ts'
```

Example 3 (javascript):
```javascript
1// For embeddings (gte-small model)2const embeddings = await model.run('Hello world', {3  mean_pool: true,4  normalize: true,5})67// For text generation (non-streaming)8const response = await model.run('Write a haiku about coding', {9  stream: false,10  timeout: 30,11})1213// For streaming responses14const stream = await model.run('Tell me a story', {15  stream: true,16  mode: 'ollama',17})
```

Example 4 (javascript):
```javascript
1const model = new Supabase.ai.Session('gte-small')23Deno.serve(async (req: Request) => {4  const params = new URL(req.url).searchParams5  const input = params.get('input')6  const output = await model.run(input, { mean_pool: true, normalize: true })7  return new Response(JSON.stringify(output), {8    headers: {9      'Content-Type': 'application/json',10      Connection: 'keep-alive',11    },12  })13})
```

---

## Consuming Supabase Queue Messages with Edge Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/queues/consuming-messages-with-edge-functions

**Contents:**
- Consuming Supabase Queue Messages with Edge Functions
- Learn how to consume Supabase Queue messages server-side with a Supabase Edge Function
- Concepts#
  - Consuming messages in an Edge Function#

Consuming Supabase Queue Messages with Edge Functions

Learn how to consume Supabase Queue messages server-side with a Supabase Edge Function

This guide helps you read & process queue messages server-side with a Supabase Edge Function. Read Queues API Reference for more details on our API.

Supabase Queues is a pull-based Message Queue consisting of three main components: Queues, Messages, and Queue Types. You should already be familiar with the Queues Quickstart.

This is a Supabase Edge Function that reads 5 messages off the queue, processes each of them, and deletes each message when it is done.

Every time this Edge Function is run it:

You might find this kind of setup handy to run with Supabase Cron. You can set up Cron so that every N number of minutes or seconds, the Edge Function will run and process a number of messages off the queue.

Similarly, you can invoke the Edge Function on command at any given time with supabase.functions.invoke.

**Examples:**

Example 1 (python):
```python
1import 'jsr:@supabase/functions-js/edge-runtime.d.ts'2import { createClient } from 'npm:@supabase/supabase-js@2'34const supabaseUrl = 'supabaseURL'5const supabaseKey = 'supabaseKey'67const supabase = createClient(supabaseUrl, supabaseKey)8const queueName = 'your_queue_name'910// Type definition for queue messages11interface QueueMessage {12  msg_id: bigint13  read_ct: number14  vt: string15  enqueued_at: string16  message: any17}1819async function processMessage(message: QueueMessage) {20  //21  // Do whatever logic you need to with the message content22  //23  // Delete the message from the queue24  const { error: deleteError } = await supabase.schema('pgmq_public').rpc('delete', {25    queue_name: queueName,26    msg_id: message.msg_id,27  })2829  if (deleteError) {30    console.error(`Failed to delete message ${message.msg_id}:`, deleteError)31  } else {32    console.log(`Message ${message.msg_id} deleted from queue`)33  }34}3536Deno.serve(async (req) => {37  const { data: messages, error } = await supabase.schema('pgmq_public').rpc('read', {38    queue_name: queueName,39    sleep_seconds: 0, // Don't wait if queue is empty40    n: 5, // Read 5 messages off the queue41  })4243  if (error) {44    console.error(`Error reading from ${queueName} queue:`, error)45    return new Response(JSON.stringify({ error: error.message }), {46      status: 500,47      headers: { 'Content-Type': 'application/json' },48    })49  }5051  if (!messages || messages.length === 0) {52    console.log('No messages in workflow_messages queue')53    return new Response(JSON.stringify({ message: 'No messages in queue' }), {54      status: 200,55      headers: { 'Content-Type': 'application/json' },56    })57  }5859  console.log(`Found ${messages.length} messages to process`)6061  // Process each message that was read off the queue62  for (const message of messages) {63    try {64      await processMessage(message as QueueMessage)65    } catch (error) {66      console.error(`Error processing message ${message.msg_id}:`, error)67    }68  }6970  // Return immediately while background processing continues71  return new Response(72    JSON.stringify({73      message: `Processing ${messages.length} messages in background`,74      count: messages.length,75    }),76    {77      status: 200,78      headers: { 'Content-Type': 'application/json' },79    }80  )81})
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-functions-delete

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

## Managing dependencies | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/dependencies

**Contents:**
- Managing dependencies
- Handle dependencies within Edge Functions.
- Importing dependencies#
  - Using deno.json (recommended)#
  - Using import maps (legacy)#
- Private NPM packages#
- Using a custom NPM registry#
- Importing types#

Managing dependencies

Handle dependencies within Edge Functions.

Supabase Edge Functions support several ways to import dependencies:

Each function should have its own deno.json file to manage dependencies and configure Deno-specific settings. This ensures proper isolation between functions and is the recommended approach for deployment. When you update the dependencies for one function, it won't accidentally break another function that needs different versions.

You can add this file directly to the function’s own directory:

It's possible to use a global deno.json in the /supabase/functions directory for local development, but this approach is not recommended for deployment. Each function should maintain its own configuration to ensure proper isolation and dependency management.

Import Maps are a legacy way to manage dependencies, similar to a package.json file. While still supported, we recommend using deno.json. If both exist, deno.json takes precedence.

Each function should have its own import_map.json file for proper isolation:

This JSON file should be located within the function’s own directory:

It's possible to use a global import_map.json in the /supabase/functions directory for local development, but this approach is not recommended for deployment. Each function should maintain its own configuration to ensure proper isolation and dependency management.

If you’re using import maps with VSCode, update your .vscode/settings.json to point to your function-specific import map:

You can override the default import map location using the --import-map <string> flag with serve and deploy commands, or by setting the import_map property in your config.toml file:

To use private npm packages, create a .npmrc file within your function’s own directory.

It's possible to use a global .npmrc in the /supabase/functions directory for local development, but this approach is not recommended for deployment. Each function should maintain its own configuration to ensure proper isolation and dependency management.

Add your registry details in the .npmrc file. Follow this guide to learn more about the syntax of npmrc files.

After configuring your .npmrc, you can import the private package in your function code:

Some organizations require a custom NPM registry for security and compliance purposes. In such cases, you can specify the custom NPM registry to use via NPM_CONFIG_REGISTRY environment variable.

You can define it in the project's .env file or directly specify it when running the deploy command:

If your environment is set up properly and the module you're importing is exporting types, the import will have types and autocompletion support.

Some npm packages may not ship out of the box types and you may need to import them from a separate package. You can specify their types with a @deno-types directive:

To include types for built-in Node APIs, add the following line to the top of your imports:

**Examples:**

Example 1 (python):
```python
1// NPM packages (recommended)2import { createClient } from 'npm:@supabase/supabase-js@2'34// Node.js built-ins5import process from 'node:process'67// JSR modules (Deno's registry)8import path from 'jsr:@std/path@1.0.8'
```

Example 2 (unknown):
```unknown
1{2  "imports": {3    "supabase": "npm:@supabase/supabase-js@2",4    "lodash": "https://cdn.skypack.dev/lodash"5  }6}
```

Example 3 (unknown):
```unknown
1└── supabase2    ├── functions3    │   ├── function-one4    │   │   ├── index.ts5    │   │   └── deno.json    # Function-specific Deno configuration6    │   └── function-two7    │       ├── index.ts8    │       └── deno.json    # Function-specific Deno configuration9    └── config.toml
```

Example 4 (unknown):
```unknown
1# /function-one/import_map.json2{3  "imports": {4    "lodash": "https://cdn.skypack.dev/lodash"5  }6}
```

---

## Handling Routing in Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/routing

**Contents:**
- Handling Routing in Functions
- Handle custom routing within Edge Functions.
- Basic routing example#
- Using route parameters#
- URL Patterns API#

Handling Routing in Functions

Handle custom routing within Edge Functions.

Usually, an Edge Function is written to perform a single action (e.g. write a record to the database). However, if your app's logic is split into multiple Edge Functions, requests to each action may seem slower.

Each Edge Function needs to be booted before serving a request (known as cold starts). If an action is performed less frequently (e.g. deleting a record), there is a high chance of that function experiencing a cold start.

One way to reduce cold starts and increase performance is to combine multiple actions into a single Edge Function. This way only one instance needs to be booted and it can handle multiple requests to different actions.

For example, we can use a single Edge Function to create a typical CRUD API (create, read, update, delete records).

To combine multiple endpoints into a single Edge Function, you can use web application frameworks such as Express, Oak, or Hono.

Here's a simple hello world example using some popular web frameworks:

Within Edge Functions, paths should always be prefixed with the function name (in this case hello-world).

You can use route parameters to capture values at specific URL segments (e.g. /tasks/:taskId/notes/:noteId).

Keep in mind paths must be prefixed by function name. Route parameters can only be used after the function name prefix.

If you prefer not to use a web framework, you can directly use URL Pattern API within your Edge Functions to implement routing.

This works well for small apps with only a couple of routes:

**Examples:**

Example 1 (python):
```python
1import { Hono } from 'jsr:@hono/hono'23const app = new Hono()45app.post('/hello-world', async (c) => {6  const { name } = await c.req.json()7  return new Response(`Hello ${name}!`)8})910app.get('/hello-world', (c) => {11  return new Response('Hello World!')12})1314Deno.serve(app.fetch)
```

Example 2 (javascript):
```javascript
1interface Task {2  id: string3  name: string4}56let tasks: Task[] = []78const router = new Map<string, (req: Request) => Promise<Response>>()910async function getAllTasks(): Promise<Response> {11  return new Response(JSON.stringify(tasks))12}1314async function getTask(id: string): Promise<Response> {15  const task = tasks.find((t) => t.id === id)16  if (task) {17    return new Response(JSON.stringify(task))18  } else {19    return new Response('Task not found', { status: 404 })20  }21}2223async function createTask(req: Request): Promise<Response> {24  const id = Math.random().toString(36).substring(7)25  const task = { id, name: '' }26  tasks.push(task)27  return new Response(JSON.stringify(task), { status: 201 })28}2930async function updateTask(id: string, req: Request): Promise<Response> {31  const index = tasks.findIndex((t) => t.id === id)32  if (index !== -1) {33    tasks[index] = { ...tasks[index] }34    return new Response(JSON.stringify(tasks[index]))35  } else {36    return new Response('Task not found', { status: 404 })37  }38}3940async function deleteTask(id: string): Promise<Response> {41  const index = tasks.findIndex((t) => t.id === id)42  if (index !== -1) {43    tasks.splice(index, 1)44    return new Response('Task deleted successfully')45  } else {46    return new Response('Task not found', { status: 404 })47  }48}4950Deno.serve(async (req) => {51  const url = new URL(req.url)52  const method = req.method53  // Extract the last part of the path as the command54  const command = url.pathname.split('/').pop()55  // Assuming the last part of the path is the task ID56  const id = command57  try {58    switch (method) {59      case 'GET':60        if (id) {61          return getTask(id)62        } else {63          return getAllTasks()64        }65      case 'POST':66        return createTask(req)67      case 'PUT':68        if (id) {69          return updateTask(id, req)70        } else {71          return new Response('Bad Request', { status: 400 })72        }73      case 'DELETE':74        if (id) {75          return deleteTask(id)76        } else {77          return new Response('Bad Request', { status: 400 })78        }79      default:80        return new Response('Method Not Allowed', { status: 405 })81    }82  } catch (error) {83    return new Response(`Internal Server Error: ${error}`, { status: 500 })84  }85})
```

Example 3 (javascript):
```javascript
1// ...23    // For more details on URLPattern, check https://developer.mozilla.org/en-US/docs/Web/API/URL_Pattern_API4    const taskPattern = new URLPattern({ pathname: '/restful-tasks/:id' })5    const matchingPath = taskPattern.exec(url)6    const id = matchingPath ? matchingPath.pathname.groups.id : null78    let task = null9    if (method === 'POST' || method === 'PUT') {10      const body = await req.json()11      task = body.task12    }1314    // call relevant method based on method and id15    switch (true) {16      case id && method === 'GET':17        return getTask(supabaseClient, id as string)18      case id && method === 'PUT':19        return updateTask(supabaseClient, id as string, task)20      case id && method === 'DELETE':21        return deleteTask(supabaseClient, id as string)22      case method === 'POST':23        return createTask(supabaseClient, task)24      case method === 'GET':25        return getAllTasks(supabaseClient)26      default:27        return getAllTasks(supabaseClient)2829    // ...
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-functions-deploy

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

## Building a Telegram Bot | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/telegram-bot

**Contents:**
- Building a Telegram Bot

Building a Telegram Bot

Handle Telegram Bot Webhooks with the grammY framework. grammY is an open source Telegram Bot Framework which makes it easy to handle and respond to incoming messages. View on GitHub.

---

## Monitoring with Sentry | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/sentry-monitoring

**Contents:**
- Monitoring with Sentry
  - Prerequisites#
  - 1. Create Supabase function#
  - 2. Add the Sentry Deno SDK#
  - 3. Deploy and test#
  - 4. Try it yourself#
- Working with scopes#

Monitoring with Sentry

Add the Sentry Deno SDK to your Supabase Edge Functions to track exceptions and get notified of errors or performance issues.

Create a new function locally:

Handle exceptions within your function and send them to Sentry.

Run function locally:

Test it: http://localhost:54321/functions/v1/sentryfied

Deploy function to Supabase:

Find the complete example on GitHub.

Sentry Deno SDK currently do not support Deno.serve instrumentation, which means that there is no scope separation between requests. Because of that, when the Edge Functions runtime is reused between multiple requests, all globally captured breadcrumbs and contextual data will be shared, which is not the desired behavior. To work around this, all default integrations in the example code above are disabled, and you should be relying on withScope to encapsulate all Sentry SDK API calls, or pass context directly to the captureException or captureMessage calls.

**Examples:**

Example 1 (unknown):
```unknown
1supabase functions new sentryfied
```

Example 2 (python):
```python
1import * as Sentry from 'https://deno.land/x/sentry/index.mjs'23Sentry.init({4  // https://docs.sentry.io/product/sentry-basics/concepts/dsn-explainer/#where-to-find-your-dsn5  dsn: SENTRY_DSN,6  defaultIntegrations: false,7  // Performance Monitoring8  tracesSampleRate: 1.0,9  // Set sampling rate for profiling - this is relative to tracesSampleRate10  profilesSampleRate: 1.0,11})1213// Set region and execution_id as custom tags14Sentry.setTag('region', Deno.env.get('SB_REGION'))15Sentry.setTag('execution_id', Deno.env.get('SB_EXECUTION_ID'))1617Deno.serve(async (req) => {18  try {19    const { name } = await req.json()20    // This will throw, as `name` in our example call will be `undefined`21    const data = {22      message: `Hello ${name}!`,23    }2425    return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } })26  } catch (e) {27    Sentry.captureException(e)28    // Flush Sentry before the running process closes29    await Sentry.flush(2000)30    return new Response(JSON.stringify({ msg: 'error' }), {31      status: 500,32      headers: { 'Content-Type': 'application/json' },33    })34  }35})
```

Example 3 (unknown):
```unknown
1supabase start2supabase functions serve --no-verify-jwt
```

Example 4 (unknown):
```unknown
1supabase functions deploy sentryfied --no-verify-jwt
```

---

## Scheduling Edge Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/schedule-functions

**Contents:**
- Scheduling Edge Functions
- Examples#
  - Invoke an Edge Function every minute#
- Resources#

Scheduling Edge Functions

The hosted Supabase Platform supports the pg_cron extension, a recurring job scheduler in Postgres.

In combination with the pg_net extension, this allows us to invoke Edge Functions periodically on a set schedule.

To access the auth token securely for your Edge Function call, we recommend storing them in Supabase Vault.

Store project_url and anon_key in Supabase Vault:

Make a POST request to a Supabase Edge Function every minute:

**Examples:**

Example 1 (unknown):
```unknown
1select vault.create_secret('https://project-ref.supabase.co', 'project_url');2select vault.create_secret('YOUR_SUPABASE_PUBLISHABLE_KEY', 'publishable_key');
```

Example 2 (unknown):
```unknown
1select2  cron.schedule(3    'invoke-function-every-minute',4    '* * * * *', -- every minute5    $$6    select7      net.http_post(8          url:= (select decrypted_secret from vault.decrypted_secrets where name = 'project_url') || '/functions/v1/function-name',9          headers:=jsonb_build_object(10            'Content-type', 'application/json',11            'Authorization', 'Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name = 'anon_key')12          ),13          body:=concat('{"time": "', now(), '"}')::jsonb14      ) as request_id;15    $$16  );
```

---

## Semantic Search | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/semantic-search

**Contents:**
- Semantic Search
- Semantic Search with pgvector and Supabase Edge Functions
  - Create the database table and webhook#
- Create a Database Function and RPC#
- Query vectors in Supabase Edge Functions#

Semantic Search with pgvector and Supabase Edge Functions

Semantic search interprets the meaning behind user queries rather than exact keywords. It uses machine learning to capture the intent and context behind the query, handling language nuances like synonyms, phrasing variations, and word relationships.

Since Supabase Edge Runtime v1.36.0 you can run the gte-small model natively within Supabase Edge Functions without any external dependencies! This allows you to generate text embeddings without calling any external APIs!

In this tutorial you're implementing three parts:

You can find the complete example code on GitHub

Given the following table definition:

You can deploy the following edge function as a database webhook to generate the embeddings for any text content inserted into the table:

With the embeddings now stored in your Postgres database table, you can query them from Supabase Edge Functions by utilizing Remote Procedure Calls (RPC).

Given the following Postgres Function:

You can use supabase-js to first generate the embedding for the search term and then invoke the Postgres function to find the relevant results from your stored embeddings, right from your Supabase Edge Function:

You now have AI powered semantic search set up without any external dependencies! Just you, pgvector, and Supabase Edge Functions!

**Examples:**

Example 1 (unknown):
```unknown
1create extension if not exists vector with schema extensions;23create table embeddings (4  id bigint primary key generated always as identity,5  content text not null,6  embedding extensions.vector (384)7);8alter table embeddings enable row level security;910create index on embeddings using hnsw (embedding vector_ip_ops);
```

Example 2 (javascript):
```javascript
1const model = new Supabase.ai.Session('gte-small')23Deno.serve(async (req) => {4  const payload: WebhookPayload = await req.json()5  const { content, id } = payload.record67  // Generate embedding.8  const embedding = await model.run(content, {9    mean_pool: true,10    normalize: true,11  })1213  // Store in database.14  const { error } = await supabase15    .from('embeddings')16    .update({ embedding: JSON.stringify(embedding) })17    .eq('id', id)18  if (error) console.warn(error.message)1920  return new Response('ok')21})
```

Example 3 (unknown):
```unknown
1-- Matches document sections using vector similarity search on embeddings2--3-- Returns a setof embeddings so that we can use PostgREST resource embeddings (joins with other tables)4-- Additional filtering like limits can be chained to this function call5create or replace function query_embeddings(embedding extensions.vector(384), match_threshold float)6returns setof embeddings7language plpgsql8as $$9begin10  return query11  select *12  from embeddings1314  -- The inner product is negative, so we negate match_threshold15  where embeddings.embedding <#> embedding < -match_threshold1617  -- Our embeddings are normalized to length 1, so cosine similarity18  -- and inner product will produce the same query results.19  -- Using inner product which can be computed faster.20  --21  -- For the different distance functions, see https://github.com/pgvector/pgvector22  order by embeddings.embedding <#> embedding;23end;24$$;
```

Example 4 (javascript):
```javascript
1const model = new Supabase.ai.Session('gte-small')23Deno.serve(async (req) => {4  const { search } = await req.json()5  if (!search) return new Response('Please provide a search param!')6  // Generate embedding for search term.7  const embedding = await model.run(search, {8    mean_pool: true,9    normalize: true,10  })1112  // Query embeddings.13  const { data: result, error } = await supabase14    .rpc('query_embeddings', {15      embedding,16      match_threshold: 0.8,17    })18    .select('content')19    .limit(3)20  if (error) {21    return Response.json(error)22  }2324  return Response.json({ search, result })25})
```

---

## Environment Variables | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/secrets

**Contents:**
- Environment Variables
- Manage sensitive data securely across environments.
- Default secrets#
- Accessing environment variables#
  - Local secrets#
  - Production secrets#

Environment Variables

Manage sensitive data securely across environments.

Edge Functions have access to these secrets by default:

In a hosted environment, functions have access to the following environment variables:

You can access environment variables using Deno's built-in handler, and passing it the name of the environment variable you’d like to access.

For example, in a function:

In development, you can load environment variables in two ways:

Never check your .env files into Git! Instead, add the path to this file to your .gitignore.

We can automatically access the secrets in our Edge Functions through Deno’s handler

Now we can invoke our function locally. If you're using the default .env file at supabase/functions/.env, it's automatically loaded:

Or you can specify a custom .env file with the --env-file flag:

This is useful for managing different environments (development, staging, etc.).

You will also need to set secrets for your production Edge Functions. You can do this via the Dashboard or using the CLI.

Note that you can paste multiple secrets at a time.

You can create a .env file to help deploy your secrets to production

Never check your .env files into Git! Instead, add the path to this file to your .gitignore.

You can push all the secrets from the .env file to your remote project using supabase secrets set. This makes the environment visible in the dashboard as well.

Alternatively, this command also allows you to set production secrets individually rather than storing them in a .env file.

To see all the secrets which you have set remotely, you can use supabase secrets list

You don't need to re-deploy after setting your secrets. They're available immediately in your functions.

**Examples:**

Example 1 (unknown):
```unknown
1Deno.env.get('NAME_OF_SECRET')
```

Example 2 (python):
```python
1import { createClient } from 'npm:@supabase/supabase-js@2'23// For user-facing operations (respects RLS)4const supabase = createClient(5  Deno.env.get('SUPABASE_URL')!,6  Deno.env.get('SUPABASE_ANON_KEY')!7)89// For admin operations (bypasses RLS)10const supabaseAdmin = createClient(11  Deno.env.get('SUPABASE_URL')!,12  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!13)
```

Example 3 (unknown):
```unknown
1supabase functions serve --env-file .env.local
```

Example 4 (javascript):
```javascript
1const secretKey = Deno.env.get('STRIPE_SECRET_KEY')
```

---

## Transcription Telegram Bot | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/elevenlabs-transcribe-speech

**Contents:**
- Transcription Telegram Bot
- Build a Telegram bot that transcribes audio and video messages in 99 languages using TypeScript with Deno in Supabase Edge Functions.
- Introduction#
- Requirements#
- Setup#
  - Register a Telegram bot#
  - Create a Supabase project locally#
  - Create a database table to log the transcription results#
  - Create a Supabase Edge Function to handle Telegram webhook requests#
  - Set up the environment variables#

Transcription Telegram Bot

Build a Telegram bot that transcribes audio and video messages in 99 languages using TypeScript with Deno in Supabase Edge Functions.

In this tutorial you will learn how to build a Telegram bot that transcribes audio and video messages in 99 languages using TypeScript and the ElevenLabs Scribe model via the speech to text API.

To check out what the end result will look like, you can test out the t.me/ElevenLabsScribeBot

Find the example project on GitHub.

Use the BotFather to create a new Telegram bot. Run the /newbot command and follow the instructions to create a new bot. At the end, you will receive your secret bot token. Note it down securely for the next step.

After installing the Supabase CLI, run the following command to create a new Supabase project locally:

Next, create a new database table to log the transcription results:

This will create a new migration file in the supabase/migrations directory. Open the file and add the following SQL:

Next, create a new Edge Function to handle Telegram webhook requests:

If you're using VS Code or Cursor, select y when the CLI prompts "Generate VS Code settings for Deno? [y/N]"!

Within the supabase/functions directory, create a new .env file and add the following variables:

The project uses a couple of dependencies:

Since Supabase Edge Function uses the Deno runtime, you don't need to install the dependencies, rather you can import them via the npm: prefix.

In your newly created scribe-bot/index.ts file, add the following code:

If you haven't already, create a new Supabase account at database.new and link the local project to your Supabase account:

Run the following command to apply the database migrations from the supabase/migrations directory:

Navigate to the table editor in your Supabase dashboard and you should see and empty transcription_logs table.

Lastly, run the following command to deploy the Edge Function:

Navigate to the Edge Functions view in your Supabase dashboard and you should see the scribe-bot function deployed. Make a note of the function URL as you'll need it later, it should look something like https://<project-ref>.functions.supabase.co/scribe-bot.

Set your bot's webhook URL to https://<PROJECT_REFERENCE>.functions.supabase.co/telegram-bot (Replacing <...> with respective values). In order to do that, run a GET request to the following URL (in your browser, for example):

Note that the FUNCTION_SECRET is the secret you set in your .env file.

Now that you have all your secrets set locally, you can run the following command to set the secrets in your Supabase project:

Finally you can test the bot by sending it a voice message, audio or video file.

After you see the transcript as a reply, navigate back to your table editor in the Supabase dashboard and you should see a new row in your transcription_logs table.

**Examples:**

Example 1 (unknown):
```unknown
1supabase init
```

Example 2 (unknown):
```unknown
1supabase migrations new init
```

Example 3 (unknown):
```unknown
1CREATE TABLE IF NOT EXISTS transcription_logs (2  id BIGSERIAL PRIMARY KEY,3  file_type VARCHAR NOT NULL,4  duration INTEGER NOT NULL,5  chat_id BIGINT NOT NULL,6  message_id BIGINT NOT NULL,7  username VARCHAR,8  transcript TEXT,9  language_code VARCHAR,10  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,11  error TEXT12);1314ALTER TABLE transcription_logs ENABLE ROW LEVEL SECURITY;
```

Example 4 (unknown):
```unknown
1supabase functions new scribe-bot
```

---

## Flutter: Invokes a Supabase Edge Function. | Supabase Docs

**URL:** https://supabase.com/docs/reference/dart/functions-invoke

---

## Local Debugging | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/debugging-tools

**Contents:**
- Local Debugging
- Debug your Edge Functions locally using Chrome DevTools for easy breakpoint debugging and code inspection.
  - Inspect with Chrome Developer Tools#

Debug your Edge Functions locally using Chrome DevTools for easy breakpoint debugging and code inspection.

Since v1.171.0 the Supabase CLI supports debugging Edge Functions via the v8 inspector protocol, allowing for debugging via Chrome DevTools and other Chromium-based browsers.

Now you should have Chrome DevTools configured and ready to debug your functions.

**Examples:**

Example 1 (unknown):
```unknown
1supabase functions serve --inspect-mode brk
```

---

## Image Manipulation | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/image-manipulation

**Contents:**
- Image Manipulation
  - Prerequisites#
  - Create the Edge Function#
  - Write the function#
  - Test it locally#
  - Deploy to your hosted project#

Supabase Storage has out-of-the-box support for the most common image transformations and optimizations you need. If you need to do anything custom beyond what Supabase Storage provides, you can use Edge Functions to write custom image manipulation scripts.

In this example, we will use magick-wasm to perform image manipulations. magick-wasm is the WebAssembly port of the popular ImageMagick library and supports processing over 100 file formats.

Edge Functions currently doesn't support image processing libraries such as Sharp, which depend on native libraries. Only WASM-based libraries are supported.

Make sure you have the latest version of the Supabase CLI installed.

Create a new function locally:

In this example, we are implementing a function allowing users to upload an image and get a blurred thumbnail.

Here's the implementation in index.ts file:

You can test the function locally by running:

Then, make a request using curl or your favorite API testing tool.

If you open the output.png file you will find a transformed version of your original image.

Now, let's deploy the function to your Supabase project.

Hosted Edge Functions have limits on memory and CPU usage.

If you try to perform complex image processing or handle large images (> 5MB) your function may return a resource limit exceeded error.

**Examples:**

Example 1 (unknown):
```unknown
1supabase functions new image-blur
```

Example 2 (python):
```python
1// This is an example showing how to use Magick WASM to do image manipulations in Edge Functions.2//3import {4  ImageMagick,5  initializeImageMagick,6  MagickFormat,7} from "npm:@imagemagick/magick-wasm@0.0.30";89const wasmBytes = await Deno.readFile(10  new URL(11    "magick.wasm",12    import.meta.resolve("npm:@imagemagick/magick-wasm@0.0.30"),13  ),14);15await initializeImageMagick(16  wasmBytes,17);1819Deno.serve(async (req) => {20  const formData = await req.formData();21  const content = await formData.get("file").bytes();2223  let result = ImageMagick.read(24    content,25    (img): Uint8Array => {26      // resize the image27      img.resize(500, 300);28      // add a blur of 60x529      img.blur(60, 5);3031      return img.write(32        (data) => data,33      );34    },35  );3637  return new Response(38    result,39    { headers: { "Content-Type": "image/png" } },40  );41});
```

Example 3 (unknown):
```unknown
1supabase start2supabase functions serve --no-verify-jwt
```

Example 4 (unknown):
```unknown
1curl --location '<http://localhost:54321/functions/v1/image-blur>' \\2--form 'file=@"/path/to/image.png"'3--output '/path/to/output.png'
```

---

## Handling WebSockets | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/websockets

**Contents:**
- Handling WebSockets
- Handle WebSocket connections in Edge Functions.
- Creating WebSocket servers#
  - Outbound WebSockets#
- Authentication#
- Testing WebSockets locally#

Handle WebSocket connections in Edge Functions.

Edge Functions supports hosting WebSocket servers that can facilitate bi-directional communications with browser clients.

Here are some basic examples of setting up WebSocket servers using Deno and Node.js APIs.

You can also establish an outbound WebSocket connection to another server from an Edge Function.

Combining it with incoming WebSocket servers, it's possible to use Edge Functions as a WebSocket proxy, for example as a relay server for the OpenAI Realtime API.

WebSocket browser clients don't have the option to send custom headers. Because of this, Edge Functions won't be able to perform the usual authorization header check to verify the JWT.

You can skip the default authorization header checks by explicitly providing --no-verify-jwt when serving and deploying functions.

To authenticate the user making WebSocket requests, you can pass the JWT in URL query params or via a custom protocol.

The maximum duration is capped based on the wall-clock, CPU, and memory limits. The Function will shutdown when it reaches one of these limits.

When testing Edge Functions locally with Supabase CLI, the instances are terminated automatically after a request is completed. This will prevent keeping WebSocket connections open.

To prevent that, you can update the supabase/config.toml with the following settings:

When running with per_worker policy, Function won't auto-reload on edits. You will need to manually restart it by running supabase functions serve.

**Examples:**

Example 1 (javascript):
```javascript
1Deno.serve((req) => {2  const upgrade = req.headers.get('upgrade') || ''34  if (upgrade.toLowerCase() != 'websocket') {5    return new Response("request isn't trying to upgrade to WebSocket.", { status: 400 })6  }78  const { socket, response } = Deno.upgradeWebSocket(req)910  socket.onopen = () => console.log('socket opened')11  socket.onmessage = (e) => {12    console.log('socket message:', e.data)13    socket.send(new Date().toString())14  }1516  socket.onerror = (e) => console.log('socket errored:', e.message)17  socket.onclose = () => console.log('socket closed')1819  return response20})
```

Example 2 (python):
```python
1import { createServer } from "node:http";2import { WebSocketServer } from "npm:ws";3import { RealtimeClient } from "https://raw.githubusercontent.com/openai/openai-realtime-api-beta/refs/heads/main/lib/client.js";45// ...67const OPENAI_API_KEY = Deno.env.get("OPENAI_API_KEY");89const server = createServer();10// Since we manually created the HTTP server,11// turn on the noServer mode.12const wss = new WebSocketServer({ noServer: true });1314wss.on("connection", async (ws) => {15  console.log("socket opened");16  if (!OPENAI_API_KEY) {17    throw new Error("OPENAI_API_KEY is not set");18  }19  // Instantiate new client20  console.log(`Connecting with key "${OPENAI_API_KEY.slice(0, 3)}..."`);21  const client = new RealtimeClient({ apiKey: OPENAI_API_KEY });2223  // Relay: OpenAI Realtime API Event -> Browser Event24  client.realtime.on("server.*", (event) => {25    console.log(`Relaying "${event.type}" to Client`);26    ws.send(JSON.stringify(event));27  });28  client.realtime.on("close", () => ws.close());2930  // Relay: Browser Event -> OpenAI Realtime API Event31  // We need to queue data waiting for the OpenAI connection32  const messageQueue = [];33  const messageHandler = (data) => {34    try {35      const event = JSON.parse(data);36      console.log(`Relaying "${event.type}" to OpenAI`);37      client.realtime.send(event.type, event);38    } catch (e) {39      console.error(e.message);40      console.log(`Error parsing event from client: ${data}`);41    }42  };4344  ws.on("message", (data) => {45    if (!client.isConnected()) {46      messageQueue.push(data);47    } else {48      messageHandler(data);49    }50  });51  ws.on("close", () => client.disconnect());5253  // Connect to OpenAI Realtime API54  try {55    console.log(`Connecting to OpenAI...`);56    await client.connect();57  } catch (e) {58    console.log(`Error connecting to OpenAI: ${e.message}`);59    ws.close();60    return;61  }62  console.log(`Connected to OpenAI successfully!`);63  while (messageQueue.length) {64    messageHandler(messageQueue.shift());65  }66});6768server.on("upgrade", (req, socket, head) => {69  wss.handleUpgrade(req, socket, head, (ws) => {70    wss.emit("connection", ws, req);71  });72});7374server.listen(8080);
```

Example 3 (python):
```python
1import { createClient } from 'npm:@supabase/supabase-js@2'23const supabase = createClient(4  Deno.env.get('SUPABASE_URL'),5  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')6)78Deno.serve((req) => {9  const upgrade = req.headers.get('upgrade') || ''10  if (upgrade.toLowerCase() != 'WebSocket') {11    return new Response("request isn't trying to upgrade to WebSocket.", { status: 400 })12  }1314  // Please be aware query params may be logged in some logging systems.15  const url = new URL(req.url)16  const jwt = url.searchParams.get('jwt')1718  if (!jwt) {19    console.error('Auth token not provided')20    return new Response('Auth token not provided', { status: 403 })21  }2223  const { error, data } = await supabase.auth.getClaims()2425  if (error) {26    console.error(error)27    return new Response('Invalid token provided', { status: 403 })28  }2930  if (!data.user) {31    console.error('user is not authenticated')32    return new Response('User is not authenticated', { status: 403 })33  }3435  const { socket, response } = Deno.upgradeWebSocket(req)3637  socket.onopen = () => console.log('socket opened')38  socket.onmessage = (e) => {39    console.log('socket message:', e.data)40    socket.send(new Date().toString())41  }4243  socket.onerror = (e) => console.log('socket errored:', e.message)44  socket.onclose = () => console.log('socket closed')4546  return response47})
```

Example 4 (unknown):
```unknown
1[edge_runtime]2policy = "per_worker"
```

---

## Taking Screenshots with Puppeteer | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/screenshots

**Contents:**
- Taking Screenshots with Puppeteer

Taking Screenshots with Puppeteer

Puppeteer is a handy tool to programmatically take screenshots and generate PDFs. However, trying to do so in Edge Functions can be challenging due to the size restrictions. Luckily there is a serverless browser offering available that we can connect to via WebSockets.

Find the code on GitHub.

---

## CAPTCHA support with Cloudflare Turnstile | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/cloudflare-turnstile

**Contents:**
- CAPTCHA support with Cloudflare Turnstile
- Setup#
- Code#
- Deploy the server-side validation Edge Functions#
- Invoke the function from your site#

CAPTCHA support with Cloudflare Turnstile

Cloudflare Turnstile is a friendly, free CAPTCHA replacement, and it works seamlessly with Supabase Edge Functions to protect your forms. View on GitHub.

Create a new function in your project:

And add the code to the index.ts file:

**Examples:**

Example 1 (unknown):
```unknown
1supabase functions new cloudflare-turnstile
```

Example 2 (python):
```python
1import { corsHeaders } from '../_shared/cors.ts'23console.log('Hello from Cloudflare Trunstile!')45function ips(req: Request) {6  return req.headers.get('x-forwarded-for')?.split(/\s*,\s*/)7}89Deno.serve(async (req) => {10  // This is needed if you're planning to invoke your function from a browser.11  if (req.method === 'OPTIONS') {12    return new Response('ok', { headers: corsHeaders })13  }1415  const { token } = await req.json()16  const clientIps = ips(req) || ['']17  const ip = clientIps[0]1819  // Validate the token by calling the20  // "/siteverify" API endpoint.21  let formData = new FormData()22  formData.append('secret', Deno.env.get('CLOUDFLARE_SECRET_KEY') ?? '')23  formData.append('response', token)24  formData.append('remoteip', ip)2526  const url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'27  const result = await fetch(url, {28    body: formData,29    method: 'POST',30  })3132  const outcome = await result.json()33  console.log(outcome)34  if (outcome.success) {35    return new Response('success', { headers: corsHeaders })36  }37  return new Response('failure', { headers: corsHeaders })38})
```

Example 3 (unknown):
```unknown
1supabase functions deploy cloudflare-turnstile2supabase secrets set CLOUDFLARE_SECRET_KEY=your_secret_key
```

Example 4 (javascript):
```javascript
1const { data, error } = await supabase.functions.invoke('cloudflare-turnstile', {2  body: { token },3})
```

---

## Slack Bot Mention Edge Function | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/slack-bot-mention

**Contents:**
- Slack Bot Mention Edge Function
- Configuring Slack apps#
- Creating the Edge Function#

Slack Bot Mention Edge Function

The Slack Bot Mention Edge Function allows you to process mentions in Slack and respond accordingly.

For your bot to seamlessly interact with Slack, you'll need to configure Slack Apps:

Deploy the following code as an Edge function using the CLI:

Here's the code of the Edge Function, you can change the response to handle the text received:

**Examples:**

Example 1 (unknown):
```unknown
1supabase --project-ref nacho_slacker secrets \2set SLACK_TOKEN=<xoxb-YOUR-SLACK-TOKEN-HERE>
```

Example 2 (python):
```python
1import { WebClient } from 'https://deno.land/x/slack_web_api@6.7.2/mod.js'23const slackBotToken = Deno.env.get('SLACK_TOKEN') ?? ''4const botClient = new WebClient(slackBotToken)56console.log(`Slack URL verification function up and running!`)7Deno.serve(async (req) => {8  try {9    const reqBody = await req.json()10    console.log(JSON.stringify(reqBody, null, 2))11    const { token, challenge, type, event } = reqBody1213    if (type == 'url_verification') {14      return new Response(JSON.stringify({ challenge }), {15        headers: { 'Content-Type': 'application/json' },16        status: 200,17      })18    } else if (event.type == 'app_mention') {19      const { user, text, channel, ts } = event20      // Here you should process the text received and return a response:21      const response = await botClient.chat.postMessage({22        channel: channel,23        text: `Hello <@${user}>!`,24        thread_ts: ts,25      })26      return new Response('ok', { status: 200 })27    }28  } catch (error) {29    return new Response(JSON.stringify({ error: error.message }), {30      headers: { 'Content-Type': 'application/json' },31      status: 500,32    })33  }34})
```

---

## Edge Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions

**Contents:**
- Edge Functions
- Globally distributed TypeScript functions.
- How it works#
- Quick technical notes#
- When to use Edge Functions#
- Examples#

Globally distributed TypeScript functions.

Edge Functions are server-side TypeScript functions, distributed globally at the edge—close to your users. They can be used for listening to webhooks or integrating your Supabase project with third-parties like Stripe. Edge Functions are developed using Deno, which offers a few benefits to you as a developer:

Check out the Edge Function Examples in our GitHub repository.

Type-Safe SQL with Kysely

Monitoring with Sentry

React Native with Stripe

Building a RESTful Service API

Working with Supabase Storage

Open Graph Image Generation

OG Image Generation & Storage CDN Caching

Oak Server Middleware

Slack Bot Mention Edge Function

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/v1-list-all-functions

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

## Regional Invocations | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/regional-invocation

**Contents:**
- Regional Invocations
- Execute Edge Functions in specific regions for optimal performance.
- Available regions#
- Usage#
- Region runtime information#
- Region outages#

Execute Edge Functions in specific regions for optimal performance.

Edge Functions automatically execute in the region closest to the user making the request. This reduces network latency and provides faster responses.

However, if your function performs intensive database or storage operations, executing in the same region as your database often provides better performance:

The following regions are supported:

You can specify the region programmatically using the Supabase Client library, or using the x-region HTTP header.

In case you cannot add the x-region header to the request (e.g.: CORS requests, Webhooks), you can use forceFunctionRegion query parameter.

You can verify the execution region by looking at the x-sb-edge-region HTTP header in the response. You can also find it as metadata in Edge Function Logs.

Functions have access to the following environment variables:

SB_REGION: The AWS region function was invoked

This is useful if you have read replicate and want to Postgres connect to a different replicate according of the Region.

When you explicitly specify a region via the x-region header, requests will NOT be automatically re-routed to another region.

During outages, consider temporarily changing to a different region.

Test your function's performance with and without regional specification to determine if the benefits outweigh automatic region selection.

**Examples:**

Example 1 (python):
```python
1import { createClient, FunctionRegion } from '@supabase/supabase-js'23const { data, error } = await supabase.functions.invoke('function-name', {4  ...5  region: FunctionRegion.UsEast1, // Execute in us-east-1 region6})
```

---

## Generating OG Images | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/og-image

**Contents:**
- Generating OG Images
- Code#

Generate Open Graph images with Deno and Supabase Edge Functions. View on GitHub.

Create a handler.tsx file to construct the OG image in React:

Create an index.ts file to execute the handler on incoming requests:

**Examples:**

Example 1 (python):
```python
1import React from 'https://esm.sh/react@18.2.0'2import { ImageResponse } from 'https://deno.land/x/og_edge@0.0.4/mod.ts'34export default function handler(req: Request) {5  return new ImageResponse(6    (7      <div8        style={{9          width: '100%',10          height: '100%',11          display: 'flex',12          alignItems: 'center',13          justifyContent: 'center',14          fontSize: 128,15          background: 'lavender',16        }}17      >18        Hello OG Image!19      </div>20    )21  )22}
```

Example 2 (python):
```python
1import handler from './handler.tsx'23console.log('Hello from og-image Function!')45Deno.serve(handler)
```

---

## Upstash Redis | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/upstash-redis

**Contents:**
- Upstash Redis
- Redis database setup#
- Code#
- Run locally#
- Deploy#

A Redis counter example that stores a hash of function invocation count per region. Find the code on GitHub.

Create a Redis database using the Upstash Console or Upstash CLI.

Select the Global type to minimize the latency from all edge locations. Copy the UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN to your .env file.

You'll find them under Details > REST API > .env.

Make sure you have the latest version of the Supabase CLI installed.

Create a new function in your project:

And add the code to the index.ts file:

Navigate to http://localhost:54321/functions/v1/upstash-redis-counter.

**Examples:**

Example 1 (unknown):
```unknown
1cp supabase/functions/upstash-redis-counter/.env.example supabase/functions/upstash-redis-counter/.env
```

Example 2 (unknown):
```unknown
1supabase functions new upstash-redis-counter
```

Example 3 (python):
```python
1import { Redis } from 'https://deno.land/x/upstash_redis@v1.19.3/mod.ts'23console.log(`Function "upstash-redis-counter" up and running!`)45Deno.serve(async (_req) => {6  try {7    const redis = new Redis({8      url: Deno.env.get('UPSTASH_REDIS_REST_URL')!,9      token: Deno.env.get('UPSTASH_REDIS_REST_TOKEN')!,10    })1112    const deno_region = Deno.env.get('DENO_REGION')13    if (deno_region) {14      // Increment region counter15      await redis.hincrby('supa-edge-counter', deno_region, 1)16    } else {17      // Increment localhost counter18      await redis.hincrby('supa-edge-counter', 'localhost', 1)19    }2021    // Get all values22    const counterHash: Record<string, number> | null = await redis.hgetall('supa-edge-counter')23    const counters = Object.entries(counterHash!)24      .sort(([, a], [, b]) => b - a) // sort desc25      .reduce((r, [k, v]) => ({ total: r.total + v, regions: { ...r.regions, [k]: v } }), {26        total: 0,27        regions: {},28      })2930    return new Response(JSON.stringify({ counters }), { status: 200 })31  } catch (error) {32    return new Response(JSON.stringify({ error: error.message }), { status: 200 })33  }34})
```

Example 4 (unknown):
```unknown
1supabase start2supabase functions serve --no-verify-jwt --env-file supabase/functions/upstash-redis-counter/.env
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-functions-download

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

## Limits | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/limits

**Contents:**
- Limits
- Limits applied Edge Functions in Supabase's hosted platform.
- Runtime limits#
- Platform limits#
  - Secrets#
- Other limits & restrictions#

Limits applied Edge Functions in Supabase's hosted platform.

---

## Rate Limiting Edge Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/rate-limiting

**Contents:**
- Rate Limiting Edge Functions

Rate Limiting Edge Functions

Redis is an open source (BSD licensed), in-memory data structure store used as a database, cache, message broker, and streaming engine. It is optimized for atomic operations like incrementing a value, for example for a view counter or rate limiting. We can even rate limit based on the user ID from Supabase Auth!

Upstash provides an HTTP/REST based Redis client which is ideal for serverless use-cases and therefore works well with Supabase Edge Functions.

Find the code on GitHub.

---

## Dart Edge | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/dart-edge

**Contents:**
- Dart Edge

Be aware that the Dart Edge project is currently not actively maintained due to numerous breaking changes in Dart's development of (WASM) support.

Dart Edge is an experimental project that enables you to write Supabase Edge Functions using Dart. It's built and maintained by Invertase.

For detailed information on how to set up and use Dart Edge with Supabase, refer to the official Dart Edge documentation for Supabase.

---

## Using Wasm modules | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/wasm

**Contents:**
- Using Wasm modules
- Use WebAssembly in Edge Functions.
  - Writing a Wasm module#
  - Create a new Edge Function
  - Create a new Cargo project
  - Add the Wasm module code
  - Update the Cargo.toml file
  - Build the Wasm module
- Calling the Wasm module from the Edge Function#
- Bundle and deploy#

Use WebAssembly in Edge Functions.

Edge Functions supports running WebAssembly (Wasm) modules. WebAssembly is useful if you want to optimize code that's slower to run in JavaScript or require low-level manipulation.

For example, libraries like magick-wasm port existing C libraries to WebAssembly for complex image processing.

You can use different languages and SDKs to write Wasm modules. For this tutorial, we will write a simple Wasm module in Rust that adds two numbers.

Follow this guide on writing Wasm modules in Rust to setup your dev environment.

Create a new Edge Function called wasm-add

Create a new Cargo project for the Wasm module inside the function's directory:

Add the following code to add-wasm/src/lib.rs.

Update the add-wasm/Cargo.toml to include the wasm-bindgen dependency.

Build the package by running:

This will produce a Wasm binary file inside add-wasm/pkg directory.

Update your Edge Function to call the add function from the Wasm module:

Supabase Edge Functions currently use Deno 1.46. From Deno 2.1, importing Wasm modules will require even less boilerplate code.

Before deploying, ensure the Wasm module is bundled with your function by defining it in supabase/config.toml:

Deploy the function by running:

**Examples:**

Example 1 (unknown):
```unknown
1supabase functions new wasm-add
```

Example 2 (unknown):
```unknown
1cd supabase/functions/wasm-add2cargo new --lib add-wasm
```

Example 3 (unknown):
```unknown
1use wasm_bindgen::prelude::*;23#[wasm_bindgen]4pub fn add(a: u32, b: u32) -> u32 {5    a + b6}
```

Example 4 (unknown):
```unknown
1[package]2name = "add-wasm"3version = "0.1.0"4description = "A simple wasm module that adds two numbers"5license = "MIT/Apache-2.0"6edition = "2021"78[lib]9crate-type = ["cdylib"]1011[dependencies]12wasm-bindgen = "0.2"
```

---

## Edge Functions Architecture | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/architecture

**Contents:**
- Edge Functions Architecture
- Understanding the Architecture of Supabase Edge Functions
- 1. Understanding Edge Functions through an example: Image filtering#
- 2. Deployment process#
- 3. Global distribution and routing#
- 4. Execution mechanics: Fast and isolated#
- Benefits and use cases#

Edge Functions Architecture

Understanding the Architecture of Supabase Edge Functions

This guide explains the architecture and inner workings of Supabase Edge Functions, based on the concepts demonstrated in the video "Supabase Edge Functions Explained". Edge functions are serverless compute resources that run at the edge of the network, close to users, enabling low-latency execution for tasks like API endpoints, webhooks, and real-time data processing. This guide breaks down Edge Functions into key sections: an example use case, deployment process, global distribution, and execution mechanics.

To illustrate how edge functions operate, consider a photo-sharing app where users upload images and apply filters (e.g., grayscale or sepia) before saving them.

This example highlights edge functions as lightweight, on-demand code snippets that integrate seamlessly with Supabase services like Storage and Auth.

Deploying an edge function is straightforward and automated, requiring no manual server setup.

Key Benefits of Deployment:

Once deployed, the function is ready for invocation from anywhere, with Supabase handling scaling and availability.

Edge functions leverage a distributed architecture to minimize latency by running code close to the user.

Architecture Components:

How Distribution Works:

This global edge network is what makes edge functions "edge-native," providing consistent performance regardless of user location.

The core of edge functions' efficiency lies in their execution environment, which prioritizes speed, isolation, and scalability.

Execution Environment:

Performance Optimizations:

Isolation and Security:

Compared to traditional serverless or monolithic architectures, this setup offers lower latency, automatic scaling, and no infrastructure management, making it perfect for global apps.

---

## JavaScript: Invokes a Supabase Edge Function. | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/functions-invoke

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-functions-new

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

## Testing your Edge Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/unit-test

**Contents:**
- Testing your Edge Functions
- Writing Unit Tests for Edge Functions using Deno Test
- Testing in Deno#
- Folder structure#
- Example#
- Running Edge Functions locally#
- Resources#

Testing your Edge Functions

Writing Unit Tests for Edge Functions using Deno Test

Testing is an essential step in the development process to ensure the correctness and performance of your Edge Functions.

Deno has a built-in test runner that you can use for testing JavaScript or TypeScript code. You can read the official documentation for more information and details about the available testing functions.

We recommend creating your testing in a supabase/functions/tests directory, using the same name as the Function followed by -test.ts:

The following script is a good example to get started with testing your Edge Functions:

This test case consists of two parts.

Make sure to replace the placeholders (supabaseUrl, supabaseKey, my_table) with the actual values relevant to your Supabase setup.

To locally test and debug Edge Functions, you can utilize the Supabase CLI. Let's explore how to run Edge Functions locally using the Supabase CLI:

Ensure that the Supabase server is running by executing the following command:

In your terminal, use the following command to serve the Edge Functions locally:

This command starts a local server that runs your Edge Functions, enabling you to test and debug them in a development environment.

Create the environment variables file:

To run the tests, use the following command in your terminal:

**Examples:**

Example 1 (unknown):
```unknown
1└── supabase2    ├── functions3    │   ├── function-one4    │   │   └── index.ts5    │   └── function-two6    │   │   └── index.ts7    │   └── tests8    │       └── function-one-test.ts  # Tests for function-one9    │       └── function-two-test.ts  # Tests for function-two10    └── config.toml
```

Example 2 (python):
```python
1// Import required libraries and modules2import { assert, assertEquals } from 'jsr:@std/assert@1'3import { createClient, SupabaseClient } from 'npm:@supabase/supabase-js@2'45// Will load the .env file to Deno.env6import 'jsr:@std/dotenv/load'78// Set up the configuration for the Supabase client9const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? ''10const supabaseKey = Deno.env.get('SUPABASE_PUBLISHABLE_KEY') ?? ''11const options = {12  auth: {13    autoRefreshToken: false,14    persistSession: false,15    detectSessionInUrl: false,16  },17}1819// Test the creation and functionality of the Supabase client20const testClientCreation = async () => {21  var client: SupabaseClient = createClient(supabaseUrl, supabaseKey, options)2223  // Verify if the Supabase URL and key are provided24  if (!supabaseUrl) throw new Error('supabaseUrl is required.')25  if (!supabaseKey) throw new Error('supabaseKey is required.')2627  // Test a simple query to the database28  const { data: table_data, error: table_error } = await client29    .from('my_table')30    .select('*')31    .limit(1)32  if (table_error) {33    throw new Error('Invalid Supabase client: ' + table_error.message)34  }35  assert(table_data, 'Data should be returned from the query.')36}3738// Test the 'hello-world' function39const testHelloWorld = async () => {40  var client: SupabaseClient = createClient(supabaseUrl, supabaseKey, options)4142  // Invoke the 'hello-world' function with a parameter43  const { data: func_data, error: func_error } = await client.functions.invoke('hello-world', {44    body: { name: 'bar' },45  })4647  // Check for errors from the function invocation48  if (func_error) {49    throw new Error('Invalid response: ' + func_error.message)50  }5152  // Log the response from the function53  console.log(JSON.stringify(func_data, null, 2))5455  // Assert that the function returned the expected result56  assertEquals(func_data.message, 'Hello bar!')57}5859// Register and run the tests60Deno.test('Client Creation Test', testClientCreation)61Deno.test('Hello-world Function Test', testHelloWorld)
```

Example 3 (unknown):
```unknown
1supabase start
```

Example 4 (unknown):
```unknown
1supabase functions serve
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-functions-list

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

## GitHub Actions | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/github-actions

**Contents:**
- GitHub Actions

Use the Supabase CLI together with GitHub Actions to automatically deploy our Supabase Edge Functions. View on GitHub.

Since Supabase CLI v1.62.0 you can deploy all functions with a single command.

Individual function configuration like JWT verification and import map location can be set via the config.toml file.

**Examples:**

Example 1 (unknown):
```unknown
1name: Deploy Function23on:4  push:5    branches:6      - main7  workflow_dispatch:89jobs:10  deploy:11    runs-on: ubuntu-latest1213    env:14      SUPABASE_ACCESS_TOKEN: YOUR_SUPABASE_ACCESS_TOKEN15      PROJECT_ID: YOUR_SUPABASE_PROJECT_ID1617    steps:18      - uses: actions/checkout@v41920      - uses: supabase/setup-cli@v121        with:22          version: latest2324      - run: supabase functions deploy --project-ref $PROJECT_ID
```

Example 2 (unknown):
```unknown
1[functions.hello-world]2verify_jwt = false
```

---

## Logging | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/logging

**Contents:**
- Logging
- Monitor your Edge Functions with logging to track execution, debug issues, and optimize performance.
- Accessing logs#
  - Production#
  - Development#
- Log event types#
  - Automatic logs#
  - Custom logs#
- Logging tips#
  - Logging request headers#

Monitor your Edge Functions with logging to track execution, debug issues, and optimize performance.

Logs are provided for each function invocation, locally and in hosted environments.

Access logs from the Functions section of your Dashboard:

When developing locally you will see error messages and console log statements printed to your local terminal window.

Your functions automatically capture several types of events:

You can add your own log messages using standard console methods:

A custom log message can contain up to 10,000 characters. A function can log up to 100 events within a 10 second period.

When debugging Edge Functions, a common mistake is to try to log headers to the developer console via code like this:

The req.headers object appears empty because Headers objects don't store data in enumerable JavaScript properties, making them opaque to JSON.stringify().

Instead, you have to convert headers to a plain object first, for example using Object.fromEntries.

This results in something like:

**Examples:**

Example 1 (javascript):
```javascript
1Deno.serve(async (req) => {2  try {3    const { name } = await req.json()45    if (!name) {6      // Log a warning message7      console.warn('Empty name parameter received')8    }910    // Log a message11    console.log(`Processing request for: ${name}`)1213    const data = {14      message: `Hello ${name || 'Guest'}!`,15    }1617    return new Response(JSON.stringify(data), {18      headers: { 'Content-Type': 'application/json' },19    })20  } catch (error) {21    // Log an error message22    console.error(`Request processing failed: ${error.message}`)23    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {24      status: 500,25      headers: { 'Content-Type': 'application/json' },26    })27  }28})
```

Example 2 (javascript):
```javascript
1// ❌ This doesn't work as expected23Deno.serve(async (req) => {4  console.log(`Headers: ${JSON.stringify(req.headers)}`) // Outputs: "{}"5})
```

Example 3 (javascript):
```javascript
1// ✅ This works correctly2Deno.serve(async (req) => {3  const headersObject = Object.fromEntries(req.headers)4  const headersJson = JSON.stringify(headersObject, null, 2)56  console.log(`Request headers:\n${headersJson}`)7})
```

Example 4 (unknown):
```unknown
1Request headers: {2    "accept": "*/*",3    "accept-encoding": "gzip",4    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN1cGFuYWNobyIsInJvbGUiOiJhbm9uIiwieW91IjoidmVyeSBzbmVha3ksIGh1aD8iLCJpYXQiOjE2NTQ1NDA5MTYsImV4cCI6MTk3MDExNjkxNn0.cwBbk2tq-fUcKF1S0jVKkOAG2FIQSID7Jjvff5Do99Y",5    "cdn-loop": "cloudflare; subreqs=1",6    "cf-ew-via": "15",7    "cf-ray": "8597a2fcc558a5d7-GRU",8    "cf-visitor": "{\"scheme\":\"https\"}",9    "cf-worker": "supabase.co",10    "content-length": "20",11    "content-type": "application/x-www-form-urlencoded",12    "host": "edge-runtime.supabase.com",13    "my-custom-header": "abcd",14    "user-agent": "curl/8.4.0",15    "x-deno-subhost": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6InN1cGFiYXNlIn0.eyJkZXBsb3ltZW50X2lkIjoic3VwYW5hY2hvX2M1ZGQxMWFiLTFjYmUtNDA3NS1iNDAxLTY3ZTRlZGYxMjVjNV8wMDciLCJycGNfcm9vdCI6Imh0dHBzOi8vc3VwYWJhc2Utb3JpZ2luLmRlbm8uZGV2L3YwLyIsImV4cCI6MTcwODYxMDA4MiwiaWF0IjoxNzA4NjA5MTgyfQ.-fPid2kEeEM42QHxWeMxxv2lJHZRSkPL-EhSH0r_iV4",16    "x-forwarded-host": "edge-runtime.supabase.com",17    "x-forwarded-port": "443",18    "x-forwarded-proto": "https"19}
```

---

## Error Handling | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/error-handling

**Contents:**
- Error Handling
- Implement proper error responses and client-side handling to create reliable applications.
- Error handling#
- Client-side error handling#
- Error monitoring#

Implement proper error responses and client-side handling to create reliable applications.

Implementing the right error responses and client-side handling helps with debugging and makes your functions much easier to maintain in production.

Within your Edge Functions, return proper HTTP status codes and error messages:

Best practices for function errors:

Within your client-side code, an Edge Function can throw three types of errors:

Make sure to handle the errors properly. Functions that fail silently are hard to debug, functions with clear error messages get fixed fast.

You can see the production error logs in the Logs tab of your Supabase Dashboard.

For more information on Logging, check out this guide.

**Examples:**

Example 1 (javascript):
```javascript
1Deno.serve(async (req) => {2  try {3    // Your function logic here4    const result = await processRequest(req)5    return new Response(JSON.stringify(result), {6      headers: { 'Content-Type': 'application/json' },7      status: 200,8    })9  } catch (error) {10    console.error('Function error:', error)11    return new Response(JSON.stringify({ error: error.message }), {12      headers: { 'Content-Type': 'application/json' },13      status: 500,14    })15  }16})
```

Example 2 (python):
```python
1import { FunctionsHttpError, FunctionsRelayError, FunctionsFetchError } from '@supabase/supabase-js'23const { data, error } = await supabase.functions.invoke('hello', {4  headers: { 'my-custom-header': 'my-custom-header-value' },5  body: { foo: 'bar' },6})78if (error instanceof FunctionsHttpError) {9  const errorMessage = await error.context.json()10  console.log('Function returned an error', errorMessage)11} else if (error instanceof FunctionsRelayError) {12  console.log('Relay error:', error.message)13} else if (error instanceof FunctionsFetchError) {14  console.log('Fetch error:', error.message)15}
```

---

## Sending Emails | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/send-emails

**Contents:**
- Sending Emails
  - Prerequisites#
  - 1. Create Supabase function#
  - 2. Edit the handler function#
  - 3. Deploy and send email#
  - 4. Try it yourself#

Sending emails from Edge Functions using the Resend API.

To get the most out of this guide, you’ll need to:

Make sure you have the latest version of the Supabase CLI installed.

Create a new function locally:

Store the RESEND_API_KEY in your .env file.

Paste the following code into the index.ts file:

Run function locally:

Test it: http://localhost:54321/functions/v1/resend

Deploy function to Supabase:

When you deploy to Supabase, make sure that your RESEND_API_KEY is set in Edge Function Secrets Management

Open the endpoint URL to send an email:

Find the complete example on GitHub.

**Examples:**

Example 1 (unknown):
```unknown
1supabase functions new resend
```

Example 2 (javascript):
```javascript
1const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')23const handler = async (_request: Request): Promise<Response> => {4  const res = await fetch('https://api.resend.com/emails', {5    method: 'POST',6    headers: {7      'Content-Type': 'application/json',8      Authorization: `Bearer ${RESEND_API_KEY}`,9    },10    body: JSON.stringify({11      from: 'onboarding@resend.dev',12      to: 'delivered@resend.dev',13      subject: 'hello world',14      html: '<strong>it works!</strong>',15    }),16  })1718  const data = await res.json()1920  return new Response(JSON.stringify(data), {21    status: 200,22    headers: {23      'Content-Type': 'application/json',24    },25  })26}2728Deno.serve(handler)
```

Example 3 (unknown):
```unknown
1supabase start2supabase functions serve --no-verify-jwt --env-file .env
```

Example 4 (unknown):
```unknown
1supabase functions deploy resend --no-verify-jwt
```

---

## CORS (Cross-Origin Resource Sharing) support for Invoking from the browser | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/cors

**Contents:**
- CORS (Cross-Origin Resource Sharing) support for Invoking from the browser
  - Recommended setup#

CORS (Cross-Origin Resource Sharing) support for Invoking from the browser

To invoke edge functions from the browser, you need to handle CORS Preflight requests.

See the example on GitHub.

We recommend adding a cors.ts file within a _shared folder which makes it easy to reuse the CORS headers across functions:

You can then import and use the CORS headers within your functions:

**Examples:**

Example 1 (javascript):
```javascript
1export const corsHeaders = {2  'Access-Control-Allow-Origin': '*',3  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',4}
```

Example 2 (python):
```python
1import { corsHeaders } from '../_shared/cors.ts'23console.log(`Function "browser-with-cors" up and running!`)45Deno.serve(async (req) => {6  // This is needed if you're planning to invoke your function from a browser.7  if (req.method === 'OPTIONS') {8    return new Response('ok', { headers: corsHeaders })9  }1011  try {12    const { name } = await req.json()13    const data = {14      message: `Hello ${name}!`,15    }1617    return new Response(JSON.stringify(data), {18      headers: { ...corsHeaders, 'Content-Type': 'application/json' },19      status: 200,20    })21  } catch (error) {22    return new Response(JSON.stringify({ error: error.message }), {23      headers: { ...corsHeaders, 'Content-Type': 'application/json' },24      status: 400,25    })26  }27})
```

---

## Generate Images with Amazon Bedrock | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator

**Contents:**
- Generate Images with Amazon Bedrock
- Setup#
  - Configure Storage#
- Code#
- Run the function locally#
- Deploy to your hosted project#

Generate Images with Amazon Bedrock

Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon. Each model is accessible through a common API which implements a broad set of features to help build generative AI applications with security, privacy, and responsible AI in mind.

This guide will walk you through an example using the Amazon Bedrock JavaScript SDK in Supabase Edge Functions to generate images using the Amazon Titan Image Generator G1 model.

Create a new function in your project:

And add the code to the index.ts file:

You've now deployed a serverless function that uses AI to generate and upload images to your Supabase storage bucket.

**Examples:**

Example 1 (unknown):
```unknown
1AWS_DEFAULT_REGION="<your_region>"2AWS_ACCESS_KEY_ID="<replace_your_own_credentials>"3AWS_SECRET_ACCESS_KEY="<replace_your_own_credentials>"4AWS_SESSION_TOKEN="<replace_your_own_credentials>"56# Mocked config files7AWS_SHARED_CREDENTIALS_FILE="./aws/credentials"8AWS_CONFIG_FILE="./aws/config"
```

Example 2 (unknown):
```unknown
1supabase functions new amazon-bedrock
```

Example 3 (python):
```python
1// We need to mock the file system for the AWS SDK to work.2import { prepareVirtualFile } from 'https://deno.land/x/mock_file@v1.1.2/mod.ts'34import { BedrockRuntimeClient, InvokeModelCommand } from 'npm:@aws-sdk/client-bedrock-runtime'5import { createClient } from 'npm:@supabase/supabase-js'6import { decode } from 'npm:base64-arraybuffer'78console.log('Hello from Amazon Bedrock!')910Deno.serve(async (req) => {11  prepareVirtualFile('./aws/config')12  prepareVirtualFile('./aws/credentials')1314  const client = new BedrockRuntimeClient({15    region: Deno.env.get('AWS_DEFAULT_REGION') ?? 'us-west-2',16    credentials: {17      accessKeyId: Deno.env.get('AWS_ACCESS_KEY_ID') ?? '',18      secretAccessKey: Deno.env.get('AWS_SECRET_ACCESS_KEY') ?? '',19      sessionToken: Deno.env.get('AWS_SESSION_TOKEN') ?? '',20    },21  })2223  const { prompt, seed } = await req.json()24  console.log(prompt)25  const input = {26    contentType: 'application/json',27    accept: '*/*',28    modelId: 'amazon.titan-image-generator-v1',29    body: JSON.stringify({30      taskType: 'TEXT_IMAGE',31      textToImageParams: { text: prompt },32      imageGenerationConfig: {33        numberOfImages: 1,34        quality: 'standard',35        cfgScale: 8.0,36        height: 512,37        width: 512,38        seed: seed ?? 0,39      },40    }),41  }4243  const command = new InvokeModelCommand(input)44  const response = await client.send(command)45  console.log(response)4647  if (response.$metadata.httpStatusCode === 200) {48    const { body, $metadata } = response4950    const textDecoder = new TextDecoder('utf-8')51    const jsonString = textDecoder.decode(body.buffer)52    const parsedData = JSON.parse(jsonString)53    console.log(parsedData)54    const image = parsedData.images[0]5556    const supabaseClient = createClient(57      // Supabase API URL - env var exported by default.58      Deno.env.get('SUPABASE_URL')!,59      // Supabase API ANON KEY - env var exported by default.60      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!61    )6263    const { data: upload, error: uploadError } = await supabaseClient.storage64      .from('images')65      .upload(`${$metadata.requestId ?? ''}.png`, decode(image), {66        contentType: 'image/png',67        cacheControl: '3600',68        upsert: false,69      })70    if (!upload) {71      return Response.json(uploadError)72    }73    const { data } = supabaseClient.storage.from('images').getPublicUrl(upload.path!)74    return Response.json(data)75  }7677  return Response.json(response)78})
```

Example 4 (unknown):
```unknown
1curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/amazon-bedrock' \2    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \3    --header 'Content-Type: application/json' \4    --data '{"prompt":"A beautiful picture of a bird"}'
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/supabase-functions-serve

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

## Supabase Docs | Edge Functions Troubleshooting

**URL:** https://supabase.com/docs/guides/functions/troubleshooting

---

## Sending Push Notifications | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/examples/push-notifications

**Contents:**
- Sending Push Notifications
- Supabase setup#
- Expo setup#
- Enhanced security for push notifications#
- Deploy the Supabase Edge Function#
- Create the database webhook#
- Send push notification#

Sending Push Notifications

Push notifications are an important part of any mobile app. They allow you to send notifications to your users even when they are not using your app. This guide will show you how to send push notifications to different mobile app frameworks from your Supabase edge functions.

Expo makes implementing push notifications easy. All the hassle with device information and communicating with Firebase Cloud Messaging (FCM) or Apple Push Notification Service (APNs) is done behind the scenes. This allows you to treat Android and iOS notifications in the same way and save time both on the frontend and backend.

Find the example code on GitHub.

To utilize Expo's push notification service, you must configure your app by installing a set of libraries, implementing functions to handle notifications, and setting up credentials for Android and iOS. Follow the official Expo Push Notifications Setup Guide to get the credentials for Android and iOS. This project uses Expo's EAS build service to simplify this part.

The database webhook handler to send push notifications is located in supabase/functions/push/index.ts. Deploy the function to your linked project and set the EXPO_ACCESS_TOKEN secret.

Navigate to the Database Webhooks settings in your Supabase Dashboard.

**Examples:**

Example 1 (python):
```python
1import { createClient } from 'npm:@supabase/supabase-js@2'23console.log('Hello from Functions!')45interface Notification {6  id: string7  user_id: string8  body: string9}1011interface WebhookPayload {12  type: 'INSERT' | 'UPDATE' | 'DELETE'13  table: string14  record: Notification15  schema: 'public'16  old_record: null | Notification17}1819const supabase = createClient(20  Deno.env.get('SUPABASE_URL')!,21  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!22)2324Deno.serve(async (req) => {25  const payload: WebhookPayload = await req.json()26  const { data } = await supabase27    .from('profiles')28    .select('expo_push_token')29    .eq('id', payload.record.user_id)30    .single()3132  const res = await fetch('https://exp.host/--/api/v2/push/send', {33    method: 'POST',34    headers: {35      'Content-Type': 'application/json',36      Authorization: `Bearer ${Deno.env.get('EXPO_ACCESS_TOKEN')}`,37    },38    body: JSON.stringify({39      to: data?.expo_push_token,40      sound: 'default',41      body: payload.record.body,42    }),43  }).then((res) => res.json())4445  return new Response(JSON.stringify(res), {46    headers: { 'Content-Type': 'application/json' },47  })48})
```

---

## Deploy to Production | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/deploy

**Contents:**
- Deploy to Production
- Deploy your Edge Functions to your remote Supabase Project.
- Step 1: Authenticate#
- Step 2: Connect your project#
      - Need a new project?
- Step 3: Deploy Functions#
  - Deploying public functions#
- Step 4: Verify successful deployment#
- Step 5: Test your live function#
- CI/CD deployment#

Deploy your Edge Functions to your remote Supabase Project.

Once you have developed your Edge Functions locally, you can deploy them to your Supabase project.

Before getting started, make sure you have the Supabase CLI installed. Check out the CLI installation guide for installation methods and troubleshooting.

Log in to the Supabase CLI if you haven't already:

Get the project ID associated with your function:

If you haven't yet created a Supabase project, you can do so by visiting database.new.

Link your local project to your remote Supabase project using the ID you just retrieved:

Now you should have your local development environment connected to your production project.

You can deploy all edge functions within the functions folder with a single command:

Or deploy individual Edge Functions by specifying the function name:

By default, Edge Functions require a valid JWT in the authorization header. If you want to deploy Edge Functions without Authorization checks (commonly used for Stripe webhooks), you can pass the --no-verify-jwt flag:

Be careful when using this flag, as it will allow anyone to invoke your Edge Function without a valid JWT. The Supabase client libraries automatically handle authorization.

🎉 Your function is now live!

When the deployment is successful, your function is automatically distributed to edge locations worldwide. Your edge functions is now running globally at https://[YOUR_PROJECT_ID].supabase.co/functions/v1/hello-world.

You can now invoke your Edge Function using the project's ANON_KEY, which can be found in the API settings of the Supabase Dashboard. You can invoke it from within your app:

Note that the SUPABASE_PUBLISHABLE_KEY is different in development and production. To get your production anon key, you can find it in your Supabase dashboard under Settings > API.

You should now see the expected response:

You can also test the function through the Dashboard. To see how that works, check out the Dashboard Quickstart guide.

You can use popular CI / CD tools like GitHub Actions, Bitbucket, and GitLab CI to automate Edge Function deployments.

You can use the official setup-cli GitHub Action to run Supabase CLI commands in your GitHub Actions.

The following GitHub Action deploys all Edge Functions any time code is merged into the main branch:

Here is the sample pipeline configuration to deploy via GitLab CI.

Here is the sample pipeline configuration to deploy via Bitbucket.

Individual function configuration like JWT verification and import map location can be set via the config.toml file.

This ensures your function configurations are consistent across all environments and deployments.

This example shows a GitHub Actions workflow that deploys all Edge Functions when code is merged into the main branch.

**Examples:**

Example 1 (unknown):
```unknown
1supabase login
```

Example 2 (unknown):
```unknown
1supabase projects list
```

Example 3 (unknown):
```unknown
1supabase link --project-ref your-project-id
```

Example 4 (unknown):
```unknown
1supabase functions deploy
```

---
