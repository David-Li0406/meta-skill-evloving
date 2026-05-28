# Workflow Automation

## Patterns


---
  #### **Name**
Sequential Workflow Pattern
  #### **Description**
Steps execute in order, each output becomes next input
  #### **When**
Content pipelines, data processing, ordered operations
  #### **Example**
    # SEQUENTIAL WORKFLOW:
    
    """
    Step 1 → Step 2 → Step 3 → Output
      ↓         ↓         ↓
    (checkpoint at each step)
    """
    
    ## Inngest Example (TypeScript)
    """
    import { inngest } from "./client";
    
    export const processOrder = inngest.createFunction(
      { id: "process-order" },
      { event: "order/created" },
      async ({ event, step }) => {
        // Step 1: Validate order
        const validated = await step.run("validate-order", async () => {
          return validateOrder(event.data.order);
        });
    
        // Step 2: Process payment (durable - survives crashes)
        const payment = await step.run("process-payment", async () => {
          return chargeCard(validated.paymentMethod, validated.total);
        });
    
        // Step 3: Create shipment
        const shipment = await step.run("create-shipment", async () => {
          return createShipment(validated.items, validated.address);
        });
    
        // Step 4: Send confirmation
        await step.run("send-confirmation", async () => {
          return sendEmail(validated.email, { payment, shipment });
        });
    
        return { success: true, orderId: event.data.orderId };
      }
    );
    """
    
    ## Temporal Example (TypeScript)
    """
    import { proxyActivities } from '@temporalio/workflow';
    import type * as activities from './activities';
    
    const { validateOrder, chargeCard, createShipment, sendEmail } =
      proxyActivities<typeof activities>({
        startToCloseTimeout: '30 seconds',
        retry: {
          maximumAttempts: 3,
          backoffCoefficient: 2,
        }
      });
    
    export async function processOrderWorkflow(order: Order): Promise<void> {
      const validated = await validateOrder(order);
      const payment = await chargeCard(validated.paymentMethod, validated.total);
      const shipment = await createShipment(validated.items, validated.address);
      await sendEmail(validated.email, { payment, shipment });
    }
    """
    
    ## n8n Pattern
    """
    [Webhook: order.created]
        ↓
    [HTTP Request: Validate Order]
        ↓
    [HTTP Request: Process Payment]
        ↓
    [HTTP Request: Create Shipment]
        ↓
    [Send Email: Confirmation]
    
    Configure each node with retry on failure.
    Use Error Trigger for dead letter handling.
    """
    

---
  #### **Name**
Parallel Workflow Pattern
  #### **Description**
Independent steps run simultaneously, aggregate results
  #### **When**
Multiple independent analyses, data from multiple sources
  #### **Example**
    # PARALLEL WORKFLOW:
    
    """
            ┌→ Step A ─┐
    Input ──┼→ Step B ─┼→ Aggregate → Output
            └→ Step C ─┘
    """
    
    ## Inngest Example
    """
    export const analyzeDocument = inngest.createFunction(
      { id: "analyze-document" },
      { event: "document/uploaded" },
      async ({ event, step }) => {
        // Run analyses in parallel
        const [security, performance, compliance] = await Promise.all([
          step.run("security-analysis", () =>
            analyzeForSecurityIssues(event.data.document)
          ),
          step.run("performance-analysis", () =>
            analyzeForPerformance(event.data.document)
          ),
          step.run("compliance-analysis", () =>
            analyzeForCompliance(event.data.document)
          ),
        ]);
    
        // Aggregate results
        const report = await step.run("generate-report", () =>
          generateReport({ security, performance, compliance })
        );
    
        return report;
      }
    );
    """
    
    ## AWS Step Functions (Amazon States Language)
    """
    {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "SecurityAnalysis",
          "States": {
            "SecurityAnalysis": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:...:security-analyzer",
              "End": true
            }
          }
        },
        {
          "StartAt": "PerformanceAnalysis",
          "States": {
            "PerformanceAnalysis": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:...:performance-analyzer",
              "End": true
            }
          }
        }
      ],
      "Next": "AggregateResults"
    }
    """
    

---
  #### **Name**
Orchestrator-Worker Pattern
  #### **Description**
Central coordinator dispatches work to specialized workers
  #### **When**
Complex tasks requiring different expertise, dynamic subtask creation
  #### **Example**
    # ORCHESTRATOR-WORKER PATTERN:
    
    """
    ┌─────────────────────────────────────┐
    │          ORCHESTRATOR               │
    │  - Analyzes task                    │
    │  - Creates subtasks                 │
    │  - Dispatches to workers            │
    │  - Aggregates results               │
    └─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    ┌───────┐  ┌───────┐  ┌───────┐
    │Worker1│  │Worker2│  │Worker3│
    │Create │  │Modify │  │Delete │
    └───────┘  └───────┘  └───────┘
    """
    
    ## Temporal Example
    """
    export async function orchestratorWorkflow(task: ComplexTask) {
      // Orchestrator decides what work needs to be done
      const plan = await analyzeTask(task);
    
      // Dispatch to specialized worker workflows
      const results = await Promise.all(
        plan.subtasks.map(subtask => {
          switch (subtask.type) {
            case 'create':
              return executeChild(createWorkerWorkflow, { args: [subtask] });
            case 'modify':
              return executeChild(modifyWorkerWorkflow, { args: [subtask] });
            case 'delete':
              return executeChild(deleteWorkerWorkflow, { args: [subtask] });
          }
        })
      );
    
      // Aggregate results
      return aggregateResults(results);
    }
    """
    
    ## Inngest with AI Orchestration
    """
    export const aiOrchestrator = inngest.createFunction(
      { id: "ai-orchestrator" },
      { event: "task/complex" },
      async ({ event, step }) => {
        // AI decides what needs to be done
        const plan = await step.run("create-plan", async () => {
          return await llm.chat({
            messages: [
              { role: "system", content: "Break this task into subtasks..." },
              { role: "user", content: event.data.task }
            ]
          });
        });
    
        // Execute each subtask as a durable step
        const results = [];
        for (const subtask of plan.subtasks) {
          const result = await step.run(`execute-${subtask.id}`, async () => {
            return executeSubtask(subtask);
          });
          results.push(result);
        }
    
        // Final synthesis
        return await step.run("synthesize", async () => {
          return synthesizeResults(results);
        });
      }
    );
    """
    

---
  #### **Name**
Event-Driven Trigger Pattern
  #### **Description**
Workflows triggered by events, not schedules
  #### **When**
Reactive systems, user actions, webhook integrations
  #### **Example**
    # EVENT-DRIVEN TRIGGERS:
    
    ## Inngest Event-Based
    """
    // Define events with TypeScript types
    type Events = {
      "user/signed.up": {
        data: { userId: string; email: string };
      };
      "order/completed": {
        data: { orderId: string; total: number };
      };
    };
    
    // Function triggered by event
    export const onboardUser = inngest.createFunction(
      { id: "onboard-user" },
      { event: "user/signed.up" },  // Trigger on this event
      async ({ event, step }) => {
        // Wait 1 hour, then send welcome email
        await step.sleep("wait-for-exploration", "1 hour");
    
        await step.run("send-welcome", async () => {
          return sendWelcomeEmail(event.data.email);
        });
    
        // Wait 3 days for engagement check
        await step.sleep("wait-for-engagement", "3 days");
    
        const engaged = await step.run("check-engagement", async () => {
          return checkUserEngagement(event.data.userId);
        });
    
        if (!engaged) {
          await step.run("send-nudge", async () => {
            return sendNudgeEmail(event.data.email);
          });
        }
      }
    );
    
    // Send events from anywhere
    await inngest.send({
      name: "user/signed.up",
      data: { userId: "123", email: "user@example.com" }
    });
    """
    
    ## n8n Webhook Trigger
    """
    [Webhook: POST /api/webhooks/order]
        ↓
    [Switch: event.type]
        ↓ order.created
    [Process New Order Subworkflow]
        ↓ order.cancelled
    [Handle Cancellation Subworkflow]
    """
    

---
  #### **Name**
Retry and Recovery Pattern
  #### **Description**
Automatic retry with backoff, dead letter handling
  #### **When**
Any workflow with external dependencies
  #### **Example**
    # RETRY AND RECOVERY:
    
    ## Temporal Retry Configuration
    """
    const activities = proxyActivities<typeof activitiesType>({
      startToCloseTimeout: '30 seconds',
      retry: {
        initialInterval: '1 second',
        backoffCoefficient: 2,
        maximumInterval: '1 minute',
        maximumAttempts: 5,
        nonRetryableErrorTypes: [
          'ValidationError',      // Don't retry validation failures
          'InsufficientFunds',    // Don't retry payment failures
        ]
      }
    });
    """
    
    ## Inngest Retry Configuration
    """
    export const processPayment = inngest.createFunction(
      {
        id: "process-payment",
        retries: 5,  // Retry up to 5 times
      },
      { event: "payment/initiated" },
      async ({ event, step, attempt }) => {
        // attempt is 0-indexed retry count
    
        const result = await step.run("charge-card", async () => {
          try {
            return await stripe.charges.create({...});
          } catch (error) {
            if (error.code === 'card_declined') {
              // Don't retry card declines
              throw new NonRetriableError("Card declined");
            }
            throw error;  // Retry other errors
          }
        });
    
        return result;
      }
    );
    """
    
    ## Dead Letter Handling
    """
    // n8n: Use Error Trigger node
    [Error Trigger]
        ↓
    [Log to Error Database]
        ↓
    [Send Alert to Slack]
        ↓
    [Create Ticket in Jira]
    
    // Inngest: Handle in onFailure
    export const myFunction = inngest.createFunction(
      {
        id: "my-function",
        onFailure: async ({ error, event, step }) => {
          await step.run("alert-team", async () => {
            await slack.postMessage({
              channel: "#errors",
              text: `Function failed: ${error.message}`
            });
          });
        }
      },
      { event: "..." },
      async ({ step }) => { ... }
    );
    """
    

---
  #### **Name**
Scheduled Workflow Pattern
  #### **Description**
Time-based triggers for recurring tasks
  #### **When**
Daily reports, periodic sync, batch processing
  #### **Example**
    # SCHEDULED WORKFLOWS:
    
    ## Inngest Cron
    """
    export const dailyReport = inngest.createFunction(
      { id: "daily-report" },
      { cron: "0 9 * * *" },  // Every day at 9 AM
      async ({ step }) => {
        const data = await step.run("gather-metrics", async () => {
          return gatherDailyMetrics();
        });
    
        await step.run("generate-report", async () => {
          return generateAndSendReport(data);
        });
      }
    );
    
    export const syncInventory = inngest.createFunction(
      { id: "sync-inventory" },
      { cron: "*/15 * * * *" },  // Every 15 minutes
      async ({ step }) => {
        await step.run("sync", async () => {
          return syncWithSupplier();
        });
      }
    );
    """
    
    ## Temporal Cron Workflow
    """
    // Schedule workflow to run on cron
    const handle = await client.workflow.start(dailyReportWorkflow, {
      taskQueue: 'reports',
      workflowId: 'daily-report',
      cronSchedule: '0 9 * * *',  // 9 AM daily
    });
    """
    
    ## n8n Schedule Trigger
    """
    [Schedule Trigger: Every day at 9:00 AM]
        ↓
    [HTTP Request: Get Metrics]
        ↓
    [Code Node: Generate Report]
        ↓
    [Send Email: Report]
    """
    

## Anti-Patterns


---
  #### **Name**
No Durable Execution for Payments
  #### **Description**
Processing payments without crash recovery
  #### **Why**
    A network hiccup during payment processing can result in charged
    card but no order, or order but no charge. Without durability,
    you can't recover to a consistent state.
    
  #### **Instead**
    Use durable execution (Temporal, Inngest, or AWS Step Functions).
    Each step is checkpointed. Crashes resume from last successful step.
    

---
  #### **Name**
Monolithic Workflows
  #### **Description**
Single huge workflow doing everything
  #### **Why**
    Hard to debug, hard to modify, hard to test. When one part fails,
    the whole workflow fails. Can't reuse pieces across workflows.
    
  #### **Instead**
    Break into focused functions. Use child workflows or subworkflows.
    Each workflow should do one thing well.
    

---
  #### **Name**
No Observability
  #### **Description**
Workflows running without visibility into state
  #### **Why**
    When something fails at 3 AM, you need to know which step failed,
    what the inputs were, and why. Without observability, debugging
    is guesswork.
    
  #### **Instead**
    All platforms provide dashboards. Use them. Add custom logging
    at step boundaries. Track execution time, success rate, error types.
    

---
  #### **Name**
Retry Without Backoff
  #### **Description**
Immediate retries on transient failures
  #### **Why**
    If a service is overloaded, hammering it with retries makes it
    worse. You'll get rate limited or cause cascading failures.
    
  #### **Instead**
    Exponential backoff with jitter. Start at 1 second, double each
    time, max at 1-5 minutes. Add randomness to prevent thundering herd.
    

---
  #### **Name**
No Dead Letter Handling
  #### **Description**
Failed workflows disappear into the void
  #### **Why**
    Without dead letter handling, failed workflows are just logged
    and forgotten. Problems accumulate. Users don't get retried.
    
  #### **Instead**
    Dead letter queue or failure handler. Alert on failures.
    Manual review or automatic re-queue after fix.
    

---
  #### **Name**
Synchronous Everything
  #### **Description**
Calling workflows synchronously and waiting
  #### **Why**
    Defeats the purpose of workflow automation. Caller blocks,
    timeouts occur, user experience suffers. Doesn't scale.
    
  #### **Instead**
    Fire-and-forget with callback. Return immediately with job ID.
    Client polls or receives webhook when complete.
    