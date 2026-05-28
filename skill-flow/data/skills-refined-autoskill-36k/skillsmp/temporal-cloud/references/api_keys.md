# Temporal-Cloud - Api Keys

**Pages:** 3

---

## Configure a Temporal Cloud profile that authenticates with an API key

**URL:** llms-txt#configure-a-temporal-cloud-profile-that-authenticates-with-an-api-key

temporal --profile prod config set --prop address --value "<region>.<cloud_provider>.api.temporal.io:7233"
temporal --profile prod config set --prop namespace --value "<namespace_id>.<account_id>"
temporal --profile prod config set --prop api_key --value "<your-api-key>"
bash

**Examples:**

Example 1 (unknown):
```unknown
</TabItem>
  <TabItem value="api-key-advanced" label="API key + advanced options">

This example shows how to set up a more advanced Temporal Cloud profile with TLS overrides and custom gRPC metadata.
```

---

## replace <your-secret-key> with the "secretKey": output from tcld apikey create command

**URL:** llms-txt#replace-<your-secret-key>-with-the-"secretkey":-output-from-tcld-apikey-create-command

**Contents:**
- Manage Temporal Cloud Namespaces with Terraform
- Manage Temporal Cloud Nexus Endpoints with Terraform
- Manage Temporal Cloud Users with Terraform
- Manage Temporal Cloud Service Accounts with Terraform
- Manage Temporal Cloud API Keys with Terraform
- Data Sources - Regions and Namespaces
- Community Involvement
- Monitor worker health
- Minimal Observations {#minimal-observations}
- Detect Task Backlog {#detect-task-backlog}

set TEMPORAL_CLOUD_API_KEY=<your-secret-key>
yml
provider "temporalcloud" { api_key = "my-temporalcloud-api-key" }
yml
   terraform { required_providers { temporalcloud = { source = "temporalio/temporalcloud" } } }

provider "temporalcloud" {

resource "temporalcloud_namespace" "namespace" { name               = "terraform" regions            =
   ["aws-us-east-1"] accepted_client_ca = base64encode(file("ca.pem")) retention_days     = 14 }
   bash
   terraform init
   bash
   terraform apply
   bash
temporalcloud_namespace.terraform: Creation complete after 2m17s [id=<your-namespace>]
bash
tcld namespace get -n "<your-namespace>.<your-account-id>"
yml
   terraform { required_providers { temporalcloud = { source = "temporalio/temporalcloud" version = ">= 0.0.6" } } }

provider "temporalcloud" {

resource "temporalcloud_namespace" "namespace" { name               = "terraform" regions            =
   ["aws-us-east-1"] accepted_client_ca = base64encode(file("ca.pem")) retention_days     = 30 }
   command
   terraform apply
   text
temporalcloud_namespace.namespace: Modifications complete after 10s [id=terraform.a1bb2]
text
temporalcloud_namespace.my_namespace: Destruction complete after 3s
Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
yml
   resource "temporalcloud_namespace" "namespace" { }
   bash
   terraform import temporalcloud_namespace.terraform namespaceid.acctid
   yml
   terraform {
     required_providers {
       temporalcloud = {
         source = "temporalio/temporalcloud"
       }
     }
   }

provider "temporalcloud" {

resource "temporalcloud_namespace" "target_namespace" {
     name           = "terraform-target-namespace"
     regions        = ["aws-us-west-2"]
     api_key_auth   = true
     retention_days = 14
     timeouts {
       create = "10m"
       delete = "10m"
     }
   }

resource "temporalcloud_namespace" "caller_namespace" {
     name           = "terraform-caller-namespace"
     regions        = ["aws-us-east-1"]
     api_key_auth   = true
     retention_days = 14
     timeouts {
       create = "10m"
       delete = "10m"
     }
   }

resource "temporalcloud_namespace" "caller_namespace_2" {
     name           = "terraform-caller-namespace-2"
     regions        = ["gcp-us-central1"]
     api_key_auth   = true
     retention_days = 14
     timeouts {
       create = "10m"
       delete = "10m"
     }
   }

resource "temporalcloud_nexus_endpoint" "nexus_endpoint" {
     name        = "terraform-nexus-endpoint"
     description = <<-EOT
       Service Name:
         my-hello-service
       Operation Names:
         echo
         say-hello

Input / Output arguments are in the following repository:
       https://github.com/temporalio/samples-go/blob/main/nexus/service/api.go
     EOT
     worker_target = {
       namespace_id = temporalcloud_namespace.target_namespace.id
       task_queue   = "terraform-task-queue"
     }
     allowed_caller_namespaces = [
       temporalcloud_namespace.caller_namespace.id,
       temporalcloud_namespace.caller_namespace_2.id,
     ]
   }
   bash
   terraform init
   bash
   terraform apply
   bash
   temporalcloud_nexus_endpoint.nexus_endpoint: Creation complete after 2s [id=b158063be978471fa1d200569b03834d]
   bash
tcld nexus endpoint get -n "<your-nexus-endpoint-name-without-account-suffix>"
yml
   resource "temporalcloud_nexus_endpoint" "nexus_endpoint" {
     name        = "terraform-nexus-endpoint"
     description = <<-EOT
       Service Name:
         my-hello-service
       Operation Names:
         echo
         say-hello

Input / Output arguments are in the following repository:
       https://github.com/temporalio/samples-go/blob/main/nexus/service/api.go
     EOT
     worker_target = {
       namespace_id = temporalcloud_namespace.target_namespace.id
       task_queue   = "terraform-task-queue"
     }
     allowed_caller_namespaces = [
       temporalcloud_namespace.caller_namespace.id
     ]
   }
   command
   terraform apply
   text
   temporalcloud_nexus_endpoint.nexus_endpoint: Modifications complete after 1s [id=b158063be978471fa1d200569b03834d]
   text
temporalcloud_nexus_endpoint.my_nexus_endpoint: Destruction complete after 3s
Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
bash
   terraform init
   yml
   terraform { required_providers { temporalcloud = { source = "temporalio/temporalcloud" } } }

provider "temporalcloud" { }

resource "temporalcloud_nexus_endpoint" "nexus_endpoint" { }
   bash
   terraform import temporalcloud_nexus_endpoint <your-nexus-endpoint-ID>
   text
   temporalcloud_nexus_endpoint.nexus_endpoint: Refreshing state... [id=3c0c75ccfa8144b092c13ce632463761]

Import successful!
   yml
   terraform { required_providers { temporalcloud = { source = "temporalio/temporalcloud" } } }

provider "temporalcloud" {

resource "temporalcloud_namespace" "namespace" { name               = "terraform" regions            =
   ["aws-us-east-1"] accepted_client_ca = base64encode(file("ca.pem")) retention_days     = 14 }

resource "temporalcloud_user" "global_admin" { email          = <admin-email> account_access = "Admin" }

resource "temporalcloud_user" "namespace_admin" { email          = <developer-email> account_access = "Developer"
   namespace_accesses = [ { namespace_id = temporalcloud_namespace.namespace.id permission = "Write" } ] }
   command
   terraform apply
   text
temporalcloud_user.namespace_admin: Creation complete after 1s [id=12a34bc5678910d38d9e8390636e7412]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
yml
   terraform { required_providers { temporalcloud = { source = "temporalio/temporalcloud" version = ">= 0.0.6" } } }

provider "temporalcloud" {

resource "temporalcloud_namespace" "namespace" { name               = "terraform" regions            =
   ["aws-us-east-1"] accepted_client_ca = base64encode(file("ca.pem")) retention_days     = 14 }

resource "temporalcloud_user" "global_admin" { email          = <admin-email> account_access = "Admin" }
   # resource "temporalcloud_user" "namespace_admin" {
   #   email          = <developer-email>
   #   account_access = "Developer"
   #   namespace_accesses = [
   #     {
   #       namespace_id = temporalcloud_namespace.namespace.id
   #       permission = "Write"
   #     }
   #   ]
   # }
   command
   terraform apply
   text
temporalcloud_user.namespace_admin: Destruction complete after 2s
Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
yml
   resource "temporalcloud_user" "user" { }
   `
1. Run the `terraform import` command and pass in the User ID
 Your User ID is available using the Temporal Cloud CLI `tcld u l` command.

The User is now a part of the Terraform state and all changes to the User should be managed by Terraform.

## Manage Temporal Cloud Service Accounts with Terraform

The process and steps to managing a Service Account with Terraform are very similar to managing a User with Terraform
with a few small differences:

- Service Accounts use the Service Account Terraform resource not the User resource.
- Service Accounts do not have email addresses, they have names instead. This means you should specify a name for a
  Service Account instead of an email.

Everything else about managing Services Accounts with Terraform follows the same process, guidance, and limitations of
managing Users with Terraform.

## Manage Temporal Cloud API Keys with Terraform

You can manage your own, personal API Keys and Service Account API Keys with Terraform. The process and steps to
managing an API Key with Terraform are very similar to managing other resources with Terraform. You can create, delete,
update and import API Keys with Terraform. One difference between working with API Keys as a Terraform resource compared
to other Temporal Cloud resources is the need to access an API Keys secure token output from Terraform. Walk through the
process of securely accessing the API Key Token in the Create section of this guide.

:::note Limits and Best Practices

- See the API Key [documentation](https://docs.temporal.io/cloud/api-keys) for information about the limits and best
  practices for managing API Keys.
- See Terraform's documentation on working with
  [sensitive data](https://www.terraform.io/docs/language/values/variables.html#sensitive-values) for more information
  on how to manage sensitive data in Terraform.

**How do I create a Temporal Cloud API Key with Terraform?**

1. Add a Terraform API Key resources configuration to your Terraform file.

- Replace the display_name, expiry_time, and disabled values with your Temporal Cloud API Key configuration.
   - Replace the owner_type and owner_id values with your Temporal Cloud Service Account or other Identity information.

1. Create an output.tf file and add the following code to output the API Key Token.

1. Apply your configuration. When prompted, answer yes to continue:

Upon completion, you will see a success message indicating the API Key has been created.

1. Access the API Key Token securely. You'll notice that if you view the state for the API Key resource, the token value
   is not displayed.

To access the token, you can use the Terraform output command.

This will display the token value in the terminal.

:::info Security and API Keys

Remember, keep your Terraform state files secure if you're managing API Keys with Terraform. The state file contains
sensitive information, like the API Key Token, that should not be shared or exposed.

**How do I update a Temporal Cloud API Key with Terraform?**

To update an API Key with Terraform, follow the same steps used to create an API Key.

:::note Editing Fields

You can only edit an API Key's name or description field. Updating an API Key does not generate a new secure token

**How do I delete a Temporal Cloud API Key with Terraform?**

To delete an API Key with Terraform, remove the Terraform API Key resources configuration from your Terraform and
output.tf files and run the `terraform apply` command.

**How do I Import a Temporal API Key?**

You cannot import an API Key into Terraform. Once created, the API Key secret isn't stored and can't be retrieved, so
you can't access it using import.

Instead, Temporal recommends creating a new API Key using Terraform directly.

## Data Sources - Regions and Namespaces

The Terraform provider also supports 2 data sources that provide you access to the available Regions and Namespaces in
your Temporal Cloud account.

:::note Terraform Data Sources

See Terraform [documentation](https://developer.hashicorp.com/terraform/language/data-sources) to learn more about
Terraform Data Sources

For example, to retrieve a list of regions available for your account, you can use the regions data_source

## Community Involvement

Do you have feedback about the provider? Want to report a bug or request a feature? We'd love to hear from you.

- Please reach out to us in the Temporal Community
  [Slack](https://join.slack.com/t/temporalio/shared_invite/zt-2u2ey8ilu-LRxnd3PSoAk9GZ94UuzoBA) in the #terraform
  channel
- Feel free to create issues and contribute PRs in the Temporal Terraform
  [GitHub repository](https://github.com/temporalio/terraform-provider-temporalcloud/tree/main)

## Monitor worker health

This page is a guide to monitoring a Temporal Worker fleet and covers the following scenarios:

- [Configuring minimal observations](#minimal-observations)
- [How to detect a backlog of Tasks](#detect-task-backlog)
- [How to detect greedy Worker resources](#detect-greedy-workers)
- [How to detect misconfigured Workers](#detect-misconfigured-workers)
- [How to configure Sticky cache](#configure-sticky-cache)

## Minimal Observations {#minimal-observations}

These alerts should be configured and understood first to gain intelligence into your application health and behaviors.

1. Create monitors and alerts for Schedule To Start latency SDK metrics (both [Workflow Executions](/references/sdk-metrics#workflow_task_schedule_to_start_latency) and [Activity Executions](/references/sdk-metrics#activity_schedule_to_start_latency)).
   See [Detect Task backlog section](#detect-task-backlog) to explore [sample queries](#prometheus-query-samples) and appropriate responses that accompany these values.

- Alert at >200ms for your p99 value
- Plot >100ms for your p95 value

2. Create a [Grafana](/cloud/metrics/prometheus-grafana) panel called Sync Match Rate.
   See the [Sync Match Rate section](#sync-match-rate) to explore example queries and appropriate responses that accompany these values.

- Alert at \<95% for your p99 value
- Plot \<99% for your p95 value

3. Create a [Grafana](/cloud/metrics/prometheus-grafana) panel called Poll Success Rate.
   See the [Detect greedy Workers section](#detect-greedy-workers) for example queries and appropriate responses that accompany these values.

- Alert at \<90% for your p99 value
- Plot \<95% for your p95 value

The following alerts build on the above to dive deeper into specific potential causes for Worker related issues you might be experiencing.

1. Create monitors and alerts for the [temporal_worker_task_slots_available](/references/sdk-metrics#worker_task_slots_available) SDK metric.
   See the [Detect misconfigured Workers section](#detect-misconfigured-workers) for appropriate responses based on the value.

- Alert at 0 for your p99 value

2. Create monitors for the [temporal_sticky_cache_size](/references/sdk-metrics#sticky_cache_size) SDK metric.
   See the [Configure Sticky Cache section](#configure-sticky-cache) for more details on this configuration.

- Plot at \{value\} > \{WorkflowCacheSize.Value\}

3. Create monitors for the [temporal_sticky_cache_total_forced_eviction](/references/sdk-metrics#sticky_cache_total_forced_eviction) SDK metric.
   This metric is available in the Go SDK, and the Java SDK only.
   See the [Configure Sticky Cache section](#configure-sticky-cache) for more details and appropriate responses.

- Alert at >\{predetermined_high_number\}

## Detect Task Backlog {#detect-task-backlog}

### Symptoms of high Task backlog

If the Task backlog is too high, you will find that tasks are waiting to find Workers to run on. This can cause a delay in
Workflow execution. Detecting a growing Task backlog is possible by watching the Schedule To Start latency and sync match rate.

- **SDK metric**: [workflow_task_schedule_to_start_latency](/references/sdk-metrics#workflow_task_schedule_to_start_latency)
- **SDK metric**: [activity_schedule_to_start_latency](/references/sdk-metrics#activity_schedule_to_start_latency)
- **Temporal Cloud metric**: [temporal_cloud_v0_poll_success_count](/production-deployment/cloud/metrics/reference#temporal_cloud_v0_poll_success_count)
- **Temporal Cloud metric**: [temporal_cloud_v0_poll_success_sync_count](/production-deployment/cloud/metrics/reference#temporal_cloud_v0_poll_success_sync_count)

### Schedule To Start latency

The Schedule To Start metric represents how long Tasks are staying unprocessed in the Task Queues.
It is the time between when a Task is enqueued and when it is started by a Worker.
This time being long (likely) means that your Workers can't keep up — either increase the number of Workers (if the host load is already high) or increase the number of pollers per Worker.

If your Schedule To Start latency alert triggers or is high, check the [Sync Match Rate](#sync-match-rate) to decide if you need to adjust your Worker or fleet, or contact Temporal Cloud support.
If your Sync Match Rate is low, contact [Temporal Cloud support](/cloud/support#support-ticket).
If your Sync Match Rate is low, you can contact Temporal Cloud support.

The schedule_to_start_latency SDK metric for both [Workflow Executions](/references/sdk-metrics#workflow_task_schedule_to_start_latency) and [Activity Executions](/references/sdk-metrics#activity_schedule_to_start_latency) should have alerts.

#### Prometheus query samples

**Workflow Task Latency, 99th percentile**

**Workflow Task Latency, average**

**Activity Task Latency, 99th percentile**

**Activity Task Latency, average**

This latency should be very low, close to zero.
Any higher value indicates a bottleneck.

### Sync Match Rate {#sync-match-rate}

The sync match rate measures the rate of Tasks that are delivered to workers without having to be persisted (workers are up and available to pick them up) to the rate of all delivered tasks.

A sync match is when a task is immediately matched to a Worker via the Sticky Queue.

An async match is when a Task cannot be matched to the Sticky Queue for a Worker. This can happen when no Worker has cached the Workflow, or if the Task times out during processing. In this case, the Task returns to the general Task Queue.

**Calculate Sync Match Rate**

#### Prometheus query samples

**sync_match_rate query**

The Sync Match Rate should be at least >95%, but preferably >99%.

### Handling Task backlog issues {#task-backlog-handling}

Once you have detected the condition of a high Task backlog, consider the scenarios below to take action.

#### High Schedule To Start latency and high sync match rate

There are three typical causes for this:

- There are not enough workers to perform work
- Each worker is either under resourced, or is misconfigured, to handle enough work
- There is congestion caused by the environment (eg., network) hosting the worker(s) and Temporal Cloud

- Increasing either the number of available workers
- Verifying that your worker hosts are appropriately resourced
- Increasing the worker configuration value for concurrent pollers for workers/task executions (if your worker resources can accommodate the increased load)
- Doing some combination of these

#### High Schedule To Start latency and low sync match rate

Verify that you have not set a value for `ScheduleToStartTimeout` in your Activity Options. This may skew your observations.

It may be acceptable for your use case to have low sync match rate.
For example, if you have known workloads or you intentionally throttle tasks.

In this case it's also important to understand the fill and drain rates of the async tasks are during these windows:

Successful async polls

[//]: # (add `temporal_cloud_v1_approximate_backlog_count` once the v2 metrics has been GA'd)

- Verify that your Worker setup is optimized for your instance:
  - Check the system CPU usage against `task_slots` and adjust `maxConcurrentWorkflowTaskExecutionSize` and `maxConcurrentActivityExecutionSize` settings as necessary.
  - Check the system memory usage against `sticky_cache_size` and adjust sticky cache size as necessary.
  - For a detailed explanation of settings, see the [Worker Performance](/develop/worker-performance#task-queues-processing-tuning) section.
- Increase the Worker config for concurrent pollers for Workflow or Activity `task_slots`, if your Worker resources can accommodate the increased load.
  - Reference [Worker Performance > Poller Count](/develop/worker-performance#poller-count).
- Increase the number of available Workers.

Setting the [Schedule To Start Timeout](/encyclopedia/detecting-activity-failures#schedule-to-start-timeout) in your Activity Options can skew your observations.
Avoid setting a Schedule To Start Timeout when load testing for latency.

## Detect greedy Worker resources {#detect-greedy-workers}

**How to detect greedy Worker resources.**

You can have too many Workers.
If you see the Poll Success Rate showing low numbers, you might have too many resources polling Temporal Cloud.

- **Temporal Cloud metric**: [temporal_cloud_v0_poll_success_count](/production-deployment/cloud/metrics/reference#temporal_cloud_v0_poll_success_count)
- **Temporal Cloud metric**: [temporal_cloud_v0_poll_success_sync_count](/production-deployment/cloud/metrics/reference#temporal_cloud_v0_poll_success_sync_count)
- **Temporal Cloud metric**: [temporal_cloud_v0_poll_timeout_count](/production-deployment/cloud/metrics/reference#temporal_cloud_v0_poll_timeout_count)
- **SDK metric**: [temporal_workflow_task_schedule_to_start_latency](/references/sdk-metrics#workflow_task_schedule_to_start_latency)
- **SDK metric**: [temporal_activity_schedule_to_start_latency](/references/sdk-metrics#activity_schedule_to_start_latency)

**Calculate Poll Success Rate**

Poll Success Rate should be >90% in most cases of systems with a steady load.
For high volume and low latency, try to target >95%.

There may be too many Pollers for the amount of Workers.

If you see all of the following at the same time then you might have too many Workers:

- Low poll success rate
- Low Schedule To Start latency
- Low worker host resource utilization

Consider sizing down your Workers by either:

- Reducing the number of Workers polling the impacted Task Queue, OR
- Reducing the concurrent pollers per Worker, OR
- Both of the above

#### Prometheus query samples

**poll_success_rate query**

## Detect misconfigured Workers {#detect-misconfigured-workers}

**How to detect misconfigured Workers.**

Worker configuration can negatively affect Task processing efficiency.

- **SDK metric**: [temporal_worker_task_slots_available](/references/sdk-metrics#worker_task_slots_available)
- **SDK metric**: [sticky_cache_size](/references/sdk-metrics#sticky_cache_size)
- **SDK metric**: [sticky_cache_total_forced_eviction](/references/sdk-metrics#sticky_cache_total_forced_eviction)

**Execution Size Configuration**

The `maxConcurrentWorkflowTaskExecutionSize` and `maxConcurrentActivityExecutionSize` define the number of total available slots for the Worker.
If this is set too low, the Worker will not be able to keep up processing Tasks.

The `temporal_worker_task_slots_available` metric should always be >0.

#### Prometheus query samples

You are likely experiencing a Task backlog if you are seeing inadequate slot counts frequently.
The work is not getting processed as fast as it should/can.

Increase the `maxConcurrentWorkflowTaskExecutionSize` and `maxConcurrentActivityExecutionSize` values and keep an eye on your Worker resource metrics (CPU utilization, etc) to make sure you haven't created a new issue.

### Configure Sticky Execution Cache {#configure-sticky-cache}

Sticky Execution means that a Worker caches a Workflow Execution Event History and creates a dedicated Task Queue to listen on.
It significantly improves performance because the Temporal Service only sends new events to the Worker instead of entire Event Histories.

The `sticky_cache_size` should report less than or equal to your `WorkflowCacheSize` value.
Also, sticky_cache_total_forced_eviction should not be reporting high numbers (relative).

If you see a high eviction count, verify there are no other inefficiencies in your Worker configuration or resource provisioning (backlog).
If you see the cache size metric exceed the `WorkflowCacheSize`, increase this value if your Worker resources can accommodate it or provision more Workers.
Finally, take time to review [the Worker performance guide](/develop/worker-performance) and see if it addresses other potential cache issues.

#### Prometheus query samples

**Sticky Cache Size**

**Sticky Cache Evictions**

## Manage Worker Heartbeating {#manage-worker-heartbeating}

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

This feature is currently in [Public Preview](/evaluate/development-production-features/release-stages#public-preview).

Workers send a heartbeat to Temporal Server every 60 seconds by default. This heartbeat serves to provide liveness and configuration data from the Worker to the Server.
Specific data sent can be found in the [API](https://github.com/temporalio/api/blob/master/temporal/api/worker/v1/message.proto). By providing a consistent heartbeat from
Workers, the Server can obtain an accurate count of Workers, understand Worker performance, and respond to Worker heartbeats with commands. Some examples of how this is useful:

- understanding the difference between a Worker that is down and a Worker that is processing tasks for a long time
- identifying a Worker with high CPU usage from the Server point of view

Use the Temporal CLI to view information about all Workers connected to Temporal Server. Use `temporal worker describe` to see details of a specific Worker. Use `temporal worker list` to get a complete list of all connected Workers.

If you wish to disable Worker heartbeating (features above will not work with this feature disabled) or set heartbeating to be more frequent than every 60 seconds (allowed range is 1s to 60s), set the configuration relevant to your SDK.
<SdkTabs hideUnsupportedLanguages>
<SdkTabs.Python>
Use `TelemetryConfig()` to adjust heartbeat settings. See the [Python SDK documentation](https://python.temporal.io/temporalio.bridge.runtime.RuntimeOptions.html#worker_heartbeat_interval_millis) for more details.
</SdkTabs.Python>
<SdkTabs.Ruby>
Add configurations to `Runtime()` to adjust heartbeat settings. See the [Ruby SDK documentation](https://ruby.temporal.io/Temporalio/Runtime.html) for more details.
</SdkTabs.Ruby>
</SdkTabs>

## Codec Server - Temporal Platform feature guide

Temporal Server stores and persists the data handled in your Workflow Execution.
Encrypting this data ensures that any sensitive application data is secure when handled by the Temporal Server.

For example, if you have sensitive information passed in the following objects that are persisted in the Workflow Execution Event History, use encryption to secure it:

- Inputs and outputs/results in your [Workflow](/workflow-execution), [Activity](/activity-execution), and [Child Workflow](/child-workflows)
- [Signal](/sending-messages#sending-signals) inputs
- [Memo](/workflow-execution#memo)
- Headers (verify if applicable to your SDK)
- [Query](/sending-messages#sending-queries) inputs and results
- Results of [Local Activities](/local-activity) and [Side Effects](/workflow-execution/event#side-effect)
- [Application errors and failures](/references/failures).
  Failure messages and call stacks are not encoded as codec-capable Payloads by default; you must explicitly enable encoding these common attributes on failures.
  For more details, see [Failure Converter](/failure-converter).

Using encryption ensures that your sensitive data exists unencrypted only on the Client and the Worker Process that is executing the Workflows and Activities, on hosts that you control.

By default, your data is serialized to a [Payload](/dataconversion#payload) by a [Data Converter](/dataconversion).
To encrypt your Payload, configure your custom encryption logic with a [Payload Codec](/payload-codec) and set it with a [custom Data Converter](/default-custom-data-converters#custom-data-converter).

A Payload Codec does byte-to-byte conversion to transform your Payload (for example, by implementing compression and/or encryption and decryption) and is an optional step that happens between the Client and the [Payload Converter](/payload-converter):

<CaptionedImage
    src="/diagrams/remote-data-encoding.svg"
    title="Remote data encoding architecture" />

You can run your Payload Codec with a [Codec Server](/codec-server) and use the Codec Server endpoints in the Web UI and CLI to decode your encrypted Payload locally.
For details on how to set up a Codec Server, see [Codec Server setup](#codec-server-setup).

However, if you plan to set up [remote data encoding](/remote-data-encoding) for your data, ensure that you consider all security implications of running encryption remotely before implementing it.

When implementing a custom codec, it is recommended to perform your compression or encryption on the entire input Payload and store the result in the data field of a new Payload with a different encoding metadata field.
This ensures that the input Payload's metadata is preserved.
When the encoded Payload is sent to be decoded, you can verify the metadata field before applying the decryption.
If your Payload is not encoded, it is recommended to pass the unencoded data to the decode function instead of failing the conversion.

Examples for implementing encryption:

- [Go sample](https://github.com/temporalio/samples-go/tree/main/encryption)
- [Java sample](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/encryptedpayloads)
- [Python sample](https://github.com/temporalio/samples-python/tree/main/encryption)
- [TypeScript sample](https://github.com/temporalio/samples-typescript/tree/main/encryption)
- [.NET sample](https://github.com/temporalio/samples-dotnet/tree/main/src/Encryption)

## Codec Server setup {#codec-server-setup}

Use a Codec Server to programmatically decode your encoded [payloads](/dataconversion#payload).

A Codec Server is an HTTP server that uses your custom Codec logic to decode your data remotely.
The Codec Server is independent of the Temporal Service and decodes your encrypted payloads through predefined endpoints. You create, operate, and manage access to your Codec Server in your own environment.
The Temporal CLI and the Web UI in turn provide built-in hooks to call the Codec Server to decode encrypted payloads on demand.

The Codec Server is independent of the Temporal Server and decodes your encrypted payloads through endpoints.
When you configure a Codec Server endpoint in the Temporal Web UI or CLI, the Web UI and CLI use the remote endpoint to receive decoded payloads from the Codec Server.
See [API contract requirements](#api-contract-specifications).

Decoded payloads can then be displayed in the Workflow Execution Event History on the Web UI. Note that when you use a Codec Server, the decoded payloads are decoded and returned on the client side only; payloads on the Temporal Server (whether on Temporal Cloud or a self-hosted Temporal Service) remain encrypted.

Because you create, operate, and manage access to your Codec Server in your controlled environment, ensure that you consider the following:

- When you register a Codec Server endpoint with your Web UI, expect the Codec Server to receive multiple requests per Workflow Execution.
- Ensure that you secure access to your Codec Server. For details, see [Authorization](#authorization). You might need some form of [Key management infrastructure](/key-management) for sharing your encryption keys between the Workers and your Codec Server.
- You will need to enable [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) on the HTTP/HTTPS endpoints in your Codec Server to receive requests from the Temporal Web UI.
- You may introduce latency in the Web UI when sending and receiving payloads to the Codec Server.

Your Codec Server should share logic with the custom [Payload Codec](/payload-codec) used elsewhere in your application.

### API contract specifications

When you create your Codec Server to handle requests from the Web UI, the following requirements must be met.

The Web UI and CLI send a POST to a `/decode` endpoint. In your Codec Server, create a `/decode` path and pass the incoming payload to the decode method in your Payload Codec.

For examples on how to create your Codec Server, see the following Codec Server implementation samples:

- [Go](https://github.com/temporalio/samples-go/tree/main/codec-server)
- [Java](https://github.com/temporalio/sdk-java/tree/master/temporal-remote-data-encoder)
- [Python](https://github.com/temporalio/samples-python/blob/main/encryption/codec_server.py)
- [TypeScript](https://github.com/temporalio/samples-typescript/blob/main/encryption/src/codec-server.ts)
- [.NET](https://github.com/temporalio/samples-dotnet/blob/main/src/Encryption/CodecServer/Program.cs)

You can also add a [verification step](#authorization) to check whether the incoming request has the required authorization to access the decode logic in your Payload Codec.

Each request from the Web UI to your Codec Server includes the following headers:

- `Content-Type: application/json`: Ensure that your Codec Server can accommodate this [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types).

- `X-Namespace: {namespace}`: This is a custom HTTP Header. Ensure that the [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) configuration in your Codec Server includes this header.

- [Optional] `Authorization: <credentials>`: Include this in your CORS configuration when enabling authorization with your Codec Server.

For details on setting up authorization, see [Authorization](#authorization).

The general specification for the `POST` request body contains payloads.
By default, all field values in your payload are base64 encoded, regardless of whether they are encrypted by your custom codec implementation.

The following example shows a sample `POST` request body with base64 encoding.

By default, in cross-origin Fetch/XHR invocations, browsers will not send credentials.
Enable [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) requests on your Codec Server to receive HTTP/HTTPS requests from the Temporal Web UI.

At a minimum, enable the following responses from your Codec Server to allow requests coming from the Temporal Web UI:

- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`

For example, for Temporal Cloud Web UI hosted at https://cloud.temporal.io, enable the following in your Codec Server:

- `Access-Control-Allow-Origin: https://cloud.temporal.io`
- `Access-Control-Allow-Methods: POST, GET, OPTIONS`
- `Access-Control-Allow-Headers: X-Namespace, Content-Type`

For details on what a sample request/response looks like from the Temporal Web UI, see [Sample Request/Response](#sample-requestresponse).
If setting authorization, include `Authorization` in your `Access-Control-Allow-Headers`.
For details on setting up authorization, see [Authorization](#authorization).

It is important to establish how you will provide access to your Codec Server.
Because it is designed to decode potentially sensitive data with a single API call, access to a production Codec Server should be restricted.

Depending on your infrastructure and risk levels, it might be sufficient to restrict HTTP ingress to your Codec Server (such as by using a VPN like [WireGuard](https://www.wireguard.com/)).
The Temporal Web UI can communicate with a Codec Server that is only accessible on `localhost`, so this is a legitimate security pattern.
However, if your Codec Server is exposed to the internet at all, you will likely need an authentication solution.

If you are already using an organization-wide authentication provider, you should integrate it with your Codec Server. Remember, a Codec Server is just a standalone HTTP server, so you can use existing libraries for OAuth, [Auth0](https://auth0.com/), or any other protocol.
[This repository](https://github.com/pvsone/codec-cors-credentials) contains an example of using Auth0 to handle browser-based auth to a Codec Server.

To enable authorization from the Web UI (for both a self-hosted Temporal Service and Temporal Cloud), your Codec Server must be an HTTPS Server.

The Temporal Cloud UI provides an option to pass access tokens (JWT) to your Codec Server endpoints.
Use the access tokens to validate access and then return decoded payloads from the Codec Server.

You can enable this by selecting **Pass access token** in your Codec Server endpoint interface where you add your endpoint.
Enabling this option in the Temporal Cloud UI adds an authorization header to each request sent to the Codec Server endpoint that you set.

In your Codec Server implementation, verify the signature on this access token (in your authorization header) against [our JWKS endpoint](https://login.tmprl.cloud/.well-known/jwks.json).

{/* Commenting this for now. _/}
{/_ If you want to unpack the claims in your token to add additional checks on whether the user has valid access to the Namespace and payloads they are trying to access, you can implement it using Auth0 SDKs, middleware, or one of the third-party libraries at JWT.io. */}

The token provided from Temporal Cloud UI contains the email identifier of the person requesting access to the payloads.
Based on the permissions you have provided to the user in your access control systems, set conditions in your Codec Server whether to return decoded payloads or just return the original encoded payloads.

**Self-hosted Temporal Service**

On a self-hosted Temporal Service, configure [authorization in the Web UI configuration](/references/web-ui-configuration#auth) in your Temporal Service setup.

With this enabled, you can pass access tokens to your Codec Server and validate the requests from the Web UI to the Codec Server endpoints that you set.
Note that with a self-hosted Temporal Service, you must explicitly configure authorization specifications for the Web UI and CLI.

#### Sample request/response

Consider the following sample request/response when creating and hosting a Codec Server with the following specifications:

- Scheme: `https`
- Host: `dev.mydomain.com/codec`
- Path: `/decode`

You can also perform remote encoding on an `/encode` endpoint, which looks the same in reverse:

- Scheme: `https`
- Host: `dev.mydomain.com/codec`
- Path: `/encode`

### Set your Codec Server endpoints with Web UI and CLI

After you create your Codec Server and expose the requisite endpoints, set the endpoints in your Web UI and CLI.

On Temporal Cloud and self-hosted Temporal Service, you can configure a Codec Server endpoint to be used for a Namespace in the Web UI.

<CaptionedImage
    src="/img/info/set-codec-endpoint-form.png"
    title="Codec Server endpoint Namespace setting"
/>

To set a Codec Server endpoint on a Namespace, do the following.

1. In the Web UI, go to Namespaces, select the Namespace where you want to configure the Codec Server endpoint, and click **Edit**.
1. In the **Codec Server** section on the Namespace configuration page, enter your Codec Server endpoint and port number.
1. Optional: If your Codec Server is configured to [authenticate requests](#authorization) from Temporal Web UI, enable **Pass access token** to send a JWT access token with the HTTPS requests.
1. Optional: If your Codec Server is configured to [verify origins of requests](#cors), enable **Include cross-origin credentials**.

On Temporal Cloud, you must have [Namespace Admin privileges](/cloud/users#namespace-level-permissions) to add a Codec Server endpoint on the Namespace. Setting a Codec Server endpoint on a Cloud Namespace enables it for all users on the Namespace.

Setting a Codec Server endpoint on a self-hosted Temporal Service enables it for the entire Temporal Service. You can use a single Codec Server to handle different encoding and decoding routes for each namespace.

You can also override the global Codec Server setting at the browser level. This can be useful when developing, testing, or troubleshooting encoding functionality.

<CaptionedImage
    src="/img/info/data-encoder-button.png"
    title="Codec Server endpoint browser setting"
/>

To set a browser override for the Namespace-level endpoint, do the following.

1. Navigate to **Workflows** in your Namespace.
2. In the top-right corner, select **Configure Codec Server**.
3. Select whether you want to use the Namespace-level (or Temporal Service-level for self-hosted Temporal Service) or the browser-level Codec Endpoint setting as the default for your browser.
   In Temporal Cloud:
   - **Use Namespace-level settings, where available. Otherwise, use my browser setting.**
     Uses the Namespace-level Codec Server endpoint by default.
     If no endpoint is set on the Namespace, your browser setting is applied.
   - **Use my browser setting and ignore Namespace-level setting.**
     Applies your browser-level setting by default, overriding the Namespace-level Codec Server endpoint.
4. Enter your Codec Server endpoint and port number.
5. Optional: If your Codec Server is configured to [authenticate requests](#authorization) from Temporal Web UI, enable **Pass access token** to send a JWT access token with the HTTPS requests.
6. Optional: If your Codec Server is configured to [verify origins of requests](#cors), enable **Include cross-origin credentials**.

In a self-hosted Temporal Service with dedicated UI Server configuration, you can also set the codec endpoint in the UI server [configuration file](/references/web-ui-configuration#codec):

You can configure a Codec Server endpoint with the Temporal CLI using the `--codec-endpoint` flag.

For example, if you are running your Codec Server on `http://localhost:8888`, you can use `env set` to set the endpoint globally:

If your Codec Server endpoint is not set globally, provide the `--codec-endpoint` option with each command.
For example, to see the decoded output of the Workflow Execution "yourWorkflow" in the Namespace "yourNamespace", run:

For details, see the [CLI reference](/cli/).

If your Codec Server requires authentication, the Temporal CLI will also accept a `--codec-auth` parameter to supply an
authorization header:

### Working with Large Payloads

Codec Servers can be used for more than encryption and decryption of sensitive data.
Codec Server behavior is left up to implementers -- they can also call external services or perform other tasks, as long as they hook in at the encoding and decoding stages of a Workflow payload.

By default, Temporal limits payload size to 4MB.
If this limitation is problematic for your use case, you could implement a codec that persists your payloads to an object store outside of workflow histories.
An example implementation is available from [DataDog](https://github.com/DataDog/temporal-large-payload-codec).

The Data Converter works the same for a Nexus Operation as it does for other payloads sent between a Worker and Temporal Cloud.
Both the caller and handler Workers must use compatible Data Converters to pass operation inputs and results between them.

See [Nexus Payload Encryption & Data Converter](/nexus/security#payload-encryption-data-converter) for details.

## Temporal Platform production deployments

**Ready to elevate your durable application into production?**

To take your application to production, you deploy your application code, including your Workflows, Activities, and Workers, on your infrastructure using your existing build, test and deploy tools.

Then you need a production-ready Temporal Service to coordinate the execution of your Workflows and Activities.

You can use Temporal Cloud, a fully-managed platform, or you can self-host the service.

## Use Temporal Cloud

You can let us handle the operations of running the Temporal Service, and focus on your application.
Follow the [Temporal Cloud guide](/cloud) to get started.

<CaptionedImage
    src="/diagrams/basic-platform-topology-cloud.svg"
    title="Connect your application instances to Temporal Cloud"
/>

## Run a Self-hosted Temporal Service

Alternatively, you can run your own production level Temporal Service to orchestrate your durable applications.
Follow the [Self-hosted guide](/self-hosted-guide) to get started.

<CaptionedImage
    src="/diagrams/basic-platform-topology-self-hosted.svg"
    title="Connect your application instances to your self-hosted Temporal Service"
/>

## Worker deployments

Whether you're hosting with Temporal Cloud or on your own, you have control over where to run and scale your Workers.
We provide guidance on [Worker Deployments](/production-deployment/worker-deployments).

## Self-hosted Archival setup

Archival is a feature that automatically backs up [Event Histories](/workflow-execution/event#event-history) and Visibility records from Temporal Service persistence to a custom blob store.

- [How to create a custom Archiver](#custom-archiver)
- [How to set up Archival](#set-up-archival)

Workflow Execution Event Histories are backed up after the [Retention Period](/temporal-service/temporal-server#retention-period) is reached.
Visibility records are backed up immediately after a Workflow Execution reaches a Closed status.

Archival enables Workflow Execution data to persist as long as needed, while not overwhelming the Temporal Service's persistence store.

This feature is helpful for compliance and debugging.

Temporal's Archival feature is considered **experimental** and not subject to normal [versioning and support policy](/temporal-service/temporal-server#versions-and-support).

Archival is not supported when running Temporal through Docker.
It's disabled by default when installing the system manually and when deploying through [helm charts](https://github.com/temporalio/helm-charts/blob/main/charts/temporal/templates/server-configmap.yaml).
It can be enabled in the [config](https://github.com/temporalio/temporal/blob/main/config/development.yaml).

### How to set up Archival {#set-up-archival}

[Archival](/temporal-service/archival) consists of the following elements:

- **Configuration:** Archival is controlled by the [server configuration](https://github.com/temporalio/temporal/blob/main/config/development.yaml#L81) (i.e. the `config/development.yaml` file).
- **Provider:** Location where the data should be archived. Supported providers are S3, GCloud, and the local file system.
- **URI:** Specifies which provider should be used. The system uses the URI schema and path to make the determination.

Take the following steps to set up Archival:

1. [Set up the provider](#providers) of your choice.
2. [Configure Archival](#configuration).
3. [Create a Namespace](#namespace-creation) that uses a valid URI and has Archival enabled.

Temporal directly supports several providers:

- **Local file system**: The [filestore archiver](https://github.com/temporalio/temporal/tree/main/common/archiver/filestore) is used to archive data in the file system of whatever host the Temporal server is running on. In the case of [temporal helm-charts](https://github.com/temporalio/helm-charts), the archive data is stored in the `history` pod. APIs do not function with the filestore archive. This provider is used mainly for local installations and testing and should not be relied on for production environments.
- **Google Cloud**: The [gcloud archiver](https://github.com/temporalio/temporal/tree/main/common/archiver/gcloud) is used to connect and archive data with [Google Cloud](https://cloud.google.com/storage).
- **S3**: The [s3store archiver](https://github.com/temporalio/temporal/tree/main/common/archiver/s3store) is used to connect and archive data with [S3](https://aws.amazon.com/s3).
- **Custom**: If you want to use a provider that is not currently supported, you can [create your own archiver](#custom-archiver) to support it.

Make sure that you save the provider's storage location URI in a place where you can reference it later, because it is passed as a parameter when you [create a Namespace](#namespace-creation).

Archival configuration is defined in the [`config/development.yaml`](https://github.com/temporalio/temporal/blob/main/config/development.yaml#L93) file.
Let's look at an example configuration:

**Examples:**

Example 1 (unknown):
```unknown
:::tip ENVIRONMENT VARIABLES

Do not confuse environment variables, set with your shell, with temporal env options.

:::

</TabItem>
</Tabs>

Or, pass it in manually in your .tf file using the provider code block
```

Example 2 (unknown):
```unknown
## Manage Temporal Cloud Namespaces with Terraform

Terraform is a great way to automate the management of Temporal Namespaces. It doesn't matter whether you want
management to be centralized within a platform team or federated to different product teams. The provider allows you to
import, create, update, and delete Namespaces with Terraform.

You must use an Identity with Temporal Cloud Namespace management privileges. This includes the Account Owner, Global
Admin, or Developer Account Role.

**How do I create a Namespace with Terraform?**

1. Create a Terraform configuration file (`terraform.tf`) to define a Namespace.
```

Example 3 (unknown):
```unknown
In this example, you create a Temporal Cloud Namespace named `terraform`, specifying the AWS region `aws-us-east-1`,
   and specifying the path to the CA certificate.

1. Initialize the Terraform provider.

   Run the following command to initialize the Terraform provider.
```

Example 4 (unknown):
```unknown
1. Apply the Terraform configuration.

   Once initialization occurs, apply the Terraform configuration to your Temporal Cloud account.
```

---

## Base API key properties (replace the placeholders)

**URL:** llms-txt#base-api-key-properties-(replace-the-placeholders)

temporal --profile prod config set --prop address --value "<region>.<cloud_provider>.api.temporal.io:7233"
temporal --profile prod config set --prop namespace --value "<namespace_id>.<account_id>"
temporal --profile prod config set --prop api_key --value "<your-api-key>"

---
