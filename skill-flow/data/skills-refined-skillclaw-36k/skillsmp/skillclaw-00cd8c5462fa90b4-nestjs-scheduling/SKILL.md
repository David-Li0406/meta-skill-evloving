---
name: nestjs-scheduling
description: Use this skill when you need to implement distributed cron jobs in a NestJS application while ensuring that tasks are executed only once in a multi-instance environment.
---

# Skill body

## Task Scheduling & Jobs

### Distributed Cron (Critical)

- **Problem**: `@Cron()` runs on **every** instance. In K8s with 3 pods, your "Daily Report" runs 3 times.
- **Solution**: **Distributed Locking** using Redis.
  - **Pattern**: Use a decorator to wrap the cron method.
  - **Logic**: `SET resource_name my_random_value NX PX 30000` (Redis Atomic Set).

### Cron Decorator Pattern

- **Implementation**:

  ```typescript
  @Cron(CronExpression.EVERY_MINUTE)
  @DistributedLock({ key: 'send_emails', ttl: 5000 })
  async handleCron() {
    // Only runs if lock acquired
  }
  ```

- **Tools**: Use `nestjs-redlock` or a custom Redis wrapper via the `redlock` library.

### Job Robustness

- **Isolation**: Never perform heavy processing inside the Cron handler.
  - **Pattern**: Cron -> Push Job ID to Queue (BullMQ) -> Worker processes it.
  - **Why**: Cron schedulers can get blocked by the Event Loop; Workers are scalable.
- **Error Handling**: Wrap ALL cron logic in `try/catch`. Uncaught exceptions in a Cron job can crash the entire Node process.