# Temporal-Cloud - Other

**Pages:** 122

---

## Get a workflow handle by its workflow ID. This could be made specific to a run by

**URL:** llms-txt#get-a-workflow-handle-by-its-workflow-id.-this-could-be-made-specific-to-a-run-by

---

## Utility method for making calls to the microservices

**URL:** llms-txt#utility-method-for-making-calls-to-the-microservices

**Contents:**
  - How to run Synchronous Activities on a Worker
- How to Implement Asynchronous Activities
  - How to run synchronous code from an asynchronous activity
- When Should You Use Async Activities
- Schedules - Python SDK
- Schedule a Workflow {#schedule-a-workflow}
  - Create a Scheduled Workflow {#create}

def call_service(stem: str, name: str) -> str:
    base = f"http://localhost:9999/{stem}"
    url = f"{base}?name={urllib.parse.quote(name)}"

response = requests.get(url)
    return response.text
python
with ThreadPoolExecutor(max_workers=42) as executor:
    worker = Worker(
        # ...
        activity_executor=executor,
        # ...
    )
python

from temporalio import activity

class TranslateActivities:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

@activity.defn
    async def greet_in_spanish(self, name: str) -> str:
        greeting = await self.call_service("get-spanish-greeting", name)
        return greeting

# Utility method for making calls to the microservices
    async def call_service(self, stem: str, name: str) -> str:
        base = f"http://localhost:9999/{stem}"
        url = f"{base}?name={urllib.parse.quote(name)}"

async with self.session.get(url) as response:
            translation = await response.text()

if response.status >= 400:
                raise ApplicationError(
                    f"HTTP Error {response.status}: {translation}",
                    # We want to have Temporal automatically retry 5xx but not 4xx
                    non_retryable=response.status < 500,
                )

return translation
python

**Examples:**

Example 1 (unknown):
```unknown
Whether to implement Activities as class methods or functions is a design
choice left up to the developer when cross-activity state isn't needed. Both are
equally valid implementations.

### How to run Synchronous Activities on a Worker

When running synchronous Activities, the Worker
needs to have an `activity_executor`. Temporal
recommends using a `ThreadPoolExecutor` as shown here:
```

Example 2 (unknown):
```unknown
## How to Implement Asynchronous Activities

The following code is an implementation of the preceding Activity, but as an
asynchronous Activity Definition.

It makes
a call to a microservice, accessed through HTTP, to request this
greeting in Spanish. This Activity uses the `aiohttp` library to make an async
safe HTTP request. Using the `requests` library here would have resulting in
blocking code within the async event loop, which will block the entire async
event loop. For more in-depth information about this issue, refer to the
[Python asyncio documentation](https://docs.python.org/3/library/asyncio-dev.html#running-blocking-code).

The following code also implements the Activity Definition as a class, rather than a
function. The `aiohttp` library requires an established `Session` to perform the
HTTP request. It would be inefficient to establish a `Session` every time an
Activity is invoked, so instead this code accepts a `Session` object as an instance
parameter and makes it available to the methods. This approach will also be
beneficial when the execution is over and the `Session` needs to be closed.

In this example, the Activity supplies the name in the URL and retrieves
the greeting from the body of the response.
```

Example 3 (unknown):
```unknown
### How to run synchronous code from an asynchronous activity

If your Activity is asynchronous and you don't want to change it to synchronous,
but you need to run blocking code inside it,
then you can use python utility functions to run synchronous code
in an asynchronous function:

- [`loop.run_in_executor()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor), which is also mentioned in the ["running blocking code" section of the "developing with asyncio" guide](https://docs.python.org/3/library/asyncio-dev.html#running-blocking-code)
- [`asyncio.to_thread()`](https://docs.python.org/3/library/asyncio-task.html#running-in-threads)

## When Should You Use Async Activities

Asynchronous Activities have many advantages, such as potential speed up of execution.
However, as discussed above, making unsafe calls within the async event loop
can cause sporadic and difficult to diagnose bugs. For this reason, we recommend
using asynchronous Activities _only_ when you are certain that your Activities
are async safe and don't make blocking calls.

If you experience bugs that you think may be a result of an unsafe call being made in an asynchronous Activity, convert it to a synchronous Activity and see if the issue resolves.

---

## Schedules - Python SDK

This page shows how to do the following:

- [Schedule a Workflow](#schedule-a-workflow)
  - [Create a Scheduled Workflow](#create)
  - [Backfill a Scheduled Workflow](#backfill)
  - [Delete a Scheduled Workflow](#delete)
  - [Describe a Scheduled Workflow](#describe)
  - [List a Scheduled Workflow](#list)
  - [Pause a Scheduled Workflow](#pause)
  - [Trigger a Scheduled Workflow](#trigger)
  - [Update a Scheduled Workflow](#update)
- [Temporal Cron Jobs](#temporal-cron-jobs)
- [Start Delay](#start-delay)

## Schedule a Workflow {#schedule-a-workflow}

**How to Schedule a Workflow Execution**

Scheduling Workflows is a crucial aspect of any automation process, especially when dealing with time-sensitive tasks. By scheduling a Workflow, you can automate repetitive tasks, reduce the need for manual intervention, and ensure timely execution of your business processes

Use any of the following action to help Schedule a Workflow Execution and take control over your automation process.

### Create a Scheduled Workflow {#create}

**How to create a Scheduled Workflow**

The create action enables you to create a new Schedule. When you create a new Schedule, a unique Schedule ID is generated, which you can use to reference the Schedule in other Schedule commands.

To create a Scheduled Workflow Execution in Python, use the [create_schedule()](https://python.temporal.io/temporalio.client.Client.html#create_schedule)
asynchronous method on the Client.
Then pass the Schedule ID and the Schedule object to the method to create a Scheduled Workflow Execution.
Set the `action` parameter to `ScheduleActionStartWorkflow` to start a Workflow Execution.
Optionally, you can set the `spec` parameter to `ScheduleSpec` to specify the schedule or set the `intervals` parameter to `ScheduleIntervalSpec` to specify the interval.
Other options include: `cron_expressions`, `skip`, `start_at`, and `jitter`.

  
    View the source code
  {' '}
  in the context of the rest of the application code.
```

---

## Example output:

**URL:** llms-txt#example-output:

---

## Raise a special exception that says an activity will be completed somewhere else

**URL:** llms-txt#raise-a-special-exception-that-says-an-activity-will-be-completed-somewhere-else

**Contents:**
- Benign exceptions - Ruby SDK
- Child Workflows - Ruby SDK
- Start a Child Workflow Execution {#child-workflows}
- Set a Parent Close Policy {#parent-close-policy}
- Continue-As-New - Ruby SDK
- Continue-As-New in Ruby {#continue-as-new}
- Converters and encryption - Ruby SDK
- Custom Payload Codec {#custom-payload-codec}
  - Using a Codec Server
- Payload conversion {#custom-payload-converter}

raise Temporalio::Activity::CompleteAsyncError
ruby
handle = my_client.async_activity_handle(captured_token)
ruby
handle.complete('completion value')
ruby
require 'temporalio/activity'

class MyActivity < Temporalio::Activity::Definition
  def execute
    begin
      call_external_service
    rescue StandardError => e
      # Mark this error as benign since it's expected
      raise Temporalio::Error::ApplicationError.new(
        e.message,
        category: Temporalio::Error::ApplicationError::Category::BENIGN
      )
    end
  end
end
ruby
Temporalio::Workflow.execute_child_workflow(MyChildWorkflow, 'my-workflow-arg')
ruby
Temporalio::Workflow.execute_child_workflow(
  MyChildWorkflow,
  'my-workflow-arg',
  parent_close_policy: Temporalio::Workflow::ParentClosePolicy::ABANDON
)
ruby
raise Temporalio::Workflow::ContinueAsNewError.new('my-new-arg')
ruby
class Base64Codec < Temporalio::Converters::PayloadCodec
  def encode(payloads)
    payloads.map do |p|
      Temporalio::Api::Common::V1::Payload.new(
        # Set our specific encoding. We may also want to add a key ID in here for use by
        # the decode side
        metadata: { 'encoding' => 'binary/my-payload-encoding' },
        data: Base64.strict_encode64(p.to_proto)
      )
    end
  end

def decode(payloads)
    payloads.map do |p|
      # Ignore if it doesn't have our expected encoding
      next p unless p.metadata['encoding'] == 'binary/my-payload-encoding'

Temporalio::Api::Common::V1::Payload.decode(
        Base64.strict_decode64(p.data)
      )
    end
  end
end
ruby
my_client = Temporalio::Client.connect(
  'localhost:7233',
  'my-namespace',
  data_converter: Temporalio::Converters::DataConverter.new(payload_codec: Base64Codec.new)
)
ruby
module ActiveModelJSONSupport
  extend ActiveSupport::Concern
  include ActiveModel::Serializers::JSON

included do
    def as_json(*)
      super.merge(::JSON.create_id => self.class.name)
    end

def to_json(*args)
      as_json.to_json(*args)
    end

def self.json_create(object)
      object = object.dup
      object.delete(::JSON.create_id)
      new(**object.symbolize_keys)
    end
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute(name)
    Temporalio::Workflow.execute_activity(
      MyActivity,
      { greeting: 'Hello', name: },
      start_to_close_timeout: 100
    )
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  # Customize the name
  workflow_name :MyDifferentWorkflowName

def execute(name)
    Temporalio::Workflow.execute_activity(
      MyActivity,
      { greeting: 'Hello', name: },
      start_to_close_timeout: 100
    )
  end
end
ruby
class MyActivity < Temporalio::Activity::Definition
  def execute(input)
    "#{input['greeting']}, #{input['name']}!"
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  # Customize the name
  workflow_name :MyDifferentWorkflowName

def execute(name)
    Temporalio::Workflow.execute_activity(
      MyActivity,
      { greeting: 'Hello', name: },
      start_to_close_timeout: 100
    )
  end
end
ruby

**Examples:**

Example 1 (unknown):
```unknown
To update an Activity outside the Activity, use the [async_activity_handle](https://ruby.temporal.io/Temporalio/Client.html#async_activity_handle-instance_method) method on the client to get the handle of the Activity.
```

Example 2 (unknown):
```unknown
Then, on that handle, you can use `heartbeat`, `complete`, `fail`, or `report_cancellation` methods to update the Activity.
```

Example 3 (unknown):
```unknown
---

## Benign exceptions - Ruby SDK

**How to mark an Activity error as benign using the Temporal Ruby SDK**

When Activities throw errors that are expected or not severe, they can create noise in your logs, metrics, and OpenTelemetry traces, making it harder to identify real issues.
By marking these errors as benign, you can exclude them from your observability data while still handling them in your Workflow logic.

To mark an error as benign, set the `category` parameter to `Temporalio::Error::ApplicationError::Category::BENIGN` when raising an `ApplicationError`.

Benign errors:
- Have Activity failure logs downgraded to DEBUG level
- Do not emit Activity failure metrics
- Do not set the OpenTelemetry failure status to ERROR
```

Example 4 (unknown):
```unknown
Use benign exceptions for Activity errors that occur regularly as part of normal operations, such as polling an external service that isn't ready yet, or handling expected transient failures that will be retried.

---

## Child Workflows - Ruby SDK

This page shows how to do the following:

- [Start a Child Workflow Execution](#child-workflows) using the Ruby SDK
- [Set a Parent Close Policy](#parent-close-policy) using the Ruby SDK

## Start a Child Workflow Execution {#child-workflows}

A [Child Workflow Execution](/child-workflows) is a Workflow Execution that is scheduled from within another Workflow using a Child Workflow API.

When using a Child Workflow API, Child Workflow related Events ([StartChildWorkflowExecutionInitiated](/references/events#startchildworkflowexecutioninitiated), [ChildWorkflowExecutionStarted](/references/events#childworkflowexecutionstarted), [ChildWorkflowExecutionCompleted](/references/events#childworkflowexecutioncompleted), etc...) are logged in the Workflow Execution Event History.

Always block progress until the [ChildWorkflowExecutionStarted](/references/events#childworkflowexecutionstarted) Event is logged to the Event History to ensure the Child Workflow Execution has started.
After that, Child Workflow Executions may be abandoned using the _Abandon_ [Parent Close Policy](/parent-close-policy) set in the Child Workflow Options.

To spawn a Child Workflow Execution in Ruby, use the `execute_child_workflow` method which starts the Child Workflow and waits for completion or
use the `start_child_workflow` method to start a Child Workflow and return its handle.
This is useful if you want to do something after it has only started, or to get the Workflow/Run ID, or to be able to signal it while running.

:::note

`execute_child_workflow` is a helper method for `start_child_workflow(...).result`.

:::
```

---

## workflow result

**URL:** llms-txt#workflow-result

**Contents:**
- Message handler patterns {#message-handler-patterns}
  - Add async handlers {#async-handlers}
  - Use wait conditions {#block-with-wait}
  - Use workflow_init to access input early
  - Use locks to prevent concurrent handler execution {#control-handler-concurrency}
- Troubleshooting {#message-handler-troubleshooting}
  - Signal issues {#signal-problems}
  - Update issues {#update-problems}
  - Query issues {#query-problems}
- Dynamic handlers {#dynamic-handler}

workflow_result = start_workflow_operation.workflow_handle.result
ruby
class CallGreetingService < Temporalio::Activity::Definition
  def execute(to_language)
    # Simulate a network call
    sleep(0.2)
    # This intentionally returns nil on not found
    CallGreetingService.greetings[to_language.to_sym]
  end

def self.greetings
    @greetings ||= {
      arabic: 'مرحبا بالعالم',
      chinese: '你好，世界',
      english: 'Hello, world',
      french: 'Bonjour, monde',
      hindi: 'नमस्ते दुनिया',
      portuguese: 'Olá mundo',
      spanish: 'Hola mundo'
    }
  end
end
ruby
class GreetingWorkflow < Temporalio::Workflow::Definition
  # ...

workflow_update
  def apply_language_with_lookup(new_language)
    # Call an activity if it's not there.
    unless @greetings.include?(new_language.to_sym)
      # We use a mutex so that, if this handler is executed multiple times, each execution
      # can schedule the activity only when the previously scheduled activity has
      # completed. This ensures that multiple calls to apply_language_with_lookup are
      # processed in order.
      @apply_language_mutex ||= Mutex.new
      @apply_language_mutex.synchronize do
        greeting = Temporalio::Workflow.execute_activity(
          CallGreetingService, new_language, start_to_close_timeout: 10
        )
        # The requested language might not be supported by the remote service. If so, we
        # raise ApplicationError, which will fail the update. The
        # WorkflowExecutionUpdateAccepted event will still be added to history. (Update
        # validators can be used to reject updates before any event is written to history,
        # but they cannot be async, and so we cannot use an update validator for this
        # purpose.)
        raise Temporalio::Error::ApplicationError, "Greeting service does not support #{new_language}" unless greeting

@greetings[new_language.to_sym] = greeting
      end
    end
    set_language(new_language)
  end
end
ruby
workflow_update
def my_update(my_update_input)
  Temporalio::Workflow.wait_condition { ready_for_update_to_execute(my_update_input) }
  # ...
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    # ...

Temporalio::Workflow.wait_condition { Temporalio::Workflow.all_handlers_finished? }
    'workflow-result'
  end
end
ruby
workflow_update unfinished_policy: Temporalio::Workflow::HandlerUnfinishedPolicy::ABANDON
def my_update
  # ...
ruby
class WorkflowInitWorkflow < Temporalio::Workflow::Definition
  workflow_init
  def initialize(input)
    @name_with_title = "Sir #{input['name']}"
  end

def execute(input)
    Temporalio::Workflow.wait_condition { @title_has_been_checked }
    "Hello, #{@name_with_title}"
  end

workflow_update
  def check_title_validity
    # The handler is now guaranteed to see some workflow input since it was
    # processed by the constructor
    valid = Temporalio::Workflow.execute_activity(
      CheckTitleValidityActivity,
      @name_with_title,
      start_to_close_timeout: 100
    )
    @title_has_been_checked = true
    valid
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  # ...

workflow_signal
  def bad_handler
    data = Temporalio::Workflow.execute_activity(
      FetchDataActivity,
      start_to_close_timeout: 100
    )
    @x = data['x']
    # 🐛🐛 Bug!! If multiple instances of this handler are executing concurrently, then
    # there may be times when the Workflow has @x from one Activity execution and @y
    # from another.
    Temporalio::Workflow.sleep(1)
    @y = data['y']
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  # ...

workflow_signal
  def safe_handler
    @mutex ||= Mutex.new
    @mutex.synchronize do
      data = Temporalio::Workflow.execute_activity(
        FetchDataActivity,
        start_to_close_timeout: 100
      )
      @x = data['x']
      # 🐛🐛 Bug!! If multiple instances of this handler are executing concurrently, then
      # there may be times when the Workflow has @x from one Activity execution and @y
      # from another.
      Temporalio::Workflow.sleep(1)
      @y = data['y']
    end
  end
end
ruby
workflow_query dynamic: true, raw_args: true
def dynamic_query(query_name, *args)
  first_param = Temporalio::Workflow.payload_converter.from_payload(
    args.first || raise 'Missing first parameter'
  )
  "Got parameter #{first_param} for query #{query_name}"
end
ruby
workflow_signal dynamic: true, raw_args: true
def dynamic_signal(signal_name, *args)
  first_param = Temporalio::Workflow.payload_converter.from_payload(
    args.first || raise 'Missing first parameter'
  )
  @pending_things << "Got parameter #{first_param} for signal #{signal_name}"
end
ruby
workflow_update dynamic: true, raw_args: true
def dynamic_update(update_name, *args)
  first_param = Temporalio::Workflow.payload_converter.from_payload(
    args.first || raise 'Missing first parameter'
  )
  @pending_things << "Got parameter #{first_param} for update #{update_name}"
end
ruby
Temporalio::Runtime.default = Temporalio::Runtime.new(
  telemetry: Temporalio::Runtime::TelemetryOptions.new(
    metrics: Temporalio::Runtime::MetricsOptions.new(
      prometheus: Temporalio::Runtime::PrometheusMetricsOptions.new(
        bind_address: '0.0.0.0:9000'
      )
    )
  )
)
ruby
require 'opentelemetry/api'
require 'opentelemetry/sdk'
require 'temporalio/client'
require 'temporalio/contrib/open_telemetry'

**Examples:**

Example 1 (unknown):
```unknown
## Message handler patterns {#message-handler-patterns}

This section covers common write operations, such as Signal and Update handlers.
It doesn't apply to pure read operations, like Queries or Update Validators.

:::tip

For additional information, see [Inject work into the main Workflow](/handling-messages#injecting-work-into-main-workflow) and [Ensuring your messages are processed exactly once](/handling-messages#exactly-once-message-processing).

:::

### Add async handlers {#async-handlers}

Signal and Update handlers can be asynchronous as well as blocking.
Using asynchronous calls allows you to wait for Activities, Child Workflows, Durable Timers, wait conditions, etc.
This expands the possibilities for what can be done by a handler but it also means that handler executions and your main Workflow method are all running concurrently, with switching occurring between them at await calls.

It's essential to understand the things that could go wrong in order to use asynchronous handlers safely.
See [Workflow message passing](/encyclopedia/workflow-message-passing) for guidance on safe usage of async Signal and Update handlers, and the [Controlling handler concurrency](#control-handler-concurrency) and [Waiting for message handlers to finish](#wait-for-message-handlers) sections below.

The following code is an Activity that simulates a network call to a remote service:
```

Example 2 (unknown):
```unknown
The following code is a Workflow Update for asynchronous use of the preceding Activity:
```

Example 3 (unknown):
```unknown
After updating the code for asynchronous calls, your Update handler can schedule an Activity and await the result.
Although an async Signal handler can initiate similar network tasks, using an Update handler allows the Client to receive a result or error once the Activity completes.
This lets your Client track the progress of asynchronous work performed by the Update's Activities, Child Workflows, etc.

### Use wait conditions {#block-with-wait}

Sometimes, async Signal or Update handlers need to meet certain conditions before they should continue.
Using a wait condition with [`wait_condition`](https://ruby.temporal.io/Temporalio/Workflow.html#wait_condition-class_method) sets a function that prevents the code from proceeding until the condition is truthy.
This is an important feature that helps you control your handler logic.

Here are two important use cases for `wait_condition`:

- Waiting in a handler until it is appropriate to continue.
- Waiting in the main Workflow until all active handlers have finished.

The condition state you're waiting for can be updated by and reflect any part of the Workflow code.
This includes the main Workflow method, other handlers, or child coroutines spawned by the main Workflow method, and so forth.

#### In handlers {#wait-in-handlers}

Sometimes, async Signal or Update handlers need to meet certain conditions before they should continue.
Using a wait condition with [`wait_condition`](https://ruby.temporal.io/Temporalio/Workflow.html#wait_condition-class_method) sets a function that prevents the code from proceeding until the condition is truthy.
This is an important feature that helps you control your handler logic.

Consider a `ready_for_update_to_execute` method that runs before your Update handler executes.
The `wait_condition` call waits until your condition is met:
```

Example 4 (unknown):
```unknown
Remember: Handlers can execute before the main Workflow method starts.

#### Before finishing the Workflow {#wait-for-message-handlers}

Workflow wait conditions can ensure your handler completes before a Workflow finishes.
When your Workflow uses async Signal or Update handlers, your main Workflow method can return or continue-as-new while a handler is still waiting on an async task, such as an Activity result.
The Workflow completing may interrupt the handler before it finishes crucial work and cause Client errors when trying retrieve Update results.
Use `Temporalio::Workflow.all_handlers_finished?` to address this problem and allow your Workflow to end smoothly:
```

---

## TYPE temporal_cloud_v1_frontend_service_request_count gauge

**URL:** llms-txt#type-temporal_cloud_v1_frontend_service_request_count-gauge

---

## the default Runtime from being lazily created.

**URL:** llms-txt#the-default-runtime-from-being-lazily-created.

**Contents:**
- Set up tracing {#tracing}

new_runtime = Runtime(telemetry=TelemetryConfig(metrics=PrometheusConfig(bind_address="0.0.0.0:9000")))
my_client = await Client.connect("my.temporal.host:7233", runtime=new_runtime)
bash

**Examples:**

Example 1 (unknown):
```unknown
## Set up tracing {#tracing}

**How to set up tracing**

Tracing allows you to view the call graph of a Workflow along with its Activities and any Child Workflows.

Temporal Web's tracing capabilities mainly track Activity Execution within a Temporal context. If you need custom tracing specific for your use case, you should make use of context propagation to add tracing logic accordingly.

To configure tracing in Python, install the `opentelemetry` dependencies.
```

---

## set your PostgreSQL environment variables

**URL:** llms-txt#set-your-postgresql-environment-variables

: "${DBNAME:=temporal}"
: "${VISIBILITY_DBNAME:=temporal_visibility}"
: "${DB_PORT:=}"
: "${POSTGRES_SEEDS:=}"
: "${POSTGRES_USER:=}"
: "${POSTGRES_PWD:=}"

#... set connection details

---

## Set Python to run in unbuffered mode

**URL:** llms-txt#set-python-to-run-in-unbuffered-mode

ENV PYTHONUNBUFFERED=1

---

## Cloud profile for Temporal Cloud

**URL:** llms-txt#cloud-profile-for-temporal-cloud

**Contents:**
- NativeConnection, Connection, and Client
  - NativeConnection vs. Connection {#native-connection-vs-connection}
  - Connection vs. Client {#connection-vs-client}
- Start Workflow Execution {#start-workflow-execution}
  - Set a Workflow's Task Queue {#set-task-queue}
  - Set a Workflow Id {#workflow-id}
  - Get the results of a Workflow Execution {#get-workflow-results}
- Temporal Nexus - TypeScript SDK Feature Guide
- Run the Temporal Development Server with Nexus enabled {#run-the-temporal-nexus-development-server}
- Create caller and handler Namespaces {#create-caller-handler-namespaces}

[profile.staging]
address = "your-namespace.a1b2c.tmprl.cloud:7233"
namespace = "your-namespace"
api_key = "your-api-key-here"
ts {1,15,17}

async function main() {
  const configFile = resolve(__dirname, '../config.toml');
  const profileName = 'staging'

// Load the 'staging' profile.
  const config = loadClientConnectConfig({
    profile: profileName,
    configSource: { path: configFile },
  });

const connection = await NativeConnection.connect(config.connectionOptions);

const worker = await Worker.create({
    connection,
    namespace: <namespace_id>.<account_id>,
    // ...
});
}
bash
export TEMPORAL_NAMESPACE="your-namespace.your-account-id"
export TEMPORAL_ADDRESS="your-namespace.a1b2c.tmprl.cloud:7233"
export TEMPORAL_TLS_CLIENT_CERT_PATH="/path/to/your/client/cert.pem"
export TEMPORAL_TLS_CLIENT_KEY_PATH="/path/to/your/client/key.pem"
ts {1,5}

async function main() {
  const config = loadClientConnectConfig();

const connection = await NativeConnection.connect(config.connectionOptions);

const worker = await Worker.create({
    connection,
    namespace: process.env.TEMPORAL_NAMESPACE,
    // ...
  });
}
ts {1,4,9}

const connection = await NativeConnection.connect({
    address: <endpoint>,
    tls: true,
    apiKey: <APIKey>,
});
const worker = await Worker.create({
    connection,
    namespace: <namespace_id>.<account_id>,
    // ...
});
typescript
const handle = await client.workflow.start(example, {
  workflowId: 'your-workflow-id',
  taskQueue: 'your-task-queue',
  args: ['argument01', 'argument02', 'argument03'], // this is typechecked against workflowFn's args
});
const handle = client.getHandle(workflowId);
const result = await handle.result();
ts

async function run() {
  // Step 1: Register Workflows and Activities with the Worker and connect to
  // the Temporal server.
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    activities,
    taskQueue: 'hello-world',
  });
  // Worker connects to localhost by default and uses console.error for logging.
  // Customize the Worker by passing more options to create():
  // https://typescript.temporal.io/api/classes/worker.Worker
  // If you need to configure server connection parameters, see docs:
  // /typescript/security#encryption-in-transit-with-mtls

// Step 2: Start accepting tasks on the `tutorial` queue
  await worker.run();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
ts

// This is the code that is used to start a Workflow.
const connection = await Connection.create();
const client = new Client({ connection });
const result = await client.workflow.execute(yourWorkflow, {
  // required
  taskQueue: 'your-task-queue',
  // required
  workflowId: 'your-workflow-id',
});
ts
const worker = await Worker.create({
  // imported elsewhere
  activities,
  taskQueue: 'your-task-queue',
});
typescript
const handle = await client.workflow.start(example, {
  workflowId: 'yourWorkflowId',
  taskQueue: 'yourTaskQueue',
  args: ['your', 'arg', 'uments'],
});
typescript
return 'Completed ' + wf.workflowInfo().workflowId + ', Total Charged: ' + totalCharged;
typescript
const handle = client.getHandle(workflowId);
const result = await handle.result();
typescript
const handle = client.getHandle(workflowId);
try {
  const result = await handle.result();
} catch (err) {
  if (err instanceof WorkflowFailedError) {
    throw new Error('Temporal workflow failed: ' + workflowId, {
      cause: err,
    });
  } else {
    throw new Error('error from Temporal workflow ' + workflowId, {
      cause: err,
    });
  }
}

temporal server start-dev

temporal operator namespace create --namespace my-target-namespace
temporal operator namespace create --namespace my-caller-namespace

temporal operator nexus endpoint create \
  --name my-nexus-endpoint-name \
  --target-namespace my-target-namespace \
  --target-task-queue my-handler-task-queue
ts

export const helloService = nexus.service('hello', {
  /**
   * Return the input message, unmodified. In the present sample, this Operation
   * will be implemented using the Synchronous Nexus Operation handler syntax.
   */
  echo: nexus.operation<EchoInput, EchoOutput>(),

/**
   * Return a salutation message, in the requested language. In the present sample,
   * this Operation will be implemented by starting the `helloWorkflow` Workflow.
   */
  hello: nexus.operation<HelloInput, HelloOutput>(),
});

export interface EchoInput {
  message: string;
}

export interface EchoOutput {
  message: string;
}

export interface HelloInput {
  name: string;
  language: LanguageCode;
}

export interface HelloOutput {
  message: string;
}

export type LanguageCode = 'en' | 'fr' | 'de' | 'es' | 'tr';
ts
// ...

export const helloServiceHandler = nexus.serviceHandler(helloService, {
  echo: async (ctx, input: EchoInput): Promise<EchoOutput> => {
    // A simple async function can be used to defined a Synchronous Nexus Operation.
    // This is often sufficient for Operations that simply make arbitrary short calls to
    // other services or databases, or that perform simple computations such as this one.
    //
    // You may also access a Temporal Client by calling `temporalNexus.getClient()`.
    // That Client can be used to make arbitrary calls, such as signaling, querying,
    // or listing workflows.
    return input;
  },
// ...
});
ts

export const helloServiceHandler = nexus.serviceHandler(helloService, {
// ...
  hello: new temporalNexus.WorkflowRunOperationHandler<HelloInput, HelloOutput>(
    // WorkflowRunOperationHandler takes a function that receives the Operation's context and input.
    // That function can be used to validate and/or transform the input before passing it to
    // the Workflow, as well as to customize various Workflow start options as appropriate.
    // Call temporalNexus.startWorkflow() to actually start the Workflow from inside the
    // WorkflowRunOperationHandler's delegate function.
    async (ctx, input: HelloInput) => {
      return await temporalNexus.startWorkflow(ctx, helloWorkflow, {
        args: [input],

// Workflow IDs should typically be business-meaningful IDs and are used to dedupe workflow starts.
        // For this example, we're using the request ID allocated by Temporal when the caller workflow schedules
        // the operation, this ID is guaranteed to be stable across retries of this operation.
        workflowId: ctx.requestId ?? randomUUID(),

// Task queue defaults to the task queue this Operation is handled on.
      });
    },
  ),
});
ts

// ...
    const namespace = 'my-target-namespace';
    const serviceTaskQueue = 'my-handler-task-queue';
    const worker = await Worker.create({
      connection,
      namespace,
      taskQueue: serviceTaskQueue,
      workflowsPath: require.resolve('./workflows'),
      nexusServices: [helloServiceHandler],
    });
ts

const HELLO_SERVICE_ENDPOINT = "hello-service-endpoint-name";

export async function helloCallerWorkflow(name: string, language: LanguageCode): Promise<string> {
  const nexusClient = wf.createNexusClient({
    service: helloService,
    endpoint: HELLO_SERVICE_ENDPOINT,
  });

const helloResult = await nexusClient.executeOperation(
    "hello",
    { name, language },
    { scheduleToCloseTimeout: "10s" }
  );

return helloResult.message;
}

brew install temporalio/brew/tcld

tcld gen ca --org $YOUR_ORG_NAME --validity-period 1y --ca-cert ca.pem --ca-key ca.key

tcld namespace create \
	--namespace <your-caller-namespace> \
	--cloud-provider aws \
	--region us-west-2 \
	--ca-certificate-file 'path/to/your/ca.pem' \
	--retention-days 1

tcld namespace create \
	--namespace <your-target-namespace> \
	--cloud-provider aws \
	--region us-west-2 \
	--ca-certificate-file 'path/to/your/ca.pem' \
	--retention-days 1

tcld nexus endpoint create \
  --name <my-nexus-endpoint-name> \
  --target-task-queue my-handler-task-queue \
  --target-namespace <my-target-namespace.account> \
  --allow-namespace <my-caller-namespace.account> \
  --description-file description.md

temporal workflow describe -w <ID>

temporal workflow show -w <ID>
ts

// A function that takes two numbers and returns a promise that resolves to the sum of the two numbers
// and the current attempt.
async function activityFoo(a: number, b: number): Promise<number> {
  return a + b + activityInfo().attempt;
}

// Create a MockActivityEnvironment with attempt set to 2. Run the activityFoo
// function with parameters 5 and 35. Assert that the result is 42.
const env = new MockActivityEnvironment({ attempt: 2 });
const result = await env.run(activityFoo, 5, 35);
assert.equal(result, 42);
ts

async function activityFoo(): Promise<void> {
  heartbeat(6);
}

const env = new MockActivityEnvironment();

env.on('heartbeat', (d: unknown) => {
  assert(d === 6);
});

await env.run(activityFoo);
ts

async function activityFoo(): Promise<void> {
  heartbeat(6);
  // @temporalio/activity's sleep() is Cancellation-aware, which means that on Cancellation,
  // CancelledFailure will be thrown from it.
  await sleep(100);
}

const env = new MockActivityEnvironment();

env.on('heartbeat', (d: unknown) => {
  assert(d === 6);
});

await assert.rejects(env.run(activityFoo), (err) => {
  assert.ok(err instanceof CancelledFailure);
});
ts

// Creating a mock object of the activities.
const mockActivities: Partial<typeof activities> = {
  makeHTTPRequest: async () => '99',
};

// Creating a worker with the mocked activities.
const worker = await Worker.create({
  activities: mockActivities,
  // ...
});
bash
npm install @temporalio/testing
typescript

let testEnv: TestWorkflowEnvironment;

// beforeAll and afterAll are injected by Jest
beforeAll(async () => {
  testEnv = await TestWorkflowEnvironment.createTimeSkipping();
});

afterAll(async () => {
  await testEnv?.teardown();
});
typescript

test('workflowFoo', async () => {
  const worker = await Worker.create({
    connection: testEnv.nativeConnection,
    taskQueue: 'test',
    ...
  });
  const result = await worker.runUntil(
    testEnv.client.workflow.execute(workflowFoo, {
      workflowId: uuid4(),
      taskQueue: 'test',
    })
  );
  expect(result).toEqual('foo');
});
ts

export async function sleeperWorkflow() {
  await sleep('1 day');
}
ts

test('sleep completes almost immediately', async () => {
  const worker = await Worker.create({
    connection: testEnv.nativeConnection,
    taskQueue: 'test',
    workflowsPath: require.resolve('./workflows'),
  });
  // Does not wait an entire day
  await worker.runUntil(
    testEnv.client.workflow.execute(sleeperWorkflow, {
      workflowId: uuid(),
      taskQueue: 'test',
    }),
  );
});
ts

export const daysQuery = defineQuery('days');

export async function sleeperWorkflow() {
  let numDays = 0;

setHandler(daysQuery, () => numDays);

for (let i = 0; i < 100; i++) {
    await sleep('1 day');
    numDays++;
  }
}
ts
test('sleeperWorkflow counts days correctly', async () => {
  const worker = await Worker.create({
    connection: testEnv.nativeConnection,
    taskQueue: 'test',
    workflowsPath: require.resolve('./workflows'),
  });

// `start()` starts the test server in "normal" mode, not skipped time mode.
  // If you don't advance time using `testEnv.sleep()`, then `sleeperWorkflow()`
  // will run for days.
  handle = await testEnv.client.workflow.start(sleeperWorkflow, {
    workflowId: uuid4(),
    taskQueue,
  });

let numDays = await handle.query(daysQuery);
  assert.equal(numDays, 0);

// Advance the test server's time by 25 hours
  await testEnv.sleep('25 hours');
  numDays = await handle.query(daysQuery);
  assert.equal(numDays, 1);

await testEnv.sleep('25 hours');
  numDays = await handle.query(daysQuery);
  assert.equal(numDays, 2);
});
ts
export async function processOrderWorkflow({
  orderProcessingMS,
  sendDelayedEmailTimeoutMS,
}: ProcessOrderOptions): Promise<string> {
  let processing = true;
  // Dynamically define the timeout based on given input
  const { processOrder } = proxyActivities<ReturnType<typeof createActivities>>({
    startToCloseTimeout: orderProcessingMS,
  });

const processOrderPromise = processOrder().then(() => {
    processing = false;
  });

await Promise.race([processOrderPromise, sleep(sendDelayedEmailTimeoutMS)]);

if (processing) {
    await sendNotificationEmail();

await processOrderPromise;
  }

return 'Order completed!';
}
ts
it('sends reminder email if processOrder does not complete in time', async () => {
  // This test doesn't actually take days to complete: the TestWorkflowEnvironment starts the
  // Test Server, which automatically skips time when there are no running Activities.
  let emailSent = false;
  const mockActivities: ReturnType<typeof createActivities> = {
    async processOrder() {
      // Test server switches to "normal" time while an Activity is executing.
      // Call `env.sleep` to skip ahead 2 days, by which time sendNotificationEmail
      // should have been called.
      await env.sleep('2 days');
    },
    async sendNotificationEmail() {
      emailSent = true;
    },
  };
  const worker = await Worker.create({
    connection: env.nativeConnection,
    taskQueue: 'test',
    workflowsPath: require.resolve('../workflows'),
    activities: mockActivities,
  });
  await worker.runUntil(
    env.client.workflow.execute(processOrderWorkflow, {
      workflowId: uuid(),
      taskQueue: 'test',
      args: [{ orderProcessingMS: ms('3 days'), sendDelayedEmailTimeoutMS: ms('1 day') }],
    }),
  );
  assert.ok(emailSent);
});
ts

export async function functionToTest(): Promise<number> {
  await sleep('1 day');
  return 42;
}
ts
const worker = await Worker.create({
  connection: testEnv.nativeConnection,
  workflowsPath: require.resolve(
    './workflows/file-with-workflow-function-to-test',
  ),
});

const result = await worker.runUntil(
  testEnv.client.workflow.execute(functionToTest, workflowOptions),
);

assert.equal(result, 42);
ts

export { someWorkflowToRunAsChild };

export async function functionToTest(): Promise<number> {
  const result = await wf.executeChild(someWorkflowToRunAsChild);
  return result + 42;
}
ts

export async function functionToTest() {
  assert.ok(false);
}
ts

TestWorkflowEnvironment,
  workflowInterceptorModules,
} from '@temporalio/testing';

const worker = await Worker.create({
  connection: testEnv.nativeConnection,
  interceptors: {
    workflowModules: workflowInterceptorModules,
  },
  workflowsPath: require.resolve(
    './workflows/file-with-workflow-function-to-test',
  ),
});

await worker.runUntil(
  testEnv.client.workflow.execute(functionToTest, workflowOptions), // throws WorkflowFailedError
);
ts
const filePath = './history_file.json';
const history = await JSON.parse(fs.promises.readFile(filePath, 'utf8'));
await Worker.runReplayHistory(
  {
    workflowsPath: require.resolve('./your/workflows'),
  },
  history,
);
ts
const connection = await Connection.connect({ address });
const client = new Client({ connection, namespace: 'your-namespace' });
const handle = client.workflow.getHandle('your-workflow-id');
const history = await handle.fetchHistory();
await Worker.runReplayHistory(
  {
    workflowsPath: require.resolve('./your/workflows'),
  },
  history,
);
ts
const executions = client.workflow.list({
  query: 'TaskQueue=foo and StartTime > "2022-01-01T12:00:00"',
});
const histories = executions.intoHistories();
const results = Worker.runReplayHistories(
  {
    workflowsPath: require.resolve('./your/workflows'),
  },
  histories,
);
for await (const result of results) {
  if (result.error) {
    console.error('Replay failed', result);
  }
}
ts
export async function processOrderWorkflow({
  orderProcessingMS,
  sendDelayedEmailTimeoutMS,
}: ProcessOrderOptions): Promise<void> {
  let processing = true;
  const processOrderPromise = processOrder(orderProcessingMS).then(() => {
    processing = false;
  });

await Promise.race([processOrderPromise, sleep(sendDelayedEmailTimeoutMS)]);

if (processing) {
    await sendNotificationEmail();
    await processOrderPromise;
  }
}
ts

const userInteraction = new Trigger<boolean>();
const completeUserInteraction = defineSignal('completeUserInteraction');

export async function yourWorkflow(userId: string) {
  setHandler(completeUserInteraction, () => userInteraction.resolve(true)); // programmatic resolve
  const userInteracted = await Promise.race([
    userInteraction,
    sleep('30 days'),
  ]);
  if (!userInteracted) {
    await sendReminderEmail(userId);
  }
}
ts
await Promise.race([
  sleep('5s').then(() => (status = 'timed_out')),
  somethingElse.then(() => (status = 'processed')),
]);

if (status === 'processed') await complete(); // takes more than 5 seconds
// status = timed_out
ts

// usage
export async function countdownWorkflow(): Promise<void> {
  const target = Date.now() + 24 * 60 * 60 * 1000; // 1 day!!!
  const timer = new UpdatableTimer(target);
  console.log('timer set for: ' + new Date(target).toString());
  wf.setHandler(setDeadlineSignal, (deadline) => {
    // send in new deadlines via Signal
    timer.deadline = deadline;
    console.log('timer now set for: ' + new Date(deadline).toString());
  });
  wf.setHandler(timeLeftQuery, () => timer.deadline - Date.now());
  await timer; // if you send in a signal with a new time, this timer will resolve earlier!
  console.log('countdown done!');
}
ts
// implementation
export class UpdatableTimer implements PromiseLike<void> {
  deadlineUpdated = false;
  #deadline: number;

constructor(deadline: number) {
    this.#deadline = deadline;
  }

private async run(): Promise<void> {
    /* eslint-disable no-constant-condition */
    while (true) {
      this.deadlineUpdated = false;
      if (
        !(await wf.condition(
          () => this.deadlineUpdated,
          this.#deadline - Date.now(),
        ))
      ) {
        break;
      }
    }
  }

then<TResult1 = void, TResult2 = never>(
    onfulfilled?: (value: void) => TResult1 | PromiseLike<TResult1>,
    onrejected?: (reason: any) => TResult2 | PromiseLike<TResult2>,
  ): PromiseLike<TResult1 | TResult2> {
    return this.run().then(onfulfilled, onrejected);
  }

set deadline(value: number) {
    this.#deadline = value;
    this.deadlineUpdated = true;
  }

get deadline(): number {
    return this.#deadline;
  }
}
ts
// v1
export async function myWorkflow(): Promise<void> {
  await activityA();
  await sleep('1 days'); // arbitrary long sleep to simulate a long running workflow we need to patch
  await activityThatMustRunAfterA();
}
ts
// vFinal
export async function myWorkflow(): Promise<void> {
  await activityB();
  await sleep('1 days');
}
ts
// v2

export async function myWorkflow(): Promise<void> {
  if (patched('my-change-id')) {
    await activityB();
    await sleep('1 days');
  } else {
    await activityA();
    await sleep('1 days');
    await activityThatMustRunAfterA();
  }
}
ts
// v3

export async function myWorkflow(): Promise<void> {
  deprecatePatch('my-change-id');
  await activityB();
  await sleep('1 days');
}
typescript
function pizzaWorkflow(order: PizzaOrder): Promise<OrderConfirmation> {
  // this function contains the original code
}

function pizzaWorkflowV2(order: PizzaOrder): Promise<OrderConfirmation> {
  // this function contains the updated code
}
typescript
const worker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  // other configurations
});
typescript
// ...
const worker = await Worker.create({
  taskQueue: 'your_task_queue_name',
  buildId: buildId,
  useVersioning: true,
  // ...
});
// ...
typescript
// ...
const { echo } = proxyActivities<typeof activities>({
  startToCloseTimeout: '20s',
  versioningIntent: 'USE_ASSIGNMENT_RULES',
});
// ...
typescript
// ...
await client.taskQueue.updateBuildIdCompatibility('your_task_queue_name', {
  operation: 'addNewIdInNewDefaultSet',
  buildId: 'deadbeef',
});
typescript
// ...
await client.taskQueue.updateBuildIdCompatibility('your_task_queue_name', {
  operation: 'addNewCompatibleVersion',
  buildId: 'deadbeef',
  existingCompatibleBuildId: 'some-existing-build-id',
});
typescript
// ...
await client.taskQueue.updateBuildIdCompatibility('your_task_queue_name', {
  operation: 'promoteBuildIdWithinSet',
  buildId: 'deadbeef',
});
typescript
// ...
await client.taskQueue.updateBuildIdCompatibility('your_task_queue_name', {
  operation: 'promoteSetByBuildId',
  buildId: 'deadbeef',
});
typescript
// ...
await client.taskQueue.updateBuildIdCompatibility('your_task_queue_name', {
  operation: 'mergeSets',
  primaryBuildId: 'deadbeef',
  secondaryBuildId: 'some-existing-build-id',
});
go
w := worker.New(c, "my-task-queue", worker.Options{
  WorkflowTaskPollerBehavior: worker.NewPollerBehaviorAutoscaling(worker.PollerBehaviorAutoscalingOptions{}),
  ActivityTaskPollerBehavior: worker.NewPollerBehaviorAutoscaling(worker.PollerBehaviorAutoscalingOptions{}),
  NexusTaskPollerBehavior: worker.NewPollerBehaviorAutoscaling(worker.PollerBehaviorAutoscalingOptions{}),
})
java
public class WorkerExample {
    public static void main(String[] args) {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);
        WorkerFactory factory = WorkerFactory.newInstance(client);
        WorkerOptions workerOptions = WorkerOptions.newBuilder()
            .setWorkflowTaskPollersBehavior(new PollerBehaviorAutoscaling())
            .setActivityTaskPollersBehavior(new PollerBehaviorAutoscaling())
            .setNexusTaskPollersBehavior(new PollerBehaviorAutoscaling())
            .build();

Worker worker = factory.newWorker("my-task-queue", workerOptions);
    }
}
python
worker = Worker(
    client,
    task_queue="my-task-queue",
    workflows=[MyWorkflow],
    activities=[my_activity],
    
    workflow_task_poller_behavior=PollerBehaviorAutoscaling(),
    activity_task_poller_behavior=PollerBehaviorAutoscaling(),
    nexus_task_poller_behavior=PollerBehaviorAutoscaling(),
)
ts
const worker = await Worker.create({
  connection,
  taskQueue: 'my-task-queue',
  workflowsPath: require.resolve('./workflows'),
  activities,
  
  workflowTaskPollerBehavior: PollerBehavior.autoscaling(),
  activityTaskPollerBehavior: PollerBehavior.autoscaling(),
  nexusTaskPollerBehavior: PollerBehavior.autoscaling(),
});
csharp
using var worker = new TemporalWorker(
    client,
    new TemporalWorkerOptions("my-task-queue")
    {
        WorkflowTaskPollerBehavior = new PollerBehavior.Autoscaling(),
        ActivityTaskPollerBehavior = new PollerBehavior.Autoscaling(),
        NexusTaskPollerBehavior = new PollerBehavior.Autoscaling(),
    }
    .AddWorkflow<MyWorkflow>()
    .AddActivity(MyActivities.MyActivity)
);
ruby
worker = Temporalio::Worker.new(
  client,
  'my-task-queue',
  workflows: [MyWorkflow],
  activities: [MyActivity],
  
  workflow_task_poller_behavior: Temporalio::Worker::PollerBehaviorAutoscaling.new,
  activity_task_poller_behavior: Temporalio::Worker::PollerBehaviorAutoscaling.new,
  nexus_task_poller_behavior: Temporalio::Worker::PollerBehaviorAutoscaling.new,
)

go
// Using the ResourceBasedTuner in worker options
tuner, err := resourcetuner.NewResourceBasedTuner(resourcetuner.ResourceBasedTunerOptions{
    TargetMem: 0.8,
    TargetCpu: 0.9,
})
if err != nil {
  return err
}
workerOptions := worker.Options{
    Tuner: tuner
}
// Combining different types
options := DefaultResourceControllerOptions()
options.MemTargetPercent = 0.8
options.CpuTargetPercent = 0.9
controller := NewResourceController(options)
wfSS, err := worker.NewFixedSizeSlotSupplier(10)
if err != nil {
  return err
}
actSS := &ResourceBasedSlotSupplier{controller: controller,
    options: defaultActivityResourceBasedSlotSupplierOptions()}
laSS := &ResourceBasedSlotSupplier{controller: controller,
    options: defaultActivityResourceBasedSlotSupplierOptions()}
nexusSS, err := worker.NewFixedSizeSlotSupplier(10)
if err != nil {
  return err
}
compositeTuner, err := worker.NewCompositeTuner(worker.CompositeTunerOptions{
    WorkflowSlotSupplier:      wfSS,
    ActivitySlotSupplier:      actSS,
    LocalActivitySlotSupplier: laSS,
    NexusSlotSupplier:         nexusSS,
})
if err != nil {
  return err
}
workerOptions := worker.Options{
    Tuner: compositeTuner
}
java
// Just resource based
WorkerOptions.newBuilder()
    .setWorkerTuner(
        ResourceBasedTuner.newBuilder()
            .setControllerOptions(
                ResourceBasedControllerOptions.newBuilder(0.8, 0.9).build())
            .build())
    .build())
// Combining different types
SlotSupplier<WorkflowSlotInfo> workflowTaskSlotSupplier = new FixedSizeSlotSupplier<>(10);
SlotSupplier<ActivitySlotInfo> activityTaskSlotSupplier =
    ResourceBasedSlotSupplier.createForActivity(
        resourceController, ResourceBasedTuner.DEFAULT_ACTIVITY_SLOT_OPTIONS);
SlotSupplier<LocalActivitySlotInfo> localActivitySlotSupplier =
    ResourceBasedSlotSupplier.createForLocalActivity(
        resourceController, ResourceBasedTuner.DEFAULT_ACTIVITY_SLOT_OPTIONS);
SlotSupplier<NexusSlotInfo> nexusSlotSupplier = new FixedSizeSlotSupplier<>(10);

WorkerOptions.newBuilder()
    .setWorkerTuner(
        new CompositeTuner(
            workflowTaskSlotSupplier,
            activityTaskSlotSupplier,
            localActivitySlotSupplier,
            nexusSlotSupplier))
    .build();
tsx
// Just resource based
const resourceBasedTunerOptions: ResourceBasedTunerOptions = {
  targetMemoryUsage: 0.8,
  targetCpuUsage: 0.9,
};
const workerOptions = {
  tuner: {
    tunerOptions: resourceBasedTunerOptions,
  },
};
// Combining different types
const resourceBasedTunerOptions: ResourceBasedTunerOptions = {
  targetMemoryUsage: 0.8,
  targetCpuUsage: 0.9,
};
const workerOptions = {
  tuner: {
    activityTaskSlotSupplier: {
      type: 'resource-based',
      tunerOptions: resourceBasedTunerOptions,
    },
    workflowTaskSlotSupplier: {
      type: 'fixed-size',
      numSlots: 10,
    },
    localActivityTaskSlotSupplier: {
      type: 'resource-based',
      tunerOptions: resourceBasedTunerOptions,
    },
  },
};
python

**Examples:**

Example 1 (unknown):
```unknown
Use the `loadClientConnectConfig` helper from `@temporalio/envconfig` to load the `staging` profile from the
configuration file and create a `NativeConnection` object as follows:
```

Example 2 (unknown):
```unknown
</TabItem>

<TabItem value="env-vars" label="Environment Variables">

Ensure you have set the necessary environment variables to connect to Temporal Cloud. For example:
```

Example 3 (unknown):
```unknown
After setting the environment variables, use the following code to create a `NativeConnection` object using the
`loadClientConnectConfig` helper from `@temporalio/envconfig`:
```

Example 4 (unknown):
```unknown
</TabItem>

<TabItem value="code" label="Code">

You can also provide connections options in your TypeScript code directly. To create an initial connection, provide the
connections to the ` NativeConnection.connect` method, and then pass the resulting `NativeConnection` object to
`Worker.create()` when creating the Worker:
```

---

## disabled = false

**URL:** llms-txt#disabled-=-false

client_cert_path = "/etc/temporal/certs/client.pem"
client_key_path  = "/etc/temporal/certs/client.key"

---

## Perform update-with-start and get update result

**URL:** llms-txt#perform-update-with-start-and-get-update-result

update_result = client.execute_with_start_workflow(
  MyWorkflow.my_update, 'update-input', start_workflow_operation:
)

---

## Do not need ConfigureAwait for workflows

**URL:** llms-txt#do-not-need-configureawait-for-workflows

dotnet_diagnostic.CA2007.severity = none

---

## Disable connections

**URL:** llms-txt#disable-connections

temporal operator cluster upsert --frontend_address="localhost:8233" --enable_connection false

---

## passing run ID. This could also just be a handle that is returned from

**URL:** llms-txt#passing-run-id.-this-could-also-just-be-a-handle-that-is-returned-from

---

## set up Cassandra schema

**URL:** llms-txt#set-up-cassandra-schema

setup_cassandra_schema() {
  #...
  # use valid schema for the version of the database you want to set up for Visibility
    VISIBILITY_SCHEMA_DIR=${TEMPORAL_HOME}/schema/cassandra/visibility/versioned
    if [[ ${SKIP_DB_CREATE} != true ]]; then
        temporal-cassandra-tool --ep "${CASSANDRA_SEEDS}" create -k "${VISIBILITY_KEYSPACE}" --rf "${CASSANDRA_REPLICATION_FACTOR}"
    fi
    temporal-cassandra-tool --ep "${CASSANDRA_SEEDS}" -k "${VISIBILITY_KEYSPACE}" setup-schema -v 0.0
    temporal-cassandra-tool --ep "${CASSANDRA_SEEDS}" -k "${VISIBILITY_KEYSPACE}" update-schema -d "${VISIBILITY_SCHEMA_DIR}"
  #...
}
#...

---

## HELP temporal_cloud_v1_approximate_backlog_count Approximate number of tasks in a task queue

**URL:** llms-txt#help-temporal_cloud_v1_approximate_backlog_count-approximate-number-of-tasks-in-a-task-queue

**Contents:**
  - List Metric Descriptors
- Managing High Cardinality
  - Cardinality Estimation
  - Filtering at Scrape Time

temporal_cloud_v1_approximate_backlog_count{temporal_namespace="production",temporal_task_queue="critical-queue",task_type="workflow", region="aws-us-west-2"} 15.0 1609459200000
shell
curl -H "Authorization: Bearer <API_KEY>" \
  "https://metrics.temporal.io/v1/descriptors"
json
{
  "meta": {
    "pagination": {
      "total": 35,
      "limit": 100,
      "offset": 0
    }
  },
  "descriptors": [
    {
      "name": "temporal_cloud_v1_workflow_success_count",
      "help": "The number of successful workflows per second",
      "dimensions": [
        "temporal_namespace",
        "temporal_workflow_type", 
        "temporal_task_queue",
        "region"
      ]
    }
  ]
}

Total series = Base metrics × Namespaces × Task queues × Workflow types
shell

**Examples:**

Example 1 (unknown):
```unknown
:::

#### Summary of Best Practices

* *Honor timestamps*: Set `honor_timestamps: true` in Prometheus  
* *Scrape interval*: Use 30 or 60 second intervals  
* *Timeout*: Set scrape timeout to 10 seconds for large responses  
* *Filtering*: Use query parameters to reduce response size

### List Metric Descriptors

`GET /v1/descriptors`

Lists all metric descriptors including metadata, data types, and available dimensions (a.k.a. labels).

#### Query Parameters

| Parameter | Type | Description |
| ----- | ----- | ----- |
| `limit` | integer | Page size (1-100, default: 100\) |
| `offset` | integer | Page offset |

:::info Example

Request:
```

Example 2 (unknown):
```unknown
Response:
```

Example 3 (unknown):
```unknown
:::

## Managing High Cardinality

:::caution

High-cardinality labels like `temporal_task_queue` and `temporal_workflow_type` can significantly increase metric volume and impact performance of your monitoring system. 

:::

### Cardinality Estimation

To estimate your metric cardinality and see if this is an issue:
```

Example 4 (unknown):
```unknown
Example:

* 6 workflow metrics with both labels  
* 10 namespaces  
* 50 task queues  
* 20 workflow types  
* \= 6 × 10 × 50 × 20 \= 60,000 time series

:::note

60,000 time series in the above example results in exceeding the 30,000 data points per scrape limit.

:::

If the cardinality is too high or you are hitting API limits, consider the following strategies.

### Filtering at Scrape Time

You can isolate only the metrics/namespaces you need.  For example, the following shows examples of filtering by modifying the `metrics_path.`
```

---

## For anything without the keep flag, replace with "unknown"

**URL:** llms-txt#for-anything-without-the-keep-flag,-replace-with-"unknown"

- source_labels: [__tmp_keep_original]
  regex: ''  # empty/missing value
  target_label: temporal_task_queue
  replacement: 'unknown'

---

## Plugins

**URL:** llms-txt#plugins

**Contents:**
- How to build a Plugin
  - Example Plugins
- What you can provide to users in a plugin
  - Built-in Activity
  - Workflow-friendly libraries
  - Built-in Workflows
  - Built-in Nexus Operations
  - Custom Data Converters
  - Interceptors
  - Special considerations for different languages

A **Plugin** is an abstraction that allows you to customize any aspect of your Temporal Worker setup, including registering Workflow and Activity definitions, modifying worker and client options, and more. Using plugins, you can build reusable open-source libraries or build add-ons for engineers at your company.

This guide will teach you how to create plugins and give platform engineers general guidance on using and managing Temporal's primitives.

Here are some common use cases for plugins:

- AI Agent SDKs
- Observability, tracing, or logging middleware
- Adding reliable built-in functionality such as LLM calls, messaging systems, and payments infrastructure
- Encryption or compliance middleware

## How to build a Plugin

The recommended way to start building plugins is with a `SimplePlugin`. This abstraction will tackle the vast majority of plugins people want to write.

For advanced use cases, you can extend the methods in lower-level classes that Simple Plugin is based on without re-implementing what you’ve done. See the [Advanced Topics section](#advanced-topics-for-plugins) for more information.

If you prefer to learn by getting hands-on with code, check out some existing plugins.

- Temporal's Python SDK ships with an [OpenAI Agents SDK](https://github.com/temporalio/sdk-python/tree/main/temporalio/contrib/openai_agents) plugin
- [Temporal client and Worker plugin for Pydantic AI](https://github.com/pydantic/pydantic-ai/blob/757d40932ebb8ef00f25cc469ff44e9b267b1aa3/pydantic_ai_slim/pydantic_ai/durable_exec/temporal/__init__.py#L83)

## What you can provide to users in a plugin

There are a number of features you can give your users with a plugin. Here's a short list of some of the things you can do.

- [Built-in Activities](#built-in-activity)
- [Workflow-friendly libraries](#workflow-friendly-libraries)
- [Built-in Workflows](#built-in-workflows)
- [Built-in Nexus Operations](#built-in-nexus-operations)
- [Custom Data Converters](#custom-data-converters)
- [Interceptors](#interceptors)

### Built-in Activity

You can provide built-in Activities in a Plugin for users to call from their Workflows. Check out the [Activities doc](/activities) for more detail on how these work.

You should refer to the [best practices for creating Activities](/activity-definition#best-practices-for-defining-activities) when you are making Activity plugins.

#### Timeouts and retry policies

Temporal's Activity retry mechanism gives applications the benefits of durable execution. See the [Activity retry policy explanation](/activity-definition#activity-retry-policy) for more details.

Here is an example with Python:

### Workflow-friendly libraries

You can provide a library with functionality for use within a Workflow if you'd like to abstract away some Temporal-specific details for your users. Your library will call elements you include in your Plugin such as Activities, Child Workflows, Signals, Updates, Queries, Nexus Operations, Interceptors, Data Converters, and any other code as long as it follows these requirements:

- It should be [deterministic](/workflow-definition#deterministic-constraints), running the same way every time it’s executed. Non-deterministic code should go in Activities or Nexus Operations.
- See [observability](/evaluate/development-production-features/observability) to avoid duplicating observation side effects when Workflows replay.
- Put other side effects inside of Activities or [Local Activities](/local-activity). This helps your Workflow handle being restarted, resumed, or executed in a different process from where it originally began without losing correctness or state consistency.
- See [testing your Plugin](#testing-your-plugin) to write tests that check for issues with side effects.
- It should run quickly since it may be replayed many times during a long Workflow execution. More expensive code should go in Activities or Nexus Operations.

A Plugin should allow a user to decompose their Workflows into Activities, as well as Child Workflows and Nexus Calls when needed. This gives users granular control through retries and timeouts, debuggability through the Temporal UI, operability with resets, pauses, and cancels, memoization for efficiency and resumability, and scalability using task queues and Workers.

Users use Workflows for:

- Orchestration and decision-making
- Interactivity via [message-passing](/evaluate/development-production-features/workflow-message-passing)
- Tracing and observability

#### Making changes to your library

Your users may want to keep their Workflows running across deployments of their Worker code. If their deployment includes a new version of your Plugin, changes to your Plugin could break Workflow code that started before the new version was deployed. This can be due to [non-deterministic behavior from code changes](/workflow-definition#non-deterministic-change) in your Plugin.

See [testing](#testing-your-plugin) to see how to test for this. And, if you make substantive changes, you need to use [patching](/patching).

#### Example of a Workflow library that uses a Plugin in Python

- [Implementation of the `OpenAIAgentsPlugin`](https://github.com/temporalio/sdk-python/tree/main/temporalio/contrib/openai_agents)
- [Example of replay testing](https://github.com/temporalio/sdk-python/blob/main/tests/contrib/openai_agents/test_openai_replay.py)

### Built-in Workflows

You can provide a built-in Workflow in a `SimplePlugin`. It’s callable as a Child Workflow or standalone. When you want to provide a piece of functionality that's more complex than an Activity, you can:

- Use a [Workflow Library](#workflow-friendly-libraries) that runs directly in the end user’s Workflow
- Add a Child Workflow

Consider adding a Child Workflow when one or more of these conditions applies:

- That child should outlive the parent.
- The Workflow Event History would otherwise [not scale](/workflow-execution/event#event-history-limits) in parent Workflows.
- When you want a separate Workflow ID for the child so that it can be operated independently of the parent's state (canceled, terminated, paused).

Any Workflow can be run as a standalone Workflow or as a Child Workflow, so registering a Child Workflow in a `SimplePlugin` is the same as registering any Workflow.

Here is an example with Python:

### Built-in Nexus Operations

Nexus calls are used from Workflows similar to Activities and you can check out some common [Nexus Use Cases](/nexus/use-cases). Like Activities, Nexus Call arguments and return values must be serializable.

Here's an example of how to register Nexus handlers in Workflows with Python:

### Custom Data Converters

A [custom Data Converter](/default-custom-data-converters#custom-data-converter) can alter data formats or provide compression or encryption.

Note that you can use an existing Data Converter such as, in Python, `PydanticPayloadConverter` in your Plugin.

Here's an example of how to add a Custom Data Converter to a Plugin with Python:

Interceptors are middleware that can run before and after various calls such as Activities, Workflows, and Signals. You can [learn more about interceptors](/develop/python/interceptors) for the details of implementing them. They're used to:

- Create side effects such as logging and tracing.
- Modify arguments, such as adding headers for authorization or tracing propagation.

Here's an example of how to add one to a Plugin with Python:

### Special considerations for different languages

Each of the SDKs has nuances you should be aware of so you can account for it in your code.

For example, you can choose to [run your Workflows in a sandbox in Python](/develop/python/python-sdk-sandbox). This lets you run Workflow code in a sandbox environment to help prevent non-determinism errors in your application. To work for users who use sandboxing, your Plugin should specify the Workflow runner that it uses.

Here's an example of how to explicitly define the Workflow runner for your Plugin with Python:

## Testing your Plugin {#testing-your-plugin}

To test your Plugin, you'll write a normal Temporal Workflow tests, having included the plugin in your Client.

Two special concerns are versioning tests, for when you're making changes to your plugin, and testing unwanted side effects.

When you make changes to your plugin after it has already shipped to users, it's recommended that you set up [replay testing](/develop/python/testing-suite#replay) on each important change to make sure that you’re not causing non-determinism errors for your users.

### Side effects tests

Your Plugin should cater to Workflows resuming in different processes than the ones they started on and then replaying from the beginning, which can happen, for example, after an intermittent failure.

You can ensure you're not depending on local side effects by turning Workflow caching off, which will mean that the Workflow replays from the top each time it progresses. Here's an example with Python:

Check for duplicate side effects or other types of failures.

It's harder to test against side effects to global variables, so this practice is best avoided entirely.

## Advanced Topics for Plugins

If you go deeper into `SimplePlugin`, you'll see it aggregates a pair of raw Plugin classes that you can use for a higher level of flexibility: a Worker Plugin and a client Plugin.

- Worker Plugins contain functionality that runs inside your users’ Workflows.
- Client Plugins contain functionality that runs when Workflows are created and return results.

If your Plugin implements both of them, registering it in the client will also register it in Workers created with that client.

Client Plugins are provided to the Temporal client on creation. They can change client configurations and service client configurations. `ClientConfig` contains settings like client Interceptors and DataConverters. `ConnectConfig` configures the actual network connections to the local or cloud Temporal server with values like an API key. This is the basic implementation of a client Plugin using Python:

The primary use case for integrations so far is setting a `DataConverter`, like in the [Data Converter example](#custom-data-converters).

Worker Plugins are provided at Worker creation and have more capabilities and corresponding implementation than client Plugins. They can change Worker configurations, run code during the Worker lifetime, and manage the Replayer in a similar way. You can learn more about the [Replayer](#replayer) in a later section.

Similar to `configure_client` above, you implement `configure_worker` and `configure_replayer` to change any necessary configurations. In addition, `run_worker` allows you to execute code before and after the Worker runs. This can be used to set up resources or globals for use during the Worker execution. `run_replayer` does the same for the Replayer, but keep in mind that the Replayer has a more complex return type. This is a basic implementation of a Worker plugin using Python:

The Replayer allows Workflow authors to validate that their Workflows will work after changes to either the Workflow or a library they depend on. It’s normally used in test runs or when testing Workers before they roll out in production.

The Replayer runs on a Workflow History created by a previous Workflow run. Suppose something in the Workflow or underlying code has changed in a way which could potentially cause a non-determinism error. In that case, the Replayer will notice the change in the way it runs compared to the history provided.

The Replayer is typically configured identically to the Worker and client. Ff you’re using `SimplePlugin`, this is already handled for you.

If you need to do something custom for the Replayer, you can configure it directly. Here's an example of how to do that with Python:

## Asynchronous Activity Completion - Python SDK

**How to Asynchronously complete an Activity using the Temporal Python SDK.**

[Asynchronous Activity Completion](/activity-execution#asynchronous-activity-completion) enables the Activity Function to return without the Activity Execution completing.

There are three steps to follow:

1. The Activity provides the external system with identifying information needed to complete the Activity Execution.
   Identifying information can be a [Task Token](/activity-execution#task-token), or a combination of Namespace, Workflow Id, and Activity Id.
2. The Activity Function completes in a way that identifies it as waiting to be completed by an external system.
3. The Temporal Client is used to Heartbeat and complete the Activity.

To mark an Activity as completing asynchronously, do the following inside the Activity.

**Examples:**

Example 1 (python):
```python
@activity.defn
async def some_activity() -> None:
  return None

plugin = SimplePlugin(
  activities = [some_activity]
)
```

Example 2 (python):
```python
@workflow.defn
class HelloWorkflow:
  @workflow.run
  async def run(self, name: str) -> str:
    return f"Hello, {name}!"

plugin = SimplePlugin(
  workflows = [HelloWorkflow]
)
 
...

client = await Client.connect(
  "localhost:7233",
  plugins=[
    plugin,
  ],
)
async with Worker(
  client,
  task_queue="task-queue",
):
  client.execute_workflow(
      HelloWorkflow.run,
      "Tim",
      task_queue=worker.task_queue,
    )
```

Example 3 (python):
```python
@nexusrpc.service
class WeatherService:
  get_weather_nexus_operation: nexusrpc.Operation[WeatherInput, Weather]

@nexusrpc.handler.service_handler(service=WeatherService)
class WeatherServiceHandler:
  @nexusrpc.handler.sync_operation
  async def get_weather_nexus_operation(
    self, ctx: nexusrpc.handler.StartOperationContext, input: WeatherInput
  ) -> Weather:
    return Weather(
      city=input.city, temperature_range="14-20C", conditions="Sunny with wind."
    )

plugin = SimplePlugin(
  nexus_service_handlers = [WeatherServiceHandler()]
)
```

Example 4 (python):
```python
def add_converter(converter: Optional[DataConverter]) -> DataConverter
  if converter is None or converter == temporalio.converter.DataConverter.default
    return pydantic_data_converter
  # Should consider interactions with other plugins, 
  # as this will override the data converter.
  # This may mean failing, warning, or something else
  return converter

plugin = SimplePlugin(
  data_converter = add_converter
)
```

---

## Production profile for Temporal Cloud

**URL:** llms-txt#production-profile-for-temporal-cloud

[profile.prod]
address = "your-namespace.a1b2c.tmprl.cloud:7233"
namespace = "your-namespace"
api_key = "your-api-key-here"

---

## cluster B

**URL:** llms-txt#cluster-b

clusterMetadata:
  enableGlobalNamespace: true
  failoverVersionIncrement: 100
  masterClusterName: "clusterB"
  currentClusterName: "clusterB"
  clusterInformation:
    clusterB:
      enabled: true
      initialFailoverVersion: 2
      rpcAddress: "127.0.0.1:8233"
shell

**Examples:**

Example 1 (unknown):
```unknown
Then you can use the Temporal CLI tool to add cluster connections. All operations should be executed in both Clusters.

{/* tctl -address 127.0.0.1:7233 admin cluster upsert-remote-cluster --frontend_address "localhost:8233" */}

{/* tctl -address 127.0.0.1:8233 admin cluster upsert-remote-cluster --frontend_address "localhost:7233" */}

{/* tctl -address 127.0.0.1:7233 admin cluster upsert-remote-cluster --frontend_address "localhost:8233" --enable_connection false
tctl -address 127.0.0.1:8233 admin cluster upsert-remote-cluster --frontend_address "localhost:7233" --enable_connection false */}

{/* tctl -address 127.0.0.1:7233 admin cluster remove-remote-cluster --cluster "clusterB"
tctl -address 127.0.0.1:8233 admin cluster remove-remote-cluster --cluster "clusterA" */}

{/* THIS MUST BE CHECKED FOR ACCURACY */}
```

---

## be provided that will shutdown when the block completes

**URL:** llms-txt#be-provided-that-will-shutdown-when-the-block-completes

**Contents:**
- Set a Dynamic Workflow {#set-a-dynamic-workflow}
- Set a Dynamic Activity {#set-a-dynamic-activity}
- Debugging - Ruby SDK
- Debugging {#debug}
- Debug in a development environment {#debug-in-a-development-environment}
- Debug in a production environment {#debug-in-a-production-environment}
- Durable Timers - Ruby SDK

worker.run(shutdown_signals: ['SIGINT'])
ruby
class MyDynamicWorkflow < Temporalio::Workflow::Definition
  # Make this the dynamic workflow and accept raw args
  workflow_dynamic
  workflow_raw_args

def execute(*raw_args)
    # Require a single arg for our workflow
    raise Temporalio::Error::ApplicationError, 'One arg expected' unless raw_args.size == 1

# Use payload converter to convert it
    name = Temporalio::Workflow.payload_converter.from_payload(raw_args.first.payload)
    Temporalio::Workflow.execute_activity(
      MyActivity,
      { greeting: 'Hello', name: },
      start_to_close_timeout: 100
    )
  end
end
ruby
class MyDynamicActivity < Temporalio::Activity::Definition
  # Make this the dynamic activity and accept raw args
  activity_dynamic
  activity_raw_args

def execute(*raw_args)
    raise Temporalio::Error::ApplicationError, 'One arg expected' unless raw_args.size == 1

# Use payload converter to convert it
    input = Temporalio::Activity::Context.current.payload_converter.from_payload(raw_args.first.payload)
    "#{input['greeting']}, #{input['name']}!"
  end
end
ruby

**Examples:**

Example 1 (unknown):
```unknown
To run multiple workers, `Temporalio::Worker.run_all` may be used instead.

All Workers listening to the same Task Queue name must be registered to handle the exact same Workflows Types and Activity Types.

If a Worker polls a Task for a Workflow Type or Activity Type it does not know about, it fails that Task.
However, the failure of the Task does not cause the associated Workflow Execution to fail.

## Set a Dynamic Workflow {#set-a-dynamic-workflow}

A Dynamic Workflow in Temporal is a Workflow that is invoked dynamically at runtime if no other Workflow with the same name is registered.
A Workflow can be made dynamic by invoking `workflow_dynamic` class method at the top of the definition.
You must register the Workflow with the Worker before it can be invoked.
Only one Dynamic Workflow can be present on a Worker.

Often, dynamic is used in conjunction with `workflow_raw_args` which does not convert arguments but instead passes them
through as a splatted array of `Temporalio::Converters::RawValue` instances.
```

Example 2 (unknown):
```unknown
## Set a Dynamic Activity {#set-a-dynamic-activity}

A Dynamic Activity in Temporal is an Activity that is invoked dynamically at runtime if no other Activity with the same name is registered.
An Activity can be made dynamic by invoking `activity_dynamic` class method at the top of the definition.
You must register the Activity with the Worker before it can be invoked.
Only one Dynamic Activity can be present on a Worker.

Often, dynamic is used in conjunction with `activity_raw_args` which does not convert arguments but instead passes them
through as a splatted array of `Temporalio::Converters::RawValue` instances.
```

Example 3 (unknown):
```unknown
---

## Debugging - Ruby SDK

## Debugging {#debug}

This page shows how to do the following:

- [Debug in a development environment](#debug-in-a-development-environment)
- [Debug in a development production](#debug-in-a-development-environment)

## Debug in a development environment {#debug-in-a-development-environment}

In developing Workflows, you can use the normal development tools of logging and a debugger to see what’s happening in your Workflow.

In addition to the normal development tools of logging and a debugger, you can also see what’s happening in your Workflow by using the [Web UI](/web-ui) or [Temporal CLI](/cli).
The Web UI provides insight into your Workflows, making it easier to identify issues and monitor the state of your Workflows in real time.

## Debug in a production environment {#debug-in-a-production-environment}

For production Workflows, debugging options include:

- [Web UI](/web-ui)
- [Temporal CLI](/cli)
- [Replay](/develop/ruby/testing-suite#replay-test)
- [Tracing](/develop/ruby/observability#tracing)
- [Logging](/develop/ruby/observability#logging)

You can analyze Worker performance using:

- [Metrics](/develop/ruby/observability#metrics)
- [Worker performance guide](/develop/worker-performance)

To monitor Server performance:

- Use [Cloud metrics](/cloud/metrics/) if you're on Temporal Cloud
- Or [self-hosted Server metrics](/self-hosted-guide/production-checklist#scaling-and-metrics) if running your own deployment

---

## Durable Timers - Ruby SDK

This page describes how to set a Durable Timer using the Temporal Ruby SDK.

A [Durable Timer](/workflow-execution/timers-delays) is used to pause the execution of a Workflow for a specified duration.
A Workflow can sleep for days or even months.
Timers are persisted, so even if your Worker or Temporal Service is down when the time period completes, as soon as your Worker and Temporal Service are back up, the Durable Timer call will resolve and your code will continue executing.

Sleeping is a resource-light operation: it does not tie up the process, and you can run millions of Timers off a single Worker.

To add a Timer in a Workflow, use `Temporalio::Workflow.sleep`.
_Technically_ `Kernel#sleep` works, but the workflow form allows one to set a summary to view in the UI.
```

---

## Install Temporal SDK in each project

**URL:** llms-txt#install-temporal-sdk-in-each-project

**Contents:**
- Run Hello World: Test Your Installation
  - 1. Create the Activity and Workflow
  - 2. Create the Worker
  - 3. Execute the Workflow
  - Verify Success
- Temporal Client - .NET SDK
- Connect to development Temporal Service {#connect-to-development-service}

dotnet add Workflow/Workflow.csproj package Temporalio
dotnet add Worker/Worker.csproj package Temporalio
dotnet add Client/Client.csproj package Temporalio`
}
      </CodeSnippet>

Build the solution:
      
      <CodeSnippet language="bash">{`dotnet build`}</CodeSnippet>
    </>
  }>
    ## Install the Temporal .NET SDK

Create a solution and the three projects used in this guide: `Workflow` (class library), `Worker` (console), and `Client` (console). Add them to the solution.

Tip: You can also centralize the `Temporalio` package for all projects using `Directory.Packages.props` and `Directory.Build.props` at the solution root.
  </SetupStep>

<SetupStep code={
    <>
      <Tabs>
        <TabItem value="macos" label="macOS" default>
          Install the Temporal CLI using Homebrew:
          <CodeSnippet language="bash">{`brew install temporal`}</CodeSnippet>
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
          <CodeSnippet language="bash">{`sudo mv temporal /usr/local/bin`}</CodeSnippet>
        </TabItem>
      </Tabs>
    </>
  }>
    ## Install Temporal CLI and start the development server

The fastest way to get a development version of the Temporal Service running on your local machine is to use [Temporal CLI](https://docs.temporal.io/cli).

Choose your operating system to install Temporal CLI:
  </SetupStep>

<SetupStep code={
    <>
      After installing, open a new Terminal window and start the development server:
      <CodeSnippet language="bash">{`temporal server start-dev`}</CodeSnippet>

Change the Web UI port
        
          The Temporal Web UI may be on a different port in some examples or tutorials.
          To change the <code>--ui-port</code> option when starting the server:
        
        <CodeSnippet language="bash">{`temporal server start-dev --ui-port 8080`}</CodeSnippet>
        
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

- Your .NET SDK installation is working
- Your local Temporal Service is running
- You can successfully create and execute Workflows and Activities
- The communication between components is functioning correctly

<details>
  <summary>Tip: Example Directory Structure</summary>

### 1. Create the Activity and Workflow

#### Create an Activity file (MyActivities.cs) in the Workflow project:

An Activity is a normal function or method that executes a single, well-defined action (either short or long running), which often involve interacting with the outside world, such as sending emails, making network requests, writing to a database, or calling an API, which are prone to failure.
If an Activity fails, Temporal automatically retries it based on your configuration.

#### Create a Workflow file (SayHelloWorkflow.cs) in the Workflow project:

Workflows orchestrate Activities and contain the application logic.
Temporal Workflows are resilient.
They can run and keep running for years, even if the underlying infrastructure fails.
If the application itself crashes, Temporal will automatically recreate its pre-failure state so it can continue right where it left off.

### 2. Create the Worker

With your Activity and Workflow defined, you need a Worker to execute them.

#### Create a Worker file (Program.cs) in the Worker project:

Keep this terminal running - you should see `Running worker` displayed.

A Worker polls a Task Queue, that you configure it to poll, looking for work to do. 
Once the Worker dequeues the Workflow or Activity task from the Task Queue, it then executes that task.

Workers are a crucial part of your Temporal application as they're what actually execute the tasks defined in your Workflows and Activities.
For more information on Workers, see [Understanding Temporal](/evaluate/understanding-temporal#workers) and a [deep dive into Workers](/workers).

### 3. Execute the Workflow

Now that your Worker is running, it's time to start a Workflow Execution.
This final step will validate that everything is working correctly.

#### Create a Client file (Program.cs) in the Client project:

While the Worker is still running, run the Workflow:

If everything is working correctly, you should see:

- Worker processing the workflow and activity
- Output: `Workflow result: Hello Temporal`
- Workflow Execution details in the [Temporal Web UI](http://localhost:8233)

<CallToAction href="https://learn.temporal.io/getting_started/dotnet/first_program_in_dotnet/">
  Next: Run your first Temporal Application
  Create a basic Workflow and run it with the Temporal .NET SDK
</CallToAction>

## Temporal Client - .NET SDK

A [Temporal Client](/encyclopedia/temporal-sdks#temporal-client) enables you to communicate with the Temporal Service.
Communication with a Temporal Service lets you perform actions such as starting Workflow Executions, sending Signals and
Queries to Workflow Executions, getting Workflow results, and more.

This page shows you how to do the following using the .NET SDK with the Temporal Client:

- [Connect to a local development Temporal Service](#connect-to-development-service)
- [Connect to Temporal Cloud](#connect-to-temporal-cloud)
- [Start a Workflow Execution](#start-workflow)
- [Get Workflow results](#get-workflow-results)

A Temporal Client cannot be initialized and used inside a Workflow. However, it is acceptable and common to use a
Temporal Client inside an Activity to communicate with a Temporal Service.

## Connect to development Temporal Service {#connect-to-development-service}

Use
[`TemporalClient.ConnectAsync`](https://dotnet.temporal.io/api/Temporalio.Client.TemporalClient.html#Temporalio_Client_TemporalClient_ConnectAsync_Temporalio_Client_TemporalClientConnectOptions_)
to create a client. Connection options include the Temporal Server address, Namespace, and (optionally) TLS
configuration. You can provide these options directly in code, or load them from **environment variables** and/or a
**TOML configuration file** using the `Temporalio.Client.EnvConfig` helpers. We recommend environment variables or a
configuration file for secure, repeatable configuration.

When you’re running a Temporal Service locally (such as with the
[Temporal CLI dev server](https://docs.temporal.io/cli/server#start-dev)), the required options are minimal. If you
don't specify a host/port, most connections default to `127.0.0.1:7233` and the `default` Namespace.

<Tabs groupId="connect-options-dotnet" defaultValue="config-file" >

<TabItem value="config-file" label="Configuration File">

You can use a TOML configuration file to set connection options for the Temporal Client. The configuration file lets you
configure multiple profiles, each with its own set of connection options. You can then specify which profile to use when
creating the Temporal Client. You can use the environment variable `TEMPORAL_CONFIG_FILE` to specify the location of the
TOML file or provide the path to the file directly in code. If you don't provide the configuration file path, the SDK
looks for it at the path `~/.config/temporalio/temporal.toml` or the equivalent on your OS. Refer to
[Environment Configuration](../environment-configuration.mdx#configuration-methods) for more details about configuration
files and profiles.

The connection options set in configuration files have lower precedence than environment variables. This means that if
you set the same option in both the configuration file and as an environment variable, the environment variable value
overrides the option set in the configuration file.

For example, the following TOML configuration file defines two profiles: `default` and `prod`. Each profile has its own
set of connection options.

```toml title="config.toml"

**Examples:**

Example 1 (text):
```text
TemporalioHelloWorld/
├── Client/
│   ├── Client.csproj
│   └── Program.cs              # Starts a workflow
├── Worker/
│   ├── Worker.csproj
│   └── Program.cs              # Runs a worker
├── Workflow/
│   ├── Workflow.csproj
│   ├── MyActivities.cs         # Activity definition
│   └── SayHelloWorkflow.cs     # Workflow definition
└── TemporalioHelloWorld.sln
```

Example 2 (csharp):
```csharp
namespace MyNamespace;

using Temporalio.Activities;

public class MyActivities
{
    // Activities can be async and/or static too! We just demonstrate instance
    // methods since many will use them that way.
    [Activity]
    public string SayHello(string name) => $"Hello, {name}!";
}
```

Example 3 (csharp):
```csharp
namespace MyNamespace;

using Temporalio.Workflows;

[Workflow]
public class SayHelloWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(string name)
    {
        // This workflow just runs a simple activity to completion.
        // StartActivityAsync could be used to just start and there are many
        // other things that you can do inside a workflow.
        return await Workflow.ExecuteActivityAsync(
            // This is a lambda expression where the instance is typed. If this
            // were static, you wouldn't need a parameter.
            (MyActivities act) => act.SayHello(name),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) }
        );
    }
}
```

Example 4 (csharp):
```csharp
using MyNamespace;
using Temporalio.Client;
using Temporalio.Worker;

// Create a client to localhost on "default" namespace
var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

// Cancellation token to shutdown worker on ctrl+c
using var tokenSource = new CancellationTokenSource();
Console.CancelKeyPress += (_, eventArgs) =>
{
    tokenSource.Cancel();
    eventArgs.Cancel = true;
};

// Create an activity instance since we have instance activities. If we had
// all static activities, we could just reference those directly.
var activities = new MyActivities();

// Create worker with the activity and workflow registered
using var worker = new TemporalWorker(
    client,
    new TemporalWorkerOptions("my-task-queue")
        .AddActivity(activities.SayHello)
        .AddWorkflow<SayHelloWorkflow>()
);

// Run worker until cancelled
Console.WriteLine("Running worker");
try
{
    await worker.ExecuteAsync(tokenSource.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Worker cancelled");
}
```

---

## UI is now accessible from host at http://localhost:8233/

**URL:** llms-txt#ui-is-now-accessible-from-host-at-http://localhost:8233/

**Contents:**
  - What the local server provides
  - Access the Web UI
- Getting CLI help
- Temporal CLI task-queue command reference
- config
  - get
  - set
- describe
- get-build-id-reachability
- get-build-ids

temporal <command> <subcommand> --help

temporal task-queue config [command] [options]

temporal task-queue config get \
    --task-queue YourTaskQueue \
    --task-queue-type activity

temporal task-queue config set \
    --task-queue YourTaskQueue \
    --task-queue-type activity \
    --namespace YourNamespace \
    --queue-rps-limit <requests_per_second:float> \
    --queue-rps-limit-reason <reason_string> \
    --fairness-key-rps-limit-default <requests_per_second:float> \
    --fairness-key-rps-limit-reason <reason_string>

temporal task-queue describe \
  --task-queue YourTaskQueue

temporal task-queue describe \
    --task-queue YourTaskQueue \
    --task-queue-type "activity"

temporal task-queue describe \
    --task-queue YourTaskQueue \
    --select-build-id "YourBuildId" \
    --report-reachability

+-----------------------------------------------------------------------------+
| CAUTION: This command is deprecated and will be removed in a later release. |
+-----------------------------------------------------------------------------+

temporal task-queue get-build-id-reachability \
    --task-queue YourTaskQueue \
    --build-id "YourBuildId"

+-----------------------------------------------------------------------------+
| CAUTION: This command is deprecated and will be removed in a later release. |
+-----------------------------------------------------------------------------+

temporal task-queue get-build-ids \
    --task-queue YourTaskQueue

temporal task-queue list-partition \
    --task-queue YourTaskQueue

+-----------------------------------------------------------------------------+
| CAUTION: This command is deprecated and will be removed in a later release. |
+-----------------------------------------------------------------------------+

temporal task-queue update-build-ids [subcommands] [options] \
    --task-queue YourTaskQueue

temporal task-queue update-build-ids add-new-compatible \
    --task-queue YourTaskQueue \
    --existing-compatible-build-id "YourExistingBuildId" \
    --build-id "YourNewBuildId"

+-----------------------------------------------------------------------------+
| CAUTION: This command is deprecated and will be removed in a later release. |
+-----------------------------------------------------------------------------+

temporal task-queue update-build-ids add-new-default \
    --task-queue YourTaskQueue \
    --build-id "YourNewBuildId"

+------------------------------------------------------------------------+
| NOTICE: This command is limited to Namespaces that support Worker      |
| versioning. Worker versioning is experimental. Versioning commands are |
| subject to change.                                                     |
+------------------------------------------------------------------------+

+-----------------------------------------------------------------------------+
| CAUTION: This command is deprecated and will be removed in a later release. |
+-----------------------------------------------------------------------------+

temporal task-queue update-build-ids promote-id-in-set \
    --task-queue YourTaskQueue \
    --build-id "YourBuildId"

+------------------------------------------------------------------------+
| NOTICE: This command is limited to Namespaces that support Worker      |
| versioning. Worker versioning is experimental. Versioning commands are |
| subject to change.                                                     |
+------------------------------------------------------------------------+

+-----------------------------------------------------------------------------+
| CAUTION: This command is deprecated and will be removed in a later release. |
+-----------------------------------------------------------------------------+

temporal task-queue update-build-ids promote-set \
    --task-queue YourTaskQueue \
    --build-id "YourBuildId"

+------------------------------------------------------------------------+
| NOTICE: This command is limited to Namespaces that support Worker      |
| versioning. Worker versioning is experimental. Versioning commands are |
| subject to change.                                                     |
+------------------------------------------------------------------------+

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning [subcommands] [options] \
    --task-queue YourTaskQueue

temporal task-queue versioning add-redirect-rule \
    --task-queue YourTaskQueue \
    --source-build-id "YourSourceBuildID" \
    --target-build-id "YourTargetBuildID"

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning commit-build-id \
    --task-queue YourTaskQueue
    --build-id "YourBuildId"

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning delete-assignment-rule \
    --task-queue YourTaskQueue \
    --rule-index YourIntegerRuleIndex

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning delete-redirect-rule \
    --task-queue YourTaskQueue \
    --source-build-id "YourBuildId"

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning get-rules \
    --task-queue YourTaskQueue

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning insert-assignment-rule \
    --task-queue YourTaskQueue \
    --build-id "YourBuildId"

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning replace-assignment-rule \
    --task-queue YourTaskQueue \
    --rule-index AnIntegerIndex \
    --build-id "YourBuildId"

temporal task-queue versioning replace-assignment-rule \
    --task-queue YourTaskQueue \
    --rule-index AnIntegerIndex \
    --build-id "YourBuildId" \
    --percentage AnIntegerPercent

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

temporal task-queue versioning replace-redirect-rule \
    --task-queue YourTaskQueue \
    --source-build-id YourSourceBuildId \
    --target-build-id YourNewTargetBuildId

+---------------------------------------------------------------------+
| CAUTION: This API has been deprecated by Worker Deployment.         |
+---------------------------------------------------------------------+

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment [command] [options]

temporal worker deployment list

temporal worker deployment set-current-version \
         --deployment-name YourDeploymentName --build-id YourBuildID

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment delete [options]

temporal worker deployment delete \
    --name YourDeploymentName \
    --identity YourIdentity

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment delete-version [options]

temporal worker deployment delete-version \
    --deployment-name YourDeploymentName --build-id YourBuildID \
    --skip-drainage

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment describe [options]

temporal worker deployment describe \
    --name YourDeploymentName

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment describe-version [options]

temporal worker deployment describe-version \
    --deployment-name YourDeploymentName --build-id YourBuildID

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment list [options]

temporal worker deployment list \
    --namespace YourDeploymentNamespace

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment manager-identity [command] [options]

temporal worker deployment describe \
    --deployment-name YourDeploymentName

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment manager-identity set [options]

temporal worker deployment manager-identity set \
   --deployment-name DeploymentName \
   --self \
   --identity YourUserIdentity # optional, populated by CLI if not provided

temporal worker deployment manager-identity set \
   --deployment-name DeploymentName \
   --manager-identity NewManagerIdentity

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment manager-identity unset [options]

temporal worker deployment manager-identity unset \
   --deployment-name YourDeploymentName

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment set-current-version [options]

temporal worker deployment set-current-version \
    --deployment-name YourDeploymentName --build-id YourBuildID

temporal worker deployment set-current-version \
    --deployment-name YourDeploymentName --unversioned

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment set-ramping-version [options]

temporal worker deployment set-ramping-version \
    --deployment-name YourDeploymentName --build-id YourBuildID \
    --percentage 10.0

temporal worker deployment set-ramping-version \
    --deployment-name YourDeploymentName --build-id YourBuildID \
    --delete

+---------------------------------------------------------------------+
| CAUTION: Worker Deployment is experimental. Deployment commands are |
| subject to change.                                                  |
+---------------------------------------------------------------------+

temporal worker deployment update-metadata-version \
    --deployment-name YourDeploymentName --build-id YourBuildID \
    --metadata bar=1 \
    --metadata foo=true

temporal worker deployment describe-version \
    --deployment-name YourDeploymentName --build-id YourBuildID \

temporal worker describe --namespace YourNamespace --worker-instance-key YourKey

temporal worker list --namespace YourNamespace --query 'taskQueue="YourTaskQueue"'

temporal workflow cancel \
    --workflow-id YourWorkflowId

temporal workflow cancel \
    --query YourQuery

temporal workflow count \
    --query YourQuery

temporal workflow delete \
    --workflow-id YourWorkflowId

temporal workflow describe \
    --workflow-id YourWorkflowId

temporal workflow describe \
    --workflow-id YourWorkflowId \
    --reset-points true

temporal workflow execute
    --workflow-id YourWorkflowId \
    --type YourWorkflow \
    --task-queue YourTaskQueue \
    --input '{"some-key": "some-value"}'

temporal workflow execute-update-with-start \
  --update-name YourUpdate \
  --update-input '{"update-key": "update-value"}' \
  --workflow-id YourWorkflowId \
  --type YourWorkflowType \
  --task-queue YourTaskQueue \
  --id-conflict-policy Fail \
  --input '{"wf-key": "wf-value"}'

temporal workflow fix-history-json \
    --source /path/to/original.json \
    --target /path/to/reserialized.json

temporal workflow list \
    --query YourQuery`

temporal workflow list \
    --archived

temporal workflow metadata \
    --workflow-id YourWorkflowId

temporal workflow query \
    --workflow-id YourWorkflowId
    --type YourQueryType
    --input '{"YourInputKey": "YourInputValue"}'

temporal workflow reset \
    --workflow-id YourWorkflowId \
    --event-id YourLastEvent

temporal workflow reset \
    --workflow-id YourWorkflowId \
    --type LastContinuedAsNew

temporal workflow result \
    --workflow-id YourWorkflowId

temporal workflow show \
    --workflow-id YourWorkflowId
    --output json

temporal workflow signal \
    --workflow-id YourWorkflowId \
    --name YourSignal \
    --input '{"YourInputKey": "YourInputValue"}'

temporal workflow signal-with-start \
  --signal-name YourSignal \
  --signal-input '{"some-key": "some-value"}' \
  --workflow-id YourWorkflowId \
  --type YourWorkflowType \
  --task-queue YourTaskQueue \
  --input '{"some-key": "some-value"}'

temporal workflow stack \
    --workflow-id YourWorkflowId

temporal workflow start \
    --workflow-id YourWorkflowId \
    --type YourWorkflow \
    --task-queue YourTaskQueue \
    --input '{"some-key": "some-value"}'

temporal workflow start-update-with-start \
  --update-name YourUpdate \
  --update-input '{"update-key": "update-value"}' \
  --update-wait-for-stage accepted \
  --workflow-id YourWorkflowId \
  --type YourWorkflowType \
  --task-queue YourTaskQueue \
  --id-conflict-policy Fail \
  --input '{"wf-key": "wf-value"}'

temporal workflow terminate \
    --reason YourReasonForTermination \
    --workflow-id YourWorkflowId

temporal workflow terminate \
    --query YourQuery \
    --reason YourReasonForTermination

temporal workflow trace \
    --workflow-id YourWorkflowId

temporal workflow update describe \
    --workflow-id YourWorkflowId \
    --update-id YourUpdateId

temporal workflow update execute \
    --workflow-id YourWorkflowId \
    --name YourUpdate \
    --input '{"some-key": "some-value"}'

temporal workflow update result \
    --workflow-id YourWorkflowId \
    --update-id YourUpdateId

temporal workflow update start \
    --workflow-id YourWorkflowId \
    --name YourUpdate \
    --input '{"some-key": "some-value"}'
    --wait-for-stage accepted

+---------------------------------------------------------------------+
| CAUTION: Worflow update-options is experimental. Workflow Execution |
| properties are subject to change.                                   |
+---------------------------------------------------------------------+

temporal workflow update-options [options]

temporal workflow update-options \
    --workflow-id YourWorkflowId \
    --versioning-override-behavior auto_upgrade

temporal workflow update-options \
    --workflow-id YourWorkflowId \
    --versioning-override-behavior pinned \
    --versioning-override-deployment-name YourDeploymentName \
    --versioning-override-build-id YourDeploymentBuildId

temporal workflow update-options \
    --workflow-id YourWorkflowId \
    --versioning-override-behavior unspecified
csharp
// Capture token for later completion
capturedToken = ActivityExecutionContext.Current.Info.TaskToken;

// Throw special exception that says an activity will be completed somewhere else
throw new CompleteAsyncException();
csharp
var handle = myClient.GetAsyncActivityHandle(capturedToken);
csharp
await handle.CompleteAsync("Completion value.");
csharp
using Temporalio.Activities;
using Temporalio.Api.Enums.V1;
using Temporalio.Exceptions;

public class MyActivities
{
    [Activity]
    public async Task<string> MyActivityAsync()
    {
        try
        {
            return await CallExternalServiceAsync();
        }
        catch (Exception e)
        {
            // Mark this error as benign since it's expected
            throw new ApplicationFailureException(
                "Service is down",
                inner: e,
                category: ApplicationErrorCategory.Benign);
        }
    }
}
csharp
[WorkflowRun]
public async Task RunAsync()
{
    try
    {
        // Whether this workflow waits on the activity to handle the cancellation or not is
        // dependent upon the CancellationType option. We leave the default here which sends the
        // cancellation but does not wait on it to be handled.
        await Workflow.ExecuteActivityAsync(
            (MyActivities a) => a.MyNormalActivity(),
            new() { ScheduleToCloseTimeout = TimeSpan.FromMinutes(5) });
    }
    catch (Exception e) when (TemporalException.IsCanceledException(e))
    {
        // The "when" clause above is because we only want to apply the logic to cancellation, but
        // this kind of cleanup could be done on any/all exceptions too.
        Workflow.Logger.LogError(e, "Cancellation occurred, performing cleanup");

// Call cleanup activity. If this throws, it will swallow the original exception which we
        // are ok with here. This could be changed to just log a failure and let the original
        // cancellation continue. We use a different cancellation token since the default one on
        // Workflow.CancellationToken is now marked cancelled.
        using var detachedCancelSource = new CancellationTokenSource();
        await Workflow.ExecuteActivityAsync(
            (MyActivities a) => a.MyCancellationCleanupActivity(),
            new()
            {
                ScheduleToCloseTimeout = TimeSpan.FromMinutes(5),
                CancellationToken = detachedCancelSource.Token;
            });

// Rethrow the cancellation
        throw;
    }
}
csharp
[Activity]
public async Task MyActivityAsync()
{
    // This is a naive loop simulating work, but similar heartbeat/cancellation logic applies to
    // other scenarios as well
    while (true)
    {
        // Send heartbeat
        ActivityExecutionContext.Current.Heartbeat();

// Do some work, passing the cancellation token
        await Task.Delay(1000, ActivityExecutionContext.Current.CancellationToken);
    }
}
csharp
// Get a workflow handle by its workflow ID. This could be made specific to a run by passing run ID.
// This could also just be a handle that is returned from StartWorkflowAsync instead.
var handle = myClient.GetWorkflowHandle("my-workflow-id");

// Send cancellation. This returns when cancellation is received by the server. Wait on the handle's
// result to wait for cancellation to be applied.
await handle.CancelAsync();
csharp
[WorkflowRun]
public async Task RunAsync()
{
    // Create a source linked to workflow cancellation. A new source could be created instead if we
    // didn't want it associated with workflow cancellation.
    using var cancelActivitySource = CancellationTokenSource.CreateLinkedTokenSource(
        Workflow.CancellationToken);

// Start the activity. Whether this workflow waits on the activity to handle the cancellation
    // or not is dependent upon the CancellationType option. We leave the default here which sends
    // the cancellation but does not wait on it to be handled.
    var activityTask = Workflow.ExecuteActivityAsync(
        (MyActivities a) => a.MyNormalActivity(),
        new()
        {
            ScheduleToCloseTimeout = TimeSpan.FromMinutes(5),
            CancellationToken = cancelActivitySource.Token;
        });
    activityTask.Start();

// Wait 5 minutes, then cancel it
    await Workflow.DelayAsync(TimeSpan.FromMinutes(5));
    cancelActivitySource.Cancel();

// Wait on the activity which will throw cancellation which will fail the workflow
    await activityTask;
}
csharp
// Get a workflow handle by its workflow ID. This could be made specific to a run by passing run ID.
// This could also just be a handle that is returned from StartWorkflowAsync instead.
var handle = myClient.GetWorkflowHandle("my-workflow-id");

// Terminate
await handle.TerminateAsync();
bash
temporal workflow reset \
    --workflow-id <workflow-id> \
    --event-id <event-id> \
    --reason "Reason for reset"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code" \
    --namespace my-namespace \
    --tls-cert-path /path/to/cert.pem \
    --tls-key-path /path/to/key.pem
csharp
await Workflow.ExecuteChildWorkflowAsync((MyChildWorkflow wf) => wf.RunAsync());
csharp
await Workflow.ExecuteChildWorkflowAsync(
  (MyChildWorkflow wf) => wf.RunAsync(),
  new() { ParentClosePolicy = ParentClosePolicy.Abandon });
csharp
public record Input
    {
        public State State { get; init; } = new();

public bool TestContinueAsNew { get; init; }
    }

[WorkflowInit]
public ClusterManagerWorkflow(Input input)

csharp
throw Workflow.CreateContinueAsNewException((ClusterManagerWorkflow wf) => wf.RunAsync(new()
{
    State = CurrentState,
    TestContinueAsNew = input.TestContinueAsNew,
}));
csharp
private bool ShouldContinueAsNew =>
    // Don't continue as new while update running
    Workflow.AllHandlersFinished &&
    // Continue if suggested or, for ease of testing, max history reached
    (Workflow.ContinueAsNewSuggested || Workflow.CurrentHistoryLength > maxHistoryLength);
csharp
public class EncryptionCodec : IPayloadCodec
{
    public Task<IReadOnlyCollection<Payload>> EncodeAsync(IReadOnlyCollection<Payload> payloads) =>
        Task.FromResult<IReadOnlyCollection<Payload>>(payloads.Select(p =>
        {
            return new Payload()
            {
                // Set our specific encoding. We may also want to add a key ID in here for use by
                // the decode side
                Metadata = { ["encoding"] = "binary/my-payload-encoding" },
                Data = ByteString.CopyFrom(Encrypt(p.ToByteArray())),
            };
        }).ToList());

public Task<IReadOnlyCollection<Payload>> DecodeAsync(IReadOnlyCollection<Payload> payloads) =>
        Task.FromResult<IReadOnlyCollection<Payload>>(payloads.Select(p =>
        {
            // Ignore if it doesn't have our expected encoding
            if (p.Metadata.GetValueOrDefault("encoding") != "binary/my-payload-encoding")
            {
                return p;
            }
            // Decrypt
            return Payload.Parser.ParseFrom(Decrypt(p.Data.ToByteArray()));
        }).ToList());

private byte[] Encrypt(byte[] data) => Encoding.ASCII.GetBytes(Convert.ToBase64String(data));

private byte[] Decrypt(byte[] data) => Convert.FromBase64String(Encoding.ASCII.GetString(data));
}
csharp
var myClient = await TemporalClient.ConnectAsync(new("localhost:7233")
{
    DataConverter = DataConverter.Default with { PayloadCodec = new EncryptionCodec() },
});
csharp
using System.Text.Json;
using Temporalio.Client;
using Temporalio.Converters;

public class CamelCasePayloadConverter : DefaultPayloadConverter
{
    public CamelCasePayloadConverter()
      : base(new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase })
    {
    }
}

var client = await TemporalClient.ConnectAsync(new()
{
    TargetHost = "localhost:7233",
    Namespace = "my-namespace",
    DataConverter = DataConverter.Default with { PayloadConverter = new CamelCasePayloadConverter() },
});
csharp
using Temporalio.Workflows;

[Workflow]
public class MyWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(string name)
    {
        var param = MyActivityParams("Hello", name);
        return await Workflow.ExecuteActivityAsync(
            (MyActivities a) => a.MyActivity(param),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });
    }
}
csharp
  [WorkflowQuery]
  public string GetSomeThing() => someThing;
  ini
##### Configuration specific for Temporal workflows #####
[*.workflow.cs]

**Examples:**

Example 1 (unknown):
```unknown
:::

### What the local server provides

- A local instance of the Temporal Service
- Automatic startup of the Web UI
- A default Namespace
- Optional persistence using SQLite

Omitting `--db-filename` uses an in-memory database. This speeds up testing but does not persist Workflow data between sessions.

### Access the Web UI

- Temporal Service: `localhost:7233`
- Web UI: [http://localhost:8233](http://localhost:8233)

:::tip
The CLI works with all Temporal SDKs.
Use it to develop and test your application before deploying to production.
:::

## Getting CLI help

From the command line:
```

Example 2 (unknown):
```unknown
For example:

- `temporal --help`
- `temporal workflow --help`
- `temporal workflow delete --help`

Available commands

| Command                            | Description                                                 |
| ---------------------------------- | ----------------------------------------------------------- |
| [**activity**](/cli/activity)      | Complete, update, pause, unpause, reset or fail an Activity |
| [**batch**](/cli/batch)            | Manage running batch jobs                                   |
| [**completion**](/cli/cmd-options) | Generate the autocompletion script for the specified shell  |
| [**env**](/cli/env)                | Manage environments                                         |
| [**operator**](/cli/operator)      | Manage Temporal deployments                                 |
| [**schedule**](/cli/schedule)      | Perform operations on Schedules                             |
| [**server**](/cli/server)          | Run Temporal Server                                         |
| [**task-queue**](/cli/task-queue)  | Manage Task Queues                                          |
| [**worker**](/cli/worker)          | Read or update Worker state                                 |
| [**workflow**](/cli/workflow)      | Start, list, and operate on Workflows                       |

---

## Temporal CLI task-queue command reference

{/* NOTE: This is an auto-generated file. Any edit to this file will be overwritten.
This file is generated from https://github.com/temporalio/cli/blob/main/temporalcli/commandsgen/commands.yml */}
## config

Manage Task Queue configuration:
```

Example 3 (unknown):
```unknown
Available commands:
- `get`: Retrieve the current configuration for a task queue
- `set`: Update the configuration for a task queue

### get

Retrieve the current configuration for a Task Queue:
```

Example 4 (unknown):
```unknown
This command returns the current configuration including:
- Queue rate limit: The overall rate limit of the task queue.
  This setting overrides the worker rate limit if set.
  Unless modified, this is the system-defined rate limit.
- Fairness key rate limit defaults: Default rate limits for fairness keys.
  If set, each individual fairness key will be limited to this rate,
  scaled by the weight of the fairness key.

Use the following options to change the behavior of this command.

**Flags:**

**--task-queue**, **-t** _string_

Task Queue name. Required.

**--task-queue-type** _string-enum_

Task Queue type. Accepted values: workflow, activity, nexus. Required. Accepted values: workflow, activity, nexus.

**Global Flags:**

**--address** _string_

Temporal Service gRPC endpoint. (default "localhost:7233")

**--api-key** _string_

API key for request.

**--client-authority** _string_

Temporal gRPC client :authority pseudoheader.

**--client-connect-timeout** _duration_

The client connection timeout. 0s means no timeout.

**--codec-auth** _string_

Authorization header for Codec Server requests.

**--codec-endpoint** _string_

Remote Codec Server endpoint.

**--codec-header** _string[]_

HTTP headers for requests to codec server. Format as a `KEY=VALUE` pair. May be passed multiple times to set multiple headers.

**--color** _string-enum_

Output coloring. Accepted values: always, never, auto. (default "auto")

**--command-timeout** _duration_

The command execution timeout. 0s means no timeout.

**--config-file** _string_

File path to read TOML config from, defaults to `$CONFIG_PATH/temporal/temporal.toml` where `$CONFIG_PATH` is defined as `$HOME/.config` on Unix, "$HOME/Library/Application Support" on macOS, and %AppData% on Windows.

:::note

Option is experimental.

:::

**--disable-config-env** _bool_

If set, disables loading environment config from environment variables.

:::note

Option is experimental.

:::

**--disable-config-file** _bool_

If set, disables loading environment config from config file.

:::note

Option is experimental.

:::

**--env** _string_

Active environment name (`ENV`). (default "default")

**--env-file** _string_

Path to environment settings file. Defaults to `$HOME/.config/temporalio/temporal.yaml`.

**--grpc-meta** _string[]_

HTTP headers for requests. Format as a `KEY=VALUE` pair. May be passed multiple times to set multiple headers. Can also be made available via environment variable as `TEMPORAL_GRPC_META_[name]`.

**--identity** _string_

The identity of the user or client submitting this request. Defaults to "temporal-cli:$USER@$HOST".

**--log-format** _string-enum_

Log format. Accepted values: text, json. (default "text")

**--log-level** _string-enum_

Log level. Default is "info" for most commands and "warn" for `server start-dev`. Accepted values: debug, info, warn, error, never. (default "info")

**--namespace**, **-n** _string_

Temporal Service Namespace. (default "default")

**--no-json-shorthand-payloads** _bool_

Raw payload output, even if the JSON option was used.

**--output**, **-o** _string-enum_

Non-logging data output format. Accepted values: text, json, jsonl, none. (default "text")

**--profile** _string_

Profile to use for config file.

:::note

Option is experimental.

:::

**--time-format** _string-enum_

Time format. Accepted values: relative, iso, raw. (default "relative")

**--tls** _bool_

Enable base TLS encryption. Does not have additional options like mTLS or client certs. This is defaulted to true if api-key or any other TLS options are present. Use --tls=false to explicitly disable.

**--tls-ca-data** _string_

Data for server CA certificate. Can't be used with --tls-ca-path.

**--tls-ca-path** _string_

Path to server CA certificate. Can't be used with --tls-ca-data.

**--tls-cert-data** _string_

Data for x509 certificate. Can't be used with --tls-cert-path.

**--tls-cert-path** _string_

Path to x509 certificate. Can't be used with --tls-cert-data.

**--tls-disable-host-verification** _bool_

Disable TLS host-name verification.

**--tls-key-data** _string_

Private certificate key data. Can't be used with --tls-key-path.

**--tls-key-path** _string_

Path to x509 private key. Can't be used with --tls-key-data.

**--tls-server-name** _string_

Override target TLS server name.

### set

Update configuration settings for a Task Queue.
```

---

## HELP temporal_cloud_v1_workflow_success_count The number of successful workflows per second

**URL:** llms-txt#help-temporal_cloud_v1_workflow_success_count-the-number-of-successful-workflows-per-second

temporal_cloud_v1_workflow_success_count{temporal_namespace="production",temporal_workflow_type="payment-processing",region="aws-us-west-2"} 42.0 1609459200000
temporal_cloud_v1_workflow_success_count{temporal_namespace="production",temporal_workflow_type="order-fulfillment",region="aws-us-west-2"} 128.0 1609459200000

---

## ES_SERVER is the URL of Elasticsearch server; for example, "http://localhost:9200".

**URL:** llms-txt#es_server-is-the-url-of-elasticsearch-server;-for-example,-"http://localhost:9200".

**Contents:**
- How to set up Dual Visibility {#dual-visibility}

SETTINGS_URL="${ES_SERVER}/_cluster/settings"
SETTINGS_FILE=${TEMPORAL_HOME}/schema/elasticsearch/visibility/cluster_settings_${ES_VERSION}.json
TEMPLATE_URL="${ES_SERVER}/_template/temporal_visibility_v1_template"
SCHEMA_FILE=${TEMPORAL_HOME}/schema/elasticsearch/visibility/index_template_${ES_VERSION}.json
INDEX_URL="${ES_SERVER}/${ES_VIS_INDEX}"
curl --fail --user "${ES_USER}":"${ES_PWD}" -X PUT "${SETTINGS_URL}" -H "Content-Type: application/json" --data-binary "@${SETTINGS_FILE}" --write-out "\n"
curl --fail --user "${ES_USER}":"${ES_PWD}" -X PUT "${TEMPLATE_URL}" -H 'Content-Type: application/json' --data-binary "@${SCHEMA_FILE}" --write-out "\n"
curl --user "${ES_USER}":"${ES_PWD}" -X PUT "${INDEX_URL}" --write-out "\n"
yaml
persistence:
  visibilityStore: cass-visibility # This is your primary Visibility store
  secondaryVisibilityStore: mysql-visibility # This is your secondary Visibility store
  datastores:
    cass-visibility:
      cassandra:
        hosts: '127.0.0.1'
        keyspace: 'temporal_primary_visibility'
    mysql-visibility:
      sql:
        pluginName: 'mysql8' # Verify supported versions. Use a version of SQL that supports advanced Visibility.
        databaseName: 'temporal_secondary_visibility'
        connectAddr: '127.0.0.1:3306'
        connectProtocol: 'tcp'
        user: 'temporal'
        password: 'temporal'
yaml
persistence:
  visibilityStore: es-visibility
  datastores:
    es-visibility:
      elasticsearch:
        version: 'v7'
        logLevel: 'error'
        url:
          scheme: 'http'
          host: '127.0.0.1:9200'
        indices:
          visibility: temporal_visibility_v1
          secondary_visibility: temporal_visibility_v1_new
        closeIdleConnectionsInterval: 15s
bash
#...

**Examples:**

Example 1 (unknown):
```unknown
**Elasticsearch privileges**

Ensure that the following privileges are granted for the Elasticsearch Temporal index:

- **Read**
  - [index privileges](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html#privileges-list-indices): `create`, `index`, `delete`, `read`
- **Write**
  - [index privileges](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html#privileges-list-indices): `write`
- **Custom Search Attributes**
  - [index privileges](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html#privileges-list-indices): `manage`
  - [cluster privileges](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html#privileges-list-cluster): `monitor` or `manage`.

## How to set up Dual Visibility {#dual-visibility}

To enable [Dual Visibility](/dual-visibility), set up a secondary Visibility store with your primary Visibility store, and configure your Temporal Service to enable read and/or write operations on the secondary Visibility store.

With Dual Visibility, you can read from only one Visibility store at a time, but can configure your Temporal Service to write to primary only, secondary only, or to both primary and secondary stores.

#### Set up secondary Visibility store

Set the secondary store with the `secondaryVisibilityStore` configuration key in your Persistence configuration, and then define the secondary Visibility store configuration under `datastores`.

You can configure any of the [supported databases](/self-hosted-guide/visibility) as your secondary store.

Examples:

To configure MySQL as a secondary store with Cassandra as your primary store, do the following.
```

Example 2 (unknown):
```unknown
To configure Elasticsearch as both your primary and secondary store, use the configuration key `elasticsearch.indices.secondary_visibility`, as shown in the following example.
```

Example 3 (unknown):
```unknown
#### Database schema and setup

The database schema and setup for a secondary store depends on the database you plan to use.

- [MySQL](#mysql)
- [PostgresSQL](#postgresql)
- [SQLite](#sqlite)
- [Elasticsearch](#elasticsearch)

For the Cassandra and MySQL configuration in the previous example, an example setup script would be as follows.
```

---

## my_workflow_file.py

**URL:** llms-txt#my_workflow_file.py

from temporalio import workflow

with workflow.unsafe.sandbox_import_notification_policy(
    workflow.SandboxImportNotificationPolicy.SILENT
):

@workflow.defn
class MyWorkflow:
     # ...
python

**Examples:**

Example 1 (unknown):
```unknown
This can also be done at worker creation time by customizing the runner's restrictions.
```

---

## Set the `on_heartbeat` property to a callback function that will be called for each Heartbeat sent by the Activity.

**URL:** llms-txt#set-the-`on_heartbeat`-property-to-a-callback-function-that-will-be-called-for-each-heartbeat-sent-by-the-activity.

env.on_heartbeat = lambda *args: heartbeats.append(args[0])

---

## Execute a workflow

**URL:** llms-txt#execute-a-workflow

**Contents:**
- Task Queues
- What is a Task Queue? {#task-queue}
- Task Routing and Worker Sessions
- What is Task Routing? {#task-routing}
  - Flow control
  - Throttling
  - Specific environments
  - Multiple priorities
  - Versioning
- What is a Worker Session? {#worker-session}

result = await client.execute_workflow(
    GreetingWorkflow.run,
    name,
    id="my-workflow",
    task_queue=TASK_QUEUE_NAME,
)
python
worker = Worker(
    client,
    task_queue=TASK_QUEUE_NAME,
    workflows=[GreetingWorkflow],
    activities=[activities.say_hello],
)
go
package app

const TaskQueueName = "my-taskqueue-name"
go
options := client.StartWorkflowOptions{
    ID:        "my-workflow",
    TaskQueue: app.TaskQueueName,
}

run, err := c.ExecuteWorkflow(ctx, options, ProcessOrderWorkflow, input)
go
w := worker.New(c, app.TaskQueueName, worker.Options{})
java
package app;

public class Constants {

public static final String taskQueueName = "my-task-queue-name";

}
java
WorkflowOptions options = WorkflowOptions.newBuilder()
        .setWorkflowId("my-workflow")
        .setTaskQueue(Constants.taskQueueName)
        .build();

MyWorkflow workflow = client.newWorkflowStub(MyWorkflow.class, options);
java
Worker worker = factory.newWorker(Constants.taskQueueName);
typescript
const TASK_QUEUE_NAME = 'my-taskqueue-name';
typescript

// additional code would follow

await client.workflow.start(OrderProcessingWorkflow, {
  args: [order],
  taskQueue: TASK_QUEUE_NAME,
  workflowId: `workflow-order-${order.id},`,
});
typescript

// additional code would follow

const worker = await Worker.create({
  taskQueue: TASK_QUEUE_NAME,
  connection,
  workflowsPath: require.resolve('./workflows'),
  activities,
});
csharp
public static class WorkflowConstants
{
    public const string TaskQueueName = "translation-tasks";
}
csharp
var options = new WorkflowOptions(
            id: "translation-workflow",
            taskQueue: WorkflowConstants.TaskQueueName);

// Run workflow
var result = await client.ExecuteWorkflowAsync(
    (TranslationWorkflow wf) => wf.RunAsync(input),
    options);
csharp
using var worker = new TemporalWorker(
    client,
    new TemporalWorkerOptions(WorkflowConstants.TaskQueueName)
    .AddAllActivities(activities)
    .AddWorkflow<TranslationWorkflow>());

┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
│ │ │ │ │
* * * * *

| Schedules              | Description                                | Equivalent To |
| ---------------------- | ------------------------------------------ | ------------- |
| @yearly (or @annually) | Run once a year, midnight, Jan. 1st        | 0 0 1 1 *     |
| @monthly               | Run once a month, midnight, first of month | 0 0 1 * *     |
| @weekly                | Run once a week, midnight between Sat/Sun  | 0 0 * * 0     |
| @daily (or @midnight)  | Run once a day, midnight                   | 0 0 * * *     |
| @hourly                | Run once an hour, beginning of hour        | 0 * * * *     |

@every <duration>
python
if patched('v3'):
    # This is the newest version of the code.
    # put this at the top, so when it is running
    # a fresh execution and not replaying,
    # this patched statement will return true
    # and it will run the new code.
    pass
elif patched('v2'):
    pass
else:
    pass
python
if patched('v2'):
    # This is bad because when doing a new execution (i.e. not replaying),
    # patched statements evaluate to True (and put a marker
    # in the event history), which means that new executions
    # will use v2, and miss v3 below
    pass
elif patched('v3'):
    pass
else:
  pass
json
{
  "year": "2022",
  "month": "Jan,Apr,Jul,Oct",
  "dayOfMonth": "1,15",
  "hour": "11-14"
}

time -------------------------------------------->
 A     |----------------------|
 B               |-------|
 C                          |---------------|
 D                                |--------------T
go
func YourBasicWorkflow(ctx workflow.Context) error {
    // ...
    return nil
}
java
// Workflow interface
@WorkflowInterface
public interface YourBasicWorkflow {

@WorkflowMethod
    String workflowMethod(Arguments args);
}
java
// Workflow implementation
public class YourBasicWorkflowImpl implements YourBasicWorkflow {
    // ...
}
php
#[WorkflowInterface]
interface YourBasicWorkflow {
    #[WorkflowMethod]
    public function workflowMethod(Arguments args);
}
php
class YourBasicWorkflowImpl implements YourBasicWorkflow {
    // ...
}
Python
@workflow.defn
class YourWorkflow:
    @workflow.run
    async def YourBasicWorkflow(self, input: str) -> str:
        # ...
Typescript
type BasicWorkflowArgs = {
  param: string;
};

export async function WorkflowExample(
  args: BasicWorkflowArgs,
): Promise<{ result: string }> {
  // ...
}
csharp
[Workflow]
public class YourBasicWorkflow {

[WorkflowRun]
    public async Task<string> workflowExample(string param) {
        // ...
    }
}
text
fn your_workflow() {
  if local_clock().is_before("12pm") {
    await workflow.sleep(duration_until("12pm"))
  } else {
    await your_afternoon_activity()
  }
}
command
temporal server start-dev --dynamic-config-value frontend.enableUpdateWorkflowExecution=true
temporal server start-dev --dynamic-config-value frontend.enableUpdateWorkflowExecutionAsyncAccepted=true

5M Actions ⨉ $50 Per Million Actions = $250
5M Actions ⨉ $45 Per Million Actions = $225
1.25M Actions ⨉ $40 Per Million Actions = $50
Actions
$250 (First Tier) + $225 (Second Tier) + $50 (Third Tier) = $525

720 GBh Active Storage ⨉ $0.042 per GBh = $30.24
3,600 GBh Retained Storage ⨉ $0.00105 per GBh = $3.78
Total Storage Bill: $30.24 Active Storage + $3.78 Retained Storage = $34.02

Greater of $100 or 5% ⨉ $3,000 = $150, so $150.

Beginning credit balance of 72,000 - 5800 credits used = 66,200, Temporal Credits remaining.
go
func main() {
   fmt.Println("print audit log from S3")
   cfg, err := config.LoadDefaultConfig(context.TODO(),
      config.WithSharedConfigProfile("your_profile"),
   )
   if err != nil {
      fmt.Println(err)
   }
   s3Client := s3.NewFromConfig(cfg)
   response, err := s3Client.GetObject(
      context.Background(),
      &s3.GetObjectInput{
         Bucket: aws.String("your_bucket_name"),
         Key:    aws.String("your_s3_file_path")})
   if err != nil {
      fmt.Println(err)
   }
   defer response.Body.Close()

content, err := io.ReadAll(response.Body)

fmt.Println(string(content))
}
json
{
  "emit_time": "2023-11-14T07:56:55Z",
  "level": "LOG_LEVEL_INFO",
  "caller_ip_address": "10.1.2.3, 10.4.5.6",
  "user_email": "user1@example.com",
  "operation": "DeleteUser",
  "details": {
    "target_users": ["d7dca96f-adcc-417d-aafc-e8f5d2ba9fe1"],
    "search_attribute_update": {}
  },
  "status": "OK",
  "category": "LOG_CATEGORY_ADMIN",
  "log_id": "0mc69c0323b871293ce231dd1c7fb639",
  "request_id": "445297d3-43a7-4793-8a04-1b1dd1999640",
  "principal": {
    "id": "988cb80b-d6be-4bb5-9c87-d09f93f58ed3",
    "type": "user",
    "name": "user1@example.com"
  }
}
json
{
  "operation":  // Operation that was performed
  "principal": // Information about who initiated the operation
  "details":  // DEPRECATED, see raw_details
  "raw_details": // details about the request
  "user_email":  // DEPRECATED, use principal.user where applicable
  "x_forwarded_for": // the IP address making the call
  "caller_ip_address": // DEPRECATED, use x_forwarded_for
  "category":  // DEPRECATED, no longer used
  "emit_time": // Time the operation was recorded
  "level": // DEPRECATED, use status
  "log_id": // Unique ID of the log entry
  "request_id": // Optional async request id set by the user when sending a request
  "status": // Status, such as OK or ERROR
  "version": // Version of the log entry
}
json
[
  {
    "operation": "UserLogin",
    "status": "OK",
    "version": 2,
    "logId": "edb3aa3e-78c4-48fc-9c7e-2078c6989775",
    "xForwardedFor": "10.1.2.3",
    "asyncOperationId": "",
    "emitTime": {
      "$typeName": "google.protobuf.Timestamp",
      "seconds": 1759436617,
      "nanos": 48000000
    },
    "principal": {
      "type": "user",
      "id": "",
      "name": "user@email.com",
      "apiKeyId": ""
    }
  },
  {
    "operation": "UserLogin",
    "status": "OK",
    "version": 2,
    "logId": "5fe6a81e-8d3c-4f4d-88a5-52db864c9ea5",
    "xForwardedFor": "10.1.2.3",
    "asyncOperationId": "",
    "emitTime": {
      "seconds": 1759178573,
      "nanos": 671000000
    },
    "principal": {
      "type": "user",
      "id": "",
      "name": "user@email.com",
      "apiKeyId": ""
    }
  }
]
command
tcld namespace export s3 create --namespace "your-namespace.your-account" --sink-name "your-sink-name" --role-arn "arn:aws:iam::123456789012:role/test-sink" --s3-bucket-name "your-aws-s3-bucket-name"
command
tcld namespace export s3 get --namespace "your-namespace.your-account" --sink-name "your-sink-name"
json
{
  "name": "your-sink-name",
  "resourceVersion": "a6442895-1c07-4da4-aaca-58d57d338345",
  "state": "Active",
  "spec": {
    "name": "your-sink-name",
    "enabled": true,
    "destinationType": "S3",
    "s3Sink": {
      "roleName": "your-export-test",
      "bucketName": "your-export-test",
      "region": "us-east-1",
      "kmsArn": "",
      "awsAccountId": "123456789012"
    }
  },
  "health": "Ok",
  "errorMessage": "",
  "latestDataExportTime": "0001-01-01T00:00:00Z",
  "lastHealthCheckTime": "2023-08-14T21:30:02Z"
}
command
tcld capacity update --namespace <namespace_name> --capacity-mode <on_demand|provisioned> --capacity-value <tru value> [--request–id <request_id> --resource-version <resource-version>]
bash
aws ec2 describe-vpc-endpoints \
  --vpc-endpoint-ids $VPC_ENDPOINT_ID \
  --query "VpcEndpoints[0].DnsEntries[0].DnsName" \
  --output text

**Examples:**

Example 1 (unknown):
```unknown
**Excerpt of code used to configure the Worker, referencing the constant
defined with the Task Queue name in Python**
```

Example 2 (unknown):
```unknown
</TabItem>
<TabItem value="go" label="Go">

**Excerpt of code used to define a constant with the Task Queue name in Go**
```

Example 3 (unknown):
```unknown
**Excerpt of code used to start the Workflow, referencing the constant defined with the Task Queue name in Go**
```

Example 4 (unknown):
```unknown
**Excerpt of code used to configure the Worker, referencing the constant defined with the Task Queue name in Go**
```

---

## We use getters for queries, they cannot be properties

**URL:** llms-txt#we-use-getters-for-queries,-they-cannot-be-properties

dotnet_diagnostic.CA1024.severity = none

---

## The workflow handle is on the start operation, here's an example of waiting on

**URL:** llms-txt#the-workflow-handle-is-on-the-start-operation,-here's-an-example-of-waiting-on

---

## Define your mocked Activity implementation

**URL:** llms-txt#define-your-mocked-activity-implementation

**Contents:**
  - How to skip time {#skip-time}
  - Assert in Workflow {#assert-in-workflow}
- How to Replay a Workflow Execution {#replay}
- Durable Timers - Python SDK

@activity.defn(name="compose_greeting")
async def compose_greeting_mocked(input: ComposeGreetingInput) -> str:
    return f"{input.greeting}, {input.name} from mocked activity!"

async def test_mock_activity(client: Client):
    task_queue_name = str(uuid.uuid4())
    # Provide the mocked Activity implementation to the Worker
    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[GreetingWorkflow],
        activities=[compose_greeting_mocked],
    ):
        # Execute your Workflow as usual
        assert "Hello, World from mocked activity!" == await client.execute_workflow(
            GreetingWorkflow.run,
            "World",
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )
python
from temporalio.testing import WorkflowEnvironment

async def test_manual_time_skipping():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        # Your code here
        # You can use the env.sleep(seconds) method to manually advance time
        await env.sleep(3) # This will advance time by 3 seconds
        # Your code here
python
workflows = client.list_workflows(f"TaskQueue=foo and StartTime > '2022-01-01T12:00:00'")
histories = workflows.map_histories()
replayer = Replayer(
    workflows=[MyWorkflowA, MyWorkflowB, MyWorkflowC]
)
await replayer.replay_workflows(histories)
python
replayer = Replayer(workflows=[YourWorkflow])
await replayer.replay_workflow(WorkflowHistory.from_json(history_json_str))
python

**Examples:**

Example 1 (unknown):
```unknown
The mocked Activity implementation should have the same signature as the real implementation (including the input and output types) and the same name.
When the Workflow invokes the Activity, it invokes the mocked implementation instead of the real one, allowing you to test your Workflow isolated.

### How to skip time {#skip-time}

Some long-running Workflows can persist for months or even years.
Implementing the test framework allows your Workflow code to skip time and complete your tests in seconds rather than the Workflow's specified amount.

For example, if you have a Workflow sleep for a day, or have an Activity failure with a long retry interval, you don't need to wait the entire length of the sleep period to test whether the sleep function works.
Instead, test the logic that happens after the sleep by skipping forward in time and complete your tests in a timely manner.

The test framework included in most SDKs is an in-memory implementation of Temporal Server that supports skipping time.
Time is a global property of an instance of `TestWorkflowEnvironment`: skipping time (either automatically or manually) applies to all currently running tests.
If you need different time behaviors for different tests, run your tests in a series or with separate instances of the test server.
For example, you could run all tests with automatic time skipping in parallel, and then all tests with manual time skipping in series, and then all tests without time skipping in parallel.

#### Skip time automatically {#automatic-method}

You can skip time automatically in the SDK of your choice.
Start a test server process that skips time as needed.
For example, in the time-skipping mode, Timers, which include sleeps and conditional timeouts, are fast-forwarded except when Activities are running.

Use the [`start_time_skipping()`](https://python.temporal.io/temporalio.testing.WorkflowEnvironment.html#start_time_skipping) method to start a test server process and skip time automatically.

Use the [`start_local()`](https://python.temporal.io/temporalio.testing.WorkflowEnvironment.html#start_local) method for a full local Temporal Server.

Use the [`from_client()`](https://python.temporal.io/temporalio.testing.WorkflowEnvironment.html#from_client) method for an existing Temporal Server.

#### Skip time manually {#manual-method}

Skip time manually in the SDK of your choice.

To implement time skipping, use the [`start_time_skipping()`](https://python.temporal.io/temporalio.testing.WorkflowEnvironment.html#start_time_skipping) static method.
```

Example 2 (unknown):
```unknown
### Assert in Workflow {#assert-in-workflow}

The `assert` statement is a convenient way to insert debugging assertions into the Workflow context.

The `assert` method is available in Python and TypeScript.

For information about assert statements in Python, see [`assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) in the Python Language Reference.

## How to Replay a Workflow Execution {#replay}

Replay recreates the exact state of a Workflow Execution.
You can replay a Workflow from the beginning of its Event History.

Replay succeeds only if the [Workflow Definition](/workflow-definition) is compatible with the provided history from a deterministic point of view.

When you test changes to your Workflow Definitions, we recommend doing the following as part of your CI checks:

1. Determine which Workflow Types or Task Queues (or both) will be targeted by the Worker code under test.
2. Download the Event Histories of a representative set of recent open and closed Workflows from each Task Queue, either programmatically using the SDK client or via the Temporal CLI.
3. Run the Event Histories through replay.
4. Fail CI if any error is encountered during replay.

The following are examples of fetching and replaying Event Histories:

To replay Workflow Executions, use the [`replay_workflows`](https://python.temporal.io/temporalio.worker.Replayer.html#replay_workflows) or [`replay_workflow`](https://python.temporal.io/temporalio.worker.Replayer.html#replay_workflow) methods, passing one or more Event Histories as arguments.

In the following example (which, as of server v1.18, requires Advanced Visibility to be enabled), Event Histories are downloaded from the server and then replayed.
If any replay fails, the code raises an exception.
```

Example 3 (unknown):
```unknown
In the next example, a single history is loaded from a JSON string:
```

Example 4 (unknown):
```unknown
In both examples, if Event History is non-deterministic, an error is thrown.
You can choose to wait until all histories have been replayed with `replay_workflows` by setting the `fail_fast` option to `false`.

:::note

If the Workflow History is exported by [Temporal Web UI](/web-ui) or through [Temporal CLI](/cli), you can pass the JSON file history object as a JSON string or as a Python dictionary through the `json.load()` function, which takes a file object and returns the JSON object.

:::tip
When fetching event histories directly from the server or exporting them, be aware that the data can be protobuf-encoded (`bytes`). The `Replayer`, however, often works with decoded histories (like a `dict`).

If you encounter `TypeError` exceptions related to `dict` vs. `bytes` mismatches during replay, ensure your event history is properly decoded before passing it to the Replayer.
:::

---

## Durable Timers - Python SDK

A Workflow can set a durable Timer for a fixed time period.
In some SDKs, the function is called `sleep()`, and in others, it's called `timer()`.

A Workflow can sleep for months.
Timers are persisted, so even if your Worker or Temporal Service is down when the time period completes, as soon as your Worker and Temporal Service are back up, the `sleep()` call will resolve and your code will continue executing.

Sleeping is a resource-light operation: it does not tie up the process, and you can run millions of Timers off a single Worker.

To set a Timer in Python, call the [`asyncio.sleep()`](https://docs.python.org/3/library/asyncio-task.html#sleeping) function and pass the duration in seconds you want to wait before continuing.

  
    View the source code
  {' '}
  in the context of the rest of the application code.
```

---

## Run workflow

**URL:** llms-txt#run-workflow

**Contents:**
  - Verify Success
- Temporal Client - Ruby SDK
- Connect to development Temporal Service {#connect-to-development-service}

result = client.execute_workflow(
  SayHelloWorkflow,
  'Temporal', # This is the input to the workflow
  id: 'my-workflow-id',
  task_queue: 'my-task-queue'
)
puts "Result: #{result}"
bash
ruby starter.rb
toml title="config.toml"

**Examples:**

Example 1 (unknown):
```unknown
Then run:
```

Example 2 (unknown):
```unknown
### Verify Success

If everything is working correctly, you should see:

- Worker processing the workflow and activity
- Output: `Workflow result: Hello, Temporal!`
- Workflow Execution details in the [Temporal Web UI](http://localhost:8233)

<CallToAction href="https://learn.temporal.io/getting_started/ruby/first_program_in_ruby/">
  Next: Run your first Temporal Application
  Create a basic Workflow and run it with the Temporal Ruby SDK
</CallToAction>

---

## Temporal Client - Ruby SDK

A [Temporal Client](/encyclopedia/temporal-sdks#temporal-client) enables you to communicate with the Temporal Service.
Communication with a Temporal Service lets you perform actions such as starting Workflow Executions, sending Signals and
Queries to Workflow Executions, getting Workflow results, and more.

This page shows you how to do the following using the Ruby SDK with the Temporal Client:

- [Connect to a local development Temporal Service](#connect-to-development-service)
- [Connect to Temporal Cloud](#connect-to-temporal-cloud)
- [Start a Workflow Execution](#start-workflow)
- [Get Workflow results](#get-workflow-results)

A Temporal Client cannot be initialized and used inside a Workflow. However, it is acceptable and common to use a
Temporal Client inside an Activity to communicate with a Temporal Service.

## Connect to development Temporal Service {#connect-to-development-service}

Use [`Client.connect`](https://ruby.temporal.io/Temporalio/Client.html#connect-class_method) to create a client.
Connection options include the Temporal Server address, Namespace, and (optionally) TLS configuration. You can provide
these options directly in code, load them from **environment variables**, or a **TOML configuration file** using the
[`EnvConfig`](https://ruby.temporal.io/Temporalio/EnvConfig.html) helpers. We recommend environment variables or a
configuration file for secure, repeatable configuration.

When you’re running a Temporal Service locally (such as with the
[Temporal CLI dev server](https://docs.temporal.io/cli/server#start-dev)), the required options are minimal. If you
don't specify a host/port, most connections default to `127.0.0.1:7233` and the `default` Namespace.

<Tabs groupId="connect-options" defaultValue="config-file" >

<TabItem value="config-file" label="Configuration File">

You can use a TOML configuration file to set connection options for the Temporal Client. The configuration file lets you
configure multiple profiles, each with its own set of connection options. You can then specify which profile to use when
creating the Temporal Client. You can use the environment variable `TEMPORAL_CONFIG_FILE` to specify the location of the
TOML file or provide the path to the file directly in code. If you don't provide the configuration file path, the SDK
looks for it at the path `~/.config/temporalio/temporal.toml` or the equivalent on your OS. Refer to
[Environment Configuration](../environment-configuration.mdx#configuration-methods) for more details about configuration
files and profiles.

:::info

The connection options set in configuration files have lower precedence than environment variables. This means that if
you set the same option in both the configuration file and as an environment variable, the environment variable value
overrides the option set in the configuration file.

:::

For example, the following TOML configuration file defines two profiles: `default` and `prod`. Each profile has its own
set of connection options.
```

---

## Count the total number of series by metric

**URL:** llms-txt#count-the-total-number-of-series-by-metric

**Contents:**
- API Limits
- Temporal Cloud OpenMetrics
- Quick Links
- Overview
- API key authentication
- Global endpoint
- Namespace and metric filtering
- Dashboard templates
- Metrics Integrations
- Integrations

count({__name__=~"temporal_cloud_v1_.*"}) by (__name__)
yaml
scrape_configs:
  - job_name: 'temporal-cloud'
    scrape_interval: 60s
    scrape_timeout: 30s
    honor_timestamps: true
    scheme: https
    authorization:
      type: Bearer
      credentials: '<API_KEY>'
    static_configs:
      - targets: ['metrics.temporal.io']
    metrics_path: '/v1/metrics'
yaml
receivers:
  prometheus:
    config:
      scrape_configs:
      - job_name: 'temporal-cloud'
        scrape_interval: 60s
        scrape_timeout: 30s
        honor_timestamps: true
        scheme: https
        authorization:
          type: Bearer
          credentials_file: <API_KEY_FILE>
        static_configs:
          - targets: ['metrics.temporal.io']
        metrics_path: '/v1/metrics'

exporters:
  otlphttp:
    endpoint: <ENDPOINT>

service:
  pipelines:
    metrics:
      receivers: [prometheus]
      processors: [batch]
      exporters: [otlphttp]

rate(temporal_cloud_v0_frontend_service_request_count[1m])

temporal_cloud_v1_frontend_service_request_count
shell
histogram_quantile(0.95, rate(temporal_cloud_v0_service_latency_bucket[5m]))

temporal_cloud_v1_service_latency_p95
shell
curl --cert /path/to/client.pem \
     --key /path/to/client.key \
     --cacert /path/to/ca.pem \

"https://<customer-specific>.tmprl.cloud/api/v1/query?query=rate(temporal_cloud_v0_frontend_service_request_count[5m])&time=2025-01-15T10:00:00Z"
shell
curl -H "Authorization: Bearer <API_KEY>" https://metrics.temporal.io/v1/metrics
shell
$ curl -H "Authorization: Bearer <API_KEY>" https://metrics.temporal.io/v1/metrics

**Examples:**

Example 1 (unknown):
```unknown
## API Limits

| Limit | Impact | Mitigation |
| ----- | ----- | ----- |
| 30k total datapoints per scrape | Response may be truncated | Use namespace/metric filtering |
| 180 requests per account per hour | HTTP 429 returned | Set appropriate scrape interval of 30-60s |

---

## Temporal Cloud OpenMetrics

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

Temporal Cloud OpenMetrics support is available in  [Public Preview](/evaluate/development-production-features/release-stages#public-preview).

:::

:::tip PRICING

Future pricing may apply to high-volume usage that exceeds standard [limits](/production-deployment/cloud/metrics/openmetrics/api-reference#api-limits).

:::

Temporal Cloud's [OpenMetrics](https://openmetrics.io/) endpoint provides operational metrics for your Temporal Cloud workloads in industry-standard Prometheus format, enabling comprehensive monitoring across Namespaces, Workflows, and Task Queues with your existing observability stack.

## Quick Links
* [Integrations](/production-deployment/cloud/metrics/openmetrics/metrics-integrations) - Get started exporting metrics with common integrations
* [API Documentation](/production-deployment/cloud/metrics/openmetrics/api-reference) - Endpoint specification and advanced configuration
* [Metrics Reference](/production-deployment/cloud/metrics/openmetrics/metrics-reference) - Complete catalog of all metrics with descriptions and labels
* [Migration Guide](/production-deployment/cloud/metrics/openmetrics/migration-guide) - Guide on how to transition from the Prometheus query endpoint

## Overview
Temporal Cloud OpenMetrics exposes 30+ metrics covering workflow lifecycles, task queue operations, service performance, and system limits. All metrics are aggregated over one-minute windows and available for scraping within two minutes.

* [Set up authentication and scraping](/production-deployment/cloud/metrics/openmetrics/api-reference#authentication) with the API documentation. 
* Browse the [complete metrics catalog](/production-deployment/cloud/metrics/openmetrics/metrics-reference) for descriptions and labels. 
* Teams using the query endpoint should review the [migration guide](/production-deployment/cloud/metrics/openmetrics/migration-guide).

## API key authentication
Create a [service account](/production-deployment/cloud/metrics/openmetrics/migration-guide#create-an-api-key) with the "Metrics Read-Only" role, generate an API key, and start scraping immediately - no certificate rotation or distribution required.

## Global endpoint
This is a single endpoint at `metrics.temporal.io` which serves all metrics across your entire account with API key authentication and standard HTTPS.

## Namespace and metric filtering
You can use query parameters to enable selective scraping to manage data volume and costs, which support wildcards for flexible namespace selection and specific metric filtering.

## Dashboard templates
Production-ready [Grafana dashboards](https://github.com/grafana/jsonnet-libs/blob/master/temporal-mixin/dashboards/temporal-overview.json) provide immediate visibility with pre-built queries and visualizations.

---

## Metrics Integrations

Metrics can be exported from Temporal Cloud using the OpenMetrics endpoint. This document describes configuring integrations that have third party support or are based on open standards.
This document is for basic configuration only. For advanced concepts such as label management and high cardinality scenarios see the 
[general API reference](/production-deployment/cloud/metrics/openmetrics/api-reference).

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

Temporal Cloud OpenMetrics support is available in  [Public Preview](/evaluate/development-production-features/release-stages#public-preview).

:::

## Integrations

### Grafana Cloud

Grafana provides a serverless integration with the OpenMetrics endpoint for Grafana Cloud. This integration will scrape metrics, store them in Grafana Cloud, and provides a default dashboard
for visualizing the metrics in Grafana Cloud. See the [integration page](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/integrations/integration-reference/integration-temporal/)
 for more details.

### ClickStack

ClickHouse provides an integration with the OpenMetrics endpoint for ClickStack. This integration uses an OpenTelemetry collector to read from the OpenMetrics endpoint, ingest data into ClickHouse, and
includes a default dashboard to visualize the data with HyperDX. See the [integration page](https://clickhouse.com/docs/use-cases/observability/clickstack/integrations/temporal-metrics) for more details.

### Prometheus \+ Grafana

Self hosted Prometheus can be used to scrape the OpenMetrics endpoint.

1. Add a new scrape job for the OpenMetrics endpoint with your [API key](/production-deployment/cloud/metrics/openmetrics/api-reference#creating-api-keys).
```

Example 2 (unknown):
```unknown
2. Import the [Grafana dashboard](https://github.com/grafana/jsonnet-libs/blob/master/temporal-mixin/dashboards/temporal-overview.json) and configure your Prometheus datasource.

### OpenTelemetry Collector Configuration

Collect metrics with a self-hosted OpenTelemetry Collector to ingest into the system of your choosing.

1. Add a new prometheus receiver for the OpenMetrics endpoint with your [API key](/production-deployment/cloud/metrics/openmetrics/api-reference#creating-api-keys).
```

Example 3 (unknown):
```unknown
:::info

Examples for these integrations and more are [here](https://github.com/temporal-community/cloud-metrics-scrape-examples).

:::

---

## OpenMetrics Metrics Reference

This document describes all metrics available from the Temporal Cloud OpenMetrics endpoint.

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

Temporal Cloud OpenMetrics support is available in  [Public Preview](/evaluate/development-production-features/release-stages#public-preview).

:::

## Metric Conventions

### Metric Types

All metrics are exposed as OpenMetrics gauges, but represent different measurement types:

* *Rate Metrics*: per-second rate of the aggregated values  
* *Value Metrics*: The most recent aggregate value within a look-back window (e.g. backlogs, limits)  
* *Percentile Metrics*: Pre-calculated aggregated latency percentiles in seconds

:::note

All metrics are stored as 1 minute aggregates.

:::

### Common Labels

All metrics include these base labels:

| Label | Description |
| ----- | ----- |
| `temporal_namespace` | The Temporal namespace |
| `temporal_account` | The Temporal account identifier |
| `region` | Cloud region where the metric originated |

## Metrics Catalog

### Frontend Service Metrics

#### temporal\_cloud\_v1\_frontend\_service\_request\_count

gRPC requests received per second.

| Label | Description |
| ----- | ----- |
| `operation` | The name of the RPC operation |

**Type**: Rate

#### temporal\_cloud\_v1\_service\_request\_throttled\_count

gRPC requests throttled per second.

| Label | Description |
| ----- | ----- |
| `operation` | The name of the RPC operation |

**Type**: Rate

#### temporal\_cloud\_v1\_frontend\_service\_error\_count

gRPC errors per second.

| Label | Description |
| ----- | ----- |
| `operation` | The name of the RPC operation |

**Type**: Rate

#### temporal\_cloud\_v1\_frontend\_service\_pending\_requests

The number of pollers that are waiting for a task. Use this to track against ``temporal_cloud_v1_poller_limit``

| Label | Description |
| ----- | ----- |
| `operation` | The name of the operation |

**Type**: Value

#### temporal\_cloud\_v1\_resource\_exhausted\_error\_count

Resource exhaustion errors per second. This metric does not include throttling due to Namespace limits.

| Label | Description |
| ----- | ----- |
| `operation` | The name of the operation |

**Type**: Rate

#### temporal\_cloud\_v1\_service\_latency\_p50

:::caution

Avoid aggregating this metric across dimensions because the percentile won't be accurate.

:::

The 50th percentile latency of service requests in seconds

| Label | Description |
| ----- | ----- |
| `operation` | The name of the operation |

**Type**: Latency  

#### temporal\_cloud\_v1\_service\_latency\_p95

:::caution

Avoid aggregating this metric across dimensions because the percentile won't be accurate.

:::

The 95th percentile latency of service requests in seconds

| Label | Description |
| ----- | ----- |
| `operation` | The name of the operation |

**Type**: Latency  

#### temporal\_cloud\_v1\_service\_latency\_p99

:::caution

Avoid aggregating this metric across dimensions as the percentile won't be accurate.

:::

The 99th percentile latency of service requests in seconds

| Label | Description |
| ----- | ----- |
| `operation` | The name of the operation |

**Type**: Latency  

### Workflow Completion Metrics

:::caution High Cardinality

These metrics could have high cardinality depending on number of workflow types and task queues.

:::

#### temporal\_cloud\_v1\_workflow\_success\_count

Successful workflow completions per second.

| Label | Description |
| ----- | ----- |
| `operation` | The operation name |
| `temporal_task_queue` | The task queue name |
| `temporal_workflow_type` | The workflow type |

**Type**: Rate  

#### temporal\_cloud\_v1\_workflow\_failed\_count

Workflow failures per second.

| Label | Description |
| ----- | ----- |
| `operation` | The operation name |
| `temporal_task_queue` | The task queue name |
| `temporal_workflow_type` | The workflow type |

**Type**: Rate

#### temporal\_cloud\_v1\_workflow\_timeout\_count

Workflow timeouts per second.

| Label | Description |
| ----- | ----- |
| `operation` | The operation name |
| `temporal_task_queue` | The task queue name |
| `temporal_workflow_type` | The workflow type |

**Type**: Rate

#### temporal\_cloud\_v1\_workflow\_cancel\_count

Workflow cancellations per second.

| Label | Description |
| ----- | ----- |
| `operation` | The operation name |
| `temporal_task_queue` | The task queue name |
| `temporal_workflow_type` | The workflow type |

**Type**: Rate

#### temporal\_cloud\_v1\_workflow\_terminate\_count

Workflow terminations per second.

| Label | Description |
| ----- | ----- |
| `operation` | The operation name |
| `temporal_task_queue` | The task queue name |
| `temporal_workflow_type` | The workflow type |

**Type**: Rate

#### temporal\_cloud\_v1\_workflow\_continued\_as\_new\_count

Workflows continued as new per second.

| Label | Description |
| ----- | ----- |
| `operation` | The operation name |
| `temporal_task_queue` | The task queue name |
| `temporal_workflow_type` | The workflow type |

**Type**: Rate

### Task Queue Metrics

:::caution High Cardinality

These metrics could have high cardinality depending on number of task queues present.

:::

#### temporal\_cloud\_v1\_approximate\_backlog\_count

The approximate number of tasks pending in a task queue. Started Activities are not included in the count as they have been dequeued from the task queue.

| Label | Description |
| ----- | ----- |
| `temporal_task_queue` | The task queue name |
| `task_type` | Type of task: `workflow` or `activity` |

**Type**: Value

#### temporal\_cloud\_v1\_poll\_success\_count

Successfully matched tasks per second.

| Label | Description |
| ----- | ----- |
| `operation` | The poll operation name |
| `task_type` | Type of task: `workflow` or `activity` |
| `temporal_task_queue` | The task queue name |

**Type**: Rate

#### temporal\_cloud\_v1\_poll\_success\_sync\_count

Tasks matched synchronously per second (no polling wait).

| Label | Description |
| ----- | ----- |
| `operation` | The poll operation name |
| `task_type` | Type of task: `workflow` or `activity` |
| `temporal_task_queue` | The task queue name |

**Type**: Rate

#### temporal\_cloud\_v1\_poll\_timeout\_count

The rate of poll requests that timed out without receiving a task.

| Label | Description |
| ----- | ----- |
| `operation` | The poll operation name |
| `task_type` | Type of task: `workflow` or `activity` |
| `temporal_task_queue` | The task queue name |

**Type**: Rate

#### temporal\_cloud\_v1\_no\_poller\_tasks\_count

The rate of tasks added to queues with no active pollers.

| Label | Description |
| ----- | ----- |
| `temporal_task_queue` | The task queue name |
| `task_type` | Type of task: `workflow` or `activity` |

**Type**: Rate

### Namespace Metrics

#### temporal\_cloud\_v1\_namespace\_open\_workflows

The current number of open workflows in a namespace.

**Type**: Value

#### temporal\_cloud\_v1\_state\_transition\_count

Workflow state transitions per second.

**Type**: Rate

#### temporal\_cloud\_v1\_total\_action\_count

The total number of actions performed per second. Actions with `is_background=false` are counted toward the ``temporal_cloud_v1_action_limit``.

| Label | Description |
| ----- | ----- |
| `is_background` | Whether the action was background: `true` or `false`. Background actions (e.g. History export) do not count toward the action rate limit |
| `namespace_mode` | Indicates if actions are produced by an `active` or a `standby` Namespace |

**Type**: Rate

#### temporal\_cloud\_v1\_total\_action\_throttled\_count

The total number of actions throttled per second.

**Type**: Rate

#### temporal\_cloud\_v1\_operations\_count

Operations performed per second.

| Label | Description |
| ----- | ----- |
| `operation` | The name of the operation |
| `is_background` | Whether the operation was background: `true` or `false`. Background operations do not count toward the operation rate limit |
| `namespace_mode` | Indicates if operations are produced by an `active` or a `standby` Namespace |

**Type**: Rate

#### temporal\_cloud\_v1\_operations\_throttled\_count

Operations throttled due to rate limits per second.

| Label | Description |
| ----- | ----- |
| `operation` | The name of the operation |
| `is_background` | Whether the operation was background: `true` or `false`. Background operations do not count toward the operation rate limit |
| `namespace_mode` | Indicates if actions are throttled in an `active` or a `standby` Namespace |

**Type**: Rate

### Schedule Metrics

#### temporal\_cloud\_v1\_schedule\_action\_success\_count

Successfully executed scheduled workflows per second.

**Type**: Rate

#### temporal\_cloud\_v1\_schedule\_buffer\_overruns\_count

The rate of schedule buffer overruns when using `BUFFER_ALL` overlap policy.

**Type**: Rate

#### temporal\_cloud\_v1\_schedule\_missed\_catchup\_window\_count

The rate of missed schedule executions outside the catchup window.

**Type**: Rate

#### temporal\_cloud\_v1\_schedule\_rate\_limited\_count

The rate of scheduled workflows delayed due to rate limiting.

**Type**: Rate

### Replication Metrics

#### temporal\_cloud\_v1\_replication\_lag\_p50

The 50th percentile cross-region replication lag in seconds.

**Type**: Latency

#### temporal\_cloud\_v1\_replication\_lag\_p95

The 95th percentile cross-region replication lag in seconds.

**Type**: Latency

#### temporal\_cloud\_v1\_replication\_lag\_p99

The 99th percentile cross-region replication lag in seconds.

**Type**: Latency

### Limit Metrics

#### temporal\_cloud\_v1\_operations\_limit

The current configured operations per second limit for a namespace.

**Type**: Value

#### temporal\_cloud\_v1\_action\_limit

The current configured actions per second limit for a namespace. Track utilization against this limit with ``temporal_cloud_v1_total_action_count`` and `is_background=false`.

**Type**: Value

#### temporal\_cloud\_v1\_frontend\_rps\_limit

The current configured frontend service RPS limit for a namespace. Track utilization against this limit with ``temporal_cloud_v1_frontend_service_request_count``

**Type**: Value

#### temporal\_cloud\_v1\_poller\_limit

The current configured poller limit for a namespace. Track utilization against this limit with ``temporal_cloud_v1_frontend_service_pending_requests``.

**Type**: Value

---

## OpenMetrics Migration Guide

Temporal Cloud is transitioning from our Prometheus query endpoint to an industry-standard OpenMetrics (Prometheus-compatible) endpoint for metrics collection. This migration represents a significant improvement in how you can monitor your Temporal Cloud workloads, bringing enhanced capabilities, better integration with observability tools, and access to high-cardinality metrics that were previously unavailable.

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

The OpenMetrics endpoint is available in  [Public Preview](/evaluate/development-production-features/release-stages#public-preview) for testing and validation. The existing Prometheus query endpoint remains fully operational and supported.

:::

## Why We're Making This Change

1. **Industry-Standard Format**: Native compatibility with Prometheus and OpenTelemetry and all major observability platforms (Datadog, New Relic etc.) without custom integrations.

2. **High-Cardinality Metrics**: Access to previously unavailable dimensions including:  
   * `temporal_task_queue` labels on multiple metrics  
   * `temporal_workflow_type` labels for workflow-specific monitoring  
   * New task queue backlog metrics for better operational visibility  
3. **Accurate Percentiles**: Our new system provides accurate percentile calculations for latency metrics, even in the presence of substantial outliers, unlike Prometheus-style histograms.

4. **Simplified Integration**: Direct scraping from your observability tools without intermediate translation layers.

5. **Enhanced Performance**: Optimized for high-cardinality data with built-in safeguards for system stability. Data is available to scrape two minutes from the time it was emitted, in line with the freshest metrics [available from any major service provider](https://docs.datadoghq.com/integrations/guide/cloud-metric-delay/).

## What's Changing

| Aspect | Current Query Endpoint | New OpenMetrics Endpoint |
| ----- | ----- | ----- |
| **Protocol** | Prometheus Query API (`/api/v1/query`) | OpenMetrics scrape endpoint (`/v1/metrics`) |
| **Authentication** | mTLS certificates with customer-specific endpoints | API keys with global endpoint |
| **Metric Temporality** | Cumulative counters | Delta temporality (pre-computed rates) |
| **Query Requirement** | Direct queries supported | Requires observability platform |
| **Cardinality** | Limited labels | High-cardinality labels available |
| **Metric Naming** | `*_v0_*` metrics | `*_v1_*` metrics |

## Migration Timeline

Here is the current estimated timeline for migrating from the Prometheus query endpoint to the OpenMetrics endpoint. 

:::caution

Timelines can shift so be sure to stay up to date on upcoming releases.

:::

**Public Preview (Current)**
* OpenMetrics endpoint available for onboarding. 
* Both endpoints run in parallel with no changes required.

**General Availability [TBA]**:
* OpenMetrics endpoint becomes production-ready and the standard for metrics collection.

**Query Endpoint Deprecation (6 months after GA)**: 
* Prometheus query endpoint deprecated and eventually removed.

:::important Action Required

Complete migration before the 6 month deprecation window ends.

:::

## Notable Differences

### 1\. No longer use `rate()` in Prometheus queries

Metrics are now pre-computed as per-second rates with delta temporality.

**Before (Prometheus query endpoint)**:
```

Example 4 (unknown):
```unknown
**After (OpenMetrics endpoint)**:
```

---

## Implementation of a simple activity

**URL:** llms-txt#implementation-of-a-simple-activity

**Contents:**
  - 2. Create the Workflow
  - 3. Create and Run the Worker

class SayHelloActivity < Temporalio::Activity::Definition
  def execute(name)
    "Hello, #{name}!"
  end
end
ruby
require 'temporalio/workflow'
require_relative 'say_hello_activity'

class SayHelloWorkflow < Temporalio::Workflow::Definition
  def execute(name)
    Temporalio::Workflow.execute_activity(
      SayHelloActivity,
      name,
      schedule_to_close_timeout: 300
    )
  end
end
ruby
require 'temporalio/client'
require 'temporalio/worker'
require_relative 'say_hello_activity'
require_relative 'say_hello_workflow'

**Examples:**

Example 1 (unknown):
```unknown
### 2. Create the Workflow

Create a Workflow file (say_hello_workflow.rb):
```

Example 2 (unknown):
```unknown
### 3. Create and Run the Worker

With your Activity and Workflow defined, you need a Worker to execute them.
Workers are a crucial part of your Temporal application as they're what actually execute the tasks defined in your Workflows and Activities.
For more information on Workers, see [Understanding Temporal](/evaluate/understanding-temporal#workers) and a [deep dive into Workers](/workers).

Create a Worker file (worker.rb):
```

---

## Wait for first act result or sleep fut

**URL:** llms-txt#wait-for-first-act-result-or-sleep-fut

act_result = Temporalio::Workflow::Future.any_of(sleep_fut, *act_futs).wait

---

## Validate your ES environment

**URL:** llms-txt#validate-your-es-environment

---

## For better cache utilization, copy package.json and lock file first and install the dependencies before copying the

**URL:** llms-txt#for-better-cache-utilization,-copy-package.json-and-lock-file-first-and-install-the-dependencies-before-copying-the

---

## Use Python 3.11 slim image as base

**URL:** llms-txt#use-python-3.11-slim-image-as-base

FROM python:3.11-slim

---

## Average latency

**URL:** llms-txt#average-latency

rate(temporal_cloud_v0_service_latency_sum[$__rate_interval])
/ rate(temporal_cloud_v0_service_latency_count[$__rate_interval])

---

## Execute workflow synchronously

**URL:** llms-txt#execute-workflow-synchronously

**Contents:**
- Viewing Summary and Details in the UI
  - Workflow Overview Section
  - Event History
- Failure detection - Ruby SDK
- Raise and Handle Exceptions {#exception-handling}
- Failing Workflows {#workflow-failure}
- Workflow timeouts {#workflow-timeouts}
  - Workflow retries {#workflow-retries}
- Activity timeouts {#activity-timeouts}
  - Activity Retry Policy {#activity-retries}

result = client.execute_workflow(
  'YourWorkflow',
  'workflow input',
  id: 'your-workflow-id',
  task_queue: 'your-task-queue',
  static_summary: 'Order processing for customer #12345',
  static_details: 'Processing premium order with expedited shipping'
)
ruby
require 'temporalio'

class YourWorkflow < Temporalio::Workflow::Definition
  def execute(input)
    # Get the current details
    current_details = Temporalio::Workflow.current_details
    Temporalio::Workflow.logger.info("Current details: #{current_details}")
    
    # Set/update the current details
    Temporalio::Workflow.current_details = 'Updated workflow details with new status'
    
    'Workflow completed'
  end
end
ruby
require 'temporalio'

class YourWorkflow < Temporalio::Workflow::Definition
  def execute(input)
    # Execute an activity with a summary
    result = Temporalio::Workflow.execute_activity(
      'YourActivity',
      input,
      start_to_close_timeout: 10,
      summary: 'Processing user data'
    )
    
    result
  end
end
ruby
require 'temporalio'

class YourWorkflow < Temporalio::Workflow::Definition
  def execute(input)
    # Create a timer with a summary
    Temporalio::Workflow.sleep(300, summary: 'Waiting for payment confirmation')
    
    'Timer completed'
  end
end
ruby
class MyError < StandardError
end

class SomethingThatFails < Temporalio::Activity::Definition
  def execute(details)
    Temporalio::Activity::Context.current.logger.info(
      "We have a problem."
    )
    raise MyError.new('Simulated failure')
  end
end
ruby
class SomethingThatFails < Temporalio::Activity::Definition
  def execute(details)
    Temporalio::Activity::Context.current.logger.info(
      "We have a problem."
    )
    raise Temporalio::Error::ApplicationError.new('Simulated failure', type: 'MyError')
  end
end
ruby
class SomethingThatFails < Temporalio::Activity::Definition
  def execute(details)
    Temporalio::Activity::Context.current.logger.info(
      "We have a problem."
    )
    raise Temporalio::Error::ApplicationError.new('Simulated failure', non_retryable: true)
  end
end
ruby
class SagaWorkflow < Temporalio::Workflow::Definition
  def execute(details)
    Temporalio::Workflow.execute_activity(Activities::SomethingThatFails, details,start_to_close_timeout: 30)
  rescue StandardError
    raise Temporalio::Error::ApplicationError.new('Fail the Workflow')
ruby
result = my_client.execute_workflow(
  MyWorkflow, 'some-input',
  id: 'my-workflow-id', task_queue: 'my-task-queue',
  execution_timeout: 5 * 60
)
ruby
result = my_client.execute_workflow(
  MyWorkflow, 'some-input',
  id: 'my-workflow-id', task_queue: 'my-task-queue',
  retry_policy: Temporalio::RetryPolicy.new(max_interval: 10)
)
ruby
Temporalio::Workflow.execute_activity(
  MyActivity,
  { greeting: 'Hello', name: },
  start_to_close_timeout: 5 * 60
)
ruby
Temporalio::Workflow.execute_activity(
  MyActivity,
  { greeting: 'Hello', name: },
  start_to_close_timeout: 5 * 60,
  retry_policy: Temporalio::RetryPolicy.new(max_interval: 10)
)
ruby
raise Temporalio::Error::ApplicationError.new(
  'Some error',
  type: 'SomeErrorType',
  next_retry_delay: 3 * Temporalio::Activity::Context.current.info.attempt
)
ruby
class MyActivity < Temporalio::Activity::Definition
  def execute
    # This is a naive loop simulating work, but similar heartbeat logic
    # applies to other scenarios as well
    loop do
      # Send heartbeat
      Temporalio::Activity::Context.current.heartbeat
      # Sleep before heartbeating again
      sleep(3)
    end
  end
end
ruby
Temporalio::Workflow.execute_activity(
  MyActivity,
  { greeting: 'Hello', name: },
  start_to_close_timeout: 5 * 60,
  heartbeat_timeout: 5
)
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    # Whether this workflow waits on the activity to handle the cancellation or not is
    # dependent upon the cancellation_type parameter. We leave the default here which
    # sends the cancellation but does not wait on it to be handled.
    Temporalio::Workflow.execute_activity(MyActivity, start_to_close_timeout: 100)
  rescue Temporalio::Error => e
    # For this sample, we only want to execute cleanup when it's a cancellation
    raise unless Temporalio::Error.canceled?(e)

# Call a cleanup activity. We have to do this with a new/detached cancellation
    # because the default workflow-level one is already canceled at this point.
    Temporalio::Workflow.execute_activity(
      MyCleanupActivity,
      start_to_close_timeout: 100,
      cancellation: Temporalio::Cancellation.new
    )

# Re-raise the original exception
    raise
  end
end
ruby
class MyActivity < Temporalio::Activity::Definition
  def execute
    # This is a naive loop simulating work, but similar heartbeat/cancellation logic
    # applies to other scenarios as well
    loop do
      # Send heartbeat
      Temporalio::Activity::Context.current.heartbeat
      # Sleep before heartbeating again
      sleep(3)
    end
  rescue Temporalio::Error::CanceledError
    raise 'Canceled!'
  end
end
ruby

**Examples:**

Example 1 (unknown):
```unknown
#### Inside the Workflow

Within a Workflow, you can get and set the _current workflow details_. 
Unlike static summary/details set at Workflow start, this value can be updated throughout the life of the Workflow. 
Current Workflow details also takes Markdown format (excluding images, HTML, and scripts) and can span multiple lines.
```

Example 2 (unknown):
```unknown
#### Adding Summary to Activities and Timers

You can attach a `summary:` to activities when starting them from within a Workflow:
```

Example 3 (unknown):
```unknown
Similarly, you can attach a `summary:` to timers within a Workflow:
```

Example 4 (unknown):
```unknown
The input format for `summary:` is a string, and limited to 200 bytes.

## Viewing Summary and Details in the UI

Once you've added summaries and details to your Workflows, Activities, and Timers, you can view this enriched information in the Temporal Web UI. 
Navigate to your Workflow's details page to see the metadata displayed in two key locations:

### Workflow Overview Section

At the top of the workflow details page, you'll find the workflow-level metadata:

- **Summary & Details** - Displays the static summary and static details set when starting the workflow
- **Current Details** - Displays the dynamic details that can be updated during workflow execution

All Workflow details support standard Markdown formatting (excluding images, HTML, and scripts), allowing you to create rich, structured information displays.

### Event History

Individual events in the Workflow's Event History display their associated summaries when available:

Workflow, Activity and Timer summaries appear in purple text next to their corresponding Events, providing immediate context without requiring you to expand the event details. When you do expand an event, the summary is also prominently displayed in the detailed view.

---

## Failure detection - Ruby SDK

This page shows how to do the following:

- [Raise and Handle Exceptions](#exception-handling)
- [Deliberately Fail Workflows](#workflow-failure)
- [Set Workflow timeouts](#workflow-timeouts)
- [Set Workflow retries](#workflow-retries)
- [Set Activity timeouts](#activity-timeouts)
- [Set Activity Retry Policy](#activity-retries)
- [Heartbeat an Activity](#activity-heartbeats)
- [Set Heartbeat timeouts](#heartbeat-timeout)

## Raise and Handle Exceptions {#exception-handling}

In each Temporal SDK, error handling is implemented idiomatically, following the conventions of the language.
Temporal uses several different error classes internally — for example, [`CancelledError`](https://ruby.temporal.io/Temporalio/Error/CanceledError.html) in the Ruby SDK, to handle a Workflow cancellation. 
You should not raise or otherwise implement these manually, as they are tied to Temporal platform logic.

The one Temporal error class that you will typically raise deliberately is [`ApplicationError`](https://ruby.temporal.io/Temporalio/Error/ApplicationError.html).
In fact, *any* other exceptions that are raised from your Ruby code in a Temporal Activity will be converted to an `ApplicationError` internally.
This way, an error's type, severity, and any additional details can be sent to the Temporal Service, indexed by the Web UI, and even serialized across language boundaries.

In other words, these two code samples do the same thing:
```

---

## Start 3 activities in background

**URL:** llms-txt#start-3-activities-in-background

fut1 = Temporalio::Workflow::Future.new do
  Temporalio::Workflow.execute_activity(MyActivity1, schedule_to_close_timeout: 300)
end
fut2 = Temporalio::Workflow::Future.new do
  Temporalio::Workflow.execute_activity(MyActivity2, schedule_to_close_timeout: 300)
end
fut3 = Temporalio::Workflow::Future.new do
  Temporalio::Workflow.execute_activity(MyActivity3, schedule_to_close_timeout: 300)
end

---

## List the forwarding rule you created for the endpoint

**URL:** llms-txt#list-the-forwarding-rule-you-created-for-the-endpoint

gcloud compute forwarding-rules list \
  --filter="NAME:<endpoint-name>" \
  --format="value(IP_ADDRESS)"

---

## vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com

**URL:** llms-txt#vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com

**Contents:**
  - Updating your workers/clients
- Configure Private DNS for Multi-Region Namespaces
  - Customer side solutions
  - Setting up the DNS override
- Available AWS regions, PrivateLink endpoints, and DNS record overrides
- Google Private Service Connect Connectivity
- Requirements
- Creating a Private Service Connect connection
- Configuring Private DNS for GCP Private Service Connect
  - Why configure private DNS?

bash
dig payments.abcde.tmprl.cloud
go
clientOptions := client.Options{
    HostPort: "payments.abcde.tmprl.cloud:7233",
    Namespace: "payments",
    // No TLS SNI override needed
}
shell

**Examples:**

Example 1 (unknown):
```unknown
Save the **`vpce-*.amazonaws.com`** value -- you will target it in the CNAME record.

#### 2. Create a Route 53 Private Hosted Zone

1. Open _Route 53 → Hosted zones → Create hosted zone_.
2. Enter the domain chosen from the table above, e.g., `payments.abcde.tmprl.cloud`.
3. Type: _Private hosted zone for Temporal Cloud_.
4. Associate the hosted zone with every VPC that contains Temporal Workers and/or SDK clients.
5. Create hosted zone.

#### 3. Add a CNAME record

Inside the new PHZ:

| Field           | Value                                                                                 |
| --------------- | ------------------------------------------------------------------------------------- |
| **Record name** | the namespace endpoint (e.g., `payments.abcde.tmprl.cloud`).                          |
| **Record type** | `CNAME`                                                                               |
| **Value**       | Your VPC Endpoint DNS name (`vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com`) |
| **TTL**         | 60s is typical; 15s for MRN namespaces; adjust as needed.                             |

#### 4. Verify DNS resolution from inside the VPC
```

Example 2 (unknown):
```unknown
If the record resolves to the VPC Endpoint, you are ready to use Temporal Cloud without SNI overrides.

### Updating your workers/clients

With private DNS in place, configure your SDKs exactly as the public-internet examples show (filling in your own namespace):
```

Example 3 (unknown):
```unknown
The DNS resolver inside your VPC returns the private endpoint, while TLS still validates the original hostname—simplifying both code and certificate management.

## Configure Private DNS for Multi-Region Namespaces

:::tip Namespaces with High Availability features and AWS PrivateLink

Proper networking configuration is required for failover to be transparent to clients and workers when using PrivateLink.
This page describes how to configure routing for Namespaces with High Availability features on AWS PrivateLink.

:::

To use AWS PrivateLink with High Availability features, you may need to:

- Override the regional DNS zone.
- Ensure network connectivity between the two regions.

This page provides the details you need to set this up.

### Customer side solutions

When using PrivateLink, you connect to Temporal Cloud through a VPC Endpoint, which uses addresses local to your network.
Temporal treats each `region.<tmprl_domain>` as a separate zone.
This setup allows you to override the default zone, ensuring that traffic is routed internally for the regions you’re using.

A Namespace's active region is reflected in the target of a CNAME record.
For example, if the active region of a Namespace is AWS us-west-2, the DNS configuration would look like this:

| Record name                         | Record type | Value                            |
| ----------------------------------- | ----------- | -------------------------------- |
| ha-namespace.account-id.tmprl.cloud | CNAME       | aws-us-west-2.region.tmprl.cloud |

After a failover, the CNAME record will be updated to point to the failover region, for example:

| Record name                         | Record type | Value                            |
| ----------------------------------- | ----------- | -------------------------------- |
| ha-namespace.account-id.tmprl.cloud | CNAME       | aws-us-east-1.region.tmprl.cloud |

The Temporal domain did not change, but the CNAME updated from us-west-2 to us-east-1.

<CaptionedImage
    src="/img/cloud/high-availability/private-link.png"
    title="Customer side solution example"
    zoom="true"
/>

### Setting up the DNS override

To set up the DNS override, configure specific regions to target the internal VPC Endpoint IP addresses.
For example, you might set aws-us-west-1.region.tmprl.cloud to target 192.168.1.2.
In AWS, this can be done using a Route 53 private hosted zone for `region.tmprl.cloud`.
Link that private zone to the VPCs you use for Workers.

When your Workers connect to the Namespace, they first resolve the `<ns>.<acct>.<tmprl_domain>` record.
This points to `<aws-active-region>.region.tmprl.cloud`, which then resolves to your internal IP addresses.

Consider how you’ll configure Workers for this setup.
You can either have Workers run in both regions continuously or establish connectivity between regions using Transit Gateway or VPC Peering.
This way, Workers can access the newly activated region once failover occurs.

## Available AWS regions, PrivateLink endpoints, and DNS record overrides

The following table lists the available Temporal regions, PrivateLink endpoints, and regional endpoints used for DNS record overrides:

<AWSRegions />

---

## Google Private Service Connect Connectivity

[Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) allows you to open a path to Temporal without opening a public egress.
It establishes a private connection between your Google Virtual Private Cloud (VPC) and Temporal Cloud.
This one-way connection means Temporal cannot establish a connection back to your service.
This is useful if normally you block traffic egress as part of your security protocols.
If you use a private environment that does not allow external connectivity, you will remain isolated.

:::warning Namespaces with High Availability features and GCP Private Service Connect

Automatic failover via Temporal Cloud DNS is not currently supported with GCP Private Service Connect.
If you use GCP Private Service Connect, you must manually update your workers to point to the active region's Private Service Connect endpoint when a failover occurs.

:::

## Requirements

Your GCP Private Service Connect connection must be in the same region as your Temporal Cloud namespace. If using [replication for High Availability](/cloud/high-availability), the PSC connection must be in the same region as one of the replicas.

## Creating a Private Service Connect connection

Set up Private Service Connect with Temporal Cloud with these steps:

1. Open the Google Cloud console
2. Navigate to **Network Services**, then **Private Service Connect**. If you haven't used **Network Services** recently, you might have to find it by clicking on **View All Products** at the bottom of the left sidebar.

   ![GCP console showing Network Services, and the View All Products button](/img/cloud/gcp/gcp-console.png)

3. Go to the **Endpoints** section. Click on **Connect endpoint**.

   ![GCP console showing the endpoints, and the Connect endpoint button](/img/cloud/gcp/connect-endpoint-button.png)

4. Under **Target**, select **Published service**, this will change the contents of the form to allow you to fill the rest as described below

   ![GCP console showing the endpoints, and the Connect endpoint button](/img/cloud/gcp/connect-endpoint.png)

- For **Target service**, fill in the **Service name** with the Private Service Connect Service Name for the region you’re trying to connect to:

:::tip

GCP Private Service Connect services are regional.
Individual Namespaces do not use separate services.

:::

<JsonTable filename="/json/privatelink_gcp.json" />

- For **Endpoint name**, enter a unique identifier to use for this endpoint. It could be for instance `temporal-api` or `temporal-api-<namespace>` if you want a different endpoint per namespace.
- For **Network** and **Subnetwork**, choose the network and subnetwork where you want to publish your endpoint.
- For **IP address**, click the dropdown and select **Create IP address** to create an internal IP from your subnet dedicated to the endpoint. Select this IP.
- Check **Enable global access** if you intend to connect the endpoint to virtual machines outside of the selected region. We recommend regional connectivity instead of global access, as it can be better in terms of latency for your workers. _**Note:** this requires the network routing mode to be set to **GLOBAL**._

5. Click the **Add endpoint** button at the bottom of the screen.

6. [Create a Temporal Cloud Connectivity Rule](/cloud/connectivity#creating-a-connectivity-rule) using the Connection ID of the newly created endpoint and the corresponding GCP Project.

7. Once the status is "Accepted", the GCP Private Service Connect endpoint is ready for use.

- Take note of the **IP address** that has been assigned to your endpoint, as it will be used to connect to Temporal Cloud.

:::caution
You still need to set up private DNS or override client configuration for your clients to actually use the new Private Service Connect connection to connect to Temporal Cloud.

See [configuring private DNS for GCP Private Service Connect](#configuring-private-dns-for-gcp-private-service-connect)
:::

## Configuring Private DNS for GCP Private Service Connect

### Why configure private DNS?

When you connect to Temporal Cloud through GCP Private Service Connect you normally must:

1. **Point your SDKs/Workers at the Private Service Connect endpoint IP address** _and_
2. **Override the Server Name Indicator (SNI)** so that the TLS handshake still presents the public Temporal Cloud hostname (e.g., `my-namespace.my-account.tmprl.cloud`).

By creating a **private Cloud DNS zone (PZ)** that maps the public TemporalC Cloud hostname (or the region hostname) directly to the PSC endpoint IP address, you can:

- Keep using the standard Temporal Cloud hostnames in code and configuration.
- Eliminate the need to set a custom SNI override.
- Make future endpoint rotations transparent—only the DNS record changes.

This approach is **optional**; Temporal Cloud works without it. It simply streamlines configuration and operations. If you cannot use private DNS, refer to [our guide for updating the server and TLS settings on your clients](/cloud/connectivity#update-dns-or-clients-to-use-private-connectivity).

### Prerequisites

| Requirement                                           | Notes                                                                             |
| ----------------------------------------------------- | --------------------------------------------------------------------------------- |
| Google Cloud VPC Network with DNS enabled             | PSC endpoints and the DNS zone must live in (or be attached to) the same network. |
| Private Service Connect endpoint for Temporal Cloud   | Create an endpoint and reserve an internal IP in the namespace region             |
| Cloud DNS API enabled and roles/dns.admin permissions | Needed to create private zones and records.                                       |
| Namespace details                                     | Determines which hostname pattern you override (table below).                     |

### Choose the override domain and endpoint

| Temporal Cloud setup                       | Use this PHZ domain                | Example                                        |
| ------------------------------------------ | ---------------------------------- | ---------------------------------------------- |
| Single-region namespace with mTLS auth     | `<account>.tmprl.cloud`            | `payments.abcde.tmprl.cloud` ↔ `X.X.X.X`       |
| Single-region namespace with API-key auth  | `<cloud_provider>.api.temporal.io` | `us-central1.gcp.api.temporal.io` ↔ `X.X.X.X`  |
| Multi-region namespace | `region.tmprl.cloud`               | `gcp-us-central1.region.tmprl.cloud` ↔ `X.X.X.X` |

### Step-by-step instructions

#### 1. Collect your PSC endpoint IP address
```

---

## Do not need task scheduler for workflows

**URL:** llms-txt#do-not-need-task-scheduler-for-workflows

dotnet_diagnostic.CA2008.severity = none

---

## TYPE temporal_cloud_v1_frontend_service_pending_requests gauge

**URL:** llms-txt#type-temporal_cloud_v1_frontend_service_pending_requests-gauge

---

## ...

**URL:** llms-txt#...

**Contents:**
- Rails integration - Ruby SDK
- ActiveRecord
- Lazy/Eager Loading
- Schedules - Ruby SDK
- Schedule a Workflow {#schedule-a-workflow}
  - Create a Scheduled Workflow {#create-a-workflow}
  - Backfill a Scheduled Workflow {#backfill-a-scheduled-workflow}
  - Delete a Scheduled Workflow {#delete-a-scheduled-workflow}
  - Describe a Scheduled Workflow {#describe-a-scheduled-workflow}
  - List a Scheduled Workflow {#list-a-scheduled-workflow}

class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    # ...

Temporalio::Workflow.upsert_search_attributes(MY_KEYWORD_KEY.value_set('some-new-value'))

Cannot access File path from inside a workflow. If this is known to be safe, the code can be run in a Temporalio::Workflow::Unsafe.illegal_call_tracing_disabled block.
ruby
handle = my_client.create_schedule(
  'my_schedule_id',
  Temporalio::Client::Schedule.new(
    action: Temporalio::Client::Schedule::Action::StartWorkflow.new(
      MyWorkflow, 'some-input',
      id: 'my-workflow-id', task_queue: 'my-task-queue'
    ),
    spec: Temporalio::Client::Schedule::Spec.new(
      intervals: [
        Temporalio::Client::Schedule::Spec::Interval.new(
          every: 5 * 24 * 60 * 60.0, # 5 days
        )
      ]
    )
  )
)
ruby
handle = my_client.schedule_handle('my-schedule-id')
now = Time.now(in: 'UTC')
handle.backfill(
  Temporalio::Client::Schedule::Backfill.new(
    start_at: now - (4 * 60),
    end_at: now - (2 * 60),
    overlap: Temporalio::Client::Schedule::OverlapPolicy::ALLOW_ALL
  )
)
ruby
handle = my_client.schedule_handle('my-schedule-id')
handle.delete
ruby
handle = my_client.schedule_handle('my-schedule-id')
desc = handle.describe
puts "Schedule info: #{desc.info}"
ruby
my_client.list_schedules.each do |sched|
  puts "Schedule info: #{sched}"
end
ruby
handle = my_client.schedule_handle('my-schedule-id')
handle.pause(note: 'Pausing the schedule for now')
ruby
handle = my_client.schedule_handle('my-schedule-id')
handle.trigger
ruby
handle = my_client.schedule_handle('my-schedule-id')
handle.update do |input|
  # Return a new schedule with the action updated
  Temporalio::Client::Schedule::Update.new(
    schedule: input.description.schedule.with(
      # Update the action
      action: Temporalio::Client::Schedule::Action::StartWorkflow.new(
        MyNewWorkflow, 'some-new-input',
        id: 'my-workflow-id', task_queue: 'my-task-queue'
      )
    )
  )
end
ruby
handle = my_client.start_workflow(
  MyWorkflow, 'some-input',
  id: 'my-workflow-id', task_queue: 'my-task-queue',
  start_delay: 3 * 60 * 60 # 3 hours
)
```

## Set up your local with the Ruby SDK

**Examples:**

Example 1 (unknown):
```unknown
---

## Rails integration - Ruby SDK

Temporal Ruby SDK is a generic Ruby library that can work in any Ruby environment.
However, there are some common conventions for Rails users to be aware of.

See the [rails_app sample](https://github.com/temporalio/samples-ruby/tree/main/rails_app) for an example of using Temporal from Rails.

## ActiveRecord

For ActiveRecord, or other general/ORM models that are used for a different purpose, it is not recommended to try to reuse them as Temporal models.
Eventually model purposes diverge and models for a Temporal workflows/activities should be specific to their use for clarity and compatibility reasons.
Also many Ruby ORMs do many lazy things and therefore provide unclear serialization semantics.
Instead, consider having models specific for Workflows/Activities and translate to/from existing models as needed.
See the [ActiveModel section](/develop/ruby/converters-and-encryption#active-model) on how to do this with ActiveModel objects.

## Lazy/Eager Loading

By default, Rails eagerly loads all application code on application start in production, but lazily loads it in non-production environments.
Temporal Workflows by default disallow use of IO during the Workflow run.
With lazy loading enabled in dev/test environments, when an Activity class is referenced in a Workflow before it has been explicitly required, it can give an error like:
```

Example 2 (unknown):
```unknown
This comes from bootsnap via zeitwerk because it is lazily loading a class/module at Workflow runtime.
It is not good to lazily load code during a Workflow run because it can be side effecting.
Workflows and the classes they reference should be eagerly loaded.

To resolve this, either always eagerly load (e.g. `config.eager_load = true`) or explicitly require what is used by a workflow at the top of the file.

Note, this only affects non-production environments.

---

## Schedules - Ruby SDK

This page shows how to do the following:

- [Schedule a Workflow](#schedule-a-workflow)
  - [Create a Scheduled Workflow](#create-a-workflow)
  - [Backfill a Scheduled Workflow](#backfill-a-scheduled-workflow)
  - [Delete a Scheduled Workflow](#delete-a-scheduled-workflow)
  - [Describe a Scheduled Workflow](#describe-a-scheduled-workflow)
  - [List a Scheduled Workflow](#list-a-scheduled-workflow)
  - [Pause a Scheduled Workflow](#pause-a-scheduled-workflow)
  - [Trigger a Scheduled Workflow](#trigger-a-scheduled-workflow)
  - [Update a Scheduled Workflow](#update-a-scheduled-workflow)
- [Use Start Delay](#start-delay)

## Schedule a Workflow {#schedule-a-workflow}

Scheduling Workflows is a crucial aspect of automation.
By scheduling a Workflow, you can automate repetitive tasks, reduce manual intervention, and ensure timely execution.

Use the following actions to manage Scheduled Workflows.

### Create a Scheduled Workflow {#create-a-workflow}

The create action enables you to create a new Schedule. When you create a new Schedule, a unique Schedule ID is generated, which you can use to reference the Schedule in other Schedule commands.

To create a Scheduled Workflow Execution in Ruby, use the [create_schedule](https://ruby.temporal.io/Temporalio/Client.html#create_schedule-instance_method)
method on the Client.
Then pass the Schedule ID and the Schedule object to the method to create a Scheduled Workflow Execution.
Set the Schedule's `action` member to an instance of `Temporalio::Client::Schedule::Action::StartWorkflow` to schedule a Workflow Execution.
```

Example 3 (unknown):
```unknown
:::tip Schedule Auto-Deletion

Once a Schedule has completed creating all its Workflow Executions, the Temporal Service deletes it since it won’t fire again.
The Temporal Service doesn't guarantee when this removal will happen.

:::

### Backfill a Scheduled Workflow {#backfill-a-scheduled-workflow}

The backfill action executes Actions ahead of their specified time range. This command is useful when you need to execute a missed or delayed Action, or when you want to test the Workflow before its scheduled time.

To backfill a Scheduled Workflow Execution in Ruby, use the [backfill](https://ruby.temporal.io/Temporalio/Client/ScheduleHandle.html#backfill-instance_method)
method on the Schedule Handle.
```

Example 4 (unknown):
```unknown
### Delete a Scheduled Workflow {#delete-a-scheduled-workflow}

The delete action enables you to delete a Schedule. When you delete a Schedule, it does not affect any Workflows that were started by the Schedule.

To delete a Scheduled Workflow Execution in Ruby, use the [delete](https://ruby.temporal.io/Temporalio/Client/ScheduleHandle.html#delete-instance_method) method on the Schedule Handle.
```

---

## Add projects to the solution

**URL:** llms-txt#add-projects-to-the-solution

dotnet sln TemporalioHelloWorld.sln add Workflow/Workflow.csproj Worker/Worker.csproj Client/Client.csproj

---

## Print act result otherwise

**URL:** llms-txt#print-act-result-otherwise

**Contents:**
- Run Worker Process {#run-worker-process}

Temporalio::Workflow.logger.info("Act result: #{act_result}")
ruby

**Examples:**

Example 1 (unknown):
```unknown
There are several other details not covered here about futures, such as how exceptions are handled, how to use a setter
proc instead of a block, etc. See the [API documentation](https://ruby.temporal.io/Temporalio/Workflow/Future.html) for details.

## Run Worker Process {#run-worker-process}

The [Worker Process](/workers#worker-process) is where Workflow Functions and Activity Functions are actually executed.
In a Temporal application deployment, you ship and scale as many Workers as you need to handle the load of your Workflows and Activities.

- Each [Worker Entity](/workers#worker-entity) in the Worker Process must register the exact Workflow Types and Activity Types it may execute.
- Each Worker Entity must also associate itself with exactly one [Task Queue](/task-queue).
- Each Worker Entity polling the same Task Queue must be registered with the same Workflow Types and Activity Types.

A [Worker Entity](/workers#worker-entity) is the component within a Worker Process that listens to a specific Task Queue.

A Worker Entity contains a Workflow Worker and/or an Activity Worker, which makes progress on Workflow Executions and Activity Executions, respectively.

Workers are implemented in each Temporal SDK, and can be deployed with just a bit of boilerplate.
To create a Worker, use `Temporalio::Worker.new()`, providing the Worker options which include Task Queue, Workflows, and Activities and more.

The following code example creates a Worker that polls for tasks from the Task Queue and executes the Workflow.
When a Worker is created, it accepts a list of Workflows, a list of Activities, or both.
```

---

## set connection details

**URL:** llms-txt#set-connection-details

---

## HELP temporal_cloud_v1_frontend_service_error_count The number of gRPC errors returned by frontend service

**URL:** llms-txt#help-temporal_cloud_v1_frontend_service_error_count-the-number-of-grpc-errors-returned-by-frontend-service

---

## (Optional) initialize the default profile for local development

**URL:** llms-txt#(optional)-initialize-the-default-profile-for-local-development

temporal config set --prop address --value "localhost:7233"
temporal config set --prop namespace --value "default"

---

## Later, with different circumstances...

**URL:** llms-txt#later,-with-different-circumstances...

**Contents:**
  - Don't use Workflow Retry Policies
- Mark specific errors as non-retryable {#mark-errors-as-non-retryable}
- Specify non-retryable error types {#specify-non-retryable-error-types}
  - When to use each approach
- Implement rollback logic with the Saga pattern {#implement-saga-pattern}
- Understand Temporal's failure types {#understand-failure-types}
  - Common failure types
  - Workflow Task vs Workflow Execution failures
  - Protecting sensitive information
- Failure detection - Python SDK

await workflow.execute_activity(
    process_order,
    order,
    start_to_close_timeout=timedelta(seconds=10),
    retry_policy=slow_retry,
)
python
from temporalio import activity
from temporalio.exceptions import ApplicationError

@activity.defn
async def process_payment(card_number: str, amount: float):
    if not is_valid_card_format(card_number):
        # Invalid format will never become valid through retries
        raise ApplicationError(
            f"Invalid credit card format: {card_number}",
            type="InvalidCardFormat",
            non_retryable=True,
        )

if amount <= 0:
        # Invalid amount won't be fixed by retrying
        raise ApplicationError(
            f"Amount must be positive: {amount}",
            type="InvalidAmount",
            non_retryable=True,
        )

# Process payment...
python
from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

@workflow.defn
class CheckoutWorkflow:
    @workflow.run
    async def run(self, payment_details):
        retry_policy = RetryPolicy(
            non_retryable_error_types=[
                "InvalidCardFormat",
                "InsufficientFunds",
                "AccountClosed",
            ]
        )

try:
            result = await workflow.execute_activity(
                process_payment,
                payment_details,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )
            return result
        except ActivityError as e:
            workflow.logger.error(f"Payment failed: {e.cause}")
            # Handle the non-retryable error...
python
from temporalio import workflow
from temporalio.exceptions import ActivityError
from datetime import timedelta

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order):
        compensations = []

try:
            # Reserve inventory
            compensations.append({
                "activity": revert_inventory,
                "input": order
            })
            await workflow.execute_activity(
                reserve_inventory,
                order,
                start_to_close_timeout=timedelta(seconds=10),
            )

# Charge payment
            compensations.append({
                "activity": refund_payment,
                "input": order
            })
            payment_id = await workflow.execute_activity(
                charge_payment,
                order,
                start_to_close_timeout=timedelta(seconds=10),
            )

# Create shipment
            compensations.append({
                "activity": cancel_shipment,
                "input": payment_id
            })
            shipment_id = await workflow.execute_activity(
                create_shipment,
                order,
                start_to_close_timeout=timedelta(seconds=10),
            )

return {"payment_id": payment_id, "shipment_id": shipment_id}

except ActivityError as e:
            workflow.logger.error(f"Order failed: {e.cause}, rolling back...")

# Execute compensations in reverse order
            for compensation in reversed(compensations):
                try:
                    await workflow.execute_activity(
                        compensation["activity"],
                        compensation["input"],
                        start_to_close_timeout=timedelta(seconds=10),
                    )
                except ActivityError as comp_err:
                    # Log compensation failure but continue with others
                    workflow.logger.error(f"Compensation failed: {comp_err.cause}")

# Re-raise the original error
            raise ApplicationError(
                f"Order failed: {e.cause}",
                type="OrderFailed"
            )
python
if distance.kilometers > MAX_DELIVERY_DISTANCE:
    # Retrying won't change the distance - this is permanent
    raise ApplicationError(
        "Customer lives outside service area",
        type="OutsideServiceArea"
    )
python 
class MyCustomError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"

@activity.defn
async def my_activity(input: MyActivityInput):
    try:
        # Your activity logic goes here
    except Exception as e:
        raise MyCustomError(
            f"Error encountered on attempt {attempt}",
        ) from e
python 
from temporalio.exceptions import ApplicationError

@activity.defn
async def my_activity(input: MyActivityInput):
    try:
        # Your activity logic goes here
    except Exception as e:
        raise ApplicationError(
            type="MyCustomError",
            message=f"Error encountered on attempt {attempt}",
        ) from e
python
from temporalio.exceptions import ApplicationError

@activity.defn
async def my_activity(input: MyActivityInput):
    try:
        # Your activity logic goes here
    except Exception as e:
        raise ApplicationError(
            type="MyNonRetryableError",
            message=f"Error encountered on attempt {attempt}",
            non_retryable=True,
        ) from e
python
try:
	credit_card_confirmation = await workflow.execute_activity_method()
except ActivityError as e:
	workflow.logger.error(f"Unable to process credit card {e.message}")
	raise ApplicationError(
		"Unable to process credit card", "CreditCardProcessingError"
	)
python

**Examples:**

Example 1 (unknown):
```unknown
### Don't use Workflow Retry Policies

Unlike Activities, Workflows don't retry by default, and you usually shouldn't add a Retry Policy.
Workflows are deterministic and not designed for failure-prone operations.
A Workflow failure typically indicates a code bug or bad input data—retrying the entire Workflow repeats the same logic without fixing the underlying issue.

If you need retry logic for specific Workflow operations, implement it in your Workflow code rather than using a Workflow Retry Policy.

## Mark specific errors as non-retryable {#mark-errors-as-non-retryable}

**How to mark specific errors as non-retryable using the Temporal Python SDK**

Some failures are permanent and won't resolve through retries.
Mark these as non-retryable to fail fast instead of waiting for timeouts.

Set the `non_retryable` flag when raising an `ApplicationError`:
```

Example 2 (unknown):
```unknown
An `ApplicationError` with `non_retryable=True` will never retry, regardless of the Retry Policy.

Use non-retryable errors for:
- Invalid input data that prevents the Activity from proceeding
- Business rule violations
- Authorization failures

**Use this sparingly.**
In most cases, it's better to let the Retry Policy handle when to stop retrying based on time or attempts.

## Specify non-retryable error types {#specify-non-retryable-error-types}

**How to specify non-retryable error types in Retry Policies using the Temporal Python SDK**

Sometimes you want the Workflow (caller) to decide which error types shouldn't retry, rather than the Activity (implementer).

List error types that shouldn't retry in your Retry Policy:
```

Example 3 (unknown):
```unknown
When an Activity raises an `ApplicationError`, Temporal checks if its `type` is in `non_retryable_error_types`.
If it matches, the Activity fails immediately without retries.

### When to use each approach

**`non_retryable=True` in the Activity**: Use when the Activity implementer knows the error is permanently unrecoverable.
This enforces the constraint for all callers.

**`non_retryable_error_types` in the Retry Policy**: Use when the caller wants to decide which errors are unrecoverable based on their business logic.
This lets different Workflows make different decisions about the same Activity.

## Implement rollback logic with the Saga pattern {#implement-saga-pattern}

**How to implement the Saga pattern using the Temporal Python SDK**

The Saga pattern coordinates a sequence of operations where each operation has a compensating action to undo its effects.
If any operation fails, execute compensating actions in reverse order to roll back previous operations.

Use this for multi-step processes like:
- E-commerce checkout (payment, inventory, shipping)
- Distributed transactions across services
- Multi-stage data updates
```

Example 4 (unknown):
```unknown
Key points:
- Add compensating actions to a list **before** executing each Activity
- Use `reversed(compensations)` to undo operations in the correct order
- Handle compensation failures gracefully (they might fail too)
- Temporal manages all state and retry logic, making Saga implementation straightforward

## Understand Temporal's failure types {#understand-failure-types}

Temporal uses specialized exception types to represent different failure scenarios.
All exceptions inherit from [`TemporalError`](https://python.temporal.io/temporalio.exceptions.TemporalError.html).

**Do not extend `TemporalError` or its children.**
Use the provided exception types to ensure:
- Consistent behavior across process and language boundaries
- Compatibility with the Temporal Service
- Proper serialization via Protocol Buffers

### Common failure types

**`ApplicationError`**: Raised by your code to indicate application-specific failures.
This is the only Temporal exception you should raise manually.
When you raise an `ApplicationError`, you can optionally provide a `type` string and mark it as `non_retryable`.

**`ActivityError`**: Wraps exceptions raised from Activities.
The `cause` field contains the original error (`ApplicationError`, `TimeoutError`, `CancelledError`, etc.).
Catch this in Workflows to handle Activity failures.

**`TimeoutError`**: Occurs when an Activity or Workflow exceeds its configured timeout.

**`CancelledError`**: Results from cancellation of a Workflow, Activity, or Timer.
You can catch and ignore this to continue execution despite cancellation.

**`TerminatedError`**: Occurs when a Workflow Execution is forcefully terminated.

**`ChildWorkflowError`**: Raised when a Child Workflow Execution fails.

**`WorkflowAlreadyStartedError`**: Raised when attempting to start a Workflow with an ID that's already running.

**`ServerError`**: Used for exceptions from the Temporal Service itself (like database failures).

### Workflow Task vs Workflow Execution failures

**Workflow Task failures** occur when Workflow code raises a non-Temporal exception (like `ValueError`, `TypeError`, or non-determinism errors).
These retry automatically, letting you fix bugs and redeploy without losing Workflow state.

**Workflow Execution failures** occur when Workflow code raises a Temporal exception like `ApplicationError`.
These put the Workflow in "Failed" state with no automatic retries.

Example of a permanent failure that should fail the Workflow:
```

---

## Run the worker until SIGINT. There are other ways to wait for shutdown, or a block can

**URL:** llms-txt#run-the-worker-until-sigint.-there-are-other-ways-to-wait-for-shutdown,-or-a-block-can

---

## Import your Activity Definition and real implementation

**URL:** llms-txt#import-your-activity-definition-and-real-implementation

from hello.hello_activity import (
    ComposeGreetingInput,
    GreetingWorkflow,
    compose_greeting,
)

---

## Add project references

**URL:** llms-txt#add-project-references

dotnet add Worker/Worker.csproj reference Workflow/Workflow.csproj
dotnet add Client/Client.csproj reference Workflow/Workflow.csproj

---

## rest of the application and building.

**URL:** llms-txt#rest-of-the-application-and-building.

COPY . /app
WORKDIR /app

---

## Run the worker

**URL:** llms-txt#run-the-worker

**Contents:**
- Publish the Worker Image to Amazon ECR
- Deploy the Workers to EKS
- Verify that the Workers are Connected
- Temporal Worker Deployments
- Temporal Worker Controller
  - Why adopt the Worker Controller?
  - Features
- Configuring Worker Lifecycles
- Running the Temporal Worker Controller
- Worker Versioning (Worker-deployments)

CMD ["python", "worker.py"]
bash
docker buildx build \
    --platform linux/amd64 \
    -t your-app .
bash
export AWS_ACCOUNT_ID=<your_aws_account_id>
export AWS_REGION=<your_aws_region>
bash
aws ecr create-repository \
    --repository-name your-app
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin \
            $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
bash
docker tag your-app $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/your-app:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/your-app:latest
bash
kubectl create namespace your-namespace
yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: temporal-worker-config
  namespace: temporal-system
data:
  TEMPORAL_HOST_URL: “<your-temporal-address>“
  TEMPORAL_NAMESPACE: “<your-temporal-cloud-namespace>”
  TEMPORAL_TASK_QUEUE: “<your-task-queue>”
bash
kubectl apply -f config-map.yaml \
    --namespace your-namespace
bash
kubectl create secret generic temporal-secret \
    --from-literal=TEMPORAL_API_KEY=$TEMPORAL_API_KEY \
    --namespace your-namespace
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
   name: your-app
   namespace: your-namespace
   labels:
      app: your-app
spec:
   selector:
      matchLabels:
         app: your-app
   replicas: 1
   template:
      metadata:
         labels:
            app: your-app
      spec:
         serviceAccountName: your-app
         containers:
            - name: your-app
              image: <your-ecr-image-name>
              env:
                - name: TEMPORAL_ADDRESS
                  valueFrom:
                    configMapKeyRef:
                      name: temporal-worker-config
                      key: TEMPORAL_ADDRESS
                - name: TEMPORAL_NAMESPACE
                  valueFrom:
                    configMapKeyRef:
                      name: temporal-worker-config
                      key: TEMPORAL_NAMESPACE
                - name: TEMPORAL_TASK_QUEUE
                  valueFrom:
                    configMapKeyRef:
                      name: temporal-worker-config
                      key: TEMPORAL_TASK_QUEUE
                - name: TEMPORAL_API_KEY
                  valueFrom:
                    secretKeyRef:
                      name: temporal-secret
                      key: TEMPORAL_API_KEY
              resources:
                limits:
                  cpu: "0.5"
                  memory: "512Mi"
                requests:
                  cpu: "0.2"
                  memory: "256Mi"
bash
kubectl apply -f deployment.yaml \
    --namespace your-namespace

kubectl get pods -n temporal-system

kubectl logs <pod-name> -n temporal-system

Initializing worker...
Starting worker... Waiting for tasks.

rollout:
  strategy: Progressive
  steps:
    - rampPercentage: 1
      pauseDuration: 30s
    - rampPercentage: 10
      pauseDuration: 1m
  gate:
    workflowType: "HelloWorld"
bash
RELEASE=temporal-worker-controller
NAMESPACE=temporal-system
VERSION=1.0.0

helm install $RELEASE oci://docker.io/temporalio/helm-charts/temporal-worker-controller \
  --version $VERSION \
  --namespace $NAMESPACE \
  --create-namespace
  
helm install temporal-worker-controller ./helm/temporal-worker-controller \
  --namespace $NAMESPACE \
  --create-namespace 
go
buildID:= mustGetEnv("MY_BUILD_ID")
w := worker.New(c, myTaskQueue, worker.Options{
  DeploymentOptions: worker.DeploymentOptions{
    UseVersioning: true,
    Version: worker.WorkerDeploymentVersion{
      DeploymentName: "llm_srv",
      BuildId:        buildID,
    },
    DefaultVersioningBehavior: workflow.VersioningBehaviorUnspecified,
  },
})
java

WorkerOptions.newBuilder()
  .setDeploymentOptions(
      WorkerDeploymentOptions.newBuilder()
      .setVersion(new WorkerDeploymentVersion("llm_srv", "1.0"))
      .setUseVersioning(true)
      .setDefaultVersioningBehavior(VersioningBehavior.AUTO_UPGRADE)
      .build())
  .build();

python
from temporalio.common import WorkerDeploymentVersion, VersioningBehavior
from temporalio.worker import Worker, WorkerDeploymentConfig

Worker(
    client,
    task_queue="mytaskqueue",
    workflows=workflows,
    activities=activities,
    deployment_config=WorkerDeploymentConfig(
        version=WorkerDeploymentVersion(
            deployment_name="llm_srv",
            build_id=my_env.build_id),
        use_worker_versioning=True,
        default_versioning_behavior=VersioningBehavior.UNSPECIFIED
    ),
)
ts
const myWorker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  taskQueue,
  workerDeploymentOptions: {
    useWorkerVersioning: true,
    version: { buildId: '1.0', deploymentName: 'llm_srv' },

defaultVersioningBehavior: 'UNSPECIFIED',
  },
  connection: nativeConnection,
});
csharp
var myWorker = new TemporalWorker(
    Client,
    new TemporalWorkerOptions(taskQueue)
    {DeploymentOptions = new(new("llm_srv", "1.0"), true)
      { DefaultVersioningBehavior = VersioningBehavior.Unspecified },
    }.AddWorkflow<MyWorkflow>());
ruby
worker = Temporalio::Worker.new(
  client: client,
  task_queue: task_queue,
  workflows: [MyWorkflow],
  deployment_options: Temporalio::Worker::DeploymentOptions.new(
      version: Temporalio::WorkerDeploymentVersion.new(
          deployment_name: 'llm_srv',
          build_id: '1.0'
      ),
      use_worker_versioning: true,
      default_versioning_behavior: Temporalio::VersioningBehavior::UNSPECIFIED
  )
)
bash
temporal worker deployment describe --name="$MY_DEPLOYMENT"
bash
temporal worker deployment set-current-version \
    --deployment-name "YourDeploymentName" \
    --build-id "YourBuildID"
bash
temporal worker deployment set-ramping-version \
    --deployment-name "YourDeploymentName" \
    --build-id "YourBuildID" \
    --percentage=5
bash
temporal workflow describe -w YourWorkflowID

Behavior               AutoUpgrade
  Version                llm_srv.2.0
  OverrideBehavior       Unspecified
go
// w is the Worker configured as in the previous example
w.RegisterWorkflowWithOptions(HelloWorld, workflow.RegisterOptions{
	// or workflow.VersioningBehaviorAutoUpgrade
    VersioningBehavior: workflow.VersioningBehaviorPinned,
})
java
@WorkflowInterface
public interface HelloWorld {
    @WorkflowMethod
    String hello();
}

public static class HelloWorldImpl implements HelloWorld {
    @Override
    @WorkflowVersioningBehavior(VersioningBehavior.PINNED)
    public String hello() {
        return "Hello, World!";
    }
}
python
@workflow.defn(versioning_behavior=VersioningBehavior.PINNED)
class HelloWorld:
    @workflow.run
    async def run(self):
        return "hello world!"
ts
setWorkflowOptions({ versioningBehavior: 'PINNED' }, helloWorld);
export async function helloWorld(): Promise<string> {
  return 'hello world!';
}
csharp
[Workflow(VersioningBehavior = VersioningBehavior.Pinned)]
public class HelloWorld
{
    [WorkflowRun]
    public async Task<string> RunAsync()
    {
        return "hello world!";
    }
}
ruby
class HelloWorld < Temporalio::Workflow::Definition
  workflow_versioning_behavior Temporalio::VersioningBehavior::PINNED

def execute
    'hello world!'
  end
end
bash
temporal workflow update-options \
    --workflow-id "$WORKFLOW_ID" \
    --versioning-override-behavior pinned \
    --versioning-override-deployment-name "$TARGET_DEPLOYMENT" \
    --versioning-override-build-id "$TARGET_BUILD_ID"
bash
temporal workflow update-options \
  --query="TemporalWorkerDeploymentVersion=$TARGET_DEPLOYMENT:$BAD_BUILD_ID" \
  --versioning-override-behavior pinned \
  --versioning-override-deployment-name "$TARGET_DEPLOYMENT" \
  --versioning-override-build-id "$FIXED_BUILD_ID"
bash
temporal workflow reset with-workflow-update-options \
    --workflow-id "$WORKFLOW_ID" \
    --event-id "$EVENT_ID" \
    --reason "$REASON" \
    --versioning-override-behavior pinned \
    --versioning-override-deployment-name "$TARGET_DEPLOYMENT" \
    --versioning-override-build-id "$TARGET_BUILD_ID"
bash
temporal workflow update-options \
    --workflow-id "$WORKFLOW_ID" \
    --versioning-override-behavior auto_upgrade
bash
temporal workflow update-options \
    --query="WorkflowType='$WORKFLOW_TYPE'" \
    --versioning-override-behavior auto_upgrade
bash
temporal workflow update-options \
    --query="WorkflowType='$WORKFLOW_TYPE' AND TemporalWorkerDeploymentVersion='$TARGET_DEPLOYMENT:$OLD_VERSION'" \
    --versioning-override-behavior auto_upgrade
bash
temporal worker deployment describe-version \
    --deployment-name "YourDeploymentName" \
    --build-id "YourBuildID"

Worker Deployment Version:
  Version                  llm_srv.1.0
  CreateTime               5 hours ago
  RoutingChangedTime       32 seconds ago
  RampPercentage           0
  DrainageStatus           draining
  DrainageLastChangedTime  31 seconds ago
  DrainageLastCheckedTime  31 seconds ago

Task Queues:
     Name        Type
  hello-world  activity
  hello-world  workflow
go
workflowOptions := client.StartWorkflowOptions{
	ID:        "MyWorkflowId",
	TaskQueue: "MyTaskQueue",
	VersioningOverride: &client.PinnedVersioningOverride{
        Version: worker.WorkerDeploymentVersion{
            DeploymentName: "DeployName",
            BuildId:        "1.0",
        },
    },
}
// c is an initialized Client
we, err := c.ExecuteWorkflow(context.Background(), workflowOptions, HelloWorld, "Hello")
java
MyWorkflow handle = client.newWorkflowStub(
    MyWorkflow.class,
    WorkflowOptions.newBuilder()
        .setWorkflowId("MyWorkflowId")
        .setTaskQueue("MyTaskQueue")
        .setVersioningOverride(new VersioningOverride.PinnedVersioningOverride(
            new WorkerDeploymentVersion("DeployName", "1.0")))
        .build()
);
WorkflowExecution we = WorkflowClient.start(handle::execute, "Hello");
python
handle = client.start_workflow(
    MyWorkflow.run,
    "Hello",
    id="MyWorkflowId",
    task_queue="MyTaskQueue",
    versioning_override=PinnedVersioningOverride(
        WorkerDeploymentVersion("DeployName", "1.0")
    ),
)
ts
const handle = await client.workflow.start('helloWorld', {
  taskQueue: 'MyTaskQueue',
  workflowId: 'MyWorkflowId',
  versioningOverride: {
    pinnedTo: { buildId: '1.0', deploymentName: 'deploy-name' },
  },
});
csharp
var workerV1 = new WorkerDeploymentVersion("deploy-name", "1.0");
var handle = await Client.StartWorkflowAsync(
    (HelloWorld wf) => wf.RunAsync(),
      	new(id: "MyWorkflowId", taskQueue: "MyTaskQueue")
      	{
           VersioningOverride = new VersioningOverride.Pinned(workerV1),
        }
);
ruby
worker_v1 = Temporalio::WorkerDeploymentVersion.new(
  deployment_name: 'deploy-name',
  build_id: '1.0'
)
handle = env.client.start_workflow(
  HelloWorld,
  id: 'MyWorkflowId',
  task_queue: 'MyTaskQueue',
  versioning_override: Temporalio::VersioningOverride.pinned(worker_v1)
)
yaml
global:
  membership:
    broadcastAddress: '127.0.0.1'
  metrics:
    prometheus:
      framework: 'tally'
      listenAddress: '127.0.0.1:8000'
yaml
global:
  tls:
    frontend:
      server:
        certFile: /path/to/cert/file
        keyFile: /path/to/key/file
      client:
        serverName: dnsSanInFrontendCertificate
yaml
global:
  tls:
    frontend:
      server:
        certFile: /path/to/cert/file
        keyFile: /path/to/key/file
      client:
        serverName: dnsSanInFrontendCertificate
        rootCaFiles:
          - /path/to/frontend/server/CA/files
yaml
global:
  tls:
    internode:
      server:
        certFile: /path/to/internode/cert/file
        keyFile: /path/to/internode/key/file
        requireClientAuth: true
        clientCaFiles:
          - /path/to/internode/serverCa
      client:
        serverName: dnsSanInInternodeCertificate
        rootCaFiles:
          - /path/to/internode/serverCa
    frontend:
      server:
        certFile: /path/to/frontend/cert/file
        keyFile: /path/to/frontend/key/file
        requireClientAuth: true
        clientCaFiles:
          - /path/to/internode/serverCa
          - /path/to/sdkClientPool1/ca
          - /path/to/sdkClientPool2/ca
      client:
        serverName: dnsSanInFrontendCertificate
        rootCaFiles:
          - /path/to/frontend/serverCa
yaml
persistence:
  defaultStore: default
  visibilityStore: cass-visibility # The primary Visibility store.
  secondaryVisibilityStore: es-visibility # A secondary Visibility store added to enable Dual Visibility.
  numHistoryShards: 512
  datastores:
    default:
      cassandra:
        hosts: '127.0.0.1'
        keyspace: 'temporal'
        user: 'username'
        password: 'password'
    cass-visibility:
      cassandra:
        hosts: '127.0.0.1'
        keyspace: 'temporal_visibility'
    es-visibility:
      elasticsearch:
        version: 'v7'
        logLevel: 'error'
        url:
          scheme: 'http'
          host: '127.0.0.1:9200'
        indices:
          visibility: temporal_visibility_v1_dev
        closeIdleConnectionsInterval: 15s
yaml
clusterMetadata:
  enableGlobalNamespace: true
  failoverVersionIncrement: 10
  masterClusterName: 'active'
  currentClusterName: 'active'
  clusterInformation:
    active:
      enabled: true
      initialFailoverVersion: 0
      rpcAddress: '127.0.0.1:7233'
  #replicationConsumer:
  #type: kafka
yaml
services:
  frontend:
    rpc:
      grpcPort: 8233
      membershipPort: 8933
      bindOnIP: '0.0.0.0'
yaml
publicClient:
  hostPort: 'localhost:8933'
yaml
  # Cluster-level Archival config enabled
  archival:
    # Event History configuration
    history:
      # Archival is enabled for the History Service data.
      state: 'enabled'
      enableRead: true
      # Namespaces can use either the local filestore provider or the Google Cloud provider.
      provider:
        filestore:
          fileMode: '0666'
          dirMode: '0766'
        gstorage:
          credentialsPath: '/tmp/gcloud/keyfile.json'
    # Configuration for archiving Visibility data.
    visibility:
      # Archival is enabled for Visibility data.
      state: 'enabled'
      enableRead: true
      provider:
        filestore:
          fileMode: '0666'
          dirMode: '0766'
  yaml
  # Cluster-level Archival config disabled
  archival:
    history:
      state: 'disabled'
      enableRead: false
    visibility:
      state: 'disabled'
      enableRead: false

namespaceDefaults:
    archival:
      history:
        state: 'disabled'
      visibility:
        state: 'disabled'
  yaml

**Examples:**

Example 1 (unknown):
```unknown
Build the Docker image and target the `linux/amd64` architecture:
```

Example 2 (unknown):
```unknown
## Publish the Worker Image to Amazon ECR

After building the Docker image, you’re ready to publish it to Amazon ECR.
Make sure that you’re authenticated with AWS, and that you’ve set your `AWS_REGION` and `AWS_ACCOUNT_ID` environment variables:
```

Example 3 (unknown):
```unknown
Create an ECR repository and authenticate ECR with the Docker container client:
```

Example 4 (unknown):
```unknown
After authenticating Docker with ECR, tag your container and publish it:
```

---

## Combining different types, with poller autoscaling

**URL:** llms-txt#combining-different-types,-with-poller-autoscaling

**Contents:**
  - .NET C# SDK
- Workflow Cache Tuning
- Available Task Queue information {#task-queue-metrics}
  - `ApproximateBacklogCount` and `ApproximateBacklogAge` {#ApproximateBacklogCountAndAge}
  - `TasksAddRate` and `TasksDispatchRate` {#TasksAddRate-and-TasksDispatchRate}
  - `BacklogIncreaseRate` {#BacklogIncreaseRate}
- Evaluate Task Queue performance {#evaluate-worker-loads}
  - Query Task Queue info with Temporal CLI {#cli-task-queue-info}
  - Query Task Queue info with the Go SDK {#go-sdk-task-queue-info}
  - Evaluate Worker availability and capacity issues {#worker-capacity-issues}

resource_based_options = ResourceBasedTunerConfig(0.8, 0.9)
tuner = WorkerTuner.create_composite(
    workflow_supplier=FixedSizeSlotSupplier(10),
    activity_supplier=ResourceBasedSlotSupplier(
        ResourceBasedSlotConfig(),
        resource_based_options,
    ),
    local_activity_supplier=ResourceBasedSlotSupplier(
        ResourceBasedSlotConfig(),
        resource_based_options,
    ),
)
worker = Worker(
    client,
    task_queue="foo",
    tuner=tuner,
    workflow_task_poller_behavior=PollerBehaviorAutoscaling(),
    activity_task_poller_behavior=PollerBehaviorAutoscaling()
)
csharp
// Just resource based
var worker = new TemporalWorker(
    Client,
    new TemporalWorkerOptions("my-task-queue")
    {
        Tuner = WorkerTuner.CreateResourceBased(0.8, 0.9),
    });
// Combining different types
var resourceTunerOptions = new ResourceBasedTunerOptions(0.8, 0.9);
var worker = new TemporalWorker(
    Client,
    new TemporalWorkerOptions("my-task-queue")
    {
        Tuner = new WorkerTuner(
             new FixedSizeSlotSupplier(10),
             new ResourceBasedSlotSupplier(
                 new ResourceBasedSlotSupplierOptions(),
                 resourceTunerOptions),
             new ResourceBasedSlotSupplier(
                 new ResourceBasedSlotSupplierOptions(),
                 resourceTunerOptions)),
    });

TasksAddRate - TasksDispatchRate

temporal task-queue describe \
    --task-queue YourTaskQueueName \
    [additional options]
go
for _, taskQueueName := range taskQueueNames {
        resp, err := s.client.DescribeTaskQueueEnhanced(ctx, client.DescribeTaskQueueEnhancedOptions{
            TaskQueue:   taskQueueName,
            ReportStats: true,
        })
        if err != nil {
            log.Printf("Error describing task queue %s: %v", taskQueueName, err)
        }

// Get the backlog count from the enhanced response
        backlogCount += getBacklogCount(resp)
    }
go
c, err := client.Dial(client.Options{
	// Set DataConverter here to ensure that workflow inputs and results are
	// encoded as required.
	DataConverter: mycustom.DataConverter,
	FailureConverter: temporal.NewDefaultFailureConverter(temporal.DefaultFailureConverterOptions{
		EncodeCommonAttributes: true,
	}),
})
go
defaultDataConverter = NewCompositeDataConverter(
    NewNilPayloadConverter(),
    NewByteSlicePayloadConverter(),
    NewProtoJSONPayloadConverter(),
    NewProtoPayloadConverter(),
    NewJSONPayloadConverter(),
)

temporal workflow describe

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
  LastAttemptFailure       {"message":"handler error (INTERNAL): internal error","applicationFailureInfo":{}}

temporal workflow describe

URL               https://nexus.phil-caller-Namespace.a2dd6.cluster.tmprl.cloud:7243/Namespaces/phil-caller-Namespace.a2dd6/nexus/callback
  Trigger           WorkflowClosed
  State             Succeeded
  Attempt           1
  RegistrationTime  32 minutes ago
sh
temporal workflow describe -w my-workflow-id
sh
Execution Info:
  WorkflowId            my-workflow-id
  ...

Pending Activities: 0
Pending Child Workflows: 0
Pending Nexus Operations: 1

Endpoint                 my-nexus-endpoint
  Service                  nexus-playground
  Operation                sync-op-ok
  OperationToken
  State                    Blocked
  Attempt                  1
  ScheduleToCloseTimeout   1d 0h 0m 0s
  LastAttemptCompleteTime  56 seconds ago
  LastAttemptFailure       {"message":"handler error (UPSTREAM_TIMEOUT): upstream timeout","cause":{"message":"upstream timeout","applicationFailureInfo":{"type":"NexusFailure"}},"applicationFailureInfo":{"type":"NexusHandlerError"}}
  BlockedReason            The circuit breaker is open.
sh
Execution Info:
  WorkflowId            my-workflow-id
  ...

Pending Activities: 0
Pending Child Workflows: 0
Pending Nexus Operations: 1

Endpoint                            my-nexus-endpoint
  Service                             nexus-playground
  Operation                           async-op-workflow-wait-for-cancel
  OperationToken                      eyJ2IjowLCJ0IjoxLCJucyI6Im5zIiwid2lkIjoidyJ
  State                               Started
  Attempt                             1
  ScheduleToCloseTimeout              1d 0h 0m 0s
  LastAttemptCompleteTime             51 seconds ago
  CancelationState                    Blocked
  CancelationAttempt                  5
  CancelationRequestedTime            37 seconds ago
  CancelationLastAttemptCompleteTime  27 seconds ago
  CancelationLastAttemptFailure       {"message":"handler error (UPSTREAM_TIMEOUT): upstream timeout","cause":{"message":"upstream timeout","applicationFailureInfo":{"type":"NexusFailure"}},"applicationFailureInfo":{"type":"NexusHandlerError"}}
  CancelationBlockedReason            The circuit breaker is open.
go
func main() {
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create client", err)
	}
	defer c.Close()

w := worker.New(c, taskQueue, worker.Options{})
	service := nexus.NewService(service.HelloServiceName)
	err = service.Register(handler.EchoOperation, handler.HelloOperation)
	if err != nil {
		log.Fatalln("Unable to register operations", err)
	}
	w.RegisterNexusService(service)
	w.RegisterWorkflow(handler.HelloHandlerWorkflow)

err = w.Run(worker.InterruptCh())
	if err != nil {
		log.Fatalln("Unable to start worker", err)
	}
}

Initial Interval     = 1 second
Backoff Coefficient  = 2.0
Maximum Interval     = 100 × Initial Interval
Maximum Attempts     = ∞
Non-Retryable Errors = []

func LoanApplicationWorkflow {

sdk.ExecuteActivity(CreditCheck)

sdk.ExecuteActivity(AutomatedApproval)

sdk.ExecuteActivity(NotifyApplicant)

func LoanApplicationWorkflow {

options = {
        MaxAttempts: 3,
        StartToCloseTimeout: 30min,
        HeartbeatTimeout: 10min,
    }

sdk.ExecuteActivity(CreditCheck, options)

sdk.ExecuteActivity(AutomatedApproval)

sdk.ExecuteActivity(NotifyApplicant)

// ...
}
go
package main

"go.temporal.io/sdk/client"
)

func main() {
	// Temporal Client setup code
	c, err := client.NewClient(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create client", err)
	}
	defer c.Close()
	// Prepare Workflow option and parameters
	workflowOptions := client.StartWorkflowOptions{
		ID:        "loan-application-1",
		TaskQueue: "loan-application-task-queue",
	}
	applicantDetails := ApplicantDetails{
		// ...
	}
	// Start the Workflow
	workflowRun, err := c.ExecuteWorkflow(context.Background(), workflowOptions, "loan-application-workflow", applicantDetails)
	if err != nil {
		// ...
	}
	// ...
}
go
func LoanApplication(ctx context.Context) (error) {
    // ...
	return nil
}
go
func LoanApplication(ctx workflow.Context, input *LoanApplicationWorkflowInput) (*LoanApplicationWorkflowResult, error) {
	// ...
	var result activities.CreditCheckResult
	f := workflow.ExecuteActivity(ctx, a.CreditCheck, CreditCheckInput(*input))
	err := f.Get(ctx, &result)
	// ...
	// Return the results
	return &loanApplicationResults, nil
}
go
// LoanApplicationWorkflow is the workflow definition.
func LoanApplicationWorkflow(ctx workflow.Context, applicantName string, loanAmount int) (string, error) {
	// Step 1: Notify the applicant that the application process has started
	err := workflow.ExecuteActivity(ctx, NotifyApplicantActivity, applicantName, "Application process started").Get(ctx, nil)
	if err != nil {
		return "", err
	}

// Step 2: Perform a credit check
	var creditCheckResult string
	err = workflow.ExecuteActivity(ctx, LoanCreditCheckActivity, loanAmount).Get(ctx, &creditCheckResult)
	if err != nil {
		return "", err
	}

// Step 3: Perform an automatic approval check
	var approvalCheckResult string
	err = workflow.ExecuteActivity(ctx, AutomaticApprovalCheckActivity, creditCheckResult).Get(ctx, &approvalCheckResult)
	if err != nil {
		return "", err
	}

// Step 4: Notify the applicant of the decision
	var notificationResult string
	err = workflow.ExecuteActivity(ctx, NotifyApplicantActivity, applicantName, approvalCheckResult).Get(ctx, &notificationResult)
	if err != nil {
		return "", err
	}

return notificationResult, nil
}
go
func main() {
    // Create the client object just once per process
    c, err := client.NewClient(client.Options{})
    if err != nil {
        log.Fatalln("Unable to create Temporal client", err)
    }
    defer c.Close()

// Create the Worker instance
    w := worker.New(c, "loan-application-task-queue", worker.Options{})

// Register the workflow and activity with the worker
    w.RegisterWorkflow(LoanApplicationWorkflow)
    w.RegisterActivity(LoanCreditCheck)

// Start listening to the Task Queue
    err = w.Run(worker.InterruptCh())
    if err != nil {
        log.Fatalln("Unable to start Worker", err)
    }
}
go
// LoanApplicationWorkflow is the Workflow Definition.
func LoanApplicationWorkflow(ctx workflow.Context, applicantName string, loanAmount int) (string, error) {
    // ...
    var creditCheckResult string
    // set a Retry Policy
    ao := workflow.ActivityOptions{
		ScheduleToCloseTimeout: time.Hour,
		HeartbeatTimeout:       time.Minute,
		RetryPolicy:            &temporal.RetryPolicy{
			InitialInterval:    time.Second,
			BackoffCoefficient: 2,
			MaximumInterval:    time.Minute,
			MaximumAttempts:    5,
		},
	}
    ctx = workflow.WithActivityOptions(ctx, ao)
    err = workflow.ExecuteActivity(ctx, LoanCreditCheckActivity, loanAmount).Get(ctx, &creditCheckResult)
    if err != nil {
        return "", err
    }
	// ...
    return notificationResult, nil
}

// LoanCreditCheckActivity is an Activity function that performs a credit check.
func LoanCreditCheckActivity(ctx context.Context, loanAmount int) (string, error) {
	// ... your logic here ...
	return "Credit check passed", nil
}
go
func LoanApplication(ctx workflow.Context, input *LoanApplicationWorkflowInput) (*LoanApplicationWorkflowResult, error) {

ctx = workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
		StartToCloseTimeout: time.Minute,
	})

var result activities.NotifyApplicantActivityResult
	f := workflow.ExecuteActivity(ctx, a.NotifyApplicantActivity, NotifyApplicantActivityInput(*input))

err := f.Get(ctx, &result)

// Return the results
	return &l.LoanApplicationState, nil
}

type Activities struct {}

func (a *Activities) NotifyApplicantActivity(ctx context.Context, input *NotifyApplicantActivityInput) (*NotifyApplicantActivityResult, error) {
	var result NotifyApplicantActivityResult

// Call the thirdparty API and handle the result

return &result, err
}

namespace α's version is 1
all workflows events generated within this namespace, will come with version 1

namespace β's version is 2
all workflows events generated within this namespace, will come with version 2

namespace α's version is 2
all workflows events generated within this namespace, will come with version 2

namespace β's version is 11
all workflows events generated within this namespace, will come with version 11

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 1               | 1       |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 3               | 1       |
| 2        | 1               |                 |         |
| 3        | 1               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 3               | 1       |
| 2        | 1               | 4               | 2       |
| 3        | 1               |                 |         |
| 4        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 3               | 1       |
| 2        | 1               | 5               | 2       |
| 3        | 1               |                 |         |
| 4        | 2               |                 |         |
| 5        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               | 3               | 2       |
| 3        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               | 4               | 2       |
| 3        | 2               |                 |         |
| 4        | 2               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- | --------------- | ------- |
| Events   | Version History |
| -------- | --------------- | --------------- | ------- |
| Event ID | Event Version   | Event ID        | Version |
| -------- | -------------   | --------------- | ------- |
| 1        | 1               | 2               | 1       |
| 2        | 1               | 3               | 2       |
| 3        | 2               | 4               | 3       |
| 4        | 3               |                 |         |
| -------- | -------------   | --------------- | ------- |

| -------- | ------------- |
                | Events        |
                | ------------- | ------------- |
                | Event ID      | Event Version |
                | --------      | ------------- |
                | 1             | 1             |
                | 2             | 1             |
                | 3             | 2             |
                | --------      | ------------- |
                |               |
                | ------------- | ------------  |
                |               |
                | --------      | ------------- |  | -------- | ------------- |
                | Event ID      | Event Version |  | Event ID | Event Version |
                | --------      | ------------- |  | -------- | ------------- |
                | 4             | 2             |  | 4        | 3             |
                | --------      | ------------- |  | -------- | ------------- |

| --------------- | ------- |
          | Version History |
          | --------------- | ------------------- |
          | Event ID        | Version             |
          | --------------- | -------             |
          | 2               | 1                   |
          | 3               | 2                   |
          | --------------- | -------             |
          |                 |
          | -------         | ------------------- |
          |                 |
          | --------------- | -------             |  | --------------- | ------- |
          | Event ID        | Version             |  | Event ID        | Version |
          | --------------- | -------             |  | --------------- | ------- |
          | 4               | 2                   |  | 4               | 3       |
          | --------------- | -------             |  | --------------- | ------- |

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

| -------- | ------------- |
| Events        |
| ------------- | -------------------------------------------- |
| Event ID      | Event Version                                |
| --------      | -------------                                |
| 1             | 1                                            |
| 2             | 1                                            |
| 3             | 2                                            |
| --------      | -------------                                |
|               |
| ------------- | -------------------------------------------- |
|               |
| --------      | -------------                                |                                  | -------- | ------------- |
| Event ID      | Event Version                                |                                  | Event ID | Event Version |
| --------      | -------------                                |                                  | -------- | ------------- |
| 4             | 2                                            | <-- task A belongs to this event | 4        | 3             | <-- current branch / mutable state |
| --------      | -------------                                |                                  | -------- | ------------- |

my-business-id-foobar
my business id foobar

Description = 'foobar'

// Doesn't match
Description = 'foo'

order-
  order-1234
  order-abracadabra
  order-~~~abracadabra
  
  order-
  order-1234
  order-abracadabra
  
WorkflowType = "main.YourWorkflowDefinition" and ExecutionStatus != "Running" and (StartTime > "2021-06-07T16:46:34.236-08:00" or CloseTime > "2021-06-07T16:46:34-08:00")
sql
WorkflowId = '<workflow-id>'
sql
WorkflowId = '<workflow-id>' or WorkflowId = '<another-workflow-id>'
sql
WorkflowId IN ('<workflow-id>', '<another-workflow-id>')
sql
WorkflowId = '<workflow-id>' and ExecutionStatus = 'Running'
sql
WorkflowId = '<workflow-id>' or ExecutionStatus = 'Running'
sql
WorkflowId = '<workflow-id>' and StartTime > '2021-08-22T15:04:05+00:00'
sql
ExecutionTime between '2021-08-22T15:04:05+00:00' and '2021-08-28T15:04:05+00:00'
sql
ExecutionTime < '2021-08-28T15:04:05+00:00' or ExecutionTime > '2021-08-22T15:04:05+00:00'
sql
WorkflowType STARTS_WITH '<workflow-type-prefix>'
sql
-- Using the original attribute name
WorkflowVersioningBehavior = 'pinned'

-- Using the Temporal-prefixed alias (equivalent)
TemporalWorkflowVersioningBehavior = 'pinned'
sql
-- If you have a custom Search Attribute named 'SchedulePaused'
-- This will use your custom attribute, not the default Search Attribute
SchedulePaused = true

-- The original system attribute still works by using the Temporal prefix
TemporalSchedulePaused = true
command
temporal task-queue get-build-id-reachability
command
temporal task-queue get-build-id-reachability --build-id "2.0"
output
BuildId                         TaskQueue                                   Reachability
    2.0  build-id-versioning-dc0068f6-0426-428f-b0b2-703a7e409a97  [NewWorkflows
                                                                   ExistingWorkflows]
```

For more information, see the [CLI documentation](/cli/) or help output.

You can also use this API `GetWorkerTaskReachability` directly from within language SDKs.

### Unversioned Workers

Unversioned Workers refer to Workers that have not opted into the Worker Versioning feature in their configuration.
They receive tasks only from Task Queues that do not have any version sets defined on them, or that have open Workflows that began executing before versions were added to the queue.

To migrate from an unversioned Task Queue, add a new default Build ID to the Task Queue.
From there, deploy Workers with the same Build ID.
Unversioned Workers will continue processing open Workflows, while Workers with the new Build ID will process new Workflow Executions.

This page discusses [Sticky Execution](#sticky-execution).

## What is a Sticky Execution? {#sticky-execution}

Workers cache the state of the Workflow they execute.
To make this caching more effective, Temporal employs a performance optimization known as "Sticky Execution", which directs Workflow Tasks to the same Worker that previously processed tasks for a specific Workflow Execution.

### How Sticky Execution Works

Once Workflow Execution begins, the Temporal Service schedules a Workflow Task and puts it into a Task Queue with the name you specify.
Any Worker that polls that Task Queue is eligible to accept the Task and begin executing the Workflow.

The Worker that picks up this Workflow Task will continue polling the original Task Queue, but will also begin polling an additional Task Queue, which the Temporal Service shares exclusively with that specific Worker.
This queue, which has an automatically-generated name, is known as a **Sticky Queue**.

The Worker caches the Workflow state in memory, which improves performance by reducing the need to reconstruct the Workflow from its Event History for every Task.
As the Workflow Execution progresses, the Temporal Service schedules additional Workflow Tasks into this Worker-specific Sticky Queue.

If the Worker fails to start a Workflow Task in the Sticky Queue shortly after it's scheduled (within five seconds by default), the Temporal Service disables stickiness for that Workflow Execution.
When stickiness is disabled, the Temporal Service reschedules the Workflow Task in the original queue, allowing any Worker to pick it up and continue the Workflow Execution.

If a Workflow Task fails, the Worker removes that Workflow Execution from its cache (as it's now in an unknown state), which invalidates the Sticky Execution.
The Workflow Task is then put back into the original Task Queue.

### Why Sticky Execution?

The main benefit of Sticky Execution is improved performance.
By caching the Workflow state in memory and directing tasks to the same Worker, it reduces the need to reconstruct the Workflow from its Event History for every Task, which is particularly useful for latency-sensitive Workflows.

Sticky Execution is the default behavior of the Temporal Platform and only applies to Workflow Tasks.
Since Event History is associated with a Workflow, the concept of Sticky Execution is not relevant to Activity Tasks.

- [How to set a `StickyScheduleToStartTimeout` on a individual Worker in Go](/develop/go/core-application#stickyscheduletostarttimeout)

Sticky Executions are the default behavior of the Temporal Platform.

## Task Queues and Naming Best Practices

**Examples:**

Example 1 (unknown):
```unknown
### .NET C# SDK
```

Example 2 (unknown):
```unknown
## Workflow Cache Tuning

When the number of cached Workflow Executions reported by `sticky_cache_size` hits `workflowCacheSize` _or_ the number of threads reported by the `workflow_active_thread_count` metrics gauge hits `maxWorkflowThreadCount`, Workflow Executions will start to be evicted from the cache.
An evicted Workflow Execution will need to be replayed when it gets any action that may advance it.

If the Workflow Cache limits described above are hit, and Worker hosts have enough free RAM and are not close to reasonable thread limits, then you may choose to increase `workflowCacheSize` and `maxWorkflowThreadCount` limits to decrease the overall latency and cost of the Replays in the system.
If the opposite occurs, consider decreasing the limits.

:::note

In CoreSDK based SDKs, like TypeScript, this metric works differently and should be monitored and adjusted on a per Worker and Task Queue basis.

:::

## Available Task Queue information {#task-queue-metrics}

:::tip Support, stability, and dependency info

The information listed in this section is readable using the `DescribeTaskQueueEnhanced` method in the [Go SDK](https://github.com/temporalio/sdk-go/blob/74320648ab0e4178b1fedde01672f9b5b9f6c898/client/client.go), with the [Temporal CLI](https://github.com/temporalio/cli/releases/tag/v1.1.0) `task-queue describe` command, and using `DescribeTaskQueue` through RPC.

:::

The Temporal Service reports information separately for each Task Queue type (not aggregated).
Use the following Task Queue properties to retrieve and evaluate information about Task Queue health and performance.
Available data include:

- [`ApproximateBacklogCount`](#ApproximateBacklogCountAndAge) and [`ApproximateBacklogAge`](#ApproximateBacklogCountAndAge)
- [`TasksAddRate`](#TasksAddRate-and-TasksDispatchRate) and [`TasksDispatchRate`](#TasksAddRate-and-TasksDispatchRate)
- [`BacklogIncreaseRate`](#BacklogIncreaseRate) (derived from [`TasksAddRate`](#TasksAddRate-and-TasksDispatchRate) and [`TasksDispatchRate`](#TasksAddRate-and-TasksDispatchRate))

### `ApproximateBacklogCount` and `ApproximateBacklogAge` {#ApproximateBacklogCountAndAge}

`ApproximateBacklogCount` represents the approximate count of Tasks currently backlogged in this Task Queue.
The number may include expired Tasks as well as active Tasks, but it will eventually converge to the correct count over time.

`ApproximateBacklogAge` returns the approximate age of the oldest Task in the backlog.
The age is based on the creation time of the Task at the head of the queue.

You can rely on both these counts when making scaling decisions.

Please note: [Sticky queues](https://docs.temporal.io/sticky-execution) will affect these values, but only for a few seconds.
That's because Tasks sent to Sticky queues are not included in the returned values for `ApproximateBacklogCount` and `ApproximateBacklogAge`.
Inaccuracies diminish as the backlog grows.

### `TasksAddRate` and `TasksDispatchRate` {#TasksAddRate-and-TasksDispatchRate}

Reports the approximate Tasks-per-second added to or dispatched from a Task Queue.
This rate is averaged over the most recent 30-second time interval.
The calculations include Tasks that were added to or dispatched from the backlog as well as Tasks that were immediately dispatched and bypassed the backlog (sync-matched).

The actual Task delivery count may be significantly higher than the number reported by these two values:

- Eager dispatch refers to a Temporal feature where Activities can be requested by an SDK using one Workflow Task completion response.
  Tasks using Eager dispatch do not pass through Task Queues.
- Tasks passed to Sticky Task Queues not included in the returned values for `TasksAddRate` and `TasksDispatchRate`.

### `BacklogIncreaseRate` {#BacklogIncreaseRate}

Approximates the _net_ Tasks per second added to the backlog, averaged over the most recent 30 seconds.
This is calculated as:
```

Example 3 (unknown):
```unknown
- Positive values of `X` indicate the backlog is growing by about `X` Tasks per second.
- Negative values of `X` indicate the backlog is shrinking by about `X` Tasks per second.

While individual `add` and `dispatch` rates may be inaccurate due to Eager and Sticky Task Queues, the `BacklogIncreaseRate` reliably reflects the rate at which the backlog is shrinking or growing for backlogs older than a few seconds.

## Evaluate Task Queue performance {#evaluate-worker-loads}

A [Task Queue](https://docs.temporal.io/task-queue) is a lightweight, dynamically allocated queue.
[Worker Entities](/workers#worker-entity) poll the queue for [Tasks](https://docs.temporal.io/tasks#task) and retrieve Tasks to work on.
Tasks are contexts that a Worker progresses using a specific Workflow Execution, Activity Execution, or a Nexus Task Execution.
Each Task Queue type offers its Tasks to compatible Workers for Task completion.
The Temporal Service dynamically creates different [Task Queue types](/task-queue) including Activity Task Queues, Workflow Task Queues, and Nexus Task Queues.

With an accurate estimate of backlog Tasks, you can determine the optimal number of Workers to deploy.
Balance your Worker count with the number of Tasks to achieve the best performance.
This approach minimizes Task backlog saturation and reduces idle Workers.

Task Queue data provide numerical insights into your Task Queue activity and backlog characteristics.
Use these numbers to tune your production deployments.
Evaluate your Worker loads and assess whether you need to scale up or reduce your Worker deployment.

:::note RATE LIMITS

[Visibility API rate limits](/cloud/limits#visibility-api-rate-limit) apply to Task Queue performance data requests.

:::

### Query Task Queue info with Temporal CLI {#cli-task-queue-info}

The Temporal CLI helps you monitor and evaluate Worker performance.
Issue the following command to display a list of active Workers that have recently polled a Task Queue:
```

Example 4 (unknown):
```unknown
This command retrieves poller information, backlog statistics, and task reachability for Task types (available in Temporal Server v1.25.0, Temporal CLI 1.1 and later).

:::warning

Task reachability status is experimental.
Determining Task reachability incurs a non-trivial computing cost.
This feature may significantly change or be removed in a future release.

:::

### Query Task Queue info with the Go SDK {#go-sdk-task-queue-info}

Retrieve Task Queue data using the Go SDK by calling `DescribeTaskQueueEnhanced`.
Specify the Task Queue name and set `ReportStats` to `true`, as in the following example:
```

---

## Copy application code

**URL:** llms-txt#copy-application-code

---

## -- RESULTING IMAGE --

**URL:** llms-txt#---resulting-image---

**Contents:**
  - Properly configure Node.js memory in Docker
  - Do not use Alpine
- How to run a Temporal Cloud Worker {#run-a-temporal-cloud-worker}
  - How to register types {#register-types}
- How to shut down a Worker and track its state {#shut-down-a-worker}
  - Worker states
- How to start a Workflow Execution {#start-workflow-execution}
  - How to set a Workflow's Task Queue {#set-task-queue}
  - How to set a Workflow Id {#workflow-id}
  - How to get the results of a Workflow Execution {#get-workflow-results}

FROM gcr.io/distroless/nodejs20-debian11

COPY --from=builder /app /app
WORKDIR /app

CMD ["node", "build/worker.js"]
sh
Error: Error loading shared library ld-linux-x86-64.so.2: No such file or directory (needed by /opt/app/node_modules/@temporalio/core-bridge/index.node)
sh
Error: Error relocating /opt/app/node_modules/@temporalio/core-bridge/index.node: __register_atfork: symbol not found
ts

async function run() {
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    taskQueue: 'snippets',
    activities,
  });

await worker.run();
}
ts

async function bundle() {
  const { code } = await bundleWorkflowCode({
    workflowsPath: require.resolve('../workflows'),
  });
  const codePath = path.join(__dirname, '../../workflow-bundle.js');

await writeFile(codePath, code);
  console.log(`Bundle written to ${codePath}`);
}
ts
const workflowOption = () =>
  process.env.NODE_ENV === 'production'
    ? {
        workflowBundle: {
          codePath: require.resolve('../workflow-bundle.js'),
        },
      }
    : { workflowsPath: require.resolve('./workflows') };

async function run() {
  const worker = await Worker.create({
    ...workflowOption(),
    activities,
    taskQueue: 'production-sample',
  });

await worker.run();
}
typescript
const handle = await client.workflow.start(example, {
  workflowId: 'your-workflow-id',
  taskQueue: 'your-task-queue',
  args: ['argument01', 'argument02', 'argument03'], // this is typechecked against workflowFn's args
});
const handle = client.getHandle(workflowId);
const result = await handle.result();
ts

async function run() {
  // Step 1: Register Workflows and Activities with the Worker and connect to
  // the Temporal server.
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    activities,
    taskQueue: 'hello-world',
  });
  // Worker connects to localhost by default and uses console.error for logging.
  // Customize the Worker by passing more options to create():
  // https://typescript.temporal.io/api/classes/worker.Worker
  // If you need to configure server connection parameters, see docs:
  // /typescript/security#encryption-in-transit-with-mtls

// Step 2: Start accepting tasks on the `tutorial` queue
  await worker.run();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
ts

// This is the code that is used to start a Workflow.
const connection = await Connection.create();
const client = new Client({ connection });
const result = await client.workflow.execute(yourWorkflow, {
  // required
  taskQueue: 'your-task-queue',
  // required
  workflowId: 'your-workflow-id',
});
ts
const worker = await Worker.create({
  // imported elsewhere
  activities,
  taskQueue: 'your-task-queue',
});
typescript
const handle = await client.workflow.start(example, {
  workflowId: 'yourWorkflowId',
  taskQueue: 'yourTaskQueue',
  args: ['your', 'arg', 'uments'],
});
typescript
return (
  'Completed '
  + wf.workflowInfo().workflowId
  + ', Total Charged: '
  + totalCharged
);
typescript
const handle = client.getHandle(workflowId);
const result = await handle.result();
typescript
const handle = client.getHandle(workflowId);
try {
  const result = await handle.result();
} catch (err) {
  if (err instanceof WorkflowFailedError) {
    throw new Error('Temporal workflow failed: ' + workflowId, {
      cause: err,
    });
  } else {
    throw new Error('error from Temporal workflow ' + workflowId, {
      cause: err,
    });
  }
}
ts

export async function cancelTimer(): Promise<void> {
  // Timers and Activities are automatically cancelled when their containing scope is cancelled.
  try {
    await CancellationScope.cancellable(async () => {
      const promise = sleep(1); // <-- Will be cancelled because it is attached to this closure's scope
      CancellationScope.current().cancel();
      await promise; // <-- Promise must be awaited in order for `cancellable` to throw
    });
  } catch (e) {
    if (e instanceof CancelledFailure) {
      console.log('Timer cancelled 👍');
    } else {
      throw e; // <-- Fail the workflow
    }
  }
}
ts

export async function cancelTimerAltImpl(): Promise<void> {
  try {
    const scope = new CancellationScope();
    const promise = scope.run(() => sleep(1));
    scope.cancel(); // <-- Cancel the timer created in scope
    await promise; // <-- Throws CancelledFailure
  } catch (e) {
    if (e instanceof CancelledFailure) {
      console.log('Timer cancelled 👍');
    } else {
      throw e; // <-- Fail the workflow
    }
  }
}
ts

const { httpPostJSON, cleanup } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10m',
});

export async function handleExternalWorkflowCancellationWhileActivityRunning(url: string, data: any): Promise<void> {
  try {
    await httpPostJSON(url, data);
  } catch (err) {
    if (isCancellation(err)) {
      console.log('Workflow cancelled');
      // Cleanup logic must be in a nonCancellable scope
      // If we'd run cleanup outside of a nonCancellable scope it would've been cancelled
      // before being started because the Workflow's root scope is cancelled.
      await CancellationScope.nonCancellable(() => cleanup(url));
    }
    throw err; // <-- Fail the Workflow
  }
}
ts
export async function nonCancellable(url: string): Promise<any> {
  // Prevent Activity from being cancelled and await completion.
  // Note that the Workflow is completely oblivious and impervious to cancellation in this example.
  return CancellationScope.nonCancellable(() => httpGetJSON(url));
}
ts

export function multipleActivitiesSingleTimeout(urls: string[], timeoutMs: number): Promise<any> {
  const { httpGetJSON } = proxyActivities<typeof activities>({
    startToCloseTimeout: timeoutMs,
  });

// If timeout triggers before all activities complete
  // the Workflow will fail with a CancelledError.
  return CancellationScope.withTimeout(timeoutMs, () => Promise.all(urls.map((url) => httpGetJSON(url))));
}
ts

const { httpGetJSON } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10m',
});

export async function resumeAfterCancellation(url: string): Promise<any> {
  let result: any = undefined;
  const scope = new CancellationScope({ cancellable: false });
  const promise = scope.run(() => httpGetJSON(url));
  try {
    result = await Promise.race([scope.cancelRequested, promise]);
  } catch (err) {
    if (!(err instanceof CancelledFailure)) {
      throw err;
    }
    // Prevent Workflow from completing so Activity can complete
    result = await promise;
  }
  return result;
}
ts

function doSomething(callback: () => any) {
  setTimeout(callback, 10);
}

export async function cancellationScopesWithCallbacks(): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    doSomething(resolve);
    CancellationScope.current().cancelRequested.catch(reject);
  });
}
ts

const { setup, httpPostJSON, cleanup } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10m',
});

export async function nestedCancellation(url: string): Promise<void> {
  await CancellationScope.cancellable(async () => {
    await CancellationScope.nonCancellable(() => setup());
    try {
      await CancellationScope.withTimeout(1000, () => httpPostJSON(url, { some: 'data' }));
    } catch (err) {
      if (isCancellation(err)) {
        await CancellationScope.nonCancellable(() => cleanup(url));
      }
      throw err;
    }
  });
}
ts
export async function sharedScopes(): Promise<any> {
  // Start activities in the root scope
  const p1 = httpGetJSON('http://url1.ninja');
  const p2 = httpGetJSON('http://url2.ninja');

const scopePromise = CancellationScope.cancellable(async () => {
    const first = await Promise.race([p1, p2]);
    // Does not cancel activity1 or activity2 as they're linked to the root scope
    CancellationScope.current().cancel();
    return first;
  });
  return await scopePromise;
  // The Activity that did not complete will effectively be cancelled when
  // Workflow completes unless the Activity is awaited:
  // await Promise.all([p1, p2]);
}
ts
export async function shieldAwaitedInRootScope(): Promise<any> {
  let p: Promise<any> | undefined = undefined;

await CancellationScope.nonCancellable(async () => {
    p = httpGetJSON('http://example.com'); // <-- Start activity in nonCancellable scope without awaiting completion
  });
  // Activity is shielded from cancellation even though it is awaited in the cancellable root scope
  return p;
}
bash
[ERROR] Module not found: Error: Can't resolve '@temporalio/workflow/lib/worker-interface.js' in '/src'
bash
[ERROR] Failed to activate workflow {
  runId: 'aaf84a83-51ce-462a-9ab7-6a641a703bff',
  error: ReferenceError: exports is not defined,
  workflowExists: false
}
ts

const config = fs.readFileSync('config.json', 'utf8');

2021-10-14T19:22:00.606Z [INFO] Module not found: Error: Can't resolve 'fs' in '/Users/you/your-project/src'
2021-10-14T19:22:00.606Z [INFO] resolve 'fs' in '/Users/you/your-project/src'
2021-10-14T19:22:00.606Z [INFO]   Parsed request is a module
2021-10-14T19:22:00.606Z [INFO]   using description file: /Users/you/your-project/package.json (relative path: ./src)
2021-10-14T19:22:00.606Z [INFO]     Field 'browser' doesn't contain a valid alias configuration
ts

export async function yourWorkflow(): Promise<string> {
  return await makeHTTPRequest('https://temporal.io');
}

2021-10-14T19:46:52.731Z [INFO] ERROR in ./src/activities.ts 8:31-46
2021-10-14T19:46:52.731Z [INFO] Module not found: Error: Can't resolve 'http' in '/Users/you/your-project/src'
2021-10-14T19:46:52.731Z [INFO]
2021-10-14T19:46:52.731Z [INFO] BREAKING CHANGE: webpack < 5 used to include polyfills for node.js core modules by default.
2021-10-14T19:46:52.731Z [INFO] This is no longer the case. Verify if you need this module and configure a polyfill for it.
2021-10-14T19:46:52.731Z [INFO]
2021-10-14T19:46:52.731Z [INFO] If you want to include a polyfill, you need to:
2021-10-14T19:46:52.731Z [INFO]         - add a fallback 'resolve.fallback: { "http": require.resolve("stream-http") }'
2021-10-14T19:46:52.731Z [INFO]         - install 'stream-http'
2021-10-14T19:46:52.731Z [INFO] If you don't want to include a polyfill, you can use an empty module like this:
2021-10-14T19:46:52.731Z [INFO]         resolve.fallback: { "http": false }
ts

const { makeHTTPRequest } = proxyActivities<typeof activities>();

export async function yourWorkflow(): Promise<string> {
  return await makeHTTPRequest('https://temporal.io');
}

Error: 3 INVALID_ARGUMENT: WorkflowType is not set on request.
js
// webpack.config.js
module.exports = {
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          keep_fnames: true, // don't strip function names in production
        },
      }),
    ],
  },
};
js
require('esbuild').buildSync({
  entryPoints: ['app.js'],
  minify: true,
  keepNames: true,
  outfile: 'out.js',
});
bash
[TransportError: transport error]

Error: 4 DEADLINE_EXCEEDED: context deadline exceeded
    at Object.callErrorFromStatus (/Users/swyx/Work/Temporal/samples-typescript/nextjs-oneclick/node_modules/@grpc/grpc-js/build/src/call.js:31:26)
    at Object.onReceiveStatus (/Users/swyx/Work/Temporal/samples-typescript/nextjs-oneclick/node_modules/@grpc/grpc-js/build/src/client.js:179:52)
    at Object.onReceiveStatus (/Users/swyx/Work/Temporal/samples-typescript/nextjs-oneclick/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:336:141)
    at Object.onReceiveStatus (/Users/swyx/Work/Temporal/samples-typescript/nextjs-oneclick/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:299:181)
    at /Users/swyx/Work/Temporal/samples-typescript/nextjs-oneclick/node_modules/@grpc/grpc-js/build/src/call-stream.js:145:78
    at processTicksAndRejections (node:internal/process/task_queues:78:11) {
  code: 4,
  details: 'context deadline exceeded',
  metadata: Metadata {
    internalRepr: Map(1) { 'content-type' => [Array] },
    options: {}
  },
  page: '/api/getBuyState'
}
typescript

const client = new Client();

// Start a workflow with static summary and details
const handle = await client.workflow.start(yourWorkflow, {
  args: ['workflow input'],
  taskQueue: 'your-task-queue',
  workflowId: 'your-workflow-id',
  staticSummary: 'Order processing for customer #12345',
  staticDetails: 'Processing premium order with expedited shipping'
});
typescript
const result = await client.workflow.execute(yourWorkflow, {
  args: ['workflow input'],
  taskQueue: 'your-task-queue',
  workflowId: 'your-workflow-id',
  staticSummary: 'Order processing for customer #12345',
  staticDetails: 'Processing premium order with expedited shipping'
});
typescript

export async function yourWorkflow(input: string): Promise<string> {
  // Get the current details
  const currentDetails = getCurrentDetails();
  console.log(`Current details: ${currentDetails}`);
  
  // Set/update the current details
  setCurrentDetails('Updated workflow details with new status');
  
  return 'Workflow completed';
}
typescript

const { yourActivity } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10 seconds'
});

export async function yourWorkflow(input: string): Promise<string> {
  // Execute an activity with a summary using executeWithOptions
  const result = await yourActivity.executeWithOptions(
    {
      staticSummary: 'Processing user data'
    },
    [input] // Note: arguments must be passed as an array
  );
  
  return result;
}
typescript

export async function yourWorkflow(input: string): Promise<string> {
  // Create a timer with a summary
  await sleep('5 minutes', { summary: 'Waiting for payment confirmation' });
  
  return 'Timer completed';
}
ts
interface Input {
  /* Define your Workflow input type here */
}
interface Update {
  /* Define your Workflow update type here */
}

const MAX_ITERATIONS = 1;

export async function entityWorkflow(
  input: Input,
  isNew = true,
): Promise<void> {
  try {
    const pendingUpdates = Array<Update>();
    setHandler(updateSignal, (updateCommand) => {
      pendingUpdates.push(updateCommand);
    });

if (isNew) {
      await setup(input);
    }

for (let iteration = 1; iteration <= MAX_ITERATIONS; ++iteration) {
      // Ensure that we don't block the Workflow Execution forever waiting
      // for updates, which means that it will eventually Continue-As-New
      // even if it does not receive updates.
      await condition(() => pendingUpdates.length > 0, '1 day');

while (pendingUpdates.length) {
        const update = pendingUpdates.shift();
        await runAnActivityOrChildWorkflow(update);
      }
    }
  } catch (err) {
    if (isCancellation(err)) {
      await CancellationScope.nonCancellable(async () => {
        await cleanup();
      });
    }
    throw err;
  }
  await continueAsNew<typeof entityWorkflow>(input, false);
}
typescript 
class InvalidChargeError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "InvalidChargeError";
        Object.setPrototypeOf(this, CustomError.prototype);
    }
}

if (chargeAmount < 0) {
  throw new InvalidChargeError(`Invalid charge amount: ${chargeAmount} (must be above zero)`);
}
typescript 
if (chargeAmount < 0) {
  throw ApplicationFailure.create({
    message: `Invalid charge amount: ${chargeAmount} (must be above zero)`,
    type: 'InvalidChargeError',
  });
}
typescript
if (chargeAmount < 0) {
  throw ApplicationFailure.create({
    message: `Invalid charge amount: ${chargeAmount} (must be above zero)`,
    nonRetryable: true
  });
}
typescript
try {
  await addAddress();
} catch (err) {
  if (err instanceof ActivityFailure && err.cause instanceof ApplicationFailure) {
    log.error(err.cause.message);
    throw err;
  }
}
typescript
await client.workflow.start(example, {
  taskQueue,
  workflowId,
  // Set Workflow Timeout duration
  workflowExecutionTimeout: '1 day',
  // workflowRunTimeout: '1 minute',
  // workflowTaskTimeout: '30 seconds',
});
typescript
const handle = await client.workflow.start(example, {
  taskQueue,
  workflowId,
  retry: {
    maximumAttempts: 3,
    maximumInterval: '30 seconds',
  },
});
typescript
const { myActivity } = proxyActivities<typeof activities>({
  scheduleToCloseTimeout: '5m',
  // startToCloseTimeout: "30s", // recommended
  // scheduleToStartTimeout: "60s",
});
typescript
const { myActivity } = proxyActivities<typeof activities>({
  // ...
  retry: {
    initialInterval: '10s',
    maximumAttempts: 5,
  },
});
typescript
throw ApplicationFailure.create({
  // ...
  nextRetryDelay: '15s',
});
typescript
export async function myActivity(): Promise<void> {
  for (let progress = 1; progress <= 1000; ++progress) {
    // Do something that takes time
    await sleep('1s');

heartbeat();
  }
}
typescript
export async function myActivity(): Promise<void> {
  // Resume work from latest heartbeat, if there's one, or start from 1 otherwise
  const startingPoint = activityInfo().heartbeatDetails?.progress ?? 1;

for (let progress = startingPoint; progress <= 1000; ++progress) {
    // Do something that takes time
    await sleep('1s');

heartbeat({ progress });
  }
}
typescript
const { myLongRunningActivity } = proxyActivities<typeof activities>({
  // ...
  heartbeatTimeout: '30s',
});
ts

ActivityInput,
  Next,
  WorkflowOutboundCallsInterceptor,
} from '@temporalio/workflow';

export class ActivityLogInterceptor
  implements WorkflowOutboundCallsInterceptor
{
  constructor(public readonly workflowType: string) {}

async scheduleActivity(
    input: ActivityInput,
    next: Next<WorkflowOutboundCallsInterceptor, 'scheduleActivity'>,
  ): Promise<unknown> {
    console.log('Starting activity', { activityType: input.activityType });
    try {
      return await next(input);
    } finally {
      console.log('Completed activity', {
        workflow: this.workflowType,
        activityType: input.activityType,
      });
    }
  }
}
ts

defaultDataConverter,
  Next,
  WorkflowInboundCallsInterceptor,
  WorkflowInput,
} from '@temporalio/workflow';

/**
 * WARNING: This demo is meant as a simple auth example.
 * Do not use this for actual authorization logic.
 * Auth headers should be encrypted and credentials
 * stored outside of the codebase.
 */
export class DumbWorkflowAuthInterceptor
  implements WorkflowInboundCallsInterceptor
{
  public async execute(
    input: WorkflowInput,
    next: Next<WorkflowInboundCallsInterceptor, 'execute'>,
  ): Promise<unknown> {
    const authHeader = input.headers.auth;
    const { user, password } = authHeader
      ? await defaultDataConverter.fromPayload(authHeader)
      : undefined;

if (!(user === 'admin' && password === 'admin')) {
      throw new Error('Unauthorized');
    }
    return await next(input);
  }
}
ts

export const interceptors = () => ({
  outbound: [new ActivityLogInterceptor(workflowInfo().workflowType)],
  inbound: [],
});
ts
const worker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  interceptors: {
    workflowModules: [require.resolve('./workflows/your-interceptors')],
  },
});
typescript
export enum Language {
  ARABIC = 'ARABIC',
  CHINESE = 'CHINESE',
  ENGLISH = 'ENGLISH',
  FRENCH = 'FRENCH',
  HINDI = 'HINDI',
  PORTUGUESE = 'PORTUGUESE',
  SPANISH = 'SPANISH',
}

interface GetLanguagesInput {
  includeUnsupported: boolean;
}

// 👉 Use the object returned by defineQuery to set the query handler in
// Workflow code, and when sending the Query in Client code.
export const getLanguages = wf.defineQuery<Language[], [GetLanguagesInput]>('getLanguages');

export async function greetingWorkflow(): Promise<string> {
  const greetings: Partial<Record<Language, string>> = {
    [Language.CHINESE]: '你好，世界',
    [Language.ENGLISH]: 'Hello, world',
  };

wf.setHandler(getLanguages, (input: GetLanguagesInput): Language[] => {
    // 👉 A Query handler returns a value: it must not mutate the Workflow state
    // and can't perform async operations.
    if (input.includeUnsupported) {
      return Object.values(Language);
    } else {
      return Object.keys(greetings) as Language[];
    }
  });

...
}
typescript
// 👉 Use the object returned by defineSignal to set the Signal handler in
// Workflow code, and to send the Signal from Client code.
export const approve = wf.defineSignal<[ApproveInput]>('approve');

export async function greetingWorkflow(): Promise<string> {
  let approvedForRelease = false;
  let approverName: string | undefined;

wf.setHandler(approve, (input) => {
    // 👉 A Signal handler mutates the Workflow state but cannot return a value.
    approvedForRelease = true;
    approverName = input.name;
  });

...
}
...
typescript
// 👉 Use the object returned by defineUpdate to set the Update handler in
// Workflow code, and to send Updates from Client code.
export const setLanguage = wf.defineUpdate<Language, [Language]>('setLanguage');

export async function greetingWorkflow(): Promise<string> {
  const greetings: Partial<Record<Language, string>> = {
    [Language.CHINESE]: '你好，世界',
    [Language.ENGLISH]: 'Hello, world',
  };

let language = Language.ENGLISH;

wf.setHandler(
    setLanguage,
    (newLanguage: Language) => {
      // 👉 An Update handler can mutate the Workflow state and return a value.
      const previousLanguage = language;
      language = newLanguage;
      return previousLanguage;
    },
    {
      validator: (newLanguage: Language) => {
        // 👉 Update validators are optional
        if (!(newLanguage in greetings)) {
          throw new Error(`${newLanguage} is not supported`);
        }
      },
    }
  );

...
}
typescript
const handle = await client.workflow.start(greetingWorkflow, {
  taskQueue: 'my-task-queue',
  args: [myArg],
  workflowId: 'my-workflow-id',
});
typescript
const supportedLanguages = await handle.query(getLanguages, {
  includeUnsupported: false,
});
typescript
await handle.signal(greetingWorkflow.approve, { name: 'me' });
typescript

export async function yourWorkflowThatSignals() {
  const handle = getExternalWorkflowHandle('workflow-id-123');
  await handle.signal(joinSignal, { userId: 'user-1', groupId: 'group-1' });
}
typescript

const client = new Client();

await client.workflow.signalWithStart(yourWorkflow, {
  workflowId: 'workflow-id-123',
  taskQueue: 'my-taskqueue',
  args: [{ foo: 1 }],
  signal: joinSignal,
  signalArgs: [{ userId: 'user-1', groupId: 'group-1' }],
});
typescript
  let previousLanguage = await handle.executeUpdate(setLanguage, {
    args: [Language.CHINESE],
  });
  typescript
  const updateHandle = await handle.startUpdate(setLanguage, {
    args: [Language.ENGLISH],
    waitForStage: WorkflowUpdateStage.ACCEPTED,
  });
  previousLanguage = await updateHandle.result();
  typescript
const startWorkflowOperation = new WithStartWorkflowOperation.create(
  transactionWorkflow,
  {
    workflowId,
    args: [transactionID],
    taskQueue: 'early-return',
    workflowIdConflictPolicy: 'FAIL',
  },
);

const earlyConfirmation = await client.workflow.executeUpdateWithStart(
  getTransactionConfirmation,
  {
    startWorkflowOperation,
  },
);

const wfHandle = await startWorkflowOperation.workflowHandle();
const finalReport = await wfHandle.result();
typescript
// 👉 Use the objects returned by defineUpdate to set the Update handler in
// Workflow code, and to send Updates from Client code.
export const setLanguageUsingActivity = wf.defineUpdate<Language, [Language]>('setLanguageUsingActivity');

export async function greetingWorkflow(): Promise<string> {
  const greetings: Partial<Record<Language, string>> = {
    [Language.CHINESE]: '你好，世界',
    [Language.ENGLISH]: 'Hello, world',
  };

let language = Language.ENGLISH;

const lock = new Mutex();
  wf.setHandler(setLanguageUsingActivity, async (newLanguage) => {
    // 👉 An Update handler can mutate the Workflow state and return a value.
    // 👉 Since this update handler is async, it can execute an activity.
    if (!(newLanguage in greetings)) {
      // 👉 Do the following with the lock held to ensure that multiple calls to set_language are processed in order.
      await lock.runExclusive(async () => {
        if (!(newLanguage in greetings)) {
          const greeting = await callGreetingService(newLanguage);
          if (!greeting) {
            // 👉 An update validator cannot be async, so cannot be used to check that the remote
            // call_greeting_service supports the requested language. Raising ApplicationError
            // will fail the Update, but the WorkflowExecutionUpdateAccepted event will still be
            // added to history.
            throw new wf.ApplicationFailure(`${newLanguage} is not supported by the greeting service`);
          }
          greetings[newLanguage] = greeting;
        }
      });
    }
    const previousLanguage = language;
    language = newLanguage;
    return previousLanguage;
  });
  ...
}
typescript
export async function greetingWorkflow(): Promise<string> {
  let approvedForRelease = false;
  let approverName: string | undefined;

wf.setHandler(approve, (input) => {
    approvedForRelease = true;
    approverName = input.name;
  });
  ...

await wf.condition(() => approvedForRelease);
  ...
}
typescript
let readyForUpdateToExecute = false;

wf.setHandler(myUpdate, async (input: MyUpdateInput): Promise<MyUpdateOutput> => {
  await wf.condition(() => readyForUpdateToExecute);
  ...
});
typescript
export async function myWorkflow(): Promise<MyWorkflowOutput> {
  await wf.condition(wf.allHandlersFinished);
  return workflowOutput;
}
typescript
export async function myWorkflow(): Promise<MyWorkflowOutput> {
  let x = 0;
  let y = 0;
  wf.setHandler(mySignal, async () => {
    const data = await myActivity();
    x = data.x;

// 🐛🐛 Bug!! If multiple instances of this handler are executing
    // concurrently, then there may be times when the Workflow has x from one
    // Activity execution and y from another.
    await wf.sleep(500); // or await anything else

y = data.y;
  });
  ...
}
typescript

export async function myWorkflow(): Promise<MyWorkflowOutput> {
  let x = 0;
  let y = 0;
  const lock = new Mutex();

wf.setHandler(mySignal, async () => {
    await lock.runExclusive(async () => {
      const data = await myActivity();
      x = data.x;

// ✅ OK: node's event loop may switch now to a different handler
      // execution, or to the main workflow function, but no other execution of
      // this handler can run until this execution finishes.
      await wf.sleep(500); // or await anything else

y = data.y;
    });
  });
  return {
    name: 'hello',
  };
}
ts

export const unblockSignal = wf.defineSignal('unblock');
export const isBlockedQuery = wf.defineQuery<boolean>('isBlocked');

export async function unblockOrCancel(): Promise<void> {
  let isBlocked = true;
  wf.setHandler(unblockSignal, () => void (isBlocked = false));
  wf.setHandler(isBlockedQuery, () => isBlocked);
  wf.log.info('Blocked');
  try {
    await wf.condition(() => !isBlocked);
    wf.log.info('Unblocked');
  } catch (err) {
    if (err instanceof wf.CancelledFailure) {
      wf.log.info('Cancelled');
    }
    throw err;
  }
}
ts

// "fat handler" solution
wf.setHandler(`genericSignal`, (payload) => {
  switch (payload.taskId) {
    case taskAId:
      // do task A things
      break;
    case taskBId:
      // do task B things
      break;
    default:
      throw new Error('Unexpected task.');
  }
});

// "inline definition" solution
wf.setHandler(wf.defineSignal(`task-${taskAId}`), (payload) => {
  /* do task A things */
});
wf.setHandler(wf.defineSignal(`task-${taskBId}`), (payload) => {
  /* do task B things */
});

// utility "inline definition" helper
const inlineSignal = (signalName, handler) =>
  wf.setHandler(wf.defineSignal(signalName), handler);
inlineSignal(`task-${taskBId}`, (payload) => {
  /* do task B things */
});
ts
/**
 * Define a signal method for a Workflow.
 */
export function defineSignal<Args extends any[] = []>(
  name: string,
): SignalDefinition<Args> {
  return {
    type: 'signal',
    name,
  };
}

/**
 * Define a query method for a Workflow.
 */
export function defineQuery<Ret, Args extends any[] = []>(
  name: string,
): QueryDefinition<Ret, Args> {
  return {
    type: 'query',
    name,
  };
}
ts
wf.setHandler(MySignal, handlerFn1);
wf.setHandler(MySignal, handlerFn2); // replaces handlerFn1
typescript
telemetryOptions: {
    metrics: {
      prometheus: { bindAddress: '0.0.0.0:9464' },
    },
    logging: { forward: { level: 'DEBUG' } },
  },
js

CompositePropagator,
    W3CBaggagePropagator,
    W3CTraceContextPropagator,
  } from '@opentelemetry/core';

propagation.setGlobalPropagator(
    new CompositePropagator({
      propagators: [
        new W3CTraceContextPropagator(),
        new W3CBaggagePropagator(),
        new JaegerPropagator(),
      ],
    }),
  );
  ts

export async function greet(name: string): Promise<string> {
  log.info('Log from activity', { name });
  return `Hello, ${name}!`;
}
ts

export async function myWorkflow(name: string): Promise<string> {
  log.info('Log from workflow', { name });
  return `Hello, ${name}!`;
}
typescript

DefaultLogger,
  makeTelemetryFilterString,
  Runtime,
} from '@temporalio/worker';

// This is your custom Logger.
const logger = new DefaultLogger('WARN', ({ level, message }) => {
  console.log(`Custom logger: ${level} — ${message}`);
});

Runtime.install({
  logger,
  // The following block is optional, but generally desired.
  // It allows capturing log messages emitted by the underlying Temporal Core SDK (native code).
  // The Telemetry Filter String determine the desired verboseness of messages emitted by the
  // Temporal Core SDK itself ("core"), and by other native libraries ("other").
  telemetryOptions: {
    logging: {
      filter: makeTelemetryFilterString({ core: 'INFO', other: 'INFO' }),
      forward: {},
    },
  },
});
typescript

DefaultLogger,
  makeTelemetryFilterString,
  Runtime,
} from '@temporalio/worker';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [new transports.File({ filename: '/path/to/worker.log' })],
});

Runtime.install({
  logger,
  // The following block is optional, but generally desired.
  // It allows capturing log messages emitted by the underlying Temporal Core SDK (native code).
  // The Telemetry Filter String determine the desired verboseness of messages emitted by the
  // Temporal Core SDK itself ("core"), and by other native libraries ("other").
  telemetryOptions: {
    logging: {
      filter: makeTelemetryFilterString({ core: 'INFO', other: 'INFO' }),
      forward: {},
    },
  },
});
ts

export interface AlertSinks extends Sinks {
  alerter: {
    alert(message: string): void;
  };
}

export type MySinks = AlertSinks;
ts

async function main() {
  const sinks: InjectedSinks<MySinks> = {
    alerter: {
      alert: {
        fn(workflowInfo, message) {
          console.log('sending SMS alert!', {
            workflowId: workflowInfo.workflowId,
            workflowRunId: workflowInfo.runId,
            message,
          });
        },
        callDuringReplay: false, // The default
      },
    },
  };
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    taskQueue: 'sinks',
    sinks,
  });
  await worker.run();
  console.log('Worker gracefully shutdown');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
ts
const { alerter } = proxySinks<MySinks>();

export async function sinkWorkflow(): Promise<string> {
  log.info('Workflow Execution started');
  alerter.alert('alerter: Workflow Execution started');
  return 'Hello, Temporal!';
}
ts

const logger = new DefaultLogger('WARN', ({ level, message }) => {
  console.log(`Custom logger: ${level} — ${message}`);
});
Runtime.install({ logger });
ts

const logs: LogEntry[] = [];
const logger = new DefaultLogger(LogLevel.TRACE, (entry) => logs.push(entry));

logger.debug('hey', { a: 1 });
logger.info('ho');
logger.warn('lets', { a: 1 });
logger.error('go');
ts

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [new transports.File({ filename: '/path/to/worker.log' })],
});
Runtime.install({ logger });
typescript

const connection = await Connection.connect();
const response = await connection.workflowService.listWorkflowExecutions({
  query: `ExecutionStatus = "Running"`,
});
ts
const handle = await client.workflow.start(example, {
  taskQueue: 'search-attributes',
  workflowId: 'search-attributes-example-0',
  searchAttributes: {
    CustomIntField: [2],
    CustomKeywordListField: ['keywordA', 'keywordB'],
    CustomBoolField: [true],
    CustomDatetimeField: [new Date()],
    CustomTextField: [
      'String field is for text. When queried, it will be tokenized for partial match. StringTypeField cannot be used in Order By',
    ],
  },
});

const { searchAttributes } = await handle.describe();
ts
export async function example(): Promise<SearchAttributes> {
  const customInt = (workflowInfo().searchAttributes.CustomIntField?.[0] as number) || 0;
  upsertSearchAttributes({
    // overwrite the existing CustomIntField: [2]
    CustomIntField: [customInt + 1],

// delete the existing CustomBoolField: [true]
    CustomBoolField: [],

// add a new value
    CustomDoubleField: [3.14],
  });
  return workflowInfo().searchAttributes;
}
typescript

async function yourWorkflow() {
  upsertSearchAttributes({ CustomIntField: [1, 2, 3] });

// ... later, to remove:
  upsertSearchAttributes({ CustomIntField: [] });
}
ts
async function run() {
  const config = loadClientConnectConfig();
  const connection = await Connection.connect(config.connectionOptions);
  const client = new Client({ connection });

// https://typescript.temporal.io/api/classes/client.ScheduleClient#create
  const schedule = await client.schedule.create({
    action: {
      type: 'startWorkflow',
      workflowType: reminder,
      args: ['♻️ Dear future self, please take out the recycling tonight. Sincerely, past you ❤️'],
      taskQueue: 'schedules',
    },
    scheduleId: 'sample-schedule',
    policies: {
      catchupWindow: '1 day',
      overlap: ScheduleOverlapPolicy.ALLOW_ALL,
    },
    spec: {
      intervals: [{ every: '10s' }],
      // or periodic calendar times:
      // calendars: [
      //   {
      //     comment: 'every wednesday at 8:30pm',
      //     dayOfWeek: 'WEDNESDAY',
      //     hour: 20,
      //     minute: 30,
      //   },
      // ],
      // or a single datetime:
      // calendars: [
      //   {
      //     comment: '1/1/23 at 9am',
      //     year: 2023,
      //     month: 1,
      //     dayOfMonth: 1,
      //     hour: 9,
      //   },
      // ],
    },
  });
ts
function subtractMinutes(minutes: number): Date {
  const now = new Date();
  return new Date(now.getTime() - minutes * 60 * 1000);
}

async function run() {
  const client = new Client({
    connection: await Connection.connect(),
  });

const backfillOptions: Backfill = {
    start: subtractMinutes(10),
    end: subtractMinutes(9),
    overlap: ScheduleOverlapPolicy.ALLOW_ALL,
  };

const handle = client.schedule.getHandle('sample-schedule');
  await handle.backfill(backfillOptions);

console.log(`Schedule is now backfilled.`);
}
ts
async function run() {
  const client = new Client({
    connection: await Connection.connect(),
  });

const handle = client.schedule.getHandle('sample-schedule');
  await handle.delete();

console.log(`Schedule is now deleted.`);
}
ts
async function run() {
  const client = new Client({
    connection: await Connection.connect(),
  });

const handle = client.schedule.getHandle('sample-schedule');

const result = await handle.describe();

console.log(`Schedule description: ${JSON.stringify(result)}`);
}
ts
async function run() {
  const client = new Client({
    connection: await Connection.connect(),
  });

const schedules = [];

const scheduleList = client.schedule.list();

for await (const schedule of scheduleList) {
    schedules.push(schedule);
  }

console.log(`Schedules are now listed: ${JSON.stringify(schedules)}`);
}
ts
async function run() {
  const client = new Client({
    connection: await Connection.connect(),
  });

const handle = client.schedule.getHandle('sample-schedule');
  await handle.pause();

console.log(`Schedule is now paused.`);
}
ts
async function run() {
  const client = new Client({
    connection: await Connection.connect(),
  });

const handle = client.schedule.getHandle('sample-schedule');

await handle.trigger();

console.log(`Schedule is now triggered.`);
}
ts
const updateSchedule = (
  input: ScheduleDescription,
): ScheduleUpdateOptions<ScheduleOptionsStartWorkflowAction<Workflow>> => {
  const scheduleAction = input.action;

scheduleAction.args = ['my updated schedule arg'];

return { ...input, ...scheduleAction };
};

async function run() {
  const client = new Client({
    connection: await Connection.connect(),
  });

const handle = client.schedule.getHandle('sample-schedule');

await handle.update(updateSchedule);

console.log(`Schedule is now updated.`);
}
typescript
const handle = await client.workflow.start(scheduledWorkflow, {
  // ...
  cronSchedule: '* * * * *', // start every minute
});

┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
typescript
const handle = await client.workflow.start(someWorkflow, {
  // ...
  startDelay: '2 hours',
});
```

## Set up your local with the Typescript SDK

**Examples:**

Example 1 (unknown):
```unknown
### Properly configure Node.js memory in Docker

By default, `node` configures its maximum old-gen memory to 25% of the _physical memory_ of the machine on which it is executing, with a maximum of 4 GB.
This is likely inappropriate when running Node.js in a Docker environment and can result in either underusage of available memory (`node` only uses a fraction of the memory allocated to the container) or overusage (`node` tries to use more memory than what is allocated to the container, which will eventually lead to the process being killed by the operating system).

Therefore we recommended that you always explicitly set the `--max-old-space-size` `node` argument to approximately 80% of the maximum size (in megabytes) that you want to allocate the `node` process.
You might need some experimentation and adjustment to find the most appropriate value based on your specific application.

In practice, it is generally easier to provide this argument through the [`NODE_OPTIONS` environment variable](https://nodejs.org/api/cli.html#node_optionsoptions).

### Do not use Alpine

Alpine replaces glibc with musl, which is incompatible with the Rust core of the TypeScript SDK.
If you receive errors like the following, it's probably because you are using Alpine.
```

Example 2 (unknown):
```unknown
Or like this:
```

Example 3 (unknown):
```unknown
## How to run a Temporal Cloud Worker {#run-a-temporal-cloud-worker}

To run a Worker that uses [Temporal Cloud](/cloud), you need to provide additional connection and client options that include the following:

- An address that includes your [Cloud Namespace Name](/namespaces) and a port number: `<Namespace>.<ID>.tmprl.cloud:<port>`.
- mTLS CA certificate.
- mTLS private key.

For more information about managing and generating client certificates for Temporal Cloud, see [How to manage certificates in Temporal Cloud](/cloud/certificates).

For more information about configuring TLS to secure inter- and intra-network communication for a Temporal Service, see [Temporal Customization Samples](https://github.com/temporalio/samples-server).

### How to register types {#register-types}

All Workers listening to the same Task Queue name must be registered to handle the exact same Workflows Types and Activity Types.

If a Worker polls a Task for a Workflow Type or Activity Type it does not know about, it fails that Task.
However, the failure of the Task does not cause the associated Workflow Execution to fail.

In development, use [`workflowsPath`](https://typescript.temporal.io/api/interfaces/worker.WorkerOptions/#workflowspath):

<!--SNIPSTART typescript-worker-create -->
[snippets/src/worker.ts](https://github.com/temporalio/samples-typescript/blob/main/snippets/src/worker.ts)
```

Example 4 (unknown):
```unknown
<!--SNIPEND-->

In this snippet, the Worker bundles the Workflow code at runtime.

In production, you can improve your Worker's startup time by bundling in advance: as part of your production build, call `bundleWorkflowCode`:

<!--SNIPSTART typescript-bundle-workflow -->
[production/src/scripts/build-workflow-bundle.ts](https://github.com/temporalio/samples-typescript/blob/main/production/src/scripts/build-workflow-bundle.ts)
```

---

## Run the worker until SIGINT. This can be done in many ways, see "Workers" section for details.

**URL:** llms-txt#run-the-worker-until-sigint.-this-can-be-done-in-many-ways,-see-"workers"-section-for-details.

**Contents:**
  - 4. Execute the Workflow

worker.run(shutdown_signals: ['SIGINT'])
bash
ruby worker.rb
ruby
require 'temporalio/client'
require_relative 'say_hello_workflow'

**Examples:**

Example 1 (unknown):
```unknown
Run the Worker:
```

Example 2 (unknown):
```unknown
### 4. Execute the Workflow

Now that your Worker is running, it's time to start a Workflow Execution.

Create a separate file called starter.rb:
```

---

## -- BUILD STEP --

**URL:** llms-txt#---build-step---

FROM node:20-bullseye AS builder

COPY . /app
WORKDIR /app

RUN npm install --only=production \
    && npm run build

---

## Fail if timer done first

**URL:** llms-txt#fail-if-timer-done-first

raise Temporalio::Error::ApplicationError, 'Timer expired' if sleep_fut.done?

---

## Count the total number of series

**URL:** llms-txt#count-the-total-number-of-series

count({__name__=~"temporal_cloud_v1_.*"})

---

## Workflow randomness is intentionally deterministic

**URL:** llms-txt#workflow-randomness-is-intentionally-deterministic

dotnet_diagnostic.CA5394.severity = none

---

## Set up Elasticsearch index

**URL:** llms-txt#set-up-elasticsearch-index

**Contents:**
- How to migrate Visibility database {#migrating-visibility-database}
- Managing custom Search Attributes {#custom-search-attributes}
  - How to create custom Search Attributes {#create-custom-search-attributes}
  - How to remove custom Search Attributes {#remove-custom-search-attributes}
- Quick Launch - Deploying your Workers on Amazon EKS
- Before you begin
- Write your Worker code
- Containerize the Worker for Kubernetes

setup_es_index() {
    ES_SERVER="${ES_SCHEME}://${ES_SEEDS%%,*}:${ES_PORT}"
    # ES_SERVER is the URL of Elasticsearch server i.e. "http://localhost:9200".
    SETTINGS_URL="${ES_SERVER}/_cluster/settings"
    SETTINGS_FILE=${TEMPORAL_HOME}/schema/elasticsearch/visibility/cluster_settings_${ES_VERSION}.json
    TEMPLATE_URL="${ES_SERVER}/_template/temporal_visibility_v1_template"
    SCHEMA_FILE=${TEMPORAL_HOME}/schema/elasticsearch/visibility/index_template_${ES_VERSION}.json
    INDEX_URL="${ES_SERVER}/${ES_VIS_INDEX}"
    curl --fail --user "${ES_USER}":"${ES_PWD}" -X PUT "${SETTINGS_URL}" -H "Content-Type: application/json" --data-binary "@${SETTINGS_FILE}" --write-out "\n"
    curl --fail --user "${ES_USER}":"${ES_PWD}" -X PUT "${TEMPLATE_URL}" -H 'Content-Type: application/json' --data-binary "@${SCHEMA_FILE}" --write-out "\n"
    curl --user "${ES_USER}":"${ES_PWD}" -X PUT "${INDEX_URL}" --write-out "\n"

# Checks for and sets up Elasticsearch as a secondary Visibility store
    if [[ ! -z "${ES_SEC_VIS_INDEX}" ]]; then
      SEC_INDEX_URL="${ES_SERVER}/${ES_SEC_VIS_INDEX}"
      curl --user "${ES_USER}":"${ES_PWD}" -X PUT "${SEC_INDEX_URL}" --write-out "\n"
    fi
}
yaml
system.secondaryVisibilityWritingMode:
  - value: 'dual'
    constraints: {}
system.enableReadFromSecondaryVisibility:
  - value: false
    constraints: {}
yaml
   persistence:
   visibilityStore: cass-visibility
   secondaryVisibilityStore: es-visibility
   datastores:
     cass-visibility:
     cassandra:
       hosts: '127.0.0.1'
       keyspace: 'temporal_visibility'
     es-visibility:
     elasticsearch:
       version: 'v7'
       logLevel: 'error'
       url:
       scheme: 'http'
       host: '127.0.0.1:9200'
       indices:
       visibility: temporal_visibility_v1_dev
       closeIdleConnectionsInterval: 15s
   yaml
   system.secondaryVisibilityWritingMode:
   - value: "dual"
   constraints: {}
   system.enableReadFromSecondaryVisibility:
   - value: false
   constraints: {}
   yaml
   system.secondaryVisibilityWritingMode:
   - value: "dual"
   constraints: {}
   system.enableReadFromSecondaryVisibility:
   - value: true
   constraints: {}
   yaml
   persistence:
   visibilityStore: es-visibility
   datastores:
     es-visibility:
     elasticsearch:
       version: 'v7'
       logLevel: 'error'
       url:
       scheme: 'http'
       host: '127.0.0.1:9200'
       indices:
       visibility: temporal_visibility_v1_dev
       closeIdleConnectionsInterval: 15s
   
temporal operator search-attribute create --name="CustomSA" --type="Keyword"

temporal operator search-attribute create --name="CustomSA" --type="Keyword" --namespace="yournamespace"
bash
add_custom_search_attributes() {
    until temporal operator search-attribute list --namespace "${DEFAULT_NAMESPACE}"; do
      echo "Waiting for namespace cache to refresh..."
      sleep 1
    done
    echo "Namespace cache refreshed."

echo "Adding Custom*Field search attributes."

temporal operator search-attribute create --namespace "${DEFAULT_NAMESPACE}" --yes \
        --name="CustomKeywordField" --type="Keyword" \
        --name="CustomStringField" --type="Text" \
        --name="CustomTextField" --type="Text" \
        --name="CustomIntField" --type="Int" \
        --name="CustomDatetimeField" --type="Datetime" \
        --name="CustomDoubleField" --type="Double" \
        --name="CustomBoolField" --type="Bool"
}
bash
add_custom_search_attributes() {
       echo "Adding Custom*Field search attributes."
       temporal operator search-attribute create \
        --name="CustomKeywordField" --type="Keyword" \
        --name="CustomStringField" --type="Text" \
        --name="CustomTextField" --type="Text" \
        --name="CustomIntField" --type="Int" \
        --name="CustomDatetimeField" --type="Datetime" \
        --name="CustomDoubleField" --type="Double" \
        --name="CustomBoolField" --type="Bool"
}

temporal operator search-attribute remove \
    --name="your_custom_attribute"

temporal operator search-attribute remove \
    --name="your_custom_attribute" \
    --namespace="your_namespace"

temporal operator search-attribute list

temporal search-attribute list --namespace="yournamespace"
python
TEMPORAL_ADDRESS = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = os.environ.get("TEMPORAL_NAMESPACE", "default")
TEMPORAL_TASK_QUEUE = os.environ.get("TEMPORAL_TASK_QUEUE", "test-task-queue")
TEMPORAL_API_KEY = os.environ.get("TEMPORAL_API_KEY", "")

client = await Client.connect(
    TEMPORAL_ADDRESS,
    namespace=TEMPORAL_NAMESPACE,
    rpc_metadata={"temporal-namespace": TEMPORAL_NAMESPACE},
    api_key=TEMPORAL_API_KEY,
    tls=True
)
python

from temporalio.worker import Worker
from temporalio.client import Client

from workflows import your_workflow
from activities import your_first_activity, your_second_activity, your_third_activity

TEMPORAL_ADDRESS = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = os.environ.get("TEMPORAL_NAMESPACE", "default")
TEMPORAL_TASK_QUEUE = os.environ.get("TEMPORAL_TASK_QUEUE", "test-task-queue")
TEMPORAL_API_KEY = os.environ.get("TEMPORAL_API_KEY", "your-api-key")

async def main():
  client = await Client.connect(
    TEMPORAL_ADDRESS,
    namespace=TEMPORAL_NAMESPACE,
    rpc_metadata={"temporal-namespace": TEMPORAL_NAMESPACE},
    api_key=TEMPORAL_API_KEY,
    tls=True
  )

print("Initializing worker...")

# Run the worker
  worker = Worker(
    client,
    task_queue=TEMPORAL_TASK_QUEUE,
    workflows=[your_workflow],
    activities=[
      your_first_activity,
      your_second_activity,
      your_third_activity
    ]
  )

print("Starting worker... Waiting for tasks.")
  await worker.run()

if __name__ == "__main__":
  asyncio.run(main())
docker

**Examples:**

Example 1 (unknown):
```unknown
#### Update Temporal Service configuration

With the primary and secondary stores set, update the `system.secondaryVisibilityWritingMode` and `system.enableReadFromSecondaryVisibility` configuration keys in your self-hosted Temporal Service's dynamic configuration YAML file to enable read and/or write operations to the secondary Visibility store.

For example, to enable write operations to both primary and secondary stores, but disable reading from the secondary store, use the following.
```

Example 2 (unknown):
```unknown
For details on the configuration options, see:

- [Secondary Visibility dynamic configuration reference](/references/dynamic-configuration#secondary-visibility-settings)
- [Migrating Visibility databases](#migrating-visibility-database)

## How to migrate Visibility database {#migrating-visibility-database}

To migrate your Visibility database, [set up a secondary Visibility store](#dual-visibility) to enable [Dual Visibility](/dual-visibility), and update the dynamic configuration in your Temporal Service to update the read and write operations for the Visibility store.

Dual Visibility setup is optional but useful in gradually migrating your Visibility data to another database.

Before you begin, verify [supported databases and versions](/self-hosted-guide/visibility) for a Visibility store.

The following steps describe how to migrate your Visibility database.

After you make any changes to your [Temporal Service configuration](/temporal-service/configuration), ensure that you restart your services.

#### Set up secondary Visibility store

1. In your Temporal Service configuration, [add a secondary Visibility store](/references/configuration#secondaryvisibilitystore) to your Visibility setup under the Persistence configuration.

   Example: To migrate from Cassandra to Elasticsearch, add Elasticsearch as your secondary database and set it up.
   For details, see [secondary Visibility database schema and setup](#dual-visibility).
```

Example 3 (unknown):
```unknown
1. Update the [dynamic configuration](/temporal-service/configuration#dynamic-configuration) keys on your self-hosted Temporal Service to enable write operations to the secondary store and disable read operations.
   Example:
```

Example 4 (unknown):
```unknown
At this point, Visibility data is read from the primary store, and all Visibility data is written to both the primary and secondary store.
This setting applies only to new Visibility data generated after Dual Visibility is enabled.
It does not migrate any existing data in the primary store to the secondary store.

For details on write options to the secondary store, see [Secondary Visibility dynamic configuration reference](/references/dynamic-configuration#secondary-visibility-settings).

#### Run in dual mode

When you enable a secondary store, only new Visibility data is written to both primary and secondary stores.
The primary store still holds the Workflow Execution data from before the secondary store was set up.

Running in dual mode lets you plan for closed and open Workflow Executions data from before the secondary store was set up in your self-hosted Temporal Service.

Example:

- To manage closed Workflow Executions data, run in dual mode until the Namespace [Retention Period](/temporal-service/temporal-server#retention-period) is reached.
  After the Retention Period, Workflow Execution data is removed from the Persistence and Visibility stores.
  If you want to keep the closed Workflow Executions data after the set Retention Period, you must set up [Archival](/self-hosted-guide/archival).
- To manage data for all open Workflow Executions, run in dual mode until all the Workflow Executions started before enabling Dual Visibility mode are closed.
  After the Workflow Executions are closed, verify the Retention Period and set up Archival if you need to keep the data beyond the Retention Period.

You can run your Visibility setup in dual mode for an indefinite period, or until you are ready to deprecate the primary store and move completely to the secondary store without losing data.

#### Deprecate primary Visibility store

When you are ready to deprecate your primary store, follow these steps.

1. Update the dynamic configuration YAML to enable read operations from the secondary store.
   Example:
```

---

## Create start-workflow operation for use with signal-with-start

**URL:** llms-txt#create-start-workflow-operation-for-use-with-signal-with-start

start_workflow_operation = Temporalio::Client::WithStartWorkflowOperation.new(
  MyWorkflow, 'my-workflow-input',
  id: 'my-workflow-id', task_queue: 'my-workflow-task-queue'
)

---

## Don't force workflows to have static methods

**URL:** llms-txt#don't-force-workflows-to-have-static-methods

dotnet_diagnostic.CA1822.severity = none

---

## Install system dependencies

**URL:** llms-txt#install-system-dependencies

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

---

## set up PostgreSQL schema

**URL:** llms-txt#set-up-postgresql-schema

**Contents:**
- How to set up SQLite Visibility store {#sqlite}
- How to set up Cassandra Visibility store {#cassandra}

setup_postgres_schema() {
    #...

# use valid schema for the version of the database you want to set up for Visibility
    VISIBILITY_SCHEMA_DIR=${TEMPORAL_HOME}/schema/postgresql/${POSTGRES_VERSION_DIR}/visibility/versioned
    if [[ ${VISIBILITY_DBNAME} != "${POSTGRES_USER}" && ${SKIP_DB_CREATE} != true ]]; then
        temporal-sql-tool --plugin postgres --ep "${POSTGRES_SEEDS}" -u "${POSTGRES_USER}" -p "${DB_PORT}" --db "${VISIBILITY_DBNAME}" create
    fi
    temporal-sql-tool --plugin postgres --ep "${POSTGRES_SEEDS}" -u "${POSTGRES_USER}" -p "${DB_PORT}" --db "${VISIBILITY_DBNAME}" update-schema -d "${VISIBILITY_SCHEMA_DIR}"
  #...
}
yaml
persistence:
  # ...
  visibilityStore: sqlite-visibility
  # ...
  datastores:
    # ...
    sqlite-visibility:
      sql:
        user: 'username_for_auth'
        password: 'password_for_auth'
        pluginName: 'sqlite'
        databaseName: 'default'
        connectAddr: 'localhost'
        connectProtocol: 'tcp'
        connectAttributes:
          mode: 'memory'
          cache: 'private'
        maxConns: 1
        maxIdleConns: 1
        maxConnLifetime: '1h'
        tls:
          enabled: false
          caFile: ''
          certFile: ''
          keyFile: ''
          enableHostVerification: false
          serverName: ''
yaml
#...
persistence:
  #...
  visibilityStore: cass-visibility
  #...
  datastores:
    default:
    #...
    cass-visibility:
      cassandra:
        hosts: '127.0.0.1'
        keyspace: 'temporal_visibility'
#...
bash
#...

**Examples:**

Example 1 (unknown):
```unknown
Note that the script uses [temporal-sql-tool](https://github.com/temporalio/temporal/blob/3b982585bf0124839e697952df4bba01fe4d9543/tools/sql/main.go) to run the setup.

## How to set up SQLite Visibility store {#sqlite}

:::tip Support, stability, and dependency info

- SQLite v3.31.0 and later.

:::

You can set SQLite as your [Visibility store](/temporal-service/visibility).
Verify [supported versions](/self-hosted-guide/visibility) before you proceed.

Temporal supports only an in-memory database with SQLite; this means that the database is automatically created when Temporal Server starts and is destroyed when Temporal Server stops.

You can change the configuration to use a file-based database so that it is preserved when Temporal Server stops.
However, if you use a file-based SQLite database, upgrading your database schema to enable advanced Visibility features is not supported; in this case, you must delete the database and create it again to upgrade.

If using SQLite v3.31.0 and later as your Visibility store with Temporal Server v1.20 and later, any [custom Search Attributes](/search-attribute#custom-search-attribute) that you create must be associated with a Namespace in that Temporal Service.

**Persistence configuration**

Set your SQLite Visibility store name in the `visibilityStore` parameter in your Persistence configuration, and then define the Visibility store configuration under `datastores`.

The following example shows how to set a Visibility store `sqlite-visibility` and define the datastore configuration in your Temporal Service configuration YAML.
```

Example 2 (unknown):
```unknown
SQLite (v3.31.0 and later) has advanced Visibility enabled by default.

**Database schema and setup**

Visibility data is stored in a database table called `executions_visibility` that must be set up according to the schemas defined (by supported versions) in https://github.com/temporalio/temporal/blob/main/schema/sqlite/v3/visibility/schema.sql.

For an example of setting up the SQLite schema, see [Temporalite](https://github.com/temporalio/temporalite/blob/main/server.go) setup.

## How to set up Cassandra Visibility store {#cassandra}

:::tip Support, stability, and dependency info

- Support for Cassandra as a Visibility database is deprecated beginning with Temporal Server v1.21. For updates, check the [Temporal Server release notes](https://github.com/temporalio/temporal/releases).
- We recommend migrating from Cassandra to any of the other supported databases for Visibility.

:::

You can set Cassandra as your [Visibility store](/temporal-service/visibility).
Verify [supported versions](/self-hosted-guide/visibility) before you proceed.

Advanced Visibility is not supported with Cassandra.

To enable advanced Visibility features, use any of the supported databases, such as MySQL, PostgreSQL, SQLite, or Elasticsearch, as your Visibility store.
We recommend using Elasticsearch for any Temporal Service setup that handles more than a few Workflow Executions because it supports the request load on the Visibility store and helps optimize performance.

To migrate from Cassandra to a supported SQL database, see [Migrating Visibility database](#migrating-visibility-database).

**Persistence configuration**

Set your Cassandra Visibility store name in the `visibilityStore` parameter in your Persistence configuration, and then define the Visibility store configuration under `datastores`.

The following example shows how to set a Visibility store `cass-visibility` and define the datastore configuration in your Temporal Service configuration YAML.
```

Example 3 (unknown):
```unknown
**Database schema and setup**

Visibility data is stored in a database table called `executions_visibility` that must be set up according to the schemas defined (by supported versions) in https://github.com/temporalio/temporal/tree/main/schema/cassandra/visibility.

The following example shows how the [auto-setup.sh](https://github.com/temporalio/docker-builds/blob/main/docker/auto-setup.sh) script sets up your Visibility store.
```

---

## Default profile for local development

**URL:** llms-txt#default-profile-for-local-development

[profile.default]
address = "localhost:7233"
namespace = "default"

---

## Perform signal-with-start

**URL:** llms-txt#perform-signal-with-start

**Contents:**
  - Send an Update {#send-update-from-client}

handle = client.signal_with_start_workflow(
  MyWorkflow.my_signal, 'signal-input', start_workflow_operation:
)
ruby
  prev_language = handle.execute_update(MessagePassingSimple::GreetingWorkflow.set_language, :chinese)
  ruby
  # Start an update and then wait for it to complete
  update_handle = handle.start_update(
    MessagePassingSimple::GreetingWorkflow.apply_language_with_lookup,
    :arabic,
    wait_for_stage: Temporalio::Client::WorkflowUpdateWaitStage::ACCEPTED
  )
  prev_language = update_handle.result
  ruby
client = Temporalio::Client.connect('localhost:7233', 'default')

**Examples:**

Example 1 (unknown):
```unknown
### Send an Update {#send-update-from-client}

An Update is a synchronous, blocking call that can change Workflow state, control its flow, and return a result.

A Client sending an Update must wait until the Server delivers the Update to a Worker.
Workers must be available and responsive.
If you need a response as soon as the Server receives the request, use a Signal instead.
Also note that you can't send Updates to other Workflow Executions.

- `WorkflowExecutionUpdateAccepted` is added to the Event History when the Worker confirms that the Update passed validation.
- `WorkflowExecutionUpdateCompleted` is added to the Event History when the Worker confirms that the Update has finished.

To send an Update to a Workflow Execution, you can:

- Call the Update method with `execute_update` from the Workflow handle and wait for the Update to complete.
  This code fetches an Update result:
```

Example 2 (unknown):
```unknown
- 2. Use `start_update` to receive a handle as soon as the Update is accepted.
     It returns a `WorkflowUpdateHandle`

  - Use this `WorkflowUpdateHandle` later to fetch your results.
  - Asynchronous Update handlers normally perform long-running async Activities.
  - `start_update` only waits until the Worker has accepted or rejected the Update, not until all asynchronous operations are complete.

  For example:
```

Example 3 (unknown):
```unknown
For more details, see the "Async handlers" section.

#### Update-With-Start {#update-with-start}

:::tip Stability

In [Public Preview](/evaluate/development-production-features/release-stages#public-preview) in Temporal Cloud.

Minimum Temporal Server version [Temporal Server version 1.26](https://github.com/temporalio/temporal/releases/tag/v1.26.2)

:::

[Update-with-Start](/sending-messages#update-with-start) lets you [send an Update](/develop/ruby/message-passing#send-update-from-client) that checks whether an already-running Workflow with that ID exists:

- If the Workflow exists, the Update is processed.
- If the Workflow does not exist, a new Workflow Execution is started with the given ID, and the Update is processed before the main Workflow method starts to execute.

Use `execute_update_with_start_workflow` to start the Update and wait for the result in one go.

Alternatively, use `start_update_with_start_workflow` to start the Update and receive a `WorkflowUpdateHandle`, and then use `update_handle.result` to retrieve the result from the Update.

These calls return once the requested Update wait stage has been reached, or when the request times out.

- You will need to provide a `WithStartWorkflowOperation` to define the Workflow that will be started if necessary, and its arguments.
- You must specify an [id_conflict_policy](/workflow-execution/workflowid-runid#workflow-id-conflict-policy) when creating the `WithStartWorkflowOperation`.
  Note that a `WithStartWorkflowOperation` can only be used once.

Here's an example:
```

---

## This causes a Workflow Task failure (retries automatically)

**URL:** llms-txt#this-causes-a-workflow-task-failure-(retries-automatically)

**Contents:**
- Handle exceptions in Workflows {#handle-exceptions-in-workflows}
- Configure custom Retry Policies {#configure-custom-retry-policies}
  - Match your Retry Policy to failure types
  - Use different policies for different Activities

raise ValueError("Unexpected condition")
python
from temporalio import workflow
from temporalio.exceptions import ActivityError, ApplicationError
from datetime import timedelta

@workflow.defn
class MoneyTransferWorkflow:
    @workflow.run
    async def run(self, details):
        # Withdraw money
        try:
            withdraw_result = await workflow.execute_activity(
                withdraw,
                details,
                start_to_close_timeout=timedelta(seconds=10)
            )
        except ActivityError as e:
            raise ApplicationError(
                f"Withdrawal failed: {e.cause}",
                type="WithdrawalError"
            )

# Deposit money
        try:
            deposit_result = await workflow.execute_activity(
                deposit,
                details,
                start_to_close_timeout=timedelta(seconds=10)
            )
        except ActivityError as e:
            # Deposit failed - attempt refund
            try:
                await workflow.execute_activity(
                    refund,
                    withdraw_result,
                    start_to_close_timeout=timedelta(seconds=10)
                )
                raise ApplicationError(
                    f"Deposit failed but money refunded to source account",
                    type="DepositError"
                )
            except ActivityError as refund_err:
                raise ApplicationError(
                    f"Deposit failed and refund also failed: {refund_err.cause}",
                    type="CriticalTransferError"
                )

return f"Transfer complete: {withdraw_result}, {deposit_result}"
python
from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order):
        # Custom retry for rate-limited service
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=10),
            backoff_coefficient=3.0,
            maximum_interval=timedelta(minutes=5),
            maximum_attempts=20,
        )

result = await workflow.execute_activity(
            call_external_service,
            order,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy,
        )
        return result
python
fast_retry = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=1.5,
)

slow_retry = RetryPolicy(
    initial_interval=timedelta(seconds=30),
    backoff_coefficient=3.0,
)

**Examples:**

Example 1 (unknown):
```unknown
This is intentional.
Regular Python exceptions are treated as bugs that can be fixed with a code deployment, not business logic failures.
The Workflow Task retries indefinitely, letting you fix the bug and redeploy without losing Workflow state.

## Handle exceptions in Workflows {#handle-exceptions-in-workflows}

**How to handle exceptions in Workflows using the Temporal Python SDK**

Use Python's `try/except` blocks to handle Activity failures in your Workflow:
```

Example 2 (unknown):
```unknown
Common Temporal exceptions you can catch in Workflows:
- `ActivityError` - Activity failed after exhausting retries
- `ChildWorkflowError` - Child Workflow failed
- `CancelledError` - Workflow, Activity, or Timer was canceled
- `TimeoutError` - Operation exceeded timeout

If these exceptions propagate unhandled, the Workflow Execution fails (or enters "Canceled" state for `CancelledError`).

## Configure custom Retry Policies {#configure-custom-retry-policies}

**How to configure custom Retry Policies using the Temporal Python SDK**

Activities have a default Retry Policy with unlimited attempts and exponential backoff.
Customize this to match your expected failure patterns.
```

Example 3 (unknown):
```unknown
Retry Policy attributes:
- **`initial_interval`**: Delay before first retry (default: 1 second)
- **`backoff_coefficient`**: Multiplier for subsequent delays (default: 2.0)
- **`maximum_interval`**: Cap on retry delay (default: 100× initial interval)
- **`maximum_attempts`**: Maximum retry attempts (default: unlimited)
- **`non_retryable_error_types`**: Error types that shouldn't retry (default: empty)

### Match your Retry Policy to failure types

**For transient failures** (brief network issues): Use the defaults or a low `initial_interval` and `backoff_coefficient`.

**For intermittent failures** (rate limiting): Increase `initial_interval` and `backoff_coefficient` to space out retries and let the condition resolve.

**For cost-sensitive APIs**: Set `maximum_attempts` to limit retries (rare—usually prefer timeouts).

### Use different policies for different Activities

You can use different Retry Policies for different Activities, or even multiple policies for the same Activity:
```

---

## set your MySQL environment variables

**URL:** llms-txt#set-your-mysql-environment-variables

: "${DBNAME:=temporal}"
: "${VISIBILITY_DBNAME:=temporal_secondary_visibility}"
: "${DB_PORT:=}"
: "${MYSQL_SEEDS:=}"
: "${MYSQL_USER:=}"
: "${MYSQL_PWD:=}"
: "${MYSQL_TX_ISOLATION_COMPAT:=false}"

---

## start_workflow instead.

**URL:** llms-txt#start_workflow-instead.

handle = my_client.workflow_handle('my-workflow-id')

---

## Clean up the temporary label

**URL:** llms-txt#clean-up-the-temporary-label

**Contents:**
- Limits
- FAQ
  - Q: Will metrics match between promQL and OpenMetrics endpoints?
  - Q: Can I still query metrics directly (e.g. with a Grafana dashboard)?
  - Q: What happens to my existing dashboards and alerts?
  - Q: Will historical data be preserved?
  - Q: Are there limits to how frequently I can scrape or how much data will be returned?
  - Q: Why are some metrics missing from my scrapes? I don’t see all the metrics documented.
- Prometheus Grafana setup
- Temporal Cloud metrics setup

- regex: '__tmp_keep_original'
  action: labeldrop

(temporal_cloud_v1_workflow_failed_count{namespace="production"} or vector(0))

curl -v --cert <path to your client-cert.pem> --key <path to your client-cert.key> "<your generated Temporal Cloud prometheus_endpoint>/api/v1/query?query=temporal_cloud_v0_state_transition_count"
   java
//You need the following packages to set up metrics in Java.
//See the Developer's guide for packages required for other SDKs.

//…
   {
     // See the Micrometer documentation for configuration details on other supported monitoring systems.
     // Set up the Prometheus registry.
     PrometheusMeterRegistry yourRegistry = new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);

public static Scope yourScope(){
     //Set up a scope, report every 10 seconds
       Scope yourScope = new RootScopeBuilder()
               .tags(ImmutableMap.of(
                       "customtag1",
                       "customvalue1",
                       "customtag2",
                       "customvalue2"))
               .reporter(new MicrometerClientStatsReporter(yourRegistry))
               .reportEvery(Duration.ofSeconds(10));

//Start Prometheus scrape endpoint at port 8077 on your local host
     HttpServer scrapeEndpoint = startPrometheusScrapeEndpoint(yourRegistry, 8077);
     return yourScope;
   }

/**
    * Starts HttpServer to expose a scrape endpoint. See
    * https://micrometer.io/docs/registry/prometheus for more info.
    */

public static HttpServer startPrometheusScrapeEndpoint(
           PrometheusMeterRegistry yourRegistry, int port) {
       try {
           HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
           server.createContext(
                   "/metrics",
                   httpExchange -> {
                       String response = registry.scrape();
                       httpExchange.sendResponseHeaders(200, response.getBytes(UTF_8).length);
                       try (OutputStream os = httpExchange.getResponseBody()) {
                           os.write(response.getBytes(UTF_8));
                       }
                   });
           server.start();
           return server;
       } catch (IOException e) {
           throw new RuntimeException(e);
       }
   }
}

// With your scrape endpoint configured, set the metrics scope in your Workflow service stub and
// use it to create a Client to start your Workers and Workflow Executions.

//…
{
    //Create Workflow service stubs to connect to the Frontend Service.
    WorkflowServiceStubs service = WorkflowServiceStubs.newServiceStubs(
               WorkflowServiceStubsOptions.newBuilder()
                      .setMetricsScope(yourScope()) //set the metrics scope for the WorkflowServiceStubs
                      .build());

//Create a Workflow service client, which can be used to start, signal, and query Workflow Executions.
   WorkflowClient yourClient = WorkflowClient.newInstance(service,
          WorkflowClientOptions.newBuilder().build());
}

//…
yaml
global:
  scrape_interval: 10s # Set the scrape interval to every 10 seconds. Default is every 1 minute.
#...

**Examples:**

Example 1 (unknown):
```unknown
## Limits

See [API limits](/production-deployment/cloud/metrics/openmetrics/api-reference#api-limits) for details.

## FAQ

### Q: Will metrics match between promQL and OpenMetrics endpoints?
No. The metrics will be approximately the same but due to aggregation differences and windowing, values likely won't match exactly between the two endpoints. 
Some metrics may be consistently different such as `temporal_cloud_v1_total_action_count` which includes History Export actions in the OpenMetrics endpoint. In the case of consistent differences
the OpenMetrics endpoint is considered to be more accurate.

### Q: Can I still query metrics directly (e.g. with a Grafana dashboard)?

Currently, the OpenMetrics endpoint requires an observability platform to collect and query metrics. Direct querying via API to return a time series of data is not supported. Supporting this type of query pattern is a future roadmap item.

### Q: What happens to my existing dashboards and alerts?

During the transition period, both endpoints remain active.

### Q: Will historical data be preserved?

Historical data from the query endpoint will remain in your observability platform. To maintain continuity:

* Combine old (`v0`) and new (`v1`) metrics in your queries during transition  
* Consider using the PromQL `or` operator: `metric_v1 or metric_v0`

### Q: Are there limits to how frequently I can scrape or how much data will be returned?

The limits are documented [here](/production-deployment/cloud/metrics/openmetrics/api-reference#api-limits).

### Q: Why are some metrics missing from my scrapes? I don’t see all the metrics documented.

The OpenMetrics endpoint only returns metrics that were generated during the one-minute aggregation window. This is different from the query endpoint which might return zeros.

**What this means:**

* If no workflows failed in the last minute, `temporal_cloud_v1_workflow_failed_count` won't appear in that scrape.
* If a specific task queue had no activity, its metrics will be absent.
* The set of metrics returned varies between scrapes based on system activity.

**This is normal behavior.** Unlike some metrics systems that populate zeros, the OpenMetrics endpoint follows a sparse reporting pattern \- metrics only appear when there's actual data to report.

**How to handle this in queries:**
```

Example 2 (unknown):
```unknown
This ensures your dashboards and alerts work correctly even when metrics are temporarily absent due to no activity.

---

## Prometheus Grafana setup

**How to set up Grafana with Temporal Cloud observability to view metrics.**

Temporal Cloud and SDKs generate metrics for monitoring performance and troubleshooting errors.

Temporal Cloud emits metrics through a [Prometheus HTTP API endpoint](https://prometheus.io/docs/prometheus/latest/querying/api/), which can be directly used as a Prometheus data source in Grafana or to query and export Cloud metrics to any observability platform.

The open-source SDKs require you to set up a Prometheus scrape endpoint for Prometheus to collect and aggregate the Worker and Client metrics.

This section describes how to set up your Temporal Cloud and SDK metrics and use them as data sources in Grafana.

The process for setting up observability includes the following steps:

1. Create or get your Prometheus endpoint for Temporal Cloud metrics and enable SDK metrics.
   - For Temporal Cloud, [generate a Prometheus HTTP API endpoint](/production-deployment/cloud/metrics/general-setup) on Temporal Cloud using valid certificates.
   - For SDKs, [expose a metrics endpoint](#sdk-metrics-setup) where Prometheus can scrape SDK metrics and [run Prometheus](#prometheus-configuration) on your host. The examples in this article describe running Prometheus on your local machine where you run your application code.
2. Run Grafana and [set up data sources for Temporal Cloud and SDK metrics](#grafana-data-sources-configuration) in Grafana. The examples in this article describe running Grafana on your local host where you run your application code.
3. [Create dashboards](#grafana-dashboards-setup) in Grafana to view Temporal Cloud metrics and SDK metrics. Temporal provides [sample community-driven Grafana dashboards](https://github.com/temporalio/dashboards) for Cloud and SDK metrics that you can use and customize according to your requirements.

If you're following through with the examples provided here, ensure that you have the following:

- Root CA certificates and end-entity certificates. See [Certificate requirements](/cloud/certificates#certificate-requirements) for details.
- Set up your connections to Temporal Cloud using an SDK of your choice and have some Workflows running on Temporal Cloud. See Connect to a Temporal Service for details.

  - [Go](/develop/go/temporal-client#connect-to-temporal-cloud)
  - [Java](/develop/java/temporal-client#connect-to-temporal-cloud)
  - [PHP](/develop/php/temporal-client#connect-to-a-dev-cluster)
  - [Python](/develop/python/temporal-client#connect-to-temporal-cloud)
  - [TypeScript](/develop/typescript/core-application#connect-to-temporal-cloud)
  - [.NET](/develop/dotnet/temporal-client#connect-to-temporal-cloud)

- Prometheus and Grafana installed.

## Temporal Cloud metrics setup

Before you set up your Temporal Cloud metrics, ensure that you have the following:

- Account Owner or Global Admin [role privileges](/cloud/users#account-level-roles) for the Temporal Cloud account.
- [CA certificate and key](/cloud/certificates) for the Observability integration.
  You will need the certificate to set up the Observability endpoint in Temporal Cloud.

The following steps describe how to set up Observability on Temporal Cloud to generate an endpoint:

1. Log in to Temporal Cloud UI with an Account Owner or Global Admin [role](/cloud/users#account-level-roles).
2. Go to **Settings** and select **Integrations**.
3. Select **Configure Observability** (if you're setting it up for the first time) or click **Edit** in the Observability section (if it was already configured before).
4. Add your root CA certificate (.pem) and save it.
   Note that if an observability endpoint is already set up, you can append your root CA certificate here to use the generated observability endpoint with your instance of Grafana.
5. To test your endpoint, run the following command on your host:
```

Example 3 (unknown):
```unknown
If you have Workflows running on a Namespace in your Temporal Cloud instance, you should see some data as a result of running this command.
6. Copy the HTTP API endpoint that is generated (it is shown in the UI).

This endpoint should be configured as a data source for Temporal Cloud metrics in Grafana.
See [Data sources configuration for Temporal Cloud and SDK metrics in Grafana](#grafana-data-sources-configuration) for details.

## SDK metrics setup

SDK metrics are emitted by SDK Clients used to start your Workers and to start, signal, or query your Workflow Executions.
You must configure a Prometheus scrape endpoint for Prometheus to collect and aggregate your SDK metrics.
Each language development guide has details on how to set this up.

- [Go SDK](/develop/go/observability#metrics)
- [Java SDK](/develop/java/observability#metrics)
- [TypeScript SDK](/develop/typescript/observability#metrics)
- [Python](/develop/python/observability#metrics)
- [.NET](/develop/dotnet/observability#metrics)

The following example uses the Java SDK to set the Prometheus registry and Micrometer stats reporter, set the scope, and expose an endpoint from which Prometheus can scrape the SDK metrics.
```

Example 4 (unknown):
```unknown
To check whether your scrape endpoints are emitting metrics, run your code and go to [http://localhost:8077/metrics](http://localhost:8077/metrics) to verify that you see the SDK metrics.

You can set up separate scrape endpoints in your Clients that you use to start your Workers and Workflow Executions.

For more examples on setting metrics endpoints in other SDKs, see the metrics samples:

- [Java SDK Samples](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/metrics)
- [Go SDK Samples](https://github.com/temporalio/samples-go/tree/main/metrics)

## SDK metrics Prometheus Configuration {#prometheus-configuration}

**How to configure Prometheus to ingest Temporal SDK metrics.**

For Temporal SDKs, you must have Prometheus running and configured to listen on the scrape endpoints exposed in your application code.

For this example, you can run Prometheus locally or as a Docker container.
In either case, ensure that you set the listen targets to the ports where you expose your scrape endpoints.
When you run Prometheus locally, set your target address to port 8077 in your Prometheus configuration YAML file. (We set the scrape endopint to port 8077 in the [SDK metrics setup](#sdk-metrics-setup) example.)

Example:
```

---

## my_worker_file.py

**URL:** llms-txt#my_worker_file.py

**Contents:**
- Temporal Python SDK synchronous vs. asynchronous Activity implementations
- The Python Asynchronous Event Loop and Blocking Calls
- Python SDK Worker Execution Architecture
  - Activities
  - Workflows
  - Number of CPU cores
  - A Worker infrastructure option: Separate Activity and Workflow Workers
- Activity Definition
- How to implement Synchronous Activities

from temporalio.worker import Worker
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner, SandboxRestrictions

my_worker = Worker(
  ...,
  workflow_runner=SandboxedWorkflowRunner(
    restrictions=SandboxRestrictions.default.with_import_notification_policy( 
      workflow.SandboxImportNotificationPolicy.WARN_ON_DYNAMIC_IMPORT | workflow.SandboxImportNotificationPolicy.WARN_ON_UNINTENTIONAL_PASSTHROUGH
    )
  )
)
python

from temporalio import activity

class TranslateActivities:

@activity.defn
    def greet_in_spanish(self, name: str) -> str:
        greeting = self.call_service("get-spanish-greeting", name)
        return greeting

# Utility method for making calls to the microservices
    def call_service(self, stem: str, name: str) -> str:
        base = f"http://localhost:9999/{stem}"
        url = f"{base}?name={urllib.parse.quote(name)}"

response = requests.get(url)
        return response.text
python
@activity.defn
def greet_in_spanish(name: str) -> str:
    greeting = call_service("get-spanish-greeting", name)
    return greeting

**Examples:**

Example 1 (unknown):
```unknown
The [`sandbox_import_notification_policy`](https://python.temporal.io/temporalio.workflow.unsafe.html#sandbox_import_notification_policy) context manager will always be respected if used in combination with the restrictions customization. 

For more information on the Python sandbox, see the following resources.

- [Python SDK README](https://github.com/temporalio/sdk-python)
- [Python API docs](https://python.temporal.io/index.html)

---

## Temporal Python SDK synchronous vs. asynchronous Activity implementations

The Temporal Python SDK supports multiple ways of implementing an Activity:

- Asynchronously using [`asyncio`](https://docs.python.org/3/library/asyncio.html)
- Synchronously multithreaded using [`concurrent.futures.ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
- Synchronously multiprocess using [`concurrent.futures.ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor) and [`multiprocessing.managers.SyncManager`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.managers.SyncManager)

It is important to implement your Activities using the correct method, otherwise
your application may fail in sporadic and unexpected ways. Which one you should
use depends on your use case. This section provides guidance to help you choose
the best approach.

## The Python Asynchronous Event Loop and Blocking Calls

First, let's look at how async event loops work in Python. The Python async
event loop runs in a thread and executes all tasks in its thread. When any
task is running in the event loop, the loop is blocked and no other tasks can be
running at the same time within that event loop. Whenever a task executes an
`await` expression, the task is suspended, and the event loop begins or resumes
execution of another task.

This means that the event loop can only pass the flow of control when the `await`
keyword is executed. If a program makes a blocking call, such as one that reads
from a file, makes a synchronous request to a network service, waits for user input,
or anything else that blocks the execution, the entire event loop must wait until
that execution has completed.

Blocking the async event loop in Python would turn your asynchronous program
into a synchronous program that executes serially, defeating the entire purpose
of using `asyncio`. This can also lead to potential deadlock, and unpredictable behavior
that causes tasks to be unable to execute. Debugging these issues can be difficult
and time consuming, as locating the source of the blocking call might not always
be immediately evident.

Due to this, Python developers must be extra careful to not make blocking calls
from within an asynchronous Activity, or use an async safe library to perform
these actions.

For example, making an HTTP call with the popular `requests` library within an
asynchronous Activity would lead to blocking your event loop. If you want to make
an HTTP call from within an asynchronous Activity, you should use an async-safe HTTP library
such as `aiohttp` or `httpx`. Otherwise, use a synchronous Activity.

## Python SDK Worker Execution Architecture

Python workers have following components for executing code:

- Your event loop, which runs Tasks from async Activities **plus the rest of the Temporal Worker, such as communicating with the server**.
- An executor for executing Activity Tasks from synchronous Activities. A thread pool executor is recommended.
- A thread pool executor for executing Workflow Tasks.

> See Also: [docs for](https://python.temporal.io/temporalio.worker.Worker.html#__init__) `worker.__init__()`

### Activities

- Async Activities and the temporal worker SDK code both run the default asyncio event loop or whatever event loop you give the Worker.
- Synchronous Activities run in the `activity_executor`.

### Workflows

Since Workflow Tasks have the following three properties, they're run in threads.

- are CPU bound
- need to be timed out for deadlock detection
- need to not block other Workflow Tasks

The `workflow_task_executor` is the thread pool these Tasks are run on.
The fact that Workflow Tasks run in a thread pool can be confusing at first because Workflow Definitions are `async`.
The key differentiator is that the `async` in Workflow Definitions isn't referring to the standard event loop -- it's referring to the Workflow's own event loop.
Each Workflow gets its own “Workflow event loop,” which is deterministic, and described in [the Python SDK blog](https://temporal.io/blog/durable-distributed-asyncio-event-loop#temporal-workflows-are-asyncio-event-loops).
The Workflow event loop doesn't constantly loop -- it just gets cycled through during a Workflow Task to make as much progress as possible on all of its futures.
When it can no longer make progress on any of its futures, then the Workflow Task is complete.

### Number of CPU cores

The only ways to use more than one core in a python Worker (considering Python's GIL) are:

- Run more than one Worker Process.
- Run the synchronous Activities in a process pool executor, but a thread pool executor is recommended.

### A Worker infrastructure option: Separate Activity and Workflow Workers

To reduce the risk of event loops or executors getting blocked,
some users choose to deploy separate Workers for Workflow Tasks and Activity Tasks.

## Activity Definition

**By default, Activities should be synchronous rather than asynchronous**.
You should only make an Activity asynchronous if you are
certain that it doesn't block the event loop.

This is because if you have blocking code in an `async def` function,
it blocks your event loop and the rest of Temporal, which can cause bugs that are
hard to diagnose, including freezing your worker and blocking Workflow progress
(because Temporal can't tell the server that Workflow Tasks are completing).
The reason synchronous Activities help is because they
run in the `activity_executor` ([docs for](https://python.temporal.io/temporalio.worker.Worker.html#__init__) `worker.__init__()`)
rather than in the global event loop,
which helps because:

- There's no risk of accidentally blocking the global event loop.
- If you have multiple
  Activity Tasks running in a thread pool rather than an event loop, one bad
  Activity Task can't slow down the others; this is because the OS scheduler preemptively
  switches between threads, which the event loop coordinator doesn't do.

> See Also:
> ["Types of Activities" section of Python SDK README](https://github.com/temporalio/sdk-python#types-of-activities)

## How to implement Synchronous Activities

The following code is a synchronous Activity Definition.
It takes a name (`str`) as input and returns a
customized greeting (`str`) as output.

It makes a call to a microservice, and when making this call,
you'll notice that it uses the `requests` library. This is safe to do in
synchronous Activities.
```

Example 2 (unknown):
```unknown
The preceding example doesn't share a session across the Activity, so
`__init__` was removed. While `requests` does have the ability to create sessions,
it's currently unknown if they're thread safe. Due to no longer having or needing
`__init__`, the case could be made here to not implement the Activities as a class,
but just as decorated functions as shown here:
```

---

## Capture token for later completion

**URL:** llms-txt#capture-token-for-later-completion

captured_token = Temporalio::Activity::Context.current.info.task_token

---

## Just a resource based tuner, with poller autoscaling

**URL:** llms-txt#just-a-resource-based-tuner,-with-poller-autoscaling

tuner = WorkerTuner.create_resource_based(
    target_memory_usage=0.5,
    target_cpu_usage=0.5,
)
worker = Worker(
    client,
    task_queue="foo",
    tuner=tuner,
    workflow_task_poller_behavior=PollerBehaviorAutoscaling(),
    activity_task_poller_behavior=PollerBehaviorAutoscaling()
)

---

## Send cancellation. This returns when cancellation is received by the server. Wait on

**URL:** llms-txt#send-cancellation.-this-returns-when-cancellation-is-received-by-the-server.-wait-on

---

## OR using short alias

**URL:** llms-txt#or-using-short-alias

**Contents:**
  - --active_cluster
  - --clusters
  - --description
  - --global_namespace
  - --history_archival_state
  - --history_uri
  - --namespace_data
  - --owner_email
  - --retention
  - --visibility_archival_state

tctl --ns your-namespace n re
bash
tctl namespace register --active_cluster <name>
bash
tctl namespace register --clusters <names>
bash
tctl namespace register --description <value>
bash
tctl namespace register --global_namespace <boolean>
bash
tctl namespace register --history_archival_state <value>
bash
tctl namespace register --history_uri <uri>
bash
tctl namespace register --namespace_data <data>
bash
tctl namespace register --owner_email <value>
bash
tctl namespace register --retention <value>
bash
tctl namespace register --visibility_archival_state <value>
bash
tctl namespace register --visibility_uri <uri>
bash
tctl namespace update --active_cluster <name>
bash
tctl namespace update --add_bad_binary <value>
bash
tctl namespace update --clusters <names>
bash
tctl namespace update --description <value>
bash
tctl namespace update --history_archival_state <value>
bash
tctl namespace update --history_uri <uri>
bash
tctl namespace update --namespace_data <data>
bash
tctl namespace update --owner_email <value>
bash
tctl namespace update --reason <value>
bash
tctl namespace update --remove_bad_binary <value>
bash
tctl namespace update --retention <value>
bash
tctl namespace update --visibility_archival_state <value>
bash
tctl namespace update --visibility_uri <uri>
shell
tctl schedule backfill --sid 'your-schedule-id' \
  --overlap-policy 'BufferAll'                \
  --start-time '2022-05-01T00:00:00Z'         \
  --end-time   '2022-05-31T23:59:59Z'
shell
$ tctl config set version next   # ensure you're using the new tctl
$ tctl schedule create \
    --schedule-id 'your-schedule-id' \
    --interval '5h/15m' \
    --calendar '{"dayOfWeek":"Fri","hour":"11","minute":"3"}' \
    --overlap-policy 'BufferAll' \
    --workflow-id 'your-workflow-id' \
    --task-queue 'your-task-queue' \
    --workflow-type 'YourWorkflowType'
shell
$ tctl schedule create \
    --schedule-id 'your-schedule-id' \
    --cron '3 11 * * Fri' \
    --workflow-id 'your-workflow-id' \
    --task-queue 'your-task-queue' \
    --workflow-type 'YourWorkflowType'

┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
shell
$ tctl schedule delete --schedule-id 'your-schedule-id'
shell
tctl schedule describe --schedule-id 'your-schedule-id'
shell
tctl schedule list
shell
$ tctl schedule toggle --schedule-id 'your-schedule-id' --pause --reason "paused because the database is down"
$ tctl schedule toggle --schedule-id 'your-schedule-id' --unpause --reason "the database is back up"
shell
$ tctl schedule trigger --schedule-id 'your-schedule-id'
shell
$ tctl schedule trigger --schedule-id 'your-schedule-id' --overlap-policy 'AllowAll'
bash
tctl taskqueue describe --taskqueue <value>
bash
tctl taskqueue describe --taskqueue <value> --taskqueuetype <type>
bash
tctl taskqueue list-partition --taskqueue <value>
bash
tctl workflow cancel --workflow_id <id>
bash
tctl workflow cancel --run_id <id>
bash
tctl workflow count --query 'ExecutionStatus="Running"'
bash
tctl workflow describe --workflow_id <id>
bash
tctl workflow describe --run_id <id>
bash
tctl workflow describe --print_raw
bash
tctl workflow describe --reset_points_only
bash
tctl workflow describeid <workflow_id> <id> --print_raw
bash
tctl workflow describeid <workflow_id> --reset_points_only
bash
tctl workflow list --print_raw_time
bash
tctl workflow list --print_datetime
bash
tctl workflow list --print_memo
bash
tctl workflow list --print_search_attr
bash
tctl workflow list --print_full
bash
tctl workflow list --print_json
bash
tctl workflow list --open
bash
tctl workflow list --earliest-time '2022-01-02T15:04:05+05:30'
bash
tctl workflow list --earliest-time '15minute'
bash
tctl workflow list --latest_time '2022-04-13T23:02:17-07:00'
bash
tctl workflow list --latest_time '10second'
bash
tctl workflow list --workflow_id <id>
bash
tctl workflow list --workflow_type <name>
bash
tctl workflow list --status <value>
bashbash
tctl workflow list --query "WorkflowId=<your-workflow-id>"
bashbash
tctl workflow list \
  --query "WorkflowType='main.SampleParentWorkflow' AND ExecutionStatus='Running'"
bashbash
tctl workflow list \
  --query '(CustomKeywordField = "keyword1" and CustomIntField >= 5) or CustomKeywordField = "keyword2"' \
  --print_search_attr
bashbash
tctl workflow list \
  --query 'CustomKeywordField in ("keyword2", "keyword1") and CustomIntField >= 5 and CloseTime between "2018-06-07T16:16:36-08:00" and "2019-06-07T16:46:34-08:00" order by CustomDatetimeField desc' \
  --print_search_attr
bashbash
tctl workflow list \
  --query 'WorkflowType = "main.Workflow" and (WorkflowId = "1645a588-4772-4dab-b276-5f9db108b3a8" or RunId = "be66519b-5f09-40cd-b2e8-20e4106244dc")'
bashbash
tctl workflow list \
  --query 'WorkflowType = "main.Workflow" StartTime > "2019-06-07T16:46:34-08:00" and ExecutionStatus = "Running"'
bash
tctl workflow list --more
bash
tctl workflow list --pagesize <value>
bash
tctl workflow listall --print_raw_time
bash
tctl workflow listall --print_datetime
bash
tctl workflow listall --print_memo
bash
tctl workflow listall --print_search_attr
bash
tctl workflow listall --print_full
bash
tctl workflow listall --print_json
bash
tctl workflow listall --open
bash
tctl workflow listall --earliest-time '2022-01-02T15:04:05+05:30'
bash
tctl workflow listall --earliest-time '15minute'
bash
tctl workflow listall --latest-time '2022-04-13T23:02:17-07:00'
bash
tctl workflow listall --latest-time '10second'
bash
tctl workflow listall --workflow_id <id>
bash
tctl workflow listall --workflow_type <name>
bash
tctl workflow listall --status <value>
bash
tctl workflow listall --query <value>
bash
tctl workflow listarchived --print_raw_time
bash
tctl workflow listarchived --print_datetime
bash
tctl workflow listarchived --print_memo
bash
tctl workflow listarchived --print_search_attr
bash
tctl workflow listarchived --print_full
bash
tctl workflow listarchived --print_json
bash
tctl workflow listarchived --query <value>
bash
tctl workflow listarchived --pagesize <value>
bash
tctl workflow listarchived --all
bash
tctl workflow observe --workflow_id <id>
bash
tctl workflow observe --run_id <id>
bash
tctl workflow observe --show_detail
bash
tctl workflow observe --max_field_length <length>
bash
tctl workflow observeid --show_detail
bash
tctl workflow observeid --max_field_length <length>
bash
$ tctl workflow query --workflow_id "HelloQuery" --query_type "getCount"
Query result as JSON:
3
bash
$ tctl workflow signal --workflow_id "HelloQuery" --name "updateGreeting" --input \"Bye\"
Signal workflow succeeded.
$ tctl workflow query --workflow_id "HelloQuery" --query_type "getCount"
Query result as JSON:
4
bash
tctl workflow query --workflow_id <id>
bash
tctl workflow query --run_id <id>
bash
tctl workflow query --query_type <value>
bash
tctl workflow query --input <json>
bash
tctl workflow query --input_file <filename>
bash
tctl workflow query --query_reject_condition <value>
bash
tctl workflow reset --workflow_id <id>
bash
tctl workflow reset --run_id <id>
bash
tctl workflow reset --event_id <id>
bash
tctl workflow reset --reason <string>
bash
tctl workflow reset --reset_type <value>
bash
tctl workflow reset --reset_reapply_type <value>
bash
tctl workflow reset --reset_bad_binary_checksum <value>
bash
tctl workflow reset-batch --input_file <filename>
bash
tctl workflow reset-batch --query <value>
bash
tctl workflow reset-batch --exclude_file <filename>
bash
tctl workflow reset-batch --input_separator <string>
bash
tctl workflow reset-batch --reason <string>
bash
tctl workflow reset-batch --input_parallism <value>
bash
tctl workflow reset-batch --skip_current_open
bash
tctl workflow reset-batch --skip_base_is_not_current
bash
tctl workflow reset-batch --only_non_deterministic
bash
tctl workflow reset-batch --dry_run
bash
tctl workflow reset-batch --reset_type <value>
bash
tctl workflow reset-batch --reset_bad_binary_checksum <value>
bash
tctl workflow run --taskqueue your-task-queue-name --workflow_type YourWorkflowDefinitionName
bash
tctl workflow run --taskqueue <name>
bash
tctl workflow run --workflow_id <id>
bash
tctl workflow run --workflow_type <name>
bash
tctl workflow run --execution_timeout <seconds>
bash
tctl workflow run --workflow_task_timeout <seconds>
bash
tctl workflow run --cron <string>
bash
tctl workflow run --workflowidreusepolicy AllowDuplicate
tctl workflow run --workflowidreusepolicy AllowDuplicateFailedOnly
tctl workflow run --workflowidreusepolicy RejectDuplicate
bash
tctl workflow run --input <json>
bash
tctl workflow run --input_file <filename>
bash
tctl workflow run --memo_key <key>
bash
tctl workflow run --memo <json>
bash
tctl workflow run --memo_file <filename>
bash
tctl workflow run --search_attr_key <key>
bash
tctl workflow run --search_attr_value <value>
bash
tctl workflow run --show_detail
bash
tctl workflow run --max_field_length <length>
bash
tctl workflow scan --print_raw_time
bash
tctl workflow scan --print_datetime
bash
tctl workflow scan --print_memo
bash
tctl workflow scan --print_search_attr
bash
tctl workflow scan --print_full
bash
tctl workflow scan --print_json
bash
tctl workflow scan --pagesize <value>
bash
tctl workflow scan --query <value>
bash
tctl workflow show --workflow_id <id>
bash
tctl workflow show --run_id <id>
bash
tctl workflow show --print_datetime
bash
tctl workflow show --print_raw_time
bash
tctl workflow show --output_filename <filename>
bash
tctl workflow show --print_full
bash
tctl workflow show --print_event_version
bash
tctl workflow show --event_id <id>
bash
tctl workflow show --max_field_length <length>
bash
tctl workflow show --reset_points_only
bashbash
tctl workflow showid <workflow_id>
bashtext
1  WorkflowExecutionStarted    {WorkflowType:{Name:HelloWorld}, ParentInitiatedEventId:0,
                                TaskQueue:{Name:HelloWorldTaskQueue, Kind:Normal},
                                Input:[Temporal], WorkflowExecutionTimeout:1h0m0s,
                                WorkflowRunTimeout:1h0m0s, WorkflowTaskTimeout:10s,
                                Initiator:Unspecified, LastCompletionResult:[],
                                OriginalExecutionRunId:f0c04163-833f-490b-99a9-ee48b6199213,
                                Identity:tctl@z0mb1e,
                                FirstExecutionRunId:f0c04163-833f-490b-99a9-ee48b6199213,
                                Attempt:1, WorkflowExecutionExpirationTime:2020-10-13
                                21:41:06.349 +0000 UTC, FirstWorkflowTaskBackoff:0s}
2  WorkflowTaskScheduled       {TaskQueue:{Name:HelloWorldTaskQueue,
                                Kind:Normal},
                                StartToCloseTimeout:10s, Attempt:1}
3  WorkflowTaskStarted         {ScheduledEventId:2, Identity:15079@z0mb1e,
                                RequestId:731f7b41-5ae4-42e4-9695-ecd857d571f1}
4  WorkflowTaskCompleted       {ScheduledEventId:2,
                                StartedEventId:3,
                                Identity:15079@z0mb1e}
5  WorkflowExecutionCompleted  {Result:[],
                                WorkflowTaskCompletedEventId:4}
bash
tctl workflow showid <workflow_id> --print_datetime
bash
tctl workflow showid <workflow_id> --print_raw_time
bash
tctl workflow showid <workflow_id> --output_filename <filename>
bash
tctl workflow showid <workflow_id> --print_full
bash
tctl workflow showid <workflow_id> --print_event_version
bash
tctl workflow showid <workflow_id> --event_id <id>
bash
tctl workflow showid <workflow_id> --max_field_length <length>
bash
tctl workflow showid <workflow_id> --reset_points_only
bash
tctl workflow start  --workflow_id "HelloSignal" --taskqueue HelloWorldTaskQueue --workflow_type HelloWorld --execution_timeout 3600 --input \"World\"
text
13:57:44.258 [workflow-method] INFO  c.t.s.javaquickstart.GettingStarted - 1: Hello World!
bash
tctl workflow signal --workflow_id "HelloSignal" --name "updateGreeting" --input \"Hi\"
text
13:57:44.258 [workflow-method] INFO  c.t.s.javaquickstart.GettingStarted - 1: Hello World!
13:58:22.352 [workflow-method] INFO  c.t.s.javaquickstart.GettingStarted - 2: Hi World!
bash
tctl workflow signal --workflow_id "HelloSignal" --name "updateGreeting" --input \"Welcome\"
text
13:57:44.258 [workflow-method] INFO  c.t.s.javaquickstart.GettingStarted - 1: Hello World!
13:58:22.352 [workflow-method] INFO  c.t.s.javaquickstart.GettingStarted - 2: Hi World!
13:59:29.097 [workflow-method] INFO  c.t.s.javaquickstart.GettingStarted - 3: Welcome World!
bash
tctl workflow signal --workflow_id "HelloSignal" --name "updateGreeting" --input \"Welcome\"
text
Signal workflow succeeded.
bash
tctl workflow signal --workflow_id "HelloSignal" --name "updateGreeting" --input \"Bye\"
bash
tctl workflow showid HelloSignal
bash
tctl workflow signal --workflow_id <id> <modifiers>
bash
tctl workflow signal --query <query> <modifiers>
bash
tctl workflow signal --workflow_id <id>
bash
tctl workflow signal --run_id <id>
bash
tctl workflow signal --query <query> --name <name>
bash
tctl workflow signal --query <query> --input <json>
bash
tctl workflow signal --query <query> --input_file <filename>
bash
tctl workflow stack --workflow_id <id>
bash
tctl workflow stack --run_id <id>
bash
tctl workflow stack --input <json>
bash
tctl workflow stack --input_file <filename>
bash
tctl workflow stack --query_reject_condition <value>
bash
tctl workflow start --taskqueue <name>
bash
tctl workflow start --workflow_id <id>
bash
tctl workflow start  --workflow_id "HelloTemporal1" --taskqueue HelloWorldTaskQueue --workflow_type HelloWorld --execution_timeout 3600 --input \"Temporal\"
bash
tctl workflow start --workflow_type <name>
bash
tctl workflow start --execution_timeout <seconds>
bash
tctl workflow start --workflow_task_timeout <seconds>
bash
tctl workflow start --cron <string>
bash
tctl workflow start --workflowidreusepolicy AllowDuplicate
tctl workflow start --workflowidreusepolicy AllowDuplicateFailedOnly
tctl workflow start --workflowidreusepolicy RejectDuplicate
bash
tctl workflow start --input <json>
bash
tctl workflow start --input_file <filename>
bash
tctl workflow start --memo_key <key>
bash
tctl workflow start \
  -tq your-task-queue \
  -wt your-workflow \
  -et 60 \
  -i '"temporal"' \
  -memo_key '<key values>' \
  -memo '<value>'
bash
tctl workflow start --memo_file <filename>
bash
tctl workflow start --search_attr_key <key>
bash
tctl workflow start --search_attr_value <value>
bash
tctl workflow terminate --workflow_id <id>
bash
tctl workflow terminate --run_id <id>
bash
tctl workflow terminate --workflow_id --reason <string>

temporal operator cluster health --address 127.0.0.1:7233

./grpc-health-probe -addr=frontendAddress:frontendPort -service=temporal.api.workflowservice.v1.WorkflowService

./grpc-health-probe -addr=matchingAddress:matchingPort -service=temporal.api.workflowservice.v1.MatchingService

./grpc-health-probe -addr=historyAddress:historyPort -service=temporal.api.workflowservice.v1.HistoryService

sum(rate(service_errors_resource_exhausted{}[1m])) by (resource_exhausted_cause)

temporal operator cluster health --address [SERVER_ADDRESS]
command
tcld namespace accepted-client-ca list \
    --namespace <namespace_id>.<account_id> | \
    jq -r '.[0].notAfter'
command
openssl s_client -connect <namespace_grpc_endpoint> -showcerts -cert ~/certs/path.pem -key .~/certs/path.key -tls1_2
command
temporal namespace describe \
    --namespace <namespace_id>.<account_id> \
    --address <namespace_grpc_endpoint> \
    --tls-cert-path <path-to-mTLS-pem-file> \
    --tls-key-path <path-to-mTLS-key-file>
```

Your Namespace gRPC endpoint is available on the details page for your [Temporal Cloud Namespace](https://cloud.temporal.io/namespaces).

### Renew TLS certification

If the certificate has expired or is about to expire, the next step is to renew it.

You can do this by contacting the certificate authority (CA) that issued the certificate and requesting a renewal.

**Existing certificate management infrastructure**

If you are using an existing certificate management infrastructure, contact the administrator of the infrastructure to renew the certificate.

**Self-signed certificate**

If you are using a self-signed certificate or don't have an existing infrastructure, you can generate a new certificate using OpenSSL, [step CLI](https://github.com/smallstep/cli), or similar tools.

For information on generating a self-signed certificate, see [Control authorization](/cloud/certificates#control-authorization).

### Update the CA certification in the server configuration

Update the new CA certificate in the Temporal Cloud server configuration.

You can update certificates using any of the following methods:

- [Update certificates using Temporal Cloud UI](/cloud/certificates#update-certificates-using-temporal-cloud-ui)
- [Update certificates using tcld](/cloud/certificates#update-certificates-using-tcld)

After you update the TLS certification in the server configuration, retry your connection.

Don't let your certificates expire.
Add reminders to your calendar to issue new CA certificates well before the expiration dates of the existing ones.

### Additional resources

The preceding steps should help you troubleshoot the `failed reaching server: last connection error` error caused by an expired TLS certificate.

If this issue persists, verify that the Client you are using to connect to the server is using the correct TLS certification and that the Client requests reach the server after the roles are fully initialized.
If you still need help, [create a support ticket](/cloud/support#support-ticket).

## Performance bottlenecks troubleshooting guide

This guide outlines common performance bottlenecks in Temporal Workers and Clients.
It covers key latency metrics and root causes of high values, and provides diagnostic steps and troubleshooting strategies.
These metrics can help you optimize Temporal deployments and Workflow execution.

To get the most out of this guide, you should be familiar with [Temporal architecture](/temporal), [Workflows](/workflows), [Activities](/activities), and [Task Queues](/task-queue).
You should also know how to use key metrics like latency, counter, rate, CPU utilization, and memory usage.

## Task processing metrics

These metrics provide insights into various stages of the [Task](/tasks) lifecycle, from scheduling to completion.
The following sections detail common metrics, their potential causes for high latency or resource depletion, and strategies for diagnosing and resolving performance issues.

### `temporal_workflow_task_schedule_to_start_latency` spike

High [`temporal_workflow_task_schedule_to_start_latency`](/references/sdk-metrics#workflow_task_schedule_to_start_latency) (P95 higher than one second) can be caused by several factors.
This metric represents the time between when a [Workflow Task](/tasks#workflow-task) is scheduled (enqueued) and when it is picked up by a Worker for processing. Here are some potential causes:

- Insufficient Worker capacity: If there aren't enough Workers or if the Workers are overloaded, they may not be able to pick up Tasks quickly enough. This can lead to Tasks waiting longer in the queue ([Detect Task Backlog](https://docs.temporal.io/production-deployment/cloud/worker-health#detect-task-backlog)).
- Worker configuration issues: Improperly configured Workers, such as having too few pollers or Task slots, can lead to increased latency ([Detect Task Backlog](https://docs.temporal.io/production-deployment/cloud/worker-health#detect-task-backlog)).
- High Workflow lock latency: If many updates are made to a single execution, this can cause Workflow lock latency, which in turn affects the Schedule-to-start latency. Reduce the rate of Signals.
- Network latency: Workers in a different region from the Temporal cluster, or large payload size, can introduce additional latency.

To diagnose and address high `temporal_workflow_task_schedule_to_start_latency`, you should:

1. Check Worker CPU and memory usage.
1. Review Worker configuration (number of pollers, Task slots, etc.).
1. Look for any spikes in Workflow or Activity starts that might be overwhelming the system.
1. Ensure Workers are in the same region as the Temporal cluster if possible.

### `temporal_activity_schedule_to_start_latency` spike

High [`temporal_activity_schedule_to_start_latency`](/references/sdk-metrics#activity_schedule_to_start_latency) (P95 higher than one second) can be caused by several factors.
This metric represents the time between when an [Activity Task](/tasks#activity-task) is scheduled (enqueued) and when it is picked up by a Worker for processing.
Here are some potential causes:

- Insufficient Worker capacity: If there aren't enough Workers or if the Workers are overloaded, they may not be able to pick up Tasks quickly enough. This can lead to Tasks waiting longer in the queue ([Detect Task Backlog](https://docs.temporal.io/production-deployment/cloud/worker-health#detect-task-backlog)).
- Worker configuration issues: Improperly configured Workers, such as having too few pollers or Task slots, can lead to increased latency ([Detect Task Backlog](https://docs.temporal.io/production-deployment/cloud/worker-health#detect-task-backlog)).
- Task Queue configuration: Setting `TaskQueueActivitiesPerSecond` too low can limit the rate at which Activities are started, leading to increased Schedule-to-start latency.
- Network latency: Workers in a different region from the Temporal cluster, or large payload size can introduce additional latency.

To diagnose and address high `temporal_activity_schedule_to_start_latency`:

1. Check Worker CPU and memory usage.
1. Review Worker configuration (number of pollers, Task slots, etc.).
1. Look for any spikes in Workflow or Activity starts that might be overwhelming the system.
1. Ensure Workers are in the same region as the Temporal cluster if possible.

### `temporal_workflow_endtoend_latency` spike

The [`temporal_workflow_endtoend_latency`](/references/sdk-metrics#workflow_endtoend_latency) metric represents the total Workflow Execution time from Schedule to the closure for a single Workflow Run.
Normal ranges for this metric depend on the use case, but here are some potential causes for the unexpected spikes:

- Complex Workflows: If the Workflows have many Activities or if the Activities take a long time to execute.
- Workflow and Activity retries: If Workflows or Activities are configured to retry upon failure and they fail often, this can increase the end-to-end latency as the system will wait for the retry delay before reattempting the failed operation.
- Worker capacity and configuration: If there aren't enough Workers or if the Workers are overloaded, they may not be able to pick up and process Tasks quickly enough. This can lead to Tasks waiting longer in the queue, thereby increasing the end-to-end latency ([Detect Task Backlog](https://docs.temporal.io/production-deployment/cloud/worker-health#detect-task-backlog)).
- External dependencies: If your Workflows or Activities depend on external systems or services (such as databases or APIs) and these systems are slow or unreliable, they can increase the end-to-end latency.
- Network latency: Workers in a different region from the Temporal cluster can introduce additional latency.

To diagnose and address high `temporal_workflow_endtoend_latency`:

1. Review your Workflow and Activity designs to ensure they are as efficient as possible.
2. Monitor your Workers to ensure they have sufficient capacity (CPU and memory) and are not overloaded.
3. Monitor your external dependencies to ensure they are performing well.
4. Ensure Workers are in the same region as the Temporal cluster if possible.

### High `temporal_workflow_task_execution_latency`

The [`temporal_workflow_task_execution_latency`](/references/sdk-metrics#workflow_task_execution_latency) metric represents the time taken by a Worker to execute a Workflow Task.
The Temporal SDK raises a “Deadlock detected during Workflow run” error or [TMPRL1101](https://github.com/temporalio/rules/blob/main/rules/TMPRL1101.md) when a Workflow Task takes more than one or two seconds to complete.
Here are some potential causes:

- CPU-intensive work: Performing CPU-intensive operations in your Workflow Task can lead to slow execution.
- Slow local Activities: Workflow Task execution time includes the Local Activity execution time.
- Slow Workflow replay: Workflow Task execution time includes the Workflow Replay time. Refer to `workflow_task_replay_latency` for more details.
- Worker resource constraints: High CPU usage on Worker pods can lead to slower Workflow Task execution. Workers with insufficient CPU resources can cause delays.
- Infinite loops or blocking calls: Workflow code with infinite loops or blocking external API calls can cause the Workflow Task to execute slowly or time out.
- Slow data conversion: Your custom Data Converter is taking too long to encode/decode payloads, for example, when talking to a remote encryption service.

To diagnose and address slow Workflow Task execution, you can:

1. Monitor Worker CPU and memory utilization.
2. Ensure that your Workers have adequate resources and are properly scaled for your workload.
3. Consider running your Workflow code in a profiler using a replayer to see where CPU cycles are spent.
4. Review your Workflow code for potential optimizations or to remove blocking operations.
5. Disable deadlock detection for Data Converter: It does not reduce Task execution latency but does remove the “Deadlock detected during Workflow run” or TMPRL1101 error. In Go, wrap it with `workflow.DataConverterWithoutDeadlockDetection`. In Java, surround your Data Converter code with `WorkflowUnsafe.deadlockDetectorOff`.

### High `workflow_task_replay_latency`

Workflow Task replay is the process of reconstructing the Workflow's state by re-executing the Workflow code from the beginning, using the recorded Event History.
This process ensures that the Workflow can continue from where it left off, even after interruptions or failures.
[`workflow_task_replay_latency`](/references/sdk-metrics#workflow_task_replay_latency) is high if it exceeds a few milliseconds.
Here are the main causes:

- Large Event Histories: Workflows with long histories take more time to replay, as the Worker needs to process all events to reconstruct the Workflow state.
- Data Converter performance: Slow Data Converters, especially those that perform encryption or interact with external services, can impact replay.
- Large payloads: Activities or Signals with large payloads can slow down the replay process, especially if the Data Converter needs to process these payloads.
- Complex Workflow logic: Workflow code with complex logic or computationally intensive operations, such as scheduling many concurrent child Workflows or Activities, can increase replay latency.
- Frequent cache evictions: If workers often evict Workflow Executions from their cache (due to memory constraints or frequent restarts), it leads to more replays and higher latency.
- Worker resource constraints: High CPU utilization or memory pressure on Worker nodes can slow down the replay.

To diagnose and address slow Workflow Task replay, you can:

1. Monitor SDK Metrics: Keep a close eye on the `temporal_workflow_task_replay_latency` metric. This histogram metric measures the time it takes to replay a Workflow Task.
1. Analyze Workflow History Size: Check the number of events in your Workflow histories and consider using the "Continue-As-New" feature for long-running Workflows.
1. Optimize Data Converters: If you're using custom Data Converters, especially for encryption or complex serialization, look for opportunities to optimize their performance.
1. Review Payload Sizes: Large Activity or Signal payloads can slow down replay. Consider optimizing the size of data being passed in your Workflows.
1. Profile Workflow Code: Use a profiler to identify CPU-intensive parts of your Workflow code that might be slowing down replay.
1. Manage Worker Cache: Frequent cache evictions can lead to more replays. Tune your Worker's cache size and eviction policies.

### `temporal_activity_execution_latency` spike

The [`temporal_activity_execution_latency`](/references/sdk-metrics#activity_execution_latency) metric measures the time from when a Worker starts processing an Activity Task until it reports to the service that the Task is complete or failed.
There are several potential causes for high `temporal_activity_execution_latency`:

- Activity implementation: The most common cause of high Activity Execution latency is the actual implementation of the Activity itself. If the Activity is performing time-consuming operations or making slow external API calls, it will take longer to execute.
- External dependencies: If your Activity is constrained by an external resource or service that all Activities access, it could cause increased latency.
- Worker resource constraints: Under-resourced Worker nodes or experiencing high CPU utilization can lead to slower Activity Execution.
- Network latency: High latency between your Workers and external services or the Temporal service itself can contribute to increased Activity Execution time.

To diagnose and address high Activity Execution latency:

1. Monitor the `activity_execution_latency` metric, which you can filter by Activity type and Activity Task queue.
2. Optimize your Activity implementation to reduce latency, especially with external services or database interactions.
3. Check your Worker CPU and memory utilization to make sure they have adequate resources.
4. Examine your Worker configuration, particularly `(Max)ConcurrentActivityExecutionSize` and `(Max)WorkerActivitiesPerSecond`, to ensure they are not limiting your activity execution.

### Depletion of `temporal_worker_task_slots_available` for `WorkflowWorker`

The [`temporal_worker_task_slots_available{worker_type=”WorkflowWorker”}`](/references/sdk-metrics#worker_task_slots_available) metric indicates the number of available slots for executing Workflow Tasks on a Worker.
This metric may go to zero for several reasons:

- High Workflow Task Load: If there are more Tasks than the Worker can handle concurrently, the available slots will be depleted. This can happen if the rate of incoming Tasks is higher than the rate at which tasks are being completed.
- Worker Configuration: The number of available slots is determined by the Worker configuration, specifically the `MaxConcurrentWorkflowTaskExecutionSize` setting. If these are set too low, the Worker may not have enough slots to handle the Task load.
- High `temporal_workflow_task_execution_latency` and `workflow_task_replay_latency`.

To prevent depletion of Workflow Task slots:

1. Monitor Worker CPU and Memory usage while increasing `(Max)ConcurrentWorkflowTaskExecutionSize` to add more execution slots.
2. Scale up Workers both vertically (increasing CPU and Memory) and horizontally (increasing Worker instances).

### Depletion of `temporal_worker_task_slots_available` for `ActivityWorker`

The [`temporal_worker_task_slots_available{worker_type=”ActivityWorker”}`](/references/sdk-metrics#worker_task_slots_available) metric indicates the number of available slots for executing Activity Tasks on a Worker.
This metric may go to zero for several reasons:

- Blocked Activities and Zombie Activities: The most common cause is activities that are blocked or not returning on time. Zombie Activities are a subset of this category. They occur when an Activity times out (hits its `StartToClose` or `HeartbeatTimeout` timeout) and has stopped Heartbeating but continues to run, occupying some or all the slots as more retries occur. This can happen if:
  - The Activity code is blocking on a downstream service call or an infinite loop.
  - There's a mismatch between the Activity's `StartToClose` timeout and any client-side timeouts for external calls.
- Resource Utilization: High CPU or memory usage on Workers can cause activities to block and not release slots.

To prevent depletion of Activity Task slots:

1. Monitor Worker CPU and Memory usage while increasing `(Max)ConcurrentActivityExecutionSize` to add more execution slots.
2. Add client-side timeout to your downstream API client.
3. Review your Task code to ensure Tasks complete within a reasonable time measured by `temporal_activity_execution_latency`.

Network issues can impact Temporal clients and workers, leading to delays, failures, and overall system instability.
This section focuses on metrics that reveal common network-related problems with your Temporal deployment, specifically related to network connectivity, latency, and request failures.
These metrics can indicate where bottlenecks exist within the communication channels between Temporal clients (including Temporal Workers) and the Temporal server.

### High `temporal_long_request_failure`

The [`temporal_long_request_failure`](/references/sdk-metrics#long_request_failure) metric counts the number of failed RPC long poll requests for `PollWorkflowTaskQueue`, `PollActivityTaskQueue`, and `GetWorkflowExecutionHistory` (when polling new events). High values of this metric can be caused by several factors:

- Network Issues: Problems with the network connection between the Temporal Client and the Temporal Server, including firewalls and proxies, can cause long poll requests to fail.
- Rate Limiting: If the rate of requests exceeds the configured limits on the Temporal Server or Temporal Cloud, additional requests may be rejected, increasing the `temporal_long_request_failure` count. This is often indicated by a `ResourceExhausted` status code.
- Server Errors: If the Temporal Server is experiencing issues, it may fail to respond to long poll requests correctly, leading to an increase in `temporal_long_request_failure`.

To diagnose the cause of high `temporal_long_request_failure`, you can:

1. Check the operation and the status or code tag of the `temporal_long_request_failure` metric to see the type of errors that are occurring.
2. If you receive a `ResourceExhausted` status code, review the rate limits configured on the Temporal Server or ask for help from Temporal Support for Temporal Cloud.
3. Check the network connection between the Temporal Client and the Temporal Server.

### High `temporal_request_failure_total`

The [`temporal_request_failure_total`](/references/sdk-metrics#request_failure) metric counts the number of RPC requests made by the Temporal Client that have failed.
High values of this metric can be caused by several factors:

- Network Issues: Problems with the network connection between the Temporal Client and the Temporal Server can cause requests to fail.
- Client Errors: If there's an issue with the Temporal Client, such as misconfiguration or resource exhaustion, it may fail to make requests correctly.
- Operation Errors: Specific operations like `SignalWorkflowExecution` or `TerminateWorkflowExecution` can fail if they are trying to act on a closed Workflow Execution that no longer exists (because it completed and was removed from persistence when it hit Namespace retention time).
- Rate Limiting: If the rate of requests exceeds the configured limits on the Temporal Server, additional requests may be rejected, increasing the counter. This is often indicated by a `ResourceExhausted` status code.
- Request Size Limit: If the Worker tries to return an Activity response that is larger than the blob size limit (2MB), the service will reject it, causing a request failure.
- Server Errors: If the Temporal Server is experiencing issues, it may fail to respond to requests correctly, leading to an increase in `temporal_request_failure_total`.

To diagnose the cause of high `temporal_request_failure_total`, you can:

1. Check the status or code tag of the `temporal_request_failure_total` metric to see the type of errors that are occurring.
2. Look at the operation tag of the `temporal_request_failure_total` metric to see which operations are failing.
3. Monitor the Temporal Server logs and the Temporal Client logs for any error messages or warnings.
4. Check the network connection between the Temporal Client and the Temporal Server.

### High `temporal_request_latency`

The [`temporal_request_latency`](/references/sdk-metrics#request_latency) metric measures the latency of gRPC requests made by the Temporal Client.
High values for this metric can be caused by several factors:

- Network Latency: The physical distance and network conditions between the Temporal Client and the Temporal Server can affect the latency of requests.
- Network Transfer Time: Larger payloads take longer to transfer over the network, which affects request latency. For example, large payloads in `RespondWorkflowTaskCompleted` can affect the latency of the request. This is especially true when Workflows are scheduling multiple activities with large inputs.
- Resource Exhaustion: Running out of resources (such as CPU or memory) on the client or server can cause delays in processing the request.
- Client Configuration: Improper client configuration, such as setting thread pool sizes too aggressively or having memory constraints that are too low for the number of allocated threads, can lead to situations where Tasks overwhelm the client, causing increased latency.
- Server Load: If the Temporal Server is under heavy load, it may take longer to respond to requests, leading to increased latency.

To diagnose and address high `temporal_request_latency`:

1. Monitor the `temporal_request_latency` metric to identify when and where latency spikes are occurring.
2. Check the network connection between the Temporal Client and the Temporal Server.
3. Monitor the resource usage on both the Temporal Client and the Temporal Server.
4. Review your Temporal Client configuration to ensure it is optimized for your workload.
5. If you're using Temporal Cloud, check if the Cloud’s [service-latency](https://docs.temporal.io/production-deployment/cloud/metrics/reference#service-latency) metric spikes up and reach out to Temporal Support for help.

### `rate(temporal_long_request_total{operation="PollActivityTaskQueue"})`

The [`rate(temporal_long_request_total{operation="PollActivityTaskQueue"})`](/references/sdk-metrics#long_request) expression measures the per-second average rate of `PollActivityTaskQueue` long poll requests over a certain period of time.

`PollActivityTaskQueue` is an operation where Workers poll for Activity Tasks from the Task Queue.
The `temporal_long_request_total` metric counts the number of these long poll requests.

By applying the `rate()` function in Prometheus, you can calculate the per-second average rate of these requests over the time range specified in the Query.
This can help you understand the load on your Temporal service and how often your Workers are polling for Activity Tasks.

### `rate(temporal_long_request_total{operation="PollWorkflowTaskQueue"})`

The [`rate(temporal_long_request_total{operation="PollWorkflowTaskQueue"})`](/references/sdk-metrics#long_request) expression measures the per-second average rate of `PollWorkflowTaskQueue` long poll requests over a certain period of time.

`PollWorkflowTaskQueue` is an operation where Workers poll for Workflow Tasks from the Task Queue.
The `temporal_long_request_total` metric counts the number of these long poll requests.

By applying the `rate()` function in Prometheus, you can calculate the per-second average rate of these requests over the time range specified in the query.
This can help you understand the load on your Temporal service and how often your Workers are polling for Workflow Tasks.

Temporal Workers relies on caching to optimize performance by reducing the overhead of fetching Workflow state from the history and Replaying.
However, unlimited caching is impossible; there's a trade-off between the benefits of cached data and the memory consumed.
These metrics allow you to balance performance gains with responsible memory usage.

### `temporal_sticky_cache_size`

The [`temporal_sticky_cache_size`](/references/sdk-metrics#sticky_cache_size) metric represents the number of Workflow executions currently cached in a Worker's memory.

The sticky cache is used to improve performance by keeping the Workflow state in memory, reducing the need to reconstruct the Workflow from its Event History for every Task.
It’s particularly useful for latency-sensitive Workflows.

There is a direct relationship between the sticky cache size and Worker memory consumption.
As the cache size increases, so does the memory usage of the Worker.

The maximum size of the sticky cache can be configured. For example, the default in the Go SDK is 10,000 Workflows.

A larger sticky cache can improve performance by reducing the need to replay Workflow histories.
However, it also increases memory usage, which can lead to issues if not properly managed.

Monitor this metric alongside Worker memory usage.
A sudden increase in `sticky_cache_size` can correlate with increased memory consumption and potential performance issues.

If memory consumption is too high, you can reduce the maximum sticky cache size.
Conversely, if you have available memory and want to improve performance, you might increase it.

### `temporal_sticky_cache_hit_total` and `temporal_sticky_cache_miss_total`

The [`temporal_sticky_cache_hit_total`](https://docs.temporal.io/references/sdk-metrics#sticky_cache_hit) metric is a counter that measures the total number of times a Workflow Task found a cached Workflow Execution to run against, and
the opposite is [`temporal_sticky_cache_miss_total`](https://docs.temporal.io/references/sdk-metrics#sticky_cache_miss), which is a counter that measures the total number of times a Workflow Task did not find a cached Workflow Execution to run against.

Sticky Execution is a feature where a Worker caches a Workflow Execution and creates a dedicated Task Queue to listen on.
This improves performance because the Temporal Service only sends new events to the Worker instead of entire Event Histories, and the Workflow doesn't have to Replay.

A “hit” means the Worker finds the Workflow in its cache when processing a Workflow Task, allowing immediate processing without fetching the full Event History from the server and Replaying.
A "miss" means the Worker didn't find the Workflow in its cache, and it must fetch the Event History and Replay.

Monitoring these two metrics and comparing them can help you understand how your sticky cache is being used.
A high rate of cache hits with a low rate of cache misses indicates that your Workflows are being scheduled efficiently, with minimal need for fetching Event Histories and Replaying.

### `temporal_sticky_cache_total_forced_eviction_total`

The [`temporal_sticky_cache_total_forced_eviction_total`](https://docs.temporal.io/references/sdk-metrics#sticky_cache_hit) metric is a counter that measures the total number of Workflow Executions that have been forcibly evicted from the sticky cache.

Sticky Execution is a feature where a Worker caches a Workflow Execution and creates a dedicated Task Queue to listen on.
This improves performance because the Temporal Service only sends new events to the Worker instead of entire Event Histories, and the Workflow doesn't have to Replay.

A "forced eviction" in this context means that a Workflow Execution was removed from the cache before it completed, typically because the cache was full and needed to make room for other Workflow Executions.
This means that if the Worker needs to process more Tasks for the evicted Workflow Execution, it will have to fetch the entire Event History from the Temporal Service and Replay.

Monitoring the `temporal_sticky_cache_total_forced_eviction_total` metric can help you understand how often your Workflows are being evicted from the cache.
A high rate of forced evictions could indicate that your cache size is too small for your workload, and you may need to increase the `WorkflowCacheSize` setting if your Worker resources can accommodate it.

**Examples:**

Example 1 (unknown):
```unknown
The following modifiers control the behavior of the command.

### --active_cluster

Specify the name of the active [Temporal Cluster](/temporal-service) when registering a [Namespace](/namespaces).
This value changes for Global Namespaces when a failover occurs.

**Example**
```

Example 2 (unknown):
```unknown
### --clusters

Specify a list of [Temporal Clusters](/temporal-service) when registering a [Namespace](/namespaces).

The list contains the names of Clusters (separated by spaces) to which the Namespace can fail over.
Make sure to include to the currently active Cluster.
This is a read-only setting and cannot be changed.

This modifier is valid only when the `--global_namespace` modifier is set to true.

**Example**
```

Example 3 (unknown):
```unknown
### --description

Specify a description when registering a [Namespace](/namespaces).

**Example**
```

Example 4 (unknown):
```unknown
### --global_namespace

Specifies whether a [Namespace](/namespaces) is a [Global Namespace](/global-namespace).
When enabled, it controls the creation of replication tasks on updates allowing the state to be replicated across Clusters.
This is a read-only setting and cannot be changed.

**Example**
```

---

## Start 5 activities

**URL:** llms-txt#start-5-activities

act_futs = 5.times.map do |i|
  Temporalio::Workflow::Future.new do
    Temporalio::Workflow.execute_activity(MyActivity, "my-arg-#{i}", schedule_to_close_timeout: 300)
  end
end

---

## cluster A

**URL:** llms-txt#cluster-a

clusterMetadata:
  enableGlobalNamespace: true
  failoverVersionIncrement: 100
  masterClusterName: "clusterA"
  currentClusterName: "clusterA"
  clusterInformation:
    clusterA:
      enabled: true
      initialFailoverVersion: 1
      rpcAddress: "127.0.0.1:7233"

---

## Add a cluster

**URL:** llms-txt#add-a-cluster

temporal operator cluster upsert --frontend_address="127.0.2.1:8233"

---

## TYPE temporal_cloud_v1_approximate_backlog_count gauge

**URL:** llms-txt#type-temporal_cloud_v1_approximate_backlog_count-gauge

---

## set your Cassandra environment variables

**URL:** llms-txt#set-your-cassandra-environment-variables

: "${KEYSPACE:=temporal}"
: "${VISIBILITY_KEYSPACE:=temporal_primary_visibility}"

: "${CASSANDRA_SEEDS:=}"
: "${CASSANDRA_PORT:=9042}"
: "${CASSANDRA_USER:=}"
: "${CASSANDRA_PASSWORD:=}"
: "${CASSANDRA_TLS_ENABLED:=}"
: "${CASSANDRA_CERT:=}"
: "${CASSANDRA_CERT_KEY:=}"
: "${CASSANDRA_CA:=}"
: "${CASSANDRA_REPLICATION_FACTOR:=1}"
#...

---

## Create a replayer

**URL:** llms-txt#create-a-replayer

replayer = Temporalio::Worker::WorkflowReplayer.new(workflows: [MyWorkflow])

---

## ... same as with regular image

**URL:** llms-txt#...-same-as-with-regular-image

**Contents:**
  - Using `distroless/nodejs` images

**Examples:**

Example 1 (unknown):
```unknown
Failure to install this dependency results in a `[TransportError: transport error]` runtime error, because the certificates cannot be verified.

### Using `distroless/nodejs` images

`distroless/nodejs` images include only the files that are strictly required to execute `node`.
This results in even smaller images (approximately half the size of `node:slim` images).
It also significantly reduces the surface of potential security issues that could be exploited by a hacker in the resulting Docker images.

It is generally possible and safe to execute TypeScript SDK Workers using `distroless/nodejs` images (unless your code itself requires dependencies that are not included in `distroless/nodejs`).

However, some tools required for the build process (notably the `npm` command) are _not_ included in the `distroless/nodejs` image.
This might result in various error messages during the Docker build.

The recommended solution is to use a multi-step Dockerfile.
For example:
```

---

## Same Activity, different policies

**URL:** llms-txt#same-activity,-different-policies

await workflow.execute_activity(
    process_order,
    order,
    start_to_close_timeout=timedelta(seconds=10),
    retry_policy=fast_retry,
)

---

## Custom headers for production

**URL:** llms-txt#custom-headers-for-production

**Contents:**
- Connect to Temporal Cloud {#connect-to-temporal-cloud}

[profile.prod.grpc_meta]
environment     = "production"
service-version = "v1.2.3"
ts {17-19,28-29}

async function main() {
  console.log('--- Loading default profile from config.toml ---');

// For this sample to be self-contained, we explicitly provide the path to
  // the config.toml file included in this directory.
  // By default though, the config.toml file will be loaded from
  // ~/.config/temporalio/temporal.toml (or the equivalent standard config directory on your OS).
  const configFile = resolve(__dirname, '../config.toml');

// loadClientConnectConfig is a helper that loads a profile and prepares
  // the configuration for Connection.connect and Client. By default, it loads the
  // "default" profile.
  const config = loadClientConnectConfig({
    configSource: { path: configFile },
  });

console.log(`Loaded 'default' profile from ${configFile}.`);
  console.log(`  Address: ${config.connectionOptions.address}`);
  console.log(`  Namespace: ${config.namespace}`);
  console.log(`  gRPC Metadata: ${JSON.stringify(config.connectionOptions.metadata)}`);

console.log('\nAttempting to connect to client...');
  try {
    const connection = await Connection.connect(config.connectionOptions);
    const client = new Client({ connection, namespace: config.namespace });
    console.log('✅ Client connected successfully!');
    await connection.close();
  } catch (err) {
    console.log(`❌ Failed to connect: ${err}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
bash
export TEMPORAL_NAMESPACE="default"
export TEMPORAL_ADDRESS="localhost:7233"
ts {7,17-18}

async function main() {
// ...
  const config = loadClientConnectConfig({
// ...
  });
// ...
  console.log(`  Address: ${config.connectionOptions.address}`);
  console.log(`  Namespace: ${config.namespace}`);
  console.log(`  gRPC Metadata: ${JSON.stringify(config.connectionOptions.metadata)}`);

console.log('\nAttempting to connect to client...');
  try {
    const connection = await Connection.connect(config.connectionOptions);
    const client = new Client({ connection, namespace: config.namespace });
    console.log('✅ Client connected successfully!');
    await connection.close();
  } catch (err) {
    console.log(`❌ Failed to connect: ${err}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
ts
const connection = await Connection.connect({
    address: <endpoint>,
    tls: true,
    apiKey: <APIKey>,
});
const client = new Client({
    connection,
    namespace: <namespace_id>.<account_id>,
});
toml

**Examples:**

Example 1 (unknown):
```unknown
You can create a Temporal Client using a profile from the configuration file as follows. In this example, you load the
`default` profile for local development:

{/* SNIPSTART typescript-env-config-load-default-profile {"highlightedLines": "17-19,28-29"} */}
[env-config/src/load-from-file.ts](https://github.com/temporalio/samples-typescript/blob/main/env-config/src/load-from-file.ts)
```

Example 2 (unknown):
```unknown
{/* SNIPEND */}

</TabItem>

<TabItem value="env-vars" label="Environment Variables">

Use the `@temporalio/envconfig` module to set connection options for the Temporal Client using environment variables.
For a list of all available environment variables and their default values, refer to
[Environment Configuration](/references/client-environment-configuration).

For example, the following code snippet loads all environment variables and creates a Temporal Client with the options
specified in those variables. If you have defined a configuration file at either the default location
(`~/.config/temporalio/temporal.toml`) or a custom location specified by the `TEMPORAL_CONFIG_FILE` environment
variable, this will also load the default profile in the configuration file. However, any options set via environment
variables will take precedence.

Set the following environment variables before running your application. Replace the placeholder values with your actual
configuration. Since this is for a local development Temporal Service, the values connect to `localhost:7233` and the
`default` Namespace. You may omit these variables entirely since they're the defaults.
```

Example 3 (unknown):
```unknown
After setting the environment variables, use the following code to create the Temporal Client. Since the environment
variables take precedence, they will override any values set in the configuration file. Therefore, you may leave
`loadClientConnectConfig`'s arguments empty:

{/* SNIPSTART typescript-env-config-load-default-profile {"highlightedLines": "7,17-18", "selectedLines": ["1-5","17","19","22-40"]} */}
[env-config/src/load-from-file.ts](https://github.com/temporalio/samples-typescript/blob/main/env-config/src/load-from-file.ts)
```

Example 4 (unknown):
```unknown
{/* SNIPEND */}

</TabItem>

<TabItem value="code" label="Code">

If you don't want to use environment variables or a configuration file, you can specify connection options directly in
code. This is convenient for local development and testing. You can also load a base configuration from environment
variables or a configuration file, and then override specific options in code.
```

---

## Set working directory

**URL:** llms-txt#set-working-directory

---

## tests/.rr.test.yaml

**URL:** llms-txt#tests/.rr.test.yaml

**Contents:**
  - How to skip time {#skip-time}
- How to Replay a Workflow Execution {#replay}
- Durable Timers - PHP SDK
- What is a Timer? {#timers}
- Versioning - PHP SDK feature guide
- Worker Versioning
- Versioning with Patching {#php-sdk-patching-api}
  - Patching with GetVersion
  - Workflow cutovers
- Runtime checking {#runtime-checking}

kv:
  test:
    driver: memory
    config:
      interval: 10
php
// worker.test.php
use Temporal\Testing\WorkerFactory;

$factory = WorkerFactory::create();
$worker = $factory->newWorker();

$worker->registerWorkflowTypes(MyWorkflow::class);
$worker->registerActivity(MyActivity::class);
$factory->run();
php
#[ActivityInterface(prefix: "SimpleActivity.")]
interface SimpleActivityInterface
{
    #[ActivityMethod('doSomething')]
    public function doSomething(string $input): string;
php
final class SimpleWorkflowTestCase extends TestCase
{
    private WorkflowClient $workflowClient;
    private ActivityMocker $activityMocks;

protected function setUp(): void
    {
        $this->workflowClient = new WorkflowClient(ServiceClient::create('localhost:7233'));
        $this->activityMocks = new ActivityMocker();

parent::setUp();
    }

protected function tearDown(): void
    {
        $this->activityMocks->clear();
        parent::tearDown();
    }

public function testWorkflowReturnsUpperCasedInput(): void
    {
        $this->activityMocks->expectCompletion('SimpleActivity.doSomething', 'world');
        $workflow = $this->workflowClient->newWorkflowStub(SimpleWorkflow::class);
        $run = $this->workflowClient->start($workflow, 'hello');
        $this->assertSame('world', $run->getResult('string'));
    }
}
php
$this->activityMocks->expectFailure('SimpleActivity.echo', new \LogicException('something went wrong'));
php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

use Temporal\Testing\Environment;

$environment = Environment::create();
$environment->start();
register_shutdown_function(fn () => $environment->stop());
php
if (getenv('RUN_TEMPORAL_TEST_SERVER') !== false) {
    $environment = Environment::create();
    $environment->start('./rr serve -c .rr.silent.yaml --workflow-id tests');
    register_shutdown_function(fn() => $environment->stop());
}
xml
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.3/phpunit.xsd"
         bootstrap="tests/bootstrap.php"
>
    <php>
        <env name="TEMPORAL_ADDRESS" value="127.0.0.1:7233" />
    </php>
</phpunit>
gitignore
temporal-test-server
php
/**
 * We assume you already have a WorkflowClient and WorkflowReplayer in scope.
 * @var \Temporal\Client\WorkflowClientInterface $workflowClient
 * @var \Temporal\Testing\Replay\WorkflowReplayer $replayer
 */

// Find all workflow executions of type "MyWorkflow" and task queue "MyTaskQueue".
$executions = $workflowClient->listWorkflowExecutions(
    "WorkflowType='MyWorkflow' AND TaskQueue='MyTaskQueue'"
);

// Replay each workflow execution.
foreach ($executions as $executionInfo) {
    try {
        $replayer->replayFromServer(
            workflowType: $executionInfo->type->name,
            execution: $executionInfo->execution,
        );
    } catch (\Temporal\Testing\Replay\Exception\ReplayerException $e) {
        // Handle a replay error.
    }
}
php
$replayer->replayFromJSON(
    workflowType: 'MyWorkflow',
    path: 'history.json',
    lastEventId: 42,  // optional
);
php
$history = $this->workflowClient->getWorkflowHistory(
    execution: $run->getExecution(),
)->getHistory();

(new WorkflowReplayer())->replayHistory($history);
php
yield Workflow::timer(300); // sleep for 5 minutes
php
#[WorkflowInterface]
class MyWorkflow
{
    private $activity;

public function __construct()
    {
        $this->activity = Workflow::newActivityStub(
            YourActivityInterface::class,
            ActivityOptions::new()->withScheduleToStartTimeout(60)
        );
    }

#[WorkflowMethod]
    public function runAsync()
    {
        $result = yield $this->activity->prePatchActivity();
    }
}
php
#[WorkflowInterface]
class MyWorkflow
{
    // ...

#[WorkflowMethod]
    public function runAsync()
    {
        $version = yield Workflow::getVersion('Step 1', Workflow::DEFAULT_VERSION, 1);

$result = $version === Workflow::DEFAULT_VERSION
            ? yield $this->activity->prePatchActivity()
            : yield $this->activity->postPatchActivity();
    }
}
php
#[WorkflowInterface]
class MyWorkflow
{
    // ...

#[WorkflowMethod]
    public function runAsync()
    {
        $version = yield Workflow::getVersion('Step 1', Workflow::DEFAULT_VERSION, maxSupported: 2);

$result = match($version) {
            Workflow::DEFAULT_VERSION => yield $this->activity->prePatchActivity()
            1 => yield $this->activity->postPatchActivity();
            2 => yield $this->activity->anotherPatchActivity();
        };
    }
}
php
    #[WorkflowMethod]
    public function runAsync()
    {
        $version = yield Workflow::getVersion('Step 1', minSupported: 1, maxSupported: 2);

$result = match($version) {
            1 => yield $this->activity->postPatchActivity();
            2 => yield $this->activity->anotherPatchActivity();
        };
    }
php
    #[WorkflowMethod]
    public function runAsync()
    {
        $version = yield Workflow::getVersion('Step 1', minSupported: 2, maxSupported: 2);

$result = yield $this->activity->anotherPatchActivity();
    }
php
#[WorkflowInterface]
class MyWorkflow
{}

#[WorkflowInterface]
class MyWorkflowV2
{}
```

You would then need to update the Worker configuration, and any other identifier strings, to register both Workflow Types.
The downside of this method is that it requires you to duplicate code and to update any commands used to start the Workflow.
This can become impractical over time.
This method also does not provide a way to version any still-running Workflows -- it is essentially just a cutover, unlike Patching.

## Runtime checking {#runtime-checking}

The Temporal PHP SDK performs a runtime check to help prevent obvious incompatible changes.
Adding, removing, or reordering any of these methods without Versioning triggers the runtime check and results in a nondeterminism error:

- `workflow.ExecuteActivity()`
- `workflow.ExecuteChildWorkflow()`
- `workflow.NewTimer()`
- `workflow.RequestCancelWorkflow()`
- `workflow.SideEffect()`
- `workflow.SignalExternalWorkflow()`
- `workflow.Sleep()`

The runtime check does not perform a thorough check.
For example, it does not check on the Activity's input arguments or the Timer duration.
Each Temporal SDK implements these sanity checks differently, and they are not a complete check for non-deterministic changes.
Instead, you should incorporate [Replay Testing](/develop/php/testing-suite#replay) when making revisions.

**Examples:**

Example 1 (unknown):
```unknown
If you want to be able to mock Activities, use `WorkerFactory` from the `Temporal\Testing` Namespace
in your PHP Worker:
```

Example 2 (unknown):
```unknown
Then, in your tests to mock an Activity, use the`ActivityMocker` class.

Assume we have the following Activity:
```

Example 3 (unknown):
```unknown
To mock it in the test, you can do this:
```

Example 4 (unknown):
```unknown
In the preceding test case, we do the following:

1. Instantiate `ActivityMocker` in the `setUp()` method of the test.
2. Clear the cache after each test in `tearDown()`.
3. Mock an Activity call to return a string `world`.

To mock a failure, use the `expectFailure()` method:
```

---

## Only specific metrics

**URL:** llms-txt#only-specific-metrics

/v1/metrics?metrics=temporal_cloud_v1_workflow_success_count

---

## TYPE temporal_cloud_v1_workflow_success_count gauge

**URL:** llms-txt#type-temporal_cloud_v1_workflow_success_count-gauge

---

## Don't avoid, but rather encourage things using TaskScheduler.Current in workflows

**URL:** llms-txt#don't-avoid,-but-rather-encourage-things-using-taskscheduler.current-in-workflows

**Contents:**
  - Customize Workflow Type {#workflow-type}
- Develop an Activity {#develop-activity}
- Start Activity Execution {#activity-execution}
  - Get Activity Execution results {#get-activity-results}
- Run Worker Process
  - Worker Processes with host builder and dependency injection
- Set a Dynamic Workflow {#set-a-dynamic-workflow}
- Set a Dynamic Activity {#set-a-dynamic-activity}
- Debugging - .NET SDK
- Debugging {#debug}

dotnet_diagnostic.VSTHRD105.severity = none
csharp
using Temporalio.Workflows;

[Workflow("MyDifferentWorkflowName")]
public class MyWorkflow
{
    public async Task<string> RunAsync(string name)
    {
        var param = MyActivityParams("Hello", name);
        return await Workflow.ExecuteActivityAsync(
            (MyActivities a) => a.MyActivity(param),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });
    }
}
csharp
using Temporalio.Activities;

public class MyActivities
{
    // Activities can be async and/or static too. We just demonstrate instance methods since many
    // use them that way.
    [Activity]
    public string MyActivity(MyActivityParams input) =>
        $"{input.Greeting}, {input.Name}!";
}
csharp
using Temporalio.Workflows;

[Workflow]
public class MyWorkflow
{
    public async Task<string> RunAsync(string name)
    {
        var param = MyActivityParams("Hello", name);
        return await Workflow.ExecuteActivityAsync(
            (MyActivities a) => a.MyActivity(param),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });
    }
}
csharp
// Create a client to localhost on default namespace
var client = await TemporalClient.ConnectAsync(new("localhost:7233")
{
    LoggerFactory = LoggerFactory.Create(builder =>
        builder.
            AddSimpleConsole(options => options.TimestampFormat = "[HH:mm:ss] ").
            SetMinimumLevel(LogLevel.Information)),
});

// Cancellation token cancelled on ctrl+c
using var tokenSource = new CancellationTokenSource();
Console.CancelKeyPress += (_, eventArgs) =>
{
    tokenSource.Cancel();
    eventArgs.Cancel = true;
};

// Create an activity instance with some state
var activities = new MyActivities();

// Run worker until cancelled
Console.WriteLine("Running worker");
using var worker = new TemporalWorker(
    client,
    new TemporalWorkerOptions(taskQueue: "my-task-queue").
        AddAllActivities(activities).
        AddWorkflow<MyWorkflow>());
try
{
    await worker.ExecuteAsync(tokenSource.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Worker cancelled");
}
csharp
var host = Host.CreateDefaultBuilder(args)
    .ConfigureLogging(ctx => ctx.AddSimpleConsole().SetMinimumLevel(LogLevel.Information))
    .ConfigureServices(ctx =>
        ctx.
            // Add the database client at the scoped level
            AddScoped<IMyDatabaseClient, MyDatabaseClient>().
            // Add the worker
            AddHostedTemporalWorker(
                clientTargetHost: "localhost:7233",
                clientNamespace: "default",
                taskQueue: "my-task-queue").
            // Add the activities class at the scoped level
            AddScopedActivities<MyActivities>().
            AddWorkflow<MyWorkflow>())
    .Build();
await host.RunAsync();
csharp
[Workflow(Dynamic = true)]
public class DynamicWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(IRawValue[] args)
    {
        var name = Workflow.PayloadConverter.ToValue<string>(args.Single());
        var param = MyActivityParams("Hello", name);
        return await Workflow.ExecuteActivityAsync(
            (MyActivities a) => a.MyActivity(param),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });
    }
}
csharp
public class MyActivities
{
    [Activity(Dynamic = true)]
    public string DynamicActivity(IRawValue[] args)
    {
        var input = ActivityExecutionContext.Current.PayloadConverter.ToValue<MyActivityParams>(args.Single());
        return $"{input.Greeting}, {input.Name}!";
    }
}
csharp
// Sleep for 3 days
await Workflow.DelayAsync(TimeSpan.FromDays(3));
csharp
using Temporalio.Client;

// Create client
var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

// Start a Workflow with static summary and details
var handle = await client.StartWorkflowAsync(
    (YourWorkflow wf) => wf.RunAsync("Workflow input"),
    new WorkflowOptions
    {
        Id = "your-Workflow-id",
        TaskQueue = "your-task-queue",
        StaticSummary = "Order processing for customer #12345",
        StaticDetails = "Processing premium order with expedited shipping"
    });
csharp
var result = await client.ExecuteWorkflowAsync(
    (YourWorkflow wf) => wf.RunAsync("Workflow input"),
    new WorkflowOptions
    {
        Id = "your-Workflow-id",
        TaskQueue = "your-task-queue",
        StaticSummary = "Order processing for customer #12345",
        StaticDetails = "Processing premium order with expedited shipping"
    });
csharp
using Temporalio.Workflows;

[Workflow]
public class YourWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(string input)
    {
        // Get the current details
        var currentDetails = Workflow.CurrentDetails;
        Workflow.Logger.LogInformation($"Current details: {currentDetails}");
        
        // Set/update the current details
        Workflow.CurrentDetails = "Updated Workflow details with new status";
        
        return "Workflow completed";
    }
}
csharp
using Temporalio.Activities;
using Temporalio.Workflows;

[Workflow]
public class YourWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(string input)
    {
        // Execute an activity with a summary
        var result = await Workflow.ExecuteActivityAsync(
            (YourActivities act) => act.YourActivityAsync(input),
            new ActivityOptions
            {
                StartToCloseTimeout = TimeSpan.FromSeconds(10),
                Summary = "Processing user data"
            });
        
        return result;
    }
}
csharp
using Temporalio.Workflows;

[Workflow]
public class YourWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(string input)
    {
        // Create a timer with a summary
        await Workflow.DelayWithOptionsAsync(new DelayOptions(TimeSpan.FromMinutes(5))
        {
            Summary = "Waiting for payment confirmation"
        });
        
        return "Timer completed";
    }
}
csharp
[Serializable]
public class InvalidDepartmentException : Exception
{
    public InvalidDepartmentException() : base() { }
    public InvalidDepartmentException(string message) : base(message) { }
    public InvalidDepartmentException(string message, Exception inner) : base(message, inner) { }
}

[Activity]
public Task<OrderConfirmation> SendBillAsync(Bill bill)
{
    throw new InvalidDepartmentException("Invalid department");
}
csharp
[Activity]
public Task<OrderConfirmation> SendBillAsync(Bill bill)
{
    throw new ApplicationFailureException("Invalid department", errorType: "InvalidDepartmentException");
}
csharp
[Activity]
public Task<OrderConfirmation> SendBillAsync(Bill bill)
{
    throw new ApplicationFailureException("Invalid department", nonRetryable: true);
}
csharp
try
{
    await Workflow.ExecuteActivityAsync(
        (Activities act) => act.ValidateCreditCardAsync(order.Customer.CreditCardNumber),
        options);
}
catch (ActivityFailureException err)
{
    logger.LogError("Unable to process credit card: {Message}", err.Message);
    throw new ApplicationFailureException(message: "Invalid credit card number error");
}
csharp
var result = await client.ExecuteWorkflowAsync(
    (MyWorkflow wf) => wf.RunAsync(),
    new(id: "my-workflow-id", taskQueue: "my-task-queue")
    {
        WorkflowExecutionTimeout = TimeSpan.FromMinutes(5),
    });
csharp
var result = await client.ExecuteWorkflowAsync(
    (MyWorkflow wf) => wf.RunAsync(),
    new(id: "my-workflow-id", taskQueue: "my-task-queue")
    {
        RetryPolicy = new() { MaximumInterval = TimeSpan.FromSeconds(10) },
    });
csharp
return await Workflow.ExecuteActivityAsync(
    (MyActivities a) => a.MyActivity(param),
    new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });
csharp
return await Workflow.ExecuteActivityAsync(
    (MyActivities a) => a.MyActivity(param),
    new()
    {
        StartToCloseTimeout = TimeSpan.FromMinutes(5),
        RetryPolicy = new() { MaximumInterval = TimeSpan.FromSeconds(10) },
    });
csharp
var attempt = ActivityExecutionContext.Current.Info.Attempt;

throw new ApplicationFailureException(
    $"Something bad happened on attempt {attempt}",
    errorType: "my_failure_type",
    nextRetryDelay: TimeSpan.FromSeconds(3 * attempt));
csharp
[Activity]
public async Task MyActivityAsync()
{
    while (true)
    {
        // Send heartbeat
        ActivityExecutionContext.Current.Heartbeat();

// Do some work, passing the cancellation token
        await Task.Delay(1000, ActivityExecutionContext.Current.CancellationToken);
    }
}
csharp
await Workflow.ExecuteActivityAsync(
    (MyActivities a) => a.MyActivity(param),
    new()
    {
        StartToCloseTimeout = TimeSpan.FromMinutes(5),
        HeartbeatTimeout = TimeSpan.FromSeconds(30),
    });
csharp
[Workflow]
public class GreetingWorkflow
{
    public enum Language
    {
        Chinese,
        English,
        French,
        Spanish,
        Portuguese,
    }

public record GetLanguagesInput(bool IncludeUnsupported);

[WorkflowQuery]
    public IList<Language> GetLanguages(GetLanguagesInput input) =>
        Enum.GetValues<Language>().
            Where(language => input.IncludeUnsupported || Greetings.ContainsKey(language)).
            ToList();

// ...
csharp
[Workflow]
public class GreetingWorkflow
{
    public enum Language
    {
        Chinese,
        English,
        French,
        Spanish,
        Portuguese,
    }

[WorkflowQuery]
    public Language CurrentLanguage { get; private set; } = Language.English;

// ...
csharp
[Workflow]
public class GreetingWorkflow
{
    public record ApproveInput(string Name);

[WorkflowSignal]
    public async Task ApproveAsync(ApproveInput input)
    {
        approvedForRelease = true;
        approverName = input.Name;
    }

// ...
csharp
[Workflow]
public class GreetingWorkflow
{
    public enum Language
    {
        Chinese,
        English,
        French,
        Spanish,
        Portuguese,
    }

[WorkflowUpdateValidator(nameof(SetCurrentLanguageAsync))]
    public void ValidateLanguage(Language language)
    {
        if (!Greetings.ContainsKey(language))
        {
            throw new ApplicationFailureException($"{language} is not supported");
        }
    }

[WorkflowUpdate]
    public async Task<Language> SetCurrentLanguageAsync(Language language)
    {
        var previousLanguage = CurrentLanguage;
        CurrentLanguage = language;
        return previousLanguage;
    }

// ...
csharp
var client = await TemporalClient.ConnectAsync(new("localhost:7233"));
var workflowHandle = await client.StartWorkflowAsync(
    (GreetingWorkflow wf) => wf.RunAsync(),
    new(id: "message-passing-workflow-id", taskQueue: "message-passing-sample"));
csharp
var supportedLanguages = await workflowHandle.QueryAsync(wf => wf.GetLanguages(new(false)));
csharp
await workflowHandle.SignalAsync(wf => wf.ApproveAsync(new("MyUser")));
csharp
// ...

[Workflow]
public class WorkflowB
{
    [WorkflowRun]
    public async Task RunAsync()
    {
        var handle = Workflow.GetExternalWorkflowHandle<WorkflowA>("workflow-a");
        await handle.SignalAsync(wf => wf.YourSignalAsync("signal argument"));
    }

// ...
csharp
var client = await TemporalClient.ConnectAsync(new("localhost:7233"));
var options = new WorkflowOptions(id: "your-signal-with-start-workflow", taskQueue: "signal-tq");
options.SignalWithStart((GreetingWorkflow wf) => wf.SubmitGreetingAsync("User Signal with Start"));
await client.StartWorkflowAsync((GreetingWorkflow wf) => wf.RunAsync(), options);
csharp
  var previousLanguage = await workflowHandle.ExecuteUpdateAsync(
    wf => wf.SetCurrentLanguageAsync(GreetingWorkflow.Language.Chinese));
  csharp
  // Wait until the update is accepted
  var updateHandle = await workflowHandle.StartUpdateAsync(
      wf => wf.SetGreetingAsync(new HelloWorldInput("World")),
      new(waitForStage: WorkflowUpdateStage.Accepted));
  // Wait until the update is completed
  var updateResult = await updateHandle.GetResultAsync();
  csharp
async Task<AddCartItemResult> AddCartItemAsync(string sessionId, ShoppingCartItem item)
{
    // Issue an update-with-start that will create the workflow if it does not
    // exist before attempting the update

// Create the start operation
    var startOperation = WithStartWorkflowOperation.Create(
        (ShoppingCartWorkflow wf) => wf.RunAsync(),
        new(id: $"cart-{sessionId}", taskQueue: TaskQueue)
        {
            IdConflictPolicy = Temporalio.Api.Enums.V1.WorkflowIdConflictPolicy.UseExisting,
        });

// Issue the update-with-start, swallowing item-unavailable failure
    decimal? subtotal;
    try
    {
        subtotal = await client.ExecuteUpdateWithStartWorkflowAsync(
            (ShoppingCartWorkflow wf) => wf.AddItemAsync(item),
            new(startOperation));
    }
    catch (WorkflowUpdateFailedException e) when (
        e.InnerException is ApplicationFailureException appErr && appErr.ErrorType == "ItemUnavailable")
    {
        // Set subtotal to null if item was not found
        subtotal = null;
    }

return new(await startOperation.GetHandleAsync(), subtotal);
}
csharp
public class MyActivities
{
    private static readonly Dictionary<Language, string> Greetings = new()
    {
        [Language.Arabic] = "مرحبا بالعالم",
        [Language.Chinese] = "你好，世界",
        [Language.English] = "Hello, world",
        [Language.French] = "Bonjour, monde",
        [Language.Hindi] = "नमस्ते दुनिया",
        [Language.Spanish] = "Hola mundo",
    };

[Activity]
    public async Task<string?> CallGreetingServiceAsync(Language language)
    {
        // Pretend that we are calling a remove service
        await Task.Delay(200);
        return Greetings.TryGetValue(language, out var value) ? value : null;
    }
}
csharp
[Workflow]
public class GreetingWorkflow
{
    private readonly Mutex mutex = new();

[WorkflowUpdate]
    public async Task<Language> SetLanguageAsync(Language language)
    {
        // 👉 Use a mutex here to ensure that multiple calls to SetLanguageAsync are processed in order.
        await mutex.WaitOneAsync();
        try
        {
            if (!greetings.ContainsKey(language))
            {
                var greeting = Workflow.ExecuteActivityAsync(
                    (MyActivities acts) => acts.CallGreetingServiceAsync(language),
                    new() { StartToCloseTimeout = TimeSpan.FromSeconds(10) });
                if (greeting == null)
                {
                    // 👉 An update validator cannot be async, so cannot be used to check that the remote
                    // CallGreetingServiceAsync supports the requested language. Throwing ApplicationFailureException
                    // will fail the Update, but the WorkflowExecutionUpdateAccepted event will still be
                    // added to history.
                    throw new ApplicationFailureException(
                        $"Greeting service does not support {language}");
                }
                greetings[language] = greeting;
            }
            var previousLanguage = CurrentLanguage;
            CurrentLanguage = language;
            return previousLanguage;
        }
        finally
        {
            mutex.ReleaseMutex();
        }
    }
}
csharp
[WorkflowUpdate]
public async Task<string> MyUpdateAsync(UpdateInput updateInput)
{
    await Workflow.WaitConditionAsync(() => ReadyForUpdateToExecute(updateInput));
    // ...
}
csharp
[Workflow]
public class MyWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync()
    {
        // ...
        await Workflow.WaitConditionAsync(() => Workflow.AllHandlersFinished);
        return "workflow-result";
    }

// ...
csharp
[WorkflowUpdate(UnfinishedPolicy = HandlerUnfinishedPolicy.Abandon)]
public async Task MyUpdateAsync()
{
    // ...
csharp
[Workflow]
public class WorkflowInitWorkflow
{
    public record Input(string Name);

private readonly string nameWithTitle;
    private bool titleHasBeenChecked;

[WorkflowInit]
    public WorkflowInitWorkflow(Input input) =>
        nameWithTitle = $"Sir {input.Name}";

[WorkflowRun]
    public async Task<string> RunAsync(Input ignored)
    {
        await Workflow.WaitConditionAsync(() => titleHasBeenChecked);
        return $"Hello, {nameWithTitle}";
    }

[WorkflowUpdate]
    public async Task<bool> CheckTitleValidityAsync()
    {
        // The handler is now guaranteed to see the workflow input after it has
        // been processed by the constructor.
        var valid = await Workflow.ExecuteActivityAsync(
            (MyActivities acts) -> acts.CheckTitleValidityAsync(nameWithTitle),
            new() { StartToCloseTimeout = TimeSpan.FromSeconds(10) });
        titleHasBeenChecked = true;
        return valid;
    }
}
csharp
[Workflow]
public class MyWorkflow
{
    // ...

[WorkflowSignal]
    public async Task BadHandlerAsync()
    {
        var data = await Workflow.ExecuteActivityAsync(
            (MyActivities acts) => acts.FetchDataAsync(),
            new() { StartToCloseTimeout = TimeSpan.FromSeconds(10) });
        this.x = data.X;
        // 🐛🐛 Bug!! If multiple instances of this handler are executing concurrently, then
        // there may be times when the Workflow has this.x from one Activity execution and this.y from another.
        await Workflow.DelayAsync(1000);
        this.y = data.Y;
    }
}
csharp
[Workflow]
public class MyWorkflow
{
    private readonly Mutex mutex = new();

[WorkflowSignal]
    public async Task SafeHandlerAsync()
    {
        await mutex.WaitOneAsync();
        try
        {
            var data = await Workflow.ExecuteActivityAsync(
                (MyActivities acts) => acts.FetchDataAsync(),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(10) });
            this.x = data.X;
            // ✅ OK: the scheduler may switch now to a different handler execution, or to the main workflow
            // method, but no other execution of this handler can run until this execution finishes.
            await Workflow.DelayAsync(1000);
            this.y = data.Y;
        }
        finally
        {
            mutex.ReleaseMutex();
        }
    }
}
csharp
[WorkflowQuery(Dynamic = true)]
public string DynamicQueryAsync(string queryName, IRawValue[] args)
{
    var input = Workflow.PayloadConverter.ToValue<MyStatusParam>(args.Single());
    return statuses[input.Type];
}
csharp
[WorkflowSignal(Dynamic = true)]
public async Task DynamicSignalAsync(string signalName, IRawValue[] args)
{
    var input = Workflow.PayloadConverter.ToValue<DoSomethingParam>(args.Single());
    pendingThings.Add(input);
}
csharp
[WorkflowUpdate(Dynamic = true)]
public async Task<string> DynamicUpdateAsync(string updateName, IRawValue[] args)
{
    var input = Workflow.PayloadConverter.ToValue<DoSomethingParam>(args.Single());
    pendingThings.Add(input);
    return statuses[input.Type];
}
csharp
using Temporalio.Client;
using Temporalio.Runtime;

var runtime = new TemporalRuntime(new()
{
    Telemetry = new() { Metrics = new() { Prometheus = new("0.0.0.0:9000") } },
});
var client = await Temporalio.ConnectAsync(new("localhost:7233") { Runtime = runtime });
csharp
using System.Diagnostics.Metrics;
using Temporalio.Client;
using Temporalio.Extensions.DiagnosticSource;
using Temporalio.Runtime;

// Create .NET meter
using var meter = new Meter("My.Meter");
// Can create MeterListener or OTel meter provider here...

// Create Temporal runtime with a custom metric meter for that meter
var runtime = new TemporalRuntime(new()
{
    Telemetry = new()
    {
        Metrics = new() { CustomMetricMeter = new CustomMetricMeter(meter) },
    },
});
var client = await Temporalio.ConnectAsync(new("localhost:7233") { Runtime = runtime });
csharp
var client = await TemporalClient.ConnectAsync(new("localhost:7233")
{
    LoggerFactory = LoggerFactory.Create(builder =>
        builder.
            AddSimpleConsole(options => options.TimestampFormat = "[HH:mm:ss] ").
            SetMinimumLevel(LogLevel.Information)),
});
csharp
Workflow.Logger.LogInformation("Given name: {Name}", name);
csharp
await foreach (var wf in client.ListWorkflowsAsync("WorkflowType='GreetingWorkflow'"))
{
    Console.WriteLine("Workflow: {0}", wf.Id);
}
csharp
// This only needs to be created once, so it is common to make it a static readonly even though we
// create inline here for demonstration
var myKeywordAttributeKey = SearchAttributeKey.CreateKeyword("MyKeywordAttribute");

// Start workflow with the search attribute collection
var handle = await client.StartWorkflowAsync(
    (MyWorkflow wf) => wf.RunAsync(),
    new(id: "my-workflow-id", taskQueue: "my-task-queue")
    {
        TypedSearchAttributes = new SearchAttributeCollection.Builder().
            Set(myKeywordAttributeKey, "SomeKeywordValue").
            ToSearchAttributeCollection(),
    });
csharp
// These only need to be created once, so it is common to make them static readonly even though we
// create inline here for demonstration
var myKeywordAttributeKey = SearchAttributeKey.CreateKeyword("MyKeywordAttribute");
var myTextAttributeKey = SearchAttributeKey.CreateText("MyTextAttribute");

// Add/Update the keyword one and remove the text one
Workflow.UpsertTypedSearchAttributes(
    myKeywordAttributeKey.ValueSet("SomeKeywordValue"),
    myTextAttrbiuteKey.ValueUnset());
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

var handle = await client.CreateScheduleAsync(
    "my-schedule-id",
    new(
        Action: ScheduleActionStartWorkflow.Create(
            (MyWorkflow wf) => wf.RunAsync(),
            new(id: "my-workflow-id", taskQueue: "my-task-queue")),
        Spec: new()
        {
            Intervals = new List<ScheduleIntervalSpec> { new(Every: TimeSpan.FromDays(5)) },
        }));
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

var handle = client.GetScheduleHandle("my-schedule-id");
var now = DateTime.Now;
await handle.BackfillAsync(new List<ScheduleBackfill>
{
    new(
        StartAt: now - TimeSpan.FromDays(30),
        EndAt: now - TimeSpan.FromDays(20),
        Overlap: ScheduleOverlapPolicy.AllowAll),
});
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

var handle = client.GetScheduleHandle("my-schedule-id");
await handle.DeleteAsync();
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

var handle = client.GetScheduleHandle("my-schedule-id");
var desc = await handle.DescribeAsync();
Console.WriteLine("Schedule info: {0}", desc.Info);
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));
await foreach (var desc in client.ListSchedulesAsync())
{
    Console.WriteLine("Schedule info: {0}", desc.Info);
}
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

var handle = client.GetScheduleHandle("my-schedule-id");
await handle.PauseAsync("Pausing the schedule for now");
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

var handle = client.GetScheduleHandle("my-schedule-id");
await handle.TriggerAsync();
csharp
using Temporalio.Client;
using Temporalio.Client.Schedules;

var client = await TemporalClient.ConnectAsync(new("localhost:7233"));

var handle = client.GetScheduleHandle("my-schedule-id");
await handle.UpdateAsync(input =>
{
    var newAction =  ScheduleActionStartWorkflow.Create(
        (MyWorkflow wf) => wf.RunAsync(),
        new(id: "my-workflow-id", taskQueue: "my-task-queue"));
    return new(input.Description.Schedule with { Action = newAction });
});
csharp
var handle = await client.StartWorkflowAsync(
    (MyWorkflow wf) => wf.RunAsync(),
    new(id: "my-workflow-id", taskQueue: "my-task-queue")
    {
        StartDelay = TimeSpan.FromHours(3),
    });
```

## Set up your local with the .NET SDK

**Examples:**

Example 1 (unknown):
```unknown
### Customize Workflow Type {#workflow-type}

**How to customize your Workflow Type name using the Temporal .NET SDK**

Workflows have a Type that are referred to as the Workflow name.

The following examples demonstrate how to set a custom name for your Workflow Type.

You can customize the Workflow name with a custom name in the attribute. For example, `[Workflow("my-workflow-name")]`. If the name parameter is not specified, the Workflow name defaults to the unqualified class name.
```

Example 2 (unknown):
```unknown
## Develop an Activity {#develop-activity}

**How to develop a basic Activity using the Temporal .NET SDK**

One of the primary things that Workflows do is orchestrate the execution of Activities.
An Activity is a normal method execution that's intended to execute a single, well-defined action (either short or long-running), such as querying a database, calling a third-party API, or transcoding a media file.
An Activity can interact with world outside the Temporal Platform or use a Temporal Client to interact with a Temporal Service.
For the Workflow to be able to execute the Activity, we must define the [Activity Definition](/activity-definition).

You can develop an Activity Definition by using the `[Activity]` attribute from the `Temporalio.Activities` namespace on the method.
To register a method as an Activity with a custom name, use an attribute parameter, for example `[Activity("your-activity")]`.
Otherwise, the activity name is the unqualified method name (sans an "Async" suffix if the method is async).

Activities can be asynchronous or synchronous.
```

Example 3 (unknown):
```unknown
There is no explicit limit to the total number of parameters that an [Activity Definition](/activity-definition) may support.
However, there is a limit to the total size of the data that ends up encoded into a gRPC message Payload.

A single argument is limited to a maximum size of 2 MB.
And the total size of a gRPC message, which includes all the arguments, is limited to a maximum of 4 MB.

Also, keep in mind that all Payload data is recorded in the [Workflow Execution Event History](/workflow-execution/event#event-history) and large Event Histories can affect Worker performance.
This is because the entire Event History could be transferred to a Worker Process with a [Workflow Task](/tasks#workflow-task).

Some SDKs require that you pass context objects, others do not.
When it comes to your application data—that is, data that is serialized and encoded into a Payload—we recommend that you use a single object as an argument that wraps the application data passed to Activities.
This is so that you can change what data is passed to the Activity without breaking a method signature.

Activity parameters are the method parameters of the method with the `[Activity]` attribute.
These can be any data type Temporal can convert, including records.
Technically this can be multiple parameters, but Temporal strongly encourages a single parameter containing all input fields.

## Start Activity Execution {#activity-execution}

**How to start an Activity Execution using the Temporal .NET SDK**

Calls to spawn [Activity Executions](/activity-execution) are written within a [Workflow Definition](/workflow-definition).
The call to spawn an Activity Execution generates the [ScheduleActivityTask](/references/commands#scheduleactivitytask) Command.
This results in the set of three [Activity Task](/tasks#activity-task) related Events ([ActivityTaskScheduled](/references/events#activitytaskscheduled), [ActivityTaskStarted](/references/events#activitytaskstarted), and ActivityTask[Closed])in your Workflow Execution Event History.

A single instance of the Activities implementation is shared across multiple simultaneous Activity invocations.
Activity implementation code should be _idempotent_.

The values passed to Activities through invocation parameters or returned through a result value are recorded in the Execution history.
The entire Execution history is transferred from the Temporal service to Workflow Workers when a Workflow state needs to recover.
A large Execution history can thus adversely impact the performance of your Workflow.

Therefore, be mindful of the amount of data you transfer through Activity invocation parameters or Return Values.
Otherwise, no additional limitations exist on Activity implementations.

To spawn an Activity Execution, use the `ExecuteActivityAsync` operation from within your Workflow Definition.
```

Example 4 (unknown):
```unknown
Activity Execution semantics rely on several parameters.
The only required value that needs to be set is either a [Schedule-To-Close Timeout](/encyclopedia/detecting-activity-failures#schedule-to-close-timeout) or a [Start-To-Close Timeout](/encyclopedia/detecting-activity-failures#start-to-close-timeout).
These values are set in the Activity Options.

### Get Activity Execution results {#get-activity-results}

**How to get the results of an Activity Execution using the Temporal .NET SDK**

The Activity result is the returned in the task from the `ExecuteActivityAsync` call.

## Run Worker Process

**How to create and run a Worker Process using the Temporal .NET SDK**

The [Worker Process](/workers#worker-process) is where Workflow Functions and Activity Functions are executed.

- Each [Worker Entity](/workers#worker-entity) in the Worker Process must register the exact Workflow Types and Activity Types it may execute.
- Each Worker Entity must also associate itself with exactly one [Task Queue](/task-queue).
- Each Worker Entity polling the same Task Queue must be registered with the same Workflow Types and Activity Types.

A [Worker Entity](/workers#worker-entity) is the component within a Worker Process that listens to a specific Task Queue.

Although multiple Worker Entities can be in a single Worker Process, a single Worker Entity Worker Process may be perfectly sufficient.
For more information, see the [Worker tuning guide](/develop/worker-performance).

A Worker Entity contains a Workflow Worker and/or an Activity Worker, which makes progress on Workflow Executions and Activity Executions, respectively.

To develop a Worker, create a new `Temporalio.Worker.TemporalWorker` providing the Client and worker options which include Task Queue, Workflows, and Activities and more.
The following code example creates a Worker that polls for tasks from the Task Queue and executes the Workflow.
When a Worker is created, it accepts a list of Workflows, a list of Activities, or both.
```

---

## Optional: Add custom gRPC headers

**URL:** llms-txt#optional:-add-custom-grpc-headers

[profile.default.grpc_meta]
my-custom-header = "development-value"
trace-id = "dev-trace-123"

---

## Use the run method to start the Activity, passing in the function that contains the Heartbeats and any necessary parameters.

**URL:** llms-txt#use-the-run-method-to-start-the-activity,-passing-in-the-function-that-contains-the-heartbeats-and-any-necessary-parameters.

await env.run(activity_with_heartbeats, "test")

---

## Replay all workflows from a list

**URL:** llms-txt#replay-all-workflows-from-a-list

**Contents:**
- Versioning - Ruby SDK
- Worker Versioning
- Versioning with Patching {#ruby-sdk-patching-api}
  - Adding a patch
  - Patching in new code
  - Deprecating patches {#deprecated-patches}
  - Removing a patch {#deploy-new-code}
  - Workflow cutovers
  - Testing a Workflow for replay safety
- Safely deploying changes to Workflow code

replayer.replay_workflows(client.list_workflows("WorkflowType = 'MyWorkflow'")).each do |result|
  # Raise if any failed (could have just set raise_on_replay_failure: true, but this
  # demonstrates iterating over the results)
  raise result.replay_failure if result.replay_failure
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    result = Temporalio::Workflow.execute_activity(
      PrePatchActivity,
      start_to_close_timeout: 100
    )

# ...
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    result = Temporalio::Workflow.execute_activity(
      PostPatchActivity,
      start_to_close_timeout: 100
    )

# ...
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    if Temporalio::Workflow.patched('my-patch')
      result = Temporalio::Workflow.execute_activity(
        PostPatchActivity,
        start_to_close_timeout: 100
      )
    else
      result = Temporalio::Workflow.execute_activity(
        PrePatchActivity,
        start_to_close_timeout: 100
      )
    end

# ...
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    Temporalio::Workflow.deprecate_patch('my-patch')
    result = Temporalio::Workflow.execute_activity(
      PostPatchActivity,
      start_to_close_timeout: 100
    )

# ...
  end
end
ruby
class MyWorkflow < Temporalio::Workflow::Definition
  def execute
    # ...
  end
end

class MyWorkflowV2 < Temporalio::Workflow::Definition
  def execute
    # ...
  end
end
ruby
client = Temporalio::Client.connect('localhost:7233', 'default')

worker = Temporalio::Worker.new(
  client:,
  task_queue: 'my-task-queue',
  workflows: [MyWorkflow, MyWorkflowV2]
)
python

from datetime import datetime, timedelta

from temporalio.client import Client
from temporalio.worker import Worker, Replayer

async def main():
    parser = argparse.ArgumentParser(prog='MyTemporalWorker')
    parser.add_argument('mode', choices=['verify', 'run'])
    args = parser.parse_args()

temporal_url = "localhost:7233"
    task_queue = "your-task-queue"
    my_workflows = [YourWorkflow]
    my_activities = [your_activity]

client = await Client.connect(temporal_url)
python
if args.mode == 'verify':
    start_time = (datetime.now() - timedelta(hours=10)).isoformat(timespec='seconds')
    workflows = client.list_workflows(
     f"TaskQueue={task_queue} and StartTime > '{start_time}'",
    limit = 100)
    histories = workflows.map_histories()
    replayer = Replayer(
        workflows=my_workflows,
    )
    await replayer.replay_workflows(histories)
    return
python
    else:
        worker = Worker(
            client,
            task_queue=task_queue,
            workflows=my_workflows,
            activities=my_activities,
        )
        await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
bash
   npm install @temporalio/ai-sdk
   ts {9-11}

//... other import statements, initializing a connection
   //  to the Temporal Service to be used by the Worker

const worker = await Worker.create({
     plugins: [
       new AiSDKPlugin({
         modelProvider: openai,
       }),
     ],
     connection,
     namespace: 'default',
     taskQueue: 'ai-sdk',
     workflowsPath: require.resolve('./workflows'),
     activities,
   });

// ... code that runs the worker
   bash
   nodemon worker.ts
   ts

async function haikuAgent(prompt: string): Promise<string> {
  const result = await generateText({
    model: openai('gpt-4o-mini'),
    prompt,
    system: 'You only respond in haikus.',
  });
  return result.text;
}
ts {2,6}

export async function haikuAgent(prompt: string): Promise<string> {
  const result = await generateText({
    model: temporalProvider.languageModel('gpt-4o-mini'),
    prompt,
    system: 'You only respond in haikus.',
  });
  return result.text;
}
ts
export async function getWeather(input: {
  location: string;
}): Promise<{ city: string; temperatureRange: string; conditions: string }> {
  console.log('Activity execution');
  return {
    city: input.location,
    temperatureRange: '14-20C',
    conditions: 'Sunny with wind.',
  };
}
ts {15-23}

const { getWeather } = proxyActivities<typeof activities>({
  startToCloseTimeout: '1 minute',
});

export async function toolsAgent(question: string): Promise<string> {
  const result = await generateText({
    model: temporalProvider.languageModel('gpt-4o-mini'),
    prompt: question,
    system: 'You are a helpful agent.',
    tools: {
      getWeather: tool({
        description: 'Get the weather for a given city',
        inputSchema: z.object({
          location: z.string().describe('The location to get the weather for'),
        }),
        execute: getWeather,
      }),
    },
    stopWhen: stepCountIs(5),
  });
  return result.text;
}
ts

const mcpClientFactories = {
     testServer: () =>
       createMCPClient({
         transport: new StdioClientTransport({
           command: 'node',
           args: ['lib/mcp-server.js'],
         }),
       }),
   };
   ts {5}
   const worker = await Worker.create({
     plugins: [
       new AiSDKPlugin({
         modelProvider: openai,
         mcpClientFactories
       }),
     ]},
     ...
   );
   ts {4-5,9}

export async function mcpAgent(prompt: string): Promise<string> {
     const mcpClient = new TemporalMCPClient({ name: 'testServer' });
     const tools = await mcpClient.tools();
     const result = await generateText({
       model: temporalProvider.languageModel('gpt-4o-mini'),
       prompt,
       tools,
       system: 'You are a helpful agent, You always use your tools when needed.',
       stopWhen: stepCountIs(5),
     });
     return result.text;
   }
   ts

export async function doSomethingAsync(): Promise<string> {
  const taskToken = activityInfo().taskToken;
  setTimeout(() => doSomeWork(taskToken), 1000);
  throw new CompleteAsyncError();
}

// this work could be done in a different process or on a different machine
async function doSomeWork(taskToken: Uint8Array): Promise<void> {
  const client = new AsyncCompletionClient();
  // does some work...
  await client.complete(taskToken, "Job's done!");
}
ts

const { getEnvVar } = workflow.proxyLocalActivities({
  startToCloseTimeout: '2 seconds',
});

export async function yourWorkflow(): Promise<void> {
  const someSetting = await getEnvVar('SOME_SETTING');
  // ...
}
typescript

ApplicationFailure,
  ApplicationFailureCategory,
} from '@temporalio/common';

export async function myActivity(): Promise<string> {
  try {
    return await callExternalService();
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    throw ApplicationFailure.create({
      message,
      // Mark this error as benign since it's expected
      category: ApplicationFailureCategory.BENIGN,
    });
  }
}
ts

export async function cancelTimer(): Promise<void> {
  // Timers and Activities are automatically cancelled when their containing scope is cancelled.
  try {
    await CancellationScope.cancellable(async () => {
      const promise = sleep(1); // <-- Will be cancelled because it is attached to this closure's scope
      CancellationScope.current().cancel();
      await promise; // <-- Promise must be awaited in order for `cancellable` to throw
    });
  } catch (e) {
    if (e instanceof CancelledFailure) {
      console.log('Timer cancelled 👍');
    } else {
      throw e; // <-- Fail the workflow
    }
  }
}
ts

export async function cancelTimerAltImpl(): Promise<void> {
  try {
    const scope = new CancellationScope();
    const promise = scope.run(() => sleep(1));
    scope.cancel(); // <-- Cancel the timer created in scope
    await promise; // <-- Throws CancelledFailure
  } catch (e) {
    if (e instanceof CancelledFailure) {
      console.log('Timer cancelled 👍');
    } else {
      throw e; // <-- Fail the workflow
    }
  }
}
ts

const { httpPostJSON, cleanup } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10m',
});

export async function handleExternalWorkflowCancellationWhileActivityRunning(url: string, data: any): Promise<void> {
  try {
    await httpPostJSON(url, data);
  } catch (err) {
    if (isCancellation(err)) {
      console.log('Workflow cancelled');
      // Cleanup logic must be in a nonCancellable scope
      // If we'd run cleanup outside of a nonCancellable scope it would've been cancelled
      // before being started because the Workflow's root scope is cancelled.
      await CancellationScope.nonCancellable(() => cleanup(url));
    }
    throw err; // <-- Fail the Workflow
  }
}
ts
export async function nonCancellable(url: string): Promise<any> {
  // Prevent Activity from being cancelled and await completion.
  // Note that the Workflow is completely oblivious and impervious to cancellation in this example.
  return CancellationScope.nonCancellable(() => httpGetJSON(url));
}
ts

export function multipleActivitiesSingleTimeout(urls: string[], timeoutMs: number): Promise<any> {
  const { httpGetJSON } = proxyActivities<typeof activities>({
    startToCloseTimeout: timeoutMs,
  });

// If timeout triggers before all activities complete
  // the Workflow will fail with a CancelledError.
  return CancellationScope.withTimeout(timeoutMs, () => Promise.all(urls.map((url) => httpGetJSON(url))));
}
ts

const { httpGetJSON } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10m',
});

export async function resumeAfterCancellation(url: string): Promise<any> {
  let result: any = undefined;
  const scope = new CancellationScope({ cancellable: false });
  const promise = scope.run(() => httpGetJSON(url));
  try {
    result = await Promise.race([scope.cancelRequested, promise]);
  } catch (err) {
    if (!(err instanceof CancelledFailure)) {
      throw err;
    }
    // Prevent Workflow from completing so Activity can complete
    result = await promise;
  }
  return result;
}
ts

function doSomething(callback: () => any) {
  setTimeout(callback, 10);
}

export async function cancellationScopesWithCallbacks(): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    doSomething(resolve);
    CancellationScope.current().cancelRequested.catch(reject);
  });
}
ts

const { setup, httpPostJSON, cleanup } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10m',
});

export async function nestedCancellation(url: string): Promise<void> {
  await CancellationScope.cancellable(async () => {
    await CancellationScope.nonCancellable(() => setup());
    try {
      await CancellationScope.withTimeout(1000, () => httpPostJSON(url, { some: 'data' }));
    } catch (err) {
      if (isCancellation(err)) {
        await CancellationScope.nonCancellable(() => cleanup(url));
      }
      throw err;
    }
  });
}
ts
export async function sharedScopes(): Promise<any> {
  // Start activities in the root scope
  const p1 = httpGetJSON('http://url1.ninja');
  const p2 = httpGetJSON('http://url2.ninja');

const scopePromise = CancellationScope.cancellable(async () => {
    const first = await Promise.race([p1, p2]);
    // Does not cancel activity1 or activity2 as they're linked to the root scope
    CancellationScope.current().cancel();
    return first;
  });
  return await scopePromise;
  // The Activity that did not complete will effectively be cancelled when
  // Workflow completes unless the Activity is awaited:
  // await Promise.all([p1, p2]);
}
ts
export async function shieldAwaitedInRootScope(): Promise<any> {
  let p: Promise<any> | undefined = undefined;

await CancellationScope.nonCancellable(async () => {
    p = httpGetJSON('http://example.com'); // <-- Start activity in nonCancellable scope without awaiting completion
  });
  // Activity is shielded from cancellation even though it is awaited in the cancellable root scope
  return p;
}
bash
temporal workflow reset \
    --workflow-id <workflow-id> \
    --event-id <event-id> \
    --reason "Reason for reset"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code" \
    --namespace my-namespace \
    --tls-cert-path /path/to/cert.pem \
    --tls-key-path /path/to/key.pem
ts

export async function parentWorkflow(names: string[]) {
  const childHandle = await startChild(childWorkflow, {
    args: [name],
    // workflowId, // add business-meaningful workflow id here
    // // regular workflow options apply here, with two additions (defaults shown):
    // cancellationType: ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
    // parentClosePolicy: ParentClosePolicy.PARENT_CLOSE_POLICY_TERMINATE
  });
  // you can use childHandle to signal or get result here
  await childHandle.signal('anySignal');
  const result = childHandle.result();
  // you can use childHandle to signal, query, cancel, terminate, or get result here
}
ts

export async function parentWorkflow(...names: string[]): Promise<string> {
  const responseArray = await Promise.all(
    names.map((name) =>
      executeChild(childWorkflow, {
        args: [name],
        // workflowId, // add business-meaningful workflow id here
        // // regular workflow options apply here, with two additions (defaults shown):
        // cancellationType: ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
        // parentClosePolicy: ParentClosePolicy.PARENT_CLOSE_POLICY_TERMINATE
      }),
    ),
  );
  return responseArray.join('\n');
}
ts

export async function terminateWorkflow() {
  const { workflowId } = workflowInfo(); // no await needed
  const handle = getExternalWorkflowHandle(workflowId); // sync function, not async
  await handle.cancel();
}
ts

export async function parentWorkflow(...names: string[]): Promise<string> {
  const responseArray = await Promise.all(
    names.map((name) =>
      executeChild(childWorkflow, {
        args: [name],
        // workflowId, // add business-meaningful workflow id here
        // // regular workflow options apply here, with two additions (defaults shown):
        // cancellationType: ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
        // parentClosePolicy: ParentClosePolicy.PARENT_CLOSE_POLICY_TERMINATE
      }),
    ),
  );
  return responseArray.join('\n');
}
typescript
export interface ClusterManagerInput {
  state?: ClusterManagerState;
}

export async function clusterManagerWorkflow(input: ClusterManagerInput = {}): Promise<ClusterManagerStateSummary> {

typescript
return await wf.continueAsNew<typeof clusterManagerWorkflow>({ 
  state: manager.getState(),
  testContinueAsNew: input.testContinueAsNew 
});
typescript
shouldContinueAsNew(): boolean {
  if (wf.workflowInfo().continueAsNewSuggested) {
    return true;
  }

// This is just for ease-of-testing. In production, we trust temporal to tell us when to continue-as-new.
  if (this.maxHistoryLength !== undefined && wf.workflowInfo().historyLength > this.maxHistoryLength) {
    return true;
  }

return false;
}
ts
interface PayloadCodec {
  /**
   * Encode an array of {@link Payload}s for sending over the wire.
   * @param payloads May have length 0.
   */
  encode(payloads: Payload[]): Promise<Payload[]>;

/**
   * Decode an array of {@link Payload}s received from the wire.
   */
  decode(payloads: Payload[]): Promise<Payload[]>;
}
typescript
export class DefaultPayloadConverter extends CompositePayloadConverter {
  constructor() {
    super(
      new UndefinedPayloadConverter(),
      new BinaryPayloadConverter(),
      new JsonPayloadConverter(),
    );
  }
}
typescript
export const payloadConverter = new CompositePayloadConverter(
  new UndefinedPayloadConverter(),
  new EjsonPayloadConverter(),
);
typescript
const worker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  taskQueue: 'ejson',
  dataConverter: {
    payloadConverterPath: require.resolve('./payload-converter'),
  },
});
typescript
const client = new Client({
  dataConverter: {
    payloadConverterPath: require.resolve('./payload-converter'),
  },
});
typescript
interface PayloadConverter {
  /**
   * Converts a value to a {@link Payload}.
   * @param value The value to convert. Example values include the Workflow args sent by the client and the values returned by a Workflow or Activity.
   */
  toPayload<T>(value: T): Payload;

/**
   * Converts a {@link Payload} back to a value.
   */
  fromPayload<T>(payload: Payload): T;
}
ts

EncodingType,
  METADATA_ENCODING_KEY,
  Payload,
  PayloadConverterWithEncoding,
  PayloadConverterError,
} from '@temporalio/common';

/**
 * Converts between values and [EJSON](https://docs.meteor.com/api/ejson.html) Payloads.
 */
export class EjsonPayloadConverter implements PayloadConverterWithEncoding {
  // Use 'json/plain' so that Payloads are displayed in the UI
  public encodingType = 'json/plain' as EncodingType;

public toPayload(value: unknown): Payload | undefined {
    if (value === undefined) return undefined;
    let ejson;
    try {
      ejson = EJSON.stringify(value);
    } catch (e) {
      throw new UnsupportedEjsonTypeError(
        `Can't run EJSON.stringify on this value: ${value}. Either convert it (or its properties) to EJSON-serializable values (see https://docs.meteor.com/api/ejson.html ), or create a custom data converter. EJSON.stringify error message: ${errorMessage(
          e,
        )}`,
        e as Error,
      );
    }

return {
      metadata: {
        [METADATA_ENCODING_KEY]: encode('json/plain'),
        // Include an additional metadata field to indicate that this is an EJSON payload
        format: encode('extended'),
      },
      data: encode(ejson),
    };
  }

public fromPayload<T>(content: Payload): T {
    return content.data ? EJSON.parse(decode(content.data)) : content.data;
  }
}

export class UnsupportedEjsonTypeError extends PayloadConverterError {
  public readonly name: string = 'UnsupportedJsonTypeError';

constructor(
    message: string | undefined,
    public readonly cause?: Error,
  ) {
    super(message ?? undefined);
  }
}
ts

export const payloadConverter = new CompositePayloadConverter(
  new UndefinedPayloadConverter(),
  new EjsonPayloadConverter(),
);
ts
const worker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  taskQueue: 'ejson',
  dataConverter: { payloadConverterPath: require.resolve('./payload-converter') },
});
ts
const client = new Client({
  connection,
  dataConverter: { payloadConverterPath: require.resolve('./payload-converter') },
});
ts
const user: User = {
  id: uuid(),
  // age: 1000n, BigInt isn't supported
  hp: Infinity,
  matcher: /.*Stormblessed/,
  token: Uint8Array.from([1, 2, 3]),
  createdAt: new Date(),
};

const handle = await client.workflow.start(example, {
  args: [user],
  taskQueue: 'ejson',
  workflowId: `example-user-${user.id}`,
});
ts

export async function example(user: User): Promise<Result> {
  const success =
    user.createdAt.getTime() < Date.now() &&
    user.hp > 50 &&
    user.matcher.test('Kaladin Stormblessed') &&
    user.token instanceof Uint8Array;
  return { success, at: new Date() };
}
sh
  pbjs -t json-module --workflow-id commonjs -o protos/json-module.js protos/*.proto
  js
const { patchProtobufRoot } = require('@temporalio/common/lib/protobufs');
const unpatchedRoot = require('./json-module');
module.exports = patchProtobufRoot(unpatchedRoot);
sh
  pbjs -t static-module protos/*.proto | pbts -o protos/root.d.ts -
  ts

export const payloadConverter = new DefaultPayloadConverterWithProtobufs({ protobufRoot: root });
ts

export const payloadConverter = new ProtobufBinaryPayloadConverter(root);
ts

BinaryPayloadConverter,
  CompositePayloadConverter,
  JsonPayloadConverter,
  UndefinedPayloadConverter,
} from '@temporalio/common';

export const payloadConverter = new CompositePayloadConverter(
  new UndefinedPayloadConverter(),
  new BinaryPayloadConverter(),
  new ProtobufBinaryPayloadConverter(root),
  new JsonPayloadConverter(),
);
ts
const worker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  activities,
  taskQueue: 'protobufs',
  dataConverter: { payloadConverterPath: require.resolve('./payload-converter') },
});
ts

async function run() {
  const config = loadClientConnectConfig();
  const connection = await Connection.connect(config.connectionOptions);
  const client = new Client({
    connection,
    dataConverter: { payloadConverterPath: require.resolve('./payload-converter') },
  });

const handle = await client.workflow.start(example, {
    args: [foo.bar.ProtoInput.create({ name: 'Proto', age: 2 })],
    // can't do:
    // args: [new foo.bar.ProtoInput({ name: 'Proto', age: 2 })],
    taskQueue: 'protobufs',
    workflowId: 'my-business-id-' + uuid(),
  });

console.log(`Started workflow ${handle.workflowId}`);

const result: ProtoResult = await handle.result();
  console.log(result.toJSON());
}
ts

const { protoActivity } = proxyActivities<typeof activities>({
  startToCloseTimeout: '1 minute',
});

export async function example(input: foo.bar.ProtoInput): Promise<ProtoResult> {
  const result = await protoActivity(input);
  return result;
}
ts

export async function protoActivity(input: foo.bar.ProtoInput): Promise<ProtoResult> {
  return ProtoResult.create({ sentence: `${input.name} is ${input.age} years old.` });
}
ts

const ENCODING = 'binary/encrypted';
const METADATA_ENCRYPTION_KEY_ID = 'encryption-key-id';

export class EncryptionCodec implements PayloadCodec {
  constructor(
    protected readonly keys: Map<string, crypto.CryptoKey>,
    protected readonly defaultKeyId: string,
  ) {}

static async create(keyId: string): Promise<EncryptionCodec> {
    const keys = new Map<string, crypto.CryptoKey>();
    keys.set(keyId, await fetchKey(keyId));
    return new this(keys, keyId);
  }

async encode(payloads: Payload[]): Promise<Payload[]> {
    return Promise.all(
      payloads.map(async (payload) => ({
        metadata: {
          [METADATA_ENCODING_KEY]: encode(ENCODING),
          [METADATA_ENCRYPTION_KEY_ID]: encode(this.defaultKeyId),
        },
        // Encrypt entire payload, preserving metadata
        data: await encrypt(
          temporal.api.common.v1.Payload.encode(payload).finish(),
          this.keys.get(this.defaultKeyId)!, // eslint-disable-line @typescript-eslint/no-non-null-assertion
        ),
      })),
    );
  }

async decode(payloads: Payload[]): Promise<Payload[]> {
    return Promise.all(
      payloads.map(async (payload) => {
        if (!payload.metadata || decode(payload.metadata[METADATA_ENCODING_KEY]) !== ENCODING) {
          return payload;
        }
        if (!payload.data) {
          throw new ValueError('Payload data is missing');
        }

const keyIdBytes = payload.metadata[METADATA_ENCRYPTION_KEY_ID];
        if (!keyIdBytes) {
          throw new ValueError('Unable to decrypt Payload without encryption key id');
        }

const keyId = decode(keyIdBytes);
        let key = this.keys.get(keyId);
        if (!key) {
          key = await fetchKey(keyId);
          this.keys.set(keyId, key);
        }
        const decryptedPayloadBytes = await decrypt(payload.data, key);
        console.log('Decrypting payload.data:', payload.data);
        return temporal.api.common.v1.Payload.decode(decryptedPayloadBytes);
      }),
    );
  }
}

async function fetchKey(_keyId: string): Promise<crypto.CryptoKey> {
  // In production, fetch key from a key management system (KMS). You may want to memoize requests if you'll be decoding
  // Payloads that were encrypted using keys other than defaultKeyId.
  const key = Buffer.from('test-key-test-key-test-key-test!');
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    key,
    {
      name: 'AES-GCM',
    },
    true,
    ['encrypt', 'decrypt'],
  );

return cryptoKey;
}
ts
const client = new Client({
  connection,
  dataConverter: await getDataConverter(),
});

const handle = await client.workflow.start(example, {
  args: ['Alice: Private message for Bob.'],
  taskQueue: 'encryption',
  workflowId: `my-business-id-${uuid()}`,
});

console.log(`Started workflow ${handle.workflowId}`);
console.log(await handle.result());
ts
const worker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  taskQueue: 'encryption',
  dataConverter: await getDataConverter(),
});
ts
export async function example(message: string): Promise<string> {
  return `${message}\nBob: Hi Alice, I'm Workflow Bob.`;
}
bash
brew install temporal
bash
brew install temporal
bash
temporal server start-dev
bash
temporal server start-dev --help
bash
npx @temporalio/create@latest ./your-app
bash
npm install @temporalio/client @temporalio/worker @temporalio/workflow @temporalio/activity @temporalio/common
ts

async function run() {
  const client = new Client();

await client.connection.close();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
ts

const { NODE_ENV = 'development' } = process.env;
const isDeployed = ['production', 'staging'].includes(NODE_ENV);

async function run() {
  const cert = await fs.readFile('./path-to/your.pem');
  const key = await fs.readFile('./path-to/your.key');

let connectionOptions = {};
  if (isDeployed) {
    connectionOptions = {
      address: 'your-namespace.tmprl.cloud:7233',
      tls: {
        clientCertPair: {
          crt: cert,
          key,
        },
      },
    };

const connection = await Connection.connect(connectionOptions);

const client = new Client({
      connection,
      namespace: 'your-namespace',
    });

await client.connection.close();
  }
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
typescript
type ExampleArgs = {
  name: string;
};

export async function example(
  args: ExampleArgs,
): Promise<{ greeting: string }> {
  const greeting = await greet(args.name);
  return { greeting };
}
typescript

...
await client.workflow.start(example, {
  args: [{ name: 'Temporal', born: 2019 }],
  taskQueue: 'your-queue',
  workflowId: 'business-meaningful-id',
});
ts
interface ExampleParam {
  name: string;
  born: number;
}
export async function example({ name, born }: ExampleParam): Promise<string> {
  return `Hello ${name}, you were born in ${born}.`;
}
typescript
interface ExampleParam {
  name: string;
  born: number;
}
export async function example({ name, born }: ExampleParam): Promise<string> {
  return `Hello ${name}, you were born in ${born}.`;
}
ts
export async function helloWorld(): Promise<string> {
  return '👋 Hello World!';
}
typescript

// this prints the *exact* same timestamp repeatedly
for (let x = 0; x < 10; ++x) {
  console.log(Date.now());
}

// this prints timestamps increasing roughly 1s each iteration
for (let x = 0; x < 10; ++x) {
  await sleep('1 second');
  console.log(Date.now());
}
ts
export async function greet(name: string): Promise<string> {
  return `👋 Hello, ${name}!`;
}
ts
export async function greet(name: string): Promise<string> {
  return `👋 Hello, ${name}!`;
}
typescript
export async function greet(name: string): Promise<string> {
  return `👋 Hello, ${name}!`;
}
ts

async function run() {
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    taskQueue: 'snippets',
    activities: {
      activityFoo: greet,
    },
  });

await worker.run();
}
ts
export interface DB {
  get(key: string): Promise<string>;
}

export const createActivities = (db: DB) => ({
  async greet(msg: string): Promise<string> {
    const name = await db.get('name'); // simulate read from db
    return `${msg}: ${name}`;
  },
  async greet_es(mensaje: string): Promise<string> {
    const name = await db.get('name'); // simulate read from db
    return `${mensaje}: ${name}`;
  },
});
ts

async function run() {
  // Mock DB connection initialization in Worker
  const db = {
    async get(_key: string) {
      return 'Temporal';
    },
  };

const worker = await Worker.create({
    taskQueue: 'dependency-injection',
    workflowsPath: require.resolve('./workflows'),
    activities: createActivities(db),
  });

await worker.run();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
ts

// Note usage of ReturnType<> generic since createActivities is a factory function
const { greet, greet_es } = proxyActivities<ReturnType<typeof createActivities>>({
  startToCloseTimeout: '30 seconds',
});
ts
export async function Workflow(name: string): Promise<string> {
  // destructuring multiple activities with the same options
  const { act1, act2, act3 } = proxyActivities<typeof activities>();
  /* activityOptions */
  await act1();
  await Promise.all([act2, act3]);
}
js
export async function DynamicWorkflow(activityName, ...args) {
  const acts = proxyActivities(/* activityOptions */);

// these are equivalent
  await acts.activity1();
  await acts['activity1']();

// dynamic reference to activities using activityName
  let result = await acts[activityName](...args);
}

ApplicationFailure: Activity function actC is not registered on this Worker, available activities: ["actA", "actB"]
typescript

// Only import the activity types, not the functions themselves

// Retrieve the Activity Handle by passing in the Activity types and options
const activityHandle = proxyActivities<typeof activities>({
  startToCloseTimeout: '1 minute',
});

// Deconstruct the individual Activity functions from the Activity Handle
const { greet } = activityHandle;

// A workflow that calls an activity
export async function example(name: string): Promise<string> {
  return await greet(name);
}
typescript
export async function DynamicWorkflow(activityName, ...args) {
  const acts = proxyActivities(/* activityOptions */);

// these are equivalent
  await acts.activity1();
  await acts['activity1']();

let result = await acts[activityName](...args);
  return result;
}
dockerfile
FROM node:20-bullseye

**Examples:**

Example 1 (unknown):
```unknown
---

## Versioning - Ruby SDK

Since Workflow Executions in Temporal can run for long periods — sometimes months or even years — it's common to need to make changes to a Workflow Definition, even while a particular Workflow Execution is in progress.

The Temporal Platform requires that Workflow code is [deterministic](/workflow-definition#deterministic-constraints).
If you make a change to your Workflow code that would cause non-deterministic behavior on Replay, you'll need to use one of our Versioning methods to gracefully update your running Workflows.
With Versioning, you can modify your Workflow Definition so that new executions use the updated code, while existing ones continue running the original version.
There are two primary Versioning methods that you can use:

- [Worker Versioning](/production-deployment/worker-deployments/worker-versioning). The Worker Versioning feature allows you to tag your Workers and programmatically roll them out in versioned deployments, so that old Workers can run old code paths and new Workers can run new code paths.
- [Versioning with Patching](#ruby-sdk-patching-api). This method works by adding branches to your code tied to specific revisions. It applies a code change to new Workflow Executions while avoiding disruptive changes to in-progress Workflow Executions.

## Worker Versioning

Temporal's [Worker Versioning](/production-deployment/worker-deployments/worker-versioning) feature allows you to tag your Workers and programmatically roll them out in Deployment Versions, so that old Workers can run old code paths and new Workers can run new code paths. This way, you can pin your Workflows to specific revisions, avoiding the need for patching.

## Versioning with Patching {#ruby-sdk-patching-api}

### Adding a patch

A Patch defines a logical branch in a Workflow for a specific change, similar to a feature flag.
It applies a code change to new Workflow Executions while avoiding disruptive changes to in-progress Workflow Executions.
When you want to make substantive code changes that may affect existing Workflow Executions, create a patch. Note that there's no need to patch [Pinned Workflows](/worker-versioning).

Suppose you have an initial Workflow that runs `PrePatchActivity`:
```

Example 2 (unknown):
```unknown
Now, you want to update your code to run `PostPatchActivity` instead. This represents your desired end state.
```

Example 3 (unknown):
```unknown
The problem is that you cannot deploy this new revision directly until you're certain there are no more running Workflows created using the `PrePatchActivity` code, otherwise you are likely to cause a nondeterminism error.
Instead, you'll need to use the [`patched`](https://ruby.temporal.io/Temporalio/Workflow.html#patched-class_method) function to check which version of the code should be executed.

Patching is a three-step process:

1. Patch in any new, updated code using the `patched()` function. Run the new patched code alongside old code.
2. Remove old code and use `deprecate_patch()` to mark a particular patch as deprecated.
3. Once there are no longer any open Worklow Executions of the previous version of the code, remove `deprecatePatch()`.
   Let's walk through this process in sequence.

### Patching in new code

Using `patched` inserts a marker into the Workflow History.
During Replay, if a Worker encounters a history with that marker, it will fail the Workflow task when the Workflow code doesn't produce the same patch marker (in this case `my-patch`).
This ensures you can safely deploy new code paths alongside the original branch.
```

Example 4 (unknown):
```unknown
### Deprecating patches {#deprecated-patches}

After ensuring that all Workflows started with `v1` code have left retention, you can [deprecate the patch](https://ruby.temporal.io/Temporalio/Workflow.html#deprecate_patch-class_method).

Once your Workflows are no longer running the pre-patch code paths, you can deploy your code with `deprecate_patch()`.
These Workers will be running the most up-to-date version of the Workflow code, which no longer requires the patch.
The `deprecate_patch()` function works similarly to the `patched()` function by recording a marker in the Workflow history.
This marker does not fail replay when Workflow code does not emit it.
Deprecated patches serve as a bridge between the pre-patch code paths and the post-patch code paths, and are useful for avoiding errors resulting from patched code paths in your Workflow history.
```

---

## Terminate

**URL:** llms-txt#terminate

**Contents:**
- Reset a Workflow Execution {#reset}
- Workflow message passing - Ruby SDK
- Write message handlers {#writing-message-handlers}
  - Query handlers {#queries}
  - Signal handlers {#signals}
  - Update handlers and validators {#updates}
- Send messages {#send-messages}
  - Send a Query {#send-query}
  - Send a Signal {#send-signal}

handle.terminate
bash
temporal workflow reset \
    --workflow-id <workflow-id> \
    --event-id <event-id> \
    --reason "Reason for reset"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code" \
    --namespace my-namespace \
    --tls-cert-path /path/to/cert.pem \
    --tls-key-path /path/to/key.pem
ruby
class GreetingWorkflow < Temporalio::Workflow::Definition
  # ...

workflow_query
  def languages(input)
    # A query handler returns a value: it can inspect but must not mutate the Workflow state.
    if input['include_unsupported']
      CallGreetingService.greetings.keys.sort
    else
      @greetings.keys.sort
    end
  end

# ...
end
ruby
class GreetingWorkflow < Temporalio::Workflow::Definition
  # This is the equivalent of:
  #    workflow_query
  #    def language
  #      @language
  #    end
  workflow_query_attr_reader :language

# ...
end
ruby
class GreetingWorkflow < Temporalio::Workflow::Definition
  # ...

workflow_signal
  def approve(input)
    # A signal handler mutates the workflow state but cannot return a value.
    @approved_for_release = true
    @approver_name = input['name']
  end

# ...
end
ruby
class GreetingWorkflow < Temporalio::Workflow::Definition
  # ...

workflow_update
  def set_language(new_language) # rubocop:disable Naming/AccessorMethodName
    # An update handler can mutate the workflow state and return a value.
    prev = @language.to_sym
    @language = new_language.to_sym
    prev
  end

workflow_update_validator(:set_language)
  def validate_set_language(new_language)
    # In an update validator you raise any exception to reject the update.
    raise "#{new_language} is not supported" unless @greetings.include?(new_language.to_sym)
  end

# ...
end
ruby
client = Temporalio::Client.connect('localhost:7233', 'default')
handle = client.start_workflow(
  MessagePassingSimple::GreetingWorkflow,
  id: 'message-passing-simple-sample-workflow-id',
  task_queue: 'message-passing-simple-sample'
)
ruby
supported_languages = handle.query(MessagePassingSimple::GreetingWorkflow.languages, { include_unsupported: false })
ruby
handle.signal(MessagePassingSimple::GreetingWorkflow.approve, { name: 'John Q. Approver' })
ruby
class WorkflowB < Temporalio::Workflow::Definition
  def execute
    handle = Temporalio::Workflow.external_workflow_handle('workflow-a-id')
    handle.signal(WorkflowA.some_signal, 'some signal arg')
  end
end
ruby
client = Temporalio::Client.connect('localhost:7233', 'default')

**Examples:**

Example 1 (unknown):
```unknown
Workflow Executions can also be Terminated directly from the WebUI. In this case, a custom note can be logged from the
UI when that happens.

## Reset a Workflow Execution {#reset}

Resetting a Workflow Execution terminates the current Workflow Execution and starts a new Workflow Execution from a
point you specify in its Event History. Use reset when a Workflow is blocked due to a non-deterministic error or other
issues that prevent it from completing.

When you reset a Workflow, the Event History up to the reset point is copied to the new Workflow Execution, and the
Workflow resumes from that point with the current code. Reset only works if you've fixed the underlying issue, such as
removing non-deterministic code. Any progress made after the reset point will be discarded. Provide a reason when
resetting, as it will be recorded in the Event History.

<Tabs>

<TabItem value="web-ui" label="Web UI">

1. Navigate to the Workflow Execution details page,
2. Click the **Reset** button in the top right dropdown menu,
3. Select the Event ID to reset to,
4. Provide a reason for the reset,
5. Confirm the reset.

The Web UI shows available reset points and creates a link to the new Workflow Execution after the reset completes.

</TabItem>

<TabItem value="cli" label="Temporal CLI">

Use the `temporal workflow reset` command to reset a Workflow Execution:
```

Example 2 (unknown):
```unknown
For example:
```

Example 3 (unknown):
```unknown
By default, the command resets the latest Workflow Execution in the `default` Namespace. Use `--run-id` to reset a
specific run. Use `--namespace` to specify a different Namespace:
```

Example 4 (unknown):
```unknown
Monitor the new Workflow Execution after resetting to ensure it completes successfully.

</TabItem>

</Tabs>

---

## Workflow message passing - Ruby SDK

A Workflow can act like a stateful service that receives messages: Queries, Signals, and Updates.
These messages interact with the Workflow via handler methods defined in the Workflow code.
Clients use messages to read Workflow state or change its behavior.

See [Workflow message passing](/encyclopedia/workflow-message-passing) for a general overview.

## Write message handlers {#writing-message-handlers}

:::info
The code that follows is part of a [working solution](https://github.com/temporalio/samples-ruby/tree/main/message_passing_simple).
:::

Follow these guidelines when writing your message handlers:

- Message handlers are defined as methods on the Workflow class, decorated by calling one of three class methods before defining the handler method: `workflow_query`, `workflow_signal`, and `workflow_update`.
- These also implicitly create class-methods with the same name as the instance methods for use by callers.
- The parameters and return values of handlers and the main Workflow function must be [serializable](/dataconversion).
- Prefer single hash/object input parameter to multiple input parameters.
  Hash/object parameters allow you to add fields without changing the calling signature.

### Query handlers {#queries}

A [Query](/sending-messages#sending-queries) is a synchronous operation that retrieves state from a Workflow Execution.
Define as a method:
```

---

## Elasticsearch

**URL:** llms-txt#elasticsearch

: "${ENABLE_ES:=false}"
: "${ES_SCHEME:=http}"
: "${ES_SEEDS:=}"
: "${ES_PORT:=9200}"
: "${ES_USER:=}"
: "${ES_PWD:=}"
: "${ES_VERSION:=v7}"
: "${ES_VIS_INDEX:=temporal_visibility_v1_dev}"
: "${ES_SEC_VIS_INDEX:=temporal_visibility_v1_new}"
: "${ES_SCHEMA_SETUP_TIMEOUT_IN_SECONDS:=0}"

---

## HELP temporal_cloud_v1_frontend_service_pending_requests The number of pollers that are waiting for a task

**URL:** llms-txt#help-temporal_cloud_v1_frontend_service_pending_requests-the-number-of-pollers-that-are-waiting-for-a-task

---

## Start a workflow with static summary and details

**URL:** llms-txt#start-a-workflow-with-static-summary-and-details

handle = client.start_workflow(
  'YourWorkflow',
  'workflow input',
  id: 'your-workflow-id',
  task_queue: 'your-task-queue',
  static_summary: 'Order processing for customer #12345',
  static_details: 'Processing premium order with expedited shipping'
)
ruby

**Examples:**

Example 1 (unknown):
```unknown
`static_summary:` is a single-line description that appears in the Workflow list view, limited to 200 bytes.
`static_details:` can be multi-line and provides more comprehensive information that appears in the Workflow details view, with a larger limit of 20K bytes.

The input format is standard Markdown excluding images, HTML, and scripts.

You can also use `execute_workflow` for synchronous execution:
```

---

## Install the Temporal Python SDK dependency

**URL:** llms-txt#install-the-temporal-python-sdk-dependency

RUN pip install --no-cache-dir temporalio

---

## Wait for them all to complete

**URL:** llms-txt#wait-for-them-all-to-complete

Temporalio::Workflow::Future.all_of(fut1, fut2, fut3).wait

Temporalio::Workflow.logger.info("Got: #{fut1.result}, #{fut2.result}, #{fut3.result}")
ruby

**Examples:**

Example 1 (unknown):
```unknown
Or, say, to wait on the first of 5 activities or a timeout to complete:
```

---

## Sleep for 72 hours

**URL:** llms-txt#sleep-for-72-hours

**Contents:**
- Enriching the User Interface - Ruby SDK
- Adding Summary and Details to Workflows
  - Starting a Workflow

Temporalio::Workflow.sleep(72 * 60 * 60, summary: 'my timer')
ruby
require 'temporalio/client'

**Examples:**

Example 1 (unknown):
```unknown
There is also a `Temporalio::Workflow.timeout` method that accepts a block and works like standard Ruby
`Timeout.timeout` if needing the ability to timeout a set of code.

---

## Enriching the User Interface - Ruby SDK

Temporal supports adding context to Workflows and Events with metadata. 
This helps users identify and understand Workflows and their operations.

## Adding Summary and Details to Workflows

### Starting a Workflow

When starting a Workflow, you can provide a static summary and details to help identify the Workflow in the UI:
```

---

## Predefined search attribute key, usually a global somewhere

**URL:** llms-txt#predefined-search-attribute-key,-usually-a-global-somewhere

MY_KEYWORD_KEY = Temporalio::SearchAttributes::Key.new(
  'my-keyword',
  Temporalio::SearchAttributes::IndexedValueType::KEYWORD
)

---

## Create a new runtime that has telemetry enabled. Create this first to avoid

**URL:** llms-txt#create-a-new-runtime-that-has-telemetry-enabled.-create-this-first-to-avoid

---

## set up MySQL schema

**URL:** llms-txt#set-up-mysql-schema

setup_mysql_schema() {
    #...
    # use valid schema for the version of the database you want to set up for Visibility
    VISIBILITY_SCHEMA_DIR=${TEMPORAL_HOME}/schema/mysql/${MYSQL_VERSION_DIR}/visibility/versioned
    if [[ ${SKIP_DB_CREATE} != true ]]; then
        temporal-sql-tool --ep "${MYSQL_SEEDS}" -u "${MYSQL_USER}" -p "${DB_PORT}" "${MYSQL_CONNECT_ATTR[@]}" --db "${VISIBILITY_DBNAME}" create
    fi
    temporal-sql-tool --ep "${MYSQL_SEEDS}" -u "${MYSQL_USER}" -p "${DB_PORT}" "${MYSQL_CONNECT_ATTR[@]}" --db "${VISIBILITY_DBNAME}" setup-schema -v 0.0
    temporal-sql-tool --ep "${MYSQL_SEEDS}" -u "${MYSQL_USER}" -p "${DB_PORT}" "${MYSQL_CONNECT_ATTR[@]}" --db "${VISIBILITY_DBNAME}" update-schema -d "${VISIBILITY_SCHEMA_DIR}"
#...
}
bash
#...

**Examples:**

Example 1 (unknown):
```unknown
For Elasticsearch as both primary and secondary Visibility store configuration in the previous example, an example setup script would be as follows.
```

---

## TYPE temporal_cloud_v1_frontend_service_error_count gauge

**URL:** llms-txt#type-temporal_cloud_v1_frontend_service_error_count-gauge

---

## Create start-workflow operation for use with update-with-start

**URL:** llms-txt#create-start-workflow-operation-for-use-with-update-with-start

start_workflow_operation = Temporalio::Client::WithStartWorkflowOperation.new(
  MyWorkflow, 'my-workflow-input',
  id: 'my-workflow-id', task_queue: 'my-workflow-task-queue',
  id_conflict_policy: Temporalio::WorkflowIDConflictPolicy::USE_EXISTING
)

---

## Wait for ES to start

**URL:** llms-txt#wait-for-es-to-start

---

## Start workflow with the search attribute set

**URL:** llms-txt#start-workflow-with-the-search-attribute-set

**Contents:**
  - Upsert Search Attributes {#upsert-search-attributes}

handle = my_client.start_workflow(
  MyWorkflow, 'some-input',
  id: 'my-workflow-id', task_queue: 'my-task-queue',
  search_attributes: Temporalio::SearchAttributes.new({ MY_KEYWORD_KEY => 'some-value' })
)
ruby

**Examples:**

Example 1 (unknown):
```unknown
### Upsert Search Attributes {#upsert-search-attributes}

You can upsert Search Attributes to add, update, or remove Search Attributes from within Workflow code.

To upsert custom Search Attributes, use the [`upsert_search_attributes`](https://ruby.temporal.io/Temporalio/Workflow.html#upsert_search_attributes-class_method) method with a set of updates.
Keys should be predefined for reuse.
```

---

## Allow async methods to not have await in them

**URL:** llms-txt#allow-async-methods-to-not-have-await-in-them

dotnet_diagnostic.CS1998.severity = none

---

## Custom gRPC headers

**URL:** llms-txt#custom-grpc-headers

[profile.default.grpc_meta]
my-custom-header = "development-value"
trace-id = "dev-trace-123"

---

## Start a timer

**URL:** llms-txt#start-a-timer

sleep_fut = Temporalio::Workflow::Future.new { Temporalio::Workflow.sleep(30) }

---

## Optional gRPC metadata for observability or routing

**URL:** llms-txt#optional-grpc-metadata-for-observability-or-routing

**Contents:**
- Load configuration profile and environment variables
- Load configuration from a custom path
- Asynchronous Activity completion - Go SDK
- Benign exceptions - Go SDK
- Interrupt a Workflow - Go SDK
- Handle Cancellation in Workflow {#handle-cancellation-in-workflow}
- Handle Cancellation in an Activity {#handle-cancellation-in-an-activity}
- Request Cancellation {#request-cancellation}
- Heartbeating after a Cancellation
- Reset a Workflow Execution {#reset}

temporal --profile prod config set --prop grpc_meta.environment --value "production"
temporal --profile prod config set --prop grpc_meta.service-version --value "v1.2.3"
python {7-8}

from temporalio.client import Client
from temporalio.envconfig import ClientConfigProfile

async def main():
    # Load the "default" profile from default locations and environment variables.
    default_profile = ClientConfigProfile.load()
    connect_config = default_profile.to_client_connect_config()

# Connect to the client using the loaded configuration.
    client = await Client.connect(**connect_config)
    print(f"✅ Client connected to {client.service_client.config.target_host} in namespace '{client.namespace}'")

if __name__ == "__main__":
		asyncio.run(main())
go {13}
package main

"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/contrib/envconfig"
)

func main() {
	// Loads the "default" profile from the standard location and environment variables.
	c, err := client.Dial(envconfig.MustLoadDefaultClientOptions())
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer c.Close()

fmt.Printf("✅ Connected to Temporal Service")
}
Ruby {16-18}
require 'temporalio/client'
require 'temporalio/env_config'

def main
  puts '--- Loading default profile from config.toml ---'

# For this sample to be self-contained, we explicitly provide the path to
  # the config.toml file included in this directory.
  # By default though, the config.toml file will be loaded from
  # ~/.config/temporalio/temporal.toml (or the equivalent standard config directory on your OS).
  config_file = File.join(__dir__, 'config.toml')

# load_client_connect_options is a helper that loads a profile and prepares
  # the configuration for Client.connect. By default, it loads the
  # "default" profile.
  args, kwargs = Temporalio::EnvConfig::ClientConfig.load_client_connect_options(
    config_source: Pathname.new(config_file)
  )

puts "Loaded 'default' profile from #{config_file}."
  puts "  Address: #{args[0]}"
  puts "  Namespace: #{args[1]}"
  puts "  gRPC Metadata: #{kwargs[:rpc_metadata]}"

puts "\nAttempting to connect to client..."
  begin
    client = Temporalio::Client.connect(*args, **kwargs)
    puts '✅ Client connected successfully!'
    sys_info = client.workflow_service.get_system_info(Temporalio::Api::WorkflowService::V1::GetSystemInfoRequest.new)
    puts "✅ Successfully verified connection to Temporal server!\n#{sys_info}"
  rescue StandardError => e
    puts "❌ Failed to connect: #{e}"
  end
end
csharp {22,27-30}
using Temporalio.Client;
using Temporalio.Client.EnvConfig;

namespace TemporalioSamples.EnvConfig;

/// <summary>
/// Sample demonstrating loading the default environment configuration profile
/// from a TOML file.
/// </summary>
public static class LoadFromFile
{
    public static async Task RunAsync()
    {
        Console.WriteLine("--- Loading default profile from config.toml ---");

try
        {
            // For this sample to be self-contained, we explicitly provide the path to
            // the config.toml file included in this directory.
            // By default though, the config.toml file will be loaded from
            // ~/.config/temporalio/temporal.toml (or the equivalent standard config directory on your OS).
            var configFile = Path.Combine(Directory.GetCurrentDirectory(), "config.toml");

// LoadClientConnectOptions is a helper that loads a profile and prepares
            // the config for TemporalClient.ConnectAsync. By default, it loads the
            // "default" profile.
            var connectOptions = ClientEnvConfig.LoadClientConnectOptions(new ClientEnvConfig.ProfileLoadOptions
            {
                ConfigSource = DataSource.FromPath(configFile),
            });

Console.WriteLine($"Loaded 'default' profile from {configFile}.");
            Console.WriteLine($"  Address: {connectOptions.TargetHost}");
            Console.WriteLine($"  Namespace: {connectOptions.Namespace}");
            if (connectOptions.RpcMetadata?.Count > 0)
            {
                Console.WriteLine($"  gRPC Metadata: {string.Join(", ", connectOptions.RpcMetadata.Select(kv => $"{kv.Key}={kv.Value}"))}");
            }

Console.WriteLine("\nAttempting to connect to client...");

var client = await TemporalClient.ConnectAsync(connectOptions);
            Console.WriteLine("✅ Client connected successfully!");

// Test the connection by checking the service
            var sysInfo = await client.Connection.WorkflowService.GetSystemInfoAsync(new());
            Console.WriteLine("✅ Successfully verified connection to Temporal server!\n{0}", sysInfo);
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            Console.WriteLine($"❌ Failed to connect: {ex.Message}");
        }
    }
}
ts {17-19,28-29}

async function main() {
  console.log('--- Loading default profile from config.toml ---');

// For this sample to be self-contained, we explicitly provide the path to
  // the config.toml file included in this directory.
  // By default though, the config.toml file will be loaded from
  // ~/.config/temporalio/temporal.toml (or the equivalent standard config directory on your OS).
  const configFile = resolve(__dirname, '../config.toml');

// loadClientConnectConfig is a helper that loads a profile and prepares
  // the configuration for Connection.connect and Client. By default, it loads the
  // "default" profile.
  const config = loadClientConnectConfig({
    configSource: { path: configFile },
  });

console.log(`Loaded 'default' profile from ${configFile}.`);
  console.log(`  Address: ${config.connectionOptions.address}`);
  console.log(`  Namespace: ${config.namespace}`);
  console.log(`  gRPC Metadata: ${JSON.stringify(config.connectionOptions.metadata)}`);

console.log('\nAttempting to connect to client...');
  try {
    const connection = await Connection.connect(config.connectionOptions);
    const client = new Client({ connection, namespace: config.namespace });
    console.log('✅ Client connected successfully!');
    await connection.close();
  } catch (err) {
    console.log(`❌ Failed to connect: ${err}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
java

public class LoadFromFile {

private static final Logger logger = LoggerFactory.getLogger(LoadFromFile.class);

public static void main(String[] args) {
    try {

ClientConfigProfile profile = ClientConfigProfile.load(LoadClientConfigProfileOptions.newBuilder().build());

WorkflowServiceStubsOptions serviceStubsOptions = profile.toWorkflowServiceStubsOptions();
      WorkflowClientOptions clientOptions = profile.toWorkflowClientOptions();

try {
        // Create the workflow client using the loaded configuration
        WorkflowClient client =
            WorkflowClient.newInstance(
                WorkflowServiceStubs.newServiceStubs(serviceStubsOptions), clientOptions);

// Test the connection by getting system info
        var systemInfo =
            client
                .getWorkflowServiceStubs()
                .blockingStub()
                .getSystemInfo(
                    io.temporal.api.workflowservice.v1.GetSystemInfoRequest.getDefaultInstance());

logger.info("✅ Client connected successfully!");
        logger.info("   Server version: {}", systemInfo.getServerVersion());

} catch (Exception e) {
        logger.error("❌ Failed to connect: {}", e.getMessage());
      }

} catch (Exception e) {
      logger.error("Failed to load configuration: {}", e.getMessage(), e);
      System.exit(1);
    }
  }
}
py {12-13,21-23}

from pathlib import Path
from temporalio.client import Client
from temporalio.envconfig import ClientConfig

async def main():
    """
    Demonstrates loading a named profile and overriding values programmatically.
    """
    print("--- Loading 'staging' profile with programmatic overrides ---")

config_file = Path(__file__).parent / "config.toml"
    profile_name = "staging"

print(
        "The 'staging' profile in config.toml has an incorrect address (localhost:9999)."
    )
    print("We'll programmatically override it to the correct address.")

# Load the 'staging' profile.
    connect_config = ClientConfig.load_client_connect_config(
        profile=profile_name,
        config_file=str(config_file),
    )

# Override the target host to the correct address.
    # This is the recommended way to override configuration values.
    connect_config["target_host"] = "localhost:7233"

print(f"\nLoaded '{profile_name}' profile from {config_file} with overrides.")
    print(
        f"  Address: {connect_config.get('target_host')} (overridden from localhost:9999)"
    )
    print(f"  Namespace: {connect_config.get('namespace')}")

print("\nAttempting to connect to client...")
    try:
        await Client.connect(**connect_config)  # type: ignore
        print("✅ Client connected successfully!")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(main())
go {14-16}
package main

"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/contrib/envconfig"
)

func main() {
  // Load a specific profile from the TOML config file.
  // This requires a [profile.prod] section in your config.
  opts, err := envconfig.LoadClientOptions(envconfig.LoadClientOptionsRequest{
    ConfigFileProfile: "prod",
    ConfigFilePath:    "/Users/yourname/.config/my-app/temporal.toml",
  })
  if err != nil {
    log.Fatalf("Failed to load 'prod' profile: %v", err)
  }

// Programmatically override the Namespace value.
  opts.Namespace = "new-namespace"

c, err := client.Dial(opts)
  if err != nil {
    log.Fatalf("Failed to connect using 'prod' profile: %v", err)
  }
  defer c.Close()

fmt.Printf("✅ Connected to Temporal namespace %q on %s using 'prod' profile\n", c.Options().Namespace, c.Options().HostPort)
}
Ruby {7-8,14-16}
require 'temporalio/client'
require 'temporalio/env_config'

def main
  puts "--- Loading 'staging' profile with programmatic overrides ---"

config_file = File.join(__dir__, 'config.toml')
  profile_name = 'staging'

puts "The 'staging' profile in config.toml has an incorrect address (localhost:9999)."
  puts "We'll programmatically override it to the correct address."

# Load the 'staging' profile.
  args, kwargs = Temporalio::EnvConfig::ClientConfig.load_client_connect_options(
    profile: profile_name,
    config_source: Pathname.new(config_file)
  )

# Override the target host to the correct address.
  # This is the recommended way to override configuration values.
  args[0] = 'localhost:7233'

puts "\nLoaded '#{profile_name}' profile from #{config_file} with overrides."
  puts "  Address: #{args[0]} (overridden from localhost:9999)"
  puts "  Namespace: #{args[1]}"

puts "\nAttempting to connect to client..."
  begin
    client = Temporalio::Client.connect(*args, **kwargs)
    puts '✅ Client connected successfully!'
    sys_info = client.workflow_service.get_system_info(Temporalio::Api::WorkflowService::V1::GetSystemInfoRequest.new)
    puts "✅ Successfully verified connection to Temporal server!\n#{sys_info}"
  rescue StandardError => e
    puts "❌ Failed to connect: #{e}"
  end
end

main if $PROGRAM_NAME == __FILE__
csharp {18-19,25-28}
using Temporalio.Client;
using Temporalio.Client.EnvConfig;

namespace TemporalioSamples.EnvConfig;

/// <summary>
/// Sample demonstrating loading a named environment configuration profile and
/// programmatically overriding its values.
/// </summary>
public static class LoadProfile
{
    public static async Task RunAsync()
    {
        Console.WriteLine("--- Loading 'staging' profile with programmatic overrides ---");

try
        {
            var configFile = Path.Combine(Directory.GetCurrentDirectory(), "config.toml");
            var profileName = "staging";

Console.WriteLine("The 'staging' profile in config.toml has an incorrect address (localhost:9999).");
            Console.WriteLine("We'll programmatically override it to the correct address.");

// Load the 'staging' profile
            var connectOptions = ClientEnvConfig.LoadClientConnectOptions(new ClientEnvConfig.ProfileLoadOptions
            {
                Profile = profileName,
                ConfigSource = DataSource.FromPath(configFile),
            });

// Override the target host to the correct address.
            // This is the recommended way to override configuration values.
            connectOptions.TargetHost = "localhost:7233";

Console.WriteLine($"\nLoaded '{profileName}' profile from {configFile} with overrides.");
            Console.WriteLine($"  Address: {connectOptions.TargetHost} (overridden from localhost:9999)");
            Console.WriteLine($"  Namespace: {connectOptions.Namespace}");

Console.WriteLine("\nAttempting to connect to client...");

var client = await TemporalClient.ConnectAsync(connectOptions);
            Console.WriteLine("✅ Client connected successfully!");

// Test the connection by checking the service
            var sysInfo = await client.Connection.WorkflowService.GetSystemInfoAsync(new());
            Console.WriteLine("✅ Successfully verified connection to Temporal server!\n{0}", sysInfo);
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            Console.WriteLine($"❌ Failed to connect: {ex.Message}");
        }
    }
}
ts {17-19,28-29}

async function main() {
  console.log('--- Loading default profile from config.toml ---');

// For this sample to be self-contained, we explicitly provide the path to
  // the config.toml file included in this directory.
  // By default though, the config.toml file will be loaded from
  // ~/.config/temporalio/temporal.toml (or the equivalent standard config directory on your OS).
  const configFile = resolve(__dirname, '../config.toml');

// loadClientConnectConfig is a helper that loads a profile and prepares
  // the configuration for Connection.connect and Client. By default, it loads the
  // "default" profile.
  const config = loadClientConnectConfig({
    configSource: { path: configFile },
  });

console.log(`Loaded 'default' profile from ${configFile}.`);
  console.log(`  Address: ${config.connectionOptions.address}`);
  console.log(`  Namespace: ${config.namespace}`);
  console.log(`  gRPC Metadata: ${JSON.stringify(config.connectionOptions.metadata)}`);

console.log('\nAttempting to connect to client...');
  try {
    const connection = await Connection.connect(config.connectionOptions);
    const client = new Client({ connection, namespace: config.namespace });
    console.log('✅ Client connected successfully!');
    await connection.close();
  } catch (err) {
    console.log(`❌ Failed to connect: ${err}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
java {21-25}

public class LoadFromFile {

private static final Logger logger = LoggerFactory.getLogger(LoadFromFile.class);

public static void main(String[] args) {
    try {

String configFilePath =
          Paths.get(LoadFromFile.class.getResource("/config.toml").toURI()).toString();

ClientConfigProfile profile =
          ClientConfigProfile.load(
              LoadClientConfigProfileOptions.newBuilder()
                  .setConfigFilePath(configFilePath)
                  .build());

WorkflowServiceStubsOptions serviceStubsOptions = profile.toWorkflowServiceStubsOptions();
      WorkflowClientOptions clientOptions = profile.toWorkflowClientOptions();

try {
        // Create the workflow client using the loaded configuration
        WorkflowClient client =
            WorkflowClient.newInstance(
                WorkflowServiceStubs.newServiceStubs(serviceStubsOptions), clientOptions);

// Test the connection by getting system info
        var systemInfo =
            client
                .getWorkflowServiceStubs()
                .blockingStub()
                .getSystemInfo(
                    io.temporal.api.workflowservice.v1.GetSystemInfoRequest.getDefaultInstance());

logger.info("✅ Client connected successfully!");
        logger.info("   Server version: {}", systemInfo.getServerVersion());

} catch (Exception e) {
        logger.error("❌ Failed to connect: {}", e.getMessage());
      }

} catch (Exception e) {
      logger.error("Failed to load configuration: {}", e.getMessage(), e);
      System.exit(1);
    }
  }
}
go
// Retrieve the Activity information needed to asynchronously complete the Activity.
activityInfo := activity.GetInfo(ctx)
taskToken := activityInfo.TaskToken
// Send the taskToken to the external service that will complete the Activity.
go
return "", activity.ErrResultPending
go
// Instantiate a Temporal service client.
// The same client can be used to complete or fail any number of Activities.
// The client is a heavyweight object that should be created once per process.
temporalClient, err := client.Dial(client.Options{})

// Complete the Activity.
temporalClient.CompleteActivity(context.Background(), taskToken, result, nil)
go
// Fail the Activity.
client.CompleteActivity(context.Background(), taskToken, nil, err)
go

"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/temporal"
)

func MyActivity(ctx context.Context) (string, error) {
	result, err := callExternalService()
	if err != nil {
		// Mark this error as benign since it's expected
		return "", temporal.NewApplicationErrorWithOptions(
			err.Error(),
			"",
			temporal.ApplicationErrorOptions{
				Category: temporal.ApplicationErrorCategoryBenign,
			},
		)
	}
	return result, nil
}
go
// ...
// YourWorkflow is a Workflow Definition that shows how it can be canceled.
func YourWorkflow(ctx workflow.Context) error {
// ...
	activityOptions := workflow.ActivityOptions{
// ...
		HeartbeatTimeout:    5 * time.Second,
		// Set WaitForCancellation to true to have the Workflow wait to return
		// until all in progress Activities have completed, failed, or accepted the Cancellation.
		WaitForCancellation: true,
	}
	defer func() {
		// This logic ensures cleanup only happens if there is a Cancelation error
		if !errors.Is(ctx.Err(), workflow.ErrCanceled) {
			return
		}
		// For the Workflow to execute an Activity after it receives a Cancellation Request
		// It has to get a new disconnected context
		newCtx, _ := workflow.NewDisconnectedContext(ctx)
		// This Activity is only executed if
		err := workflow.ExecuteActivity(newCtx, a.CleanupActivity).Get(ctx, nil)
		if err != nil {
			logger.Error("CleanupActivity failed", "Error", err)
		}
	}()
// ...
	err := workflow.ExecuteActivity(ctx, a.ActivityToBeCanceled).Get(ctx, &result)
// ...
	// This call to execute the Activity is expected to return an error "canceled".
	// And the Activity Execution is skipped.
	err = workflow.ExecuteActivity(ctx, a.ActivityToBeSkipped).Get(ctx, nil)
// ...
	// Return any errors.
	// If a CanceledError is returned, the Workflow changes to a Canceled state.
	return err
}
go
// ActivityToBeCanceled is the Activity that will respond to the Cancellation Request
func (a *Activities) ActivityToBeCanceled(ctx context.Context) (string, error) {
// ...
	// A for select statement is a common approach to listening for a Cancellation is an Activity
	for {
		select {
		case <-time.After(1 * time.Second):
			logger.Info("Heartbeating...")
			activity.RecordHeartbeat(ctx, "")
		// Listen for ctx.Done() to know if a Cancellation Request has propagated to the Activity.
		case <-ctx.Done():
			logger.Info("This Activity is canceled!")
			return "I am canceled by Done", nil
		}
	}
}
// ...
go
func main() {
// ...
	// Call the CancelWorkflow API to cancel a Workflow
	// In this call we are relying on the Workflow Id only.
	// But a Run Id can also be supplied to ensure the correct Workflow is Canceled.
	err = temporalClient.CancelWorkflow(context.Background(), cancellation.WorkflowId, "")
	if err != nil {
		log.Fatalln("Unable to cancel Workflow Execution", err)
	}
// ...
}
bash
temporal workflow reset \
    --workflow-id <workflow-id> \
    --event-id <event-id> \
    --reason "Reason for reset"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code"
bash
temporal workflow reset \
    --workflow-id my-background-check \
    --event-id 4 \
    --reason "Fixed non-deterministic code" \
    --namespace my-namespace \
    --tls-cert-path /path/to/cert.pem \
    --tls-key-path /path/to/key.pem
go
func YourWorkflowDefinition(ctx workflow.Context, params ParentParams) (ParentResp, error) {

childWorkflowOptions := workflow.ChildWorkflowOptions{}
  ctx = workflow.WithChildOptions(ctx, childWorkflowOptions)

var result ChildResp
  err := workflow.ExecuteChildWorkflow(ctx, YourOtherWorkflowDefinition, ChildParams{}).Get(ctx, &result)
  if err != nil {
    // ...
  }
  // ...
  return resp, nil
}

func YourOtherWorkflowDefinition(ctx workflow.Context, params ChildParams) (ChildResp, error) {
  // ...
  return resp, nil
}
go

// ...
  "go.temporal.io/api/enums/v1"
)

func YourWorkflowDefinition(ctx workflow.Context, params ParentParams) (ParentResp, error) {

childWorkflowOptions := workflow.ChildWorkflowOptions{
    ParentClosePolicy: enums.PARENT_CLOSE_POLICY_ABANDON,
  }
  ctx = workflow.WithChildOptions(ctx, childWorkflowOptions)

childWorkflowFuture := workflow.ExecuteChildWorkflow(ctx, YourOtherWorkflowDefinition, ChildParams{})
  // Wait for the Child Workflow Execution to spawn
  var childWE workflow.Execution
  if err := childWorkflowFuture.GetChildWorkflowExecution().Get(ctx, &childWE); err != nil {
     return err
  }
  // ...
  return resp, nil
}

func YourOtherWorkflowDefinition(ctx workflow.Context, params ChildParams) (ChildResp, error) {
  // ...
  return resp, nil
}
go

// ...
  "go.temporal.io/api/enums/v1"
)

func YourWorkflowDefinition(ctx workflow.Context, params ParentParams) (ParentResp, error) {
  // ...
  childWorkflowOptions := workflow.ChildWorkflowOptions{
    // ...
    ParentClosePolicy: enums.PARENT_CLOSE_POLICY_ABANDON,
  }
  ctx = workflow.WithChildOptions(ctx, childWorkflowOptions)
  childWorkflowFuture := workflow.ExecuteChildWorkflow(ctx, YourOtherWorkflowDefinition, ChildParams{})
  // ...
}

func YourOtherWorkflowDefinition(ctx workflow.Context, params ChildParams) (ChildResp, error) {
  // ...
  return resp, nil
}
go
ClusterManagerInput struct {
    State             *ClusterManagerState
    TestContinueAsNew bool
}

func newClusterManager(ctx workflow.Context, wfInput ClusterManagerInput) (*ClusterManager, error) {

go
return ClusterManagerResult{}, workflow.NewContinueAsNewError(
    ctx,
    ClusterManagerWorkflow,
    ClusterManagerInput{
        State:             &cm.state,
        TestContinueAsNew: cm.testContinueAsNew,
    },
)
go
func (cm *ClusterManager) shouldContinueAsNew(ctx workflow.Context) bool {
	if workflow.GetInfo(ctx).GetContinueAsNewSuggested() {
		return true
	}
	if cm.maxHistoryLength > 0 && workflow.GetInfo(ctx).GetCurrentHistoryLength() > cm.maxHistoryLength {
		return true
	}
	return false
}
go
// Create an instance of Data Converter with your codec.
var DataConverter = converter.NewCodecDataConverter(
	converter.GetDefaultDataConverter(),
	NewPayloadCodec(),
)
//...
// Create an instance of PaylodCodec.
func NewPayloadCodec() converter.PayloadCodec {
	return &Codec{}
}
go
// Codec implements converter.PayloadEncoder for snappy compression.
type Codec struct{}

// Encode implements converter.PayloadCodec.Encode.
func (Codec) Encode(payloads []*commonpb.Payload) ([]*commonpb.Payload, error) {
	result := make([]*commonpb.Payload, len(payloads))
	for i, p := range payloads {
		// Marshal proto
		origBytes, err := p.Marshal()
		if err != nil {
			return payloads, err
		}
		// Compress
		b := snappy.Encode(nil, origBytes)
		result[i] = &commonpb.Payload{
			Metadata: map[string][]byte{converter.MetadataEncoding: []byte("binary/snappy")},
			Data:     b,
		}
	}

// Decode implements converter.PayloadCodec.Decode.
func (Codec) Decode(payloads []*commonpb.Payload) ([]*commonpb.Payload, error) {
	result := make([]*commonpb.Payload, len(payloads))
	for i, p := range payloads {
		// Decode only if it's our encoding
		if string(p.Metadata[converter.MetadataEncoding]) != "binary/snappy" {
			result[i] = p
			continue
		}
		// Uncompress
		b, err := snappy.Decode(nil, p.Data)
		if err != nil {
			return payloads, err
		}
		// Unmarshal proto
		result[i] = &commonpb.Payload{}
		err = result[i].Unmarshal(b)
		if err != nil {
			return payloads, err
		}
	}

return result, nil
}
go
//...
c, err := client.Dial(client.Options{
		// Set DataConverter here to ensure that Workflow inputs and results are
		// encoded as required.
		DataConverter: mycodecpackage.DataConverter,
	})
//...
go
  dataConverter := converter.NewCompositeDataConverter(YourCustomPayloadConverter())
  go
  dataConverter := converter.NewCompositeDataConverter(
    converter.NewNilPayloadConverter(),
    converter.NewByteSlicePayloadConverter(),
    converter.NewProtoJSONPayloadConverter(),
    converter.NewProtoPayloadConverter(),
    YourCustomPayloadConverter(),
    converter.NewJSONPayloadConverter(),
  )
  bash
brew install temporal
bash
brew install temporal
bash
temporal server start-dev
bash
temporal server start-dev --help
bash
go get go.temporal.io/sdk
bash
git clone git@github.com:temporalio/sdk-go.git
go
package yourapp

"go.temporal.io/sdk/workflow"
)
// ...

// YourSimpleWorkflowDefinition is the most basic Workflow Definition.
func YourSimpleWorkflowDefinition(ctx workflow.Context) error {
    // ...
    return nil
}
go
package yourapp

"go.temporal.io/sdk/workflow"
)

// YourWorkflowParam is the object passed to the Workflow.
type YourWorkflowParam struct {
    WorkflowParamX string
    WorkflowParamY int
}
// ...
// YourWorkflowDefinition is your custom Workflow Definition.
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) (*YourWorkflowResultObject, error) {
// ...
}
go
package yourapp

"go.temporal.io/sdk/workflow"
)
// ...

// YourWorkflowResultObject is the object returned by the Workflow.
type YourWorkflowResultObject struct {
    WFResultFieldX string
    WFResultFieldY int
}
// ...
// YourWorkflowDefinition is your custom Workflow Definition.
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) (*YourWorkflowResultObject, error) {
// ...
    if err != nil {
        return nil, err
    }
    // Make the results of the Workflow Execution available.
    workflowResult := &YourWorkflowResultObject{
        WFResultFieldX: activityResult.ResultFieldX,
        WFResultFieldY: activityResult.ResultFieldY,
    }
    return workflowResult, nil
}
go
package main

"go.temporal.io/sdk/activity"
    "go.temporal.io/sdk/client"
    "go.temporal.io/sdk/worker"
    "go.temporal.io/sdk/workflow"

"documentation-samples-go/yourapp"
)
// ...
func main() {
// ...
    yourWorker := worker.New(temporalClient, "your-custom-task-queue-name", worker.Options{})
// ...
    // Use RegisterOptions to set the name of the Workflow Type for example.
    registerWFOptions := workflow.RegisterOptions{
        Name: "JustAnotherWorkflow",
    }
    yourWorker.RegisterWorkflowWithOptions(yourapp.YourSimpleWorkflowDefinition, registerWFOptions)
// ...
}
go
package yourapp

"go.temporal.io/sdk/activity"
)
// ...

// YourSimpleActivityDefinition is a basic Activity Definition.
func YourSimpleActivityDefinition(ctx context.Context) error {
    return nil
}

// YourActivityObject is the struct that maintains shared state across Activities.
// If the Worker crashes this Activity object loses its state.
type YourActivityObject struct {
    Message *string
    Number  *int
}

// YourActivityDefinition is your custom Activity Definition.
// An Activity Definition is an exportable function.
func (a *YourActivityObject) YourActivityDefinition(ctx context.Context, param YourActivityParam) (*YourActivityResultObject, error) {
// ...
}
go
// YourActivityParam is the struct passed to your Activity.
// Use a struct so that your function signature remains compatible if fields change.
type YourActivityParam struct {
    ActivityParamX string
    ActivityParamY int
}
// ...
func (a *YourActivityObject) YourActivityDefinition(ctx context.Context, param YourActivityParam) (*YourActivityResultObject, error) {
// ...
}
go
// YourActivityResultObject is the struct returned from your Activity.
// Use a struct so that you can return multiple values of different types.
// Additionally, your function signature remains compatible if the fields change.
type YourActivityResultObject struct {
    ResultFieldX string
    ResultFieldY int
}
// ...
func (a *YourActivityObject) YourActivityDefinition(ctx context.Context, param YourActivityParam) (*YourActivityResultObject, error) {
// ...
    result := &YourActivityResultObject{
        ResultFieldX: "Success",
        ResultFieldY: 1,
    }
    // Return the results back to the Workflow Execution.
    // The results persist within the Event History of the Workflow Execution.
    return result, nil
}
go
func main() {
// ...
    yourWorker := worker.New(temporalClient, "your-custom-task-queue-name", worker.Options{})
// ...
    // Use RegisterOptions to change the name of the Activity Type for example.
    registerAOptions := activity.RegisterOptions{
        Name: "JustAnotherActivity",
    }
    yourWorker.RegisterActivityWithOptions(yourapp.YourSimpleActivityDefinition, registerAOptions)
    // Run the Worker
    err = yourWorker.Run(worker.InterruptCh())
// ...
}
// ...
go
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) (*YourWorkflowResultObject, error) {
    // Set the options for the Activity Execution.
    // Either StartToClose Timeout OR ScheduleToClose is required.
    // Not specifying a Task Queue will default to the parent Workflow Task Queue.
    activityOptions := workflow.ActivityOptions{
        StartToCloseTimeout: 10 * time.Second,
    }
    ctx = workflow.WithActivityOptions(ctx, activityOptions)
    activityParam := YourActivityParam{
        ActivityParamX: param.WorkflowParamX,
        ActivityParamY: param.WorkflowParamY,
    }
    // Use a nil struct pointer to call Activities that are part of a struct.
    var a *YourActivityObject
    // Execute the Activity and wait for the result.
    var activityResult YourActivityResultObject
    err := workflow.ExecuteActivity(ctx, a.YourActivityDefinition, activityParam).Get(ctx, &activityResult)
    if err != nil {
        return nil, err
    }
// ...
}
go
activityOptions := workflow.ActivityOptions{
  // Set Activity Timeout duration
  ScheduleToCloseTimeout: 10 * time.Second,
  // StartToCloseTimeout: 10 * time.Second,
  // ScheduleToStartTimeout: 10 * time.Second,
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  ActivityID: "your-activity-id",
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  TaskQueueName: "your-task-queue-name",
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  ScheduleToCloseTimeout: 10 * time.Second,
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  ScheduleToStartTimeout: 10 * time.Second,
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  StartToCloseTimeout: 10 * time.Second,
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  HeartbeatTimeout: 10 * time.Second,
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  WaitForCancellation: false,
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
activityOptions := workflow.ActivityOptions{
  OriginalTaskQueueName: "your-original-task-queue-name",
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
retryPolicy := &temporal.RetryPolicy{
  InitialInterval:    time.Second,
  BackoffCoefficient: 2.0,
  MaximumInterval:    time.Second * 100, // 100 * InitialInterval
  MaximumAttempts:    0, // Unlimited
  NonRetryableErrorTypes: []string, // empty
}
go
retryPolicy := &temporal.RetryPolicy{
  InitialInterval:    time.Second,
  BackoffCoefficient: 2.0,
  MaximumInterval:    time.Second * 100,
}

activityOptions := workflow.ActivityOptions{
  RetryPolicy: retryPolicy,
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) (YourWorkflowResponse, error) {
 // ...
 future := workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam)
 var yourActivityResult YourActivityResult
 if err := future.Get(ctx, &yourActivityResult); err != nil {
   // ...
 }
 // ...
}
go
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) (YourWorkflowResponse, error) {
 // ...
 future := workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam)
 // ...
 if(future.IsReady()) {
   var yourActivityResult YourActivityResult
   if err := future.Get(ctx, &yourActivityResult); err != nil {
     // ...
   }
 }
 // ...
}
bash
go install github.com/mitranim/gow@latest
gow run worker/main.go # automatically reloads when file changes
go
package main

"go.temporal.io/sdk/activity"
    "go.temporal.io/sdk/client"
    "go.temporal.io/sdk/worker"
    "go.temporal.io/sdk/workflow"

"documentation-samples-go/yourapp"
)

func main() {
    // Create a Temporal Client
    // A Temporal Client is a heavyweight object that should be created just once per process.
    temporalClient, err := client.Dial(client.Options{})
    if err != nil {
        log.Fatalln("Unable to create client", err)
    }
    defer temporalClient.Close()
    // Create a new Worker.
    yourWorker := worker.New(temporalClient, "your-custom-task-queue-name", worker.Options{})
    // Register your Workflow Definitions with the Worker.
    // Use the RegisterWorkflow or RegisterWorkflowWithOptions method for each Workflow registration.
    yourWorker.RegisterWorkflow(yourapp.YourWorkflowDefinition)
// ...
    // Register your Activity Definitons with the Worker.
    // Use this technique for registering all Activities that are part of a struct and set the shared variable values.
    message := "This could be a connection string or endpoint details"
    number := 100
    activities := &yourapp.YourActivityObject{
        Message: &message,
        Number:  &number,
    }
    // Use the RegisterActivity or RegisterActivityWithOptions method for each Activity.
    yourWorker.RegisterActivity(activities)
// ...
    // Run the Worker
    err = yourWorker.Run(worker.InterruptCh())
    if err != nil {
        log.Fatalln("Unable to start Worker", err)
    }
}
// ...
go
// ...
workerOptions := worker.Options{
  MaxConcurrentActivityExecutionSize: 1000,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    WorkerActivitiesPerSecond: 100000,
  // ..
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    MaxConcurrentLocalActivityExecutionSize: 1000,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    WorkerLocalActivitiesPerSecond: 100000,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    TaskQueueActivitiesPerSecond: 100000,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    MaxConcurrentActivityTaskPollers: 2,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    MaxConcurrentWorkflowTaskExecutionSize: 1000,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    MaxConcurrentWorkflowTaskPollers: 2,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    EnableLoggingInReplay: false,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    StickyScheduleToStartTimeout: time.Second(5),
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    StickyScheduleToStartTimeout: time.Second(5),
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
ctx := context.WithValue(context.Background(), "your-key", "your-value")
workerOptions := worker.Options{
    BackgroundActivityContext: ctx,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    DisableStickyExecution: internal.BlockWorkflow,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    WorkerStopTimeout: time.Second(0),
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    EnableSessionWorker: true,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    MaxConcurrentSessionExecutionSize: 1000,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    LocalActivityWorkerOnly: 1000,
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    Identity: "your_custom_identity",
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
// ...
workerOptions := worker.Options{
    DeadlockDetectionTimeout: time.Second(1),
  // ...
}
w := worker.New(c, "your_task_queue_name", workerOptions)
// ...
go
package main

"crypto/tls"
    "log"

"go.temporal.io/sdk/client"
    "go.temporal.io/sdk/worker"

"documentation-samples-go/cloud"
)

func main() {
    // Get the key and cert from your env or local machine
    clientKeyPath := "./secrets/yourkey.key"
    clientCertPath := "./secrets/yourcert.pem"
    // Specify the host and port of your Temporal Cloud Namespace
    // Host and port format: namespace.unique_id.tmprl.cloud:port
    hostPort := "<yournamespace>.<id>.tmprl.cloud:7233"
    namespace := "<yournamespace>.<id>"
    // Use the crypto/tls package to create a cert object
    cert, err := tls.LoadX509KeyPair(clientCertPath, clientKeyPath)
    if err != nil {
        log.Fatalln("Unable to load cert and key pair.", err)
    }
    // Add the cert to the tls certificates in the ConnectionOptions of the Client
    temporalClient, err := client.Dial(client.Options{
        HostPort:  hostPort,
        Namespace: namespace,
        ConnectionOptions: client.ConnectionOptions{
            TLS: &tls.Config{Certificates: []tls.Certificate{cert}},
        },
    })
    if err != nil {
        log.Fatalln("Unable to connect to Temporal Cloud.", err)
    }
    defer temporalClient.Close()
    // Create a new Worker.
    yourWorker := worker.New(temporalClient, "cloud-connection-example-go-task-queue", worker.Options{})
// ...
}
go
w.RegisterActivity(ActivityA)
w.RegisterActivity(ActivityB)
w.RegisterActivity(ActivityC)
w.RegisterWorkflow(WorkflowA)
w.RegisterWorkflow(WorkflowB)
w.RegisterWorkflow(WorkflowC)
go
// ...
w := worker.New(temporalClient, "your_task_queue_name", worker.Options{})
registerOptions := workflow.RegisterOptions{
  DisableAlreadyRegisteredCheck: `false`,
  // ...
}
w.RegisterWorkflowWithOptions(YourWorkflowDefinition, registerOptions)
// ...
go
// ...
w := worker.New(temporalClient, "your_task_queue_name", worker.Options{})
registerOptions := activity.RegisterOptions{
  DisableAlreadyRegisteredCheck: false,
  // ...
}
w.RegisterActivityWithOptions(a.YourActivityDefinition, registerOptions)
// ...
go
// ...
w := worker.New(temporalClient, "your_task_queue_name", worker.Options{})
registerOptions := activity.RegisterOptions{
  SkipInvalidStructFunctions: false,
  // ...
}
w.RegisterActivityWithOptions(a.YourActivityDefinition, registerOptions)
// ...
go
func DynamicWorkflow(ctx workflow.Context, args converter.EncodedValues) (string, error) {
	var result string
	info := workflow.GetInfo(ctx)

var arg1, arg2 string
	err := args.Get(&arg1, &arg2)
	if err != nil {
		return "", fmt.Errorf("failed to decode arguments: %w", err)
	}

if info.WorkflowType.Name == "dynamic-activity" {
		ctx = workflow.WithActivityOptions(ctx, workflow.ActivityOptions{StartToCloseTimeout: 10 * time.Second})
		err := workflow.ExecuteActivity(ctx, "random-activity-name", arg1, arg2).Get(ctx, &result)
		if err != nil {
			return "", err
		}
	} else {
		result = fmt.Sprintf("%s - %s - %s", info.WorkflowType.Name, arg1, arg2)
	}

return result, nil
}
go
func DynamicActivity(ctx context.Context, args converter.EncodedValues) (string, error) {
	var arg1, arg2 string
	err := args.Get(&arg1, &arg2)
	if err != nil {
		return "", fmt.Errorf("failed to decode arguments: %w", err)
	}

info := activity.GetInfo(ctx)
	result := fmt.Sprintf("%s - %s - %s", info.WorkflowType.Name, arg1, arg2)

return result, nil
}
go
package sample

"context"
        "errors"
        "testing"

"github.com/stretchr/testify/mock"
        "github.com/stretchr/testify/suite"

"go.temporal.io/sdk/activity"
        "go.temporal.io/sdk/testsuite"
)

type UnitTestSuite struct {
        suite.Suite
        testsuite.WorkflowTestSuite

env *testsuite.TestWorkflowEnvironment
}

func (s *UnitTestSuite) SetupTest() {
        s.env = s.NewTestWorkflowEnvironment()
}

func (s *UnitTestSuite) AfterTest(suiteName, testName string) {
        s.env.AssertExpectations(s.T())
}

func (s *UnitTestSuite) Test_SimpleWorkflow_Success() {
        s.env.ExecuteWorkflow(SimpleWorkflow, "test_success")

s.True(s.env.IsWorkflowCompleted())
        s.NoError(s.env.GetWorkflowError())
}

func (s *UnitTestSuite) Test_SimpleWorkflow_ActivityParamCorrect() {
        s.env.OnActivity(SimpleActivity, mock.Anything, mock.Anything).Return(
          func(ctx context.Context, value string) (string, error) {
                s.Equal("test_success", value)
                return value, nil
        })
        s.env.ExecuteWorkflow(SimpleWorkflow, "test_success")

s.True(s.env.IsWorkflowCompleted())
        s.NoError(s.env.GetWorkflowError())
}

func (s *UnitTestSuite) Test_SimpleWorkflow_ActivityFails() {
        s.env.OnActivity(SimpleActivity, mock.Anything, mock.Anything).Return(
          "", errors.New("SimpleActivityFailure"))
        s.env.ExecuteWorkflow(SimpleWorkflow, "test_failure")

s.True(s.env.IsWorkflowCompleted())

err := s.env.GetWorkflowError()
        s.Error(err)
        var applicationErr *temporal.ApplicationError
        s.True(errors.As(err, &applicationErr))
        s.Equal("SimpleActivityFailure", applicationErr.Error())
}

func TestUnitTestSuite(t *testing.T) {
        suite.Run(t, new(UnitTestSuite))
}
go
func (s *UnitTestSuite) Test_SimpleWorkflow_Success() {
        s.env.ExecuteWorkflow(SimpleWorkflow, "test_success")

s.True(s.env.IsWorkflowCompleted())
        s.NoError(s.env.GetWorkflowError())
}
go
func (s *UnitTestSuite) Test_SimpleWorkflow_ActivityFails() {
        s.env.OnActivity(SimpleActivity, mock.Anything, mock.Anything).Return(
          "", errors.New("SimpleActivityFailure"))
        s.env.ExecuteWorkflow(SimpleWorkflow, "test_failure")

s.True(s.env.IsWorkflowCompleted())

err := s.env.GetWorkflowError()
        s.Error(err)
        var applicationErr *temporal.ApplicationError
        s.True(errors.As(err, &applicationErr))
        s.Equal("SimpleActivityFailure", applicationErr.Error())
}
go
s.env.OnActivity(SimpleActivity, mock.Anything, mock.Anything).Return(
  "", errors.New("SimpleActivityFailure"))
go
func (s *UnitTestSuite) Test_SimpleWorkflow_ActivityParamCorrect() {
        s.env.OnActivity(SimpleActivity, mock.Anything, mock.Anything).Return(
          func(ctx context.Context, value string) (string, error) {
                s.Equal("test_success", value)
                return value, nil
        })
        s.env.ExecuteWorkflow(SimpleWorkflow, "test_success")

s.True(s.env.IsWorkflowCompleted())
        s.NoError(s.env.GetWorkflowError())
}
go
func ProgressWorkflow(ctx workflow.Context, percent int) error {
	logger := workflow.GetLogger(ctx)

err := workflow.SetQueryHandler(ctx, "getProgress", func(input []byte) (int, error) {
		return percent, nil
	})
	if err != nil {
		logger.Info("SetQueryHandler failed.", "Error", err)
		return err
	}

for percent = 0; percent<100; percent++ {
                // Important! Use `workflow.Sleep()`, not `time.Sleep()`, because Temporal's
                // test environment doesn't stub out `time.Sleep()`.
		workflow.Sleep(ctx, time.Second*1)
	}

return nil
}
go
func (s *UnitTestSuite) Test_ProgressWorkflow() {
	value := 0

// After 10 seconds plus padding, progress should be 10.
	// Note that `RegisterDelayedCallback()` doesn't actually make your test wait for 10 seconds!
	// Temporal's test framework advances time internally, so this test should take < 1 second.
	s.env.RegisterDelayedCallback(func() {
		res, err := s.env.QueryWorkflow("getProgress")
		s.NoError(err)
		err = res.Get(&value)
		s.NoError(err)
		s.Equal(10, value)
	}, time.Second*10+time.Millisecond*1)

s.env.ExecuteWorkflow(ProgressWorkflow, 0)

s.True(s.env.IsWorkflowCompleted())

// Once the workflow is completed, progress should always be 100
	res, err := s.env.QueryWorkflow("getProgress")
	s.NoError(err)
	err = res.Get(&value)
	s.NoError(err)
	s.Equal(value, 100)
}
go

"context"
    "go.temporal.io/sdk/client"
)

func main() {
    // Create the client
    c, err := client.Dial(client.Options{})
    if err != nil {
        // Handle error
    }
    defer c.Close()

// Start workflow options with static summary and details
    workflowOptions := client.StartWorkflowOptions{
        ID:        "your-workflow-id",
        TaskQueue: "your-task-queue",
        StaticSummary: "Order processing for customer #12345",
        StaticDetails: "Processing premium order with expedited shipping",
    }

// Start the workflow
    we, err := c.ExecuteWorkflow(context.Background(), workflowOptions, YourWorkflow, "workflow input")
    if err != nil {
        // Handle error
    }
}
go

"go.temporal.io/sdk/workflow"
)

func YourWorkflow(ctx workflow.Context, input string) (string, error) {
    // Get the current details
    currentDetails := workflow.GetCurrentDetails(ctx)
    workflow.GetLogger(ctx).Info("Current details", "details", currentDetails)
    
    // Set/update the current details
    workflow.SetCurrentDetails(ctx, "Updated workflow details with new status")
    
    return "Workflow completed", nil
}
go

"time"
    "go.temporal.io/sdk/workflow"
)

func YourWorkflow(ctx workflow.Context, input string) (string, error) {
    // Activity options with summary
    ao := workflow.ActivityOptions{
        StartToCloseTimeout: 10 * time.Second,
        Summary: "Processing user data",
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

// Execute the activity
    var result string
    err := workflow.ExecuteActivity(ctx, YourActivity, input).Get(ctx, &result)
    if err != nil {
        return "", err
    }
    
    return result, nil
}
go

"time"
    "go.temporal.io/sdk/workflow"
)

func YourWorkflow(ctx workflow.Context, input string) (string, error) {
    // Create a timer with options including summary
    timerFuture := workflow.NewTimerWithOptions(ctx, 5*time.Minute, workflow.TimerOptions{
        Summary: "Waiting for payment confirmation",
    })
    
    // Wait for the timer
    err := timerFuture.Get(ctx, nil)
    if err != nil {
        return "", err
    }
    
    return "Timer completed", nil
}
go
err := workflow.ExecuteActivity(ctx, YourActivity, ...).Get(ctx, nil)
if err != nil {
	var applicationErr *ApplicationError
	if errors.As(err, &applicationErr) {
		// retrieve error message
		fmt.Println(applicationError.Error())

// handle Activity errors (created via NewApplicationError() API)
		var detailMsg string // assuming Activity return error by NewApplicationError("message", true, "string details")
		applicationErr.Details(&detailMsg) // extract strong typed details

// handle Activity errors (errors created other than using NewApplicationError() API)
		switch applicationErr.Type() {
		case "CustomErrTypeA":
			// handle CustomErrTypeA
		case CustomErrTypeB:
			// handle CustomErrTypeB
		default:
			// newer version of Activity could return new errors that Workflow was not aware of.
		}
	}

var canceledErr *CanceledError
	if errors.As(err, &canceledErr) {
		// handle cancellation
	}

var timeoutErr *TimeoutError
	if errors.As(err, &timeoutErr) {
		// handle timeout, could check timeout type by timeoutErr.TimeoutType()
        switch err.TimeoutType() {
        case commonpb.ScheduleToStart:
                // Handle ScheduleToStart timeout.
        case commonpb.StartToClose:
                // Handle StartToClose timeout.
        case commonpb.Heartbeat:
                // Handle heartbeat timeout.
        default:
        }
	}

var panicErr *PanicError
	if errors.As(err, &panicErr) {
		// handle panic, message and call stack are available by panicErr.Error() and panicErr.StackTrace()
	}
}
go
workflowOptions := client.StartWorkflowOptions{
  // ...
  // Set Workflow Timeout duration
  WorkflowExecutionTimeout: 24 * 365 * 10 * time.Hour,
  // WorkflowRunTimeout: 24 * 365 * 10 * time.Hour,
  // WorkflowTaskTimeout: 10 * time.Second,
  // ...
}
workflowRun, err := c.ExecuteWorkflow(context.Background(), workflowOptions, YourWorkflowDefinition)
if err != nil {
  // ...
}
go
retrypolicy := &temporal.RetryPolicy{
  InitialInterval:    time.Second,
  BackoffCoefficient: 2.0,
  MaximumInterval:    time.Second * 100,
}
workflowOptions := client.StartWorkflowOptions{
  RetryPolicy: retrypolicy,
  // ...
}
workflowRun, err := temporalClient.ExecuteWorkflow(context.Background(), workflowOptions, YourWorkflowDefinition)
if err != nil {
  // ...
}
go
activityoptions := workflow.ActivityOptions{
  // Set Activity Timeout duration
  ScheduleToCloseTimeout: 10 * time.Second,
  // StartToCloseTimeout: 10 * time.Second,
  // ScheduleToStartTimeout: 10 * time.Second,
}
ctx = workflow.WithActivityOptions(ctx, activityoptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
retrypolicy := &temporal.RetryPolicy{
  InitialInterval:    time.Second,
  BackoffCoefficient: 2.0,
  MaximumInterval:    time.Second * 100, // 100 * InitialInterval
  MaximumAttempts: 0, // Unlimited
  NonRetryableErrorTypes: []string, // empty
}
go
retrypolicy := &temporal.RetryPolicy{
  InitialInterval:    time.Second,
  BackoffCoefficient: 2.0,
  MaximumInterval:    time.Second * 100,
}

activityoptions := workflow.ActivityOptions{
  RetryPolicy: retrypolicy,
}
ctx = workflow.WithActivityOptions(ctx, activityoptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
attempt := activity.GetInfo(ctx).Attempt;

return temporal.NewApplicationErrorWithOptions(fmt.Sprintf("Something bad happened on attempt %d", attempt), "NextDelay", temporal.ApplicationErrorOptions{
  NextRetryDelay: 3 * time.Second * delay,
})
go

// ...
    "go.temporal.io/sdk/workflow"
    // ...
)

func YourActivityDefinition(ctx, YourActivityDefinitionParam) (YourActivityDefinitionResult, error) {
    // ...
    activity.RecordHeartbeat(ctx, details)
    // ...
}
go
// The client is a heavyweight object that should be created once per process.
temporalClient, err := client.Dial(client.Options{})
// Record heartbeat.
err := temporalClient.RecordActivityHeartbeat(ctx, taskToken, details)
go
func SampleActivity(ctx context.Context, inputArg InputParams) error {
    startIdx := inputArg.StartIndex
    if activity.HasHeartbeatDetails(ctx) {
        // Recover from finished progress.
        var finishedIndex int
        if err := activity.GetHeartbeatDetails(ctx, &finishedIndex); err == nil {
            startIdx = finishedIndex + 1 // Start from next one.
        }
    }

// Normal Activity logic...
    for i:=startIdx; i<inputArg.EndIdx; i++ {
        // Code for processing item i goes here...
        activity.RecordHeartbeat(ctx, i) // Report progress.
    }
}
go
activityoptions := workflow.ActivityOptions{
  HeartbeatTimeout: 10 * time.Second,
}
ctx = workflow.WithActivityOptions(ctx, activityoptions)
var yourActivityResult YourActivityResult
err = workflow.ExecuteActivity(ctx, YourActivityDefinition, yourActivityParam).Get(ctx, &yourActivityResult)
if err != nil {
  // ...
}
go
type Language string

const Chinese Language = "chinese"
const English Language = "english"
const French Language = "french"
const Spanish Language = "spanish"
const Portuguese Language = "portuguese"

const GetLanguagesQuery = "GetLanguages"

type GetLanguagesInput struct {
	IncludeUnsupported bool
}

func GreetingWorkflow(ctx workflow.Context) (string, error) {
    ...
    greeting := map[Language]string{English: "Hello", Chinese: "你好，世界"}
    err := workflow.SetQueryHandler(ctx, GetLanguagesQuery, func(input GetLanguagesInput) ([]Language, error) {
        // 👉 A Query handler returns a value: it can inspect but must not mutate the Workflow state.
        if input.IncludeUnsupported {
            return []Language{Chinese, English, French, Spanish, Portuguese}, nil
        } else {
            // Range over map is a nondeterministic operation.
            // It is OK to have a non-deterministic operation in a query function.
            //workflowcheck:ignore
            return maps.Keys(greeting), nil
        }
    })
    ...
}
go
const ApproveSignal = "approve"

type ApproveInput struct {
	Name string
}

func GreetingWorkflow(ctx workflow.Context) error {
    logger := workflow.GetLogger(ctx)
	approverName := ""
	...
	// Block until the language is approved
	var approveInput ApproveInput
	workflow.GetSignalChannel(ctx, ApproveSignal).Receive(ctx, &approveInput)
	approverName = approveInput.Name
	logger.Info("Received approval", "Approver", approverName)
	...
}
go
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) error {
   var signal MySignal
   signalChan := workflow.GetSignalChannel(ctx, "your-signal-name")
 	workflow.Go(ctx, func(ctx workflow.Context) {
 		for {
 			selector := workflow.NewSelector(ctx)
 			selector.AddReceive(signalChan, func(c workflow.ReceiveChannel, more bool) {
 				c.Receive(ctx, &signal)
 			})
 			selector.Select(ctx)
 		}
 	})
   // You could now submit an activity; any signals will still be received while the activity is pending.
 }
go
reportCompletionChannel := workflow.GetSignalChannel(ctx, "ReportCompletion")
// Drain signals async
for {
	var recordId int
	ok := reportCompletionChannel.ReceiveAsync(&recordId)
	if !ok {
		break
	}
	s.recordCompletion(ctx, recordId)
}
go
type Language string

const SetLanguageUpdate = "set-language"

func GreetingWorkflow(ctx workflow.Context) error {
	language := English

err = workflow.SetUpdateHandlerWithOptions(ctx, SetLanguageUpdate, func(ctx workflow.Context, newLanguage Language) (Language, error) {
		// 👉 An Update handler can mutate the Workflow state and return a value.
		var previousLanguage Language
		previousLanguage, language = language, newLanguage
		return previousLanguage, nil
	}, workflow.UpdateHandlerOptions{
		Validator: func(ctx workflow.Context, newLanguage Language) error {
			if _, ok := greeting[newLanguage]; !ok {
				// 👉 In an Update validator you return any error to reject the Update.
				return fmt.Errorf("%s unsupported language", newLanguage)
			}
			return nil
		},
	})
  ...
}
go
// ...
supportedLangResult, err := temporalClient.QueryWorkflow(context.Background(), we.GetID(), we.GetRunID(), message.GetLanguagesQuery, message.GetLanguagesInput{IncludeUnsupported: false})
if err != nil {
    log.Fatalf("Unable to query workflow: %v", err)
}
var supportedLang []message.Language
err = supportedLangResult.Get(&supportedLang)
if err != nil {
    log.Fatalf("Unable to get query result: %v", err)
}
log.Println("Supported languages:", supportedLang)
// ...
go
// ...
err = temporalClient.SignalWorkflow(context.Background(), we.GetID(), we.GetRunID(), message.ApproveSignal, message.ApproveInput{Name: ""})
if err != nil {
    log.Fatalf("Unable to signal workflow: %v", err)
}
// ...
go
// ...
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) error {
  ...
  signal := MySignal {
    Message: "Some important data",
  }
  err :=  workflow.SignalExternalWorkflow(ctx, "some-workflow-id", "", "your-signal-name", signal).Get(ctx, nil)
  if err != nil {
    // ...
  }
// ...
}
go
// ...
signal := MySignal {
  Message: "Some important data",
}
err = temporalClient.SignalWithStartWorkflow(context.Background(), "your-workflow-id", "your-signal-name", signal)
if err != nil {
	log.Fatalln("Error sending the Signal", err)
	return
}
go
ctxWithTimeout, cancel := context.WithTimeout(context.Background(), 15*time.Second)
defer cancel()

updateHandle, err := temporalClient.UpdateWorkflow(ctxWithTimeout, client.UpdateWorkflowOptions{
    WorkflowID:   we.GetID(),
    RunID:        we.GetRunID(),
    UpdateName:   message.SetLanguageUpdate,
    WaitForStage: client.WorkflowUpdateStageAccepted,
    Args:         []interface{}{message.Chinese},
})
if err != nil {
    log.Fatalf("Unable to update workflow: %v", err)
}

var previousLang message.Language
err = updateHandle.Get(ctxWithTimeout, &previousLang)
if err != nil {
    log.Fatalf("Unable to get update result: %v", err)
}
go
ctxWithTimeout, cancel := context.WithTimeout(context.Background(), 15*time.Second)
defer cancel()

workflowOptions := client.StartWorkflowOptions{
    ID:                       "some-workflow-id",
    TaskQueue:                "some-task-queue",
    WorkflowIDConflictPolicy: enumspb.WORKFLOW_ID_CONFLICT_POLICY_USE_EXISTING,
}

updateOptions := client.UpdateWorkflowOptions{
    UpdateName:   message.SetLanguageUpdate,
    WaitForStage: client.WorkflowUpdateStageCompleted,
}

startWorkflowOp := temporalClient.NewWithStartWorkflowOperation(workflowOptions, MyWorkflow)
updateHandle, err := temporalClient.UpdateWithStartWorkflow(
	ctxWithTimeout,
	client.UpdateWithStartWorkflowOptions{
        StartWorkflowOperation: startWorkflowOp,
        UpdateOptions:          updateOptions,
    })
if err != nil {
    log.Fatalf("Unable to execute update-with-start: %v", err)
}

var previousLang message.Language
err = updateHandle.Get(ctxWithTimeout, &previousLang)
if err != nil {
    log.Fatalf("Unable to obtain update result: %v", err)
}

workflowRun, err := startWorkflowOp.Get(ctxWithTimeout)
if err != nil {
    log.Fatalf("Unable to obtain workflow run: %v", err)
}
go
func GreetingWorkflow(ctx workflow.Context) error {
	language := English

err = workflow.SetUpdateHandler(ctx, SetLanguageUpdate, func(ctx workflow.Context, newLanguage Language) (Language, error) {
        if _, ok := greeting[newLanguage]; !ok {
            ao := workflow.ActivityOptions{
                StartToCloseTimeout: 10 * time.Second,
            }
            ctx = workflow.WithActivityOptions(ctx, ao)

var greeting string
            err := workflow.ExecuteActivity(ctx, CallGreetingService, newLanguage).Get(ctx, &greeting)
            if err != nil {
                return nil, err
            }
            greeting[newLanguage] = greeting
        }
		var previousLanguage Language
		previousLanguage, language = language, newLanguage
		return previousLanguage, nil
	})
  ...
}
go
err = workflow.SetUpdateHandler(ctx, "UpdateHandler", func(ctx workflow.Context, input UpdateInput) error {
    workflow.Await(ctx, updateUnblockedFunc)
    ...
})
go
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) error {
    ...
	err = workflow.Await(ctx, func() bool {
		return workflow.AllHandlersFinished(ctx)
	})
    return nil
}
go
err = workflow.SetUpdateHandlerWithOptions(ctx, UpdateHandlerName, UpdateFunc, workflow.UpdateHandlerOptions{
       UnfinishedPolicy: workflow.HandlerUnfinishedPolicyAbandon,
})
go
// ...
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) error {
    ...
    err := workflow.SetUpdateHandler(ctx, "BadUpdateHandler", func(ctx workflow.Context) error {
        ao := workflow.ActivityOptions{
            StartToCloseTimeout: 10 * time.Second,
        }
        ctx = workflow.WithActivityOptions(ctx, ao)

var result Data
        err := workflow.ExecuteActivity(ctx, FetchData, name).Get(ctx, &result)
        x = result.x
        // 🐛🐛 Bug!! If multiple instances of this handler are executing concurrently, then
        // there may be times when the Workflow has self.x from one Activity execution and self.y from another.
        err = workflow.Sleep(ctx, time.Second)
        if err != nil {
            return err
        }
        y = result.y
    })
    ...
}
go
func YourWorkflowDefinition(ctx workflow.Context, param YourWorkflowParam) error {
    ...
    err := workflow.SetUpdateHandler(ctx, "SafeUpdateHandler", func(ctx workflow.Context) error {
        err := mutex.Lock(ctx)
        if err != nil {
            return err
        }
        defer mutex.Unlock()
        ao := workflow.ActivityOptions{
            StartToCloseTimeout: 10 * time.Second,
        }
        ctx = workflow.WithActivityOptions(ctx, ao)

var result Data
        err := workflow.ExecuteActivity(ctx, FetchData, name).Get(ctx, &result)
        x = data.x
        // ✅ OK: the scheduler may switch now to a different handler execution, or to the main workflow
        // method, but no other execution of this handler can run until this execution finishes.
        err = workflow.Sleep(ctx, time.Second)
        if err != nil {
            return err
        }
        self.y = data.y
    })
    ...
}
go
client, err := client.NewNamespaceClient(client.Options{HostPort: ts.config.ServiceAddr})
        //...
    err = client.Register(ctx, &workflowservice.RegisterNamespaceRequest{
        Namespace: your-namespace-name,
        WorkflowExecutionRetentionPeriod: &retention,
    })
go
    //...
      err = client.Update(context.Background(), &workflowservice.UpdateNamespaceRequest{
      Namespace:         "your-namespace-name",
      UpdateInfo:        &namespace.UpdateNamespaceInfo{ //updates info for the namespace "your-namespace-name"
          Description:   "updated namespace description",
          OwnerEmail:    "newowner@mail.com",
          //Data:        nil,
          //State:       0,
      },
      /*other details that you can update:
      Config:            &namespace.NamespaceConfig{ //updates the configuration of the namespace with the following options
          //WorkflowExecutionRetentionTtl: nil,
          //BadBinaries:                   nil,
          //HistoryArchivalState:          0,
          //HistoryArchivalUri:            "",
          //VisibilityArchivalState:       0,
          //VisibilityArchivalUri:         "",
      },
      ReplicationConfig: &replication.NamespaceReplicationConfig{ //updates the replication configuration for the namespace
          //ActiveClusterName: "",
          //Clusters:          nil,
          //State:             0,
      },
      SecurityToken:     "",
      DeleteBadBinary:   "",
      PromoteNamespace:  false,
      })*/
    //...
    go
    //...
      client, err := client.NewNamespaceClient(client.Options{})
      //...
      client.Describe(context.Background(), "default")
    //...
    go
  //...
      namespace.Handler.ListNamespaces(context.Context(), &workflowservice.ListNamespacesRequest{ //lists 1 page (1-100) of namespaces on the active Temporal Service. You can set a large PageSize or loop until NextPageToken is nil
          //PageSize:        0,
          //NextPageToken:   nil,
          //NamespaceFilter: nil,
          })
  //...
  go
  //...
  client.OperatorService().DeleteNamespace(ctx, &operatorservice.DeleteNamespaceRequest{...
  //...
  go
client.Options{
		MetricsHandler: sdktally.NewMetricsHandler(newPrometheusScope(prometheus.Configuration{
			ListenAddress: "0.0.0.0:9090",
			TimerType:     "histogram",
		}
proto
message Header {
    map<string, Payload> fields = 1;
}
go
type HeaderWriter interface {
	Set(string, *commonpb.Payload)
}

type HeaderReader interface {
	Get(string) (*commonpb.Payload, bool)
	ForEachKey(handler func(string, *commonpb.Payload) error) error
}
go
type ContextPropagator interface {
  Inject(context.Context, HeaderWriter) error

Extract(context.Context, HeaderReader) (context.Context, error)

InjectFromWorkflow(Context, HeaderWriter) error

ExtractToWorkflow(Context, HeaderReader) (Context, error)
}
go
// create Interceptor
tracingInterceptor, err := opentracing.NewInterceptor(opentracing.TracerOptions{})
go
// create Interceptor
tracingInterceptor, err := opentelemetry.NewTracingInterceptor(opentelemetry.TracerOptions{})
go
// create Interceptor
tracingInterceptor, err := tracing.NewTracingInterceptor(tracing.TracerOptions{})
go
c, err := client.Dial(client.Options{
  Interceptors:       []interceptor.ClientInterceptor{tracingInterceptor},
})
go

"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/workflow"
)

// Workflow is a standard workflow definition.
// Note that the Workflow and Activity don't need to care that
// their inputs/results are being compressed.
func Workflow(ctx workflow.Context, name string) (string, error) {
// ...

workflow.WithActivityOptions(ctx, ao)

// Getting the logger from the context.
	logger := workflow.GetLogger(ctx)
// Logging a message with the key value pair `name` and `name`
	logger.Info("Compressed Payloads workflow started", "name", name)

info := map[string]string{
		"name": name,
	}

logger.Info("Compressed Payloads workflow completed.", "result", result)

return result, nil
}
go
package main

"go.temporal.io/sdk/client"

"github.com/sirupsen/logrus"
	logrusadapter "logur.dev/adapter/logrus"
	"logur.dev/logur"
)

func main() {
  // ...
  logger := logur.LoggerToKV(logrusadapter.New(logrus.New()))
  clientOptions := client.Options{
    Logger: logger,
  }
  temporalClient, err := client.Dial(clientOptions)
  // ...
}
go
request := &workflowservice.ListWorkflowExecutionsRequest{ Query: "CloseTime = missing" }
go
resp, err := temporalClient.ListWorkflow(ctx.Background(), request)
if err != nil {
  return err
}

fmt.Println("First page of results:")
for _, exec := range resp.Executions {
  fmt.Printf("Workflow ID %v\n", exec.Execution.WorkflowId)
}
go
func (c *Client) CallYourWorkflow(ctx context.Context, workflowID string, payload map[string]interface{}) error {
    // ...
    searchAttributes := map[string]interface{}{
        "CustomerId": payload["customer"],
        "MiscData": payload["miscData"]
    }
    options := client.StartWorkflowOptions{
        SearchAttributes:   searchAttributes
        // ...
    }
    we, err := c.Client.ExecuteWorkflow(ctx, options, app.YourWorkflow, payload)
    // ...
}
go
func YourWorkflow(ctx workflow.Context, input string) error {

attr1 := map[string]interface{}{
        "CustomIntField": 1,
        "CustomBoolField": true,
    }
    workflow.UpsertSearchAttributes(ctx, attr1)

attr2 := map[string]interface{}{
        "CustomIntField": 2,
        "CustomKeywordField": "seattle",
    }
    workflow.UpsertSearchAttributes(ctx, attr2)
}
go
map[string]interface{}{
    "CustomIntField": 2, // last update wins
    "CustomBoolField": true,
    "CustomKeywordField": "seattle",
}
go
func main() {
// ...
	scheduleID := "schedule_id"
	workflowID := "schedule_workflow_id"
	// Create the schedule.
	scheduleHandle, err := temporalClient.ScheduleClient().Create(ctx, client.ScheduleOptions{
		ID:   scheduleID,
		Spec: client.ScheduleSpec{},
		Action: &client.ScheduleWorkflowAction{
			ID:        workflowID,
			Workflow:  schedule.ScheduleWorkflow,
			TaskQueue: "schedule",
		},
	})
// ...
}
// ...
go
func main() {
// ...
	err = scheduleHandle.Backfill(ctx, client.ScheduleBackfillOptions{
		Backfill: []client.ScheduleBackfill{
			{
				Start:   now.Add(-4 * time.Minute),
				End:     now.Add(-2 * time.Minute),
				Overlap: enums.SCHEDULE_OVERLAP_POLICY_ALLOW_ALL,
			},
			{
				Start:   now.Add(-2 * time.Minute),
				End:     now,
				Overlap: enums.SCHEDULE_OVERLAP_POLICY_ALLOW_ALL,
			},
		},
	})
	if err != nil {
		log.Fatalln("Unable to Backfill Schedule", err)
	}
// ...
}
// ...
go
func main() {
// ...
	defer func() {
		log.Println("Deleting schedule", "ScheduleID", scheduleHandle.GetID())
		err = scheduleHandle.Delete(ctx)
		if err != nil {
			log.Fatalln("Unable to delete schedule", err)
		}
	}()
// ...
go
func main() {
// ...
	scheduleHandle.Describe(ctx)
// ...
go
func main() {
// ...
	listView, _ := temporalClient.ScheduleClient().List(ctx, client.ScheduleListOptions{
		PageSize: 1,
	})

for listView.HasNext() {
		log.Println(listView.Next())
	}
// ...
go
func main() {
// ...
	err = scheduleHandle.Pause(ctx, client.SchedulePauseOptions{
		Note: "The Schedule has been paused.",
	})
// ...
	err = scheduleHandle.Unpause(ctx, client.ScheduleUnpauseOptions{
		Note: "The Schedule has been unpaused.",
	})
go
func main() {
// ...
	for i := 0; i < 5; i++ {
		scheduleHandle.Trigger(ctx, client.ScheduleTriggerOptions{
			Overlap: enums.SCHEDULE_OVERLAP_POLICY_ALLOW_ALL,
		})
		time.Sleep(2 * time.Second)
	}
// ...
go
func main() {
// ...
	updateSchedule := func(input client.ScheduleUpdateInput) (*client.ScheduleUpdate, error) {
		return &client.ScheduleUpdate{
			Schedule: &input.Description.Schedule,
		}, nil
	}

_ = scheduleHandle.Update(ctx, client.ScheduleUpdateOptions{
		DoUpdate: updateSchedule,
	})
}
// ...
go
workflowOptions := client.StartWorkflowOptions{
  // ...
  // Start the workflow in 12 hours
  StartDelay: time.Hours * 12,
  // ...
}
workflowRun, err := c.ExecuteWorkflow(context.Background(), workflowOptions, YourWorkflowDefinition)
if err != nil {
  // ...
}
go
workflowOptions := client.StartWorkflowOptions{
  CronSchedule: "15 8 * * *",
  // ...
}
workflowRun, err := c.ExecuteWorkflow(context.Background(), workflowOptions, YourWorkflowDefinition)
if err != nil {
  // ...
}

┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
go
func SampleWorkflow(ctx workflow.Context) error {
	// standard Workflow setup code omitted...

// API Example: declare a new selector
	selector := workflow.NewSelector(ctx)

// API Example: defer code execution until the Future that represents Activity result is ready
	work := workflow.ExecuteActivity(ctx, ExampleActivity)
	selector.AddFuture(work, func(f workflow.Future) {
		// deferred code omitted...
	})

// more parallel timers and activities initiated...

// API Example: receive information from a Channel
	var signalVal string
	channel := workflow.GetSignalChannel(ctx, channelName)
	selector.AddReceive(channel, func(c workflow.ReceiveChannel, more bool) {
		// matching on the channel doesn't consume the message.
	 	// So it has to be explicitly consumed here
		c.Receive(ctx, &signalVal)
		// do something with received information
	})

// API Example: block until the next Future is ready to run
	// important! none of the deferred code runs until you call selector.Select
	selector.Select(ctx)

// Todo: document selector.HasPending
}
go
// API Example: defer code execution until after an activity is done
work := workflow.ExecuteActivity(ctx, ExampleActivity)
selector.AddFuture(work, func(f workflow.Future) {
	// deferred code omitted...
})
go
	// API Example: blocking conditionally
  if somecondition != nil {
		selector.Select(ctx)
  }

// API Example: popping off all remaining Futures
  for i := 0; i < len(someArray); i++ {
		selector.Select(ctx) // this will wait for one branch
		// you can interrupt execution here
	}
go
var processingDone bool
f := workflow.ExecuteActivity(ctx, OrderProcessingActivity)
selector.AddFuture(f, func(f workflow.Future) {
	processingDone = true
	// cancel timerFuture
	cancelHandler()
})

// use timer future to send notification email if processing takes too long
timerFuture := workflow.NewTimer(childCtx, processingTimeThreshold)
selector.AddFuture(timerFuture, func(f workflow.Future) {
	if !processingDone {
		// processing is not done yet when timer fires, send notification email
		_ = workflow.ExecuteActivity(ctx, SendEmailActivity).Get(ctx, nil)
	}
})

// wait the timer or the order processing to finish
selector.Select(ctx)
go
// API Example: receive information from a Channel
var signalVal string
channel := workflow.GetSignalChannel(ctx, channelName)
selector.AddReceive(channel, func(c workflow.ReceiveChannel, more bool) {
	c.Receive(ctx, &signalVal)
	// do something with received information
})
go
// ...
func main() {
// ...
	// Enable Sessions for this Worker.
	workerOptions := worker.Options{
		EnableSessionWorker: true,
// ...
	}
	w := worker.New(temporalClient, "fileprocessing", workerOptions)
	w.RegisterWorkflow(sessions.SomeFileProcessingWorkflow)
	w.RegisterActivity(&sessions.FileActivities{})
	err = w.Run(worker.InterruptCh())
// ...
}
go
func main() {
// ...
	workerOptions := worker.Options{
// ...
		// This configures the maximum allowed concurrent sessions.
		// Customize this value only if you need to.
		MaxConcurrentSessionExecutionSize: 1000,
// ...
}
// ...
go
package sessions

"go.temporal.io/sdk/workflow"
)

// ...
// SomeFileProcessingWorkflow is a Workflow Definition.
func SomeFileProcessingWorkflow(ctx workflow.Context, param FileProcessingWFParam) error {
	activityOptions := workflow.ActivityOptions{
		StartToCloseTimeout: time.Minute,
	}
	ctx = workflow.WithActivityOptions(ctx, activityOptions)
// ...
	sessionOptions := &workflow.SessionOptions{
		CreationTimeout:  time.Minute,
		ExecutionTimeout: time.Minute,
	}
	// Create a Session with the Worker so that all Activities execute with the same Worker.
	sessionCtx, err := workflow.CreateSession(ctx, sessionOptions)
	if err != nil {
		return err
	}
	defer workflow.CompleteSession(sessionCtx)
// ...
	err = workflow.ExecuteActivity(sessionCtx, a.DownloadFile, param).Get(sessionCtx, &downloadResult)
// ...
	err = workflow.ExecuteActivity(sessionCtx, a.ProcessFile, processParam).Get(sessionCtx, &processResult)
// ...
	err = workflow.ExecuteActivity(sessionCtx, a.UploadFile, uploadParam).Get(sessionCtx, nil)
// ...
}
go
type SessionInfo struct {
 // A unique Id for the session
 SessionID         string
 // The hostname of the worker that is executing the session
 HostName          string
 // ... other unexported fields
}

func GetSessionInfo(ctx Context) *SessionInfo
go
func RecreateSession(ctx Context, recreateToken []byte, sessionOptions *SessionOptions) (Context, error)
go
token := workflow.GetSessionInfo(sessionCtx).GetRecreateToken()
```

**Is there a complete example?**

Yes, the [file processing example](https://github.com/temporalio/samples-go/tree/master/fileprocessing) in the [temporalio/samples-go](https://github.com/temporalio/samples-go) repo has been updated to use the session framework.

**What happens to my Activity if the Worker dies?**

If your Activity has already been scheduled, it will be canceled.
If not, you will get a `workflow.ErrSessionFailed` error when you call `workflow.ExecuteActivity()`.

**Is the concurrent session limitation per process or per host?**

It's per Worker Process, so make sure there's only one Worker Process running on the host if you plan to use this feature.

- Right now, a Session is considered failed if the Worker Process dies.
  However, for some use cases, you may only care whether the Worker host is alive or not.
  For these use cases, the Session should be automatically re-established if the Worker Process is restarted.

- The current implementation assumes that all Sessions are consuming the same type of resource and there's only one global limitation.
  Our plan is to allow you to specify what type of resource your Session will consume and enforce different limitations on different types of resources.

## Set up your local with the Go SDK

**Examples:**

Example 1 (unknown):
```unknown
</TabItem>
</Tabs>

## Load configuration profile and environment variables

If you don't specify a profile, the SDKs load the `default` profile and the environment variables. If you haven't set
`TEMPORAL_CONFIG_FILE`, the SDKs will look for the configuration file in the default location. Refer to
[Configuration methods](#configuration-methods) for the default locations for your operating system.

No matter what profile you choose to load, environment variables are always loaded when you use the APIs in the
environment configuration package to load Temporal Client connection options. They always take precedence over TOML file
settings in the profiles.

<SdkTabs hideUnsupportedLanguages>
  <SdkTabs.Python>

To load the `default` profile along with any environment variables in Python, use the `ClientConfigProfile.load()`
method from the `temporalio.envconfig` package.
```

Example 2 (unknown):
```unknown
</SdkTabs.Python>
  <SdkTabs.Go>

To load the `default` profile along with any environment variables in Go, use the
`envconfig.MustLoadDefaultClientOptions()` function from the `temporalio.envconfig` package.
```

Example 3 (unknown):
```unknown
</SdkTabs.Go>
  <SdkTabs.Ruby>

To load the `default` profile along with any environment variables in Ruby, use the
`EnvConfig::ClientConfig.load_client_connect_options()` method from the `temporalio.env_config` package.
```

Example 4 (unknown):
```unknown
</SdkTabs.Ruby>

  <SdkTabs.DotNet>

To load the `default` profile along with any environment variables in .NET C#, use the
`ClientEnvConfig.LoadClientConnectOptions()` method from the `Temporalio.Client.EnvConfig` package.
```

---

## Task Queue Names

**URL:** llms-txt#task-queue-names

The Temporal Service maintains a set of Task Queues, which Workers poll to see
what work needs to be done. Each Task Queue is identified by a name, which is
provided to the Temporal Service when launching a Workflow Execution.

<Tabs groupId="start-workflow-configure-worker-by-sdk" queryString>

<TabItem value="python" label="Python">

**Excerpt of code used to start the Workflow in Python**

```python
client = await Client.connect("localhost:7233", namespace="default")

---

## Verify that the expected Heartbeats are received by the callback function.

**URL:** llms-txt#verify-that-the-expected-heartbeats-are-received-by-the-callback-function.

**Contents:**
- Testing Workflows {#test-workflows}
  - How to mock Activities {#mock-activities}

assert heartbeats == ["param: test", "second heartbeat"]
python

from temporalio.client import Client
from temporalio.worker import Worker

**Examples:**

Example 1 (unknown):
```unknown
## Testing Workflows {#test-workflows}

### How to mock Activities {#mock-activities}

Mock the Activity invocation when unit testing your Workflows.

When integration testing Workflows with a Worker, you can mock Activities by providing mock Activity implementations to the Worker.

Provide mock Activity implementations to the Worker.
```

---

## Temporal Platform Documentation

**URL:** llms-txt#temporal-platform-documentation

**Contents:**
- Security Controls for Temporal Cloud
- Identity and Access Management
  - Best Practices:
- Secure Application Authentication and API Access
  - Best Practices:
- Network Configuration and Isolation
  - Best Practices:
- Data Protection and Encryption
  - Best Practices:
  - Availability and Disaster Recovery

> Build invincible applications

This file contains all documentation content in a single document following the llmstxt.org standard.

## Security Controls for Temporal Cloud

Temporal Cloud provides the capabilities of Self-Hosted Temporal as a managed service; it does not manage your applications or workers. Applications and services written using Temporal SDKs still run in your compute environment, and you have full control over how you secure your applications and services.

These best practices ensure your Temporal Cloud environment adheres to the security guidelines recommended by our team. You can also learn more about our security practices, compliance posture, and subscribe for vulnerability (CVE) updates at https://trust.temporal.io/.

If you have any concerns or questions, please reach out to your Account Executive or to our security team at security@temporal.io.

**Stay Updated on Temporal Security Advisories:** 
Subscribe to Temporal’s security updates on the [Temporal Trust Portal](https://trust.temporal.io/) so you are aware of any patches or CVEs. While Temporal Cloud server-side updates are handled by the vendor, your Temporal SDKs (in application code) should be kept up-to-date.

## Identity and Access Management

Strong identity management in Temporal Cloud is crucial for ensuring secure access for your Temporal account. It’s critical that only authorized users and services can access your Temporal Cloud account and that each has the minimum necessary permissions needed for their role.

#### 1. Enable [SAML Single Sign-on](https://docs.temporal.io/cloud/saml) (SSO) for User Access

Integrate Temporal Cloud with your organization's identity provider via SAML 2.0 for centralized authentication. SSO allows you to enforce your corporate login policies (MFA, password complexity, etc.). When you configure SAML with Temporal Cloud, you can disable social logins (i.e. Microsoft, Google) by opening a support ticket.

#### 2. Use Least-Privilege Roles for Temporal Cloud Users

Temporal Cloud provides [preconfigured account-level roles](https://docs.temporal.io/cloud/users) (Account Owner, Finance Admin, Global Admin, Developer, Read-Only) and Namespace-level permissions. Assign users the lowest level of access they need. For example, give developers access only to the Namespaces they work on, and use read-only roles for auditors or reviewers. Regularly review user roles and remove or downgrade accounts that are no longer needed

#### 3. Leverage SCIM or Automated User Provisioning

When applicable, use [SCIM](https://docs.temporal.io/cloud/scim) or the Temporal Cloud user management API to automate adding and removing user accounts. This ensures timely removal of access when people change roles or leave the organization.

#### Use Service Accounts for Automation

For non-human access (CI/CD pipelines, backend services), use [Temporal Cloud Service Accounts](https://docs.temporal.io/cloud/service-accounts) instead of shared user logins. Service Accounts are machine identities that can be granted specific permissions without ties to an individual. Create separate Service Accounts with unique API keys for different applications or microservices, and apply least privilege to each (e.g. a service account that only has access to one Namespace).

## Secure Application Authentication and API Access

Clients interact with the Temporal Service to initiate and manage Workflows, while Workers execute the business logic defined in Workflows and Activities in your own environment.

A crucial aspect of strengthening your usage involves securing these interactions. Temporal Cloud offers two authentication methods for your applications: mutual TLS certificates and API keys.

#### 1. Using Mutual TLS (mTLS) provides comprehensive security

Temporal Cloud secures its gRPC endpoint per Namespace via mutual TLS. This means you provide a Certificate Authority (CA) certificate for your Namespace, and all your Temporal clients/workers must present client certificates signed by that CA.

We recommend you enable mTLS for strong identity assurance of clients; it ensures only systems holding a valid certificate (issued by your trusted CA) can connect. Generate a private key and CA certificate (or use your enterprise CA) and upload the CA to Temporal Cloud. Do not share these certificates and associated keys beyond the authorized services.

#### 2. Proactively manage and rotate certificates

Track the expiration dates of your client and [Certificate Authority certificates](https://docs.temporal.io/cloud/certificates). Temporal Cloud trusts the uploaded CA; if it expires, all client authorizations will fail. Establish and automate a certificate rotation schedule (e.g. rotate client certificates quarterly and CA certificates annually, well before expiry). Temporal supports uploading a new CA certificate alongside the old one to allow seamless rollover. Always test new certificates in a staging environment if possible.

#### 3. If you’re using API Keys, handle them with strict care

Temporal Cloud API keys are an alternative to mTLS for authentication of SDKs, CLI, and automation. If you opt for API keys, handle them with strict care by enacting the following practices: 
- Keep them secret: store in a secrets manager, never in code or Git.
- Rotate at least every 90 days: Temporal lets you create a new key, swap it in, then delete the old one.
- One key per service/person: no sharing or reuse.
- Monitor usage & revoke on anomalies: feed Temporal audit logs to SIEM.
- Optional: Admins can disable all user API keys if your policy is “mTLS only.”

## Network Configuration and Isolation

Although Temporal Cloud is a SaaS offering, you retain control over its networking configurations, allowing for tailored security measures. By minimizing public internet exposure and segmenting Temporal workflows into suitable network zones, you can significantly bolster security and reduce potential vulnerabilities. This approach ensures that your workflows are isolated and protected within your defined network boundaries, even while leveraging the benefits of a cloud-based service.

#### 1. Use Private Connectivity

Temporal Cloud supports private connectivity options such as [AWS PrivateLink](https://docs.temporal.io/cloud/connectivity/aws-connectivity) and [Google Cloud Private Service Connect](https://docs.temporal.io/cloud/connectivity/gcp-connectivity). If your infrastructure is in AWS or GCP, configure a PrivateLink/PSC endpoint for Temporal Cloud. This allows your workers and applications to reach Temporal Cloud over a private network path, avoiding traversal of the public internet. Private connectivity reduces the surface for man-in-the-middle attacks and can meet stringent network security policies.

#### 2. Separate environments by Namespace

Use [Temporal Namespaces](https://learn.temporal.io/best_practice_guides/managing_a_namespace/#2-use-domain-service-and-environment-to-name-namespaces) to isolate workflows for different environments or teams (e.g. development, staging, production). Each Namespace is logically segregated and cannot interact with others by default, providing a security boundary.

Ensure that your production Namespace uses stricter network controls (e.g. only accessible from the prod network) and that credentials for it are separate from non-prod Namespaces. This limits the impact of any compromise in a lower environment, and as workflow data is only visible to users with access to that Namespace, separating environments by Namespace also enforces data-visibility boundaries.

## Data Protection and Encryption

Temporal's data encryption capabilities ensure the security and confidentiality of your Workflows and provide protection without compromising performance. Protecting the data that you send to and store in Temporal Cloud is a joint responsibility. Temporal Cloud already encrypts all data at rest on the server side, but you can add additional layers of encryption and control.

#### 1. Enable Client-Side Encryption for Workflow Data

Temporal provides an optional [data conversion framework](https://docs.temporal.io/dataconversion) (Data Converter) and payload codec interface; customers must implement, deploy, and operate their own custom codec and manage encryption keys.

In practice, this means you can encrypt any sensitive data before it is sent to Temporal Cloud and only decrypt it on the Client/Worker side. Because encryption keys stay under your control, you are responsible for key generation, secure storage, rotation, and versioning. Implementing this involves developing a custom codec plugin in your Temporal SDK and optionally (if you need to inspect decrypted payloads in the Web UI or CLI) deploying a dedicated codec server.

#### 2. Encode Workflow Failure Details with a [Failure Converter](https://docs.temporal.io/failure-converter)

Temporal’s default behavior copies error messages and call stacks as plain text, and this text is directly accessible in the Message field of Workflow Executions.

If your failure messages and stack traces contain sensitive information, it is recommended that you configure the [Failure Converter](https://docs.temporal.io/failure-converter) to encrypt the error information. This would encrypt the `message` and `stack_trace` fields in the payloads.

#### 3. Leverage Namespace Data Retention Policies

Temporal Cloud Namespace has a [Retention Period](https://docs.temporal.io/temporal-service/temporal-server#retention-period) setting for workflow histories (1 to 90 days). Set an appropriate retention period to balance operational needs with security. Shorter retention means completed workflow data (history, payloads) is purged sooner, reducing the amount of sensitive data stored in the cloud at any time. Document your retention choices to align with your company’s data retention policies and regulatory requirements. For retention periods over 90 days, these can be exported to your own GCS or S3 buckets.

### Availability and Disaster Recovery

Temporal Cloud’s platform is engineered for fault-tolerance out of the box, but you determine which Namespaces merit the very highest availability guarantees. Use the table below to decide when to turn on different High Availability models and how to operationalise them.

| Namespace scope | Use Case | Uptime SLA | Recovery Time Objective (RTO) | Recovery Point Objective (RPO) |
|-----------------|----------|------------|--------------------------------|--------------------------------|
| **Single-Region** | **If your application is built for one region and does not have stringent high-availability or disaster recovery requirements.** | 99.9% | ≤ 8 hours | ≤ 8 hours |
| **Same-Region Replication** | **If you want higher availability but your application is designed for a single region or if cross region latency doesn’t meet SLAs for application** | 99.99% | ≤ 20 minutes | Near-zero (≈ seconds) |
| **Multi-Region Replication** | **If a disruption of your workflow will cause loss of revenue, poor end-user experience, or issues with regulatory compliance.** | 99.99% | ≤ 20 minutes | Near-zero (≈ seconds) |
| **Multi-Cloud Replication** | **If you need the highest level of disaster tolerance, protecting against outages of an entire cloud provider (e.g., AWS or GCP)** | 99.99% | ≤ 20 minutes | Near-zero (≈ seconds) |

#### 1. Identify Availability-sensitive Namespaces

Run a business-impact analysis to flag workflows where a regional outage would cause significant customer, revenue, or safety impact. Identify Namespaces that are availability-sensitive where a regional outage may have outsized business impacts such as revenue loss, poor customer experience, or inability to meet legal obligations.

#### 2. Enable High Availability for business critical use cases

For many organizations, ensuring High Availability (HA) is required because of strict uptime requirements, compliance, and regulatory needs.

For these critical use cases, enable High Availability features for specific namespaces for a [99.99% contractual SLA](https://docs.temporal.io/cloud/high-availability#high-availability-features). When choosing between [same-region, multi-region, and multi-cloud replication](https://docs.temporal.io/cloud/high-availability), it is recommended to use multi-region/multi-cloud replication to distribute your dependencies across regions. Using physically separated regions improves the fault tolerance of your application.

By default, Temporal Cloud provides a [99.9% contractual SLA guarantee](https://docs.temporal.io/cloud/high-availability) against service errors for all namespaces.

Note: [enabling HA features for namespaces will 2x the consumption cost.](https://docs.temporal.io/cloud/pricing#high-availability-features)

## Security model - Temporal Cloud

**What kind of security does Temporal Cloud provide?**

The security model of [Temporal Cloud](/cloud) encompasses applications, data, and the Temporal Cloud platform itself.

:::info General platform security

For information about the general security features of Temporal, see our [Platform security page](/security).

## Application and data {#applications-and-data}

**What is the security model for applications and data in Temporal Cloud?**

### Code execution boundaries

Temporal Cloud provides the capabilities of Temporal Server as a managed service; it does not manage your applications or [Workers](/workers#worker).
Applications and services written using [Temporal SDKs](/encyclopedia/temporal-sdks) run in your computing environment, such as containers (Docker, Kubernetes) or virtual machines (in any hosting environment).
You have full control over how you secure your applications and services.

### Data Converter: Client-side encryption

The optional [Data Conversion](/dataconversion) capability of the Temporal Platform lets you transparently encrypt data before it's sent to Temporal Cloud and decrypt it when it comes out.

Data Conversion runs on your Temporal Workers and [Clients](/encyclopedia/temporal-sdks#temporal-client); Temporal Cloud cannot see or decrypt your data.
If you use this feature, data stored in Temporal Cloud remains encrypted even if the service itself is compromised.

By deploying a [Codec Server](/production-deployment/data-encryption) you can securely decrypt data in the [Temporal Web UI](/web-ui) without sharing encryption keys with Temporal.

## The platform {#the-platform}

**What is the security model for the Temporal Cloud platform?**

### Namespace isolation

The base unit of isolation in a Temporal environment is a [Namespace](/namespaces).
Each Temporal Cloud account can have multiple Namespaces.
A Namespace (regardless of account) cannot interact with other Namespaces.
Each Namespace is available through a secure gRPC (mTLS) endpoint and an HTTPS (TLS) endpoint.
Temporal Cloud is a multi-tenant service.
Namespaces in the same environment are logically segregated.
Namespaces do not share data processing or data storage across regional boundaries.

### Private Connectivity

Temporal Cloud supports private connectivity to enable you to connect to Temporal Cloud from a secured network.

See the [Connectivity](/cloud/connectivity) page for more information and details about using AWS PrivateLink and GCP Private Service Connect with Temporal Cloud.

Like Namespaces, a Nexus Endpoint is an account-scoped resource that is global within a Temporal Cloud account.
Any Developer role (or higher) in an account, who is also a Namespace Admin on the endpoint’s target Namespace, can manage (create/update/delete) a Nexus Endpoint.
All users with a Read-only role (or higher) in an account, can view and browse the full list of Endpoints.

Runtime access from a Workflow in a caller Namespace to a Nexus Endpoint is controlled by an allowlist policy (of caller Namespaces) for each Endpoint in the Nexus API registry.
Workers authenticate with Temporal Cloud as they do today with mTLS certificates or API keys as allowed by the Namespace configuration.
Nexus requests are sent from the caller’s Namespace to the handler’s Namespace over a secure multi-region mTLS Envoy mesh.

For payload encryption, the DataConverter works the same for a Nexus Operation as it does for other payloads sent between a Worker and Temporal Cloud.

See [Nexus Security](/nexus/security) for more information.

Communication into and out of Namespaces is over TLS.
All communication within our production environments is over TLS 1.3.
Data is stored in two separate locations: an Elasticsearch instance (used when filtering Workflows in SDK clients, the [CLI](/cloud/tcld), or the Web UI) and the core Temporal Cloud persistence layer.
Both are encrypted at rest with AES-256-GCM.

For more information, see [Requirements for CA certificates in Temporal Cloud](/cloud/certificates#certificate-requirements).

Authentication to gRPC endpoints is provided by mTLS per Namespace.

For more information, see [How to manage SAML authentication with Temporal Cloud](/cloud/saml).

Authorization is managed at the account and Namespace level.
Users and systems are assigned one or more preconfigured roles.
Users hold [account-level Roles](/cloud/users#account-level-roles) of administrators, developers, and read-only users.
Systems and applications processes hold their own distinct roles.

In addition to extensive system monitoring for operational and availability requirements, we collect and monitor audit logs from the AWS environment and all calls to the gRPC API (which is used by the SDKs, CLI, and Web UI).
These audit logs can be made available for ingestion into your security monitoring system.

We contract with a third party to perform a full-scope pentest (with the exception of social engineering) annually.
Additionally, we perform targeted third-party and internal testing on an as-needed basis, such as when a significant feature is being released.

### Internal Temporal access

We restrict access to production systems to the small team of employees who maintain our production infrastructure.
We log all access to production systems; shared accounts are not allowed.
Access to all production systems is through SSO, with MFA enabled.

Access to our cloud environments is granted only for limited periods of time, with a maximum of 8 hours.
(For more information, see the blog post [Rolling out access hours at Temporal](https://temporal.io/blog/rolling-out-access-hours-at-temporal).)

All Temporal engineering systems are secured by GitHub credentials, which require both membership in the Temporal GitHub organization and MFA.
Access grants are reviewed quarterly.

Temporal Technologies is SOC 2 Type 2 certified and compliant with GDPR and HIPAA regulations.
Compliance audits are available by request through our [Contact](https://pages.temporal.io/contact-us) page.

## Security - Temporal Nexus

:::tip SUPPORT, STABILITY, and DEPENDENCY INFO

Temporal Nexus is now [Generally Available](/evaluate/development-production-features/release-stages#general-availability).
Learn why you should use Nexus in the [evaluation guide](/evaluate/nexus).

Temporal Cloud has built-in Nexus security.
It provides secure Nexus connectivity across Namespaces with an mTLS secured Envoy mesh.
Workers authenticate to their Namespace with mTLS client certificates or API keys, as allowed by their Namespace.
Encryption for Nexus payloads is also supported, for example using shared symmetric keys and compatible Data Converters.

## Registry roles and permissions

Nexus Endpoints are Account-scoped resources, similar to a Namespace.
The following roles and permissions are required to manage and view Nexus Endpoints in the Nexus Registry:

- Viewing and browsing the full list of Nexus Endpoints in an Account:
  - Read-only role (or higher)
- Managing a Nexus Endpoint (create, update, delete):
  - Developer role (or higher) and Namespace Admin permission on the Endpoint’s target Namespace

## Runtime access controls

The Nexus Registry allows setting Endpoint access policy on each Endpoint.
This currently includes an allow list of caller Namespaces that can use the Endpoint at runtime.
Endpoint access control policies are enforced at runtime:

1. Caller's Worker authenticates with their Namespace as they do today with mTLS certificates or API keys.
   This establishes the caller's identity and caller Namespace.
2. Caller Workflow executes a Nexus Operation on a Nexus Endpoint.
3. Endpoint access control policy is enforced, checking if the caller Namespace is in the Endpoint allow list.

See [Runtime Access Controls](/nexus/security#runtime-access-controls) and [Configuring Runtime Access Controls](/nexus/registry#configure-runtime-access-controls) for additional details.

## Secure connectivity

Nexus Endpoints are only privately accessible from within a Temporal Cloud and mTLS is used for all Nexus communication, including across cloud cells and regions.
Workers authenticate to their Namespaces through mTLS or an API key as allowed by their Namespace configuration.

<CaptionedImage
    src="/img/cloud/nexus/nexus-workers-short.png"
    title="Nexus Security"
/>

See [Nexus Secure Connectivity](/nexus/security#secure-connectivity) for additional details.

## Payload encryption

For payload encryption, the DataConverter works the same for a Nexus Operation as it does for other payloads sent between a Worker and Temporal Cloud.

See [Nexus Payload Encryption & Data Converter](/nexus/security#payload-encryption-data-converter) for additional details.

## Temporal Platform security features

:::info General company security

For information about the general security habits of Temporal Technologies, see our [trust page](https://trust.temporal.io).

:::info Cloud security

For information about Temporal Cloud security features, see our [Cloud security page](/cloud/security)
:::

The Temporal Platform is designed with security in mind, and there are many features that you can use to keep both the Platform itself and your user's data secure.

A secured Temporal Server has its network communication encrypted and has authentication and authorization protocols set up for API calls made to it.
Without these, your server could be accessed by unwanted entities.

What is documented on this page are the built-in opt-in security measures that come with Temporal.
However users may also choose to design their own security architecture with reverse proxies or run unsecured instances inside of a VPC environment.

The https://github.com/temporalio/samples-server repo offers two examples, which are further explained below:

- **TLS:** how to configure Transport Layer Security (TLS) to secure network communication with and within a Temporal Service.
- **Authorizer:** how to inject a low-level authorizer component that can control access to all API calls.

### Encryption in transit with mTLS

Temporal supports Mutual Transport Layer Security (mTLS) as a way of encrypting network traffic between the services of a Temporal Service and also between application processes and a Temporal Service.
Self-signed or properly minted certificates can be used for mTLS.
mTLS is set in Temporal's [TLS configuration](/references/configuration#tls).
The configuration includes two sections such that intra-Temporal Service and external traffic can be encrypted with different sets of certificates and settings:

- `internode`: Configuration for encrypting communication between nodes in the Temporal Service.
- `frontend`: Configuration for encrypting the Frontend's public endpoints.

A customized configuration can be passed using either the [WithConfig](/references/server-options#withconfig) or [WithConfigLoader](/references/server-options#withconfigloader) Server options.

See [TLS configuration reference](/references/configuration#tls) for more details.

There are a few authentication protocols available to prevent unwanted access such as authentication of servers, clients, and users.

To prevent spoofing and [MITM attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) you can specify the `serverName` in the `client` section of your respective mTLS configuration.
This enables established connections to authenticate the endpoint, ensuring that the server certificate presented to any connecting Client has the appropriate server name in its CN property.
It can be used for both `internode` and `frontend` endpoints.

More guidance on mTLS setup can be found in [the `samples-server` repo](https://github.com/temporalio/samples-server/tree/main/tls) and you can reach out to us for further guidance.

### Client connections

To restrict a client's network access to Temporal Service endpoints you can limit it to clients with certificates issued by a specific Certificate Authority (CA).
Use the `clientCAFiles`/ `clientCAData` and `requireClientAuth` properties in both the `internode` and `frontend` sections of the [mTLS configuration](/references/configuration#tls).

To restrict access to specific users, authentication and authorization is performed through extensibility points and plugins as described in the [Authorization](#authorization) section below.

:::note
Information regarding [`Authorizer`](#authorizer-plugin) and [`ClaimMapper`](#claim-mapper) has been moved to another location.
:::

Temporal offers two plugin interfaces for implementing API call authorization:

- [`ClaimMapper`](#claim-mapper)
- [`Authorizer`](#authorizer-plugin)

The authorization and claim mapping logic is customizable, making it available to a variety of use cases and identity schemes.
When these are provided the frontend invokes the implementation of these interfaces before executing the requested operation.

See https://github.com/temporalio/samples-server/blob/main/extensibility/authorizer for a sample implementation.

<CaptionedImage
    src="/diagrams/frontend-authorization-order-of-operations.png"
    title="Front-end authorization order of operations"
/>

### Single sign-on integration

Temporal can be integrated with a single sign-on (SSO) experience by using the `ClaimMapper` and `Authorizer` plugins.
The default JWT `ClaimMapper` implementation can be used as is or as a base for a custom implementation of a similar plugin.

To enable SSO authentication in the Temporal UI using environment credentials, you need to configure the UI container with specific environment variables that define your identity provider and OAuth settings.
In your docker-compose.yaml, set `TEMPORAL_AUTH_ENABLED=true` to activate authentication.
Next, specify the required OAuth credentials and endpoints using environment variables such as:

- `TEMPORAL_AUTH_CLIENT_ID`
- `TEMPORAL_AUTH_CLIENT_SECRET`
- `TEMPORAL_AUTH_PROVIDER_URL`
- `TEMPORAL_AUTH_CALLBACK_URL`

These values correspond to the client credentials and endpoints provided by your OAuth identity provider (such as Google, Auth0, Okta).
When properly configured, Temporal UI will redirect users to your SSO login page and enforce authentication on access.
This approach does not require any additional configuration files, making it ideal for containerized environments using secure environment variable injection.

For more general guidance for configuration, refer to the [Temporal UI README](https://github.com/temporalio/ui?tab=readme-ov-file#configuration).
For more details on configuration with Docker, refer to [Temporal UI Config](https://github.com/temporalio/ui/blob/c95265ee6431fd0f6cf78ae06373885d66a8ee0c/server/docker/config-template.yaml).

## Temporal Service plugins {#plugins}

The Temporal Service supports some pluggable components.

### What is a ClaimMapper Plugin? {#claim-mapper}

The Claim Mapper component is a pluggable component that extracts Claims from JSON Web Tokens (JWTs).

This process is achieved with the method `GetClaims`, which translates `AuthInfo` structs from the caller into `Claims` about the caller's roles within Temporal.

A `Role` (within Temporal) is a bit mask that combines one or more of the role constants.
In the following example, the role is assigned constants that allow the caller to read and write information.

`GetClaims` is customizable and can be modified with the `temporal.WithClaimMapper` server option.
Temporal also offers a default JWT `ClaimMapper` for your use.

A typical approach is for `ClaimMapper` to interpret custom `Claims` from a caller's JWT, such as membership in groups, and map them to Temporal roles for the user.
The subject information from the caller's mTLS certificate can also be a parameter in determining roles.

`AuthInfo` is a struct that is passed to `GetClaims`. `AuthInfo` contains an authorization token extracted from the `authorization` header of the gRPC request.

`AuthInfo` includes a pointer to the `pkix.Name` struct.
This struct contains an [x.509](https://www.ibm.com/docs/en/ibm-mq/7.5?topic=certificates-distinguished-names) Distinguished Name from the caller's mTLS certificate.

`Claims` is a struct that contains information about permission claims granted to the caller.

`Authorizer` assumes that the caller has been properly authenticated, and trusts the `Claims` when making an authorization decision.

#### Default JWT ClaimMapper

Temporal offers a default JWT `ClaimMapper` that extracts the information needed to form Temporal `Claims`.
This plugin requires a public key to validate digital signatures.

To get an instance of the default JWT `ClaimMapper`, call `NewDefaultJWTClaimMapper` and provide it with the following:

- a `TokenKeyProvider` instance
- a `config.Authorization` pointer
- a logger

The code for the default `ClaimMapper` can also be used to build a custom `ClaimMapper`.

#### Token key provider

A `TokenKeyProvider` obtains public keys from specified issuers' URIs that adhere to a specific format.
The default JWT `ClaimMapper` uses this component to obtain and refresh public keys over time.

Temporal provides a `defaultTokenKeyProvider`.
This component dynamically obtains public keys that follow the [JWKS format](https://tools.ietf.org/html/rfc7517).
It supports formats such as `RSA` and `ECDSA`.

`KeySourceURIs` are the HTTP endpoints that return public keys of token issuers in the [JWKS format](https://tools.ietf.org/html/rfc7517).
`RefreshInterval` defines how frequently keys should be refreshed.
For example, [Auth0](https://auth0.com/) exposes endpoints such as `https://YOUR_DOMAIN/.well-known/jwks.json`.

By default, "permissions" is used to name the `permissionsClaimName` value.

Configure the plugin with `config.Config.Global.Authorization.JWTKeyProvider`.

#### JSON Web Token format

The default JWT `ClaimMapper` expects authorization tokens to be formatted as follows:

The Permissions Claim in the JWT Token is expected to be a collection of Individual Permission Claims.
Each Individual Permission Claim must be formatted as follows:

These permissions are then converted into Temporal roles for the caller.
This can be one of Temporal's four values:

- read
- write
- worker
- admin

Multiple permissions for the same Namespace are overridden by the `ClaimMapper`.

##### Example of a payload for the default JWT ClaimMapper

### What is an Authorizer Plugin? {#authorizer-plugin}

The `Authorizer` plugin contains a single `Authorize` method, which is invoked for each incoming API call.
`Authorize` receives information about the API call, along with the role and permission claims of the caller.

`Authorizer` allows for a wide range of authorization logic, including call target, role/permissions claims, and other data available to the system.

The following arguments must be passed to `Authorizer`:

- `context.Context`: General context of the call.
- `authorization.Claims`: Claims about the roles assigned to the caller. Its intended use is described in the [`Claims`](#claims) section earlier on this page.
- `authorization.CallTarget`: Target of the API call.

`Authorizer` then returns one of two decisions:

- `DecisionDeny`: the requested API call is not invoked and an error is returned to the caller.
- `DecisionAllow`: the requested API call is invoked.

:::warning Security Warning

If you do **not** explicitly configure an `Authorizer`, Temporal uses the default `noopAuthorizer`. This default allows **every** API request,
with no authentication or access control. Anyone who can reach your Temporal Server can invoke any API, including sensitive administrative operations.
This is **not secure** for production or for any environment that is accessible to untrusted clients (such as over the internet).

**To protect your Temporal Server, you must configure an `Authorizer` plugin with a corresponding `ClaimMapper`.** Without this, your deployment is
effectively open to anyone with network access.

Configure your `Authorizer` with the [`temporal.WithAuthorizer`](/references/server-options#withauthorizer) server option, and your `ClaimMapper` with
the [`temporal.WithClaimMapper`](/references/server-options#withclaimmapper) server option.

#### How to authorize SDK API calls {#authorize-api-calls}

When authentication is enabled, you can authorize API calls made to the Frontend Service.

The Temporal Server [expects](#authentication) an `authorization` gRPC header with an authorization token to be passed with API calls if [requests authorization](#authorization) is configured.

Authorization Tokens may be provided to the Temporal Java SDK by implementing a `io.temporal.authorization.AuthorizationTokenSupplier` interface.
The implementation should be used to create `io.temporal.authorization.AuthorizationGrpcMetadataProvider` that may be configured on ServiceStub gRPC interceptors list.

The implementation is called for each SDK gRPC request and may supply dynamic tokens.

One of the token types that may be passed this way are JWT tokens.
Temporal Server provides a [default implementation of JWT authentication](#default-jwt-claimmapper).

- [How to secure a Temporal Service](/security)

## Data Converter {#data-converter}

Each Temporal SDK provides a [Data Converter](/dataconversion) that can be customized with a custom [Payload Codec](/payload-codec) to encode and secure your data.

For details on what data can be encoded, how to secure it, and what to consider when using encryption, see [Data encryption](/production-deployment/data-encryption).

You can use a [Codec Server](/codec-server) with your custom Payload Codec to decode the data you see on your Web UI and CLI locally through remote endpoints.
However, ensure that you consider all security implications of [remote data encoding](/remote-data-encoding) before using a Codec Server.

For details on how to set up a Codec Server, see [Codec Server setup](/production-deployment/data-encryption#codec-server-setup).

## Temporal Platform security

Find security information for your Temporal deployment, whether you're using Temporal Cloud or self-hosting.

Company Security
      Learn about Temporal Technologies' general security practices, compliance certifications, and organizational security measures.

Temporal Cloud Security
      Explore the security features of our SaaS offering, including mTLS, end-to-end encryption, and enterprise compliance.

Self-Hosted Security
      Discover how to deploy and secure your own Temporal Platform infrastructure with production-ready best practices.

Temporal Cloud Security Whitepaper
      Learn how Temporal Cloud provides provable security by design - orchestrating encrypted workflows without ever accessing your sensitive data.

<style jsx>{`
  .security-cards-container {
    margin: 2rem 0;
  }

.security-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

.security-card {
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
    border: 1px solid #e1e8ed;
    border-radius: 12px;
    padding: 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    position: relative;
    overflow: hidden;
  }

.security-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #444ce7 0%, #b664ff 100%);
  }

.security-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(68, 76, 231, 0.12);
    border-color: #444ce7;
  }

.security-card-header h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.375rem;
    font-weight: 600;
    color: #1a1b23;
    line-height: 1.3;
  }

.security-card-divider {
    width: 40px;
    height: 3px;
    background: linear-gradient(90deg, #444ce7 0%, #b664ff 100%);
    border-radius: 2px;
    margin-bottom: 1.5rem;
  }

.security-card-body p {
    color: #5d6b7d;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
  }

.security-card-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: #444ce7;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    padding: 0.5rem 0;
  }

.security-card-button:hover {
    color: #3730a3;
    text-decoration: none;
    transform: translateX(2px);
  }

.security-card-button svg {
    transition: transform 0.2s ease;
  }

.security-card-button:hover svg {
    transform: translateX(2px);
  }

@media (max-width: 768px) {
    .security-cards-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

.security-card {
      padding: 1.5rem;
    }
  }
`}</style>

## Temporal Web UI configuration reference

The Temporal Web UI Server uses a configuration file for many of the UI's settings.

An example development.yaml file can be found in the [temporalio/ui-server repo](https://github.com/temporalio/ui-server/blob/main/config/development.yaml).

Multiple configuration files can be created for configuring specific areas of the UI, such as Auth or TLS.

Configures authorization for the Temporal Server.
Settings apply when Auth is enabled.

## batchActionsDisabled

Prevents the execution of Batch actions.

Enables the Cloud UI.

Codec Server configuration.

The name of the `cors` field stands for Cross-Origin Resource Sharing.
Use this field to provide a list of domains that are authorized to access the UI Server APIs.

The default Namespace that the UI loads data for.
Defaults to `default`.

## disableWriteActions

Prevents the user from executing Workflow Actions on the Web UI.

This option affects Bulk Actions for Recent Workflows as well as Workflow Actions on the Workflow Details page.

:::note
`disableWriteActions` overrides the configuration values of each individual Workflow Action.
Setting this variable to `true` disables all Workflow Actions on the Web UI.
:::

Enables the browser UI.
This configuration can be set dynamically with the [TEMPORAL_UI_ENABLED](/references/web-ui-environment-variables#temporal_ui_enabled) environment variable.
If disabled—that is, set to `false`—the UI server APIs remain available.

The URL to direct users to when they click on the Feedback button in the UI.
If not specified, it defaults to the UI's GitHub Issue page.

Configures headers for forwarding.

If enabled, disables any server logs from being printed to the console.

## hideWorkflowQueryErrors

Hides any errors resulting from a Query to the Workflow.

## notifyOnNewVersion

When enabled—that is, when set to `true`—a notification appears in the UI when a newer version of the [Temporal Server](/temporal-service/temporal-server) is available.

The port used by the Temporal Web UI Server and any APIs.

The path used by the Temporal Web UI Server and any APIs.

How often the configuration UI Server reads the configuration file for new values.
Currently, only [tls](#tls) configuration values are propagated during a refresh.

## showTemporalSystemNamespace

When enabled—that is, when set to `true`—the Temporal System Namespace becomes visible in the UI.
The Temporal System Namespace lists Workflow Executions used by the Temporal Platform.

## temporalGrpcAddress

The frontend address for the Temporal Cluster.

The default address is localhost (127.0.0.1:7233).

Transport Layer Security (TLS) configuration for the Temporal Server.
Settings apply when TLS is enabled.

## workflowCancelDisabled

Prevents the user from canceling Workflow Executions from the Web UI.

## workflowResetDisabled

Prevents the user from resetting Workflows from the Web UI.

## workflowSignalDisabled

Prevents the user from signaling Workflow Executions from the Web UI.

## workflowTerminateDisabled

Prevents the user from terminating Workflow Executions from the Web UI.

## Temporal Web UI environment variables reference

You can use environment variables to dynamically alter the configuration of your Temporal Web UI.

These can be used in many environments, such as with Docker. For example:

The environment variables are defined in the
[UI server configuration template file](https://github.com/temporalio/ui-server/blob/main/config/docker.yaml)
and described in more detail below.

## `TEMPORAL_ADDRESS`

The [Frontend Service](/temporal-service/temporal-server#frontend-service) address for the Temporal Cluster. This
variable can be set [in the base configuration file](/references/web-ui-configuration#temporalgrpcaddress) using
`temporalGrpcAddress`.

This variable is required for setting other environment variables.

## `TEMPORAL_UI_PORT`

The port used by the Temporal WebUI Server and the HTTP API.

This variable is needed for `TEMPORAL_OPENAPI_ENABLED` and all auth-related settings to work properly.

## `TEMPORAL_UI_PUBLIC_PATH`

Stores a value such as "" or "/custom-path" that allows the UI to be served from a subpath.

## `TEMPORAL_UI_ENABLED`

Enables or disables the [browser UI](/references/web-ui-configuration#enableui) for the Temporal Cluster.

Enabling the browser UI allows the Server to be accessed from your web browser. If disabled, the server cannot be viewed
on the web, but the UI server APIs remain available for use.

## `TEMPORAL_BANNER_TEXT`

Provides banner text to display on the Web UI.

## `TEMPORAL_CLOUD_UI`

If enabled, use the alternate UI from Temporal Cloud.

## `TEMPORAL_DEFAULT_NAMESPACE`

The default [Namespace](/namespaces) that the Web UI opens first.

## `TEMPORAL_FEEDBACK_URL`

The URL that users are directed to when they click the Feedback button in the UI.

If not specified, this variable defaults to the UI's GitHub Issue page.

## `TEMPORAL_NOTIFY_ON_NEW_VERSION`

Enables or disables notifications that appear in the UI whenever a newer version of the Temporal Cluster is available.

## `TEMPORAL_CONFIG_REFRESH_INTERVAL`

Determines how often the UI Server reads the configuration file for new values.

## `TEMPORAL_SHOW_TEMPORAL_SYSTEM_NAMESPACE`

If enabled, shows the System Namespace that handles internal Temporal Workflows in the Web UI.

## `TEMPORAL_DISABLE_WRITE_ACTIONS`

Disables any button in the UI that allows the user to modify Workflows or Activities.

## `TEMPORAL_AUTH_ENABLED`

Enables or disables Web UI authentication and authorization methods.

When enabled, the Web UI will use the provider information in the
[UI configuration file](/references/web-ui-configuration#auth) to verify the identity of users.

All auth-related variables can be defined when `TEMPORAL_AUTH_ENABLED` is set to "true". Disabling the variable will
retain given values.

## `TEMPORAL_AUTH_TYPE`

Specifies the type of authentication. Defaults to `oidc`.

## `TEMPORAL_AUTH_PROVIDER_URL`

The .well-known IDP discovery URL for authentication and authorization.

This can be set as in the UI server configuration with [auth](/references/web-ui-configuration#auth).

## `TEMPORAL_AUTH_ISSUER_URL`

The URL for the authentication or authorization issuer.

This value is only needed when the issuer differes from the auth provider URL.

## `TEMPORAL_AUTH_CLIENT_ID`

The client ID used for authentication or authorization.

This value is a required parameter.

## `TEMPORAL_AUTH_CLIENT_SECRET`

The client secret used for authentication and authorization.

Client Secrets are used by the oAuth Client for authentication.

## `TEMPORAL_AUTH_CALLBACK_URL`

The callback URL used by Temporal for authentication and authorization.

Callback URLs are invoked by IDP after user has finished authenticating in IDP.

## `TEMPORAL_AUTH_SCOPES`

Specifies a set of scopes for auth. Typically, this is `openid`, `profile`, `email`.

The path for the Transport Layer Security (TLS) Certificate Authority file.

In order to [configure TLS for your server](/references/web-ui-configuration#tls), you'll need a CA certificate issued
by a trusted Certificate Authority. Set this variable to properly locate and use the file.

## `TEMPORAL_TLS_CERT`

The path for the Transport Layer Security (TLS) Certificate.

In order to [configure TLS for your server](/references/web-ui-configuration#tls), you'll need a self-signed
certificate. Set the path to allow the environment to locate and use the certificate.

## `TEMPORAL_TLS_KEY`

The path for the Transport Layer Security (TLS) [key file](/references/web-ui-configuration#tls).

A key file is used to create private and public keys for encryption and signing. Together, these keys are used to create
certificates.

## `TEMPORAL_TLS_CA_DATA`

Stores the data for a TLS CA file.

This variable can be used instead of providing a path for `TEMPORAL_TLS_CA`.

## `TEMPORAL_TLS_CERT_DATA`

Stores the data for a TLS cert file.

This variable can be used instead of providing a path for `TEMPORAL_TLS_CERT`.

## `TEMPORAL_TLS_KEY_DATA`

Stores the data for a TLS key file.

This variable can be used instead of providing a path for `TEMPORAL_TLS_KEY`.

## `TEMPORAL_TLS_ENABLE_HOST_VERIFICATION`

Enables or disables [Transport Layer Security (TLS) host verification](/references/web-ui-configuration#tls).

When enabled, TLS checks the Host Server to ensure that files are being sent to and from the correct URL.

## `TEMPORAL_TLS_SERVER_NAME`

The server on which to operate [Transport Layer Security (TLS) protocols](/references/web-ui-configuration#tls).

TLS allows the current server to transmit encrypted files to other URLs without having to reveal itself. Because of
this, TLS operates a go-between server.

## `TEMPORAL_CODEC_ENDPOINT`

The endpoint for the [Codec Server](/codec-server), if configured.

## `TEMPORAL_CODEC_PASS_ACCESS_TOKEN`

Specifies whether to send a JWT access token as ‘authorization' header in requests with the Codec Server.

## `TEMPORAL_CODEC_INCLUDE_CREDENTIALS`

Specifies whether to include credentials along with requests to the Codec Server.

## `TEMPORAL_FORWARD_HEADERS`

Forward-specified HTTP headers to direct from HTTP API requests to the Temporal gRPC backend. This is a
comma-delimited list of the HTTP headers to be forwarded.

## `TEMPORAL_HIDE_LOGS`

If enabled, does not print logs from the Temporal Service.

The Temporal Web UI provides users with Workflow Execution state and metadata for debugging purposes. It ships with
every [Temporal CLI](/cli) release and [Docker Compose](https://github.com/temporalio/docker-compose) update and is
available with [Temporal Cloud](/cloud).

You can configure the Temporal Web UI to work in your own environment. See the
[UI configuration reference](/references/web-ui-configuration).

Web UI open source repos:

- [temporalio/ui](https://github.com/temporalio/ui)
- [temporalio/ui-server](https://github.com/temporalio/ui-server)

All Namespaces in your self-hosted Temporal Service or Temporal Cloud account are listed under **Namespaces** in the
left section of the window. You can also switch Namespaces from the Workflows view by selecting from the Namespace
switcher at the top right corner of the window. After you select a Namespace, the Web UI shows the Recent Workflows page
for that Namespace. In Temporal Cloud, users can access only the Namespaces that they have been granted access to. For
details, see [Namespace-level permissions](/cloud/users#namespace-level-permissions).

The main Workflows page displays a table of all Workflow Executions within the retention period.

Users can list Workflow Executions by any of the following:

- [Status](/workflow-execution#workflow-execution-status)
- [Workflow ID](/workflow-execution/workflowid-runid#workflow-id)
- [Workflow Type](/workflow-definition#workflow-type)
- Start time
- End time
- Any other Default or Custom [Search Attribute](/search-attribute) that uses [List Filter](/list-filter)

For start time and end time, users can set their preferred date and time format as one of the following:

- UTC
- Local
- Relative

Select a Workflow Execution to view the Workflow Execution's History, Workers, Relationships, pending Activities and
Nexus Operations, Queries, and Metadata.

### Saved Views {#saved-views}

Saved Views let you save and reuse your frequently used visibility queries in the Temporal Web UI. Instead of recreating
complex filters every time, you can save them once and apply them with a single click.

Saved Views are stored locally in your browser and are available to you whenever you use the Temporal Web UI in this
browser. Each user will have their own private collection.

#### Apply a Saved View

By default, The Workflows page has several default Saved Views. You can also create your own Saved Views.

Click the name of a Saved View in the list to display the corresponding Workflows that match the query.

The Workflow List page will refresh with the results of the Saved View.

#### Create a Saved View

You can create a new Saved View from the Workflows page.

1. Create a Saved View by using the filter UI to build your criteria, or you can use the raw query editor to write
   custom query strings.
1. Your new view will appear in the Custom Views list as New View. Click the Save as New button to bring up the Save as
   View window. Name your Saved View. Names must be unique to each user and can contain a max of 255 characters.
1. Click Save. Your new view will appear in the Custom Views list

You can create up to 20 Saved Views. When you reach this limit, you'll need to delete some Saved Views before you can
save new ones.

#### Make Temporary Changes to a Saved View query

You can modify a Saved View temporarily without changing the saved criteria.

1. Select the Saved View you want to change.
1. Adjust the UI filters as needed.
1. The Workflows page will refresh with the results of the new query, without changing the Saved View.
1. If you want to keep your temporary changes, you can:
   - Click Save, which will replace the original Saved View with your modifications.
   - Click Edit, modify the name, and click Save, which will replace the original Saved View with your modifications and
     change the name.
   - Click Edit, modify the name, and click Create New, which will create a new Saved View with your new settings and a
     new name.

#### Rename a Saved View Query

You can rename an existing Saved View from the Workflows page.

1. Select the Saved View you want to change.
1. Click Edit.
1. In the Edit View dialog box, enter a new name for the Saved View.
1. Click Save to apply your changes and rename the existing Saved View, or click Create Copy to create a new Saved View
   with the new name.

#### Deleting Saved Views

You can delete a Saved View from the Workflows page, because it is no longer useful, or to create room for new Saved
Views.

1. Select the Saved View you want to delete. You can only delete queries you’ve created; you cannot delete the system
   defaults.
1. Click “Edit” and then "Delete this Saved View".

:::note Deleting Saved Views is permanent

Deleted queries cannot be recovered, so make sure you won't need them again. If you accidentally delete a Saved List,
you will need to recreate it.

#### Share a Saved View

You can share a Saved View as a URL.

1. Select the Saved View you want to share.
1. Click the “Share” button to copy the URL for this Saved View to the clipboard. You can also copy the URL directly
   from the browser.

:::note Saved Views and time

Saved Views that use relative times will be shared with absolute time.

## Task Failures View {#task-failures-view}

The Task Failures view is a pre-defined Saved View that displays Workflows that have a Workflow Task failure.
These Workflows are still running, but one of their Tasks has failed or timed out.

The details of the Task Failures view displays the Workflow's ID, the Run ID, and the Workflow type. 
Clicking on any of the links in the details opens the Workflow page for that Workflow. 
On this page, you will find more information about the Task that failed and remaining pending tasks.
You can also cancel the Workflow by clicking the Request Cancellation button on this page.

Our system monitors Workflow task execution patterns in real-time. When a Workflow experiences five consecutive task failures or timeouts, it gets automatically flagged. The moment the Workflow recovers with a successful task, the flag clears. This smart threshold filters out minor glitches while surfacing Workflows with genuine problems.

### Activating Task Failures View {#activate-task-failures-view}

This is enabled by default for Temporal Cloud users. If you're self-hosting Temporal, you'll need to update the `system.numConsecutiveWorkflowTaskProblemsToTriggerSearchAttribute` [dynamic config](/references/dynamic-configuration).

Here's an example of how to make the config update for the dev server:

`numConsecutiveWorkflowTaskProblemsToTriggerSearchAttribute` is the number of consecutive Workflow Task Failures required to trigger the `TemporalReportedProblems` search attribute. The default value is 5. If adding this search attribute causes strain on the visibility system, consider increasing this number.

To turn off the feature for a Namespace, set `numConsecutiveWorkflowTaskProblemsToTriggerSearchAttribute` to 0.

A Workflow Execution History is a view of the [Events](/workflow-execution/event#event) and Event fields within the
Workflow Execution. Approximately [40 different Events](/references/events) can appear in a Workflow Execution's Event
History.

The top of the page lists the following execution metadata:

- Start Time, Close Time and Duration
- [Run Id](/workflow-execution/workflowid-runid#run-id)
- [Workflow Type](/workflow-definition#workflow-type)
- [Task Queue](/task-queue)
- Parent and Parent ID
- SDK
- [State Transitions](/workflow-execution#state-transition)
- [Billable Actions Count](/cloud/actions#actions-in-workflows) (Temporal Cloud only)

The Input and Results section displays the function arguments and return values for debugging purposes. Results are not
available until the Workflow finishes.

The History tab has the following views:

- Timeline: A chronological or reverse-chronological order of events with a summary. Clicking into an Event displays all
  details for that Event.
- All: View all History Events.
- Compact: A logical grouping of Activities, Signals and Timers.
- JSON: The full JSON code for the workflow.

### Download Event History

The entire Workflow Execution Event History, in JSON format, can be downloaded from this section.

Workflow Executions can request a Cancellation, send a Signal or Update, or Reset and Terminate directly from the UI.
Start a new Workflow Execution with pre-filled values with the Start Workflow Like This One button.

Displays the full hierarchy of a Workflow Execution with all parent and child nodes displayed in a tree.

Displays the Workers currently polling on the Workflow Task Queue with a count. If no Workers are polling, an error
displays.

### Pending Activities

Displays a summary of recently active and/or pending Activity Executions. Clicking a pending Activity directs the user
to the Pending Activities tab to view details.

The screen shows the captured result from the [\_\_stack_trace](/sending-messages#stack-trace-query) Query. The Query is
performed when the tab is selected. It works only if a Worker is running and available to return the call stack. The
call stack shows each location where Workflow code is waiting.

Lists all Queries sent to the Workflow Execution.

Displays User Metadata including static Workflow Summary and Details and dynamic Current Details. Lists all Events with
User Metadata data to give you a human-readable log of what's happening in your Workflow.

On Temporal Cloud and self-hosted Temporal Service Web UI, the Schedules page lists all the [Schedules](/schedule)
created on the selected Namespace.

Click a Schedule to see details, such as configured frequency, start and end times, and recent and upcoming runs.

:::tip Setting Schedules with Strings

Temporal Workflow Schedule Cron strings follow this format:

To read more about Schedules, explore these links:

<RelatedReadContainer>
  <RelatedReadItem path="/develop/go/schedules" text="Schedules using the Go SDK" archetype="feature-guide" />
  <RelatedReadItem path="/develop/java/schedules" text="Schedules using the Java SDK" archetype="feature-guide" />
  <RelatedReadItem path="/develop/php/schedules" text="Schedules using the PHP SDK" archetype="feature-guide" />
  <RelatedReadItem path="/develop/python/schedules" text="Schedules using the Python SDK" archetype="feature-guide" />
  <RelatedReadItem
    path="/develop/typescript/schedules"
    text="Schedules using the TypeScript SDK"
    archetype="feature-guide"
  />
  <RelatedReadItem path="/develop/dotnet/schedules" text="Schedules using the .NET SDK" archetype="feature-guide" />
</RelatedReadContainer>

On Temporal Cloud, **Settings** is visible only to Account Owner and Global Admin
[roles](/cloud/users#account-level-roles).

Click **Settings** to see and manage the list of users in your account and to set up integrations such as
[Observability](/cloud/metrics) and [Audit logging](/cloud/audit-logs).

On a self-hosted Temporal Service, manage your users, metrics, and logging in your
[server configuration](/references/configuration).

On a self-hosted Temporal Service, Archive shows [Archived](/temporal-service/archival) data of your Workflow Executions
on the Namespace.

To see data in your self-hosted Temporal Service, you must have
[Archival set up and configured](/self-hosted-guide/archival).

For information and details on the Archive feature in Temporal Cloud, contact your Temporal representative.

The Web UI can use a [Codec Server](/codec-server) with a custom Data Converter to decode inputs and return values. For
details, see [Securing your data](/production-deployment/data-encryption).

The UI supports a [Codec Server endpoint](/production-deployment/data-encryption#web-ui). For details on setting the
Codec Server endpoint, see [Codec Server setup](/production-deployment/data-encryption#codec-server-setup).

The following terms are used in [Temporal Platform](/temporal) documentation.

#### [Action](/cloud/pricing#action)

An Action is the fundamental pricing unit in Temporal Cloud. Temporal Actions are the building blocks for Workflow
Executions. When you execute a Temporal Workflow, its Actions create the ongoing state and progress of your Temporal
Application.

<!-- _Tags: [term](/tags/term), [pricing](/tags/pricing), [temporal-cloud](/tags/temporal-cloud), [explanation](/tags/explanation)_ -->

#### [Actions Per Second (APS)](/cloud/limits#actions-per-second)

APS, or Actions per second, is specific to Temporal Cloud. Each Temporal Cloud Namespace enforces a rate limit, which is
measured in Actions per second (APS). This is the number of Actions, such as starting or signaling a Workflow, that can
be performed per second within a specific Namespace.

<!-- _Tags: [term](/tags/term), [pricing](/tags/pricing), [temporal-cloud](/tags/temporal-cloud), [explanation](/tags/explanation)_ -->

#### [Activity](/activities)

In day-to-day conversation, the term "Activity" denotes an Activity Type, Activity Definition, or Activity Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Activity Definition](/activity-definition)

An Activity Definition is the code that defines the constraints of an Activity Task Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Activity Execution](/activity-execution)

An Activity Execution is the full chain of Activity Task Executions.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Activity Heartbeat](/encyclopedia/detecting-activity-failures#activity-heartbeat)

An Activity Heartbeat is a ping from the Worker that is executing the Activity to the Temporal Service.

Each ping informs the Temporal Service that the Activity Execution is making progress and the Worker has not crashed.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Activity Id](/activity-execution#activity-id)

A unique identifier for an Activity Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Activity Task](/tasks#activity-task)

An Activity Task contains the context needed to make an Activity Task Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Activity Task Execution](/tasks#activity-task-execution)

An Activity Task Execution occurs when a Worker uses the context provided from the Activity Task and executes the
Activity Definition.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Activity Type](/activity-definition#activity-type)

An Activity Type is the mapping of a name to an Activity Definition.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Archival](/temporal-service/archival)

Archival is a feature specific to a Self-hosted Temporal Service that automatically backs up Event Histories from
Temporal Service persistence to a custom blob store after the Closed Workflow Execution retention period is reached.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Asynchronous Activity Completion](/activity-execution#asynchronous-activity-completion)

Asynchronous Activity Completion occurs when an external system provides the final result of a computation, started by
an Activity, to the Temporal System.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Audit Logging](/cloud/audit-logs)

Audit Logging is a feature that provides forensic access information for accounts, users, and Namespaces.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [temporal-cloud](/tags/temporal-cloud), [operations](/tags/operations)_ -->

#### [Authorizer Plugin](/self-hosted-guide/security#authorizer-plugin)

The `Authorizer` plugin contains a single `Authorize` method, which is invoked for each incoming API call. `Authorize`
receives information about the API call, along with the role and permission claims of the caller.

<!-- _Tags: [term](/tags/term)_ -->

#### [Availability Zone](/cloud/high-availability)

An availability zone is a part of the Temporal system where tasks or operations are handled and executed. This design
helps manage workloads and ensure tasks are completed. Temporal Cloud Namespaces are automatically distributed across
three availability zones, offering the 99.9% uptime outlined in our Cloud [SLA](/cloud/sla).

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Child Workflow](/child-workflows)

A Child Workflow Execution is a Workflow Execution that is spawned from within another Workflow.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [child-workflow](/tags/child-workflow)_ -->

#### [Claim Mapper](/self-hosted-guide/security#claim-mapper)

The Claim Mapper component is a pluggable component that extracts Claims from JSON Web Tokens (JWTs).

<!-- _Tags: [term](/tags/term)_ -->

#### [Codec Server](/codec-server)

A Codec Server is an HTTP server that uses your custom Payload Codec to encode and decode your data remotely through
endpoints.

<!-- _Tags: [term](/tags/term)_ -->

#### [Command](/workflow-execution#command)

A Command is a requested action issued by a Worker to the Temporal Service after a Workflow Task Execution completes.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Continue-As-New](/workflow-execution/continue-as-new)

Continue-As-New is the mechanism by which all relevant state is passed to a new Workflow Execution with a fresh Event
History.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [continue-as-new](/tags/continue-as-new)_ -->

#### [Core SDK](https://temporal.io/blog/why-rust-powers-core-sdk)

The Core SDK is a shared common core library used by several Temporal SDKs. Written in Rust, the Core SDK provides
complex concurrency management and state machine logic among its standout features. Centralizing development enables the
Core SDK to support quick and reliable deployment of new features to existing SDKs, and to more easily add new SDK
languages to the Temporal ecosystem.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [continue-as-new](/tags/continue-as-new)_ -->

#### [Custom Data Converter](/default-custom-data-converters#custom-data-converter)

A custom Data Converter extends the default Data Converter with custom logic for Payload conversion or Payload
encryption.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Data Converter](/dataconversion)

A Data Converter is a Temporal SDK component that serializes and encodes data entering and exiting a Temporal Service.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Default Data Converter](/default-custom-data-converters#default-data-converter)

The default Data Converter is used by the Temporal SDK to convert objects into bytes using a series of Payload
Converters.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Delay Workflow Execution](/workflow-execution/timers-delays)

Start Delay determines the amount of time to wait before initiating a Workflow Execution. If the Workflow receives a
Signal-With-Start or Update-With-Start during the delay, it dispatches a Workflow Task and the remaining delay is
bypassed.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [delay-workflow](/tags/delay-workflow)_ -->

#### [Dual Visibility](/dual-visibility)

Dual Visibility is a feature, specific to a Self-hosted Temporal Service, that lets you set a secondary Visibility store
in your Temporal Service to facilitate migrating your Visibility data from one database to another.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [filtered-lists](/tags/filtered-lists), [visibility](/tags/visibility)_ -->

#### [Durable Execution](/temporal#durable-execution)

Durable Execution in the context of Temporal refers to the ability of a Workflow Execution to maintain its state and
progress even in the face of failures, crashes, or server outages.

<!-- _Tags: [temporal](/tags/temporal), [durable-execution](/tags/durable-execution), [term](/tags/term)_ -->

#### [Dynamic Handler](/dynamic-handler)

Dynamic Handlers are Workflows, Activities, Signals, or Queries that are unnamed and invoked when no other named handler
matches the call from the Server at runtime.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Event](/workflow-execution/event#event)

Events are created by a Temporal Service in response to external occurrences and Commands generated by a Workflow
Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Event History](/workflow-execution/event#event-history)

An append-only log of Events that represents the full state a Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Failback](/cloud/high-availability)

After Temporal Cloud has resolved an outage or incident involving a failover, a failback process shifts Workflow
Execution processing back to the original region that was active before the incident.

#### [Failover](/cloud/high-availability)

A failover shifts Workflow Execution processing from an active Temporal Namespace region to a standby Temporal Namespace
region during outages or other incidents. Standby Namespace regions use replication to duplicate data and prevent data
loss during failover.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Failure](/temporal#failure)

Temporal Failures are representations of various types of errors that occur in the system.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Failure Converter](/failure-converter)

A Failure Converter converts error objects to proto Failures and back.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Failures](/references/failures)

A Failure is Temporal's representation of various types of errors that occur in the system.

<!-- _Tags: [failure](/tags/failure), [explanation](/tags/explanation), [term](/tags/term)_ -->

#### [Frontend Service](/temporal-service/temporal-server#frontend-service)

The Frontend Service is a stateless gateway service that exposes a strongly typed Proto API. The Frontend Service is
responsible for rate limiting, authorizing, validating, and routing all inbound calls.

<!-- _Tags: [term](/tags/term)_ -->

#### [General Availability](/evaluate/development-production-features/release-stages#general-availability)

Learn more about the General Availability release stage

<!-- _Tags: [product-release-stages](/tags/product-release-stages), [term](/tags/term)_ -->

#### [Global Namespace](/global-namespace)

A Global Namespace is a Namespace that duplicates data from an active [Temporal Service](#temporal-cluster) to a standby
Service using the replication to keep both Namespaces in sync. Global Namespaces are designed to respond to service
issues like network congestion. When service to the primary Cluster is compromised, a [failover](#failover) transfers
control from the active to the standby cluster.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Heartbeat Timeout](/encyclopedia/detecting-activity-failures#heartbeat-timeout)

A Heartbeat Timeout is the maximum time between Activity Heartbeats.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [High Availability](/cloud/high-availability/)

High availability ensures that a system remains operational with minimal downtime. It achieves this with redundancy and
failover mechanisms that handle failures, so end-users remain unaware of incidents. Temporal Cloud guarantees this high
availability with its Service Level Agreements ([SLA](/cloud/sla))

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [High Availability features](/cloud/high-availability#high-availability-features)

High Availability features automatically synchronize your data between a primary Namespace and its replica, keeping them
in sync. In case of an incident or an outage, Temporal will automatically failover your Namespace from the primary to
the replica. This supports high levels of business continuity, allowing Workflow Executions to continue with minimal
interruptions or data loss.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [History Service](/temporal-service/temporal-server#history-service)

The History Service is responsible for persisting Workflow Execution state and determining what to do next to progress
the Workflow Execution through History Shards.

<!-- _Tags: [term](/tags/term)_ -->

#### [History Shard](/temporal-service/temporal-server#history-shard)

A History Shard is an important unit within a Temporal Service by which the scale of concurrent Workflow Execution
throughput can be measured.

<!-- _Tags: [term](/tags/term)_ -->

#### [Idempotency](/activity-definition#idempotency)

An "idempotent" approach avoids process duplication that could withdraw money twice or ship extra orders by mistake.
Idempotency keeps operations from producing additional effects, protecting your processes from accidental or repeated
actions, for more reliable execution. Design your activities to succeed once and only once. Run-once actions maintain
data integrity and prevent costly errors.

<!-- _Tags: [term](/tags/term)_ -->

#### [Isolation Domain](/cloud/high-availability)

An isolation domain is a defined area within Temporal Cloud's infrastructure. It helps contain failures and prevents
them from spreading to other parts of the system, providing redundancy and fault tolerance.

<!-- _Tags: [term](/tags/term)_ -->

#### [List Filter](/list-filter)

A List Filter is the SQL-like string that is provided as the parameter to an advanced Visibility List API.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [filtered-lists](/tags/filtered-lists), [visibility](/tags/visibility)_ -->

#### [Local Activity](/local-activity)

A Local Activity is an Activity Execution that executes in the same process as the Workflow Execution that spawns it.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Matching Service](/temporal-service/temporal-server#matching-service)

The Matching Service is responsible for hosting external Task Queues for Task dispatching.

<!-- _Tags: [term](/tags/term)_ -->

#### [Memo](/workflow-execution#memo)

A Memo is a non-indexed user-supplied set of Workflow Execution metadata that is returned when you describe or list
Workflow Executions.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Multi-Cluster Replication](/self-hosted-guide/multi-cluster-replication)

Multi-Cluster Replication is a feature which asynchronously replicates Workflow Executions from active Clusters to other
passive Clusters, for backup and state reconstruction.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Multi-cloud Replication](/cloud/high-availability/enable)

Multi-cloud Replication replicates Workflows and metadata to a different cloud provider (AWS or GCP). This is
particularly beneficial for organizations required to be highly available across regions for compliance purposes.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Multi-region Replication](/cloud/high-availability/enable)

Multi-region Replication replicates Workflows and metadata to a different region that is not co-located with the primary
Namespace. This is particularly beneficial for organizations with multi-regional architectures or those required to be
highly available across regions for compliance purposes.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Namespace](/namespaces)

A Namespace is a unit of isolation within the Temporal Platform.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### Nexus Async Completion Callback

A Nexus Async Completion Callback is the completion callback for an asynchronous Nexus Operation.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

A Nexus Endpoint is a reverse proxy that can serve one or more Nexus Services. It routes Nexus requests to a target
Namespace and Task Queue, that a Nexus Worker is polling. This allows service providers to present a clean service
contract and hide the underlying implementation, which may consist of many internal Workflows. Multiple Nexus Endpoints
can target the same Namespace, and over time a Nexus Endpoint will be able to span multiple Namespaces with service
routing rules.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

Temporal has built-in Nexus Machinery to guarantee at-least-once execution of Nexus Operations with state-machine-based
invocation and completion callbacks. The Nexus Machinery uses [Nexus RPC](/glossary#nexus-rpc), a protocol designed with
Durable Execution in mind, to communicate across Namespace boundaries. Caller Workflows and Nexus handlers don't have to
use Nexus RPC directly, since the Temporal SDK provides a streamlined developer experience to build, run, and use Nexus
Services.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

An arbitrary-duration operation that may be synchronous or asynchronous, short-lived, or long-lived, and used to connect
durable executions within and across Namespaces, clusters, regions, and clouds. Unlike a traditional RPC, an
asynchronous Nexus Operation has an operation token that can be used to re-attach to a long-lived Nexus Operation, for
example, one backed by a Temporal Workflow. Nexus Operations support a uniform interface to get the status of an
operation or its result, receive a completion callback, or cancel the operation – all of which are fully integrated into
the Temporal Platform.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### Nexus Operation Events

Nexus Operations Events are history events that surface in the Caller Workflow to indicate the state of an Operation
including `Nexus Operation Scheduled`, `Nexus Operation Started`, `Nexus Operation Completed`.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### Nexus Operation Handler

The Nexus handler code in a Temporal Worker typically created using Temporal SDK builder functions that make it easy to
abstract Temporal primitives and expose a clean service contract for others to use.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

The Nexus Registry manages Nexus Endpoints and provides lookup services for resolving Nexus requests at runtime. In the
open source version of Temporal, the Registry is scoped to a Cluster, while in Temporal Cloud, it is scoped to an
Account. Endpoint names must be unique within the Registry. When the Temporal Service dispatches a Nexus request, it
resolves the request's Endpoint to a Namespace and Task Queue through the Registry.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Nexus RPC](https://github.com/nexus-rpc/api/blob/main/SPEC.md)

Nexus RPC is a protocol designed with durable execution in mind. It supports arbitrary-duration Operations that extend
beyond a traditional RPC — a key underpinning to connect durable executions within and across Namespaces, clusters,
regions, and cloud boundaries.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

A Nexus Service is a named collection of arbitrary-duration Nexus Operations that provide a microservice contract
suitable for sharing across team and application boundaries. Nexus Services are registered with a Temporal Worker that
is polling a Nexus Endpoint's target Namespace and Task Queue.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### Nexus Service Contract

A common code package, schema, or documentation that a Caller can use to obtain Service and Operation names as
associated input/output types a Service will accept for a given Operation.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Parent Close Policy](/parent-close-policy)

If a Workflow Execution is a Child Workflow Execution, a Parent Close Policy determines what happens to the Workflow
Execution if its Parent Workflow Execution changes to a Closed status (Completed, Failed, Timed out).

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [child-workflow-executions](/tags/child-workflow-executions)_ -->

#### [Payload](/dataconversion#payload)

A Payload represents binary data such as input and output from Activities and Workflows.

<!-- _Tags: [term](/tags/term), [payloads](/tags/payloads), [explanation](/tags/explanation)_ -->

#### [Payload Codec](/payload-codec)

A Payload Codec transforms an array of Payloads into another array of Payloads.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Payload Converter](/payload-converter)

A Payload Converter serializes data, converting objects or values to bytes and back.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Pre-release](/evaluate/development-production-features/release-stages#pre-release)

Learn more about the Pre-release stage

<!-- _Tags: [product-release-stages](/tags/product-release-stages), [term](/tags/term)_ -->

#### [Public Preview](/evaluate/development-production-features/release-stages#public-preview)

Learn more about the Public Preview release stage

<!-- _Tags: [product-release-stages](/tags/product-release-stages), [term](/tags/term)_ -->

#### [Query](/sending-messages#sending-queries)

A Query is a synchronous operation that is used to report the state of a Workflow Execution.

<!-- _Tags: [term](/tags/term), [queries](/tags/queries), [explanation](/tags/explanation)_ -->

#### [Remote data encoding](/remote-data-encoding)

Remote data encoding is using your custom Data Converter to decode (and encode) your Payloads remotely through
endpoints.

<!-- _Tags: [term](/tags/term), [queries](/tags/queries), [explanation](/tags/explanation)_ -->

#### [Replication Lag](/cloud/high-availability/monitoring#replication-lag-metric)

The transmission delay of Workflow updates and history events from the active region to the standby region.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Requests Per Second (RPS)](/references/dynamic-configuration#service-level-rps-limits)

RPS, or Requests per second, is used in the Temporal Service (both in self-hosted Temporal and Temporal Cloud). This is
a measure that controls the rate of requests at the service level, such as the Frontend, History, or Matching Service.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [temporal](/tags/temporal)_ -->

#### [Reset](/workflow-execution/event#reset)

A Reset terminates a Workflow Execution, removes the progress in the Event History up to the reset point, and then
creates a new Workflow Execution with the same Workflow Type and Id to continue.

<!-- _Tags: [term](/tags/term), [resets](/tags/resets), [explanation](/tags/explanation)_ -->

#### [Retention Period](/temporal-service/temporal-server#retention-period)

A Retention Period is the amount of time a Workflow Execution Event History remains in the Temporal Service's
persistence store.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Retry Policy](/encyclopedia/retry-policies)

A Retry Policy is a collection of attributes that instructs the Temporal Server how to retry a failure of a Workflow
Execution or an Activity Task Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Run Id](/workflow-execution/workflowid-runid#run-id)

A Run Id is a globally unique, platform-level identifier for a Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Same-region Replication](/cloud/high-availability/enable)

Same-region Replication replicates Workflows and metadata to an isolation domain within the same region as the primary
Namespace. It provides a reliable failover mechanism while maintaining deployment simplicity.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Schedule](/schedule)

A Schedule enables the scheduling of Workflow Executions.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Schedule-To-Close Timeout](/encyclopedia/detecting-activity-failures#schedule-to-close-timeout)

A Schedule-To-Close Timeout is the maximum amount of time allowed for the overall Activity Execution, from when the
first Activity Task is scheduled to when the last Activity Task, in the chain of Activity Tasks that make up the
Activity Execution, reaches a Closed status.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [Schedule-To-Start Timeout](/encyclopedia/detecting-activity-failures#schedule-to-start-timeout)

A Schedule-To-Start Timeout is the maximum amount of time that is allowed from when an Activity Task is placed in a Task
Queue to when a Worker picks it up from the Task Queue.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [Search Attribute](/search-attribute)

A Search Attribute is an indexed name used in List Filters to filter a list of Workflow Executions that have the Search
Attribute in their metadata.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [filtered-lists](/tags/filtered-lists), [visibility](/tags/visibility)_ -->

#### [Side Effect](/workflow-execution/event#side-effect)

A Side Effect is a way to execute a short, non-deterministic code snippet, such as generating a UUID, that executes the
provided function once and records its result into the Workflow Execution Event History.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Signal](/sending-messages#sending-signals)

A Signal is an asynchronous request to a Workflow Execution.

<!-- _Tags: [term](/tags/term), [signals](/tags/signals), [explanation](/tags/explanation)_ -->

#### [Signal-With-Start](/sending-messages#signal-with-start)

Signal-With-Start starts and Signals a Workflow Execution, or just Signals it if it already exists.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Start-To-Close Timeout](/encyclopedia/detecting-activity-failures#start-to-close-timeout)

A Start-To-Close Timeout is the maximum time allowed for a single Activity Task Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [State Transition](/workflow-execution#state-transition)

A State Transition is a unit of progress by a Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Sticky Execution](/sticky-execution)

A Sticky Execution is a when a Worker Entity caches the Workflow Execution Event History and creates a dedicated Task
Queue to listen on.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Task](/tasks#task)

A Task is the context needed to make progress with a specific Workflow Execution or Activity Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Task Queue](/task-queue)

A Task Queue is a first-in, first-out queue that a Worker Process polls for Tasks.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Task Routing](/task-routing)

Task Routing is when a Task Queue is paired with one or more Worker Processes, primarily for Activity Task Executions.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Task Token](/activity-execution#task-token)

A Task Token is a unique identifier for an Activity Task Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal](/temporal)

Temporal is a scalable and reliable runtime for Reentrant Processes called Temporal Workflow Executions.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Application](/temporal#temporal-application)

A Temporal Application is a set of Workflow Executions.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal CLI](/cli) {#cli}

The Temporal CLI is the most recent version of Temporal's command-line tool.

<!-- _Tags: [term](/tags/term), [cli](/tags/cli)_ -->

#### [Temporal Client](/encyclopedia/temporal-sdks#temporal-client)

A Temporal Client, provided by a Temporal SDK, provides a set of APIs to communicate with a Temporal Service.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Cloud](/cloud/overview)

Temporal Cloud is a managed, hosted Temporal environment that provides a platform for Temporal Applications.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Cloud Account Id](/cloud/namespaces#temporal-cloud-account-id)

A Temporal Cloud Account Id is a unique identifier for a customer.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Cloud Namespace Id](/cloud/namespaces#temporal-cloud-namespace-id)

A Cloud Namespace Id is a globally unique identifier for a Namespace in Temporal Cloud.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Cloud Namespace Name](/cloud/namespaces#temporal-cloud-namespace-name)

A Cloud Namespace Name is a customer-supplied name for a Namespace in Temporal Cloud.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Cloud gRPC Endpoint](/cloud/namespaces#temporal-cloud-grpc-endpoint)

A Cloud gRPC Endpoint is a Namespace-specific address used to access Temporal Cloud from your code.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Cluster](/temporal-service)

The term "Temporal Cluster" is being phased out. Instead the term [Temporal Service](#temporal-service) is now being
used.

#### [Temporal Service](/temporal-service)

A Temporal Service is a Temporal Server paired with Persistence and Visibility stores.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Service configuration](/temporal-service/configuration)

Temporal Service configuration is the setup and configuration details of your Temporal Service, defined using YAML.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Cron Job](/cron-job)

A Temporal Cron Job is the series of Workflow Executions that occur when a Cron Schedule is provided in the call to
spawn a Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Platform](/temporal#temporal-platform)

The Temporal Platform consists of a Temporal Service and Worker Processes.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal SDK](/encyclopedia/temporal-sdks)

A Temporal SDK is a language-specific library that offers APIs to construct and use a Temporal Client to communicate
with a Temporal Service, develop Workflow Definitions, and develop Worker Programs.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Server](/temporal-service/temporal-server)

The Temporal Server is a grouping of four horizontally scalable services.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Temporal Web UI](/web-ui)

The Temporal Web UI provides users with Workflow Execution state and metadata for debugging purposes.

<!-- _Tags: [term](/tags/term), [web-ui](/tags/web-ui)_ -->

#### [Timer](/workflow-execution/timers-delays)

Temporal SDKs offer Timer APIs so that Workflow Executions are deterministic in their handling of time values.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Update](/sending-messages#sending-updates)

An Update is a request to and a response from Workflow Execution.

<!-- _Tags: [term](/tags/term), [updates](/tags/updates), [explanation](/tags/explanation)_ -->

#### [Visibility](/temporal-service/visibility)

The term Visibility, within the Temporal Platform, refers to the subsystems and APIs that enable an operator to view
Workflow Executions that currently exist within a Temporal Service.

<!-- _Tags: [term](/tags/term)_ -->

#### [Worker](/workers#worker)

In day-to-day conversations, the term Worker is used to denote both a Worker Program and a Worker Process. Temporal
documentation aims to be explicit and differentiate between them.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Worker Entity](/workers#worker-entity)

A Worker Entity is the individual Worker within a Worker Process that listens to a specific Task Queue.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Worker Process](/workers#worker-process)

A Worker Process is responsible for polling a Task Queue, dequeueing a Task, executing your code in response to a Task,
and responding to the Temporal Server with the results.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Worker Program](/workers#worker-program)

A Worker Program is the static code that defines the constraints of the Worker Process, developed using the APIs of a
Temporal SDK.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Worker Service](/temporal-service/temporal-server#worker-service)

The Worker Service runs background processing for the replication queue, system Workflows, and (in versions older than
1.5.0) the Kafka visibility processor.

<!-- _Tags: [term](/tags/term)_ -->

#### [Worker Session](/task-routing#worker-session)

A Worker Session is a feature provided by some SDKs that provides a straightforward way to ensure that Activity Tasks
are executed with the same Worker without requiring you to manually specify Task Queue names.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow](/workflows)

In day-to-day conversations, the term "Workflow" frequently denotes either a Workflow Type, a Workflow Definition, or a
Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Definition](/workflow-definition)

A Workflow Definition is the code that defines the constraints of a Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Execution](/workflow-execution)

A Temporal Workflow Execution is a durable, scalable, reliable, and reactive function execution. It is the main unit of
execution of a Temporal Application.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Execution Timeout](/encyclopedia/detecting-workflow-failures#workflow-execution-timeout)

A Workflow Execution Timeout is the maximum time that a Workflow Execution can be executing (have an Open status)
including retries and any usage of Continue As New.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [Workflow History Export](/cloud/export)

Workflow History export allows users to export Closed Workflow Histories to a user's Cloud Storage Sink.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [temporal-cloud](/tags/temporal-cloud), [operations](/tags/operations)_ -->

#### [Workflow Id](/workflow-execution/workflowid-runid#workflow-id)

A Workflow Id is a customizable, application-level identifier for a Workflow Execution that is unique to an Open
Workflow Execution within a Namespace.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Id Conflict Policy](/workflow-execution/workflowid-runid#workflow-id-conflict-policy)

A Workflow Id Conflict Policy determines how to resolve the conflict when spawning a new Workflow Execution with a
particular Workflow Id that is used by an Open Workflow Execution already.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Id Reuse Policy](/workflow-execution/workflowid-runid#workflow-id-reuse-policy)

A Workflow Id Reuse Policy determines whether a Workflow Execution is allowed to spawn with a particular Workflow Id, if
that Workflow Id has been used with a previous, and now Closed, Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Run Timeout](/encyclopedia/detecting-workflow-failures#workflow-run-timeout)

This is the maximum amount of time that a single Workflow Run is restricted to.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [Workflow Task](/tasks#workflow-task)

A Workflow Task is a Task that contains the context needed to make progress with a Workflow Execution.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Task Execution](/tasks#workflow-task-execution)

A Workflow Task Execution occurs when a Worker picks up a Workflow Task and uses it to make progress on the execution of
a Workflow Definition.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### [Workflow Task Timeout](/encyclopedia/detecting-workflow-failures#workflow-task-timeout)

A Workflow Task Timeout is the maximum amount of time that the Temporal Server will wait for a Worker to start
processing a Workflow Task after the Task has been pulled from the Task Queue.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation), [timeouts](/tags/timeouts)_ -->

#### [Workflow Type](/workflow-definition#workflow-type)

A Workflow Type is a name that maps to a Workflow Definition.

<!-- _Tags: [term](/tags/term), [explanation](/tags/explanation)_ -->

#### tctl (_deprecated_)

tctl is a command-line tool that you can use to interact with a Temporal Service. It is superseded by the
[Temporal CLI utility](#cli).

## Managing Temporal Cloud Access Control

Temporal Cloud supports two secure authentication methods for Workers:
- **mTLS Certificates**
- **API Keys** (configured via the UI when creating a namespace)

Both options help secure communication between workers and Temporal Cloud. Choosing the right method and managing it properly is key to maintaining security and minimizing downtime.

The high-level end-to-end rotation process is:

1. **Generate new credentials**: Create new certificates or API keys in Temporal Cloud before the current ones expire
2. **Support dual credentials**: Update Temporal Cloud to support both old and new credentials
3. **Migrate Workers**: Transition Worker applications from old credentials to new credentials
4. **Validate connectivity**: Confirm all Workers can authenticate, and business processes operate normally with new credentials
5. **Remove old credentials**: Remove old certificates and API keys from your secrets provider after confirming successful migration

This approach ensures near-zero-downtime rotation and prevents authentication failures that could impact running workflows. For specific guidance to rotate mTLS certificates and API keys, see:
- https://docs.temporal.io/cloud/certificates#manage-certificates 
- https://docs.temporal.io/cloud/api-keys#rotate-an-api-key 
- https://github.com/temporal-sa/temporal-Worker-cert-rotation

For mutual TLS (mTLS) implementations, using Let's Encrypt is not recommended, as it is designed primarily for public-facing services and lacks support for internal certificate requirements.

While we are not making a specific product recommendation, there are several valid options for managing certificates. Many organizations choose vendor solutions such as AWS Private CA, Setigo, Microsoft Certification Authority, or DigiCert for their robust integration and lifecycle features. Alternatively, self-signed certificates are a valid and commonly used approach, even in production environments. If you choose to self-sign, tools like [OpenSSL](https://openssl-library.org/), [CFSSL](https://github.com/cloudflare/cfssl), or [step CLI](https://github.com/smallstep/cli) can help generate and manage certificates effectively.

Select the option that aligns best with your infrastructure, security requirements, and operational needs.

In the case that you are using multiple certificates signed by the same CA, and some of these certificates are for production environments, there are some workarounds you can employ.

One convention is to give certificates a common name that matches the namespace. If you do this when using the same CA for dev and prod, then you can leverage Certificate Filters to prevent access to production environments. This is described in detail under the [authorization section](https://docs.temporal.io/cloud/certificates#control-authorization) of the documentation.

## Best practices: 
#### 1. Establish clear guidelines on authentication methods: Teams should standardize on either [mTLS certificates](https://docs.temporal.io/cloud/certificates) or [API keys](https://docs.temporal.io/cloud/api-keys) for the following operations:
- Connect Temporal clients to Temporal Cloud (e.g. Worker processes)
- Automation (e.g. Temporal Cloud [Operations API](https://docs.temporal.io/ops), [Terraform provider](https://docs.temporal.io/production-deployment/cloud/terraform-provider), [Temporal CLI](https://docs.temporal.io/cli/setup-cli))

By default, it is recommended for teams to use API keys and [service accounts](https://docs.temporal.io/cloud/service-accounts) for both operations because API keys are easier to manage and rotate for most teams. In addition, you can control account-level and namespace-level roles for service accounts.

If your organization requires mutual authentication and stronger cryptographic guarantees, then it is encouraged for your teams to use mTLS certificates to authenticate Temporal clients to Temporal Cloud and use API keys for automation (because Temporal Cloud [Operations API](https://docs.temporal.io/ops) and [Terraform provider](https://docs.temporal.io/production-deployment/cloud/terraform-provider) only supports API key for authentication)

#### 2. Use Certificate Filters to restrict access when using shared CAs (e.g., `dev` vs `prod`):

Certificate Filters are an additional way of validating using the client certificate presented during client authenticationGive certificates a common name that matches the namespace. This is not a requirement.

If you do this when using the same CA for dev and prod environments, then you can leverage Certificate Filters to prevent access to production.

These guides outline foundational principles and best practices for using Temporal Cloud. It exists to provide a
**validated, opinionated** framework that helps teams that either do not have an enablement plan for or want to evaluate
and refine their use of Temporal.

Without clearly defined Temporal standards, organizations often struggle with inconsistent Workflow implementations,
fragmented best practices, and misaligned development approaches. This documentation framework helps developers
establish robust Temporal standards by providing:

- **Proven foundation principles** that have been validated across diverse use cases
- **Standardized implementation patterns** for teams to adopt consistently across projects
- **Confidence in alignment** with Temporal's architectural principles and recommended practices

By following this guidance, developers can define comprehensive Temporal standards that ensure their workflow
orchestration implementations are maintainable, scalable, and aligned with platform best practices from the start.

This section is intended for:

- Developers responsible for building a Temporal Cloud practice within their organization.
- Anyone building tutorials, courses, onboarding paths, or documentation
- Partners or vendors creating Temporal-related learning materials

- **[Managing a Namespace](./managing-namespace.mdx)** Best practices for configuring, managing, and optimizing Temporal
  Namespaces.

- **[Managing Temporal Cloud Access Control](./cloud-access-control.mdx)** Guidelines for implementing proper access
  control and user management in Temporal Cloud.

- **[Security Controls for Temporal Cloud](./security-controls.mdx)** Comprehensive security practices for protecting
  your Temporal Cloud deployment.

- **[Worker Deployment and Performance](./worker.mdx)** Best practices for deploying and optimizing Temporal Workers for
  performance and reliability.

## Managing Actions per Second (APS) Limits in Temporal Cloud

If you're running Workflows on Temporal Cloud, you've probably noticed that each Namespace comes with an Actions Per Second (APS) limit. 
But what exactly does that mean, and why does it matter?

In Temporal, an "action" is any operation that modifies Workflow state or interacts with the Temporal service. 
Your Namespace's APS limit controls how many of these operations can happen per second across all Workflows within that Namespace.
When the APS limit is reached, Temporal begins to throttle requests. 
Depending on the business priority of the Workflow, this may be fine or it may have significant impact.

The difficulty is that APS consumption isn't always intuitive. 
A single Workflow Execution generates multiple actions from the moment it starts, and use cases that fit nicely within APS limits at small scale can exhaust those limits as they grow. 
Many customers are surprised to find they're hitting APS constraints well before they expected to based on their Workflow count alone.

This guide will help you understand why customers hit APS limits, how to design Workflows that use actions efficiently, and what to do when you're approaching capacity. 
Whether you're just getting started with Temporal Cloud or optimizing an existing deployment, managing APS effectively is key to building scalable, reliable applications.

## Understanding Actions in Temporal

Before we dive into why customers hit APS limits, let's talk about what actions are.

### What Counts as an Action?

In Temporal, actions are the fundamental operations that drive your Workflows forward. 
Here's an overview of what counts, with [the full list in our documentation](/cloud/actions).

- Workflows: Starting, completing, resetting. Also starting Child Workflows, as well as Schedules and Timers
- Activities: Starting, retrying, Heartbeating
- Signals, Updates, and Queries

Actions that count toward an APS limit are, with a few exemptions, the same as actions that are billable. 
The key insight here is that nearly everything that happens in Temporal--state changes, decision points, interactions--is counted as an action.

### The Action Multiplier Effect

What this means is that when you start a single Workflow, you're not performing just one action as it relates to APS because a Workflow isn’t a single atomic operation, it’s a series of events that Temporal orchestrates. 
Each Activity at the start of the Workflow is an Action, so there can be a burst of Activities at the start of a Workflow. 
Additionally, there are often business reasons to start multiple Workflows at the same time.

These can all contribute to the multiplier effect.

### The Effect of Rate Limiting

In Temporal Cloud, the effect of rate limiting is increased latency, not lost work. 
Workers [might take longer](/cloud/service-availability#throughput) to complete Workflows.

## Common Reasons Customers Hit APS Limits

Now that you understand how actions are defined and how they count toward APS limits, let's look at the patterns that most commonly push customers into APS constraints.

Most businesses don't operate at constant velocity—they have rhythms, cycles, and spikes. 
These patterns can create APS challenges because Temporal Cloud enforces limits at the per-second level.

Common bursty patterns include:

- Calendar-driven spikes: Month-end financial close processes, quarterly reporting Workflows, payroll that runs on the 1st and 15th, scheduled batch jobs that kick off at midnight. These create predictable but intense load concentrations.
- Event-driven surges: Product launches, marketing campaigns, flash sales, breaking news, or seasonal events like Black Friday. 
- Recovery scenarios: When a downstream dependency fails and then recovers, you often get a thundering herd effect—hundreds or thousands of Workflows that were waiting all suddenly resume execution simultaneously, creating an artificial spike in APS consumption.
- Geographic/business hours concentration: Global applications often see load follow the sun, with peak activity during business hours in each region. If your business concentrates in specific markets, you'll see daily peaks rather than even 24/7 distribution.
- Retry Storms: when a large number of Workflows get stuck on an Activity, and that Activity is failing, if retry delay is very short, this can cause a spike in Actions.
- Timer Storms: a large number of Workflows all set a Timer for the exact same time--triggering a spike as those Timers fire and then Activities run, causing a lot of actions all at the same time.

These types of processes can result in your Namespace averaging 200 APS over a day, but spiking to 800 APS or more during your peak hour/day/event/etc.

You can’t change the patterns of how customers interact with your systems, but there are some adjustments you can make to your Workflows to make traffic patterns more consistent, especially for use cases where immediate response isn’t necessary.

These adjustments include:
- Implement application-level queuing or rate limiting to smooth out predictable spikes.
- For scheduled batch operations, stagger start times rather than triggering everything at once--implement jitter in your high-volume [Schedules](/schedule#spec).
- Implement jitter when starting Workflows, such as with [Start Delay](/workflow-execution/timers-delays#delay-workflow-execution).
- Accept rate limiting
- [Provisioned Capacity](/cloud/capacity-modes#provisioned-capacity)

### Cascading Workflows and Fan-Out Patterns

Decomposing complex processes into parent and Child Workflows (or with Nexus) is a common and often appropriate pattern, but the APS costs multiply dramatically with depth and fan-out.

Consider an order fulfillment Workflow that spawns Child Workflows for payment processing, inventory management, shipping, and customer notifications. 
Each Child Workflow goes through its full action lifecycle (start, tasks, activities, completion), and all of those actions count toward the APS limits on your Namespace.

This pattern appears frequently in:
- Batch processing: A parent workflow processes a file with 1,000 records, spawning a Child Workflow for each record. Batch processing is also often bursty whenever the batch begins.
- Map-reduce patterns: Data processing Workflows that fan out to process partitions in parallel, then aggregate results.

This challenge additionally compounds when you have multiple levels of nesting--parent Workflows that create children, which create their own children.

- Evaluate whether Child Workflows are necessary--other options include Activities or Workflows in another Namespace (via Nexus)
- When you do use Child Workflows, limit fan-out size--design a Child Workflow to process its work in batches rather than one Child per work item. [This sample application](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/batch/slidingwindow) shows more detail.
- Consider flattening deeply nested hierarchies into shallower structures.

### Human-in-the-Loop Processes at Scale

Workflows that incorporate human decision-making--approvals, reviews, manual data entry, quality checks--tend to be long-running and interaction-intensive, which creates sustained APS load.

These Workflows can involve Queries from UIs to display current state and pending tasks.

At small scale, this is manageable. But when you're running thousands of them at the same time--like a content moderation queue with pending reviews, or a loan approval system processing applications, or a support ticket system managing thousands of open cases--the cumulative APS load from all of those long-running Workflows adds up.

- Avoid polling patterns where UIs constantly query Workflow state. Instead, push state changes to a database that UIs can read.

### Real-Time SLAs and Deadline Management

Businesses with strict service level agreements often implement active monitoring and escalation in their Workflows. 
This is generally accomplished by setting Timers every [x] minutes to determine if an SLA deadline is approaching, allowing the Workflow to trigger escalations or alerts.

Each of these Timers/monitoring actions affect APS. 
When you have thousands of in-flight Workflows all actively monitoring their own SLAs, the background load becomes significant.
You're consuming substantial APS capacity even when Workflows aren't doing their primary work.

- Use longer monitoring intervals where possible. For example, check SLAs every 30 minutes rather than every 1 minute.
- Where possible, consolidate Timers. Rather than 10 Timers that check 10 tasks, have 1 Timer and then check those 10 tasks.
- Where possible, have an external system signal your Workflow rather than using short-lived Timers to poll.
- For retries, use exponential backoff with reasonable initial intervals.

## Additional Design Patterns
There are some design patterns that can lead to high APS that are consistent across many different types of business use cases.

### Many Small Activities

Consider two approaches to processing 1,000 records:

- Approach A: Create a Workflow that spawns 1,000 separate activities, one per record.
- Approach B: Create a Workflow that spawns 10 activities, each processing 100 records in a batch.

Approach B will clearly result in less APS. 
This is a simple example, but this pattern shows up everywhere: processing individual transactions versus batches, sending individual notifications versus bulk operations, or making separate API calls versus batch endpoints. 
Each separate Activity adds Action overhead.

- Consider if you can combine multiple external calls within a single Activity.
- If processing a large amount of data, process it in chunks.
- See [How Many Activities should I use in my Temporal Workflow?](https://temporal.io/blog/how-many-activities-should-i-use-in-my-temporal-workflow) for more information.

### Multiple Use Cases in One Namespace
Often when starting with Temporal, the first use case is implemented in a single Namespace, generally one per logical environment. 
When the second Temporal use case is implemented, it runs in the same Namespace, the same for the third, fourth, etc.

An APS limit is set per Namespace, so multiple use cases with multiple traffic patterns in the same Namespace can exhaust this limit quickly.

Plan for a set of Namespaces (one per environment) per use case. See [Managing a Namespace](/best-practices/managing-namespace) for more details.

#### Provisioned Capacity

If you have a workload that is both latency-sensitive and is being rate-limited, you can also use [Provisioned Capacity](/cloud/capacity-modes#provisioned-capacity) Modes on your Namespace. 
This allows you to set Temporal Resource units that will scale up your limits to meet the needs of your specific workloads.

## Knowing if You’re Hitting APS Limits

In addition to understanding the patterns that can affect APS limits on a Temporal Namespace, it’s also important to know if you’re approaching (or exceeding) these limits. 
Temporal Cloud provides several metrics that, if tracked, will tell you if you’re being rate limited due to APS. 
See the documentation on [detecting resource exhaustion](/production-deployment/cloud/service-health#rps-aps-rate-limits) for an explanation of those metrics as well as a sample Grafana dashboard that shows how they could be viewed.

Let's recap the main reasons customers hit APS limits and how to address them:

| Reason for Hitting APS Limits | How to Address It |
|-------------------------------|-------------------|
| Bursty Traffic                | Implement application-level queuing or rate limiting to smooth spike, stagger start times for scheduled batch operations. | 
| Cascading Workflows and Fan-Out Patterns | Evaluate if Child Workflows are necessary (consider activities or another Namespace), limit fan-out size by processing work in batches within a Child Workflow, consider flattening deeply nested hierarchies. |
| Human-in-the-Loop Processes at Scale | Design long-running Workflows to minimize sustained APS load from interaction (by avoiding polling where UIs constantly Query state and using Signals only for key human inputs). |
| Many small activities         | Consider if you can combine multiple external calls within a single Activity. If processing a large amount of data, process it in chunks. |
| Multiple use cases in one Namespace | Plan for a set of Namespaces (one per environment) per use case. |

When designing Temporal Workflows with an eye toward APS limits, ask yourself the following questions: 
- How many actions will a single execution of this Workflow consume?
- How many Workflows will typically be running at the same time?
- What happens to APS consumption when the number of Actions * number of active Workflows scales to 100x current volume?
- Are there natural opportunities to combine operations: combine activities, or process chunks of data together?
- Am I polling when I could be using Signals?
- Does this Workflow need to run continuously, or can it be event-driven?

A few hours spent optimizing Workflow design can save you from capacity crunches, emergency limit increases, and potentially significant cost increases down the road.

## Managing a Namespace

A [Namespace](https://docs.temporal.io/namespaces) is a unit of isolation within the Temporal platform. It ensures that workflow executions, task queues, and resources are logically separated, preventing any conflicts and enabling safe multi-tenant usage.

Namespaces are created on the Temporal Service, and one Namespace will not impact another on the same Temporal Service. However, a single Namespace can be multi-tenant, and they act solely as a logical separation.

If you are running Temporal on your own, you might be familiar with services within a cluster, such as the front-end, backend, matching service, and more. In Temporal Cloud all of these services are managed by us, so you don’t have to worry about managing them at all!

## How to Register a Namespace

[Registering a Namespace](https://docs.temporal.io/namespaces#registration) creates the Namespace on the Temporal Service. You’re also required to set the retention period when creating the Namespace.

On Temporal Cloud, use the Temporal Cloud UI or `tcld` commands to create and manage Namespaces. If no other Namespace is specified, the Temporal Service uses the Namespace `default` for all Temporal SDKs and the Temporal CLI.

Temporal Cloud enforces limits on Namespace count and workflow execution size. You are allowed up to **10 Namespaces by default**. Exceeding this limit requires a support ticket.

When it comes to naming Namespaces for your team, we recommend grouping them by factors such as teams, products or lines of business. You’ll also likely want to distinguish between dev and prod environments in the naming convention.

Each Namespace in Temporal Cloud runs in a specific region, which determines where your workflows and data are hosted. Temporal Cloud currently runs on AWS and GCP, with support for other clouds planned for the future.

While your cloud infrastructure might be limited to a single region, Temporal Cloud supports multiple regions, and you’ll have access to a full list of available regions during Namespace creation. To view the current list of supported regions and their operational status, visit: https://status.temporal.io

#### 1. Use lowercase and hyphens for Namespace names: Temporal Cloud treats Namespace names as case-insensitive. To maintain consistency and avoid potential issues, use lowercase letters and hyphen (-) as separators. Example: `payment-checkout-prd`

#### 2. Use domain, service, and environment to name Namespaces
Use the following pattern to name Temporal Namespaces: `<use-case>-<domain>-<region>-<environment>`
    
  The following rules ensure that the Namespace name doesn’t exceed [39 characters](https://docs.temporal.io/cloud/namespaces#temporal-cloud-namespace-name):
  - Use at most 10 characters for `use case` (e.g. `payments`, `fulfill`)
  - Use at most 10 character for `domain` (e.g. `checkout`, `notify`)
  - Use at most 5 characters for `region` (e.g. `aps1`, `apse1`)
  - Use at most 3 characters for `environment` (e.g. `dev`, `prd`)

Examples: `payments-checkout-dev`, `payments-checkout-prd`, `fulfill-notify-prd`

**Why this pattern?**
- Simple and easy to understand.
- Complies to [Temporal Cloud Namespace requirements](https://docs.temporal.io/cloud/namespaces#temporal-cloud-namespace-name)
- Clearly separates environments (e.g., `dev`, `prod`)
- Groups related services under domains that organization has defined
- Allows for platform teams to implement chargeback to application teams, given most domains are owned by separate teams within organizations 
- Namespace level [system limits](https://docs.temporal.io/cloud/limits#namespace-level) are isolated between different services and environments.
- Multiple workflows that are part of the same use case need to communicate with each other via Signals or by starting Child Workflows.

Note: [A Temporal Cloud account can have up to 100 Namespaces](https://docs.temporal.io/cloud/limits#namespaces) (soft limit).

#### 3. When selecting a region for your Namespace, choose one that aligns with your application's latency, compliance, and data residency requirements (use https://status.temporal.io/ to identify the right region for you).

Check out some more best practices for configuring Namespaces in [our documentation](https://docs.temporal.io/cloud/namespaces#general-guidance).

With Temporal, it’s important to be able to configure your Namespaces as well as see details for them. Whether you’re self-hosting or using Temporal Cloud, you’re able to get details for your Namespaces, update Namespace configuration, and deprecate or delete your Namespaces.

On Temporal Cloud, use the Temporal Cloud UI or `tcld` commands to manage Namespaces. We provide [guidance for both methods](https://docs.temporal.io/cloud/namespaces#manage-namespaces) in our docs that you can reference.

Regardless of how you run Temporal, you must register a Namespace with the Temporal Service before setting it in the Temporal Client.

We recommend you use a custom [Authorizer](https://docs.temporal.io/self-hosted-guide/security#authorizer-plugin) on your Frontend Service in the Temporal Service to set restrictions on who can create, update, or deprecate Namespaces. If an Authorizer is not set in the server options, Temporal uses the nopAuthority authorizer that unconditionally allows all API calls to pass through.

#### 1. Enable deletion protection for `prd` Namespaces: [Prevent accidental deletion](https://docs.temporal.io/cloud/namespaces#delete-protection) of production Namespaces.

#### 2. Enable multi-region replication for business critical use cases: For many organizations, ensuring high availability (HA) is required because of strict uptime requirements, compliance, and regulatory needs.

For these critical use cases, enable High Availability features for specific Namespaces for a [99.99% contractual SLA](https://docs.temporal.io/cloud/high-availability#high-availability-features). When choosing between [same-region and multi-region replication](https://docs.temporal.io/cloud/high-availability/how-it-works#deployment-options), favor multi-region replication to optimize reliability over proximity.

By default, Temporal Cloud provides a [99.9% contractual SLA](https://docs.temporal.io/cloud/high-availability) guarantee against service errors for all Namespaces.

Note: [enabling HA features for Namespaces will 2x the consumption cost](https://docs.temporal.io/cloud/pricing#high-availability-features).

#### 3. Use Terraform to manage Namespaces:
Use [Temporal Cloud Terraform provider](https://docs.temporal.io/production-deployment/cloud/terraform-provider) to manage Temporal Cloud Namespaces. This allows us to maintain documentation that outlines the purpose of each Namespace and their owners. In addition, Terraform enables us to prevent infrastructure drift (e.g. someone accidentally deletes a Namespace).

Use `prevent_destroy = true` to prevent Terraform from destroying the Namespace.

Reference: https://github.com/kawofong/temporal-terraform

[Tags](https://docs.temporal.io/cloud/namespaces#tag-a-namespace) are key-value metadata pairs that can be attached to Namespaces in Temporal Cloud to help operators organize, track, and manage Namespaces more easily.

### Tag Structure and Limits
- Each Namespace can have a maximum of 10 tags
- Each key must be unique for a given Namespace (e.g., a Namespace cannot have both `team:foo` and `team:bar` tags)
- Keys and values must be 1-63 characters in length
- Allowed characters: lowercase letters (a-z), numbers (0-9), periods (.), underscores (_), and hyphens (-)
- Tags are not a secure storage mechanism and should not store PII or PHI
- Tags will not change the behavior of the tagged resource
- There is a soft limit of 1000 unique tag keys per account

We also recommend tagging your Namespaces based on the following criteria: 
- Environment
- Latency sensitivity
- Business criticality: regulatory, user-facing
- Data sensitivity
- Team or Project
- Division

Temporal Cloud provides a few configurable parameters associated with a Namespace, client, or service that determines how Temporal behaves for that scope. You can configure many of these settings when creating or editing a Namespace via the UI or CLI (`tcld`).

You must also set Namespaces in your SDK Client to isolate your Workflow Executions to the Namespace. If you do not set a Namespace, all Workflow Executions started using the Client will be associated with the `default` Namespace. This means, you must have a default Namespace called `default` registered with your Temporal Service.

Here are some of the typical Namespace settings you’re able to configure:

| Setting | Description |
|---------|-------------|
| `namespace` (SDK/client) | The name of the Namespace your client is scoped to |
| `retention` | How long workflow execution history is kept |
| `certificate` | The client certificate used for mTLS authentication |
| `codec_server_endpoint` | URL to a Codec Server for decrypting encrypted payloads in the UI |
| `default_task_queue` | The task queue used if none is specified in the workflow code |
| `search_attributes` | Custom fields that allow filtering and querying workflow executions |
| `data_converter` | Used to serialize/deserialize and encrypt/decrypt workflow payloads |
| `visibility settings` | Controls how workflow status data is indexed and queried |

## Worker deployment and performance

This document outlines best practices for deploying and optimizing Workers to ensure high performance, reliability, and
scalability. It covers deployment strategies, scaling techniques, tuning recommendations, and monitoring approaches to
help you get the most out of your Temporal Workers.

We also provide a reference application, the Order Management System (OMS), that demonstrates the deployment best
practices in action. You can find the OMS codebase on
[GitHub](https://github.com/temporalio/reference-app-orders-go/tree/main/docs).

Designing a comprehensive Worker deployment strategy to optimize production performance involves many considerations. We
provide a quick checklist to help you get started. Before deploying Workers to production, ensure you address the
following. Follow the links to the relevant sections for more details.

- **[Configure each Worker appropriately](#actively-tune-worker-options-instead-of-relying-on-defaults)**: Actively tune
  Worker options based on your code, language runtime limits, and system resource constraints. Don't rely on defaults,
  which are designed for ease in development and testing, but not optimal for production environments.
- **[Deploy enough Workers](#interpret-metrics-as-a-whole)**: Monitor performance metrics and scale Workers to meet your
  workload requirements.
- **[Separate Task Queues logically](#separate-task-queues-logically)**: Size and split work across Task types
  (Activities and Workflows) and Task Queues based on workload characteristics.
- **[Version Workers for safe deployments](#use-worker-versioning-to-safely-deploy-new-workflow-code)**: Ensure you can
  deploy new Workflow code without breaking running Executions.
- **Run benchmarks**: Test your configuration under realistic load to confirm limits and settings are appropriate for
  your environment.

## Deployment and lifecycle management

Well-designed Worker deployment ensures resilience, observability, and maintainability. A Worker should be treated as a
long-running service that can be deployed, upgraded, and scaled in a controlled way.

### Package and configure Workers for flexibility

Workers should be artifacts produced by a CI/CD pipeline. Inject all required parameters for connecting to Temporal
Cloud or a self-hosted Temporal Service at runtime via environment variables, configuration files, or command-line
parameters. This allows for more granularity, easier testability, easier upgrades, scalability, and isolation of
Workers.

In the order management reference app, Workers are packaged as Docker images with configuration provided via environment
variables and mounted configuration files. The following Dockerfile uses a multi-stage build to create a minimal,
production-ready Worker image:

{/* SNIPSTART oms-dockerfile-worker */}
[Dockerfile](https://github.com/temporalio/reference-app-orders-go/blob/main/Dockerfile)

{/* SNIPEND oms-dockerfile-worker */}

This Dockerfile uses a multi-stage build pattern with two stages:

1. `oms-builder` stage: compiles the Worker binary.

1. Copies dependency files and downloads dependencies using BuildKit cache mounts to speed up subsequent builds.
   2. Copies the application code and builds a statically linked binary that doesn't require external libraries at
      runtime.

2. `oms-worker` stage: creates a minimal final image.

1. Copies only the compiled binary from the `oms-builder` stage.
   2. Sets the entrypoint to run the Worker process.

The entrypoint `oms worker` starts the Worker process, which reads configuration from environment variables at runtime.
For example, the
[Billing Worker deployment in Kubernetes](https://github.com/temporalio/reference-app-orders-go/blob/main/deployments/k8s/billing-worker-deployment.yaml)
uses environment variables to configure the Worker:

{/* SNIPSTART oms-billing-worker-deployment {"selectedLines": ["20-35"]} */}
[deployments/k8s/billing-worker-deployment.yaml](https://github.com/temporalio/reference-app-orders-go/blob/main/deployments/k8s/billing-worker-deployment.yaml)

**Examples:**

Example 1 (yaml):
```yaml
temporal-ui:
  container_name: temporal-ui
  depends_on:
    - temporal
  environment:
    - TEMPORAL_GRPC_ENDPOINT=temporal:7233
    - TEMPORAL_ADDRESS=temporal:7233
    - TEMPORAL_AUTH_ENABLED=true
    - TEMPORAL_AUTH_PROVIDER_URL=https://example.com
    - TEMPORAL_AUTH_CLIENT_ID=xxxxxxxxxxxxxx
    - TEMPORAL_AUTH_CLIENT_SECRET=xxxxxxxxxxxxxx
    - TEMPORAL_AUTH_CALLBACK_URL=https://your-domain/auth/sso/callback
    - TEMPORAL_AUTH_SCOPES=openid profile email
  image: temporalio/ui:latest
  networks:
    - temporal-network
  ports:
    - 8080:8080
```

Example 2 (go):
```go
role := authorization.RoleReader | authorization.RoleWriter
```

Example 3 (go):
```go
provider := authorization.NewDefaultTokenKeyProvider(cfg, logger)
```

Example 4 (unknown):
```unknown
Bearer <token>
```

---

## Set your scrape configuration targets to the ports exposed on your endpoints in the SDK.

**URL:** llms-txt#set-your-scrape-configuration-targets-to-the-ports-exposed-on-your-endpoints-in-the-sdk.

**Contents:**
- Grafana data sources configuration {#grafana-data-sources-configuration}
  - Grafana dashboards setup
- PromQL Metrics
- Temporal Cloud metrics reference
- Available Temporal Cloud metrics {#available-metrics}
  - Frontend Service metrics {#frontend}
  - Poll metrics {#poll}
  - Replication lag metrics {#replication-lag}
  - Schedule metrics {#schedule}
  - Service latency metrics {#service-latency}

scrape_configs:
  - job_name: 'temporalsdkmetrics'
    metrics_path: /metrics
    scheme: http
    static_configs:
      - targets:
          # This is the scrape endpoint where Prometheus listens for SDK metrics.
          - localhost:8077
        # You can have multiple targets here, provided they are set up in your application code.
text
temporal_cloud_v0_poll_success_count{__rollup__="true", operation="TaskQueueMgr", task_type="Activity", temporal_account="12345", temporal_namespace="your_namespace.12345", temporal_service_type="matching"}
yaml
   frontend.keepAliveMaxConnectionAge:
   - value: "2h"
   yaml
   dcRedirectionPolicy:
      policy: "all-apis-forwarding"

clusterMetadata:
   enableGlobalNamespace: true # add this
   failoverVersionIncrement: 1000000 # to match failoverVersionIncrement in our migration server
   masterClusterName: _NO_CHANGE_
   currentClusterName: _NO_CHANGE_
   clusterInformation:
      _NO_CHANGE_:
         enabled: true
         initialFailoverVersion: [1,100] # pick a unique number between 1 and 100 for each server 
         rpcName: _NO_CHANGE_
         rpcAddress: _NO_CHANGE_
   yaml
   "failoverVersionIncrement": "1000000",
   "initialFailoverVersion": "the number you picked"
   "isGlobalNamespaceEnabled": true
   go
   go get github.com/temporalio/cloud-sdk-go
   go

"github.com/temporalio/cloud-sdk-go/client"
   )
   command
   git clone https://github.com/temporalio/cloud-api.git
   cd cloud-api
   python
   python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ *.proto
   bash
   urn:auth0:prod-tmprl:ACCOUNT_ID-saml
   bash
   urn:auth0:prod-tmprl:f45a2-saml
   bash
   https://login.tmprl.cloud/login/callback?connection=ACCOUNT_ID-saml
   bash
   https://login.tmprl.cloud/login/callback?connection=f45a2-saml
   bash
   https://cloud.temporal.io/login/saml?connection=ACCOUNT_ID-saml
   bash
   https://cloud.temporal.io/login/saml?connection=f45a2-saml
   bash
   https://login.tmprl.cloud/login/callback?connection=ACCOUNT_ID-saml
   bash
   https://login.tmprl.cloud/login/callback?connection=f45a2-saml
   bash
   urn:auth0:prod-tmprl:ACCOUNT_ID-saml
   bash
   urn:auth0:prod-tmprl:f45a2-saml
   
avg_over_time((
    (

(
            sum(increase(temporal_cloud_v1_frontend_service_request_count{temporal_namespace=~"$namespace", operation=~"StartWorkflowExecution|SignalWorkflowExecution|SignalWithStartWorkflowExecution|RequestCancelWorkflowExecution|TerminateWorkflowExecution"}[10m]))
            -
            sum(increase(temporal_cloud_v1_frontend_service_error_count{temporal_namespace=~"$namespace", operation=~"StartWorkflowExecution|SignalWorkflowExecution|SignalWithStartWorkflowExecution|RequestCancelWorkflowExecution|TerminateWorkflowExecution"}[10m]))
        )
        /
        sum(increase(temporal_cloud_v1_frontend_service_request_count{temporal_namespace=~"$namespace", operation=~"StartWorkflowExecution|SignalWorkflowExecution|SignalWithStartWorkflowExecution|RequestCancelWorkflowExecution|TerminateWorkflowExecution"}[10m]))
    )

Activity Failure --> Retry Logic --> More Activity Failures --> Workflow Decision --> Potential Workflow Failure

workflow_failure_rate = temporal_cloud_v1_workflow_failed_count / temporal_activity_execution_failed

activity_success_rate = (total_activities - temporal_activity_execution_failed) / total_activities
bash
tcld account metrics accepted-client-ca add --request-id <request_id> --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca add --resource-version <etag> --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca add --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca add --ca-certificate-file <path>
bash
tcld account metrics accepted-client-ca remove --request-id <request_id> --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca remove --resource-version <etag> --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca remove --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca remove --ca-certificate-file <path>
bash
tcld account metrics accepted-client-ca remove --ca-certificate-fingerprint <fingerprint>
bash
tcld account metrics accepted-client-ca set --request-id <request_id> --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca set --resource-version <etag> --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca set --ca-certificate <encoded_certificate>
bash
tcld account metrics accepted-client-ca set --ca-certificate-file <path>
bash
tcld apikey create --name <name>
bash
tcld apikey create --name <name> --description "Your API Key"
bash
tcld apikey create --name <name> --duration 24h
bash
tcld apikey create --name <name> --expiry '2023-11-28T09:23:24-08:00'
bash
tcld apikey create --name <name> --request-id <request_id>
bash
tcld apikey get --id <apikey_id>
bash
tcld apikey list
bash
tcld apikey delete --id <apikey_id>
bash
tcld apikey delete --id <apikey_id> --resource-version <version>
bash
tcld apikey delete --id <apikey_id> --request-id <request_id>
bash
tcld apikey disable --id <apikey_id>
bash
tcld apikey disable --id <apikey_id> --resource-version <version>
bash
tcld apikey disable --id <apikey_id> --request-id <request_id>
bash
tcld apikey enable --id <apikey_id>
bash
tcld apikey enable --id <apikey_id> --resource-version <version>
bash
tcld apikey enable --id <apikey_id> --request-id <request_id>
json
[
  {
    "Name": "enable-apikey",
    "Value": true
  }
]
json
Feature flag enable-apikey is now true
bash
tcld generate-certificates certificate-authority-certificate --organization <value>
bash
tcld generate-certificates certificate-authority-certificate --validity-period <value>
bash
tcld generate-certificates certificate-authority-certificate --ca-certificate-file <path>
bash
tcld generate-certificates certificate-authority-certificate --ca-key-file <path>
bash
tcld generate-certificates certificate-authority-certificate --rsa-algorithm <boolean>
bash
tcld generate-certificates end-entity-certificate --organization <value>
bash
tcld generate-certificates end-entity-certificate --organization-unit <value>
bash
tcld generate-certificates end-entity-certificate --validity-period <value>
bash
tcld generate-certificates end-entity-certificate --ca-certificate-file <path>
bash
tcld generate-certificates end-entity-certificate --ca-key-file <path>
bash
tcld generate-certificates end-entity-certificate --certificate-file <path>
bash
tcld generate-certificates end-entity-certificate --key-file <path>
bash
brew install temporalio/brew/tcld
bash
   go version
   bash
   git clone https://github.com/temporalio/tcld.git
   cd tcld
   make
   bash
   cp tcld /usr/local/bin/tcld
   bash
   tcld version
   bash
tcld namespace add-region \
    --namespace <namespace_id> \
    --region <replica_region>
bash
tcld --api-key <your_api_key> \
    add-region \
    --namespace <namespace_id> \
    --region <replica_region>
bash
tcld namespace create \
    --namespace <namespace_id> \
    --region <primary_region> [\]
    [--region <replica_region>] // if adding replica
bash
tcld --api-key <your_api_key> \
    namespace create \
    --namespace <namespace_id> \
    --region <primary_region> [\]
    [--region <replica_region>] // if adding replica
bash
tcld namespace create \
    --namespace <namespace_id> \
    --cloud-provider aws \
    --region us-west-2 \
    --retention-days 60 \
    --certificate-filter-input '{"filters": [{"commonName": "test1"}]}' \
    --user-namespace-permission "user@example.com=Admin" \
    --search-attribute "customer_id=Int" \
    --search-attribute "customer_name=Text" \
    --endpoint "https://test-codec-server.com" \
    --pass-access-token \
    --include-credentials \
    --tag "key=value"
bash
tcld namespace create \
    --namespace <namespace_id> \
    --cloud-provider aws \
    --region us-west-2 \
    --retention-days 60 \
    --certificate-filter-input '{"filters": [{"commonName": "test1"}]}' \
    --user-namespace-permission "user@example.com=Admin" \
    --search-attribute "customer_id=Int" \
    --search-attribute "customer_name=Text" \
    --endpoint "https://test-codec-server.com" \
    --pass-access-token \
    --include-credentials \
    --connectivity-rule-ids <rule_id1> \
    --connectivity-rule-ids <rule_id2> // if adding multiple rules
bash
tcld namespace delete \
    --namespace <namespace_id>
bash
tcld namespace delete-region \
    --namespace <namespace_id>\
    --region <replica_region>
bash
tcld --api-key <your_api_key> \
    delete-region \
    --namespace <namespace_id> \
    --region <replica_region>
bash
tcld namespace failover \
    --namespace <namespace_id> \
    --region <target_region>
bash
tcld --api-key <your_api_key> \
    namespace failover \
    --namespace <namespace_id> \
    --region <target_region>
bash
tcld namespace get \
    --namespace <namespace_id>
bash
tcld namespace export s3 create \
    --namespace <namespace_id> \
    --sink-name <sink_name> \
    --s3-bucket-name <bucket_name> \
    --role-arn <role_arn>
bash
tcld namespace export s3 get \
    --namespace <namespace_id> \
    --sink-name <sink_name>
bash
tcld namespace export s3 delete \
    --namespace <namespace_id> \
    --sink-name <sink_name>
bash
tcld namespace export s3 list \
    --namespace <namespace_id>
bash
tcld namespace export s3 update \
    --namespace <namespace_id> \
    --sink-name <sink_name> \
    --enabled true
bash
tcld namespace export s3 validate \
    --namespace <namespace_id> \
    --sink-name <sink_name> \
    --s3-bucket-name <bucket_name> \
    --role-arn <role_arn>
bash
tcld namespace accepted-client-ca add \
    --namespace <namespace_id> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca add \
    --request-id <request_id> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca add \
    --resource-version <etag> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca add \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca add \
    --ca-certificate-file <path>
bash
tcld namespace accepted-client-ca list \
    --namespace <namespace_id>
bash
tcld namespace accepted-client-ca remove \
    --namespace <namespace_id> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca remove \
    --request-id <request_id> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca remove \
    --resource-version <etag> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca remove \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca remove \
    --ca-certificate-file <path>
bash
tcld namespace accepted-client-ca remove \
    --ca-certificate-fingerprint <fingerprint>

-----BEGIN CERTIFICATE-----
   ... old CA cert ...
   -----END CERTIFICATE-----
   -----BEGIN CERTIFICATE-----
   ... new CA cert ...
   -----END CERTIFICATE-----
   bash
   tcld namespace accepted-client-ca set \
       --ca-certificate-file <path>
   bash
tcld namespace accepted-client-ca set \
    --namespace <namespace_id>
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca set \
    --request-id <request_id> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca set \
    --resource-version <etag> \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca set \
    --ca-certificate <encoded_certificate>
bash
tcld namespace accepted-client-ca set \
    --ca-certificate-file <path>
bash
tcld namespace certificate-filters add \
    --namespace <namespace_id> \
    --certificate-filter-file <file>
bash
tcld namespace certificate-filters add \
    --request-id <request_id> \
    --certificate-filter-file <file>
bash
tcld namespace certificate-filters add \
    --resource-version <etag> \
    --certificate-filter-file <file>
bash
tcld namespace certificate-filters add \
    --certificate-filter-file <file>
bash
tcld namespace certificate-filters add \
    --certificate-filter-input <JSON>
bash
tcld namespace certificate-filters clear \
    --namespace <namespace_id>
bash
tcld namespace certificate-filters clear
    --request-id <request_id>
bash
tcld namespace certificate-filters clear \
    --resource-version <etag>
bash
tcld namespace certificate-filters export \
    --certificate-filter-file <path>
bash
tcld namespace certificate-filters import \
    --namespace <namespace_id> \
    --certificate-filter-input <json>
bash
tcld namespace certificate-filters import \
    --request-id <request_id> \
    --certificate-filter-input <json>
bash
tcld namespace certificate-filters import \
    --resource-version <etag> \
    --certificate-filter-input <json>
bash
tcld namespace certificate-filters import \
    --certificate-filter-file <path>
bash
tcld namespace certificate-filters import \
    --certificate-filter-input <json>
bash
tcld namespace certificate-filters import \
    --namespace <namespace_id> \
    --certificate-filter-input <json>
bash
tcld namespace certificate-filters import \
    --request-id <request_id> \
    --certificate-filter-input <json>
bash
tcld namespace certificate-filters import \
    --resource-version <etag> \
    --certificate-filter-input <json>
bash
tcld namespace search-attributes add \
    --namespace <namespace_id> \
    --search-attribute <value>
bash
tcld namespace search-attributes add \
    --request-id <request_id> \
    --search-attribute <value>
bash
tcld namespace search-attributes add \
    --resource-version <etag> \
    --search-attribute <value>
bash
tcld namespace search-attributes add \
    --search-attribute "YourSearchAttribute1=Text" \
    --search-attribute "YourSearchAttribute2=Double"
bash
tcld namespace search-attributes rename \
    --namespace <namespace_id> \
    --existing-name <value> \
    --new-name <value>
bash
tcld namespace search-attributes rename \
    --request-id <request_id> \
    --existing-name <value> \
    --new-name <value>
bash
tcld namespace search-attributes rename \
    --resource-version <etag> \
    --existing-name <value> \
    --new-name <value>
bash
tcld namespace search-attributes rename \
    --existing-name <value> \
    --new-name <value>
bash
tcld namespace search-attributes rename \
    --existing-name <value> \
    --new-name <value>
bash
tcld namespace retention get \
    --namespace <namespace_id>
bash
tcld namespace retention set \
    --namespace <namespace_id> \
    --retention-days <retention_days>
bash
tcld namespace update-codec-server \
    --namespace <namespace_id> \
    --endpoint <http_url>
bash
tcld namespace update-codec-server \
    --namespace <namespace_id> \
    --endpoint <https_url>
bash
tcld namespace update-codec-server \
    --namespace <namespace_id> \
    --endpoint <https_url> \
    --pass-access-token <bool>
bash
tcld namespace update-codec-server \
    --namespace <namespace_id> \
    --endpoint <https_url> \
    --include-credentials true

tcld namespace update-high-availability \
    --namespace <namespace_id> \
    --disable-auto-failover=true

tcld --api-key <your_api_key> \
    namespace update-high-availability \
    --namespace <namespace_id> \
    --disable-auto-failover=true
bash
tcld namespace tags upsert \
    --namespace <namespace_id> \
    --tag "key1=value1" \
    --tag "key2=updated"
bash
tcld namespace tags remove \
    --namespace <namespace_id> \
    --tag-key "key1" \
    --tag-key "key2"
bash
tcld request get --request-id <request_id>
command
tcld user delete --user-email <test@example.com>
command
tcld user delete --user-id <test-user-id>
command
tcld user delete --user-email <test@example.com>
command
tcld user delete --user-id <test-user-id>
command
tcld user invite --user-email <test@example.com> --account-role developer --namespace-permission ns1=Admin --namespace-permission ns2=Write --request-id <123456>
command
tcld user list
command
tcld user list --namespace <namespace_id>
bash
tcld user resend-invite --user-email <test@example.com>
bash
tcld user resend-invite --user-id <test-user-id>
command
tcld user set-account-role --user-email <test@example.com> --account-role Developer
command
tcld user set-account-role --user-id <test-user-id> --account-role Developer
command
tcld user set-namespace-permissions --user-email <test@example.com>
command
tcld user set-namespace-permissions --user-id <test-user-id>
bash

**Examples:**

Example 1 (unknown):
```unknown
See the [Prometheus documentation](https://prometheus.io/docs/introduction/first_steps/) for more details on how you can run Prometheus locally or using Docker.

Note that Temporal Cloud exposes metrics through a [Prometheus HTTP API endpoint](https://prometheus.io/docs/prometheus/latest/querying/api/) (not a scrape endpoint) that can be configured as a data source in Grafana.
The Prometheus configuration described here is for scraping metrics data on endpoints for SDK metrics only.

To check whether Prometheus is receiving metrics from your SDK target, go to [http://localhost:9090](http://localhost:9090) and navigate to **Status&nbsp;> Targets**.
The status of your target endpoint defined in your configuration appears here.

## Grafana data sources configuration {#grafana-data-sources-configuration}

**How to configure data sources for Temporal Cloud and SDK metrics in Grafana.**

Depending on how you use Grafana, you can either install and run it locally, run it as a Docker container, or log in to Grafana Cloud to set up your data sources.

If you have installed and are running Grafana locally, go to [http://localhost:3000](http://localhost:3000) and sign in.

You must configure your Temporal Cloud and SDK metrics data sources separately in Grafana.

To add the Temporal Cloud Prometheus HTTP API endpoint that we generated in the [Temporal Cloud metrics setup](/production-deployment/cloud/metrics/general-setup) section, do the following:

1. Go to **Configuration&nbsp;> Data sources**.
1. Select **Add data source&nbsp;> Prometheus**.
1. Enter a name for your Temporal Cloud metrics data source, such as _Temporal Cloud metrics_.
1. In the **Connection** section, paste the URL that was generated in the Observability section on the Temporal Cloud UI.
1. The **Authentication** section may be left as **No Authentication**.
1. In the **TLS Settings** section, select **TLS Client Authentication**:
   - Leave **ServerName** blank. This is not required.
   - Paste in your end-entity certificate and key.
   - Note that the end-entity certificate used here must be part of the certificate chain with the root CA certificates used in your [Temporal Cloud observability setup](/production-deployment/cloud/metrics/general-setup).
     <ZoomingImage src="/img/cloud/prometheus/add-prometheus-api-endpoint.png" alt="Data source configuration in Grafana" />
1. Click **Save and test** to verify that the data source is working.

If you see issues in setting this data source, verify your CA certificate chain and ensure that you are setting the correct certificates in your Temporal Cloud observability setup and in the TLS authentication in Grafana.

To add the SDK metrics Prometheus endpoint that we configured in the [SDK metrics setup](#sdk-metrics-setup) and [Prometheus configuration for SDK metrics](#prometheus-configuration) sections, do the following:

1. Go to **Configuration&nbsp;> Data sources**.
2. Select **Add data source&nbsp;> Prometheus**.
3. Enter a name for your Temporal Cloud metrics data source, such as _Temporal SDK metrics_.
4. In the **HTTP** section, enter your Prometheus endpoint in the URL field.
   If running Prometheus locally as described in the examples in this article, enter `http://localhost:9090`.
5. For this example, enable **Skip TLS Verify** in the **Auth** section.
6. Click **Save and test** to verify that the data source is working.

If you see issues in setting this data source, check whether the endpoints set in your SDKs are showing metrics.
If you don't see your SDK metrics at the scrape endpoints defined, check whether your Workers and Workflow Executions are running.
If you see metrics on the scrape endpoints, but Prometheus shows your targets are down, then there is an issue with connecting to the targets set in your SDKs.
Verify your Prometheus configuration and restart Prometheus.

If you're running Grafana as a container, you can set your SDK metrics Prometheus data source in your Grafana configuration.
See the example Grafana configuration described in the [Prometheus and Grafana setup for open-source Temporal Service](/self-hosted-guide/monitoring#grafana) article.

### Grafana dashboards setup

To set up dashboards in Grafana, you can use the UI or configure them directly in your Grafana deployment.

:::tip

Temporal provides community-driven example dashboards for [Temporal Cloud](https://github.com/temporalio/dashboards/tree/master/cloud) and [Temporal SDKs](https://github.com/temporalio/dashboards/tree/master/sdk) that you can customize to meet your needs.

:::

To import a dashboard in Grafana:

1. In the left-hand navigation bar, select **Dashboards** > **Import dashboard**.
2. You can either copy and paste the JSON from the [Temporal Cloud](https://github.com/temporalio/dashboards/tree/master/cloud) and [Temporal SDK](https://github.com/temporalio/dashboards/tree/master/sdk) sample dashboards, or import the JSON files into Grafana.
3. Save the dashboard and review the metrics data in the graphs.

To configure dashboards with the UI:

1. Go to **Create > Dashboard** and add an empty panel.
2. On the **Panel configuration** page, in the **Query** tab, select the "Temporal Cloud metrics" or "Temporal SDK metrics" data source that you configured earlier.
   If you need to add multiple queries from both data sources, choose `–Mixed–`.
3. Add your metrics queries:
   - For Temporal Cloud metrics, expand the **Metrics browser** and select the metrics you want.
     You can also select associated labels and values to sort the query data.
     The [Cloud metrics documentation](/production-deployment/cloud/metrics/reference) lists all metrics emitted from Temporal Cloud.
   - For Temporal SDK metrics, expand the **Metrics browser** and select the metrics you want.
     A list of Worker performance metrics is described in the [Developer's Guide - Worker performance](/develop/worker-performance).
     All SDK-related metrics are listed in the [SDK metrics](/references/sdk-metrics) reference.
4. The graph should now display data based on your selected queries.
   Note that SDK metrics will only show if you have Workflow Execution data and running Workers.
   If you don't see SDK metrics, run your Worker and Workflow Executions, then monitor the dashboard.

---

## PromQL Metrics

:::tip

Need to scrape metrics into your observability stack? Try out the new [OpenMetrics endpoint](/cloud/metrics/openmetrics).

:::

Metrics for all Namespaces in your account are available from your metrics endpoint. Keep in mind that your Temporal Cloud metrics lag real-time performance by about one minute. Temporal Cloud also only retains raw metrics for seven days.

To ensure security of your metrics, a CA certificate dedicated to observability is required.
Only clients that use certificates signed by that CA, or that chain up to the CA, can query the metrics endpoint.
For more information about CA certificates in Temporal Cloud, see [Certificate requirements](/cloud/certificates#certificate-requirements).

- [General setup](/production-deployment/cloud/metrics/general-setup)
- [Available metrics](/production-deployment/cloud/metrics/reference)
- [Prometheus & Grafana setup](/cloud/metrics/prometheus-grafana)
- [Datadog setup](/cloud/metrics/datadog)

---

## Temporal Cloud metrics reference

A metric is a measurement or data point that provides insights into the performance and health of a system.
This document describes the metrics available on the Temporal Cloud platform.
Temporal Cloud metrics help you monitor performance and troubleshoot errors.
They provide insights into different aspects of the Service.

This document describes:

- **[Available Temporal Cloud metrics](#available-metrics)**:
  The metrics emitted by Temporal Cloud include counts of gRPC errors, requests, successful task matches to a poller, and more.
- **[Metrics labels](#metrics-labels)**:
  Temporal Cloud metrics labels can filter metrics and help categorize and differentiate results.
- **[Operations](#metrics-operations)**:
  An operation is a special type of label that categorizes the type of operation being performed when the metric was collected.

:::info SDK METRICS

This document discusses metrics emitted by [Temporal Cloud](/cloud).
Temporal SDKs also emit metrics, sourced from Temporal Clients and Worker processes.
You can find information about Temporal SDK metrics on its [dedicated page](/references/sdk-metrics).

Please note:

- SDK metrics start with the phrase `temporal_`.
- Temporal Cloud metrics start with `temporal_cloud_`.

:::

## Available Temporal Cloud metrics {#available-metrics}

**What metrics are emitted from Temporal Cloud?**

The following metrics are emitted for your Namespaces:

### Frontend Service metrics {#frontend}

#### temporal_cloud_v0_frontend_service_error_count

This is a count of gRPC errors returned aggregated by operation.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_frontend_service_request_count

This is a count of gRPC requests received aggregated by operation.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_resource_exhausted_error_count

gRPC requests received that were rate-limited by Temporal Cloud, aggregated by cause.
Labels: temporal_account, temporal_namespace, resource_exhausted_cause

#### temporal_cloud_v0_state_transition_count

Count of state transitions for each Namespace.

#### temporal_cloud_v0_total_action_count

Approximate count of Temporal Cloud Actions.
Labels: temporal_account, temporal_namespace, is_background, namespace_mode

### Poll metrics {#poll}

#### temporal_cloud_v0_poll_success_count

Tasks that are successfully matched to a poller.
Labels: temporal_account, temporal_namespace, operation, task_type, temporal_service_type

#### temporal_cloud_v0_poll_success_sync_count

Tasks that are successfully sync matched to a poller.
Labels: temporal_account, temporal_namespace, operation, task_type, temporal_service_type

#### temporal_cloud_v0_poll_timeout_count

When no tasks are available for a poller before timing out.
Labels: temporal_account, temporal_namespace, operation, task_type, temporal_service_type

### Replication lag metrics {#replication-lag}

#### temporal_cloud_v0_replication_lag_bucket

A histogram of [replication lag](/cloud/high-availability/monitoring#replication-lag-metric) during a specific time interval for a Namespace with high availability.
Labels: temporal_account, temporal_namespace, le

#### temporal_cloud_v0_replication_lag_count

The [replication lag](/cloud/high-availability/monitoring#replication-lag-metric) count during a specific time interval for a Namespace with high availability.
Labels: temporal_account, temporal_namespace

#### temporal_cloud_v0_replication_lag_sum

The sum of [replication lag](/cloud/high-availability/monitoring#replication-lag-metric) during a specific time interval for a Namespace with high availability.
Labels: temporal_account, temporal_namespace

### Schedule metrics {#schedule}

#### temporal_cloud_v0_schedule_action_success_count

Successful execution of a Scheduled Workflow.
Labels: temporal_account, temporal_namespace

#### temporal_cloud_v0_schedule_buffer_overruns_count

When average schedule run length is greater than average schedule interval while a `buffer_all` overlap policy is configured.
Labels: temporal_account, temporal_namespace

#### temporal_cloud_v0_schedule_missed_catchup_window_count

Skipped Scheduled executions when Workflows were delayed longer than the catchup window.
Labels: temporal_account, temporal_namespace

#### temporal_cloud_v0_schedule_rate_limited_count

Workflows that were delayed due to exceeding a rate limit.
Labels: temporal_account, temporal_namespace

### Service latency metrics {#service-latency}

#### temporal_cloud_v0_service_latency_bucket

Latency for `SignalWithStartWorkflowExecution`, `SignalWorkflowExecution`, `StartWorkflowExecution` operations.
Labels: temporal_account, temporal_namespace, le, operation, temporal_service_type

#### temporal_cloud_v0_service_latency_count

Count of latency observations for `SignalWithStartWorkflowExecution`, `SignalWorkflowExecution`, `StartWorkflowExecution` operations.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_service_latency_sum

Sum of latency observation time for `SignalWithStartWorkflowExecution`, `SignalWorkflowExecution`, `StartWorkflowExecution` operations.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

### Workflow metrics {#workflow}

#### temporal_cloud_v0_workflow_cancel_count

Workflows canceled before completing execution.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_workflow_continued_as_new_count

Workflow Executions that were Continued-As-New from a past execution.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_workflow_failed_count

Workflows that failed before completion.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_workflow_success_count

Workflows that successfully completed.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_workflow_terminate_count

Workflows terminated before completing execution.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

#### temporal_cloud_v0_workflow_timeout_count

Workflows that timed out before completing execution.
Labels: temporal_account, temporal_namespace, operation, temporal_service_type

## Metrics labels {#metrics-labels}

**What labels can you use to filter metrics?**

Temporal Cloud metrics include key-value pairs called labels in their associated metadata.
Labels help you categorize and differentiate metrics for precise filtering, querying, and aggregation.
Use labels to specific attributes or compare values, such as numeric buckets in histograms.
This added context enhances the monitoring and analysis capabilities, providing deeper insights into your data.

Use the following labels to filter metrics:

| Label                      | Explanation                                                                                                                                                                                                                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `le`                       | Less than or equal to (`le`) is used in histograms to categorize observations into buckets based on their value being less than or equal to a predefined upper limit.                                                                                                                      |
| `operation`                | This includes gRPC operations and general Cloud operations such as:SignalWorkflowExecutionStartBatchOperationStartWorkflowExecutionTaskQueueMgrTerminateWorkflowExecutionUpdateNamespaceUpdateSchedule See: [Metric Operations](#metrics-operations) and [Temporal Cloud Operation reference](/references/operation-list)|
| `resource_exhausted_cause` | Cause for resource exhaustion.                                                                                                                                                                                                                                                             |
| `task_type`                | Activity, Workflow, or Nexus.                                                                                                                                                                                                                                                              |
| `temporal_account`         | Temporal Account.                                                                                                                                                                                                                                                                          |
| `temporal_namespace`       | Temporal Namespace.                                                                                                                                                                                                                                                                        |
| `temporal_service_type`    | Frontend or Matching or History or Worker.                                                                                                                                                                                                                                                 |
| `is_background`            | This label on `temporal_cloud_v0_total_action_count` indicates when actions are produced by a Temporal background job, for example: hourly Workflow Export.                                                                                                                                |
| `namespace_mode`           | This label on `temporal_cloud_v0_total_action_count` indicates if actions are produced by an active vs a standby Namespace. For a regular Namespace, `namespace_mode` will always be “active”.                                                                                             |

The following is an example of how you can filter metrics using labels:
```

Example 2 (unknown):
```unknown
## Operations {#metrics-operations}

**What operation labels are captured by Temporal Cloud?**

Operations are a special class of metrics label.
They describe the context during which a metric was captured.
Temporal Cloud includes the following operations labels:

- AdminDescribeMutableState
- AdminGetWorkflowExecutionRawHistory
- AdminGetWorkflowExecutionRawHistoryV2
- AdminReapplyEvents
- CountWorkflowExecutions
- CreateSchedule
- DeleteSchedule
- DeleteWorkflowExecution
- DescribeBatchOperation
- DescribeNamespace
- DescribeSchedule
- DescribeTaskQueue
- DescribeWorkflowExecution
- GetWorkerBuildIdCompatibility
- GetWorkerTaskReachability
- GetWorkflowExecutionHistory
- GetWorkflowExecutionHistoryReverse
- ListBatchOperations
- ListClosedWorkflowExecutions
- OperatorDeleteNamespace
- PatchSchedule
- PollActivityTaskQueue
- PollNexusTaskQueue
- PollWorkflowExecutionHistory
- PollWorkflowExecutionUpdate
- PollWorkflowTaskQueue
- QueryWorkflow
- RecordActivityTaskHeartbeat
- RecordActivityTaskHeartbeatById
- RegisterNamespace
- RequestCancelWorkflowExecution
- ResetStickyTaskQueue
- ResetWorkflowExecution
- RespondActivityTaskCanceled
- RespondActivityTaskCompleted
- RespondActivityTaskCompletedById
- RespondActivityTaskFailed
- RespondActivityTaskFailedById
- RespondNexusTaskCompleted
- RespondNexusTaskFailed
- RespondQueryTaskCompleted
- RespondWorkflowTaskCompleted
- RespondWorkflowTaskFailed
- SignalWithStartWorkflowExecution
- SignalWorkflowExecution
- StartBatchOperation
- StartWorkflowExecution
- StopBatchOperation
- TerminateWorkflowExecution
- UpdateNamespace
- UpdateSchedule
- UpdateWorkerBuildIdCompatibility
- UpdateWorkflowExecution

As the following table shows, certain [metrics groups](#available-metrics) support [operations](#metrics-operations) for aggregation and filtering:

| Metrics Group / Operations                      | All Operations | SignalWithStartWorkflowExecution / SignalWorkflowExecution / StartWorkflowExecution | TaskQueueMgr | CompletionStats |
| ----------------------------------------------- | -------------- | ----------------------------------------------------------------------------------- | ------------ | --------------- |
| **[Frontend Service Metrics](#frontend)**       | X              |                                                                                     |              |                 |
| **[Service Latency Metrics](#service-latency)** |                | X                                                                                   |              |                 |
| **[Poll Metrics](#poll)**                       |                |                                                                                     | X            |                 |
| **[Workflow Metrics](#workflow)**               |                |                                                                                     |              | X               |

---

## Automated Migration

Automated migration is designed to provide a zero-downtime, secure means of migrating to Temporal Cloud. This guide outlines the current process
for transitioning workflows from a self-hosted setup to one hosted within Temporal Cloud.

:::tip Support, stability, and dependency info

Automated migration is currently in [Pre-release](/evaluate/development-production-features/release-stages#pre-release).

:::

### Solution overview

As illustrated below, there are 2 components that support automated migrations:

1. Migration proxy - The [s2s proxy](https://hub.docker.com/r/temporalio/s2s-proxy/tags) provides a security layer between the self-hosted server
   and the migration server. The customer-side proxy is installed on your infrastructure, while the cloud-side proxy is managed by Temporal. Communications to the
   proxies are secured via [mutual TLS](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/) (mTLS).
2. Migration server - A Temporal service (server) enables secure connections between your self-hosted setup and Temporal Cloud. It provides the core
   functionality of the service.

![Temporal automated migration components](/img/cloud/migration/auto-migration-components.png)

### Process overview

The migration process is separated into several phases, part of which involves coordinating with Temporal to create necessary cloud-side resources.

Migration involves the following phases:

1. Prepare - Preparing for a migration will require you to deploy a customer-side migration proxy, and will also involve coordinating with Temporal to
   configure a migration server.
2. Initiate - Use the _[StartMigrationRequest](https://pkg.go.dev/github.com/temporalio/tcld#readme-start-a-migration)_ API to specify namespaces for migration along with endpoint
   details.
   A corresponding namespace is created in Temporal Cloud with a “non-active” status. You will configure permissions and access controls during this phase.
3. Monitor - The _[GetMigrationResponse](https://pkg.go.dev/github.com/temporalio/tcld#readme-get-a-migration)_ API allows you to track replication progress, including workflows
   replicated, remaining workflows, and estimated
   time for completion.
4. Handover - Once replication is complete, you may use the _[HandoverNamespaceRequest](https://pkg.go.dev/github.com/temporalio/tcld#readme-perform-handover-during-a-migration)_ API to switch traffic between your source namespace (self-hosted)
   and target namespace (cloud). This is the opportunity to validate functionality within Temporal Cloud prior to finalizing the migration.
5. Finalize - Use _[ConfirmMigrationRequest](https://pkg.go.dev/github.com/temporalio/tcld#readme-confirm-a-migration)_ API to finalize the migration. In the event of issues, you may use
   the _[AbortMigrationRequest](https://pkg.go.dev/github.com/temporalio/tcld#readme-abort-a-migration)_ to
   roll-back changes without impacting your workflows. These APIs provide granular control over every step of the process, ensuring transparency and flexibility.

### Current limitations

The following are known limitations for the Pre-release phase of this service.

- OSS server versions 1.22 or newer are required. Refer to the [upgrade](https://docs.temporal.io/self-hosted-guide/upgrade-server#upgrade-server) procedure as needed.
- History shard counts must be a multiple of two.
- Enabling payload encryption as part of migration is not yet supported. If payloads are already [encrypted](https://docs.temporal.io/payload-codec#encryption) in your self-hosted server
  via data converter, then they will remain encrypted during and after migration.
- If you are using multi-cluster replication in your self-hosted setup and have previously failed over namespaces, then this may impact your eligibility for automated migration.
- If you have multiple self-hosted servers and they are all configured with the same cluster name (by default Temporal uses 'active' as cluster name), they cannot be connected to
  a single migration server simultaneously due to cluster name collision. There are 2 available options:
  1. Migrate one server at a time using a single migration server.
  2. Create multiple migration servers (one for each self-hosted server) if you need to migrate all servers simultaneously.
- OSS supports cross-namespace commands (e.g., parent-child, SignalExternal, CancelExternal) through the `system.enableCrossNamespaceCommands` configuration. This
  configuration is disabled on Temporal Cloud. If cross-namespace calls exist within workflow code, they must be updated or removed prior to migration.

### Getting started

To prepare for migration, you must first provide qualification details to Temporal via a support ticket. If eligible, the Temporal team will work with you to facilitate your migration.

Submit a support ticket with the following details:

- A list of your Temporal accounts
- Target Temporal Cloud service regions
- For each cluster, provide the server configuration by running `temporal operator cluster describe --address <frontend:7233> --output json` (see [notes](#alternative-commands-for-versions-1281-and-prior) for Temporal server version 1.28.1 and prior).
- Metrics for the namespaces to be migrated:
  - number of open/closed workflows
  - storage used
  - retention policy
  - any custom search attributes
  - peak request per second (RPS) and action per second (APS) - refer to [this document](https://docs.google.com/document/d/151xjeI53SBfJ94X1toi5krPp4oeyzJ6wVUrOBhgK714) for instructions on fetching these metrics
- If you use a SQL-based datastore for visibility, and you use custom search attributes, provide _CustomSearchAttributeAliases_ of your namespace by running
  temporal operator namespace describe using the [latest Temporal CLI](https://github.com/temporalio/cli).

:::warning

Proceed only when your request has been approved by Temporal.

:::

### Create cloud-side resources

Cloud-side resources must be in place prior to starting a migration. Complete the following procedure.

1. Create one or more empty namespaces in Temporal Cloud to serve as the migration targets. Since migration cannot proceed into a namespace that's already in use, these namespaces should
   remain empty (no workflows).
2. Create a support ticket requesting these namespaces be configured with [system limits](https://docs.temporal.io/cloud/limits)
   (including APS/RPS) matching your existing self-hosted workload.
3. Verify that a migration endpoint has been created in Temporal Cloud (e.g., `your-endpoint.{your-acct}.tmprl.cloud`). If you don't have one, request one via a support ticket.
4. Create any required custom search attributes used by your workflow.
5. If you need [private connectivity](https://docs.temporal.io/cloud/connectivity) for the namespace in Temporal Cloud, then prepare this setup in advance.

### Prepare your self-hosted service

1. Set the following [dynamic configurations](https://docs.temporal.io/references/dynamic-configuration) settings and then restart the Temporal frontend.
```

Example 3 (unknown):
```unknown
2. If not already enabled, enable _GlobalNamspace_ by updating the _clusterMetadata_ and the _dcRedirectionPolicy_ in your [server config yaml file](https://github.com/temporalio/temporal/tree/main/config) to
   the following and restart all Temporal services (frontend, history, matching, worker), starting with the frontend.
```

Example 4 (unknown):
```unknown
3. Run `temporal operator cluster describe` to check the output. The following output is expected:
```

---

## Consolidate non-critical task queues

**URL:** llms-txt#consolidate-non-critical-task-queues

**Contents:**
  - Monitoring Cardinality

- source_labels: [temporal_task_queue]
  regex: '(critical-queue|payment-queue)'
  target_label: __tmp_keep_original
  replacement: 'true'
  
- source_labels: [__tmp_keep_original]
  regex: ''
  target_label: temporal_task_queue
  replacement: 'other'
  
- regex: '__tmp_keep_original'
  action: labeldrop

processors:
  filter:
    metrics:
      include:
        match_type: regexp
        expressions:
          # Only keep metrics with critical-queue or payment-queue
          - Label("temporal_task_queue") == nil or IsMatch(Label("temporal_task_queue"), "^(critical-queue|payment-queue)$")
shell

**Examples:**

Example 1 (unknown):
```unknown
#### OpenTelemetry Collector

To accomplish the same as Prometheus, a filter can be used in the collector along with any other processors.
```

Example 2 (unknown):
```unknown
### Monitoring Cardinality

Cardinality can be monitored using this PromQL query.
```

---
