---
name: monitor-api
description: Use this skill when you need to continuously track web changes relevant to specific queries and receive updates on a scheduled basis.
---

# Skill body

The Monitor API allows you to track the web for changes based on your specified queries. You can set up monitors to run on a schedule (hourly, daily, or weekly) and receive webhook notifications when changes are detected.

## Features

- **Scheduling**: Choose how often you want to receive updates (Hourly, Daily, Weekly).
- **Webhooks**: Get notified when events are detected or when monitors complete their scheduled runs.
- **Event History**: Access updates from recent runs or specify a lookback window (e.g., `10d`).
- **Lifecycle Management**: Modify the cadence, webhook, or metadata of your monitors, or delete them to stop future runs.
- **Structured Outputs**: Receive events in JSON format that conforms to your specified schema.

## Common Use Cases

| Use Case              | Example Query                                                       |
| --------------------- | ------------------------------------------------------------------- |
| News tracking         | "What is the latest AI funding news?"                               |
| Brand mentions        | "Let me know when someone mentions Parallel Web Systems on the web" |
| Product announcements  | "Alert me when Apple announces new MacBook models"                 |
| Regulatory updates     | "Notify me of any new FDA guidance on AI in medical devices"       |
| Price monitoring       | "Let me know when the price for AirPods drops below $150"         |
| Stock availability     | "Alert me when the PS5 Pro is back in stock at Best Buy"          |

## Getting Started

1. **Create a Monitor**: Define your query in natural language.
2. **Set the Schedule**: Choose how frequently you want to receive updates.
3. **Configure Webhooks**: Specify where notifications should be sent.
4. **Manage Monitors**: Update or delete monitors as needed.

**Note**: The Monitor API is currently in public alpha, and endpoints or request/response formats may change.