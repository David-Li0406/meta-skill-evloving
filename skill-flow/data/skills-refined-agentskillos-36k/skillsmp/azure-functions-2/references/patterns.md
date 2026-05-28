# Azure Functions

## Patterns


---
  #### **Name**
Isolated Worker Model (.NET)
  #### **Description**
Modern .NET execution model with process isolation
  #### **When**
Building new .NET Azure Functions apps
  #### **Template**
    // Program.cs - Isolated Worker Model
    using Microsoft.Azure.Functions.Worker;
    using Microsoft.Extensions.DependencyInjection;
    using Microsoft.Extensions.Hosting;
    
    var host = new HostBuilder()
        .ConfigureFunctionsWorkerDefaults()
        .ConfigureServices(services =>
        {
            // Add Application Insights
            services.AddApplicationInsightsTelemetryWorkerService();
            services.ConfigureFunctionsApplicationInsights();
    
            // Add HttpClientFactory (prevents socket exhaustion)
            services.AddHttpClient();
    
            // Add your services
            services.AddSingleton<IMyService, MyService>();
        })
        .Build();
    
    host.Run();
    
    // HttpTriggerFunction.cs
    using Microsoft.Azure.Functions.Worker;
    using Microsoft.Azure.Functions.Worker.Http;
    using Microsoft.Extensions.Logging;
    
    public class HttpTriggerFunction
    {
        private readonly ILogger<HttpTriggerFunction> _logger;
        private readonly IMyService _service;
    
        public HttpTriggerFunction(
            ILogger<HttpTriggerFunction> logger,
            IMyService service)
        {
            _logger = logger;
            _service = service;
        }
    
        [Function("HttpTrigger")]
        public async Task<HttpResponseData> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequestData req)
        {
            _logger.LogInformation("Processing request");
    
            try
            {
                var result = await _service.ProcessAsync(req);
    
                var response = req.CreateResponse(HttpStatusCode.OK);
                await response.WriteAsJsonAsync(result);
                return response;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing request");
                var response = req.CreateResponse(HttpStatusCode.InternalServerError);
                await response.WriteAsJsonAsync(new { error = "Internal server error" });
                return response;
            }
        }
    }
    
  #### **Notes**
    - In-process model deprecated November 2026
    - Isolated worker supports .NET 8, 9, 10, and .NET Framework
    - Full dependency injection support
    - Custom middleware support

---
  #### **Name**
Node.js v4 Programming Model
  #### **Description**
Modern code-centric approach for TypeScript/JavaScript
  #### **When**
Building Node.js Azure Functions
  #### **Template**
    // src/functions/httpTrigger.ts
    import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
    
    export async function httpTrigger(
      request: HttpRequest,
      context: InvocationContext
    ): Promise<HttpResponseInit> {
      context.log(`Http function processed request for url "${request.url}"`);
    
      try {
        const name = request.query.get("name") || (await request.text()) || "world";
    
        return {
          status: 200,
          jsonBody: { message: `Hello, ${name}!` }
        };
      } catch (error) {
        context.error("Error processing request:", error);
        return {
          status: 500,
          jsonBody: { error: "Internal server error" }
        };
      }
    }
    
    // Register function with app object
    app.http("httpTrigger", {
      methods: ["GET", "POST"],
      authLevel: "function",
      handler: httpTrigger
    });
    
    // Timer trigger example
    app.timer("timerTrigger", {
      schedule: "0 */5 * * * *",  // Every 5 minutes
      handler: async (myTimer, context) => {
        context.log("Timer function executed at:", new Date().toISOString());
      }
    });
    
    // Blob trigger example
    app.storageBlob("blobTrigger", {
      path: "samples-workitems/{name}",
      connection: "AzureWebJobsStorage",
      handler: async (blob, context) => {
        context.log(`Blob trigger processing: ${context.triggerMetadata.name}`);
        context.log(`Blob size: ${blob.length} bytes`);
      }
    });
    
  #### **Notes**
    - v4 model is code-centric, no function.json files
    - Uses app object similar to Express.js
    - TypeScript first-class support
    - All triggers registered in code

---
  #### **Name**
Python v2 Programming Model
  #### **Description**
Decorator-based approach for Python functions
  #### **When**
Building Python Azure Functions
  #### **Template**
    # function_app.py
    import azure.functions as func
    import logging
    import json
    
    app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
    
    @app.route(route="hello", methods=["GET", "POST"])
    async def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
        logging.info("Python HTTP trigger function processed a request.")
    
        try:
            name = req.params.get("name")
            if not name:
                try:
                    req_body = req.get_json()
                    name = req_body.get("name")
                except ValueError:
                    pass
    
            if name:
                return func.HttpResponse(
                    json.dumps({"message": f"Hello, {name}!"}),
                    mimetype="application/json"
                )
            else:
                return func.HttpResponse(
                    json.dumps({"message": "Hello, World!"}),
                    mimetype="application/json"
                )
        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": "Internal server error"}),
                status_code=500,
                mimetype="application/json"
            )
    
    @app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer")
    def timer_trigger(myTimer: func.TimerRequest) -> None:
        logging.info("Timer trigger executed")
    
    @app.blob_trigger(arg_name="myblob", path="samples-workitems/{name}",
                      connection="AzureWebJobsStorage")
    def blob_trigger(myblob: func.InputStream):
        logging.info(f"Blob trigger: {myblob.name}, Size: {myblob.length} bytes")
    
    @app.queue_trigger(arg_name="msg", queue_name="myqueue",
                       connection="AzureWebJobsStorage")
    def queue_trigger(msg: func.QueueMessage) -> None:
        logging.info(f"Queue message: {msg.get_body().decode('utf-8')}")
    
  #### **Notes**
    - v2 model uses decorators, no function.json files
    - Python runs out-of-process (always isolated)
    - Linux-based hosting required for Python
    - Async functions supported

---
  #### **Name**
Durable Functions - Function Chaining
  #### **Description**
Sequential execution with state persistence
  #### **When**
Need sequential workflow with automatic retry
  #### **Template**
    // C# Isolated Worker - Function Chaining
    using Microsoft.Azure.Functions.Worker;
    using Microsoft.DurableTask;
    using Microsoft.DurableTask.Client;
    
    public class OrderWorkflow
    {
        [Function("OrderOrchestrator")]
        public static async Task<OrderResult> RunOrchestrator(
            [OrchestrationTrigger] TaskOrchestrationContext context)
        {
            var order = context.GetInput<Order>();
    
            // Functions execute sequentially, state persisted between each
            var validated = await context.CallActivityAsync<ValidatedOrder>(
                "ValidateOrder", order);
    
            var payment = await context.CallActivityAsync<PaymentResult>(
                "ProcessPayment", validated);
    
            var shipped = await context.CallActivityAsync<ShippingResult>(
                "ShipOrder", new ShipRequest { Order = validated, Payment = payment });
    
            var notification = await context.CallActivityAsync<bool>(
                "SendNotification", shipped);
    
            return new OrderResult
            {
                OrderId = order.Id,
                Status = "Completed",
                TrackingNumber = shipped.TrackingNumber
            };
        }
    
        [Function("ValidateOrder")]
        public static async Task<ValidatedOrder> ValidateOrder(
            [ActivityTrigger] Order order, FunctionContext context)
        {
            var logger = context.GetLogger<OrderWorkflow>();
            logger.LogInformation("Validating order {OrderId}", order.Id);
    
            // Validation logic...
            return new ValidatedOrder { /* ... */ };
        }
    
        [Function("ProcessPayment")]
        public static async Task<PaymentResult> ProcessPayment(
            [ActivityTrigger] ValidatedOrder order, FunctionContext context)
        {
            // Payment processing with built-in retry...
            return new PaymentResult { /* ... */ };
        }
    
        [Function("OrderWorkflow_HttpStart")]
        public static async Task<HttpResponseData> HttpStart(
            [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
            [DurableClient] DurableTaskClient client,
            FunctionContext context)
        {
            var order = await req.ReadFromJsonAsync<Order>();
            string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
                "OrderOrchestrator", order);
    
            return client.CreateCheckStatusResponse(req, instanceId);
        }
    }
    
  #### **Notes**
    - State automatically persisted between activities
    - Automatic retry on transient failures
    - Survives process restarts
    - Built-in status endpoint for monitoring

---
  #### **Name**
Durable Functions - Fan-Out/Fan-In
  #### **Description**
Parallel execution with result aggregation
  #### **When**
Processing multiple items in parallel
  #### **Template**
    // C# Isolated Worker - Fan-Out/Fan-In
    using Microsoft.Azure.Functions.Worker;
    using Microsoft.DurableTask;
    
    public class ParallelProcessing
    {
        [Function("ProcessImagesOrchestrator")]
        public static async Task<ProcessingResult> RunOrchestrator(
            [OrchestrationTrigger] TaskOrchestrationContext context)
        {
            var images = context.GetInput<List<string>>();
    
            // Fan-out: Start all tasks in parallel
            var tasks = images.Select(image =>
                context.CallActivityAsync<ImageResult>("ProcessImage", image));
    
            // Fan-in: Wait for all tasks to complete
            var results = await Task.WhenAll(tasks);
    
            // Aggregate results
            var successful = results.Count(r => r.Success);
            var failed = results.Count(r => !r.Success);
    
            return new ProcessingResult
            {
                TotalProcessed = results.Length,
                Successful = successful,
                Failed = failed,
                Results = results.ToList()
            };
        }
    
        [Function("ProcessImage")]
        public static async Task<ImageResult> ProcessImage(
            [ActivityTrigger] string imageUrl, FunctionContext context)
        {
            var logger = context.GetLogger<ParallelProcessing>();
            logger.LogInformation("Processing image: {Url}", imageUrl);
    
            try
            {
                // Image processing logic...
                await Task.Delay(1000); // Simulated work
    
                return new ImageResult
                {
                    Url = imageUrl,
                    Success = true,
                    ProcessedUrl = $"processed-{imageUrl}"
                };
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Failed to process {Url}", imageUrl);
                return new ImageResult { Url = imageUrl, Success = false };
            }
        }
    
        // Python equivalent
        // @app.orchestration_trigger(context_name="context")
        // def process_images_orchestrator(context: df.DurableOrchestrationContext):
        //     images = context.get_input()
        //
        //     # Fan-out: Create parallel tasks
        //     tasks = [context.call_activity("ProcessImage", img) for img in images]
        //
        //     # Fan-in: Wait for all
        //     results = yield context.task_all(tasks)
        //
        //     return {"processed": len(results), "results": results}
    }
    
  #### **Notes**
    - Parallel execution for independent tasks
    - Results aggregated when all complete
    - Memory efficient - only stores task IDs
    - Up to thousands of parallel activities

---
  #### **Name**
Cold Start Optimization
  #### **Description**
Minimize cold start latency in production
  #### **When**
Need fast response times in production
  #### **Template**
    // 1. Use Premium Plan with pre-warmed instances
    // host.json
    {
      "version": "2.0",
      "extensions": {
        "durableTask": {
          "hubName": "MyTaskHub"
        }
      },
      "functionTimeout": "00:30:00"
    }
    
    // 2. Add warmup trigger (Premium Plan)
    [Function("Warmup")]
    public static void Warmup(
        [WarmupTrigger] object warmupContext,
        FunctionContext context)
    {
        var logger = context.GetLogger("Warmup");
        logger.LogInformation("Warmup trigger executed - initializing dependencies");
    
        // Pre-initialize expensive resources
        // Database connections, HttpClients, etc.
    }
    
    // 3. Use static/singleton clients with DI
    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            // HttpClientFactory prevents socket exhaustion
            services.AddHttpClient<IMyApiClient, MyApiClient>(client =>
            {
                client.BaseAddress = new Uri("https://api.example.com");
                client.Timeout = TimeSpan.FromSeconds(30);
            });
    
            // Singleton for expensive initialization
            services.AddSingleton<IExpensiveService>(sp =>
            {
                // Initialize once, reuse across invocations
                return new ExpensiveService();
            });
        }
    }
    
    // 4. Reduce package size
    // .csproj - exclude unnecessary dependencies
    <PropertyGroup>
      <PublishTrimmed>true</PublishTrimmed>
      <TrimMode>partial</TrimMode>
    </PropertyGroup>
    
    // 5. Run from package deployment
    // Azure CLI
    // az functionapp deployment source config-zip \
    //   --resource-group myResourceGroup \
    //   --name myFunctionApp \
    //   --src myapp.zip \
    //   --build-remote true
    
  #### **Notes**
    - Cold starts improved ~53% across all regions/languages
    - Premium Plan provides pre-warmed instances
    - Warmup trigger initializes before traffic
    - Package deployment can reduce cold start

---
  #### **Name**
Queue Trigger with Error Handling
  #### **Description**
Reliable message processing with poison queue
  #### **When**
Processing messages from Azure Storage Queue
  #### **Template**
    // C# Isolated Worker - Queue Trigger
    using Microsoft.Azure.Functions.Worker;
    
    public class QueueProcessor
    {
        private readonly ILogger<QueueProcessor> _logger;
        private readonly IMyService _service;
    
        public QueueProcessor(ILogger<QueueProcessor> logger, IMyService service)
        {
            _logger = logger;
            _service = service;
        }
    
        [Function("ProcessQueueMessage")]
        public async Task Run(
            [QueueTrigger("myqueue-items", Connection = "AzureWebJobsStorage")]
            QueueMessage message)
        {
            _logger.LogInformation("Processing message: {Id}", message.MessageId);
    
            try
            {
                var payload = JsonSerializer.Deserialize<MyPayload>(message.Body);
                await _service.ProcessAsync(payload);
    
                _logger.LogInformation("Message processed successfully: {Id}", message.MessageId);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing message: {Id}", message.MessageId);
    
                // Message will be retried up to maxDequeueCount (default 5)
                // Then moved to poison queue: myqueue-items-poison
                throw;
            }
        }
    
        // Optional: Monitor poison queue
        [Function("ProcessPoisonQueue")]
        public async Task ProcessPoison(
            [QueueTrigger("myqueue-items-poison", Connection = "AzureWebJobsStorage")]
            QueueMessage message)
        {
            _logger.LogWarning("Processing poison message: {Id}", message.MessageId);
    
            // Log to monitoring, alert, or store for manual review
            await _service.HandlePoisonMessageAsync(message);
        }
    }
    
    // host.json - Queue configuration
    // {
    //   "version": "2.0",
    //   "extensions": {
    //     "queues": {
    //       "maxPollingInterval": "00:00:02",
    //       "visibilityTimeout": "00:00:30",
    //       "batchSize": 16,
    //       "maxDequeueCount": 5,
    //       "newBatchThreshold": 8
    //     }
    //   }
    // }
    
  #### **Notes**
    - Messages retried up to maxDequeueCount times
    - Failed messages moved to poison queue
    - Configure visibilityTimeout for processing time
    - batchSize controls parallel processing

---
  #### **Name**
HTTP Trigger with Long-Running Pattern
  #### **Description**
Handle work exceeding 230-second HTTP limit
  #### **When**
HTTP request triggers long-running work
  #### **Template**
    // Async HTTP pattern - return immediately, poll for status
    [Function("StartLongRunning")]
    public static async Task<HttpResponseData> StartLongRunning(
        [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
        [DurableClient] DurableTaskClient client,
        FunctionContext context)
    {
        var input = await req.ReadFromJsonAsync<WorkRequest>();
    
        // Start orchestration (returns immediately)
        string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
            "LongRunningOrchestrator", input);
    
        // Return status URLs for polling
        return client.CreateCheckStatusResponse(req, instanceId);
    }
    
    // Response includes:
    // {
    //   "id": "abc123",
    //   "statusQueryGetUri": "https://.../instances/abc123",
    //   "sendEventPostUri": "https://.../instances/abc123/raiseEvent/{eventName}",
    //   "terminatePostUri": "https://.../instances/abc123/terminate"
    // }
    
    // Alternative: Queue-based pattern without Durable Functions
    [Function("StartWork")]
    [QueueOutput("work-queue")]
    public static async Task<WorkItem> StartWork(
        [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
        FunctionContext context)
    {
        var input = await req.ReadFromJsonAsync<WorkRequest>();
        var workId = Guid.NewGuid().ToString();
    
        // Queue the work, return immediately
        var workItem = new WorkItem
        {
            Id = workId,
            Request = input
        };
    
        // Return work ID for status checking
        var response = req.CreateResponse(HttpStatusCode.Accepted);
        await response.WriteAsJsonAsync(new
        {
            workId = workId,
            statusUrl = $"/api/status/{workId}"
        });
    
        return workItem;
    }
    
    [Function("ProcessWork")]
    public static async Task ProcessWork(
        [QueueTrigger("work-queue")] WorkItem work,
        FunctionContext context)
    {
        // Long-running processing here
        // Update status in storage for polling
    }
    
  #### **Notes**
    - HTTP timeout is 230 seconds regardless of plan
    - Use Durable Functions for async patterns
    - Return immediately with status endpoint
    - Client polls for completion

## Anti-Patterns


---
  #### **Name**
Blocking Async Calls
  #### **Description**
Using .Result, .Wait(), or Thread.Sleep blocks threads
  #### **Instead**
Use await/async pattern with Task.Delay

---
  #### **Name**
New HttpClient Per Request
  #### **Description**
Creating HttpClient instances causes socket exhaustion
  #### **Instead**
Use IHttpClientFactory or static client with DI

---
  #### **Name**
In-Process Model for New Projects
  #### **Description**
In-process model deprecated in November 2026
  #### **Instead**
Use isolated worker model for .NET

---
  #### **Name**
Synchronous External Calls
  #### **Description**
Blocks threads, causes thread starvation
  #### **Instead**
Use async patterns for all I/O

---
  #### **Name**
Verbose Logging in Production
  #### **Description**
Excessive logging degrades performance
  #### **Instead**
Use appropriate log levels, structured logging