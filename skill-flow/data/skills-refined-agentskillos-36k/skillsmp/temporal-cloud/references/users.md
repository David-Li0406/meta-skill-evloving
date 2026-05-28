# Temporal-Cloud - Users

**Pages:** 3

---

## ... assumes my_otel_tracer_provider is a tracer provider created by the user

**URL:** llms-txt#...-assumes-my_otel_tracer_provider-is-a-tracer-provider-created-by-the-user

**Contents:**
- Log from a Workflow {#logging}
- Use Visibility APIs {#visibility}
  - Use Search Attributes {#search-attributes}
  - List Workflow Executions {#list-workflow-executions}
  - Set Custom Search Attributes {#custom-search-attributes}

my_tracer = my_otel_tracer_provider.tracer('my-otel-tracer')

my_client = Temporalio::Client.connect(
  'localhost:7233', 'my-namespace',
  interceptors: [Temporalio::Contrib::OpenTelemetry::TracingInterceptor.new(my_tracer)]
)
ruby
require 'logger'
require 'temporalio/client'

my_client = Temporalio::Client.connect(
  'localhost:7233', 'my-namespace',
  logger: Logger.new($stdout, level: Logger::INFO)
)
ruby
Temporalio::Workflow.logger.info("Some log #{some_value}")
ruby
Temporalio::Activity::Context.current.logger.info("Some log #{some_value}")
ruby
my_client.list_workflows("WorkflowType='GreetingWorkflow'").each do |wf|
  puts "Workflow: #{wf.id}"
end
ruby

**Examples:**

Example 1 (unknown):
```unknown
When your Client is connected, spans are created for all Client calls, Activities, and Workflow invocations on the Worker.
Spans are created and serialized through the server to give one trace for a Workflow Execution.

## Log from a Workflow {#logging}

Logging enables you to capture and persist important execution details from your Workflow and Activity code.

Logging levels typically include:

| Level   | Use                                                                                                       |
| ------- | --------------------------------------------------------------------------------------------------------- |
| `DEBUG` | Detailed information, typically useful for debugging purposes.                                            |
| `INFO`  | General information about the application's operation.                                                    |
| `WARN`  | Indicates potentially harmful situations or minor issues that don't prevent the application from working. |
| `ERROR` | Indicates error conditions that might still allow the application to continue running.                    |

Logging uses the Ruby standard logging APIs.
The `logger` can be set when connecting a client.
The following example shows logging on the console and sets the level to `INFO`.
```

Example 2 (unknown):
```unknown
You can log from a Workflow using `Temporalio::Workflow.logger` which is a special instance of Ruby's `Logger` that
appends workflow details to every log and does not log during replay.
```

Example 3 (unknown):
```unknown
There's also one for use in activities that appends Activity details to every log:
```

Example 4 (unknown):
```unknown
## Use Visibility APIs {#visibility}

Visibility refers to Temporal features for listing, filtering, and inspecting Workflow Executions.

### Use Search Attributes {#search-attributes}

- [Default Search Attributes](/search-attribute#default-search-attribute) like `WorkflowType`, `StartTime`, and `ExecutionStatus` are automatically indexed.
- [Custom Search Attributes](/search-attribute#custom-search-attribute) let you store domain-specific metadata for Workflows.

The typical method of retrieving a Workflow Execution is by its Workflow Id.

However, sometimes you'll want to retrieve one or more Workflow Executions based on another property. For example, imagine you want to get all Workflow Executions of a certain type that have failed within a time range, so that you can start new ones with the same arguments.

You can do this with [Search Attributes](/search-attribute).

- [Default Search Attributes](/search-attribute#default-search-attribute) like `WorkflowType`, `StartTime` and `ExecutionStatus` are automatically added to Workflow Executions.
- _Custom Search Attributes_ can contain their own domain-specific data (like `customerId` or `numItems`).
- A few [generic Custom Search Attributes](/search-attribute#custom-search-attribute) like `CustomKeywordField` and `CustomIntField` are created by default in Temporal's [Docker Compose](https://github.com/temporalio/docker-compose).

The steps to using custom Search Attributes are:

- Create a new Search Attribute in your Temporal Service in the CLI or Web UI.
  - For example: `temporal operator search-attribute create --name CustomKeywordField --type Text`
    - Replace `CustomKeywordField` with the name of your Search Attribute.
    - Replace `Text` with a type value associated with your Search Attribute: `Text` | `Keyword` | `Int` | `Double` | `Bool` | `Datetime` | `KeywordList`
- Set the value of the Search Attribute for a Workflow Execution:
  - On the Client by including it as an argument when starting the Execution.
  - In the Workflow by calling `Temporalio::Workflow.upsert_search_attributes`.
- Read the value of the Search Attribute:
  - On the Client by calling `describe` on a `WorkflowHandle`.
  - In the Workflow by looking at `Temporalio::Workflow.search_attributes`.
- Query Workflow Executions by the Search Attribute using a [List Filter](/list-filter):
  - [In the Temporal CLI](/cli/operator#list-2)
  - In code by calling `list_workflows`.

### List Workflow Executions {#list-workflow-executions}

Use the [list_workflows](https://ruby.temporal.io/Temporalio/Client.html#list_workflows-instance_method) method on the Client and pass a [List Filter](/list-filter) as an argument to filter the listed Workflows.
The result is a lazy enumerator/enumerable.
```

---

## the handle's result to wait for cancellation to be applied.

**URL:** llms-txt#the-handle's-result-to-wait-for-cancellation-to-be-applied.

**Contents:**
- Termination {#termination}

handle.cancel
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    # Create a new cancellation linked to the workflow one, so that it inherits
    # cancellation that comes from the workflow. Users can choose to make it
    # completely detached by not providing a parent.
    cancellation, cancel_proc = Temporalio::Cancellation.new(
      Temporalio::Workflow.cancellation
    )

# Start the activity in the background. Whether this workflow waits on the activity
    # to handle the cancellation or not is dependent upon the cancellation_type
    # parameter. We leave the default here which sends the cancellation but does not wait
    # on it to be handled.
    future = Temporalio::Future.new do
      Temporalio::Workflow.execute_activity(
        MyActivity,
        start_to_close_timeout: 100,
        cancellation:
      )
    end

# Wait 5 minutes, then cancel it
    Temporalio::Workflow.sleep(5 * 60)
    cancel_proc.call

# Wait on the activity which will raise an activity error with a cause of
    # cancellation which will fail the workflow
    future.wait
  end
end
ruby

**Examples:**

Example 1 (unknown):
```unknown
By default, Activities are automatically cancelled when the Workflow is cancelled since the workflow cancellation is
used by activities by default. To issue a cancellation explicitly, a new cancellation token can be created.
```

Example 2 (unknown):
```unknown
## Termination {#termination}

To Terminate a Workflow Execution in Ruby, use the `terminate` method on the Workflow handle.
```

---

## Delete connections

**URL:** llms-txt#delete-connections

**Contents:**
- Server Frontend API Reference
- gRPC API
  - Use with code
  - Use manually
- HTTP API
- Self-hosted Temporal Nexus
- Enable Nexus
- Build and use Nexus Services
- Learn more
- Upgrade the Temporal Server

temporal operator cluster remove --name="someClusterName"
shell
git clone https://github.com/temporalio/api.git
cd api
shell
cd /path/to/api
evans --proto temporal/api/workflowservice/v1/service.proto --port 7233
shell
evans --proto temporal/api/workflowservice/v1/service.proto --host devrel.a2dd6.tmprl.cloud --port 7233 --tls --cert /Users/me/certs/temporal.pem --certkey /Users/me/certs/temporal.key
shell
/path/to/api/temporal/api/workflowservice/v1/service.proto
`sh
$ curl localhost:8233/api/v1/namespaces/default/workflows

{
  "executions": [
    {
      "execution": {
        "workflowId": "workflow-_homozdkzYWLRpX6Rfou5",
        "runId": "c981cb26-baa4-4af8-ac5f-866451d3f83c"
      },
      "type": {
        "name": "example"
      },
      "startTime": ...
    },
    ...
  ],
  "nextPageToken": null
}
`

## Self-hosted Temporal Nexus

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

Temporal Nexus is now [Generally Available](/evaluate/development-production-features/release-stages#general-availability).
Learn why you should use Nexus in the [evaluation guide](/evaluate/nexus).

[Temporal Nexus](/nexus) allows you to reliably connect Temporal Applications.
It was designed with Durable Execution in mind and enables each team to have their own Namespace for improved modularity, security, debugging, and fault isolation.

<CaptionedImage
    src="/img/cloud/nexus/nexus-overview-short.png"
    title="Nexus Overview"
/>

Enable Nexus in your self-hosted Temporal Service by updating the server's static configuration file and enabling Nexus through dynamic config, then setting the public callback URL and allowed callback addresses.
Nexus is only supported in single cluster setups at this time.
For additional information on operating Nexus workloads in your self-hosted cluster, see [Nexus Architecture](https://github.com/temporalio/temporal/blob/main/docs/architecture/nexus.md).

:::note
Replace `$PUBLIC_URL` with a URL value that's accessible to external callers or internally within the cluster.
Currently, external Nexus calls are considered experimental so it should be safe to use the address of an internal load balancer for the Frontend Service.
:::

To enable Nexus in your deployment:

1. Ensure that the server's static configuration file enables the HTTP API.

2. Enable Nexus through dynamic config, set the public callback URL, and set the allowed callback addresses.

## Build and use Nexus Services

Nexus has a familiar programming model to build and use Nexus Services using the Temporal SDK.
The [Nexus Operation lifecycle](/nexus/operations#operation-lifecycle) supports both synchronous and asynchronous Operations.
Nexus Operations can be implemented with Temporal primitives, like a Workflow, or execute arbitrary code.

- [Go SDK - Nexus quick start and code sample](/develop/go/nexus)
- [Java SDK - Nexus quick start and code sample](/develop/java/nexus)

- [Evaluate](/evaluate/nexus) why you should use Nexus and watch the [Nexus keynote and demo](https://youtu.be/qqc2vsv1mrU?feature=shared&t=2082).
- [Learn key Nexus concepts](/nexus) and how Nexus works in the [Nexus deep dive talk](https://www.youtube.com/watch?v=izR9dQ_eIe4&t=934s)
- Explore [additional resources](/evaluate/nexus#learn-more) to learn more about Nexus.

## Upgrade the Temporal Server

## How to upgrade the Temporal Server version {#upgrade-server}

If a newer version of the [Temporal Server](/temporal-service/temporal-server) is available, a notification appears in the Temporal Web UI.

If you are using a version that is older than 1.0.0, reach out to us at [community.temporal.io](http://community.temporal.io) to ask how to upgrade.

First check to see if an upgrade to the database schema is required for the version you wish to upgrade to.
If a database schema upgrade is required, it will be called out directly in the [release notes](https://github.com/temporalio/temporal/releases).
Some releases require changes to the schema, and some do not.
We ensure that any consecutive versions are compatible in terms of database schema upgrades, features, and system behavior; however there is no guarantee that there is compatibility between _any_ two non-consecutive versions.

### Key considerations

When upgrading the Temporal Server, there are two key considerations to keep in mind:

1. **Sequential Upgrades:** Temporal Server should be upgraded sequentially.
   That is, if you're on version \(v1.n.x\), your next upgrade should be to \(v1.n+1.x\) or the closest available subsequent version.
   This sequence should be repeated until your desired version is reached.

2. **Data Compatibility:** During an upgrade, the Temporal Server either updates or restructures the existing version data to match the data format of the newer version.
   Temporal Server ensures backward compatibility only between two successive minor versions.
   Consequently, skipping versions during an upgrade may lead to older data formats becoming unreadable.
   If the previous data format cannot be interpreted and converted to the newer format, the upgrade process will be unsuccessful.

### Step-by-Step Upgrade Procedure:

Upgrading the Temporal Server requires a methodical approach to ensure data integrity, compatibility, and seamless transition between versions.
The following documentation outlines the step-by-step process to successfully upgrade your Temporal Server.

When upgrading your Temporal Server version, ensure that you upgrade sequentially.

1. **Upgrade Database Schema:** Before initiating the Temporal Server upgrade, use one of the recommended upgrade tools to update your database schema.
   This ensures it is aligned with the version of Temporal Server you aim to upgrade to.
2. **Upgrade Temporal Server:** Once the database schema is updated, proceed to upgrade the Temporal Server deployment to the next sequential version.
3. **Iterative Upgrades** (optional): Continue this process (steps 1 and 2) iteratively until you reach the desired Temporal Server version.

By adhering to the above guidelines and following the step-by-step procedure, you can ensure a smooth and successful upgrade of your Temporal Server.

The Temporal Server upgrade updates or rewrites the old version data with the format introduced in the newer version.
Because Temporal Server guarantees backward compatibility between two consecutive minor versions, and because older versions of the code are eventually removed from the code base, skipping versions when upgrading might cause older formats to become unrecognizable.
If the old format of the data can't be read to be rewritten to the new format, the upgrades fail.

Check the [Temporal Server releases](https://github.com/temporalio/temporal/releases) and follow these releases in order.
You can skip patch versions; use the latest patch of a minor version when upgrading.

Also, be aware that each upgrade requires the History Service to load all Shards and update the Shard metadata, so allow approximately 10 minutes on each version for these processes to complete before upgrading to the next version.

Use one of the upgrade tools to upgrade your database schema to be compatible with the Temporal Server version being upgraded to.

If you are using a schema tools version prior to Temporal Server v1.8.0, we strongly recommend _never_ using the "dryrun" (`-y`, or `--dryrun`) options in any of your schema update commands.
Using this option might lead to potential loss of data, as when using it will create a new database and drop your
existing one.
This flag was removed in the 1.8.0 release.

### Upgrade Cassandra schema

If you are using Cassandra for your Temporal Service's persistence, use the `temporal-cassandra-tool` to upgrade both the default Persistence and Visibility schemas.

**Example default schema upgrade:**

**Example visibility schema upgrade:**

### Upgrade PostgreSQL or MySQL schema

If you are using MySQL or PostgreSQL use the `temporal-sql-tool`, which works similarly to the `temporal-cassandra-tool`.

Refer to this [Makefile](https://github.com/temporalio/temporal/blob/v1.4.1/Makefile#L367-L383) for context.

**Example default schema upgrade:**

**Example visibility schema upgrade:**

If you're upgrading PostgreSQL to v12 or later to enable advanced Visibility features with Temporal Server v1.20, upgrade your PostgreSQL version first, and then run `temporal-sql-tool` with the `postgres12` plugin, as shown in the following example:

**Example default schema upgrade:**

**Example visibility schema upgrade:**

If you're upgrading MySQL to v8.0.17 or later to enable advanced Visibility features with Temporal Server v1.20, upgrade your MySQL version first, and then run `temporal-sql-tool` with the `mysql8` plugin, as shown in the following example:

### Roll-out technique

We recommend preparing a staging Temporal Service and then do the following to verify the upgrade is successful:

1. Create some simulation load on the staging Temporal Service.
2. Upgrade the database schema in the staging Temporal Service.
3. Wait and observe for a few minutes to verify that there is no unstable behavior from both the server and the simulation load logic.
4. Upgrade the server.
5. Now do the same to the live environment Temporal Service.

## Self-hosted Visibility feature setup

A [Visibility](/temporal-service/visibility) store is set up as a part of your [Persistence store](/temporal-service/persistence) to enable listing and filtering details about Workflow Executions that exist on your Temporal Service.

A Visibility store is required in a Temporal Service setup because it is used by Temporal Web UI and CLI to pull Workflow Execution data and enables features like batch operations on a group of Workflow Executions.

With the Visibility store, you can use [List Filters](/list-filter) with [Search Attributes](/search-attribute) to list and filter Workflow Executions that you want to review.

Setting up [advanced Visibility](/visibility#advanced-visibility) enables access to creating and using multiple custom Search Attributes with your List Filters.

For details, see [Search Attributes](/search-attribute).

Note that if you use MySQL, PostgreSQL, or SQLite as your Visibility store, Temporal Server version 1.20 and later supports advanced Visibility features on MySQL (version 8.0.17 and later), PostgreSQL (version 12 and later) and SQLite (v3.31.0 and later), in addition to Elasticsearch.

To enable advanced Visibility on your SQL databases, ensure that you do the following:

- [Upgrade your Temporal Server](/self-hosted-guide/upgrade-server#upgrade-server) to version 1.20 or later.
- [Update your database schemas](/self-hosted-guide/upgrade-server#upgrade-server) for MySQL to version 8.0.17 (or later), PostgreSQL to version 12 (or later), or SQLite to v3.31.0 (or later).

Beginning with Temporal Server v1.21, you can set up a secondary Visibility store in your Temporal Service to enable [Dual Visibility](/dual-visibility).
This is useful for migrating your Visibility store database.

#### Supported databases

The following databases are supported as Visibility stores:

- [MySQL](#mysql) v5.7 and later.
  Use v8.0.17 (or later) with Temporal Server v1.20 or later for advanced Visibility capabilities.
  Because standard Visibility is deprecated beginning with Temporal Server v1.21, support for older versions of MySQL will be dropped.
- [PostgreSQL](#postgresql) v9.6 and later.
  Use v12 (or later) with Temporal Server v1.20 or later for advanced Visibility capabilities.
  Because standard Visibility is deprecated beginning with Temporal Server v1.21, support for older versions of PostgreSQL will be dropped.
- [SQLite](#sqlite) v3.31.0 and later for advanced Visibility capabilities.
- [Cassandra](#cassandra).
  Support for Cassandra as a Visibility database is deprecated beginning with Temporal Server v1.21.
  For information on migrating from Cassandra to any of the supported databases, see [Migrating Visibility database](#migrating-visibility-database).
- [Elasticsearch](#elasticsearch) supported versions.
  We recommend operating a Temporal Service with Elasticsearch as your Visibility store for any use case that spawns more than a few Workflow Executions.

You can use any combination of the supported databases for your Persistence and Visibility stores.
For updates, check [Server release notes](https://github.com/temporalio/temporal/releases).

## How to set up MySQL Visibility store {#mysql}

:::tip Support, stability, and dependency info

- MySQL v5.7 and later.
- Support for MySQL v5.7 will be deprecated for all Temporal Server versions after v1.20.
- With Temporal Server version 1.20 and later, advanced Visibility is available on MySQL v8.0.17 and later.

You can set MySQL as your [Visibility store](/temporal-service/visibility).
Verify [supported versions](/self-hosted-guide/visibility) before you proceed.

If using MySQL v8.0.17 or later as your Visibility store with Temporal Server v1.20 and later, any [custom Search Attributes](/search-attribute#custom-search-attribute) that you create must be associated with a Namespace in that Temporal Service.

**Persistence configuration**

Set your MySQL Visibility store name in the `visibilityStore` parameter in your Persistence configuration, and then define the Visibility store configuration under `datastores`.

The following example shows how to set a Visibility store `mysql-visibility` and define the datastore configuration in your Temporal Service configuration YAML.

For details on the configuration parameters and values, see [Temporal Service configuration](/references/configuration#sql).

To enable advanced Visibility features on your MySQL Visibility store, upgrade to MySQL v8.0.17 or later with Temporal Server v1.20 or later.
See [Upgrade Server](/self-hosted-guide/upgrade-server#upgrade-server) on how to upgrade your Temporal Server and database schemas.

For example configuration templates, see [MySQL Visibility store configuration](https://github.com/temporalio/temporal/blob/main/config/development-mysql8.yaml).

**Database schema and setup**

Visibility data is stored in a database table called `executions_visibility` that must be set up according to the schemas defined (by supported versions):

- [MySQL v8.0.17 and later](https://github.com/temporalio/temporal/tree/main/schema/mysql/v8/visibility)

The following example shows how the [auto-setup.sh](https://github.com/temporalio/docker-builds/blob/main/docker/auto-setup.sh) script sets up your Visibility store.

**Examples:**

Example 1 (unknown):
```unknown
---

## Server Frontend API Reference

While it's usually easiest to interact with [Temporal Server](/temporal-service/temporal-server) via a [Client SDK](/encyclopedia/temporal-sdks#temporal-client) or the [Temporal CLI](https://docs.temporal.io/cli), you can also use its gRPC API.

## gRPC API

Our Client and Worker SDKs use the gRPC API. The API reference is located here:

[`api-docs.temporal.io`](https://api-docs.temporal.io/)

### Use with code

Usually you interact with the API via high-level methods like `client.workflow.start()`. However, Client SDKs also expose the underlying gRPC services. For instance, the TypeScript SDK has:

- WorkflowService: [`Client.connection.workflowService`](https://typescript.temporal.io/api/classes/client.Connection#workflowservice)
- OperatorService: [`Client.connection.operatorService`](https://typescript.temporal.io/api/classes/client.Connection/#operatorservice)
- HealthService: [`Client.connection.healthService`](https://typescript.temporal.io/api/classes/client.Connection/#healthservice)

If you're not using an SDK Client (rare), you can generate gRPC client stubs by:

- Cloning [`temporalio/api`](https://github.com/temporalio/api) (repo with the protobuf files)
- Generating code in [your language](https://grpc.io/docs/languages/)

### Use manually

To query the API manually via command line or a GUI, first:

- If you don't already have a Server to connect to, run [`temporal server start-dev`](/cli/server#start-dev)
- Clone this repo:
```

Example 2 (unknown):
```unknown
#### With command line

Install [`evans`](https://github.com/ktr0731/evans#installation).
```

Example 3 (unknown):
```unknown
To connect to Temporal Cloud, set the host, cert, cert key, and TLS flag:
```

Example 4 (unknown):
```unknown
Once inside the evans prompt, you can run commands like `help`, `show service` to list available methods, and `call ListWorkflowExecutions`.

#### With a GUI

- Install [BloomRPC](https://github.com/bloomrpc/bloomrpc#installation).
- Open the app
- Select "Import Paths" button on the top-left and enter the path to the cloned repo: `/path/to/api`
- Select the "Import protos" + button and select this file:
```

---
