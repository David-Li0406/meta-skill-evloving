# Temporal-Cloud - Getting Started

**Pages:** 1

---

## Quickstart - Setup

**URL:** llms-txt#quickstart---setup

**Contents:**
- Install Node.js
- Install the Temporal TypeScript SDK
- Install Temporal CLI
- Start the development server
- Run Hello World: Test Your Installation
  - 1. Create the Activity
  - 2. Create the Workflow
  - 3. Create and Run the Worker
  - 4. Execute the Workflow
  - Verify Success

Configure your local development environment to get started developing with Temporal.

<SetupSteps>
<SetupStep code={
  <>
    The TypeScript SDK requires Node.js 18 or later.
    Install Node.js via your package manager by following the official Node.js instructions.
  </>
}>
## Install Node.js

The TypeScript SDK requires Node.js 18 or later. Install Node.js via your package manager by following the official Node.js instructions.

<SetupStep code={
<>
<CodeSnippet language="bash">
npx @temporalio/create@latest ./my-app
</CodeSnippet>

When prompted to select a sample, choose the hello-world sample.
</>
}>

## Install the Temporal TypeScript SDK

You can create a new project with the Temporal SDK:

If you're creating a new project using `npx @temporalio/create`, the required SDK packages will be installed automatically.

To add Temporal to an existing project, install the required packages manually with `npm install @temporalio/client @temporalio/worker @temporalio/workflow`.

Next, you'll configure a local Temporal Service for development.

<SetupStep code={
<>
<Tabs>
<TabItem value="macos" label="macOS" default>

Install the Temporal CLI using Homebrew:
        <CodeSnippet language="bash">
        brew install temporal
        </CodeSnippet>
      </TabItem>

<TabItem value="windows" label="Windows">
        Download the Temporal CLI archive for your architecture:
        
          Windows amd64
          Windows arm64
        
        Extract it and add <code>temporal.exe</code> to your PATH.
      </TabItem>

<TabItem value="linux" label="Linux">
        Download the Temporal CLI for your architecture:
        
          Linux amd64
          Linux arm64
        
        Extract the archive and move the <code>temporal</code> binary into your PATH, for example:
        <CodeSnippet language="bash">
        sudo mv temporal /usr/local/bin
        </CodeSnippet>
      </TabItem>
    </Tabs>

## Install Temporal CLI

The fastest way to get a development version of the Temporal Service running on your local machine is to use [Temporal CLI](https://docs.temporal.io/cli).

Choose your operating system to install Temporal CLI.

After installing, open a new Terminal window and start the development server:

<CodeSnippet language="bash">
temporal server start-dev
</CodeSnippet>

Change the Web UI port
The Temporal Web UI may be on a different port in some examples or tutorials. To change the port for the Web UI, use the <code>--ui-port</code> option when starting the server:
<CodeSnippet language="bash">
temporal server start-dev --ui-port 8080
</CodeSnippet>
The Temporal Web UI will now be available at http://localhost:8080.

<style>
{`.port-info { background: rgba(68, 76, 231, 0.1); border: 1px solid rgba(68, 76, 231, 0.2); border-radius: 0.75rem; padding: 1.5rem; margin: 1.5rem 0; transition: all 0.3s ease-in-out; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); } [data-theme='dark'] .port-info { background: rgba(68, 76, 231, 0.15); border-color: rgba(68, 76, 231, 0.3); } .port-info h4 { margin-top: 0; margin-bottom: 1rem; color: var(--ifm-color-emphasis-900); font-weight: 600; } .port-info p { margin-bottom: 1rem; font-size: 0.95rem; line-height: 1.5; color: var(--ifm-color-emphasis-800); } .port-info p:last-child { margin-bottom: 0; } .port-info code { background: rgba(255, 255, 255, 0.5); padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.9em; } [data-theme='dark'] .port-info code { background: rgba(0, 0, 0, 0.2); } @media (max-width: 768px) { .port-info { padding: 1.25rem; } }`}
</style>
</>
}>

## Start the development server

Once you've installed Temporal CLI and added it to your PATH, open a new Terminal window and run the following command.

This command starts a local Temporal Service. It starts the Web UI, creates the default Namespace, and uses an in-memory database.

The Temporal Service will be available on localhost:7233.
The Temporal Web UI will be available at http://localhost:8233.

Leave the local Temporal Service running as you work through tutorials and other projects. You can stop the Temporal Service at any time by pressing CTRL+C.

Once you have everything installed, you're ready to build apps with Temporal on your local machine.

</SetupStep>
</SetupSteps>

## Run Hello World: Test Your Installation

Now let's verify your setup is working by creating and running a complete Temporal application with both a Workflow and Activity.

This test will confirm that:

- The Temporal TypeScript SDK is properly installed
- Your local Temporal Service is running
- You can successfully create and execute Workflows and Activities
- The communication between components is functioning correctly

### 1. Create the Activity

Create an Activity file (activities.ts):

An Activity is a normal function or method that executes a single, well-defined action (either short or long running), which often involve interacting with the outside world, such as sending emails, making network requests, writing to a database, or calling an API, which are prone to failure. If an Activity fails, Temporal automatically retries it based on your configuration.

### 2. Create the Workflow

Create a Workflow file (workflows.ts):

Workflows orchestrate Activities and contain the application logic.
Temporal Workflows are resilient.
They can run and keep running for years, even if the underlying infrastructure fails.
If the application itself crashes, Temporal will automatically recreate its pre-failure state so it can continue right where it left off.

### 3. Create and Run the Worker

Create a Worker file (worker.ts):

Run the Worker and keep this terminal running:

With your Activity and Workflow defined, you need a Worker to execute them.
A Worker polls a Task Queue, that you configure it to poll, looking for work to do. Once the Worker dequeues a Workflow or Activity task from the Task Queue, it then executes that task.

Workers are a crucial part of your Temporal application as they're what actually execute the tasks defined in your Workflows and Activities.
For more information on Workers, see [Understanding Temporal](/evaluate/understanding-temporal#workers) and a [deep dive into Workers](/workers).

### 4. Execute the Workflow

Now that your Worker is running, it's time to start a Workflow Execution.

This final step will validate that everything is working correctly with your file labeled `client.ts`.

Create a separate file called `client.ts`.

If everything is working correctly, you should see:

- Worker processing the workflow and activity
- Output: `Workflow result: Hello, Temporal!`
- Workflow Execution details in the [Temporal Web UI](http://localhost:8233)

<details>
<summary>Additional details about Workflow Execution</summary>

- Temporal clients are not explicitly closed.
- To enable TLS, the `tls` option can be set to `true` or a `Temporalio::Client::Connection::TLSOptions` instance.
- Calling `client.workflow.start()` and `client.workflow.execute()` send a command to Temporal Server to schedule a new Workflow Execution on the specified Task Queue.
- If you started a Workflow with `client.workflow.start()`, you can choose to wait for the result anytime with handle.result().
- Using a Workflow Handle isn't necessary with `client.workflow.execute()`.

<CallToAction href="https://learn.temporal.io/getting_started/typescript/first_program_in_typescript/">
  Next: Run your first Temporal Application
  Create a basic Workflow and run it with the Temporal TypeScript SDK
</CallToAction>

## Temporal Client - Typescript SDK

A [Temporal Client](/encyclopedia/temporal-sdks#temporal-client) enables you to communicate with the Temporal Service.
Communication with a Temporal Service lets you perform actions such as starting Workflow Executions, sending Signals and
Queries to Workflow Executions, getting Workflow results, and more. You cannot initialize a Temporal Client inside a
Workflow. However, they're commonly initialized inside an Activity to communicate with a Temporal Service.

This page shows you how to do the following using the TypeScript SDK with the Temporal Client:

- [Connect to a local development Temporal Service](#connect-to-development-service)
- [Connect to Temporal Cloud](#connect-to-temporal-cloud)
- [Connect to Temporal Service from a Worker](#connect-to-temporal-service-from-a-worker)
- [Start a Workflow Execution](#start-workflow-execution)
- [Get Workflow results](#get-workflow-results)

In the TypeScript SDK, connecting to Temporal Service from a Temporal Application and from within an Activity rely on a
different type of connection than connecting from a Worker. The sections
[Connect to a local development Temporal Service](#connect-to-development-service) and
[Connect to Temporal Cloud](#connect-to-temporal-cloud) apply to connecting from a Temporal Application or from within
an Activity. See [Connect to Temporal Service from a Worker](#connect-to-temporal-service-from-a-worker) for details on
connecting from a Worker.

## Connect to development Temporal Service {#connect-to-development-service}

To connect to a development Temporal service from a Temporal Application or from within an Activity, import the
[`Connection` class](https://typescript.temporal.io/api/classes/client.Connection) from `@temporalio/client` and use
[`Connection.connect`](https://typescript.temporal.io/api/classes/client.Connection#connect) to create a Connection
object to connect to the Temporal Service. Then pass in that connection when you create a new `Client` instance. If you
leave the connection options empty, the SDK defaults to connecting to `127.0.0.1:7233` in the `default` Namespace.

If you need to connect to a Temporal Service with custom options, you can provide connection options directly in code,
load them from **environment variables**, or a **TOML configuration file** using the `@temporalio/envconfig` helpers. We
recommend environment variables or a configuration file for secure, repeatable configuration.

<Tabs groupId="connect-options" defaultValue="config-file" >

<TabItem value="config-file" label="Configuration File">

You can use a TOML configuration file to set connection options for the Temporal Client. The configuration file lets you
configure multiple profiles, each with its own set of connection options. You can then specify which profile to use when
creating the Temporal Client.

You can use the environment variable `TEMPORAL_CONFIG_FILE` to specify the location of the TOML file or provide the path
to the file directly in code. If you don't provide the configuration file path, the SDK looks for it at the path
`~/.config/temporalio/temporal.toml` or the equivalent on your OS. Refer to
[Environment Configuration](../environment-configuration.mdx) for more details about configuration files and profiles.

The connection options set in configuration files have lower precedence than environment variables. This means that if
you set the same option in both the configuration file and as an environment variable, the environment variable value
overrides the option set in the configuration file.

For example, the following TOML configuration file defines two profiles: `default` and `prod`. Each profile has its own
set of connection options.

```toml title="config.toml"

**Examples:**

Example 1 (ts):
```ts
export async function greet(name: string): Promise<string> {
  return `Hello, ${name}!`;
}
```

Example 2 (ts):
```ts
// Only import the activity types

const { greet } = proxyActivities<typeof activities>({
  startToCloseTimeout: '1 minute',
});

/** A workflow that simply calls an activity */
export async function example(name: string): Promise<string> {
  return await greet(name);
}
```

Example 3 (ts):
```ts
async function run() {
  // Step 1: Establish a connection with Temporal server.
  //
  // Worker code uses `@temporalio/worker.NativeConnection`.
  // (But in your application code it's `@temporalio/client.Connection`.)
  const connection = await NativeConnection.connect({
    address: 'localhost:7233',
    // TLS and gRPC metadata configuration goes here.
  });
  try {
    // Step 2: Register Workflows and Activities with the Worker.
    const worker = await Worker.create({
      connection,
      namespace: 'default',
      taskQueue: 'hello-world',
      // Workflows are registered using a path as they run in a separate JS context.
      workflowsPath: require.resolve('./workflows'),
      activities,
    });

    // Step 3: Start accepting tasks on the `hello-world` queue
    //
    // The worker runs until it encounters an unexpected error or the process receives a shutdown signal registered on
    // the SDK Runtime object.
    //
    // By default, worker logs are written via the Runtime logger to STDERR at INFO level.
    //
    // See https://typescript.temporal.io/api/classes/worker.Runtime#install to customize these defaults.
    await worker.run();
  } finally {
    // Close the connection once the worker has stopped
    await connection.close();
  }
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

Example 4 (bash):
```bash
npm run start
```

---
