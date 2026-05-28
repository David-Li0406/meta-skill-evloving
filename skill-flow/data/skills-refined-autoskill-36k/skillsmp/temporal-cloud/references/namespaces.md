# Temporal-Cloud - Namespaces

**Pages:** 8

---

## Temporal Service level Archival config

**URL:** llms-txt#temporal-service-level-archival-config

archival:
  # Event History configuration
  history:
    # Archival is enabled at the Temporal Service level
    state: 'enabled'
    enableRead: true
    # Namespaces can use either the local filestore provider or the Google Cloud provider
    provider:
      filestore:
        fileMode: '0666'
        dirMode: '0766'
      gstorage:
        credentialsPath: '/tmp/gcloud/keyfile.json'

---

## Combined filtering

**URL:** llms-txt#combined-filtering

**Contents:**
  - Label Management

/v1/metrics?namespaces=prod-*&metrics=temporal_cloud_v1_approximate_backlog_count
yaml
scrape_configs:
- job_name: 'temporal-cloud'
  ...
  static_configs:
    - targets: ['metrics.temporal.io']
  metrics_path: '/v1/metrics'
  params:
    namespaces: ['prod-*']
    metrics: ['temporal_cloud_v1_approximate_backlog_count']

yaml
metric_relabel_configs:

**Examples:**

Example 1 (unknown):
```unknown
:::info

In Prometheus, the `params` config can be set to match the same behavior as above.
```

Example 2 (unknown):
```unknown
:::

### Label Management

#### Prometheus

If using Prometheus, you can configure it to drop metrics with a specific label or even rename specific label values to reduce the cardinality.
```

---

## Create a client to localhost on default namespace

**URL:** llms-txt#create-a-client-to-localhost-on-default-namespace

client = Temporalio::Client.connect('localhost:7233', 'default')

---

## Default values for a Namespace if none are provided at creation.

**URL:** llms-txt#default-values-for-a-namespace-if-none-are-provided-at-creation.

**Contents:**
- dcRedirectionPolicy
- dynamicConfigClient
- Temporal Cluster dynamic configuration reference
- Format
  - Constraints
- Commonly used dynamic configuration keys
  - Service-level RPS limits
  - QPS limits for Persistence store
  - Activity and Workflow default policy setting
  - Size limit settings

namespaceDefaults:
  # Archival defaults.
  archival:
    # Event History defaults.
    history:
      state: 'enabled'
      # New Namespaces will default to the local provider.
      URI: 'file:///tmp/temporal_archival/development'
    visibility:
      state: 'disabled'
      URI: 'file:///tmp/temporal_vis_archival/development'
yaml
#...
dcRedirectionPolicy:
  policy: 'selected-apis-forwarding'
#...
yaml
dynamicConfigClient:
  filepath: 'config/dynamicconfig/development-cass.yaml'
  pollInterval: '10s'
yaml
testGetBoolPropertyKey:
  - value: false
  - value: true
    constraints:
      namespace: 'your-namespace'
  - value: false
    constraints:
      namespace: 'your-other-namespace'
testGetDurationPropertyKey:
  - value: '1m'
    constraints:
      namespace: 'your-namespace'
      taskQueueName: 'longIdleTimeTaskqueue'
testGetFloat64PropertyKey:
  - value: 12.0
    constraints:
      namespace: 'your-namespace'
testGetMapPropertyKey:
  - value:
      key1: 1
      key2: 'value 2'
      key3:
        - false
        - key4: true
          key5: 2.0
yaml
  frontend.globalNamespaceRPS: # Total per-Namespace RPC rate limit applied across the Cluster.
    - value: 5000
  yaml
  frontend.persistenceNamespaceMaxQPS: # Rate limit on the number of queries the Frontend sends to the Persistence store.
    - constraints: {} # Sets default value that applies to all Namespaces
      value: 2000 # The default value for this key is 0.
    - constraints: { namespace: 'namespace1' } # Sets limit on number of queries that can be sent from "namespace1" Namespace to the Persistence store.
      value: 4000
    - constraints: { namespace: 'namespace2' }
      value: 1000
  yaml
  matching.numTaskqueueReadPartitions: # Number of Task Queue partitions for read operations.
    - constraints: { namespace: 'namespace1', taskQueueName: 'tq' } # Applies to the "tq" Task Queue for both Workflows and Activities.
      value: 8 # The default value for this key is 4. Task Queues that need to support high traffic require higher number of partitions. Set these values in accordance to your poller count.
    - constraints: {
          namespace: 'namespace1',
          taskQueueName: 'other-tq',
          taskType: 'Activity',
        } # Applies to the "other_tq" Task Queue for Activities specifically.
      value: 20
    - constraints: { namespace: 'namespace2' } # Applies to all task queues in "namespace2".
      value: 10
    - constraints: {} # Applies to all other task queues in "namespace1" and all other Namespaces.
      value: 16
  matching.numTaskqueueWritePartitions: # Number of Task Queue partitions for write operations.
    - constraints: { namespace: 'namespace1', taskQueueName: 'tq' } # Applies to the "tq" Task Queue for both Workflows and Activities.
      value: 8 # The default value for this key is 4. Task Queues that need to support high traffic require higher number of partitions. Set these values in accordance to your poller count.
    - constraints: {
          namespace: 'namespace1',
          taskQueueName: 'other-tq',
          taskType: 'Activity',
        } # Applies to the "other_tq" Task Queue for Activities specifically.
      value: 20
    - constraints: { namespace: 'namespace2' } # Applies to all task queues in "namespace2".
      value: 10
    - constraints: {} # Applies to all other task queues in "namespace1" and all other Namespaces.
      value: 16
  
temporal workflow describe -w my-workflow-id
...
Pending Nexus Operations: 1

Endpoint                 myendpoint
  Service                  my-hello-service
  Operation                echo
  OperationToken
  State                    BackingOff
  Attempt                  6
  ScheduleToCloseTimeout   0s
  NextAttemptScheduleTime  20 seconds from now
  LastAttemptCompleteTime  11 seconds ago
  LastAttemptFailure       {"message":"unexpected response status: "500 Internal Server Error": internal error","applicationFailureInfo":{}}
go
s, err := temporal.NewServer()
if err != nil {
	log.Fatal(err)
}
err = s.Start()
if err != nil{
	log.Fatal(err)
}
go
s, err := temporal.NewServer(
	temporal.WithConfig(cfg),
)
go
s, err := temporal.NewServer(
	temporal.WithConfigLoader(configDir, env, zone),
)
go
s, err := temporal.NewServer(
	temporal.ForServices(temporal.Services),
)
go
s, err := temporal.NewServer(
	temporal.InterruptOn(temporal.InterruptCh()),
)
go
s, err := temporal.NewServer(
	temporal.WithAuthorizer(myAuthorizer),
)
go
s, err := temporal.NewServer(
	temporal.WithTLSConfigFactory(yourTLSConfigProvider),
)
go
s, err := temporal.NewServer(
  temporal.WithClaimMapper(func(cfg *config.Config) authorization.ClaimMapper {
  		logger := getYourLogger() // Replace with how you retrieve or initialize your logger
		return authorization.NewDefaultJWTClaimMapper(
			authorization.NewDefaultTokenKeyProvider(cfg, logger),
			cfg
		)
	}),
)
go
s, err := temporal.NewServer(
	temporal.WithCustomMetricsReporter(myReporter),
)
bash
tctl activity complete --workflow_id <id>
bash
tctl activity complete --run_id <id>
bash
tctl activity complete --activity_id <id>
bash
tctl activity complete --result <value>
bash
tctl activity complete --identity <value>
bash
tctl activity fail --workflow_id <id>
bash
tctl activity fail --run_id <id>
bash
tctl activity fail --activity_id <id>
bash
tctl activity fail --reason <value>
bash
tctl activity fail --detail <value>
bash
tctl activity complete --identity <value>
bash
tctl admin cluster add-search-attributes --name <SearchAttributeName> --type <SearchAttributeValueType>
bash
tctl admin cluster remove-search-attributes --name <SearchAttributeKey>
bash
tctl batch start --query <value>
bash
tctl batch start --query <value> --reason <string>
bash
tctl batch start --query <value> --batch_type <operation>
bash
tctl batch start --query <value> --batch_type signal --signal_name <name>
bash
tctl batch start --query <value> --input <json>
bash
tctl batch start --query <value> --rps <value>
bash
tctl batch start --query <value> --yes
bash
tctl batch list --pagesize <value>
bash
tctl batch describe --job_id <id>
bash
tctl batch terminate --job_id <id>
bash
tctl batch terminate --job_id <id> --reason <string>
bash
tctl cluster get-search-attributes
text
+-----------------------+----------+
|         NAME          |   TYPE   |
+-----------------------+----------+
| BinaryChecksums       | Keyword  |
| CloseTime             | Int      |
| CustomBoolField       | Bool     |
| CustomDatetimeField   | Datetime |
| CustomDoubleField     | Double   |
| CustomIntField        | Int      |
| CustomKeywordField    | Keyword  |
| CustomNamespace       | Keyword  |
| CustomStringField     | String   |
| ExecutionStatus       | Int      |
| ExecutionTime         | Int      |
| Operator              | Keyword  |
| RunId                 | Keyword  |
| StartTime             | Int      |
| TaskQueue             | Keyword  |
| TemporalChangeVersion | Keyword  |
| WorkflowId            | Keyword  |
| WorkflowType          | Keyword  |
+-----------------------+----------+
bash
tctl dataconverter web --web_ui_url <url> --port <value>
bash
tctl dataconverter web --web_ui_url <url>
bash
tctl namespace describe --namespace_id <id>
bash
$ tctl --ns canary-namespace n desc
Name: canary-namespace
Description: testing namespace
OwnerEmail: dev@yourtech.io
NamespaceData:
Status: REGISTERED
RetentionInDays: 7
EmitMetrics: true
ActiveClusterName: dc1
Clusters: dc1, dc2
bash
tctl --namespace your-namespace namespace register

**Examples:**

Example 1 (unknown):
```unknown
## dcRedirectionPolicy

_Optional_

Contains the Frontend datacenter API redirection policy that you can use for cross-DC replication.

Supported values:

- `policy`: Supported values are `noop`, `selected-apis-forwarding`, and `all-apis-forwarding`.
  - `noop`: Not setting a value or setting `noop` means no redirection. This is the default value.
  - `selected-apis-forwarding`: Sets up forwarding for the following APIs to the active Cluster based on the Namespace.
    - `StartWorkflowExecution`
    - `SignalWithStartWorkflowExecution`
    - `SignalWorkflowExecution`
    - `RequestCancelWorkflowExecution`
    - `TerminateWorkflowExecution`
    - `QueryWorkflow`
  - `all-apis-forwarding`: Sets up forwarding for all APIs on the Namespace in the active Cluster.

Example:
```

Example 2 (unknown):
```unknown
## dynamicConfigClient

_Optional_

Configuration for setting up file-based [dynamic configuration](/temporal-service/configuration#dynamic-configuration) client for the Cluster.

This setting is required if specifying dynamic configuration. Supported configuration values are as follows:

- `filepath`: Specifies the path where the dynamic configuration YAML file is stored. The path should be relative to the root directory.
- `pollInterval`: Interval between the file-based client polls to check for dynamic configuration updates. The minimum period you can set is 5 seconds.

Example:
```

Example 3 (unknown):
```unknown
---

## Temporal Cluster dynamic configuration reference

Temporal Cluster provides [dynamic configuration](/temporal-service/configuration#dynamic-configuration) keys that you can update and apply to a running Cluster without restarting your services.

The dynamic configuration keys are set with default values when you create your Cluster configuration.
You can override these values as you test your Cluster setup for optimal performance according to your workload requirements.

For the complete list of dynamic configuration keys, see [https://github.com/temporalio/temporal/blob/main/common/dynamicconfig/constants.go](https://github.com/temporalio/temporal/blob/main/common/dynamicconfig/constants.go).
Ensure that you check server release notes for any changes to these keys and values.

For the default values of dynamic configuration keys, check the following links:

- [Frontend Service](https://github.com/temporalio/temporal/blob/5783e781504d8ffac59f9848b830868f3139b980/service/frontend/service.go#L176)
- [History Service](https://github.com/temporalio/temporal/blob/5783e781504d8ffac59f9848b830868f3139b980/service/history/configs/config.go#L309)
- [Matching Service](https://github.com/temporalio/temporal/blob/5783e781504d8ffac59f9848b830868f3139b980/service/matching/config.go#L125)
- [Worker Service](https://github.com/temporalio/temporal/blob/5783e781504d8ffac59f9848b830868f3139b980/service/worker/service.go#L193)

Setting dynamic configuration is optional.
Change these values only if you need to override the default values to achieve better performance on your Temporal Cluster.
Also, ensure that you test your changes before setting these in production.

## Format

To override the default dynamic configuration values, specify your custom values and constraints for the dynamic configuration keys that you want to change in a YAML configuration file.
Use the following format when creating your dynamic configuration file.
```

Example 4 (unknown):
```unknown
### Constraints

You can define constraints on some dynamic configuration keys to set specific values that apply on a Namespace or Task Queue level.
Not defining constraints on a dynamic configuration key sets the values across the Cluster.

- To set global values for the configuration key with no constraints, use the following:
```

---

## HELP temporal_cloud_v1_frontend_service_request_count The number of RPC requests received by the service..

**URL:** llms-txt#help-temporal_cloud_v1_frontend_service_request_count-the-number-of-rpc-requests-received-by-the-service..

**Contents:**
  - Configuring Grafana \+ Prometheus
  - Configuring Datadog
  - Metric Mapping Reference
  - Managing High-Cardinality

yaml
scrape_configs:
  - job_name: temporal-cloud
    static_configs:
      - targets:
        - 'metrics.temporal.io'
    scheme: https
    metrics_path: '/v1/metrics'
    honor_timestamps: true
    scrape_interval: 60s
    scrape_timeout: 30s
    authorization:
      type: Bearer
      credentials: 'API_KEY'

https://metrics.temporal.io/v1/metrics?namespaces=production-*

https://metrics.temporal.io/v1/metrics?metrics=temporal_cloud_v1_workflow_success_count?namespaces=production-*
yaml
metric_relabel_configs:
- source_labels: [__name__]
  regex: 'temporal_cloud_v1_poll_success_count'
  action: labeldrop
  regex: 'temporal_task_queue'
yaml
metric_relabel_configs:
- source_labels: [temporal_task_queue]
  regex: '(critical-queue|payment-queue)'
  target_label: __tmp_keep_original
  replacement: 'true'

**Examples:**

Example 1 (unknown):
```unknown
Now you are ready to scrape your metrics\!

### Configuring Grafana \+ Prometheus

#### Update Prometheus Configuration

Add a new scrape job for the OpenMetrics endpoint with your API key.
```

Example 2 (unknown):
```unknown
:::note

This replaces the direct Grafana datasource configuration you used with the query endpoint.

:::

#### Install New Dashboards

* Download the new Grafana dashboard: [temporal\_cloud\_openmetrics.json](https://github.com/temporalio/dashboards/blob/master/cloud/temporal_cloud_openmetrics.json)  
* Import alongside existing dashboards during transition  
* Update any custom alerts and queries to use new metrics and remove `rate()` functions

### Configuring Datadog

:::tip

Automated integration update coming soon.

:::

The Datadog team is working on updating the official Temporal Cloud integration to use the new endpoint. This transition should be largely transparent for most users.

For users that want to get started immediately, Temporal Cloud metrics can be directly integrated into Datadog by configuring the Datadog agent to scrape the OpenMetrics endpoint.  An example for that lives [here](https://github.com/temporal-community/cloud-metrics-scrape-examples/tree/main/datadog/openmetrics).

#### Other Observability Providers

Consult the documentation for your observability system for how to configure it to scrape this endpoint and retrieve your metrics:

* [NewRelic](https://docs.newrelic.com/docs/infrastructure/prometheus-integrations/install-configure-openmetrics/configure-prometheus-openmetrics-integrations/)  
* [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/configuration/#receivers)

Examples for all these integrations live [here](https://github.com/temporal-community/cloud-metrics-scrape-examples).

### Metric Mapping Reference

Below is a template for mapping metrics from the old query endpoint to the new OpenMetrics endpoint. Note that all metrics follow the pattern of `v0` → `v1` version change, and the fundamental difference is the shift from cumulative counters to pre-computed rates for the majority of the metrics. Note that the labels below are only new labels added to the metrics. For the complete list of labels, see the /production-deployment/cloud/metrics/openmetrics/metrics-reference.

#### Frontend Service Metrics

| Old Metric (v0) | New Metric (v1) | New Labels |
| ----- | ----- | ----- |
| `temporal_cloud_v0_frontend_service_error_count` | `temporal_cloud_v1_frontend_service_error_count` | `region` |
| `temporal_cloud_v0_frontend_service_request_count` | `temporal_cloud_v0_frontend_service_request_count` | `region` |
| `temporal_cloud_v0_resource_exhausted_error_count` | `temporal_cloud_v1_resource_exhausted_error_count` | `region` |
| `temporal_cloud_v0_state_transition_count` | `temporal_cloud_v1_state_transition_count` | `region` |
| `temporal_cloud_v0_total_action_count` | `temporal_cloud_v1_total_action_count` | `region` |

#### Workflow Metrics

| Old Metric (v0) | New Metric (v1) | New Labels |
| ----- | ----- | ----- |
| `temporal_cloud_v0_workflow_cancel_count` | `temporal_cloud_v1_workflow_cancel_count` | `region` `temporal_workflow_type` `temporal_task_queue` |
| `temporal_cloud_v0_workflow_continued_as_new_count` | `temporal_cloud_v1_workflow_continued_as_new_count` | `region` `temporal_workflow_type` `temporal_task_queue` |
| `temporal_cloud_v0_workflow_failed_count` | `temporal_cloud_v1_workflow_failed_count` | `region` `temporal_workflow_type` `temporal_task_queue` |
| `temporal_cloud_v0_workflow_success_count` | `temporal_cloud_v1_workflow_success_count` | `region` `temporal_workflow_type` `temporal_task_queue` |
| `temporal_cloud_v0_workflow_terminate_count` | `temporal_cloud_v1_workflow_terminate_count` | `region` `temporal_workflow_type` `temporal_task_queue` |
| `temporal_cloud_v0_workflow_timeout_count` | `temporal_cloud_v1_workflow_timeout_count` | `region` `temporal_workflow_type` `temporal_task_queue` |

#### Poll Metrics

| Old Metric (v0) | New Metric (v1) | New Labels |
| ----- | ----- | ----- |
| `temporal_cloud_v0_poll_success_count` | `temporal_cloud_v1_poll_success_count` | `region` `temporal_task_queue` |
| `temporal_cloud_v0_poll_success_sync_count` | `temporal_cloud_v1_poll_success_sync_count` | `region` `temporal_task_queue` |
| `temporal_cloud_v0_poll_timeout_count` | `temporal_cloud_v1_poll_timeout_count` | `region` `temporal_task_queue` |

#### Latency Metrics

| Old Metric (v0) | New Metric (v1) | New Labels |
| ----- | ----- | ----- |
| `temporal_cloud_v0_service_latency_buckettemporal_cloud_v0_service_latency_counttemporal_cloud_v0_service_latency_sum` | `temporal_cloud_v1_service_latency_p99temporal_cloud_v1_service_latency_p95temporal_cloud_v1_service_latency_p50` | `region` |
| `temporal_cloud_v0_replication_lag_buckettemporal_cloud_v0_replication_lag_counttemporal_cloud_v0_replication_lag_sum` | `temporal_cloud_v1_replication_lag_p99temporal_cloud_v1_replication_lag_p95temporal_cloud_v1_replication_lag_p50` | `region` |

#### Schedule Metrics

| Old Metric (v0) | New Metric (v1) | New Labels |
| ----- | ----- | ----- |
| `temporal_cloud_v0_schedule_action_success_count` | `temporal_cloud_v1_schedule_action_success_count` | `region` |
| `temporal_cloud_v0_schedule_buffer_overruns_count` | `temporal_cloud_v1_schedule_buffer_overruns_count` | `region` |
| `temporal_cloud_v0_schedule_missed_catchup_window_count` | `temporal_cloud_v1_schedule_missed_catchup_window_count` | `region` |
| `temporal_cloud_v0_schedule_rate_limited_count` | `temporal_cloud_v1_schedule_rate_limited_count` | `region` |

In addition to these metrics, there are a number of new metrics provided by our OpenMetrics endpoint. 

:::info

See the [metrics reference](/production-deployment/cloud/metrics/openmetrics/metrics-reference) for an up-to-date list of all available metrics and their full descriptions.

:::

### Managing High-Cardinality

The new endpoint provides access to high-cardinality labels that can significantly increase your metric volume:

#### High-Cardinality Labels

* `temporal_task_queue`  
* `temporal_workflow_type`

#### Best Practices

##### Namespace/Metric filtering

Namespace filtering can be used to ensure that metrics are scraped for relevant Namespaces, which reduces cardinality.
```

Example 3 (unknown):
```unknown
This can be taken further by only scraping relevant metrics for a given namespace which ensures that any new high cardinality metrics won’t be an issue for your observability system.
```

Example 4 (unknown):
```unknown
##### Relabeling

If the above doesn’t work, consider dropping problematic labels post-scrape but pre-ingestion into your observability system.  

For example, in Prometheus this can be done via [relabeling rules](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config).
```

---

## Default values for a Namespace if none are provided at creation

**URL:** llms-txt#default-values-for-a-namespace-if-none-are-provided-at-creation

**Contents:**
  - How to create a custom Archiver {#custom-archiver}
- Temporal Platform's production readiness checklist
- Self-Hosting Challenge Areas
- Scalability with Variable or Growing Workloads {#scaling-and-metrics}
- Availability
- Management and Control Plane
- Maintenance and Upgrades
- Expert Support
- Cost Management
- Self-hosted Temporal Service defaults

namespaceDefaults:
  # Archival defaults
  archival:
    # Event History defaults
    history:
      state: 'enabled'
      # New Namespaces will default to the local provider
      URI: 'file:///tmp/temporal_archival/development'
yaml
archival:
  history:
    state: 'disabled'

namespaceDefaults:
  archival:
    history:
      state: 'disabled'
bash
./temporal-server start
bash
./temporal operator namespace create --namespace="my-namespace" --global false --history-archival-state="enabled" --retention="4d"
bash
./temporal workflow show --workflow-id="my-workflow-id" --run-id="my-run-id" --namespace="my-namespace"

temporal/common/archiver
  - filestore/                      -- Filestore implementation
  - provider/
      - provider.go                 -- Provider of archiver instances
  - yourImplementation/
      - historyArchiver.go          -- HistoryArchiver implementation
      - historyArchiver_test.go     -- Unit tests for HistoryArchiver
      - visibilityArchiver.go       -- VisibilityArchiver implementations
      - visibilityArchiver_test.go  -- Unit tests for VisibilityArchiver
go
func(a * Archiver) Archive(ctx context.Context, URI string, request * ArchiveRequest, opts...ArchiveOption) error {
    featureCatalog: = GetFeatureCatalog(opts...) // this function is defined in options.go
    var progress progress
    // Check if the feature for recording progress is enabled.
    if featureCatalog.ProgressManager != nil {
        if err: = featureCatalog.ProgressManager.LoadProgress(ctx, & prevProgress);
        err != nil {
            // log some error message and return error if needed.
        }
    }

// Your archiver implementation...

// Record current progress
    if featureCatalog.ProgressManager != nil {
        if err: = featureCatalog.ProgressManager.RecordProgress(ctx, progress);
        err != nil {
            // log some error message and return error if needed.
        }
    }
}
go
func(a * Archiver) Archive(ctx context.Context, URI string, request * ArchiveRequest, opts...ArchiveOption) error {
    featureCatalog: = GetFeatureCatalog(opts...) // this function is defined in options.go

err: = youArchiverImpl()

if nonRetryableErr(err) {
        if featureCatalog.NonRetryableError != nil {
            return featureCatalog.NonRetryableError() // when the caller gets this error type back it will not retry anymore.
        }
    }
}
bash
git clone https://github.com/temporalio/docker-compose.git
cd docker-compose
docker compose up
bash
docker run
    # persistence/schema setup flags omitted
    -e SERVICES=history \                      -- Spin up one or more: history, matching, worker, frontend
    -e LOG_LEVEL=debug,info \                           -- Logging level
    -e DYNAMIC_CONFIG_FILE_PATH=config/foo.yaml         -- Dynamic config file to be watched
    temporalio/server:<tag>

global:
 scrape_interval: 10s
scrape_configs:
 - job_name: 'temporalmetrics'
   metrics_path: /metrics
   scheme: http
   static_configs:
     # Temporal Service metrics target
     - targets:
         - 'host.docker.internal:8000'
       labels:
         group: 'server-metrics'

# Local app targets (set in SDK code)
     - targets:
         - 'host.docker.internal:8077'
         - 'host.docker.internal:8078'
       labels:
         group: 'sdk-metrics'
bash
docker run -p 9090:9090 -v /path/to/prometheus.yml /etc/prometheus/prometheus.yml prom/prometheus
bash
temporal server start-dev --metrics-port 8000
bash
docker run -d -p 3000:3000 grafana/grafana-enterprise

service {
  check {
    type     = "tcp"
    port     = 7233
    interval = "10s"
    timeout  = "2s"
  }

service {
  check {
    type         = "grpc"
    port         = 7233
    interval     = "10s"
    timeout      = "2s"
  }

namespace α's version is 1
all workflows events generated within this namespace, will come with version 1

namespace β's version is 2
all workflows events generated within this namespace, will come with version 2

namespace α's version is 2
all workflows events generated within this namespace, will come with version 2

namespace β's version is 11
all workflows events generated within this namespace, will come with version 11

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 1               | 1       |
| -------- | -------------   | --------------- | ------- |

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 3               | 1       |
| 2        | 1               |                 |         |
| 3        | 1               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 3               | 1       |
| 2        | 1               | 4               | 2       |
| 3        | 1               |                 |         |
| 4        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 3               | 1       |
| 2        | 1               | 5               | 2       |
| 3        | 1               |                 |         |
| 4        | 2               |                 |         |
| 5        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               | 3               | 2       |
| 3        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               | 4               | 2       |
| 3        | 2               |                 |         |
| 4        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | --------------- | --------------- | ------- |
| Events   | Version History |                 |         |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               | 3               | 2       |
| 3        | 2               | 4               | 3       |
| 4        | 3               |                 |         |
| -------- | -------------   | --------------- | ------- |

| ------------- | ------------- |
| Events         |               |
| -------------- | ------------- |
| Event ID       | Event Version |
| -------------  | ------------- |
| 1              | 1             |
| 2              | 1             |
| 3              | 2             |
| -------------  | ------------- |
|                |               |
| -------------  | ------------- |
|                |               |
| -------------- | ------------- |  | -------- | ------------- |
| Event ID       | Event Version |  | Event ID | Event Version |
| -------------  | ------------- |  | -------- | ------------- |
| 4              | 2             |  | 4        | 3             |
| -------------- | ------------- |  | -------- | ------------- |

| --------------- | ----------- |
| Version History |              |
| --------------- | ------------ |
| Event ID        | Version      |
| --------------- | ------------ |
| 2               | 1            |
| 3               | 2            |
| --------------- | ------------ |

| --------------- | ----------- |  | --------------- | ------- |
| Event ID | Version |  | Event ID | Version |
| -------- | ------- || --------------- | ------- |
| 4   | 2   |  | 4 | 3 |
| --- | --- || --------------- | ------- |

| ------------- |          | ------------- |          | ------------- |
| Cluster A |  | Network Layer |  | Cluster B |
| --------- || ------------- |          | ------------- |
        |                          |                          |
        | Run 1 Replication Events |                          |
        | -----------------------> |                          |
        |                          |                          |
        | Run 2 Replication Events |                          |
        | -----------------------> |                          |
        |                          |                          |
        |                          |                          |
        |                          |                          |
        |                          | Run 2 Replication Events |
        |                          | -----------------------> |
        |                          |                          |
        |                          | Run 1 Replication Events |
        |                          | -----------------------> |
        |     |  |
        | --- || ------------- |          | ------------- |
| Cluster A |  | Network Layer |  | Cluster B |
| --------- || ------------- |          | ------------- |

| -------- | ------------- |
| Events   |
| -------- | ------------- |
| Event ID | Event Version |
| -------- | ------------- |
| 1        | 1             |
| 2        | 1             |
| 3        | 2             |
| -------- | ------------- |
|          |
|          |
| -------- | ------------- |
| Event ID | Event Version |
| -------- | ------------- |
| 4        | 2             | <-- task A belongs to this event |
| -------- | ------------- |

| ------------- | -------------- |
| Events        |
| ------------- | -------------- |
| Event ID      | Event Version  |
| ------------- | -------------- |
| 1             | 1              |
| 2             | 1              |
| 3             | 2              |
| ------------- | -------------- |

| --------------| -------------- |                                  |----------| ----------------- |
| Event ID | Event Version |  | Event ID | Event Version |
| -------- | ------------- || -------- | ----------------- |
| 4   | 2   | <-- task A belongs to this event | 4 | 3 | <-- current branch / mutable state |
| --- | --- || -------- | ----------------- |
yaml

**Examples:**

Example 1 (unknown):
```unknown
You can disable Archival by setting `archival.history.state` and `namespaceDefaults.archival.history.state` to `"disabled"`.

Example:
```

Example 2 (unknown):
```unknown
The following table showcases acceptable values for each configuration and what purpose they serve.

| Config                                         | Acceptable values                                                                  | Description                                                                                                                  |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `archival.history.state`                       | `enabled`, `disabled`                                                              | Must be `enabled` to use the Archival feature with any Namespace in the Temporal Service.                                    |
| `archival.history.enableRead`                  | `true`, `false`                                                                    | Must be `true` to read from the archived Event History.                                                                      |
| `archival.history.provider`                    | Sub provider configs are `filestore`, `gstorage`, `s3`, or `your_custom_provider`. | Default config specifies `filestore`.                                                                                        |
| `archival.history.provider.filestore.fileMode` | File permission string                                                             | File permissions of the archived files. We recommend using the default value of `"0666"` to avoid read/write issues.         |
| `archival.history.provider.filestore.dirMode`  | File permission string                                                             | Directory permissions of the archive directory. We recommend using the default value of `"0766"` to avoid read/write issues. |
| `namespaceDefaults.archival.history.state`     | `enabled`, `disabled`                                                              | Default state of the Archival feature whenever a new Namespace is created without specifying the Archival state.             |
| `namespaceDefaults.archival.history.URI`       | Valid URI                                                                          | Must be a URI of the file store location and match a schema that correlates to a provider.                                   |

Additional resources: [Temporal Service configuration reference](/references/configuration).

#### Namespace creation

Although Archival is configured at the Temporal Service level, it operates independently within each Namespace.
If an Archival URI is not specified when a Namespace is created, the Namespace uses the value of `defaultNamespace.archival.history.URI` from the `config/development.yaml` file.
The Archival URI cannot be changed after the Namespace is created.
Each Namespace supports only a single Archival URI, but each Namespace can use a different URI.
A Namespace can safely switch Archival between `enabled` and `disabled` states as long as Archival is enabled at the Temporal Service level.

Archival is supported in [Global Namespaces](/global-namespace) (Namespaces that span multiple clusters).
When Archival is running in a Global Namespace, it first runs on the active cluster; later it runs on the standby cluster. Before archiving, a history check is done to see what has been previously archived.

#### Test setup

To test Archival locally, start by running a Temporal server:
```

Example 3 (unknown):
```unknown
Then register a new Namespace with Archival enabled.

{/* ./tctl --ns samples-namespace namespace register --gd false --history_archival_state enabled --retention 3 */}
```

Example 4 (unknown):
```unknown
:::note

If the retention period isn't set, it defaults to 72h.
The minimum retention period is one day.
The maximum retention period is 30 days.

Setting the retention period to 0 results in the error _A valid retention period is not set on request_.

:::

Next, run a sample Workflow such as the [helloworld temporal sample](https://github.com/temporalio/temporal-go-samples/tree/master/helloworld).

When execution is finished, Archival occurs.

#### Retrieve archives

You can retrieve archived Event Histories by copying the `workflowId` and `runId` of the completed Workflow from the log output and running the following command:

{/* ./tctl --ns samples-namespace wf show --wid <workflowId> --rid <runId> */}
```

---

## Approximate 99th percentile latency broken down by operation

**URL:** llms-txt#approximate-99th-percentile-latency-broken-down-by-operation

**Contents:**
- Temporal Cloud Observability and Metrics
- OpenMetrics API Reference
- Available Metrics Reference
- Authentication
  - Creating API Keys
  - Using API Keys
- Object Model
  - Metrics
  - Metric Types
  - Labels

histogram_quantile(0.99, sum(rate(temporal_cloud_v0_service_latency_bucket[$__rate_interval])) by (le, operation))
shell
curl -H "Authorization: Bearer <API_KEY>" https://metrics.temporal.io/v1/metrics
shell
curl -H "Authorization: Bearer <API_KEY>" \
  "https://metrics.temporal.io/v1/metrics?namespaces=production-*"

**Examples:**

Example 1 (unknown):
```unknown
Metrics are scraped every 30 seconds and exposed to the metrics endpoint with a 1-minute lag.\
The endpoint returns data with a 15-second resolution, which results in displaying the same value twice.

Set up Grafana with Temporal Cloud observability to view metrics by creating or getting your Prometheus endpoint for Temporal Cloud metrics and enabling SDK metrics.

<RelatedReadContainer>
  <RelatedReadItem path="/cloud/metrics/prometheus-grafana" text="How to set up Grafana with Temporal Cloud observability" archetype="feature-guide" />
  <RelatedReadItem path="/production-deployment/cloud/worker-health" text="How to monitor Worker Health with Temporal Cloud Metrics" archetype="feature-guide" />
  <RelatedReadItem path="/production-deployment/cloud/service-health" text="How to monitor Service Health with Temporal Cloud Metrics" archetype="feature-guide" />
</RelatedReadContainer>

---

## Temporal Cloud Observability and Metrics

Temporal offers two distinct sources of metrics: [Cloud/Server Metrics](/production-deployment/cloud/metrics/reference) and [SDK Metrics](/references/sdk-metrics).
Each source provides options for levels of granularity and filtering, monitoring-tool integrations, and configuration.
Before implementing Temporal Cloud observability, decide what you need to measure for your use case. There are two primary use cases for metrics:

- To measure the health and performance of Temporal-backed applications and key business processes.
- To measure the health and performance of Temporal infrastructure and user provided infrastructure in the form of Temporal Workers and Temporal Clients.

When measuring the performance of Temporal-backed applications and key business processes, you should rely on Temporal SDK metrics as a source of truth.
This is because Temporal SDKs provide visibility from the perspective of your application, not from the perspective of the Temporal Service.

SDK metrics monitor individual workers and your code's behavior.
Cloud metrics monitor Temporal behavior.
When used together, Temporal Cloud and SDK metrics measure the health and performance of your full Temporal infrastructure, including the Temporal Cloud Service and user-supplied Temporal Workers.

Cloud Metrics for all Namespaces in your account are available from two sources:

- [OpenMetrics Endpoint](/cloud/metrics/openmetrics) - A Prometheus-compatible scrapable endpoint.
- [PromQL Endpoint](/cloud/metrics/promql) - A Prometheus query endpoint.

:::note

OpenMetrics is the recommended option for most users.

:::

---

## OpenMetrics API Reference

The Temporal Cloud OpenMetrics API provides actionable operational metrics about your Temporal Cloud deployment. This is a scrapable HTTP API that returns metrics in OpenMetrics format, suitable for ingestion by Prometheus-compatible monitoring systems.

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

Temporal Cloud OpenMetrics support is available in  [Public Preview](/evaluate/development-production-features/release-stages#public-preview).

:::

## Available Metrics Reference

Metrics descriptions are also available programmatically via the `/v1/descriptors` endpoint. You can see the Metrics Reference for a list of available metrics.

## Authentication

Temporal uses API keys for integrating with the OpenMetrics endpoint. Applications must be authorized and authenticated before they can access metrics from Temporal Cloud.

An API key is owned by a Service Account and inherits the permissions granted to the owner.

### Creating API Keys

API keys can be created using the [Temporal Cloud UI](https://cloud.temporal.io):

1. Navigate to Settings → Service Accounts  
2. Create a service account with **"Metrics Read-Only"** Account Level Role
3. Generate an API key within the service account

:::info

See the [docs](https://docs.temporal.io/cloud/api-keys#serviceaccount-api-keys) for more details on generating API keys.

:::

### Using API Keys

All API requests must be made over HTTPS. Calls made over plain HTTP will fail. API requests without authentication will also fail.
```

Example 2 (unknown):
```unknown
## Object Model

The object model for the Metrics API follows the [OpenMetrics](https://openmetrics.io/) standard.

### Metrics

A metric is a numeric attribute measured at a specific point in time, labeled with contextual metadata gathered at the point of instrumentation.

### Metric Types

All Temporal Cloud metrics are exposed as *gauges* in OpenMetrics format, but represent different measurement types:

* **Rate metrics**: Pre-computed per-second rates with delta temporality (e.g., `temporal_cloud_v1_workflow_success_count` \- workflows completed per second)  
* **Value metrics**: Current or instantaneous values (e.g., `temporal_cloud_v1_approximate_backlog_count` \- current number of tasks in queue)

The list of metrics and their labels are available via the [List Descriptors](/production-deployment/cloud/metrics/openmetrics/api-reference#list-metric-descriptors) endpoint or in the [Metrics Reference](/production-deployment/cloud/metrics/openmetrics/metrics-reference).

### Labels

A label is a key-value attribute associated with a metric data point. Labels can be used to filter or aggregate metrics.

Common labels include:

* `temporal_namespace`: The Temporal namespace  
* `temporal_account`: The Temporal account  
* `region`: The cloud region where the metric originated  
* `temporal_workflow_type`: The workflow type (where applicable)  
* `temporal_task_queue`: The task queue name (where applicable)

Each metric has its own set of applicable labels. See the Metrics Reference for complete details.

### Metric Family

A [Metric Family](https://github.com/prometheus/OpenMetrics/blob/main/specification/OpenMetrics.md#metricfamily) may have zero or more metrics.  The set of metrics returned will vary based on actual system activity.  Metrics only appear in a Metric Family if they were reported during the aggregation window.

## Client Considerations

### Rate Limiting

To protect the stability of the API and keep it available to all users, Temporal employs multiple safeguards.

When a rate limit is breached, an HTTP `429 Too Many Requests` error is returned with the following headers:

| Header | Description |
| ----- | ----- |
| `Retry-After` | The time in seconds until the rate limit window resets |

#### Rate Limit Scopes
:::note
Rate limit scopes are subject to change.

:::

| Scope | Limit |
| ----- | ----- |
| Account | 180 requests per hour |

### Response Completeness

The `X-Completeness` header indicates whether the response contains all available data:

* `complete`: The response contains all metrics requested  
* `limited`: Response truncated due to size limits (30k metric data points max). Use namespace or metric filtering to reduce the response size.
* `unknown`: Completeness cannot be determined (possibly due to regional issues or timeouts). Clients are encouraged to retry.

### Retry Logic

Implement retry logic in your client to gracefully handle transient API failures. Use exponential backoff with jitter to avoid retry storms with reasonable retry intervals to avoid reaching rate limits.

### Data Latency

Metric data points are available for query within 2 minutes of their origination. This is in line with the freshest metrics [available from any major service provider](https://docs.datadoghq.com/integrations/guide/cloud-metric-delay/). This latency should be accounted for when setting up monitoring alerts.

## Endpoints

:::info

All endpoints are served from: `metrics.temporal.io`

:::

### Get Metrics

`GET /v1/metrics`

Returns metrics in OpenMetrics format suitable for scraping by Prometheus-compatible systems.

#### Timestamp Offset

To account for metric data latency, this endpoint returns metrics from the current timestamp minus a fixed offset.  The current offset is 2 minutes rounded down to the start of the minute. To accommodate this offset, the timestamps in the response should be honored when importing the metrics. For example, in Prometheus this can be controlled using the `honor\_timestamps` flag.

#### Query Parameters

| Parameter | Type | Description |
| ----- | ----- | ----- |
| `namespaces` | string array | Filter to specific Namespaces. Supports wildcards (e.g., `production-*`) |
| `metrics` | string array | Filter to specific metrics |

#### Response Headers

| Header | Description |
| ----- | ----- |
| `X-Completeness` | Indicates the response status: `complete`, `limited`, or `unknown` |
| `Content-Type` | `application/openmetrics-text` |

:::info Example

Request:
```

Example 3 (unknown):
```unknown
Response:
```

---

## Only specific namespaces matching the wildcard pattern

**URL:** llms-txt#only-specific-namespaces-matching-the-wildcard-pattern

/v1/metrics?namespaces=production-*

---
