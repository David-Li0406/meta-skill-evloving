# Temporal-Cloud - Tcld Cli

**Pages:** 5

---

## This command installs the `opentelemetry` dependencies.

**URL:** llms-txt#this-command-installs-the-`opentelemetry`-dependencies.

**Contents:**
- Log from a Workflow {#logging}

pip install temporalio[opentelemetry]
python
logging.basicConfig(level=logging.INFO)
python

**Examples:**

Example 1 (unknown):
```unknown
Then the [`temporalio.contrib.opentelemetry.TracingInterceptor`](https://python.temporal.io/temporalio.contrib.opentelemetry.TracingInterceptor.html) class can be set as an interceptor as an argument of [`Client.connect()`](https://python.temporal.io/temporalio.client.Client.html#connect).

When your Client is connected, spans are created for all Client calls, Activities, and Workflow invocations on the Worker.
Spans are created and serialized through the server to give one trace for a Workflow Execution.

## Log from a Workflow {#logging}

Logging enables you to record critical information during code execution.
Loggers create an audit trail and capture information about your Workflow's operation.
An appropriate logging level depends on your specific needs.
During development or troubleshooting, you might use debug or even trace.
In production, you might use info or warn to avoid excessive log volume.

The logger supports the following logging levels:

| Level   | Use                                                                                                       |
| ------- | --------------------------------------------------------------------------------------------------------- |
| `TRACE` | The most detailed level of logging, used for very fine-grained information.                               |
| `DEBUG` | Detailed information, typically useful for debugging purposes.                                            |
| `INFO`  | General information about the application's operation.                                                    |
| `WARN`  | Indicates potentially harmful situations or minor issues that don't prevent the application from working. |
| `ERROR` | Indicates error conditions that might still allow the application to continue running.                    |

The Temporal SDK core normally uses `WARN` as its default logging level.

**How to log from a Workflow**

Send logs and errors to a logging service, so that when things go wrong, you can see what happened.

The SDK core uses `WARN` for its default logging level.

You can log from a Workflow using Python's standard library, by importing the logging module `logging`.

Set your logging configuration to a level you want to expose logs to.
The following example sets the logging information level to `INFO`.
```

Example 2 (unknown):
```unknown
Then in your Workflow, set your [`logger`](https://python.temporal.io/temporalio.workflow.html#logger) and level on the Workflow. The following example logs the Workflow.

  
    View the source code
  {' '}
  in the context of the rest of the application code.
```

---

## Example output: 10.1.2.3

**URL:** llms-txt#example-output:-10.1.2.3

**Contents:**
  - Updating your workers/clients
- Available GCP regions, PSC endpoints, and DNS record overrides
- Connectivity
- Private network connectivity for namespaces
  - Required steps
- Connectivity rules
  - Definition
  - Permissions and limits
- Creating a connectivity rule
  - Temporal Cloud CLI (tcld)

shell
dig payments.abcde.tmprl.cloud
go
clientOptions := client.Options{
    HostPort: "payments.abcde.tmprl.cloud:7233",
    Namespace: "payments",
    // No TLS SNI override needed
}
bash
tcld connectivity-rule create --connectivity-type private --connection-id "vpce-abcde" --region "aws-us-east-1"
bash
tcld connectivity-rule create --connectivity-type private --connection-id "1234567890" --region "gcp-us-central1" --gcp-project-id "my-project-123"
bash
tcld connectivity-rule create --connectivity-type public
bash
tcld cr create --connectivity-type private --connection-id "vpce-abcde" --region "aws-us-east-1"
bash
tcld cr create --connectivity-type public
bash
tcld namespace set-connectivity-rules --namespace "my-namespace.abc123" --connectivity-rule-ids "rule-id-1" --connectivity-rule-ids "rule-id-2"
bash
tcld n scrs -n "my-namespace.abc123" --ids "rule-id-1" --ids "rule-id-2"
bash
tcld namespace set-connectivity-rules --namespace "my-namespace.abc123 --ids rule-a --ids rule-b
bash
tcld namespace set-connectivity-rules --namespace "my-namespace.abc123" --remove-all
bash
tcld namespace get -n "my-namespace.abc123"
bash
tcld connectivity-rule list -n "my-namespace.abc123"
bash
TEMPORAL_ADDRESS=vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233
TEMPORAL_NAMESPACE=my-namespace.my-account
TEMPORAL_TLS_CERT=<path/to/cert.pem>
TEMPORAL_TLS_KEY=<path/to/cert.key>
TEMPORAL_TLS_SERVER_NAME=my-namespace.my-account.tmprl.cloud

temporal workflow count -n $TEMPORAL_NAMESPACE
bash
grpcurl \
    -servername my-namespace.my-account.tmprl.cloud \
    -cert path/to/cert.pem \
    -key path/to/cert.key \
    vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233 \
    temporal.api.workflowservice.v1.WorkflowService/GetSystemInfo
go
c, err := client.Dial(client.Options{
	HostPort:  "vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233",
	Namespace: "namespace-name.accId",
	ConnectionOptions: client.ConnectionOptions{
		TLS: &tls.Config{
			Certificates: []tls.Certificate{cert},
			ServerName:   "my-namespace.my-account.tmprl.cloud",
		},
	},
})
java
WorkflowServiceStubs service =
        WorkflowServiceStubs.newServiceStubs(
            WorkflowServiceStubsOptions.newBuilder()
                .setSslContext(sslContext)
                .setTarget("vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233")
                .setChannelInitializer(
                    c -> c.overrideAuthority("my-namespace.my-account.tmprl.cloud"))
                .build());
ts
const connection = await NativeConnection.connect({
  address: "vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233",
  tls: {
    serverNameOverride: "my-namespace.my-account.tmprl.cloud",
    //serverRootCACertificate,
    // See docs for other TLS options
    clientCertPair: {
      crt: fs.readFileSync(clientCertPath),
      key: fs.readFileSync(clientKeyPath),
    },
  },
});
python
client_config["tls"] = TLSConfig(
    client_cert=bytes(crt, "utf-8"),
    client_private_key=bytes(key, "utf-8"),
    domain="my-namespace.my-account.tmprl.cloud",
)

client = await Client.connect("vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233")
dotnet
// Create client 
var client = await TemporalClient.ConnectAsync(
  new(ctx.ParseResult.GetValueForOption(targetHostOption)!)
  {
    Namespace = ctx.ParseResult.GetValueForOption (namespaceOption)!,
    // Set TLS options with client certs. Note, more options could 
    // be added here for server CA (i.e. "ServerRootCACert") or SNI 
    // override (i.e. "Domain") for self-hosted environments with 
    // self-signed certificates. 
    Tls = new() 
    {
      ClientCert = 
        await File.ReadAllBytesAsync(ctx.ParseResult.GetValueForOption(clientCertOption) !.FullName), 
      ClientPrivateKey = 
        await File.ReadAllBytesAsync(ctx.ParseResult.GetValueFor0ption(clientKey0ption)!.FullName), Domain = "my-namespace.my-account.tmprl.cloud",
  },
});

// dotnet run --target-host "vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233"
bash
nc -zv vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com 7233
bash
   //[bucket-name]/temporal-workflow-history/export/[Namespace]/[Year]/[Month]/[Day]/[Hour]/[Minute]/
   bash
   NAME:
      tcld namespace export gcs - Manage GCS export sink

USAGE:
      tcld namespace export gcs command [command options] [arguments...]

COMMANDS:
      create, c    Create export sink
      update, u    Update export sink
      validate, v  Validate export sink
      get, g       Get export sink
      delete, d    Delete export sink
      list, l      List export sinks
      help, h      Shows a list of commands or help for one command

OPTIONS:
      --help, -h  show help
   bash
   tcld n export gcs create -n test.ns --sink-name test-sink --service-account-email test-sink@test-export-sink.iam.gserviceaccount.com --gcs-bucket test-export-validation
   bash
tcld n export gcs g -n test.ns --sink-name test-sink
{
	"name": "test.ns",
	"resourceVersion": "b954de0c-c6ae-4dcc-90bd-3918b52c3f28",
	"state": "Active",
	"spec": {
		"name": "test-sink",
		"enabled": true,
		"destinationType": "Gcs",
		"s3Sink": null,
		"gcsSink": {
			"saId": "test-sink",
			"bucketName": "test-export-validation",
			"gcpProjectId": "test-export-sink",
		}
	},
	"health": "Ok",
	"errorMessage": "",
	"latestDataExportTime": "0001-01-01T00:00:00Z",
	"lastHealthCheckTime": "2024-01-23T06:40:02Z"
}
command
tcld login
tcld apikey create \
    --name <api-key-name> \
    --description "<api-key-description>" \
    --duration <api-key-duration>
command
tcld login
tcld apikey disable --id <api-key-id>
tcld apikey enable --id <api-key-id>
command
tcld login
tcld apikey delete --id <api-key-id>

tcld apikey create \
    --name <api-key-name> \
    --description "<api-key-description>" \
    --duration <api-key-duration> \
    --service-account-id <service-account-id>

tcld login
tcld apikey disable --id <api-key-id>
tcld apikey enable --id <api-key-id>

tcld login
tcld apikey delete --id <api-key-id>
bash
export TEMPORAL_API_KEY=<key-secret>
temporal workflow list \
    --address <endpoint> \
    --namespace <namespace_id>.<account_id>
sh
mkdir temporal-certs
cd temporal-certs
tcld gen ca --org temporal -d 1y --ca-cert ca.pem --ca-key ca.key
sh
tcld gen leaf --org temporal -d 364d --ca-cert ca.pem --ca-key ca.key --cert client.pem --key client.key
command
step certificate create "CertAuth" CertAuth.crt CertAuth.key --profile root-ca --no-password --insecure
command
export NAMESPACE_NAME=your-namespace
command
set NAMESPACE_NAME=your-namespace
command
step certificate create ${NAMESPACE_NAME} ${NAMESPACE_NAME}.crt ${NAMESPACE_NAME}.key --ca CertAuth.crt --ca-key CertAuth.key --no-password --insecure --not-after 8760h
command
openssl pkcs8 -topk8 -inform PEM -outform PEM -in ${NAMESPACE_NAME}.key -out ${NAMESPACE_NAME}.pkcs8.key -nocrypt

-----BEGIN CERTIFICATE-----
   ... old CA cert ...
   -----END CERTIFICATE-----
   -----BEGIN CERTIFICATE-----
   ... new CA cert ...
   -----END CERTIFICATE-----
   bash
   tcld namespace accepted-client-ca set --ca-certificate-file <path>
   json
AuthorizedClientCertificate {
  CN : "code.example.com"
}
json
AuthorizedClientCertificate {
  CN : "stage.example.com"
  O : "Example Code Inc."
}
sh
temporal <command> <subcommand> \
    --tls-ca-path <Path to server CA certificate> \
    --tls-cert-path <Path to x509 certificate> \
    --tls-key-path <Path to private certificate key> \
    --tls-server-name <Override for target TLS server name>

tcld login
       
       Login via this url: https://login.tmprl.cloud/activate?user_code=KTGC-ZPWQ
       
       tcld namespace list
       
       {
         "namespaces": [
           "your-namespace.123de",
           "another-namespace.123de"
         ],
         "nextPageToken": ""
       }
       
tcld namespace lifecycle set \
    --namespace <namespace_id.account_id> \
    --enable-delete-protection <Boolean>

tcld service-account create -n "sa_test" -d "this is a test SA" --ar "Read"

tcld service-account list

tcld service-account delete --service-account-id "e9d87418221548"

tcld service-account update --id "2f68507677904e09b9bcdbf93380bb95" -d "new description"

tcld service-account created-scoped -n "test-scoped-sa" --np "test-ns=Admin"

tcld namespace create \
   --namespace <namespace_id>.<account_id> \
   --region <primary_region> \
   --region <replica_region>

tcld namespace add-region \
   --namespace <namespace_id>.<account_id> \
   --region <replica_region>

tcld namespace delete-region \
    --api-key <api_key> \
    --namespace <namespace_id>.<account_id> \
    --region <replica_region>

tcld namespace failover \
    --namespace <namespace_id>.<account_id> \
    --region <target_region>

tcld namespace update-high-availability \
    --namespace <namespace_id>.<account_id> \
    --disable-auto-failover=true

histogram_quantile(0.99, sum(rate(temporal_cloud_v0_replication_lag_bucket[$__rate_interval])) by (temporal_namespace, le))

sum(rate(temporal_cloud_v0_replication_lag_sum[$__rate_interval])) by (temporal_namespace)
/
sum(rate(temporal_cloud_v0_replication_lag_count[$__rate_interval])) by (temporal_namespace)

curl -v --cert <path to your client-cert.pem> --key <path to your client-cert.key> "<your generated Temporal Cloud prometheus_endpoint>/api/v1/query?query=temporal_cloud_v0_state_transition_count"
   
https://<account-id>.tmprl.cloud/prometheus/api/v1/query?query=temporal_cloud_v0_state_transition_count

$ curl --cert client.pem --key client-key.pem "https://<account-id>.tmprl.cloud/prometheus/api/v1/query?query=temporal_cloud_v0_state_transition_count" | jq .
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "temporal_cloud_v0_state_transition_count",
          "__rollup__": "true",
          "operation": "WorkflowContext",
          "temporal_account": "your-account",
          "temporal_namespace": "your-namespace.your-account-is",
          "temporal_service_type": "history"
        },
        "value": [
          1672347471.2,
          "0"
        ]
      },
      ...
}

rate(temporal_cloud_v0_frontend_service_request_count[$__rate_interval])

**Examples:**

Example 1 (unknown):
```unknown
Save the internal IP -- you will point the A record at it.

#### 2. Create a Cloud DNS private zone

1. Open _Network Services → Cloud DNS → Create zone_.
2. Select zone type **Private**.
3. Enter a **Zone name** (e.g., `temporal-cloud`).
4. Enter a **DNS name** based on the table above (e.g., `payments.abcde.tmprl.cloud` or `aws-us-east-1.region.tmprl.cloud`).
5. Select **Add networks** and choose the Project and Network that contains your PSC endpoint.
6. Click **Create**.

#### 3. Add an A record

Inside the new zone, add a _standard A record_:

| Field                | Value                                                          |
| -------------------- | -------------------------------------------------------------- |
| DNS name             | the namespace endpoint (e.g. `payments.abcde.tmprl.cloud`)     |
| Resource record type | A                                                              |
| TTL                  | 60s is typical, but you can adjust as needed.                  |
| IPv4 Address         | the internal IP address of your PSC endpoint (e.g. `10.1.2.3`) |

#### 4. Verify DNS resolution from inside the Network
```

Example 2 (unknown):
```unknown
If the hostname resolves to the PSC endpoint IP address from a VM in the bound network, the override is working.

### Updating your workers/clients

With private DNS in place, configure your SDKs exactly as the public-internet examples show (filling in your own namespace):
```

Example 3 (unknown):
```unknown
The DNS resolver inside your network returns the private endpoint IP address, while TLS still validates the original hostname—simplifying both code and certificate management.

## Available GCP regions, PSC endpoints, and DNS record overrides

The following table lists the available Temporal regions, PrivateLink endpoints, and regional endpoints used for DNS record overrides:

<GCPRegions />

---

## Connectivity

## Private network connectivity for namespaces

Temporal Cloud supports private connectivity to namespaces via AWS PrivateLink or GCP Private Services Connect in addition to the default internet endpoints.

Namespace access is always securely authenticated via [API keys](/cloud/api-keys#overview) or [mTLS](/cloud/certificates), regardless of how you choose to connect.

For information about IP address stability and allowlisting, see [IP addresses](/cloud/connectivity/ip-addresses).

### Required steps

To use private connectivity with Temporal Cloud:

1. Set up the private connection from your VPC to the region where your Temporal namespace is located.
1. Update your private DNS and/or worker configuration to use the private connection.
1. (Required to complete Google PSC setup, optional if using AWS PrivateLink): create a connectivity rule for the private connection and attach it to the target namespace(s). This will block all access to the namespace that is not over the private connection, but you can also add a public rule to also allow internet connectivity.

For steps 1 and 2, follow our guides for the target namespace's cloud provider:
- [AWS PrivateLink](/cloud/connectivity/aws-connectivity) creation and private DNS setup
- [Google Cloud Private Service Connect](/cloud/connectivity/gcp-connectivity) creation and private DNS setup

:::caution Finish client setup (complete step 2)

After creating a private connection, you must set up private DNS or update the configuration of all clients you want to use the private connection.

We recommend using private DNS.

Without this step, your clients may connect to the namespace over the internet if they were previously using public connectivity, or they will not be able to connect at all.

If that's not an option for you, refer to [our guide for updating the server and TLS settings on your clients](/cloud/connectivity#update-dns-or-clients-to-use-private-connectivity).

:::

For step 3, keep reading for details on [connectivity rules](/cloud/connectivity#connectivity-rules).

## Connectivity rules

:::tip Support, stability, and dependency info

Connectivity rules are currently in [public preview](/evaluate/development-production-features/release-stages#public-preview).

:::

:::info Web UI Connectivity

The Temporal Cloud Web UI is not currently subject to connectivity rule enforcement.
Even if a namespace is configured with private connectivity rules, the Web UI for that namespace remains accessible over the public internet.

:::

### Definition

Connectivity rules are Temporal Cloud's mechanism for limiting the network access paths that can be used to access a namespace.

By default, a namespace has zero connectivity rules, and is accessible from 1. the public internet and 2. all private connections you've configured to the region containing the namespace. Namespace access is always securely authenticated via [API keys](/cloud/api-keys#overview) or [mTLS](/cloud/certificates), regardless of connectivity rules.

When you attach one or more connectivity rules to a namespace, Temporal Cloud will immediately block all traffic that does not have a corresponding connectivity rule from accessing the namespace. One namespace can have multiple connectivity rules, and may mix both public and private rules.

Each connectivity rule specifies either generic public (i.e. internet) access or a specific private connection.

A public connectivity rule takes no parameters.

An AWS PrivateLink (PL) private connectivity rule requires the following parameters:

- `connection-id`: The VPC endpoint ID of the PL connection (ex: `vpce-00939a7ed9EXAMPLE`)
- `region`: The region of the PL connection, prefixed with aws (ex: `aws-us-east-1`). Must be the same region as the namespace. Refer to the [Temporal Cloud region list](/cloud/regions) for supported regions.

A GCP Private Service Connect (PSC) private connectivity rule requires the following parameters:

- `connection-id`: The ID of the PSC connection (ex: `1234567890123456789`)
- `region`: The region of the PSC connection, prefixed with gcp (ex: `gcp-us-east1`). Must be the same region as the namespace. Refer to the [Temporal Cloud region list](/cloud/regions) for supported regions.
- `gcp-project-id`: The ID of the GCP project where you created the PSC connection (ex: `my-example-project-123`)

Connectivity rules can be created and managed with [tcld](https://docs.temporal.io/cloud/tcld/), [Terraform](https://github.com/temporalio/terraform-provider-temporalcloud/), or the [Cloud Ops API](/ops)

### Permissions and limits

Only [Account Admins and Account Owners](/cloud/users#account-level-roles) can create and manage connectivity rules. Connectivity rules are visible to Account Developers, Account Admins, and Account Owners.

By default each namespace is limited to 5 private connectivity rules, and each account is limited to 50 private connectivity rules. You can [contact support](/cloud/support#support-ticket) to request a higher limit.

There is only one public rule allowed per account, because it's generic and can be reused for all namespaces that you want to be available on the internet. Trying to create more than one public rule will throw an error.

## Creating a connectivity rule

### Temporal Cloud CLI (tcld)

Create private connectivity rule (AWS):
```

Example 4 (unknown):
```unknown
Create private connectivity rule (GCP):
```

---

## Create client

**URL:** llms-txt#create-client

client = Temporalio::Client.connect('localhost:7233')

---

## Create a client

**URL:** llms-txt#create-a-client

client = Temporalio::Client.connect('localhost:7233', 'default')

---

## Create a worker with the client, activities, and workflows

**URL:** llms-txt#create-a-worker-with-the-client,-activities,-and-workflows

worker = Temporalio::Worker.new(
  client:,
  task_queue: 'my-task-queue',
  workflows: [SayHelloWorkflow],
  # There are various forms an activity can take, see "Activities" section for details
  activities: [SayHelloActivity]
)

---
