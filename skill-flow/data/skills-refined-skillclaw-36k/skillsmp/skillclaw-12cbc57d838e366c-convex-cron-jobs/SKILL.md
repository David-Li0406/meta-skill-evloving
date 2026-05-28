---
name: convex-cron-jobs
description: Use this skill when you need to schedule recurring functions for background tasks, including interval scheduling, cron expressions, job monitoring, and retry strategies in Convex applications.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Cron Jobs Documentation](https://docs.convex.dev/scheduling/cron-jobs)
- Scheduling Overview: [Scheduling Overview](https://docs.convex.dev/scheduling)
- Scheduled Functions: [Scheduled Functions](https://docs.convex.dev/scheduling/scheduled-functions)
- For broader context: [LLMs Context](https://docs.convex.dev/llms.txt)

## Instructions

### Cron Jobs Overview

Convex cron jobs allow you to schedule functions to run at regular intervals or specific times. Key features include:

- Running functions on a fixed schedule
- Supporting interval-based and cron expression scheduling
- Automatic retries on failure
- Monitoring via the Convex dashboard

### Basic Cron Setup

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Run every hour
crons.interval(
  "cleanup expired sessions",
  { hours: 1 },
  internal.tasks.cleanupExpiredSessions,
  {}
);

// Run every day at midnight UTC
crons.cron(
  "daily report",
  "0 0 * * *",
  internal.reports.generateDailyReport,
  {}
);

export default crons;
```

### Interval-Based Scheduling

Use `crons.interval` for simple recurring tasks:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Every 5 minutes
crons.interval(
  "sync external data",
  { minutes: 5 },
  internal.sync.fetchExternalData,
  {}
);

// Every 2 hours
crons.interval(
  "cleanup temp files",
  { hours: 2 },
  internal.files.cleanupTempFiles,
  {}
);

// Every 30 seconds (minimum interval)
crons.interval(
  "health check",
  { seconds: 30 },
  internal.monitoring.healthCheck,
  {}
);

export default crons;
```

### Cron Expression Scheduling

Use `crons.cron` for precise scheduling with cron expressions:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Every day at 9 AM UTC
crons.cron(
  "morning notification",
  "0 9 * * *",
  internal.notifications.sendMorningNotification,
  {}
);

export default crons;
```