---
name: monitor-api
description: Use this skill when building applications with the Parallel Monitor API to track web changes based on specified queries and schedules.
---

# Monitor API Complete Reference

> Track web changes continuously with scheduled queries and webhook notifications.

The Monitor API lets you continuously track the web for changes relevant to a query, on a schedule you control. Create a monitor with a natural-language query, choose a cadence (hourly, daily, weekly), and receive webhook notifications when changes are detected.

<Note>
  **Alpha Notice**: The Monitor API is currently in public alpha. Endpoints and request/response formats are subject to change.
</Note>

## Table of Contents

- [Features and Use Cases](#features-and-use-cases)
- [Getting Started](#getting-started)
- [Creating Monitors](#creating-monitors)
- [Events and Event Groups](#events-and-event-groups)
- [Webhooks](#webhooks)
- [Structured Outputs](#structured-outputs)
- [Testing with Simulate Event](#testing-with-simulate-event)
- [Managing Monitors](#managing-monitors)
- [Slack Integration](#slack-integration)
- [Best Practices](#best-practices)

## Features and Use Cases

The Monitor API automates continuous research for any topic, including companies, products, or regulatory areas—without building complicated web monitoring infrastructure. Define a query once along with the desired schedule, and the service will detect relevant changes and deliver concise updates (with source links) to your systems via webhooks.

**Current Features:**

- **Scheduling**: Set update cadence to Hourly, Daily, or Weekly
- **Webhooks**: Receive updates when events are detected or when monitors finish a scheduled run
- **Events history**: Retrieve updates from recent runs or via a lookback window (e.g., `10d`)
- **Lifecycle management**: Update cadence, webhook, or metadata; delete to stop future runs
- **Structured outputs**: Return events as JSON conforming to your schema

**Common Use Cases:**

| Use Case              | Example Query                                                       |
| --------------------- | ------------------------------------------------------------------- |
| News tracking         | "What is the latest AI funding news?"                               |
| Brand mentions        | "Let me know when someone mentions Parallel Web Systems on the web" |
| Product announcements | "Alert me when Apple announces new MacBook models"                  |
| Regulatory updates    | "Notify me of any new FDA guidance on AI in medical devices"        |
| Price monitoring      | "Let me know when the price for AirPods drops below $150"           |
| Stock availability    | "Alert me when the PS5 Pro is back in stock at Best Buy"            |
| Content updates       | "Notify me when the React documentation is updated"                 |
| Policy changes        | "Track changes to OpenAI's terms of service"                        |

## Getting Started

### Prerequisites

Generate your API key on [Platform](https://platform.parallel.ai), then set it in your shell:

```bash
export PARALLEL_API_KEY="PARALLEL_API_KEY"
```

### Quick Example

Create a monitor that gathers daily AI news:

```bash
curl --request POST \
  --url https://api.parallel.ai/v1alpha/monitors \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $PARALLEL_API_KEY" \
  --data '{
    "query": "Extract recent news about quantum in AI",
    "cadence": "daily",
    "webhook": {
      "url": "https://example.com/webhook",
      "event_types": ["monitor.event.detected"]
    },
    "metadata": { "key": "value" }
  }'
```

**Response:**

```json
{
  "monitor_id": "monitor_b0079f70195e4258a3b982c1b6d8bd3a",
  "query": "Extract recent news about quantum in AI",
  "status": "active",
  "cadence": "daily",
  "metadata": { "key": "value" },
  "webhook": {
    "url": "https://example.com/webhook",
    "event_types": ["monitor.event.detected"]
  },
  "created_at": "2025-04-23T20:21:48.037943Z"
}
```

## Creating Monitors

### POST /v1alpha/monitors

Creates a monitor that periodically runs the specified query over the web at the specified cadence (hourly, daily, or weekly). The monitor runs once at creation and then continues according to the specified frequency.

**Request Body:**

| Parameter       | Type           | Required | Description                                                                                                                                                                                                                                                                                                |
| --------------- | -------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `query`         | string         | Yes      | Search query to monitor for material changes.                                                                                                                                                                                                                                                              |
| `cadence`       | string         | Yes      | Cadence of the monitor. One of: `daily`, `weekly`, `hourly`                                                                                                                                                                                                                                                |
| `webhook`       | object \| null | No       | Webhook to receive notifications about the monitor's execution.                                                                                                                                                                                                                                            |
| `metadata`      | object \| null | No       | User-provided metadata stored with the monitor. This field is returned in webhook notifications and GET requests, enabling you to map responses to corresponding objects in your application. For example, if you are building a Slackbot that monitors changes, you could store the Slack thread ID here. |
| `output_schema` | object \| null | No       | Output schema for the monitor event. See [Structured Outputs](#structured-outputs).                                                                                                                                                                                                                        |

**Webhook Object:**

| Parameter     | Type           | Required | Description                                                                               |
| ------------- | -------------- | -------- | ----------------------------------------------------------------------------------------- |
| `url`         | string         | Yes      | URL for the webhook.                                                                      |
| `event_types` | array\[string] | No       | Event types to send webhook notifications for. See [Webhooks](#webhooks) for event types. |

**Response:**

Returns a `MonitorResponse` object with status code `201`.

## Events and Event Groups

Monitors produce a stream of events each time they run. These events capture:

- new results detected by your query (events)
- run completions
- errors (if a run fails)

Related events are grouped by an `event_group_id` so you can fetch the full set of results that belong to the same discovery.

### Event Groups

Event groups collect related results under a single `event_group_id`. When a monitor detects new results, it creates an event group. Subsequent runs can add additional events to the same group if they're related to the same discovery.

Use event groups to present the full context of a discovery (multiple sources, follow-up updates) as one unit.

### Event Types

Besides events with new results, monitors emit:

- **Event** (`type: "event"`): indicates a material change was detected
- **Completion** (`type: "completion"`): indicates a run finished successfully without detected events
- **Error** (`type: "error"`): indicates a run failed

### Accessing Events

You can receive events via webhooks (recommended) or retrieve them via endpoints.

- **Webhooks (recommended)**: lowest latency, push-based delivery. Subscribe to `monitor.event.detected`, `monitor.execution.completed`, and `monitor.execution.failed`.
- **Endpoints (for history/backfill)**:
  - `GET /v1alpha/monitors/{monitor_id}/events` — list events for a monitor in reverse chronological order (up to recent ~300 runs). This flattens out events, meaning that multiple events from the same event group will be listed as different events.
  - `GET /v1alpha/monitors/{monitor_id}/event_groups/{event_group_id}` - list all events given an `event_group_id`.

## Webhooks

Webhooks allow you to receive real-time notifications when a Monitor execution completes, fails, or when material events are detected, eliminating the need for polling.

### Setup

To register a webhook for a Monitor, include a `webhook` parameter when creating the monitor:

```bash
curl --request POST \
  --url https://api.parallel.ai/v1alpha/monitors \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $PARALLEL_API_KEY" \
  --data '{
    "query": "Extract recent news about AI",
    "cadence": "daily",
    "webhook": {
      "url": "https://your-domain.com/webhooks/monitor",
      "event_types": [
        "monitor.event.detected",
        "monitor.execution.completed",
        "monitor.execution.failed"
      ]
    },
    "metadata": { "team": "research" }
  }'
```

### Event Types

Monitors support the following webhook event types:

| Event Type                    | Description                                                                  |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `monitor.event.detected`      | Emitted when a run detects one or more material events.                      |
| `monitor.execution.completed` | Emitted when a Monitor run completes successfully (without detected events). |
| `monitor.execution.failed`    | Emitted when a Monitor run fails due to an error.                            |

### Webhook Payload Structure

For Monitor webhooks, the `data` object contains:

- `monitor_id`: The unique ID of the Monitor
- `event`: The event record for this run
- `metadata`: User-provided metadata from the Monitor (if any)

## Structured Outputs

Structured outputs enable you to define a JSON schema for monitor events. Each detected event conforms to the specified schema, returning data in a consistent, machine-readable format suitable for downstream processing in databases, analytics pipelines, or automation workflows.

### Defining an Output Schema

Include an `output_schema` field when creating a monitor:

```bash
curl --request POST \
  --url https://api.parallel.ai/v1alpha/monitors \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $PARALLEL_API_KEY" \
  --data '{
    "query": "monitor ai news",
    "cadence": "daily",
    "output_schema": {
      "type": "json",
      "json_schema": {
        "type": "object",
        "properties": {
          "company_name": {
            "type": "string",
            "description": "Name of the company the news is about, NA if not company-specific"
          },
          "sentiment": {
            "type": "string",
            "description": "Sentiment of the news: positive or negative"
          },
          "description": {
            "type": "string",
            "description": "Brief description of the news"
          }
        }
      }
    }
  }'
```

### Retrieving Structured Events

Events from monitors configured with structured outputs include a `result` field containing the parsed JSON object.

## Testing with Simulate Event

The simulate event endpoint allows you to test your webhook integration without waiting for a scheduled monitor run.

### POST /v1alpha/monitors/{monitor_id}/simulate_event

**Path Parameters:**

| Parameter    | Type   | Required | Description       |
| ------------ | ------ | -------- | ----------------- |
| `monitor_id` | string | Yes      | ID of the monitor |

**Query Parameters:**

| Parameter    | Type   | Default                  | Description                                                                                                         |
| ------------ | ------ | ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| `event_type` | string | `monitor.event.detected` | Event type to simulate. One of: `monitor.event.detected`, `monitor.execution.completed`, `monitor.execution.failed` |

**Response:**

Returns `204 No Content` on success.

## Managing Monitors

### GET /v1alpha/monitors

List all monitors for your account.

### GET /v1alpha/monitors/{monitor_id}

Retrieve a specific monitor by ID.

### PATCH /v1alpha/monitors/{monitor_id}

Update a monitor's configuration. You can update the cadence, webhook, and metadata.

### DELETE /v1alpha/monitors/{monitor_id}

Delete a monitor, stopping all future executions. Deleted monitors can no longer be updated or retrieved.

## Slack Integration

The Parallel Slack app brings Monitor directly into your Slack workspace. Create monitors with slash commands and receive updates in dedicated threads.

### Installation

1. Go to [platform.parallel.ai](https://platform.parallel.ai) and navigate to the Integrations section
2. Click **Add to Slack** to begin the OAuth flow
3. Authorize the Parallel app in your workspace
4. Invite the bot to any channel where you want to use monitoring: `/invite @Parallel`

### Commands

- `/monitor <query>` - Create a daily monitor
- `/hourly <query>` - Create an hourly monitor
- `/help` - View available commands
- Reply with `cancelmonitor` in a monitoring thread to cancel

## Best Practices

### Scope Your Query

Clear queries with explicit instructions lead to higher-quality event detection. Monitor works best with natural language queries that clearly describe what you're looking for.

### Choose the Right Cadence

- Use `hourly` for fast-moving topics
- Use `daily` for most news
- Use `weekly` for slower changes

### Use for Current Events, Not Historical Research

**Don't use for historical research**: Monitor is designed to track _new_ updates as they happen, not to retrieve past news.

### Don't Include Dates

Monitor automatically tracks updates from when it's created. Adding specific dates to your query is unnecessary and can cause confusion.

### Prefer Webhooks

Use webhooks to avoid unnecessary polling and reduce latency to updates. This is especially important for hourly and daily monitors.

### Manage Lifecycle

Cancel monitors you no longer need to reduce your usage bills.

## Rate Limits

See [Rate Limits](/resources/rate-limits) for default quotas and how to request higher limits.

## Pricing

<Note>
  See [Pricing](/pricing) for a detailed schedule of rates.
</Note>

---
> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.parallel.ai/llms.txt