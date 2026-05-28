---
name: nestjs-scheduling
description: Use this skill for implementing distributed cron jobs and locking patterns in NestJS applications.
---

# Task Scheduling & Jobs

## Distributed Cron (Critical)

- **Problem**: `@Cron()` runs on **every** instance. In K8s with multiple pods, your scheduled tasks may execute multiple times.
- **Solution**: **Distributed Locking** using Redis.
  - **Pattern**: Use a decorator to wrap the cron method.
  - **Logic**: `SET resource_name my_random_value NX PX 30000` (Redis Atomic Set).

## Cron Decorator Pattern

- **Implementation**:

  ```typescript
  @Cron(CronExpression.EVERY_MINUTE)
  @DistributedLock({ key: 'send_emails', ttl: 5000 })
  async handleCron() {
    // Only runs if lock acquired
  }
  ```

- **Tools**: Utilize `nestjs-redlock` or a custom Redis wrapper via the `redlock` library.

## Job Robustness

- **Isolation**: Avoid heavy processing inside the Cron handler.
  - **Pattern**: Cron -> Push Job ID to Queue (BullMQ) -> Worker processes it.
  - **Why**: Cron schedulers can block the Event Loop; Workers are scalable.
- **Error Handling**: Always wrap cron logic in `try/catch`. Uncaught exceptions in a Cron job can crash the entire Node process.